import pandas as pd

from mlt.data.cache import FrameCache
from mlt.data.schema import validate_candles

T0 = pd.Timestamp("2024-01-01", tz="UTC")
H = pd.Timedelta(hours=1)


def candles(first_close, n):
    idx = pd.date_range(first_close, periods=n, freq="1h", tz="UTC")
    return pd.DataFrame(
        {"open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 1.0}, index=idx
    )


class FakeProvider:
    name = "fake"

    def __init__(self):
        self.calls = []

    def get_candles(self, instrument, interval, start, end):
        self.calls.append((start, end))
        first = (start + H) if start == start.floor("1h") else start.ceil("1h")
        first = max(first, start + H)
        n = int((end - first) / H) + 1
        return candles(first, max(n, 0)) if n > 0 else candles(first, 0)

    def get_funding(self, instrument, start, end):
        self.calls.append((start, end))
        idx = pd.date_range(start.ceil("1h"), end, freq="1h", tz="UTC", name="timestamp")
        return pd.DataFrame({"interest_1h": 1e-6}, index=idx)


def test_first_call_downloads_and_saves(tmp_path):
    cache, prov = FrameCache(tmp_path), FakeProvider()
    df = cache.get_candles(prov, "X", "1h", T0, T0 + 10 * H)
    assert len(df) == 10
    assert cache.path("fake", "X", "candles", "1h").exists()
    validate_candles(df, "1h")


def test_second_call_is_served_from_cache(tmp_path):
    cache, prov = FrameCache(tmp_path), FakeProvider()
    cache.get_candles(prov, "X", "1h", T0, T0 + 10 * H)
    prov.calls.clear()
    df = cache.get_candles(prov, "X", "1h", T0, T0 + 10 * H)
    assert prov.calls == []
    assert len(df) == 10


def test_extending_the_range_downloads_only_the_missing_tail(tmp_path):
    cache, prov = FrameCache(tmp_path), FakeProvider()
    cache.get_candles(prov, "X", "1h", T0, T0 + 10 * H)
    prov.calls.clear()
    df = cache.get_candles(prov, "X", "1h", T0, T0 + 15 * H)
    assert len(prov.calls) == 1
    assert prov.calls[0][0] == T0 + 10 * H
    assert len(df) == 15
    validate_candles(df, "1h")


def test_extending_backwards_downloads_only_the_missing_head(tmp_path):
    cache, prov = FrameCache(tmp_path), FakeProvider()
    cache.get_candles(prov, "X", "1h", T0 + 5 * H, T0 + 10 * H)
    prov.calls.clear()
    df = cache.get_candles(prov, "X", "1h", T0, T0 + 10 * H)
    assert len(prov.calls) == 1
    assert len(df) == 10
    validate_candles(df, "1h")


def test_no_temp_file_left_behind(tmp_path):
    cache, prov = FrameCache(tmp_path), FakeProvider()
    cache.get_candles(prov, "X", "1h", T0, T0 + 3 * H)
    assert not list(tmp_path.rglob("*.tmp"))


def test_funding_cache_roundtrip_and_extension(tmp_path):
    cache, prov = FrameCache(tmp_path), FakeProvider()
    a = cache.get_funding(prov, "X", T0, T0 + 5 * H)
    prov.calls.clear()
    b = cache.get_funding(prov, "X", T0, T0 + 8 * H)
    assert len(prov.calls) == 1
    assert len(b) > len(a)
    assert b.index.is_unique
