from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from tools import higodot_task2_bridge as bridge


MANIFEST_NAME = "higodot-task2-provenance.json"
SENSITIVE_KEY_FRAGMENTS = (
    "token",
    "secret",
    "password",
    "authorization",
    "cookie",
    "credential",
)
SENSITIVE_EXACT_KEYS = {"env", "environ", "environment"}
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
sha256_file = bridge.sha256_file


def assert_no_sensitive_provenance_fields(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in SENSITIVE_EXACT_KEYS or any(fragment in normalized for fragment in SENSITIVE_KEY_FRAGMENTS):
                raise ValueError(f"sensitive provenance field is forbidden: {path}.{key}")
            assert_no_sensitive_provenance_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_sensitive_provenance_fields(child, f"{path}[{index}]")


def validate_provenance_schema_contract(schema: dict[str, Any]) -> None:
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise ValueError("provenance schema must use JSON Schema draft 2020-12")
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        raise ValueError("provenance schema top-level object must fail closed")
    if set(schema.get("required", [])) != bridge.REQUIRED_PROVENANCE_FIELDS:
        raise ValueError("provenance schema required fields do not match bridge contract")
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise ValueError("provenance schema properties are missing")
    if properties.get("repository", {}).get("const") != bridge.TARGET_REPOSITORY:
        raise ValueError("provenance schema repository const is not canonical")
    if properties.get("pr_number", {}).get("const") != bridge.TARGET_PR:
        raise ValueError("provenance schema PR const is not canonical")
    changed_items = properties.get("changed_paths", {}).get("items", {}).get("enum", [])
    if set(changed_items) != set(bridge.ALLOWED_SERIALIZED_PATHS):
        raise ValueError("provenance schema changed_paths allowlist is not canonical")
    serialized = properties.get("serialized_sha256", {})
    if set(serialized.get("required", [])) != set(bridge.ALLOWED_SERIALIZED_PATHS):
        raise ValueError("provenance schema serialized_sha256 keys are not canonical")
    if serialized.get("additionalProperties") is not False:
        raise ValueError("provenance schema serialized_sha256 must reject extra keys")


def _load_schema(schema_path: Path) -> dict[str, Any]:
    payload = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("provenance schema must be a JSON object")
    validate_provenance_schema_contract(payload)
    return payload


def _expected_artifact_hash_keys() -> set[str]:
    product = {f"product/{path}" for path in bridge.ALLOWED_SERIALIZED_PATHS}
    validation = {
        f"validation/{name}.evidence"
        for name in bridge.REQUIRED_POST_AUTHORING_VALIDATIONS
    }
    return product | validation


def _actual_artifact_files(artifact_root: Path) -> set[str]:
    return {
        path.relative_to(artifact_root).as_posix()
        for path in artifact_root.rglob("*")
        if path.is_file()
    }


def _copy_exact(source: Path, destination: Path) -> str:
    if not source.is_file():
        raise ValueError(f"artifact source is missing: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = source.read_bytes()
    destination.write_bytes(payload)
    if destination.read_bytes() != payload:
        raise ValueError(f"artifact byte copy mismatch: {destination}")
    return bridge.sha256_file(destination)


def prepare_provenance_artifact(
    *,
    repo: Path,
    artifact_root: Path,
    context: dict[str, Any],
    operations: list[dict[str, Any]],
    serialized_hashes: dict[str, str],
    validations: dict[str, dict[str, str]],
    validation_files: dict[str, Path],
    expected_head: str,
    schema_path: Path,
) -> dict[str, Any]:
    assert_no_sensitive_provenance_fields(context)
    assert_no_sensitive_provenance_fields(operations)
    assert_no_sensitive_provenance_fields(validations)
    _load_schema(schema_path)

    if context.get("input_head_sha") != expected_head:
        raise ValueError("context input head does not match expected head")
    if set(serialized_hashes) != set(bridge.ALLOWED_SERIALIZED_PATHS):
        raise ValueError("serialized hashes do not match exact product allowlist")
    validations = bridge.validate_post_authoring_validations(validations)
    if set(validation_files) != bridge.REQUIRED_POST_AUTHORING_VALIDATIONS:
        raise ValueError("validation files do not match exact required set")
    if artifact_root.exists():
        raise ValueError("artifact root must not pre-exist")

    artifact_hashes: dict[str, str] = {}
    for relative in sorted(bridge.ALLOWED_SERIALIZED_PATHS):
        source = repo / relative
        source_hash = bridge.sha256_file(source)
        if source_hash != serialized_hashes[relative]:
            raise ValueError(f"serialized source hash mismatch: {relative}")
        artifact_relative = f"product/{relative}"
        copied_hash = _copy_exact(source, artifact_root / artifact_relative)
        if copied_hash != source_hash:
            raise ValueError(f"serialized artifact hash mismatch: {relative}")
        artifact_hashes[artifact_relative] = copied_hash

    for name in sorted(bridge.REQUIRED_POST_AUTHORING_VALIDATIONS):
        source = validation_files[name]
        source_hash = bridge.sha256_file(source)
        if source_hash != validations[name]["sha256"]:
            raise ValueError(f"validation source hash mismatch: {name}")
        artifact_relative = f"validation/{name}.evidence"
        copied_hash = _copy_exact(source, artifact_root / artifact_relative)
        if copied_hash != source_hash:
            raise ValueError(f"validation artifact hash mismatch: {name}")
        artifact_hashes[artifact_relative] = copied_hash

    manifest_context = copy.deepcopy(context)
    manifest_context["changed_paths"] = sorted(bridge.ALLOWED_SERIALIZED_PATHS)
    manifest_context["artifact_sha256"] = dict(sorted(artifact_hashes.items()))
    manifest = bridge.build_provenance(
        manifest_context,
        copy.deepcopy(operations),
        dict(sorted(serialized_hashes.items())),
        validations,
    )
    assert_no_sensitive_provenance_fields(manifest)
    bridge.validate_provenance(manifest, expected_head)

    manifest_path = artifact_root / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    validate_provenance_artifact(artifact_root, expected_head, schema_path)
    return manifest


def validate_provenance_artifact(
    artifact_root: Path,
    expected_head: str,
    schema_path: Path,
) -> dict[str, Any]:
    _load_schema(schema_path)
    manifest_path = artifact_root / MANIFEST_NAME
    if not manifest_path.is_file():
        raise ValueError("provenance manifest is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("provenance manifest must be an object")
    assert_no_sensitive_provenance_fields(manifest)
    bridge.validate_provenance(manifest, expected_head)
    bridge.validate_post_authoring_validations(manifest["validations"])

    artifact_hashes = manifest.get("artifact_sha256")
    expected_hash_keys = _expected_artifact_hash_keys()
    if not isinstance(artifact_hashes, dict) or set(artifact_hashes) != expected_hash_keys:
        raise ValueError("artifact hash set does not match exact provenance bundle")

    expected_files = {MANIFEST_NAME} | expected_hash_keys
    actual_files = _actual_artifact_files(artifact_root)
    if actual_files != expected_files:
        raise ValueError(
            f"artifact file set mismatch: expected {sorted(expected_files)}, got {sorted(actual_files)}"
        )

    for relative in sorted(expected_hash_keys):
        actual_hash = bridge.sha256_file(artifact_root / relative)
        expected_hash = artifact_hashes[relative]
        if actual_hash != expected_hash:
            raise ValueError(f"artifact hash mismatch: {relative}")

    serialized = manifest["serialized_sha256"]
    for relative in sorted(bridge.ALLOWED_SERIALIZED_PATHS):
        if artifact_hashes[f"product/{relative}"] != serialized[relative]:
            raise ValueError(f"product artifact hash does not match serialized hash: {relative}")

    validations = manifest["validations"]
    for name in sorted(bridge.REQUIRED_POST_AUTHORING_VALIDATIONS):
        if artifact_hashes[f"validation/{name}.evidence"] != validations[name]["sha256"]:
            raise ValueError(f"validation artifact hash does not match evidence hash: {name}")

    return manifest


def verify_publish_head(expected_head: str, actual_remote_head: str) -> None:
    if _SHA40.fullmatch(expected_head or "") is None or _SHA40.fullmatch(actual_remote_head or "") is None:
        raise ValueError("publish head values must be lowercase 40-hex commit SHAs")
    if actual_remote_head != expected_head:
        raise ValueError(
            f"publish target branch moved: expected {expected_head}, got {actual_remote_head}"
        )


def _git_status_porcelain(repo: Path) -> list[str]:
    output = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [line for line in output.splitlines() if line.strip()]


def stage_proven_artifact(
    artifact_root: Path,
    checkout_root: Path,
    expected_head: str,
    schema_path: Path,
) -> dict[str, Any]:
    manifest = validate_provenance_artifact(artifact_root, expected_head, schema_path)
    if _git_status_porcelain(checkout_root):
        raise ValueError("publish checkout must be clean before staging proven bytes")

    for relative in sorted(bridge.ALLOWED_SERIALIZED_PATHS):
        source = artifact_root / "product" / relative
        destination = checkout_root / relative
        copied_hash = _copy_exact(source, destination)
        expected_hash = manifest["serialized_sha256"][relative]
        if copied_hash != expected_hash:
            raise ValueError(f"staged product hash mismatch: {relative}")

    changed = bridge.git_changed_paths(checkout_root)
    if len(changed) != len(bridge.ALLOWED_SERIALIZED_PATHS) or set(changed) != set(bridge.ALLOWED_SERIALIZED_PATHS):
        raise ValueError(f"staged publish diff escaped exact allowlist: {changed}")

    for relative in sorted(bridge.ALLOWED_SERIALIZED_PATHS):
        actual_hash = bridge.sha256_file(checkout_root / relative)
        if actual_hash != manifest["serialized_sha256"][relative]:
            raise ValueError(f"staged checkout hash mismatch: {relative}")

    return manifest
