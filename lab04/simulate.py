"""Monte Carlo: taxa de rejeição dos dois testes (erro tipo I com effect=0, poder com effect>0)."""
from collections.abc import Sequence

import numpy as np
import pandas as pd

from lab04.config import ALPHA, ALPHAS, EFFECTS, N_REPS, TEST_NAMES
from lab04.generate import generate_groups
from lab04.scenarios import Scenario
from lab04.stat_tests import mann_whitney_pvalues, welch_pvalues

_PVALUES = {"welch": welch_pvalues, "mann_whitney": mann_whitney_pvalues}

COLUMNS = ["scenario", "scenario_label", "n", "effect", "alpha", "test",
           "rejection_rate", "ci_low", "ci_high", "n_reps"]


def _pvalues(rng: np.random.Generator, scenario: Scenario, effect: float,
             n_reps: int) -> dict[str, np.ndarray]:
    """Gera um lote `(A, B)` e devolve os p-valores dos dois testes sobre o mesmo lote."""
    A, B = generate_groups(rng, scenario, effect, n_reps)
    return {t: _PVALUES[t](A, B) for t in TEST_NAMES}


def rejection_rates(
    rng: np.random.Generator, scenario: Scenario, effect: float,
    n_reps: int = N_REPS, alpha: float = ALPHA,
) -> dict[str, float]:
    """Gera um lote `(A, B)` e aplica os dois testes no mesmo lote; devolve a fração de p < alpha."""
    p = _pvalues(rng, scenario, effect, n_reps)
    return {t: float((p[t] < alpha).mean()) for t in TEST_NAMES}


def _ci95(p: float, n_reps: int) -> tuple[float, float]:
    half = 1.96 * np.sqrt(p * (1 - p) / n_reps)
    return max(0.0, p - half), min(1.0, p + half)


def run_grid(
    rng: np.random.Generator, scenarios: Sequence[Scenario],
    effects: Sequence[float] = EFFECTS, n_reps: int = N_REPS,
    alphas: Sequence[float] = ALPHAS,
) -> pd.DataFrame:
    """Taxa de rejeição e IC 95% (aproximação normal), em blocos por alfa e, dentro de cada
    bloco, na ordem cenário → efeito → teste.

    Cada (cenário, efeito) sorteia um único lote; os p-valores são calculados uma vez e
    contados contra cada alfa. Assim a sequência do `rng` não depende de `alphas` e as
    linhas de um alfa são as mesmas com ou sem os outros.
    """
    blocos: dict[float, list[dict]] = {float(a): [] for a in alphas}
    for s in scenarios:
        for e in effects:
            p = _pvalues(rng, s, e, n_reps)
            for a, rows in blocos.items():
                for t in TEST_NAMES:
                    rate = float((p[t] < a).mean())
                    lo, hi = _ci95(rate, n_reps)
                    rows.append({"scenario": s.name, "scenario_label": s.label, "n": s.n,
                                 "effect": float(e), "alpha": a, "test": t,
                                 "rejection_rate": rate, "ci_low": lo, "ci_high": hi,
                                 "n_reps": n_reps})
    rows = [r for bloco in blocos.values() for r in bloco]
    return pd.DataFrame(rows, columns=COLUMNS)
