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

## Verification checklist (owner)
Attach the answers outside the repository if they contain personal data; record only the conclusion here.

| ID | Check | Done when | Result |
|---|---|---|---|
| V1 | In Coinbase Advanced, is the **Derivatives** tab available for the owner's account? Which legal entity is shown in the account agreement for derivatives (Coinbase Financial Services Europe vs a non-EEA entity)? | Entity and product named | not yet checked |
| V2 | Written answer from Coinbase support: which product and entity serve a Bulgarian resident (EEA perpetual-style futures and/or Global Derivatives)? | Reply received and summarised | not yet checked |
| V3 | Can the product from V2 be traded through the Advanced Trade API (REST/WebSocket or the JSON-RPC gateway)? | Docs or support confirm | not yet checked |
