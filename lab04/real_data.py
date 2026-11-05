"""Dados reais: carga do CSV de PRs, ajuste da lognormal e estatísticas descritivas por grupo."""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from lab04.config import DATA_DIR, GROUPS

REQUIRED_COLUMNS: tuple[str, ...] = ("pr_number", "group", "hours_to_merge")


def load_real_data(path: Path = DATA_DIR / "real_prs.csv") -> pd.DataFrame:
    """Lê o CSV da R10 de `data/REGRAS_COLETA.md`.

    Levanta ValueError se faltar coluna, se aparecer grupo fora de `GROUPS` ou se
    `hours_to_merge <= 0` (o log da lognormal exige valores positivos), citando o `pr_number`.
    """
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{path}: faltam as colunas {missing}")
    bad_group = df[~df["group"].isin(GROUPS)]
    if not bad_group.empty:
        raise ValueError(f"grupo desconhecido nos pr_number {bad_group['pr_number'].tolist()}")
    bad_hours = df[~(df["hours_to_merge"] > 0)]  # também pega NaN
    if not bad_hours.empty:
        raise ValueError(f"hours_to_merge <= 0 nos pr_number {bad_hours['pr_number'].tolist()}")
    return df


def fit_lognormal(x: np.ndarray) -> tuple[float, float]:
    """Parâmetros `(mu, sigma)` do log de `x`: média e desvio amostral (ddof=1)."""
    logs = np.log(np.asarray(x, dtype=float))
    return float(logs.mean()), float(logs.std(ddof=1))


def _n_outliers(x: pd.Series) -> int:
    q1, q3 = np.percentile(x, [25, 75])
    return int((x > q3 + 1.5 * (q3 - q1)).sum())


def describe_real(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por grupo (na ordem de `GROUPS`): n, média, mediana, desvio, assimetria e outliers.

    Outlier é o valor acima de `Q3 + 1.5·IQR` (a cauda longa do tempo de merge fica à direita).
    """
    rows = {}
    for g in GROUPS:
        x = df.loc[df["group"] == g, "hours_to_merge"]
        rows[g] = {"n": int(x.size), "media": x.mean(), "mediana": x.median(), "desvio": x.std(ddof=1),
                   "assimetria": float(stats.skew(x)), "n_outliers": _n_outliers(x)}
    out = pd.DataFrame.from_dict(rows, orient="index")
    out.index.name = "group"
    return out
