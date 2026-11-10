"""Resumo da grade de simulação: status do erro tipo I e qual teste tem mais poder."""
import numpy as np
import pandas as pd

from lab04.config import ALPHA


def classify_type1(grid: pd.DataFrame, alpha: float = ALPHA) -> pd.DataFrame:
    """Com `effect == 0`: "liberal" se o IC fica todo acima de alpha, "conservador" se todo abaixo."""
    h0 = grid[grid.effect == 0].copy()
    h0["status"] = np.select([h0.ci_low > alpha, h0.ci_high < alpha],
                             ["liberal", "conservador"], default="ok")
    return h0[["scenario", "test", "rejection_rate", "status"]].reset_index(drop=True)


def power_winner(grid: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por (cenário, effect > 0); `diferenca` = MW − Welch em pontos percentuais."""
    h1 = grid[grid.effect > 0]
    wide = h1.pivot_table(index=["scenario", "effect"], columns="test",
                          values="rejection_rate", sort=False).reset_index()
    diff = (wide["mann_whitney"] - wide["welch"]) * 100
    melhor = np.select([diff > 0, diff < 0], ["mann_whitney", "welch"], default="empate")
    return pd.DataFrame({"scenario": wide.scenario, "effect": wide.effect,
                         "melhor": melhor, "diferenca": diff})
