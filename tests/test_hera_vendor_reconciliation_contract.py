from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
AGENTS = ROOT / "AGENTS.md"
DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
DEVELOPMENT_GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
RECONCILIATION = ROOT / "docs/operations/BLACKSMITH_HERA_VENDOR_RECONCILIATION_2026-08-08.md"
PROJECT = ROOT / "project.godot"
HERA_MANIFEST = ROOT / "addons/hera_agent_godot/plugin.cfg"

DECISION_ID = "BS-HERA-20260808-01"
TOOLCHAIN_DECISION_ID = "BS-TOOLCHAIN-20260809-01"
HIGODOT_DECISION_ID = "BS-HIGODOT-20260808-01"
HIGODOT_EXEC_DECISION_ID = "BS-HIGODOT-EXEC-20260808-01"
HISTORICAL_HERA_STATE = "VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE"
CURRENT_HERA_STATE = "VENDORED_PRESENT_ENABLED_NON_AUTHORITATIVE"
INTRODUCED_MAIN_COMMIT = "a5126d8a2091ce2350e50713eac614a045cc6ef2"
OBSERVED_MAIN = "2dddf864519a557152c6bbf0f0ee7fb94eadf11c"
MERGE_MAIN = "29b06e323185e436d709fcdf638f445b9099266e"
INITIALIZER_DECISION_ID = "BS-VS-INIT-20260808-01"


def _text(path: Path) -> str:
    assert path.is_file(), f"missing required Hera reconciliation surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(_text(path))


def test_historical_reconciliation_and_current_activation_decisions_are_both_preserved() -> None:
    reconciliation = _text(RECONCILIATION)
    assert DECISION_ID in reconciliation
    assert HISTORICAL_HERA_STATE in reconciliation
    for current_surface in (_text(AGENTS), _text(DECISIONS), _text(DEVELOPMENT_GATES)):
        assert DECISION_ID in current_surface
        assert TOOLCHAIN_DECISION_ID in current_surface


def test_policy_acknowledges_enabled_hera_without_granting_authority() -> None:
    policy = _json(POLICY)
    assert DECISION_ID in policy["decision_ids"]
    assert TOOLCHAIN_DECISION_ID in policy["decision_ids"]
    hera = policy["hera"]
    assert hera["decision_id"] == DECISION_ID
    assert hera["installed_path"] == "addons/hera_agent_godot"
    assert hera["installed_plugin_version"] == "1.0.0"
    assert hera["introduced_main_commit"] == INTRODUCED_MAIN_COMMIT
    assert hera["observed_current_main"] == OBSERVED_MAIN
    assert hera["status"] == CURRENT_HERA_STATE
    assert hera["project_plugin_enabled"] is True
    assert hera["plugin_activation_decision_id"] == TOOLCHAIN_DECISION_ID
    assert hera["authoring_authority"] == "NONE"
    assert hera["production_activation"] == "USER_APPROVED_EDITOR_PLUGIN_ENABLED_NON_AUTHORITATIVE"
    assert hera["mutation_permission"] == "NONE_UNLESS_SEPARATELY_SCOPED"
    assert hera["serialized_mutation_permission"] == "NONE_UNLESS_SEPARATELY_SCOPED"


def test_higodot_activation_preserves_gut_and_hera_authority_boundaries() -> None:
    policy = _json(POLICY)
    assert HIGODOT_DECISION_ID in policy["decision_ids"]
    assert HIGODOT_EXEC_DECISION_ID in policy["decision_ids"]
    assert policy["higodot"]["current_state"] == "FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY"
    assert policy["higodot"]["production_activation"] == "USER_APPROVED_ACTIVE"
    assert policy["higodot"]["activation_scope"] == "TASK2_SCOPED_AUTHORING_ONLY"
    assert policy["higodot"]["production_execution_path"] == "PROVEN_TASK2_COMPLETED"
    assert policy["gut"]["status"] == "FORMALLY_ADOPTED_ACTIVE"
    assert policy["gut"]["project_plugin_enabled"] is True
    assert policy["gut"]["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"
    assert policy["hera"]["project_plugin_enabled"] is True
    assert policy["hera"]["authoring_authority"] == "NONE"


def test_development_gates_match_current_tool_and_task_authority() -> None:
    gates = _text(DEVELOPMENT_GATES)
    for marker in (
        "R2_CHECKPOINT_005_CLOSED_MAIN_CANON",
        "HIGODOT_AUTHORING_AUTHORITY: FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY",
        "HIGODOT_PRODUCTION_ACTIVATION: USER_APPROVED_ACTIVE",
        "HIGODOT_PRODUCTION_EXECUTION_PATH: PROVEN_TASK2_COMPLETED",
        "GUT_TEST_AUTHORITY: FORMALLY_ADOPTED_ACTIVE",
        "GUT_CONFIG_PRESENT: true",
        "GUT_PROJECT_TEST_ROOT_PRESENT: true",
        "GUT_RUNTIME_CI: true",
        "GUT_FORMAL_AUTHORITY: FORMALLY_ADOPTED_ACTIVE",
        "TASK1: PR130_MERGED_MAIN_CANON",
        "PR122: CLOSED_SUPERSEDED_UNMERGED",
        f"PR132: MERGED_MAIN_CANON_{MERGE_MAIN}",
        f"INITIALIZER_DECISION: {INITIALIZER_DECISION_ID}",
        "INITIALIZER_AUTHORITY: RESOLVED_USER_APPROVED",
        HIGODOT_DECISION_ID,
        HIGODOT_EXEC_DECISION_ID,
        DECISION_ID,
        TOOLCHAIN_DECISION_ID,
        "HERA_AGENT_STATE: VENDORED_PRESENT_ENABLED_NON_AUTHORITATIVE",
        "HERA_AGENT_PLUGIN_ENABLED: true",
        "HERA_AGENT_AUTHORITY: NONE",
        "GUT_PLUGIN_ENABLED: true",
        "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED",
    ):
        assert marker in gates
    assert "VENDORED_PRESENT_FORMAL_ADOPTION_PENDING" not in gates
    assert "HERA_RECONCILIATION_DRAFT_PENDING_MERGE" not in gates


def test_project_activates_approved_editor_plugins_without_changing_authority() -> None:
    project = _text(PROJECT)
    for plugin in (
        "res://addons/godot_ai/plugin.cfg",
        "res://addons/gut/plugin.cfg",
        "res://addons/hera_agent_godot/plugin.cfg",
    ):
        assert plugin in project
    policy = _json(POLICY)
    assert policy["higodot"]["policy_role"] == "SOLE_GODOT_AUTHORING_AUTHORITY"
    assert policy["gut"]["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"
    assert policy["hera"]["authoring_authority"] == "NONE"


def test_hera_vendor_identity_is_pinned_to_observed_main_content() -> None:
    manifest = _text(HERA_MANIFEST)
    assert 'name="Hera Agent Godot"' in manifest
    assert 'version="1.0.0"' in manifest


def test_active_agent_rules_record_current_activation_without_expanding_hera_authority() -> None:
    agents = _text(AGENTS)
    assert "GUT 9.7.1" in agents
    assert "FORMALLY_ADOPTED_ACTIVE" in agents
    assert "VENDORED_PRESENT_FORMAL_ADOPTION_PENDING" not in agents
    assert HIGODOT_DECISION_ID in agents
    assert DECISION_ID in agents
    assert TOOLCHAIN_DECISION_ID in agents
    assert CURRENT_HERA_STATE in agents
    assert "Hera" in agents and "NONE" in agents
