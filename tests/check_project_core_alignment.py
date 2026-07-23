#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


REQUIRED_TEXT = {
    "README.md": (
        "장비의 출생·성장·소유·사건 기록",
        "장비 한 점의 생애 PoC",
        "현재 구현",
        "확정 설계·다음 구현",
    ),
    "[기획서]/00_프로젝트_허브/START_HERE.md": (
        "장비의 출생·성장·소유·사건 기록",
        "CORE_CONFIRMED",
        "IMPLEMENTATION_NOT_STARTED",
        "장비 한 점의 생애 PoC",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "CORE_CONFIRMED / CORE_RECORDED",
        "SPEC_READY / IMPLEMENTATION_NOT_STARTED",
        "장비 한 점의 생애 PoC",
        "docs/MVP-003_SCOPE.md",
    ),
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (
        "2026-07-23-project-core-design.md",
        "2026-07-23-equipment-lifecycle-poc-integrated-spec.md",
        "2026-07-23-equipment-lifecycle-poc-implementation.md",
        "MVP-003_SCOPE.md",
    ),
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (
        "Project core confirmation",
        "Equipment lifecycle PoC specification",
        "Equipment lifecycle PoC implementation",
        "NOT_STARTED",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "장비 한 점의 생애 PoC — CURRENT",
        "docs/MVP-003_SCOPE.md",
        "구현 미시작",
    ),
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md": (
        "장비의 출생·성장·소유·사건 기록",
        "영구 완성도",
        "피로도",
        "세계 장비 기록",
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
        "IMPLEMENTATION_NOT_STARTED",
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
}

FORBIDDEN_TEXT = {
    "[기획서]/00_프로젝트_허브/DECISION_LOG.md": (
        "Base 기준 commit은 `ee265576da7f67d3278f8099dd97d4e714ef0651`",
        "상태: 범위 확정·실행 미착수",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "다음 제품 작업은 한 변수군 후보안 비교와 자동 반복·실제 플레이 검증이다",
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
