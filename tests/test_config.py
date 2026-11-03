import plotly.graph_objects as go

from lab04 import config
from lab04.charts import style


def test_constantes_do_enunciado():
    assert config.SEED == 42
    assert config.ALPHA == 0.05
    assert config.N_REPS == 10_000
    assert len(config.EFFECTS) >= 5 and config.EFFECTS[0] == 0.0
    assert list(config.EFFECTS) == sorted(config.EFFECTS)


def test_uma_cor_por_teste():
    assert set(config.COLORS) == set(config.TEST_NAMES)
    assert len(set(config.COLORS.values())) == len(config.TEST_NAMES)


def test_style_cor_e_layout():
    # importa o módulo (e não a função) para o pytest não coletar `test_color` como teste
    assert style.test_color("welch") == config.COLORS["welch"]
    f = style.apply_layout(go.Figure(), "T", "x (h)", "y (%)")
    assert f.layout.title.text == "T"
    assert f.layout.xaxis.title.text == "x (h)"
    assert f.layout.showlegend
