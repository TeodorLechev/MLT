# 0005 – Data handling: zero-volume candles and missing funding
- Status: accepted
- Date: 2026-10-29
- Evidence: tests/data/test_schema.py

## Question
How are the 13 zero-volume candles and the 36 candles without a funding observation (R-001, R-002, R-003) treated in research?

## Options considered
1. **Keep and flag.** A zero-volume candle is a valid closed candle; it stays in the series. A missing funding value counts as zero funding for that bar, and the number of such bars is reported with every result.
2. **Drop the affected bars.** This breaks the regular hourly grid that features and the accounting rely on.
3. **Fill (forward-fill or interpolate).** Invents data that no one traded or paid; rejected.

## Experiment
Not a modelling experiment. Checked by tests: a zero-volume candle passes validation and is not dropped (`tests/data/test_schema.py::test_zero_volume_candle_is_valid_and_kept`); the accounting counts missing funding and does not hide it (`tests/test_evaluation.py::test_funding_long_pays_short_receives_and_missing_is_counted`).

## Result
At most 13 + 36 of about 26,300 bars (0.19 % of the series, 0.14 % for funding). Notebook 02 now prints the dates of both groups so that clusters can be spotted; the effect on results was not measured separately (not recorded).

## Decision and consequences
Option 1, accepted by the owner on 2026-10-29. Revisit if the printed dates show clusters inside the evaluated window or if funding turns out to be missing in a pattern that matters (for example around large moves).
