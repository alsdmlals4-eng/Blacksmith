from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_C0_SHA = "2b595570bd237174b2b962a1eb54588b5ecc508d"
GODOT_ARCHIVE_SHA256 = "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba"
DESCRIPTOR = ROOT / ".godot-live-editor/project-pilot.json"
ADOPTION_DOC = ROOT / "docs/GODOT_LIVE_EDITOR_ADOPTION.md"
WORKFLOW = ROOT / ".github/workflows/validate-godot-live-editor-pilot.yml"
ALLOWED_PATHS = {
    ".github/workflows/validate-godot-live-editor-pilot.yml",
    ".godot-live-editor/project-pilot.json",
    "docs/GODOT_LIVE_EDITOR_ADOPTION.md",
    "tests/test_godot_live_editor_adoption.py",
}


def _text(path: Path) -> str:
    assert path.is_file(), f"missing adoption surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _changed_paths() -> set[str]:
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/main"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    output = subprocess.run(
        ["git", "diff", "--name-only", f"{merge_base}..HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return {line.strip() for line in output.splitlines() if line.strip()}


def test_descriptor_is_exact_blacksmith_boundary() -> None:
    payload = json.loads(_text(DESCRIPTOR))
    assert payload["project_identity"] == {
        "repository": "alsdmlals4-eng/Blacksmith",
        "project_id": "blacksmith",
    }
    assert payload["base_pilot_commit"] == BASE_C0_SHA
    assert payload["godot"] == {
        "version": "4.7.1-stable",
        "archive_sha256": GODOT_ARCHIVE_SHA256,
    }
    assert payload["main_scene_source"] == "application/run/main_scene"
    assert payload["legacy_editor_plugins"] == ["res://addons/godot_ai/plugin.cfg"]
    assert payload["legacy_autoloads"] == ["_mcp_game_helper"]
    assert payload["legacy_disable_mode"] == "TEMPORARY_COPY_ONLY"
    assert payload["source_mutation_policy"] == "FORBIDDEN"
    assert payload["expected_platform"] == "ANDROID_MOBILE"


def test_source_legacy_authority_and_main_scene_remain_installed() -> None:
    project = _text(ROOT / "project.godot")
    assert 'run/main_scene="res://scenes/test/enhancement_test.tscn"' in project
    assert '_mcp_game_helper="*res://addons/godot_ai/runtime/game_helper.gd"' in project
    assert 'enabled=PackedStringArray("res://addons/godot_ai/plugin.cfg")' in project
    assert (ROOT / "addons/godot_ai/plugin.cfg").is_file()


def test_workflow_and_document_pin_the_same_immutable_base() -> None:
    workflow = _text(WORKFLOW)
    document = _text(ADOPTION_DOC)
    assert workflow.count(BASE_C0_SHA) == 2
    assert f"base_pilot_commit: {BASE_C0_SHA}" in document
    assert "TEMPORARY_COPY_ONLY" in document
    assert "MAIN_SCENE_READ_ONLY" in document
    assert "PRODUCTION_ADAPTER_READY: NOT_READY" in document


def test_adoption_scope_is_exactly_four_files() -> None:
    assert _changed_paths() == ALLOWED_PATHS
