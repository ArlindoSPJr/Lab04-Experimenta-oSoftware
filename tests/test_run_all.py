import json

import pandas as pd
import pytest

from lab04.config import ALPHAS, EFFECTS, RESULTS_DIR, ROOT
from lab04.real_data import fit_lognormal, load_real_data
from lab04.run_all import main

ARQUIVOS_S01 = ("params.json", "simulado_exemplo.csv", "exemplo.json")
ARQUIVOS_S02 = ("simulacao.csv", "tipo1_status.csv", "poder_vencedor.csv")
ARQUIVOS = ARQUIVOS_S01 + ARQUIVOS_S02


def test_gera_arquivos_s01(tmp_path):
    main(n_reps=200, out_dir=tmp_path)
    for f in ARQUIVOS:
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
    for f in ARQUIVOS:
        assert (tmp_path / "a" / f).read_bytes() == (tmp_path / "b" / f).read_bytes()


def test_conteudo_s02(tmp_path):
    main(n_reps=200, out_dir=tmp_path)
    sim = pd.read_csv(tmp_path / "simulacao.csv")
    assert len(sim) == len(ALPHAS) * 4 * len(EFFECTS) * 2        # 96 linhas
    assert list(sim["scenario"].unique()) == ["base", "n_pequeno", "outliers", "assimetria_forte"]
    assert (sim["n_reps"] == 200).all()
    assert len(pd.read_csv(tmp_path / "tipo1_status.csv")) == len(ALPHAS) * 4 * 2   # efeito 0
    assert len(pd.read_csv(tmp_path / "poder_vencedor.csv")) == len(ALPHAS) * 4 * (len(EFFECTS) - 1)


def test_s02_nao_altera_a_s01(tmp_path):
    main(n_reps=200, out_dir=tmp_path)
    for f in ARQUIVOS_S01:
        assert (tmp_path / f).read_bytes() == (RESULTS_DIR / f).read_bytes()


def test_grava_dados_reais(tmp_path):
    main(n_reps=200, out_dir=tmp_path)
    caminho = tmp_path / "dados_reais.csv"
    assert caminho.exists()
    tabela = pd.read_csv(caminho)
    assert len(tabela) == 2
    assert list(tabela.columns) == ["teste", "estatistica", "p_valor", "efeito_nome", "efeito",
                                    "rejeita_h0", "conclusao"]


# #48: os números de alfa = 0,05 (citados nos textos do dashboard) não podem mudar.
# tests/fixtures/alfa005/ guarda os CSVs da main antes do alfa = 0,01 (sem a coluna alpha).
FIXTURES = ROOT / "tests" / "fixtures" / "alfa005"


@pytest.mark.parametrize("arquivo", ARQUIVOS_S02)
def test_results_alfa_005_identicos_aos_publicados(arquivo):
    atual = pd.read_csv(RESULTS_DIR / arquivo, keep_default_na=False)
    assert set(atual["alpha"]) == set(ALPHAS)
    so_005 = atual[atual["alpha"] == 0.05].drop(columns="alpha").reset_index(drop=True)
    antes = pd.read_csv(FIXTURES / arquivo, keep_default_na=False)
    pd.testing.assert_frame_equal(so_005[list(antes.columns)], antes)
