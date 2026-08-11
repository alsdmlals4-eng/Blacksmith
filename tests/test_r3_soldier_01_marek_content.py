from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"


class Soldier01MarekContentContractTests(unittest.TestCase):
    def test_r3_registry_preserves_marek_as_approved_third_content_decision(self) -> None:
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
        ):
            self.assertIn(decision_id, decisions)

        decision = decisions.get("BS-CONTENT-20260811-03", {})
        self.assertIn("USER_APPROVED_R3_R7_3_OF_10", decision.get("status", ""))
        contract = decision.get("contract", {})
        self.assertEqual("SOLDIER_01", contract.get("content_id"))
        self.assertEqual("MAREK_OLDEN", contract.get("customer_id"))
        self.assertEqual("SMALL_LOT_STANDARD_ORDER", contract.get("activity_family"))
        self.assertEqual("UNIT_READINESS_AND_STANDARD_FIT", contract.get("content_goal"))
        self.assertEqual("BLACKSMITH_SMALL_LOT_EQUIPMENT_DECISION_MAKER_NOT_LOGISTICS_OR_COMBAT_CONTROLLER", contract.get("player_role"))
        self.assertEqual(10, contract.get("baseline_order_quantity"))
        self.assertEqual("NON_CANONICAL_BASELINE_TEST_FIXTURE", contract.get("order_quantity_status"))
        self.assertTrue(contract.get("per_item_uid_preserved"))
        self.assertTrue(contract.get("per_item_cost_and_result_preserved"))
        self.assertFalse(contract.get("free_item_cloning"))
        self.assertFalse(contract.get("worker_or_production_line_system"))
        self.assertFalse(contract.get("direct_tactical_combat"))
        self.assertFalse(contract.get("realtime_logistics_control"))
        self.assertFalse(contract.get("opaque_standardization_score"))
        self.assertEqual(
            ["UNIT_MISSION_STATE", "STANDARD_ADOPTION_STATE", "BATCH_ITEM_LIFECYCLE_STATE"],
            contract.get("result_axes"),
        )

    def test_marek_canon_preserves_authored_items_inside_small_lot(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-03",
            "SOLDIER_01",
            "MAREK_OLDEN",
            "마레크 올덴",
            "SMALL_LOT_STANDARD_ORDER",
            "UNIT_READINESS_AND_STANDARD_FIT",
            "REFERENCE_ITEM_UID",
            "ORDER_QUANTITY = 10",
            "NON_CANONICAL_BASELINE_TEST_PRESET",
            "PER_ITEM_UID_PRESERVED",
            "PER_ITEM_COST_AND_RESULT_PRESERVED",
            "UNIT_MISSION_STATE",
            "STANDARD_ADOPTION_STATE",
            "BATCH_ITEM_LIFECYCLE_STATE",
            "직접 전술 전투",
            "실시간 병참",
            "제품 구현: `BLOCKED`",
            "Task3 구현: `NOT_APPROVED`",
        ):
            self.assertIn(token, canon)

        for forbidden in (
            "STANDARDIZATION_SCORE: true",
            "FREE_ITEM_CLONING: true",
            "WORKER_PRODUCTION_LINE: true",
            "DIRECT_TACTICAL_COMBAT: true",
            "REALTIME_LOGISTICS_CONTROL: true",
            "TASK3_IMPLEMENTATION_APPROVED",
        ):
            self.assertNotIn(forbidden, canon)

    def test_current_routers_preserve_marek_history_while_liana_is_current(self) -> None:
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
            self.assertIn("R3_R7_APPROVAL_COUNTER: 8/10", text)
            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08", text)
            self.assertIn("BS-CONTENT-20260811-03", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", text)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", text)
            self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", text)

        for text in (active, start_here, roadmap):
            self.assertIn("COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED", text)

        self.assertIn("Marek", active)
        self.assertIn("BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md", start_here)
        self.assertIn("### 3/10 — `BS-CONTENT-20260811-03`", roadmap)
        self.assertIn("BS-CONTENT-20260811-03", gates)

    def test_marek_does_not_turn_auto_enhancement_into_content_owned_power(self) -> None:
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        self.assertIn("자동 강화 상한은 별도 시스템 Decision이 소유한다", canon)
        self.assertIn("Marek 콘텐츠 자체는 자동 강화 상한을 해금하거나 상승시키지 않는다", canon)
        self.assertNotIn("MAREK_AUTO_ENHANCEMENT_BONUS", canon)


if __name__ == "__main__":
    unittest.main()
