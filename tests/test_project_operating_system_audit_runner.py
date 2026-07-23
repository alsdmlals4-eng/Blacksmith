from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
