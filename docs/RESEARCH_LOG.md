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

### R-002 – Baselines: flat, buy-and-hold and the previous linear model, with costs and funding (2026-10-29)
- **Question:** which bar must a candidate model beat on this instrument after costs and funding, and does the previous linear model clear it?
- **Notebook / commit:** notebooks/02_baselines.ipynb @ 2026-10-29 (run by the owner; the numbers are those printed in that run)
- **Data:** `BTC_USDC-PERPETUAL`, 1h, Deribit public API, cache of 26,290 candles from 2023-10-29 23:00 to 2026-10-29 08:00 UTC (re-fetched after R-001, hence a slightly different window); funding 26,254 observations, 36 candles without a funding value (treated as zero funding, counted); evaluated bars 24,003 from 2024-02-02 06:00 UTC (warm-up of 287 bars plus a burn-in of 2,000 updates); no train / validation / test split yet (ADR 0004)
- **Setup:** 1x leverage, position as a fraction of equity; linear model with the predecessor's parameters (windows 125-250 h, horizon 37, lr 0.00325, L2 0.425, threshold 1.0 x (fee + slippage), shorts allowed, predictions clipped to +-0.2), trained online on matured samples only; fee 3.5 bp taker taken from the gateway (E37), the fee schedule of the account was not read; funding sign and timing assumed (long pays a positive rate); no parameter tuned in the notebook. The predecessor tuned these parameters on Binance data to 2026-08-01, which overlaps this series.
- **Result** (gateway taker 3.5 bp, funding included):

| Strategy | Total return | CAGR | Sharpe | Max drawdown | In market | Trades |
|---|---|---|---|---|---|---|
| Flat | 0.0 % | 0.0 % | – | 0.0 % | 0 % | 0 |
| Buy-and-hold | +57.9 % | 18.1 % | 0.59 | -54.6 % | 100 % | 1 |
| Linear model | +92.1 % | 26.9 % | 0.745 | -35.3 % | 96.4 % | 165 |

| Linear model by cost scenario | Total return | Sharpe | Max drawdown | Trades |
|---|---|---|---|---|
| gateway taker 3.5 bp | +92.1 % | 0.745 | -35.3 % | 165 |
| + 5 bp slippage | +78.9 % | 0.695 | -39.3 % | 181 |
| predecessor costs (10 + 5 bp) | +16.6 % | 0.347 | -42.6 % | 190 |

| Slice (gateway taker, funding) | Buy-and-hold | Linear model |
|---|---|---|
| 2024 | +96.2 % (Sharpe 1.66) | +61.9 % (1.27) |
| 2025 | -9.8 % (-0.01) | +3.0 % (0.29) |
| 2026 to 2026-10-29 | -11.1 % (-0.12) | +15.4 % (0.63) |
| after 2026-08-01, 2,144 bars (not seen by the predecessor's tuning) | +25.3 % (2.82) | +10.4 % (1.36) |

- **Sensitivity:** funding off: buy-and-hold +85.1 % (Sharpe 0.71, drawdown -53.8 %), linear +109.9 % (0.81, -35.2 %); funding with a one-bar lag: practically unchanged (+57.86 % and +92.1 %). Timing test (200 circular shifts of the model's positions, same exposure, trades and costs): real Sharpe 0.745, shifted mean -0.086, 5th-95th percentile [-1.053, 0.728]; 5.0 % of shifted runs are at least as good as the real one.
- **Conclusion:** the reference bar at gateway costs with funding is Sharpe 0.745 (linear) and 0.59 (buy-and-hold). The linear model is not shown to be better: its parameters were tuned on this period, its Sharpe lead of about 0.15 is small against the sampling error of a 2.75-year series (rough standard error near 0.7 per Sharpe, assuming independent returns; a reviewer's estimate, not measured), it loses most of its return under the predecessor's costs, it trails buy-and-hold in the only slice it never saw, and the timing test is borderline (5 %). Buy-and-hold loses about 27 percentage points to funding, which any long-biased candidate must also pay. Not recorded: where the 13 zero-volume candles and the 36 candles without funding lie; the fee schedule of the account; the verified funding convention. Supports the need for a fixed held-out window before any model comparison: see ADR 0004.

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
