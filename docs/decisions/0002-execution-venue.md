# 0002 – Execution venue
- Status: proposed
- Date: 2026-10-23
- Evidence: docs/evidence/venue-availability-2026-10-23.md

## Question
Where do we trade, given that the owner must be able to trade freely and legally from Bulgaria (EU/EEA)?

## Constraint (stated by the project owner)
The owner has no preference between Binance, Coinbase and Deribit as long as trading from the current location is free and legal.

## Options considered
1. **Binance** – excluded: it has no MiCA authorisation and suspended EU services including derivatives from 2026-07-01 (E1, E2).
2. **Coinbase** – the only reviewed option with a documented EU derivatives authorisation (MiFID II, CySEC) and an API route (E3, E4, E8). Bulgaria is **not yet confirmed** (E7, E9).
3. **Deribit (direct)** – legal grey zone for EEA retail clients (E11); no MiFID II licence reported.
4. **Other EU-authorised venues** (Kraken, Crypto.com, OKX, Gemini) – not evaluated for Bulgaria or API support (E13); fallback if Coinbase fails verification.

## Experiment
Not a modelling experiment. Verification checks V1–V3 in the evidence file must pass: derivatives are available to the owner's account, the serving entity and product are known, and the product is tradable through the API.

## Result
Not yet measured. V1–V3 are open.

## Decision and consequences
**Owner decision (2026-10-23): use Coinbase.** The record stays `proposed` until V1–V3 are done; it becomes `accepted` only with their results in the evidence file. If V1–V3 fail, option 4 is evaluated before any research is finalised.
Consequences: the broker adapter targets the Coinbase API (Global Derivatives uses JSON-RPC 2.0 since 2026-10-01); the instrument is decided separately in [ADR 0003](0003-instrument-and-data-source.md); no live trading before this record is accepted (phase P4 gate).
