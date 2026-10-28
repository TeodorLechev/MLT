"""Parquet cache for candles and funding. One file per (venue, instrument, kind[, interval]).

The cache is PRIVATE research data (provider terms usually forbid redistribution) and lives
in `data/`, which is git-ignored. Writes are atomic, so an interrupted download never leaves
a corrupt file behind.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from mlt.data.providers.base import CandleProvider, FundingProvider
from mlt.data.schema import interval_to_ms, validate_candles


def _merge(*frames: pd.DataFrame) -> pd.DataFrame:
    frames = tuple(f for f in frames if f is not None and len(f))
    if not frames:
        raise ValueError("nothing to merge")
    df = pd.concat(frames).sort_index()
    return df[~df.index.duplicated(keep="last")]


class FrameCache:
    def __init__(self, root: str | Path = "data") -> None:
        self.root = Path(root)

    def path(self, venue: str, instrument: str, kind: str, interval: str | None = None) -> Path:
        name = f"{kind}_{interval}.parquet" if interval else f"{kind}.parquet"
        return self.root / venue / instrument / name

    def load(self, path: Path) -> pd.DataFrame | None:
        return pd.read_parquet(path) if path.exists() else None

    def save(self, path: Path, df: pd.DataFrame) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        df.to_parquet(tmp)
        tmp.replace(path)

    def read(self, venue: str, instrument: str, kind: str, interval: str | None = None) -> pd.DataFrame:
        """Return a cached frame as it is, without any network access (for reproducible research)."""
        path = self.path(venue, instrument, kind, interval)
        df = self.load(path)
        if df is None:
            raise FileNotFoundError(f"nothing cached at {path}; run the data notebook first")
        return df

    # ------------------------------------------------------------------ candles
    def get_candles(
        self,
        provider: CandleProvider,
        instrument: str,
        interval: str,
        start: pd.Timestamp,
        end: pd.Timestamp,
    ) -> pd.DataFrame:
        """Return candles for [start, end], downloading only what the cache is missing."""
        step = pd.Timedelta(milliseconds=interval_to_ms(interval))
        path = self.path(provider.name, instrument, "candles", interval)
        cached = self.load(path)
        if cached is None or cached.empty:
            df = provider.get_candles(instrument, interval, start, end)
        else:
            parts = [cached]
            first_open = cached.index[0] - step
            if start < first_open:
                parts.append(provider.get_candles(instrument, interval, start, cached.index[0] - step))
            if end > cached.index[-1]:
                parts.append(provider.get_candles(instrument, interval, cached.index[-1], end))
            df = _merge(*parts)
        if len(df):
            validate_candles(df)
            if cached is None or not df.index.equals(cached.index):
                self.save(path, df)
        return df[((df.index - step) >= start) & (df.index <= end)]

    # ------------------------------------------------------------------ funding
    def get_funding(
        self, provider: FundingProvider, instrument: str, start: pd.Timestamp, end: pd.Timestamp
    ) -> pd.DataFrame:
        path = self.path(provider.name, instrument, "funding")
        cached = self.load(path)
        if cached is None or cached.empty:
            df = provider.get_funding(instrument, start, end)
        else:
            parts = [cached]
            if start < cached.index[0]:
                parts.append(provider.get_funding(instrument, start, cached.index[0]))
            if end > cached.index[-1]:
                parts.append(provider.get_funding(instrument, cached.index[-1], end))
            df = _merge(*parts)
        if len(df) and (cached is None or not df.index.equals(cached.index)):
            self.save(path, df)
        return df[(df.index >= start) & (df.index <= end)]
