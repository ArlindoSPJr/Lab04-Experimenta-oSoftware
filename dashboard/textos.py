"""Textos das seções do dashboard (S01: seções 1 a 3; S02: seções 4 e 5; Final: 6 e 7).

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
    "bicaudal": (
        "O teste é bicaudal porque, antes de ver os dados, não havia uma direção esperada para a "
        "diferença: os PRs do core podiam demorar mais, por serem maiores e mexerem em partes "
        "centrais do código, e os de novatos podiam demorar mais, por precisarem de mais rodadas de "
        "revisão. Escolher a cauda depois de olhar os dados dobraria, na prática, a chance de erro "
        "tipo I, então os 5% de α ficam divididos entre as duas caudas, com 2,5% em cada uma."
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
    "p_valor_nao_e": (
        "O p-valor do exemplo (0,34 no Welch e 0,94 no Mann-Whitney) não é a probabilidade de H₀ "
        "ser verdadeira: ele é calculado supondo H₀ verdadeira e diz só o quão raro seria um "
        "resultado tão extremo nesse caso. Ele também não mede o tamanho do efeito, papel do d de "
        "Cohen e do r rank-biserial, porque um efeito pequeno com amostra grande também dá p "
        "minúsculo. E p alto não prova que não há diferença: no exemplo o efeito existia (mediana do "
        "core 20% menor) e nenhum dos testes o detectou, o que é um erro tipo II, e não uma prova "
        "de que os grupos são iguais."
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
    # Números de results/tipo1_status.csv e results/simulacao.csv (base, efeito 0,5)
    "erros_tipo": (
        "Neste cenário, o erro tipo I é concluir que PRs de novatos e do core têm tempos de merge "
        "diferentes quando não têm, o que custaria só um esforço de onboarding desnecessário, e o "
        "erro tipo II é deixar de detectar uma demora real dos PRs de novatos. Para o grupo, o erro "
        "tipo II é o mais grave: novatos que esperam demais pelo merge tendem a desistir de "
        "contribuir, e o projeto perde gente nova sem perceber. E esse é justamente o ponto fraco do "
        "t de Welch: conservador, ele errou pouco sem efeito (0,5% a 1,3%), mas com a mediana do "
        "core 50% menor detectou a diferença em só 2,4% das repetições no cenário base, ou seja, "
        "cometeu erro tipo II em 97,6% delas, contra 85,2% do Mann-Whitney (poder de 14,8%)."
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
    # Seção 6 — Dados reais; números de tabela_dados_reais(load_real_data()) e describe_real
    "dados_reais": (
        "Nos 60 PRs reais os dois testes concordam e rejeitam H₀ a 5%: o t de Welch deu t = 3,07 "
        "(p = 0,0046) e o Mann-Whitney deu U = 587 (p = 0,044), os dois apontando que os PRs de "
        "novatos demoram mais para ser mergeados. O efeito é relevante na prática: a mediana dos "
        "novatos (96,7 h, cerca de 4 dias) é quatro vezes a do core (24,0 h), o d de Cohen é 0,79 e o "
        "r rank-biserial de 0,30 indica que, em 65% dos pares novato × core, o PR do novato demorou "
        "mais. O Welch ter rejeitado com p menor que o do Mann-Whitney, depois de ser tão "
        "conservador na simulação, tem explicação: a diferença real é maior que o maior efeito "
        "simulado (mediana do core cerca de 75% menor, contra no máximo 50%) e o core real é bem "
        "menos disperso que o simulado (σ do log de 1,32, contra os 2,73 usados para os dois "
        "grupos), o que encolhe o erro padrão do t. Além disso, a cauda longa dos novatos (até "
        "4.447 h) puxa a média deles para 664 h, contra 60,9 h do core, ou seja, aqui os valores "
        "extremos jogam a favor do Welch porque estão do lado do efeito, mas um único PR extremo no "
        "outro grupo poderia ter escondido a diferença, como no exemplo simulado da seção 3."
    ),
    # Seção 7 — Conclusão; números de results/tipo1_status.csv, simulacao.csv e poder_vencedor.csv
    "conclusao_palpite": (
        "Acertamos o principal: o Mann-Whitney venceu, com mais poder em todos os 4 cenários e em "
        "todos os tamanhos de efeito (de 3,2 a 12,9 pontos percentuais a mais que o Welch), e manteve "
        "o erro tipo I entre 4,4% e 4,9% (Q1 e Q3). Também acertamos que o Welch seria conservador, "
        "mas subestimamos o quanto: ele ficou abaixo de 5% em todos os cenários, e não só nos mais "
        "assimétricos, com erro tipo I entre 0,5% e 1,3% e poder de no máximo 2,4% mesmo com a "
        "mediana do core 50% menor (Q2). O que não previmos foi que o Mann-Whitney também teria "
        "pouco poder, no máximo cerca de 15% (efeito 0,5), porque com σ = 2,73 e n = 30 os grupos "
        "simulados se sobrepõem muito, e que nos dados reais o Welch rejeitaria H₀ com p menor que "
        "o do Mann-Whitney (0,0046 × 0,044). Isso mostra que a simulação, ao dar aos dois grupos a "
        "mesma dispersão dos novatos, foi mais dura com o Welch do que os dados reais, em que o core "
        "é bem menos disperso."
    ),
    "conclusao_recomendacao": (
        "Para tempos de merge de PRs, recomendamos o Mann-Whitney como teste principal. Na simulação "
        "calibrada com os dados reais, ele segurou o erro tipo I perto de 5% e teve mais poder que o "
        "t de Welch em todos os cenários, inclusive com outliers e assimetria forte, enquanto o Welch "
        "ficou conservador (0,5% a 1,3%) e quase nunca detectou reduções de até 50% na mediana. Ele "
        "também responde à pergunta mais natural para esse tipo de dado, se um PR de novato tende a "
        "demorar mais que um do core, sem depender de uma média dominada por poucos PRs de milhares "
        "de horas. O Welch pode entrar como complemento, mas, sozinho, um resultado não significativo "
        "dele não quer dizer que o efeito não existe."
    ),
    "conclusao_quando_muda": (
        "A recomendação mudaria se os dados fossem quase normais, por exemplo ao analisar o log do "
        "tempo de merge, caso em que o t de Welch fica perto dos 5% e tem poder parecido com o do "
        "Mann-Whitney. Também mudaria com amostras muito maiores que 30 por grupo, em que a média "
        "amostral fica mais perto da normal e o Welch deixa de ser tão conservador (na simulação ele "
        "já foi menos conservador com n = 30, 1,3%, do que com n = 10, 0,7%), e quando a pergunta for "
        "sobre a média, como o total de horas de espera de cada grupo, que o Mann-Whitney não "
        "responde porque compara postos e não médias. Por fim, se os dois grupos tiverem formas muito "
        "diferentes, como aqui, em que o core é bem menos disperso, o Mann-Whitney deixa de comparar "
        "só as medianas e passa a dizer se um grupo tende a ter valores maiores que o outro, e a "
        "conclusão deve ser lida nesse sentido."
    ),
    # Seção 7 — Limitações; as 6 de data/REGRAS_COLETA.md ("Limitações conhecidas")
    "limitacoes": (
        "- **Viés de sobrevivência (a principal):** só entram PRs mergeados, então os PRs de "
        "novatos fechados sem merge, provavelmente os mais lentos ou problemáticos, ficam de fora, "
        "e a demora real dos novatos tende a ser maior que a medida.\n"
        "- **Associação atual:** o grupo do autor é o de hoje, então quem entrou no core "
        "recentemente tem os PRs antigos contados como core.\n"
        "- **Novato só neste repositório:** a pessoa pode ter experiência em outros projetos.\n"
        "- **Janelas de tempo diferentes:** os novatos cobrem cerca de 11 meses e o core cerca de "
        "3, e mudanças no projeto nesse período (releases, férias dos mantenedores) se misturam ao "
        "efeito.\n"
        "- **PRs em rascunho:** o tempo conta a partir da abertura do PR, mesmo que ele tenha "
        "começado como draft, o que infla o tempo dos PRs que passaram por rascunho.\n"
        "- **Core team pequeno:** poucas pessoas revisam os PRs, então a disponibilidade "
        "individual delas pesa nos tempos."
    ),
}
