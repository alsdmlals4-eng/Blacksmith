from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"


class Collector02SedricArchivalAccessionContractTests(unittest.TestCase):
    def test_r3_registry_promotes_sedric_as_approved_eighth_content_decision(self) -> None:
        self.assertTrue(REGISTRY.is_file())
        registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
        self.assertEqual("R3_R7_DESIGN_ACTIVE", registry.get("stage_status"))
        self.assertEqual("BLOCKED", registry.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", registry.get("task3_implementation"))
        self.assertEqual("8/10", registry.get("next_approval_counter"))

        decisions = {item["id"]: item for item in registry.get("current_decisions", [])}
        for decision_id in (
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
            "BS-CONTENT-20260811-05",
            "BS-CONTENT-20260811-06",
            "BS-CONTENT-20260811-07",
            "BS-CONTENT-20260811-08",
        ):
            self.assertIn(decision_id, decisions)

        decision = decisions.get("BS-CONTENT-20260811-08", {})
        self.assertIn("USER_APPROVED_R3_R7_8_OF_10", decision.get("status", ""))
        contract = decision.get("contract", {})
        self.assertEqual("COLLECTOR_02", contract.get("content_id"))
        self.assertEqual("SEDRIC_VAEL", contract.get("customer_id"))
        self.assertEqual("COLLECTOR", contract.get("customer_archetype"))
        self.assertEqual("ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY", contract.get("activity_family"))
        self.assertEqual("ARCHIVAL_STEWARDSHIP_THROUGH_EXPLAINABLE_PROVENANCE_AND_CUSTODY", contract.get("content_goal"))
        self.assertEqual(
            "BLACKSMITH_ITEM_AND_HISTORY_DECISION_MAKER_NOT_ARCHIVE_MANAGER",
            contract.get("player_role"),
        )
        self.assertTrue(contract.get("existing_sedric_vael_customer_reused"))
        self.assertTrue(contract.get("same_item_uid_preserved"))
        self.assertTrue(contract.get("ersa_exhibition_responsibility_preserved"))
        self.assertTrue(contract.get("noble01_treatment_depth_responsibility_preserved"))
        for key in (
            "opaque_authenticity_provenance_or_archive_score",
            "oldest_item_always_best",
            "highest_artistry_always_best",
            "most_chronicle_events_always_best",
            "highest_enhancement_always_best",
            "document_fabrication",
            "unrecorded_history_autofill",
            "accession_count_artistry_growth",
            "appraisal_or_review_count_artistry_growth",
            "automatic_chronicle_affix_from_archiving",
            "archive_storage_management",
            "museum_management_sim",
            "visitor_management",
            "staff_or_shelf_management",
            "preservation_environment_simulation",
            "loan_logistics_management",
        ):
            self.assertFalse(contract.get(key), key)
        self.assertEqual(
            ["ARCHIVE_ACCESSION_STATE", "PROVENANCE_DOCUMENTATION_STATE", "ITEM_UID_CUSTODY_LEGACY_STATE"],
            contract.get("result_axes"),
        )
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", contract.get("task3_implementation"))
        self.assertEqual("NOT_RUN", contract.get("human_playtest"))

    def test_sedric_canon_separates_archival_accession_from_ersa_and_noble01(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-08",
            "COLLECTOR_02",
            "SEDRIC_VAEL",
            "ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY",
            "ARCHIVE_ACCESSION_STATE",
            "PROVENANCE_DOCUMENTATION_STATE",
            "ITEM_UID_CUSTODY_LEGACY_STATE",
            "SAME_ITEM_UID_PRESERVED",
            "ERSA_EXHIBITION_RESPONSIBILITY_PRESERVED",
            "NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED",
            "NO_AUTHENTICITY_TOTAL_SCORE",
            "NO_PROVENANCE_COMPLETENESS_SCORE",
            "NO_ARCHIVE_PRESTIGE_SCORE",
            "NO_HIGHEST_ARTISTRY_ALWAYS_BEST",
            "NO_OLDEST_ITEM_ALWAYS_BEST",
            "NO_MOST_CHRONICLE_EVENTS_ALWAYS_BEST",
            "NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST",
            "NO_DOCUMENT_FABRICATION",
            "NO_UNRECORDED_HISTORY_AUTOFILL",
            "NO_ACCESSION_COUNT_ARTISTRY_GROWTH",
            "NO_APPRAISAL_OR_REVIEW_COUNT_ARTISTRY_GROWTH",
            "NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_ARCHIVING",
            "NO_ARCHIVE_STORAGE_MANAGEMENT",
            "NO_MUSEUM_MANAGEMENT_SIM",
            "NO_VISITOR_MANAGEMENT",
            "NO_LOAN_LOGISTICS_MANAGEMENT",
            "ERSA_ROEN",
            "EXHIBITION_EVIDENCE_AND_PROVENANCE",
            "CEREMONIAL_NOBLE",
            "HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY",
            "P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED",
            "제품 구현: `BLOCKED`",
            "Task3 구현: `NOT_APPROVED`",
        ):
            self.assertIn(token, canon)

        for forbidden in (
            "AUTHENTICITY_TOTAL_SCORE: true",
            "PROVENANCE_COMPLETENESS_SCORE: true",
            "ARCHIVE_PRESTIGE_SCORE: true",
            "DOCUMENT_FABRICATION: true",
            "UNRECORDED_HISTORY_AUTOFILL: true",
            "MUSEUM_MANAGEMENT_SIM: true",
            "TASK3_IMPLEMENTATION_APPROVED",
        ):
            self.assertNotIn(forbidden, canon)

    def test_current_routers_move_to_eight_of_ten_without_opening_product_code(self) -> None:
        current = CURRENT.read_text(encoding="utf-8")
        active = ACTIVE.read_text(encoding="utf-8")
        start_here = START_HERE.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        gates = GATES.read_text(encoding="utf-8")

        for decision_id in (
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
            "BS-CONTENT-20260811-05",
            "BS-CONTENT-20260811-06",
            "BS-CONTENT-20260811-07",
            "BS-CONTENT-20260811-08",
        ):
            self.assertIn(decision_id, current)

        for text in (active, start_here, roadmap, gates):
            self.assertIn("R3_R7_DESIGN_ACTIVE", text)
            self.assertIn("R3_R7_APPROVAL_COUNTER: 8/10", text)
            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", text)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", text)
            self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", text)

        for text in (active, start_here, roadmap):
            self.assertIn("COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED", text)

        self.assertIn("현재 Decision은 `BS-CONTENT-20260811-08`", active)
        self.assertIn("현재 연속 작업은 `BS-CONTENT-20260811-08`", start_here)
        self.assertIn("현재 승인 카운터: `8/10`.", roadmap)
        self.assertIn("Decision: `BS-CONTENT-20260811-08`.", gates)

        d06_heading = "### 6/10 — `BS-CONTENT-20260811-06`"
        d07_heading = "### 7/10 — `BS-CONTENT-20260811-07`"
        d08_heading = "### 8/10 — `BS-CONTENT-20260811-08`"
        self.assertIn(d07_heading, roadmap)
        self.assertLess(roadmap.index(d06_heading), roadmap.index(d07_heading))
        self.assertLess(roadmap.index(d07_heading), roadmap.index(d08_heading))
        self.assertIn("SOLDIER_02 / LIANA_BERG", roadmap[roadmap.index(d07_heading):roadmap.index(d08_heading)])


if __name__ == "__main__":
    unittest.main()
