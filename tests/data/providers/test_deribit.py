import pandas as pd
import pytest

from mlt.data.providers.deribit import DeribitError, DeribitProvider

H = 3_600_000
T0 = pd.Timestamp("2024-01-01", tz="UTC")
T0_MS = int(T0.value // 1_000_000)


class Resp:
    def __init__(self, status=200, body=None):
        self.status_code = status
        self._body = body if body is not None else {}
        self.text = str(self._body)

    def json(self):
        return self._body


class FakeSession:
    """Serves hourly candles for any requested window and records the calls."""

    def __init__(self, script=None):
        self.calls = []
        self.script = list(script or [])

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, dict(params)))
        if self.script:
            return self.script.pop(0)
        if url.endswith("get_tradingview_chart_data"):
            lo, hi = params["start_timestamp"], params["end_timestamp"]
            ticks = list(range(lo, hi + 1, H))
            n = len(ticks)
            return Resp(200, {"result": {
                "status": "ok", "ticks": ticks, "open": [100.0] * n, "high": [101.0] * n,
                "low": [99.0] * n, "close": [100.5] * n, "volume": [2.0] * n,
            }})
        raise AssertionError(url)


def provider(session, **kw):
    kw.setdefault("sleep", lambda s: None)
    kw.setdefault("min_interval_s", 0)
    kw.setdefault("now", lambda: pd.Timestamp("2030-01-01", tz="UTC"))
    return DeribitProvider(session=session, **kw)


def test_candles_are_indexed_by_close_time():
    p = provider(FakeSession())
    df = p.get_candles("BTC_USDC-PERPETUAL", "1h", T0, T0 + pd.Timedelta(hours=3))
    assert list(df.index) == [T0 + pd.Timedelta(hours=h) for h in (1, 2, 3)]
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]


def test_pagination_splits_requests_and_dedupes():
    s = FakeSession()
    p = provider(s, max_bars=10)
    df = p.get_candles("X", "1h", T0, T0 + pd.Timedelta(hours=25))
    assert len(s.calls) == 3
    assert len(df) == 25
    assert df.index.is_unique and df.index.is_monotonic_increasing


def test_unclosed_candle_is_dropped():
    now = T0 + pd.Timedelta(hours=2, minutes=30)
    p = provider(FakeSession(), now=lambda: now)
    df = p.get_candles("X", "1h", T0, T0 + pd.Timedelta(hours=5))
    assert df.index.max() < now
    assert len(df) == 2


def test_error_payload_raises():
    s = FakeSession([Resp(200, {"error": {"code": 13009, "message": "bad"}})])
    with pytest.raises(DeribitError):
        provider(s).get_candles("X", "1h", T0, T0 + pd.Timedelta(hours=2))


def test_retries_on_server_error_then_succeeds():
    ok = Resp(200, {"result": {"status": "no_data"}})
    s = FakeSession([Resp(503), Resp(429), ok])
    df = provider(s).get_candles("X", "1h", T0, T0 + pd.Timedelta(hours=2))
    assert len(s.calls) == 3
    assert df.empty


def test_gives_up_after_retries():
    s = FakeSession([Resp(500)] * 10)
    with pytest.raises(DeribitError):
        provider(s, retries=2).get_candles("X", "1h", T0, T0 + pd.Timedelta(hours=2))
    assert len(s.calls) == 3


def test_client_error_is_not_retried():
    s = FakeSession([Resp(400, {"x": 1})])
    with pytest.raises(DeribitError):
        provider(s).get_candles("X", "1h", T0, T0 + pd.Timedelta(hours=2))
    assert len(s.calls) == 1


def test_naive_timestamps_rejected():
    with pytest.raises(ValueError):
        provider(FakeSession()).get_candles("X", "1h", pd.Timestamp("2024-01-01"), T0)


def test_unsupported_interval_rejected():
    with pytest.raises(ValueError):
        provider(FakeSession()).get_candles("X", "7h", T0, T0 + pd.Timedelta(hours=2))


def test_funding_is_parsed_sorted_and_unique():
    rows = [
        {"timestamp": T0_MS + H, "interest_1h": 1e-6, "interest_8h": 8e-6,
         "index_price": 101.0, "prev_index_price": 100.0},
        {"timestamp": T0_MS, "interest_1h": 2e-6, "interest_8h": 1.6e-5,
         "index_price": 100.0, "prev_index_price": 99.0},
        {"timestamp": T0_MS, "interest_1h": 2e-6, "interest_8h": 1.6e-5,
         "index_price": 100.0, "prev_index_price": 99.0},
    ]
    s = FakeSession([Resp(200, {"result": rows})])
    df = provider(s).get_funding("X", T0, T0 + pd.Timedelta(hours=3))
    assert list(df.index) == [T0, T0 + pd.Timedelta(hours=1)]
    assert df.index.is_unique
    assert list(df.columns) == ["interest_1h", "interest_8h", "index_price", "prev_index_price"]
