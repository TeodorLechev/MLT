# Changelog

Dated history of what changed and why. Groups: Added, Changed, Fixed, Removed, Docs.

<!-- changelog:start -->

## 2026-10-23

### Added
- docs/evidence/venue-availability-2026-10-23.md - sourced review of Binance, Coinbase and Deribit availability for a Bulgarian resident, with verification checklist V1-V3
- ADR 0003 (traded instrument and research data source), proposed
- evidence E14-E19 and a comparison of EU-authorised derivatives routes (Coinbase, Kraken, OKX) in docs/evidence
- evidence E20 (owner's Coinbase account shows BTC_USDC-PERPETUAL on the Global Derivatives portfolio); V1 partly done

### Changed
- ADR 0002 renamed to 'Execution venue'; owner chose Coinbase on 2026-10-23, kept proposed until eligibility for Bulgaria is verified
- ADR 0002 now has an explicit decision rule and Kraken/OKX as ranked fallbacks; verification checklist gets V4
- evidence E15 verified from Coinbase's own page - true perpetuals for EEA users are served by non-EEA affiliates, not under an EU licence
- ADR 0002/0003 now require the EU-licensed Coinbase product to pass V1-V3 (incl. API); Global Derivatives perpetual demoted to an option needing the owner's own legal check
- ADR 0003 notes the hypothesis that Deribit public candles of the same contract are the traded series, to be verified in 01_data

### Docs
- STATUS next steps and open questions rewritten around checks V1-V3; README constraints updated
- STATUS open questions note that the current Coinbase derivatives may be served by a non-EU entity
- STATUS risks updated (legal path and API path at Coinbase may not coincide)
- STATUS risk about over-broad API key permissions


## 2026-10-22

### Added
- project skeleton (config, canonical candle schema, Forecaster contract) with 19 unit tests, CI and pre-commit
- research notebooks 00-05 as outlines with explicit status lines
- decision records 0001 (model stack, proposed) and 0002 (traded instrument and venue, proposed)

### Docs
- documentation system - README, STATUS, ARCHITECTURE, RESEARCH_LOG, CHANGELOG, decisions with an evidence rule

### Fixed
- removed two stray empty directories from the first skeleton archive

