from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "higodot_task2_bridge.py"
RECIPE = ROOT / ".github" / "validation" / "higodot-task2-authoring-recipe.json"
WORKFLOW = ROOT / ".github" / "workflows" / "higodot-task2-authoring-bridge.yml"
PROJECT_PATH = "/workspace/Blacksmith"
HEAD = "a" * 40


def _load_driver():
    spec = importlib.util.spec_from_file_location("higodot_task2_bridge", DRIVER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run_prove_binds_preflight_mutations_and_provenance_context() -> None:
    from tests.test_higodot_task2_mcp_driver import FakeClient, _preflight_responses, _required_tools

    driver = _load_driver()
    recipe = driver.load_recipe(RECIPE)
    responses = _preflight_responses()
    for index, item in enumerate(recipe["operations"]):
        responses.setdefault(item["tool"], []).append({"status": "ok", "operation_index": index})
    client = FakeClient(_required_tools(recipe), responses)

    result = asyncio.run(driver.run_prove(client, recipe, PROJECT_PATH, HEAD))

    assert set(result) == {"context", "operations"}
    context = result["context"]
    assert context["input_head_sha"] == HEAD
    assert context["repository"] == "alsdmlals4-eng/Blacksmith"
    assert context["pr_number"] == 131
    assert context["godot"] == {"version": "4.7.1-stable"}
    assert context["higodot"] == {"version": "3.0.5"}
    assert context["server"] == {"version": "3.0.5"}
    assert context["session"]["id"] == "blacksmith@a3f2"
    assert context["session"]["project_path"] == PROJECT_PATH
    assert set(context["changed_paths"]) == set(driver.ALLOWED_SERIALIZED_PATHS)
    assert len(result["operations"]) == len(recipe["operations"])
    assert all(record["success"] is True for record in result["operations"])


def test_driver_exposes_fail_closed_real_prove_cli() -> None:
    source = DRIVER.read_text(encoding="utf-8")
    for marker in (
        "async def run_prove(",
        "def write_prove_evidence(",
        'choices=["prove"]',
        "FastMCPBridgeClient",
        "asyncio.run",
        "session-context.json",
        "operation-evidence.json",
        'if __name__ == "__main__":',
    ):
        assert marker in source, marker


def test_workflow_invokes_real_prove_before_serialized_diff_validation() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    prove = text[text.index("prove:") : text.index("publish:")]
    for marker in (
        "python tools/higodot_task2_bridge.py prove",
        ".github/validation/higodot-task2-authoring-recipe.json",
        "artifacts/higodot-task2/session-context.json",
        "artifacts/higodot-task2/operation-evidence.json",
        "EXPECTED_HEAD_SHA",
        "EDITOR_PID",
        "kill \"$EDITOR_PID\"",
    ):
        assert marker in prove, marker
    assert "--quit-after 2" not in prove
    assert prove.index("python tools/higodot_task2_bridge.py prove") < prove.index("verify_serialized_diff")


def test_workflow_pins_uv_for_higodot_plugin_server_startup() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    prove = text[text.index("prove:") : text.index("publish:")]
    assert '"uv==0.12.3"' in prove
    assert "uv --version" in prove
    assert "uvx --version" in prove
