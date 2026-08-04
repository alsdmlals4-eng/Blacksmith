#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CURRENT_R2_REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CURRENT_R1_REGISTRY = ROOT / "docs/planning/CURRENT_R1_CANON_REGISTRY.json"
LEGACY_REGISTRY = ROOT / "docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json"

CURRENT_REQUIRED_TEXT = {
    "CURRENT_CONFIRMED_DECISIONS.md": (
        "[현재 정본]",
        "BS-OPS-20260804-02",
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
        "일반 수식어 A·B 구조 재도입 금지",
        "보조재료 슬롯 재도입 금지",
        "제품 구현: `BLOCKED`",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2_CHECKPOINT_003",
        "BS-OPS-20260804-02",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "전체 병합 단위: [폐기]",
        "다음 승인 카운터: `0/10`",
        "제품 구현: `BLOCKED`",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "R2_CHECKPOINT_003",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "일반 수식어 A·B 재도입 금지",
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
        "PR #81",
        "DO_NOT_MERGE_AS_UNIT",
    ),
    "docs/planning/BLACKSMITH_CANON_ADVERSARIAL_REVIEW_AND_LEGACY_STATUS_2026-08-04.md": (
        "BS-ADV-20260804-01",
        "COMPLETED_WITH_OPEN_USER_DECISIONS",
        "CORE_FUN_DIRECTION: VALID",
        "P0: 0",
        "P1_DOCUMENT_AUTHORITY_RESOLVED: 6",
        "P1_USER_DECISION_OPEN: 1",
    ),
    "docs/MVP-003_SCOPE.md": (
        "[역사 증거] [보류]",
        "NOT_CURRENT_PRODUCT_SCOPE / HOLD",
        "최신 제품 PASS를 의미하지 않습니다",
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

HISTORICAL_REQUIRED_TEXT = {
    "README.md": (
        "장비의 출생·성장·소유·사건 기록",
        "장비 한 점의 생애 PoC",
        "docs/CI_EXECUTION_POLICY.md",
    ),
    "docs/MVP-003_IMPLEMENTATION_STATUS.md": (
        "IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING",
        "PR validation #468",
        "test_equipment_lifecycle_poc.gd",
        "ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED",
    ),
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (
        "2026-07-23-equipment-lifecycle-poc-integrated-spec.md",
        "2026-07-23-equipment-lifecycle-poc-implementation.md",
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
        '"general_affix_slots": 2',
        '"auxiliary_material_slot_exists": true',
    ),
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (
        "일반 수식어 A·B가 현재 수식어",
        "보조재료 슬롯이 존재",
    ),
}

EXPECTED_LEGACY_MARKERS = {
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


def forbid_tokens(relative: str, tokens: tuple[str, ...], failures: list[str]) -> None:
    path = ROOT / relative
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    for token in tokens:
        if token in text:
            failures.append(f"{relative}: stale active statement remains {token!r}")


def validate_r2_registry(failures: list[str]) -> None:
    registry = load_json(CURRENT_R2_REGISTRY, failures)
    if not registry:
        return

    if registry.get("schema_version") != 6:
        failures.append("CURRENT_R2_CANON_REGISTRY.json: schema_version must be 6")
    if "R2_CHECKPOINT_003_CANON" not in str(registry.get("stage_status")):
        failures.append("CURRENT_R2_CANON_REGISTRY.json: checkpoint 003 must be current canon")
    if registry.get("product_implementation") != "BLOCKED":
        failures.append("CURRENT_R2_CANON_REGISTRY.json: product implementation must remain BLOCKED")
    if registry.get("next_approval_counter") != "0/10":
        failures.append("CURRENT_R2_CANON_REGISTRY.json: next approval counter must be 0/10")

    evidence = registry.get("immutable_merge_evidence", {}).get("checkpoint_003", {})
    expected_evidence = {
        "planning_pr": 103,
        "planning_merge_sha": "674ee21013cb5d41f89a1a3f3b10ecfc31238295",
        "closure_pr": 104,
        "closure_merge_sha": "d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9",
        "github_readback": "PASS",
        "sheet_readback": "PASS",
    }
    for key, expected in expected_evidence.items():
        if evidence.get(key) != expected:
            failures.append(f"CURRENT_R2_CANON_REGISTRY.json: checkpoint evidence {key!r} must equal {expected!r}")

    decisions = {
        item.get("id"): item
        for item in registry.get("current_decisions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    affix = decisions.get("BS-CRAFT-20260804-06", {}).get("contract", {})
    if affix.get("affix_slots") != ["GRADE_AFFIX", "CATALYST_AFFIX", "CHRONICLE_AFFIX"]:
        failures.append("CURRENT_R2_CANON_REGISTRY.json: current affix slots must be grade/catalyst/chronicle")
    if affix.get("affix_slot_count") != 3:
        failures.append("CURRENT_R2_CANON_REGISTRY.json: affix slot count must be 3")

    precision = decisions.get("BS-CRAFT-20260804-04", {}).get("contract", {})
    if precision.get("auxiliary_material_slot_exists") is not False:
        failures.append("CURRENT_R2_CANON_REGISTRY.json: auxiliary material slot must be false")

    pr81 = registry.get("legacy_reference_pull_request", {})
    if pr81.get("whole_pr_merge") != "REJECTED":
        failures.append("CURRENT_R2_CANON_REGISTRY.json: PR81 whole merge must be REJECTED")


def validate_r1_registry(failures: list[str]) -> None:
    registry = load_json(CURRENT_R1_REGISTRY, failures)
    if not registry:
        return
    if registry.get("registry_status") != "HISTORICAL_R1_APPROVED_BASELINE_R2_REFINED":
        failures.append("CURRENT_R1_CANON_REGISTRY.json: R1 registry must be historical and R2 refined")
    historical = registry.get("historical_core_contract", {})
    if historical.get("general_affix_slots_status") != "SUPERSEDED_BY_EXACTLY_THREE_GRADE_CATALYST_CHRONICLE_SLOTS":
        failures.append("CURRENT_R1_CANON_REGISTRY.json: historical two-slot structure must be explicitly superseded")


def validate_legacy_registry(failures: list[str]) -> None:
    registry = load_json(LEGACY_REGISTRY, failures)
    if not registry:
        return

    for item in registry.get("documents", []):
        if not isinstance(item, dict):
            failures.append("legacy registry contains a non-object document entry")
            continue
        relative = item.get("path")
        status = item.get("status")
        if not isinstance(relative, str) or not isinstance(status, str):
            failures.append("legacy registry document entry requires path and status strings")
            continue
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"legacy registry points to missing file: {relative}")
            continue
        marker = EXPECTED_LEGACY_MARKERS.get(status)
        if marker and marker not in path.read_text(encoding="utf-8", errors="replace"):
            failures.append(f"{relative}: status {status!r} requires visible marker {marker!r}")

    pr_entries = [item for item in registry.get("pull_requests", []) if isinstance(item, dict)]
    pr81 = next((item for item in pr_entries if item.get("number") == 81), None)
    if pr81 is None:
        failures.append("legacy registry must include PR81")
    else:
        if pr81.get("merge_unit_status") != "REJECTED":
            failures.append("legacy registry: PR81 merge_unit_status must be REJECTED")
        if pr81.get("selective_promotion_status") != "HOLD":
            failures.append("legacy registry: PR81 selective promotion must be HOLD")


def validate_design_registry(failures: list[str]) -> None:
    registry_path = ROOT / "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    registry = load_json(registry_path, failures)
    if not registry:
        return
    ids = {item.get("document_id") for item in registry.get("documents", []) if isinstance(item, dict)}
    for required_id in (
        "project-core-contract",
        "equipment-lifecycle-poc-integrated-spec",
        "equipment-lifecycle-poc-implementation-plan",
        "mvp-003-equipment-lifecycle-scope",
        "final-adversarial-review-report",
    ):
        if required_id not in ids:
            failures.append(f"design registry missing document_id {required_id!r}")


def main() -> int:
    failures: list[str] = []

    for relative, tokens in CURRENT_REQUIRED_TEXT.items():
        require_tokens(relative, tokens, failures)
    for relative, tokens in HISTORICAL_REQUIRED_TEXT.items():
        require_tokens(relative, tokens, failures)
    for relative, tokens in FORBIDDEN_ACTIVE_TEXT.items():
        forbid_tokens(relative, tokens, failures)

    validate_r2_registry(failures)
    validate_r1_registry(failures)
    validate_legacy_registry(failures)
    validate_design_registry(failures)

    if failures:
        print("Project core alignment FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Project core alignment PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
