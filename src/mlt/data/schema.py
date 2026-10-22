"""Canonical candle schema shared by research, backtest and live.

Every provider converts to this schema. Venue-specific extra columns are allowed
but must never be used by a deployed model (they would not exist for every venue).
"""
from __future__ import annotations

import pandas as pd

CANDLE_COLUMNS = ["open", "high", "low", "close", "volume"]
_UNIT_MS = {"m": 60_000, "h": 3_600_000, "d": 86_400_000}


def interval_to_ms(interval: str) -> int:
    """'1h' -> 3_600_000. Raises ValueError on unsupported input."""
    if len(interval) < 2 or interval[-1] not in _UNIT_MS or not interval[:-1].isdigit():
        raise ValueError(f"Unsupported interval: {interval!r}")
    n = int(interval[:-1])
    if n <= 0:
        raise ValueError(f"Unsupported interval: {interval!r}")
    return n * _UNIT_MS[interval[-1]]


def validate_candles(df: pd.DataFrame, interval: str | None = None) -> pd.DataFrame:
    """Validate a candle frame. Returns it unchanged if valid, otherwise raises ValueError.

    Rules: UTC DatetimeIndex (candle CLOSE time), sorted, unique, required columns,
    finite positive prices, high >= low. If `interval` is given, also checks spacing
    and reports gaps (no silent filling).
    """
    if not isinstance(df.index, pd.DatetimeIndex) or df.index.tz is None:
        raise ValueError("index must be a timezone-aware (UTC) DatetimeIndex")
    if str(df.index.tz) != "UTC":
        raise ValueError("index timezone must be UTC")
    missing = [c for c in CANDLE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    if not df.index.is_monotonic_increasing:
        raise ValueError("index must be sorted ascending")
    if df.index.has_duplicates:
        raise ValueError("index contains duplicate timestamps")
    prices = df[["open", "high", "low", "close"]]
    if not prices.notna().all().all() or (prices <= 0).any().any():
        raise ValueError("prices must be finite and positive")
    if (df["high"] < df["low"]).any():
        raise ValueError("found candle with high < low")
    if interval is not None and len(df) > 1:
        step = pd.Timedelta(milliseconds=interval_to_ms(interval))
        gaps = df.index.to_series().diff().dropna()
        bad = gaps[gaps != step]
        if len(bad):
            raise ValueError(f"{len(bad)} irregular gap(s) in index, first at {bad.index[0]}")
    return df


def drop_unclosed(df: pd.DataFrame, now: pd.Timestamp) -> pd.DataFrame:
    """Keep only candles whose close time is strictly before `now` (causality guard)."""
    return df[df.index < now]
