# 0002 – Traded instrument and data venue
- Status: proposed
- Date: 2026-10-22

## Question
Which instrument will be traded, and from which venue do research data come? Research and live must use the **same** instrument (README §1).

## Constraints (stated by the project owner)
- The venue must be legally accessible from Bulgaria / EU. Binance holds no licence for Bulgaria, which is why execution moved to Coinbase.
- Research data must be reproducible without an API key where possible.

## Options considered
1. Deribit `BTC-PERPETUAL` for data (public, no key), execution on the Coinbase perpetual.
2. Data and execution both from the Coinbase Global Derivatives perpetual.
3. Binance data for research only (rejected for execution by the constraint above).

## Experiment (to do)
Load the candidate series in `01_data`, compare price/volume series, fees and funding between the options, and measure how far the signal and costs differ when the same strategy is run on each. Venue eligibility must be confirmed in writing with the venue before go-live.

## Result
Not yet measured.

## Decision and consequences
Pending. Until accepted, notebooks 02–04 must not be treated as final.
