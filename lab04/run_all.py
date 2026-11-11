"""Comando único do Lab04: `python -m lab04.run_all` grava todos os resultados em `results/`.

Etapa S01: parâmetros da lognormal ajustada aos dados reais, um dataset simulado de exemplo
e os dois testes aplicados a ele.
Etapa S02: erro tipo I e poder dos dois testes nos quatro cenários (base + Q3), em
`simulacao.csv`, com os resumos `tipo1_status.csv` e `poder_vencedor.csv`.
O único gerador aleatório é criado aqui, com `SEED`, e a S02 o usa logo depois da S01.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from lab04.config import DATA_DIR, GROUPS, N_REPS, RESULTS_DIR, ROOT, SEED
from lab04.generate import generate_groups
from lab04.real_data import fit_lognormal, load_real_data
from lab04.scenarios import all_scenarios, base_scenario
from lab04.simulate import run_grid
from lab04.stat_tests import mann_whitney, welch
from lab04.summary import classify_type1, power_winner

EXAMPLE_EFFECT: float = 0.2


def _write_json(path: Path, obj: dict) -> None:
    # sort_keys e "\n" fixo: o arquivo sai igual byte a byte em qualquer execução e SO
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                    encoding="utf-8", newline="\n")


def _relative(path: Path) -> str:
    path = Path(path).resolve()
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()


def _write_csv(path: Path, df: pd.DataFrame) -> None:
    df.to_csv(path, index=False, float_format="%.6f", lineterminator="\n")


def main(n_reps: int = N_REPS, out_dir: Path = RESULTS_DIR,
         data_path: Path = DATA_DIR / "real_prs.csv") -> None:
    """Roda o pipeline com semente fixa. `n_reps` é o número de repetições por condição na S02."""
    rng = np.random.default_rng(SEED)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_real_data(data_path)
    mu, sigma = fit_lognormal(df.loc[df["group"] == GROUPS[0], "hours_to_merge"])
    scenario = base_scenario(mu, sigma)
    _write_json(out_dir / "params.json",
                {"mu": mu, "sigma": sigma, "n": scenario.n, "fonte": _relative(data_path)})

    A, B = generate_groups(rng, scenario, EXAMPLE_EFFECT)
    a, b = A[0], B[0]
    sim = pd.DataFrame({"group": np.repeat(GROUPS, scenario.n), "hours_to_merge": np.concatenate([a, b])})
    sim.to_csv(out_dir / "simulado_exemplo.csv", index=False, float_format="%.6f", lineterminator="\n")
    _write_json(out_dir / "exemplo.json", {"effect": EXAMPLE_EFFECT,
                                           "welch": welch(a, b).to_dict(),
                                           "mann_whitney": mann_whitney(a, b).to_dict()})

    # S02: mesmo rng, logo depois da S01 (assim os arquivos da S01 não mudam)
    grid = run_grid(rng, all_scenarios(scenario), n_reps=n_reps)
    _write_csv(out_dir / "simulacao.csv", grid)
    _write_csv(out_dir / "tipo1_status.csv", classify_type1(grid))
    _write_csv(out_dir / "poder_vencedor.csv", power_winner(grid))
    print(f"Resultados gravados em {out_dir}")


if __name__ == "__main__":
    main()
