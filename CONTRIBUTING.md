# Regras para subir no GitHub — Lab04

Este documento é a **fonte única** das regras de trabalho com Git, GitHub e GitHub Projects. Ele vale para todos os integrantes (A, B e C).

> **Por que é rígido:** a correção é feita pelo GitHub Projects. **Commits sem o número da Issue não são considerados**, e há desconto de até 10% da nota da sprint por uso ruim do Projects (WIP não respeitado, Issues sem Assignee, cartões desatualizados, falta de evolução semanal).

> ## ⚖️ Regra geral, sem exceção
> 1. **Todo commit referencia uma Issue** (`#<N>` no início da mensagem).
> 2. **Toda mudança entra na `main` por Pull Request** com `Closes #<N>`. Ninguém commita nem dá push direto na `main`, nem para documentação, dados ou correções pequenas.
>
> Se não existe Issue para a mudança, crie a Issue primeiro. Assim cada cartão do board fica com a evidência vinculada (commits e PR).

---

## 1. Desenvolvimento com TDD (obrigatório)

Todo código de `lab04/`, `scripts/` e `dashboard/` nasce de um teste. O ciclo de cada funcionalidade é este:

| Passo | O que fazer | Como conferir |
|---|---|---|
| 🔴 **Red** | Escrever o teste, que está no plano, **antes** do código | `pytest <arquivo> -v` **falha** pelo motivo esperado (função inexistente ou valor errado), e não por erro de sintaxe |
| 🟢 **Green** | Escrever o **mínimo** de código para o teste passar | `pytest <arquivo> -v` passa |
| 🔵 **Refactor** | Melhorar nomes e remover duplicação **sem mudar o comportamento** | `pytest -q` continua todo verde |

Regras:

- **O teste vem antes, inclusive no histórico.** O commit do teste (`test:`) aparece **antes** do commit da implementação (`feat:`) na mesma branch. Isso é a evidência de TDD para quem corrige.
- **Não há código sem teste.** Se uma função não tem teste, ela não entra no PR. A exceção são os textos (`dashboard/textos.py`), testados só quanto a chaves e número de frases, e os arquivos gerados (`data/real_prs.csv` e `results/`).
- **Bug encontrado vira teste primeiro.** Antes de corrigir, escrever o teste que reproduz o bug e vê-lo falhar. Só então corrigir (`fix:`).
- **Não se apaga nem se enfraquece teste para fazer passar.** Se o teste estiver errado, a correção vai num commit próprio (`test:`), explicando o motivo na mensagem.
- **Testes determinísticos.** Todo aleatório usa `np.random.default_rng(<semente fixa>)`. Nada de `np.random.seed` nem de gerador sem semente.

## 2. Issues e board

- **Uma tarefa é uma Issue**, e todo trabalho começa numa Issue que já existe. As Issues e a ordem das ondas estão em `docs/superpowers/plans/2026-11-03-lab04-testes-hipotese.md`.
- **Uma Issue só entra em "In progress" com Assignee.**
- **WIP:** no máximo **1 Issue em "In progress" por integrante**.
- **Fluxo dos cartões:**

  | Coluna | Quando |
  |---|---|
  | **Backlog** | Issues da Sprint 02 |
  | **Ready** | Issues da sprint atual, prontas para começar |
  | **In progress** | Ao criar a branch da Issue |
  | **Done** | Quando o PR é mergeado (a Issue fecha pelo `Closes #N`) |

- **Evolução semanal:** cada integrante faz pelo menos um commit ou move pelo menos um cartão **toda semana**.
- Cada integrante tem pelo menos **uma Issue com código commitado em cada sprint**.

## 3. Branches

- **Nunca commitar direto na `main`** (regra geral, sem exceção). Os três primeiros commits do repositório (`dd626b2`, `1335b7d` e `5e2ea3d`, todos da #1) foram feitos direto na `main` porque o repositório estava vazio. A #1 foi regularizada depois com um PR.
- **Uma branch por Issue**, criada a partir da `main` atualizada:

  ```bash
  git switch main && git pull
  git switch -c issue-<N>-<slug>      # ex.: issue-2-testes-estatisticos
  ```

- **O slug** é curto, sem acento e com hífens. Use o mesmo da seção "Como trabalhar" da Issue.

## 4. Commits

O formato é:

```
#<N> <tipo>: <descrição no imperativo, em português>
```

| Tipo | Uso | Exemplo |
|---|---|---|
| `test` | teste novo ou alterado (o passo 🔴) | `#2 test: welch confere com valores conhecidos` |
| `feat` | código que faz um teste passar (o passo 🟢) | `#2 feat: implementa welch e mann_whitney` |
| `refactor` | melhoria sem mudar o comportamento (o passo 🔵) | `#2 refactor: extrai calculo do tamanho de efeito` |
| `fix` | correção de bug, já com o teste que o reproduz | `#4 fix: ignora PR com merged_by nulo` |
| `data` | dados ou resultados gerados (`data/`, `results/`) | `#6 data: atualiza results da etapa S01` |
| `docs` | README, regras, textos, plano | `#5 docs: registra palpite antes de simular` |
| `chore` | configuração, dependências, estrutura | `#1 chore: cria estrutura do projeto` |

- **Todo commit começa com `#N`**, sem exceção. Commits sem o número não contam na nota.
- **Commits pequenos:** cada um faz uma coisa e deixa o repositório num estado que roda.
- **Arquivos gerados:** `data/real_prs.csv` e `results/` só mudam pelo script (`python scripts/collect_prs.py` ou `python -m lab04.run_all`), nunca à mão, e vão num commit `data:` separado do código.

## 5. Antes de dar push

Rodar, nesta ordem, na raiz do repositório:

```bash
pytest -q                     # tudo verde
python -m lab04.run_all       # só se a Issue mexe na análise; depois commitar results/ (tipo data:)
git status                    # nada esquecido e nenhum arquivo estranho
git push -u origin issue-<N>-<slug>
```

**Não se faz push com teste falhando.** Trabalho incompleto vai para a branch com o teste marcado como `xfail` e uma justificativa, nunca com o teste quebrado.

## 6. Pull Request

- **Título:** `#<N> <título da Issue>`.
- **Descrição:**
  - `Closes #<N>` (fecha a Issue no merge)
  - o que foi feito, em 1 a 3 linhas
  - a saída de `pytest -q`, colada ou resumida
  - os checkpoints da Issue marcados
- **Revisão:** pelo menos **1 aprovação de outro integrante**. O revisor confere:
  1. os testes vieram antes (o commit `test:` aparece antes do `feat:`)
  2. `pytest -q` passa na branch
  3. os nomes e assinaturas batem com o plano (outras Issues dependem deles)
  4. todos os commits começam com `#N`
- **Tipo de merge:** **"Create a merge commit"**, **não** "Squash". O squash apaga os commits individuais, que são a evidência de TDD e de autoria cobrada na correção.
- **Ordem:** o merge segue a ordem das ondas da sprint (Onda 1 → 2 → 3). Uma onda só mergeia depois que a anterior estiver na `main`.
- Depois do merge: apagar a branch e conferir que o cartão foi para **Done**.

## 7. Fechamento de sprint

Quem faz o fechamento é o responsável pela última Issue da sprint (#9 na S01 e #16 na S02):

```bash
git switch main && git pull
python -m lab04.run_all && pytest -q
git tag sprint-0<X> && git push origin sprint-0<X>
```

Depois, conferir que:

- [ ] todos os cartões da sprint estão em **Done**
- [ ] A, B e C têm pelo menos uma Issue com código commitado nesta sprint
- [ ] o dashboard abre e mostra os gráficos da sprint
