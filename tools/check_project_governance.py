#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".github" / "project-governance.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    errors: list[str] = []
    checks = 0
    config = load_json(CONFIG)

    for item in config["required_files"]:
        checks += 1
        if not (ROOT / item).is_file():
            errors.append(f"missing required file: {item}")

    base_version = (ROOT / "docs/BASE_RULES_VERSION.md").read_text(encoding="utf-8")
    checks += 1
    if config["base_commit"] not in base_version:
        errors.append("BASE_RULES_VERSION does not pin configured Base commit")

    for item in config["obsolete_paths"]:
        checks += 1
        if (ROOT / item).exists():
            errors.append(f"obsolete path still active: {item}")

    project_text = (ROOT / "project.godot").read_text(encoding="utf-8")
    checks += 2
    if f'run/main_scene="{config["expected_main_scene"]}"' not in project_text:
        errors.append("project.godot main scene is not the enhancement F5 entrypoint")
    if "자동 단조 검증 실행" in project_text:
        errors.append("temporary project.godot validation comment remains")

    for item in config["current_docs"]:
        text = (ROOT / item).read_text(encoding="utf-8")
        for token in config["forbidden_current_tokens"]:
            checks += 1
            if token in text:
                errors.append(f"{item}: stale active token {token!r}")

    balance = load_json(ROOT / "data/crafting/enhancement_balance.json")
    expected = [
        ("max_level", balance.get("max_level"), 100),
        ("precision_interval", balance.get("precision_interval"), 10),
        ("material_interval", balance.get("material_interval"), 10),
        ("pity.bonus_per_failure", balance.get("pity", {}).get("bonus_per_failure"), 0.04),
        ("pity.max_bonus", balance.get("pity", {}).get("max_bonus"), 0.24),
        ("risk.safe_until_level", balance.get("risk", {}).get("safe_until_level"), 10),
        ("risk.destroy_start_level", balance.get("risk", {}).get("destroy_start_level"), 30),
        ("overdrive.leap_chance", balance.get("skills", {}).get("overdrive", {}).get("leap_chance"), 0.08),
        ("overdrive.leap_levels", balance.get("skills", {}).get("overdrive", {}).get("leap_levels"), 2),
    ]
    for name, actual, wanted in expected:
        checks += 1
        if actual != wanted:
            errors.append(f"enhancement balance {name}: expected {wanted}, got {actual}")

    current_required = {
        "+11": ["docs/MVP-002_SCOPE.md", "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"],
        "+30": ["docs/MVP-002_SCOPE.md", "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"],
        "자동 단조": ["README.md", "docs/MVP-002_SCOPE.md", "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md"],
        "8%": ["docs/MVP-002_SCOPE.md", "[기획서]/00_프로젝트_허브/DECISION_LOG.md"],
    }
    for token, paths in current_required.items():
        for item in paths:
            checks += 1
            if token not in (ROOT / item).read_text(encoding="utf-8"):
                errors.append(f"{item}: missing current rule token {token!r}")

    game_bible = (ROOT / "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md").read_text(encoding="utf-8")
    for token in config.get("required_game_bible_tokens", []):
        checks += 1
        if token not in game_bible:
            errors.append(f"Game Bible lost preserved product detail {token!r}")

    interview_path = ROOT / "[기획서]/00_프로젝트_허브/INTERVIEW_REGISTRY.json"
    interview_registry = load_json(interview_path)
    interview_ids = {entry.get("interview_id") for entry in interview_registry.get("interviews", [])}
    for interview_id in config.get("preserved_interview_ids", []):
        checks += 1
        if interview_id not in interview_ids:
            errors.append(f"INTERVIEW_REGISTRY lost preserved interview {interview_id}")
    for entry in interview_registry.get("interviews", []):
        record = entry.get("record_path")
        if record:
            checks += 1
            if not (interview_path.parent / record).is_file():
                errors.append(f"interview {entry.get('interview_id')}: missing record {record}")

    skill_path = ROOT / "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json"
    skill_registry = load_json(skill_path)
    checks += 6
    policy = skill_registry.get("routing_policy", {})
    if skill_registry.get("schema_version") != 3:
        errors.append("SKILL_REGISTRY schema_version must be 3")
    if policy.get("default_selection") != "automatic-trigger-match":
        errors.append("SKILL_REGISTRY default_selection must be automatic-trigger-match")
    if policy.get("load_all_skills") is not False:
        errors.append("SKILL_REGISTRY load_all_skills must be false")
    if policy.get("require_execution_report") is not True:
        errors.append("SKILL_REGISTRY execution report must be required")
    if policy.get("work_modes") != ["PLAN", "BUILD", "REVIEW"]:
        errors.append("SKILL_REGISTRY work_modes mismatch")
    skill_ids = [entry.get("skill_id") for entry in skill_registry.get("skills", [])]
    if len(skill_ids) != len(set(skill_ids)):
        errors.append("SKILL_REGISTRY duplicate skill_id")

    known_skill_ids = set(skill_ids)
    for entry in skill_registry.get("skills", []):
        skill_id = entry.get("skill_id", "<unknown>")
        checks += 6
        if entry.get("status") == "ACTIVE" and entry.get("load_by_default") is not False:
            errors.append(f"{skill_id}: active skill must not load by default")
        for key in ("trigger_tags", "use_when", "do_not_use_when", "review_triggers"):
            if not entry.get(key):
                errors.append(f"{skill_id}: missing {key}")
        path = (skill_path.parent / entry.get("path", "")).resolve()
        if not path.is_file():
            errors.append(f"{skill_id}: missing skill path {entry.get('path')}")
        learning_log = (skill_path.parent / entry.get("learning_log", "")).resolve()
        if not learning_log.is_file():
            errors.append(f"{skill_id}: missing learning log {entry.get('learning_log')}")

    for discipline, entrypoints in skill_registry.get("discipline_entrypoints", {}).items():
        for skill_id in entrypoints:
            checks += 1
            if skill_id not in known_skill_ids:
                errors.append(f"discipline {discipline}: unknown skill id {skill_id}")

    presentation = skill_registry.get("human_presentation", {})
    manifest_name = presentation.get("publication_manifest")
    checks += 1
    if not manifest_name or not (skill_path.parent / manifest_name).is_file():
        errors.append("SKILL_REGISTRY publication manifest is missing")

    design_path = ROOT / "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    design_registry = load_json(design_path)
    allowed_policies = {"source_only", "milestone_sync", "always_sync"}
    covered: set[str] = set()
    for document in design_registry.get("documents", []):
        checks += 2
        covered.update(document.get("responsibility_coverage", []))
        source = (design_path.parent / document["source_path"]).resolve()
        if not source.is_file():
            errors.append(f"document {document['document_id']}: missing source {document['source_path']}")
        if document.get("publication_policy") not in allowed_policies:
            errors.append(f"document {document['document_id']}: invalid publication policy")
        if document.get("publication_policy") != "source_only":
            manifest = document.get("publication_manifest")
            checks += 1
            if not manifest or not (design_path.parent / manifest).resolve().is_file():
                errors.append(f"document {document['document_id']}: publication manifest missing")
        for actual_path in document.get("actual_paths", []):
            checks += 1
            if not (design_path.parent / actual_path).resolve().exists():
                errors.append(f"document {document['document_id']}: missing actual path {actual_path}")

    for responsibility in design_registry.get("required_responsibility_coverage", []):
        checks += 1
        if responsibility not in covered:
            errors.append(f"DESIGN_DOCUMENT_REGISTRY uncovered responsibility {responsibility}")

    test_text = (ROOT / "tests/unit/test_enhancement_session.gd").read_text(encoding="utf-8")
    checks += 1
    if "EnhancementSession tests PASSED (12 cases)" not in test_text:
        errors.append("enhancement test count contract is not 12 cases")

    for path in ROOT.rglob("*.json"):
        if ".godot" in path.parts:
            continue
        checks += 1
        try:
            load_json(path)
        except Exception as exc:
            errors.append(f"{relative(path)}: invalid JSON: {exc}")

    if errors:
        print("Blacksmith project governance FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Blacksmith project governance PASSED ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
