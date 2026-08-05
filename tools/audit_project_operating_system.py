#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

LOCAL_PREFIXES = (
    "AGENTS.md",
    "README.md",
    "project.godot",
    "docs/",
    "skills/",
    "tools/",
    "tests/",
    "data/",
    "scripts/",
    "scenes/",
    "schemas/",
    ".github/",
    "[기획서]/",
)
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BACKTICK = re.compile(r"`([^`\n]+)`")

ACTIVE_DOCS = (
    "README.md",
    "AGENTS.md",
    "CURRENT_CONFIRMED_DECISIONS.md",
    "docs/planning/CURRENT_R2_CANON_REGISTRY.json",
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md",
    "docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md",
    "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md",
    "[기획서]/00_프로젝트_허브/START_HERE.md",
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
    "[기획서]/00_프로젝트_허브/ROADMAP.md",
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md",
    "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json",
)

REQUIRED_ASSERTIONS = {
    "README.md": ("장비의 출생·성장·소유·사건 기록", "Godot AI"),
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
    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (
        '"schema_version":8',
        '"stage_status":"R2_BATCH_005_ACTIVE_0_OF_10"',
        '"next_approval_counter":"0/10"',
        '"planning_pr":103',
        '"closure_pr":104',
        '"canon_audit_pr":105',
        '"planning_pr":106',
        '"planning_merge_sha":"789c73f38003f40dde5e9a99cd7dcb3ca03863f7"',
        '"closure_pr":107',
        '"id":"R2_BATCH_004"',
        '"id":"R2_BATCH_005"',
        '"id":"BS-CRAFT-20260804-07"',
        '"id":"BS-CRAFT-20260805-01"',
        '"id":"BS-OPS-20260805-01"',
        '"domain":"NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM"',
        '"minimum":0',
        '"fixed_design_maximum":null',
        '"current_artistry_model":"NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM_NO_NAMED_TIERS"',
        '"historical_bounded_artistry_model":"INTEGER_1_TO_10_NO_NAMED_TIERS_SUPERSEDED"',
        '"five_grade_product_implementation":"NOT_STARTED_BLOCKED"',
        '"artistry_product_implementation":"NOT_STARTED_BLOCKED"',
        '"product_implementation":"BLOCKED"',
    ),
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (
        "[현재 정본]",
        "R2_BATCH_005_0_OF_10",
        "GRADE_AFFIX",
        "CATALYST_AFFIX",
        "CHRONICLE_AFFIX",
        "[보통] → [우수] → [명품] → [걸작] → [전설]",
        "예술성 27",
        "고정 설계 최대치 없음",
        "예술성 단계명 없음",
        "보조재료 슬롯 재도입 금지",
        "일반 수식어 A·B 구조 재도입 금지",
        "과거 3단계 구현 PASS를 현재 5단계 제품 구현 PASS로 해석 금지",
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
        "예술성 단계명 없음",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
        "전투 성능을 기본적으로 올리지 않는다",
    ),
    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": (
        "Diablo IV",
        "Path of Exile",
        "Dwarf Fortress",
        "예술성 27",
        "채택",
        "비채택",
    ),
    "[기획서]/00_프로젝트_허브/START_HERE.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "예술성 27",
        "고정 설계 최대치 없음",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2 체크포인트 004",
        "R2_BATCH_005_0_OF_10",
        "현재 승인 카운터: `0/10`",
        "MERGED_PR106",
        "예술성 27",
        "고정 설계 최대치 없음",
        "제품 구현: `BLOCKED`",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "PRODUCT_IMPLEMENTATION: BLOCKED",
    ),
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_ACTIVE_0_OF_10",
        "Three Affix Gate",
        "Benchmark Gate",
        "TDD Gate",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
        "CODEX_IMPLEMENTATION_GATE: BLOCKED",
    ),
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": (
        "R2_CHECKPOINT_004",
        "R2_BATCH_005_0_OF_10",
        "예술성 원수치 능력치",
    ),
    "project.godot": (
        "res://addons/godot_ai/plugin.cfg",
        "res://addons/godot_ai/runtime/game_helper.gd",
    ),
}

STALE_ACTIVE_ASSERTIONS = {
    "CURRENT_CONFIRMED_DECISIONS.md": (
        "APPROVED_PENDING_MERGE",
        "R2_BATCH_004 / 2/10",
        "예술성 7/10",
        "예술성 1~10",
    ),
    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (
        "R2_BATCH_004_ACTIVE_2_OF_10",
        "APPROVED_PENDING_MERGE",
        '"auxiliary_material_slot_exists":true',
    ),
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (
        "R2_BATCH_004_2_OF_10",
        "예술성 7/10",
        "예술성 1~10",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2_BATCH_004_2_OF_10",
        "현재 승인 카운터: `2/10`",
        "Draft PR 유지",
    ),
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


def add(
    findings: list[Finding],
    severity: str,
    code: str,
    message: str,
    path: Path | str | None = None,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            code=code,
            message=message,
            path=None if path is None else str(path),
        )
    )


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return value


def git_head(root: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def skill_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.glob("skills/**/SKILL.md"))


def audit_base(base_root: Path, profile: dict[str, Any], findings: list[Finding]) -> dict[str, Any]:
    if not base_root.is_dir():
        add(findings, "ERROR", "BASE_ROOT_MISSING", str(base_root))
        return {"active_skill_count": 0, "head": None}

    skills = skill_files(base_root)
    expected_commit = profile.get("base_commit")
    head = git_head(base_root)
    if expected_commit and head and head != expected_commit:
        add(
            findings,
            "WARNING",
            "BASE_HEAD_DIFFERS_FROM_PROFILE",
            f"profile={expected_commit} actual={head}",
        )

    capability_ids = {
        item.get("base_skill_id")
        for item in profile.get("capabilities", [])
        if isinstance(item, dict) and isinstance(item.get("base_skill_id"), str)
    }
    if not capability_ids:
        add(findings, "ERROR", "BASE_CAPABILITY_MAP_EMPTY", "profile has no capabilities")

    return {
        "active_skill_count": len(skills),
        "mapped_capability_count": len(capability_ids),
        "head": head,
    }


def local_reference_candidates(text: str) -> Iterable[str]:
    for match in MARKDOWN_LINK.finditer(text):
        yield match.group(1).strip()
    for match in BACKTICK.finditer(text):
        yield match.group(1).strip()


def normalize_local_reference(value: str) -> str | None:
    value = value.split("#", 1)[0].strip().strip(".,;:")
    if not value or value.startswith(("http://", "https://", "mailto:", "res://")):
        return None
    if any(token in value for token in ("*", "{", "}", "<", ">", "|", "$", " → ", " = ")):
        return None
    if " " in value and not value.startswith("[기획서]/"):
        return None
    if value.startswith(LOCAL_PREFIXES) or value.startswith(("../", "./")):
        return value
    return None


def audit_references(project_root: Path, findings: list[Finding]) -> int:
    checked = 0
    for relative in ACTIVE_DOCS:
        source = project_root / relative
        if not source.is_file() or source.suffix not in {".md", ".json"}:
            continue
        text = source.read_text(encoding="utf-8", errors="replace")
        for raw in local_reference_candidates(text):
            candidate = normalize_local_reference(raw)
            if candidate is None:
                continue
            checked += 1
            if candidate.startswith(LOCAL_PREFIXES):
                target = project_root / candidate
            else:
                target = source.parent / candidate
            if not target.exists():
                add(
                    findings,
                    "ERROR",
                    "BROKEN_LOCAL_REFERENCE",
                    f"{relative} -> {candidate}",
                    relative,
                )
    return checked


def audit_project(project_root: Path, profile: dict[str, Any], findings: list[Finding]) -> dict[str, Any]:
    required_entrypoints = profile.get("required_entrypoints", [])
    for relative in required_entrypoints:
        if isinstance(relative, str) and not (project_root / relative).exists():
            add(findings, "ERROR", "REQUIRED_ENTRYPOINT_MISSING", relative, relative)

    for relative, assertions in REQUIRED_ASSERTIONS.items():
        path = project_root / relative
        if not path.is_file():
            add(findings, "ERROR", "ACTIVE_DOCUMENT_MISSING", relative, relative)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for assertion in assertions:
            if assertion not in text:
                add(
                    findings,
                    "ERROR",
                    "REQUIRED_ASSERTION_MISSING",
                    f"Required current assertion {assertion!r} is missing",
                    relative,
                )

    for relative, stale_values in STALE_ACTIVE_ASSERTIONS.items():
        path = project_root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for stale in stale_values:
            if stale in text:
                add(
                    findings,
                    "ERROR",
                    "STALE_ACTIVE_ASSERTION",
                    f"Stale active assertion {stale!r} remains",
                    relative,
                )

    for relative in (
        "docs/planning/CURRENT_R2_CANON_REGISTRY.json",
        "docs/planning/CURRENT_R1_CANON_REGISTRY.json",
        "docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json",
        "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json",
    ):
        try:
            read_json(project_root / relative)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            add(findings, "ERROR", "INVALID_JSON", str(exc), relative)

    reference_count = audit_references(project_root, findings)
    project_skills = skill_files(project_root)
    expected_skill_count = profile.get("project_skill_count")
    if isinstance(expected_skill_count, int) and len(project_skills) != expected_skill_count:
        add(
            findings,
            "ERROR",
            "PROJECT_SKILL_COUNT_MISMATCH",
            f"expected={expected_skill_count} actual={len(project_skills)}",
        )

    return {
        "project_skill_count": len(project_skills),
        "required_entrypoint_count": len(required_entrypoints),
        "active_document_count": len(ACTIVE_DOCS),
        "local_reference_count": reference_count,
        "head": git_head(project_root),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Blacksmith project operating system")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--base-root", required=True)
    parser.add_argument("--profile", default="docs/BASE_ADOPTION_PROFILE.json")
    parser.add_argument("--report", default="artifacts/base-adoption-report.json")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    base_root = Path(args.base_root).resolve()
    findings: list[Finding] = []
    profile = read_json(project_root / args.profile)
    base_summary = audit_base(base_root, profile, findings)
    project_summary = audit_project(project_root, profile, findings)
    errors = [item for item in findings if item.severity == "ERROR"]
    report = {
        "status": "PASS" if not errors else "FAIL",
        "base": base_summary,
        "project": project_summary,
        "finding_counts": {
            "errors": len(errors),
            "warnings": len([item for item in findings if item.severity == "WARNING"]),
        },
        "findings": [asdict(item) for item in findings],
    }
    report_path = project_root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Base adoption audit {report['status']}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
