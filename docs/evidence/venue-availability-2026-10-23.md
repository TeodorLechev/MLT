# Evidence: venue availability for a Bulgarian (EU/EEA) resident

- Collected: 2026-10-23 (web review; sources and dates below)
- Used by: [ADR 0002](../decisions/0002-execution-venue.md), [ADR 0003](../decisions/0003-instrument-and-data-source.md)
- Not legal advice. Anything marked *unverified* must be confirmed with the venue in writing before real money is used.

## Why this file exists
The project may only trade where the owner can trade legally and freely from Bulgaria. Perpetual-style derivatives are outside MiCA and fall under MiFID II, so the venue needs an EU authorisation for derivatives, not only a crypto-asset licence.

## Findings

| # | Claim | Status | Source |
|---|---|---|---|
| E1 | Binance withdrew its Greek MiCA application on 2026-06-24 and suspended most services for EU/EEA users from 2026-07-01, including futures and derivatives. | Secondary sources only (no Binance notice found) | [Tangem](https://tangem.com/en/learning-hub/post/is-binance-mica-authorised/), [Bleap](https://www.bleap.finance/en-us/blog/is-binance-mica-licensed) |
| E2 | After 2026-07-01 a firm without a MiCA licence must stop serving EU clients (ESMA, no extension). | Secondary sources only | [Bleap](https://www.bleap.finance/en-us/blog/is-binance-mica-licensed) |
| E3 | Coinbase offers futures, including "perpetual-style" futures (5-year expiry, hourly funding, settled daily, up to 10x on BTC/ETH), in 26 European countries through Coinbase Advanced, launched 2026-03-09. | **Official** (Coinbase blog) | [Coinbase blog](https://www.coinbase.com/blog/futures-contracts-europe) |
| E4 | The EEA derivatives service is provided by Coinbase Financial Services Europe Ltd (CySEC licence 374/19), only to eligible customers after suitability checks. | **Official** | [Coinbase blog](https://www.coinbase.com/blog/futures-contracts-europe) |
| E5 | Coinbase help says the derivatives offering is available in "most countries" of the EEA, and products may not be available in a given country. | **Official** | [Coinbase help](https://help.coinbase.com/en/coinbase/derivatives/us-derivatives-intro) |
| E6 | Bulgaria is in Coinbase's MiCA service migration to Coinbase Luxembourg S.A. (effective 2025-10-13). This concerns spot/custody, not derivatives. | **Official** | [Coinbase help](https://help.coinbase.com/en/coinbase/other-topics/other/mica-cblu) |
| E7 | The list of the 26 countries is not published in the sources reviewed. **Bulgaria is not confirmed.** | *Unverified* | – |
| E8 | "Global Derivatives" (Deribit-powered gateway, former INTX) offers perpetuals to "eligible non-US clients"; INTX perpetual trading through the Advanced Trade API ended on 2026-10-01; the new protocol is JSON-RPC 2.0 with the same CDP API key. | **Official** (CDP docs) | [CDP docs](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/overview), [migration guide](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/guides/derivatives/overview) |
| E9 | No public country table exists for Global Derivatives; whether Bulgarian retail clients are eligible is **unverified**. | *Unverified* (third-party statement) | [coinperps](https://www.coinperps.com/learn/coinbase-perpetuals-restricted-countries) |
| E10 | Coinbase acquired Deribit (closed 2025-08-14). | **Official** (SEC 10-Q) | [SEC 10-Q](https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000054/coin-20260331.htm) |
| E11 | Deribit's restricted-jurisdiction list for Europe names Belarus, Russia, UK retail and parts of Ukraine, not Bulgaria; it is reported not to hold a MiFID II licence, leaving EEA retail access in a legal grey zone. | Secondary sources only | [Datawallet](https://www.datawallet.com/crypto/deribit-restricted-countries), [perpfinder](https://perpfinder.com/mica/deribit) |
| E12 | It is not established whether the EEA "perpetual-style futures" (E3) can be traded through the Advanced Trade API. The API docs list spot, US futures and Global Derivatives only. | *Unverified* | [CDP docs](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/overview) |
| E13 | Other EU-authorised derivatives venues exist (Kraken, Crypto.com, OKX, Gemini); Bybit's global platform is restricted for Bulgaria. Availability for Bulgaria and API support were not checked. | Secondary sources only | [Finance Magnates](https://www.financemagnates.com/cryptocurrency/regulation/europes-crypto-market-after-july-1-who-stays-who-leaves-and-what-changes-under-mica/), [Forklog](https://forklog.com/en/bybit-to-restrict-global-exchange-services-for-eu-residents/) |
| E14 | Coinbase's annual report states two separate derivatives routes: Coinbase Financial Services Europe Ltd is a MiFID derivatives broker (CySEC) for eligible EU customers, while Coinbase International Exchange (Bermuda, BMA) offers perpetuals to eligible non-US customers; Deribit FZE operates under VARA (Dubai). So "derivatives are a non-MiCA service provided by CB Bermuda Ltd" describes the non-EU route, not the EEA route (confirmed by E15). | **Official** (SEC 10-K FY2025) | [SEC 10-K](https://www.sec.gov/Archives/edgar/data/1679788/000167978826000015/coin-20251231.htm) |
| E15 | Coinbase's own "What is MiCA" Learn page lists **derivatives trading — crypto perpetual futures via non-EEA Coinbase affiliate entities** among services that are regulated but "not provided under an EU licence"; MiCA/EU protections do not apply to them, and Coinbase says it tells the user before such a service is used. The page does not mention Bulgaria or the CySEC futures product (E3, E4). | **Official** (Coinbase Learn) | [Coinbase Learn](https://www.coinbase.com/learn/your-crypto/what-is-mica-markets-in-crypto-assets-regulation) |
| E16 | Kraken: MiFID investment firm Payward Europe Digital Solutions (CY) Ltd (CySEC licence 342/17) plus two MiCA CASP authorisations from the Central Bank of Ireland; Kraken states the footprint covers all 30 EEA countries. | **Official** (Kraken) | [Kraken regulation page](https://www.kraken.com/learn/how-kraken-is-regulated) |
| E17 | Kraken launched MiFID perpetual and fixed-maturity futures for EEA retail and institutional clients on 2025-05-20 via that Cyprus entity; clients must pass an eligibility assessment; 150+ perpetual markets on Kraken Pro EU (Nov 2025). | **Official** (Kraken blog) | [Kraken blog](https://blog.kraken.com/news/euro-reg-futures), [Kraken Pro EU](https://blog.kraken.com/product/kraken-derivatives/crypto-collateral-eu-futures) |
| E18 | OKX: "X-Perps" (5-year expiry, funding rate, up to 10x) launched across the EEA through OKX's Malta MiFID entity; the MiCA country list including Bulgaria comes from a third-party tracker. | Secondary sources only | [Bankless Times](https://www.banklesstimes.com/articles/2026/04/15/okx-launches-mifid-regulated-x-perps-in-europe/), [casptracker](https://casptracker.eu/exchange/okx/) |
| E19 | Kraken has a Futures REST/WebSocket API (used via an unofficial Python SDK). Whether accounts of the EU MiFID entity can trade through it is unverified; OKX's API was not checked. | *Unverified* | [python-kraken-sdk](https://github.com/btschwertfeger/python-kraken-sdk) |
| E20 | Owner's Coinbase Advanced account (reported 2026-10-23): the Derivatives tab is visible and shows the product `BTC_USDC-PERPETUAL` (a true perpetual); the owner's API key is bound to the "Global Derivatives" portfolio. The serving legal entity was not read from the agreement yet. | Owner-reported, not independently verified | owner |

## Comparison of EU-authorised derivatives routes (reviewed 2026-10-23)

| Criterion | Coinbase (CBFSE, CySEC) | Kraken (Payward Europe Digital Solutions, CySEC) | OKX (OKX Europe Markets, MFSA) |
|---|---|---|---|
| EU derivatives licence (MiFID II) | Yes, official (E4, E14) | Yes, official (E16, E17) | Yes, secondary sources (E18) |
| Explicitly confirmed for Bulgaria | **No** (E7) | **No**, EEA-wide claim only (E16) | **No**, EEA-wide claim only (E18) |
| Contract form for EEA retail | 5-year "perpetual-style" future, hourly funding, up to 10x (E3) | perpetual and fixed-maturity futures (E17) | 5-year "X-Perps" with funding, up to 10x (E18) |
| API trading for the EU product | Unverified (E12) | Unverified (E19) | Not checked |
| Owner preference | **Chosen** (2026-10-23) | fallback | fallback |

All three need the owner's own eligibility assessment, so the real test is V1–V3 on the account, not the press releases.

## Verification checklist (owner)
Attach the answers outside the repository if they contain personal data; record only the conclusion here.

| ID | Check | Done when | Result |
|---|---|---|---|
| V1 | In Coinbase Advanced, is the **Derivatives** tab available for the owner's account? Which legal entity is shown in the account agreement for derivatives (Coinbase Financial Services Europe vs a non-EEA entity)? | Entity and product named | partly: Derivatives tab visible, product BTC_USDC-PERPETUAL on the Global Derivatives portfolio (E20); entity named in the agreement still to be read |
| V2 | Written answer from Coinbase support: which product and entity serve a Bulgarian resident (EEA perpetual-style futures and/or Global Derivatives)? | Reply received and summarised | not yet checked |
| V3 | Can the product from V2 be traded through the Advanced Trade API (REST/WebSocket or the JSON-RPC gateway)? | Docs or support confirm | not yet checked |
| V4 | Only if V1–V3 fail: repeat the same three checks for Kraken (Kraken Pro derivatives eligibility, serving entity, API trading), then OKX. | One venue passes all three | not needed yet |
