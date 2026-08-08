from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "higodot-task2-authoring-bridge.yml"
DRIVER = ROOT / "tools" / "higodot_task2_bridge.py"
RECIPE = ROOT / ".github" / "validation" / "higodot-task2-authoring-recipe.json"
SCHEMA = ROOT / ".github" / "validation" / "higodot-task2-provenance-schema.json"
DECISION = ROOT / "docs" / "decisions" / "BS-HIGODOT-EXEC-20260808-01_TASK2_CI_AUTHORING_BRIDGE.md"
DECISION_ID = "BS-HIGODOT-EXEC-20260808-01"
TARGET_BRANCH = "feat/vertical-slice-task2-app-shell"
ALLOWED_SERIALIZED_PATHS = {
    "project.godot",
    "scenes/vertical_slice/main_menu.tscn",
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
}


def _required_text(path: Path) -> str:
    assert path.is_file(), f"missing bridge surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _load_driver():
    assert DRIVER.is_file(), f"missing bridge surface: {DRIVER.relative_to(ROOT)}"
    spec = importlib.util.spec_from_file_location("higodot_task2_bridge", DRIVER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _valid_recipe() -> dict:
    return {
        "schema_version": "1",
        "decision_id": DECISION_ID,
        "related_decision_ids": [
            "BS-HIGODOT-20260808-01",
            "BS-VS-TASK2-20260807-01",
            "BS-VS-INIT-20260808-01",
        ],
        "repository": "alsdmlals4-eng/Blacksmith",
        "pr_number": 131,
        "branch": TARGET_BRANCH,
        "godot_version": "4.7.1-stable",
        "higodot_version": "3.0.5",
        "mcp_url": "http://127.0.0.1:8000/mcp",
        "serialized_outputs": sorted(ALLOWED_SERIALIZED_PATHS),
        "operations": [
            {"tool": "scene_manage", "operation": "create", "scene": "res://scenes/vertical_slice/main_menu.tscn"},
            {"tool": "node_create", "operation": "create", "node_type": "Control"},
            {"tool": "node_set_property", "operation": "set", "property": "custom_minimum_size"},
            {"tool": "ui_manage", "operation": "layout", "minimum_control_size": [48, 48]},
            {"tool": "node_manage", "operation": "attach_script", "script": "res://scripts/vertical_slice/ui/vs_main_menu.gd"},
            {
                "tool": "project_manage",
                "operation": "settings_set",
                "setting": "application/run/main_scene",
                "value": "res://scenes/vertical_slice/main_menu.tscn",
            },
        ],
    }


def _valid_provenance_context(head: str) -> dict:
    return {
        "decision_ids": [
            DECISION_ID,
            "BS-HIGODOT-20260808-01",
            "BS-VS-TASK2-20260807-01",
        ],
        "repository": "alsdmlals4-eng/Blacksmith",
        "pr_number": 131,
        "input_head_sha": head,
        "godot": {"version": "4.7.1-stable"},
        "higodot": {"version": "3.0.5"},
        "server": {"version": "3.0.5"},
        "session": {"id": "session-1", "project_path": "/workspace/Blacksmith"},
        "changed_paths": sorted(ALLOWED_SERIALIZED_PATHS),
    }


@pytest.mark.parametrize("path", [DRIVER, RECIPE, SCHEMA])
def test_task2_infrastructure_surfaces_exist(path: Path) -> None:
    assert path.is_file(), f"missing Task 2 bridge infrastructure: {path.relative_to(ROOT)}"


def test_decision_records_reviewed_plan_and_fail_closed_boundary() -> None:
    text = _required_text(DECISION)
    assert DECISION_ID in text
    assert "WRITTEN_SPEC_REVIEW = APPROVED" in text
    assert "BRIDGE_TDD = RED_NEXT" in text
    assert "SCENE_PROJECT_MUTATION = 0" in text
    assert "Base generic Godot production adapter remains `NOT_READY`" in text
    assert "This Decision is not merge approval" in text


def test_recipe_is_exact_task2_scope_and_forbids_text_serialization_fallback() -> None:
    payload = json.loads(_required_text(RECIPE))
    assert payload["decision_id"] == DECISION_ID
    assert payload["repository"] == "alsdmlals4-eng/Blacksmith"
    assert payload["pr_number"] == 131
    assert payload["branch"] == TARGET_BRANCH
    assert payload["godot_version"] == "4.7.1-stable"
    assert payload["higodot_version"] == "3.0.5"
    assert set(payload["serialized_outputs"]) == ALLOWED_SERIALIZED_PATHS
    operations = json.dumps(payload.get("operations", []), sort_keys=True)
    for forbidden in ("filesystem_manage", "script_create", "script_patch"):
        assert forbidden not in operations
    assert "application/run/main_scene" in operations
    assert "res://scripts/vertical_slice/ui/vs_main_menu.gd" in operations
    assert "res://scripts/vertical_slice/ui/vs_app.gd" in operations


def test_provenance_schema_requires_identity_operations_hashes_and_validation() -> None:
    payload = json.loads(_required_text(SCHEMA))
    assert payload.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    assert payload.get("additionalProperties") is False
    required = set(payload.get("required", []))
    for field in (
        "decision_ids",
        "repository",
        "pr_number",
        "input_head_sha",
        "godot",
        "higodot",
        "server",
        "session",
        "operations",
        "changed_paths",
        "serialized_sha256",
        "validations",
        "artifact_sha256",
    ):
        assert field in required


def test_driver_declares_task2_pure_fail_closed_interfaces() -> None:
    text = _required_text(DRIVER)
    for marker in (
        "ALLOWED_SERIALIZED_PATHS",
        'MCP_URL = "http://127.0.0.1:8000/mcp"',
        'TARGET_REPOSITORY = "alsdmlals4-eng/Blacksmith"',
        "TARGET_PR = 131",
        f'TARGET_BRANCH = "{TARGET_BRANCH}"',
        "def load_recipe(",
        "def validate_recipe(",
        "def sha256_file(",
        "def git_changed_paths(",
        "def verify_project_setting_delta(",
        "def verify_serialized_diff(",
        "def build_provenance(",
        "def validate_provenance(",
    ):
        assert marker in text
    for forbidden_claim in (
        "from fastmcp import Client",
        "PRODUCTION_ADAPTER_READY = READY",
        "git push --force",
        "git rebase",
    ):
        assert forbidden_claim not in text


def test_validate_recipe_accepts_exact_identity_and_scope() -> None:
    driver = _load_driver()
    assert driver.validate_recipe(_valid_recipe()) is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("repository", "other/repo"),
        ("pr_number", 999),
        ("branch", "main"),
        ("godot_version", "4.6-stable"),
        ("higodot_version", "3.0.6"),
    ],
)
def test_validate_recipe_rejects_identity_drift(field: str, value: object) -> None:
    driver = _load_driver()
    recipe = _valid_recipe()
    recipe[field] = value
    with pytest.raises(ValueError):
        driver.validate_recipe(recipe)


def test_validate_recipe_rejects_scope_expansion_and_text_writer() -> None:
    driver = _load_driver()

    expanded = _valid_recipe()
    expanded["serialized_outputs"].append("scenes/vertical_slice/forbidden.tscn")
    with pytest.raises(ValueError):
        driver.validate_recipe(expanded)

    writer = _valid_recipe()
    writer["operations"].append({"tool": "filesystem_manage", "operation": "write_text"})
    with pytest.raises(ValueError):
        driver.validate_recipe(writer)


def test_verify_project_setting_delta_accepts_only_start_scene_change() -> None:
    driver = _load_driver()
    before = '[application]\nrun/main_scene="res://scenes/test/enhancement_test.tscn"\n[display]\nwindow/size/viewport_width=720\n'
    after = '[application]\nrun/main_scene="res://scenes/vertical_slice/main_menu.tscn"\n[display]\nwindow/size/viewport_width=720\n'
    assert driver.verify_project_setting_delta(before, after) is None


def test_verify_project_setting_delta_rejects_any_other_change() -> None:
    driver = _load_driver()
    before = '[application]\nrun/main_scene="res://scenes/test/enhancement_test.tscn"\n[display]\nwindow/size/viewport_width=720\n'
    after = '[application]\nrun/main_scene="res://scenes/vertical_slice/main_menu.tscn"\n[display]\nwindow/size/viewport_width=1080\n'
    with pytest.raises(ValueError):
        driver.verify_project_setting_delta(before, after)


def test_sha256_file_is_deterministic(tmp_path: Path) -> None:
    driver = _load_driver()
    path = tmp_path / "evidence.bin"
    path.write_bytes(b"blacksmith-bridge")
    assert driver.sha256_file(path) == hashlib.sha256(b"blacksmith-bridge").hexdigest()


def test_build_and_validate_provenance_binds_head_paths_hashes_and_validation() -> None:
    driver = _load_driver()
    head = "a" * 40
    hashes = {path: "b" * 64 for path in sorted(ALLOWED_SERIALIZED_PATHS)}
    operations = [{"tool": "scene_manage", "arguments_sha256": "c" * 64, "success": True, "result_sha256": "d" * 64, "error": None}]
    validations = {"focused_contract": {"status": "PASS", "sha256": "e" * 64}}
    payload = driver.build_provenance(_valid_provenance_context(head), operations, hashes, validations)
    payload["artifact_sha256"] = {"product_bundle": "f" * 64}

    assert driver.validate_provenance(payload, head) is None
    assert set(payload["serialized_sha256"]) == ALLOWED_SERIALIZED_PATHS
    assert set(payload["changed_paths"]) == ALLOWED_SERIALIZED_PATHS


def test_validate_provenance_rejects_wrong_head_and_output_set() -> None:
    driver = _load_driver()
    head = "a" * 40
    hashes = {path: "b" * 64 for path in sorted(ALLOWED_SERIALIZED_PATHS)}
    payload = driver.build_provenance(
        _valid_provenance_context(head),
        [],
        hashes,
        {"focused_contract": {"status": "PASS", "sha256": "e" * 64}},
    )
    payload["artifact_sha256"] = {"product_bundle": "f" * 64}

    with pytest.raises(ValueError):
        driver.validate_provenance(payload, "1" * 40)

    changed = copy.deepcopy(payload)
    changed["changed_paths"] = ["project.godot"]
    with pytest.raises(ValueError):
        driver.validate_provenance(changed, head)


@pytest.mark.skipif(not WORKFLOW.is_file(), reason="Task 3 workflow not implemented yet")
def test_workflow_is_manual_only_and_bound_to_exact_pr_head() -> None:
    text = _required_text(WORKFLOW)
    assert "workflow_dispatch:" in text
    assert "expected_head_sha:" in text
    assert TARGET_BRANCH in text
    assert "alsdmlals4-eng/Blacksmith" in text
    assert "PR #131" in text or "pr_number: 131" in text or "TARGET_PR=131" in text
    for forbidden_trigger in ("\n  pull_request:", "\n  push:", "\n  schedule:", "repository_dispatch:"):
        assert forbidden_trigger not in text


@pytest.mark.skipif(not WORKFLOW.is_file(), reason="Task 3 workflow not implemented yet")
def test_workflow_separates_prove_read_from_publish_write() -> None:
    text = _required_text(WORKFLOW)
    assert "prove:" in text
    assert "publish:" in text
    assert "contents: read" in text
    assert "contents: write" in text
    assert "needs: prove" in text
    assert text.index("contents: read") < text.index("contents: write")


@pytest.mark.skipif(not WORKFLOW.is_file(), reason="Task 3 workflow not implemented yet")
def test_mutation_runtime_is_xvfb_non_headless_and_version_bound() -> None:
    text = _required_text(WORKFLOW)
    assert "xvfb-run" in text
    assert "4.7.1" in text
    assert "3.0.5" in text
    assert "GODOT_AI_MODE" in text and "user" in text
    assert "GODOT_AI_DISABLE_TELEMETRY" in text
    mutation_lines = [line for line in text.splitlines() if "xvfb-run" in line or "author" in line.lower() and "godot" in line.lower()]
    assert mutation_lines, "missing non-headless authoring command"
    assert all("--headless" not in line for line in mutation_lines)


@pytest.mark.skipif(not WORKFLOW.is_file(), reason="Task 3 workflow not implemented yet")
def test_publish_is_byte_identical_transport_not_second_authoring_pass() -> None:
    text = _required_text(WORKFLOW)
    publish = text[text.index("publish:") :]
    for forbidden in ("xvfb-run", "godot --", "godot-ai", "/mcp", "--force", " rebase "):
        assert forbidden not in publish
    for marker in ("expected_head_sha", "sha256", "artifact", "git push"):
        assert marker in publish
