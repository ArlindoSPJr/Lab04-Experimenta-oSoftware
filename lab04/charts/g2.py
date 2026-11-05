"""G2: distribuição da estatística sob H₀, região de rejeição e p-valor do exemplo.

Um gráfico por teste, sempre na cor do teste:
- Welch: densidade t de Student com gl = `r.df`;
- Mann-Whitney: aproximação normal de U, média n_a·n_b/2 e desvio √(n_a·n_b·(n_a+n_b+1)/12).
A região de rejeição (bicaudal, α/2 em cada cauda) é sombreada em tom claro e a área do
p-valor (|estatística| ao menos tão extrema quanto a observada) é sombreada em tom forte por cima.
"""
import numpy as np
import plotly.graph_objects as go
from scipy import stats

from lab04.charts.style import apply_layout, test_color
from lab04.config import ALPHA, LABELS
from lab04.stat_tests import TestResult

N_PONTOS = 801
CINZA = "#555555"


def _num(x: float, casas: int = 2) -> str:
    """Número no formato brasileiro, com sinal de menos tipográfico."""
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".").replace("-", "−")


def _p(p: float) -> str:
    """p-valor com 4 casas; abaixo de 0,0001 mostra "< 0,0001" em vez de "= 0,0000"."""
    return "< 0,0001" if p < 0.0001 else f"= {_num(p, 4)}"


def _rgba(hex_cor: str, alpha: float) -> str:
    r, g, b = (int(hex_cor[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{alpha})"


def _area(x: np.ndarray, y: np.ndarray, mask: np.ndarray, **kw) -> go.Scatter:
    return go.Scatter(x=x[mask], y=y[mask], mode="lines", fill="tozeroy", hoverinfo="skip", **kw)


def _fig_g2(r: TestResult, alpha: float, x: np.ndarray, densidade: np.ndarray, centro: float,
            critico: float, simbolo: str, x_title: str, y_title: str, casas: int) -> go.Figure:
    """Monta o G2 a partir da curva sob H₀ já calculada; `critico` é a distância do centro."""
    cor = test_color(r.name)
    dist_obs = abs(r.statistic - centro)
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=densidade, mode="lines", name="Distribuição sob H₀", line=dict(color=cor, width=2.5),
        hovertemplate=f"{simbolo} = %{{x:.2f}}<br>densidade = %{{y:.4f}}<extra></extra>",
    ))
    for i, cauda in enumerate((x <= centro - critico, x >= centro + critico)):
        fig.add_trace(_area(
            x, densidade, cauda, name="Região de rejeição", legendgroup="rejeicao", showlegend=i == 0,
            line=dict(width=0, color=cor), fillcolor=_rgba(cor, 0.30),
        ))
    for i, cauda in enumerate((x <= centro - dist_obs, x >= centro + dist_obs)):
        fig.add_trace(_area(
            x, densidade, cauda, name="p-valor", legendgroup="pvalor", showlegend=i == 0,
            line=dict(width=1, color=cor), fillcolor=_rgba(cor, 0.55),
        ))

    pico = float(densidade.max())
    topo = pico * 1.30
    for lado in (-1, 1):
        x_crit = centro + lado * critico
        fig.add_vline(x=x_crit, line=dict(color=CINZA, dash="dash", width=1.5))
        fig.add_annotation(x=x_crit, y=topo, yanchor="top", xanchor="right" if lado < 0 else "left",
                           text=f"crítico {_num(x_crit, casas)}", showarrow=False, xshift=4 * lado,
                           font=dict(size=11, color=CINZA), bgcolor="rgba(255,255,255,0.9)")
    fig.add_vline(x=r.statistic, line=dict(color=cor, width=2.5))
    fig.add_vline(x=2 * centro - r.statistic, line=dict(color=cor, width=1.5, dash="dot"))
    fig.add_annotation(
        x=r.statistic, y=pico * 1.13, xanchor="right" if r.statistic >= centro else "left",
        xshift=-6 if r.statistic >= centro else 6,
        showarrow=False, bgcolor="rgba(255,255,255,0.9)", bordercolor=cor, borderwidth=1, borderpad=4,
        text=f"{simbolo} = {_num(r.statistic, casas)} · <b>p-valor {_p(r.p_value)}</b>",
        font=dict(size=12, color=cor),
    )

    # Entradas de legenda para as linhas verticais (não desenham dados)
    for nome, linha in (("Estatística observada", dict(color=cor, width=2.5)),
                        ("Espelho (bicaudal)", dict(color=cor, width=1.5, dash="dot")),
                        ("Valores críticos", dict(color=CINZA, dash="dash", width=1.5))):
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name=nome, line=linha, hoverinfo="skip"))

    titulo = (f"G2 — {LABELS[r.name]}: distribuição de {simbolo} sob H₀"
              f"<br><sup>bicaudal, α = {_num(alpha)} ({_num(alpha / 2, 3)} em cada cauda)</sup>")
    apply_layout(fig, titulo, x_title, y_title)
    fig.update_xaxes(range=[float(x.min()), float(x.max())])
    fig.update_yaxes(range=[0, topo])
    fig.update_layout(separators=",.", legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center"),
                      margin=dict(t=60, b=40))
    return fig


def fig_g2_welch(r: TestResult, alpha: float = ALPHA) -> go.Figure:
    """Densidade t(gl = r.df) com região |t| > t₁₋α/₂ e área do p-valor |t| ≥ |t_obs|."""
    critico = float(stats.t.ppf(1 - alpha / 2, r.df))
    limite = max(4.0, abs(r.statistic) + 1.0)
    x = np.linspace(-limite, limite, N_PONTOS)
    return _fig_g2(r, alpha, x, stats.t.pdf(x, r.df), 0.0, critico, "t",
                   "Estatística t (adimensional)", "Densidade de probabilidade (por unidade de t)", 2)


def fig_g2_mw(r: TestResult, alpha: float = ALPHA) -> go.Figure:
    """Aproximação normal de U sob H₀ com região de rejeição e área do p-valor."""
    media = r.n_a * r.n_b / 2
    desvio = float(np.sqrt(r.n_a * r.n_b * (r.n_a + r.n_b + 1) / 12))
    critico = float(stats.norm.ppf(1 - alpha / 2)) * desvio
    meia_largura = max(4 * desvio, abs(r.statistic - media) + desvio)
    x = np.linspace(max(0.0, media - meia_largura), min(r.n_a * r.n_b, media + meia_largura), N_PONTOS)
    return _fig_g2(r, alpha, x, stats.norm.pdf(x, media, desvio), media, critico, "U",
                   "Estatística U (contagem de pares)", "Densidade de probabilidade (por unidade de U)", 1)
