from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tools" / "higodot_task2_bridge.py"
PROVENANCE = ROOT / "tools" / "higodot_task2_provenance.py"
WORKFLOW = ROOT / ".github" / "workflows" / "higodot-task2-authoring-bridge.yml"
SCHEMA = ROOT / ".github" / "validation" / "higodot-task2-provenance-schema.json"
ALLOWED = {
    "project.godot",
    "scenes/vertical_slice/main_menu.tscn",
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
}
VALIDATION_NAMES = {
    "task2_static_contract",
    "godot_import",
    "smoke_main_menu",
    "smoke_vertical_slice_app",
    "smoke_workshop",
    "gut",
    "task1_contract",
    "model_integration",
}


def _load_module(name: str, path: Path):
    assert path.is_file(), f"missing module: {path.relative_to(ROOT)}"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_driver():
    return _load_module("higodot_task2_bridge", DRIVER)


def _load_provenance():
    return _load_module("higodot_task2_provenance", PROVENANCE)


def _materialize_source(repo: Path) -> dict[str, str]:
    driver = _load_driver()
    hashes: dict[str, str] = {}
    for relative in sorted(ALLOWED):
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative == "project.godot":
            payload = '[application]\nrun/main_scene="res://scenes/vertical_slice/main_menu.tscn"\n'
        else:
            payload = f"[gd_scene format=3]\n; {relative}\n"
        path.write_text(payload, encoding="utf-8")
        hashes[relative] = driver.sha256_file(path)
    return hashes


def _validation_files(tmp_path: Path) -> tuple[dict[str, dict[str, str]], dict[str, Path]]:
    driver = _load_driver()
    evidence: dict[str, dict[str, str]] = {}
    files: dict[str, Path] = {}
    for name in sorted(VALIDATION_NAMES):
        path = tmp_path / "validation-source" / f"{name}.bin"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"PASS:{name}\n".encode("utf-8"))
        evidence[name] = {"status": "PASS", "sha256": driver.sha256_file(path)}
        files[name] = path
    return evidence, files


def _context(head: str) -> dict:
    return {
        "decision_ids": [
            "BS-HIGODOT-EXEC-20260808-01",
            "BS-HIGODOT-20260808-01",
            "BS-VS-TASK2-20260807-01",
        ],
        "repository": "alsdmlals4-eng/Blacksmith",
        "pr_number": 131,
        "input_head_sha": head,
        "godot": {"version": "4.7.1-stable"},
        "higodot": {"version": "3.0.5"},
        "server": {"version": "3.0.5"},
        "session": {"id": "blacksmith@abcd", "project_path": "/workspace/Blacksmith"},
        "changed_paths": sorted(ALLOWED),
    }


def _operations() -> list[dict]:
    return [
        {
            "tool": "scene_manage",
            "arguments_sha256": "a" * 64,
            "success": True,
            "result_sha256": "b" * 64,
            "error": None,
        }
    ]


def test_prepare_provenance_artifact_copies_only_exact_products_and_validation_bytes(tmp_path: Path) -> None:
    provenance = _load_provenance()
    repo = tmp_path / "repo"
    repo.mkdir()
    hashes = _materialize_source(repo)
    validations, validation_files = _validation_files(tmp_path)
    head = "c" * 40
    artifact = tmp_path / "artifact"

    manifest = provenance.prepare_provenance_artifact(
        repo=repo,
        artifact_root=artifact,
        context=_context(head),
        operations=_operations(),
        serialized_hashes=hashes,
        validations=validations,
        validation_files=validation_files,
        expected_head=head,
        schema_path=SCHEMA,
    )

    assert (artifact / "higodot-task2-provenance.json").is_file()
    expected_files = {"higodot-task2-provenance.json"}
    expected_files |= {f"product/{path}" for path in ALLOWED}
    expected_files |= {f"validation/{name}.evidence" for name in VALIDATION_NAMES}
    actual_files = {
        path.relative_to(artifact).as_posix()
        for path in artifact.rglob("*")
        if path.is_file()
    }
    assert actual_files == expected_files
    assert list(manifest["changed_paths"]) == sorted(ALLOWED)

    for relative in sorted(ALLOWED):
        copied = artifact / "product" / relative
        assert copied.read_bytes() == (repo / relative).read_bytes()
        assert manifest["serialized_sha256"][relative] == hashes[relative]
        assert manifest["artifact_sha256"][f"product/{relative}"] == hashes[relative]

    for name in sorted(VALIDATION_NAMES):
        copied = artifact / "validation" / f"{name}.evidence"
        assert copied.read_bytes() == validation_files[name].read_bytes()
        assert manifest["artifact_sha256"][f"validation/{name}.evidence"] == validations[name]["sha256"]


def test_prepare_provenance_rejects_sensitive_context_before_writing(tmp_path: Path) -> None:
    provenance = _load_provenance()
    repo = tmp_path / "repo"
    repo.mkdir()
    hashes = _materialize_source(repo)
    validations, validation_files = _validation_files(tmp_path)
    head = "d" * 40
    context = _context(head)
    context["session"]["github_token"] = "secret-value"
    artifact = tmp_path / "artifact"

    with pytest.raises(ValueError, match="sensitive"):
        provenance.prepare_provenance_artifact(
            repo=repo,
            artifact_root=artifact,
            context=context,
            operations=_operations(),
            serialized_hashes=hashes,
            validations=validations,
            validation_files=validation_files,
            expected_head=head,
            schema_path=SCHEMA,
        )
    assert not artifact.exists()


def test_sensitive_scan_rejects_environment_dump_nested_anywhere() -> None:
    provenance = _load_provenance()
    payload = _context("e" * 40)
    payload["session"]["environment"] = {"PATH": "/tmp", "HOME": "/home/runner"}
    with pytest.raises(ValueError, match="sensitive"):
        provenance.assert_no_sensitive_provenance_fields(payload)


def test_validate_provenance_artifact_rejects_product_tamper(tmp_path: Path) -> None:
    provenance = _load_provenance()
    repo = tmp_path / "repo"
    repo.mkdir()
    hashes = _materialize_source(repo)
    validations, validation_files = _validation_files(tmp_path)
    head = "f" * 40
    artifact = tmp_path / "artifact"
    provenance.prepare_provenance_artifact(
        repo=repo,
        artifact_root=artifact,
        context=_context(head),
        operations=_operations(),
        serialized_hashes=hashes,
        validations=validations,
        validation_files=validation_files,
        expected_head=head,
        schema_path=SCHEMA,
    )
    (artifact / "product/project.godot").write_text("tampered\n", encoding="utf-8")
    with pytest.raises(ValueError, match="artifact hash"):
        provenance.validate_provenance_artifact(artifact, head, SCHEMA)


def test_validate_provenance_artifact_rejects_manifest_head_or_extra_file(tmp_path: Path) -> None:
    provenance = _load_provenance()
    repo = tmp_path / "repo"
    repo.mkdir()
    hashes = _materialize_source(repo)
    validations, validation_files = _validation_files(tmp_path)
    head = "1" * 40
    artifact = tmp_path / "artifact"
    provenance.prepare_provenance_artifact(
        repo=repo,
        artifact_root=artifact,
        context=_context(head),
        operations=_operations(),
        serialized_hashes=hashes,
        validations=validations,
        validation_files=validation_files,
        expected_head=head,
        schema_path=SCHEMA,
    )
    with pytest.raises(ValueError, match="input head"):
        provenance.validate_provenance_artifact(artifact, "2" * 40, SCHEMA)

    (artifact / "environment.json").write_text('{"PATH":"/tmp"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="artifact file set"):
        provenance.validate_provenance_artifact(artifact, head, SCHEMA)


def test_provenance_schema_contract_is_checked_from_committed_schema() -> None:
    provenance = _load_provenance()
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert provenance.validate_provenance_schema_contract(schema) is None
    bad = copy.deepcopy(schema)
    bad["properties"]["repository"].pop("const")
    with pytest.raises(ValueError, match="repository"):
        provenance.validate_provenance_schema_contract(bad)


def test_workflow_builds_and_validates_provenance_before_upload() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    prove = text[text.index("prove:") : text.index("publish:")]
    for marker in (
        "higodot_task2_provenance",
        "prepare_provenance_artifact",
        "validate_provenance_artifact",
        "higodot-task2-provenance.json",
        "product/project.godot",
        "validation-evidence.json",
        "actions/upload-artifact@",
        "higodot-task2-provenance",
    ):
        assert marker in prove, marker
    assert prove.index("validate_provenance_artifact") < prove.index("actions/upload-artifact@")
    assert prove.index("validate_post_authoring_validations") < prove.index("prepare_provenance_artifact")
    assert "provenance_ready=true" not in prove
