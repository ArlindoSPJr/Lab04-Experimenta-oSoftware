import json

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


def test_dashboard_publicado_com_link_no_topo_e_no_readme():
    from lab04.config import DASHBOARD_URL
    assert DASHBOARD_URL.startswith("https://") and DASHBOARD_URL.endswith(".streamlit.app/")
    at = _rodar()
    topo = " ".join(m.value for m in at.markdown[:3])
    assert DASHBOARD_URL in topo
    assert DASHBOARD_URL in (ROOT / "README.md").read_text(encoding="utf-8")


def _textos_da_pagina(at):
    elementos = list(at.info) + list(at.markdown) + list(at.caption) + list(at.warning)
    return [e.value for e in elementos] + [h.value for h in at.subheader]


def test_final_secoes_na_ordem_sem_em_construcao():
    at = _rodar()
    assert not at.exception
    assert [h.value for h in at.header] == SECOES
    assert not any("Em construção" in t for t in _textos_da_pagina(at))


def test_final_secao_6_tem_tabela_dos_dados_reais():
    at = _rodar()
    tabelas = [d.value for d in at.dataframe
               if {"t de Welch", "Mann-Whitney"} <= set(d.value.astype(str).values.ravel())]
    assert len(tabelas) >= 1
    tabela = tabelas[-1]
    assert len(tabela) == 2
    texto = " ".join(tabela.astype(str).values.ravel())
    assert "t = 3,07" in texto and "U = 587" in texto and "d de Cohen = 0,79" in texto


def test_final_secao_7_mostra_conclusao():
    from dashboard.textos import TEXTOS
    at = _rodar()
    textos = " ".join(m.value for m in at.markdown)
    for chave in ("dados_reais", "conclusao_palpite", "conclusao_recomendacao",
                  "conclusao_quando_muda"):
        assert TEXTOS[chave] in textos


def test_final_sem_results_secao_6_mostra_aviso(tmp_path, monkeypatch):
    monkeypatch.setenv("LAB04_RESULTS_DIR", str(tmp_path))
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert [h.value for h in at.header] == SECOES


# --- #48: seletor de alfa nas seções 4 e 5 ---

def _linhas_de_referencia(at):
    ys = []
    for c in at.get("plotly_chart"):
        fig = json.loads(c.proto.spec)
        if fig["layout"].get("title", {}).get("text", "").startswith(("G3", "G4")):
            ys.append(sorted({round(s["y0"], 9) for s in fig["layout"].get("shapes", [])}))
    return ys


def test_seletor_de_alfa_muda_g3_g4_e_tabelas():
    from dashboard.textos import TEXTOS
    at = _rodar()
    assert not at.exception
    seletor = at.radio[0]
    assert list(seletor.options) == ["0,05", "0,01"] and seletor.value == 0.05
    assert _linhas_de_referencia(at) == [[5.0], [5.0]]
    assert TEXTOS["alfa_001"] in " ".join(m.value for m in at.markdown)
    tabelas_005 = [d.value.to_string() for d in at.dataframe]
    at = seletor.set_value(0.01).run()
    assert not at.exception
    assert _linhas_de_referencia(at) == [[1.0], [1.0]]
    assert [d.value.to_string() for d in at.dataframe] != tabelas_005
