from __future__ import annotations

import asyncio
import copy
import hashlib
import importlib
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
TARGET_HIGODOT_VERSION = "3.1.3"
MCP_URL = "http://127.0.0.1:8000/mcp"
EXPECTED_MAIN_SCENE = "res://scenes/vertical_slice/main_menu.tscn"
SESSION_DISCOVERY_ATTEMPTS = 41
SESSION_DISCOVERY_DELAY_SECONDS = 0.5

ALLOWED_SERIALIZED_PATHS: tuple[str, ...] = (
    "project.godot",
    "scenes/vertical_slice/main_menu.tscn",
    "scenes/vertical_slice/vertical_slice_app.tscn",
    "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
)
ALLOWED_NATIVE_TOOLS = {
    "scene_manage",
    "scene_save",
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
PREFLIGHT_TOOLS = {
    "session_manage",
    "session_activate",
    "editor_state",
    "scene_get_hierarchy",
    "project_manage",
}
REQUIRED_POST_AUTHORING_VALIDATIONS = {
    "task2_static_contract",
    "godot_import",
    "smoke_main_menu",
    "smoke_vertical_slice_app",
    "smoke_workshop",
    "gut",
    "task1_contract",
    "model_integration",
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


class AmbiguousMutationError(RuntimeError):
    """Mutation may have committed but its response was lost; never blind-retry."""


class FastMCPBridgeClient:
    """Lazy FastMCP client adapter so static/unit validation has no MCP dependency."""

    def __init__(self, url: str = MCP_URL):
        self.url = url
        self._client = None

    async def __aenter__(self):
        fastmcp = importlib.import_module("fastmcp")
        self._client = fastmcp.Client(self.url)
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._client is not None:
            return await self._client.__aexit__(exc_type, exc, tb)
        return None

    async def list_tool_names(self) -> set[str]:
        if self._client is None:
            raise RuntimeError("FastMCPBridgeClient is not connected")
        tools = await self._client.list_tools()
        return {str(tool.name) for tool in tools}

    async def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if self._client is None:
            raise RuntimeError("FastMCPBridgeClient is not connected")
        result = await self._client.call_tool(name, arguments)
        if result.data is not None:
            if isinstance(result.data, dict):
                return copy.deepcopy(result.data)
            raise ValueError(f"MCP tool {name!r} returned non-object data")
        if isinstance(result.structured_content, dict):
            return copy.deepcopy(result.structured_content)
        for block in result.content:
            text = getattr(block, "text", None)
            if isinstance(text, str) and text.lstrip().startswith("{"):
                payload = json.loads(text)
                if isinstance(payload, dict):
                    return payload
        raise ValueError(f"MCP tool {name!r} returned no structured object")


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_recipe(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("recipe must be a JSON object")
    validate_recipe(payload)
    validate_executable_recipe(payload)
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

    if not all(isinstance(item, dict) and set(item) == {"tool", "arguments"} for item in operations):
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


def validate_executable_recipe(recipe: dict[str, Any]) -> None:
    operations = recipe.get("operations")
    if not isinstance(operations, list) or not operations:
        raise ValueError("executable recipe operations must be a non-empty list")
    project_writes = 0
    for index, item in enumerate(operations):
        if not isinstance(item, dict) or set(item) != {"tool", "arguments"}:
            raise ValueError(f"operation {index} must contain exactly tool and arguments")
        tool = item["tool"]
        arguments = item["arguments"]
        if tool not in ALLOWED_NATIVE_TOOLS:
            raise ValueError(f"operation {index} uses non-allowlisted tool {tool!r}")
        if tool in FORBIDDEN_WRITER_TOOLS or "filesystem" in tool:
            raise ValueError(f"operation {index} uses forbidden writer {tool!r}")
        if not isinstance(arguments, dict) or "session_id" in arguments:
            raise ValueError(f"operation {index} arguments must be an object without session_id")
        if tool == "node_manage" and arguments.get("op") == "attach_script":
            raise ValueError("node_manage has no attach_script op in HiGodot 3.1.3")
        if tool == "ui_manage" and arguments.get("op") not in {
            "set_anchor_preset", "set_text", "build_layout", "draw_recipe"
        }:
            raise ValueError("ui_manage op is not available in HiGodot 3.1.3")
        if tool == "node_set_property" and arguments.get("property") == "script":
            if arguments.get("value") not in APPROVED_SCRIPT_PATHS:
                raise ValueError("script property points outside approved Task 2 scripts")
        if tool == "project_manage":
            if arguments.get("op") == "settings_set":
                project_writes += 1
                params = arguments.get("params")
                if not isinstance(params, dict):
                    raise ValueError("project settings_set requires params")
                if params.get("key") != "application/run/main_scene" or params.get("value") != EXPECTED_MAIN_SCENE:
                    raise ValueError("project_manage may only set the approved main scene")
            elif arguments.get("op") != "settings_get":
                raise ValueError("project_manage op is outside Task 2 scope")
    if project_writes != 1:
        raise ValueError("executable recipe must contain exactly one main-scene write")


def required_mcp_tools(recipe: dict[str, Any]) -> set[str]:
    operations = recipe.get("operations", [])
    return PREFLIGHT_TOOLS | {str(item["tool"]) for item in operations}


def _normalize_project_path(value: str) -> str:
    return value.replace("\\", "/").rstrip("/")


def _require_session_identity(session: dict[str, Any], expected_project_path: str) -> None:
    if _normalize_project_path(str(session.get("project_path", ""))) != _normalize_project_path(expected_project_path):
        raise ValueError("session project_path mismatch")
    if session.get("plugin_version") != TARGET_HIGODOT_VERSION:
        raise ValueError(f"HiGodot plugin must be {TARGET_HIGODOT_VERSION}")
    if session.get("server_version") != TARGET_HIGODOT_VERSION:
        raise ValueError(f"HiGodot server must be {TARGET_HIGODOT_VERSION}")
    if not str(session.get("godot_version", "")).startswith("4.7.1"):
        raise ValueError("Godot editor must be 4.7.1")
    if session.get("readiness") != "ready":
        raise ValueError("Godot editor session is not ready")
    if session.get("server_launch_mode") != "uvx":
        raise ValueError("HiGodot server launch mode must be uvx")


async def _discover_project_session(
    client,
    expected_project_path: str,
    *,
    attempts: int = SESSION_DISCOVERY_ATTEMPTS,
    delay_seconds: float = SESSION_DISCOVERY_DELAY_SECONDS,
) -> dict[str, Any]:
    if attempts < 1:
        raise ValueError("session discovery attempts must be at least 1")
    if delay_seconds < 0:
        raise ValueError("session discovery delay must be non-negative")

    expected = _normalize_project_path(expected_project_path)
    for attempt in range(attempts):
        listing = await client.call("session_manage", {"op": "list", "params": {}})
        sessions = listing.get("sessions")
        if not isinstance(sessions, list):
            raise ValueError("session_manage(list) returned invalid sessions payload")
        matches = [
            item
            for item in sessions
            if isinstance(item, dict)
            and _normalize_project_path(str(item.get("project_path", ""))) == expected
        ]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise ValueError(f"expected exactly one Blacksmith project session, found {len(matches)}")
        if attempt + 1 < attempts:
            await asyncio.sleep(delay_seconds)

    raise ValueError("expected exactly one Blacksmith project session, found 0")


async def preflight_mcp(client, recipe: dict[str, Any], expected_project_path: str) -> dict[str, Any]:
    available = await client.list_tool_names()
    missing = required_mcp_tools(recipe) - set(available)
    if missing:
        raise ValueError(f"required MCP tools are unavailable: {sorted(missing)}")

    session = await _discover_project_session(client, expected_project_path)
    _require_session_identity(session, expected_project_path)
    session_id = str(session.get("session_id", ""))
    if not session_id:
        raise ValueError("matching session is missing session_id")

    activated = await client.call("session_activate", {"session_id": session_id})
    if activated.get("status") != "ok" or activated.get("active_session_id") != session_id:
        raise ValueError("session activation was not confirmed")

    editor = await client.call("editor_state", {"session_id": session_id})
    if editor.get("readiness") != "ready" or editor.get("is_playing") is not False:
        raise ValueError("editor_state is not writable/ready")
    if editor.get("project_name") != "Blacksmith":
        raise ValueError("editor_state project_name mismatch")
    if not str(editor.get("godot_version", "")).startswith("4.7.1"):
        raise ValueError("editor_state Godot version mismatch")

    hierarchy = await client.call(
        "scene_get_hierarchy",
        {"depth": 10, "offset": 0, "limit": 100, "session_id": session_id},
    )
    if not isinstance(hierarchy.get("nodes"), list):
        raise ValueError("scene_get_hierarchy returned invalid nodes payload")

    project_setting = await client.call(
        "project_manage",
        {
            "op": "settings_get",
            "params": {"key": "application/run/main_scene"},
            "session_id": session_id,
        },
    )
    if project_setting.get("key") != "application/run/main_scene":
        raise ValueError("project settings readback returned the wrong key")

    return {
        "session_id": session_id,
        "session": copy.deepcopy(session),
        "editor_state": editor,
        "hierarchy": hierarchy,
        "project_setting": project_setting,
        "available_tools": sorted(available),
    }


def recipe_operation_to_call(item: dict[str, Any], session_id: str) -> tuple[str, dict[str, Any]]:
    if not isinstance(item, dict) or set(item) != {"tool", "arguments"}:
        raise ValueError("recipe operation must contain tool and arguments")
    name = str(item["tool"])
    arguments = copy.deepcopy(item["arguments"])
    if not isinstance(arguments, dict):
        raise ValueError("recipe operation arguments must be an object")
    if "session_id" in arguments and arguments["session_id"] != session_id:
        raise ValueError("recipe operation carries a conflicting session_id")
    arguments["session_id"] = session_id
    return name, arguments


async def _readback_after_ambiguous(client, tool: str, arguments: dict[str, Any], session_id: str) -> dict[str, Any]:
    if tool == "project_manage" and arguments.get("op") == "settings_set":
        params = arguments.get("params") or {}
        return await client.call(
            "project_manage",
            {"op": "settings_get", "params": {"key": params.get("key")}, "session_id": session_id},
        )
    return await client.call(
        "scene_get_hierarchy",
        {"depth": 10, "offset": 0, "limit": 100, "session_id": session_id},
    )


async def execute_recipe_operations(client, recipe: dict[str, Any], session_id: str) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for item in recipe.get("operations", []):
        tool, arguments = recipe_operation_to_call(item, session_id)
        arguments_hash = canonical_json_sha256(arguments)
        try:
            result = await client.call(tool, arguments)
        except (TimeoutError, ConnectionError) as exc:
            readback = await _readback_after_ambiguous(client, tool, arguments, session_id)
            raise AmbiguousMutationError(
                f"ambiguous {tool} mutation after {type(exc).__name__}; "
                f"readback_sha256={canonical_json_sha256(readback)}"
            ) from exc
        evidence.append(
            {
                "tool": tool,
                "arguments_sha256": arguments_hash,
                "success": True,
                "result_sha256": canonical_json_sha256(result),
                "error": None,
            }
        )
    return evidence


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


def _require_sha256(value: Any, field: str) -> None:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise ValueError(f"{field} must be a lowercase SHA-256 hex digest")


def validate_post_authoring_validations(
    evidence: dict[str, dict[str, str]],
) -> dict[str, dict[str, str]]:
    if not isinstance(evidence, dict) or set(evidence) != REQUIRED_POST_AUTHORING_VALIDATIONS:
        raise ValueError("validation evidence must equal the exact required set")
    normalized: dict[str, dict[str, str]] = {}
    for name in sorted(REQUIRED_POST_AUTHORING_VALIDATIONS):
        record = evidence.get(name)
        if not isinstance(record, dict) or set(record) != {"status", "sha256"}:
            raise ValueError(f"validation {name!r} must contain status and sha256 only")
        if record.get("status") != "PASS":
            raise ValueError(f"validation {name!r} must be PASS")
        _require_sha256(record.get("sha256"), f"validation {name!r} SHA-256")
        normalized[name] = {"status": "PASS", "sha256": str(record["sha256"])}
    return normalized


def build_provenance(
    context: dict[str, Any],
    operations: list[dict[str, Any]],
    hashes: dict[str, str],
    validations: dict[str, Any],
) -> dict[str, Any]:
    return {
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
    for name, record in validations.items():
        if not isinstance(record, dict) or record.get("status") != "PASS":
            raise ValueError(f"validation {name!r} must be PASS")
        _require_sha256(record.get("sha256"), f"validations[{name!r}].sha256")
    artifacts = payload.get("artifact_sha256")
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("artifact_sha256 must contain at least one artifact digest")
    for name, digest in artifacts.items():
        _require_sha256(digest, f"artifact_sha256[{name!r}]")
