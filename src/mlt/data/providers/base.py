"""Provider contracts. Implementations (Deribit, Coinbase, ...) return the canonical schema."""
from __future__ import annotations

from typing import Protocol

import pandas as pd


class CandleProvider(Protocol):
    name: str

    def get_candles(
        self, instrument: str, interval: str, start: pd.Timestamp, end: pd.Timestamp
    ) -> pd.DataFrame:
        """Return validated candles (see mlt.data.schema.validate_candles).

        Index = candle CLOSE time (UTC). Only candles with open >= start and close <= end
        that are already closed are returned.
        """
        ...


class FundingProvider(Protocol):
    name: str

    def get_funding(
        self, instrument: str, start: pd.Timestamp, end: pd.Timestamp
    ) -> pd.DataFrame:
        """Return funding observations indexed by UTC timestamp, sorted and unique."""
        ...
