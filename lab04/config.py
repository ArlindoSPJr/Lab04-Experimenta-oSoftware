"""Constantes globais do Lab04 (P1: t de Welch × Mann-Whitney, novatos × core team).

Todos os módulos importam daqui; nenhum outro arquivo repete estes valores.
"""
from pathlib import Path

# Reprodutibilidade e simulação (Enunciado: semente fixa, alfa 5%, 10.000 repetições)
SEED: int = 42
ALPHA: float = 0.05
N_REPS: int = 10_000
N_PER_GROUP: int = 30

# Redução relativa da mediana do tempo de merge do grupo `core` (0 = H0 verdadeira)
EFFECTS: tuple[float, ...] = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)

# Teste bicaudal (decisão do grupo)
ALTERNATIVE: str = "two-sided"

TEST_NAMES: tuple[str, ...] = ("welch", "mann_whitney")
LABELS: dict[str, str] = {"welch": "t de Welch", "mann_whitney": "Mann-Whitney"}
# Mesma cor para cada teste em todos os gráficos (exigência do enunciado)
COLORS: dict[str, str] = {"welch": "#1f77b4", "mann_whitney": "#ff7f0e"}

# Convenção: a = novato, b = core
GROUPS: tuple[str, ...] = ("novato", "core")

ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = ROOT / "data"
RESULTS_DIR: Path = ROOT / "results"

REPO_URL: str = "https://github.com/ArlindoSPJr/Lab04-Experimenta-oSoftware"
PROJECT_URL: str = "https://github.com/users/ArlindoSPJr/projects/6"
DASHBOARD_URL: str = ""  # preenchido na publicação (Issue #16)
