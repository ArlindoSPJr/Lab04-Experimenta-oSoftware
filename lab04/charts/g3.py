"""G3: erro tipo I de cada teste em cada situação simulada (H₀ verdadeira, efeito 0).

Barras agrupadas por cenário, uma por teste e sempre na cor do teste, com barras de erro
pelo IC de 95% da taxa de rejeição e uma linha tracejada em α. Se a grade tem a coluna
`alpha` (#48), usa só as linhas do α escolhido.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from lab04.charts.style import apply_layout, test_color
from lab04.config import ALPHA, LABELS, TEST_NAMES


def fig_g3(grid: pd.DataFrame, alpha: float = ALPHA) -> go.Figure:
    if "alpha" in grid:
        grid = grid[np.isclose(grid["alpha"], alpha)]
    h0 = grid[grid["effect"] == 0]
    cenarios = list(dict.fromkeys(h0["scenario_label"]))
    fig = go.Figure()
    for nome in TEST_NAMES:
        d = h0[h0["test"] == nome].set_index("scenario_label").reindex(cenarios)
        taxa = d["rejection_rate"] * 100
        fig.add_trace(go.Bar(
            x=cenarios,
            y=taxa.tolist(),
            name=LABELS[nome],
            legendgroup=nome,
            marker=dict(color=test_color(nome)),
            error_y=dict(type="data", symmetric=False,
                         array=(d["ci_high"] * 100 - taxa).tolist(),
                         arrayminus=(taxa - d["ci_low"] * 100).tolist()),
            hovertemplate="%{x}<br>" + LABELS[nome] + ": %{y:.2f}%<extra></extra>",
        ))
    fig.add_hline(y=alpha * 100, line_dash="dash", line_color="#333333",
                  annotation_text=f"α = {alpha * 100:g}%", annotation_position="top left")
    fig.update_layout(barmode="group")
    return apply_layout(fig, "G3 — Erro tipo I com H₀ verdadeira, por situação simulada",
                        "Situação simulada", "Taxa de erro tipo I (%)")
