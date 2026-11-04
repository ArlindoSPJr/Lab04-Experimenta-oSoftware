# Issue #2 — Testes de hipótese (t de Welch e Mann-Whitney) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar `lab04/stat_tests.py` com os dois testes do par P1 (t de Welch e Mann-Whitney), em versão escalar (com `TestResult`) e vetorizada (só p-valores, para as 10.000 repetições).

**Architecture:** Um módulo só, sem estado. As funções escalares embrulham `scipy.stats.ttest_ind(equal_var=False)` e `scipy.stats.mannwhitneyu` num `TestResult` imutável e serializável em JSON; as vetorizadas chamam as mesmas funções do SciPy com `axis=1` e devolvem só o vetor de p-valores.

**Tech Stack:** Python 3, NumPy, SciPy (≥ 1.11; venv tem 1.18.1), pytest.

**Spec:** `docs/superpowers/plans/2026-11-03-lab04-testes-hipotese.md`, Sprint 01, **Task 1.2**, e a Issue #2 (Contexto, Objetivos, Checkpoints).

## Global Constraints

- `ALPHA = 0.05` e `ALTERNATIVE = "two-sided"` vêm de `lab04/config.py`; não redefinir.
- Convenção de grupos: `a = novato`, `b = core`. Efeito positivo = novatos mais lentos (média/postos de `a` maiores).
- Bibliotecas: só NumPy e SciPy neste módulo. Nada de pacotes novos.
- TDD (CONTRIBUTING §1): commit `#2 test: ...` antes do `#2 feat: ...`. Todo commit começa com `#2` e termina com `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Escopo de arquivos: só `lab04/stat_tests.py` e `tests/test_stat_tests.py`.

## Review Focus

1. **`to_dict()` com tipos NumPy** (`np.float64`, `np.bool_`): o `results/*.json` da Task 2.3 quebraria no `json.dumps`. Esperado: só `float`/`bool`/`int`/`None` Python. Teste `test_to_dict_serializa_em_json`.
2. **`alpha` diferente do padrão**: `reject` deve ser `p_value < alpha` com o `alpha` recebido, não com `ALPHA`. Teste `test_reject_respeita_alpha`.
3. **Sinal do efeito**: com `a` claramente maior que `b`, d e r devem ser positivos (convenção novato − core). Teste `test_sinal_do_efeito`.
4. **Empates nos dados reais** (horas arredondadas): Mann-Whitney deve devolver p finito e r em `[-1, 1]`. Teste `test_mann_whitney_com_empates`.
5. **Coleta do pytest**: `TestResult` começa com "Test" e é importado no arquivo de teste; o pytest tenta coletá-lo e emite `PytestCollectionWarning`. Esperado: `__test__ = False` na classe e `pytest -q` sem warnings. Verificado no Step 4.

---

### Task 1: `lab04/stat_tests.py`

**Files:**
- Create: `lab04/stat_tests.py`
- Test: `tests/test_stat_tests.py`

**Interfaces:**
- Consumes: `lab04.config.ALPHA`, `lab04.config.ALTERNATIVE`
- Produces (usado por #6, #8, #10):
  - `@dataclass(frozen=True) class TestResult: name: str; statistic: float; p_value: float; reject: bool; effect_size: float; effect_label: str; df: float | None; n_a: int; n_b: int`, com `to_dict() -> dict` e `@classmethod from_dict(d: dict) -> TestResult`
  - `welch(a: np.ndarray, b: np.ndarray, alpha: float = ALPHA) -> TestResult` — `name="welch"`, efeito `(mean_a - mean_b) / sqrt((var_a + var_b) / 2)` (ddof=1), `effect_label="d de Cohen"`, `df` de Welch
  - `mann_whitney(a: np.ndarray, b: np.ndarray, alpha: float = ALPHA) -> TestResult` — `name="mann_whitney"`, estatística = U de `a`, efeito `2*U/(n_a*n_b) - 1`, `effect_label="r rank-biserial"`, `df=None`
  - `welch_pvalues(A: np.ndarray, B: np.ndarray) -> np.ndarray` e `mann_whitney_pvalues(A: np.ndarray, B: np.ndarray) -> np.ndarray` — entradas `(n_reps, n)`, saída `(n_reps,)`, `axis=1`

- [ ] **Step 1: Escrever os testes com falha** em `tests/test_stat_tests.py`: os quatro testes do plano mestre, sem alteração, mais os do Review Focus:

```python
import json
import numpy as np, pytest
from lab04.stat_tests import welch, mann_whitney, welch_pvalues, mann_whitney_pvalues, TestResult

# --- plano mestre (Task 1.2), literais ---
def test_welch_valores_conhecidos(): ...          # t=-1, p≈0.3466, df=8, d≈-0.6325, reject False
def test_mann_whitney_valores_conhecidos(): ...   # U=0, p=0.1, r=-1
def test_vetorizado_igual_ao_escalar(): ...       # rng(0), lognormal (50, 30), linha 7
def test_roundtrip_dict(): ...

# --- Review Focus ---
def test_to_dict_serializa_em_json():
    for r in (welch(np.array([1., 2, 3, 4]), np.array([2., 3, 5, 9])),
              mann_whitney(np.array([1., 2, 3, 4]), np.array([2., 3, 5, 9]))):
        assert TestResult.from_dict(json.loads(json.dumps(r.to_dict()))) == r
        assert type(r.reject) is bool and type(r.p_value) is float and type(r.n_a) is int

def test_reject_respeita_alpha():
    a, b = np.array([1., 2, 3, 4, 5]), np.array([2., 3, 4, 5, 6])
    assert welch(a, b, alpha=0.5).reject is True       # p ≈ 0.3466
    assert mann_whitney(np.array([1., 2, 3]), np.array([4., 5, 6]), alpha=0.2).reject is True  # p = 0.1

def test_sinal_do_efeito():
    a, b = np.array([10., 11, 12, 13, 14]), np.array([1., 2, 3, 4, 5])
    assert welch(a, b).effect_size > 0 and mann_whitney(a, b).effect_size == pytest.approx(1.0)

def test_mann_whitney_com_empates():
    r = mann_whitney(np.array([1., 1, 2, 2, 3]), np.array([2., 2, 3, 3, 4]))
    assert np.isfinite(r.p_value) and -1 <= r.effect_size <= 1
```

(Os `...` acima são os corpos literais do plano mestre, Task 1.2 Step 1.)

- [ ] **Step 2: Rodar** `C:/Faculdade/Lab04-Experimenta-oSoftware/.venv/Scripts/python -m pytest tests/test_stat_tests.py -v`. Esperado: FAIL na coleta com `ModuleNotFoundError: No module named 'lab04.stat_tests'`. Commit: `#2 test: welch e mann-whitney conferem com valores conhecidos`.

- [ ] **Step 3: Implementar** `lab04/stat_tests.py` com as interfaces acima. `scipy.stats.ttest_ind(a, b, equal_var=False, alternative=ALTERNATIVE)` (o `df` vem de `res.df`); `scipy.stats.mannwhitneyu(a, b, alternative=ALTERNATIVE, method="auto")` (o `statistic` já é o U de `a`). Vetorizadas: mesmas chamadas com `axis=1`. Converter tudo para `float`/`bool`/`int` Python; `reject = p_value < alpha`. `from_dict` = `cls(**d)`. Colocar `__test__ = False` em `TestResult` (Review Focus 5).

- [ ] **Step 4: Rodar** `... -m pytest -q`. Esperado: todos PASS (test_config + test_stat_tests) e nenhum `PytestCollectionWarning`.

- [ ] **Step 5: Commit** `#2 feat: testes de Welch e Mann-Whitney`. Depois `git push -u origin issue-2-testes-estatisticos` (sem PR; aguarda revisão independente).
