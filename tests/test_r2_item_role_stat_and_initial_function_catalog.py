from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-06-item-role-stat-and-function-catalog-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-06-item-role-stat-and-function-catalog.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
WEIGHT_CONVERSION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md"
CUSTOMER_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md"
PRECISION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md"
MOBILE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md"
WEAPON_BASES = ROOT / "data/crafting/weapon_bases.json"


def read_or_empty(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class ItemRoleStatInitialFunctionCatalogContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}
        cls.contract = cls.decisions.get("BS-ITEM-20260806-04", {}).get("contract", {})

    def test_batch_005_contains_eight_approved_decisions(self) -> None:
        self.assertEqual("R2_BATCH_005_ACTIVE_8_OF_10", self.registry["stage_status"])
        self.assertEqual("8/10", self.registry["next_approval_counter"])
        active = self.registry["active_batch"]
        self.assertEqual(8, active["approved_decisions"])
        self.assertEqual("8/10", active["counter"])
        self.assertEqual(
            [
                "BS-CRAFT-20260805-02",
                "BS-CUSTOMER-20260805-01",
                "BS-UX-20260805-01",
                "BS-CUSTOMER-20260806-01",
                "BS-ITEM-20260806-01",
                "BS-ITEM-20260806-02",
                "BS-ITEM-20260806-03",
                "BS-ITEM-20260806-04",
            ],
            active["decisions"],
        )

    def test_single_primary_role_stat_model_is_exact(self) -> None:
        self.assertIn("BS-ITEM-20260806-04", self.decisions)
        self.assertEqual(
            "SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS",
            self.contract.get("item_role_stat_model"),
        )
        self.assertEqual(
            {
                "SWORD": "ATTACK",
                "AXE": "ATTACK",
                "BLUNT": "ATTACK",
                "POLEARM": "ATTACK",
                "RANGED": "ATTACK",
                "SHIELD_SUPPORT": "DEFENSE",
                "LIGHT_ARMOR": "DEFENSE",
                "MEDIUM_ARMOR": "DEFENSE",
                "HEAVY_ARMOR": "DEFENSE",
                "TOOL": None,
                "CLOTHING_OR_ROBE": None,
                "ACCESSORY": None,
            },
            self.contract.get("primary_role_stat_by_equipment_group"),
        )
        self.assertTrue(self.contract.get("non_applicable_stats_are_omitted"))

    def test_attack_and_defense_source_formulas_are_exact(self) -> None:
        self.assertEqual(
            ["CRAFTED_ATTACK", "WEIGHT_ATTACK_OUTPUT", "APPROVED_ENHANCEMENT_ATTACK_OUTPUT"],
            self.contract.get("display_attack_sources"),
        )
        self.assertEqual(
            ["CRAFTED_DEFENSE", "WEIGHT_DEFENSE_OUTPUT", "APPROVED_ENHANCEMENT_DEFENSE_OUTPUT"],
            self.contract.get("display_defense_sources"),
        )
        self.assertEqual(
            "FIRST_CRAFT_COMPLETION_SINGLE_STORED_RESULT_WITH_SOURCE_LEDGER",
            self.contract.get("crafted_role_stat_determination"),
        )
        self.assertEqual(
            ["BASE_ITEM_DESIGN", "PRIMARY_MATERIAL", "DIRECT_FORGING_RESULT"],
            self.contract.get("crafted_role_stat_sources"),
        )
        self.assertFalse(self.contract.get("crafting_grade_auto_modifies_attack_or_defense", True))
        self.assertFalse(self.contract.get("artistry_auto_modifies_attack_or_defense", True))
        self.assertFalse(self.contract.get("same_source_double_count_allowed", True))

    def test_default_secondary_combat_stats_are_not_added(self) -> None:
        self.assertEqual([], self.contract.get("default_secondary_combat_stats"))
        self.assertEqual(
            [
                "CRITICAL_CHANCE",
                "CRITICAL_DAMAGE",
                "PENETRATION",
                "ACCURACY",
                "ATTACK_SPEED",
                "EVASION",
                "BLOCK_RATE",
                "ELEMENTAL_DAMAGE",
            ],
            self.contract.get("secondary_stats_require_separate_approved_owner"),
        )

    def test_initial_magic_function_catalog_is_exact(self) -> None:
        self.assertEqual(
            {
                "ARCANE_CONDUCTION": {
                    "capacity_cost": 1,
                    "output_tag": "CAN_CHANNEL_MAGIC_THROUGH_ITEM",
                    "bound_context_required": False,
                },
                "ELEMENTAL_WARD": {
                    "capacity_cost": 1,
                    "output_tag": "MITIGATES_ONE_BOUND_ELEMENTAL_HAZARD",
                    "bound_context_required": True,
                },
                "ARCANE_SENSING": {
                    "capacity_cost": 2,
                    "output_tag": "CAN_DETECT_MATCHING_ARCANE_TRACE",
                    "bound_context_required": True,
                },
            },
            self.contract.get("initial_magic_function_catalog"),
        )

    def test_initial_utility_function_catalog_is_exact(self) -> None:
        self.assertEqual(
            {
                "ENVIRONMENTAL_SEALING": {
                    "capacity_cost": 1,
                    "output_tag": "RESISTS_ONE_BOUND_ENVIRONMENT",
                    "bound_context_required": True,
                },
                "FIELD_SERVICEABILITY": {
                    "capacity_cost": 1,
                    "output_tag": "CAN_PERFORM_FIELD_MAINTENANCE",
                    "bound_context_required": False,
                },
                "TASK_INTEGRATION": {
                    "capacity_cost": 1,
                    "output_tag": "SUPPORTS_ONE_BOUND_TASK",
                    "bound_context_required": True,
                },
            },
            self.contract.get("initial_utility_function_catalog"),
        )

    def test_function_capacity_and_abuse_guards_are_exact(self) -> None:
        self.assertEqual(
            "FUNCTION_ID_PLUS_CAPACITY_COST_PLUS_OPTIONAL_BOUND_CONTEXT",
            self.contract.get("special_function_instance_model"),
        )
        self.assertTrue(self.contract.get("capacity_is_total_cost_limit"))
        self.assertFalse(self.contract.get("duplicate_function_id_stack_allowed", True))
        self.assertFalse(self.contract.get("remaining_capacity_auto_generates_function", True))
        self.assertFalse(self.contract.get("weight_gain_auto_grants_function", True))
        self.assertFalse(self.contract.get("function_tags_added_to_generic_event_success", True))
        self.assertEqual(
            ["ELIGIBILITY", "RISK_MITIGATION", "SPECIFIC_INTERACTION"],
            self.contract.get("function_effect_modes"),
        )
        self.assertEqual(3, self.contract.get("transformative_function_capacity_cost"))
        self.assertTrue(self.contract.get("transformative_function_requires_separate_design_approval"))
        self.assertEqual("BLOCKED", self.contract.get("product_implementation"))

    def test_authority_documents_and_refinements_exist(self) -> None:
        for path in (CANON, SPEC, PLAN):
            self.assertTrue(path.exists(), f"missing authority document: {path}")
        canon = read_or_empty(CANON)
        for token in (
            "BS-ITEM-20260806-04",
            "R2_BATCH_005_8_OF_10",
            "SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS",
            "DISPLAY_ATTACK",
            "DISPLAY_DEFENSE",
            "ARCANE_CONDUCTION",
            "ELEMENTAL_WARD",
            "ARCANE_SENSING",
            "ENVIRONMENTAL_SEALING",
            "FIELD_SERVICEABILITY",
            "TASK_INTEGRATION",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)
        self.assertIn("BS-ITEM-20260806-04", read_or_empty(CURRENT))
        self.assertIn("R2_BATCH_005 / 8/10", read_or_empty(CURRENT))
        self.assertIn("작품 역할 원수치", read_or_empty(BIBLE))
        for path in (WEIGHT_CONVERSION_CANON, CUSTOMER_CANON, PRECISION_CANON, MOBILE_CANON):
            text = read_or_empty(path)
            self.assertIn("REFINED_BY_BS-ITEM-20260806-04", text)
            self.assertIn("R2_BATCH_005_8_OF_10", text)
        weapon_bases = read_or_empty(WEAPON_BASES)
        self.assertNotIn('"attack"', weapon_bases)
        self.assertNotIn('"defense"', weapon_bases)
        self.assertNotIn('"special_functions"', weapon_bases)


if __name__ == "__main__":
    unittest.main()
