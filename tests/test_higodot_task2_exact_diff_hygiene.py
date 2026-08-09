from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "higodot_task2_bridge.py"
REAL_PROVE = ROOT / "tools" / "higodot_task2_real_prove.py"
ALLOWED_SERIALIZED_PATHS = {
    "project.godot",
    "scenes/vertical_slice/main_menu.tscn",
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
}
BEFORE_PROJECT = (
    '[application]\n'
    'run/main_scene="res://scenes/test/enhancement_test.tscn"\n'
    '[display]\n'
    'window/size/viewport_width=720\n'
)
AFTER_PROJECT = (
    '[application]\n'
    'run/main_scene="res://scenes/vertical_slice/main_menu.tscn"\n'
    '[display]\n'
    'window/size/viewport_width=720\n'
)


def _load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        capture_output=True,
        text=True,
    )


def _prepare_authored_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Blacksmith Test")

    (repo / "scripts").mkdir(parents=True)
    (repo / "project.godot").write_text(BEFORE_PROJECT, encoding="utf-8")
    (repo / "scripts" / "tracked.gd").write_text("extends Node\n", encoding="utf-8")
    _git(repo, "add", "project.godot", "scripts/tracked.gd")
    _git(repo, "commit", "-qm", "baseline")

    (repo / "project.godot").write_text(AFTER_PROJECT, encoding="utf-8")
    for relative in sorted(ALLOWED_SERIALIZED_PATHS - {"project.godot"}):
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("[gd_scene format=3]\n", encoding="utf-8")
    return repo


def _write_expected_prove_byproducts(repo: Path) -> tuple[Path, Path]:
    evidence_root = repo / "artifacts" / "higodot-task2"
    evidence_root.mkdir(parents=True, exist_ok=True)
    context = evidence_root / "session-context.json"
    operations = evidence_root / "operation-evidence.json"
    context.write_text("{}\n", encoding="utf-8")
    operations.write_text("[]\n", encoding="utf-8")
    (repo / "scripts" / "tracked.gd.uid").write_text("uid://generated\n", encoding="utf-8")
    return context, operations


def _apply_hygiene(repo: Path, context: Path, operations: Path) -> None:
    real_prove = _load(REAL_PROVE, "higodot_task2_real_prove_hygiene")
    real_prove.register_runtime_byproduct_excludes(repo, context, operations)


def test_exact_diff_stays_strict_after_ephemeral_runtime_byproducts_are_excluded(tmp_path: Path) -> None:
    driver = _load(DRIVER, "higodot_task2_bridge_hygiene")
    repo = _prepare_authored_repo(tmp_path)
    context, operations = _write_expected_prove_byproducts(repo)

    _apply_hygiene(repo, context, operations)
    hashes = driver.verify_serialized_diff(repo, BEFORE_PROJECT)

    assert set(hashes) == ALLOWED_SERIALIZED_PATHS
    exclude_text = (repo / ".git" / "info" / "exclude").read_text(encoding="utf-8")
    assert "/artifacts/higodot-task2/session-context.json" in exclude_text
    assert "/artifacts/higodot-task2/operation-evidence.json" in exclude_text
    assert "/scripts/tracked.gd.uid" in exclude_text


def test_exact_diff_hygiene_does_not_hide_unknown_higodot_artifact(tmp_path: Path) -> None:
    driver = _load(DRIVER, "higodot_task2_bridge_unknown_artifact")
    repo = _prepare_authored_repo(tmp_path)
    context, operations = _write_expected_prove_byproducts(repo)
    (repo / "artifacts" / "higodot-task2" / "unexpected.json").write_text("{}\n", encoding="utf-8")

    _apply_hygiene(repo, context, operations)
    with pytest.raises(ValueError, match="serialized diff escaped Task 2 allowlist"):
        driver.verify_serialized_diff(repo, BEFORE_PROJECT)


def test_exact_diff_hygiene_rejects_orphan_generated_uid(tmp_path: Path) -> None:
    repo = _prepare_authored_repo(tmp_path)
    context, operations = _write_expected_prove_byproducts(repo)
    (repo / "scripts" / "orphan.gd.uid").write_text("uid://orphan\n", encoding="utf-8")

    with pytest.raises(ValueError, match="paired tracked \.gd"):
        _apply_hygiene(repo, context, operations)


def test_exact_diff_hygiene_rejects_uid_for_untracked_script(tmp_path: Path) -> None:
    repo = _prepare_authored_repo(tmp_path)
    context, operations = _write_expected_prove_byproducts(repo)
    (repo / "scripts" / "untracked.gd").write_text("extends Node\n", encoding="utf-8")
    (repo / "scripts" / "untracked.gd.uid").write_text("uid://untracked\n", encoding="utf-8")

    with pytest.raises(ValueError, match="paired tracked \.gd"):
        _apply_hygiene(repo, context, operations)


def test_exact_diff_hygiene_does_not_hide_modified_tracked_uid(tmp_path: Path) -> None:
    driver = _load(DRIVER, "higodot_task2_bridge_tracked_uid")
    repo = _prepare_authored_repo(tmp_path)
    tracked_uid = repo / "scripts" / "committed.gd.uid"
    tracked_uid.write_text("uid://before\n", encoding="utf-8")
    _git(repo, "add", "scripts/committed.gd.uid")
    _git(repo, "commit", "-qm", "track uid")
    tracked_uid.write_text("uid://after\n", encoding="utf-8")
    context, operations = _write_expected_prove_byproducts(repo)

    _apply_hygiene(repo, context, operations)
    with pytest.raises(ValueError, match="serialized diff escaped Task 2 allowlist"):
        driver.verify_serialized_diff(repo, BEFORE_PROJECT)


def test_exact_diff_hygiene_requires_exact_evidence_output_paths(tmp_path: Path) -> None:
    repo = _prepare_authored_repo(tmp_path)
    context, operations = _write_expected_prove_byproducts(repo)
    wrong_context = repo / "artifacts" / "higodot-task2" / "wrong-context.json"
    wrong_context.write_text("{}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="evidence path"):
        _apply_hygiene(repo, wrong_context, operations)
