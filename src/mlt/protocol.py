"""Evaluation protocol (ADR 0004): a frozen data window and three consecutive time blocks.

All timestamps are candle CLOSE times (UTC). Blocks are half-open ``[start, end)`` except the
last, which runs to the frozen data end (inclusive). Model and parameter choices may use the
development and validation blocks only; the test block is evaluated once, for the final
candidate (notebook 04), and reading it needs an explicit ``allow_test=True``.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

DATA_START = pd.Timestamp("2023-10-30 22:00", tz="UTC")      # first candle of the cache used in R-003
DATA_END = pd.Timestamp("2026-10-29 08:00", tz="UTC")        # frozen: the last candle used (R-002)
VALIDATION_START = pd.Timestamp("2025-10-01 00:00", tz="UTC")
TEST_START = pd.Timestamp("2026-05-01 00:00", tz="UTC")
BLOCKS = ("development", "validation", "test")


def freeze(df: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    """Restrict a time-indexed object to the frozen window (never read data after DATA_END)."""
    return df.loc[(df.index >= DATA_START) & (df.index <= DATA_END)]


def require_window(df: pd.DataFrame | pd.Series, what: str = "data") -> None:
    """Fail loudly if the cache does not cover the whole frozen window (gate G4: reproducibility)."""
    if len(df) == 0 or df.index[0] > DATA_START or df.index[-1] < DATA_END:
        have = f"{df.index[0]} -> {df.index[-1]}" if len(df) else "nothing"
        raise ValueError(f"{what} does not cover the frozen window {DATA_START} -> {DATA_END} (has {have}); re-run notebook 01")


def block_mask(index: pd.DatetimeIndex, name: str, allow_test: bool = False) -> np.ndarray:
    """Boolean mask of the rows of ``index`` that fall in block ``name``."""
    if name not in BLOCKS:
        raise ValueError(f"unknown block {name!r}; expected one of {BLOCKS}")
    if name == "test" and not allow_test:
        raise PermissionError("the test block is evaluated once, for the final candidate: pass allow_test=True")
    if name == "development":
        m = (index >= DATA_START) & (index < VALIDATION_START)
    elif name == "validation":
        m = (index >= VALIDATION_START) & (index < TEST_START)
    else:
        m = (index >= TEST_START) & (index <= DATA_END)
    return np.asarray(m)


def purge_mask(index: pd.DatetimeIndex, name: str, horizon: int) -> np.ndarray:
    """Rows usable as TRAINING samples for a batch model evaluated on block ``name``.

    A sample at row ``i`` has a target that reaches ``horizon`` bars ahead, so rows within
    ``horizon`` bars before the block start would see the block's prices through their target
    and are dropped (online training on matured samples needs no purge).
    """
    starts = {"development": DATA_START, "validation": VALIDATION_START, "test": TEST_START}
    first = int(index.searchsorted(starts[name]))
    return np.arange(len(index)) < first - horizon
