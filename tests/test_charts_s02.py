import pandas as pd
import pytest
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


# --- #48: G3 e G4 filtram pelo alfa e põem a linha de referência em alfa ---

G2 = pd.concat([G.assign(alpha=0.05),
                G.assign(alpha=0.01, rejection_rate=G.rejection_rate / 5,
                         ci_low=G.ci_low / 5, ci_high=G.ci_high / 5)], ignore_index=True)


def _linhas_y(f):
    return sorted({round(s.y0, 9) for s in f.layout.shapes})


def test_g3_filtra_pelo_alfa_e_muda_a_linha():
    f5, f1 = fig_g3(G2, alpha=0.05), fig_g3(G2, alpha=0.01)
    assert len(f5.data) == len(f1.data) == 2
    assert list(f5.data[0].y) == pytest.approx([5.0, 5.0]) and list(f1.data[0].y) == pytest.approx([1.0, 1.0])
    assert _linhas_y(f5) == [5.0] and _linhas_y(f1) == [1.0]
    assert any("α = 1%" in a.text for a in f1.layout.annotations)


def test_g4_filtra_pelo_alfa_e_muda_a_linha():
    f5, f1 = fig_g4(G2, alpha=0.05), fig_g4(G2, alpha=0.01)
    assert len(f5.data) == len(f1.data) == 4
    assert list(f5.data[0].y) == pytest.approx([5.0, 25.0]) and list(f1.data[0].y) == pytest.approx([1.0, 5.0])
    assert _linhas_y(f5) == [5.0] and _linhas_y(f1) == [1.0]
    assert any("α = 1%" in a.text for a in f1.layout.annotations)
