"""Deribit provider: PUBLIC market data only (no API key, no account, no orders).

Endpoints used (Deribit API v2, HTTP GET):
- public/get_tradingview_chart_data  -> OHLCV candles (ticks are candle OPEN times)
- public/get_funding_rate_history    -> hourly funding observations (perpetuals)
- public/get_instrument              -> contract specification

Data terms: Deribit's Terms of Service allow market data for personal use only (see
docs/evidence E34). Keep the cache private; never publish or redistribute it.
"""
from __future__ import annotations

import time
from collections.abc import Callable

import pandas as pd
import requests

from mlt.data.schema import CANDLE_COLUMNS, drop_unclosed, interval_to_ms, validate_candles

BASE_URL = "https://www.deribit.com/api/v2"

# Deribit chart resolutions (minutes, or "1D") keyed by our interval strings.
RESOLUTIONS = {
    "1m": "1", "3m": "3", "5m": "5", "10m": "10", "15m": "15", "30m": "30",
    "1h": "60", "2h": "120", "3h": "180", "6h": "360", "12h": "720", "1d": "1D",
}  # fmt: skip

FUNDING_COLUMNS = ["interest_1h", "interest_8h", "index_price", "prev_index_price"]


class DeribitError(RuntimeError):
    """The API returned an error payload or kept failing after retries."""


def _ms(ts: pd.Timestamp) -> int:
    if ts.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware (UTC)")
    return int(ts.tz_convert("UTC").value // 1_000_000)


def _empty_candles() -> pd.DataFrame:
    idx = pd.DatetimeIndex([], tz="UTC", name="close_time")
    return pd.DataFrame({c: pd.Series(dtype="float64") for c in CANDLE_COLUMNS}, index=idx)


class DeribitProvider:
    name = "deribit"

    def __init__(
        self,
        session: requests.Session | None = None,
        base_url: str = BASE_URL,
        max_bars: int = 1000,
        funding_window_days: int = 30,
        min_interval_s: float = 0.25,
        retries: int = 3,
        backoff_s: float = 1.0,
        timeout_s: float = 30.0,
        sleep: Callable[[float], None] = time.sleep,
        now: Callable[[], pd.Timestamp] | None = None,
    ) -> None:
        self.session = session or requests.Session()
        self.base_url = base_url.rstrip("/")
        self.max_bars = max_bars
        self.funding_window_days = funding_window_days
        self.min_interval_s = min_interval_s
        self.retries = retries
        self.backoff_s = backoff_s
        self.timeout_s = timeout_s
        self._sleep = sleep
        self._now = now or (lambda: pd.Timestamp.now(tz="UTC"))
        self._last_call = 0.0

    # ------------------------------------------------------------------ transport
    def _throttle(self) -> None:
        wait = self.min_interval_s - (time.monotonic() - self._last_call)
        if wait > 0:
            self._sleep(wait)
        self._last_call = time.monotonic()

    def _get(self, method: str, params: dict) -> dict | list:
        url = f"{self.base_url}/{method}"
        last: Exception | None = None
        for attempt in range(self.retries + 1):
            self._throttle()
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout_s)
            except requests.RequestException as exc:
                last = exc
            else:
                if resp.status_code == 200:
                    body = resp.json()
                    if "error" in body:
                        raise DeribitError(f"{method}: {body['error']}")
                    return body["result"]
                if resp.status_code == 429 or resp.status_code >= 500:
                    last = DeribitError(f"{method}: HTTP {resp.status_code}")
                else:
                    raise DeribitError(f"{method}: HTTP {resp.status_code}: {resp.text[:200]}")
            self._sleep(self.backoff_s * 2**attempt)
        raise DeribitError(f"{method} failed after {self.retries + 1} attempts: {last}")

    # ------------------------------------------------------------------ public API
    def get_instrument(self, instrument: str) -> dict:
        """Contract specification (size, tick, settlement, fees ...). Compare with the venue."""
        result = self._get("public/get_instrument", {"instrument_name": instrument})
        assert isinstance(result, dict)
        return result

    def get_candles(
        self, instrument: str, interval: str, start: pd.Timestamp, end: pd.Timestamp
    ) -> pd.DataFrame:
        if interval not in RESOLUTIONS:
            raise ValueError(f"Unsupported interval for Deribit: {interval!r}")
        step_ms = interval_to_ms(interval)
        step = pd.Timedelta(milliseconds=step_ms)
        start_ms, end_ms = _ms(start), _ms(end)
        if end_ms <= start_ms:
            return _empty_candles()

        frames = []
        t = -(-start_ms // step_ms) * step_ms  # first grid-aligned open time >= start
        span = self.max_bars * step_ms
        while t < end_ms:
            result = self._get(
                "public/get_tradingview_chart_data",
                {
                    "instrument_name": instrument,
                    "start_timestamp": t,
                    "end_timestamp": min(t + span - 1, end_ms),
                    "resolution": RESOLUTIONS[interval],
                },
            )
            frames.append(self._parse_chart(result, step_ms))
            t += span

        frames = [f for f in frames if len(f)]
        if not frames:
            return _empty_candles()
        df = pd.concat(frames).sort_index()
        df = df[~df.index.duplicated(keep="last")]
        df = df[((df.index - step) >= start) & (df.index <= end)]
        df = drop_unclosed(df, self._now())
        return validate_candles(df)

    def get_funding(
        self, instrument: str, start: pd.Timestamp, end: pd.Timestamp
    ) -> pd.DataFrame:
        start_ms, end_ms = _ms(start), _ms(end)
        window = self.funding_window_days * 86_400_000
        rows: list[dict] = []
        t = start_ms
        while t < end_ms:
            result = self._get(
                "public/get_funding_rate_history",
                {
                    "instrument_name": instrument,
                    "start_timestamp": t,
                    "end_timestamp": min(t + window - 1, end_ms),
                },
            )
            rows.extend(result)  # type: ignore[arg-type]
            t += window
        idx = pd.DatetimeIndex([], tz="UTC", name="timestamp")
        if not rows:
            return pd.DataFrame({c: pd.Series(dtype="float64") for c in FUNDING_COLUMNS}, index=idx)
        df = pd.DataFrame(rows)
        df.index = pd.to_datetime(df.pop("timestamp"), unit="ms", utc=True)
        df.index.name = "timestamp"
        df = df.reindex(columns=FUNDING_COLUMNS).astype("float64").sort_index()
        return df[~df.index.duplicated(keep="last")]

    # ------------------------------------------------------------------ parsing
    @staticmethod
    def _parse_chart(result: dict, step_ms: int) -> pd.DataFrame:
        if result.get("status") == "no_data" or not result.get("ticks"):
            return _empty_candles()
        ticks = result["ticks"]
        cols = {c: result[c] for c in CANDLE_COLUMNS}
        if any(len(v) != len(ticks) for v in cols.values()):
            raise DeribitError("chart arrays have different lengths")
        # Deribit ticks are candle OPEN times; the canonical schema indexes by CLOSE time.
        idx = pd.to_datetime([t + step_ms for t in ticks], unit="ms", utc=True)
        df = pd.DataFrame(cols, index=idx).astype("float64")
        df.index.name = "close_time"
        return df
