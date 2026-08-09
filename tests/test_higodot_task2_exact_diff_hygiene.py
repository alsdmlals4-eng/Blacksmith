from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "higodot_task2_bridge.py"
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


def _load_driver():
    spec = importlib.util.spec_from_file_location("higodot_task2_bridge_hygiene", DRIVER)
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


def _write_expected_prove_byproducts(repo: Path) -> None:
    evidence_root = repo / "artifacts" / "higodot-task2"
    evidence_root.mkdir(parents=True, exist_ok=True)
    (evidence_root / "session-context.json").write_text("{}\n", encoding="utf-8")
    (evidence_root / "operation-evidence.json").write_text("[]\n", encoding="utf-8")
    (repo / "scripts" / "tracked.gd.uid").write_text("uid://generated\n", encoding="utf-8")


def test_verify_serialized_diff_ignores_only_expected_runtime_byproducts(tmp_path: Path) -> None:
    driver = _load_driver()
    repo = _prepare_authored_repo(tmp_path)
    _write_expected_prove_byproducts(repo)

    hashes = driver.verify_serialized_diff(repo, BEFORE_PROJECT)

    assert set(hashes) == ALLOWED_SERIALIZED_PATHS


def test_verify_serialized_diff_rejects_unknown_higodot_artifact(tmp_path: Path) -> None:
    driver = _load_driver()
    repo = _prepare_authored_repo(tmp_path)
    _write_expected_prove_byproducts(repo)
    (repo / "artifacts" / "higodot-task2" / "unexpected.json").write_text("{}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="serialized diff escaped Task 2 allowlist"):
        driver.verify_serialized_diff(repo, BEFORE_PROJECT)


def test_verify_serialized_diff_rejects_orphan_generated_uid(tmp_path: Path) -> None:
    driver = _load_driver()
    repo = _prepare_authored_repo(tmp_path)
    _write_expected_prove_byproducts(repo)
    (repo / "scripts" / "orphan.gd.uid").write_text("uid://orphan\n", encoding="utf-8")

    with pytest.raises(ValueError, match="serialized diff escaped Task 2 allowlist"):
        driver.verify_serialized_diff(repo, BEFORE_PROJECT)


def test_verify_serialized_diff_rejects_uid_for_untracked_script(tmp_path: Path) -> None:
    driver = _load_driver()
    repo = _prepare_authored_repo(tmp_path)
    _write_expected_prove_byproducts(repo)
    (repo / "scripts" / "untracked.gd").write_text("extends Node\n", encoding="utf-8")
    (repo / "scripts" / "untracked.gd.uid").write_text("uid://untracked\n", encoding="utf-8")

    with pytest.raises(ValueError, match="serialized diff escaped Task 2 allowlist"):
        driver.verify_serialized_diff(repo, BEFORE_PROJECT)


def test_verify_serialized_diff_rejects_modified_tracked_uid(tmp_path: Path) -> None:
    driver = _load_driver()
    repo = _prepare_authored_repo(tmp_path)
    _write_expected_prove_byproducts(repo)
    tracked_uid = repo / "scripts" / "committed.gd.uid"
    tracked_uid.write_text("uid://before\n", encoding="utf-8")
    _git(repo, "add", "scripts/committed.gd.uid")
    _git(repo, "commit", "-qm", "track uid")
    tracked_uid.write_text("uid://after\n", encoding="utf-8")

    with pytest.raises(ValueError, match="serialized diff escaped Task 2 allowlist"):
        driver.verify_serialized_diff(repo, BEFORE_PROJECT)
