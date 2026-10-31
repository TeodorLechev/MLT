# 0004 – Evaluation protocol: fixed data window and time split
- Status: accepted
- Date: 2026-10-29
- Evidence: tests/test_protocol.py

## Question
How do we compare candidate models without fooling ourselves? The predecessor's parameters were tuned on data that overlaps almost the whole series, so only a short slice is untouched; and the cache grew between two notebook runs (R-001 and R-002 cover slightly different windows), which breaks gate G4 (reproducibility).

## Options considered
1. **Fixed data window and three consecutive time blocks:** development 2023-10-30 22:00 -> 2025-09-30, validation 2025-10-01 -> 2026-04-30, final test 2026-05-01 -> the frozen data end. Tuning and model choice use development and validation only; the final test is evaluated **once**, in notebook 04. Baselines are reported on development and validation; their test-block numbers are produced in notebook 04 together with the final candidate (a clarification made while implementing, so that not even a baseline's test result can steer the design).
2. **Rolling walk-forward with no final block:** every bar is eventually out-of-sample, but nothing is kept untouched, so a choice made after seeing the results leaks.
3. **Use only the slice after 2026-08-01 as the test:** untouched by the predecessor, but about 2,100 bars from one regime: far too short to say anything.

Note (2026-10-29): the first draft said 2023-10-29; the cache used in R-003 starts at 2023-10-30 22:00, so the constant `DATA_START` was set to the real first candle and `require_window` now fails loudly if a cache does not cover the window. Notebook 01 uses the frozen constants, so a re-run reproduces the same cache.

## Experiment
Not a modelling experiment. It is checked by the process: the window constants are fixed in one place and quoted in every R-xxx entry; a notebook never reads data after the frozen end; the test block is not looked at before the selection is final.

## Result
Implemented in `mlt.protocol` (frozen window 2023-10-30 22:00 -> 2026-10-29 08:00 UTC, the three blocks on candle close time, a guard that refuses to read the test block without `allow_test=True`, and a purge of the `horizon` rows before a block for batch training) with 6 unit tests; notebook 02 reads only the frozen window. The per-block baseline table is recorded in [R-003](../RESEARCH_LOG.md). Context: R-002 shows how little a 2.75-year series separates a Sharpe of 0.745 from 0.59 (sampling error near 0.7), so the final block should be as long as possible; option 1 gives about 6 months, which is a minimum and an honest limit of the data.

## Decision and consequences
Accepted by the owner on 2026-10-29 with the boundaries above. Consequences: the data end is frozen to a date written into the research log, the three blocks become constants used by notebooks 03-04, and the final test is run once. Changing a boundary later needs a new ADR that supersedes this one, written before looking at any test-block result.
