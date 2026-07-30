from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_RELEASE = "30ca6c7b5f93521f0eb0eed42d01437cd43c50ae"
BASE_EVIDENCE = "462a86db192d23d0f386281a1eb54b0a8cbad62e"
BASE_REGISTRY_SHA256 = "9847bb2b225c776ad7916930f0f48c490bc2a898bea8e02ea1fdd0e6caac60c1"
SHEET_ID = "1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg"


class BaseV9AdoptionTests(unittest.TestCase):
    def test_project_adapter_uses_released_base_v9_3(self) -> None:
        adapter = json.loads((ROOT / "skills/PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        self.assertEqual(adapter["base_release"]["version"], "9.3.0")
        self.assertEqual(adapter["base_release"]["release_commit"], BASE_RELEASE)
        self.assertEqual(adapter["base_release"]["release_evidence_commit"], BASE_EVIDENCE)
        self.assertEqual(adapter["skill_registry"]["base"]["sha256"], BASE_REGISTRY_SHA256)
        self.assertEqual(adapter["gdd_sheet"]["sync_status"], "CURRENT")
        self.assertEqual(adapter["gdd_sheet"]["spreadsheet_id"], SHEET_ID)
        self.assertEqual(adapter["validation"]["android_device"], "NOT_RUN")

    def test_v9_application_and_adversarial_gates_exist(self) -> None:
        application = (ROOT / "docs/operations/BLACKSMITH_VERTICAL_SLICE_V9_APPLICATION.md").read_text(
            encoding="utf-8"
        )
        reconciliation = (ROOT / "docs/operations/BLACKSMITH_V9_RECONCILIATION_PACKET.md").read_text(
            encoding="utf-8"
        )
        workflow = (ROOT / ".github/workflows/validate-base-v9-adoption.yml").read_text(encoding="utf-8")
        for token in (
            "APPLICATION_BINDING",
            "RECONCILIATION_PLANNING_PROFILE",
            BASE_RELEASE,
            SHEET_ID,
        ):
            self.assertIn(token, application)
        for token in ("Legacy Requirement Traceability", "Critical Gate", "NOT_RUN"):
            self.assertIn(token, reconciliation)
        self.assertIn("ci-gate", workflow)
        self.assertIn("adversarial-gate", workflow)


if __name__ == "__main__":
    unittest.main()
