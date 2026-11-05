import numpy as np
import pandas as pd
import pytest

from lab04.real_data import describe_real, fit_lognormal, load_real_data


def _csv(tmp_path, hours, groups=None):
    p = tmp_path / "r.csv"
    pd.DataFrame({"pr_number": range(len(hours)),
                  "group": groups or ["novato", "core"] * (len(hours) // 2),
                  "created_at": "", "merged_at": "", "hours_to_merge": hours}).to_csv(p, index=False)
    return p


def test_rejeita_tempo_zero(tmp_path):
    with pytest.raises(ValueError, match="pr_number"):
        load_real_data(_csv(tmp_path, [1.0, 0.0]))


def test_rejeita_grupo_desconhecido(tmp_path):
    with pytest.raises(ValueError, match="pr_number"):
        load_real_data(_csv(tmp_path, [1.0, 2.0], groups=["novato", "veterano"]))


def test_rejeita_coluna_faltando(tmp_path):
    p = tmp_path / "r.csv"
    pd.DataFrame({"pr_number": [1], "group": ["novato"]}).to_csv(p, index=False)
    with pytest.raises(ValueError, match="hours_to_merge"):
        load_real_data(p)


def test_fit_lognormal_recupera_parametros():
    x = np.random.default_rng(0).lognormal(2.0, 0.8, 20_000)
    mu, s = fit_lognormal(x)
    assert mu == pytest.approx(2.0, abs=0.02) and s == pytest.approx(0.8, abs=0.02)


def test_describe_conta_outlier(tmp_path):
    df = load_real_data(_csv(tmp_path, [1, 1, 2, 2, 3, 3, 100, 2]))
    d = describe_real(df)
    assert d.loc["novato", "n_outliers"] == 1 and d.loc["novato", "n"] == 4
