import pytest

from mlt.config import LIVE_CONFIRM_PHRASE, Settings


def test_defaults_are_safe():
    s = Settings.from_env({})
    assert s.dry_run is True
    assert s.live_enabled is False


def test_live_requires_confirmation_phrase():
    with pytest.raises(ValueError):
        Settings.from_env({"DRY_RUN": "false"})


def test_live_enabled_only_with_both_conditions():
    s = Settings.from_env({"DRY_RUN": "false", "LIVE_TRADING_CONFIRM": LIVE_CONFIRM_PHRASE})
    assert s.live_enabled is True


def test_unrecognised_dry_run_value_stays_dry():
    assert Settings.from_env({"DRY_RUN": "maybe"}).dry_run is True
