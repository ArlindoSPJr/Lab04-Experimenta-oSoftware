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
# Mesma cor para cada teste em todos os gráficos (exigência do enunciado).
# Paleta validada sobre branco: contraste >= 3:1 e separação para daltonismo
# (protan/deutan/tritan) entre as quatro cores abaixo, comparadas duas a duas.
COLORS: dict[str, str] = {"welch": "#2a78d6", "mann_whitney": "#d55e00"}

# Convenção: a = novato, b = core
GROUPS: tuple[str, ...] = ("novato", "core")

# Cores de dados real × simulado no G1 (diferentes das cores dos testes)
DATA_COLORS: dict[str, str] = {"real": "#a23b8f", "simulado": "#20a080"}
GROUP_LABELS: dict[str, str] = {"novato": "Novatos", "core": "Core team"}

# Cores de apoio dos gráficos (fundo, texto, grade, linhas de referência).
# Fundo branco: o dashboard é apresentado em projetor.
CHART_COLORS: dict[str, str] = {
    "fundo": "#ffffff",
    "texto": "#1f1f1f",
    "texto_secundario": "#52514e",  # rótulos de apoio e linhas de referência (7,9:1 sobre branco)
    "grade": "#e5e4df",
    "eixo": "#9a998f",
}
FONT_SIZE: int = 15  # px; rótulos de eixo legíveis em projetor (mínimo 14)

ROOT: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = ROOT / "data"
RESULTS_DIR: Path = ROOT / "results"

REPO_URL: str = "https://github.com/ArlindoSPJr/Lab04-Experimenta-oSoftware"
PROJECT_URL: str = "https://github.com/users/ArlindoSPJr/projects/6"
DASHBOARD_URL: str = "https://lab04-experimentacao-software.streamlit.app/"
