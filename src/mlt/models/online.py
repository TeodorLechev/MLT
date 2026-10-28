"""Causal walk-forward training protocol for online models.

At step ``i`` the model is updated with the sample that has just MATURED, i.e. row ``i - horizon``
(its target, a return over ``horizon`` bars, is only known from bar ``i`` on), and then predicts
row ``i``. Hence the prediction at ``i`` uses no information from after bar ``i``.
"""
from __future__ import annotations

import numpy as np

from .base import Forecaster


def run_online(model: Forecaster, X: np.ndarray, y: np.ndarray, horizon: int) -> np.ndarray:
    """Return one prediction per row (NaN where the feature row is not finite)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(X)
    preds = np.full(n, np.nan)
    for i in range(n):
        j = i - horizon
        if j >= 0 and np.isfinite(y[j]) and np.all(np.isfinite(X[j])):
            model.partial_fit(X[j : j + 1], y[j : j + 1])
        if np.all(np.isfinite(X[i])):
            preds[i] = model.predict(X[i : i + 1])[0]
    return preds
