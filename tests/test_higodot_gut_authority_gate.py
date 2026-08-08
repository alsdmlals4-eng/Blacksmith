from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "docs/planning/BLACKSMITH_HIGODOT_GUT_AUTHORITY_AND_ENTRY_GATE_SPEC_2026-08-06.md"
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
SNAPSHOT = ROOT / "docs/operations/BLACKSMITH_ENTRY_GATE_SNAPSHOT_2026-08-06.json"
WORKFLOW = ROOT / ".github/workflows/validate-higodot-gut-authority-gate.yml"
PYTHON_VALIDATION = ROOT / ".github/workflows/python-validation.yml"
AGENTS = ROOT / "AGENTS.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
FORMAL_ADOPTION_CONTRACT = ROOT / "tests/test_gut_formal_adoption_contract.py"
MANIFEST = ROOT / "docs/testing/GUT_9_7_1_FORMAL_ADOPTION_MANIFEST.json"

ADOPTION_MAIN_SHA = "2c4ae7eb244f1e6e01fd0392b747f8ffc3cee7eb"
VALIDATED_HEAD_SHA = "9ab46229946ae11529824fabefc6d558bd608d5d"
RUNTIME_RUN_ID = 31111242901
HIGODOT_ACTIVATION_DECISION = "BS-HIGODOT-20260808-01"

ALLOWED_CHANGED_PATHS = {
    str(SPEC.relative_to(ROOT)),
    str(POLICY.relative_to(ROOT)),
    str(SNAPSHOT.relative_to(ROOT)),
    str(WORKFLOW.relative_to(ROOT)),
    str(PYTHON_VALIDATION.relative_to(ROOT)),
    str(Path(__file__).relative_to(ROOT)),
    str(AGENTS.relative_to(ROOT)),
    str(GATES.relative_to(ROOT)),
}


def _text(path: Path) -> str:
    assert path.is_file(), f"missing required authority-gate surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(_text(path))


def test_policy_separates_active_test_authority_from_active_higodot_authority() -> None:
    policy = _json(POLICY)
    assert policy["schema_version"] == "1.1.0"
    assert policy["adoption_state"] == "FORMALLY_ADOPTED_ACTIVE_TEST_FRAMEWORK_AUTHORITY"
    assert policy["effective_scope"] == "MAIN_CANON_AUTHORITY_GATE_AND_GUT_RUNTIME"
    assert policy["adoption_main_sha"] == ADOPTION_MAIN_SHA
    assert HIGODOT_ACTIVATION_DECISION in policy["decision_ids"]
    assert policy["higodot"]["current_state"] == "FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY"
    assert policy["higodot"]["policy_role"] == "SOLE_GODOT_AUTHORING_AUTHORITY"
    assert policy["higodot"]["production_activation"] == "USER_APPROVED_ACTIVE"
    assert policy["higodot"]["activation_decision_id"] == HIGODOT_ACTIVATION_DECISION
    assert policy["higodot"]["activation_scope"] == "TASK2_SCOPED_AUTHORING_ONLY"
    assert policy["higodot"]["production_execution_path"] == "BLOCKED_UNAVAILABLE_OR_UNVERIFIED"
    assert policy["gut"]["status"] == "FORMALLY_ADOPTED_ACTIVE"
    assert policy["gut"]["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"
    assert policy["gut"]["official_version"] == "9.7.1"
    assert policy["gut"]["official_tag"] == "v9.7.1"
    assert policy["gut"]["official_tag_commit"] == "aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605"
    assert policy["gut"]["license"] == "MIT"
    assert policy["gut"]["godot_compatibility"] == "4.7.x"
    assert policy["gut"]["local_license_blob_sha"] == policy["gut"]["upstream_license_blob_sha"]
    assert policy["gut"]["project_plugin_enabled"] is False
    assert policy["gut"]["config_present"] is True
    assert policy["gut"]["project_gut_test_root_present"] is True
    assert policy["gut"]["formal_ci_authority"] is True


def test_policy_forbids_role_intrusion_and_defines_consumption_removal() -> None:
    policy = _json(POLICY)
    assert policy["conflict_rules"]["tracked_file_mutation_by_gut_runtime"] == "FORBIDDEN"
    assert policy["conflict_rules"]["higodot_edits_gut_tests_or_vendor_bytes"] == "FORBIDDEN"
    assert policy["conflict_rules"]["gut_edits_scene_resource_or_project_settings"] == "FORBIDDEN"
    assert policy["conflict_rules"]["same_file_dual_authority"] == "FORBIDDEN"
    assert policy["gut"]["consumption"] == {
        "vendor_root": "addons/gut",
        "config": ".gutconfig.json",
        "test_roots": ["res://tests/gut/unit", "res://tests/gut/integration"],
        "cli_entry": "res://addons/gut/gut_cmdln.gd",
        "result_format": "JUnit XML",
    }
    assert policy["ci"]["runtime_job"] == "gut-runtime-read-only"
    assert policy["ci"]["test_count_minimum"] == 1
    assert policy["ci"]["zero_tests"] == "FAIL"
    assert policy["ci"]["tracked_authoring_surface_hash_before_after"] == "REQUIRED"
    assert policy["ci"]["latest_validated_head_sha"] == VALIDATED_HEAD_SHA
    assert policy["ci"]["latest_runtime_run_id"] == RUNTIME_RUN_ID
    assert policy["removal"]["project_settings_change_authority"] == "HIGODOT_ONLY"
    assert policy["removal"]["preserve_historical_test_evidence"] is True


def test_entry_snapshot_rejects_false_ready_states_and_preserves_blockers() -> None:
    snapshot = _json(SNAPSHOT)
    assert snapshot["schema_version"] == "1.2.0"
    assert snapshot["snapshot_scope"] == "POSTMERGE_ADOPTION_CANON_CLOSURE"
    assert snapshot["source_main_sha_at_capture"] == ADOPTION_MAIN_SHA
    assert snapshot["general_product_implementation"] == "BLOCKED"
    assert snapshot["scoped_vertical_slice"] == "OPEN_ONLY_FOR_APPROVED_NAMESPACES"
    assert snapshot["pr_122"]["state"] == "OPEN_DRAFT_UNMERGED"
    # This dated snapshot is retained as historical evidence from before the 2026-08-08 activation.
    assert snapshot["higodot"] == "PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY"
    assert snapshot["gut"]["aggregate"] == "FORMALLY_ADOPTED_ACTIVE"
    assert snapshot["gut"]["plugin_enabled"] is False
    assert snapshot["gut"]["config_present"] is True
    assert snapshot["gut"]["project_test_root_present"] is True
    assert snapshot["gut"]["formal_ci_authority"] is True
    assert snapshot["gut"]["validated_head_sha"] == VALIDATED_HEAD_SHA
    assert snapshot["gut"]["runtime_run_id"] == RUNTIME_RUN_ID
    assert snapshot["sheet_schema_gate"]["aggregate"] == "SCHEMA_ALIGNMENT_REPAIRED_READBACK_PASS"
    assert snapshot["resolved_findings"]["71_이미지기획_생성목록"] == "SCHEMA_ALIGNMENT_REPAIRED_READBACK_PASS"
    assert snapshot["image_gate"]["aggregate"] == "BLOCKED_NOT_PRODUCT_READY"
    assert snapshot["image_gate"]["normalized_k2_status"] == "BLOCKED_IMAGE_NOT_GENERATED"
    assert "IMAGE_NOT_GENERATED" in snapshot["open_findings"]["BS-IMG-004"]
    assert "SOURCE_AND_LICENSE_NOT_RECORDED" in snapshot["open_findings"]["BS-IMG-005"]
    assert snapshot["corrected_sheet_states"]["01_작업순서!H2"] == "COMPLETE_MAIN_CANON"
    assert snapshot["corrected_sheet_states"]["01_작업순서!H3"] == "R1_COMPLETE_MAIN_CANON"
    assert "READY" in snapshot["forbidden_unqualified_states"]
    assert "AWAITING" in snapshot["forbidden_unqualified_states"]
    assert "IN_REVIEW" in snapshot["forbidden_unqualified_states"]
    assert snapshot["entry_decision"] == (
        "AUTHORITY_GATE_MAIN_CANON / GUT_FORMALLY_ADOPTED / "
        "VISUAL_GATE_BLOCKED / GENERAL_PRODUCT_BLOCKED"
    )


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

    for preserved_marker in (
        "VERTICAL_SLICE_IMPLEMENTATION_APPROVED",
        "R2_CHECKPOINT_005",
    ):
        assert preserved_marker in gates


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
    if FORMAL_ADOPTION_CONTRACT.is_file() or not (ROOT / ".git").exists():
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
            ["git", "-c", "core.quotepath=false", "diff", "--name-only", f"{merge_base}..HEAD"],
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


def test_postmerge_manifest_pins_main_and_latest_runtime_evidence() -> None:
    manifest = _json(MANIFEST)
    assert manifest["decision_id"] == "BS-TEST-20260806-01"
    assert manifest["adoption_status"] == "MAIN_CANON_ACTIVE_TEST_FRAMEWORK_AUTHORITY"
    assert manifest["adoption_main_sha"] == ADOPTION_MAIN_SHA
    runtime = manifest["runtime_validation"]
    assert runtime["main_base_validation_head_sha"] == VALIDATED_HEAD_SHA
    assert runtime["workflow_run_id"] == RUNTIME_RUN_ID
    assert runtime["result"] == "PASS"
    assert runtime["junit"] == {"tests": 1, "failures": 0, "errors": 0, "skipped": 0}
    assert runtime["tracked_authoring_surface_hash"] == "UNCHANGED"
