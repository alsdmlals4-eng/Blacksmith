from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_C0_SHA = "2b595570bd237174b2b962a1eb54588b5ecc508d"
GODOT_ARCHIVE_SHA256 = "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba"
DOWNLOAD_ARTIFACT_SHA = "634f93cb2916e3fdff6788551b99b062d0335ce0"
DESCRIPTOR = ROOT / ".godot-live-editor/project-pilot.json"
ADOPTION_DOC = ROOT / "docs/GODOT_LIVE_EDITOR_ADOPTION.md"
WORKFLOW = ROOT / ".github/workflows/validate-godot-live-editor-pilot.yml"
ALLOWED_PATHS = {
    ".godot-live-editor/project-pilot.json",
    "docs/GODOT_LIVE_EDITOR_ADOPTION.md",
    "tests/test_godot_live_editor_adoption.py",
    ".github/workflows/validate-godot-live-editor-pilot.yml",
}
BEHAVIOR_TARGETS = [
    "res://tests/unit/test_forging_session.gd",
    "res://tests/unit/test_enhancement_session.gd",
    "res://tests/unit/test_workshop_resources.gd",
    "res://tests/unit/test_workshop_calendar.gd",
    "res://tests/unit/test_craftsmanship_grade_resolver.gd",
    "res://tests/unit/test_customer_contract.gd",
    "res://tests/unit/test_world_activity_resolver.gd",
    "res://tests/unit/test_equipment_world_registry.gd",
    "res://tests/unit/test_poc_telemetry.gd",
    "res://tests/integration/test_manual_enhancement_economy.gd",
    "res://tests/integration/test_forging_quality_enhancement.gd",
    "res://tests/integration/test_workshop_action_atomicity.gd",
    "res://tests/integration/test_equipment_lifecycle_controller.gd",
    "res://tests/integration/test_equipment_lifecycle_poc.gd",
]


def _required_text(path: Path) -> str:
    assert path.is_file(), f"missing required adoption surface: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def _changed_paths_from_main() -> set[str]:
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


def _configured_main_scene(project_text: str) -> str:
    prefix = 'run/main_scene="'
    assert prefix in project_text, "application/run/main_scene must remain configured"
    return project_text.split(prefix, 1)[1].split('"', 1)[0]


def test_descriptor_is_exact_blacksmith_contract() -> None:
    payload = json.loads(_required_text(DESCRIPTOR))
    assert payload["schema_version"] == "1"
    assert payload["project_identity"] == {
        "repository": "alsdmlals4-eng/Blacksmith",
        "project_id": "blacksmith",
    }
    assert payload["base_pilot_commit"] == BASE_C0_SHA
    assert payload["project_state"] == "EXISTING_GODOT_PROJECT"
    assert payload["godot"] == {
        "version": "4.7.1-stable",
        "archive_sha256": GODOT_ARCHIVE_SHA256,
    }
    assert payload["project_file"] == "project.godot"
    assert payload["main_scene_source"] == "application/run/main_scene"
    assert payload["legacy_editor_plugins"] == ["res://addons/godot_ai/plugin.cfg"]
    assert payload["legacy_autoloads"] == ["_mcp_game_helper"]
    assert payload["legacy_disable_mode"] == "TEMPORARY_COPY_ONLY"
    assert payload["source_mutation_policy"] == "FORBIDDEN"
    assert payload["scratch_scene_path"] == "res://.godot-live-editor-pilot/scratch.tscn"
    assert payload["expected_platform"] == "ANDROID"
    assert payload["behavior_checks"] == [
        {"kind": "GODOT_SCRIPT", "target": target, "timeout_seconds": 60}
        for target in BEHAVIOR_TARGETS
    ]


def test_source_legacy_authority_and_configured_main_scene_remain_installed() -> None:
    project = (ROOT / "project.godot").read_text(encoding="utf-8")
    main_scene = _configured_main_scene(project)
    assert main_scene.startswith("res://")
    assert main_scene.endswith(".tscn")
    assert (ROOT / main_scene.removeprefix("res://")).is_file(), main_scene
    assert '_mcp_game_helper="*res://addons/godot_ai/runtime/game_helper.gd"' in project
    assert '"res://addons/godot_ai/plugin.cfg"' in project
    assert (ROOT / "addons/godot_ai/plugin.cfg").is_file()
    for target in BEHAVIOR_TARGETS:
        assert (ROOT / target.removeprefix("res://")).is_file(), target


def test_adoption_document_preserves_boundaries() -> None:
    text = _required_text(ADOPTION_DOC)
    for marker in (
        "LEGACY_GODOT_AI_SOURCE_PRESERVED",
        "LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY",
        "DUAL_MUTATION_AUTHORITY_FORBIDDEN",
        "MAIN_SCENE_READ_ONLY",
        "source-configured main Scene",
        "SCRATCH_SCENE_MUTATION_ONLY",
        "SOURCE_TREE_UNCHANGED",
        "SELF_CONTAINED_EVIDENCE_BUNDLE",
        "project-pilot-evidence.json",
        "runtime-result.json",
        "scratch.tscn",
        "expected_platform: ANDROID",
        "android_device: NOT_RUN",
        "PRODUCTION_ADAPTER_READY: NOT_READY",
        "four adoption files",
    ):
        assert marker in text
    for forbidden_claim in (
        "PRODUCTION_ADAPTER_READY: READY",
        "LEGACY_GODOT_AI_SOURCE_REMOVED",
        "HUMAN_USABILITY: PASS",
        "android_device: PASS",
        "res://scenes/test/enhancement_test.tscn",
    ):
        assert forbidden_claim not in text


def test_workflow_uses_one_immutable_base_pin() -> None:
    text = _required_text(WORKFLOW)
    reusable = (
        "alsdmlals4-eng/Base/.github/workflows/"
        f"reusable-godot-project-pilot.yml@{BASE_C0_SHA}"
    )
    assert reusable in text
    assert f"base_pilot_commit: {BASE_C0_SHA}" in text
    assert "descriptor_path: .godot-live-editor/project-pilot.json" in text
    assert "pull_request:" in text
    assert "push:" in text
    assert "workflow_dispatch:" in text
    assert "permissions:\n  contents: read" in text
    assert "fetch-depth: 0" in text
    assert "persist-credentials: false" in text
    assert "python -m pytest tests/test_godot_live_editor_adoption.py -q" in text
    assert "@main" not in text
    assert text.count(BASE_C0_SHA) == 2


def test_workflow_surfaces_bounded_pilot_failure_marker() -> None:
    text = _required_text(WORKFLOW)
    assert "pilot-failure-diagnostics:" in text
    assert "needs: project-pilot" in text
    assert "needs.project-pilot.result == 'failure'" in text
    assert f"actions/download-artifact@{DOWNLOAD_ARTIFACT_SHA}" in text
    assert "godot-project-pilot-${{ github.repository_id }}-${{ github.sha }}" in text
    assert ".godot-live-editor/pilot-failure/failure.json" in text
    assert "cat .godot-live-editor/pilot-failure/failure.json" in text


def test_pull_request_trigger_is_scoped_to_adoption_surface() -> None:
    text = _required_text(WORKFLOW)
    assert "    paths:\n" in text
    for path in sorted(ALLOWED_PATHS):
        assert f"      - {path}\n" in text


def test_adoption_slice_change_surface_is_bounded_to_four_files() -> None:
    changed = _changed_paths_from_main()
    # This boundary applies when the live-editor adoption slice itself changes.
    # Unrelated maintenance PRs must not be rejected merely because this
    # repository-wide test is included in their validation suite.
    adoption_payload_paths = ALLOWED_PATHS - {"tests/test_godot_live_editor_adoption.py"}
    if changed & adoption_payload_paths:
        assert changed <= ALLOWED_PATHS, f"forbidden changed paths: {sorted(changed - ALLOWED_PATHS)}"
