import numpy as np
import pytest

from mlt.models import Forecaster


class Dummy(Forecaster):
    def predict(self, x):
        return np.zeros(len(x))

    def get_state(self):
        return {}

    def set_state(self, state):
        pass


def test_optional_training_not_supported_by_default():
    m = Dummy()
    with pytest.raises(NotImplementedError):
        m.fit(np.zeros((2, 1)), np.zeros(2))
    with pytest.raises(NotImplementedError):
        m.partial_fit(np.zeros((2, 1)), np.zeros(2))


def test_cannot_instantiate_abstract():
    with pytest.raises(TypeError):
        Forecaster()
