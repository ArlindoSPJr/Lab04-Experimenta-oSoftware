# Regras de coleta dos dados reais — Lab04

Este documento é a **fonte única** das regras de coleta. O script `scripts/collect_prs.py` implementa estas regras, e qualquer mudança nelas é feita aqui primeiro, com uma Issue própria.

**Cenário:** tempo até o merge de PRs de **novatos** × **core team** (par P1, t de Welch × Mann-Whitney).

---

## R1. Fonte

| Item | Valor |
|---|---|
| Repositório | [`pallets/click`](https://github.com/pallets/click) (público) |
| API | GitHub **GraphQL** (`https://api.github.com/graphql`) |
| Autenticação | token em `GITHUB_TOKEN`, ou `gh auth login` |
| Por que GraphQL | a listagem REST de PRs não traz `mergedBy`, que é necessário para a R4.4 |

Query (paginada com `after: $endCursor` até `hasNextPage = false`):

```graphql
query($endCursor: String) {
  repository(owner: "pallets", name: "click") {
    pullRequests(first: 100, after: $endCursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number authorAssociation createdAt mergedAt
        author { login __typename }
        mergedBy { login }
      }
    }
  }
}
```

## R2. Data de corte

Só entram PRs com `createdAt` **e** `mergedAt` anteriores a **`2026-11-04T00:00:00Z`**. Com isso, quem rodar a coleta depois obtém a mesma amostra.

## R3. Histórico completo

Baixar **todos** os PRs do repositório, em qualquer estado (aberto, fechado ou mergeado), desde o primeiro. Sem o histórico completo não dá para saber qual é o primeiro PR de cada autor (R6).

## R4. Exclusões

Aplicadas nesta ordem. Um PR excluído não entra em nenhum grupo:

1. **Bots:** `author.__typename == "Bot"` ou login terminado em `[bot]`.
2. **Autor apagado:** `author == null` (o GitHub mostra como "ghost").
3. **Não mergeado:** `mergedAt == null`.
4. **Automerge:** `mergedBy.login == author.login`. O próprio autor mergeou, sem revisão de outra pessoa. Também se exclui `mergedBy == null` (merge sem registro de quem fez).
5. **Fora da data de corte** (R2).

> Mesmo excluídos, os PRs das regras 3 a 5 **contam para o histórico** do autor na R6. Exemplo: se o primeiro PR de uma pessoa não foi mergeado, o segundo PR dela **não** é de novato.

## R5. Grupo `core`

`authorAssociation ∈ {MEMBER, OWNER, COLLABORATOR}`.

## R6. Grupo `novato`

O PR é o **primeiro PR do autor no histórico completo** (R3, em qualquer estado) **e** o autor não é `core`.

- **Não usar** `authorAssociation == FIRST_TIME_CONTRIBUTOR`. O campo mostra a relação **atual** do autor com o repositório, não a relação na época do PR. Na triagem de 2026-11-03 ele apareceu **0 vezes** em 8 repositórios.
- A R5 tem precedência: um autor core nunca é novato.

## R7. Fora dos dois grupos

PRs de autores que não são core e **não** estão fazendo o primeiro PR (contribuidores recorrentes) ficam de fora.

## R8. Amostra

Entre os PRs elegíveis de cada grupo, pegar os **30 com `createdAt` mais recente**. Em caso de empate, vale o maior `number`. Isso dá n = 30 por grupo, 60 no total.

## R9. Métrica

```
hours_to_merge = (mergedAt − createdAt) em segundos / 3600
```

- Tudo em UTC, gravado com 6 casas decimais.
- O valor precisa ser **> 0**. `lab04/real_data.py::load_real_data` recusa qualquer linha com valor ≤ 0.

## R10. Saída

O arquivo `data/real_prs.csv` (UTF-8, separador vírgula, uma linha por PR) tem estas colunas:

| Coluna | Tipo | Exemplo |
|---|---|---|
| `pr_number` | int | `2871` |
| `author` | str | `fulano` |
| `author_association` | str | `CONTRIBUTOR` |
| `merged_by` | str | `mantenedor` |
| `group` | `novato` \| `core` | `novato` |
| `created_at` | ISO 8601 UTC | `2026-03-02T14:05:11Z` |
| `merged_at` | ISO 8601 UTC | `2026-03-06T09:40:00Z` |
| `hours_to_merge` | float | `91.582222` |

## R11. Integridade

- O CSV é gerado **somente** pelo script: `python scripts/collect_prs.py`. É proibido editar à mão.
- O CSV é commitado no repositório, porque a análise roda sobre o arquivo commitado e não sobre uma nova coleta.
- Se for preciso coletar de novo, isso é feito numa Issue própria, e o registro abaixo é atualizado.

## R12. Registro da coleta

*Preencher ao rodar a coleta (Task 2.1, Step 4).*

| Item | Valor |
|---|---|
| Data e hora da coleta (UTC) | |
| Comando | `python scripts/collect_prs.py` |
| Commit do script | |
| PRs no histórico (total baixado) | |
| Elegíveis `novato` / `core` (antes da R8) | |
| Período coberto pela amostra `novato` | |
| Período coberto pela amostra `core` | |
| Responsável | Integrante B |

---

## Justificativa da escolha do repositório

Triagem feita em 2026-11-03 com o histórico completo de 8 repositórios, aplicando a R4.1, a R4.3, a R5 e a R6 (sem a R4.4). Os valores são dos 30 PRs mais recentes de cada grupo:

| Repositório | Período novato | Período core | Mediana novato | Mediana core |
|---|---|---|---|---|
| **pallets/click** ✔ | 2025-09 a 2026-08 | 2026-08 a 2026-10 | 96,7 h | 14,3 h |
| python-poetry/poetry | 2026-06 a 2026-10 | 2026-06 a 2026-10 | 189,2 h | 0,3 h |
| pmndrs/zustand | 2025-08 a 2026-05 | 2025-11 a 2026-10 | 7,1 h | 0,4 h |
| encode/httpx | 2024-01 a 2026-02 | 2024-10 a 2025-12 | 73,4 h | 0,5 h |
| marshmallow-code/marshmallow | 2021-11 a 2026-09 | 2025-12 a 2026-11 | 171,3 h | 0,2 h |
| Textualize/rich | 2024-02 a 2025-12 | 2025-06 a 2026-06 | 525,5 h | 0,2 h |
| pallets/flask | 2023-10 a 2026-07 | 2024-11 a 2026-10 | 347,4 h | 0,0 h |
| tqdm/tqdm | 2021-07 a 2026-09 | 2021-02 a 2026-09 | 396,1 h | 44,3 h |

**Por que o click:** os dois grupos são recentes, a diferença entre eles é clara sem ser extrema, e os dados são muito assimétricos (média de 664 h × mediana de 97 h nos novatos). O histórico tem cerca de 1.900 PRs, ou umas 20 páginas da API. Com a R4.4 aplicada, a triagem mostrou 356 novatos e 122 core elegíveis. Nos 30 mais recentes, a mediana ficou em 96,7 h × 23,9 h, e o menor tempo do core foi 3,6 h.

## Limitações conhecidas

*Estas limitações devem ser citadas na seção 7 (Conclusão) do dashboard.*

1. **Viés de sobrevivência:** só entram PRs mergeados. PRs de novatos fechados sem merge, que provavelmente são os casos mais lentos ou problemáticos, ficam de fora.
2. **Associação atual:** a R5 usa a associação do autor **hoje**. Alguém que entrou no core recentemente tem os PRs antigos contados como core.
3. **"Novato" só neste repositório:** a pessoa pode ter experiência em outros projetos.
4. **Janelas de tempo diferentes:** a amostra de novatos cobre cerca de 11 meses, e a do core cerca de 3. Mudanças no projeto nesse período (releases, férias dos mantenedores) se misturam ao efeito.
5. **PRs em rascunho:** `createdAt` conta a partir da abertura do PR, mesmo que ele tenha começado como draft. Isso infla o tempo dos PRs que passaram por rascunho.
6. **Core team pequeno:** poucas pessoas revisam os PRs, então a disponibilidade individual delas pesa nos tempos.
