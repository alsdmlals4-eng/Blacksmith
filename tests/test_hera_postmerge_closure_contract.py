from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
RECONCILIATION = ROOT / "docs/operations/BLACKSMITH_HERA_VENDOR_RECONCILIATION_2026-08-08.md"
HEALTH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"

DECISION_ID = "BS-HERA-20260808-01"
MERGE_MAIN = "29b06e323185e436d709fcdf638f445b9099266e"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_hera_decision_is_closed_as_merged_main_canon() -> None:
    text = _text(DECISIONS)
    assert DECISION_ID in text
    assert "MERGED_PR132_MAIN_CANON" in text
    assert "DRAFT_PR132_PENDING_MERGE" not in text


def test_entry_gate_records_merged_reconciliation_and_keeps_task2_blocked() -> None:
    text = _text(GATES)
    assert "PR132: MERGED_MAIN_CANON_29b06e323185e436d709fcdf638f445b9099266e" in text
    assert "PR131: DESIGN_APPROVED_REBASE_REVIEW_PENDING" in text
    assert "TASK2_DESIGN_APPROVED_IMPLEMENTATION_BLOCKED" in text
    assert "HERA_RECONCILIATION_DRAFT_PENDING_MERGE" not in text


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
    assert record["sha256"] == hashlib.sha256(DECISIONS.read_bytes()).hexdigest()
