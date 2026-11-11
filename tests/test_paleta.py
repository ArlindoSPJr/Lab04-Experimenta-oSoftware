"""Issue #49: paleta segura sobre fundo branco, tema claro no Streamlit e estilo dos gráficos.

- tema do Streamlit claro com fundo branco;
- todos os gráficos com fundo do gráfico e do papel brancos e fontes legíveis em projetor;
- nenhuma cor literal em `lab04/charts/` (todas vêm de `config`);
- cores dos testes e dos dados com contraste ≥ 3:1 sobre branco e distintas entre si;
- cada teste com a mesma cor em G2, G3 e G4.
"""
import re
import tomllib
from pathlib import Path

import pytest

from lab04 import config
from lab04.charts import style
from tests.test_requisitos_graficos import GRAFICOS, IDS, _g2_mw, _g2_welch, _g3, _g4

CHARTS_DIR = config.ROOT / "lab04" / "charts"
BRANCO = {"#ffffff", "#fff", "white"}
FONTE_MINIMA = 14  # px, rótulos de eixo legíveis em projetor
LARGURA_MEIA = 650  # px, G2 em meia largura (duas colunas no dashboard)

# Cor literal: hex, rgb()/rgba() com números, ou nome de cor do CSS entre aspas
COR_LITERAL = re.compile(
    r"#[0-9a-fA-F]{3,8}\b|rgba?\(\s*\d|[\"'](white|black|gray|grey|red|blue|green|orange)[\"']"
)


def _luminancia(hex_cor: str) -> float:
    canais = [int(hex_cor[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _contraste_com_branco(hex_cor: str) -> float:
    return 1.05 / (_luminancia(hex_cor) + 0.05)


def test_tema_do_streamlit_claro_com_fundo_branco():
    toml = config.ROOT / ".streamlit" / "config.toml"
    assert toml.exists(), ".streamlit/config.toml não existe"
    tema = tomllib.loads(toml.read_text(encoding="utf-8"))["theme"]
    assert tema["base"] == "light"
    assert tema["backgroundColor"].lower() in BRANCO
    assert tema["primaryColor"].lower() in {c.lower() for c in config.COLORS.values()}


@pytest.mark.parametrize("construtor", [g[1] for g in GRAFICOS], ids=IDS)
def test_graficos_com_fundo_branco(construtor):
    fig = construtor()
    assert str(fig.layout.paper_bgcolor).lower() in BRANCO
    assert str(fig.layout.plot_bgcolor).lower() in BRANCO


@pytest.mark.parametrize("construtor", [g[1] for g in GRAFICOS], ids=IDS)
def test_fontes_legiveis_em_projetor(construtor):
    fig = construtor()
    assert fig.layout.font.size is not None and fig.layout.font.size >= FONTE_MINIMA
    for nome in fig.layout:
        if not re.fullmatch(r"[xy]axis\d*", nome):
            continue
        eixo = fig.layout[nome]
        for fonte in (eixo.title.font, eixo.tickfont):
            assert fonte.size is None or fonte.size >= FONTE_MINIMA, f"{nome}: fonte {fonte.size}"
    for anotacao in fig.layout.annotations:
        assert anotacao.font.size is None or anotacao.font.size >= FONTE_MINIMA - 2


@pytest.mark.parametrize("arquivo", sorted(CHARTS_DIR.glob("*.py")), ids=lambda p: p.name)
def test_nenhuma_cor_literal_nos_graficos(arquivo: Path):
    achados = [
        f"{arquivo.name}:{i}: {linha.strip()}"
        for i, linha in enumerate(arquivo.read_text(encoding="utf-8").splitlines(), start=1)
        if not linha.lstrip().startswith("#") and COR_LITERAL.search(linha)
    ]
    assert not achados, "cores literais fora de config:\n" + "\n".join(achados)


def test_cores_com_contraste_sobre_branco():
    for nome, cor in {**config.COLORS, **config.DATA_COLORS}.items():
        assert _contraste_com_branco(cor) >= 3.0, f"{nome} ({cor}) com contraste < 3:1 sobre branco"


def test_cores_dos_dados_distintas_das_dos_testes():
    cores_testes = {c.lower() for c in config.COLORS.values()}
    cores_dados = {c.lower() for c in config.DATA_COLORS.values()}
    assert len(cores_dados) == len(config.DATA_COLORS)
    assert not cores_testes & cores_dados


def test_cada_teste_com_a_mesma_cor_em_g2_g3_g4():
    cores = {nome: set() for nome in config.TEST_NAMES}
    cores["welch"].add(_g2_welch().data[0].line.color)
    cores["mann_whitney"].add(_g2_mw().data[0].line.color)
    for fig in (_g3(), _g4()):
        for t in fig.data:
            if t.legendgroup in cores:
                cores[t.legendgroup] |= {c for c in (t.marker.color, t.line.color if hasattr(t, "line") else None) if c}
    for nome, vistas in cores.items():
        assert vistas == {style.test_color(nome)}, f"{nome}: cores {vistas}"


@pytest.mark.parametrize("construtor", [_g2_welch, _g2_mw], ids=["G2-welch", "G2-mw"])
def test_g2_cabe_em_meia_largura(construtor):
    """No dashboard o G2 fica em meia largura (~650 px): o título do eixo y não pode
    invadir o título do gráfico e a legenda não pode deixar uma linha com um item só."""
    fig = construtor()
    assert len(fig.layout.yaxis.title.text) <= 30, fig.layout.yaxis.title.text
    itens = [t for t in fig.data if t.showlegend is not False and t.name]
    legenda = fig.layout.legend
    # Itens com largura fixa: em ~650 px cabem 2 por linha (3 linhas cheias com 6 itens)
    assert legenda.entrywidthmode == "pixels" and legenda.entrywidth
    por_linha = int(LARGURA_MEIA // (legenda.entrywidth + 60))
    assert por_linha >= 2
    assert len(itens) % por_linha == 0, f"{len(itens)} itens, {por_linha} por linha"
