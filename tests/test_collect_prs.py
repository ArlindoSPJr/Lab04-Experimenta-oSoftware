import pytest

from scripts.collect_prs import classify_prs, pr_to_row, select_sample


def test_pr_nao_mergeado_e_ignorado():
    assert pr_to_row({"number": 1, "created_at": "2026-01-01T00:00:00Z", "merged_at": None}, "novato") is None
    row = pr_to_row({"number": 2, "created_at": "2026-01-01T00:00:00Z", "merged_at": "2026-01-01T12:30:00Z"}, "core")
    assert row["hours_to_merge"] == pytest.approx(12.5)


def _pr(n, login, assoc, day, kind="User", merged_by="maint"):
    return {"number": n, "user": {"login": login, "type": kind}, "author_association": assoc,
            "created_at": f"2026-01-{day:02d}T00:00:00Z", "merged_at": f"2026-01-{day:02d}T05:00:00Z",
            "merged_by": merged_by}


def test_classifica_segundo_regras_R4_a_R7():
    nao_mergeado = {**_pr(7, "leo", "CONTRIBUTOR", 8), "merged_at": None}
    prs = [_pr(3, "ana", "CONTRIBUTOR", 5),                  # R7: 2º PR da ana -> fora
           _pr(1, "ana", "CONTRIBUTOR", 1),                  # R6: 1º PR da ana -> novato
           _pr(2, "rui", "MEMBER", 2),                       # R5: core revisado por outro
           _pr(5, "rui", "MEMBER", 6, merged_by="rui"),      # R4.4: automerge -> fora
           _pr(6, "eva", "MEMBER", 7, merged_by=None),       # R4.4: merged_by nulo -> fora
           _pr(4, "dependabot[bot]", "NONE", 3, kind="Bot"), # R4.1: bot -> fora
           nao_mergeado,                                     # R4.3: fora, mas conta no histórico
           _pr(8, "leo", "CONTRIBUTOR", 9)]                  # 2º PR do leo -> fora (R6)
    got = {pr["number"]: g for pr, g in classify_prs(prs)}
    assert got == {1: "novato", 2: "core"}


def test_data_de_corte():
    assert classify_prs([_pr(1, "ana", "CONTRIBUTOR", 10)], cutoff="2026-01-05T00:00:00Z") == []


def test_amostra_pega_os_mais_recentes_por_grupo():
    cl = [(_pr(i, f"u{i}", "CONTRIBUTOR", i), "novato") for i in range(1, 6)]
    assert [p["number"] for p, _ in select_sample(cl, n=2)] == [5, 4]
