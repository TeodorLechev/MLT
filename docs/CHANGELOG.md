# Changelog

Dated history of what changed and why. Groups: Added, Changed, Fixed, Removed, Docs.

<!-- changelog:start -->

## 2026-10-23

### Added
- docs/evidence/venue-availability-2026-10-23.md - sourced review of Binance, Coinbase and Deribit availability for a Bulgarian resident, with verification checklist V1-V3
- ADR 0003 (traded instrument and research data source), proposed

### Changed
- ADR 0002 renamed to 'Execution venue'; owner chose Coinbase on 2026-10-23, kept proposed until eligibility for Bulgaria is verified

### Docs
- STATUS next steps and open questions rewritten around checks V1-V3; README constraints updated


## 2026-10-22

### Added
- project skeleton (config, canonical candle schema, Forecaster contract) with 19 unit tests, CI and pre-commit
- research notebooks 00-05 as outlines with explicit status lines
- decision records 0001 (model stack, proposed) and 0002 (traded instrument and venue, proposed)

### Docs
- documentation system - README, STATUS, ARCHITECTURE, RESEARCH_LOG, CHANGELOG, decisions with an evidence rule

### Fixed
- removed two stray empty directories from the first skeleton archive

