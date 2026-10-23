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
2. **Coinbase** – two different products: (a) the CySEC/MiFID "perpetual-style" future, which is EU-licensed (E3, E4); (b) true perpetuals (Global Derivatives), which Coinbase itself says are provided by non-EEA affiliates and **not under an EU licence** (E15). An API route is documented only for (b) (E8, E12). Bulgaria is **not yet confirmed** for either (E7, E9).
3. **Deribit (direct)** – legal grey zone for EEA retail clients (E11); no MiFID II licence reported.
4. **Kraken** – MiFID investment firm in Cyprus (CySEC 342/17) plus MiCA authorisations; perpetual and fixed-maturity futures for EEA retail since 2025-05-20 (E16, E17). Strongest-documented fallback. Bulgaria and API access for the EU product not confirmed (E19).
5. **OKX** – MiFID entity in Malta, 5-year "X-Perps" for the EEA (E18). Second fallback; not confirmed for Bulgaria; API not checked.

## Experiment
Not a modelling experiment. Verification checks V1–V3 in the evidence file must pass: derivatives are available to the owner's account, the serving entity and product are known, and the product is tradable through the API.

## Result
Not yet measured. V1–V3 are open.

## Decision and consequences
**Owner decision (2026-10-23): use Coinbase.** The record stays `proposed` until V1–V3 are done; it becomes `accepted` only with their results in the evidence file. Acceptance requires the **EU-licensed product (a)** to pass V1–V3, in particular V3 (API trading); passing them only for the non-EU product (b) is not enough, see E15. Decision rule: the first venue that passes V1–V3 (derivatives eligible for the owner's account, serving entity is EU/MiFID-authorised, API trading works) is accepted; order of evaluation: Coinbase, Kraken, OKX (V4 in the evidence file). A non-EU entity (Bermuda, Dubai) serving the account is not enough, see E14.
Consequences: the broker adapter targets the Coinbase API (Global Derivatives uses JSON-RPC 2.0 since 2026-10-01); the instrument is decided separately in [ADR 0003](0003-instrument-and-data-source.md); no live trading before this record is accepted (phase P4 gate).
