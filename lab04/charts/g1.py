"""G1: dados reais × simulados, um histograma de densidade por grupo."""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from lab04.charts.style import apply_layout
from lab04.config import DATA_COLORS, GROUP_LABELS, GROUPS

X_TITLE = "Tempo até o merge (horas)"
Y_TITLE = "Densidade (1/hora)"


def fig_g1(real: pd.DataFrame, simulated: pd.DataFrame) -> go.Figure:
    """Um subplot por grupo, com os histogramas real e simulado sobrepostos (densidade)."""
    fig = make_subplots(rows=1, cols=len(GROUPS), subplot_titles=[GROUP_LABELS[g] for g in GROUPS])
    fontes = (("real", "Real", real), ("simulado", "Simulado (lognormal)", simulated))
    for col, g in enumerate(GROUPS, start=1):
        for chave, rotulo, df in fontes:
            fig.add_trace(
                go.Histogram(
                    x=df.loc[df["group"] == g, "hours_to_merge"], name=rotulo,
                    histnorm="probability density", marker_color=DATA_COLORS[chave],
                    opacity=0.6, legendgroup=chave, showlegend=(col == 1),
                ),
                row=1, col=col,
            )
    apply_layout(fig, "G1 — Tempo até o merge: dados reais × simulados", X_TITLE, Y_TITLE)
    fig.update_xaxes(title_text=X_TITLE)
    fig.update_yaxes(title_text=Y_TITLE)
    fig.update_layout(barmode="overlay")
    return fig
