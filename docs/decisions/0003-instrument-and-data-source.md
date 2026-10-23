# 0003 – Traded instrument and research data source
- Status: proposed
- Date: 2026-10-23
- Evidence: docs/evidence/venue-availability-2026-10-23.md

## Question
Which instrument is traded on Coinbase, and which series is used for research? Research and live must use the **same** instrument (README §1).

## Options considered
1. **EEA "perpetual-style" future** from Coinbase Financial Services Europe: 5-year expiry, hourly funding, daily settlement, up to 10x on BTC/ETH (E3). Candidate if V1–V3 show it is the product available to the owner. If it cannot be traded through the API (E12), automated trading is impossible on this product and ADR 0002 falls back to Kraken/OKX.
2. **Global Derivatives perpetual** (Deribit-powered gateway): perpetuals with up to 50x leverage; eligibility for Bulgaria unverified (E8, E9). Coinbase states these perpetuals come from non-EEA affiliates, not under an EU licence (E15), so this option is used only after the owner's own legal check, never as the default. The owner's account currently shows `BTC_USDC-PERPETUAL` under this route (E20). The name matches Deribit's USDC-margined perpetual and the gateway is Deribit-powered (E8); if contract specification and funding match (to be checked in `01_data`), Deribit public candles are the traded series, not a proxy.
3. **Deribit public `BTC-PERPETUAL` data as a proxy** for research. Public data needs no account, but it is a different contract than options 1 and 2; it may be used only if the difference is measured.

## Experiment (to do)
After V1–V3: load the candles and funding of the chosen product in `01_data`; if a proxy (option 3) is used, measure its difference to the traded series (price, funding, volume) and the effect on net returns of a fixed baseline strategy.

## Result
Not yet measured.

## Decision and consequences
Pending. Depends on ADR 0002 (V1–V3). Until accepted, notebooks 02–04 must not be treated as final.
