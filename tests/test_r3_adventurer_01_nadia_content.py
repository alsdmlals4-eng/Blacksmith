from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"


class Adventurer01NadiaContentContractTests(unittest.TestCase):
    def test_r3_registry_promotes_the_approved_first_content_decision(self) -> None:
        self.assertTrue(REGISTRY.is_file())
        registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
        self.assertEqual("R3_R7_DESIGN_ACTIVE", registry.get("stage_status"))
        self.assertEqual("BLOCKED", registry.get("product_implementation"))
        self.assertEqual("1/10", registry.get("next_approval_counter"))
        decisions = {item["id"]: item for item in registry.get("current_decisions", [])}
        self.assertIn("BS-CONTENT-20260811-01", decisions)
        decision = decisions.get("BS-CONTENT-20260811-01", {})
        self.assertEqual("USER_APPROVED_R3_R7_1_OF_10_MERGED_PR142_MAIN_CANON", decision.get("status"))
        contract = decision.get("contract", {})
        self.assertEqual("ADVENTURER_01", contract.get("content_id"))
        self.assertEqual("NADIA_VENN", contract.get("customer_id"))
        self.assertEqual("SURVIVAL_AND_RECOVERY", contract.get("content_goal"))
        self.assertFalse(contract.get("direct_combat_or_exploration_minigame"))
        self.assertFalse(contract.get("single_always_best_equipment_answer"))
        self.assertEqual("ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE", contract.get("personal_schedule_progression"))
        self.assertEqual("BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED", contract.get("exact_values"))
        self.assertEqual(
            ["DEFAULT_CUSTOMER_CARD", "POST_EQUIPMENT_DECISION_LAYER", "DETAIL_VIEW"],
            contract.get("customer_information_layers"),
        )
        self.assertEqual("LOAD_GATE_THEN_ENHANCEMENT_THEN_RELEVANT_UTILITY_THEN_SMALL_CUSTOMER_CONTEXT", contract.get("reason_priority"))
        self.assertEqual("THREE_STATE_SUMMARY_TWO_TO_FOUR_REASONS_ONE_PRIMARY_NEXT_ACTION", contract.get("result_information_hierarchy"))
        self.assertEqual("NON_CANONICAL_BASELINE_TEST_FIXTURE", contract.get("test_fixture_status"))
        self.assertEqual("OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL", contract.get("playtest_evidence"))

    def test_canon_keeps_blacksmith_core_and_delayed_item_lifecycle(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-01",
            "ADVENTURER_01",
            "NADIA_VENN",
            "나디아 벤",
            "생환 + 회수",
            "같은 UID",
            "직접 전투·탐험 미니게임을 추가하지 않는다",
            "ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE",
            "BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED",
            "Potion Craft",
            "Crusader Kings III",
            "Games User Research",
        ):
            self.assertIn(token, canon)

    def test_detail_contract_is_explainable_mobile_first_and_noncanonical_where_required(self) -> None:
        canon = CANON.read_text(encoding="utf-8")
        for token in (
            "MERGED_PR142_MAIN_CANON",
            "DEFAULT_CUSTOMER_CARD",
            "POST_EQUIPMENT_DECISION_LAYER",
            "DETAIL_VIEW",
            "작품 미선택 기본 예상 성공률",
            "LOAD_GATE_THEN_ENHANCEMENT_THEN_RELEVANT_UTILITY_THEN_SMALL_CUSTOMER_CONTEXT",
            "OVERWEIGHT이면 예상 성공률보다 배정 불가를 우선한다",
            "자동 추천·Best 배지 금지",
            "THREE_STATE_SUMMARY_TWO_TO_FOUR_REASONS_ONE_PRIMARY_NEXT_ACTION",
            "NON_CANONICAL_BASELINE_TEST_FIXTURE",
            "APPROVED_RELEVANT_UTILITY_PLACEHOLDER",
            "OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL",
            "어떤 작품을 맡겼나요?",
            "결정할 때 무엇을 봤나요?",
            "돌아온 작품은 이전 작품과 어떤 관계인가요?",
            "48dp",
        ):
            self.assertIn(token, canon)
        self.assertNotIn("AUTO_RECOMMENDED_BEST_ITEM: true", canon)
        self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", canon)

    def test_stable_entrypoints_record_the_decision_without_opening_product_code(self) -> None:
        current = CURRENT.read_text(encoding="utf-8")
        active = ACTIVE.read_text(encoding="utf-8")
        start_here = START_HERE.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        gates = GATES.read_text(encoding="utf-8")

        self.assertIn("BS-CONTENT-20260811-01", current)
        self.assertIn("MERGED_PR142_MAIN_CANON", current)
        self.assertNotIn("USER_APPROVED / R3_R7_1_OF_10 / PENDING_MERGE / PLANNING_ONLY", current)
        self.assertIn("R3_R7_DESIGN_ACTIVE", active)
        self.assertIn("ADVENTURER_01_DETAIL_APPROVED", active)
        self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", active)
        self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", active)

        for text in (start_here, roadmap, gates):
            self.assertIn("R3_R7_DESIGN_ACTIVE", text)
            self.assertIn("BS-CONTENT-20260811-01", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", text)
            self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", text)

        self.assertIn("MERGED_PR142_MAIN_CANON", roadmap)
        self.assertNotIn("R3_R7_1_OF_10_PENDING_MERGE", roadmap)
        self.assertNotIn("R3_R7_DESIGN_PAUSED", start_here)
        self.assertNotIn("ADVENTURER_01_DETAIL_PENDING", start_here)
        self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", gates)


if __name__ == "__main__":
    unittest.main()
