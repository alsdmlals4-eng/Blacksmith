from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "testing" / "HIGODOT_GUT_AUTHORITY_POLICY.json"
HERA_PLUGIN = ROOT / "addons" / "hera_agent_godot" / "hera_agent_plugin.gd"
DECISION_ID = "BS-TOOLCHAIN-20260809-01"


def _policy() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def test_current_policy_records_approved_editor_plugins_without_expanding_authority() -> None:
    policy = _policy()
    assert DECISION_ID in policy["decision_ids"]

    higodot = policy["higodot"]
    assert higodot["installed_plugin_version"] == "3.1.3"
    assert higodot["policy_role"] == "SOLE_GODOT_AUTHORING_AUTHORITY"
    assert higodot["activation_scope"] == "TASK2_SCOPED_AUTHORING_ONLY"

    gut = policy["gut"]
    assert gut["project_plugin_enabled"] is True
    assert gut["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"

    hera = policy["hera"]
    assert hera["project_plugin_enabled"] is True
    assert hera["status"] == "VENDORED_PRESENT_ENABLED_NON_AUTHORITATIVE"
    assert hera["authoring_authority"] == "NONE"
    assert hera["plugin_activation_decision_id"] == DECISION_ID
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
