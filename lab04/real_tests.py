"""Testes aplicados aos PRs reais: a tabela da seção 6 do dashboard.

Convenção de `stat_tests`: `a = novato`, `b = core`, bicaudal; efeito positivo
significa tempos de merge maiores entre os novatos.
"""
import pandas as pd

from lab04.config import ALPHA, GROUPS, LABELS, TEST_NAMES
from lab04.stat_tests import TestResult, mann_whitney, welch

_TESTES = {"welch": welch, "mann_whitney": mann_whitney}


def _alpha_br() -> str:
    return f"{ALPHA:g}".replace(".", ",")


def _conclusao(res: TestResult) -> str:
    if not res.reject:
        return f"não rejeita H₀ a α = {_alpha_br()}: sem evidência de diferença"
    sentido = "mais" if res.effect_size > 0 else "menos"
    return f"rejeita H₀ a α = {_alpha_br()}: novatos demoram {sentido}"


def tabela_dados_reais(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por teste (ordem de `TEST_NAMES`) com estatística, p-valor, efeito e conclusão.

    `df` é o retorno de `load_real_data` (colunas `group` e `hours_to_merge`).
    """
    a, b = (df.loc[df["group"] == g, "hours_to_merge"].to_numpy() for g in GROUPS)
    linhas = []
    for nome in TEST_NAMES:
        res = _TESTES[nome](a, b, ALPHA)
        linhas.append({"teste": LABELS[nome], "estatistica": res.statistic, "p_valor": res.p_value,
                       "efeito_nome": res.effect_label, "efeito": res.effect_size,
                       "rejeita_h0": res.reject, "conclusao": _conclusao(res)})
    return pd.DataFrame(linhas)
