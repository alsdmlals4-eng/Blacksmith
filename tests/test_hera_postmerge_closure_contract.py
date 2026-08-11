from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
START_HERE = ROOT / "[기획서]/00_프로젝트_허브/START_HERE.md"
HIGODOT_EXEC = ROOT / "docs/decisions/BS-HIGODOT-EXEC-20260808-01_TASK2_CI_AUTHORING_BRIDGE.md"
RECONCILIATION = ROOT / "docs/operations/BLACKSMITH_HERA_VENDOR_RECONCILIATION_2026-08-08.md"
HEALTH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"

DECISION_ID = "BS-HERA-20260808-01"
HIGODOT_DECISION_ID = "BS-HIGODOT-20260808-01"
HIGODOT_EXEC_DECISION_ID = "BS-HIGODOT-EXEC-20260808-01"
MERGE_MAIN = "29b06e323185e436d709fcdf638f445b9099266e"
TASK2_MERGE_MAIN = "a61a0bceec4254c4b78350980275cc9a903f9042"
TASK2_TECHNICAL_BASELINE = "fa9595b2df95897c915331a1cb5d9b1a583611f0"
CURRENT_HANDOFF_MAIN = "68540e6cd288aff138b1ea4c5b1feeb9e0653947"
BASE_CURRENT_MAIN_OBSERVED = "315c66eea9614c284b9c11c4d522141065dfa4b0"
PROJECT_BASE_ADAPTER_PIN = "2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b"
INITIALIZER_DECISION_ID = "BS-VS-INIT-20260808-01"
R3_FIRST_DECISION_ID = "BS-CONTENT-20260811-01"
R3_THIRD_DECISION_ID = "BS-CONTENT-20260811-03"
R3_CURRENT_DECISION_ID = "BS-CONTENT-20260811-04"
R3_CURRENT_RESUME_LOCATOR = "COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git_blob_bytes(path: Path) -> bytes:
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT)


def _markdown_section(text: str, heading: str) -> str:
    start = text.index(heading)
    remainder = text[start + len(heading) :]
    next_heading = remainder.find("\n## ")
    if next_heading == -1:
        return remainder
    return remainder[:next_heading]


def test_hera_decision_is_closed_as_merged_main_canon() -> None:
    text = _text(DECISIONS)
    assert DECISION_ID in text
    assert "MERGED_PR132_MAIN_CANON" in text
    assert "DRAFT_PR132_PENDING_MERGE" not in _markdown_section(text, "## 현재 운영 폐쇄 상태")


def test_entry_gate_records_merged_reconciliation_and_current_task2_authority() -> None:
    text = _text(GATES)
    current = _markdown_section(text, "## Current Gate Summary")
    assert f"PR132: MERGED_MAIN_CANON_{MERGE_MAIN}" in current
    assert f"PR131: MERGED_MAIN_CANON_{TASK2_MERGE_MAIN}" in current
    assert "TASK2: MAIN_MERGED_POSTMERGE_CI_CLOSURE_COMPLETE" in current
    assert "HIGODOT_PRODUCTION_EXECUTION_PATH: PROVEN_TASK2_COMPLETED" in current
    assert f"INITIALIZER_DECISION: {INITIALIZER_DECISION_ID}" in current
    assert "INITIALIZER_AUTHORITY: RESOLVED_USER_APPROVED" in current
    assert f"HIGODOT_ACTIVATION_DECISION: {HIGODOT_DECISION_ID}" in current
    assert "NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED" in current
    assert "EXECUTION_PATH_BLOCKED" not in current
    assert "HERA_RECONCILIATION_DRAFT_PENDING_MERGE" not in current


def test_handoff_router_records_current_main_and_r3_planning_only_boundary() -> None:
    active = _text(ACTIVE_CONTEXT)
    start = _text(START_HERE)

    for text in (active, start):
        assert CURRENT_HANDOFF_MAIN in text
        assert BASE_CURRENT_MAIN_OBSERVED in text
        assert PROJECT_BASE_ADAPTER_PIN in text
        assert "BASE_CURRENT_MAIN_OBSERVED" in text
        assert "PROJECT_BASE_ADAPTER_PIN" in text
        assert "TASK2_MAIN_MERGED" in text
        assert "POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE" in text
        assert "PR81_REFERENCE_ONLY_DO_NOT_MERGE" in text
        assert "R3_R7_DESIGN_ACTIVE" in text
        assert R3_FIRST_DECISION_ID in text
        assert R3_THIRD_DECISION_ID in text
        assert R3_CURRENT_DECISION_ID in text
        assert R3_CURRENT_RESUME_LOCATOR in text
        assert "PRODUCT_IMPLEMENTATION: BLOCKED" in text
        assert "TASK3_IMPLEMENTATION: NOT_APPROVED" in text
        assert "HUMAN_PLAYTEST: NOT_RUN" in text
        assert "ANDROID_DEVICE: NOT_RUN" in text
        assert "R3_R7_DESIGN_PAUSED" not in text
        assert "ADVENTURER_01_DETAIL_PENDING" not in text
        assert "NON_CANONICAL_RESUME_LOCATOR" not in text

    # Decision 01 remains discoverable as the first approved R3 history, while
    # current routing is allowed to advance to later approved planning decisions.
    assert "ADVENTURER_01" in active
    assert "ADVENTURER_01" in start
    assert "R2_BATCH_006_NOT_STARTED_0_OF_10" not in start
    assert "POSTMERGE_CLOSURE_PENDING" not in start
    assert "Task 1 Schema·UID·SaveEnvelope TDD" not in active


def test_higodot_execution_decision_records_actual_task2_closure_evidence() -> None:
    text = _text(HIGODOT_EXEC)
    assert HIGODOT_EXEC_DECISION_ID in text
    assert "TASK2_MAIN_MERGED" in text
    assert "POSTMERGE_CI_CLOSURE_COMPLETE" in text
    assert "02420ebd3bcdd86776c4ab70824738aa4071a168" in text
    assert "8afb9a439df46eec3568a75d7f2536b89e1edaba" in text
    assert "345cf339e2af754d447099dd8e1b278b80b849d5" in text
    assert TASK2_MERGE_MAIN in text
    assert TASK2_TECHNICAL_BASELINE in text
    current = _markdown_section(text, "## Current closure")
    assert "PR131 = MERGED" in current
    assert "BRIDGE_TDD = COMPLETE" in current
    assert "SCENE_PROJECT_MUTATION = HIGODOT_PROVEN_PUBLISHED" in current


def test_current_decision_router_preserves_task2_technical_baseline_and_r3_scope() -> None:
    text = _text(DECISIONS)
    current = _markdown_section(text, "## 현재 운영 폐쇄 상태")
    assert HIGODOT_EXEC_DECISION_ID in current
    assert "TASK2: TASK2_MAIN_MERGED" in current
    assert "POSTMERGE: POSTMERGE_CI_CLOSURE_COMPLETE" in current
    assert TASK2_MERGE_MAIN in current
    assert TASK2_TECHNICAL_BASELINE in current
    assert "NEW_PRODUCT_SCOPE_USER_DECISION_REQUIRED" in current
    assert "R3_R7_DESIGN_STATE: R3_R7_DESIGN_ACTIVE" in current
    assert f"R3_R7_CURRENT_DECISION: {R3_CURRENT_DECISION_ID}" in current
    assert "R3_R7_APPROVAL_COUNTER: 4/10" in current
    assert R3_THIRD_DECISION_ID in text
    assert "TASK3_IMPLEMENTATION: NOT_APPROVED" in current
    assert "PRODUCT_IMPLEMENTATION: BLOCKED" in current

    # The first R3 decision remains historical/current-canon evidence elsewhere;
    # it is not required to remain the current router forever.
    assert R3_FIRST_DECISION_ID in text

    # Historical activation-stage wording remains legitimate evidence below the
    # current closure router; this test intentionally does not require its deletion.
    assert "BLOCKED_UNAVAILABLE_OR_UNVERIFIED" in text


def test_reconciliation_evidence_records_postmerge_validation_truthfully() -> None:
    text = _text(RECONCILIATION)
    assert "status: USER_APPROVED_RECONCILIATION_MERGED_PR132_MAIN_CANON" in text
    assert f"merge_main: {MERGE_MAIN}" in text
    assert "postmerge_full_validation_run: 111" in text
    assert "postmerge_full_validation: PASS" in text
    assert "authority_workflow_startup_failure: PREEXISTING_ZERO_JOB_FAILURE_NOT_INTRODUCED_BY_PR132" in text


def test_operating_health_hash_tracks_current_decisions_after_closure() -> None:
    health = json.loads(_text(HEALTH))
    record = next(item for item in health["evidence"]["operating"] if item["id"] == "BS-CURRENT-DECISIONS")
    assert record["sha256"] == hashlib.sha256(_git_blob_bytes(DECISIONS)).hexdigest()