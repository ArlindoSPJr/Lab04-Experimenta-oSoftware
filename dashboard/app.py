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

from dashboard.textos import PERGUNTAS, TEXTOS  # noqa: E402
from lab04 import config  # noqa: E402
from lab04.charts.g1 import fig_g1  # noqa: E402
from lab04.charts.g2 import fig_g2_mw, fig_g2_welch  # noqa: E402
from lab04.charts.g3 import fig_g3  # noqa: E402
from lab04.charts.g4 import fig_g4  # noqa: E402
from lab04.real_data import describe_real, load_real_data  # noqa: E402
from lab04.stat_tests import TestResult  # noqa: E402

RESULTS_DIR = Path(os.environ.get("LAB04_RESULTS_DIR", config.RESULTS_DIR))
ARQUIVOS = ("params.json", "simulado_exemplo.csv", "exemplo.json")
ARQUIVOS_S02 = ("simulacao.csv", "tipo1_status.csv", "poder_vencedor.csv")
ARQUIVO_DADOS_REAIS = "dados_reais.csv"


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


@st.cache_data
def _resultados_s02(pasta: str) -> dict | None:
    """Lê a grade de simulação e os resumos da S02; devolve None se faltar algum."""
    pasta = Path(pasta)
    if not all((pasta / f).exists() for f in ARQUIVOS_S02):
        return None
    return {
        "grade": pd.read_csv(pasta / "simulacao.csv"),
        "tipo1": pd.read_csv(pasta / "tipo1_status.csv"),
        "poder": pd.read_csv(pasta / "poder_vencedor.csv"),
    }


def _do_alfa(df: pd.DataFrame, alfa: float) -> pd.DataFrame:
    """Linhas do α escolhido (#48); resultados sem a coluna `alpha` valem para qualquer α."""
    return df[(df["alpha"] - alfa).abs() < 1e-9] if "alpha" in df else df


def _tabela_tipo1(tipo1: pd.DataFrame, rotulos: dict) -> pd.DataFrame:
    """Uma linha por situação, com a taxa e o status de cada teste."""
    linhas = []
    for cenario, g in tipo1.groupby("scenario", sort=False):
        linha = {"Situação": rotulos.get(cenario, cenario)}
        for r in g.itertuples():
            linha[f"{config.LABELS[r.test]} (%)"] = _num(r.rejection_rate * 100)
            linha[f"{config.LABELS[r.test]}: status"] = r.status
        linhas.append(linha)
    return pd.DataFrame(linhas)


def _tabela_poder(poder: pd.DataFrame, rotulos: dict) -> pd.DataFrame:
    return pd.DataFrame({
        "Situação": poder["scenario"].map(lambda s: rotulos.get(s, s)),
        "Redução da mediana": poder["effect"].map(lambda e: f"{e:.0%}"),
        "Mais poder": poder["melhor"].map(lambda m: config.LABELS.get(m, m)),
        "Vantagem (p.p.)": poder["diferenca"].map(lambda d: _num(abs(d))),
    })


@st.cache_data
def _resultados_reais(pasta: str) -> pd.DataFrame | None:
    """Lê os testes aplicados aos dados reais; devolve None se o arquivo faltar."""
    arquivo = Path(pasta) / ARQUIVO_DADOS_REAIS
    return pd.read_csv(arquivo) if arquivo.exists() else None


def _tabela_dados_reais(reais: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por teste, no formato brasileiro."""
    def estatistica(r) -> str:
        if r.teste == config.LABELS["welch"]:
            return f"t = {_num(r.estatistica)}"
        return f"U = {_num(r.estatistica, 0 if float(r.estatistica).is_integer() else 1)}"

    return pd.DataFrame([
        {
            "Teste": r.teste,
            "Estatística": estatistica(r),
            "p-valor": _p(r.p_valor),
            "Tamanho de efeito": f"{r.efeito_nome} = {_num(r.efeito)}",
            f"Decisão (α = {_num(config.ALPHA)})": "rejeita H₀" if r.rejeita_h0 else "não rejeita H₀",
            "Conclusão": r.conclusao,
        }
        for r in reais.itertuples()
    ])


def _sem_resultados() -> None:
    st.caption("Gráfico indisponível: faltam os arquivos de `results/`.")


def _secao(numero: int, titulo: str) -> None:
    """Cabeçalho da seção com âncora `secao-N` e a etiqueta das perguntas que ela responde (#50)."""
    st.header(f"{numero}. {titulo}", anchor=f"secao-{numero}")
    numeros = [str(p["numero"]) for p in PERGUNTAS if p["secao"] == numero]
    if len(numeros) == 1:
        st.caption(f"Responde à pergunta {numeros[0]}")
    else:
        st.caption(f"Responde às perguntas {', '.join(numeros[:-1])} e {numeros[-1]}")


def _ancora(ident: str) -> None:
    """Âncora invisível logo antes do bloco que responde a uma pergunta (links da sidebar)."""
    st.markdown(f'<div id="{ident}"></div>', unsafe_allow_html=True)


def _pct(taxa: float) -> str:
    return f"{_num(taxa * 100)}%"


def _taxa_base(grade: pd.DataFrame, alfa: float, efeito: float) -> dict[str, float]:
    """Taxa de rejeição de cada teste no cenário base, no α e no efeito pedidos."""
    sel = _do_alfa(grade[grade["scenario"] == "base"], alfa)
    sel = sel[(sel["effect"] - efeito).abs() < 1e-9]
    return dict(zip(sel["test"], sel["rejection_rate"]))


def _indice() -> None:
    """Sidebar com as 15 perguntas da apresentação, cada uma com link para o bloco que responde."""
    st.sidebar.title("15 perguntas da apresentação")
    st.sidebar.caption("Clique para ir ao bloco do dashboard que responde à pergunta.")
    for p in PERGUNTAS:
        st.sidebar.markdown(f"[P{p['numero']} · {p['curto']} — seção {p['secao']}](#{p['ancora']})",
                            help=p["texto"])


# ---------------------------------------------------------------- topo
st.set_page_config(page_title="Lab04 — Welch × Mann-Whitney", page_icon="📊", layout="wide")

dashboard_link = f"[{config.DASHBOARD_URL}]({config.DASHBOARD_URL})"
st.title("Testes de Hipótese por Dentro: t de Welch × Mann-Whitney")
st.markdown(
    f"**Dashboard:** {dashboard_link}  \n"
    f"**Repositório:** [{config.REPO_URL}]({config.REPO_URL})  \n"
    f"**GitHub Projects:** [{config.PROJECT_URL}]({config.PROJECT_URL})"
)
st.caption("PUC Minas · Laboratório de Experimentação de Software · Lab04 · par P1")
_indice()

real = _dados_reais()
res = _resultados(str(RESULTS_DIR))
if res is None:
    st.warning(
        f"Faltam arquivos em `{RESULTS_DIR}` ({', '.join(ARQUIVOS)}). "
        "Rode `python -m lab04.run_all` na raiz do repositório para gerá-los."
    )

# ---------------------------------------------------------------- 1. Cenário
_secao(1, "Cenário")
st.markdown(f"**Pergunta.** {TEXTOS['pergunta']}")
col_h0, col_h1 = st.columns(2)
with col_h0.container(border=True):
    st.markdown(TEXTOS["h0"])
with col_h1.container(border=True):
    st.markdown(TEXTOS["h1"])
_ancora("p2")
st.markdown(f"**Por que bicaudal.** {TEXTOS['bicaudal']}")

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
_secao(2, "Os dados")
if res is None:
    _sem_resultados()
else:
    st.plotly_chart(fig_g1(real, res["simulado"]), width="stretch", theme=None)
_ancora("p4")
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
_secao(3, "Como os testes funcionam")
st.markdown(TEXTOS["como_funcionam"])
if res is None:
    _sem_resultados()
else:
    testes = res["testes"]
    _ancora("p6")
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
_ancora("p7")
st.markdown(TEXTOS["exemplo"])
st.markdown(f"**O que o p-valor não é.** {TEXTOS['p_valor_nao_e']}")

# ---------------------------------------------------------------- 4. Erro tipo I
s02 = _resultados_s02(str(RESULTS_DIR))
rotulos = {} if s02 is None else dict(zip(s02["grade"]["scenario"], s02["grade"]["scenario_label"]))

_secao(4, "Erro tipo I")
alfa = config.ALPHA
if s02 is None:
    _sem_resultados()
else:
    # #48: o α escolhido vale para as seções 4 e 5 (G3, G4 e as duas tabelas)
    _ancora("p12")
    alfa = st.radio("Nível de significância (α) das seções 4 e 5", config.ALPHAS,
                    format_func=_num, horizontal=True)
    tipo1_base = _taxa_base(s02["grade"], alfa, 0.0)
    colunas = st.columns(len(config.TEST_NAMES))
    for col, teste in zip(colunas, config.TEST_NAMES):
        col.metric(f"Erro tipo I · {config.LABELS[teste]}", _pct(tipo1_base[teste]), border=True,
                   help=f"Cenário base (n = {config.N_PER_GROUP}), H₀ verdadeira, α = {_num(alfa)}: "
                        f"o ideal é ficar perto de {_pct(alfa)}.")
    st.markdown(TEXTOS["alfa_001"])
    st.plotly_chart(fig_g3(s02["grade"], alpha=alfa), width="stretch", theme=None)
    st.markdown(f"**Status do erro tipo I** (H₀ verdadeira, {config.N_REPS:,} repetições por "
                f"situação; o status vem do IC de 95% da taxa)".replace(",", "."))
    st.dataframe(_tabela_tipo1(_do_alfa(s02["tipo1"], alfa), rotulos), width="stretch",
                 hide_index=True)
st.markdown(TEXTOS["erro_tipo_1"])
_ancora("p8")
with st.container(border=True):
    st.markdown(f"⚖️ **Erro tipo I × erro tipo II neste cenário.** {TEXTOS['erros_tipo']}")

# ---------------------------------------------------------------- 5. Poder
_secao(5, "Poder")
if s02 is None:
    _sem_resultados()
else:
    efeito_max = max(config.EFFECTS)
    poder_base = _taxa_base(s02["grade"], alfa, efeito_max)
    colunas = st.columns(len(config.TEST_NAMES))
    for col, teste in zip(colunas, config.TEST_NAMES):
        col.metric(f"Poder com efeito de {efeito_max:.0%} · {config.LABELS[teste]}",
                   _pct(poder_base[teste]), border=True,
                   help=f"Cenário base (n = {config.N_PER_GROUP}), mediana do core "
                        f"{efeito_max:.0%} menor, α = {_num(alfa)}.")
    st.plotly_chart(fig_g4(s02["grade"], alpha=alfa), width="stretch", theme=None)
    st.markdown("**Teste com mais poder** em cada situação e tamanho de efeito "
                "(vantagem = diferença nas taxas de rejeição)")
    st.dataframe(_tabela_poder(_do_alfa(s02["poder"], alfa), rotulos), width="stretch",
                 hide_index=True)
st.markdown(TEXTOS["poder"])
_ancora("p11")
st.markdown(f"**Por que cada violação pesa mais para um teste.** {TEXTOS['violacoes']}")

# ---------------------------------------------------------------- 6. Dados reais
_secao(6, "Dados reais")
reais = _resultados_reais(str(RESULTS_DIR))
if reais is None:
    _sem_resultados()
else:
    st.markdown(f"**Os dois testes aplicados aos {len(real)} PRs reais** "
                "(H₀ bilateral, novatos × core team)")
    colunas = st.columns(2 * len(reais))
    for i, r in enumerate(reais.itertuples()):
        colunas[2 * i].metric(f"p-valor · {r.teste}", _p(r.p_valor), border=True,
                              help=f"Teste bicaudal; α = {_num(config.ALPHA)}.")
        colunas[2 * i + 1].metric(f"{r.efeito_nome} · {r.teste}", _num(r.efeito), border=True)
    st.dataframe(_tabela_dados_reais(reais), width="stretch", hide_index=True)
st.markdown(TEXTOS["dados_reais"])

# ---------------------------------------------------------------- 7. Conclusão
_secao(7, "Conclusão")
st.subheader("Palpite × resultado", anchor="palpite-resultado")
st.markdown(TEXTOS["conclusao_palpite"])
st.subheader("Recomendação", anchor="recomendacao")
with st.container(border=True):
    st.markdown(TEXTOS["conclusao_recomendacao"])
st.subheader("Quando a recomendação muda")
st.markdown(TEXTOS["conclusao_quando_muda"])
st.subheader("Limitações do estudo")
st.markdown(TEXTOS["limitacoes"])

st.divider()
st.caption(f"Resultados reproduzíveis com `python -m lab04.run_all` (semente fixa {config.SEED}).")
