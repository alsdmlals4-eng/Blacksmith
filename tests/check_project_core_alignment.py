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
        "BS-OPS-20260804-02",
        "BS-OPS-20260805-01",
        "BS-CRAFT-20260804-07",
        "BS-CRAFT-20260805-01",
        "[보통] → [우수] → [명품] → [걸작] → [전설]",
        "예술성 1~10",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "PR #81 전체 병합 단위는 `[폐기]`",
        "제품 구현: `BLOCKED`",
    ),
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (
        "[현재 정본]",
        "R2_BATCH_004_2_OF_10",
        "[보통] → [우수] → [명품] → [걸작] → [전설]",
        "예술성 단계명 없음",
        "일반 수식어 A·B 구조 재도입 금지",
        "보조재료 슬롯 재도입 금지",
        "과거 3단계 구현 PASS를 현재 5단계 제품 구현 PASS로 해석 금지",
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
        "예술성 7/10",
        "단계명 없음",
        "전투 성능을 기본적으로 올리지 않는다",
    ),
    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": (
        "Diablo IV",
        "Dwarf Fortress",
        "채택",
        "비채택",
        "Differentiation",
    ),
    "docs/planning/BLACKSMITH_R2_FOUR_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md": (
        "[대체됨]",
        "[보통] → [우수] → [걸작] → [전설]",
        "BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2 체크포인트 003",
        "BS-OPS-20260804-02",
        "R2_BATCH_004_2_OF_10",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "전체 병합 단위: [폐기]",
        "현재 승인 카운터: `2/10`",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "R2_CHECKPOINT_003",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "일반 수식어 A·B 재도입",
        "첫 코어 버티컬 슬라이스",
        "행동 증거",
        "PRODUCT_IMPLEMENTATION: BLOCKED",
    ),
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (
        "Three Affix Gate",
        "Precision Enhancement Gate",
        "Equipment Name·Chronicle Detail Gate",
        "Core Fun Validation Gate",
        "Legacy Document Gate",
        "CODEX_IMPLEMENTATION_GATE: BLOCKED",
    ),
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md": (
        "[부분 대체됨]",
        "현재 구현·후속 기획의 직접 기준으로 사용하지 마십시오",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md",
    ),
    "docs/MVP-003_SCOPE.md": (
        "[역사 증거] [보류]",
        "NOT_CURRENT_PRODUCT_SCOPE / HOLD",
        "PASS를 의미하지 않습니다",
    ),
    "docs/CI_EXECUTION_POLICY.md": (
        "ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED",
        "문서 전용 PR",
        "코드·데이터·테스트·Workflow 변경 PR",
        "cancel-in-progress: true",
    ),
    ".github/workflows/data-validation.yml": (
        "pull_request:",
        "scope=docs",
        "scope=code",
        "cancel-in-progress: true",
    ),
    ".github/workflows/godot-validation.yml": (
        "workflow_call:",
        "equipment_lifecycle_poc.tscn",
        "test_equipment_lifecycle_poc.gd",
        "cancel-in-progress: true",
    ),
}

FORBIDDEN_ACTIVE_TEXT = {
    "CURRENT_CONFIRMED_DECISIONS.md": (
        "R2_CHECKPOINT_003_PENDING_MERGE",
        "PENDING_POSTMERGE_CLOSURE_PR104",
    ),
    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (
        '"current_main"',
        "PENDING_POSTMERGE_CLOSURE_PR104",
        '"auxiliary_material_slot_exists":true',
    ),
}

EXPECTED_MARKERS = {
    "SUPERSEDED": "[대체됨]",
    "PARTIALLY_SUPERSEDED": "[부분 대체됨]",
    "HISTORICAL_EVIDENCE": "[역사 증거]",
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


def require_tokens(relative: str, tokens: tuple[str, ...], failures: list[str]) -> None:
    path = ROOT / relative
    if not path.is_file():
        failures.append(f"missing required file: {relative}")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    for token in tokens:
        if token not in text:
            failures.append(f"{relative}: missing required token {token!r}")


def validate_r2(failures: list[str]) -> None:
    registry = load_json(R2_REGISTRY_PATH, failures)
    if not registry:
        return
    if registry.get("schema_version") != 8:
        failures.append("R2 registry schema_version must be 8")
    if registry.get("stage_status") != "R2_BATCH_004_ACTIVE_2_OF_10":
        failures.append("R2 registry must identify batch 004 at 2/10")
    if registry.get("product_implementation") != "BLOCKED":
        failures.append("product implementation must remain BLOCKED")
    if registry.get("next_approval_counter") != "2/10":
        failures.append("next approval counter must be 2/10")

    evidence = registry.get("immutable_merge_evidence", {}).get("checkpoint_003", {})
    expected = {
        "planning_pr": 103,
        "planning_merge_sha": "674ee21013cb5d41f89a1a3f3b10ecfc31238295",
        "closure_pr": 104,
        "closure_merge_sha": "d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9",
        "canon_audit_pr": 105,
        "canon_audit_merge_sha": "95f8fa33a645914578451af325afcaa32732c426",
        "github_readback": "PASS",
        "sheet_readback": "PASS",
    }
    for key, value in expected.items():
        if evidence.get(key) != value:
            failures.append(f"checkpoint evidence {key!r} must equal {value!r}")

    decisions = {
        item.get("id"): item
        for item in registry.get("current_decisions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    affix = decisions.get("BS-CRAFT-20260804-06", {}).get("contract", {})
    if affix.get("affix_slots") != ["GRADE_AFFIX", "CATALYST_AFFIX", "CHRONICLE_AFFIX"]:
        failures.append("current affix slots must be grade/catalyst/chronicle")

    grade = decisions.get("BS-CRAFT-20260804-07", {}).get("contract", {})
    if grade.get("grade_count") != 5:
        failures.append("current crafting grade count must be 5")
    if grade.get("grade_ids") != [
        "CRAFT_NORMAL",
        "CRAFT_SUPERIOR",
        "CRAFT_FINE",
        "CRAFT_MASTERWORK",
        "CRAFT_LEGENDARY",
    ]:
        failures.append("current crafting grade IDs must match five-tier model")
    if grade.get("korean_labels") != ["보통", "우수", "명품", "걸작", "전설"]:
        failures.append("current Korean grade labels must be 보통/우수/명품/걸작/전설")
    if grade.get("post_craft_promotion_allowed") is not False:
        failures.append("post-craft grade promotion must be false")

    artistry = decisions.get("BS-CRAFT-20260805-01", {}).get("contract", {})
    if artistry.get("stat_role") != "WEAPON_ITEM_STAT":
        failures.append("artistry must be a weapon item stat")
    if artistry.get("scale") != "INTEGER_1_TO_10" or artistry.get("named_tiers_exist") is not False:
        failures.append("artistry must be integer 1-10 without named tiers")
    if artistry.get("combat_power_by_default") is not False:
        failures.append("artistry must not increase combat by default")

    ops = decisions.get("BS-OPS-20260805-01", {}).get("contract", {})
    if ops.get("maximum_approved_decisions_per_batch") != 10:
        failures.append("maximum approved decision batch size must be 10")
    if ops.get("early_checkpoint_triggers") != [
        "HIGH_RISK_CONFLICT",
        "SESSION_END",
        "LARGE_CANON_IMPACT",
    ]:
        failures.append("early checkpoint triggers are incomplete")
    if ops.get("tdd_cycle") != ["RED", "GREEN", "REFACTOR"]:
        failures.append("TDD cycle must be RED/GREEN/REFACTOR")

    alignment = registry.get("implementation_alignment", {})
    if alignment.get("historical_implemented_grade_model") != ["STANDARD", "GOOD", "PERFECT"]:
        failures.append("historical grade model must remain separately recorded")
    if alignment.get("five_grade_product_implementation") != "NOT_STARTED_BLOCKED":
        failures.append("five-grade implementation must remain blocked")

    batch = registry.get("active_batch", {})
    if batch.get("counter") != "2/10" or batch.get("maximum_size") != 10:
        failures.append("active batch must be 2/10 with maximum size 10")

    precision = decisions.get("BS-CRAFT-20260804-04", {}).get("contract", {})
    if precision.get("auxiliary_material_slot_exists") is not False:
        failures.append("auxiliary material slot must be false")
    pr81 = registry.get("legacy_reference_pull_request", {})
    if pr81.get("whole_pr_merge") != "REJECTED":
        failures.append("PR81 whole merge must be REJECTED")


def validate_r1(failures: list[str]) -> None:
    registry = load_json(R1_REGISTRY_PATH, failures)
    if not registry:
        return
    if registry.get("registry_status") != "HISTORICAL_R1_APPROVED_BASELINE_R2_REFINED":
        failures.append("R1 registry must be historical and R2 refined")


def validate_legacy(failures: list[str]) -> None:
    registry = load_json(LEGACY_REGISTRY_PATH, failures)
    if not registry:
        return
    for item in registry.get("documents", []):
        if not isinstance(item, dict):
            continue
        relative = item.get("path")
        status = item.get("status")
        if not isinstance(relative, str) or not isinstance(status, str):
            failures.append("legacy document requires path and status")
            continue
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"legacy registry points to missing file: {relative}")
            continue
        marker = EXPECTED_MARKERS.get(status)
        if marker and marker not in path.read_text(encoding="utf-8", errors="replace"):
            failures.append(f"{relative}: status {status!r} requires marker {marker!r}")

    pr81 = next(
        (item for item in registry.get("pull_requests", []) if isinstance(item, dict) and item.get("number") == 81),
        None,
    )
    if pr81 is None or pr81.get("merge_unit_status") != "REJECTED":
        failures.append("legacy registry must reject PR81 as merge unit")


def validate_design_registry(failures: list[str]) -> None:
    path = ROOT / "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    registry = load_json(path, failures)
    if not registry:
        return
    ids = {item.get("document_id") for item in registry.get("documents", []) if isinstance(item, dict)}
    for required in (
        "project-core-contract",
        "equipment-lifecycle-poc-integrated-spec",
        "equipment-lifecycle-poc-implementation-plan",
        "mvp-003-equipment-lifecycle-scope",
        "final-adversarial-review-report",
    ):
        if required not in ids:
            failures.append(f"design registry missing document_id {required!r}")


def main() -> int:
    failures: list[str] = []
    for relative, tokens in REQUIRED_TEXT.items():
        require_tokens(relative, tokens, failures)
    for relative, tokens in FORBIDDEN_ACTIVE_TEXT.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in tokens:
            if token in text:
                failures.append(f"{relative}: stale active statement remains {token!r}")

    validate_r2(failures)
    validate_r1(failures)
    validate_legacy(failures)
    validate_design_registry(failures)

    if failures:
        print("Project core alignment FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Project core alignment PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
