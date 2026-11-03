# Lab04 — Testes de Hipótese por Dentro (P1: Welch × Mann-Whitney) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Comparar, por simulação de Monte Carlo calibrada com dados reais de PRs do GitHub, o t de Welch e o Mann-Whitney na pergunta "o tempo até o merge de PRs de contribuidores novatos é diferente do de membros do core team?", entregando tudo num dashboard Streamlit (Sprints 01 e 02).

**Architecture:** Pacote Python `lab04/` com módulos pequenos (config → dados reais → gerador → testes → simulação). Um único comando `python -m lab04.run_all` roda tudo com semente fixa e grava `results/*.csv|json`. O dashboard `dashboard/app.py` **só lê** `results/` e desenha os gráficos de `lab04/charts/`. Os textos ficam em `dashboard/textos.py`.

**Tech Stack:** Python ≥ 3.11, NumPy, SciPy ≥ 1.11 (`ttest_ind(...).df`), pandas, Plotly, Streamlit ≥ 1.28 (`AppTest`), pytest.

**Spec:** `Enunciado.pdf` (raiz do repositório)

## Global Constraints

- Par escolhido: **P1 — t de Welch × Mann-Whitney**, cenário "tempo até o merge de PRs de **novatos** × **core team**" (escolhido pelo grupo em 2026-11-03).
- Coleta dos dados reais: seguir **exatamente** `data/REGRAS_COLETA.md` (regras R1–R12). Este plano não repete as regras.
- Semente fixa: `SEED = 42`, com o gerador criado **só** por `np.random.default_rng(SEED)` em `run_all`. Os módulos recebem `rng` como parâmetro e nunca criam o próprio.
- `ALPHA = 0.05`, `N_REPS = 10_000` repetições por condição, `N_PER_GROUP = 30`.
- Tamanhos de efeito: `EFFECTS = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)`, ou seja, redução relativa da mediana no grupo `core`. São ≥ 5 valores começando em zero.
- Teste bicaudal: `ALTERNATIVE = "two-sided"` (decidido pelo grupo).
- Convenção de grupos: `a = novato`, `b = core`. Efeito positivo significa que os PRs do core team são mergeados mais rápido que os dos novatos.
- Q3: pelo menos uma situação que viole pressupostos. O plano usa três: `n_pequeno`, `outliers`, `assimetria_forte`.
- Gráficos: título, eixos com nome **e unidade**, legenda, e **a mesma cor para cada teste** em todos os gráficos: `COLORS = {"welch": "#1f77b4", "mann_whitney": "#ff7f0e"}`.
- Dashboard: as 7 seções na ordem do enunciado (1. Cenário, 2. Os dados, 3. Como os testes funcionam, 4. Erro tipo I, 5. Poder, 6. Dados reais, 7. Conclusão), cada gráfico com um texto de 2 a 4 frases, e **links do dashboard e do repositório/GitHub Projects no topo**.
- Bibliotecas permitidas: NumPy, SciPy, statsmodels, pandas, Matplotlib, Seaborn, Plotly (mais Streamlit e pytest como ferramentas).
- Comandos documentados no README: `python -m lab04.run_all` roda tudo e `streamlit run dashboard/app.py` abre o dashboard. Os arquivos de `results/` **são commitados**, para o dashboard abrir sem rodar a simulação e funcionar no Streamlit Cloud.
- Git, GitHub, Projects e **TDD**: seguir `CONTRIBUTING.md` (fonte única). Cada tarefa abaixo é 1 Issue. Os commits seguem o formato `#<n> <tipo>: ...`, e o `test:` vem antes do `feat:`.

## Review Focus

1. **PR com tempo de merge 0 ou negativo no CSV** (mesmo timestamp, ou dado digitado errado): `log(0)` quebra o ajuste da lognormal. `load_real_data` deve recusar com `ValueError` que cite a linha. O teste fica na Task 2.1.
2. **Dashboard aberto sem `results/`** (clone novo, deploy antes do `run_all`): a página deve mostrar um `st.warning` com o comando, e não um traceback. O teste fica na Task 3.3.
3. **Reprodutibilidade**: rodar `run_all` duas vezes precisa gerar arquivos idênticos byte a byte. O teste fica na Task 2.3 (S01) e na Task 2.2 (S02).
4. **Cenário `outliers` gerando valor ≤ 0 ou NaN**: todos os valores simulados precisam ser finitos e > 0 em qualquer cenário. O teste fica na Task 1.3 (S01) e na Task 2.1 (S02).
5. **Cor trocada entre gráficos**: o Welch precisa ser sempre `#1f77b4` e o Mann-Whitney sempre `#ff7f0e` no G2, no G3 e no G4. O teste fica nas Tasks 3.2 (S01) e 3.1 (S02).

---

## Organização em ondas (wave orchestration)

Em cada sprint há **3 ondas**, e **cada onda pertence a um único integrante**. A ordem segue as dependências:

| Sprint | Onda 1 — **A** | Onda 2 — **B** | Onda 3 — **C** |
|---|---|---|---|
| S01 | Fundação + motor estatístico (estrutura, config, estilo dos gráficos, testes, gerador) | Dados reais + cenário + pipeline S01 | Gráficos G1, G2 + dashboard seções 1–3 |
| S02 | Motor de simulação (Q1, Q2) + classificação de erro tipo I e poder | Cenários Q3 + pipeline S02 + textos 4–5 | Gráficos G3, G4 + dashboard seções 4–5 + deploy |

**Regras das ondas** (merge, revisão, WIP e fechamento de sprint estão em `CONTRIBUTING.md`, seções 2, 6 e 7):
- O **trabalho** pode começar antes do merge da onda anterior. As interfaces de cada tarefa estão fixadas abaixo, então B e C podem começar no primeiro dia usando dados falsos nos testes. Em especial, a **coleta de dados reais (Task 2.1 do S01) deve começar no primeiro dia**, porque não depende de código.
- Fim de onda = todos os PRs da onda mergeados (seguindo a seção 6 do `CONTRIBUTING.md`).

---

## Estrutura de arquivos

```
requirements.txt
README.md
lab04/
  __init__.py
  config.py            # constantes globais (Task 1.1)
  stat_tests.py        # Welch, Mann-Whitney, versões vetorizadas (Task 1.2)
  scenarios.py         # Scenario (S01 Task 1.3) + cenários Q3 (S02 Task 2.1)
  generate.py          # gerador lognormal (Task 1.3)
  real_data.py         # carregar CSV, ajustar lognormal, descrever (Task 2.1)
  simulate.py          # taxas de rejeição, grade Q1/Q2/Q3 (S02 Task 1.1)
  summary.py           # classificar erro tipo I (S02 Task 1.2)
  run_all.py           # comando único (S01 Task 2.3, S02 Task 2.2)
  charts/
    __init__.py
    style.py           # cores, layout padrão (S01 Task 1.1)
    g1.py g2.py g3.py g4.py
scripts/collect_prs.py # coleta via API do GitHub (Task 2.1)
data/real_prs.csv
data/REGRAS_COLETA.md  # regras de coleta R1–R12 + registro + limitações (já existe)
results/               # gerado por run_all, commitado
dashboard/
  app.py               # Streamlit (C)
  textos.py            # textos das seções (B)
tests/                 # um test_<módulo>.py por módulo
```

---

# SPRINT 01 — Lab04S01 (7 pontos)

Entregáveis: dados reais, cenário, código do gerador, os dois testes aplicados a **um** dataset simulado com interpretação, e G1 + G2 no dashboard.

## Onda 1 — Integrante A (fundação e motor estatístico)

### Task 1.1: Estrutura do projeto, config e GitHub Projects

**Files:**
- Create: `requirements.txt`, `README.md`, `lab04/__init__.py`, `lab04/config.py`, `lab04/charts/__init__.py`, `lab04/charts/style.py`, `tests/test_config.py`, `.gitignore`

**Interfaces:**
- Produces (`lab04/config.py`): `SEED: int = 42`, `ALPHA: float = 0.05`, `N_REPS: int = 10_000`, `N_PER_GROUP: int = 30`, `EFFECTS: tuple[float, ...]`, `ALTERNATIVE: str = "two-sided"`, `TEST_NAMES = ("welch", "mann_whitney")`, `COLORS: dict[str, str]`, `LABELS = {"welch": "t de Welch", "mann_whitney": "Mann-Whitney"}`, `GROUPS = ("novato", "core")`, `ROOT, DATA_DIR, RESULTS_DIR: pathlib.Path`, `REPO_URL: str`, `PROJECT_URL: str`, `DASHBOARD_URL: str`
- Produces (`lab04/charts/style.py`): `test_color(name: str) -> str` e `apply_layout(fig: go.Figure, title: str, x_title: str, y_title: str) -> go.Figure` (título, eixos e legenda visível). Todos os gráficos (G1–G4) usam essas funções.

- [ ] **Step 1: Preencher o board** https://github.com/users/ArlindoSPJr/projects/6 com uma Issue por Task deste plano, cada uma com o Assignee indicado. Convenção das colunas: **Backlog** = Issues da Sprint 02, **Ready** = Issues da Sprint 01 prontas para começar, e depois In progress → In review → Done. Anotar o número de cada Issue na tabela do fim deste documento. Em `config.py`, `PROJECT_URL = "https://github.com/users/ArlindoSPJr/projects/6"`.
- [ ] **Step 2: Escrever o teste com falha** `tests/test_config.py`

```python
from lab04 import config

def test_constantes_do_enunciado():
    assert config.SEED == 42
    assert config.ALPHA == 0.05
    assert config.N_REPS == 10_000
    assert len(config.EFFECTS) >= 5 and config.EFFECTS[0] == 0.0
    assert list(config.EFFECTS) == sorted(config.EFFECTS)

def test_uma_cor_por_teste():
    assert set(config.COLORS) == set(config.TEST_NAMES)
    assert len(set(config.COLORS.values())) == len(config.TEST_NAMES)

def test_style_cor_e_layout():
    import plotly.graph_objects as go
    from lab04.charts import style  # módulo, não a função: o pytest coletaria `test_color` como teste
    assert style.test_color("welch") == config.COLORS["welch"]
    f = style.apply_layout(go.Figure(), "T", "x (h)", "y (%)")
    assert f.layout.title.text == "T" and f.layout.xaxis.title.text == "x (h)" and f.layout.showlegend
```

- [ ] **Step 3: Rodar** `pytest tests/test_config.py -v`. Esperado: FAIL (`ModuleNotFoundError: lab04`). Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 4: Implementar** `lab04/config.py` com os valores das Global Constraints e `lab04/charts/style.py`. `requirements.txt`: `numpy`, `scipy>=1.11`, `pandas`, `plotly`, `streamlit>=1.28`, `pytest`. README: seções "Instalação" (`pip install -r requirements.txt`), "Rodar tudo" (`python -m lab04.run_all`), "Abrir dashboard" (`streamlit run dashboard/app.py`) e "Testes" (`pytest -q`).
- [ ] **Step 5: Rodar** `pytest tests/test_config.py -v`. Esperado: PASS.
- [ ] **Step 6: Commit** `#1 chore: estrutura do projeto, config e estilo`, push da branch e PR com `Closes #1` (regra geral do CONTRIBUTING: todo commit referencia Issue e entra na `main` por PR). *Histórico: os primeiros commits foram feitos direto na `main` com o repositório vazio, e a #1 foi regularizada com o PR `issue-1-regra-pr`.* Depois do merge, B e C podem criar suas branches.

### Task 1.2: Os dois testes de hipótese

**Files:**
- Create: `lab04/stat_tests.py`, `tests/test_stat_tests.py`

**Interfaces:**
- Consumes: `config.ALPHA`, `config.ALTERNATIVE`
- Produces:
  - `@dataclass(frozen=True) class TestResult: name: str; statistic: float; p_value: float; reject: bool; effect_size: float; effect_label: str; df: float | None; n_a: int; n_b: int`, com `to_dict() -> dict` e `@classmethod from_dict(d: dict) -> TestResult`
  - `welch(a: np.ndarray, b: np.ndarray, alpha: float = ALPHA) -> TestResult`. O efeito é o d de Cohen com desvio médio: `(mean_a - mean_b) / sqrt((var_a + var_b) / 2)` (ddof=1), com `effect_label="d de Cohen"`.
  - `mann_whitney(a, b, alpha=ALPHA) -> TestResult`. A estatística é o U de `a`, e o efeito é a correlação rank-biserial `2*U/(n_a*n_b) - 1`, com `effect_label="r rank-biserial"`, `df=None`.
  - `welch_pvalues(A: np.ndarray, B: np.ndarray) -> np.ndarray` e `mann_whitney_pvalues(A, B) -> np.ndarray`. As entradas têm shape `(n_reps, n)`, a saída tem shape `(n_reps,)`, e o cálculo é vetorizado com `axis=1`.

- [ ] **Step 1: Escrever os testes com falha**

```python
import numpy as np, pytest
from lab04.stat_tests import welch, mann_whitney, welch_pvalues, mann_whitney_pvalues, TestResult

def test_welch_valores_conhecidos():
    r = welch(np.array([1., 2, 3, 4, 5]), np.array([2., 3, 4, 5, 6]))
    assert r.statistic == pytest.approx(-1.0)
    assert r.p_value == pytest.approx(0.3466, abs=1e-4)
    assert r.df == pytest.approx(8.0)
    assert r.effect_size == pytest.approx(-0.6325, abs=1e-4)
    assert r.reject is False

def test_mann_whitney_valores_conhecidos():
    r = mann_whitney(np.array([1., 2, 3]), np.array([4., 5, 6]))
    assert r.statistic == 0.0
    assert r.p_value == pytest.approx(0.1)
    assert r.effect_size == pytest.approx(-1.0)

def test_vetorizado_igual_ao_escalar():
    rng = np.random.default_rng(0)
    A, B = rng.lognormal(size=(50, 30)), rng.lognormal(size=(50, 30))
    pw, pm = welch_pvalues(A, B), mann_whitney_pvalues(A, B)
    assert pw.shape == pm.shape == (50,)
    assert pw[7] == pytest.approx(welch(A[7], B[7]).p_value)
    assert pm[7] == pytest.approx(mann_whitney(A[7], B[7]).p_value)

def test_roundtrip_dict():
    r = welch(np.array([1., 2, 3, 4]), np.array([2., 3, 5, 9]))
    assert TestResult.from_dict(r.to_dict()) == r
```

- [ ] **Step 2: Rodar** `pytest tests/test_stat_tests.py -v`. Esperado: FAIL (ImportError). Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** usando `scipy.stats.ttest_ind(equal_var=False, alternative=ALTERNATIVE)` e `scipy.stats.mannwhitneyu(alternative=ALTERNATIVE, method="auto")`. Nas versões vetorizadas, passar `axis=1`. Converter os escalares para `float` e `bool` Python, para o `to_dict` serializar em JSON.
- [ ] **Step 4: Rodar** `pytest tests/test_stat_tests.py -v`. Esperado: PASS.
- [ ] **Step 5: Commit** `#<issue> feat: testes de Welch e Mann-Whitney`

### Task 1.3: Cenário e gerador de dados simulados

**Files:**
- Create: `lab04/scenarios.py`, `lab04/generate.py`, `tests/test_generate.py`

**Interfaces:**
- Produces:
  - `@dataclass(frozen=True) class Scenario: name: str; label: str; n: int; mu: float; sigma: float; outlier_frac: float = 0.0; outlier_mult: float = 10.0`. `mu` e `sigma` são os parâmetros **do log** do grupo `novato`.
  - `base_scenario(mu: float, sigma: float, n: int = N_PER_GROUP) -> Scenario`, com `name="base"` e `label="Base (lognormal ajustada, n=30)"`
  - `generate_groups(rng: np.random.Generator, scenario: Scenario, effect: float, n_reps: int = 1) -> tuple[np.ndarray, np.ndarray]`, que retorna `(A, B)` com shape `(n_reps, scenario.n)`. `A ~ LogNormal(mu, sigma)` e `B ~ LogNormal(mu + ln(1 - effect), sigma)`. Se `outlier_frac > 0`, cada valor dos dois grupos é multiplicado por `outlier_mult` com probabilidade `outlier_frac`.

- [ ] **Step 1: Escrever os testes com falha**

```python
import numpy as np, pytest
from lab04.scenarios import Scenario, base_scenario
from lab04.generate import generate_groups

S = base_scenario(mu=np.log(10), sigma=1.0)

def test_formato():
    A, B = generate_groups(np.random.default_rng(1), S, 0.0, n_reps=7)
    assert A.shape == B.shape == (7, 30)

def test_efeito_reduz_mediana():
    A, B = generate_groups(np.random.default_rng(1), S, 0.5, n_reps=4000)
    assert np.median(A) == pytest.approx(10, rel=0.05)
    assert np.median(B) == pytest.approx(5, rel=0.05)

def test_mesma_semente_mesmos_dados():
    x = generate_groups(np.random.default_rng(42), S, 0.2, 3)
    y = generate_groups(np.random.default_rng(42), S, 0.2, 3)
    assert np.array_equal(x[0], y[0]) and np.array_equal(x[1], y[1])

def test_outliers_positivos_e_finitos():
    s = Scenario("outliers", "Outliers", 30, np.log(10), 1.0, outlier_frac=0.05)
    A, B = generate_groups(np.random.default_rng(3), s, 0.3, 2000)
    for X in (A, B):
        assert np.all(np.isfinite(X)) and np.all(X > 0)
    assert (A > np.quantile(A, 0.5) * 10).mean() > 0.02

def test_efeito_invalido():
    with pytest.raises(ValueError):
        generate_groups(np.random.default_rng(0), S, 1.0)
```

- [ ] **Step 2: Rodar** `pytest tests/test_generate.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** com `rng.lognormal(mean, sigma, size=(n_reps, n))` e uma máscara `rng.random(size) < outlier_frac`. Rejeitar `effect` fora de `[0, 1)` com `ValueError`.
- [ ] **Step 4: Rodar** `pytest -q`. Esperado: tudo PASS.
- [ ] **Step 5: Commit** `#<issue> feat: gerador de dados simulados (lognormal)`

## Onda 2 — Integrante B (dados reais, cenário e pipeline S01)

> A Task 2.1 (coleta) **começa no primeiro dia do sprint**, em paralelo com a Onda 1.

### Task 2.1: Coleta e carga dos dados reais

**Files:**
- Create: `scripts/collect_prs.py`, `data/real_prs.csv`, `lab04/real_data.py`, `tests/test_real_data.py`, `tests/test_collect_prs.py`
- Modify: `data/REGRAS_COLETA.md` (só a seção R12, Registro da coleta)

**Interfaces:**
- Produces:
  - CSV `data/real_prs.csv` com as colunas da **R10** de `data/REGRAS_COLETA.md`.
  - `scripts/collect_prs.py`, que implementa as regras R1–R11 de `data/REGRAS_COLETA.md`:
    - Formato interno de cada PR (normalizado a partir do GraphQL): `{"number", "user": {"login", "type"} | None, "author_association", "created_at", "merged_at", "merged_by"}`, onde `merged_by` é um login ou `None`.
    - `pr_to_row(pr: dict, group: str) -> dict | None`: monta a linha da R10. Retorna `None` se `merged_at` for nulo. O valor `hours_to_merge` segue a R9.
    - `classify_prs(prs: list[dict], cutoff: str = "2026-11-04T00:00:00Z") -> list[tuple[dict, str]]`: aplica as regras R2 a R7 e devolve pares `(pr, grupo)`.
    - `select_sample(classified: list[tuple[dict, str]], n: int = 30) -> list[tuple[dict, str]]`: aplica a R8.
    - `main()`: faz a coleta da R1 (histórico completo, R3), depois `classify_prs`, `select_sample`, `pr_to_row`, e grava o CSV.
  - `lab04/real_data.py`:
    - `load_real_data(path: Path = DATA_DIR / "real_prs.csv") -> pd.DataFrame`, com as colunas `group` e `hours_to_merge`. Faz `ValueError` se faltar coluna, se aparecer um grupo desconhecido ou se `hours_to_merge <= 0`, citando o `pr_number`.
    - `fit_lognormal(x: np.ndarray) -> tuple[float, float]`, que retorna `(mean(log x), std(log x, ddof=1))`.
    - `describe_real(df) -> pd.DataFrame`, com índice `group` e colunas `n, media, mediana, desvio, assimetria, n_outliers` (outlier = fora de `Q3 + 1.5·IQR`).

- [ ] **Step 1: Escrever os testes com falha**

```python
import numpy as np, pandas as pd, pytest
from lab04.real_data import load_real_data, fit_lognormal, describe_real
from scripts.collect_prs import pr_to_row, classify_prs, select_sample

def _csv(tmp_path, hours):
    p = tmp_path / "r.csv"
    pd.DataFrame({"pr_number": range(len(hours)), "group": ["novato", "core"] * (len(hours) // 2),
                  "created_at": "", "merged_at": "", "hours_to_merge": hours}).to_csv(p, index=False)
    return p

def test_rejeita_tempo_zero(tmp_path):
    with pytest.raises(ValueError, match="pr_number"):
        load_real_data(_csv(tmp_path, [1.0, 0.0]))

def test_fit_lognormal_recupera_parametros():
    x = np.random.default_rng(0).lognormal(2.0, 0.8, 20_000)
    mu, s = fit_lognormal(x)
    assert mu == pytest.approx(2.0, abs=0.02) and s == pytest.approx(0.8, abs=0.02)

def test_describe_conta_outlier(tmp_path):
    df = load_real_data(_csv(tmp_path, [1, 1, 2, 2, 3, 3, 100, 2]))
    d = describe_real(df)
    assert d.loc["novato", "n_outliers"] == 1 and d.loc["novato", "n"] == 4

def test_pr_nao_mergeado_e_ignorado():
    assert pr_to_row({"number": 1, "created_at": "2026-01-01T00:00:00Z", "merged_at": None}, "novato") is None
    row = pr_to_row({"number": 2, "created_at": "2026-01-01T00:00:00Z", "merged_at": "2026-01-01T12:30:00Z"}, "core")
    assert row["hours_to_merge"] == pytest.approx(12.5)

def _pr(n, login, assoc, day, kind="User", merged_by="maint"):
    return {"number": n, "user": {"login": login, "type": kind}, "author_association": assoc,
            "created_at": f"2026-01-{day:02d}T00:00:00Z", "merged_at": f"2026-01-{day:02d}T05:00:00Z",
            "merged_by": merged_by}

def test_classifica_segundo_regras_R4_a_R7():
    nao_mergeado = {**_pr(7, "leo", "CONTRIBUTOR", 8), "merged_at": None}
    prs = [_pr(3, "ana", "CONTRIBUTOR", 5),                  # R7: 2º PR da ana -> fora
           _pr(1, "ana", "CONTRIBUTOR", 1),                  # R6: 1º PR da ana -> novato
           _pr(2, "rui", "MEMBER", 2),                       # R5: core revisado por outro
           _pr(5, "rui", "MEMBER", 6, merged_by="rui"),      # R4.4: automerge -> fora
           _pr(6, "eva", "MEMBER", 7, merged_by=None),       # R4.4: merged_by nulo -> fora
           _pr(4, "dependabot[bot]", "NONE", 3, kind="Bot"), # R4.1: bot -> fora
           nao_mergeado,                                     # R4.3: fora, mas conta no histórico
           _pr(8, "leo", "CONTRIBUTOR", 9)]                  # 2º PR do leo -> fora (R6)
    got = {pr["number"]: g for pr, g in classify_prs(prs)}
    assert got == {1: "novato", 2: "core"}

def test_data_de_corte():
    assert classify_prs([_pr(1, "ana", "CONTRIBUTOR", 10)], cutoff="2026-01-05T00:00:00Z") == []

def test_amostra_pega_os_mais_recentes_por_grupo():
    cl = [(_pr(i, f"u{i}", "CONTRIBUTOR", i), "novato") for i in range(1, 6)]
    assert [p["number"] for p, _ in select_sample(cl, n=2)] == [5, 4]
```

- [ ] **Step 2: Rodar** `pytest tests/test_real_data.py tests/test_collect_prs.py -v`. Esperado: FAIL. (Criar `scripts/__init__.py` para o import funcionar.) Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** os três módulos. Para a assimetria, usar `scipy.stats.skew`.
- [ ] **Step 4: Rodar a coleta real** com `python scripts/collect_prs.py` e gerar `data/real_prs.csv`. Preencher a tabela da **R12 (Registro da coleta)** em `data/REGRAS_COLETA.md`.
- [ ] **Step 5: Rodar** `pytest -q`. Esperado: PASS.
- [ ] **Step 6: Commit** `#<issue> feat: coleta e carga dos dados reais de PRs`

### Task 2.2: Cenário escrito e textos do dashboard (seções 1–3)

**Files:**
- Create: `dashboard/textos.py`, `tests/test_textos.py`

**Interfaces:**
- Produces: `TEXTOS: dict[str, str]` com as chaves `"pergunta"`, `"h0"`, `"h1"`, `"fonte"`, `"palpite"`, `"dados"`, `"como_funcionam"`, `"exemplo"`. O texto de `"palpite"` registra **antes de simular** qual teste o grupo espera que vença e por quê. A chave `"exemplo"` interpreta o resultado de `results/exemplo.json`.

- [ ] **Step 1: Escrever o teste com falha**

```python
from dashboard.textos import TEXTOS

CHAVES_S01 = {"pergunta", "h0", "h1", "fonte", "palpite", "dados", "como_funcionam", "exemplo"}

def test_chaves_presentes():
    assert CHAVES_S01 <= set(TEXTOS)

def test_textos_de_grafico_tem_2_a_4_frases():
    for k in ("dados", "como_funcionam"):
        n = TEXTOS[k].count(". ") + 1
        assert 2 <= n <= 4, k
```

- [ ] **Step 2: Rodar** `pytest tests/test_textos.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Escrever os textos** em `dashboard/textos.py` (criar `dashboard/__init__.py`). A pergunta deve ter uma frase só. H₀: "o tempo até o merge tem a mesma distribuição para PRs de novatos e do core team". H₁: "as distribuições são diferentes (bicaudal)". O texto `"dados"` cita a assimetria e os outliers de `describe_real` e o motivo da lognormal. Os números de `"exemplo"` são preenchidos depois de rodar a Task 2.3.
- [ ] **Step 4: Rodar** `pytest tests/test_textos.py -v`. Esperado: PASS.
- [ ] **Step 5: Commit** `#<issue> docs: cenário, hipóteses e palpite`

### Task 2.3: Comando único — etapa S01

**Files:**
- Create: `lab04/run_all.py`, `lab04/__main__.py` (opcional), `tests/test_run_all.py`
- Output: `results/params.json`, `results/simulado_exemplo.csv`, `results/exemplo.json`

**Interfaces:**
- Consumes: `load_real_data`, `fit_lognormal`, `base_scenario`, `generate_groups`, `welch`, `mann_whitney`, `TestResult.to_dict`
- Produces:
  - `main(n_reps: int = N_REPS, out_dir: Path = RESULTS_DIR, data_path: Path = DATA_DIR / "real_prs.csv") -> None`, que cria `rng = np.random.default_rng(SEED)` uma única vez.
  - `params.json`: `{"mu": float, "sigma": float, "n": int, "fonte": "data/real_prs.csv"}`
  - `simulado_exemplo.csv`: colunas `group,hours_to_merge`, um dataset com `effect=0.2`
  - `exemplo.json`: `{"effect": 0.2, "welch": TestResult.to_dict(), "mann_whitney": TestResult.to_dict()}`

- [ ] **Step 1: Escrever os testes com falha**

```python
import json
from lab04.run_all import main

def test_gera_arquivos_s01(tmp_path):
    main(n_reps=200, out_dir=tmp_path)
    for f in ("params.json", "simulado_exemplo.csv", "exemplo.json"):
        assert (tmp_path / f).exists()
    ex = json.loads((tmp_path / "exemplo.json").read_text())
    assert set(ex) >= {"effect", "welch", "mann_whitney"}

def test_reprodutivel(tmp_path):
    main(n_reps=200, out_dir=tmp_path / "a"); main(n_reps=200, out_dir=tmp_path / "b")
    for f in ("params.json", "simulado_exemplo.csv", "exemplo.json"):
        assert (tmp_path / "a" / f).read_bytes() == (tmp_path / "b" / f).read_bytes()
```

- [ ] **Step 2: Rodar** `pytest tests/test_run_all.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** `main`, com `if __name__ == "__main__": main()`. Gravar o JSON com `indent=2, sort_keys=True` e o CSV com `float_format="%.6f"`, para o resultado ser estável byte a byte.
- [ ] **Step 4: Rodar** `python -m lab04.run_all` e depois `pytest -q`. Esperado: PASS e `results/` gerado. Preencher `TEXTOS["exemplo"]` com os números reais.
- [ ] **Step 5: Commit** `#<issue> feat: run_all etapa S01 e resultados` (incluir `results/`)

## Onda 3 — Integrante C (gráficos G1, G2 e dashboard)

### Task 3.1: Gráfico G1

**Files:**
- Create: `lab04/charts/g1.py`, `tests/test_charts_s01.py`

**Interfaces:**
- Consumes: `config.GROUPS`, `style.apply_layout` (Task 1.1)
- Produces:
  - `g1.fig_g1(real: pd.DataFrame, simulated: pd.DataFrame) -> go.Figure`: um subplot por grupo, com histogramas real × simulado sobrepostos (`histnorm="probability density"`). O eixo x é "Tempo até o merge (horas)" e o eixo y é "Densidade (1/hora)".

- [ ] **Step 1: Escrever o teste com falha**

```python
import pandas as pd
from lab04.charts.g1 import fig_g1

def _df(v): return pd.DataFrame({"group": ["novato", "core"] * 3, "hours_to_merge": v})

def test_g1_tem_4_histogramas_com_titulos():
    f = fig_g1(_df([1, 2, 3, 4, 5, 6]), _df([2, 3, 4, 5, 6, 7]))
    assert len([t for t in f.data if t.type == "histogram"]) == 4
    assert f.layout.title.text
    assert "horas" in f.layout.xaxis.title.text
```

- [ ] **Step 2: Rodar** `pytest tests/test_charts_s01.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** com `plotly.subplots.make_subplots(rows=1, cols=2)`, usando cores para real/simulado que **não** sejam as cores dos testes.
- [ ] **Step 4: Rodar** o mesmo comando. Esperado: PASS.
- [ ] **Step 5: Commit** `#<issue> feat: gráfico G1`

### Task 3.2: G2 — distribuição sob H₀, região de rejeição e p-valor

**Files:**
- Create: `lab04/charts/g2.py`
- Modify: `tests/test_charts_s01.py`

**Interfaces:**
- Consumes: `TestResult` (Task 1.2), `ALPHA`
- Produces:
  - `fig_g2_welch(r: TestResult, alpha: float = ALPHA) -> go.Figure`: densidade `t(df=r.df)`, região `|t| > t_{1-α/2}` sombreada (trace `"Região de rejeição"`), área `|t| ≥ |t_obs|` sombreada (trace `"p-valor"`), e linha vertical em `t_obs`. O eixo x é "Estatística t (adimensional)".
  - `fig_g2_mw(r: TestResult, alpha: float = ALPHA) -> go.Figure`: aproximação normal de U sob H₀, com média `n_a·n_b/2` e desvio `sqrt(n_a·n_b·(n_a+n_b+1)/12)`, e os mesmos traces. O eixo x é "Estatística U (contagem de pares)".
  - Todos os traces usam `test_color(r.name)`.

- [ ] **Step 1: Escrever o teste com falha** (acrescentar)

```python
import numpy as np
from lab04.stat_tests import welch, mann_whitney
from lab04.charts.g2 import fig_g2_welch, fig_g2_mw
from lab04.config import COLORS

A = np.random.default_rng(0).lognormal(2, 1, 30); B = A * 0.7

def test_g2_tem_regiao_e_pvalor_na_cor_do_teste():
    for fig, nome in ((fig_g2_welch(welch(A, B)), "welch"), (fig_g2_mw(mann_whitney(A, B)), "mann_whitney")):
        nomes = {t.name for t in fig.data}
        assert {"Região de rejeição", "p-valor"} <= nomes
        assert all(COLORS[nome] in str(t.line.color or t.fillcolor) for t in fig.data if t.name == "p-valor")
        assert fig.layout.xaxis.title.text and fig.layout.yaxis.title.text
```

- [ ] **Step 2: Rodar** `pytest tests/test_charts_s01.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** com `scipy.stats.t.pdf/ppf` e `scipy.stats.norm`, e áreas via `go.Scatter(fill="tozeroy")`. A legenda mostra o p-valor com 4 casas.
- [ ] **Step 4: Rodar** o mesmo comando. Esperado: PASS.
- [ ] **Step 5: Commit** `#<issue> feat: gráfico G2`

### Task 3.3: Dashboard — topo e seções 1–3

**Files:**
- Create: `dashboard/app.py`, `tests/test_app.py`

**Interfaces:**
- Consumes: `results/params.json`, `results/simulado_exemplo.csv`, `results/exemplo.json`, `load_real_data`, `describe_real`, `fig_g1`, `fig_g2_welch`, `fig_g2_mw`, `TestResult.from_dict`, `TEXTOS`, `REPO_URL`, `PROJECT_URL`, `DASHBOARD_URL`
- Produces: a página com, no topo, os links do dashboard e do repositório/Projects. Em seguida vêm os `st.header` "1. Cenário", "2. Os dados", "3. Como os testes funcionam", "4. Erro tipo I", "5. Poder", "6. Dados reais" e "7. Conclusão". As seções 4 a 7 ficam com `st.info("Em construção — Sprint 02 / Final")`. Lê `RESULTS_DIR` da variável de ambiente `LAB04_RESULTS_DIR`, com padrão `config.RESULTS_DIR`.

- [ ] **Step 1: Escrever os testes com falha**

```python
import os
from streamlit.testing.v1 import AppTest

SECOES = ["1. Cenário", "2. Os dados", "3. Como os testes funcionam", "4. Erro tipo I",
          "5. Poder", "6. Dados reais", "7. Conclusão"]

def test_secoes_na_ordem():
    at = AppTest.from_file("dashboard/app.py", default_timeout=30).run()
    assert not at.exception
    assert [h.value for h in at.header] == SECOES

def test_sem_results_mostra_aviso(tmp_path, monkeypatch):
    monkeypatch.setenv("LAB04_RESULTS_DIR", str(tmp_path))
    at = AppTest.from_file("dashboard/app.py", default_timeout=30).run()
    assert not at.exception
    assert any("run_all" in w.value for w in at.warning)
```

- [ ] **Step 2: Rodar** `pytest tests/test_app.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** `app.py` com `st.set_page_config(layout="wide")`. A seção 1 mostra pergunta, H₀/H₁, fonte, n por grupo e palpite. A seção 2 mostra `fig_g1`, a tabela `describe_real`, os parâmetros e `TEXTOS["dados"]`. A seção 3 mostra os dois G2 lado a lado, uma tabela do exemplo (estatística, p-valor, efeito, decisão), `TEXTOS["como_funcionam"]` e `TEXTOS["exemplo"]`. Se faltar algum arquivo de `results/`, mostrar `st.warning("Rode python -m lab04.run_all")` e continuar.
- [ ] **Step 4: Rodar** `pytest -q` e depois `streamlit run dashboard/app.py` para conferir visualmente. Esperado: PASS, com a página mostrando G1 e G2.
- [ ] **Step 5: Commit** `#<issue> feat: dashboard seções 1-3 com G1 e G2`
- [ ] **Step 6: Fechar o sprint.** Rodar `python -m lab04.run_all`, depois `pytest -q`, criar a tag `sprint-01`, mover os cartões para Done e conferir que A, B e C têm Issue com código commitado.

---

# SPRINT 02 — Lab04S02 (7 pontos)

Entregáveis: simulações Q1, Q2 e Q3, e G3 + G4 no dashboard.

## Onda 1 — Integrante A (motor de simulação e análise)

### Task 1.1: Taxas de rejeição e grade de simulação

**Files:**
- Create: `lab04/simulate.py`, `tests/test_simulate.py`

**Interfaces:**
- Consumes: `Scenario`, `generate_groups`, `welch_pvalues`, `mann_whitney_pvalues`, `EFFECTS`, `N_REPS`, `ALPHA`
- Produces:
  - `rejection_rates(rng, scenario: Scenario, effect: float, n_reps: int = N_REPS, alpha: float = ALPHA) -> dict[str, float]`, com chaves `TEST_NAMES`. Gera **um** lote `(A, B)` e aplica os dois testes no mesmo lote.
  - `run_grid(rng, scenarios: Sequence[Scenario], effects: Sequence[float] = EFFECTS, n_reps: int = N_REPS, alpha: float = ALPHA) -> pd.DataFrame`, com colunas `scenario, scenario_label, n, effect, test, rejection_rate, ci_low, ci_high, n_reps`. O IC é de 95% pela aproximação normal: `p ± 1.96·sqrt(p(1-p)/n_reps)`, cortado em [0, 1]. A ordem é cenário → efeito → teste.

- [ ] **Step 1: Escrever os testes com falha**

```python
import numpy as np, pytest
from lab04.scenarios import base_scenario
from lab04.simulate import rejection_rates, run_grid

S = base_scenario(np.log(10), 1.0)

def test_erro_tipo_I_perto_de_5():
    r = rejection_rates(np.random.default_rng(42), S, 0.0, n_reps=10_000)
    for t in ("welch", "mann_whitney"):
        assert 0.040 <= r[t] <= 0.060

def test_poder_cresce_com_efeito():
    g = run_grid(np.random.default_rng(42), [S], effects=(0.0, 0.25, 0.5), n_reps=2000)
    for t, sub in g.groupby("test"):
        rates = sub.sort_values("effect").rejection_rate.to_numpy()
        assert np.all(np.diff(rates) > 0) and rates[-1] > rates[0] + 0.3

def test_grade_formato_e_determinismo():
    a = run_grid(np.random.default_rng(1), [S], effects=(0.0, 0.1), n_reps=300)
    b = run_grid(np.random.default_rng(1), [S], effects=(0.0, 0.1), n_reps=300)
    assert len(a) == 1 * 2 * 2
    assert a.equals(b)
    assert (a.ci_low <= a.rejection_rate).all() and (a.rejection_rate <= a.ci_high).all()
```

- [ ] **Step 2: Rodar** `pytest tests/test_simulate.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar.** `rejection_rate = (pvalues < alpha).mean()`.
- [ ] **Step 4: Rodar** `pytest tests/test_simulate.py -v`. Esperado: PASS. Medir o tempo da grade completa (4 cenários × 6 efeitos × 10.000), que deve ficar abaixo de alguns minutos. Se passar disso, conferir se o cálculo está vetorizado (`axis=1`).
- [ ] **Step 5: Commit** `#<issue> feat: simulação de erro tipo I e poder`

### Task 1.2: Classificar erro tipo I e comparar poder

**Files:**
- Create: `lab04/summary.py`, `tests/test_summary.py`

**Interfaces:**
- Consumes: o DataFrame de `run_grid`
- Produces:
  - `classify_type1(grid: pd.DataFrame, alpha: float = ALPHA) -> pd.DataFrame`, que filtra `effect == 0`. Tem as colunas `scenario, test, rejection_rate, status`, com `status ∈ {"ok", "liberal", "conservador"}`: `"liberal"` se `ci_low > alpha`, `"conservador"` se `ci_high < alpha`, e `"ok"` nos outros casos.
  - `power_winner(grid) -> pd.DataFrame`, com uma linha por `(scenario, effect>0)` e as colunas `scenario, effect, melhor, diferenca`, onde `diferenca = MW − Welch` em pontos percentuais.

- [ ] **Step 1: Escrever os testes com falha**

```python
import pandas as pd, pytest
from lab04.summary import classify_type1, power_winner

G = pd.DataFrame({
    "scenario": ["x"] * 4, "effect": [0.0, 0.0, 0.3, 0.3], "test": ["welch", "mann_whitney"] * 2,
    "rejection_rate": [0.08, 0.03, 0.40, 0.55], "ci_low": [0.075, 0.027, 0.39, 0.54],
    "ci_high": [0.085, 0.033, 0.41, 0.56]})

def test_classifica():
    c = classify_type1(G).set_index("test").status
    assert c["welch"] == "liberal" and c["mann_whitney"] == "conservador"

def test_vencedor_de_poder():
    w = power_winner(G)
    assert w.iloc[0].melhor == "mann_whitney"
    assert w.iloc[0].diferenca == pytest.approx(15.0)
```

- [ ] **Step 2: Rodar** `pytest tests/test_summary.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** com `pivot_table` por teste.
- [ ] **Step 4: Rodar** o mesmo comando. Esperado: PASS.
- [ ] **Step 5: Commit** `#<issue> feat: classificação de erro tipo I e poder`

## Onda 2 — Integrante B (cenários Q3, pipeline S02 e textos)

### Task 2.1: Cenários que violam pressupostos (Q3)

**Files:**
- Modify: `lab04/scenarios.py`
- Test: `tests/test_scenarios.py`

**Interfaces:**
- Produces: `q3_scenarios(base: Scenario) -> list[Scenario]`, que retorna, nesta ordem:
  - `n_pequeno` (n=10)
  - `outliers` (`outlier_frac=0.05`, `outlier_mult=10`)
  - `assimetria_forte` (`sigma = base.sigma * 1.5`)

  Cada um tem um `label` em português que explica a violação. `all_scenarios(base) -> list[Scenario]` retorna `[base, *q3_scenarios(base)]`.

- [ ] **Step 1: Escrever os testes com falha**

```python
import numpy as np
from scipy.stats import skew
from lab04.scenarios import base_scenario, q3_scenarios, all_scenarios
from lab04.generate import generate_groups

B = base_scenario(np.log(10), 1.0)

def test_nomes_e_ordem():
    assert [s.name for s in all_scenarios(B)] == ["base", "n_pequeno", "outliers", "assimetria_forte"]

def test_violacoes_acontecem():
    q = {s.name: s for s in q3_scenarios(B)}
    rng = np.random.default_rng(0)
    assert q["n_pequeno"].n == 10
    base_A, _ = generate_groups(rng, B, 0.0, 2000)
    forte_A, _ = generate_groups(rng, q["assimetria_forte"], 0.0, 2000)
    assert skew(forte_A.ravel()) > skew(base_A.ravel())
    out_A, _ = generate_groups(rng, q["outliers"], 0.0, 2000)
    assert np.all(out_A > 0) and np.all(np.isfinite(out_A))
```

- [ ] **Step 2: Rodar** `pytest tests/test_scenarios.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** com `dataclasses.replace(base, ...)`.
- [ ] **Step 4: Rodar** o mesmo comando. Esperado: PASS.
- [ ] **Step 5: Commit** `#<issue> feat: cenários de violação de pressupostos (Q3)`

### Task 2.2: Comando único — etapa S02

**Files:**
- Modify: `lab04/run_all.py`, `tests/test_run_all.py`
- Output: `results/simulacao.csv`, `results/tipo1_status.csv`, `results/poder_vencedor.csv`

**Interfaces:**
- Consumes: `all_scenarios`, `run_grid`, `classify_type1`, `power_winner`
- Produces: `main(...)` passa a gravar também os 3 CSVs acima. Usa o **mesmo** `rng` que a etapa S01, logo depois dela.

- [ ] **Step 1: Escrever o teste com falha.** Estender `test_gera_arquivos_s01` e `test_reprodutivel` para os 3 arquivos novos, e checar que `simulacao.csv` tem `4 × len(EFFECTS) × 2` linhas.
- [ ] **Step 2: Rodar** `pytest tests/test_run_all.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar.**
- [ ] **Step 4: Rodar** `python -m lab04.run_all` e depois `pytest -q`. Esperado: PASS e `results/` atualizado.
- [ ] **Step 5: Commit** `#<issue> feat: run_all etapa S02 (Q1, Q2, Q3)` (incluir `results/`)

### Task 2.3: Textos das seções 4 e 5

**Files:**
- Modify: `dashboard/textos.py`, `tests/test_textos.py`

**Interfaces:**
- Produces: as chaves `TEXTOS["erro_tipo_1"]`, `TEXTOS["poder"]` e `TEXTOS["violacoes"]` (por que cada cenário Q3 afeta mais o Welch ou o MW).

- [ ] **Step 1: Escrever o teste com falha.** Incluir as 3 chaves novas no teste de chaves, e `"erro_tipo_1"` e `"poder"` no teste de 2 a 4 frases.
- [ ] **Step 2: Rodar** `pytest tests/test_textos.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Escrever os textos** a partir dos resultados reais de `results/tipo1_status.csv` e `results/poder_vencedor.csv`, que saem da Task 2.2 (rodar antes).
- [ ] **Step 4: Rodar** o mesmo comando. Esperado: PASS.
- [ ] **Step 5: Commit** `#<issue> feat: textos de erro tipo I e poder`

## Onda 3 — Integrante C (G3, G4, dashboard e publicação)

### Task 3.1: Gráficos G3 e G4

**Files:**
- Create: `lab04/charts/g3.py`, `lab04/charts/g4.py`, `tests/test_charts_s02.py`

**Interfaces:**
- Consumes: o DataFrame de `run_grid`, `style.test_color`, `style.apply_layout`
- Produces:
  - `fig_g3(grid: pd.DataFrame, alpha: float = ALPHA) -> go.Figure`: barras agrupadas (x = `scenario_label`, uma barra por teste) com `effect == 0`, barras de erro pelo IC e `add_hline(y=alpha)`. O eixo y é "Taxa de erro tipo I (%)", em escala percentual.
  - `fig_g4(grid: pd.DataFrame) -> go.Figure`: um subplot por cenário, com linhas+marcadores de rejeição × efeito, uma linha por teste e legenda única. O eixo x é "Redução da mediana do tempo de merge (%)" e o eixo y é "Poder (% de rejeições)".

- [ ] **Step 1: Escrever os testes com falha**

```python
import pandas as pd
from lab04.charts.g3 import fig_g3
from lab04.charts.g4 import fig_g4
from lab04.config import COLORS

G = pd.DataFrame([{"scenario": s, "scenario_label": s, "n": 30, "effect": e, "test": t,
                   "rejection_rate": 0.05 + e, "ci_low": 0.04 + e, "ci_high": 0.06 + e, "n_reps": 100}
                  for s in ("base", "outliers") for e in (0.0, 0.2) for t in ("welch", "mann_whitney")])

def test_g3_linha_5_e_cores():
    f = fig_g3(G)
    assert any(abs(s.y0 - 0.05) < 1e-9 or abs(s.y0 - 5) < 1e-9 for s in f.layout.shapes)
    for t in f.data:
        assert t.marker.color == COLORS[t.legendgroup]

def test_g4_cores_consistentes_e_legenda_unica():
    f = fig_g4(G)
    for t in f.data:
        assert t.line.color == COLORS[t.legendgroup]
    assert sum(1 for t in f.data if t.showlegend is not False) == 2
```

- [ ] **Step 2: Rodar** `pytest tests/test_charts_s02.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar.** Usar `legendgroup=<nome do teste>` em todos os traces e `showlegend` só no primeiro subplot.
- [ ] **Step 4: Rodar** o mesmo comando. Esperado: PASS.
- [ ] **Step 5: Commit** `#<issue> feat: gráficos G3 e G4`

### Task 3.2: Dashboard — seções 4 e 5 e publicação

**Files:**
- Modify: `dashboard/app.py`, `tests/test_app.py`, `README.md`, `lab04/config.py` (`DASHBOARD_URL`)

**Interfaces:**
- Consumes: `results/simulacao.csv`, `results/tipo1_status.csv`, `results/poder_vencedor.csv`, `fig_g3`, `fig_g4`, e os `TEXTOS` `"erro_tipo_1"`, `"poder"` e `"violacoes"`
- Produces: a seção 4 mostra o G3, a tabela de status e o texto. A seção 5 mostra o G4, a tabela de vencedor e os textos. As seções 6 e 7 continuam "Em construção — Final".

- [ ] **Step 1: Escrever o teste com falha.** Em `test_app.py`, adicionar `test_s02_tem_graficos`: com os `results/` reais, `len(at.get("plotly_chart")) >= 5` (G1, 2×G2, G3, G4), e nenhum `st.info` "Sprint 02" sobrando nas seções 4 e 5.
- [ ] **Step 2: Rodar** `pytest tests/test_app.py -v`. Esperado: FAIL. Commitar o teste: `#<issue> test: ...` (🔴, CONTRIBUTING §1).
- [ ] **Step 3: Implementar** as seções 4 e 5.
- [ ] **Step 4: Rodar** `pytest -q` e `streamlit run dashboard/app.py`. Esperado: PASS e os 4 gráficos visíveis.
- [ ] **Step 5: Publicar** no Streamlit Community Cloud (entry point `dashboard/app.py`), atualizar `DASHBOARD_URL` e o README com o link.
- [ ] **Step 6: Commit** `#<issue> feat: dashboard seções 4-5 com G3 e G4 e publicação`
- [ ] **Step 7: Fechar o sprint.** Rodar `python -m lab04.run_all`, depois `pytest -q`, criar a tag `sprint-02`, mover os cartões para Done e conferir as Issues com código para A, B e C.

---

## Fora do escopo deste plano (Entrega Final)

A seção 6 (tabela dos testes nos dados reais: `welch`/`mann_whitney` sobre `load_real_data`) e a seção 7 (palpite × resultado e recomendação) do dashboard, além da apresentação oral, ficam para um plano posterior. As funções `welch` e `mann_whitney` já devolvem estatística, p-valor e tamanho do efeito, então a seção 6 vai só reaproveitá-las.

## Mapa Tarefa → Issue → Responsável

> A = ArlindoSPJr. Os usuários do GitHub de B e C serão informados depois. Até lá, as Issues de B e C podem ser criadas com o rótulo `integrante-B` ou `integrante-C` e receber o Assignee quando os usuários forem informados (antes de entrar em "In progress").

| Sprint | Onda | Task | Responsável | Issue |
|---|---|---|---|---|
| S01 | 1 | 1.1 Estrutura + config + estilo + Projects | A | #1 |
| S01 | 1 | 1.2 Testes Welch/MW | A | #2 |
| S01 | 1 | 1.3 Cenário + gerador | A | #3 |
| S01 | 2 | 2.1 Coleta e carga dos dados reais | B | #4 |
| S01 | 2 | 2.2 Cenário escrito + textos 1–3 | B | #5 |
| S01 | 2 | 2.3 run_all S01 | B | #6 |
| S01 | 3 | 3.1 G1 | C | #7 |
| S01 | 3 | 3.2 G2 | C | #8 |
| S01 | 3 | 3.3 Dashboard 1–3 | C | #9 |
| S02 | 1 | 1.1 Simulação Q1/Q2 | A | #10 |
| S02 | 1 | 1.2 Classificação tipo I / poder | A | #11 |
| S02 | 2 | 2.1 Cenários Q3 | B | #12 |
| S02 | 2 | 2.2 run_all S02 | B | #13 |
| S02 | 2 | 2.3 Textos 4–5 | B | #14 |
| S02 | 3 | 3.1 G3 + G4 | C | #15 |
| S02 | 3 | 3.2 Dashboard 4–5 + deploy | C | #16 |

### Equilíbrio de carga (peso: baixa = 1, média = 2, alta = 3)

| Integrante | Sprint 01 | Sprint 02 | Total de Issues | Peso total |
|---|---|---|---|---|
| A | 1.1 (1) + 1.2 (2) + 1.3 (2) = **5** | 1.1 (3) + 1.2 (2) = **5** | 5 | **10** |
| B | 2.1 (3) + 2.2 (1) + 2.3 (2) = **6** | 2.1 (1) + 2.2 (1) + 2.3 (2) = **4** | 6 | **10** |
| C | 3.1 (1) + 3.2 (3) + 3.3 (2) = **6** | 3.1 (2) + 3.2 (2) = **4** | 5 | **10** |

## Perguntas em aberto (o grupo precisa decidir)

1. ~~Repositório dos dados reais~~ **Decidido: `pallets/click`, excluindo automerges.** As regras, a triagem dos 8 repositórios e as limitações estão em `data/REGRAS_COLETA.md`.
2. ~~Uni ou bicaudal~~ **Decidido: bicaudal** (`ALTERNATIVE = "two-sided"`).
3. ~~Valores de efeito~~ **Decidido:** `EFFECTS = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)`.
4. ~~Cenários do Q3~~ **Decidido:** `n_pequeno`, `outliers` e `assimetria_forte`, como no plano.
5. **Links:** o GitHub Projects é https://github.com/users/ArlindoSPJr/projects/6. Ainda falta a URL do repositório de código (`REPO_URL`) e os usuários do GitHub de B e C para os Assignees.
