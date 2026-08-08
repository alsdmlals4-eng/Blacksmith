from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "higodot_task2_bridge.py"
WORKFLOW = ROOT / ".github" / "workflows" / "higodot-task2-authoring-bridge.yml"
ALLOWED = {
    "project.godot",
    "scenes/vertical_slice/main_menu.tscn",
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
}
REQUIRED_VALIDATIONS = {
    "task2_static_contract",
    "godot_import",
    "smoke_main_menu",
    "smoke_vertical_slice_app",
    "smoke_workshop",
    "gut",
    "task1_contract",
    "model_integration",
}


def _load_driver():
    spec = importlib.util.spec_from_file_location("higodot_task2_bridge", DRIVER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(repo: Path, *args: str) -> None:
    subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True)


def _repo_with_baseline(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _run(repo, "git", "init")
    _run(repo, "git", "config", "user.email", "ci@example.invalid")
    _run(repo, "git", "config", "user.name", "CI")
    baseline = (
        '[application]\n'
        'run/main_scene="res://scenes/test/enhancement_test.tscn"\n'
        '[display]\n'
        'window/size/viewport_width=720\n'
        '[rendering]\n'
        'renderer/rendering_method="gl_compatibility"\n'
    )
    (repo / "project.godot").write_text(baseline, encoding="utf-8")
    _run(repo, "git", "add", "project.godot")
    _run(repo, "git", "commit", "-m", "baseline")
    return repo, baseline


def _materialize_allowed_outputs(repo: Path, *, extra_project_line: str = "") -> None:
    project = (
        '[application]\n'
        'run/main_scene="res://scenes/vertical_slice/main_menu.tscn"\n'
        '[display]\n'
        'window/size/viewport_width=720\n'
        '[rendering]\n'
        'renderer/rendering_method="gl_compatibility"\n'
    )
    if extra_project_line:
        project += extra_project_line
    (repo / "project.godot").write_text(project, encoding="utf-8")
    for relative in sorted(ALLOWED - {"project.godot"}):
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("[gd_scene format=3]\n", encoding="utf-8")


def _passing_evidence() -> dict[str, dict[str, str]]:
    return {
        name: {"status": "PASS", "sha256": f"{index + 1:064x}"}
        for index, name in enumerate(sorted(REQUIRED_VALIDATIONS))
    }


def test_verify_serialized_diff_accepts_exact_four_paths(tmp_path: Path) -> None:
    driver = _load_driver()
    repo, baseline = _repo_with_baseline(tmp_path)
    _materialize_allowed_outputs(repo)
    hashes = driver.verify_serialized_diff(repo, baseline)
    assert set(hashes) == ALLOWED
    assert all(len(value) == 64 for value in hashes.values())


def test_verify_serialized_diff_rejects_fifth_tracked_or_untracked_path(tmp_path: Path) -> None:
    driver = _load_driver()
    repo, baseline = _repo_with_baseline(tmp_path)
    _materialize_allowed_outputs(repo)
    (repo / "scenes/vertical_slice/forbidden.tscn").write_text("[gd_scene format=3]\n", encoding="utf-8")
    with pytest.raises(ValueError, match="allowlist"):
        driver.verify_serialized_diff(repo, baseline)


def test_verify_serialized_diff_rejects_unrelated_project_setting_change(tmp_path: Path) -> None:
    driver = _load_driver()
    repo, baseline = _repo_with_baseline(tmp_path)
    _materialize_allowed_outputs(repo, extra_project_line='environment/defaults/default_clear_color=Color(1, 0, 0, 1)\n')
    with pytest.raises(ValueError, match="outside application/run/main_scene"):
        driver.verify_serialized_diff(repo, baseline)


def test_validation_evidence_requires_exact_named_pass_set() -> None:
    driver = _load_driver()
    evidence = _passing_evidence()
    normalized = driver.validate_post_authoring_validations(evidence)
    assert set(normalized) == REQUIRED_VALIDATIONS

    missing = dict(evidence)
    missing.pop("gut")
    with pytest.raises(ValueError, match="exact required set"):
        driver.validate_post_authoring_validations(missing)

    failed = _passing_evidence()
    failed["godot_import"] = {"status": "FAIL", "sha256": "f" * 64}
    with pytest.raises(ValueError, match="must be PASS"):
        driver.validate_post_authoring_validations(failed)


def test_validation_evidence_rejects_invalid_hash() -> None:
    driver = _load_driver()
    evidence = _passing_evidence()
    evidence["gut"] = {"status": "PASS", "sha256": "not-a-hash"}
    with pytest.raises(ValueError, match="SHA-256"):
        driver.validate_post_authoring_validations(evidence)


def test_workflow_runs_required_post_authoring_validations_before_provenance_gate() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    prove = text[text.index("prove:") : text.index("publish:")]
    required_markers = (
        "tests.test_vertical_slice_task2_app_shell_contract",
        "--headless --editor --path . --quit",
        "res://scenes/vertical_slice/main_menu.tscn",
        "res://scenes/vertical_slice/vertical_slice_app.tscn",
        "res://scenes/vertical_slice/screens/vs_workshop_screen.tscn",
        "addons/gut/gut_cmdln.gd",
        "tools/validate_gut_junit.py",
        "tests.test_vertical_slice_task1_canon_contract",
        "test_equipment_lifecycle_poc.gd",
        "verify_serialized_diff",
        "validate_post_authoring_validations",
    )
    for marker in required_markers:
        assert marker in prove, marker
    gate_index = prove.index("provenance_ready=false")
    for marker in required_markers:
        assert prove.index(marker) < gate_index, marker


def test_workflow_has_no_artifact_upload_before_post_authoring_validation() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    prove = text[text.index("prove:") : text.index("publish:")]
    validation_index = prove.index("validate_post_authoring_validations")
    prefix = prove[:validation_index]
    assert "actions/upload-artifact" not in prefix


def test_workflow_uses_canonical_equipment_lifecycle_controller_marker() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Equipment lifecycle controller integration tests PASSED" in text
    assert '"Equipment lifecycle controller tests PASSED"' not in text
