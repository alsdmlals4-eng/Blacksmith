from __future__ import annotations

import platform
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping

REQUIRED_MATRIX_LANES: dict[str, tuple[str, str]] = {
    "windows-py311": ("windows", "3.11"),
    "windows-py312": ("windows", "3.12"),
    "windows-py313": ("windows", "3.13"),
    "wsl-ubuntu-py312": ("wsl-ubuntu", "3.12"),
}


@dataclass(frozen=True)
class PackEvaluation:
    status: str
    missing_lanes: list[str]
    failed_lanes: list[str]
    unexpected_lanes: list[str]
    full_lane_valid: bool


def detect_platform_kind(
    *,
    system: str | None = None,
    release: str | None = None,
    proc_version: str | None = None,
    os_release: str | None = None,
) -> str:
    system_value = system if system is not None else platform.system()
    release_value = release if release is not None else platform.release()
    if system_value == "Windows":
        return "windows"
    if system_value != "Linux":
        return "unsupported"
    if proc_version is None:
        try:
            proc_version = Path("/proc/version").read_text(encoding="utf-8")
        except OSError:
            proc_version = ""
    if os_release is None:
        try:
            os_release = Path("/etc/os-release").read_text(encoding="utf-8")
        except OSError:
            os_release = ""
    is_wsl = "microsoft" in f"{release_value}\n{proc_version}".lower()
    ubuntu = (
        re.search(r"(?m)^ID=['\"]?ubuntu['\"]?\s*$", os_release)
        is not None
    )
    return "wsl-ubuntu" if is_wsl and ubuntu else "unsupported"


def lane_is_valid(manifest: Mapping[str, object], expected_head: str) -> bool:
    lane_id = manifest.get("lane_id")
    if not isinstance(lane_id, str) or lane_id not in REQUIRED_MATRIX_LANES:
        return False
    expected_platform, expected_python = REQUIRED_MATRIX_LANES[lane_id]
    return all(
        (
            manifest.get("validation_mode") == "LOCAL_PYTHON_MATRIX_LANE",
            manifest.get("platform_kind") == expected_platform,
            manifest.get("detected_platform_kind") == expected_platform,
            manifest.get("python_required") == expected_python,
            manifest.get("python_version_match") is True,
            manifest.get("status") == "PASS",
            manifest.get("head_sha") == expected_head,
            manifest.get("exact_head") is True,
            manifest.get("clean_before") is True,
            manifest.get("clean_after") is True,
            manifest.get("authoring_surface_hash_unchanged") is True,
        )
    )


def authoritative_manifest_is_valid(
    manifest: Mapping[str, object],
    expected_head: str,
) -> bool:
    environment = manifest.get("environment")
    operating_base = manifest.get("operating_base")
    contract_base = manifest.get("contract_base")
    if not isinstance(environment, Mapping):
        return False
    if not isinstance(operating_base, Mapping):
        return False
    if not isinstance(contract_base, Mapping):
        return False
    platform_value = environment.get("platform")
    return all(
        (
            manifest.get("validation_mode")
            == "LOCAL_EXACT_HEAD_NO_GITHUB_ACTIONS",
            manifest.get("status") == "PASS",
            manifest.get("head_sha") == expected_head,
            manifest.get("expected_head_sha") == expected_head,
            manifest.get("exact_head") is True,
            manifest.get("clean_before") is True,
            manifest.get("clean_after") is True,
            manifest.get("authoring_surface_hash_unchanged") is True,
            isinstance(platform_value, str)
            and platform_value.startswith("Windows"),
            environment.get("python_version_match") is True,
            operating_base.get("pin_match") is True,
            operating_base.get("workflow_pin_match") is True,
            contract_base.get("pin_match") is True,
            contract_base.get("workflow_pin_match") is True,
            manifest.get("protected_base_valid") is True,
            manifest.get("godot_required") is True,
            manifest.get("godot_present") is True,
        )
    )


def evaluate_pack(
    full_manifest: Mapping[str, object],
    lane_manifests: Iterable[Mapping[str, object]],
    expected_head: str,
) -> PackEvaluation:
    lanes_by_id: dict[str, Mapping[str, object]] = {}
    duplicate_lanes: set[str] = set()
    unexpected_lanes: set[str] = set()
    for manifest in lane_manifests:
        lane_id = manifest.get("lane_id")
        if not isinstance(lane_id, str):
            unexpected_lanes.add("<missing-lane-id>")
            continue
        if lane_id not in REQUIRED_MATRIX_LANES:
            unexpected_lanes.add(lane_id)
            continue
        if lane_id in lanes_by_id:
            duplicate_lanes.add(lane_id)
        lanes_by_id[lane_id] = manifest

    missing = sorted(set(REQUIRED_MATRIX_LANES) - set(lanes_by_id))
    failed = sorted(
        lane_id
        for lane_id, manifest in lanes_by_id.items()
        if not lane_is_valid(manifest, expected_head)
    )
    failed = sorted(set(failed) | duplicate_lanes)
    unexpected = sorted(unexpected_lanes)
    full_valid = authoritative_manifest_is_valid(full_manifest, expected_head)
    status = (
        "PASS"
        if full_valid and not missing and not failed and not unexpected
        else "FAIL"
    )
    return PackEvaluation(status, missing, failed, unexpected, full_valid)
