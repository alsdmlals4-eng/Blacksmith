from __future__ import annotations

import asyncio
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "higodot_task2_bridge.py"
RECIPE = ROOT / ".github" / "validation" / "higodot-task2-authoring-recipe.json"
PROJECT_PATH = "/workspace/Blacksmith"
SESSION_ID = "blacksmith@a3f2"


def _load_driver():
    spec = importlib.util.spec_from_file_location("higodot_task2_bridge", DRIVER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeClient:
    def __init__(self, tools: set[str], responses: dict[str, list[object]]):
        self.tools = set(tools)
        self.responses = {key: list(values) for key, values in responses.items()}
        self.calls: list[tuple[str, dict]] = []

    async def list_tool_names(self) -> set[str]:
        self.calls.append(("__list_tools__", {}))
        return set(self.tools)

    async def call(self, name: str, arguments: dict) -> dict:
        self.calls.append((name, arguments))
        values = self.responses.get(name, [])
        if not values:
            raise AssertionError(f"unexpected call: {name} {arguments}")
        value = values.pop(0)
        if isinstance(value, BaseException):
            raise value
        assert isinstance(value, dict)
        return value


def _session() -> dict:
    return {
        "session_id": SESSION_ID,
        "name": "Blacksmith",
        "godot_version": "4.7.1.stable.official",
        "project_path": PROJECT_PATH,
        "plugin_version": "3.0.5",
        "server_version": "3.0.5",
        "protocol_version": 1,
        "current_scene": "res://scenes/test/enhancement_test.tscn",
        "play_state": "stopped",
        "readiness": "ready",
        "editor_pid": 42,
        "server_launch_mode": "uvx",
        "connected_at": "2026-08-08T13:00:00+00:00",
        "last_seen": "2026-08-08T13:00:01+00:00",
        "is_active": False,
    }


def _preflight_responses(sessions: list[dict] | None = None) -> dict[str, list[object]]:
    return {
        "session_manage": [{"sessions": sessions or [_session()], "count": len(sessions or [_session()]), "exclude_domains": []}],
        "session_activate": [{"status": "ok", "active_session_id": SESSION_ID, "matched": "exact_id"}],
        "editor_state": [{
            "godot_version": "4.7.1.stable.official",
            "project_name": "Blacksmith",
            "current_scene": "res://scenes/test/enhancement_test.tscn",
            "is_playing": False,
            "readiness": "ready",
            "game_capture_ready": False,
            "game_status": {"status": "stopped"},
            "helper_live": False,
            "session_active": False,
        }],
        "scene_get_hierarchy": [{"nodes": [], "total_count": 0, "offset": 0, "limit": 100, "has_more": False}],
        "project_manage": [{"key": "application/run/main_scene", "value": "res://scenes/test/enhancement_test.tscn", "type": "String"}],
    }


def _required_tools(recipe: dict) -> set[str]:
    return {
        "session_manage",
        "session_activate",
        "editor_state",
        "scene_get_hierarchy",
        "project_manage",
        *(item["tool"] for item in recipe["operations"]),
    }


def test_recipe_uses_exact_305_executable_call_shape() -> None:
    payload = json.loads(RECIPE.read_text(encoding="utf-8"))
    assert payload["operations"]
    for item in payload["operations"]:
        assert set(item) == {"tool", "arguments"}, item
        assert isinstance(item["arguments"], dict)
    encoded = json.dumps(payload["operations"], sort_keys=True)
    assert '"tool": "node_manage"' not in encoded
    assert '"tool": "scene_save"' in encoded
    assert '"property": "script"' in encoded
    assert '"op": "set_anchor_preset"' in encoded
    assert '"preset": "full_rect"' in encoded


def test_preflight_orders_read_only_identity_checks_before_mutation() -> None:
    driver = _load_driver()
    recipe = driver.load_recipe(RECIPE)
    client = FakeClient(_required_tools(recipe), _preflight_responses())
    result = asyncio.run(driver.preflight_mcp(client, recipe, PROJECT_PATH))
    assert result["session_id"] == SESSION_ID
    assert result["project_setting"]["value"] == "res://scenes/test/enhancement_test.tscn"
    assert [name for name, _ in client.calls] == [
        "__list_tools__",
        "session_manage",
        "session_activate",
        "editor_state",
        "scene_get_hierarchy",
        "project_manage",
    ]
    assert client.calls[1][1] == {"op": "list", "params": {}}
    assert client.calls[2][1] == {"session_id": SESSION_ID}
    assert client.calls[5][1] == {
        "op": "settings_get",
        "params": {"key": "application/run/main_scene"},
        "session_id": SESSION_ID,
    }


def test_preflight_rejects_missing_required_tool_before_session_calls() -> None:
    driver = _load_driver()
    recipe = driver.load_recipe(RECIPE)
    tools = _required_tools(recipe) - {"ui_manage"}
    client = FakeClient(tools, _preflight_responses())
    with pytest.raises(ValueError, match="required MCP tools"):
        asyncio.run(driver.preflight_mcp(client, recipe, PROJECT_PATH))
    assert client.calls == [("__list_tools__", {})]


def test_preflight_rejects_ambiguous_project_sessions_before_activation() -> None:
    driver = _load_driver()
    recipe = driver.load_recipe(RECIPE)
    second = dict(_session(), session_id="blacksmith@b4e1", editor_pid=43)
    responses = _preflight_responses([_session(), second])
    client = FakeClient(_required_tools(recipe), responses)
    with pytest.raises(ValueError, match="exactly one"):
        asyncio.run(driver.preflight_mcp(client, recipe, PROJECT_PATH))
    assert [name for name, _ in client.calls] == ["__list_tools__", "session_manage"]


def test_preflight_rejects_version_or_readiness_drift_before_activation() -> None:
    driver = _load_driver()
    recipe = driver.load_recipe(RECIPE)
    bad = dict(_session(), plugin_version="3.0.6")
    client = FakeClient(_required_tools(recipe), _preflight_responses([bad]))
    with pytest.raises(ValueError, match="3.0.5"):
        asyncio.run(driver.preflight_mcp(client, recipe, PROJECT_PATH))
    assert [name for name, _ in client.calls] == ["__list_tools__", "session_manage"]


def test_recipe_operation_to_call_injects_session_without_mutating_recipe() -> None:
    driver = _load_driver()
    recipe = driver.load_recipe(RECIPE)
    item = recipe["operations"][0]
    original = json.dumps(item, sort_keys=True)
    name, arguments = driver.recipe_operation_to_call(item, SESSION_ID)
    assert name == item["tool"]
    assert arguments["session_id"] == SESSION_ID
    assert json.dumps(item, sort_keys=True) == original


def test_execute_recipe_records_canonical_success_evidence() -> None:
    driver = _load_driver()
    recipe = {
        "operations": [{"tool": "scene_manage", "arguments": {"op": "create", "params": {"path": "res://x.tscn", "root_type": "Control"}}}]
    }
    client = FakeClient({"scene_manage"}, {"scene_manage": [{"path": "res://x.tscn", "root_type": "Control"}]})
    evidence = asyncio.run(driver.execute_recipe_operations(client, recipe, SESSION_ID))
    assert len(evidence) == 1
    assert evidence[0]["tool"] == "scene_manage"
    assert evidence[0]["success"] is True
    assert len(evidence[0]["arguments_sha256"]) == 64
    assert len(evidence[0]["result_sha256"]) == 64
    assert evidence[0]["error"] is None


def test_mutation_timeout_is_read_back_once_and_never_blindly_retried() -> None:
    driver = _load_driver()
    recipe = {
        "operations": [{
            "tool": "project_manage",
            "arguments": {"op": "settings_set", "params": {"key": "application/run/main_scene", "value": "res://scenes/vertical_slice/main_menu.tscn"}},
        }]
    }
    client = FakeClient(
        {"project_manage"},
        {"project_manage": [TimeoutError("lost response"), {"key": "application/run/main_scene", "value": "res://scenes/vertical_slice/main_menu.tscn", "type": "String"}]},
    )
    with pytest.raises(driver.AmbiguousMutationError):
        asyncio.run(driver.execute_recipe_operations(client, recipe, SESSION_ID))
    assert [name for name, _ in client.calls] == ["project_manage", "project_manage"]
    assert client.calls[1][1]["op"] == "settings_get"


def test_fastmcp_adapter_is_lazy_and_uses_structured_data_contract() -> None:
    source = DRIVER.read_text(encoding="utf-8")
    assert 'importlib.import_module("fastmcp")' in source
    assert "class FastMCPBridgeClient" in source
    assert "result.data" in source
    assert "result.structured_content" in source
    assert "from fastmcp import Client" not in source
