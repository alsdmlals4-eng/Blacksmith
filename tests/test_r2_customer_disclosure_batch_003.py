from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
FIVE_GRADE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md"
ARTISTRY_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md"
FOUR_GRADE_HISTORY = ROOT / "docs/planning/BLACKSMITH_R2_FOUR_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md"
AGENTS = ROOT / "AGENTS.md"


class R2Checkpoint003AndBatch004Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_checkpoint_003_is_closed_and_batch_004_is_two_of_ten(self) -> None:
        closed = self.registry["closed_batch"]
        self.assertEqual("R2_BATCH_003", closed["id"])
        self.assertEqual(10, closed["approved_decisions"])
        self.assertEqual("10/10", closed["counter"])

        active = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_004", active["id"])
        self.assertEqual(2, active["approved_decisions"])
        self.assertEqual("2/10", active["counter"])
        self.assertEqual(10, active["maximum_size"])
        self.assertEqual(
            ["BS-CRAFT-20260804-07", "BS-CRAFT-20260805-01"],
            active["decisions"],
        )
        self.assertEqual(
            ["HIGH_RISK_CONFLICT", "SESSION_END", "LARGE_CANON_IMPACT"],
            active["early_checkpoint_triggers"],
        )

    def test_three_affix_slots_remain_independent(self) -> None:
        contract = self.decisions["BS-CRAFT-20260804-06"]["contract"]
        self.assertEqual(3, contract["affix_slot_count"])
        self.assertEqual(
            ["GRADE_AFFIX", "CATALYST_AFFIX", "CHRONICLE_AFFIX"],
            contract["affix_slots"],
        )
        self.assertFalse(contract["cross_slot_overwrite_allowed"])
        self.assertEqual("THREE_SEPARATE_UID_FIELDS", contract["storage"])

    def test_five_tier_birth_grade_contract(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-07"]
        contract = decision["contract"]
        self.assertEqual("USER_APPROVED_R2_BATCH_004_1_OF_10_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual(5, contract["grade_count"])
        self.assertEqual(
            [
                "CRAFT_NORMAL",
                "CRAFT_SUPERIOR",
                "CRAFT_FINE",
                "CRAFT_MASTERWORK",
                "CRAFT_LEGENDARY",
            ],
            contract["grade_ids"],
        )
        self.assertEqual(["보통", "우수", "명품", "걸작", "전설"], contract["korean_labels"])
        self.assertTrue(contract["immutable_for_same_item_uid"])
        self.assertFalse(contract["post_craft_promotion_allowed"])
        self.assertFalse(contract["post_craft_demotion_allowed"])
        self.assertEqual("EXTREMELY_RARE_FIRST_CRAFT_RESULT", contract["legendary_origin"])
        for key in (
            "legendary_guarantees_max_artistry",
            "legendary_guarantees_catalyst_affix",
            "legendary_guarantees_chronicle_affix",
            "legendary_guarantees_universal_best_performance",
        ):
            self.assertFalse(contract[key])

        canon = FIVE_GRADE_CANON.read_text(encoding="utf-8")
        self.assertIn("[보통] → [우수] → [명품] → [걸작] → [전설]", canon)
        self.assertIn("제작 후 등급 승격 금지", canon)

    def test_numeric_artistry_has_no_named_tiers(self) -> None:
        decision = self.decisions["BS-CRAFT-20260805-01"]
        contract = decision["contract"]
        self.assertEqual("USER_APPROVED_R2_BATCH_004_2_OF_10_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("WEAPON_ITEM_STAT", contract["stat_role"])
        self.assertEqual("INTEGER_1_TO_10", contract["scale"])
        self.assertFalse(contract["named_tiers_exist"])
        self.assertTrue(contract["displayed_with_weapon_stats"])
        self.assertFalse(contract["combat_power_by_default"])
        self.assertFalse(contract["universal_affix_multiplier"])

        canon = ARTISTRY_CANON.read_text(encoding="utf-8")
        self.assertIn("예술성 7/10", canon)
        self.assertIn("단계명 없음", canon)

    def test_superseded_four_tier_file_is_visibly_historical(self) -> None:
        text = FOUR_GRADE_HISTORY.read_text(encoding="utf-8")
        self.assertIn("[대체됨]", text)
        self.assertIn("BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md", text)

    def test_tdd_and_checkpoint_governance(self) -> None:
        contract = self.decisions["BS-OPS-20260805-01"]["contract"]
        self.assertTrue(contract["benchmarking_before_questions_and_recommendations"])
        self.assertTrue(contract["industry_comparison_required"])
        self.assertEqual(10, contract["maximum_approved_decisions_per_batch"])
        self.assertTrue(contract["tdd_required_for_every_change"])
        self.assertEqual(["RED", "GREEN", "REFACTOR"], contract["tdd_cycle"])

        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("벤치마킹·현업 비교", agents)
        self.assertIn("조기 체크포인트", agents)
        self.assertIn("작업마다 TDD", agents)

    def test_product_implementation_remains_blocked(self) -> None:
        self.assertEqual("BLOCKED", self.registry["product_implementation"])
        self.assertEqual("NOT_STARTED_BLOCKED", self.registry["implementation_alignment"]["five_grade_product_implementation"])
        self.assertEqual("NOT_STARTED_BLOCKED", self.registry["implementation_alignment"]["artistry_product_implementation"])


if __name__ == "__main__":
    unittest.main()
