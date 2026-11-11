# Roteiro da apresentação oral — Lab04 (P1: t de Welch × Mann-Whitney)

> **Status:** proposta, a ser aprovada pelos 3 integrantes no PR da #35. A divisão das falas e os tempos são uma sugestão e devem ser ajustados depois do ensaio (seção [Ensaio](#6-ensaio)).

- Dashboard: https://lab04-experimentacao-software.streamlit.app/
- Repositório: https://github.com/ArlindoSPJr/Lab04-Experimenta-oSoftware
- GitHub Projects: https://github.com/users/ArlindoSPJr/projects/6

## Formato exigido pelo enunciado

O `Enunciado.pdf` (seção 5, "Apresentação oral: 15 perguntas") define o formato, e ele manda sobre qualquer outra estimativa:

- a apresentação dura **até 7 minutos** e é feita **sobre o próprio dashboard**;
- o grupo responde às **15 perguntas** do enunciado, com respostas **curtas e diretas (~30 s cada)**;
- as perguntas são divididas entre os integrantes, e **cada um responde a pelo menos 4**;
- **o professor pode pedir a qualquer integrante que responda a qualquer pergunta.** Por isso todos precisam saber todas as respostas deste roteiro, não só as suas.

O roteiro abaixo segue as 7 seções do dashboard, de cima para baixo, e encaixa as 15 perguntas na seção em que a resposta aparece na tela. Assim a rolagem da página acompanha a fala, e as perguntas saem praticamente na ordem do enunciado.

Todos os números vêm de `results/` (gerados por `python -m lab04.run_all`, semente 42) ou de `dashboard/textos.py`. **Não arredonde nem invente números na fala:** se não lembrar, aponte para a tabela na tela.

---

## 1. Roteiro por seção

### Divisão proposta das falas

| Integrante | Seções | Perguntas do enunciado | Por quê |
|---|---|---|---|
| **B** (ArthurAstolfi) | Topo, 1. Cenário, 2. Os dados | 1, 2, 3, 4 | Fez a coleta dos dados reais (R12 do `data/REGRAS_COLETA.md`) |
| **A** (ArlindoSPJr) | 3. Como os testes funcionam, 4. Erro tipo I | 5, 6, 7, 8, 9 | Fez o gerador, os testes e a simulação |
| **C** (CamszMelo) | 5. Poder, 6. Dados reais, 7. Conclusão | 10, 11, 12, 13, 14, 15 | Fez os gráficos e o dashboard |

São só duas trocas de apresentador (B → A no início da seção 3, A → C no início da seção 5). Cada integrante responde a pelo menos 4 perguntas, como exige o enunciado.

### Tempo estimado

| # | Seção do dashboard | Quem | Perguntas | Tempo | Acumulado |
|---|---|---|---|---|---|
| — | Topo (links) | B | — | 0:05 | 0:05 |
| 1 | Cenário | B | 1, 2 | 0:50 | 0:55 |
| 2 | Os dados (G1) | B | 3, 4 | 0:55 | 1:50 |
| 3 | Como os testes funcionam (G2) | A | 5, 6, 7 | 1:20 | 3:10 |
| 4 | Erro tipo I (G3) | A | 8, 9 | 0:50 | 4:00 |
| 5 | Poder (G4) | C | 10, 11, 12 | 1:15 | 5:15 |
| 6 | Dados reais (tabela) | C | 14 | 0:25 | 5:40 |
| 7 | Conclusão | C | 13, 15 | 0:55 | 6:35 |
| | **Folga** | | | 0:25 | **7:00** |

Se o ensaio passar de 6:35, corte primeiro os detalhes marcados como *(se sobrar tempo)*.

---

### Topo — B (0:05)

**Na tela:** o topo do dashboard, com os links do dashboard, do repositório e do GitHub Projects.

**Fala:** "Este é o nosso dashboard do Lab04, par P1, t de Welch contra Mann-Whitney. Os links do dashboard, do repositório e do Projects estão aqui no topo."

### Seção 1. Cenário — B (0:50) · perguntas 1 e 2

**Na tela:** a pergunta, H₀/H₁, o quadro "De onde vêm os dados" e o palpite 🎯.

**Pergunta 1 — cenário, H₀ e H₁ em palavras simples.**
"Queremos saber se o PR de quem está contribuindo pela primeira vez com o pallets/click demora um tempo diferente para ser mergeado do que o PR de alguém do core team. H₀ diz que o tempo até o merge tem a mesma distribuição nos dois grupos; H₁ diz que as distribuições são diferentes."

**Pergunta 2 — unicaudal ou bicaudal?**
"Bicaudal. A pergunta é se o tempo é *diferente*, e antes de ver os dados não tínhamos motivo forte para descartar o lado oposto: PRs do core podem ser refatorações grandes e demorar mais. O teste bicaudal também é o mais cauteloso, porque divide os 5% entre as duas caudas."

*(se sobrar tempo)* "Antes de simular registramos o palpite: o Mann-Whitney venceria, e o Welch ficaria conservador nos cenários mais assimétricos."

### Seção 2. Os dados (G1) — B (0:55) · perguntas 3 e 4

**Na tela:** o G1 (histogramas real × simulado por grupo, eixo em horas em escala log) e a tabela de parâmetros da lognormal.

**Pergunta 3 — como os dados foram coletados e o que mostraram.**
"Coletamos pela API GraphQL do GitHub, com um script do repositório, os PRs mergeados do pallets/click até 2026-11-04, sem bots e sem automerge. Novato é quem está no primeiro PR do histórico completo; core é MEMBER, OWNER ou COLLABORATOR. Pegamos os 30 mais recentes de cada grupo, 60 no total. Os dados são muito assimétricos à direita: nos novatos a média é 664 h e a mediana 96,7 h."

**Pergunta 4 — como os dados reais definiram os parâmetros da simulação.**
"Como o log dos tempos é aproximadamente normal, usamos uma lognormal com μ e σ iguais à média e ao desvio do log dos tempos dos novatos: μ = 4,38 e σ = 2,73, o que dá mediana de cerca de 80 h. O core é simulado com a mesma forma e a mediana reduzida pelo tamanho de efeito, então efeito 0 deixa H₀ verdadeira."

> **Frase-chave do G1:** "Os tempos de merge são muito assimétricos — nos novatos a média de 664 h é quase sete vezes a mediana de 96,7 h —, por isso simulamos com uma lognormal ajustada ao log dos tempos reais (μ = 4,38, σ = 2,73)."

### Seção 3. Como os testes funcionam (G2) — A (1:20) · perguntas 5, 6 e 7

**Na tela:** os dois G2 lado a lado (Welch à esquerda, Mann-Whitney à direita) e a tabela do exemplo logo abaixo.

**Pergunta 5 — o que cada teste compara de fato.**
"O t de Welch compara **médias**: divide a diferença das médias pelo erro padrão, sem supor variâncias iguais. O Mann-Whitney ignora os valores e usa só os **postos**: o U conta quantas vezes um PR de novato demorou mais que um do core. Com formas parecidas isso equivale a comparar medianas; no geral, ele testa se um grupo tende a ter valores maiores que o outro."

**Pergunta 6 — a distribuição sob H₀ e onde fica a região de rejeição.**
"A curva é a distribuição que a estatística teria se H₀ fosse verdadeira: uma t de Student com cerca de 30 graus de liberdade para o Welch, e a aproximação normal de U, centrada em n_a·n_b/2 = 450, para o Mann-Whitney. A região de rejeição fica nas duas caudas porque o teste é bicaudal, com 2,5% de cada lado: |t| > 2,04 no Welch, e U abaixo de 317 ou acima de 583 no Mann-Whitney."

**Pergunta 7 — o que o p-valor do exemplo significa e o que não significa.**
"No exemplo simulado com efeito 0,2, o Welch deu t = −0,97 com p = 0,34, e o Mann-Whitney deu U = 456 com p = 0,94. O p-valor é a área sombreada: a probabilidade de ver uma estatística pelo menos tão extrema **se H₀ fosse verdadeira**. Ele **não** é a probabilidade de H₀ ser verdadeira nem mede o tamanho do efeito. Aliás, neste exemplo H₀ é falsa — simulamos o core 20% mais rápido —, então não rejeitar foi um erro tipo II, e um único dataset não decide qual teste é melhor."

> **Frase-chave do G2:** "O p-valor do exemplo (0,34 no Welch, 0,94 no Mann-Whitney) é a área sombreada além da estatística observada nas duas caudas — a chance de um resultado tão extremo se H₀ fosse verdadeira, não a chance de H₀ ser verdadeira."

### Seção 4. Erro tipo I (G3) — A (0:50) · perguntas 8 e 9

**Na tela:** o G3 (barras dos dois testes por situação, com a linha de 5%) e a tabela de status.

**Pergunta 8 — erro tipo I e tipo II no nosso cenário; qual é mais grave.**
"Erro tipo I seria concluir que novatos e core têm tempos diferentes quando não têm — o projeto poderia mudar o processo de revisão à toa. Erro tipo II seria não detectar que os novatos esperam mais quando de fato esperam — e novato que espera demais tende a não voltar. Para nós o tipo II é o mais grave, porque investigar um alarme falso custa pouco, e perder contribuidores custa muito." *(posição do grupo — confirmar no ensaio)*

**Pergunta 9 — algum teste se afastou de 5%? Liberal ou conservador, e por quê?**
"O Welch se afastou em todos os cenários e ficou **conservador**: rejeitou H₀ em só 0,5% (assimetria forte) a 1,3% (base) das repetições. A cauda longa da lognormal infla o desvio padrão da amostra e, com ele, o denominador do t, então o |t| raramente passa do valor crítico. O Mann-Whitney ficou entre 4,4% e 4,9%; só na amostra pequena (n = 10) o intervalo de confiança ficou todo abaixo de 5%."

> **Frase-chave do G3:** "Com H₀ verdadeira, o Mann-Whitney ficou perto dos 5% (4,4% a 4,9%) e o t de Welch ficou conservador em todas as situações, rejeitando só 0,5% a 1,3% das vezes."

### Seção 5. Poder (G4) — C (1:15) · perguntas 10, 11 e 12

**Na tela:** o G4 (curvas de poder dos dois testes, um painel por situação) e a tabela "Teste com mais poder".

**Pergunta 10 — qual tem mais poder e se a diferença muda com o efeito.**
"O Mann-Whitney teve mais poder em todos os cenários e em todos os tamanhos de efeito, e a vantagem cresce com o efeito: com a mediana do core 50% menor, ele rejeitou H₀ em 14,8% das repetições no cenário base, contra 2,4% do Welch. A vantagem nunca muda de lado, só encolhe na amostra pequena (7,3% × 0,9%) e na assimetria forte (9,4% × 0,7%)."

**Pergunta 11 — que violação simularam e por que afeta mais um teste.**
"Simulamos três: amostra pequena (n = 10), outliers (5% dos PRs com tempo ×10) e assimetria forte (σ × 1,5). Todas atacam a média e a variância, que são a base do Welch: um valor gigante desloca a média e infla o denominador do t. Para o Mann-Whitney o outlier vira só o maior posto, por isso o poder dele com outliers quase não mudou em relação ao cenário base (cerca de 15% nos dois casos no efeito 0,5)."

**Pergunta 12 — o que mudaria com α = 0,01.**
"No G3 a linha de referência desceria para 1%, e um teste válido deveria rejeitar perto de 1% sob H₀. No G4 todas as curvas desceriam: com α menor, cometemos menos erro tipo I e mais erro tipo II, então o poder, que já é baixo, cairia nos dois testes. Nos dados reais, o Welch (p = 0,0046) continuaria rejeitando H₀, mas o Mann-Whitney (p = 0,044) deixaria de rejeitar." *(não simulamos α = 0,01; não cite taxas para esse α)*

> **Frase-chave do G4:** "O Mann-Whitney tem mais poder em todas as situações e a vantagem cresce com o efeito — 14,8% contra 2,4% do Welch com a mediana do core 50% menor —, mas o poder dos dois é baixo, porque com σ = 2,73 e n = 30 o ruído esconde o efeito."

### Seção 6. Dados reais (tabela) — C (0:25) · pergunta 14

**Na tela:** a tabela com estatística, p-valor, tamanho de efeito e conclusão de cada teste.

**Pergunta 14 — os testes concordaram? O efeito importa na prática?**
"Sim, os dois rejeitam H₀ a 5%: Welch com t = 3,07 (p = 0,0046) e Mann-Whitney com U = 587 (p = 0,044), os dois dizendo que novatos demoram mais. O efeito é relevante na prática: a mediana dos novatos, 96,7 h ou cerca de 4 dias, é quatro vezes a do core, 24,0 h; o d de Cohen é 0,79 e o r rank-biserial de 0,30 diz que em 65% dos pares novato × core o PR do novato demorou mais."

> **Frase-chave da tabela:** "Nos 60 PRs reais os dois testes rejeitam H₀ — Welch p = 0,0046, Mann-Whitney p = 0,044 — e o efeito importa: a mediana dos novatos (96,7 h) é quatro vezes a do core (24,0 h)."

### Seção 7. Conclusão — C (0:55) · perguntas 13 e 15

**Na tela:** os três blocos da conclusão (palpite × encontrado, recomendação, quando a recomendação muda) e as limitações.

**Pergunta 13 — a simulação confirmou o palpite?**
"No principal, sim: o Mann-Whitney venceu, com 3,2 a 12,9 pontos percentuais a mais de poder, e manteve o erro tipo I entre 4,4% e 4,9%. Acertamos que o Welch seria conservador, mas subestimamos o quanto: ele ficou abaixo de 5% em todos os cenários, não só nos mais assimétricos. Não previmos que o Mann-Whitney também teria pouco poder, no máximo cerca de 15%, nem que nos dados reais o Welch teria p menor. Isso aconteceu porque a simulação deu aos dois grupos a dispersão dos novatos, e o core real é bem menos disperso."

**Pergunta 15 — recomendação, quando muda e principal limitação.**
"Recomendamos o Mann-Whitney para tempos de merge de PRs: segura os 5% e tem mais poder em todas as situações, inclusive com outliers e assimetria forte. A recomendação mudaria se os dados fossem quase normais (por exemplo, analisando o log do tempo), com amostras bem maiores que 30 por grupo, ou se a pergunta fosse sobre a média, como o total de horas de espera. A principal limitação é o viés de sobrevivência: só entram PRs mergeados, e os PRs de novatos fechados sem merge, provavelmente os mais lentos, ficaram de fora."

> **Frase-chave da conclusão:** "Recomendamos o Mann-Whitney: na simulação calibrada com os dados reais ele manteve o erro tipo I entre 4,4% e 4,9% e teve mais poder em todas as situações, enquanto o Welch ficou conservador (0,5% a 1,3%) e quase nunca detectou reduções de até 50% na mediana."

---

## 2. Frases-chave (cola rápida)

| Onde | Quem | Frase que precisa ser dita |
|---|---|---|
| G1 | B | Os tempos de merge são muito assimétricos — nos novatos a média de 664 h é quase sete vezes a mediana de 96,7 h —, por isso simulamos com uma lognormal ajustada ao log dos tempos reais (μ = 4,38, σ = 2,73). |
| G2 | A | O p-valor do exemplo (0,34 no Welch, 0,94 no Mann-Whitney) é a área sombreada além da estatística observada nas duas caudas — a chance de um resultado tão extremo se H₀ fosse verdadeira, não a chance de H₀ ser verdadeira. |
| G3 | A | Com H₀ verdadeira, o Mann-Whitney ficou perto dos 5% (4,4% a 4,9%) e o t de Welch ficou conservador em todas as situações, rejeitando só 0,5% a 1,3% das vezes. |
| G4 | C | O Mann-Whitney tem mais poder em todas as situações e a vantagem cresce com o efeito — 14,8% contra 2,4% do Welch com a mediana do core 50% menor —, mas o poder dos dois é baixo. |
| Tabela | C | Nos 60 PRs reais os dois testes rejeitam H₀ — Welch p = 0,0046, Mann-Whitney p = 0,044 — e a mediana dos novatos (96,7 h) é quatro vezes a do core (24,0 h). |
| Conclusão | C | Recomendamos o Mann-Whitney: manteve o erro tipo I entre 4,4% e 4,9% e teve mais poder em todas as situações, enquanto o Welch ficou conservador (0,5% a 1,3%). |

---

## 3. Perguntas prováveis da banca (além das 15)

Respostas de até 30 s. Qualquer integrante pode ser chamado, então todos devem ler esta seção.

**Por que lognormal?**
Tempo até o merge é positivo e tem cauda longa à direita (assimetria perto de 1,9 nos dois grupos, média muito acima da mediana). O log desses tempos é aproximadamente simétrico, e a lognormal é exatamente a distribuição cujo log é normal. Ajustamos μ e σ ao log dos tempos reais dos novatos (μ = 4,38, σ = 2,73).

**Por que bicaudal?**
A pergunta é "diferente", não "maior". Antes de ver os dados não podíamos descartar que o core fosse mais lento (PRs maiores, refatorações). Escolher o lado depois de ver os dados inflaria o erro tipo I. O bicaudal é a escolha mais cautelosa, e está fixado em `lab04/config.py` (`ALTERNATIVE = "two-sided"`).

**Por que 10.000 réplicas?**
Para a taxa de rejeição estimada ser precisa. O erro padrão de uma proporção perto de 5% com 10.000 réplicas é √(0,05 · 0,95 / 10.000) ≈ 0,22 ponto percentual, então o intervalo de confiança de 95% fica em cerca de 5% ± 0,43 p.p. Isso basta para dizer com segurança que o Welch (0,5% a 1,3%) está abaixo de 5%. E o pipeline inteiro roda em cerca de 10 segundos.

**O que muda com n pequeno (n = 10)?**
A média e o desvio ficam ainda mais instáveis, e o Welch quase não rejeita mais (0,7% sem efeito). O Mann-Whitney fica levemente conservador (4,4%, com o IC todo abaixo de 5%), porque com só 10 × 10 = 100 pares a estatística U tem poucos valores possíveis. Os dois perdem poder: no efeito 0,5, 7,3% × 0,9%.

**Por que o Welch foi tão conservador na simulação e mesmo assim rejeitou nos dados reais, com p menor que o do Mann-Whitney?**
Três motivos (estão no texto da seção 6): a diferença real é maior que o maior efeito simulado (mediana do core cerca de 75% menor, contra no máximo 50%); o core real é bem menos disperso que o simulado (σ do log de 1,32, contra 2,73 usado nos dois grupos), o que encolhe o erro padrão do t; e os valores extremos estão do lado do efeito — a cauda longa dos novatos (até 4.447 h) puxa a média deles para 664 h contra 60,9 h do core. Um único PR extremo no core poderia ter escondido a diferença, como aconteceu no exemplo simulado da seção 3.

**Por que o poder simulado foi tão baixo?**
Porque o ruído é enorme. Com σ = 2,73 no log, reduzir a mediana em 50% desloca o log em ln(0,5) ≈ −0,69, cerca de um quarto de desvio padrão. Com n = 30 por grupo, os grupos simulados se sobrepõem muito, e o melhor teste (Mann-Whitney) chega a só cerca de 15%. Para 80% seriam necessários efeitos ou amostras bem maiores.

**O que o Mann-Whitney testa de fato quando as formas diferem?**
Ele não compara medianas nesse caso: testa se P(novato > core) é diferente de 1/2, ou seja, se um grupo tende a ter valores maiores que o outro. Nos dados reais o core é bem menos disperso (σ do log 1,32 × 2,73), então a conclusão deve ser lida assim: o r rank-biserial de 0,30 diz que em 65% dos pares novato × core o PR do novato demorou mais.

**Quais são as limitações da coleta?** (de `data/REGRAS_COLETA.md`)
1. Viés de sobrevivência: só PRs mergeados; os de novatos fechados sem merge, provavelmente os mais lentos, ficam de fora.
2. A associação ao core é a de hoje, não a da época do PR.
3. "Novato" é só neste repositório; a pessoa pode ter experiência em outros projetos.
4. Janelas diferentes: a amostra de novatos cobre cerca de 11 meses, a do core cerca de 3.
5. PRs que começaram como rascunho contam o tempo de draft.
6. O core team é pequeno, então a disponibilidade de poucas pessoas pesa nos tempos.

**Como garantem a reprodutibilidade?**
Um único comando, `python -m lab04.run_all`, roda tudo de ponta a ponta com semente fixa 42 (`SEED` em `lab04/config.py`) e grava `results/`; rodar de novo gera arquivos idênticos byte a byte. Os dados reais estão commitados em `data/real_prs.csv`, gerados só pelo script de coleta (R11), e o dashboard só lê `results/`.

---

## 4. Plano B e plano C

### Plano B — Streamlit Cloud fora do ar: rodar o dashboard localmente

Preparar **antes** da aula, no notebook que vai para a projeção (com o repositório já clonado e o ambiente instalado, para não depender da internet da sala):

```bash
git clone https://github.com/ArlindoSPJr/Lab04-Experimenta-oSoftware.git
cd Lab04-Experimenta-oSoftware
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Na hora:

```bash
python -m lab04.run_all          # só se results/ estiver vazio (leva ~10 s)
streamlit run dashboard/app.py   # abre em http://localhost:8501
```

O dashboard local é o mesmo do publicado (lê os mesmos `results/`). Avise a banca: "o Streamlit Cloud está fora; este é o mesmo dashboard rodando localmente a partir do repositório".

### Plano C — nem o dashboard local abre

1. Abrir o repositório no GitHub e mostrar os CSVs de `results/` (o GitHub renderiza como tabela): `simulacao.csv` (G3 e G4), `tipo1_status.csv`, `poder_vencedor.csv`, `dados_reais.csv`, e o `params.json`.
2. Ler as frases-chave da seção 2 deste roteiro apontando para as tabelas.
3. Ter um PDF do dashboard salvo no dia anterior (navegador → Imprimir → Salvar como PDF) num pendrive e no celular, para mostrar os gráficos.

---

## 5. Checklist pré-apresentação

- [ ] **Na véspera:** rodar `pytest -q` e `python -m lab04.run_all` na `main` atualizada e conferir que os números do dashboard batem com este roteiro.
- [ ] **Na véspera:** salvar o PDF do dashboard (plano C) e preparar o ambiente local (plano B) no notebook da projeção.
- [ ] **10–15 min antes:** abrir https://lab04-experimentacao-software.streamlit.app/ para "acordar" o app — o Streamlit Cloud põe o app para dormir quando fica parado e pode levar alguns minutos para voltar.
- [ ] Conferir que os links do dashboard, do repositório e do GitHub Projects aparecem no topo.
- [ ] Conferir que as seções 6 e 7 já mostram a tabela e a conclusão (não o aviso "em construção").
- [ ] Testar a projeção: resolução, zoom do navegador (Ctrl + / Ctrl −) para os gráficos e tabelas ficarem legíveis do fundo da sala, cores dos dois testes visíveis (Welch azul, Mann-Whitney laranja).
- [ ] Deixar abertas em abas: o dashboard, o repositório e o GitHub Projects.
- [ ] Combinar quem controla a rolagem (sugestão: quem está falando) e as duas trocas (B → A na seção 3, A → C na seção 5).
- [ ] Cronômetro no celular de quem não está falando, com aviso aos 6:00.

---

## 6. Ensaio

O ensaio é feito pelo grupo. Anotar os tempos reais e ajustar a divisão e as falas acima se o total passar de 7:00.

| # | Seção | Quem | Perguntas | Tempo previsto | Tempo real (ensaio 1) | Tempo real (ensaio 2) | Ajuste |
|---|---|---|---|---|---|---|---|
| — | Topo | B | — | 0:05 | | | |
| 1 | Cenário | B | 1, 2 | 0:50 | | | |
| 2 | Os dados (G1) | B | 3, 4 | 0:55 | | | |
| 3 | Como os testes funcionam (G2) | A | 5, 6, 7 | 1:20 | | | |
| 4 | Erro tipo I (G3) | A | 8, 9 | 0:50 | | | |
| 5 | Poder (G4) | C | 10, 11, 12 | 1:15 | | | |
| 6 | Dados reais | C | 14 | 0:25 | | | |
| 7 | Conclusão | C | 13, 15 | 0:55 | | | |
| | **Total** | | | **6:35** | | | |

Data do ensaio: ______ · Presentes: ______ · Observações: ______
