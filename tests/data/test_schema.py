import pandas as pd
import pytest

from mlt.data.schema import drop_unclosed, interval_to_ms, validate_candles


def make(n=5, freq="1h"):
    idx = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")
    return pd.DataFrame(
        {"open": 100.0, "high": 101.0, "low": 99.0, "close": 100.5, "volume": 1.0}, index=idx
    )


def test_interval_to_ms():
    assert interval_to_ms("1h") == 3_600_000
    assert interval_to_ms("15m") == 900_000
    assert interval_to_ms("1d") == 86_400_000


@pytest.mark.parametrize("bad", ["", "h", "1x", "0h", "-1h", "1.5h"])
def test_interval_to_ms_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        interval_to_ms(bad)


def test_valid_frame_passes():
    df = make()
    assert validate_candles(df, "1h") is df


def test_naive_index_rejected():
    df = make()
    df.index = df.index.tz_localize(None)
    with pytest.raises(ValueError):
        validate_candles(df)


def test_duplicates_rejected():
    df = make()
    df = pd.concat([df, df.iloc[[0]]]).sort_index()
    with pytest.raises(ValueError):
        validate_candles(df)


def test_gap_detected_not_filled():
    full = make()
    df = full.drop(full.index[2])
    with pytest.raises(ValueError, match="gap"):
        validate_candles(df, "1h")


def test_high_below_low_rejected():
    df = make()
    df.iloc[1, df.columns.get_loc("high")] = 50.0
    with pytest.raises(ValueError):
        validate_candles(df)


def test_drop_unclosed_is_causal():
    df = make()
    now = df.index[3]
    out = drop_unclosed(df, now)
    assert out.index.max() < now
    assert len(out) == 3
