"""Cenários da simulação: parâmetros da lognormal do grupo `novato` e contaminação por outliers."""
from dataclasses import dataclass, replace

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


def q3_scenarios(base: Scenario) -> list[Scenario]:
    """Cenários do Q3: cada um viola um pressuposto do t de Welch e muda só uma coisa do `base`.

    - `n_pequeno`: n = 10, a aproximação pela distribuição t fica pior com poucos dados;
    - `outliers`: 5% dos PRs (dos dois grupos) com o tempo multiplicado por 10, o que infla a variância;
    - `assimetria_forte`: σ do log 1,5 vez maior, a cauda direita fica ainda mais longa.
    """
    return [
        replace(base, name="n_pequeno", label="Amostra pequena (n=10)", n=10),
        replace(base, name="outliers", label="Outliers (5% dos PRs com tempo ×10)",
                outlier_frac=0.05, outlier_mult=10.0),
        replace(base, name="assimetria_forte", label="Assimetria forte (σ × 1,5)",
                sigma=base.sigma * 1.5),
    ]


def all_scenarios(base: Scenario) -> list[Scenario]:
    """O cenário base seguido dos cenários do Q3, na ordem usada na simulação e nos gráficos."""
    return [base, *q3_scenarios(base)]
