# Runbook: Coinbase API smoke test

**Purpose.** Verify, with the owner's own key, that the Global Derivatives gateway accepts authentication and an order lifecycle on `BTC_USDC-PERPETUAL` (check V3 in [ADR 0002](decisions/0002-execution-venue.md)). It does **not** prove that trading is permitted for a Bulgarian resident; that is V1–V2 in the [evidence file](evidence/venue-availability-2026-10-23.md).

**Script:** `tools/coinbase_smoke_test.py` (unit-tested against a fake gateway; never run against the real one by the project author).

## Before you run
1. Create a **separate** CDP API key with only `view` + `trade`, bound to the Global Derivatives portfolio, with an IP allowlist if the portal offers one. Do **not** reuse a key that has `transfer` or `export`.
2. Save the key JSON **outside the repository** (for example `~/keys/cdp_mlt.json`). Never commit it, never paste it into a chat.
3. `pip install -e ".[dev,live]"`

## Stages (run them in order)
| Stage | Command | What it does | Risk |
|---|---|---|---|
| 0 | `python tools/coinbase_smoke_test.py` | Public calls only: instrument specification and ticker. No key. | none |
| 1 | `python tools/coinbase_smoke_test.py --key-file ~/keys/cdp_mlt.json` | Authenticates, reads account summary and positions. | none (read-only) |
| 2 | `LIVE_TRADING_CONFIRM=YES_I_UNDERSTAND python tools/coinbase_smoke_test.py --key-file ~/keys/cdp_mlt.json --execute` | Places ONE minimum-size, post-only limit BUY 3 % below the best bid, verifies it is `open`, then cancels it. | a resting order for a few seconds, far from the market; no fill expected |

Safeguards: no market orders, no leverage change, notional capped by `--max-notional` (default 15 USDC), the order is cancelled in a `finally` block, and `--execute` is refused without the confirmation phrase.

## What to record afterwards
The script writes `logs/smoke_<time>.json` (git-ignored; contains no secrets and no balances). Record only the conclusion in the evidence file (V3 row): did `public/auth` succeed (and with which JWT variant), were the order states `open` → `cancelled`, and what errors, if any, were returned.

## If something fails
- `public/auth` rejected with both JWT variants: the `uri` claim for this host is undocumented; report the exact error text (no tokens) so the flow can be adjusted.
- Order rejected for price band or minimum size: lower `--offset-pct` or read the error; do not raise the size.
- Anything that leaves an open order: cancel it manually in the Coinbase app.

## Windows (PowerShell) example
Key file at `D:\cdp_api_key.json` (outside the repository), repository checked out in the current folder:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev,live]"
python tools\coinbase_smoke_test.py --key-file D:\cdp_api_key.json            # stages 0-1

$env:LIVE_TRADING_CONFIRM = "YES_I_UNDERSTAND"                                  # stage 2 only
python tools\coinbase_smoke_test.py --key-file D:\cdp_api_key.json --execute
Remove-Item Env:LIVE_TRADING_CONFIRM
```

Run from the repository root so that `logs\` (git-ignored) is the report folder. The key must be an **ECDSA** (ES256) CDP key; an Ed25519 key is rejected with a clear message.
