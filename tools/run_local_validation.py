#!/usr/bin/env python3
"""Run Blacksmith validation without consuming GitHub Actions minutes.

The runner is fail-closed for merge evidence: PASS requires a clean exact HEAD,
the pinned Base audit, Godot 4.7.1 import/smoke/model suites, GUT/JUnit, and no
tracked authoring-surface mutation. Missing engine/Base evidence yields PARTIAL.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

BASE_PIN = "41a20584dd2ee51d917e5c9d7cab6838e1ceba7e"
BLOCKING_GODOT_MARKERS = ("SCRIPT ERROR:", "Parse Error:", "Compile Error:", "ERROR:")
EXPECTED_GODOT_MARKERS = {
    "godot-test_forging_session": "ForgingSession tests PASSED",
    "godot-test_enhancement_session": "EnhancementSession tests PASSED",
    "godot-test_workshop_resources": "WorkshopResources tests PASSED",
    "godot-test_workshop_calendar": "WorkshopCalendar tests PASSED",
    "godot-test_craftsmanship_grade_resolver": "CraftsmanshipGradeResolver tests PASSED",
    "godot-test_customer_contract": "CustomerContract tests PASSED",
    "godot-test_world_activity_resolver": "WorldActivityResolver tests PASSED",
    "godot-test_equipment_world_registry": "EquipmentWorldRegistry tests PASSED",
    "godot-test_poc_telemetry": "PocTelemetry tests PASSED",
    "godot-test_manual_enhancement_economy": "Manual enhancement economy integration tests PASSED",
    "godot-test_forging_quality_enhancement": "Forging quality enhancement integration tests PASSED",
    "godot-test_workshop_action_atomicity": "Workshop action atomicity integration tests PASSED",
    "godot-test_equipment_lifecycle_controller": "Equipment lifecycle controller integration tests PASSED",
    "godot-test_equipment_lifecycle_poc": "Equipment lifecycle PoC integration tests PASSED",
}


@dataclass
class CommandResult:
    name: str
    command: list[str]
    exit_code: int
    started_at: str
    completed_at: str
    log_path: str

    @property
    def passed(self) -> bool:
        return self.exit_code == 0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_authoring_surface(path: str) -> bool:
    return (
        path == "project.godot"
        or path.endswith((".tscn", ".tres", ".res"))
        or path.startswith("addons/godot_ai/")
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_output(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=repo, text=True, encoding="utf-8"
    ).strip()


def tracked_authoring_hashes(repo: Path) -> dict[str, str]:
    tracked = git_output(repo, "ls-files", "-z").split("\0")
    return {
        path: sha256_file(repo / path)
        for path in sorted(tracked)
        if path and is_authoring_surface(path) and (repo / path).is_file()
    }


def run_command(
    name: str,
    command: Sequence[str],
    cwd: Path,
    log_dir: Path,
) -> CommandResult:
    log_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in name)
    log_path = log_dir / f"{safe_name}.log"
    started = utc_now()
    with log_path.open("w", encoding="utf-8", errors="replace") as log:
        process = subprocess.run(
            list(command),
            cwd=cwd,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
    return CommandResult(
        name=name,
        command=list(command),
        exit_code=process.returncode,
        started_at=started,
        completed_at=utc_now(),
        log_path=str(log_path.resolve()),
    )


def validate_logged_result(result: CommandResult) -> CommandResult:
    log_text = Path(result.log_path).read_text(encoding="utf-8", errors="replace")
    if result.name == "godot-version" and "4.7.1" not in log_text:
        result.exit_code = 20
        return result
    if result.name.startswith(("godot-", "scene-", "gut-cli")) and result.name != "gut-junit":
        if any(marker in log_text for marker in BLOCKING_GODOT_MARKERS):
            result.exit_code = 21
            return result
    expected_marker = EXPECTED_GODOT_MARKERS.get(result.name)
    if expected_marker and expected_marker not in log_text:
        result.exit_code = 22
    return result


def python_commands(python: str, scope: str, base_root: Path | None) -> list[tuple[str, list[str]]]:
    commands: list[tuple[str, list[str]]] = [
        ("pytest-version", [python, "-c", "import pytest; assert pytest.__version__ == '8.3.5', pytest.__version__"]),
        ("local-validation-fallback", [python, "-m", "unittest", "tests/test_local_validation_fallback.py", "-v"]),
        ("no-merge-conflicts-unittest", [python, "-m", "unittest", "tests/test_no_merge_conflicts.py"]),
        ("no-merge-conflicts-scan", [python, "tests/check_no_merge_conflicts.py", "."]),
        ("project-core-alignment", [python, "tests/check_project_core_alignment_current.py"]),
        ("ci-workflow-structure", [python, "-m", "unittest", "tests/test_ci_workflow_structure.py"]),
        ("higodot-gut-authority", [python, "-m", "pytest", "tests/test_higodot_gut_authority_gate.py", "-q"]),
        ("gut-adoption-contract", [python, "-m", "unittest", "tests/test_gut_formal_adoption_contract.py", "-v"]),
        ("archive-governance", [python, "tools/check_archive_governance.py"]),
        ("archive-retention", [python, "-m", "unittest", "tests.test_archive_retention_governance", "-v"]),
    ]
    if base_root is not None:
        commands.extend([
            ("operating-audit-runner", [python, "-m", "unittest", "tests/test_project_operating_system_audit_runner.py"]),
            ("operating-audit", [python, "tools/run_project_operating_system_audit.py", "--base-root", str(base_root), "--report", "artifacts/base-adoption-report.json"]),
        ])
    if scope == "code":
        commands.extend([
            ("game-data", [python, "tools/validate_game_data.py"]),
            ("lifecycle-data", [python, "tools/validate_lifecycle_data.py"]),
            ("lifecycle-contract", [python, "-m", "unittest", "tests/test_lifecycle_data_contract.py"]),
            ("forging-quality", [python, "tests/check_forging_quality_contract.py"]),
            ("enhancement-failure", [python, "tests/check_enhancement_failure_contract.py"]),
            ("enhancement-simulator", [python, "-m", "unittest", "tests/test_enhancement_balance_simulator.py"]),
            ("enhancement-simulator-contract", [python, "tests/check_enhancement_balance_simulator_contract.py"]),
        ])
    return commands


def godot_commands(godot: str, repo: Path) -> list[tuple[str, list[str]]]:
    commands: list[tuple[str, list[str]]] = [
        ("godot-version", [godot, "--version"]),
        ("godot-import", [godot, "--headless", "--editor", "--path", str(repo), "--quit"]),
    ]
    for scene in (
        "res://scenes/test/enhancement_test.tscn",
        "res://scenes/test/equipment_lifecycle_poc.tscn",
        "res://scenes/main/main.tscn",
    ):
        commands.append((f"scene-{Path(scene).stem}", [godot, "--headless", "--path", str(repo), scene, "--quit-after", "2"]))
    suites = (
        "res://tests/unit/test_forging_session.gd",
        "res://tests/unit/test_enhancement_session.gd",
        "res://tests/unit/test_workshop_resources.gd",
        "res://tests/unit/test_workshop_calendar.gd",
        "res://tests/unit/test_craftsmanship_grade_resolver.gd",
        "res://tests/unit/test_customer_contract.gd",
        "res://tests/unit/test_world_activity_resolver.gd",
        "res://tests/unit/test_equipment_world_registry.gd",
        "res://tests/unit/test_poc_telemetry.gd",
        "res://tests/integration/test_manual_enhancement_economy.gd",
        "res://tests/integration/test_forging_quality_enhancement.gd",
        "res://tests/integration/test_workshop_action_atomicity.gd",
        "res://tests/integration/test_equipment_lifecycle_controller.gd",
        "res://tests/integration/test_equipment_lifecycle_poc.gd",
    )
    commands.extend((f"godot-{Path(path).stem}", [godot, "--headless", "--path", str(repo), "--script", path]) for path in suites)
    commands.extend([
        ("godot-gut-import", [godot, "--headless", "--import", "--path", str(repo)]),
        ("gut-cli", [godot, "--headless", "-d", "-s", "--path", str(repo), "addons/gut/gut_cmdln.gd", "-gdir=res://tests/gut/unit", "-gdir=res://tests/gut/integration", "-ginclude_subdirs", "-gexit", "-gjunit_xml_file=res://artifacts/gut/junit.xml"]),
        ("gut-junit", [sys.executable, "tools/validate_gut_junit.py", "artifacts/gut/junit.xml", "--minimum-tests", "1"]),
    ])
    return commands


def summarize_status(
    command_results: Iterable[CommandResult],
    exact_head: bool,
    clean_before: bool,
    clean_after: bool,
    authoring_unchanged: bool,
    base_present: bool,
    godot_present: bool,
    require_godot: bool,
    contract_consistent: bool = True,
) -> str:
    if not contract_consistent:
        return "FAIL"
    if not exact_head or not clean_before or not clean_after or not authoring_unchanged:
        return "FAIL"
    if any(not result.passed for result in command_results):
        return "FAIL"
    if not base_present or (require_godot and not godot_present):
        return "PARTIAL"
    return "PASS" if godot_present else "PARTIAL"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--base-root")
    parser.add_argument("--godot")
    parser.add_argument("--scope", choices=("docs", "code"), default="code")
    parser.add_argument("--require-godot", action="store_true")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo_root).resolve()
    output = Path(args.output).resolve()
    log_dir = output.parent / f"{output.stem}-logs"
    base_root = Path(args.base_root).resolve() if args.base_root else None
    head = git_output(repo, "rev-parse", "HEAD")
    exact_head = head == args.expected_head
    clean_before = git_output(repo, "status", "--porcelain", "--untracked-files=no") == ""
    before_hashes = tracked_authoring_hashes(repo)

    results: list[CommandResult] = []
    for name, command in python_commands(sys.executable, args.scope, base_root):
        result = run_command(name, command, repo, log_dir)
        results.append(result)
        if not result.passed:
            break

    godot_present = bool(args.godot and Path(args.godot).is_file())
    if all(result.passed for result in results) and godot_present:
        (repo / "artifacts" / "gut").mkdir(parents=True, exist_ok=True)
        for name, command in godot_commands(str(Path(args.godot).resolve()), repo):
            result = validate_logged_result(run_command(name, command, repo, log_dir))
            results.append(result)
            if not result.passed:
                break

    after_hashes = tracked_authoring_hashes(repo)
    authoring_unchanged = before_hashes == after_hashes
    clean_after = git_output(repo, "status", "--porcelain", "--untracked-files=no") == ""
    base_head = git_output(base_root, "rev-parse", "HEAD") if base_root is not None and (base_root / ".git").exists() else None
    base_pin_match = base_head == BASE_PIN
    workflow_text = (repo / ".github" / "workflows" / "python-validation.yml").read_text(encoding="utf-8")
    workflow_base_pin_match = BASE_PIN in workflow_text
    status = summarize_status(
        results,
        exact_head,
        clean_before,
        clean_after,
        authoring_unchanged,
        base_pin_match,
        godot_present,
        args.require_godot,
        workflow_base_pin_match,
    )
    manifest = {
        "schema_version": "1.0.0",
        "validation_mode": "LOCAL_EXACT_HEAD_NO_GITHUB_ACTIONS",
        "head_sha": head,
        "expected_head_sha": args.expected_head,
        "exact_head": exact_head,
        "scope": args.scope,
        "status": status,
        "started_environment": {
            "platform": platform.platform(),
            "python": sys.version,
            "working_directory": str(repo),
        },
        "base_root": str(base_root) if base_root else None,
        "base_expected_head": BASE_PIN,
        "base_actual_head": base_head,
        "base_pin_match": base_pin_match,
        "workflow_base_pin_match": workflow_base_pin_match,
        "godot_executable": str(Path(args.godot).resolve()) if args.godot else None,
        "godot_required": args.require_godot,
        "godot_present": godot_present,
        "clean_before": clean_before,
        "clean_after": clean_after,
        "authoring_surface_hash_unchanged": authoring_unchanged,
        "authoring_surface_count": len(before_hashes),
        "commands": [asdict(result) | {"passed": result.passed} for result in results],
        "completed_at": utc_now(),
        "limitations": [
            "This manifest substitutes the execution venue only; it does not waive any v4.3 validation gate.",
            "Windows and Android device validation remain separate unless explicitly captured by additional evidence.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "manifest": str(output), "head": head}, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
