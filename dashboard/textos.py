"""Textos das seções do dashboard (S01: seções 1 a 3; S02: seções 4 e 5; Final: 6 e 7).

Os textos que acompanham um gráfico têm de 2 a 4 frases (exigência do enunciado) e são curtos,
para a projeção (#57); a explicação completa de cada um está em `docs/apresentacao.md`.
Os números vêm de `describe_real` e `fit_lognormal` sobre `data/real_prs.csv`.
"""

TEXTOS: dict[str, str] = {
    # Seção 1 — Cenário
    "pergunta": (
        "O tempo até o merge dos PRs de novatos (o primeiro PR do autor) é diferente do tempo "
        "dos PRs do core team no pallets/click?"
    ),
    "h0": "H₀: o tempo até o merge tem a mesma distribuição nos dois grupos.",
    "h1": "H₁: as distribuições são diferentes (teste bicaudal).",
    "fonte": (
        "PRs mergeados do pallets/click, pela API GraphQL do GitHub, sem bots (regras R1–R12). "
        "Os 30 mais recentes de cada grupo."
    ),
    "palpite": (
        "Palpite registrado antes de simular: o Mann-Whitney vence. A cauda longa infla a "
        "variância e tira poder do Welch, que deve ficar conservador (abaixo de 5%)."
    ),
    "bicaudal": (
        "Antes de ver os dados não havia direção esperada: qualquer grupo podia demorar mais. "
        "α = 5% dividido em 2,5% por cauda."
    ),
    # Seção 2 — Os dados (G1)
    "dados": (
        "Tempos muito assimétricos: nos novatos, média 664 h × mediana 96,7 h. A simulação usa "
        "uma lognormal ajustada aos novatos: μ = 4,38 e σ = 2,73 (mediana ≈ 80 h). O core tem a "
        "mesma forma, com a mediana reduzida pelo efeito."
    ),
    # Seção 3 — Como os testes funcionam (G2)
    "como_funcionam": (
        "Welch compara médias: rejeita H₀ se |t| > 2,04. Mann-Whitney compara postos: rejeita "
        "se U < 317 ou U > 583 (centro em 450). A área sombreada é o p-valor do exemplo."
    ),
    "exemplo": (
        "Efeito 0,2: nenhum teste rejeita H₀ (p = 0,34 e 0,94), um erro tipo II. Um único PR "
        "simulado do core, com ~22 mil h, inverteu o sinal do Welch."
    ),
    "p_valor_nao_e": (
        "Chance de um resultado tão extremo supondo H₀ verdadeira. Não é a probabilidade de H₀ "
        "ser verdadeira, nem o tamanho do efeito. p alto não prova que os grupos são iguais."
    ),
    # Seção 4 — Erro tipo I (G3); números de results/tipo1_status.csv
    "erro_tipo_1": (
        "Mann-Whitney perto de 5% (4,4% a 4,9%). Welch conservador em todas as situações "
        "(0,5% a 1,3%): a cauda longa infla o desvio e encolhe o |t|."
    ),
    # Números de results/tipo1_status.csv e results/simulacao.csv (base, efeito 0,5)
    "erros_tipo": (
        "Tipo I: ver diferença que não existe. Tipo II: não ver a demora real dos novatos, o mais "
        "grave, porque novato que espera desiste. Com efeito 0,5, o Welch comete erro tipo II "
        "em 97,6% das vezes; o Mann-Whitney, em 85,2%."
    ),
    # Seção 5 — Poder (G4); números de results/simulacao.csv e results/poder_vencedor.csv
    "poder": (
        "Mann-Whitney tem mais poder em todas as situações: 14,8% × 2,4% (efeito 0,5, base). "
        "A vantagem cresce com o efeito e nunca muda de lado. O poder dos dois é baixo: com "
        "σ = 2,73 e n = 30, o ruído esconde o efeito."
    ),
    "violacoes": (
        "- **n = 10:** Welch quase não rejeita (0,7%); MW perde poder (7,3%).\n"
        "- **Outliers (5% × 10):** movem a média; no MW viram só o maior posto (poder 15,3%).\n"
        "- **Assimetria forte (σ × 1,5):** Welch cai para 0,5% de erro tipo I."
    ),
    # Seções 4 e 5 — α = 0,01 (pergunta 12, #48); números de results/ com alpha = 0,01
    "alfa_001": (
        "Com α = 0,01 em vez de 0,05, os dois rejeitam menos: sem efeito, MW 0,78% a 0,87% e "
        "Welch 0% a 0,04%. Poder com efeito 0,5: MW 14,8% → 4,7%, Welch 2,4% → 0,13%. O "
        "Mann-Whitney segue na frente."
    ),
    # Seção 6 — Dados reais; números de tabela_dados_reais(load_real_data()) e describe_real
    "dados_reais": (
        "Os dois testes rejeitam H₀ a 5%: novatos demoram mais. Na prática, a mediana dos "
        "novatos (96,7 h, ~4 dias) é quatro vezes a do core (24,0 h)."
    ),
    # Seção 7 — Conclusão; números de results/tipo1_status.csv, simulacao.csv e poder_vencedor.csv
    "conclusao_palpite": (
        "Acertamos: o Mann-Whitney venceu (+3,2 a +12,9 p.p. de poder) e o Welch ficou "
        "conservador. Subestimamos o quanto: abaixo de 5% em todas as situações. Não previmos o "
        "poder baixo do MW (≤ 15%) nem o p menor do Welch nos dados reais."
    ),
    "conclusao_recomendacao": (
        "Recomendamos o **Mann-Whitney**: erro tipo I perto de 5% e mais poder em todas as "
        "situações. O t de Welch ficou conservador (0,5% a 1,3%) e quase nunca detectou o efeito."
    ),
    "conclusao_quando_muda": (
        "Usaríamos o Welch com dados quase normais (ex.: log do tempo) ou amostras muito maiores "
        "que 30. Também se a pergunta fosse sobre a média, como o total de horas de espera."
    ),
    # Seção 7 — Limitações; as 6 de data/REGRAS_COLETA.md ("Limitações conhecidas")
    "limitacoes": (
        "- **Viés de sobrevivência (a principal):** só entram PRs mergeados.\n"
        "- **Associação atual:** o grupo é o de hoje, não o da época do PR.\n"
        "- **Novato só neste repositório.**\n"
        "- **Janelas de tempo diferentes:** ~11 meses × 3.\n"
        "- **PRs em rascunho** contam o tempo de draft.\n"
        "- **Core team pequeno:** poucos revisores."
    ),
}


# #50: as 15 perguntas da apresentação (Enunciado.pdf, seção 5) e o bloco do dashboard que
# responde a cada uma. `ancora` é o id do cabeçalho (`secao-N` ou subheader) ou do `<div id>`
# posto logo antes do bloco; `curto` é o rótulo do link na sidebar. Reaproveitado pelo roteiro.
PERGUNTAS: list[dict] = [
    {"numero": 1, "secao": 1, "ancora": "secao-1", "curto": "Cenário, H₀ e H₁",
     "texto": "Qual é o cenário de vocês e o que H₀ e H₁ afirmam, em palavras simples?"},
    {"numero": 2, "secao": 1, "ancora": "p2", "curto": "Unicaudal ou bicaudal",
     "texto": "O teste de vocês é unicaudal ou bicaudal? Por quê?"},
    {"numero": 3, "secao": 2, "ancora": "secao-2", "curto": "Coleta e forma dos dados",
     "texto": "Como os dados reais foram coletados, e o que eles mostraram sobre a forma da "
              "distribuição?"},
    {"numero": 4, "secao": 2, "ancora": "p4", "curto": "Parâmetros da simulação",
     "texto": "Como os dados reais ajudaram a escolher os parâmetros da simulação?"},
    {"numero": 5, "secao": 3, "ancora": "secao-3", "curto": "O que cada teste compara",
     "texto": "O que cada um dos dois testes compara de fato (médias, postos, proporções...)?"},
    {"numero": 6, "secao": 3, "ancora": "p6", "curto": "G2: estatística sob H₀",
     "texto": "No G2: o que é a distribuição da estatística sob H₀, e por que a região de "
              "rejeição fica onde fica?"},
    {"numero": 7, "secao": 3, "ancora": "p7", "curto": "O p-valor do exemplo",
     "texto": "O que significa o p-valor do exemplo mostrado no G2? E o que ele não significa?"},
    {"numero": 8, "secao": 4, "ancora": "p8", "curto": "Erro tipo I × II",
     "texto": "No cenário de vocês, o que seria um erro tipo I e um erro tipo II? Qual dos dois "
              "seria mais grave?"},
    {"numero": 9, "secao": 4, "ancora": "secao-4", "curto": "G3: liberal ou conservador",
     "texto": "No G3, algum teste se afastou de 5%? Ele ficou liberal ou conservador, e por quê?"},
    {"numero": 10, "secao": 5, "ancora": "secao-5", "curto": "G4: qual tem mais poder",
     "texto": "No G4, qual teste tem mais poder? A diferença entre eles muda conforme o tamanho "
              "do efeito?"},
    {"numero": 11, "secao": 5, "ancora": "p11", "curto": "Violações de pressuposto",
     "texto": "Que violação de pressuposto vocês simularam, e por que ela afeta mais um teste do "
              "que o outro?"},
    {"numero": 12, "secao": 4, "ancora": "p12", "curto": "α = 0,01 no G3 e no G4",
     "texto": "Se vocês usassem α = 0,01 em vez de 0,05, o que mudaria no G3 e no G4?"},
    {"numero": 13, "secao": 7, "ancora": "palpite-resultado", "curto": "Palpite × resultado",
     "texto": "A simulação confirmou o que o grupo esperava antes de simular? Se não, o que "
              "explica a diferença?"},
    {"numero": 14, "secao": 6, "ancora": "secao-6", "curto": "Dados reais e efeito prático",
     "texto": "Nos dados reais, os dois testes chegaram à mesma conclusão? O tamanho do efeito "
              "tem importância prática?"},
    {"numero": 15, "secao": 7, "ancora": "recomendacao", "curto": "Recomendação e limitações",
     "texto": "Qual teste vocês recomendam para o cenário, em que situação mudariam a "
              "recomendação, e qual é a principal limitação do estudo?"},
]
