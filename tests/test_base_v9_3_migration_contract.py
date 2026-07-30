from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_RELEASE = "30ca6c7b5f93521f0eb0eed42d01437cd43c50ae"
BASE_EVIDENCE = "462a86db192d23d0f386281a1eb54b0a8cbad62e"
BASE_REGISTRY_SHA256 = "9847bb2b225c776ad7916930f0f48c490bc2a898bea8e02ea1fdd0e6caac60c1"
SHEET_ID = "1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg"
LEGACY_BASE_SHA = "c987647d01ad2baa028a16e03d85ddfc1572a727"


class BaseV93MigrationContractTests(unittest.TestCase):
    def test_adapter_uses_released_v9_3_lock_and_current_sheet(self) -> None:
        adapter = json.loads((ROOT / "skills/PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        self.assertEqual(adapter["base_release"]["version"], "9.3.0")
        self.assertEqual(adapter["base_release"]["release_commit"], BASE_RELEASE)
        self.assertEqual(adapter["base_release"]["release_evidence_commit"], BASE_EVIDENCE)
        self.assertEqual(adapter["skill_registry"]["base"]["sha256"], BASE_REGISTRY_SHA256)
        self.assertEqual(adapter["gdd_sheet"]["sync_status"], "CURRENT")
        self.assertEqual(adapter["gdd_sheet"]["spreadsheet_id"], SHEET_ID)
        self.assertEqual(
            adapter["protected_paths"],
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
        )

    def test_project_registry_and_generated_views_share_v9_3_identity(self) -> None:
        registry = json.loads(
            (ROOT / "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        )
        integration = registry["base_integration"]
        self.assertEqual(integration["version"], "9.3.0")
        self.assertEqual(integration["release_commit"], BASE_RELEASE)
        self.assertEqual(integration["release_evidence_commit"], BASE_EVIDENCE)
        self.assertEqual(integration["registry_sha256"], BASE_REGISTRY_SHA256)
        self.assertEqual(
            integration["execution_prompt"],
            "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
        )

        for relative in ("skills/BASE_V9_ADAPTER.json", "skills/PROJECT_BASE_SKILL_ADAPTER.json"):
            view = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            self.assertEqual(view["base_release"]["version"], "9.3.0", relative)
            self.assertEqual(view["base_release"]["release_commit"], BASE_RELEASE, relative)
            self.assertEqual(view["base_release"]["release_evidence_commit"], BASE_EVIDENCE, relative)

        snapshot = json.loads((ROOT / "skills/PROJECT_SKILL_SNAPSHOT.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["base_registry"]["sha256"], BASE_REGISTRY_SHA256)
        self.assertEqual(len(snapshot["project_routes"]), 3)
        self.assertEqual(len(snapshot["effective_routes"]), 6)

    def test_active_operating_docs_use_vertical_slice_v9(self) -> None:
        for relative in ("AGENTS.md", "README.md", "docs/BASE_RULES_VERSION.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md", text, relative)
            self.assertIn(BASE_RELEASE, text, relative)
            self.assertNotIn("VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md", text, relative)
            self.assertNotIn(LEGACY_BASE_SHA, text, relative)

        application = (ROOT / "docs/operations/BLACKSMITH_VERTICAL_SLICE_V9_APPLICATION.md").read_text(
            encoding="utf-8"
        )
        reconciliation = (ROOT / "docs/operations/BLACKSMITH_V9_RECONCILIATION_PACKET.md").read_text(
            encoding="utf-8"
        )
        for token in ("APPLICATION_BINDING", BASE_RELEASE, SHEET_ID, "RECONCILIATION_PLANNING_PROFILE"):
            self.assertIn(token, application)
        for token in ("Legacy Requirement Traceability", "Critical Gate", "FND-V9-001"):
            self.assertIn(token, reconciliation)

    def test_future_ranking_server_contract_is_explicitly_not_implemented(self) -> None:
        contract = (ROOT / "docs/planning/BLACKSMITH_HIGH_GRADE_RANKING_SERVER_CONTRACT.md").read_text(
            encoding="utf-8"
        )
        for token in (
            "FUTURE_SERVER_READY",
            "NOT_IMPLEMENTED",
            "+50",
            "등급",
            "수식어",
            "SERVER_AUTHORITATIVE",
            "OFFLINE_FIRST",
            "idempotency",
            "클라이언트가 제출한 점수를 신뢰하지 않는다",
        ):
            self.assertIn(token, contract)

    def test_sheet_contract_records_v9_3_and_server_followup(self) -> None:
        workbook = (ROOT / "docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md").read_text(encoding="utf-8")
        for token in (SHEET_ID, BASE_RELEASE, "Base v9.3", "고등급 작품 랭킹", "NOT_IMPLEMENTED"):
            self.assertIn(token, workbook)


if __name__ == "__main__":
    unittest.main()
