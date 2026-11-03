"""Os dois testes do par P1: t de Welch e Mann-Whitney (bicaudais).

Convenção: `a = novato`, `b = core`. Efeito positivo = valores de `a` maiores.
As versões `*_pvalues` são vetorizadas (`axis=1`) para as repetições de Monte Carlo.
"""
from dataclasses import asdict, dataclass

import numpy as np
from scipy import stats

from lab04.config import ALPHA, ALTERNATIVE


@dataclass(frozen=True)
class TestResult:
    __test__ = False  # o nome começa com "Test": impede o pytest de coletá-la

    name: str
    statistic: float
    p_value: float
    reject: bool
    effect_size: float
    effect_label: str
    df: float | None
    n_a: int
    n_b: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "TestResult":
        return cls(**d)


def _check_not_empty(a: np.ndarray, b: np.ndarray) -> None:
    if not (a.size > 0 and b.size > 0):
        raise ValueError(f"amostra vazia: n_a={a.size}, n_b={b.size}")


def welch(a: np.ndarray, b: np.ndarray, alpha: float = ALPHA) -> TestResult:
    """t de Welch bicaudal; efeito = d de Cohen com desvio médio (ddof=1).

    Levanta ValueError se `a` ou `b` estiver vazio. NaN na entrada, ou variância
    zero nos dois grupos, produz NaN em statistic, p_value e effect_size (e
    reject=False); a função não trata esses casos.
    """
    a, b =np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    _check_not_empty(a, b)
    res = stats.ttest_ind(a, b, equal_var=False, alternative=ALTERNATIVE)
    d = (a.mean() - b.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    p = float(res.pvalue)
    return TestResult(
        name="welch", statistic=float(res.statistic), p_value=p, reject=bool(p < alpha),
        effect_size=float(d), effect_label="d de Cohen", df=float(res.df),
        n_a=int(a.size), n_b=int(b.size),
    )


def mann_whitney(a: np.ndarray, b: np.ndarray, alpha: float = ALPHA) -> TestResult:
    """Mann-Whitney bicaudal; statistic = U de `a`, efeito = r rank-biserial.

    Levanta ValueError se `a` ou `b` estiver vazio. NaN na entrada produz NaN em
    statistic, p_value e effect_size (e reject=False); todos os valores iguais
    (variância zero) produzem p_value NaN. A função não trata esses casos.
    """
    a, b =np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    _check_not_empty(a, b)
    res = stats.mannwhitneyu(a, b, alternative=ALTERNATIVE, method="auto")
    u = float(res.statistic)  # U de `a`
    p = float(res.pvalue)
    return TestResult(
        name="mann_whitney", statistic=u, p_value=p, reject=bool(p < alpha),
        effect_size=float(2 * u / (a.size * b.size) - 1), effect_label="r rank-biserial", df=None,
        n_a=int(a.size), n_b=int(b.size),
    )


def welch_pvalues(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return stats.ttest_ind(A, B, axis=1, equal_var=False, alternative=ALTERNATIVE).pvalue


def mann_whitney_pvalues(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    return stats.mannwhitneyu(A, B, axis=1, alternative=ALTERNATIVE, method="auto").pvalue
