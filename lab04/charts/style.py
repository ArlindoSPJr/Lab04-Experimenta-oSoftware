"""Estilo comum a todos os gráficos (G1–G4)."""
import plotly.graph_objects as go

from lab04.config import CHART_COLORS, COLORS, FONT_SIZE


def test_color(name: str) -> str:
    """Cor fixa do teste `name` ("welch" ou "mann_whitney")."""
    return COLORS[name]


# Evita que o pytest trate esta função como teste se ela for importada num módulo de teste.
test_color.__test__ = False


def com_alpha(hex_cor: str, alpha: float) -> str:
    """Cor `#rrggbb` com transparência `alpha`, no formato rgba do Plotly."""
    r, g, b = (int(hex_cor[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{alpha})"


def apply_layout(fig: go.Figure, title: str, x_title: str, y_title: str) -> go.Figure:
    """Aplica título, nomes dos eixos (com unidade), legenda visível e o estilo de fundo branco.

    Fundo do gráfico e do papel brancos, grade discreta e fontes legíveis em projetor
    (todas as cores vêm de `CHART_COLORS`).
    """
    fig.update_layout(
        separators=",.",  # vírgula decimal e ponto de milhar (formato brasileiro)
        title=dict(text=title, font=dict(size=FONT_SIZE + 5, color=CHART_COLORS["texto"])),
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=True,
        template="plotly_white",
        paper_bgcolor=CHART_COLORS["fundo"],
        plot_bgcolor=CHART_COLORS["fundo"],
        font=dict(size=FONT_SIZE, color=CHART_COLORS["texto"]),
        legend=dict(font=dict(size=FONT_SIZE), bgcolor=CHART_COLORS["fundo"]),
        hoverlabel=dict(font=dict(size=FONT_SIZE - 1)),
    )
    eixos = dict(
        title_font=dict(size=FONT_SIZE + 1), tickfont=dict(size=FONT_SIZE - 1),
        gridcolor=CHART_COLORS["grade"], zerolinecolor=CHART_COLORS["grade"],
        showline=True, linecolor=CHART_COLORS["eixo"], ticks="outside", tickcolor=CHART_COLORS["eixo"],
    )
    fig.update_xaxes(**eixos)
    fig.update_yaxes(**eixos)
    return fig
