from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "project.godot"
GODOT_AI_PLUGIN = ROOT / "addons/godot_ai/plugin.cfg"
ACTIVATION_DECISION = ROOT / "docs/decisions/BS-TOOLCHAIN-20260809-01_GODOT_AI_313_HERA_GUT_PLUGIN_ACTIVATION.md"
CURRENT_VERSION_DECISION = ROOT / "docs/decisions/BS-TOOLCHAIN-20260811-02_GODOT_AI_314_CURRENT_VENDOR_ALIGNMENT.md"
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


def test_github_vendor_matches_user_approved_current_godot_ai_314() -> None:
    assert _godot_ai_version() == "3.1.4"
    current = _text(CURRENT_VERSION_DECISION)
    assert "BS-TOOLCHAIN-20260811-02" in current
    assert "VENDOR_ALIGNMENT: EXACT_UPSTREAM_V3_1_4" in current


def test_github_project_enables_exact_user_approved_editor_plugins() -> None:
    assert _enabled_editor_plugins() == EXPECTED_EDITOR_PLUGINS


def test_current_version_alignment_preserves_historical_activation_and_authority_boundaries() -> None:
    activation = _text(ACTIVATION_DECISION)
    current = _text(CURRENT_VERSION_DECISION)

    assert "BS-TOOLCHAIN-20260809-01" in activation
    assert "GODOT_AI_TARGET_VERSION = 3.1.3" in activation
    assert "HERA_EDITOR_PLUGIN_ENABLEMENT = USER_APPROVED" in activation
    assert "GUT_EDITOR_PLUGIN_ENABLEMENT = USER_APPROVED" in activation
    assert "HERA_AUTHORING_AUTHORITY = NONE_UNLESS_SEPARATELY_SCOPED" in activation
    assert "GUT_TEST_AUTHORITY = FORMALLY_ADOPTED_ACTIVE / SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY" in activation

    assert "CURRENT_GODOT_AI_VERSION: 3.1.4" in current
    assert "Historical Task2 toolchain version remains `3.1.3`" in current

    policy = json.loads(_text(POLICY))
    assert policy["higodot"]["installed_plugin_version"] == "3.1.4"
    assert policy["higodot"]["current_state"] == "FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY"
    assert policy["higodot"]["activation_scope"] == "TASK2_SCOPED_AUTHORING_ONLY"
    assert policy["gut"]["authority_role"] == "SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY"
    assert policy["hera"]["authoring_authority"] == "NONE"
