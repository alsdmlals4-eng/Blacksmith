from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "project.godot"
GODOT_AI_PLUGIN = ROOT / "addons/godot_ai/plugin.cfg"
DECISION = ROOT / "docs/decisions/BS-TOOLCHAIN-20260809-01_GODOT_AI_313_HERA_GUT_PLUGIN_ACTIVATION.md"
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"

EXPECTED_EDITOR_PLUGINS = {
    "res://addons/godot_ai/plugin.cfg",
    "res://addons/hera_agent_godot/plugin.cfg",
    "res://addons/gut/plugin.cfg",
}


def _text(path: Path) -> str:
    assert path.is_file(), f"missing approved toolchain surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _godot_ai_version() -> str:
    match = re.search(r'^version="([^"]+)"$', _text(GODOT_AI_PLUGIN), re.MULTILINE)
    assert match is not None, "addons/godot_ai/plugin.cfg has no exact version field"
    return match.group(1)


def _enabled_editor_plugins() -> set[str]:
    project = _text(PROJECT)
    match = re.search(r'^enabled=PackedStringArray\((.*)\)$', project, re.MULTILINE)
    assert match is not None, "project.godot has no editor_plugins enabled array"
    return set(re.findall(r'"([^"]+)"', match.group(1)))


def test_github_vendor_matches_user_approved_godot_ai_313() -> None:
    assert _godot_ai_version() == "3.1.3"


def test_github_project_enables_exact_user_approved_editor_plugins() -> None:
    assert _enabled_editor_plugins() == EXPECTED_EDITOR_PLUGINS


def test_plugin_enablement_does_not_expand_authoring_authority() -> None:
    decision = _text(DECISION)
    assert "BS-TOOLCHAIN-20260809-01" in decision
    assert "GODOT_AI_TARGET_VERSION = 3.1.3" in decision
    assert "HERA_EDITOR_PLUGIN_ENABLEMENT = USER_APPROVED" in decision
    assert "GUT_EDITOR_PLUGIN_ENABLEMENT = USER_APPROVED" in decision
    assert "HERA_AUTHORING_AUTHORITY = NONE_UNLESS_SEPARATELY_SCOPED" in decision
    assert "GUT_TEST_AUTHORITY = FORMALLY_ADOPTED_ACTIVE / SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY" in decision

    policy = json.loads(_text(POLICY))
    assert policy["higodot"]["current_state"] == "FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY"
    assert policy["higodot"]["activation_scope"] == "TASK2_SCOPED_AUTHORING_ONLY"
    assert policy["gut"]["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"
    assert policy["hera"]["authoring_authority"] == "NONE"
