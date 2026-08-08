from __future__ import annotations

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


@pytest.mark.parametrize("path", [WORKFLOW, DRIVER, RECIPE, SCHEMA])
def test_bridge_surfaces_exist(path: Path) -> None:
    assert path.is_file(), f"missing bridge surface: {path.relative_to(ROOT)}"


def test_decision_records_reviewed_plan_and_fail_closed_boundary() -> None:
    text = _required_text(DECISION)
    assert DECISION_ID in text
    assert "WRITTEN_SPEC_REVIEW = APPROVED" in text
    assert "BRIDGE_TDD = RED_NEXT" in text
    assert "SCENE_PROJECT_MUTATION = 0" in text
    assert "Base generic Godot production adapter remains `NOT_READY`" in text
    assert "This Decision is not merge approval" in text


@pytest.mark.skipif(not WORKFLOW.is_file(), reason="bridge workflow intentionally absent at initial RED")
def test_workflow_is_manual_only_and_bound_to_exact_pr_head() -> None:
    text = _required_text(WORKFLOW)
    assert "workflow_dispatch:" in text
    assert "expected_head_sha:" in text
    assert TARGET_BRANCH in text
    assert "alsdmlals4-eng/Blacksmith" in text
    assert "PR #131" in text or "pr_number: 131" in text or "TARGET_PR=131" in text
    for forbidden_trigger in ("\n  pull_request:", "\n  push:", "\n  schedule:", "repository_dispatch:"):
        assert forbidden_trigger not in text


@pytest.mark.skipif(not WORKFLOW.is_file(), reason="bridge workflow intentionally absent at initial RED")
def test_workflow_separates_prove_read_from_publish_write() -> None:
    text = _required_text(WORKFLOW)
    assert "prove:" in text
    assert "publish:" in text
    assert "contents: read" in text
    assert "contents: write" in text
    assert "needs: prove" in text
    assert text.index("contents: read") < text.index("contents: write")


@pytest.mark.skipif(not WORKFLOW.is_file(), reason="bridge workflow intentionally absent at initial RED")
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


@pytest.mark.skipif(not RECIPE.is_file(), reason="bridge recipe intentionally absent at initial RED")
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


@pytest.mark.skipif(not SCHEMA.is_file(), reason="provenance schema intentionally absent at initial RED")
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


@pytest.mark.skipif(not DRIVER.is_file(), reason="bridge driver intentionally absent at initial RED")
def test_driver_declares_exact_authority_and_fail_closed_interfaces() -> None:
    text = _required_text(DRIVER)
    for marker in (
        "ALLOWED_SERIALIZED_PATHS",
        'MCP_URL = "http://127.0.0.1:8000/mcp"',
        'TARGET_REPOSITORY = "alsdmlals4-eng/Blacksmith"',
        "TARGET_PR = 131",
        f'TARGET_BRANCH = "{TARGET_BRANCH}"',
        "def validate_recipe(",
        "def verify_project_setting_delta(",
        "def verify_serialized_diff(",
        "def validate_provenance(",
        "async def run_prove(",
        "def run_publish_verify(",
        "from fastmcp import Client",
        "await client.list_tools()",
        "await client.call_tool(",
    ):
        assert marker in text
    for forbidden_claim in (
        "PRODUCTION_ADAPTER_READY = READY",
        "git push --force",
        "git rebase",
    ):
        assert forbidden_claim not in text


@pytest.mark.skipif(not WORKFLOW.is_file(), reason="bridge workflow intentionally absent at initial RED")
def test_publish_is_byte_identical_transport_not_second_authoring_pass() -> None:
    text = _required_text(WORKFLOW)
    publish = text[text.index("publish:") :]
    for forbidden in ("xvfb-run", "godot --", "godot-ai", "/mcp", "--force", " rebase "):
        assert forbidden not in publish
    for marker in ("expected_head_sha", "sha256", "artifact", "git push"):
        assert marker in publish
