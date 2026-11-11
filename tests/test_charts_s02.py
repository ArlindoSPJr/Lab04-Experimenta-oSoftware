import pandas as pd
from lab04.charts.g3 import fig_g3
from lab04.charts.g4 import fig_g4
from lab04.config import COLORS

G = pd.DataFrame([{"scenario": s, "scenario_label": s, "n": 30, "effect": e, "test": t,
                   "rejection_rate": 0.05 + e, "ci_low": 0.04 + e, "ci_high": 0.06 + e, "n_reps": 100}
                  for s in ("base", "outliers") for e in (0.0, 0.2) for t in ("welch", "mann_whitney")])


def test_g3_linha_5_e_cores():
    f = fig_g3(G)
    assert any(abs(s.y0 - 0.05) < 1e-9 or abs(s.y0 - 5) < 1e-9 for s in f.layout.shapes)
    for t in f.data:
        assert t.marker.color == COLORS[t.legendgroup]


def test_g3_usa_so_efeito_zero_em_percentual():
    f = fig_g3(G)
    assert len(f.data) == 2
    for t in f.data:
        assert list(t.y) == [5.0, 5.0]
    assert "Taxa de erro tipo I (%)" == f.layout.yaxis.title.text
    assert f.layout.title.text


def test_g4_cores_consistentes_e_legenda_unica():
    f = fig_g4(G)
    for t in f.data:
        assert t.line.color == COLORS[t.legendgroup]
    assert sum(1 for t in f.data if t.showlegend is not False) == 2


def test_g4_um_subplot_por_cenario_e_eixos_com_unidade():
    f = fig_g4(G)
    assert len(f.data) == 4  # 2 cenários × 2 testes
    assert {t.xaxis for t in f.data} == {"x", "x2"}
    assert "Redução da mediana do tempo de merge (%)" in f.layout.xaxis.title.text
    assert "Poder (% de rejeições)" in f.layout.yaxis.title.text
    assert list(f.data[0].x) == [0.0, 20.0]
    assert f.layout.title.text
