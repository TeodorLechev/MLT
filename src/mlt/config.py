"""Central configuration. Safe by default: dry-run is ON."""
from __future__ import annotations

import os
from dataclasses import dataclass

LIVE_CONFIRM_PHRASE = "YES_I_UNDERSTAND"


@dataclass(frozen=True)
class Settings:
    venue: str = "deribit"
    instrument: str = "BTC-PERPETUAL"
    interval: str = "1h"
    dry_run: bool = True
    live_trading_confirm: str = ""

    @property
    def live_enabled(self) -> bool:
        """Live orders require BOTH dry_run=False and the explicit confirmation phrase."""
        return (not self.dry_run) and self.live_trading_confirm == LIVE_CONFIRM_PHRASE

    def validate(self) -> None:
        if not self.dry_run and self.live_trading_confirm != LIVE_CONFIRM_PHRASE:
            raise ValueError(
                "dry_run=False requires LIVE_TRADING_CONFIRM=" + LIVE_CONFIRM_PHRASE
            )
        if not self.instrument:
            raise ValueError("instrument must not be empty")

    @classmethod
    def from_env(cls, env: dict | None = None) -> Settings:
        env = os.environ if env is None else env
        raw_dry = str(env.get("DRY_RUN", "true")).strip().lower()
        settings = cls(
            venue=env.get("VENUE", cls.venue),
            instrument=env.get("INSTRUMENT", cls.instrument),
            interval=env.get("INTERVAL", cls.interval),
            dry_run=raw_dry not in ("false", "0", "no"),
            live_trading_confirm=env.get("LIVE_TRADING_CONFIRM", ""),
        )
        settings.validate()
        return settings
