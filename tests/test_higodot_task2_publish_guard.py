from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "tools" / "higodot_task2_provenance.py"
WORKFLOW = ROOT / ".github" / "workflows" / "higodot-task2-authoring-bridge.yml"
SCHEMA = ROOT / ".github" / "validation" / "higodot-task2-provenance-schema.json"
ALLOWED = {
    "project.godot",
    "scenes/vertical_slice/main_menu.tscn",
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
}
VALIDATIONS = {
    "task2_static_contract", "godot_import", "smoke_main_menu", "smoke_vertical_slice_app",
    "smoke_workshop", "gut", "task1_contract", "model_integration",
}


def _load():
    spec = importlib.util.spec_from_file_location("higodot_task2_provenance", PROVENANCE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(repo: Path, *args: str) -> str:
    return subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def _make_artifact(tmp_path: Path, head: str) -> Path:
    from tools import higodot_task2_bridge as bridge
    provenance = _load()
    source = tmp_path / "source"; source.mkdir()
    hashes = {}
    for relative in sorted(ALLOWED):
        path = source / relative; path.parent.mkdir(parents=True, exist_ok=True)
        payload = '[application]\nrun/main_scene="res://scenes/vertical_slice/main_menu.tscn"\n' if relative == "project.godot" else f"[gd_scene format=3]\n; {relative}\n"
        path.write_text(payload, encoding="utf-8"); hashes[relative] = bridge.sha256_file(path)
    evidence = {}; files = {}
    for name in sorted(VALIDATIONS):
        path = tmp_path / "evidence" / f"{name}.bin"; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(f"PASS:{name}\n", encoding="utf-8")
        evidence[name] = {"status": "PASS", "sha256": bridge.sha256_file(path)}; files[name] = path
    context = {
        "decision_ids": ["BS-HIGODOT-EXEC-20260808-01", "BS-HIGODOT-20260808-01", "BS-VS-TASK2-20260807-01"],
        "repository": "alsdmlals4-eng/Blacksmith", "pr_number": 131, "input_head_sha": head,
        "godot": {"version": "4.7.1-stable"}, "higodot": {"version": "3.1.3"}, "server": {"version": "3.1.3"},
        "session": {"id": "blacksmith@abcd", "project_path": "/workspace/Blacksmith"}, "changed_paths": sorted(ALLOWED),
    }
    operations = [{"tool": "scene_manage", "arguments_sha256": "a"*64, "success": True, "result_sha256": "b"*64, "error": None}]
    artifact = tmp_path / "artifact"
    provenance.prepare_provenance_artifact(repo=source, artifact_root=artifact, context=context, operations=operations, serialized_hashes=hashes, validations=evidence, validation_files=files, expected_head=head, schema_path=SCHEMA)
    return artifact


def _clean_checkout(tmp_path: Path) -> Path:
    repo = tmp_path / "checkout"; repo.mkdir()
    _run(repo, "git", "init"); _run(repo, "git", "config", "user.email", "ci@example.invalid"); _run(repo, "git", "config", "user.name", "CI")
    (repo / "project.godot").write_text('[application]\nrun/main_scene="res://scenes/test/enhancement_test.tscn"\n', encoding="utf-8")
    _run(repo, "git", "add", "project.godot"); _run(repo, "git", "commit", "-m", "baseline")
    return repo


def test_verify_publish_head_rejects_race_and_invalid_sha() -> None:
    p = _load(); head = "a"*40
    assert p.verify_publish_head(head, head) is None
    with pytest.raises(ValueError, match="moved"): p.verify_publish_head(head, "b"*40)
    with pytest.raises(ValueError, match="40-hex"): p.verify_publish_head("bad", "b"*40)


def test_stage_proven_artifact_copies_exact_bytes_and_exact_four_diff(tmp_path: Path) -> None:
    p = _load(); head = "c"*40; artifact = _make_artifact(tmp_path, head); checkout = _clean_checkout(tmp_path)
    manifest = p.stage_proven_artifact(artifact, checkout, head, SCHEMA)
    tracked = set(filter(None, _run(checkout, "git", "diff", "--name-only").splitlines()))
    untracked = set(filter(None, _run(checkout, "git", "ls-files", "--others", "--exclude-standard").splitlines()))
    assert tracked | untracked == ALLOWED
    for relative in ALLOWED:
        assert (checkout/relative).read_bytes() == (artifact/"product"/relative).read_bytes()
        assert p.sha256_file(checkout/relative) == manifest["serialized_sha256"][relative]


def test_stage_proven_artifact_rejects_dirty_checkout(tmp_path: Path) -> None:
    p = _load(); head = "d"*40; artifact = _make_artifact(tmp_path, head); checkout = _clean_checkout(tmp_path)
    (checkout/"unexpected.txt").write_text("dirty\n", encoding="utf-8")
    with pytest.raises(ValueError, match="clean"): p.stage_proven_artifact(artifact, checkout, head, SCHEMA)


def test_workflow_publish_is_guarded_byte_transport_only() -> None:
    text = WORKFLOW.read_text(encoding="utf-8"); prove = text[text.index("prove:"):text.index("publish:")]; publish = text[text.index("publish:"):]
    assert "provenance_ready=true" in prove
    assert prove.index("actions/upload-artifact@") < prove.index("provenance_ready=true")
    for marker in (
        "actions/download-artifact@634f93cb2916e3fdff6788551b99b062d0335ce0", "verify_publish_head", "stage_proven_artifact",
        "git ls-remote --heads origin refs/heads/feat/vertical-slice-task2-app-shell", "git diff --name-only", "git push origin HEAD:feat/vertical-slice-task2-app-shell",
    ): assert marker in publish, marker
    for forbidden in ("xvfb-run", "godot-ai", "fastmcp", "/mcp", "--force", "git rebase", "godot --"):
        assert forbidden not in publish
    assert publish.count("git ls-remote --heads origin refs/heads/feat/vertical-slice-task2-app-shell") >= 2


def test_publish_captures_remote_head_before_staging_and_checks_again_before_push() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    publish = text[text.index("publish:"):]
    capture = publish.index("Capture remote head before staging")
    stage = publish.index("Verify remote head and stage byte-identical proven outputs")
    before_push = publish.index("Verify target branch has not moved before push")
    push = publish.index("git push origin HEAD:feat/vertical-slice-task2-app-shell")
    assert capture < stage < before_push < push
    assert "Verify target branch has not moved before staging" not in publish
