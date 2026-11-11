import numpy as np
from scipy.stats import skew
from lab04.scenarios import base_scenario, q3_scenarios, all_scenarios
from lab04.generate import generate_groups

B = base_scenario(np.log(10), 1.0)

def test_nomes_e_ordem():
    assert [s.name for s in all_scenarios(B)] == ["base", "n_pequeno", "outliers", "assimetria_forte"]

def test_violacoes_acontecem():
    q = {s.name: s for s in q3_scenarios(B)}
    rng = np.random.default_rng(0)
    assert q["n_pequeno"].n == 10
    base_A, _ = generate_groups(rng, B, 0.0, 2000)
    forte_A, _ = generate_groups(rng, q["assimetria_forte"], 0.0, 2000)
    assert skew(forte_A.ravel()) > skew(base_A.ravel())
    out_A, _ = generate_groups(rng, q["outliers"], 0.0, 2000)
    assert np.all(out_A > 0) and np.all(np.isfinite(out_A))

def test_cada_cenario_muda_so_uma_coisa_e_tem_label():
    q = {s.name: s for s in q3_scenarios(B)}
    assert (q["n_pequeno"].mu, q["n_pequeno"].sigma, q["n_pequeno"].outlier_frac) == (B.mu, B.sigma, 0.0)
    assert (q["outliers"].n, q["outliers"].sigma) == (B.n, B.sigma)
    assert (q["outliers"].outlier_frac, q["outliers"].outlier_mult) == (0.05, 10)
    assert (q["assimetria_forte"].n, q["assimetria_forte"].outlier_frac) == (B.n, 0.0)
    assert q["assimetria_forte"].sigma == B.sigma * 1.5
    labels = [s.label for s in all_scenarios(B)]
    assert all(labels) and len(set(labels)) == 4
