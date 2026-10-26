# 0003 – Traded instrument and research data source
- Status: proposed
- Date: 2026-10-23
- Evidence: docs/evidence/venue-availability-2026-10-23.md

## Question
Which instrument is traded on Coinbase, and which series is used for research? Research and live must use the **same** instrument (README §1).

## Options considered
1. **EEA "perpetual-style" future** from Coinbase Financial Services Europe: 5-year expiry, hourly funding, daily settlement, up to 10x on BTC/ETH (E3). It is the US-regulated derivatives offering reached through CBFSE (E22, E23). Per the exchange rulebook (E25) the BTC contract is 1/100 BTC, based on the MarketVector Coinbase Bitcoin Benchmark Rate, cash settled daily, with hourly funding applied as cash adjustments and ±10% hourly price limits; these mechanics must be compared with the Deribit-based perpetual before the two series are mixed. The available price history may be short; check in `01_data`. Candidate if V1–V3 show it is the product available to the owner. If it cannot be traded through the API (E12), automated trading is impossible on this product and ADR 0002 falls back to Kraken/OKX.
2. **Global Derivatives perpetual** (Deribit-powered gateway): perpetuals with up to 50x leverage; eligibility for Bulgaria unverified (E8, E9). Coinbase states these perpetuals come from non-EEA affiliates, not under an EU licence (E15), so this option (served by Coinbase Bermuda Ltd under the Deribit Rulebook, E21) is used only after the owner's own legal check, never as the default. The owner's account currently shows `BTC_USDC-PERPETUAL` under this route (E20). The name matches Deribit's USDC-margined perpetual and the gateway is Deribit-powered (E8); if contract specification and funding match (to be checked in `01_data`; the gateway reports contract size 0.0001 BTC, tick 0.1, minimum amount 0.0001 BTC, max leverage 50, maker/taker 0.015 %/0.035 %, E37), Deribit public candles are the traded series, not a proxy. The agreement confirms that orders are executed only on the Deribit Exchange (E31), which strengthens this hypothesis. Data used for research must come under terms that allow a local cache: the Coinbase Bermuda agreement restricts storing market data obtained through its services (E32), so the data comes from Deribit's public API instead. Deribit's Terms of Service allow market data for personal use only (E34): the cache stays private, git-ignored and unshared, and the owner re-reads the current terms.
3. **Deribit public `BTC-PERPETUAL` data as a proxy** for research. Public data needs no account, but it is a different contract than options 1 and 2; it may be used only if the difference is measured.

## Experiment (to do)
After V1–V3: load the candles and funding of the chosen product in `01_data`; if a proxy (option 3) is used, measure its difference to the traded series (price, funding, volume) and the effect on net returns of a fixed baseline strategy.

## Result
Not yet measured.

## Decision and consequences
Pending. Depends on ADR 0002 (V1–V3). Until accepted, notebooks 02–04 must not be treated as final.
