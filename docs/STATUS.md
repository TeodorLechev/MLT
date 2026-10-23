# Project status

Single place that answers "where are we, what is next and why". Tables are generated from the code, tests, notebooks and decision records (`<!-- auto -->` blocks, do not edit by hand); the sections below them are maintained by hand at every sync.

<!-- BEGIN:auto:status -->
| | |
|---|---|
| **Current phase** | P1 – Research (in progress) |
| **Last synced** | 2026-10-23 |
| **Tests** | 19 passed, 0 failed |
| **Modules done** | 3 / 9 |
| **Decisions** | 0 accepted · 3 proposed · 0 rejected |
<!-- END:auto:status -->

## Current focus

Phase **P1 – Research** has just started; the foundation (P0) is done. No experiment has been run yet, so **no performance claim is made anywhere in this repository**. The owner decided on 2026-10-23 to use **Coinbase** as the execution venue ([ADR 0002](decisions/0002-execution-venue.md)). That decision stays `proposed` until the eligibility checks V1–V3 in the [evidence file](evidence/venue-availability-2026-10-23.md) are done, because Bulgaria is not confirmed in any public source. Which instrument is traded, and therefore which series the research uses, follows from those checks ([ADR 0003](decisions/0003-instrument-and-data-source.md)).

## Next steps

Each step states **why** it is needed and its **exit criterion**, so progress is checkable.

| # | Step | Why it is needed | Done when |
|---|---|---|---|
| 1 | Run checks V1–V3 with Coinbase (derivatives available for the account, serving entity and product, API access) | Coinbase is chosen, but eligibility for a Bulgarian resident and API access are unverified; trading where it is not allowed is not an option | V1–V3 results recorded in the evidence file; ADR 0002 `accepted`; if the checks fail, V4 (Kraken, then OKX) is run before any research is finalised |
| 2 | Choose the traded instrument and research data source ([ADR 0003](decisions/0003-instrument-and-data-source.md)) | Research must use the instrument that will be traded; funding, settlement and leverage differ between the candidate products | ADR 0003 `accepted` with the measured proxy difference, if a proxy is used |
| 3 | Candle provider + funding history in `01_data` | Every later result depends on clean, reproducible data | Notebook 01 `done`; cache reproducible; schema tests green |
| 4 | Baselines in `02_baselines` (buy-and-hold, flat, linear model) with costs | These are the bars any candidate must beat (gate G1) | Notebook 02 `done`; numbers in the research log (R-001) |

## Open questions and risks

| Question / risk | Impact | Owner / how we resolve it |
|---|---|---|
| Is Bulgaria among the 26 countries where Coinbase offers EEA derivatives, and is the owner's account eligible? | Hard blocker for paper/live (P3/P4) and for choosing the research instrument | Owner runs V1–V2; result in the [evidence file](evidence/venue-availability-2026-10-23.md) |
| Can the EEA "perpetual-style" future be traded through the API, or only the Global Derivatives gateway? | Decides the broker adapter and what data can be cached. If the EU-licensed product has no API, an automated strategy cannot run legally at Coinbase and Kraken/OKX become the plan | V3; Coinbase docs or support |
| Coinbase states that true perpetual futures for EEA users come from non-EEA affiliates, not under an EU licence (E15); only the CySEC futures product is EU-licensed (E4). The owner's current derivatives may be served by the non-EU route | Legal basis and traded product may differ from what the research assumes | V1 names the entity; use the EU-licensed product or a fallback venue |
| The owner's Coinbase API key carries `transfer` and `export` permissions in addition to `trade` and `view` | A leaked key could move funds; a trading bot needs only `view` and `trade` | Create a separate key with `view` + `trade` for the bot before any automated run; keep it outside the repository |
| Binance status rests on secondary sources only | Low; Binance is excluded either way | Optionally confirm against Binance's own notice |
| Coinbase API for derivatives changed on 2026-10-01 (JSON-RPC 2.0 gateway, no parallel run) | Any code written against the old INTX REST endpoints must be rewritten | Execution adapter is built only after ADR 0002 is accepted |
| Model family is open (linear, NN, boosting, sequence) | Avoid anchoring on the predecessor's setup | Compared fairly in `03_features_model`; tracked in [ADR 0001](decisions/0001-model-stack.md) |

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
| [0002](decisions/0002-execution-venue.md) | Execution venue | proposed | [docs/evidence/venue-availability-2026-10-23.md](../docs/evidence/venue-availability-2026-10-23.md) |
| [0003](decisions/0003-instrument-and-data-source.md) | Traded instrument and research data source | proposed | [docs/evidence/venue-availability-2026-10-23.md](../docs/evidence/venue-availability-2026-10-23.md) |
<!-- END:auto:decisions -->
