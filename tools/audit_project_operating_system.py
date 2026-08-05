#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

TEXT_SUFFIXES = {".md", ".json", ".py", ".gd", ".tscn", ".yml", ".yaml", ".txt", ".toml"}
VENDORED_REFERENCE_ROOTS = ("addons/",)
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
BACKTICK = re.compile(r"`([^`\n]+)`")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ANCHOR = re.compile(r"#.*$")
FRONT_MATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
FRONT_FIELD = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):\s*(?P<value>.+?)\s*$", re.MULTILINE)

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
    "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json",
)

STALE_PATTERNS = {
    "legacy +5 milestone": re.compile(r"\+5[^\n]{0,80}(첫 수식어|수식어 판정|완료 후 새 철검)", re.IGNORECASE),
    "legacy current two-affix claim": re.compile(
        r"현재[^\n]{0,60}(일반 수식어 A.{0,20}일반 수식어 B|수식어 슬롯.{0,10}2개)",
        re.IGNORECASE,
    ),
    "legacy current auxiliary material claim": re.compile(
        r"현재[^\n]{0,60}보조재료 슬롯.{0,20}(존재|사용|필수)",
        re.IGNORECASE,
    ),
    "legacy universal day preset": re.compile(r"모든[^\n]{0,80}(3일 결과|4일 재방문)", re.IGNORECASE),
    "legacy optional precision enhancement": re.compile(r"정밀 강화\s*ON/OFF", re.IGNORECASE),
    "legacy current three-grade planning claim": re.compile(
        r"현재[^\n]{0,80}(baseline ID|제작 등급)[^\n]{0,40}STANDARD\s*/\s*GOOD\s*/\s*PERFECT",
        re.IGNORECASE,
    ),
    "legacy current four-grade planning claim": re.compile(
        r"현재[^\n]{0,80}\[보통\][^\n]{0,20}\[우수\][^\n]{0,20}\[걸작\][^\n]{0,20}\[전설\]",
        re.IGNORECASE,
    ),
    "named artistry tiers current": re.compile(
        r"현재[^\n]{0,80}(BASIC|REFINED)[^\n]{0,80}(MASTERWORK|MASTERPIECE)",
        re.IGNORECASE,
    ),
    "bounded artistry current": re.compile(
        r"현재[^\n]{0,100}예술성[^\n]{0,50}(1\s*~\s*10|\d+\s*/\s*10)",
        re.IGNORECASE,
    ),
    "fixed artistry maximum current": re.compile(
        r"현재[^\n]{0,100}예술성[^\n]{0,50}(10\s*=\s*최고|고정 최대치\s*10)",
        re.IGNORECASE,
    ),
}

REQUIRED_ASSERTIONS = {
    "README.md": (
        "장비의 출생·성장·소유·사건 기록",
        "Godot AI",
    ),
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
        "예술성 27",
        "고정 설계 최대치 없음",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "제품 구현: `BLOCKED`",
    ),
    "docs/planning/CURRENT_R2_CANON_REGISTRY.json": (
        '"schema_version":8',
        '"planning_pr":103',
        '"closure_pr":104',
        '"canon_audit_pr":105',
        '"next_approval_counter":"2/10"',
        '"product_implementation":"BLOCKED"',
        '"id":"BS-CRAFT-20260804-07"',
        '"id":"BS-CRAFT-20260805-01"',
        '"id":"BS-OPS-20260805-01"',
        '"domain":"NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM"',
        '"minimum":0',
        '"fixed_design_maximum":null',
        '"denominator_display_allowed":false',
        '"technical_storage_limit_is_content_maximum":false',
        '"current_artistry_model":"NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM_NO_NAMED_TIERS"',
        '"historical_bounded_artistry_model":"INTEGER_1_TO_10_NO_NAMED_TIERS_SUPERSEDED"',
        '"five_grade_product_implementation":"NOT_STARTED_BLOCKED"',
    ),
    "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md": (
        "[현재 정본]",
        "R2_BATCH_004_2_OF_10",
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
        "CRAFT_FINE",
        "[보통] → [우수] → [명품] → [걸작] → [전설]",
        "제작 후 등급 승격 금지",
    ),
    "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md": (
        "BS-CRAFT-20260805-01",
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
    "docs/planning/BLACKSMITH_R2_FOUR_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md": (
        "[대체됨]",
        "BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md",
    ),
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": (
        "R2 체크포인트 003",
        "BS-OPS-20260804-02",
        "BS-OPS-20260805-01",
        "BS-CRAFT-20260805-01",
        "R2_BATCH_004_2_OF_10",
        "예술성 27",
        "고정 설계 최대치 없음",
        "현재 승인 카운터: `2/10`",
        "제품 구현: `BLOCKED`",
    ),
    "[기획서]/00_프로젝트_허브/ROADMAP.md": (
        "R2_CHECKPOINT_003",
        "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
        "예술성 27",
        "PRODUCT_IMPLEMENTATION: BLOCKED",
    ),
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": (
        "Three Affix Gate",
        "Benchmark Gate",
        "TDD Gate",
        "Legacy Document Gate",
        "NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM",
        "예술성 27",
        "CODEX_IMPLEMENTATION_GATE: BLOCKED",
    ),
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md": (
        "[부분 대체됨]",
        "현재 구현·후속 기획의 직접 기준으로 사용하지 마십시오",
        "BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md",
    ),
    "docs/MVP-003_SCOPE.md": (
        "[역사 증거] [보류]",
        "NOT_CURRENT_PRODUCT_SCOPE / HOLD",
    ),
    "project.godot": (
        "res://addons/godot_ai/plugin.cfg",
        "res://addons/godot_ai/runtime/game_helper.gd",
    ),
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return value


def text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in {".git", ".godot", "external", "artifacts", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"AGENTS.md", "README.md", "project.godot"}:
            yield path


def git_head(root: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def front_matter_fields(text: str) -> dict[str, str]:
    match = FRONT_MATTER.search(text)
    if not match:
        return {}
    return {
        item.group("key"): item.group("value").strip().strip("'\"")
        for item in FRONT_FIELD.finditer(match.group("body"))
    }


def normalize_candidate(raw: str) -> str | None:
    value = raw.strip().strip(".,;:")
    if not value or value.startswith(("http://", "https://", "mailto:", "res://")):
        return None
    value = ANCHOR.sub("", value)
    if not value or any(token in value for token in ("*", "{", "}", "<", ">", "|", "$", "$(")):
        return None
    if " → " in value or " / " in value or " = " in value:
        return None
    if value.startswith(("python ", "godot ", "git ", "RRULE", "BEGIN:")):
        return None
    if " " in value and not value.startswith("[기획서]/"):
        return None
    if value.startswith(LOCAL_PREFIXES) or value.startswith(("../", "./")):
        return value
    if value in {
        "ACTIVE_CONTEXT.md",
        "DOCUMENTATION_MAP.md",
        "DEVELOPMENT_GATES.md",
        "DESIGN_DOCUMENT_REGISTRY.json",
        "SKILL_REGISTRY.json",
        "ROADMAP.md",
        "CHANGELOG.md",
        "DECISION_LOG.md",
        "START_HERE.md",
        "WORK_MODE_AND_SKILL_ROUTING.md",
    }:
        return value
    return None


def is_vendored_reference_source(project_root: Path, source: Path) -> bool:
    relative = source.relative_to(project_root).as_posix()
    return relative.startswith(VENDORED_REFERENCE_ROOTS)


def resolve_reference(project_root: Path, source: Path, candidate: str) -> Path:
    if candidate.startswith(LOCAL_PREFIXES):
        return (project_root / candidate).resolve()
    local = (source.parent / candidate).resolve()
    if local.exists():
        return local
    hub = (project_root / "[기획서]/00_프로젝트_허브" / candidate).resolve()
    return hub if hub.exists() else local


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


def audit_base(base_root: Path, profile: dict, findings: list[Finding]) -> dict:
    registry_path = base_root / "skills/SKILL_REGISTRY.json"
    if not registry_path.is_file():
        add(findings, "ERROR", "BASE_REGISTRY_MISSING", "Base Skill Registry is missing", registry_path)
        return {}

    registry = read_json(registry_path)
    active = [item for item in registry.get("skills", []) if item.get("status") == "ACTIVE"]
    active_ids = {item.get("skill_id") for item in active}
    mapped = {item.get("base_skill_id") for item in profile.get("capabilities", [])}

    missing = sorted(active_ids - mapped)
    extra = sorted(mapped - active_ids)
    if missing:
        add(findings, "ERROR", "BASE_CAPABILITY_UNMAPPED", f"Active Base skills are not mapped: {missing}")
    if extra:
        add(findings, "ERROR", "PROFILE_UNKNOWN_CAPABILITY", f"Profile maps unknown Base skills: {extra}")

    for item in active:
        path = base_root / str(item.get("path", ""))
        if not path.is_file():
            add(findings, "ERROR", "BASE_SKILL_PATH_MISSING", f"Base skill path missing for {item.get('skill_id')}", path)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        fields = front_matter_fields(text)
        if fields.get("name") != item.get("skill_id"):
            add(findings, "ERROR", "BASE_SKILL_ID_MISMATCH", f"Base skill front matter mismatch for {item.get('skill_id')}", path)
        if item.get("load_by_default") is not False:
            add(findings, "ERROR", "BASE_SKILL_NOT_SELECTIVE", f"Base skill must remain selective: {item.get('skill_id')}", path)

    expected_commit = profile.get("base_commit")
    actual_commit = git_head(base_root)
    if expected_commit and actual_commit and actual_commit != expected_commit:
        add(findings, "ERROR", "BASE_COMMIT_MISMATCH", f"Expected Base {expected_commit}, got {actual_commit}")
    elif expected_commit and actual_commit is None:
        add(findings, "WARNING", "BASE_COMMIT_UNVERIFIED", "Could not read Base git HEAD")

    base_files = list(text_files(base_root))
    suffix_counts = Counter(path.suffix.lower() or path.name for path in base_files)
    return {
        "commit": actual_commit,
        "active_skill_count": len(active),
        "active_skill_ids": sorted(active_ids),
        "text_file_count": len(base_files),
        "text_file_types": dict(sorted(suffix_counts.items())),
    }


def audit_project(project_root: Path, profile: dict, findings: list[Finding]) -> dict:
    for relative in profile.get("required_entrypoints", []):
        if not (project_root / relative).exists():
            add(findings, "ERROR", "ENTRYPOINT_MISSING", "Required project entrypoint is missing", relative)

    for relative in profile.get("forbidden_temporary_paths", []):
        if (project_root / relative).exists():
            add(findings, "ERROR", "TEMPORARY_PATH_REMAINS", "Temporary migration artifact remains", relative)

    project_registry_path = project_root / "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json"
    project_registry = read_json(project_registry_path)
    policy = project_registry.get("routing_policy", {})
    if policy.get("default_selection") != "automatic-trigger-match":
        add(findings, "ERROR", "PROJECT_ROUTING_NOT_AUTOMATIC", "Project Skill routing must use automatic-trigger-match", project_registry_path)
    if policy.get("load_all_skills") is not False:
        add(findings, "ERROR", "PROJECT_LOADS_ALL_SKILLS", "Project must not load all skills", project_registry_path)

    project_skills = project_registry.get("skills", [])
    expected_count = profile.get("project_skill_count")
    if expected_count is not None and len(project_skills) != expected_count:
        add(findings, "ERROR", "PROJECT_SKILL_COUNT", f"Expected {expected_count} project skills, found {len(project_skills)}", project_registry_path)

    skill_by_id = {item.get("skill_id"): item for item in project_skills}
    for item in project_skills:
        skill_id = item.get("skill_id")
        path = (project_registry_path.parent / str(item.get("path", ""))).resolve()
        if not path.is_file():
            add(findings, "ERROR", "PROJECT_SKILL_PATH_MISSING", f"Project skill path missing for {skill_id}", path)
            continue
        if item.get("load_by_default") is not False:
            add(findings, "ERROR", "PROJECT_SKILL_NOT_SELECTIVE", f"Project skill must remain selective: {skill_id}", path)
        text = path.read_text(encoding="utf-8", errors="replace")
        fields = front_matter_fields(text)
        if fields and fields.get("name") != skill_id:
            add(findings, "ERROR", "PROJECT_SKILL_ID_MISMATCH", f"Project skill front matter mismatch for {skill_id}", path)
        for mode in item.get("skill_modes", []):
            if mode not in text:
                add(findings, "ERROR", "PROJECT_SKILL_MODE_MISSING", f"Registry mode '{mode}' is absent from {skill_id}", path)

    for capability in profile.get("capabilities", []):
        owner_value = capability.get("local_owner")
        if not owner_value:
            add(findings, "ERROR", "CAPABILITY_OWNER_MISSING", f"Capability has no local owner: {capability.get('base_skill_id')}")
            continue
        owner_path = project_root / ANCHOR.sub("", owner_value)
        if not owner_path.exists():
            add(findings, "ERROR", "CAPABILITY_OWNER_NOT_FOUND", f"Local owner missing for {capability.get('base_skill_id')}", owner_value)
        local_skill_id = capability.get("local_skill_id")
        if local_skill_id and local_skill_id not in skill_by_id:
            add(findings, "ERROR", "CAPABILITY_SKILL_NOT_FOUND", f"Mapped local skill does not exist: {local_skill_id}")
        if capability.get("disposition") not in {"ADOPT", "ADAPT", "CONSOLIDATE", "ROUTE_ON_DEMAND"}:
            add(findings, "ERROR", "CAPABILITY_DISPOSITION_INVALID", f"Invalid disposition for {capability.get('base_skill_id')}")
        if not capability.get("activation"):
            add(findings, "ERROR", "CAPABILITY_ACTIVATION_MISSING", f"Capability activation missing: {capability.get('base_skill_id')}")

    design_registry_path = project_root / "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    design_registry = read_json(design_registry_path)
    document_ids: set[str] = set()
    for document in design_registry.get("documents", []):
        document_id = document.get("document_id")
        if document_id in document_ids:
            add(findings, "ERROR", "DUPLICATE_DOCUMENT_ID", f"Duplicate document_id: {document_id}", design_registry_path)
        document_ids.add(document_id)
        source = (design_registry_path.parent / str(document.get("source_path", ""))).resolve()
        if not source.is_file():
            add(findings, "ERROR", "DOCUMENT_SOURCE_MISSING", f"Design document source missing: {document_id}", source)
        for raw_path in document.get("actual_paths", []):
            actual = (design_registry_path.parent / raw_path).resolve()
            if not actual.exists():
                add(findings, "ERROR", "DOCUMENT_ACTUAL_PATH_MISSING", f"Actual path missing for {document_id}", actual)
        output_pdf = document.get("output_pdf")
        if output_pdf and document.get("publication_status") == "CURRENT":
            pdf = (design_registry_path.parent / output_pdf).resolve()
            if not pdf.is_file():
                add(findings, "ERROR", "CURRENT_PUBLICATION_MISSING", f"CURRENT publication PDF is missing: {document_id}", pdf)

    broken_refs: list[str] = []
    for source in text_files(project_root):
        if is_vendored_reference_source(project_root, source):
            continue
        text = source.read_text(encoding="utf-8", errors="replace")
        raw_refs = set(BACKTICK.findall(text)) | set(MARKDOWN_LINK.findall(text))
        for raw in raw_refs:
            candidate = normalize_candidate(raw)
            if candidate is None:
                continue
            target = resolve_reference(project_root, source, candidate)
            if not target.exists():
                broken_refs.append(f"{source.relative_to(project_root)} -> {candidate}")
    for item in sorted(set(broken_refs)):
        add(findings, "ERROR", "BROKEN_LOCAL_REFERENCE", item)

    for relative in ACTIVE_DOCS:
        path = project_root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in STALE_PATTERNS.items():
            match = pattern.search(text)
            if match:
                add(findings, "ERROR", "STALE_ACTIVE_RULE", f"{label}: {match.group(0)}", relative)

    for relative, required in REQUIRED_ASSERTIONS.items():
        path = project_root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in required:
            if token not in text:
                add(findings, "ERROR", "REQUIRED_ASSERTION_MISSING", f"Required current assertion '{token}' is missing", relative)

    required_runtime_paths = (
        "project.godot",
        "scenes/test/enhancement_test.tscn",
        "scripts/enhancement/enhancement_session.gd",
        "scripts/ui/enhancement_screen.gd",
        "scripts/ui/enhancement_test_runner.gd",
        "scripts/ui/game_flow_screen.gd",
        "tests/unit/test_enhancement_session.gd",
        "data/crafting/enhancement_balance.json",
        "addons/godot_ai/plugin.cfg",
        "addons/godot_ai/plugin.gd",
        "addons/godot_ai/runtime/game_helper.gd",
    )
    for relative in required_runtime_paths:
        if not (project_root / relative).is_file():
            add(findings, "ERROR", "RUNTIME_PATH_MISSING", "Required runtime path is missing", relative)

    project_files = list(text_files(project_root))
    return {
        "project_skill_count": len(project_skills),
        "project_skill_ids": sorted(skill_by_id),
        "design_document_count": len(design_registry.get("documents", [])),
        "text_file_count": len(project_files),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Base adoption and Blacksmith operating-system integrity")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--base-root", required=True)
    parser.add_argument("--profile", default="docs/BASE_ADOPTION_PROFILE.json")
    parser.add_argument("--report", default="artifacts/base-adoption-report.json")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    base_root = Path(args.base_root).resolve()
    profile_path = (project_root / args.profile).resolve()
    report_path = (project_root / args.report).resolve()

    findings: list[Finding] = []
    try:
        profile = read_json(profile_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Base adoption audit FAILED: {exc}")
        return 1

    try:
        base_summary = audit_base(base_root, profile, findings)
        project_summary = audit_project(project_root, profile, findings)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        add(findings, "ERROR", "AUDIT_EXCEPTION", str(exc))
        base_summary = {}
        project_summary = {}

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
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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
