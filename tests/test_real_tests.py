import numpy as np
import pandas as pd
import pytest

from lab04.config import ALPHA, LABELS, TEST_NAMES
from lab04.real_data import load_real_data
from lab04.real_tests import tabela_dados_reais
from lab04.stat_tests import mann_whitney, welch

COLUNAS = ["teste", "estatistica", "p_valor", "efeito_nome", "efeito", "rejeita_h0", "conclusao"]


def _df(novato, core):
    return pd.DataFrame({"group": ["novato"] * len(novato) + ["core"] * len(core),
                         "hours_to_merge": list(novato) + list(core)})


@pytest.fixture(scope="module")
def real():
    return load_real_data()


@pytest.fixture(scope="module")
def tabela(real):
    return tabela_dados_reais(real)


def test_duas_linhas_e_colunas_exatas(tabela):
    assert list(tabela.columns) == COLUNAS
    assert list(tabela["teste"]) == [LABELS[t] for t in TEST_NAMES]


def test_p_valor_entre_zero_e_um(tabela):
    assert tabela["p_valor"].between(0, 1).all()


def test_rejeita_h0_coerente_com_alpha(tabela):
    assert (tabela["rejeita_h0"] == (tabela["p_valor"] < ALPHA)).all()


def test_valores_iguais_aos_testes_diretos(real, tabela):
    a = real.loc[real["group"] == "novato", "hours_to_merge"].to_numpy()
    b = real.loc[real["group"] == "core", "hours_to_merge"].to_numpy()
    for (_, linha), res in zip(tabela.iterrows(), (welch(a, b, ALPHA), mann_whitney(a, b, ALPHA))):
        assert linha["estatistica"] == pytest.approx(res.statistic)
        assert linha["p_valor"] == pytest.approx(res.p_value)
        assert linha["efeito"] == pytest.approx(res.effect_size)
        assert linha["efeito_nome"] == res.effect_label
        assert linha["rejeita_h0"] == res.reject


def test_conclusao_coerente_com_rejeita(tabela):
    for _, linha in tabela.iterrows():
        if linha["rejeita_h0"]:
            assert linha["conclusao"].startswith("rejeita H₀")
        else:
            assert linha["conclusao"].startswith("não rejeita H₀")


def test_conclusao_indica_sentido_quando_rejeita():
    rng = np.random.default_rng(0)
    novato = rng.lognormal(3, 0.3, 40)
    core = rng.lognormal(1, 0.3, 40)
    t = tabela_dados_reais(_df(novato, core))
    assert t["rejeita_h0"].all()
    assert t["conclusao"].str.contains("novatos demoram mais").all()
    t = tabela_dados_reais(_df(core, novato))
    assert t["conclusao"].str.contains("novatos demoram menos").all()


def test_conclusao_sem_diferenca_quando_nao_rejeita():
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    t = tabela_dados_reais(_df(x, x))
    assert not t["rejeita_h0"].any()
    assert t["conclusao"].str.contains("sem evidência de diferença").all()
