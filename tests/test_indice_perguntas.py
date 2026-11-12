"""#50: índice das 15 perguntas na sidebar, etiquetas por seção e números-chave (st.metric)."""
import re

import pandas as pd
from streamlit.testing.v1 import AppTest

from lab04 import config

APP = str(config.ROOT / "dashboard" / "app.py")
RESULTS = config.RESULTS_DIR

SECOES = ["1. Cenário", "2. Os dados", "3. Como os testes funcionam", "4. Erro tipo I",
          "5. Poder", "6. Dados reais", "7. Conclusão"]


def _rodar():
    return AppTest.from_file(APP, default_timeout=30).run()


def _num(x: float, casas: int = 2) -> str:
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "−")


def _percorrer(no):
    filhos = getattr(no, "children", None)
    if filhos is None:
        yield no
        return
    for filho in filhos.values():
        yield from _percorrer(filho)


def _ancoras_da_pagina(at) -> set[str]:
    """Âncoras que existem na área principal: as de cabeçalhos e os `<div id=...>`."""
    ancoras = set()
    for e in _percorrer(at.main):
        if e.type in ("header", "subheader", "title") and e.proto.anchor:
            ancoras.add(e.proto.anchor)
        valor = getattr(e, "value", None)
        if isinstance(valor, str):
            ancoras.update(re.findall(r'id="([^"]+)"', valor))
    return ancoras


# ---------------------------------------------------------------- constante PERGUNTAS

def test_perguntas_tem_as_15_com_secao_e_ancora():
    from dashboard.textos import PERGUNTAS
    assert [p["numero"] for p in PERGUNTAS] == list(range(1, 16))
    for p in PERGUNTAS:
        assert p["texto"].strip().endswith("?"), p["numero"]
        assert p["curto"].strip(), p["numero"]
        assert p["secao"] in range(1, 8), p["numero"]
        assert re.fullmatch(r"[a-z0-9-]+", p["ancora"]), p["numero"]


def test_perguntas_usam_o_texto_do_enunciado():
    from dashboard.textos import PERGUNTAS
    texto = {p["numero"]: p["texto"] for p in PERGUNTAS}
    assert "unicaudal ou bicaudal" in texto[2]
    assert "erro tipo I e um erro tipo II" in texto[8]
    assert "α = 0,01" in texto[12]
    assert "principal limitação" in texto[15]


def test_toda_secao_responde_a_alguma_pergunta():
    from dashboard.textos import PERGUNTAS
    assert {p["secao"] for p in PERGUNTAS} == set(range(1, 8))


# ---------------------------------------------------------------- sidebar

def test_sidebar_lista_as_15_perguntas_com_link():
    from dashboard.textos import PERGUNTAS
    at = _rodar()
    assert not at.exception
    assert "15 perguntas da apresentação" in [t.value for t in at.sidebar.title]
    links = " ".join(m.value for m in at.sidebar.markdown)
    for p in PERGUNTAS:
        assert f"(#{p['ancora']})" in links, p["numero"]
        assert f"P{p['numero']} ·" in links, p["numero"]
        assert f"seção {p['secao']}" in links, p["numero"]


def test_toda_pergunta_aponta_para_ancora_que_existe():
    from dashboard.textos import PERGUNTAS
    at = _rodar()
    ancoras = _ancoras_da_pagina(at)
    for p in PERGUNTAS:
        assert p["ancora"] in ancoras, (p["numero"], p["ancora"])


def test_ancora_fica_na_secao_que_responde():
    from dashboard.textos import PERGUNTAS
    at = _rodar()
    secao_da_ancora, atual = {}, None
    for e in _percorrer(at.main):
        if e.type == "header":
            atual = SECOES.index(e.value) + 1
        if e.type in ("header", "subheader") and e.proto.anchor:
            secao_da_ancora[e.proto.anchor] = atual
        valor = getattr(e, "value", None)
        if isinstance(valor, str):
            for a in re.findall(r'id="([^"]+)"', valor):
                secao_da_ancora[a] = atual
    for p in PERGUNTAS:
        assert secao_da_ancora[p["ancora"]] == p["secao"], p["numero"]


# ---------------------------------------------------------------- etiquetas

def test_cada_secao_mostra_a_etiqueta_logo_abaixo_do_header():
    from dashboard.textos import PERGUNTAS
    at = _rodar()
    elementos = list(_percorrer(at.main))
    for i, e in enumerate(elementos):
        if e.type != "header":
            continue
        secao = SECOES.index(e.value) + 1
        numeros = [str(p["numero"]) for p in PERGUNTAS if p["secao"] == secao]
        seguinte = elementos[i + 1]
        assert seguinte.type == "caption", e.value
        assert seguinte.value.startswith("Responde à"), e.value
        assert re.findall(r"\d+", seguinte.value) == numeros, e.value


# ---------------------------------------------------------------- métricas

def _metricas(at) -> dict[str, str]:
    return {m.label: m.value for m in at.metric}


def _taxa_base(alfa: float, efeito: float) -> dict[str, str]:
    sim = pd.read_csv(RESULTS / "simulacao.csv")
    sel = sim[(sim["scenario"] == "base") & ((sim["alpha"] - alfa).abs() < 1e-9)
              & ((sim["effect"] - efeito).abs() < 1e-9)]
    return {r.test: f"{_num(r.rejection_rate * 100)}%" for r in sel.itertuples()}


def test_metricas_da_secao_4_e_5_batem_com_results():
    at = _rodar()
    assert not at.exception
    for alfa in config.ALPHAS:
        if alfa != config.ALPHA:
            at = at.radio[0].set_value(alfa).run()
            assert not at.exception
        metricas = _metricas(at)
        tipo1, poder = _taxa_base(alfa, 0.0), _taxa_base(alfa, 0.5)
        for teste in config.TEST_NAMES:
            rotulo = config.LABELS[teste]
            assert metricas[f"Erro tipo I · {rotulo}"] == tipo1[teste], (alfa, teste)
            assert metricas[f"Poder com efeito de 50% · {rotulo}"] == poder[teste], (alfa, teste)


def test_metricas_da_secao_6_batem_com_results():
    reais = pd.read_csv(RESULTS / "dados_reais.csv").set_index("teste")
    at = _rodar()
    metricas = _metricas(at)
    for teste in config.TEST_NAMES:
        r = reais.loc[config.LABELS[teste]]
        assert metricas[f"p-valor · {r.name}"] == _num(r.p_valor, 4)
        assert metricas[f"{r.efeito_nome} · {r.name}"] == _num(r.efeito)


def test_metricas_ficam_nas_secoes_4_5_e_6():
    at = _rodar()
    secao_da_metrica, atual = {}, None
    for e in _percorrer(at.main):
        if e.type == "header":
            atual = e.value
        elif e.type == "metric":
            secao_da_metrica[e.label] = atual
    for teste in config.TEST_NAMES:
        rotulo = config.LABELS[teste]
        assert secao_da_metrica[f"Erro tipo I · {rotulo}"] == "4. Erro tipo I"
        assert secao_da_metrica[f"Poder com efeito de 50% · {rotulo}"] == "5. Poder"
        assert secao_da_metrica[f"p-valor · {rotulo}"] == "6. Dados reais"
