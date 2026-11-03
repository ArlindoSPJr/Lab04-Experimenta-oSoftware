"""Gerador dos dados simulados: tempo até o merge (horas) dos grupos novato (A) e core (B)."""
import numpy as np

from lab04.scenarios import Scenario


def generate_groups(
    rng: np.random.Generator, scenario: Scenario, effect: float, n_reps: int = 1
) -> tuple[np.ndarray, np.ndarray]:
    """Sorteia `(A, B)` com shape `(n_reps, scenario.n)`.

    A ~ LogNormal(mu, sigma) e B ~ LogNormal(mu + ln(1 - effect), sigma), ou seja,
    `effect` é a redução relativa da mediana do grupo core. Com `outlier_frac > 0`,
    cada valor dos dois grupos é multiplicado por `outlier_mult` com essa probabilidade.
    """
    if not (0 <= effect < 1):  # também recusa NaN
        raise ValueError(f"effect deve estar em [0, 1), recebido {effect!r}")
    if not (0 <= scenario.outlier_frac <= 1):  # também recusa NaN
        raise ValueError(f"outlier_frac deve estar em [0, 1], recebido {scenario.outlier_frac!r}")
    if not (np.isfinite(scenario.outlier_mult) and scenario.outlier_mult > 0):
        raise ValueError(f"outlier_mult deve ser finito e > 0, recebido {scenario.outlier_mult!r}")
    size = (n_reps, scenario.n)
    a = rng.lognormal(scenario.mu, scenario.sigma, size=size)
    b = rng.lognormal(scenario.mu + np.log(1 - effect), scenario.sigma, size=size)
    if scenario.outlier_frac > 0:
        for x in (a, b):
            x[rng.random(size) < scenario.outlier_frac] *= scenario.outlier_mult
    return a, b
