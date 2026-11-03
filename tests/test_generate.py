import dataclasses

import numpy as np
import pytest

from lab04.generate import generate_groups
from lab04.scenarios import Scenario, base_scenario

S = base_scenario(mu=np.log(10), sigma=1.0)


def test_base_scenario():
    assert S == Scenario("base", "Base (lognormal ajustada, n=30)", 30, np.log(10), 1.0)


def test_scenario_imutavel():
    with pytest.raises(dataclasses.FrozenInstanceError):
        S.n = 5


def test_formato():
    A, B = generate_groups(np.random.default_rng(1), S, 0.0, n_reps=7)
    assert A.shape == B.shape == (7, 30)


def test_efeito_reduz_mediana():
    A, B = generate_groups(np.random.default_rng(1), S, 0.5, n_reps=4000)
    assert np.median(A) == pytest.approx(10, rel=0.05)
    assert np.median(B) == pytest.approx(5, rel=0.05)


def test_efeito_zero_mesma_mediana():
    A, B = generate_groups(np.random.default_rng(1), S, 0.0, n_reps=4000)
    assert np.median(B) == pytest.approx(np.median(A), rel=0.05)


def test_mesma_semente_mesmos_dados():
    x = generate_groups(np.random.default_rng(42), S, 0.2, 3)
    y = generate_groups(np.random.default_rng(42), S, 0.2, 3)
    assert np.array_equal(x[0], y[0]) and np.array_equal(x[1], y[1])


def test_outliers_positivos_e_finitos():
    s = Scenario("outliers", "Outliers", 30, np.log(10), 1.0, outlier_frac=0.05)
    A, B = generate_groups(np.random.default_rng(3), s, 0.3, 2000)
    for X in (A, B):
        assert np.all(np.isfinite(X)) and np.all(X > 0)
    assert (A > np.quantile(A, 0.5) * 10).mean() > 0.02


@pytest.mark.parametrize("effect", [1.0, 1.5, -0.1, float("nan")])
def test_efeito_invalido(effect):
    with pytest.raises(ValueError):
        generate_groups(np.random.default_rng(0), S, effect)
