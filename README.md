# mlt — research-first ML trading framework for crypto perpetuals

> **mlt** is a framework for designing, *proving* and only then running a machine-learning trading strategy on a crypto perpetual. Every component is first justified in a research notebook and then built as a unit-tested module. Nothing is trusted because it "seems reasonable"; it is trusted because evidence is linked in this repository.

## Current status

<!-- BEGIN:auto:status -->
| | |
|---|---|
| **Current phase** | P1 – Research (in progress) |
| **Last synced** | 2026-10-24 |
| **Tests** | 37 passed, 0 failed |
| **Modules done** | 3 / 9 |
| **Decisions** | 0 accepted · 3 proposed · 0 rejected |
<!-- END:auto:status -->

**Focus now / next step:** see [docs/STATUS.md](docs/STATUS.md#current-focus) (kept in sync with every change).

## 1. Goals, non-goals and constraints

**Goals**
- Establish, with honest out-of-sample evidence, whether an ML model has a net-of-cost edge on the instrument we actually trade.
- Run *the same code* in research, backtest and live (parity), so a result in a notebook means something in production.
- Keep models, data venues and brokers swappable behind small contracts, so a better idea or a legal change never forces a rewrite.

**Non-goals**
- Guaranteed profit, high-frequency trading, or trading on any venue that is not legally accessible to the operator.

**Constraints and why they exist**

| Constraint | Why |
|---|---|
| Venue must be legally accessible from the operator's jurisdiction (Bulgaria / EU) | Binance withdrew its MiCA application and suspended EU derivatives from 2026-07-01 (secondary sources). Coinbase is the chosen venue ([ADR 0002](docs/decisions/0002-execution-venue.md), `proposed` until eligibility for Bulgaria is verified). Evidence: [docs/evidence](docs/evidence/venue-availability-2026-10-23.md). |
| Research instrument = traded instrument | In the predecessor project research used Binance spot BTCUSDT while the live bot traded a different perpetual; fees, funding and price series differ, so results did not transfer. |
| Only features that exist live | The predecessor's neural network used Binance-only fields that the live feed does not provide. |
| `DRY_RUN=true` by default | A mistake in configuration must never be able to place a real order. |

## 2. How we work (research-first)

1. **Stage 1 – Research (`notebooks/`)**: data → baselines → features/models → honest validation → decision.
   *Why:* an idea is cheap to test in a notebook and expensive to unwind from production code.
2. **Research gate** (all must hold): **G1** beats the baselines on a held-out period after costs and funding; **G2** is not sensitive to one lucky parameter set; **G3** uses only features available live; **G4** is reproducible from cached data and fixed seeds.
   *Why:* the predecessor's results were tuned and tested on the same period; the gate prevents that.
3. **Stage 2 – Build (`src/`)**: module by module in dependency order, each with unit tests, merged only when tests are green.
4. **Parity test**: the same input window must give the same prediction in the notebook, the backtest and the live engine.
5. **Decisions are evidence-based**: every non-trivial choice (model family, features, instrument, training scheme) is an ADR in [docs/decisions](docs/decisions/README.md) and is `accepted` only with a link to the experiment. Any model family may compete: linear, NN, gradient boosting, sequence models.

## 3. Roadmap

<!-- BEGIN:auto:phases -->
| Phase | Goal | Gate (exit criteria) | Status |
|---|---|---|---|
| P0 – Foundation | Repository skeleton, CI, config, candle schema, model contract. | Skeleton installs, lint is clean, unit tests pass in CI. | done |
| P1 – Research | Show with out-of-sample evidence whether a model has a net-of-cost edge on the traded instrument. | G1 beats baselines on a held-out period after costs and funding; G2 stable to parameter changes; G3 uses only features available live; G4 reproducible from cached data and fixed seeds. | in progress |
| P2 – Build | Implement the validated design module by module, each with unit tests. | All modules done; parity test (notebook = backtest = live engine) green; backtest reproduces notebook 04. | not started |
| P3 – Paper trading | Run the full engine on live data without orders. | Signals and PnL match the backtest within a tolerance defined in an ADR before the run starts. | not started |
| P4 – Live, minimal size | Trade real money with the smallest meaningful size and all risk limits on. | Defined in an ADR before go-live; requires written venue eligibility check. | not started |
<!-- END:auto:phases -->

## 4. Project structure

<!-- BEGIN:auto:modules -->
| Module | What it does | Status | Tests |
|---|---|---|---|
| `config` | Typed settings from environment; dry-run is the default, live needs an explicit confirmation phrase. | done | 4 |
| `data` | Candle providers (Deribit, Coinbase), one canonical OHLCV schema, validation, parquet cache. | done | 31 |
| `features` | Pure feature functions, identical in research, backtest and live (no look-ahead). | stub | 0 |
| `models` | Model-agnostic Forecaster contract plus the models that won experiments. | done | 2 |
| `strategy` | Turns predictions into target positions (thresholds, cost filter). | stub | 0 |
| `risk` | Position limits, daily loss halt, liquidation distance. | stub | 0 |
| `backtest` | Walk-forward simulation with fees, slippage and funding; must reproduce notebook results. | stub | 0 |
| `execution` | Broker contract with a paper broker and the venue adapter; dry-run by default. | stub | 0 |
| `engine` | Wires data -> features -> model -> strategy -> risk -> execution into one live loop. | stub | 0 |
<!-- END:auto:modules -->

Module contracts and data flow: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 5. Notebooks

<!-- BEGIN:auto:notebooks -->
| Notebook | Purpose | Status |
|---|---|---|
| [00_colab_bootstrap.ipynb](notebooks/00_colab_bootstrap.ipynb) | 00 – Colab bootstrap: Run this first in Google Colab (needed only for experiments that require PyTorch/GPU). | not started |
| [01_data.ipynb](notebooks/01_data.ipynb) | 01 – Data: Goal: load the perpetual we will actually trade, validate it, cache it. Checks: gaps, duplicates, closed candles only, UTC. Add funding rates. | in progress |
| [02_baselines.ipynb](notebooks/02_baselines.ipynb) | 02 – Baselines: Buy-and-hold, flat, and the previous linear model on the NEW data, with costs. | not started |
| [03_features_model.ipynb](notebooks/03_features_model.ipynb) | 03 – Features and models: Only features that exist live. Compare model families fairly (same data, costs, splits). | not started |
| [04_validation.ipynb](notebooks/04_validation.ipynb) | 04 – Validation: Tune on an early window; test ONCE on a held-out later window. Costs and funding included. | not started |
| [05_decision.ipynb](notebooks/05_decision.ipynb) | 05 – Decision: Does the candidate pass the research gate? Summarise evidence and update docs/decisions. | not started |
<!-- END:auto:notebooks -->

Experiment results with numbers, data period and costs: [docs/RESEARCH_LOG.md](docs/RESEARCH_LOG.md).

## 6. Decisions and evidence

<!-- BEGIN:auto:decisions -->
| ID | Decision | Status | Evidence |
|---|---|---|---|
| [0001](docs/decisions/0001-model-stack.md) | Model stack (NumPy core vs PyTorch) | proposed | – |
| [0002](docs/decisions/0002-execution-venue.md) | Execution venue | proposed | [docs/evidence/venue-availability-2026-10-23.md](docs/evidence/venue-availability-2026-10-23.md) |
| [0003](docs/decisions/0003-instrument-and-data-source.md) | Traded instrument and research data source | proposed | [docs/evidence/venue-availability-2026-10-23.md](docs/evidence/venue-availability-2026-10-23.md) |
<!-- END:auto:decisions -->

## 7. Recent changes

<!-- BEGIN:auto:changes -->
**2026-10-24**
- **Added:** evidence E28 - the Derivatives Exchange desk does not handle retail questions; V2 to be retried through retail support
- **Added:** evidence E29 - key terms of the Coinbase Bermuda User Agreement (Part A) that apply to the owner's Global Derivatives account
- **Added:** evidence E30-E33 (Coinbase Bermuda agreement Parts B, D and Appendix 4: EEA clients are CBBM clients with a Luxembourg pledge, orders execute only on Deribit, market-data storage restriction, version differences)
- **Added:** Deribit public provider (candles, funding, instrument spec) with retries, pagination and canonical close-time index; parquet cache with incremental download and atomic writes; find_gaps in the schema module
- **Added:** 18 unit tests for the provider, the cache and gap detection (fake HTTP session, no network)
- **Added:** notebooks/01_data with working cells for spec check, candles, quality checks and funding (status in progress; to be run by the owner)
- **Added:** evidence E34 (Deribit Terms of Service: personal use only)
- **Docs:** STATUS next step 1 names the correct channel
- **Docs:** STATUS risks on contract terms and on market-data licensing
- **Docs:** STATUS next step 3 and data-licensing risk updated
- **Changed:** V1 now asks the owner to confirm the entity from the onboarding screen or e-mail and to read Part D (country-specific terms)
- **Changed:** V1 now names Coinbase Bermuda Ltd with Luxembourg custody as the serving entity, pending the owner's confirmation; ADR 0002 and 0003 updated

**2026-10-23**
- **Added:** docs/evidence/venue-availability-2026-10-23.md - sourced review of Binance, Coinbase and Deribit availability for a Bulgarian resident, with verification checklist V1-V3
- **Added:** ADR 0003 (traded instrument and research data source), proposed
- **Added:** evidence E14-E19 and a comparison of EU-authorised derivatives routes (Coinbase, Kraken, OKX) in docs/evidence
- **Added:** evidence E20 (owner's Coinbase account shows BTC_USDC-PERPETUAL on the Global Derivatives portfolio); V1 partly done
- **Added:** evidence E21-E24 (Coinbase help: Global Derivatives served by Coinbase Bermuda Ltd for unlisted jurisdictions; EU-licensed product is the US derivatives offering via CBFSE; developer-docs answers)
- **Added:** evidence E25-E27 (Coinbase Derivatives rulebook: BIP contract specification; EEA user agreement scope)
- **Changed:** ADR 0002 renamed to 'Execution venue'; owner chose Coinbase on 2026-10-23, kept proposed until eligibility for Bulgaria is verified
- **Changed:** ADR 0002 now has an explicit decision rule and Kraken/OKX as ranked fallbacks; verification checklist gets V4
- **Changed:** evidence E15 verified from Coinbase's own page - true perpetuals for EEA users are served by non-EEA affiliates, not under an EU licence
- **Changed:** ADR 0002/0003 now require the EU-licensed Coinbase product to pass V1-V3 (incl. API); Global Derivatives perpetual demoted to an option needing the owner's own legal check
- **Changed:** ADR 0003 notes the hypothesis that Deribit public candles of the same contract are the traded series, to be verified in 01_data
- **Changed:** V1 narrowed to confirming the entity in the owner's agreement; V2 not answered by the docs assistant; V3 partly answered
- **Changed:** ADR 0003 option 1 records the contract mechanics; V1 points to the derivatives agreement, not the EEA user agreement
- **Docs:** STATUS next steps and open questions rewritten around checks V1-V3; README constraints updated
- **Docs:** STATUS open questions note that the current Coinbase derivatives may be served by a non-EU entity
- **Docs:** STATUS risks updated (legal path and API path at Coinbase may not coincide)
- **Docs:** STATUS risk about over-broad API key permissions
- **Docs:** ADR 0002 and 0003 describe the two Coinbase routes by entity
- **Docs:** STATUS risk about the history and mechanics of the EU-licensed contract

**2026-10-22**
- **Added:** project skeleton (config, canonical candle schema, Forecaster contract) with 19 unit tests, CI and pre-commit
- **Added:** research notebooks 00-05 as outlines with explicit status lines
- **Added:** decision records 0001 (model stack, proposed) and 0002 (traded instrument and venue, proposed)
- **Docs:** documentation system - README, STATUS, ARCHITECTURE, RESEARCH_LOG, CHANGELOG, decisions with an evidence rule
- **Fixed:** removed two stray empty directories from the first skeleton archive

Full history: [docs/CHANGELOG.md](docs/CHANGELOG.md).
<!-- END:auto:changes -->

## 8. Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"      # core + tooling
pip install -e ".[torch]"    # only if an experiment needs it (see docs/decisions)
pre-commit install
make test                    # unit tests
make notebook                # JupyterLab
```
Heavy experiments (PyTorch/GPU) run in Google Colab via `notebooks/00_colab_bootstrap.ipynb`; the package is installed from this repository so Colab and local runs use the same code.

## 9. Safety, legal and disclaimers

- Live orders require **both** `DRY_RUN=false` **and** `LIVE_TRADING_CONFIRM=YES_I_UNDERSTAND`.
- Never commit credentials; key files live outside the repository.
- Venue availability and licensing differ per jurisdiction: verify eligibility yourself before trading. Nothing here is financial advice; trading can lose all invested capital.

## 10. Documentation map

| Document | Purpose |
|---|---|
| [docs/STATUS.md](docs/STATUS.md) | Current state, focus, next steps with reasons, open questions |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Modules, contracts, data flow, parity principle |
| [docs/RESEARCH_LOG.md](docs/RESEARCH_LOG.md) | Every experiment: setup, numbers, conclusion, link to notebook |
| [docs/decisions/README.md](docs/decisions/README.md) | Decision records (ADRs) and their evidence |
| [docs/evidence/](docs/evidence/venue-availability-2026-10-23.md) | Sources and verification checklist behind the venue decision |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Dated history of changes |
