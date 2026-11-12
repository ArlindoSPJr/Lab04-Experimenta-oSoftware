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


# --- #59: G4 sem textos sobrepostos ---

G4_CENARIOS = pd.DataFrame([{"scenario": s, "scenario_label": s, "n": 30, "effect": e, "test": t,
                             "rejection_rate": 0.05 + e, "ci_low": 0.04 + e, "ci_high": 0.06 + e,
                             "n_reps": 100}
                            for s in ("base", "pequena", "outliers", "assimetria")
                            for e in (0.0, 0.2) for t in ("welch", "mann_whitney")])


def _linha(f, eixo_y):
    """Faixa vertical (em px) da área de plotagem do eixo `eixo_y`."""
    m = f.layout.margin
    area = f.layout.height - m.t - m.b
    d0, d1 = f.layout[eixo_y].domain
    return m.b + d0 * area, m.b + d1 * area


def test_g4_altura_cresce_com_as_linhas_e_titulo_y_cabe_na_linha():
    f = fig_g4(G4_CENARIOS)
    assert f.layout.height is not None and f.layout.margin.t is not None and f.layout.margin.b is not None
    base, topo = _linha(f, "yaxis")
    # "Poder (% de rejeições)" tem 22 caracteres; cada um ocupa ~0,6 da fonte em px.
    from lab04.config import FONT_SIZE
    assert topo - base >= 22 * 0.6 * (FONT_SIZE + 1) + 20
    assert fig_g4(G4_CENARIOS).layout.height > fig_g4(G).layout.height


def test_g4_espaco_entre_linhas_cabe_ticks_titulo_x_e_titulo_do_subplot():
    f = fig_g4(G4_CENARIOS)
    from lab04.config import FONT_SIZE
    baixo_cima, _ = _linha(f, "yaxis")      # linha de cima (subplot 1)
    _, topo_baixo = _linha(f, "yaxis3")     # linha de baixo (subplot 3)
    # rótulos dos ticks + título do eixo x + título do subplot de baixo, com folga.
    assert baixo_cima - topo_baixo >= 3 * (FONT_SIZE + 1) * 1.5 + 20


def test_g4_rotulo_do_alfa_fora_da_area_das_curvas():
    f = fig_g4(G4_CENARIOS)
    rotulos = [a for a in f.layout.annotations if a.text and "α =" in a.text]
    assert len(rotulos) == 1
    a = rotulos[0]
    assert a.xref == "paper" and a.x > 1  # à direita dos subplots, junto da legenda
