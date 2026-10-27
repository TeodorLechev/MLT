# Research log

Every experiment that supports a decision is recorded here **with its numbers**, so any claim in the README or an ADR can be traced to data period, costs and notebook. Only values that were actually computed are recorded; if a number is missing, the entry says so.

## Entry template

```
### R-001 – Short title (YYYY-MM-DD)
- **Question:** what was tested and why
- **Notebook / commit:** notebooks/0X_name.ipynb @ <commit or date>
- **Data:** instrument, interval, period, source, train / validation / test split
- **Setup:** model, features, horizon, fees, slippage, funding, seeds
- **Result:** table of metrics (net of costs) vs baselines
- **Sensitivity:** how the result changes with parameters
- **Conclusion:** supports / contradicts which hypothesis; linked ADR
```

## Entries

<!-- Newest first. -->

### R-001 – Data foundation: BTC_USDC-PERPETUAL hourly candles and funding (2026-10-27)
- **Question:** is the Deribit public series of `BTC_USDC-PERPETUAL` clean enough to research on, and is it the same contract that the Coinbase gateway serves?
- **Notebook / commit:** notebooks/01_data.ipynb @ 2026-10-27 (run by the owner; the results below are the numbers printed in that run)
- **Data:** `BTC_USDC-PERPETUAL`, 1h, 2023-10-28 23:00 -> 2026-10-27 22:00 UTC, source Deribit public API, cached in `data/` (private, git-ignored); no train / validation / test split yet
- **Setup:** no model, no costs; provider `DeribitProvider`, schema checks and `find_gaps`
- **Result:**

| Check | Value |
|---|---|
| Closed hourly candles | 26,280 |
| Gaps / missing candles | 0 / 0 |
| Duplicate timestamps | 0 |
| Candles with open/close outside high-low | 0 |
| Zero-volume candles | 13 |
| Funding observations (hourly) | 26,244 |
| Candles without a funding observation | 36 (0.14 %) |
| Mean hourly funding / std | 7.85e-06 / 1.68e-05 |
| Annualised mean funding (simple mean x 24 x 365) | about 6.9 % |
| Contract specification, Deribit vs Coinbase gateway (E37) | identical on contract size, tick, minimum amount, max leverage, maker/taker, settlement, quote currency |

- **Sensitivity:** not applicable (no parameters).
- **Conclusion:** supports the ADR 0003 hypothesis that Deribit public candles are the traded series for the Global Derivatives route. Not recorded: where the 13 zero-volume candles and the 36 candles without funding lie, and how they will be handled; the app's product page was not compared.
