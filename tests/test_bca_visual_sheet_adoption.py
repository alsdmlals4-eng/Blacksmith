from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_VERSION = "9.4.0"
BASE_PAYLOAD_SHA = "a728712cb776ec98f4875914a580fcf7d0156593"
BASE_EVIDENCE_SHA = "ef1fba11167e4da0b298123b0c85ebd268191a42"
LEGACY_BCA_SHA = "c987647d01ad2baa028a16e03d85ddfc1572a727"
SHEET_ID = "1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg"
REGISTRY_PATH = "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json"


class BCAAdoptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads((ROOT / REGISTRY_PATH).read_text(encoding="utf-8"))
        cls.base_rules = (ROOT / "docs/BASE_RULES_VERSION.md").read_text(encoding="utf-8")
        cls.workbook = (ROOT / "docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md").read_text(
            encoding="utf-8"
        )

    def test_base_integration_matches_current_release_metadata(self) -> None:
        for token in (BASE_VERSION, BASE_PAYLOAD_SHA, BASE_EVIDENCE_SHA):
            self.assertIn(token, self.base_rules)
            self.assertIn(token, self.workbook)

        integration = self.registry["base_integration"]
        self.assertEqual(BASE_VERSION, integration["released_version"])
        self.assertEqual(BASE_PAYLOAD_SHA, integration["release_commit"])
        self.assertEqual(BASE_EVIDENCE_SHA, integration["evidence_commit"])
        self.assertNotIn(LEGACY_BCA_SHA, self.workbook)

    def test_sheet_workspace_contract_matches_registry(self) -> None:
        for token in (
            "PROJECT_SHEET_CONFIGURED",
            SHEET_ID,
            "USER_FACING_GDD_WORKSPACE",
            "PROPOSED_SHEET_CHANGE",
            "05_GDD_요약",
            "15_조작_게임규칙",
        ):
            self.assertIn(token, self.workbook)

        sheet = self.registry["bca_visual_sheet"]
        self.assertEqual(SHEET_ID, sheet["spreadsheet_id"])
        self.assertEqual("USER_FACING_GDD_WORKSPACE", sheet["workbook_role"])
        self.assertIn("05_GDD_요약", sheet["required_tabs"])
        self.assertIn("15_조작_게임규칙", sheet["required_tabs"])


if __name__ == "__main__":
    unittest.main()
