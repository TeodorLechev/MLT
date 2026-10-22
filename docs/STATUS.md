# Project status

Single place that answers "where are we, what is next and why". Tables are generated from the code, tests, notebooks and decision records (`<!-- auto -->` blocks, do not edit by hand); the sections below them are maintained by hand at every sync.

<!-- BEGIN:auto:status -->
| | |
|---|---|
| **Current phase** | P1 – Research (in progress) |
| **Last synced** | 2026-10-22 |
| **Tests** | 19 passed, 0 failed |
| **Modules done** | 3 / 9 |
| **Decisions** | 0 accepted · 2 proposed · 0 rejected |
<!-- END:auto:status -->

## Current focus

Phase **P1 – Research** has just started. The foundation (P0) is done: config, canonical candle schema and the model contract are implemented and tested. No experiment has been run yet, so **no performance claim is made anywhere in this repository**. The immediate goal is to fix the traded instrument and build the data foundation (`01_data`) that every later experiment depends on.

## Next steps

Each step states **why** it is needed and its **exit criterion**, so progress is checkable.

| # | Step | Why it is needed | Done when |
|---|---|---|---|
| 1 | Choose the traded instrument and data venue ([ADR 0002](decisions/0002-venue-and-instrument.md)) | Research must use the instrument that will be traded; costs and funding differ per venue | ADR 0002 `accepted` with evidence, venue eligibility confirmed |
| 2 | Candle provider + funding history in `01_data` | Every later result depends on clean, reproducible data | Notebook 01 `done`; cache reproducible; schema tests green |
| 3 | Baselines in `02_baselines` (buy-and-hold, flat, linear model) with costs | These are the bars any candidate must beat (gate G1) | Notebook 02 `done`; numbers in the research log (R-001) |

## Open questions and risks

| Question / risk | Impact | Owner / how we resolve it |
|---|---|---|
| Which instrument is executed on the venue (Deribit `BTC-PERPETUAL` data vs the Coinbase Global Derivatives perpetual)? | Costs, funding and symbol mapping differ, so results may not transfer | Owner decides; tracked in [ADR 0002](decisions/0002-venue-and-instrument.md), must be settled before notebook 02 |
| Is the chosen venue legally open to a Bulgarian / EU resident? | Hard blocker for P3/P4 (paper and live) | Owner confirms in writing with the venue before go-live; not verified by this project |
| Model family is open (linear, NN, boosting, sequence) | Avoid anchoring on the predecessor's linear/NN setup | Compared fairly in `03_features_model`; tracked in [ADR 0001](decisions/0001-model-stack.md) |

## Modules

<!-- BEGIN:auto:modules -->
| Module | What it does | Status | Tests |
|---|---|---|---|
| `config` | Typed settings from environment; dry-run is the default, live needs an explicit confirmation phrase. | done | 4 |
| `data` | Candle providers (Deribit, Coinbase), one canonical OHLCV schema, validation, parquet cache. | done | 13 |
| `features` | Pure feature functions, identical in research, backtest and live (no look-ahead). | stub | 0 |
| `models` | Model-agnostic Forecaster contract plus the models that won experiments. | done | 2 |
| `strategy` | Turns predictions into target positions (thresholds, cost filter). | stub | 0 |
| `risk` | Position limits, daily loss halt, liquidation distance. | stub | 0 |
| `backtest` | Walk-forward simulation with fees, slippage and funding; must reproduce notebook results. | stub | 0 |
| `execution` | Broker contract with a paper broker and the venue adapter; dry-run by default. | stub | 0 |
| `engine` | Wires data -> features -> model -> strategy -> risk -> execution into one live loop. | stub | 0 |
<!-- END:auto:modules -->

## Notebooks

<!-- BEGIN:auto:notebooks -->
| Notebook | Purpose | Status |
|---|---|---|
| [00_colab_bootstrap.ipynb](../notebooks/00_colab_bootstrap.ipynb) | 00 – Colab bootstrap: Run this first in Google Colab (needed only for experiments that require PyTorch/GPU). | not started |
| [01_data.ipynb](../notebooks/01_data.ipynb) | 01 – Data: Goal: load the perpetual we will actually trade, validate it, cache it. | not started |
| [02_baselines.ipynb](../notebooks/02_baselines.ipynb) | 02 – Baselines: Buy-and-hold, flat, and the previous linear model on the NEW data, with costs. | not started |
| [03_features_model.ipynb](../notebooks/03_features_model.ipynb) | 03 – Features and models: Only features that exist live. Compare model families fairly (same data, costs, splits). | not started |
| [04_validation.ipynb](../notebooks/04_validation.ipynb) | 04 – Validation: Tune on an early window; test ONCE on a held-out later window. Costs and funding included. | not started |
| [05_decision.ipynb](../notebooks/05_decision.ipynb) | 05 – Decision: Does the candidate pass the research gate? Summarise evidence and update docs/decisions. | not started |
<!-- END:auto:notebooks -->

## Decisions

<!-- BEGIN:auto:decisions -->
| ID | Decision | Status | Evidence |
|---|---|---|---|
| [0001](decisions/0001-model-stack.md) | Model stack (NumPy core vs PyTorch) | proposed | – |
| [0002](decisions/0002-venue-and-instrument.md) | Traded instrument and data venue | proposed | – |
<!-- END:auto:decisions -->
