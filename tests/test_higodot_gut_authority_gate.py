from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/planning/BLACKSMITH_HIGODOT_GUT_AUTHORITY_AND_ENTRY_GATE_SPEC_2026-08-06.md"
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
SNAPSHOT = ROOT / "docs/operations/BLACKSMITH_ENTRY_GATE_SNAPSHOT_2026-08-06.json"
WORKFLOW = ROOT / ".github/workflows/validate-higodot-gut-authority-gate.yml"
AGENTS = ROOT / "AGENTS.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"

ALLOWED_CHANGED_PATHS = {
    str(SPEC.relative_to(ROOT)),
    str(POLICY.relative_to(ROOT)),
    str(SNAPSHOT.relative_to(ROOT)),
    str(WORKFLOW.relative_to(ROOT)),
    str(Path(__file__).relative_to(ROOT)),
    str(AGENTS.relative_to(ROOT)),
    str(GATES.relative_to(ROOT)),
}


def _text(path: Path) -> str:
    assert path.is_file(), f"missing required authority-gate surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(_text(path))


def test_policy_separates_current_state_from_target_authorities() -> None:
    policy = _json(POLICY)
    assert policy["schema_version"] == "1.0.0"
    assert policy["adoption_state"] == "VENDORED_PRESENT_FORMAL_ADOPTION_PENDING"
    assert policy["higodot"]["current_state"] == "PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY"
    assert policy["higodot"]["target_role"] == "SOLE_GODOT_AUTHORING_AUTHORITY"
    assert policy["gut"]["status"] == "VENDORED_PRESENT_FORMAL_ADOPTION_PENDING"
    assert policy["gut"]["target_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"
    assert policy["gut"]["official_version"] == "9.7.1"
    assert policy["gut"]["official_tag"] == "v9.7.1"
    assert policy["gut"]["official_tag_commit"] == "aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605"
    assert policy["gut"]["license"] == "MIT"
    assert policy["gut"]["godot_compatibility"] == "4.7.x"
    assert policy["gut"]["local_license_blob_sha"] == policy["gut"]["upstream_license_blob_sha"]
    assert policy["gut"]["project_plugin_enabled"] is False
    assert policy["gut"]["config_present"] is False
    assert policy["gut"]["project_gut_test_root_present"] is False
    assert policy["gut"]["formal_ci_authority"] is False


def test_policy_forbids_role_intrusion_and_defines_consumption_removal() -> None:
    policy = _json(POLICY)
    assert policy["conflict_rules"]["tracked_file_mutation_by_gut_runtime"] == "FORBIDDEN"
    assert policy["conflict_rules"]["higodot_edits_gut_tests_or_vendor_bytes"] == "FORBIDDEN"
    assert policy["conflict_rules"]["gut_edits_scene_resource_or_project_settings"] == "FORBIDDEN"
    assert policy["conflict_rules"]["same_file_dual_authority"] == "FORBIDDEN"
    assert policy["gut"]["planned_consumption"] == {
        "vendor_root": "addons/gut",
        "config": ".gutconfig.json",
        "test_roots": ["res://tests/gut/unit", "res://tests/gut/integration"],
        "cli_entry": "res://addons/gut/gut_cmdln.gd",
        "result_format": "JUnit XML",
    }
    assert policy["ci"]["planned_runtime_job"] == "gut-runtime-read-only"
    assert policy["ci"]["planned_test_count_minimum"] == 1
    assert policy["ci"]["zero_tests"] == "FAIL"
    assert policy["ci"]["tracked_authoring_surface_hash_before_after"] == "REQUIRED"
    assert policy["removal"]["project_settings_change_authority"] == "HIGODOT_ONLY"
    assert policy["removal"]["preserve_historical_test_evidence"] is True


def test_entry_snapshot_rejects_false_ready_states() -> None:
    snapshot = _json(SNAPSHOT)
    assert snapshot["source_main_sha"] == "07f77041f85bde223768128949ad8dc587d5a003"
    assert snapshot["general_product_implementation"] == "BLOCKED"
    assert snapshot["scoped_vertical_slice"] == "OPEN_ONLY_FOR_APPROVED_NAMESPACES"
    assert snapshot["pr_122"]["state"] == "OPEN_DRAFT_UNMERGED"
    assert snapshot["gut"]["aggregate"] == "VENDORED_PRESENT_FORMAL_ADOPTION_PENDING"
    assert snapshot["gut"]["plugin_enabled"] is False
    assert snapshot["image_gate"]["aggregate"] == "BLOCKED_NOT_PRODUCT_READY"
    assert snapshot["image_gate"]["normalized_k2_status"] == "BLOCKED_IMAGE_NOT_GENERATED"
    assert snapshot["open_findings"]["71_이미지기획_생성목록"] == "ENTRY_BLOCKED_SHEET_SCHEMA_DRIFT"
    assert snapshot["corrected_sheet_states"]["01_작업순서!H2"] == "COMPLETE_MAIN_CANON"
    assert snapshot["corrected_sheet_states"]["01_작업순서!H3"] == "R1_COMPLETE_MAIN_CANON"
    assert "READY" in snapshot["forbidden_unqualified_states"]
    assert "AWAITING" in snapshot["forbidden_unqualified_states"]
    assert "IN_REVIEW" in snapshot["forbidden_unqualified_states"]


def test_spec_and_top_level_gates_include_required_markers() -> None:
    spec = _text(SPEC)
    for marker in (
        "HIGODOT_SOLE_AUTHORING_AUTHORITY",
        "GUT_SOLE_TEST_AUTHORITY",
        "VENDORED_PRESENT_FORMAL_ADOPTION_PENDING",
        "ENTRY_GATE_FAIL_CLOSED",
        "GUT_RUNTIME_TRACKED_MUTATION_FORBIDDEN",
        "SEPARATE_REVIEWED_CHANGE_ONLY",
        "NO_PRODUCT_PATH_CHANGE",
    ):
        assert marker in spec

    agents = _text(AGENTS)
    gates = _text(GATES)
    for marker in (
        "HIGODOT_SOLE_AUTHORING_AUTHORITY",
        "GUT_SOLE_TEST_AUTHORITY",
        "ENTRY_GATE_FAIL_CLOSED",
    ):
        assert marker in agents
        assert marker in gates


def test_design_workflow_is_static_and_does_not_claim_gut_runtime() -> None:
    workflow = _text(WORKFLOW)
    assert "name: Validate HiGodot GUT Authority Gate" in workflow
    assert "authority-entry-contract:" in workflow
    assert "python -m pytest tests/test_higodot_gut_authority_gate.py -q" in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "fetch-depth: 0" in workflow
    assert "persist-credentials: false" in workflow
    assert "gut_cmdln.gd" not in workflow
    assert "--headless" not in workflow


def test_design_pr_change_surface_excludes_product_and_vendor_paths() -> None:
    if not (ROOT / ".git").exists():
        return
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    changed = {
        line.strip()
        for line in subprocess.run(
            ["git", "diff", "--name-only", f"{merge_base}..HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        if line.strip()
    }
    assert changed <= ALLOWED_CHANGED_PATHS, sorted(changed - ALLOWED_CHANGED_PATHS)
    assert not any(path.startswith(("addons/", "scenes/", "scripts/", "data/", "assets/")) for path in changed)
    assert "project.godot" not in changed
