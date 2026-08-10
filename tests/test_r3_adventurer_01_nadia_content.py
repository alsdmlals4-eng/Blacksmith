from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


class Adventurer01NadiaContentContractTests(unittest.TestCase):
    def test_r3_registry_promotes_the_approved_first_content_decision(self) -> None:
        self.assertTrue(REGISTRY.is_file())
        registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
        self.assertEqual("R3_R7_DESIGN_ACTIVE", registry.get("stage_status"))
        self.assertEqual("BLOCKED", registry.get("product_implementation"))
        self.assertEqual("1/10", registry.get("next_approval_counter"))
        decisions = {item["id"]: item for item in registry.get("current_decisions", [])}
        self.assertIn("BS-CONTENT-20260811-01", decisions)
        contract = decisions.get("BS-CONTENT-20260811-01", {}).get("contract", {})
        self.assertEqual("ADVENTURER_01", contract.get("content_id"))
        self.assertEqual("NADIA_VENN", contract.get("customer_id"))
        self.assertEqual("SURVIVAL_AND_RECOVERY", contract.get("content_goal"))
        self.assertFalse(contract.get("direct_combat_or_exploration_minigame"))
        self.assertFalse(contract.get("single_always_best_equipment_answer"))
        self.assertEqual("ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE", contract.get("personal_schedule_progression"))
        self.assertEqual("BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED", contract.get("exact_values"))

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

    def test_stable_entrypoints_record_the_decision_without_opening_product_code(self) -> None:
        current = CURRENT.read_text(encoding="utf-8")
        active = ACTIVE.read_text(encoding="utf-8")
        self.assertIn("BS-CONTENT-20260811-01", current)
        self.assertIn("R3_R7_DESIGN_ACTIVE", active)
        self.assertIn("ADVENTURER_01_DETAIL_APPROVED", active)
        self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", active)
        self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", active)


if __name__ == "__main__":
    unittest.main()
