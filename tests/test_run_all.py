import json

import pandas as pd
import pytest

from lab04.real_data import fit_lognormal, load_real_data
from lab04.run_all import main

ARQUIVOS_S01 = ("params.json", "simulado_exemplo.csv", "exemplo.json")


def test_gera_arquivos_s01(tmp_path):
    main(n_reps=200, out_dir=tmp_path)
    for f in ARQUIVOS_S01:
        assert (tmp_path / f).exists()
    ex = json.loads((tmp_path / "exemplo.json").read_text())
    assert set(ex) >= {"effect", "welch", "mann_whitney"}


def test_conteudo_s01(tmp_path):
    main(n_reps=200, out_dir=tmp_path)
    params = json.loads((tmp_path / "params.json").read_text())
    df = load_real_data()
    mu, sigma = fit_lognormal(df.loc[df["group"] == "novato", "hours_to_merge"])
    assert params == {"mu": pytest.approx(mu), "sigma": pytest.approx(sigma), "n": 30,
                      "fonte": "data/real_prs.csv"}
    sim = pd.read_csv(tmp_path / "simulado_exemplo.csv")
    assert sim["group"].value_counts().to_dict() == {"novato": 30, "core": 30}
    assert (sim["hours_to_merge"] > 0).all()
    ex = json.loads((tmp_path / "exemplo.json").read_text())
    assert ex["effect"] == 0.2 and ex["welch"]["name"] == "welch"


def test_reprodutivel(tmp_path):
    main(n_reps=200, out_dir=tmp_path / "a")
    main(n_reps=200, out_dir=tmp_path / "b")
    for f in ARQUIVOS_S01:
        assert (tmp_path / "a" / f).read_bytes() == (tmp_path / "b" / f).read_bytes()
