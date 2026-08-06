from __future__ import annotations

from dataclasses import dataclass
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
    full_lane_valid: bool


def lane_is_valid(manifest: Mapping[str, object], expected_head: str) -> bool:
    lane_id = manifest.get("lane_id")
    if not isinstance(lane_id, str) or lane_id not in REQUIRED_MATRIX_LANES:
        return False
    expected_platform, expected_python = REQUIRED_MATRIX_LANES[lane_id]
    return all(
        (
            manifest.get("platform_kind") == expected_platform,
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


def evaluate_pack(
    full_manifest: Mapping[str, object],
    lane_manifests: Iterable[Mapping[str, object]],
    expected_head: str,
) -> PackEvaluation:
    lanes_by_id: dict[str, Mapping[str, object]] = {}
    duplicate_lanes: set[str] = set()
    for manifest in lane_manifests:
        lane_id = manifest.get("lane_id")
        if not isinstance(lane_id, str):
            continue
        if lane_id in lanes_by_id:
            duplicate_lanes.add(lane_id)
        lanes_by_id[lane_id] = manifest

    missing = sorted(set(REQUIRED_MATRIX_LANES) - set(lanes_by_id))
    failed = sorted(
        lane_id
        for lane_id, manifest in lanes_by_id.items()
        if lane_id in REQUIRED_MATRIX_LANES
        and not lane_is_valid(manifest, expected_head)
    )
    failed = sorted(set(failed) | duplicate_lanes)
    full_valid = all(
        (
            full_manifest.get("status") == "PASS",
            full_manifest.get("head_sha") == expected_head,
            full_manifest.get("expected_head_sha") == expected_head,
            full_manifest.get("exact_head") is True,
            full_manifest.get("clean_before") is True,
            full_manifest.get("clean_after") is True,
            full_manifest.get("authoring_surface_hash_unchanged") is True,
        )
    )
    status = "PASS" if full_valid and not missing and not failed else "FAIL"
    return PackEvaluation(status, missing, failed, full_valid)
