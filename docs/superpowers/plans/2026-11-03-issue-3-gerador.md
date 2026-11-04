# Issue #3 — Cenário e gerador de dados simulados (lognormal) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o `Scenario` imutável e o gerador lognormal `generate_groups`, que produzem os grupos `novato` (A) e `core` (B) da simulação de Monte Carlo com efeito controlado.

**Architecture:** `lab04/scenarios.py` guarda só a descrição do cenário (dataclass congelada + fábrica `base_scenario`). `lab04/generate.py` recebe o `rng` de fora e sorteia matrizes `(n_reps, n)` de uma lognormal; o efeito desloca o `mu` do grupo B em `ln(1 - effect)`, o que reduz a mediana em `effect`. Os cenários Q3 (S02, Task 2.1) serão acrescentados depois em `scenarios.py`, sem mudar estas interfaces.

**Tech Stack:** Python ≥ 3.11, NumPy (`Generator.lognormal`, `Generator.random`), pytest.

**Spec:** `docs/superpowers/plans/2026-11-03-lab04-testes-hipotese.md`, Sprint 01, Task 1.3, e a Issue #3 (Objetivos e Checkpoints).

## Global Constraints

- `rng` sempre recebido como parâmetro; nenhum módulo chama `np.random.default_rng` nem `np.random.seed`.
- Constantes vêm de `lab04/config.py` (`N_PER_GROUP = 30`); não redefinir.
- `mu` e `sigma` são parâmetros **do log** do grupo `novato`.
- `effect` = redução relativa da mediana do grupo `core`; válido só em `[0, 1)`, caso contrário `ValueError`.
- Commits: `#3 <tipo>: ...`, com o `test:` antes do `feat:` (CONTRIBUTING §1 e §4).
- Arquivos permitidos: `lab04/scenarios.py`, `lab04/generate.py`, `tests/test_generate.py`, este plano.

## Review Focus

1. **Outliers produzindo valor ≤ 0, `inf` ou NaN**: todo valor gerado deve ser finito e > 0 em qualquer cenário (teste `test_outliers_positivos_e_finitos`).
2. **Efeito negativo** (`-0.1`): `ln(1.1)` não quebraria nada e geraria dados "válidos" silenciosamente, invertendo o sinal da hipótese. Deve dar `ValueError` (teste `test_efeito_invalido`, parametrizado).
3. **Efeito NaN**: comparações com NaN são falsas, então uma checagem `effect < 0 or effect >= 1` deixaria passar e geraria só NaN. A checagem deve ser `not (0 <= effect < 1)` (mesmo teste parametrizado).
4. **Efeito 0 (H₀ verdadeira)**: é o caso de borda válido; os dois grupos devem ter a mesma mediana (teste `test_efeito_zero_mesma_mediana`).
5. **`Scenario` mutável**: um cenário alterado no meio da grade contaminaria as condições seguintes; a dataclass precisa ser `frozen` (teste `test_scenario_imutavel`).

---

### Task 1: Scenario + generate_groups

**Files:**
- Create: `lab04/scenarios.py`, `lab04/generate.py`
- Test: `tests/test_generate.py`

**Interfaces:**
- Consumes: `lab04.config.N_PER_GROUP`
- Produces:
  - `@dataclass(frozen=True) class Scenario: name: str; label: str; n: int; mu: float; sigma: float; outlier_frac: float = 0.0; outlier_mult: float = 10.0`
  - `base_scenario(mu: float, sigma: float, n: int = N_PER_GROUP) -> Scenario`, com `name="base"`, `label="Base (lognormal ajustada, n=30)"`
  - `generate_groups(rng: np.random.Generator, scenario: Scenario, effect: float, n_reps: int = 1) -> tuple[np.ndarray, np.ndarray]` → `(A, B)`, shape `(n_reps, scenario.n)`; `A ~ LogNormal(mu, sigma)`, `B ~ LogNormal(mu + ln(1 - effect), sigma)`; com `outlier_frac > 0`, cada valor dos dois grupos é multiplicado por `outlier_mult` com probabilidade `outlier_frac`.
  - Consumidores: #6 (pipeline S01), #10 (`run_grid`), #12 (cenários Q3).

- [ ] **Step 1: Escrever os testes com falha** em `tests/test_generate.py`: os cinco testes do plano mestre (`test_formato`, `test_efeito_reduz_mediana`, `test_mesma_semente_mesmos_dados`, `test_outliers_positivos_e_finitos`, `test_efeito_invalido`), com `test_efeito_invalido` parametrizado em `[1.0, 1.5, -0.1, float("nan")]`, mais:

```python
def test_base_scenario():
    assert S == Scenario("base", "Base (lognormal ajustada, n=30)", 30, np.log(10), 1.0)

def test_scenario_imutavel():
    with pytest.raises(dataclasses.FrozenInstanceError):
        S.n = 5

def test_efeito_zero_mesma_mediana():
    A, B = generate_groups(np.random.default_rng(1), S, 0.0, n_reps=4000)
    assert np.median(B) == pytest.approx(np.median(A), rel=0.05)
```

- [ ] **Step 2: Rodar** `pytest tests/test_generate.py -v`. Esperado: FAIL com `ModuleNotFoundError: lab04.scenarios`. Commit `#3 test: gerador lognormal, formato, efeito, semente e outliers`.
- [ ] **Step 3: Implementar** `scenarios.py` e `generate.py`: `rng.lognormal(mean, sigma, size=(n_reps, n))` para A e depois B; se `outlier_frac > 0`, aplicar a máscara `rng.random(size) < outlier_frac` em A e em B. Validar `effect` com `not (0 <= effect < 1)` antes de sortear.
- [ ] **Step 4: Rodar** `pytest -q`. Esperado: tudo PASS.
- [ ] **Step 5: Commit** `#3 feat: gerador de dados simulados (lognormal)`.
