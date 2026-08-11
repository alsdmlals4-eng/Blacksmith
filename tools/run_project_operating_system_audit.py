#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import audit_project_operating_system as audit

PLANNED_REFERENCE_PREFIX = "docs/superpowers/plans/"
R3_REGISTRY = "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
R3_NADIA_CANON = "docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md"
R3_TOREN_CANON = "docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md"
R3_MAREK_CANON = "docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md"
R3_ERSA_CANON = "docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md"
R3_FIRST_DECISION = "BS-CONTENT-20260811-01"
R3_SECOND_DECISION = "BS-CONTENT-20260811-02"
R3_THIRD_DECISION = "BS-CONTENT-20260811-03"
R3_CURRENT_DECISION = "BS-CONTENT-20260811-04"


def classify_planned_references(findings: list[audit.Finding]) -> None:
    """Downgrade missing paths declared by implementation plans.

    Plans intentionally name files that do not exist until their task is executed.
    Every other missing local reference remains an ERROR.
    """
    for finding in findings:
        if (
            finding.severity == "ERROR"
            and finding.code == "BROKEN_LOCAL_REFERENCE"
            and finding.message.startswith(PLANNED_REFERENCE_PREFIX)
        ):
            finding.severity = "WARNING"
            finding.code = "PLANNED_PATH_NOT_YET_CREATED"


def configure_current_assertions() -> None:
    """Align the long-lived audit with current R2/Task2 evidence and R3 planning authority.

    R2/Task2 merge evidence remains historical/current-compatible authority. R3–R7 is
    a planning-only layer: it is current for design routing but does not open product
    or Task3 implementation. Earlier R3 decisions stay auditable as history while the
    current router advances with later user-approved planning decisions.
    """
    assertions = dict(audit.REQUIRED_ASSERTIONS)

    registry_path = "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
    registry_tokens = list(assertions[registry_path])
    replacements = {
        '"stage_status":"R2_CHECKPOINT_005_CLOSED_MAIN_CANON"':
            '"stage_status":"R2_BATCH_006_APPROVED_MAIN_CANON"',
        '"status":"NOT_STARTED"':
            '"status":"APPROVED_MERGED_PR120_MAIN_CANON"',
    }
    registry_tokens = [replacements.get(token, token) for token in registry_tokens]
    for token in (
        '"vertical_slice_implementation":"APPROVED"',
        '"implementation_scope":"VERTICAL_SLICE_NAMESPACES_ONLY"',
        '"planning_pr":120',
        '"planning_merge_sha":"a8a94343c78a68bf7bb14b411e7741f43b257138"',
    ):
        if token not in registry_tokens:
            registry_tokens.append(token)
    assertions[registry_path] = tuple(registry_tokens)

    assertions[R3_REGISTRY] = (
        '"stage_status": "R3_R7_DESIGN_ACTIVE"',
        '"product_implementation": "BLOCKED"',
        '"task3_implementation": "NOT_APPROVED"',
        '"next_approval_counter": "4/10"',
        f'"id": "{R3_FIRST_DECISION}"',
        f'"id": "{R3_SECOND_DECISION}"',
        f'"id": "{R3_THIRD_DECISION}"',
        f'"id": "{R3_CURRENT_DECISION}"',
        '"content_id": "COLLECTOR_01"',
        '"customer_id": "ERSA_ROEN"',
        '"activity_family": "EXHIBITION_EVIDENCE_AND_PROVENANCE"',
        '"same_item_uid_preserved": true',
        '"opaque_collector_or_exhibition_score": false',
    )
    assertions[R3_NADIA_CANON] = (
        R3_FIRST_DECISION,
        "ADVENTURER_01",
        "NADIA_VENN",
        "생환 + 회수",
        "같은 UID",
        "직접 전투·탐험 미니게임을 추가하지 않는다",
        "BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED",
        "제품 구현: `BLOCKED`",
        "Task3 구현: `NOT_APPROVED`",
    )
    assertions[R3_TOREN_CANON] = (
        R3_SECOND_DECISION,
        "ADVENTURER_02",
        "TOREN_MARCH",
        "JOURNEY_CONTINUITY_AND_RELIABILITY",
        "ENVIRONMENTAL_SEALING",
        "FIELD_SERVICEABILITY",
        "직접 이동·지도 경로 선택·실시간 생존 조작을 요구하지 않는다",
        "자동 매일 내구도 감소 금지",
        "BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED",
        "제품 구현: `BLOCKED`",
        "Task3 구현: `NOT_APPROVED`",
    )
    assertions[R3_MAREK_CANON] = (
        R3_THIRD_DECISION,
        "SOLDIER_01",
        "MAREK_OLDEN",
        "SMALL_LOT_STANDARD_ORDER",
        "ORDER_QUANTITY = 10",
        "PER_ITEM_UID_PRESERVED",
        "UNIT_MISSION_STATE",
        "STANDARD_ADOPTION_STATE",
        "BATCH_ITEM_LIFECYCLE_STATE",
        "제품 구현: `BLOCKED`",
        "Task3 구현: `NOT_APPROVED`",
    )
    assertions[R3_ERSA_CANON] = (
        R3_CURRENT_DECISION,
        "COLLECTOR_01",
        "ERSA_ROEN",
        "EXHIBITION_EVIDENCE_AND_PROVENANCE",
        "CRAFTSMANSHIP_EVIDENCE",
        "LIVED_HISTORY_EVIDENCE",
        "EXHIBITION_RECEPTION_STATE",
        "EXHIBIT_THESIS_FIT_STATE",
        "ITEM_UID_PUBLIC_LEGACY_STATE",
        "SAME_ITEM_UID_PRESERVED",
        "NO_CHRONICLE_COUNT_OPTIMIZATION",
        "제품 구현: `BLOCKED`",
        "Task3 구현: `NOT_APPROVED`",
    )

    gates_path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
    gate_tokens = list(assertions[gates_path])
    gate_tokens = [
        "GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED"
        if token == "CODEX_IMPLEMENTATION_GATE: BLOCKED"
        else token
        for token in gate_tokens
    ]
    for token in (
        "VERTICAL_SLICE_CODE_GATE: TASK2_MAIN_MERGED_NO_NEW_PRODUCT_SCOPE",
        "VERTICAL_SLICE_IMPLEMENTATION_APPROVED",
        "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED",
        "R3_R7_DESIGN_ACTIVE",
        "R3_R7_APPROVAL_COUNTER: 4/10",
        f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION}",
        R3_THIRD_DECISION,
        "TASK3_IMPLEMENTATION: NOT_APPROVED",
    ):
        if token not in gate_tokens:
            gate_tokens.append(token)
    assertions[gates_path] = tuple(gate_tokens)

    router_paths = (
        "[기획서]/00_프로젝트_허브/START_HERE.md",
        "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    )
    stale_router_tokens = {"예술성 27", "고정 설계 최대치 없음"}
    for path in router_paths:
        tokens = [
            token
            for token in assertions[path]
            if token not in stale_router_tokens
        ]
        if path.endswith("START_HERE.md"):
            tokens = [token for token in tokens if token != "R2_CHECKPOINT_005"]
        if path.endswith("ACTIVE_CONTEXT.md"):
            tokens = [
                token
                for token in tokens
                if token not in {"현재 승인 카운터: `0/10`", "제품 구현: `BLOCKED`"}
            ]
        for token in (
            "TASK2_MAIN_MERGED",
            "POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE",
            "PRODUCT_IMPLEMENTATION: BLOCKED",
            "R3_R7_DESIGN_ACTIVE",
            R3_FIRST_DECISION,
            R3_SECOND_DECISION,
            R3_THIRD_DECISION,
            R3_CURRENT_DECISION,
            f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION}",
            "COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED",
            "TASK3_IMPLEMENTATION: NOT_APPROVED",
        ):
            if token not in tokens:
                tokens.append(token)
        if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `4/10`" not in tokens:
            tokens.append("현재 R3–R7 승인 카운터: `4/10`")
        assertions[path] = tuple(tokens)

    audit.REQUIRED_ASSERTIONS = assertions
    current_docs = list(audit.ACTIVE_DOCS)
    for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON):
        if path not in current_docs:
            current_docs.append(path)
    audit.ACTIVE_DOCS = tuple(current_docs)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit Base adoption while distinguishing implementation-plan future paths"
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--base-root", required=True)
    parser.add_argument("--profile", default="docs/BASE_ADOPTION_PROFILE.json")
    parser.add_argument("--report", default="artifacts/base-adoption-report.json")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    base_root = Path(args.base_root).resolve()
    profile_path = (project_root / args.profile).resolve()
    report_path = (project_root / args.report).resolve()

    findings: list[audit.Finding] = []
    try:
        profile = audit.read_json(profile_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Base adoption audit FAILED: {exc}")
        return 1

    configure_current_assertions()
    try:
        base_summary = audit.audit_base(base_root, profile, findings)
        project_summary = audit.audit_project(project_root, profile, findings)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        audit.add(findings, "ERROR", "AUDIT_EXCEPTION", str(exc))
        base_summary = {}
        project_summary = {}

    classify_planned_references(findings)
    errors = [item for item in findings if item.severity == "ERROR"]
    warnings = [item for item in findings if item.severity == "WARNING"]
    report = {
        "status": "PASS" if not errors else "FAIL",
        "base": base_summary,
        "project": project_summary,
        "finding_counts": {"errors": len(errors), "warnings": len(warnings)},
        "findings": [asdict(item) for item in findings],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Base adoption audit {report['status']}")
    print(f"- Base active skills: {base_summary.get('active_skill_count', 'unknown')}")
    print(f"- Project skills: {project_summary.get('project_skill_count', 'unknown')}")
    print(f"- Errors: {len(errors)} / Warnings: {len(warnings)}")
    for item in findings:
        location = f" [{item.path}]" if item.path else ""
        print(f"- {item.severity} {item.code}{location}: {item.message}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())