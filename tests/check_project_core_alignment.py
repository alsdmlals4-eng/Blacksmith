#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
R2_REGISTRY_PATH = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
R1_REGISTRY_PATH = ROOT / "docs/planning/CURRENT_R1_CANON_REGISTRY.json"
LEGACY_REGISTRY_PATH = ROOT / "docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json"

REQUIRED_TEXT = {
    "AGENTS.md": (
        "벤치마킹·현업 비교",
        "최대 배치 크기",
        "조기 체크포인트",
        "작업마다 TDD",
        "RED → GREEN → REFACTOR",
    ),
    "CURRENT_CONFIRMED_DECISIONS.md": (
        "[현재 정본]",
        "R2_CHECKPOINT_004",
        "R2_BATCH_005 / 0/10",
        "BS-CRAFT-20260804-07",
        "BS-CRAFT-20260805-01",
        "MERGED_PR106",
        "789c73f38003f40dde5e9a99cd7dcb3ca03863f7",
        "예술성 27",
        "고정 설계 최대치 없음",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
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
    "docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md": (
        "BS-CRAFT-20260804-07",
        "CRAFT_FINE",
        "[보통] → [우수] → [명품] → [걸작] → [전설]",
        "제작 후 등급 승격 금지",
        "제품 구현: `BLOCKED`",
    ),
    "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md": (
        "BS-CRAFT-20260805-01",
        "예술성 27",
        "고정 설계 최대치 없음",
        "예술성 단계명 없음",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
        "전투 성능을 기본적으로 올리지 않는다",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2 체크포인트 004",
        "R2_BATCH_005_0_OF_10",
        "현재 승인 카운터: `0/10`",
        "MERGED_PR106",
        "789c73f38003f40dde5e9a99cd7dcb3ca03863f7",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "제품 구현: `BLOCKED`",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "첫 코어 버티컬 슬라이스",
        "PRODUCT_IMPLEMENTATION: BLOCKED",
    ),
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "Three Affix Gate",
        "Precision Enhancement Gate",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
        "CODEX_IMPLEMENTATION_GATE: BLOCKED",
    ),
    "[기획서]/00_프로젝트_허브/START_HERE.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "예술성 27",
        "고정 설계 최대치 없음",
    ),
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_0_OF_10",
        "예술성 원수치 능력치",
        "고정 설계 최대치 없음",
    ),
    "docs/CI_EXECUTION_POLICY.md": (
        "ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED",
        "문서 전용 PR",
        "코드·데이터·테스트·Workflow 변경 PR",
    ),
}

FORBIDDEN_ACTIVE_TEXT = {
    "CURRENT_CONFIRMED_DECISIONS.md": (
        "APPROVED_PENDING_MERGE",
        "R2_BATCH_004 / 2/10",
        "예술성 1~10",
        "예술성 7/10",
    ),
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (
        "R2_BATCH_004_2_OF_10",
        "예술성 1~10",
        "예술성 7/10",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2_BATCH_004_2_OF_10",
        "현재 승인 카운터: `2/10`",
        "Draft PR 유지",
    ),
    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (
        '"current_main"',
        "R2_BATCH_004_ACTIVE_2_OF_10",
        "APPROVED_PENDING_MERGE",
        '"auxiliary_material_slot_exists":true',
    ),
}


def load_json(path: Path, failures: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"cannot read JSON {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"JSON root must be object: {path.relative_to(ROOT)}")
        return {}
    return value


def validate_text(failures: list[str]) -> None:
    for relative, tokens in REQUIRED_TEXT.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing required file: {relative}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in tokens:
            if token not in text:
                failures.append(f"{relative}: missing required token {token!r}")

    for relative, tokens in FORBIDDEN_ACTIVE_TEXT.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in tokens:
            if token in text:
                failures.append(f"{relative}: stale active statement remains {token!r}")


def validate_r2(failures: list[str]) -> None:
    registry = load_json(R2_REGISTRY_PATH, failures)
    if not registry:
        return

    expected_scalars = {
        "schema_version": 8,
        "stage_status": "R2_BATCH_005_ACTIVE_0_OF_10",
        "product_implementation": "BLOCKED",
        "next_approval_counter": "0/10",
    }
    for key, expected in expected_scalars.items():
        if registry.get(key) != expected:
            failures.append(f"R2 registry {key!r} must equal {expected!r}")

    evidence = registry.get("immutable_merge_evidence", {})
    checkpoint_003 = evidence.get("checkpoint_003", {})
    for key, expected in {
        "planning_pr": 103,
        "planning_merge_sha": "674ee21013cb5d41f89a1a3f3b10ecfc31238295",
        "closure_pr": 104,
        "closure_merge_sha": "d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9",
        "canon_audit_pr": 105,
        "canon_audit_merge_sha": "95f8fa33a645914578451af325afcaa32732c426",
        "github_readback": "PASS",
        "sheet_readback": "PASS",
    }.items():
        if checkpoint_003.get(key) != expected:
            failures.append(f"checkpoint 003 evidence {key!r} must equal {expected!r}")

    checkpoint_004 = evidence.get("checkpoint_004", {})
    for key, expected in {
        "planning_pr": 106,
        "planning_exact_head": "227b2dabf0d98832811415156e72f65d601332a9",
        "planning_merge_sha": "789c73f38003f40dde5e9a99cd7dcb3ca03863f7",
        "merge_method": "SQUASH",
        "github_readback": "PASS",
        "sheet_readback": "PASS",
        "closure_status": "PENDING_EXPECTED_HEAD_MERGE",
    }.items():
        if checkpoint_004.get(key) != expected:
            failures.append(f"checkpoint 004 evidence {key!r} must equal {expected!r}")

    closed = registry.get("closed_batch", {})
    if closed.get("id") != "R2_BATCH_004" or closed.get("counter") != "2/10":
        failures.append("closed batch must be R2_BATCH_004 at 2/10")
    if closed.get("decisions") != ["BS-CRAFT-20260804-07", "BS-CRAFT-20260805-01"]:
        failures.append("closed batch 004 decision list is incomplete")
    if closed.get("closure_reason") != "USER_APPROVED_EARLY_CHECKPOINT":
        failures.append("closed batch 004 must record the approved early checkpoint")

    active = registry.get("active_batch", {})
    if active.get("id") != "R2_BATCH_005" or active.get("counter") != "0/10":
        failures.append("active batch must be R2_BATCH_005 at 0/10")
    if active.get("approved_decisions") != 0 or active.get("decisions") != []:
        failures.append("active batch 005 must start empty")
    if active.get("maximum_size") != 10:
        failures.append("active batch maximum size must remain 10")

    decisions = {
        item.get("id"): item
        for item in registry.get("current_decisions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    world = decisions.get("BS-WORLD-20260803-03", {}).get("contract", {})
    if world.get("personal_schedule_activation") != "CUSTOMER_VISIT_PLUS_SALE_OR_DELIVERY":
        failures.append("world/customer schedule contract is missing")

    customer = decisions.get("BS-CUSTOMER-20260803-02", {}).get("contract", {})
    if customer.get("event_risk_scale") != "INTEGER_1_TO_10":
        failures.append("customer risk scale must remain integer 1-10")

    precision = decisions.get("BS-CRAFT-20260804-04", {}).get("contract", {})
    if precision.get("auxiliary_material_slot_exists") is not False:
        failures.append("auxiliary material slot must remain false")

    affix = decisions.get("BS-CRAFT-20260804-06", {}).get("contract", {})
    if affix.get("affix_slots") != ["GRADE_AFFIX", "CATALYST_AFFIX", "CHRONICLE_AFFIX"]:
        failures.append("current affix slots must remain grade/catalyst/chronicle")
    if affix.get("cross_slot_overwrite_allowed") is not False:
        failures.append("cross-slot overwrite must remain false")

    grade_decision = decisions.get("BS-CRAFT-20260804-07", {})
    if grade_decision.get("status") != "USER_APPROVED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON":
        failures.append("five-tier crafting grade status must be merged PR106 main canon")
    grade = grade_decision.get("contract", {})
    if grade.get("grade_ids") != [
        "CRAFT_NORMAL",
        "CRAFT_SUPERIOR",
        "CRAFT_FINE",
        "CRAFT_MASTERWORK",
        "CRAFT_LEGENDARY",
    ]:
        failures.append("five-tier crafting grade IDs are incomplete")
    if grade.get("post_craft_promotion_allowed") is not False:
        failures.append("post-craft grade promotion must remain false")

    artistry_decision = decisions.get("BS-CRAFT-20260805-01", {})
    if artistry_decision.get("status") != "USER_APPROVED_REFINED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON":
        failures.append("artistry status must be merged PR106 main canon")
    artistry = artistry_decision.get("contract", {})
    if artistry.get("domain") != "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM":
        failures.append("artistry must use the approved unbounded domain")
    if artistry.get("minimum") != 0 or artistry.get("fixed_design_maximum") is not None:
        failures.append("artistry must have minimum zero and no fixed design maximum")
    for key in (
        "decimals_allowed",
        "denominator_display_allowed",
        "named_tiers_exist",
        "technical_storage_limit_is_content_maximum",
        "grade_sets_fixed_artistry_maximum",
        "zero_means_incomplete_or_unusable",
        "combat_power_by_default",
        "universal_affix_multiplier",
    ):
        if artistry.get(key) is not False:
            failures.append(f"artistry guard {key!r} must remain false")

    ops = decisions.get("BS-OPS-20260805-01", {}).get("contract", {})
    if ops.get("maximum_approved_decisions_per_batch") != 10:
        failures.append("maximum approved decisions per batch must remain 10")
    if ops.get("tdd_cycle") != ["RED", "GREEN", "REFACTOR"]:
        failures.append("TDD cycle must remain RED/GREEN/REFACTOR")

    alignment = registry.get("implementation_alignment", {})
    if alignment.get("historical_implemented_grade_model") != ["STANDARD", "GOOD", "PERFECT"]:
        failures.append("historical grade model must remain separately recorded")
    if alignment.get("five_grade_product_implementation") != "NOT_STARTED_BLOCKED":
        failures.append("five-grade product implementation must remain blocked")
    if alignment.get("artistry_product_implementation") != "NOT_STARTED_BLOCKED":
        failures.append("artistry product implementation must remain blocked")

    if registry.get("legacy_reference_pull_request", {}).get("whole_pr_merge") != "REJECTED":
        failures.append("PR81 whole merge must remain rejected")


def validate_historical_registries(failures: list[str]) -> None:
    r1 = load_json(R1_REGISTRY_PATH, failures)
    if r1 and r1.get("registry_status") != "HISTORICAL_R1_APPROVED_BASELINE_R2_REFINED":
        failures.append("R1 registry must remain historical and R2 refined")

    legacy = load_json(LEGACY_REGISTRY_PATH, failures)
    if legacy:
        if legacy.get("schema_version") != 2:
            failures.append("legacy registry schema version must remain 2")
        pr81 = next(
            (item for item in legacy.get("pull_requests", []) if isinstance(item, dict) and item.get("number") == 81),
            None,
        )
        if pr81 is None or pr81.get("merge_unit_status") != "REJECTED":
            failures.append("legacy registry must reject PR81 as a merge unit")


def main() -> int:
    failures: list[str] = []
    validate_text(failures)
    validate_r2(failures)
    validate_historical_registries(failures)

    if failures:
        print("Project core alignment FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Project core alignment PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
