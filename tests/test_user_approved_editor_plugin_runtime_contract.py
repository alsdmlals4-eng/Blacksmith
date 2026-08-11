from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "testing" / "HIGODOT_GUT_AUTHORITY_POLICY.json"
HERA_PLUGIN = ROOT / "addons" / "hera_agent_godot" / "hera_agent_plugin.gd"
HIGODOT_PLUGIN = ROOT / "addons" / "godot_ai" / "plugin.gd"
HIGODOT_PROJECT_HANDLER = ROOT / "addons" / "godot_ai" / "handlers" / "project_handler.gd"
HIGODOT_TOOL_CATALOG = ROOT / "addons" / "godot_ai" / "tool_catalog.gd"
ACTIVATION_DECISION_ID = "BS-TOOLCHAIN-20260809-01"
CURRENT_VERSION_DECISION_ID = "BS-TOOLCHAIN-20260811-02"


def _policy() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def test_current_policy_records_approved_editor_plugins_without_expanding_authority() -> None:
    policy = _policy()
    assert ACTIVATION_DECISION_ID in policy["decision_ids"]
    assert CURRENT_VERSION_DECISION_ID in policy["decision_ids"]

    higodot = policy["higodot"]
    assert higodot["installed_plugin_version"] == "3.1.4"
    assert higodot["current_version_decision_id"] == CURRENT_VERSION_DECISION_ID
    assert higodot["vendor_alignment"] == "EXACT_UPSTREAM_V3_1_4"
    assert higodot["historical_task2_toolchain_version"] == "3.1.3"
    assert higodot["policy_role"] == "SOLE_GODOT_AUTHORING_AUTHORITY"
    assert higodot["activation_scope"] == "TASK2_SCOPED_AUTHORING_ONLY"

    gut = policy["gut"]
    assert gut["project_plugin_enabled"] is True
    assert gut["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"

    hera = policy["hera"]
    assert hera["project_plugin_enabled"] is True
    assert hera["status"] == "VENDORED_PRESENT_ENABLED_NON_AUTHORITATIVE"
    assert hera["authoring_authority"] == "NONE"
    assert hera["plugin_activation_decision_id"] == ACTIVATION_DECISION_ID
    assert hera["serialized_mutation_permission"] == "NONE_UNLESS_SEPARATELY_SCOPED"


def test_hera_exits_headless_before_ui_autoload_or_server_construction() -> None:
    source = HERA_PLUGIN.read_text(encoding="utf-8")
    enter = source[source.index("func _enter_tree() -> void:") : source.index("func _process(")]

    guard = 'DisplayServer.get_name() == "headless"'
    assert guard in enter
    guard_index = enter.index(guard)

    for forbidden_before_guard in (
        "set_process(true)",
        "_create_main_screen()",
        "_ensure_game_autoload()",
        "_registry = ToolRegistry.new()",
        "_server = HttpServer.new()",
    ):
        assert guard_index < enter.index(forbidden_before_guard), forbidden_before_guard


def test_current_upstream_314_retires_task2_raw_main_scene_overlay_and_keeps_generic_guard() -> None:
    policy = _policy()
    plugin = HIGODOT_PLUGIN.read_text(encoding="utf-8")
    project_handler = HIGODOT_PROJECT_HANDLER.read_text(encoding="utf-8")
    tool_catalog = HIGODOT_TOOL_CATALOG.read_text(encoding="utf-8")

    assert (
        policy["higodot"]["task2_only_main_scene_vendor_overlay"]
        == "HISTORICAL_PROVEN_RETIRED_FROM_CURRENT_VENDOR"
    )
    assert policy["higodot"]["future_main_scene_mutation"] == "NEW_SCOPE_DECISION_REQUIRED"

    assert '"application/run/main_scene"' in project_handler
    assert "STARTUP_EXECUTION_KEYS_EXACT" in project_handler
    assert "func set_main_scene(params: Dictionary) -> Dictionary:" not in project_handler
    assert (
        '_dispatcher.register_lazy("set_main_scene", "project", &"set_main_scene")'
        not in plugin
    )

    project_domain = (
        '{"id": "project", "label": "project", "count": 2, '
        '"tools": ["project_manage", "project_run"]}'
    )
    assert project_domain in tool_catalog
    assert "set_main_scene" not in tool_catalog
