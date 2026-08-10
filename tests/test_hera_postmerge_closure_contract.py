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
CURRENT_MAIN = "fa9595b2df95897c915331a1cb5d9b1a583611f0"
BASE_MAIN = "637dad32c773c56a27d44d847518580848dee493"
INITIALIZER_DECISION_ID = "BS-VS-INIT-20260808-01"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git_blob_bytes(path: Path) -> bytes:
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT)


def test_hera_decision_is_closed_as_merged_main_canon() -> None:
    text = _text(DECISIONS)
    assert DECISION_ID in text
    assert "MERGED_PR132_MAIN_CANON" in text
    assert "DRAFT_PR132_PENDING_MERGE" not in text


def test_entry_gate_records_merged_reconciliation_and_current_task2_authority() -> None:
    text = _text(GATES)
    assert f"PR132: MERGED_MAIN_CANON_{MERGE_MAIN}" in text
    assert f"PR131: MERGED_MAIN_CANON_{TASK2_MERGE_MAIN}" in text
    assert "TASK2: MAIN_MERGED_POSTMERGE_CI_CLOSURE_COMPLETE" in text
    assert "HIGODOT_PRODUCTION_EXECUTION_PATH: PROVEN_TASK2_COMPLETED" in text
    assert f"INITIALIZER_DECISION: {INITIALIZER_DECISION_ID}" in text
    assert "INITIALIZER_AUTHORITY: RESOLVED_USER_APPROVED" in text
    assert f"HIGODOT_ACTIVATION_DECISION: {HIGODOT_DECISION_ID}" in text
    assert "EXECUTION_PATH_BLOCKED" not in text
    assert "HERA_RECONCILIATION_DRAFT_PENDING_MERGE" not in text


def test_handoff_router_records_current_main_and_paused_design_boundary() -> None:
    active = _text(ACTIVE_CONTEXT)
    start = _text(START_HERE)

    for text in (active, start):
        assert CURRENT_MAIN in text
        assert BASE_MAIN in text
        assert "TASK2_MAIN_MERGED" in text
        assert "POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE" in text
        assert "PR81_REFERENCE_ONLY_DO_NOT_MERGE" in text
        assert "R3_R7_DESIGN_PAUSED" in text
        assert "ADVENTURER_01_DETAIL_PENDING" in text
        assert "PRODUCT_IMPLEMENTATION: BLOCKED" in text
        assert "HUMAN_PLAYTEST: NOT_RUN" in text
        assert "ANDROID_DEVICE: NOT_RUN" in text

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
    assert CURRENT_MAIN in text
    assert "PR131 = DRAFT_UNMERGED" not in text
    assert "BRIDGE_TDD = RED_NEXT" not in text


def test_current_decision_router_does_not_report_completed_higodot_path_as_blocked() -> None:
    text = _text(DECISIONS)
    assert HIGODOT_EXEC_DECISION_ID in text
    assert "TASK2_MAIN_MERGED / POSTMERGE_CI_CLOSURE_COMPLETE" in text
    assert "현재 실행 경로는 `BLOCKED_UNAVAILABLE_OR_UNVERIFIED`" not in text
    assert "PR #131 병합은 별도 승인" not in text


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
