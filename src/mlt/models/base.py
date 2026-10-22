"""Model contract. Deliberately model-agnostic so ANY approach can compete fairly:
online linear, small NN, gradient boosting, sequence models, ...

A model is chosen only by experiment (see docs/decisions), never by habit.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class Forecaster(ABC):
    """Predicts a forward return from a feature row."""

    @abstractmethod
    def predict(self, x: np.ndarray) -> np.ndarray:
        """x: (n_samples, n_features) -> (n_samples,) predictions."""

    def fit(self, X: np.ndarray, y: np.ndarray) -> Forecaster:
        """Batch training (optional). Default: not supported."""
        raise NotImplementedError(f"{type(self).__name__} does not support fit()")

    def partial_fit(self, X: np.ndarray, y: np.ndarray) -> Forecaster:
        """Online update on matured samples (optional). Default: not supported."""
        raise NotImplementedError(f"{type(self).__name__} does not support partial_fit()")

    @abstractmethod
    def get_state(self) -> dict:
        """Serializable state so live can resume instead of retraining from scratch."""

    @abstractmethod
    def set_state(self, state: dict) -> None:
        """Restore state produced by get_state()."""
