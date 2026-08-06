from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "docs/superpowers/specs/2026-08-06-higodot-gut-authority-and-entry-gates-design.md"
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
SNAPSHOT = ROOT / "docs/operations/BLACKSMITH_ENTRY_GATE_SNAPSHOT_2026-08-06.json"
WORKFLOW = ROOT / ".github/workflows/validate-higodot-gut-authority-gate.yml"
AGENTS = ROOT / "AGENTS.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"

ALLOWED_CHANGED_PATHS = {
    str(DESIGN.relative_to(ROOT)),
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


def test_policy_separates_authoring_and_testing_authorities() -> None:
    policy = _json(POLICY)
    assert policy["schema_version"] == "1.0.0"
    assert policy["adoption_state"] == "DESIGN_REVIEW_REQUIRED"
    assert policy["higodot"]["current_state"] == "PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY"
    assert policy["higodot"]["target_role"] == "SOLE_GODOT_AUTHORING_AUTHORITY"
    assert policy["higodot"]["installed_plugin_version"] == "3.0.5"
    assert policy["gut"]["status"] == "NOT_INSTALLED_DESIGN_ONLY"
    assert policy["gut"]["target_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"
    assert policy["gut"]["version"] == "9.7.1"
    assert policy["gut"]["tag"] == "v9.7.1"
    assert policy["gut"]["commit"] == "aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605"
    assert policy["gut"]["license"] == "MIT"
    assert policy["gut"]["godot_compatibility"] == "4.7.x"
    assert policy["conflict_rules"]["tracked_file_mutation_by_gut_runtime"] == "FORBIDDEN"
    assert policy["conflict_rules"]["higodot_edits_gut_tests_or_vendor_bytes"] == "FORBIDDEN"
    assert policy["conflict_rules"]["gut_edits_scene_resource_or_project_settings"] == "FORBIDDEN"


def test_policy_defines_real_consumption_ci_and_removal() -> None:
    policy = _json(POLICY)
    assert policy["gut"]["planned_consumption"] == {
        "vendor_root": "addons/gut",
        "config": ".gutconfig.json",
        "test_roots": ["res://tests/gut/unit", "res://tests/gut/integration"],
        "cli_entry": "res://addons/gut/gut_cmdln.gd",
        "result_format": "JUnit XML",
    }
    assert policy["ci"]["design_contract_job"] == "authority-entry-contract"
    assert policy["ci"]["planned_runtime_job"] == "gut-runtime-read-only"
    assert policy["ci"]["tracked_authoring_surface_hash_before_after"] == "REQUIRED"
    assert policy["removal"]["project_settings_change_authority"] == "HIGODOT_ONLY"
    assert policy["removal"]["preserve_historical_test_evidence"] is True


def test_entry_snapshot_blocks_false_ready_or_awaiting_states() -> None:
    snapshot = _json(SNAPSHOT)
    assert snapshot["source_main_sha"] == "07f77041f85bde223768128949ad8dc587d5a003"
    assert snapshot["scoped_vertical_slice"] == "OPEN_ONLY_FOR_APPROVED_NAMESPACES"
    assert snapshot["general_product_implementation"] == "BLOCKED"
    assert snapshot["pr_122"] == {
        "state": "OPEN_DRAFT_UNMERGED",
        "head_sha": "f4568468c2c04f29ea1472e2ac12329447f1a365",
    }
    assert snapshot["higodot"] == "PILOT_ONLY_NOT_PRODUCTION_READY"
    assert snapshot["gut_adoption"] == "BLOCKED_DESIGN_REVIEW_REQUIRED"
    assert snapshot["image_gate"]["aggregate"] == "BLOCKED_NOT_PRODUCT_READY"
    assert snapshot["image_gate"]["image_generated"] == "NOT_RUN"
    assert snapshot["image_gate"]["rights_verified"] == "NOT_RUN"
    assert snapshot["image_gate"]["runtime_verified"] == "NOT_RUN"
    assert snapshot["stale_sheet_cells"]["00_프로젝트_허브!E2"] == "R0_CANONICAL_RECOVERY_IN_PROGRESS"
    assert snapshot["stale_sheet_cells"]["01_작업순서!H3"] == "NOT_STARTED"
    assert snapshot["stale_sheet_cells"]["01_작업순서!H4"] == "BLOCKED_BY_R0_AND_PRIOR_BUNDLES"
    assert snapshot["corrected_gate_states"]["00_프로젝트_허브!E2"].startswith("R2_BATCH_006")
    assert snapshot["corrected_gate_states"]["72_이미지검수_승인로그!K2"] == "BLOCKED_IMAGE_NOT_GENERATED"
    assert "READY" not in snapshot["permitted_aggregate_states"]
    assert "AWAITING" not in snapshot["permitted_aggregate_states"]


def test_design_and_authority_surfaces_have_required_markers() -> None:
    design = _text(DESIGN)
    for marker in (
        "HIGODOT_SOLE_AUTHORING_AUTHORITY",
        "GUT_SOLE_TEST_AUTHORITY",
        "GUT_9_7_1_DESIGN_ONLY",
        "ENTRY_GATE_FAIL_CLOSED",
        "PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY",
        "GUT_RUNTIME_TRACKED_MUTATION_FORBIDDEN",
        "REMOVAL_BY_SEPARATE_REVIEWED_CHANGE",
        "NO_PRODUCT_PATH_CHANGE",
    ):
        assert marker in design

    agents = _text(AGENTS)
    gates = _text(GATES)
    for marker in (
        "HIGODOT_SOLE_AUTHORING_AUTHORITY",
        "GUT_SOLE_TEST_AUTHORITY",
        "ENTRY_GATE_FAIL_CLOSED",
    ):
        assert marker in agents
        assert marker in gates


def test_workflow_validates_design_without_installing_gut() -> None:
    workflow = _text(WORKFLOW)
    assert "name: Validate HiGodot GUT Authority Gate" in workflow
    assert "authority-entry-contract:" in workflow
    assert "python -m pytest tests/test_higodot_gut_authority_gate.py -q" in workflow
    assert "permissions:\n  contents: read" in workflow
    assert "fetch-depth: 0" in workflow
    assert "persist-credentials: false" in workflow
    assert "addons/gut" not in workflow
    assert "gut_cmdln.gd" not in workflow


def test_design_pr_change_surface_excludes_product_and_gut_vendor_paths() -> None:
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
