from __future__ import annotations

import sys
from pathlib import Path

def python_commands(python: str, scope: str, operating_base: Path, contract_base: Path, protected_base_sha: str, pr_base_sha: str) -> list[tuple[str, list[str]]]:
    commands = [
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
        ("base-v9-adoption", [python, "-m", "unittest", "tests.test_base_v9_adoption"]),
        ("bca-contracts", [python, "-m", "unittest", "tests.test_bca_visual_sheet_adoption", "tests.test_bca_workflow_contract", "-v"]),
        ("thin-adapter", [python, "tests/test_project_base_adapter_thin_migration.py", "-v"]),
        ("pr-diff-whitespace", ["git", "diff", "--check", f"{pr_base_sha}...HEAD"]),
        ("operating-audit-runner", [python, "-m", "unittest", "tests/test_project_operating_system_audit_runner.py"]),
        ("operating-audit", [python, "tools/run_project_operating_system_audit.py", "--base-root", str(operating_base), "--report", "artifacts/base-adoption-report.json"]),
        ("project-base-adapter", [python, str(contract_base / "tools" / "check_project_operating_contract.py"), "--project-root", ".", "--base-repository", str(contract_base), "--protected-base", protected_base_sha, "--check"]),
    ]
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
    commands = [
        ("godot-version", [godot, "--version"]),
        ("godot-import", [godot, "--headless", "--editor", "--path", str(repo), "--quit"]),
    ]
    for scene in ("res://scenes/test/enhancement_test.tscn", "res://scenes/test/equipment_lifecycle_poc.tscn", "res://scenes/main/main.tscn"):
        commands.append((f"scene-{Path(scene).stem}", [godot, "--headless", "--path", str(repo), scene, "--quit-after", "2"]))
    suites = (
        "res://tests/unit/test_forging_session.gd", "res://tests/unit/test_enhancement_session.gd",
        "res://tests/unit/test_workshop_resources.gd", "res://tests/unit/test_workshop_calendar.gd",
        "res://tests/unit/test_craftsmanship_grade_resolver.gd", "res://tests/unit/test_customer_contract.gd",
        "res://tests/unit/test_world_activity_resolver.gd", "res://tests/unit/test_equipment_world_registry.gd",
        "res://tests/unit/test_poc_telemetry.gd", "res://tests/integration/test_manual_enhancement_economy.gd",
        "res://tests/integration/test_forging_quality_enhancement.gd", "res://tests/integration/test_workshop_action_atomicity.gd",
        "res://tests/integration/test_equipment_lifecycle_controller.gd", "res://tests/integration/test_equipment_lifecycle_poc.gd",
    )
    commands.extend((f"godot-{Path(path).stem}", [godot, "--headless", "--path", str(repo), "--script", path]) for path in suites)
    commands.extend([
        ("godot-gut-import", [godot, "--headless", "--import", "--path", str(repo)]),
        ("gut-cli", [godot, "--headless", "-d", "-s", "--path", str(repo), "addons/gut/gut_cmdln.gd", "-gdir=res://tests/gut/unit", "-gdir=res://tests/gut/integration", "-ginclude_subdirs", "-gexit", "-gjunit_xml_file=res://artifacts/gut/junit.xml"]),
        ("gut-junit", [sys.executable, "tools/validate_gut_junit.py", "artifacts/gut/junit.xml", "--minimum-tests", "1"]),
    ])
    return commands
