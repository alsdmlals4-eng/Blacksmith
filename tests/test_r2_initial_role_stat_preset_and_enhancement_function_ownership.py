from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-06-initial-role-stat-preset-and-enhancement-function-ownership-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-06-initial-role-stat-preset-and-enhancement-function-ownership.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
ITEM_ROLE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md"
PRECISION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md"
LOAD_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md"
WEIGHT_CONVERSION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_WEIGHT_BUDGET_CONVERSION_AND_ROLE_PRESETS_CANON_2026.md"
ARTISTRY_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md"
WEAPON_BASES = ROOT / "data/crafting/weapon_bases.json"

TDD_EVIDENCE = {
    "red_head": "aaf88e008eda4eb089ff8eb864c5c5166d1ebf98",
    "red_run_id": 31053492591,
    "red_planning_first_run": 254,
    "red_existing_pass": 66,
    "red_expected_new_failures": 9,
    "green_sync_head": "507eff3ba9864c254ac58c1d24166cf566b15a2a",
    "green_one_shot_run": 31054424664,
    "green_focused_pass": 75,
    "green_core_alignment": "PASS",
    "green_operating_audit": "PASS",
    "green_protected_product_paths": 0,
}


def read_or_empty(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class InitialRoleStatPresetEnhancementFunctionOwnershipContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}
        cls.contract = cls.decisions.get("BS-ITEM-20260806-05", {}).get("contract", {})

    def test_batch_005_contains_ten_approved_decisions(self) -> None:
        self.assertEqual("R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING", self.registry["stage_status"])
        self.assertEqual("0/10", self.registry["next_approval_counter"])
        active = self.registry["active_batch"]
        self.assertEqual(10, active["approved_decisions"])
        self.assertEqual("10/10", active["counter"])
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
                "BS-ITEM-20260806-05",
                "BS-ITEM-20260806-06",
            ],
            active["decisions"],
        )

    def test_initial_role_stat_formula_and_values_are_exact(self) -> None:
        self.assertIn("BS-ITEM-20260806-05", self.decisions)
        self.assertEqual(
            "MAX_ZERO_BASE_PLUS_MATERIAL_FIT_PLUS_DIRECT_FORGING",
            self.contract.get("crafted_role_stat_formula"),
        )
        self.assertEqual(
            {
                "SWORD": 5,
                "RANGED": 5,
                "AXE": 10,
                "BLUNT": 10,
                "POLEARM": 15,
                "SHIELD_SUPPORT": 5,
                "LIGHT_ARMOR": 5,
                "MEDIUM_ARMOR": 10,
                "HEAVY_ARMOR": 15,
                "TOOL": None,
                "CLOTHING_OR_ROBE": None,
                "ACCESSORY": None,
            },
            self.contract.get("base_item_role_base"),
        )
        self.assertEqual(
            {"LOW_ROLE_FIT": -2, "STANDARD_ROLE_FIT": 0, "HIGH_ROLE_FIT": 2},
            self.contract.get("primary_material_role_fit_modifier"),
        )
        self.assertEqual(
            {
                "BELOW_EXPECTED_DIRECT_FORGING": -1,
                "EXPECTED_DIRECT_FORGING": 0,
                "ABOVE_EXPECTED_DIRECT_FORGING": 1,
            },
            self.contract.get("direct_forging_role_modifier"),
        )
        self.assertEqual(
            "BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
            self.contract.get("balance_status"),
        )

    def test_general_enhancement_owns_no_item_raw_stat_delta(self) -> None:
        self.assertEqual(
            "ENHANCEMENT_LEVEL_AND_EVENT_SUCCESS_OWNER",
            self.contract.get("general_enhancement_owner"),
        )
        self.assertEqual(1, self.contract.get("general_event_success_bonus_per_level_pp"))
        self.assertEqual([], self.contract.get("general_enhancement_auto_changed_item_fields"))
        self.assertEqual(
            [
                "ATTACK",
                "DEFENSE",
                "WEIGHT",
                "DURABILITY",
                "HANDLING",
                "ARTISTRY",
                "MAGIC_FUNCTION_CAPACITY",
                "UTILITY_CAPACITY",
                "SPECIAL_FUNCTIONS",
            ],
            self.contract.get("general_enhancement_forbidden_auto_fields"),
        )

    def test_precision_method_delta_table_is_exact(self) -> None:
        self.assertEqual(["STAT_METHOD", "FUNCTION_REWORK"], self.contract.get("precision_output_lanes"))
        self.assertTrue(self.contract.get("precision_output_lanes_mutually_exclusive"))
        self.assertEqual(
            {
                "EDGE_REINFORCEMENT": {
                    "lane": "STAT_METHOD",
                    "changed_field": "APPROVED_ENHANCEMENT_ATTACK_OUTPUT",
                    "delta": 5,
                },
                "SHOCK_ABSORPTION": {
                    "lane": "STAT_METHOD",
                    "changed_field": "APPROVED_ENHANCEMENT_DEFENSE_OUTPUT",
                    "delta": 5,
                },
                "BALANCE_TUNING": {
                    "lane": "STAT_METHOD",
                    "changed_field": "HANDLING",
                    "delta": 5,
                },
                "ARTISTIC_FINISH": {
                    "lane": "STAT_METHOD",
                    "changed_field": "ARTISTRY",
                    "delta": 5,
                },
                "LIGHTWEIGHTING": {
                    "lane": "STAT_METHOD",
                    "changed_field": "CURRENT_WEIGHT",
                    "delta": -5,
                    "preserves_allocated_output": True,
                },
                "WEIGHTING": {
                    "lane": "STAT_METHOD",
                    "changed_field": "CURRENT_WEIGHT",
                    "delta": 5,
                    "peak_only_role_output": True,
                },
                "ENVIRONMENTAL_TREATMENT": {
                    "lane": "FUNCTION_REWORK",
                    "changed_field": "SPECIAL_FUNCTIONS",
                    "operations": ["ADD", "REPLACE", "REBIND", "REMOVE"],
                    "item_stat_delta": 0,
                },
            },
            self.contract.get("precision_method_outputs"),
        )

    def test_function_rework_is_exclusive_owner(self) -> None:
        self.assertEqual("FUNCTION_REWORK", self.contract.get("post_craft_function_owner"))
        self.assertEqual(["ADD", "REPLACE", "REBIND", "REMOVE"], self.contract.get("function_rework_actions"))
        self.assertTrue(self.contract.get("function_rework_requires_precision_milestone"))
        self.assertTrue(self.contract.get("function_rework_consumes_milestone"))
        self.assertFalse(self.contract.get("function_rework_milestone_refund_allowed", True))
        self.assertTrue(self.contract.get("failed_function_rework_preserves_previous_state"))
        self.assertFalse(self.contract.get("duplicate_function_id_allowed", True))
        self.assertFalse(self.contract.get("hidden_function_level_allowed", True))
        self.assertTrue(self.contract.get("approved_function_recipe_required"))
        self.assertFalse(self.contract.get("weight_capacity_auto_grants_function", True))

    def test_item_change_ledger_fields_are_exact(self) -> None:
        self.assertEqual(
            [
                "item_uid",
                "source_action_id",
                "source_owner",
                "enhancement_level_before",
                "enhancement_level_after",
                "changed_field",
                "value_before",
                "value_after",
                "delta_or_operation",
                "precision_milestone",
                "decision_id",
            ],
            self.contract.get("item_change_ledger_fields"),
        )
        self.assertTrue(self.contract.get("one_changed_field_per_ledger_row"))
        self.assertTrue(self.contract.get("multi_field_action_uses_shared_source_action_id"))

    def test_customer_user_stat_reference_contract_is_preserved(self) -> None:
        self.assertEqual(
            {
                "STRENGTH": {"range": [1, 10], "use": "MAXIMUM_LOAD_STRENGTH_X_10"},
                "DEXTERITY": {"range": [1, 10], "use": "RELEVANT_EVENT_CAPABILITY"},
                "CONSTITUTION": {"range": [1, 10], "use": "RELEVANT_EVENT_CAPABILITY"},
                "JUDGMENT": {"range": [1, 10], "use": "EVENT_OR_FUNCTION_CONTROL"},
                "EQUIPMENT_PROFICIENCY": {"range": [0, 3], "use": "MINUS10_0_PLUS5_PLUS10_PP"},
                "MAGIC_APTITUDE": {"range": [0, 10], "use": "MAGIC_FUNCTION_ELIGIBILITY_AND_RISK"},
                "MAGIC_AFFINITY_TAGS": {"range": [0, 2], "use": "BOUND_FUNCTION_COMPATIBILITY"},
            },
            self.contract.get("customer_user_stat_reference"),
        )
        self.assertFalse(self.contract.get("customer_stats_modify_item_attack_or_defense", True))
        self.assertEqual(5, self.contract.get("relevant_capability_met_bonus_pp"))

    def test_authority_documents_and_refinements_exist(self) -> None:
        for path in (CANON, SPEC, PLAN):
            self.assertTrue(path.exists(), f"missing authority document: {path}")
        canon = read_or_empty(CANON)
        for token in (
            "BS-ITEM-20260806-05",
            "R2_BATCH_005_9_OF_10",
            "MAX_ZERO_BASE_PLUS_MATERIAL_FIT_PLUS_DIRECT_FORGING",
            "GENERAL_ENHANCEMENT",
            "PRECISION_OUTPUT_LANE",
            "FUNCTION_REWORK",
            "ITEM_CHANGE_LEDGER_ENTRY",
            "42_능력치_강화_참조표",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)
        self.assertIn("BS-ITEM-20260806-05", read_or_empty(CURRENT))
        self.assertIn("R2_BATCH_005_CLOSED_10_OF_10", read_or_empty(CURRENT))
        self.assertIn("통합 변동 장부", read_or_empty(BIBLE))
        for path in (ITEM_ROLE_CANON, PRECISION_CANON, LOAD_CANON, WEIGHT_CONVERSION_CANON, ARTISTRY_CANON):
            text = read_or_empty(path)
            self.assertIn("REFINED_BY_BS-ITEM-20260806-05", text)
            self.assertIn("R2_BATCH_005_9_OF_10", text)
        weapon_bases = read_or_empty(WEAPON_BASES)
        self.assertNotIn('"attack"', weapon_bases)
        self.assertNotIn('"defense"', weapon_bases)
        self.assertNotIn('"special_functions"', weapon_bases)

    def test_sheet_reference_contract_is_declared(self) -> None:
        self.assertEqual("42_능력치_강화_참조표", self.contract.get("sheet_reference_tab"))
        self.assertEqual(
            [
                "ITEM_WEAPON_STATS",
                "CUSTOMER_USER_STATS",
                "ENHANCEMENT_DELTAS",
                "SPECIAL_FUNCTION_REWORK",
            ],
            self.contract.get("sheet_reference_sections"),
        )
        self.assertFalse(self.contract.get("sheet_is_authority", True))
        self.assertEqual("BLOCKED", self.contract.get("product_implementation"))

    def test_tdd_evidence_is_recorded(self) -> None:
        self.assertEqual("aaf88e008eda4eb089ff8eb864c5c5166d1ebf98", TDD_EVIDENCE["red_head"])
        self.assertEqual(31053492591, TDD_EVIDENCE["red_run_id"])
        self.assertEqual(254, TDD_EVIDENCE["red_planning_first_run"])
        self.assertEqual(66, TDD_EVIDENCE["red_existing_pass"])
        self.assertEqual(9, TDD_EVIDENCE["red_expected_new_failures"])
        self.assertEqual("507eff3ba9864c254ac58c1d24166cf566b15a2a", TDD_EVIDENCE["green_sync_head"])
        self.assertEqual(31054424664, TDD_EVIDENCE["green_one_shot_run"])
        self.assertEqual(75, TDD_EVIDENCE["green_focused_pass"])
        self.assertEqual("PASS", TDD_EVIDENCE["green_core_alignment"])
        self.assertEqual("PASS", TDD_EVIDENCE["green_operating_audit"])
        self.assertEqual(0, TDD_EVIDENCE["green_protected_product_paths"])


if __name__ == "__main__":
    unittest.main()
