from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_CFG = ROOT / "addons/godot_ai/plugin.cfg"
PLUGIN = ROOT / "addons/godot_ai/plugin.gd"
PROJECT_HANDLER = ROOT / "addons/godot_ai/handlers/project_handler.gd"
PROJECT = ROOT / "project.godot"
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
DECISION = ROOT / "docs/decisions/BS-TOOLCHAIN-20260811-02_GODOT_AI_314_CURRENT_VENDOR_ALIGNMENT.md"
HISTORICAL_BRIDGE = ROOT / "tools/higodot_task2_bridge.py"
HISTORICAL_DECISION = ROOT / "docs/decisions/BS-TOOLCHAIN-20260809-01_GODOT_AI_313_HERA_GUT_PLUGIN_ACTIVATION.md"

CURRENT_DECISION_ID = "BS-TOOLCHAIN-20260811-02"
HISTORICAL_DECISION_ID = "BS-TOOLCHAIN-20260809-01"
UPSTREAM_TAG_COMMIT = "96cc8b8c3d25ce487e24801d01d5214fea150349"
UPSTREAM_ADDON_TREE = "69010571e11123dfc4e09483f80cb9e6ca93511a"
CURRENT_VERSION = "3.1.4"
HISTORICAL_TASK2_VERSION = "3.1.3"
EXPECTED_MAIN_SCENE = "res://scenes/vertical_slice/main_menu.tscn"


def _text(path: Path) -> str:
    assert path.is_file(), f"missing current alignment surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _plugin_version() -> str:
    match = re.search(r'^version="([^"]+)"$', _text(PLUGIN_CFG), re.MULTILINE)
    assert match is not None
    return match.group(1)


def test_current_vendor_is_314_and_new_decision_records_official_identity() -> None:
    assert _plugin_version() == CURRENT_VERSION
    decision = _text(DECISION)
    for token in (
        CURRENT_DECISION_ID,
        "GODOT_AI_314_CURRENT_VENDOR_ALIGNMENT",
        "v3.1.4",
        UPSTREAM_TAG_COMMIT,
        UPSTREAM_ADDON_TREE,
        "EXACT_UPSTREAM_V3_1_4",
        "PRODUCT_IMPLEMENTATION: BLOCKED",
        "TASK3_IMPLEMENTATION: NOT_APPROVED",
    ):
        assert token in decision


def test_current_policy_distinguishes_314_vendor_from_313_task2_history() -> None:
    policy = json.loads(_text(POLICY))
    assert CURRENT_DECISION_ID in policy["decision_ids"]
    assert HISTORICAL_DECISION_ID in policy["decision_ids"]

    higodot = policy["higodot"]
    assert higodot["installed_plugin_version"] == CURRENT_VERSION
    assert higodot["current_version_decision_id"] == CURRENT_DECISION_ID
    assert higodot["upstream_tag"] == "v3.1.4"
    assert higodot["upstream_tag_commit"] == UPSTREAM_TAG_COMMIT
    assert higodot["upstream_vendor_tree_sha"] == UPSTREAM_ADDON_TREE
    assert higodot["vendor_alignment"] == "EXACT_UPSTREAM_V3_1_4"
    assert higodot["historical_task2_toolchain_version"] == HISTORICAL_TASK2_VERSION
    assert higodot["task2_only_main_scene_vendor_overlay"] == "HISTORICAL_PROVEN_RETIRED_FROM_CURRENT_VENDOR"
    assert higodot["future_main_scene_mutation"] == "NEW_SCOPE_DECISION_REQUIRED"
    assert higodot["policy_role"] == "SOLE_GODOT_AUTHORING_AUTHORITY"
    assert higodot["activation_scope"] == "TASK2_SCOPED_AUTHORING_ONLY"

    assert policy["gut"]["official_version"] == "9.7.1"
    assert policy["gut"]["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"
    assert policy["hera"]["authoring_authority"] == "NONE"
    assert policy["remaining_blockers"]["general_product_implementation"] == "BLOCKED"


def test_current_upstream_vendor_keeps_generic_main_scene_guard_without_retired_raw_overlay() -> None:
    plugin = _text(PLUGIN)
    handler = _text(PROJECT_HANDLER)
    project = _text(PROJECT)

    assert '"application/run/main_scene"' in handler
    assert "STARTUP_EXECUTION_KEYS_EXACT" in handler
    assert "func set_main_scene(params: Dictionary)" not in handler
    assert '_dispatcher.register_lazy("set_main_scene", "project", &"set_main_scene")' not in plugin
    assert f'run/main_scene="{EXPECTED_MAIN_SCENE}"' in project


def test_completed_task2_313_execution_evidence_is_preserved_as_history() -> None:
    historical_decision = _text(HISTORICAL_DECISION)
    bridge = _text(HISTORICAL_BRIDGE)

    assert HISTORICAL_DECISION_ID in historical_decision
    assert "GODOT_AI_TARGET_VERSION = 3.1.3" in historical_decision
    assert 'TARGET_HIGODOT_VERSION = "3.1.3"' in bridge
    assert CURRENT_DECISION_ID not in historical_decision
    assert 'TARGET_HIGODOT_VERSION = "3.1.4"' not in bridge
