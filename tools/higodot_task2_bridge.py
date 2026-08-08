from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


DECISION_ID = "BS-HIGODOT-EXEC-20260808-01"
RELATED_DECISION_IDS = (
    "BS-HIGODOT-20260808-01",
    "BS-VS-TASK2-20260807-01",
    "BS-VS-INIT-20260808-01",
)
TARGET_REPOSITORY = "alsdmlals4-eng/Blacksmith"
TARGET_PR = 131
TARGET_BRANCH = "feat/vertical-slice-task2-app-shell"
TARGET_GODOT_VERSION = "4.7.1-stable"
TARGET_HIGODOT_VERSION = "3.0.5"
MCP_URL = "http://127.0.0.1:8000/mcp"
EXPECTED_MAIN_SCENE = "res://scenes/vertical_slice/main_menu.tscn"

ALLOWED_SERIALIZED_PATHS: tuple[str, ...] = (
    "project.godot",
    "scenes/vertical_slice/main_menu.tscn",
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
)
ALLOWED_NATIVE_TOOLS = {
    "scene_manage",
    "node_create",
    "node_manage",
    "node_set_property",
    "project_manage",
    "ui_manage",
}
FORBIDDEN_WRITER_TOOLS = {
    "filesystem_manage",
    "script_create",
    "script_patch",
    "file_write",
    "text_write",
}
APPROVED_SCRIPT_PATHS = {
    "res://scripts/vertical_slice/ui/vs_main_menu.gd",
    "res://scripts/vertical_slice/ui/vs_app.gd",
}
REQUIRED_PROVENANCE_FIELDS = {
    "decision_ids",
    "repository",
    "pr_number",
    "input_head_sha",
    "godot",
    "higodot",
    "server",
    "session",
    "operations",
    "changed_paths",
    "serialized_sha256",
    "validations",
    "artifact_sha256",
}
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MAIN_SCENE_LINE = re.compile(r'^run/main_scene=.*$', re.MULTILINE)


def load_recipe(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("recipe must be a JSON object")
    validate_recipe(payload)
    return payload


def validate_recipe(recipe: dict[str, Any]) -> None:
    expected_identity = {
        "decision_id": DECISION_ID,
        "repository": TARGET_REPOSITORY,
        "pr_number": TARGET_PR,
        "branch": TARGET_BRANCH,
        "godot_version": TARGET_GODOT_VERSION,
        "higodot_version": TARGET_HIGODOT_VERSION,
        "mcp_url": MCP_URL,
    }
    for field, expected in expected_identity.items():
        if recipe.get(field) != expected:
            raise ValueError(f"recipe {field} must equal {expected!r}")

    outputs = recipe.get("serialized_outputs")
    if not isinstance(outputs, list):
        raise ValueError("serialized_outputs must be a list")
    if len(outputs) != len(ALLOWED_SERIALIZED_PATHS) or set(outputs) != set(ALLOWED_SERIALIZED_PATHS):
        raise ValueError("serialized_outputs must equal the exact Task 2 allowlist")

    related = recipe.get("related_decision_ids")
    if related is not None:
        if not isinstance(related, list) or set(related) != set(RELATED_DECISION_IDS):
            raise ValueError("related_decision_ids must match the approved Task 2 authority set")

    approved_scripts = recipe.get("approved_scripts")
    if approved_scripts is not None:
        if not isinstance(approved_scripts, list) or set(approved_scripts) != APPROVED_SCRIPT_PATHS:
            raise ValueError("approved_scripts must equal the two already-GREEN Task 2 UI scripts")

    operations = recipe.get("operations")
    if not isinstance(operations, list) or not operations:
        raise ValueError("operations must be a non-empty list")

    project_writes = 0
    for index, operation in enumerate(operations):
        if not isinstance(operation, dict):
            raise ValueError(f"operation {index} must be an object")
        tool = operation.get("tool")
        if not isinstance(tool, str) or not tool:
            raise ValueError(f"operation {index} must name a tool")
        lowered = tool.lower()
        if lowered in FORBIDDEN_WRITER_TOOLS or any(token in lowered for token in ("filesystem", "script_create", "script_patch")):
            raise ValueError(f"operation {index} uses forbidden text/filesystem writer {tool!r}")
        if tool not in ALLOWED_NATIVE_TOOLS:
            raise ValueError(f"operation {index} uses non-allowlisted native tool {tool!r}")

        script = operation.get("script")
        if script is not None and script not in APPROVED_SCRIPT_PATHS:
            raise ValueError(f"operation {index} references unapproved script {script!r}")

        if tool == "project_manage":
            project_writes += 1
            if operation.get("operation") != "settings_set":
                raise ValueError("project_manage may only use settings_set")
            if operation.get("setting") != "application/run/main_scene":
                raise ValueError("project_manage may only change application/run/main_scene")
            if operation.get("value") != EXPECTED_MAIN_SCENE:
                raise ValueError("project main scene must point at the approved MainMenu")

    if project_writes != 1:
        raise ValueError("recipe must contain exactly one project main-scene write")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_changed_paths(repo: Path) -> list[str]:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return sorted({path.strip().replace("\\", "/") for path in (*tracked, *untracked) if path.strip()})


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _one_main_scene_line(text: str) -> str:
    matches = _MAIN_SCENE_LINE.findall(text)
    if len(matches) != 1:
        raise ValueError("project.godot must contain exactly one run/main_scene setting")
    return matches[0]


def verify_project_setting_delta(before: str, after: str) -> None:
    before_normalized = _normalize_newlines(before)
    after_normalized = _normalize_newlines(after)
    before_line = _one_main_scene_line(before_normalized)
    after_line = _one_main_scene_line(after_normalized)
    expected_after = f'run/main_scene="{EXPECTED_MAIN_SCENE}"'
    if after_line != expected_after:
        raise ValueError("application/run/main_scene does not point at the approved MainMenu")
    if before_line == after_line:
        raise ValueError("project.godot main scene did not change")

    sentinel = "run/main_scene=__BLACKSMITH_TASK2_SENTINEL__"
    before_rest = _MAIN_SCENE_LINE.sub(sentinel, before_normalized, count=1)
    after_rest = _MAIN_SCENE_LINE.sub(sentinel, after_normalized, count=1)
    if before_rest != after_rest:
        raise ValueError("project.godot contains changes outside application/run/main_scene")


def verify_serialized_diff(repo: Path, before_project_text: str) -> dict[str, str]:
    changed = git_changed_paths(repo)
    if len(changed) != len(ALLOWED_SERIALIZED_PATHS) or set(changed) != set(ALLOWED_SERIALIZED_PATHS):
        raise ValueError(f"serialized diff escaped Task 2 allowlist: {changed}")

    project_path = repo / "project.godot"
    if not project_path.is_file():
        raise ValueError("project.godot is missing after authoring")
    verify_project_setting_delta(before_project_text, project_path.read_text(encoding="utf-8"))

    hashes: dict[str, str] = {}
    for relative in sorted(ALLOWED_SERIALIZED_PATHS):
        path = repo / relative
        if not path.is_file():
            raise ValueError(f"expected serialized output is missing: {relative}")
        hashes[relative] = sha256_file(path)
    return hashes


def build_provenance(
    context: dict[str, Any],
    operations: list[dict[str, Any]],
    hashes: dict[str, str],
    validations: dict[str, Any],
) -> dict[str, Any]:
    payload = {
        "decision_ids": copy.deepcopy(context.get("decision_ids")),
        "repository": context.get("repository"),
        "pr_number": context.get("pr_number"),
        "input_head_sha": context.get("input_head_sha"),
        "godot": copy.deepcopy(context.get("godot")),
        "higodot": copy.deepcopy(context.get("higodot")),
        "server": copy.deepcopy(context.get("server")),
        "session": copy.deepcopy(context.get("session")),
        "operations": copy.deepcopy(operations),
        "changed_paths": copy.deepcopy(context.get("changed_paths")),
        "serialized_sha256": copy.deepcopy(hashes),
        "validations": copy.deepcopy(validations),
        "artifact_sha256": copy.deepcopy(context.get("artifact_sha256", {})),
    }
    return payload


def _require_sha256(value: Any, field: str) -> None:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise ValueError(f"{field} must be a lowercase SHA-256 hex digest")


def _require_version_identity(value: Any, expected: str, field: str) -> None:
    if not isinstance(value, dict) or value.get("version") != expected:
        raise ValueError(f"{field}.version must equal {expected}")


def validate_provenance(payload: dict[str, Any], expected_head: str) -> None:
    if not isinstance(payload, dict):
        raise ValueError("provenance must be an object")
    if set(payload) != REQUIRED_PROVENANCE_FIELDS:
        raise ValueError("provenance top-level fields do not match the approved schema")

    decision_ids = payload.get("decision_ids")
    if not isinstance(decision_ids, list) or DECISION_ID not in decision_ids:
        raise ValueError("provenance must bind the bridge Decision ID")
    if payload.get("repository") != TARGET_REPOSITORY or payload.get("pr_number") != TARGET_PR:
        raise ValueError("provenance repository/PR identity mismatch")
    if not isinstance(expected_head, str) or _SHA40.fullmatch(expected_head) is None:
        raise ValueError("expected_head must be a lowercase 40-hex commit SHA")
    if payload.get("input_head_sha") != expected_head:
        raise ValueError("provenance input head does not match expected head")

    _require_version_identity(payload.get("godot"), TARGET_GODOT_VERSION, "godot")
    _require_version_identity(payload.get("higodot"), TARGET_HIGODOT_VERSION, "higodot")
    _require_version_identity(payload.get("server"), TARGET_HIGODOT_VERSION, "server")

    session = payload.get("session")
    if not isinstance(session, dict) or not isinstance(session.get("id"), str) or not session.get("id"):
        raise ValueError("provenance session.id is required")
    if not isinstance(session.get("project_path"), str) or not session.get("project_path"):
        raise ValueError("provenance session.project_path is required")

    changed_paths = payload.get("changed_paths")
    if not isinstance(changed_paths, list) or len(changed_paths) != len(ALLOWED_SERIALIZED_PATHS):
        raise ValueError("changed_paths must contain exactly four entries")
    if set(changed_paths) != set(ALLOWED_SERIALIZED_PATHS):
        raise ValueError("changed_paths must equal the exact Task 2 serialized allowlist")

    serialized = payload.get("serialized_sha256")
    if not isinstance(serialized, dict) or set(serialized) != set(ALLOWED_SERIALIZED_PATHS):
        raise ValueError("serialized_sha256 keys must equal the exact Task 2 serialized allowlist")
    for path, digest in serialized.items():
        _require_sha256(digest, f"serialized_sha256[{path!r}]")

    operations = payload.get("operations")
    if not isinstance(operations, list):
        raise ValueError("operations must be a list")
    for index, operation in enumerate(operations):
        if not isinstance(operation, dict):
            raise ValueError(f"operation evidence {index} must be an object")
        if not isinstance(operation.get("tool"), str) or not operation.get("tool"):
            raise ValueError(f"operation evidence {index} requires tool")
        _require_sha256(operation.get("arguments_sha256"), f"operations[{index}].arguments_sha256")
        if operation.get("success") is not True:
            raise ValueError(f"operation evidence {index} is not successful")
        _require_sha256(operation.get("result_sha256"), f"operations[{index}].result_sha256")
        if operation.get("error") is not None:
            raise ValueError(f"operation evidence {index} contains an error")

    validations = payload.get("validations")
    if not isinstance(validations, dict) or not validations:
        raise ValueError("validations must contain at least one PASS record")
    for name, evidence in validations.items():
        if not isinstance(evidence, dict) or evidence.get("status") != "PASS":
            raise ValueError(f"validation {name!r} must be PASS")
        _require_sha256(evidence.get("sha256"), f"validations[{name!r}].sha256")

    artifacts = payload.get("artifact_sha256")
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("artifact_sha256 must contain at least one artifact digest")
    for name, digest in artifacts.items():
        _require_sha256(digest, f"artifact_sha256[{name!r}]")
