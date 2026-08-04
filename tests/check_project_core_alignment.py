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
    "CURRENT_CONFIRMED_DECISIONS.md": (
        "[현재 정본]",
        "BS-OPS-20260804-02",
        "BS-CRAFT-20260804-07",
        "[보통] → [우수] → [걸작] → [전설]",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "PR #81 전체 병합 단위는 `[폐기]`",
        "제품 구현: `BLOCKED`",
    ),
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (
        "[현재 정본]",
        "GRADE_AFFIX",
        "CATALYST_AFFIX",
        "CHRONICLE_AFFIX",
        "[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어",
        "[보통] → [우수] → [걸작] → [전설]",
        "일반 수식어 A·B 구조 재도입 금지",
        "보조재료 슬롯 재도입 금지",
        "과거 3단계 구현 PASS를 현재 4단계 제품 구현 PASS로 해석 금지",
    ),
    "docs/planning/BLACKSMITH_R2_FOUR_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md": (
        "BS-CRAFT-20260804-07",
        "R2_BATCH_004_1_OF_10",
        "CRAFT_NORMAL",
        "CRAFT_SUPERIOR",
        "CRAFT_MASTERWORK",
        "CRAFT_LEGENDARY",
        "제작 후 `걸작 → 전설` 승격 금지",
        "제품 구현: `BLOCKED`",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2 체크포인트 003",
        "BS-OPS-20260804-02",
        "BS-CRAFT-20260804-07",
        "R2_BATCH_004_1_OF_10",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "전체 병합 단위: [폐기]",
        "현재 승인 카운터: `1/10`",
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
    "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md": (
        "[현재 정본]",
        "CURRENT_R2_CANON_REGISTRY.json",
        "GRADE_AFFIX + CATALYST_AFFIX + CHRONICLE_AFFIX",
        "DO_NOT_MERGE_AS_UNIT",
    ),
    "docs/planning/BLACKSMITH_CANON_ADVERSARIAL_REVIEW_AND_LEGACY_STATUS_2026-08-04.md": (
        "BS-ADV-20260804-01",
        "CORE_FUN_DIRECTION: VALID",
        "P0: 0",
    ),
    "docs/MVP-003_SCOPE.md": (
        "[역사 증거] [보류]",
        "NOT_CURRENT_PRODUCT_SCOPE / HOLD",
        "PASS를 의미하지 않습니다",
    ),
    "docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md": (
        "[역사 증거] [보류]",
        "NO_IMPLEMENTATION_AUTHORITY",
        "제품 구현: `BLOCKED`",
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
        "baseline ID: `STANDARD / GOOD / PERFECT`",
    ),
    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (
        '"current_main"',
        "PENDING_POSTMERGE_CLOSURE_PR104",
        '"auxiliary_material_slot_exists": true',
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
        failures.append(f"JSON root must be an object: {path.relative_to(ROOT)}")
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
    if registry.get("schema_version") != 7:
        failures.append("R2 registry schema_version must be 7")
    if registry.get("stage_status") != "R2_BATCH_004_ACTIVE_1_OF_10":
        failures.append("R2 registry must identify batch 004 as active at 1/10")
    if registry.get("product_implementation") != "BLOCKED":
        failures.append("R2 registry product implementation must remain BLOCKED")
    if registry.get("next_approval_counter") != "1/10":
        failures.append("R2 registry next approval counter must be 1/10")

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
            failures.append(f"R2 checkpoint evidence {key!r} must equal {value!r}")

    decisions = {
        item.get("id"): item
        for item in registry.get("current_decisions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    affix = decisions.get("BS-CRAFT-20260804-06", {}).get("contract", {})
    if affix.get("affix_slot_count") != 3:
        failures.append("current affix slot count must be 3")
    if affix.get("affix_slots") != ["GRADE_AFFIX", "CATALYST_AFFIX", "CHRONICLE_AFFIX"]:
        failures.append("current affix slots must be grade/catalyst/chronicle")

    grade = decisions.get("BS-CRAFT-20260804-07", {}).get("contract", {})
    if grade.get("grade_count") != 4:
        failures.append("current crafting grade count must be 4")
    if grade.get("grade_ids") != [
        "CRAFT_NORMAL",
        "CRAFT_SUPERIOR",
        "CRAFT_MASTERWORK",
        "CRAFT_LEGENDARY",
    ]:
        failures.append("current crafting grade IDs must match the approved four-tier model")
    if grade.get("korean_labels") != ["보통", "우수", "걸작", "전설"]:
        failures.append("current Korean crafting grade labels must be 보통/우수/걸작/전설")
    if grade.get("post_craft_promotion_allowed") is not False:
        failures.append("post-craft grade promotion must be false")
    if grade.get("legendary_origin") != "EXTREMELY_RARE_FIRST_CRAFT_RESULT":
        failures.append("legendary grade must be an extremely rare first-craft result")

    alignment = registry.get("implementation_alignment", {})
    if alignment.get("historical_implemented_grade_model") != ["STANDARD", "GOOD", "PERFECT"]:
        failures.append("historical implemented grade model must remain separately recorded")
    if alignment.get("four_grade_product_implementation") != "NOT_STARTED_BLOCKED":
        failures.append("four-tier product implementation must remain blocked and not started")

    batch = registry.get("active_batch", {})
    if batch.get("id") != "R2_BATCH_004" or batch.get("counter") != "1/10":
        failures.append("active batch must be R2_BATCH_004 at 1/10")

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
    status = registry.get("historical_core_contract", {}).get("general_affix_slots_status")
    if status != "SUPERSEDED_BY_EXACTLY_THREE_GRADE_CATALYST_CHRONICLE_SLOTS":
        failures.append("historical two-slot contract must be explicitly superseded")


def validate_legacy(failures: list[str]) -> None:
    registry = load_json(LEGACY_REGISTRY_PATH, failures)
    if not registry:
        return
    if registry.get("schema_version") != 2:
        failures.append("legacy registry schema_version must be 2")
    for item in registry.get("documents", []):
        if not isinstance(item, dict):
            failures.append("legacy registry contains non-object document entry")
            continue
        relative = item.get("path")
        status = item.get("status")
        if not isinstance(relative, str) or not isinstance(status, str):
            failures.append("legacy document entry requires path and status")
            continue
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"legacy registry points to missing file: {relative}")
            continue
        marker = EXPECTED_MARKERS.get(status)
        if marker and marker not in path.read_text(encoding="utf-8", errors="replace"):
            failures.append(f"{relative}: status {status!r} requires visible marker {marker!r}")

    grade_history = registry.get("grade_model_history", [])
    current = next(
        (item for item in grade_history if isinstance(item, dict) and item.get("decision") == "BS-CRAFT-20260804-07"),
        None,
    )
    if current is None or current.get("status") != "CURRENT_CANON":
        failures.append("legacy registry must identify BS-CRAFT-20260804-07 as current grade canon")
    historical = next(
        (item for item in grade_history if isinstance(item, dict) and item.get("source") == "historical runtime and data"),
        None,
    )
    if historical is None or historical.get("status") != "HISTORICAL_EVIDENCE":
        failures.append("legacy registry must keep the three-tier runtime model as historical evidence")

    entries = [item for item in registry.get("pull_requests", []) if isinstance(item, dict)]
    pr81 = next((item for item in entries if item.get("number") == 81), None)
    if pr81 is None:
        failures.append("legacy registry must include PR81")
    else:
        if pr81.get("merge_unit_status") != "REJECTED":
            failures.append("legacy registry PR81 merge unit must be REJECTED")
        if pr81.get("selective_promotion_status") != "HOLD":
            failures.append("legacy registry PR81 selective promotion must be HOLD")


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
