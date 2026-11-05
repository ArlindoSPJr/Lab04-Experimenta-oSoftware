"""Textos das seções do dashboard (S01: seções 1 a 3).

Os textos que acompanham um gráfico têm de 2 a 4 frases (exigência do enunciado).
Os números vêm de `describe_real` e `fit_lognormal` sobre `data/real_prs.csv`.
"""

TEXTOS: dict[str, str] = {
    # Seção 1 — Cenário
    "pergunta": (
        "O tempo até o merge de PRs abertos por contribuidores novatos (o primeiro PR do autor) "
        "é diferente do tempo dos PRs abertos por membros do core team do pallets/click?"
    ),
    "h0": (
        "H₀: o tempo até o merge tem a mesma distribuição para PRs de novatos e do core team."
    ),
    "h1": (
        "H₁: as distribuições são diferentes (teste bicaudal)."
    ),
    "fonte": (
        "PRs mergeados do repositório pallets/click, coletados pela API GraphQL do GitHub em "
        "2026-11-05 com `python scripts/collect_prs.py`, seguindo as regras R1–R12 de "
        "`data/REGRAS_COLETA.md` (sem bots e sem automerge). A amostra tem os 30 PRs mais recentes "
        "de cada grupo, n = 60 no total: novatos de 2025-09 a 2026-08 e core de 2026-07 a 2026-10."
    ),
    "palpite": (
        "Palpite registrado antes de simular: esperamos que o Mann-Whitney vença. Os tempos de merge "
        "são muito assimétricos e têm outliers, o que infla a variância e tira poder do t de Welch, "
        "enquanto o Mann-Whitney usa só os postos e não é afetado pela cauda longa. Com n = 30 por "
        "grupo, também esperamos que o Welch fique abaixo dos 5% de erro tipo I (conservador) "
        "nos cenários mais assimétricos."
    ),
    # Seção 2 — Os dados (G1)
    "dados": (
        "Os tempos até o merge são muito assimétricos à direita: nos novatos a média (664 h) é quase "
        "sete vezes a mediana (96,7 h), e no core a média é 60,9 h contra mediana de 24,0 h, com "
        "assimetria perto de 1,9 nos dois grupos e 1 outlier nos novatos e 4 no core acima de "
        "Q3 + 1,5·IQR. Por isso a simulação usa uma lognormal, cujo logaritmo é normal, com μ e σ "
        "iguais à média e ao desvio do log dos tempos dos novatos (μ = 4,38 e σ = 2,73, o que dá "
        "mediana e^μ ≈ 80 h). O grupo core é simulado com a mesma forma e a mediana reduzida pelo "
        "tamanho de efeito, de modo que efeito 0 deixa H₀ verdadeira."
    ),
    # Seção 3 — Como os testes funcionam (G2)
    "como_funcionam": (
        "O t de Welch compara as médias dos dois grupos, dividindo a diferença pelo erro padrão sem "
        "supor variâncias iguais, e rejeita H₀ quando |t| cai nas caudas da distribuição t de "
        "Student, além do quantil de 97,5% (α = 5% bicaudal). O Mann-Whitney ignora os valores e "
        "usa só os postos: a estatística U conta quantas vezes um PR de novato demorou mais que um "
        "do core, e rejeita H₀ quando U fica longe de n_a·n_b/2. O p-valor do exemplo é a área "
        "sombreada nas duas caudas além da estatística observada, ou seja, a probabilidade de ver "
        "um resultado pelo menos tão extremo se H₀ fosse verdadeira."
    ),
    "exemplo": (
        "No dataset simulado com efeito 0,2 (mediana do core 20% menor), nenhum dos dois testes "
        "rejeitou H₀ a 5%: Welch com t = −0,97 (p = 0,34) e Mann-Whitney com U = 456 (p = 0,94). "
        "O Welch saiu até com o sinal invertido (d = −0,25), porque um único PR simulado do core com "
        "cerca de 22 mil horas puxou a média do core para 1.070 h, acima da dos novatos (347 h), "
        "enquanto as medianas ficaram quase iguais (102 h × 104 h). Com σ = 2,73 e n = 30, um efeito "
        "de 20% na mediana fica escondido pelo ruído, e a média fica refém dos outliers. Um único "
        "dataset não decide qual teste é melhor: quem responde são as taxas de rejeição em 10.000 "
        "repetições (Sprint 02)."
    ),
}
