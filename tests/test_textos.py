from dashboard.textos import TEXTOS

CHAVES_S01 = {"pergunta", "h0", "h1", "fonte", "palpite", "dados", "como_funcionam", "exemplo"}


def _frases(texto):
    return texto.count(". ") + 1


def test_chaves_presentes():
    assert CHAVES_S01 <= set(TEXTOS)


def test_textos_nao_vazios():
    for k in CHAVES_S01:
        assert TEXTOS[k].strip(), k


def test_pergunta_tem_uma_frase():
    assert _frases(TEXTOS["pergunta"]) == 1


def test_textos_de_grafico_tem_2_a_4_frases():
    for k in ("dados", "como_funcionam"):
        assert 2 <= _frases(TEXTOS[k]) <= 4, k


CHAVES_S02 = {"erro_tipo_1", "poder", "violacoes"}


def test_chaves_s02_presentes_e_nao_vazias():
    assert CHAVES_S02 <= set(TEXTOS)
    for k in CHAVES_S02:
        assert TEXTOS[k].strip(), k


def test_textos_de_grafico_s02_tem_2_a_4_frases():
    for k in ("erro_tipo_1", "poder"):
        assert 2 <= _frases(TEXTOS[k]) <= 4, k


CHAVES_FINAL = {"dados_reais", "conclusao_palpite", "conclusao_recomendacao", "conclusao_quando_muda"}


def test_chaves_final_presentes_e_nao_vazias():
    assert CHAVES_FINAL <= set(TEXTOS)
    for k in CHAVES_FINAL:
        assert TEXTOS[k].strip(), k


def test_textos_final_tem_2_a_4_frases():
    for k in CHAVES_FINAL:
        assert 2 <= _frases(TEXTOS[k]) <= 4, k


def test_recomendacao_cita_os_dois_testes():
    texto = TEXTOS["conclusao_recomendacao"]
    assert "Welch" in texto
    assert "Mann-Whitney" in texto


def test_texto_alfa_001_tem_2_a_4_frases_e_cita_os_dois_alfas():
    texto = TEXTOS["alfa_001"]
    assert 2 <= _frases(texto) <= 4
    assert "0,01" in texto and "0,05" in texto

CHAVES_PERGUNTAS = {"bicaudal", "p_valor_nao_e", "erros_tipo", "limitacoes"}


def test_chaves_perguntas_presentes_e_nao_vazias():
    assert CHAVES_PERGUNTAS <= set(TEXTOS)
    for k in CHAVES_PERGUNTAS:
        assert TEXTOS[k].strip(), k


def test_textos_perguntas_tem_2_a_4_frases():
    for k in ("bicaudal", "p_valor_nao_e", "erros_tipo"):
        assert 2 <= _frases(TEXTOS[k]) <= 4, k


def test_erros_tipo_fala_dos_dois_erros_e_do_welch():
    texto = TEXTOS["erros_tipo"]
    assert "tipo I" in texto and "tipo II" in texto
    assert "Welch" in texto


def test_limitacoes_tem_as_6_com_a_principal_em_negrito():
    texto = TEXTOS["limitacoes"]
    itens = [linha for linha in texto.splitlines() if linha.lstrip().startswith("- ")]
    assert len(itens) == 6
    assert "**" in itens[0] and "sobrevivência" in itens[0]
    for termo in ("sobrevivência", "Associação atual", "Novato", "Janelas de tempo",
                  "rascunho", "Core team pequeno"):
        assert termo in texto, termo
