# mlt — research-first ML trading framework

Principle: **nothing enters production code until it has been justified in a notebook and covered by tests.**

## Workflow
1. **Stage 1 – Research (notebooks/)**: data -> baselines -> features/models -> honest validation -> decision.
   Gate: the candidate beats the baselines on a held-out period *after costs*, and is not sensitive to one lucky parameter set.
2. **Stage 2 – Build (src/mlt/)**: module by module, each with unit tests, in dependency order:
   config -> data -> features -> models -> strategy -> risk -> backtest -> execution -> engine.
3. **Parity test**: the same input window must give the same prediction in the notebook, the backtest and the live engine.

Every non-trivial choice (model family, features, instrument, training scheme) is recorded in `docs/decisions/`
with the experiment that supports it. Models are open-ended: linear, NN, gradient boosting, anything — if it is tested.

## Setup
```bash
pip install -e ".[dev]"      # core + tooling
pip install -e ".[torch]"    # only if an experiment needs it
pre-commit install
make test
```

## Safety
`DRY_RUN=true` by default. Live orders need `DRY_RUN=false` **and** `LIVE_TRADING_CONFIRM=YES_I_UNDERSTAND`.
Never commit credentials. Check licensing/eligibility of any venue for your jurisdiction before trading.
