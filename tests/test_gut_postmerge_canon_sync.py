from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/testing/HIGODOT_GUT_AUTHORITY_POLICY.json"
MANIFEST = ROOT / "docs/testing/GUT_9_7_1_FORMAL_ADOPTION_MANIFEST.json"
SNAPSHOT = ROOT / "docs/operations/BLACKSMITH_ENTRY_GATE_SNAPSHOT_2026-08-06.json"

ADOPTION_MAIN_SHA = "2c4ae7eb244f1e6e01fd0392b747f8ffc3cee7eb"
VALIDATED_HEAD_SHA = "9ab46229946ae11529824fabefc6d558bd608d5d"
RUNTIME_RUN_ID = 31111242901


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_postmerge_policy_is_active_not_pending() -> None:
    policy = _json(POLICY)
    assert policy["adoption_state"] == "FORMALLY_ADOPTED_ACTIVE_TEST_FRAMEWORK_AUTHORITY"
    assert policy["effective_scope"] == "MAIN_CANON_AUTHORITY_GATE_AND_GUT_RUNTIME"
    assert policy["gut"]["status"] == "FORMALLY_ADOPTED_ACTIVE"
    assert policy["gut"]["config_present"] is True
    assert policy["gut"]["project_gut_test_root_present"] is True
    assert policy["gut"]["formal_ci_authority"] is True


def test_postmerge_manifest_pins_main_and_latest_runtime_evidence() -> None:
    manifest = _json(MANIFEST)
    assert manifest["decision_id"] == "BS-TEST-20260806-01"
    assert manifest["adoption_status"] == "MAIN_CANON_ACTIVE_TEST_FRAMEWORK_AUTHORITY"
    assert manifest["adoption_main_sha"] == ADOPTION_MAIN_SHA
    runtime = manifest["runtime_validation"]
    assert runtime["main_base_validation_head_sha"] == VALIDATED_HEAD_SHA
    assert runtime["workflow_run_id"] == RUNTIME_RUN_ID
    assert runtime["result"] == "PASS"
    assert runtime["junit"] == {"tests": 1, "failures": 0, "errors": 0, "skipped": 0}
    assert runtime["tracked_authoring_surface_hash"] == "UNCHANGED"


def test_entry_snapshot_matches_merged_main_but_preserves_blockers() -> None:
    snapshot = _json(SNAPSHOT)
    assert snapshot["source_main_sha"] == ADOPTION_MAIN_SHA
    assert snapshot["gut"]["aggregate"] == "FORMALLY_ADOPTED_ACTIVE"
    assert snapshot["gut"]["config_present"] is True
    assert snapshot["gut"]["project_test_root_present"] is True
    assert snapshot["gut"]["formal_ci_authority"] is True
    assert snapshot["general_product_implementation"] == "BLOCKED"
    assert snapshot["higodot"] == "PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY"
    assert snapshot["image_gate"]["aggregate"] == "BLOCKED_NOT_PRODUCT_READY"
    assert snapshot["entry_decision"] == (
        "AUTHORITY_GATE_MAIN_CANON / GUT_FORMALLY_ADOPTED / "
        "VISUAL_GATE_BLOCKED / GENERAL_PRODUCT_BLOCKED"
    )
