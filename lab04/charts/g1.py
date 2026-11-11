"""G1: dados reais × simulados, um histograma por grupo em escala log.

O tempo até o merge vai de menos de 1 hora a milhares de horas, então o eixo x usa
log10(horas) com marcas em horas. Real e simulado usam as mesmas faixas em cada
grupo, e uma linha tracejada marca a mediana de cada histograma.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from lab04.charts.style import apply_layout
from lab04.config import DATA_COLORS, GROUP_LABELS, GROUPS

X_TITLE = "Tempo até o merge (horas, escala log)"
Y_TITLE = "PRs do grupo (%)"
BIN_SIZE = 0.5  # largura da faixa em log10: meia década (ex.: de 10 h a ~32 h)
TICKS_HORAS = (0.1, 1, 10, 100, 1_000, 10_000, 100_000)
FONTES = (("real", "Real"), ("simulado", "Simulado (lognormal)"))


def _horas(x: float) -> str:
    return f"{x:,.0f}".replace(",", ".") if x >= 10 else f"{x:g}".replace(".", ",")


def fig_g1(real: pd.DataFrame, simulated: pd.DataFrame) -> go.Figure:
    """Um subplot por grupo, com os histogramas real e simulado sobrepostos (% do grupo)."""
    dados = {"real": real, "simulado": simulated}
    horas = {(g, k): dados[k].loc[dados[k]["group"] == g, "hours_to_merge"].to_numpy(float)
             for g in GROUPS for k, _ in FONTES}
    medianas = {chave: float(np.median(x)) for chave, x in horas.items()}
    titulos = [
        f"<b>{GROUP_LABELS[g]}</b><br><sup>mediana real {_horas(medianas[g, 'real'])} h · "
        f"simulada {_horas(medianas[g, 'simulado'])} h</sup>"
        for g in GROUPS
    ]
    fig = make_subplots(rows=1, cols=len(GROUPS), subplot_titles=titulos,
                        shared_yaxes=True, horizontal_spacing=0.10)

    for col, g in enumerate(GROUPS, start=1):
        logs = np.log10(np.concatenate([horas[g, k] for k, _ in FONTES]))
        inicio = np.floor(logs.min() / BIN_SIZE) * BIN_SIZE
        fim = np.ceil(logs.max() / BIN_SIZE) * BIN_SIZE + BIN_SIZE
        faixas = dict(start=inicio, end=fim, size=BIN_SIZE)
        for chave, rotulo in FONTES:
            cor = DATA_COLORS[chave]
            fig.add_trace(
                go.Histogram(
                    x=np.log10(horas[g, chave]), name=rotulo, histnorm="percent", xbins=faixas,
                    marker=dict(color=cor, line=dict(color="white", width=1)), opacity=0.6,
                    legendgroup=chave, showlegend=(col == 1),
                    hovertemplate=f"{rotulo}: %{{y:.1f}}% dos PRs<extra></extra>",
                ),
                row=1, col=col,
            )
            fig.add_vline(x=np.log10(medianas[g, chave]), line=dict(color=cor, dash="dash", width=2),
                          row=1, col=col)

    # Entrada de legenda para explicar as linhas tracejadas (não desenha dados)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name="Mediana (tracejado)",
                             line=dict(color="#555555", dash="dash", width=2), hoverinfo="skip"))

    apply_layout(fig, "G1 — Tempo até o merge: dados reais × simulados", X_TITLE, Y_TITLE)
    fig.update_annotations(yshift=12)
    fig.update_xaxes(title_text=X_TITLE, tickvals=np.log10(TICKS_HORAS),
                     ticktext=[_horas(t) for t in TICKS_HORAS])
    fig.update_yaxes(title_text=Y_TITLE, ticksuffix="%")
    # Cada subplot nomeia o próprio eixo y (enunciado: todos os eixos nomeados com unidade)
    fig.update_yaxes(showticklabels=True, col=2)
    fig.update_layout(barmode="overlay", bargap=0, margin=dict(t=140),
                      legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center"))
    return fig
