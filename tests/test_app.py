from streamlit.testing.v1 import AppTest

from lab04.config import PROJECT_URL, REPO_URL, ROOT

# Caminho absoluto: o AppTest resolve caminhos relativos a partir da pasta tests/
APP = str(ROOT / "dashboard" / "app.py")

SECOES = ["1. Cenário", "2. Os dados", "3. Como os testes funcionam", "4. Erro tipo I",
          "5. Poder", "6. Dados reais", "7. Conclusão"]


def _rodar():
    return AppTest.from_file(APP, default_timeout=30).run()


def test_secoes_na_ordem():
    at = _rodar()
    assert not at.exception
    assert [h.value for h in at.header] == SECOES


def test_sem_results_mostra_aviso(tmp_path, monkeypatch):
    monkeypatch.setenv("LAB04_RESULTS_DIR", str(tmp_path))
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert any("run_all" in w.value for w in at.warning)


def test_s01_mostra_g1_e_os_dois_g2():
    at = _rodar()
    assert len(at.get("plotly_chart")) >= 3


def test_links_no_topo():
    at = _rodar()
    topo = " ".join(m.value for m in at.markdown[:3])
    assert REPO_URL in topo and PROJECT_URL in topo


def test_s02_tem_graficos():
    at = _rodar()
    assert not at.exception
    # G1, 2×G2, G3 e G4
    assert len(at.get("plotly_chart")) >= 5
    assert not any("Sprint 02" in i.value for i in at.info)
    # tabela de status do erro tipo I (seção 4) e de vencedor de poder (seção 5)
    assert len(at.dataframe) >= 4


def test_s02_sem_simulacao_mostra_aviso_nas_secoes_4_e_5(tmp_path, monkeypatch):
    monkeypatch.setenv("LAB04_RESULTS_DIR", str(tmp_path))
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert len(at.get("plotly_chart")) == 0
