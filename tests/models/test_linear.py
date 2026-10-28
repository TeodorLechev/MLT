import numpy as np
import pytest

from mlt.models.linear import OnlineLinear
from mlt.models.online import run_online


def test_update_matches_the_hand_computed_sgd_step():
    m = OnlineLinear(2, lr=0.1, l2=0.5)
    m.w = np.array([1.0, 2.0])
    m.b = 0.5
    m.partial_fit(np.array([[1.0, 1.0]]), np.array([2.0]))
    # err = (1+2+0.5) - 2 = 1.5 ; w -= 0.1*(1.5*x + 0.5*w) ; b -= 0.1*1.5
    assert m.w == pytest.approx([1.0 - 0.1 * (1.5 + 0.5), 2.0 - 0.1 * (1.5 + 1.0)])
    assert m.b == pytest.approx(0.5 - 0.15)


def test_learns_a_linear_relation():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(3000, 2))
    y = X @ np.array([0.5, -0.3]) + 0.1
    m = OnlineLinear(2, lr=0.05).partial_fit(X, y)
    assert m.w == pytest.approx([0.5, -0.3], abs=0.05)
    assert m.predict(np.array([[1.0, 1.0]]))[0] == pytest.approx(0.3, abs=0.05)


def test_state_roundtrip():
    m = OnlineLinear(3, lr=0.01, l2=0.1).partial_fit(np.ones((5, 3)), np.arange(5.0))
    n = OnlineLinear(3)
    n.set_state(m.get_state())
    assert n.predict(np.ones((1, 3)))[0] == pytest.approx(m.predict(np.ones((1, 3)))[0])
    assert (n.lr, n.l2) == (0.01, 0.1)


def test_run_online_prediction_never_uses_unmatured_targets():
    rng = np.random.default_rng(1)
    n, horizon, i = 200, 10, 120
    X = rng.normal(size=(n, 3))
    y = rng.normal(size=n)
    base = run_online(OnlineLinear(3, lr=0.01), X, y, horizon)
    y2 = y.copy()
    y2[i - horizon + 1:] += 100.0          # targets of rows that are NOT matured at step i
    other = run_online(OnlineLinear(3, lr=0.01), X, y2, horizon)
    assert other[i] == pytest.approx(base[i])
    assert not np.allclose(other[i + 1 :], base[i + 1 :])   # later predictions do change


def test_run_online_returns_nan_for_non_finite_features():
    X = np.ones((20, 2))
    X[:3] = np.nan
    preds = run_online(OnlineLinear(2), X, np.zeros(20), horizon=2)
    assert np.isnan(preds[:3]).all() and np.isfinite(preds[3:]).all()
