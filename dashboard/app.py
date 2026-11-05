"""Dashboard do Lab04 — t de Welch × Mann-Whitney (novatos × core team no pallets/click).

Abre com `streamlit run dashboard/app.py`. Só lê arquivos: os dados reais de `data/` e os
resultados de `results/`, gerados por `python -m lab04.run_all`. A pasta de resultados pode
ser trocada pela variável de ambiente `LAB04_RESULTS_DIR`.
"""
import json
import math
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# `streamlit run dashboard/app.py` põe só a pasta dashboard/ no sys.path; a raiz traz o `lab04`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dashboard.textos import TEXTOS  # noqa: E402
from lab04 import config  # noqa: E402
from lab04.charts.g1 import fig_g1  # noqa: E402
from lab04.charts.g2 import fig_g2_mw, fig_g2_welch  # noqa: E402
from lab04.real_data import describe_real, load_real_data  # noqa: E402
from lab04.stat_tests import TestResult  # noqa: E402

RESULTS_DIR = Path(os.environ.get("LAB04_RESULTS_DIR", config.RESULTS_DIR))
ARQUIVOS = ("params.json", "simulado_exemplo.csv", "exemplo.json")
EM_CONSTRUCAO_S02 = "Em construção — Sprint 02"
EM_CONSTRUCAO_FINAL = "Em construção — Entrega final"


def _num(x: float, casas: int = 2) -> str:
    """Número no formato brasileiro (vírgula decimal, ponto de milhar)."""
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "−")


def _p(p: float) -> str:
    return "< 0,0001" if p < 0.0001 else _num(p, 4)


@st.cache_data
def _dados_reais() -> pd.DataFrame:
    return load_real_data()


@st.cache_data
def _resultados(pasta: str) -> dict | None:
    """Lê os arquivos de `results/`; devolve None se faltar algum."""
    pasta = Path(pasta)
    if not all((pasta / f).exists() for f in ARQUIVOS):
        return None
    exemplo = json.loads((pasta / "exemplo.json").read_text(encoding="utf-8"))
    return {
        "params": json.loads((pasta / "params.json").read_text(encoding="utf-8")),
        "simulado": pd.read_csv(pasta / "simulado_exemplo.csv"),
        "efeito": exemplo["effect"],
        "testes": {nome: TestResult.from_dict(exemplo[nome]) for nome in config.TEST_NAMES},
    }


def _sem_resultados() -> None:
    st.caption("Gráfico indisponível: faltam os arquivos de `results/`.")


# ---------------------------------------------------------------- topo
st.set_page_config(page_title="Lab04 — Welch × Mann-Whitney", page_icon="📊", layout="wide")

dashboard_link = (f"[{config.DASHBOARD_URL}]({config.DASHBOARD_URL})" if config.DASHBOARD_URL
                  else "*publicado na Sprint 02*")
st.title("Testes de Hipótese por Dentro: t de Welch × Mann-Whitney")
st.markdown(
    f"**Dashboard:** {dashboard_link}  \n"
    f"**Repositório:** [{config.REPO_URL}]({config.REPO_URL})  \n"
    f"**GitHub Projects:** [{config.PROJECT_URL}]({config.PROJECT_URL})"
)
st.caption("PUC Minas · Laboratório de Experimentação de Software · Lab04 · par P1")

real = _dados_reais()
res = _resultados(str(RESULTS_DIR))
if res is None:
    st.warning(
        f"Faltam arquivos em `{RESULTS_DIR}` ({', '.join(ARQUIVOS)}). "
        "Rode `python -m lab04.run_all` na raiz do repositório para gerá-los."
    )

# ---------------------------------------------------------------- 1. Cenário
st.header("1. Cenário")
st.markdown(f"**Pergunta.** {TEXTOS['pergunta']}")
col_h0, col_h1 = st.columns(2)
with col_h0.container(border=True):
    st.markdown(TEXTOS["h0"])
with col_h1.container(border=True):
    st.markdown(TEXTOS["h1"])

n_por_grupo = real["group"].value_counts()
col_fonte, col_n = st.columns([3, 2])
with col_fonte:
    st.markdown(f"**De onde vêm os dados.** {TEXTOS['fonte']}")
with col_n:
    m1, m2, m3 = st.columns(3)
    m1.metric("PRs de novatos", int(n_por_grupo.get("novato", 0)))
    m2.metric("PRs do core team", int(n_por_grupo.get("core", 0)))
    m3.metric("Total", len(real))
with st.container(border=True):
    st.markdown(f"🎯 {TEXTOS['palpite']}")

# ---------------------------------------------------------------- 2. Os dados
st.header("2. Os dados")
if res is None:
    _sem_resultados()
else:
    st.plotly_chart(fig_g1(real, res["simulado"]), width="stretch", theme=None)
st.markdown(TEXTOS["dados"])

col_desc, col_par = st.columns([3, 2])
with col_desc:
    st.markdown("**Dados reais por grupo** (tempo até o merge, em horas)")
    desc = describe_real(real)
    tabela = pd.DataFrame({
        "n": desc["n"].astype(int),
        "Média (h)": desc["media"].map(lambda v: _num(v, 1)),
        "Mediana (h)": desc["mediana"].map(lambda v: _num(v, 1)),
        "Desvio (h)": desc["desvio"].map(lambda v: _num(v, 1)),
        "Assimetria": desc["assimetria"].map(_num),
        "Outliers": desc["n_outliers"].astype(int),
    })
    tabela.insert(0, "Grupo", [config.GROUP_LABELS[g] for g in desc.index])
    st.dataframe(tabela, width="stretch", hide_index=True)
with col_par:
    st.markdown("**Parâmetros da simulação** (lognormal)")
    if res is None:
        _sem_resultados()
    else:
        par = res["params"]
        p1, p2, p3 = st.columns(3)
        p1.metric("μ (média do log)", _num(par["mu"]))
        p2.metric("σ (desvio do log)", _num(par["sigma"]))
        p3.metric("Mediana e^μ", f"{_num(math.exp(par['mu']), 0)} h")
        st.caption(f"Ajustados em `{par['fonte']}` · n = {par['n']} por grupo em cada simulação.")

# ---------------------------------------------------------------- 3. Como os testes funcionam
st.header("3. Como os testes funcionam")
st.markdown(TEXTOS["como_funcionam"])
if res is None:
    _sem_resultados()
else:
    testes = res["testes"]
    col_w, col_m = st.columns(2)
    col_w.plotly_chart(fig_g2_welch(testes["welch"]), width="stretch", theme=None)
    col_m.plotly_chart(fig_g2_mw(testes["mann_whitney"]), width="stretch", theme=None)

    st.markdown(f"**Exemplo:** um dataset simulado com efeito {_num(res['efeito'], 1)} "
                f"(mediana do core {res['efeito']:.0%} menor), n = {testes['welch'].n_a} por grupo")
    exemplo = pd.DataFrame([
        {
            "Teste": config.LABELS[r.name],
            "Estatística": (f"t = {_num(r.statistic)} (gl = {_num(r.df, 1)})" if r.name == "welch"
                            else f"U = {_num(r.statistic, 0 if float(r.statistic).is_integer() else 1)}"),
            "p-valor": _p(r.p_value),
            "Tamanho de efeito": f"{r.effect_label} = {_num(r.effect_size)}",
            f"Decisão (α = {_num(config.ALPHA)})": "rejeita H₀" if r.reject else "não rejeita H₀",
        }
        for r in testes.values()
    ])
    st.dataframe(exemplo, width="stretch", hide_index=True)
st.markdown(TEXTOS["exemplo"])

# ---------------------------------------------------------------- 4 a 7
st.header("4. Erro tipo I")
st.info(EM_CONSTRUCAO_S02)
st.header("5. Poder")
st.info(EM_CONSTRUCAO_S02)
st.header("6. Dados reais")
st.info(EM_CONSTRUCAO_FINAL)
st.header("7. Conclusão")
st.info(EM_CONSTRUCAO_FINAL)

st.divider()
st.caption(f"Resultados reproduzíveis com `python -m lab04.run_all` (semente fixa {config.SEED}).")
