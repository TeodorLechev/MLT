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
