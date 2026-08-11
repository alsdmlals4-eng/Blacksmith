from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"


class Collector01ErsaContentContractTests(unittest.TestCase):
    def test_r3_registry_preserves_ersa_as_approved_fourth_content_decision(self) -> None:
        self.assertTrue(REGISTRY.is_file())
        registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
        self.assertEqual("R3_R7_DESIGN_ACTIVE", registry.get("stage_status"))
        self.assertEqual("BLOCKED", registry.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", registry.get("task3_implementation"))
        self.assertEqual("9/10", registry.get("next_approval_counter"))

        decisions = {item["id"]: item for item in registry.get("current_decisions", [])}
        for decision_id in (
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
            "BS-CONTENT-20260811-05",
            "BS-CONTENT-20260811-06",
            "BS-CONTENT-20260811-07",
        ):
            self.assertIn(decision_id, decisions)

        decision = decisions.get("BS-CONTENT-20260811-04", {})
        self.assertIn("USER_APPROVED_R3_R7_4_OF_10", decision.get("status", ""))
        contract = decision.get("contract", {})
        self.assertEqual("COLLECTOR_01", contract.get("content_id"))
        self.assertEqual("ERSA_ROEN", contract.get("customer_id"))
        self.assertEqual("COLLECTOR", contract.get("customer_archetype"))
        self.assertEqual("EXHIBITION_EVIDENCE_AND_PROVENANCE", contract.get("activity_family"))
        self.assertEqual("PUBLIC_MEANING_THROUGH_CRAFT_AND_LIFECYCLE_EVIDENCE", contract.get("content_goal"))
        self.assertEqual(
            "BLACKSMITH_ITEM_AND_EVIDENCE_DECISION_MAKER_NOT_CURATOR_CONTROLLER",
            contract.get("player_role"),
        )
        self.assertEqual(
            ["CRAFTSMANSHIP_EVIDENCE", "LIVED_HISTORY_EVIDENCE"],
            contract.get("exhibition_intent_families"),
        )
        self.assertFalse(contract.get("opaque_collector_or_exhibition_score"))
        self.assertFalse(contract.get("chronicle_count_optimization"))
        self.assertFalse(contract.get("oldest_item_always_best"))
        self.assertFalse(contract.get("highest_artistry_always_best"))
        self.assertFalse(contract.get("highest_enhancement_always_best"))
        self.assertFalse(contract.get("exhibition_count_artistry_growth"))
        self.assertFalse(contract.get("automatic_chronicle_affix_from_display"))
        self.assertTrue(contract.get("same_item_uid_preserved"))
        self.assertFalse(contract.get("direct_exhibition_minigame"))
        self.assertFalse(contract.get("gallery_or_visitor_management"))
        self.assertEqual(
            ["EXHIBITION_RECEPTION_STATE", "EXHIBIT_THESIS_FIT_STATE", "ITEM_UID_PUBLIC_LEGACY_STATE"],
            contract.get("result_axes"),
        )
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", contract.get("task3_implementation"))

    def test_ersa_canon_uses_existing_uid_evidence_without_new_prestige_score(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-04",
            "COLLECTOR_01",
            "ERSA_ROEN",
            "에르사 로엔",
            "EXHIBITION_EVIDENCE_AND_PROVENANCE",
            "CRAFTSMANSHIP_EVIDENCE",
            "LIVED_HISTORY_EVIDENCE",
            "EXHIBITION_RECEPTION_STATE",
            "EXHIBIT_THESIS_FIT_STATE",
            "ITEM_UID_PUBLIC_LEGACY_STATE",
            "SAME_ITEM_UID_PRESERVED",
            "NO_CHRONICLE_COUNT_OPTIMIZATION",
            "NO_EXHIBITION_COUNT_ARTISTRY_GROWTH",
            "NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_DISPLAY",
            "제품 구현: `BLOCKED`",
            "Task3 구현: `NOT_APPROVED`",
        ):
            self.assertIn(token, canon)

        for forbidden in (
            "RARITY_SCORE: true",
            "PRESTIGE_SCORE: true",
            "COLLECTOR_SCORE: true",
            "EXHIBITION_SCORE: true",
            "CHRONICLE_COUNT_OPTIMIZATION: true",
            "EXHIBITION_COUNT_ARTISTRY_GROWTH: true",
            "AUTOMATIC_CHRONICLE_AFFIX_FROM_DISPLAY: true",
            "DIRECT_EXHIBITION_MINIGAME: true",
            "TASK3_IMPLEMENTATION_APPROVED",
        ):
            self.assertNotIn(forbidden, canon)

    def test_current_routers_preserve_ersa_history_while_sedric_is_current(self) -> None:
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
        ):
            self.assertIn(decision_id, current)

        for text in (active, start_here, roadmap, gates):
            self.assertIn("R3_R7_DESIGN_ACTIVE", text)
            self.assertIn("R3_R7_APPROVAL_COUNTER: 9/10", text)
            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", text)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", text)
            self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", text)

        for text in (active, start_here, roadmap):
            self.assertIn("GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED", text)

        self.assertIn("현재 Decision은 `BS-CONTENT-20260811-09`", active)
        self.assertIn("현재 연속 작업은 `BS-CONTENT-20260811-09`", start_here)
        self.assertIn("현재 승인 카운터: `9/10`.", roadmap)
        self.assertIn("Decision: `BS-CONTENT-20260811-09`.", gates)

    def test_exhibition_does_not_become_free_artistry_or_chronicle_progression(self) -> None:
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        self.assertIn("전시 횟수만으로 `ARTISTRY`가 증가하지 않는다", canon)
        self.assertIn("전시했다는 사실만으로 `CHRONICLE_AFFIX`를 자동 부여하지 않는다", canon)
        self.assertIn("같은 작품 UID", canon)
        self.assertNotIn("EXHIBITION_FARMING_BONUS", canon)


if __name__ == "__main__":
    unittest.main()
