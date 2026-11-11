"""Resumo da grade de simulação: status do erro tipo I e qual teste tem mais poder, por alfa."""
import numpy as np
import pandas as pd

from lab04.config import ALPHA


def _com_alpha(grid: pd.DataFrame, alpha: float) -> pd.DataFrame:
    """Grades sem a coluna `alpha` (anteriores à #48) valem para o `alpha` informado."""
    return grid if "alpha" in grid else grid.assign(alpha=alpha)


def classify_type1(grid: pd.DataFrame, alpha: float = ALPHA) -> pd.DataFrame:
    """Com `effect == 0`: "liberal" se o IC fica todo acima do alfa da linha, "conservador"
    se todo abaixo. `alpha` só é usado quando a grade não tem a coluna `alpha`."""
    h0 = _com_alpha(grid, alpha)
    h0 = h0[h0.effect == 0].copy()
    h0["status"] = np.select([h0.ci_low > h0.alpha, h0.ci_high < h0.alpha],
                             ["liberal", "conservador"], default="ok")
    return h0[["scenario", "alpha", "test", "rejection_rate", "status"]].reset_index(drop=True)


def power_winner(grid: pd.DataFrame, alpha: float = ALPHA) -> pd.DataFrame:
    """Uma linha por (alfa, cenário, effect > 0); `diferenca` = MW − Welch em pontos percentuais."""
    h1 = _com_alpha(grid, alpha)
    h1 = h1[h1.effect > 0]
    wide = h1.pivot_table(index=["alpha", "scenario", "effect"], columns="test",
                          values="rejection_rate", sort=False).reset_index()
    diff = (wide["mann_whitney"] - wide["welch"]) * 100
    melhor = np.select([diff > 0, diff < 0], ["mann_whitney", "welch"], default="empate")
    return pd.DataFrame({"scenario": wide.scenario, "effect": wide.effect, "alpha": wide.alpha,
                         "melhor": melhor, "diferenca": diff})
