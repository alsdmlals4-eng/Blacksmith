from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

spec = importlib.util.spec_from_file_location(
    "run_project_operating_system_audit",
    TOOLS / "run_project_operating_system_audit.py",
)
assert spec is not None and spec.loader is not None
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

import audit_project_operating_system as audit


class PlannedReferenceClassificationTests(unittest.TestCase):
    def test_missing_plan_path_becomes_warning(self) -> None:
        finding = audit.Finding(
            severity="ERROR",
            code="BROKEN_LOCAL_REFERENCE",
            message="docs/superpowers/plans/example.md -> scripts/future.gd",
        )

        runner.classify_planned_references([finding])

        self.assertEqual(finding.severity, "WARNING")
        self.assertEqual(finding.code, "PLANNED_PATH_NOT_YET_CREATED")

    def test_missing_active_reference_remains_error(self) -> None:
        finding = audit.Finding(
            severity="ERROR",
            code="BROKEN_LOCAL_REFERENCE",
            message="README.md -> docs/missing.md",
        )

        runner.classify_planned_references([finding])

        self.assertEqual(finding.severity, "ERROR")
        self.assertEqual(finding.code, "BROKEN_LOCAL_REFERENCE")

    def test_other_plan_finding_remains_error(self) -> None:
        finding = audit.Finding(
            severity="ERROR",
            code="DOCUMENT_SOURCE_MISSING",
            message="docs/superpowers/plans/example.md",
        )

        runner.classify_planned_references([finding])

        self.assertEqual(finding.severity, "ERROR")
        self.assertEqual(finding.code, "DOCUMENT_SOURCE_MISSING")


class CurrentAssertionConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_assertions = copy.deepcopy(audit.REQUIRED_ASSERTIONS)
        self.original_active_docs = tuple(audit.ACTIVE_DOCS)

    def tearDown(self) -> None:
        audit.REQUIRED_ASSERTIONS = self.original_assertions
        audit.ACTIVE_DOCS = self.original_active_docs

    def test_registry_assertions_follow_approved_batch_006(self) -> None:
        runner.configure_current_assertions()
        tokens = audit.REQUIRED_ASSERTIONS["docs/planning/CURRENT_R2_CANON_REGISTRY.json"]
        self.assertIn('"stage_status":"R2_BATCH_006_APPROVED_MAIN_CANON"', tokens)
        self.assertIn('"status":"APPROVED_MERGED_PR120_MAIN_CANON"', tokens)
        self.assertIn('"vertical_slice_implementation":"APPROVED"', tokens)
        self.assertIn('"product_implementation":"BLOCKED"', tokens)
        self.assertNotIn('"stage_status":"R2_CHECKPOINT_005_CLOSED_MAIN_CANON"', tokens)
        self.assertNotIn('"status":"NOT_STARTED"', tokens)

    def test_r3_planning_authority_is_audited_without_opening_product_scope(self) -> None:
        runner.configure_current_assertions()
        registry = audit.REQUIRED_ASSERTIONS[runner.R3_REGISTRY]
        nadia = audit.REQUIRED_ASSERTIONS[runner.R3_NADIA_CANON]
        toren = audit.REQUIRED_ASSERTIONS[runner.R3_TOREN_CANON]
        marek = audit.REQUIRED_ASSERTIONS[runner.R3_MAREK_CANON]
        ersa = audit.REQUIRED_ASSERTIONS[runner.R3_ERSA_CANON]
        cassia = audit.REQUIRED_ASSERTIONS[runner.R3_CASSIA_CANON]
        noble = audit.REQUIRED_ASSERTIONS[runner.R3_NOBLE_CANON]
        liana = audit.REQUIRED_ASSERTIONS[runner.R3_LIANA_CANON]
        self.assertIn('"stage_status": "R3_R7_DESIGN_ACTIVE"', registry)
        self.assertIn('"product_implementation": "BLOCKED"', registry)
        self.assertIn('"task3_implementation": "NOT_APPROVED"', registry)
        self.assertIn('"next_approval_counter": "7/10"', registry)
        for decision_id in (
            '"id": "BS-CONTENT-20260811-01"',
            '"id": "BS-CONTENT-20260811-02"',
            '"id": "BS-CONTENT-20260811-03"',
            '"id": "BS-CONTENT-20260811-04"',
            '"id": "BS-CONTENT-20260811-05"',
            '"id": "BS-CONTENT-20260811-06"',
            '"id": "BS-CONTENT-20260811-07"',
        ):
            self.assertIn(decision_id, registry)
        self.assertIn('"content_id": "COLLECTOR_01"', registry)
        self.assertIn('"customer_id": "ERSA_ROEN"', registry)
        self.assertIn('"content_id": "NOBLE_01"', registry)
        self.assertIn('"customer_id": "CEREMONIAL_NOBLE"', registry)
        self.assertIn("BS-CONTENT-20260811-01", nadia)
        self.assertIn("직접 전투·탐험 미니게임을 추가하지 않는다", nadia)
        self.assertIn("BS-CONTENT-20260811-02", toren)
        self.assertIn("JOURNEY_CONTINUITY_AND_RELIABILITY", toren)
        self.assertIn("FIELD_SERVICEABILITY", toren)
        self.assertIn("BS-CONTENT-20260811-03", marek)
        self.assertIn("SMALL_LOT_STANDARD_ORDER", marek)
        self.assertIn("BS-CONTENT-20260811-04", ersa)
        self.assertIn("EXHIBITION_EVIDENCE_AND_PROVENANCE", ersa)
        self.assertIn("SAME_ITEM_UID_PRESERVED", ersa)
        self.assertIn("BS-CONTENT-20260811-05", cassia)
        self.assertIn("ARENA_SIGNATURE_WEAPON_AND_LEGACY", cassia)
        self.assertIn("EQUIPMENT_CONTRIBUTION_STATE", cassia)
        self.assertIn("SAME_ITEM_UID_PRESERVED", cassia)
        self.assertIn("BS-CONTENT-20260811-06", noble)
        self.assertIn("HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY", noble)
        self.assertIn("NO_FULL_RESTORATION_ALWAYS_BEST", noble)
        self.assertIn("NO_HISTORY_ERASURE_ON_REPAIR", noble)
        self.assertIn("BS-CONTENT-20260811-07", liana)
        self.assertIn("SOLDIER_02", liana)
        self.assertIn("LIANA_BERG", liana)
        self.assertIn("FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY", liana)
        self.assertIn("MISSION_DUTY_STATE", liana)
        self.assertIn("COMMANDER_RETURN_STATE", liana)
        self.assertIn("ITEM_UID_FIELD_LEGACY_STATE", liana)
        self.assertIn("SAME_ITEM_UID_PRESERVED", liana)
        self.assertIn("NO_DIRECT_TACTICAL_COMBAT", liana)
        self.assertIn("NO_ITEM_AS_SOLE_CAUSE_OF_MISSION_RESULT", liana)
        self.assertIn("NO_BASELINE_PERMADEATH_FOR_LIANA", liana)
        for path in (
            runner.R3_REGISTRY,
            runner.R3_NADIA_CANON,
            runner.R3_TOREN_CANON,
            runner.R3_MAREK_CANON,
            runner.R3_ERSA_CANON,
            runner.R3_CASSIA_CANON,
            runner.R3_NOBLE_CANON,
            runner.R3_LIANA_CANON,
        ):
            self.assertIn(path, audit.ACTIVE_DOCS)

    def test_gate_assertions_keep_general_block_and_task2_closed_scope(self) -> None:
        runner.configure_current_assertions()
        tokens = audit.REQUIRED_ASSERTIONS["[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"]
        self.assertIn("GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED", tokens)
        self.assertIn("VERTICAL_SLICE_CODE_GATE: TASK2_MAIN_MERGED_NO_NEW_PRODUCT_SCOPE", tokens)
        self.assertIn("NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED", tokens)
        self.assertIn("R3_R7_DESIGN_ACTIVE", tokens)
        self.assertIn("R3_R7_APPROVAL_COUNTER: 8/10", tokens)
        self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08", tokens)
        self.assertIn("BS-CONTENT-20260811-03", tokens)
        self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", tokens)
        self.assertNotIn("VERTICAL_SLICE_CODE_GATE: USER_APPROVED", tokens)
        self.assertNotIn("CODEX_IMPLEMENTATION_GATE: BLOCKED", tokens)

    def test_handoff_router_assertions_do_not_duplicate_domain_artistry_contract(self) -> None:
        runner.configure_current_assertions()
        start = audit.REQUIRED_ASSERTIONS["[기획서]/00_프로젝트_허브/START_HERE.md"]
        active = audit.REQUIRED_ASSERTIONS["[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"]
        for tokens in (start, active):
            self.assertNotIn("예술성 27", tokens)
            self.assertNotIn("고정 설계 최대치 없음", tokens)
            self.assertIn("TASK2_MAIN_MERGED", tokens)
            self.assertIn("POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE", tokens)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", tokens)
            self.assertIn("R3_R7_DESIGN_ACTIVE", tokens)
            for decision_id in (
                "BS-CONTENT-20260811-01",
                "BS-CONTENT-20260811-02",
                "BS-CONTENT-20260811-03",
                "BS-CONTENT-20260811-04",
                "BS-CONTENT-20260811-05",
                "BS-CONTENT-20260811-06",
                "BS-CONTENT-20260811-07",
            ):
                self.assertIn(decision_id, tokens)
            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08", tokens)
            self.assertIn("COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED", tokens)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", tokens)
        self.assertNotIn("R2_CHECKPOINT_005", start)
        self.assertNotIn("현재 승인 카운터: `0/10`", active)
        self.assertNotIn("제품 구현: `BLOCKED`", active)
        self.assertIn("현재 R3–R7 승인 카운터: `7/10`", active)


if __name__ == "__main__":
    unittest.main()
