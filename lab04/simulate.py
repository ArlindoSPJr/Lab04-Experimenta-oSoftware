"""Monte Carlo: taxa de rejeição dos dois testes (erro tipo I com effect=0, poder com effect>0)."""
from collections.abc import Sequence

import numpy as np
import pandas as pd

from lab04.config import ALPHA, EFFECTS, N_REPS, TEST_NAMES
from lab04.generate import generate_groups
from lab04.scenarios import Scenario
from lab04.stat_tests import mann_whitney_pvalues, welch_pvalues

_PVALUES = {"welch": welch_pvalues, "mann_whitney": mann_whitney_pvalues}

COLUMNS = ["scenario", "scenario_label", "n", "effect", "test",
           "rejection_rate", "ci_low", "ci_high", "n_reps"]


def rejection_rates(
    rng: np.random.Generator, scenario: Scenario, effect: float,
    n_reps: int = N_REPS, alpha: float = ALPHA,
) -> dict[str, float]:
    """Gera um lote `(A, B)` e aplica os dois testes no mesmo lote; devolve a fração de p < alpha."""
    A, B = generate_groups(rng, scenario, effect, n_reps)
    return {t: float((_PVALUES[t](A, B) < alpha).mean()) for t in TEST_NAMES}


def _ci95(p: float, n_reps: int) -> tuple[float, float]:
    half = 1.96 * np.sqrt(p * (1 - p) / n_reps)
    return max(0.0, p - half), min(1.0, p + half)


def run_grid(
    rng: np.random.Generator, scenarios: Sequence[Scenario],
    effects: Sequence[float] = EFFECTS, n_reps: int = N_REPS, alpha: float = ALPHA,
) -> pd.DataFrame:
    """Taxa de rejeição e IC 95% (aproximação normal) na ordem cenário → efeito → teste."""
    rows = []
    for s in scenarios:
        for e in effects:
            rates = rejection_rates(rng, s, e, n_reps, alpha)
            for t in TEST_NAMES:
                lo, hi = _ci95(rates[t], n_reps)
                rows.append({"scenario": s.name, "scenario_label": s.label, "n": s.n,
                             "effect": float(e), "test": t, "rejection_rate": rates[t],
                             "ci_low": lo, "ci_high": hi, "n_reps": n_reps})
    return pd.DataFrame(rows, columns=COLUMNS)
