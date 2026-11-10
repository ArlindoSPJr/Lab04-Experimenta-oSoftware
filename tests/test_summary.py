import pandas as pd, pytest
from lab04.summary import classify_type1, power_winner

G = pd.DataFrame({
    "scenario": ["x"] * 4, "effect": [0.0, 0.0, 0.3, 0.3], "test": ["welch", "mann_whitney"] * 2,
    "rejection_rate": [0.08, 0.03, 0.40, 0.55], "ci_low": [0.075, 0.027, 0.39, 0.54],
    "ci_high": [0.085, 0.033, 0.41, 0.56]})

def test_classifica():
    c = classify_type1(G).set_index("test").status
    assert c["welch"] == "liberal" and c["mann_whitney"] == "conservador"

def test_vencedor_de_poder():
    w = power_winner(G)
    assert w.iloc[0].melhor == "mann_whitney"
    assert w.iloc[0].diferenca == pytest.approx(15.0)


# --- Contrato da interface (plano, Task 1.2 da S02) ---

def _grade(rates_by_scenario):
    rows = []
    for s, pares in rates_by_scenario.items():
        for e, (w, m) in pares.items():
            for t, p in (("welch", w), ("mann_whitney", m)):
                rows.append({"scenario": s, "effect": e, "test": t, "rejection_rate": p,
                             "ci_low": p - 0.005, "ci_high": p + 0.005})
    return pd.DataFrame(rows)

def test_ic_contendo_alfa_e_ok():
    g = _grade({"y": {0.0: (0.048, 0.052)}})
    c = classify_type1(g)
    assert list(c.columns) == ["scenario", "test", "rejection_rate", "status"]
    assert (c.status == "ok").all()

def test_vencedor_uma_linha_por_cenario_e_efeito_positivo():
    g = _grade({"a": {0.0: (0.05, 0.05), 0.1: (0.30, 0.20), 0.2: (0.60, 0.70)},
                "b": {0.0: (0.05, 0.05), 0.1: (0.10, 0.12)}})
    w = power_winner(g)
    assert list(w.columns) == ["scenario", "effect", "melhor", "diferenca"]
    assert list(zip(w.scenario, w.effect)) == [("a", 0.1), ("a", 0.2), ("b", 0.1)]
    assert list(w.melhor) == ["welch", "mann_whitney", "mann_whitney"]
    assert w.diferenca.tolist() == pytest.approx([-10.0, 10.0, 2.0])
