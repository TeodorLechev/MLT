"""Online linear regression trained by SGD with L2 (the predecessor's model, as a baseline).

Update on one sample: err = w.x + b - y; w -= lr * (err * x + l2 * w); b -= lr * err.
It is a baseline, not a recommendation: the model family is chosen by experiment (ADR 0001).
"""
from __future__ import annotations

import numpy as np

from .base import Forecaster


class OnlineLinear(Forecaster):
    def __init__(self, n_features: int, lr: float = 0.001, l2: float = 0.0) -> None:
        self.w = np.zeros(n_features, dtype=float)
        self.b = 0.0
        self.lr = lr
        self.l2 = l2

    def predict(self, x: np.ndarray) -> np.ndarray:
        x = np.atleast_2d(np.asarray(x, dtype=float))
        return x @ self.w + self.b

    def partial_fit(self, X: np.ndarray, y: np.ndarray) -> OnlineLinear:
        for xi, yi in zip(np.atleast_2d(np.asarray(X, dtype=float)), np.asarray(y, dtype=float).reshape(-1)):
            err = float(np.dot(self.w, xi) + self.b) - float(yi)
            self.w -= self.lr * (err * xi + self.l2 * self.w)
            self.b -= self.lr * err
        return self

    def get_state(self) -> dict:
        return {"w": self.w.tolist(), "b": self.b, "lr": self.lr, "l2": self.l2}

    def set_state(self, state: dict) -> None:
        self.w = np.asarray(state["w"], dtype=float)
        self.b = float(state["b"])
        self.lr = float(state["lr"])
        self.l2 = float(state["l2"])
