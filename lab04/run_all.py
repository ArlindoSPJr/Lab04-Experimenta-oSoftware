"""Comando único do Lab04: `python -m lab04.run_all` grava todos os resultados em `results/`.

Etapa S01: parâmetros da lognormal ajustada aos dados reais, um dataset simulado de exemplo
e os dois testes aplicados a ele. O único gerador aleatório é criado aqui, com `SEED`.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from lab04.config import DATA_DIR, GROUPS, N_REPS, RESULTS_DIR, ROOT, SEED
from lab04.generate import generate_groups
from lab04.real_data import fit_lognormal, load_real_data
from lab04.scenarios import base_scenario
from lab04.stat_tests import mann_whitney, welch

EXAMPLE_EFFECT: float = 0.2


def _write_json(path: Path, obj: dict) -> None:
    # sort_keys e "\n" fixo: o arquivo sai igual byte a byte em qualquer execução e SO
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                    encoding="utf-8", newline="\n")


def _relative(path: Path) -> str:
    path = Path(path).resolve()
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()


def main(n_reps: int = N_REPS, out_dir: Path = RESULTS_DIR,
         data_path: Path = DATA_DIR / "real_prs.csv") -> None:
    """Roda o pipeline com semente fixa. `n_reps` é usado pela simulação da S02."""
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
    print(f"Resultados gravados em {out_dir}")


if __name__ == "__main__":
    main()
