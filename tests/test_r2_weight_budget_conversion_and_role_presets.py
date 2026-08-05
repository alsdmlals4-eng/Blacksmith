from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-06-weight-budget-conversion-and-role-presets-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-06-weight-budget-conversion-and-role-presets.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
WEIGHT_BUDGET_CANON = ROOT / "docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md"
WEIGHT_CANON = ROOT / "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md"
LOAD_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md"
WEAPON_BASES = ROOT / "data/crafting/weapon_bases.json"


def read_or_empty(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class WeightBudgetConversionRolePresetContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}
        cls.contract = cls.decisions.get("BS-ITEM-20260806-03", {}).get("contract", {})

    def test_batch_005_contains_seven_approved_decisions(self) -> None:
        self.assertEqual("R2_BATCH_005_ACTIVE_7_OF_10", self.registry["stage_status"])
        self.assertEqual("7/10", self.registry["next_approval_counter"])
        active = self.registry["active_batch"]
        self.assertEqual(7, active["approved_decisions"])
        self.assertEqual("7/10", active["counter"])
        self.assertEqual(
            [
                "BS-CRAFT-20260805-02",
                "BS-CUSTOMER-20260805-01",
                "BS-UX-20260805-01",
                "BS-CUSTOMER-20260806-01",
                "BS-ITEM-20260806-01",
                "BS-ITEM-20260806-02",
                "BS-ITEM-20260806-03",
            ],
            active["decisions"],
        )

    def test_point_conversion_is_exact(self) -> None:
        self.assertIn("BS-ITEM-20260806-03", self.decisions)
        self.assertEqual(
            "ROLE_PRESET_AUTOMATIC_SINGLE_LANE",
            self.contract.get("performance_budget_conversion_model"),
        )
        self.assertEqual(
            {
                "ATTACK_BUDGET": {"output": "ATTACK", "per_budget_point": 5},
                "DEFENSE_BUDGET": {"output": "DEFENSE", "per_budget_point": 5},
                "MAGIC_FUNCTION_BUDGET": {
                    "output": "MAGIC_FUNCTION_CAPACITY",
                    "per_budget_point": 1,
                },
                "UTILITY_BUDGET": {
                    "output": "UTILITY_CAPACITY",
                    "per_budget_point": 1,
                },
            },
            self.contract.get("point_conversion"),
        )

    def test_role_presets_are_automatic_and_immutable(self) -> None:
        self.assertEqual(
            "FIRST_CRAFT_COMPLETION_FROM_BASE_ITEM_DEFINITION",
            self.contract.get("performance_profile_selection"),
        )
        self.assertTrue(self.contract.get("performance_profile_immutable_for_uid"))
        self.assertFalse(self.contract.get("player_free_allocation_ui", True))
        self.assertFalse(self.contract.get("post_craft_free_reallocation_allowed", True))
        self.assertTrue(self.contract.get("new_budget_uses_existing_profile"))
        self.assertFalse(self.contract.get("hybrid_profile_baseline_allowed", True))
        self.assertTrue(self.contract.get("explicit_profile_override_requires_approved_item_design"))

    def test_default_equipment_profiles_and_examples_are_exact(self) -> None:
        self.assertEqual(
            {
                "SWORD": "PHYSICAL_WEAPON",
                "AXE": "PHYSICAL_WEAPON",
                "BLUNT": "PHYSICAL_WEAPON",
                "POLEARM": "PHYSICAL_WEAPON",
                "RANGED": "PHYSICAL_WEAPON",
                "LIGHT_ARMOR": "PROTECTIVE_GEAR",
                "MEDIUM_ARMOR": "PROTECTIVE_GEAR",
                "HEAVY_ARMOR": "PROTECTIVE_GEAR",
                "SHIELD_SUPPORT": "PROTECTIVE_GEAR",
                "TOOL": "UTILITY_IMPLEMENT",
                "CLOTHING_OR_ROBE": "UTILITY_GARMENT",
                "ACCESSORY": "NONE",
            },
            self.contract.get("default_profile_by_equipment_group"),
        )
        self.assertEqual(
            {
                "SWORD": {"weight": 10, "budget": 2, "output": "ATTACK +10"},
                "AXE": {"weight": 15, "budget": 3, "output": "ATTACK +15"},
                "BLUNT": {"weight": 15, "budget": 3, "output": "ATTACK +15"},
                "POLEARM": {"weight": 20, "budget": 4, "output": "ATTACK +20"},
                "RANGED": {"weight": 10, "budget": 2, "output": "ATTACK +10"},
                "LIGHT_ARMOR": {"weight": 10, "budget": 2, "output": "DEFENSE +10"},
                "MEDIUM_ARMOR": {"weight": 20, "budget": 4, "output": "DEFENSE +20"},
                "HEAVY_ARMOR": {"weight": 30, "budget": 6, "output": "DEFENSE +30"},
                "SHIELD_SUPPORT": {"weight": 10, "budget": 2, "output": "DEFENSE +10"},
                "TOOL": {"weight": 5, "budget": 1, "output": "UTILITY_CAPACITY +1"},
                "CLOTHING_OR_ROBE": {
                    "weight": 5,
                    "budget": 1,
                    "output": "UTILITY_CAPACITY +1",
                },
                "ACCESSORY": {"weight": 0, "budget": 0, "output": "NONE"},
            },
            self.contract.get("baseline_examples"),
        )

    def test_magic_and_utility_capacity_costs_are_integer_and_guarded(self) -> None:
        self.assertEqual(
            {
                "STANDARD_APPROVED_FUNCTION": 1,
                "STRONG_OR_MULTI_CONTEXT_FUNCTION": 2,
                "TRANSFORMATIVE_OR_RULE_BYPASS_FUNCTION": 3,
            },
            self.contract.get("function_capacity_costs"),
        )
        self.assertTrue(self.contract.get("function_capacity_costs_are_positive_integers"))
        self.assertTrue(self.contract.get("transformative_function_requires_separate_design_approval"))
        self.assertEqual(
            "MAGIC_IMPLEMENT",
            self.contract.get("approved_magic_item_profile"),
        )
        self.assertEqual(
            "EXPLICIT_BASE_ITEM_DESIGN_ONLY",
            self.contract.get("magic_profile_override_scope"),
        )

    def test_weighting_follows_profile_and_lightweighting_preserves_output(self) -> None:
        self.assertTrue(self.contract.get("weighting_new_point_follows_existing_profile"))
        self.assertEqual(1, self.contract.get("weighting_budget_points_per_new_peak_five_weight"))
        self.assertTrue(self.contract.get("lightweighting_preserves_allocated_output"))
        self.assertEqual(
            {
                "PHYSICAL_WEAPON": "WEIGHT +5 / ATTACK +5",
                "PROTECTIVE_GEAR": "WEIGHT +5 / DEFENSE +5",
                "MAGIC_IMPLEMENT": "WEIGHT +5 / MAGIC_FUNCTION_CAPACITY +1",
                "UTILITY_IMPLEMENT": "WEIGHT +5 / UTILITY_CAPACITY +1",
                "UTILITY_GARMENT": "WEIGHT +5 / UTILITY_CAPACITY +1",
            },
            self.contract.get("weighting_preview_by_profile"),
        )

    def test_conversion_does_not_double_count_or_change_generic_success(self) -> None:
        self.assertFalse(self.contract.get("budget_output_added_to_generic_event_success", True))
        self.assertFalse(self.contract.get("base_progress_repurposed_as_attack", True))
        self.assertFalse(self.contract.get("base_value_repurposed_as_attack_or_defense", True))
        self.assertFalse(self.contract.get("same_weight_source_counted_twice", True))
        self.assertEqual("BLOCKED", self.contract.get("product_implementation"))
        weapon_bases = read_or_empty(WEAPON_BASES)
        self.assertNotIn('"attack"', weapon_bases)
        self.assertNotIn('"defense"', weapon_bases)
        self.assertNotIn('"performance_profile"', weapon_bases)

    def test_authority_documents_and_refinements_exist(self) -> None:
        for path in (CANON, SPEC, PLAN):
            self.assertTrue(path.exists(), f"missing authority document: {path}")
        canon = read_or_empty(CANON)
        for token in (
            "BS-ITEM-20260806-03",
            "R2_BATCH_005_7_OF_10",
            "1 ATTACK_BUDGET = ATTACK +5",
            "1 DEFENSE_BUDGET = DEFENSE +5",
            "1 MAGIC_FUNCTION_BUDGET = MAGIC_FUNCTION_CAPACITY +1",
            "1 UTILITY_BUDGET = UTILITY_CAPACITY +1",
            "ROLE_PRESET_AUTOMATIC_SINGLE_LANE",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)
        self.assertIn("BS-ITEM-20260806-03", read_or_empty(CURRENT))
        self.assertIn("R2_BATCH_005 / 7/10", read_or_empty(CURRENT))
        self.assertIn("중량 예산 환산", read_or_empty(BIBLE))
        for path in (WEIGHT_BUDGET_CANON, WEIGHT_CANON, LOAD_CANON):
            text = read_or_empty(path)
            self.assertIn("REFINED_BY_BS-ITEM-20260806-03", text)
            self.assertIn("R2_BATCH_005_7_OF_10", text)


if __name__ == "__main__":
    unittest.main()
