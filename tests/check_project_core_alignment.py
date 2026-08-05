#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
R1 = ROOT / "docs/planning/CURRENT_R1_CANON_REGISTRY.json"
LEGACY = ROOT / "docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json"

REQUIRED_TEXT = {
    "AGENTS.md": (
        "벤치마킹·현업 비교",
        "최대 배치 크기",
        "조기 체크포인트",
        "RED → GREEN → REFACTOR",
    ),
    "CURRENT_CONFIRMED_DECISIONS.md": (
        "[현재 정본]",
        "R2_CHECKPOINT_004",
        "R2_BATCH_005 / 0/10",
        "MERGED_PR106",
        "7a46fa38586a42f268cd0432744203049649ddd5",
        "예술성 27",
        "고정 설계 최대치 없음",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "제품 구현: `BLOCKED`",
    ),
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (
        "[현재 정본]",
        "R2_BATCH_005_0_OF_10",
        "[보통] → [우수] → [명품] → [걸작] → [전설]",
        "예술성 27",
        "고정 설계 최대치 없음",
        "일반 수식어 A·B 구조 재도입 금지",
        "보조재료 슬롯 재도입 금지",
    ),
    "docs/planning/BLACKSMITH_R2_CHECKPOINT_004_POSTMERGE_CLOSURE_2026.md": (
        "CLOSURE_MERGED_PR107",
        "1ad791123eaf6c727e964380814ffb69f1357bbf",
        "7a46fa38586a42f268cd0432744203049649ddd5",
        "Planning-first `101`",
        "Base `579`",
        "PR validation `1170`",
        "R2_BATCH_005: ACTIVE / 0_OF_10",
        "제품 구현: `BLOCKED`",
    ),
    "docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md": (
        "BS-CRAFT-20260804-07",
        "MERGED_PR106",
        "CRAFT_FINE",
        "제작 후 등급 승격 금지",
    ),
    "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md": (
        "BS-CRAFT-20260805-01",
        "MERGED_PR106",
        "예술성 27",
        "고정 설계 최대치 없음",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2 체크포인트 004",
        "R2_BATCH_005_0_OF_10",
        "현재 승인 카운터: `0/10`",
        "7a46fa38586a42f268cd0432744203049649ddd5",
        "제품 구현: `BLOCKED`",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "첫 코어 버티컬 슬라이스",
        "PRODUCT_IMPLEMENTATION: BLOCKED",
    ),
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "7a46fa38586a42f268cd0432744203049649ddd5",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
        "CODEX_IMPLEMENTATION_GATE: BLOCKED",
    ),
    "[기획서]/00_프로젝트_허브/START_HERE.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "예술성 27",
    ),
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_0_OF_10",
        "예술성 원수치 능력치",
    ),
}

FORBIDDEN = {
    "CURRENT_CONFIRMED_DECISIONS.md": (
        "APPROVED_PENDING_MERGE",
        "R2_BATCH_004 / 2/10",
        "예술성 7/10",
        "예술성 1~10",
    ),
    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (
        "R2_BATCH_004_ACTIVE_2_OF_10",
        "PENDING_EXPECTED_HEAD_MERGE",
        "APPROVED_PENDING_MERGE",
        '"auxiliary_material_slot_exists":true',
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "현재 승인 카운터: `2/10`",
        "Draft PR 유지",
    ),
}


def load(path: Path, failures: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"cannot read JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"JSON root must be an object: {path.relative_to(ROOT)}")
        return {}
    return value


def check_text(failures: list[str]) -> None:
    for relative, tokens in REQUIRED_TEXT.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing required file: {relative}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in tokens:
            if token not in text:
                failures.append(f"{relative}: missing required token {token!r}")
    for relative, tokens in FORBIDDEN.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in tokens:
            if token in text:
                failures.append(f"{relative}: stale token remains {token!r}")


def check_r2(failures: list[str]) -> None:
    registry = load(R2, failures)
    if not registry:
        return
    expected = {
        "schema_version": 8,
        "stage_status": "R2_BATCH_005_ACTIVE_0_OF_10",
        "next_approval_counter": "0/10",
        "product_implementation": "BLOCKED",
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            failures.append(f"R2 registry {key!r} must equal {value!r}")

    cp3 = registry.get("immutable_merge_evidence", {}).get("checkpoint_003", {})
    for key, value in {
        "planning_pr": 103,
        "planning_merge_sha": "674ee21013cb5d41f89a1a3f3b10ecfc31238295",
        "closure_pr": 104,
        "closure_merge_sha": "d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9",
        "canon_audit_pr": 105,
        "canon_audit_merge_sha": "95f8fa33a645914578451af325afcaa32732c426",
    }.items():
        if cp3.get(key) != value:
            failures.append(f"checkpoint 003 {key!r} must equal {value!r}")

    cp4 = registry.get("immutable_merge_evidence", {}).get("checkpoint_004", {})
    for key, value in {
        "planning_pr": 106,
        "planning_exact_head": "227b2dabf0d98832811415156e72f65d601332a9",
        "planning_merge_sha": "789c73f38003f40dde5e9a99cd7dcb3ca03863f7",
        "closure_pr": 107,
        "closure_exact_head": "1ad791123eaf6c727e964380814ffb69f1357bbf",
        "closure_merge_sha": "7a46fa38586a42f268cd0432744203049649ddd5",
        "closure_status": "MERGED_MAIN_CANON",
        "merge_method": "SQUASH",
        "github_readback": "PASS",
        "sheet_readback": "PASS",
    }.items():
        if cp4.get(key) != value:
            failures.append(f"checkpoint 004 {key!r} must equal {value!r}")

    green = registry.get("tdd_evidence", {}).get("closure_green", {})
    for key, value in {
        "commit": "1ad791123eaf6c727e964380814ffb69f1357bbf",
        "planning_first_run": 101,
        "base_run": 579,
        "pr_validation_run": 1170,
        "status": "PASS",
    }.items():
        if green.get(key) != value:
            failures.append(f"closure GREEN {key!r} must equal {value!r}")

    closed = registry.get("closed_batch", {})
    if closed.get("id") != "R2_BATCH_004" or closed.get("counter") != "2/10":
        failures.append("closed batch must be R2_BATCH_004 at 2/10")
    if closed.get("decisions") != ["BS-CRAFT-20260804-07", "BS-CRAFT-20260805-01"]:
        failures.append("closed batch 004 decisions are incomplete")
    if closed.get("closure_reason") != "USER_APPROVED_EARLY_CHECKPOINT":
        failures.append("closed batch 004 reason is incorrect")

    active = registry.get("active_batch", {})
    if active.get("id") != "R2_BATCH_005" or active.get("counter") != "0/10":
        failures.append("active batch must be R2_BATCH_005 at 0/10")
    if active.get("approved_decisions") != 0 or active.get("decisions") != []:
        failures.append("active batch 005 must start empty")

    decisions = {
        item.get("id"): item
        for item in registry.get("current_decisions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    customer = decisions.get("BS-CUSTOMER-20260803-02", {}).get("contract", {})
    if customer.get("event_risk_scale") != "INTEGER_1_TO_10":
        failures.append("customer risk scale contract is missing")
    precision = decisions.get("BS-CRAFT-20260804-04", {}).get("contract", {})
    if precision.get("auxiliary_material_slot_exists") is not False:
        failures.append("auxiliary material slot must remain false")
    affix = decisions.get("BS-CRAFT-20260804-06", {}).get("contract", {})
    if affix.get("affix_slots") != ["GRADE_AFFIX", "CATALYST_AFFIX", "CHRONICLE_AFFIX"]:
        failures.append("three affix slots are incomplete")
    grade = decisions.get("BS-CRAFT-20260804-07", {}).get("contract", {})
    if grade.get("grade_count") != 5 or grade.get("post_craft_promotion_allowed") is not False:
        failures.append("five-tier immutable grade contract is incomplete")
    artistry = decisions.get("BS-CRAFT-20260805-01", {}).get("contract", {})
    if artistry.get("domain") != "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM":
        failures.append("unbounded artistry domain is missing")
    if artistry.get("minimum") != 0 or artistry.get("fixed_design_maximum") is not None:
        failures.append("artistry minimum or maximum is incorrect")
    if artistry.get("combat_power_by_default") is not False:
        failures.append("artistry must not increase combat by default")
    ops = decisions.get("BS-OPS-20260805-01", {}).get("contract", {})
    if ops.get("tdd_cycle") != ["RED", "GREEN", "REFACTOR"]:
        failures.append("TDD cycle is incomplete")

    alignment = registry.get("implementation_alignment", {})
    if alignment.get("historical_implemented_grade_model") != ["STANDARD", "GOOD", "PERFECT"]:
        failures.append("historical grade model is missing")
    if alignment.get("five_grade_product_implementation") != "NOT_STARTED_BLOCKED":
        failures.append("five-grade product implementation must remain blocked")
    if alignment.get("artistry_product_implementation") != "NOT_STARTED_BLOCKED":
        failures.append("artistry product implementation must remain blocked")
    if registry.get("legacy_reference_pull_request", {}).get("whole_pr_merge") != "REJECTED":
        failures.append("PR81 whole merge must remain rejected")


def check_historical(failures: list[str]) -> None:
    r1 = load(R1, failures)
    if r1 and r1.get("registry_status") != "HISTORICAL_R1_APPROVED_BASELINE_R2_REFINED":
        failures.append("R1 registry must remain historical")
    legacy = load(LEGACY, failures)
    if legacy:
        if legacy.get("schema_version") != 2:
            failures.append("legacy registry schema version must be 2")
        pr81 = next(
            (item for item in legacy.get("pull_requests", []) if isinstance(item, dict) and item.get("number") == 81),
            None,
        )
        if pr81 is None or pr81.get("merge_unit_status") != "REJECTED":
            failures.append("legacy registry must reject PR81")


def main() -> int:
    failures: list[str] = []
    check_text(failures)
    check_r2(failures)
    check_historical(failures)
    if failures:
        print("Project core alignment FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Project core alignment PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
