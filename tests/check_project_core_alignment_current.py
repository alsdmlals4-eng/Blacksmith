#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, Callable

import check_project_core_alignment as legacy

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
EXPECTED_BATCH_006 = [
    "BS-VS-20260806-01",
    "BS-SAVE-20260806-01",
    "BS-MATERIAL-20260806-01",
    "BS-CRAFT-20260806-01",
    "BS-ITEM-20260806-07",
    "BS-ENHANCE-20260806-01",
    "BS-ENHANCE-20260806-02",
    "BS-CATALYST-20260806-01",
    "BS-CUSTOMER-20260806-02",
    "BS-CHRONICLE-20260806-01",
]


def load_current(failures: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(R2.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"cannot read current R2 registry: {exc}")
        return {}
    if not isinstance(value, dict):
        failures.append("current R2 registry root must be an object")
        return {}
    return value


def check_current_batch_006(failures: list[str], registry: dict[str, Any]) -> None:
    expected = {
        "schema_version": 9,
        "stage_status": "R2_BATCH_006_APPROVED_MAIN_CANON",
        "next_approval_counter": "0/10",
        "product_implementation": "BLOCKED",
        "vertical_slice_implementation": "APPROVED",
        "implementation_scope": "VERTICAL_SLICE_NAMESPACES_ONLY",
        "human_playtest": "NOT_RUN",
    }
    for key, value in expected.items():
        if registry.get(key) != value:
            failures.append(f"current R2 registry {key!r} must equal {value!r}")

    active = registry.get("active_batch", {})
    active_expected = {
        "id": "R2_BATCH_006",
        "status": "APPROVED_MERGED_PR120_MAIN_CANON",
        "counter": "10/10",
        "approved_decisions": 10,
        "approved_count": 10,
        "maximum_size": 10,
        "maximum_count": 10,
        "planning_pr": 120,
        "planning_exact_head": "388eff03c61126d8021601c3ab84efaa2133253e",
        "planning_merge_sha": "a8a94343c78a68bf7bb14b411e7741f43b257138",
    }
    for key, value in active_expected.items():
        if active.get(key) != value:
            failures.append(f"active Batch 006 {key!r} must equal {value!r}")
    if active.get("decisions") != EXPECTED_BATCH_006:
        failures.append("active Batch 006 must contain the ten approved vertical-slice decisions in order")

    evidence = registry.get("immutable_merge_evidence", {}).get("batch_006", {})
    if evidence.get("planning_pr") != 120:
        failures.append("Batch 006 immutable evidence must reference PR #120")
    if evidence.get("planning_merge_sha") != "a8a94343c78a68bf7bb14b411e7741f43b257138":
        failures.append("Batch 006 immutable evidence has the wrong squash merge SHA")
    if evidence.get("status") != "USER_APPROVED_MERGED_MAIN_CANON":
        failures.append("Batch 006 immutable evidence must be user-approved main canon")

    decisions = {
        item.get("id"): item
        for item in registry.get("current_decisions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for decision_id in EXPECTED_BATCH_006:
        decision = decisions.get(decision_id)
        if not decision:
            failures.append(f"missing approved Batch 006 decision {decision_id}")
            continue
        if decision.get("status") != "USER_APPROVED_MERGED_PR120_MAIN_CANON":
            failures.append(f"{decision_id} must be approved and merged main canon")


def make_checkpoint_005_compatibility_view(registry: dict[str, Any]) -> dict[str, Any]:
    view = copy.deepcopy(registry)
    view["stage_status"] = "R2_CHECKPOINT_005_CLOSED_MAIN_CANON"
    view["next_approval_counter"] = "0/10"
    view["product_implementation"] = "BLOCKED"
    view["active_batch"] = {
        "id": "R2_BATCH_006",
        "status": "NOT_STARTED",
        "approved_decisions": 0,
        "approved_count": 0,
        "counter": "0/10",
        "decisions": [],
        "maximum_size": 10,
        "maximum_count": 10,
    }
    return view


def main() -> int:
    failures: list[str] = []
    registry = load_current(failures)
    if registry:
        check_current_batch_006(failures, registry)

    required = copy.deepcopy(legacy.REQUIRED_TEXT)

    gate_tokens = list(required["[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"])
    gate_tokens.remove("CODEX_IMPLEMENTATION_GATE: BLOCKED")
    gate_tokens.extend(
        [
            "GENERAL_PRODUCT_IMPLEMENTATION: APPROVED_WITHIN_EXISTING_CANON_NEW_SCOPE_REQUIRES_DECISION",
            "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON",
            "VERTICAL_SLICE_CODE_GATE: TASK2_MAIN_MERGED_NO_NEW_PRODUCT_SCOPE",
            "VERTICAL_SLICE_IMPLEMENTATION_APPROVED",
            "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED",
            "R3_R7_DESIGN_ACTIVE",
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
            "BS-CONTENT-20260811-05",
            "BS-CONTENT-20260811-06",
            "BS-CONTENT-20260811-07",
            "BS-CONTENT-20260811-08",
            "BS-CONTENT-20260811-09",
            "R3_R7_APPROVAL_COUNTER: 9/10",
            "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09",
            "GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED",
            "BS-OPS-20260811-03",
            "PLANNING_COMPLETE: USER_DECLARED",
            "P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING",
            "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED",
            "HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED",
            "HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED",
        ]
    )
    required["[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"] = tuple(gate_tokens)

    active_tokens = list(required["[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"])
    active_tokens.remove("현재 승인 카운터: `0/10`")
    active_tokens.remove("제품 구현: `BLOCKED`")
    active_tokens.extend(
        [
            "현재 R3–R7 승인 카운터: `9/10`",
            "R3_R7_DESIGN_ACTIVE",
            "R3_R7_APPROVAL_COUNTER: 9/10",
            "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09",
            "R3_R7_RESUME_LOCATOR: GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED",
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
            "BS-CONTENT-20260811-05",
            "BS-CONTENT-20260811-06",
            "BS-CONTENT-20260811-07",
            "BS-OPS-20260811-03",
            "PLANNING_COMPLETE: USER_DECLARED",
            "PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON",
            "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED",
            "P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING",
            "HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED",
            "HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED",
        ]
    )
    required["[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"] = tuple(active_tokens)

    original_required = legacy.REQUIRED_TEXT
    legacy.REQUIRED_TEXT = required
    try:
        legacy.check_text(failures)
    finally:
        legacy.REQUIRED_TEXT = original_required

    original_load: Callable[[Path, list[str]], dict[str, Any]] = legacy.load

    def compatibility_load(path: Path, nested_failures: list[str]) -> dict[str, Any]:
        value = original_load(path, nested_failures)
        if path == legacy.R2 and value:
            return make_checkpoint_005_compatibility_view(value)
        return value

    legacy.load = compatibility_load
    try:
        legacy.check_r2(failures)
    finally:
        legacy.load = original_load
    legacy.check_historical(failures)

    if failures:
        print("Project core alignment FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Project core alignment PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
