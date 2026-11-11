"""Textos das seções do dashboard (S01: seções 1 a 3; S02: seções 4 e 5).

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
    # Seção 4 — Erro tipo I (G3); números de results/tipo1_status.csv
    "erro_tipo_1": (
        "Sem efeito (H₀ verdadeira), o Mann-Whitney ficou perto dos 5% em todos os cenários, entre "
        "4,4% e 4,9%, e só na amostra pequena (n = 10) ficou levemente conservador, com o intervalo "
        "de confiança todo abaixo de 5%. O t de Welch se desviou em todos os cenários e ficou "
        "conservador, rejeitando H₀ em apenas 0,5% (assimetria forte) a 1,3% (base) das repetições, "
        "bem abaixo dos 5% nominais. Isso acontece porque a cauda longa da lognormal infla o desvio "
        "padrão da amostra e, com ele, o denominador do t, então o |t| raramente passa do valor "
        "crítico. Ser conservador parece seguro, mas tem um preço: o Welch quase nunca rejeita H₀, "
        "nem quando o efeito existe."
    ),
    # Seção 5 — Poder (G4); números de results/simulacao.csv e results/poder_vencedor.csv
    "poder": (
        "O Mann-Whitney teve mais poder em todos os cenários e em todos os tamanhos de efeito, e a "
        "vantagem cresce com o efeito: com a mediana do core 50% menor, ele rejeitou H₀ em 14,8% das "
        "repetições no cenário base, contra 2,4% do Welch. A vantagem não muda de lado em nenhuma "
        "situação simulada, mas encolhe na amostra pequena (7,3% × 0,9%) e na assimetria forte "
        "(9,4% × 0,7%), em que os dois testes perdem poder. Mesmo assim, o poder dos dois é baixo: "
        "com σ = 2,73 e n = 30, uma redução de até 50% na mediana fica escondida pelo ruído, e seriam "
        "necessários efeitos ou amostras maiores para chegar a 80%."
    ),
    "violacoes": (
        "Amostra pequena (n = 10): com poucos dados, a média e o desvio ficam ainda mais instáveis e o "
        "Welch quase não rejeita mais (0,7% sem efeito), enquanto o Mann-Whitney mantém o erro tipo I "
        "perto de 5%, mas, com só 100 pares para comparar, também perde poder. Outliers (5% dos PRs "
        "com tempo ×10): um valor gigante desloca a média e infla a variância, o que prejudica o "
        "Welch, mas para o Mann-Whitney ele vira apenas o maior posto, e por isso o poder dele quase "
        "não mudou em relação ao cenário base. Assimetria forte (σ × 1,5): a cauda direita fica tão "
        "longa que o Welch cai para 0,5% de erro tipo I e quase nenhum poder, enquanto o Mann-Whitney "
        "segura os 5% porque compara só a ordem dos valores, embora também perca poder, já que os "
        "dois grupos passam a se sobrepor mais."
    ),
}
