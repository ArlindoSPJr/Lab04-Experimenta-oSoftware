"""Coleta dos PRs de `pallets/click` seguindo as regras R1–R11 de `data/REGRAS_COLETA.md`.

Uso: `python scripts/collect_prs.py` (token em `GITHUB_TOKEN`, ou `gh auth login`).
"""
import csv
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # permite rodar como script

from lab04.config import DATA_DIR, GROUPS, N_PER_GROUP  # noqa: E402

GRAPHQL_URL = "https://api.github.com/graphql"
CUTOFF = "2026-11-04T00:00:00Z"
CORE_ASSOCIATIONS = {"MEMBER", "OWNER", "COLLABORATOR"}
COLUMNS = ["pr_number", "author", "author_association", "merged_by", "group",
           "created_at", "merged_at", "hours_to_merge"]

QUERY = """
query($endCursor: String) {
  repository(owner: "pallets", name: "click") {
    pullRequests(first: 100, after: $endCursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number authorAssociation createdAt mergedAt
        author { login __typename }
        mergedBy { login }
      }
    }
  }
}
"""


def _ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _order(pr: dict) -> tuple[datetime, int]:
    return _ts(pr["created_at"]), pr["number"]


def pr_to_row(pr: dict, group: str) -> dict | None:
    """Linha da R10, com `hours_to_merge` da R9. Retorna None se o PR não foi mergeado."""
    if pr["merged_at"] is None:
        return None
    hours = (_ts(pr["merged_at"]) - _ts(pr["created_at"])).total_seconds() / 3600
    user = pr.get("user") or {}
    return {"pr_number": pr["number"], "author": user.get("login"),
            "author_association": pr.get("author_association"), "merged_by": pr.get("merged_by"),
            "group": group, "created_at": pr["created_at"], "merged_at": pr["merged_at"],
            "hours_to_merge": round(hours, 6)}


def _is_bot(user: dict) -> bool:
    return user["type"] == "Bot" or user["login"].endswith("[bot]")


def classify_prs(prs: list[dict], cutoff: str = CUTOFF) -> list[tuple[dict, str]]:
    """Aplica as regras R2 a R7 e devolve `(pr, grupo)` em ordem de criação.

    Todo PR com autor conhecido entra no histórico (R6), mesmo que seja excluído pela R4.3–R4.5.
    """
    limit = _ts(cutoff)
    seen: set[str] = set()
    out = []
    for pr in sorted(prs, key=_order):
        user = pr["user"]
        if user is None:  # R4.2: autor apagado, sem histórico possível
            continue
        first_pr = user["login"] not in seen
        seen.add(user["login"])
        if (_is_bot(user)                                                         # R4.1
                or pr["merged_at"] is None                                        # R4.3
                or pr["merged_by"] in (None, user["login"])                       # R4.4
                or _ts(pr["created_at"]) >= limit or _ts(pr["merged_at"]) >= limit):  # R4.5 / R2
            continue
        if pr["author_association"] in CORE_ASSOCIATIONS:  # R5 tem precedência sobre a R6
            out.append((pr, "core"))
        elif first_pr:                                     # R6
            out.append((pr, "novato"))
        # R7: contribuidor recorrente fica de fora
    return out


def select_sample(classified: list[tuple[dict, str]], n: int = N_PER_GROUP) -> list[tuple[dict, str]]:
    """R8: os `n` PRs mais recentes de cada grupo (empate: maior `number`), do mais novo ao mais antigo."""
    out = []
    for g in GROUPS:
        prs = sorted((pr for pr, grp in classified if grp == g), key=_order, reverse=True)
        out += [(pr, g) for pr in prs[:n]]
    return out


def _token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        sys.exit("Defina GITHUB_TOKEN ou rode `gh auth login` (R1).")


def _normalize(node: dict) -> dict:
    author = node["author"]
    return {"number": node["number"],
            "user": None if author is None else {"login": author["login"], "type": author["__typename"]},
            "author_association": node["authorAssociation"], "created_at": node["createdAt"],
            "merged_at": node["mergedAt"], "merged_by": (node["mergedBy"] or {}).get("login")}


def fetch_all_prs(token: str) -> list[dict]:
    """R1 + R3: histórico completo de PRs, paginado, já no formato interno."""
    prs, cursor = [], None
    while True:
        body = json.dumps({"query": QUERY, "variables": {"endCursor": cursor}}).encode()
        req = urllib.request.Request(GRAPHQL_URL, data=body,
                                     headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.load(resp)
        if "errors" in payload:
            raise RuntimeError(payload["errors"])
        page = payload["data"]["repository"]["pullRequests"]
        prs += [_normalize(n) for n in page["nodes"]]
        if not page["pageInfo"]["hasNextPage"]:
            return prs
        cursor = page["pageInfo"]["endCursor"]


def main(out_path: Path = DATA_DIR / "real_prs.csv") -> None:
    prs = fetch_all_prs(_token())
    classified = classify_prs(prs)
    rows = [pr_to_row(pr, g) for pr, g in select_sample(classified)]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows({**r, "hours_to_merge": f"{r['hours_to_merge']:.6f}"} for r in rows)
    # Números para a R12 (Registro da coleta)
    print(f"PRs no histórico: {len(prs)}")
    for g in GROUPS:
        dates = sorted(r["created_at"] for r in rows if r["group"] == g)
        n_elig = sum(1 for _, grp in classified if grp == g)
        print(f"{g}: {n_elig} elegíveis, amostra {len(dates)} de {dates[0]} a {dates[-1]}")


if __name__ == "__main__":
    main()
