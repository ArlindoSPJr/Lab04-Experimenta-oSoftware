import pandas as pd
from lab04.charts.g1 import fig_g1

def _df(v): return pd.DataFrame({"group": ["novato", "core"] * 3, "hours_to_merge": v})

def test_g1_tem_4_histogramas_com_titulos():
    f = fig_g1(_df([1, 2, 3, 4, 5, 6]), _df([2, 3, 4, 5, 6, 7]))
    assert len([t for t in f.data if t.type == "histogram"]) == 4
    assert f.layout.title.text
    assert "horas" in f.layout.xaxis.title.text
