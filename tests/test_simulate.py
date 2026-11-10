import numpy as np, pytest
from lab04.scenarios import base_scenario
from lab04.simulate import rejection_rates, run_grid

S = base_scenario(np.log(10), 1.0)

def test_erro_tipo_I_perto_de_5():
    r = rejection_rates(np.random.default_rng(42), S, 0.0, n_reps=10_000)
    for t in ("welch", "mann_whitney"):
        assert 0.040 <= r[t] <= 0.060

def test_poder_cresce_com_efeito():
    g = run_grid(np.random.default_rng(42), [S], effects=(0.0, 0.25, 0.5), n_reps=2000)
    for t, sub in g.groupby("test"):
        rates = sub.sort_values("effect").rejection_rate.to_numpy()
        assert np.all(np.diff(rates) > 0) and rates[-1] > rates[0] + 0.3

def test_grade_formato_e_determinismo():
    a = run_grid(np.random.default_rng(1), [S], effects=(0.0, 0.1), n_reps=300)
    b = run_grid(np.random.default_rng(1), [S], effects=(0.0, 0.1), n_reps=300)
    assert len(a) == 1 * 2 * 2
    assert a.equals(b)
    assert (a.ci_low <= a.rejection_rate).all() and (a.rejection_rate <= a.ci_high).all()


# --- Contrato da interface (plano, Task 1.1 da S02) ---

def test_colunas_e_ordem_da_grade():
    g = run_grid(np.random.default_rng(3), [S], effects=(0.0, 0.2), n_reps=100)
    assert list(g.columns) == ["scenario", "scenario_label", "n", "effect", "test",
                               "rejection_rate", "ci_low", "ci_high", "n_reps"]
    assert list(g.effect) == [0.0, 0.0, 0.2, 0.2]
    assert list(g.test) == ["welch", "mann_whitney"] * 2
    assert (g.scenario == "base").all() and (g.n == 30).all() and (g.n_reps == 100).all()

def test_ic_cortado_em_0_e_1():
    g = run_grid(np.random.default_rng(4), [S], effects=(0.0, 0.9), n_reps=50)
    assert (g.ci_low >= 0).all() and (g.ci_high <= 1).all()

def test_chaves_sao_os_dois_testes():
    r = rejection_rates(np.random.default_rng(5), S, 0.0, n_reps=50)
    assert set(r) == {"welch", "mann_whitney"}
