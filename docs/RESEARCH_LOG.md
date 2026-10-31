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

### R-003 – Baselines under the evaluation protocol: development and validation blocks (2026-10-29)
- **Question:** how do the baselines behave in the development and validation blocks, now that the data window is frozen (ADR 0004), and do the R-002 numbers survive a re-run?
- **Notebook / commit:** notebooks/02_baselines.ipynb @ 2026-10-29 (second run by the owner; the numbers are those printed in that run)
- **Data:** `BTC_USDC-PERPETUAL`, 1h, Deribit public API; the cache held 26,267 candles from 2023-10-30 22:00 to 2026-10-29 08:00 UTC (23 candles fewer at the start than in R-002, because the cache was re-fetched), funding 26,231 observations, 36 candles without funding. Evaluated bars: from 2024-02-03 05:00 UTC (derived from the cache index: warm-up 287 bars plus burn-in 2,000 updates), 23,980 bars in total, of which 14,539 in the development block and 5,088 in the validation block; the test block (the last 4,353 evaluated bars) was **not evaluated**.
- **Setup:** as R-002 (1x leverage, taker 3.5 bp from the gateway, funding sign and timing assumed, predecessor's linear model with its own parameters, no tuning). The predecessor's tuning data (Binance, to 2026-08-01) overlaps both blocks, so neither block is clean for that model.
- **Result** (gateway taker 3.5 bp, funding included):

| Block | Strategy | Total return | Sharpe | Max drawdown | Trades |
|---|---|---|---|---|---|
| Development (14,539 bars) | Buy-and-hold | +133.6 % | 1.28 | -34.8 % | 1 |
| Development | Linear model | +55.8 % | 0.79 | -35.3 % | 99 |
| Validation (5,088 bars) | Buy-and-hold | -34.3 % | -1.28 | -50.9 % | 1 |
| Validation | Linear model | +7.2 % | 0.49 | -31.1 % | 31 |

Whole evaluated period, gateway taker 3.5 bp: buy-and-hold +57.6 % (Sharpe 0.59, drawdown -54.6 %), linear model +91.8 % (Sharpe 0.744, drawdown -35.3 %, 165 trades, 96 % in the market, turnover 60 per year). With +5 bp slippage the linear model gives +76.8 % (Sharpe 0.686); with the predecessor's costs +16.7 % (Sharpe 0.348).

- **Sensitivity:** against R-002 (window starting 23 bars earlier) the main numbers move by 0.3 points or less (buy-and-hold +57.9 % -> +57.6 %, linear +92.1 % -> +91.8 %), but the linear model with +5 bp slippage moves from +78.9 % to +76.8 %: a different start changes the path of an online model by about two points. Funding off: buy-and-hold +84.7 %, linear +109.5 %; one-bar lag: no visible change. Calendar years (gateway taker, funding): 2024 +95.9 % vs +61.6 %; 2025 -9.8 % vs +3.0 %; 2026 to date -11.1 % vs +15.4 %; after 2026-08-01 +25.3 % vs +10.4 % (buy-and-hold vs linear model). Timing test: real Sharpe 0.744, shifted mean -0.083, 5th-95th percentile [-1.065, 0.695], 4.0 % of shifted runs at least as good.
- **Conclusion:** the linear model behaves as a defensive trend follower: it loses to buy-and-hold in the strongly rising development block and in the last three months, and it clearly wins in the falling validation block (+7.2 % against -34.3 %), keeping a positive Sharpe in both blocks (0.79 and 0.49). That is a reference level, not an edge: its parameters were tuned on this data, and a Sharpe of 0.5 over 5,088 bars has a wide error. The bars for a candidate on the validation block are Sharpe 0.49 / drawdown -31.1 % (linear model) and buy-and-hold -1.28 / -50.9 %; how a candidate must beat them is to be defined in notebook 04 before it is looked at. Not recorded: the dates of the 13 zero-volume candles and the 36 candles without funding (the notebook now prints them; ADR 0005); the fee schedule of the account; the verified funding convention.

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
