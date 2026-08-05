from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
FIVE_GRADE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md"
ARTISTRY_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md"
AGENTS = ROOT / "AGENTS.md"


class R2Checkpoint004ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_checkpoint_004_is_closed_and_batch_005_starts_empty(self) -> None:
        closed = self.registry["closed_batch"]
        self.assertEqual("R2_BATCH_004", closed["id"])
        self.assertEqual(2, closed["approved_decisions"])
        self.assertEqual("2/10", closed["counter"])
        self.assertEqual(
            ["BS-CRAFT-20260804-07", "BS-CRAFT-20260805-01"],
            closed["decisions"],
        )
        self.assertEqual("USER_APPROVED_EARLY_CHECKPOINT", closed["closure_reason"])

        active = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_005", active["id"])
        self.assertEqual(0, active["approved_decisions"])
        self.assertEqual("0/10", active["counter"])
        self.assertEqual([], active["decisions"])
        self.assertEqual(10, active["maximum_size"])

    def test_three_affix_slots_remain_independent(self) -> None:
        contract = self.decisions["BS-CRAFT-20260804-06"]["contract"]
        self.assertEqual(3, contract["affix_slot_count"])
        self.assertEqual(
            ["GRADE_AFFIX", "CATALYST_AFFIX", "CHRONICLE_AFFIX"],
            contract["affix_slots"],
        )
        self.assertFalse(contract["cross_slot_overwrite_allowed"])
        self.assertEqual("THREE_SEPARATE_UID_FIELDS", contract["storage"])

    def test_five_tier_birth_grade_is_merged(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-07"]
        self.assertEqual("USER_APPROVED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON", decision["status"])
        contract = decision["contract"]
        self.assertEqual(5, contract["grade_count"])
        self.assertEqual(
            ["CRAFT_NORMAL", "CRAFT_SUPERIOR", "CRAFT_FINE", "CRAFT_MASTERWORK", "CRAFT_LEGENDARY"],
            contract["grade_ids"],
        )
        self.assertEqual(["보통", "우수", "명품", "걸작", "전설"], contract["korean_labels"])
        self.assertTrue(contract["immutable_for_same_item_uid"])
        self.assertFalse(contract["post_craft_promotion_allowed"])
        self.assertFalse(contract["post_craft_demotion_allowed"])
        for key in (
            "legendary_guarantees_max_artistry",
            "legendary_guarantees_catalyst_affix",
            "legendary_guarantees_chronicle_affix",
            "legendary_guarantees_universal_best_performance",
        ):
            self.assertFalse(contract[key])
        canon = FIVE_GRADE_CANON.read_text(encoding="utf-8")
        self.assertIn("MERGED_PR106", canon)
        self.assertIn("제작 후 등급 승격 금지", canon)

    def test_artistry_is_unbounded_raw_value_and_merged(self) -> None:
        decision = self.decisions["BS-CRAFT-20260805-01"]
        self.assertEqual(
            "USER_APPROVED_REFINED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON",
            decision["status"],
        )
        contract = decision["contract"]
        self.assertEqual("NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM", contract["domain"])
        self.assertEqual(0, contract["minimum"])
        self.assertIsNone(contract["fixed_design_maximum"])
        for key in (
            "decimals_allowed",
            "denominator_display_allowed",
            "named_tiers_exist",
            "technical_storage_limit_is_content_maximum",
            "grade_sets_fixed_artistry_maximum",
            "zero_means_incomplete_or_unusable",
            "combat_power_by_default",
            "universal_affix_multiplier",
        ):
            self.assertFalse(contract[key])
        canon = ARTISTRY_CANON.read_text(encoding="utf-8")
        self.assertIn("MERGED_PR106", canon)
        self.assertIn("예술성 27", canon)
        self.assertNotIn("예술성 7/10", canon)
        self.assertNotIn("예술성 1~10", canon)

    def test_tdd_and_product_boundary(self) -> None:
        contract = self.decisions["BS-OPS-20260805-01"]["contract"]
        self.assertEqual(10, contract["maximum_approved_decisions_per_batch"])
        self.assertEqual(["RED", "GREEN", "REFACTOR"], contract["tdd_cycle"])
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertIn("벤치마킹·현업 비교", agents)
        self.assertIn("조기 체크포인트", agents)
        self.assertIn("작업마다 TDD", agents)
        self.assertEqual("BLOCKED", self.registry["product_implementation"])
        self.assertEqual("NOT_STARTED_BLOCKED", self.registry["implementation_alignment"]["five_grade_product_implementation"])
        self.assertEqual("NOT_STARTED_BLOCKED", self.registry["implementation_alignment"]["artistry_product_implementation"])


if __name__ == "__main__":
    unittest.main()
