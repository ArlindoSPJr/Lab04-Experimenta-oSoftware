import numpy as np, pandas as pd, pytest
from lab04.scenarios import base_scenario
from lab04.simulate import rejection_rates, run_grid

S = base_scenario(np.log(10), 1.0)

def test_erro_tipo_I_perto_de_5():
    # Lognormal com sigma=0.1 e quase normal: os dois testes precisam ficar em ~5%.
    quase_normal = base_scenario(np.log(10), 0.1)
    r = rejection_rates(np.random.default_rng(42), quase_normal, 0.0, n_reps=10_000)
    for t in ("welch", "mann_whitney"):
        assert 0.040 <= r[t] <= 0.060

def test_assimetria_deixa_welch_conservador():
    # Com sigma=1 o MW (livre de distribuicao) segue em ~5%; o Welch cai abaixo.
    r = rejection_rates(np.random.default_rng(42), S, 0.0, n_reps=10_000)
    assert 0.040 <= r["mann_whitney"] <= 0.060
    assert r["welch"] < 0.045

def test_poder_cresce_com_efeito():
    g = run_grid(np.random.default_rng(42), [S], effects=(0.0, 0.25, 0.5), n_reps=2000)
    for t, sub in g.groupby("test"):
        rates = sub.sort_values("effect").rejection_rate.to_numpy()
        assert np.all(np.diff(rates) > 0) and rates[-1] > rates[0] + 0.3

def test_grade_formato_e_determinismo():
    a = run_grid(np.random.default_rng(1), [S], effects=(0.0, 0.1), n_reps=300)
    b = run_grid(np.random.default_rng(1), [S], effects=(0.0, 0.1), n_reps=300)
    assert len(a) == 2 * 1 * 2 * 2          # alfas × cenários × efeitos × testes
    assert a.equals(b)
    assert (a.ci_low <= a.rejection_rate).all() and (a.rejection_rate <= a.ci_high).all()


# --- Contrato da interface (plano, Task 1.1 da S02) ---

def test_colunas_e_ordem_da_grade():
    # #48: a grade ganhou a coluna `alpha`; com um só alfa a ordem continua cenário → efeito → teste
    g = run_grid(np.random.default_rng(3), [S], effects=(0.0, 0.2), n_reps=100, alphas=(0.05,))
    assert list(g.columns) == ["scenario", "scenario_label", "n", "effect", "alpha", "test",
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


# --- #48: alfa = 0,01 com os mesmos lotes do alfa = 0,05 ---

def test_grade_tem_os_dois_alfas_em_blocos():
    from lab04.config import ALPHAS
    assert ALPHAS == (0.05, 0.01)
    g = run_grid(np.random.default_rng(6), [S], effects=(0.0, 0.2), n_reps=200)
    assert list(dict.fromkeys(g.alpha)) == [0.05, 0.01]
    assert (g.alpha.value_counts() == 4).all()

def test_alfa_005_igual_a_grade_so_com_005():
    so_005 = run_grid(np.random.default_rng(7), [S], effects=(0.0, 0.2), n_reps=300, alphas=(0.05,))
    dois = run_grid(np.random.default_rng(7), [S], effects=(0.0, 0.2), n_reps=300)
    pd.testing.assert_frame_equal(dois[dois.alpha == 0.05].reset_index(drop=True), so_005)

def test_taxa_001_nunca_maior_que_005():
    g = run_grid(np.random.default_rng(8), [S], effects=(0.0, 0.3, 0.6), n_reps=500)
    chave = ["scenario", "effect", "test"]
    a5 = g[g.alpha == 0.05].set_index(chave).rejection_rate
    a1 = g[g.alpha == 0.01].set_index(chave).rejection_rate
    assert (a1 <= a5).all() and (a1 < a5).any()
