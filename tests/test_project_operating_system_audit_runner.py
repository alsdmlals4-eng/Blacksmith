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
        self.original = copy.deepcopy(audit.REQUIRED_ASSERTIONS)

    def tearDown(self) -> None:
        audit.REQUIRED_ASSERTIONS = self.original

    def test_registry_assertions_follow_approved_batch_006(self) -> None:
        runner.configure_current_assertions()
        tokens = audit.REQUIRED_ASSERTIONS["docs/planning/CURRENT_R2_CANON_REGISTRY.json"]
        self.assertIn('"stage_status":"R2_BATCH_006_APPROVED_MAIN_CANON"', tokens)
        self.assertIn('"status":"APPROVED_MERGED_PR120_MAIN_CANON"', tokens)
        self.assertIn('"vertical_slice_implementation":"APPROVED"', tokens)
        self.assertIn('"product_implementation":"BLOCKED"', tokens)
        self.assertNotIn('"stage_status":"R2_CHECKPOINT_005_CLOSED_MAIN_CANON"', tokens)
        self.assertNotIn('"status":"NOT_STARTED"', tokens)

    def test_gate_assertions_keep_general_block_and_task2_closed_scope(self) -> None:
        runner.configure_current_assertions()
        tokens = audit.REQUIRED_ASSERTIONS["[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"]
        self.assertIn("GENERAL_PRODUCT_IMPLEMENTATION: BLOCKED", tokens)
        self.assertIn("VERTICAL_SLICE_CODE_GATE: TASK2_MAIN_MERGED_NO_NEW_PRODUCT_SCOPE", tokens)
        self.assertIn("NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED", tokens)
        self.assertNotIn("VERTICAL_SLICE_CODE_GATE: USER_APPROVED", tokens)
        self.assertNotIn("CODEX_IMPLEMENTATION_GATE: BLOCKED", tokens)

    def test_handoff_router_assertions_do_not_duplicate_domain_artistry_contract(self) -> None:
        runner.configure_current_assertions()
        start = audit.REQUIRED_ASSERTIONS["[기획서]/00_프로젝트_허브/START_HERE.md"]
        active = audit.REQUIRED_ASSERTIONS["[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"]
        for tokens in (start, active):
            self.assertNotIn("예술성 27", tokens)
            self.assertNotIn("고정 설계 최대치 없음", tokens)
        self.assertNotIn("R2_CHECKPOINT_005", start)
        for token in (
            "TASK2_MAIN_MERGED",
            "POSTMERGE_CONTINUOUS_CI_CLOSURE_COMPLETE",
            "PRODUCT_IMPLEMENTATION: BLOCKED",
        ):
            self.assertIn(token, start)
            self.assertIn(token, active)


if __name__ == "__main__":
    unittest.main()
