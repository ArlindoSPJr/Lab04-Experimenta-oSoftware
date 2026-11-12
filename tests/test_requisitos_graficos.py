"""Requisitos do enunciado em todos os gráficos (G1–G4), gerados a partir de `results/`.

Cada gráfico precisa de título, eixos nomeados com unidade, legenda visível e a mesma
cor para cada teste em todos os gráficos.
"""
import json
import re

import pandas as pd
import pytest

from lab04 import config
from lab04.charts import style
from lab04.charts.g1 import fig_g1
from lab04.charts.g2 import fig_g2_mw, fig_g2_welch
from lab04.charts.g3 import fig_g3
from lab04.charts.g4 import fig_g4
from lab04.real_data import load_real_data
from lab04.stat_tests import TestResult

RESULTS = config.RESULTS_DIR

# Eixos sem unidade, aceitos de propósito: o eixo x do G3 é categórico (uma barra por
# situação simulada), então não há grandeza nem unidade para mostrar.
SEM_UNIDADE = {("G3", "xaxis")}


def _exemplo() -> dict:
    return json.loads((RESULTS / "exemplo.json").read_text(encoding="utf-8"))


def _g1():
    return fig_g1(load_real_data(), pd.read_csv(RESULTS / "simulado_exemplo.csv"))


def _g2_welch():
    return fig_g2_welch(TestResult.from_dict(_exemplo()["welch"]))


def _g2_mw():
    return fig_g2_mw(TestResult.from_dict(_exemplo()["mann_whitney"]))


def _g3():
    return fig_g3(pd.read_csv(RESULTS / "simulacao.csv"))


def _g4():
    return fig_g4(pd.read_csv(RESULTS / "simulacao.csv"))


# (id, construtor, teste que o gráfico mostra sozinho — só no G2)
GRAFICOS = [
    ("G1", _g1, None),
    ("G2-welch", _g2_welch, "welch"),
    ("G2-mw", _g2_mw, "mann_whitney"),
    ("G3", _g3, None),
    ("G4", _g4, None),
]
IDS = [g[0] for g in GRAFICOS]


@pytest.fixture(scope="module", params=GRAFICOS, ids=IDS)
def grafico(request):
    nome, construtor, teste = request.param
    return nome.split("-")[0], construtor(), teste


def _eixos_com_tracos(fig) -> set[str]:
    """Nomes de layout dos eixos (xaxis, xaxis2, yaxis...) que desenham algum traço."""
    eixos = set()
    for t in fig.data:
        for ref, base in ((t.xaxis or "x", "xaxis"), (t.yaxis or "y", "yaxis")):
            eixos.add(base + ref[1:])
    return eixos


def _texto(titulo) -> str:
    return (titulo.text or "").strip() if titulo is not None else ""


def test_titulo_nao_vazio(grafico):
    _, fig, _ = grafico
    assert _texto(fig.layout.title)


def test_todos_os_eixos_com_titulo_e_unidade(grafico):
    nome, fig, _ = grafico
    eixos = _eixos_com_tracos(fig)
    assert any(e.startswith("xaxis") for e in eixos) and any(e.startswith("yaxis") for e in eixos)
    for eixo in sorted(eixos):
        titulo = _texto(fig.layout[eixo].title)
        assert titulo, f"{nome}: {eixo} sem título"
        if (nome, eixo) not in SEM_UNIDADE:
            assert re.search(r"\(.+\)", titulo), f"{nome}: {eixo} sem unidade entre parênteses: {titulo!r}"


def test_legenda_visivel(grafico):
    _, fig, _ = grafico
    assert fig.layout.showlegend is not False
    assert any(t.showlegend is not False and t.name for t in fig.data)


def _teste_do_traco(t) -> str | None:
    for nome in config.TEST_NAMES:
        if t.legendgroup == nome or t.name == config.LABELS[nome]:
            return nome
    return None


def _cores(t) -> set:
    cores = set()
    for parte in ("marker", "line"):
        obj = getattr(t, parte, None)
        if obj is not None and obj.color is not None:
            cores.add(obj.color)
    return cores


def test_tracos_dos_testes_usam_a_cor_do_teste(grafico):
    nome, fig, teste = grafico
    tracos = [(t, _teste_do_traco(t)) for t in fig.data]
    tracos = [(t, n) for t, n in tracos if n is not None]
    if nome in ("G3", "G4"):
        assert {n for _, n in tracos} == set(config.TEST_NAMES)
    for t, n in tracos:
        assert _cores(t) == {style.test_color(n)}, f"{nome}: traço {t.name!r} fora da cor de {n}"
    if teste is not None:
        # G2 mostra um teste só: a curva sob H₀ (primeiro traço) usa a cor desse teste.
        assert fig.data[0].line.color == style.test_color(teste)
        assert config.LABELS[teste] in fig.layout.title.text


def test_numeros_dos_eixos_em_formato_brasileiro(grafico):
    nome, fig, _ = grafico
    assert fig.layout.separators == ",.", f"{nome}: eixos sem vírgula decimal"
