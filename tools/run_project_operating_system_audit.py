#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import audit_project_operating_system as audit

PLANNED_REFERENCE_PREFIX = "docs/superpowers/plans/"


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
    """Keep the long-lived audit aligned with the approved Batch 006 authority.

    Historical Batch 005 assertions remain in the source documents and legacy
    contracts. Only assertions that describe the *current* stage and scoped
    implementation gate are advanced here.
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
    ):
        if token not in gate_tokens:
            gate_tokens.append(token)
    assertions[gates_path] = tuple(gate_tokens)

    audit.REQUIRED_ASSERTIONS = assertions


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
