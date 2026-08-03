#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VALIDATED_STATUS = "IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING"
ACTIONS_STATUS = "ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED"

# Active authority documents validate the current merged R1 canon. Historical
# PoC evidence remains required in dedicated implementation records.
REQUIRED_TEXT = {
    "README.md": (
        "장비의 출생·성장·소유·사건 기록",
        "장비 한 점의 생애 PoC",
        VALIDATED_STATUS,
        "PR validation #468",
        "docs/CI_EXECUTION_POLICY.md",
    ),
    "[기획서]/00_프로젝트_허브/START_HERE.md": (
        "R1_STATUS: R1_CANON_ALIGNED / USER_FINAL_REVIEW_PENDING",
        "+10/+20/+30/+40/+50",
        "REFERENCE_IMPLEMENTATION / HISTORICAL_POC",
        "PRODUCT_IMPLEMENTATION: BLOCKED",
        "CANON_BASELINE_PR: 94",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "USER_FINAL_REVIEW_PENDING",
        "+10/+20/+30/+40/+50",
        "REFERENCE_IMPLEMENTATION / HISTORICAL_POC",
        "행동 증거",
        "MERGED_CANON_BASELINE",
    ),
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (
        "2026-07-23-project-core-design.md",
        "2026-07-23-equipment-lifecycle-poc-integrated-spec.md",
        "2026-07-23-equipment-lifecycle-poc-implementation.md",
        VALIDATED_STATUS,
        ACTIONS_STATUS,
    ),
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (
        "CORE_CONFLICT_DECISION_GATE: PASS",
        "Core Vertical Slice Gate",
        "Core Fun Validation Gate",
        "REFERENCE_IMPLEMENTATION",
        "MERGED_CANON_BASELINE",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "CANON_ALIGNED / USER_FINAL_REVIEW_PENDING",
        "첫 코어 버티컬 슬라이스",
        "행동 증거",
        "FUTURE_CONTENT_HOLD",
        "PR #94 병합 SHA",
    ),
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md": (
        "작품의 출생·성장·소유·손상·복원·사건 기록",
        "영구 완성도",
        "현재 검증 상한: `+50`",
        "활성 사건·연대기 수식어 1개",
        "회상 인터뷰",
    ),
    "[기획서]/00_프로젝트_허브/DECISION_LOG.md": (
        "DEC-023 프로젝트 코어 확정",
        "DEC-024 피로도·날짜 진행",
        "DEC-025 장비 생애 PoC",
        "41a20584dd2ee51d917e5c9d7cab6838e1ceba7e",
    ),
    "docs/BASE_ADOPTION_AUDIT.md": (
        "Data validation #389 PASS",
        "Base ACTIVE Skill: 25개 매핑 완료",
    ),
    "docs/MVP-003_SCOPE.md": (
        "장비 한 점의 생애 PoC",
        "+5",
        "+10",
        VALIDATED_STATUS,
        "PR validation #468",
        "REFERENCE_IMPLEMENTATION / HISTORICAL_POC",
        "E2E",
    ),
    "docs/MVP-003_IMPLEMENTATION_STATUS.md": (
        VALIDATED_STATUS,
        "PR validation #468",
        "test_equipment_lifecycle_poc.gd",
        ACTIONS_STATUS,
    ),
    "docs/CI_EXECUTION_POLICY.md": (
        ACTIONS_STATUS,
        "문서 전용 PR",
        "코드·데이터·테스트·Workflow 변경 PR",
        "cancel-in-progress: true",
    ),
    "docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md": (
        "PoC 임시 기준값",
        "미숙한 +5 철검",
        "DEFEAT",
        "상태 이름공간",
        "record_schema_version",
        "원자적 납품",
        "정밀 입력 대안",
    ),
    "docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md": (
        "자동 단조 호환",
        "record_schema_version",
        "상태 이름공간",
        "원자적 납품",
        "정밀 입력 대안",
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

FORBIDDEN_TEXT = {
    "README.md": (
        "GitHub Actions 자동 실행은 현재 비용 문제로 중지",
        "IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED",
    ),
    "[기획서]/00_프로젝트_허브/START_HERE.md": (
        "IMPLEMENTATION_NOT_STARTED",
        "IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED",
        "DEFERRED_UNTIL_ACTIONS_AVAILABLE",
        "#33 Draft, stacked",
        "CURRENT_AUTHORITY_PR",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "SPEC_READY / IMPLEMENTATION_NOT_STARTED",
        "IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED",
        "DEFERRED_UNTIL_ACTIONS_AVAILABLE",
        "agent/propose-project-core-contract",
        "CURRENT_AUTHORITY_REPAIR / DRAFT",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "구현 미시작",
        "IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED",
        "DEFERRED_UNTIL_ACTIONS_AVAILABLE",
        "CURRENT_DRAFT_PR",
    ),
    "docs/MVP-003_SCOPE.md": (
        "IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED",
        "제품 구현은 시작되지 않았다",
    ),
    "docs/MVP-003_IMPLEMENTATION_STATUS.md": (
        "IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED",
        "DEFERRED_UNTIL_ACTIONS_AVAILABLE",
    ),
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md": (
        "SPEC_READY / IMPLEMENTATION_NOT_STARTED",
        "IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED",
        "DEFERRED_UNTIL_ACTIONS_AVAILABLE",
    ),
    "[기획서]/00_프로젝트_허브/DECISION_LOG.md": (
        "Base 기준 commit은 `ee265576da7f67d3278f8099dd97d4e714ef0651`",
        "상태: 범위 확정·실행 미착수",
    ),
    ".github/workflows/data-validation.yml": (
        "ACTIONS_BUDGET_HOLD",
    ),
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []

    for relative, tokens in REQUIRED_TEXT.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing required file: {relative}", failures)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in tokens:
            if token not in text:
                fail(f"{relative}: missing current core token {token!r}", failures)

    for relative, tokens in FORBIDDEN_TEXT.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in tokens:
            if token in text:
                fail(f"{relative}: stale active statement remains {token!r}", failures)

    registry_path = ROOT / "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read design registry: {exc}", failures)
        registry = {}

    ids = {item.get("document_id") for item in registry.get("documents", []) if isinstance(item, dict)}
    for required_id in (
        "project-core-contract",
        "equipment-lifecycle-poc-integrated-spec",
        "equipment-lifecycle-poc-implementation-plan",
        "mvp-003-equipment-lifecycle-scope",
        "final-adversarial-review-report",
    ):
        if required_id not in ids:
            fail(f"design registry missing document_id {required_id!r}", failures)

    if failures:
        print("Project core alignment FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Project core alignment PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
