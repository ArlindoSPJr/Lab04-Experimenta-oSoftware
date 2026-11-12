# Roteiro da apresentação oral — Lab04 (P1: t de Welch × Mann-Whitney)

> **Status:** proposta da #54, que continua a #35. A divisão das perguntas e os tempos são uma sugestão: precisam ser aprovados pelos 3 integrantes no PR e ajustados depois do ensaio ([Ensaio](#ensaio)).

- Dashboard: https://lab04-experimentacao-software.streamlit.app/
- Repositório: https://github.com/ArlindoSPJr/Lab04-Experimenta-oSoftware
- GitHub Projects: https://github.com/users/ArlindoSPJr/projects/6

## Como a apresentação funciona

A seção 5 do `Enunciado.pdf` define o formato, e ele manda sobre qualquer outra estimativa:

- até **7 minutos**, **usando o próprio dashboard**;
- o grupo responde às **15 perguntas** do enunciado, com respostas **curtas e diretas (~30 s cada)**;
- cada integrante responde a **pelo menos 4**;
- **o professor pode pedir a qualquer integrante que responda a qualquer pergunta.** Todos precisam saber todas as fichas, não só as suas.

Cada ficha abaixo diz quem responde, onde está a resposta na tela, o que falar em ~30 s, o número que precisa ser dito em voz alta e o que acrescentar se o professor aprofundar. O atalho "índice lateral → P<n>" é o índice das 15 perguntas que a #50 está criando na sidebar; enquanto ele não estiver na `main`, role até a seção indicada.

Todos os números vêm de `results/` (gerados por `python -m lab04.run_all`, semente 42) ou de `dashboard/textos.py`. **Não arredonde nem invente números na fala:** se não lembrar, aponte para a tabela na tela.

## Tabela-resumo

| P | Quem | Seção → bloco do dashboard | Número-chave |
|---|---|---|---|
| 1 | B | 1. Cenário → Pergunta e quadros H₀/H₁ | 30 novatos + 30 core = 60 PRs |
| 2 | B | 1. Cenário → "Por que bicaudal" | α = 5% dividido em 2,5% por cauda |
| 3 | B | 1. Cenário → "De onde vêm os dados"; 2. Os dados → G1 e tabela "Dados reais por grupo" | média 664 h × mediana 96,7 h (novatos) |
| 4 | B | 2. Os dados → quadro "Parâmetros da simulação" | μ = 4,38, σ = 2,73, mediana ≈ 80 h |
| 5 | A | 3. Como os testes funcionam → texto de abertura | Welch: médias · Mann-Whitney: postos |
| 6 | A | 3. Como os testes funcionam → os dois G2 | \|t\| > 2,04 · U < 317 ou U > 583 |
| 7 | A | 3. Como os testes funcionam → G2, tabela do exemplo e "O que o p-valor não é" | p = 0,34 (Welch) e 0,94 (Mann-Whitney) |
| 8 | A | 4. Erro tipo I → quadro ⚖️ "Erro tipo I × erro tipo II" | Welch erra o tipo II em 97,6% (efeito 0,5) |
| 9 | A | 4. Erro tipo I → G3 e tabela "Status do erro tipo I" | Welch 0,5% a 1,3% · MW 4,4% a 4,9% |
| 10 | C | 5. Poder → G4 e tabela "Teste com mais poder" | 14,8% × 2,4% (efeito 0,5, base) |
| 11 | C | 5. Poder → "Por que cada violação pesa mais para um teste" | outliers: MW 15,3% × base 14,8% |
| 12 | C | 4. Erro tipo I → seletor de α = 0,01 (vale para G3 e G4) | poder MW 14,8% → 4,7% |
| 13 | C | 1. Cenário → palpite 🎯; 7. Conclusão → "Palpite × resultado" | MW +3,2 a +12,9 p.p. de poder |
| 14 | C | 6. Dados reais → tabela dos dois testes | p = 0,0046 e 0,044 · mediana 96,7 h × 24,0 h |
| 15 | C | 7. Conclusão → "Recomendação", "Quando a recomendação muda", "Limitações do estudo" | Mann-Whitney · viés de sobrevivência |

Divisão: **B** (ArthurAstolfi) responde 1–4, porque fez a coleta; **A** (ArlindoSPJr) responde 5–9, porque fez o gerador, os testes e a simulação; **C** (CamszMelo) responde 10–15, porque fez os gráficos e o dashboard. B fica com 4 perguntas, A com 5 e C com 6. A P12 está com C, mas a tela dela é o seletor de α no topo da seção 4: C sobe a página até lá.

---

## Fichas das 15 perguntas

### P1 — Qual é o cenário de vocês e o que H₀ e H₁ afirmam, em palavras simples?

- **Quem responde:** B
- **Onde está:** índice lateral → P1 · **seção 1. Cenário** → frase "**Pergunta.**" e os dois quadros H₀ e H₁ lado a lado; as métricas "PRs de novatos / PRs do core team / Total" ficam à direita do texto da fonte.
- **Resposta em ~30 s:** "Comparamos o tempo até o merge dos PRs do pallets/click em dois grupos: novatos, que é o primeiro PR do autor no repositório, e o core team. H₀ diz que o tempo até o merge tem a mesma distribuição nos dois grupos. H₁ diz que as distribuições são diferentes, sem dizer qual grupo demora mais. Usamos 30 PRs de cada grupo, 60 no total."
- **Número-chave:** 30 + 30 = 60 PRs.
- **Se o professor aprofundar:** a pergunta é de Engenharia de Software porque um novato que espera demais pelo merge tende a não voltar a contribuir. Os testes comparados são o t de Welch e o Mann-Whitney, o par P1 do enunciado.

### P2 — O teste de vocês é unicaudal ou bicaudal? Por quê?

- **Quem responde:** B
- **Onde está:** índice lateral → P2 · **seção 1. Cenário** → parágrafo "**Por que bicaudal.**", logo abaixo dos quadros H₀/H₁.
- **Resposta em ~30 s:** "Bicaudal. Antes de ver os dados não havia direção esperada: os PRs do core podiam demorar mais por serem maiores e mexerem no núcleo do código, e os de novatos por precisarem de mais rodadas de revisão. Escolher a cauda depois de olhar os dados dobraria, na prática, a chance de erro tipo I, então os 5% ficam divididos, 2,5% em cada cauda."
- **Número-chave:** 2,5% em cada cauda.
- **Se o professor aprofundar:** a escolha está fixada no código, em `lab04/config.py` (`ALTERNATIVE = "two-sided"`), antes de qualquer resultado. É também a opção mais cautelosa: um unicaudal teria mais poder, mas só se a direção fosse conhecida de antemão.

### P3 — Como os dados reais foram coletados, e o que eles mostraram sobre a forma da distribuição?

- **Quem responde:** B
- **Onde está:** índice lateral → P3 · **seção 1. Cenário** → "**De onde vêm os dados.**" · depois **seção 2. Os dados** → G1 (histogramas real × simulado por grupo, eixo em horas) e a tabela "**Dados reais por grupo**" (média, mediana, desvio, assimetria, outliers).
- **Resposta em ~30 s:** "Coletamos pela API GraphQL do GitHub, com o script `scripts/collect_prs.py`, os PRs mergeados do pallets/click, sem bots e sem automerge, seguindo as regras R1 a R12 do `data/REGRAS_COLETA.md`. Pegamos os 30 mais recentes de cada grupo. Os tempos são muito assimétricos à direita: nos novatos a média é 664 h e a mediana 96,7 h, quase sete vezes menor, e a assimetria fica perto de 1,9 nos dois grupos."
- **Número-chave:** média 664 h × mediana 96,7 h nos novatos.
- **Se o professor aprofundar:** no core a média é 60,9 h e a mediana 24,0 h. Há 1 outlier nos novatos e 4 no core acima de Q3 + 1,5·IQR. Novato é quem está no primeiro PR do histórico completo; core é MEMBER, OWNER ou COLLABORATOR.

### P4 — Como os dados reais ajudaram a escolher os parâmetros da simulação?

- **Quem responde:** B
- **Onde está:** índice lateral → P4 · **seção 2. Os dados** → quadro "**Parâmetros da simulação** (lognormal)" à direita, com as métricas μ, σ e mediana e^μ, e o texto abaixo do G1.
- **Resposta em ~30 s:** "Como os tempos são assimétricos e o log deles é aproximadamente normal, usamos uma lognormal. μ e σ são a média e o desvio do log dos tempos dos novatos: μ = 4,38 e σ = 2,73, o que dá mediana de cerca de 80 h. O core é simulado com a mesma forma e a mediana reduzida pelo tamanho de efeito, então efeito 0 deixa H₀ verdadeira."
- **Número-chave:** μ = 4,38, σ = 2,73.
- **Se o professor aprofundar:** efeito 0,5 quer dizer mediana do core 50% menor. O G1 mostra que o histograma simulado acompanha o real; a diferença é que o core real é bem menos disperso (σ do log 1,32) do que o simulado, que usa 2,73 nos dois grupos.

### P5 — O que cada um dos dois testes compara de fato?

- **Quem responde:** A
- **Onde está:** índice lateral → P5 · **seção 3. Como os testes funcionam** → texto de abertura, logo acima dos dois G2.
- **Resposta em ~30 s:** "O t de Welch compara **médias**: divide a diferença das médias pelo erro padrão, sem supor variâncias iguais. O Mann-Whitney ignora os valores e usa só os **postos**: a estatística U conta quantas vezes um PR de novato demorou mais que um do core. Por isso um PR de milhares de horas mexe muito no Welch e quase nada no Mann-Whitney."
- **Número-chave:** médias × postos.
- **Se o professor aprofundar:** com formas parecidas, o Mann-Whitney equivale a comparar medianas; no geral, ele testa se P(novato > core) é diferente de 1/2, isto é, se um grupo tende a ter valores maiores.

### P6 — No G2: o que é a distribuição da estatística sob H₀, e por que a região de rejeição fica onde fica?

- **Quem responde:** A
- **Onde está:** índice lateral → P6 · **seção 3. Como os testes funcionam** → os dois G2 lado a lado (Welch à esquerda, Mann-Whitney à direita); apontar a curva e as duas caudas sombreadas.
- **Resposta em ~30 s:** "A curva é a distribuição que a estatística teria se H₀ fosse verdadeira: uma t de Student com cerca de 30 graus de liberdade no Welch, e a aproximação normal de U, centrada em n_a·n_b/2 = 450, no Mann-Whitney. A região de rejeição fica nas duas caudas porque o teste é bicaudal, com 2,5% de cada lado: |t| maior que 2,04 no Welch, e U abaixo de 317 ou acima de 583 no Mann-Whitney."
- **Número-chave:** |t| > 2,04 · U < 317 ou U > 583.
- **Se o professor aprofundar:** os graus de liberdade (30,0) vêm da fórmula de Welch-Satterthwaite no exemplo (tabela do exemplo, coluna "Estatística"). As caudas são onde ficam os resultados raros sob H₀; juntas somam α = 5%.

### P7 — O que significa o p-valor do exemplo mostrado no G2? E o que ele não significa?

- **Quem responde:** A
- **Onde está:** índice lateral → P7 · **seção 3. Como os testes funcionam** → área sombreada do p-valor nos G2, a tabela "**Exemplo:**" logo abaixo e o parágrafo "**O que o p-valor não é.**"
- **Resposta em ~30 s:** "No exemplo simulado com efeito 0,2, o Welch deu p = 0,34 e o Mann-Whitney p = 0,94. O p-valor é a área sombreada: a chance de ver uma estatística pelo menos tão extrema **supondo H₀ verdadeira**. Ele **não** é a probabilidade de H₀ ser verdadeira, não mede o tamanho do efeito, e p alto não prova que os grupos são iguais: aqui o efeito existia e nenhum teste detectou, um erro tipo II."
- **Número-chave:** p = 0,34 (Welch) e p = 0,94 (Mann-Whitney).
- **Se o professor aprofundar:** o Welch saiu até com sinal invertido (t = −0,97, d = −0,25), porque um único PR simulado do core com cerca de 22 mil horas puxou a média do core para 1.070 h, acima dos 347 h dos novatos. Um único dataset não decide qual teste é melhor; quem decide são as 10.000 repetições das seções 4 e 5.

### P8 — No cenário de vocês, o que seria um erro tipo I e um erro tipo II? Qual dos dois seria mais grave?

- **Quem responde:** A
- **Onde está:** índice lateral → P8 · **seção 4. Erro tipo I** → quadro ⚖️ "**Erro tipo I × erro tipo II neste cenário**", no fim da seção.
- **Resposta em ~30 s:** "Erro tipo I é concluir que novatos e core têm tempos diferentes quando não têm, o que custaria só um esforço de onboarding desnecessário. Erro tipo II é não detectar uma demora real dos PRs de novatos. Para o grupo, o **tipo II é o mais grave**: novato que espera demais desiste, e o projeto perde gente nova sem perceber. E é o ponto fraco do Welch: com a mediana do core 50% menor, ele errou o tipo II em 97,6% das repetições, contra 85,2% do Mann-Whitney."
- **Número-chave:** erro tipo II de 97,6% (Welch) × 85,2% (Mann-Whitney), cenário base, efeito 0,5.
- **Se o professor aprofundar:** erro tipo II = 1 − poder; 97,6% vem do poder de 2,4% do Welch no G4. Por isso o Welch ser conservador (pouco erro tipo I) não é vantagem aqui: ele compra segurança contra o erro menos grave.

### P9 — No G3, algum teste se afastou de 5%? Ele ficou liberal ou conservador, e por quê?

- **Quem responde:** A
- **Onde está:** índice lateral → P9 · **seção 4. Erro tipo I** → G3 (barras dos dois testes por situação, com a linha de 5%, seletor em α = 0,05) e a tabela "**Status do erro tipo I**" logo abaixo.
- **Resposta em ~30 s:** "O t de Welch se afastou em todas as situações e ficou **conservador**: rejeitou H₀ em só 0,5% (assimetria forte) a 1,3% (base) das repetições. A cauda longa da lognormal infla o desvio padrão da amostra e, com ele, o denominador do t, então o |t| raramente passa do valor crítico. O Mann-Whitney ficou entre 4,4% e 4,9%."
- **Número-chave:** Welch 0,5% a 1,3% · Mann-Whitney 4,4% a 4,9%.
- **Se o professor aprofundar:** o status da tabela vem do IC de 95% da taxa: com 10.000 repetições a margem é de cerca de ±0,4 p.p. O Mann-Whitney só aparece como "conservador" na amostra pequena (4,4%, IC todo abaixo de 5%), porque com 10 × 10 = 100 pares U tem poucos valores possíveis.

### P10 — No G4, qual teste tem mais poder? A diferença entre eles muda conforme o tamanho do efeito?

- **Quem responde:** C
- **Onde está:** índice lateral → P10 · **seção 5. Poder** → G4 (curvas de poder, um painel por situação) e a tabela "**Teste com mais poder**" logo abaixo.
- **Resposta em ~30 s:** "O Mann-Whitney tem mais poder em todas as situações e em todos os tamanhos de efeito, e a vantagem cresce com o efeito: com a mediana do core 50% menor, no cenário base, ele rejeitou H₀ em 14,8% das repetições, contra 2,4% do Welch. A vantagem nunca muda de lado; só encolhe na amostra pequena, 7,3% contra 0,9%, e na assimetria forte, 9,4% contra 0,7%."
- **Número-chave:** 14,8% × 2,4%.
- **Se o professor aprofundar:** o poder dos dois é baixo porque, com σ = 2,73 e n = 30, uma redução de até 50% na mediana fica escondida pelo ruído; seriam necessários efeitos ou amostras maiores para chegar a 80%. Na tabela, a vantagem vai de 3,2 a 12,9 pontos percentuais.

### P11 — Que violação de pressuposto vocês simularam, e por que ela afeta mais um teste do que o outro?

- **Quem responde:** C
- **Onde está:** índice lateral → P11 · **seção 5. Poder** → parágrafo "**Por que cada violação pesa mais para um teste.**", abaixo do G4; os painéis do G4 mostram cada situação.
- **Resposta em ~30 s:** "Simulamos três: amostra pequena (n = 10), outliers (5% dos PRs com tempo ×10) e assimetria forte (σ × 1,5). As três atacam a média e a variância, que são a base do Welch: um valor gigante desloca a média e infla o denominador do t. Para o Mann-Whitney o outlier vira só o maior posto, e por isso o poder dele com outliers quase não mudou: 15,3% contra 14,8% no cenário base, com efeito 0,5."
- **Número-chave:** Mann-Whitney com outliers 15,3% × base 14,8%.
- **Se o professor aprofundar:** na assimetria forte o Welch cai para 0,5% de erro tipo I e quase nenhum poder (0,7%). Com n = 10 a média e o desvio ficam ainda mais instáveis e o Welch rejeita só 0,7% sem efeito; o Mann-Whitney segura o erro tipo I, mas, com só 100 pares, também perde poder (7,3%).

### P12 — Se vocês usassem α = 0,01 em vez de 0,05, o que mudaria no G3 e no G4?

- **Quem responde:** C
- **Onde está:** índice lateral → P12 · **seção 4. Erro tipo I** → seletor "**Nível de significância (α) das seções 4 e 5**", acima do G3: **clicar em 0,01**. O texto logo abaixo do seletor é a resposta; o G3, o G4 e as duas tabelas mudam juntos. Depois de responder, **voltar o seletor para 0,05**.
- **Resposta em ~30 s:** "A linha de referência do G3 desce para 1% e os dois testes rejeitam menos: sem efeito, o Mann-Whitney fica entre 0,78% e 0,87%, e o Welch cai para 0% a 0,04%. No G4 o poder despenca: no cenário base, com efeito 0,5, o Mann-Whitney vai de 14,8% para 4,7%, e o Welch de 2,4% para 0,13%. O Mann-Whitney continua na frente em todas as situações, mas a vantagem cai para no máximo 4,7 pontos."
- **Número-chave:** poder do Mann-Whitney 14,8% → 4,7%.
- **Se o professor aprofundar:** α menor troca menos falsos positivos por mais erro tipo II, e isso pesa mais para o Welch, que já era conservador. Nos dados reais, o Welch (p = 0,0046) continuaria rejeitando H₀ a 1%, mas o Mann-Whitney (p = 0,044) deixaria de rejeitar.

### P13 — A simulação confirmou o que o grupo esperava antes de simular? Se não, o que explica a diferença?

- **Quem responde:** C
- **Onde está:** índice lateral → P13 · **seção 1. Cenário** → quadro 🎯 do palpite (mostrar rápido que foi registrado antes) · **seção 7. Conclusão** → subtítulo "**Palpite × resultado**".
- **Resposta em ~30 s:** "No principal, sim: o Mann-Whitney venceu, com 3,2 a 12,9 pontos percentuais a mais de poder, e manteve o erro tipo I entre 4,4% e 4,9%. Acertamos que o Welch seria conservador, mas subestimamos o quanto: ele ficou abaixo de 5% em todas as situações, não só nas mais assimétricas. Não previmos que o Mann-Whitney também teria pouco poder, no máximo cerca de 15%, nem que nos dados reais o Welch teria p menor."
- **Número-chave:** +3,2 a +12,9 p.p. de poder para o Mann-Whitney.
- **Se o professor aprofundar:** a diferença nos dados reais tem explicação: a simulação deu aos dois grupos a dispersão dos novatos (σ = 2,73), mas o core real é bem menos disperso (σ do log 1,32), e isso encolhe o erro padrão do t. A simulação foi mais dura com o Welch do que os dados reais.

### P14 — Nos dados reais, os dois testes chegaram à mesma conclusão? O tamanho do efeito tem importância prática?

- **Quem responde:** C
- **Onde está:** índice lateral → P14 · **seção 6. Dados reais** → tabela "**Os dois testes aplicados aos 60 PRs reais**" (estatística, p-valor, tamanho de efeito, conclusão) e o texto abaixo.
- **Resposta em ~30 s:** "Sim, os dois rejeitam H₀ a 5%: Welch com t = 3,07 e p = 0,0046, Mann-Whitney com U = 587 e p = 0,044, os dois dizendo que novatos demoram mais. O efeito importa na prática: a mediana dos novatos, 96,7 h, cerca de 4 dias, é quatro vezes a do core, 24,0 h. O d de Cohen é 0,79, e o r rank-biserial de 0,30 diz que em 65% dos pares novato × core o PR do novato demorou mais."
- **Número-chave:** mediana 96,7 h × 24,0 h (quatro vezes).
- **Se o professor aprofundar:** o Welch rejeitou com p menor, depois de ser tão conservador na simulação, porque a diferença real (mediana do core cerca de 75% menor) é maior que o maior efeito simulado (50%), o core real é menos disperso e os valores extremos estão do lado do efeito: a cauda dos novatos vai até 4.447 h. Um único PR extremo no core poderia ter escondido a diferença, como no exemplo da seção 3.

### P15 — Qual teste vocês recomendam, em que situação mudariam a recomendação, e qual é a principal limitação do estudo?

- **Quem responde:** C
- **Onde está:** índice lateral → P15 · **seção 7. Conclusão** → quadro "**Recomendação**", subtítulo "**Quando a recomendação muda**" e subtítulo "**Limitações do estudo**" (a primeira da lista é a principal).
- **Resposta em ~30 s:** "Recomendamos o Mann-Whitney: segurou o erro tipo I perto de 5% e teve mais poder em todas as situações, enquanto o Welch ficou entre 0,5% e 1,3% e quase nunca detectou reduções de até 50% na mediana. Mudaríamos para o Welch com dados quase normais, como o log do tempo, com amostras bem maiores que 30, ou se a pergunta fosse sobre a média, como o total de horas de espera. A principal limitação é o viés de sobrevivência: só entram PRs mergeados, e os de novatos fechados sem merge, provavelmente os mais lentos, ficaram de fora."
- **Número-chave:** Welch 0,5% a 1,3% de erro tipo I × Mann-Whitney perto de 5%.
- **Se o professor aprofundar:** as outras limitações estão na lista: associação ao core é a de hoje, "novato" é só neste repositório, janelas de tempo diferentes (cerca de 11 meses × 3), PRs em rascunho contam o tempo de draft e o core é pequeno. Como o core tem forma diferente, a conclusão do Mann-Whitney deve ser lida como "um PR de novato tende a demorar mais", e não como "as medianas diferem".

---

## Tempo total (≤ 7 min)

15 respostas de ~30 s dão 7:30, então a maioria precisa sair em 25 s. A soma prevista abaixo é **6:45**, com 15 s de folga.

| Bloco | Quem | Perguntas | Tempo | Acumulado |
|---|---|---|---|---|
| Topo (links) | B | — | 0:05 | 0:05 |
| Cenário e dados | B | P1 25 s · P2 20 s · P3 25 s · P4 25 s | 1:35 | 1:40 |
| Testes e erro tipo I | A | P5 20 s · P6 30 s · P7 30 s · P8 25 s · P9 30 s | 2:15 | 3:55 |
| Poder, dados reais e conclusão | C | P10 30 s · P11 30 s · P12 25 s · P13 25 s · P14 30 s · P15 30 s | 2:50 | 6:45 |
| **Folga** | | | 0:15 | **7:00** |

Se o ensaio passar de 6:45, corte primeiro as frases "Se o professor aprofundar" (elas só entram se ele perguntar) e depois o segundo número de cada resposta.

## Ordem de rolagem da página

Se o professor seguir a ordem do enunciado, a página desce sem voltar, exceto na P12 e na P13:

1. Topo (links) → **seção 1**: P1, P2 (e P3, primeira parte: quadro da fonte).
2. **Seção 2**: P3 (G1 e tabela), P4. Troca B → A.
3. **Seção 3**: P5, P6, P7.
4. **Seção 4**: P8 (quadro ⚖️, no fim da seção), P9 (G3, no começo). Troca A → C.
5. **Seção 5**: P10, P11.
6. **Volta para a seção 4**: P12 (seletor α = 0,01, olhar G3 e descer até o G4), **voltar o seletor para 0,05**.
7. **Seção 7** (P13, com uma subida rápida ao 🎯 da seção 1) → **seção 6**: P14 → **seção 7**: P15.

Se o professor pular perguntas, use o índice lateral (P1–P15) em vez de rolar.

## Plano B e plano C

**Plano B — Streamlit Cloud fora do ar.** No notebook da projeção, com o repositório clonado e o ambiente instalado na véspera:

```bash
python -m lab04.run_all          # só se results/ estiver vazio (~10 s)
streamlit run dashboard/app.py   # http://localhost:8501
```

É o mesmo dashboard, lendo os mesmos `results/`. Avisar: "o Streamlit Cloud está fora; este é o mesmo dashboard rodando a partir do repositório".

**Plano C — nem o local abre.** Mostrar no GitHub os CSVs de `results/` (`simulacao.csv`, `tipo1_status.csv`, `poder_vencedor.csv`, `dados_reais.csv`) e o `params.json`, e o PDF do dashboard salvo na véspera (pendrive e celular). As fichas acima continuam valendo: troque "aponte para o gráfico" por "aponte para a linha da tabela".

## Checklist pré-apresentação

- [ ] **Véspera:** `pytest -q` e `python -m lab04.run_all` na `main` atualizada; conferir que os números do dashboard batem com as fichas.
- [ ] **Véspera:** salvar o PDF do dashboard (plano C) e preparar o ambiente local (plano B).
- [ ] **Véspera:** conferir que o índice lateral (#50) está publicado e que cada P<n> leva ao bloco da ficha.
- [ ] **10–15 min antes:** abrir o dashboard publicado para "acordar" o app no Streamlit Cloud.
- [ ] Seletor de α em **0,05** ao começar.
- [ ] Zoom do navegador legível do fundo da sala; Welch e Mann-Whitney com as cores de sempre em todos os gráficos.
- [ ] Abas abertas: dashboard, repositório, GitHub Projects.
- [ ] Combinar que quem responde controla a rolagem; cronômetro com quem não está falando, aviso aos 6:00.

## Ensaio

Anotar o tempo real de cada resposta e ajustar as fichas se o total passar de 7:00. No segundo ensaio, o "professor" sorteia perguntas fora de ordem e para qualquer integrante.

| P | Quem | Previsto | Ensaio 1 | Ensaio 2 | Ajuste |
|---|---|---|---|---|---|
| Topo | B | 0:05 | | | |
| 1 | B | 0:25 | | | |
| 2 | B | 0:20 | | | |
| 3 | B | 0:25 | | | |
| 4 | B | 0:25 | | | |
| 5 | A | 0:20 | | | |
| 6 | A | 0:30 | | | |
| 7 | A | 0:30 | | | |
| 8 | A | 0:25 | | | |
| 9 | A | 0:30 | | | |
| 10 | C | 0:30 | | | |
| 11 | C | 0:30 | | | |
| 12 | C | 0:25 | | | |
| 13 | C | 0:25 | | | |
| 14 | C | 0:30 | | | |
| 15 | C | 0:30 | | | |
| **Total** | | **6:45** | | | |

Data do ensaio: ______ · Presentes: ______ · Observações: ______

---

## Apêndice — Perguntas extras

Não fazem parte das 15. Vêm da seção 6 do enunciado ("Para discutir: tamanho da amostra") e de dúvidas comuns. Respostas de até 30 s, para qualquer integrante.

**Com o n real (30 por grupo), qual o poder de cada teste para o efeito observado?**
O cenário base já usa n = 30, igual aos dados reais. Lá, com o maior efeito simulado (mediana do core 50% menor), o poder foi de 14,8% no Mann-Whitney e 2,4% no Welch. O efeito real é maior (cerca de 75% menor) e o core real é menos disperso, então o poder real deve ser maior que isso; o G4 só dá o piso, porque não simulamos um efeito desse tamanho.

**Quantas observações seriam necessárias para chegar a 80% de poder? Seria viável?**
Bem mais que 30 por grupo: no cenário base, com efeito 0,5, nem o Mann-Whitney passa de cerca de 15%. Não simulamos um n maior, então não temos o número exato. A viabilidade esbarra no próprio repositório: o core do pallets/click é pequeno, e 30 PRs do core já cobrem só cerca de 3 meses; centenas de PRs exigiriam anos de histórico, com o projeto mudando no meio.

**Com amostras muito grandes, o que importa mais: o p-valor ou o tamanho do efeito?**
O tamanho do efeito. Com n grande, até uma diferença de minutos dá p minúsculo. Por isso a tabela da seção 6 mostra o d de Cohen (0,79) e o r rank-biserial (0,30), e a P14 usa a mediana, 96,7 h × 24,0 h, para dizer que a diferença importa na prática.

**Se o resultado real não fosse significativo, provaria que não há efeito?**
Não. Com o poder tão baixo da simulação, um p alto seria o resultado mais provável mesmo com efeito real: é o erro tipo II do exemplo da seção 3 (efeito 0,2, p = 0,34 e 0,94).

**O tamanho da amostra muda qual teste é o melhor?**
Na simulação, não: o Mann-Whitney venceu com n = 10 e n = 30. Os pressupostos pesam mais com n pequeno: o Welch caiu de 1,3% para 0,7% de erro tipo I. Com amostras muito maiores a média fica mais perto da normal e o Welch deixa de ser tão conservador, e aí a vantagem pode diminuir.

**Por que 10.000 repetições?**
Para a taxa estimada ter pouca variação: perto de 5%, a margem de erro fica em cerca de ±0,4 ponto percentual. Isso basta para dizer com segurança que o Welch (0,5% a 1,3%) está abaixo de 5%.
