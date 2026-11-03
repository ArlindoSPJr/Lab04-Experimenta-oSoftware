"""Estilo comum a todos os gráficos (G1–G4)."""
import plotly.graph_objects as go

from lab04.config import COLORS


def test_color(name: str) -> str:
    """Cor fixa do teste `name` ("welch" ou "mann_whitney")."""
    return COLORS[name]


# Evita que o pytest trate esta função como teste se ela for importada num módulo de teste.
test_color.__test__ = False


def apply_layout(fig: go.Figure, title: str, x_title: str, y_title: str) -> go.Figure:
    """Aplica título, nomes dos eixos (com unidade) e legenda visível."""
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        showlegend=True,
        template="plotly_white",
    )
    return fig
