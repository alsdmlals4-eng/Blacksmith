from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
AGENTS = ROOT / "AGENTS.md"
RECONCILIATION = ROOT / "docs/operations/BLACKSMITH_HERA_VENDOR_RECONCILIATION_2026-08-08.md"
PROJECT = ROOT / "project.godot"
HERA_MANIFEST = ROOT / "addons/hera_agent_godot/plugin.cfg"

DECISION_ID = "BS-HERA-20260808-01"
HERA_STATE = "VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE"
INTRODUCED_MAIN_COMMIT = "a5126d8a2091ce2350e50713eac614a045cc6ef2"
OBSERVED_MAIN = "ddb914f7e70e0deb62f5840fb990eb471eb7f441"


def _text(path: Path) -> str:
    assert path.is_file(), f"missing required Hera reconciliation surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(_text(path))


def test_same_decision_id_is_present_in_active_canon_and_reconciliation_evidence() -> None:
    assert DECISION_ID in _text(AGENTS)
    assert DECISION_ID in _text(RECONCILIATION)


def test_policy_acknowledges_hera_without_granting_authority() -> None:
    policy = _json(POLICY)
    assert DECISION_ID in policy["decision_ids"]
    hera = policy["hera"]
    assert hera["decision_id"] == DECISION_ID
    assert hera["installed_path"] == "addons/hera_agent_godot"
    assert hera["installed_plugin_version"] == "1.0.0"
    assert hera["introduced_main_commit"] == INTRODUCED_MAIN_COMMIT
    assert hera["observed_current_main"] == OBSERVED_MAIN
    assert hera["status"] == HERA_STATE
    assert hera["project_plugin_enabled"] is False
    assert hera["authoring_authority"] == "NONE"
    assert hera["production_activation"] == "REQUIRES_SEPARATE_USER_APPROVED_ADOPTION"
    assert hera["mutation_permission"] == "NONE_UNTIL_SEPARATE_ADOPTION"


def test_existing_higodot_and_gut_authorities_are_preserved() -> None:
    policy = _json(POLICY)
    assert policy["higodot"]["current_state"] == "PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY"
    assert policy["higodot"]["production_activation"] == "PENDING_SEPARATE_APPROVAL"
    assert policy["gut"]["status"] == "FORMALLY_ADOPTED_ACTIVE"
    assert policy["gut"]["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"


def test_project_does_not_activate_hera_and_keeps_current_higodot_plugin() -> None:
    project = _text(PROJECT)
    assert 'res://addons/godot_ai/plugin.cfg' in project
    assert 'res://addons/hera_agent_godot/plugin.cfg' not in project


def test_hera_vendor_identity_is_pinned_to_observed_main_content() -> None:
    manifest = _text(HERA_MANIFEST)
    assert 'name="Hera Agent Godot"' in manifest
    assert 'version="1.0.0"' in manifest


def test_active_agent_rules_no_longer_claim_gut_adoption_is_pending() -> None:
    agents = _text(AGENTS)
    assert "GUT 9.7.1" in agents
    assert "FORMALLY_ADOPTED_ACTIVE" in agents
    assert "VENDORED_PRESENT_FORMAL_ADOPTION_PENDING" not in agents
    assert DECISION_ID in agents
    assert HERA_STATE in agents
