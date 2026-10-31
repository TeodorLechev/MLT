import numpy as np
import pandas as pd
import pytest

from mlt import protocol as p

IDX = pd.date_range(p.DATA_START - pd.Timedelta(hours=48), p.DATA_END + pd.Timedelta(hours=48),
                    freq="1h", tz="UTC")


def test_freeze_clips_to_the_window():
    df = pd.DataFrame({"x": 1.0}, index=IDX)
    out = p.freeze(df)
    assert out.index[0] == p.DATA_START and out.index[-1] == p.DATA_END


def test_blocks_partition_the_frozen_index():
    idx = p.freeze(pd.DataFrame({"x": 1.0}, index=IDX)).index
    masks = [p.block_mask(idx, b, allow_test=True) for b in p.BLOCKS]
    assert np.all(sum(m.astype(int) for m in masks) == 1)     # every row in exactly one block
    assert all(m.any() for m in masks)


def test_boundaries_are_half_open_on_close_time():
    idx = pd.DatetimeIndex([p.VALIDATION_START - pd.Timedelta(hours=1), p.VALIDATION_START,
                            p.TEST_START - pd.Timedelta(hours=1), p.TEST_START, p.DATA_END])
    assert list(p.block_mask(idx, "development")) == [True, False, False, False, False]
    assert list(p.block_mask(idx, "validation")) == [False, True, True, False, False]
    assert list(p.block_mask(idx, "test", allow_test=True)) == [False, False, False, True, True]


def test_test_block_needs_an_explicit_acknowledgement():
    with pytest.raises(PermissionError):
        p.block_mask(IDX, "test")
    with pytest.raises(ValueError):
        p.block_mask(IDX, "holdout")


def test_purge_drops_samples_whose_target_reaches_into_the_block():
    idx = p.freeze(pd.DataFrame({"x": 1.0}, index=IDX)).index
    horizon = 37
    keep = p.purge_mask(idx, "validation", horizon)
    first_val = int(idx.searchsorted(p.VALIDATION_START))
    assert keep.sum() == first_val - horizon
    assert idx[keep][-1] + pd.Timedelta(hours=horizon) < p.VALIDATION_START


def test_window_is_consistent():
    assert p.DATA_START < p.VALIDATION_START < p.TEST_START < p.DATA_END


def test_require_window_accepts_full_coverage_and_rejects_gaps_at_either_end():
    full = pd.DataFrame({"x": 1.0}, index=IDX)
    p.require_window(full)                                       # covers the window with margin
    with pytest.raises(ValueError):
        p.require_window(full.loc[full.index > p.DATA_START])    # head missing
    with pytest.raises(ValueError):
        p.require_window(full.loc[full.index < p.DATA_END])      # tail missing
    with pytest.raises(ValueError):
        p.require_window(full.iloc[:0])
