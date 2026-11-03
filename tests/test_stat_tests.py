import json

import numpy as np, pytest
from lab04.stat_tests import welch, mann_whitney, welch_pvalues, mann_whitney_pvalues, TestResult


# --- Plano mestre, Sprint 01 Task 1.2 ---

def test_welch_valores_conhecidos():
    r = welch(np.array([1., 2, 3, 4, 5]), np.array([2., 3, 4, 5, 6]))
    assert r.statistic == pytest.approx(-1.0)
    assert r.p_value == pytest.approx(0.3466, abs=1e-4)
    assert r.df == pytest.approx(8.0)
    assert r.effect_size == pytest.approx(-0.6325, abs=1e-4)
    assert r.reject is False

def test_mann_whitney_valores_conhecidos():
    r = mann_whitney(np.array([1., 2, 3]), np.array([4., 5, 6]))
    assert r.statistic == 0.0
    assert r.p_value == pytest.approx(0.1)
    assert r.effect_size == pytest.approx(-1.0)

def test_vetorizado_igual_ao_escalar():
    rng = np.random.default_rng(0)
    A, B = rng.lognormal(size=(50, 30)), rng.lognormal(size=(50, 30))
    pw, pm = welch_pvalues(A, B), mann_whitney_pvalues(A, B)
    assert pw.shape == pm.shape == (50,)
    assert pw[7] == pytest.approx(welch(A[7], B[7]).p_value)
    assert pm[7] == pytest.approx(mann_whitney(A[7], B[7]).p_value)

def test_roundtrip_dict():
    r = welch(np.array([1., 2, 3, 4]), np.array([2., 3, 5, 9]))
    assert TestResult.from_dict(r.to_dict()) == r


# --- Review Focus do plano da Issue #2 ---

def test_to_dict_serializa_em_json():
    a, b = np.array([1., 2, 3, 4]), np.array([2., 3, 5, 9])
    for r in (welch(a, b), mann_whitney(a, b)):
        assert TestResult.from_dict(json.loads(json.dumps(r.to_dict()))) == r
        assert type(r.reject) is bool and type(r.p_value) is float and type(r.n_a) is int

def test_reject_respeita_alpha():
    a, b = np.array([1., 2, 3, 4, 5]), np.array([2., 3, 4, 5, 6])
    assert welch(a, b, alpha=0.5).reject is True  # p ≈ 0,3466
    assert mann_whitney(np.array([1., 2, 3]), np.array([4., 5, 6]), alpha=0.2).reject is True  # p = 0,1

def test_sinal_do_efeito():
    a, b = np.array([10., 11, 12, 13, 14]), np.array([1., 2, 3, 4, 5])
    assert welch(a, b).effect_size > 0
    assert mann_whitney(a, b).effect_size == pytest.approx(1.0)

def test_mann_whitney_com_empates():
    r = mann_whitney(np.array([1., 1, 2, 2, 3]), np.array([2., 2, 3, 3, 4]))
    assert np.isfinite(r.p_value) and -1 <= r.effect_size <= 1
