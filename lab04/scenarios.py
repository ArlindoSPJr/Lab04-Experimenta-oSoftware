"""Cenários da simulação: parâmetros da lognormal do grupo `novato` e contaminação por outliers."""
from dataclasses import dataclass

from lab04.config import N_PER_GROUP


@dataclass(frozen=True)
class Scenario:
    """Situação simulada. `mu` e `sigma` são parâmetros do log do grupo `novato`."""

    name: str
    label: str
    n: int
    mu: float
    sigma: float
    outlier_frac: float = 0.0
    outlier_mult: float = 10.0


def base_scenario(mu: float, sigma: float, n: int = N_PER_GROUP) -> Scenario:
    """Cenário base: lognormal ajustada aos dados reais, sem violação de pressupostos."""
    return Scenario(name="base", label="Base (lognormal ajustada, n=30)", n=n, mu=mu, sigma=sigma)
