"""G4: curvas de poder dos dois testes (proporção de rejeições × tamanho do efeito).

Um subplot por cenário, uma linha por teste na cor do teste. A legenda aparece só uma
vez por teste (`legendgroup` liga as linhas do mesmo teste em todos os subplots).
Se a grade tem a coluna `alpha` (#48), usa só as linhas do α escolhido, e a linha de
referência fica em α.
"""
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from lab04.charts.style import apply_layout, test_color
from lab04.config import ALPHA, CHART_COLORS, LABELS, TEST_NAMES

X_TITULO = "Redução da mediana do tempo de merge (%)"
Y_TITULO = "Poder (% de rejeições)"


def fig_g4(grid: pd.DataFrame, alpha: float = ALPHA) -> go.Figure:
    if "alpha" in grid:
        grid = grid[np.isclose(grid["alpha"], alpha)]
    cenarios = list(dict.fromkeys(grid["scenario"]))
    rotulos = [grid.loc[grid["scenario"] == s, "scenario_label"].iloc[0] for s in cenarios]
    ncols = min(2, len(cenarios))
    nrows = math.ceil(len(cenarios) / ncols)
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=rotulos,
                        horizontal_spacing=0.08, vertical_spacing=0.18)
    for i, cenario in enumerate(cenarios):
        row, col = i // ncols + 1, i % ncols + 1
        g = grid[grid["scenario"] == cenario]
        for nome in TEST_NAMES:
            d = g[g["test"] == nome].sort_values("effect")
            fig.add_trace(go.Scatter(
                x=(d["effect"] * 100).tolist(),
                y=(d["rejection_rate"] * 100).tolist(),
                mode="lines+markers",
                name=LABELS[nome],
                legendgroup=nome,
                showlegend=i == 0,
                line=dict(color=test_color(nome)),
                marker=dict(color=test_color(nome)),
                hovertemplate="Efeito %{x:.0f}%<br>" + LABELS[nome] + ": %{y:.1f}%<extra></extra>",
            ), row=row, col=col)
        rotulo_alfa = dict(annotation_text=f"α = {alpha * 100:g}%",
                           annotation_position="bottom right",
                           annotation_font_color=CHART_COLORS["texto_secundario"]) if i == 0 else {}
        fig.add_hline(y=alpha * 100, line_dash="dot", line_color=CHART_COLORS["texto_secundario"],
                      row=row, col=col,
                      **rotulo_alfa)
    apply_layout(fig, "G4 — Curvas de poder: rejeições × tamanho do efeito", X_TITULO, Y_TITULO)
    fig.update_xaxes(title_text=X_TITULO)
    fig.update_yaxes(title_text=Y_TITULO, rangemode="tozero", matches="y")
    return fig
