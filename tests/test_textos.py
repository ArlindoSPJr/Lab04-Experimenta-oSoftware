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
