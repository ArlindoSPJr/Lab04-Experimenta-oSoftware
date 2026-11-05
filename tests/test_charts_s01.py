import numpy as np
import pandas as pd
from lab04.charts.g1 import fig_g1
from lab04.stat_tests import welch, mann_whitney
from lab04.charts.g2 import fig_g2_welch, fig_g2_mw
from lab04.config import COLORS

def _df(v): return pd.DataFrame({"group": ["novato", "core"] * 3, "hours_to_merge": v})

def test_g1_tem_4_histogramas_com_titulos():
    f = fig_g1(_df([1, 2, 3, 4, 5, 6]), _df([2, 3, 4, 5, 6, 7]))
    assert len([t for t in f.data if t.type == "histogram"]) == 4
    assert f.layout.title.text
    assert "horas" in f.layout.xaxis.title.text


def test_g1_real_e_simulado_usam_as_mesmas_faixas_em_cada_grupo():
    f = fig_g1(_df([1, 2, 3, 400, 5, 6000]), _df([2, 30, 4, 5, 60, 7]))
    hists = [t for t in f.data if t.type == "histogram"]
    for eixo in {t.xaxis for t in hists}:
        do_painel = [t for t in hists if t.xaxis == eixo]
        assert len(do_painel) == 2
        assert do_painel[0].xbins.size is not None
        assert do_painel[0].xbins == do_painel[1].xbins


def test_g1_marca_a_mediana_de_cada_histograma():
    f = fig_g1(_df([1, 2, 3, 4, 5, 6]), _df([2, 3, 4, 5, 6, 7]))
    tracejadas = [s for s in f.layout.shapes if s.line.dash == "dash"]
    assert len(tracejadas) == 4
    assert all("mediana" in a.text for a in f.layout.annotations)


A = np.random.default_rng(0).lognormal(2, 1, 30); B = A * 0.7

def test_g2_tem_regiao_e_pvalor_na_cor_do_teste():
    for fig, nome in ((fig_g2_welch(welch(A, B)), "welch"), (fig_g2_mw(mann_whitney(A, B)), "mann_whitney")):
        nomes = {t.name for t in fig.data}
        assert {"Região de rejeição", "p-valor"} <= nomes
        assert all(COLORS[nome] in str(t.line.color or t.fillcolor) for t in fig.data if t.name == "p-valor")
        assert fig.layout.xaxis.title.text and fig.layout.yaxis.title.text


def test_g2_mostra_o_pvalor_com_4_casas():
    for r, fig_fn in ((welch(A, B), fig_g2_welch), (mann_whitney(A, B), fig_g2_mw)):
        texto = " ".join(a.text for a in fig_fn(r).layout.annotations)
        assert f"{r.p_value:.4f}".replace(".", ",") in texto
