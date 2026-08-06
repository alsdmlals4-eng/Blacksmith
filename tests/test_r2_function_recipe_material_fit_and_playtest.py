from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_FUNCTION_RECIPE_MATERIAL_FIT_AND_PLAYTEST_CANON_2026.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-06-function-recipes-material-fit-forging-playtest-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-06-function-recipes-material-fit-forging-playtest.md"
EVIDENCE = ROOT / "docs/planning/BLACKSMITH_R2_FUNCTION_RECIPE_MATERIAL_FIT_AND_PLAYTEST_EVIDENCE_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
INITIAL_OWNERSHIP_CANON = ROOT / "docs/planning/BLACKSMITH_R2_INITIAL_ROLE_STAT_PRESET_AND_ENHANCEMENT_FUNCTION_OWNERSHIP_CANON_2026.md"
ITEM_FUNCTION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md"
PRECISION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md"
MATERIALS = ROOT / "data/crafting/materials.json"
WEAPON_BASES = ROOT / "data/crafting/weapon_bases.json"
FORGING_BALANCE = ROOT / "data/crafting/forging_balance.json"
CRAFTSMANSHIP_GRADES = ROOT / "data/crafting/craftsmanship_grades.json"


def read_or_empty(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class FunctionRecipeMaterialFitPlaytestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}
        cls.contract = cls.decisions.get("BS-ITEM-20260806-06", {}).get("contract", {})

    def test_batch_005_is_complete_at_ten_of_ten(self) -> None:
        self.assertEqual("R2_BATCH_006_APPROVED_MAIN_CANON", self.registry["stage_status"])
        self.assertEqual("0/10", self.registry["next_approval_counter"])
        closed = self.registry["closed_batch"]
        self.assertEqual(10, closed["approved_decisions"])
        self.assertEqual("10/10", closed["counter"])
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
            closed["decisions"],
        )

    def test_primary_material_role_fit_matrix_is_exact(self) -> None:
        self.assertIn("BS-ITEM-20260806-06", self.decisions)
        self.assertEqual(
            "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP",
            self.contract.get("material_role_fit_model"),
        )
        self.assertEqual(
            {
                "iron": {
                    "SWORD": 0,
                    "AXE": 0,
                    "BLUNT": 0,
                    "POLEARM": 0,
                    "RANGED": 0,
                    "SHIELD_SUPPORT": 0,
                    "LIGHT_ARMOR": 0,
                    "MEDIUM_ARMOR": 0,
                    "HEAVY_ARMOR": 0,
                },
                "silver": {
                    "SWORD": 2,
                    "AXE": -2,
                    "BLUNT": -2,
                    "POLEARM": -2,
                    "RANGED": 2,
                    "SHIELD_SUPPORT": 0,
                    "LIGHT_ARMOR": 2,
                    "MEDIUM_ARMOR": 0,
                    "HEAVY_ARMOR": -2,
                },
                "meteor_iron": {
                    "SWORD": 0,
                    "AXE": 2,
                    "BLUNT": 2,
                    "POLEARM": 2,
                    "RANGED": -2,
                    "SHIELD_SUPPORT": 0,
                    "LIGHT_ARMOR": -2,
                    "MEDIUM_ARMOR": 0,
                    "HEAVY_ARMOR": 2,
                },
            },
            self.contract.get("primary_material_role_fit"),
        )

    def test_role_fit_is_not_applied_to_non_role_items(self) -> None:
        self.assertEqual(
            ["TOOL", "CLOTHING_OR_ROBE", "ACCESSORY"],
            self.contract.get("role_fit_not_applied_equipment_groups"),
        )
        self.assertFalse(self.contract.get("role_fit_creates_missing_attack_or_defense", True))

    def test_direct_forging_role_strike_is_exact_and_deterministic(self) -> None:
        self.assertEqual(
            "DETERMINISTIC_ROLE_STRIKE_THREE_ZONE",
            self.contract.get("direct_forging_role_result_model"),
        )
        self.assertEqual(
            {
                "OUTSIDE_GOOD_ZONE": -1,
                "GOOD_ZONE": 0,
                "PERFECT_ZONE": 1,
            },
            self.contract.get("direct_forging_role_result_modifiers"),
        )
        self.assertEqual(0, self.contract.get("automatic_forging_role_modifier"))
        self.assertFalse(self.contract.get("direct_forging_role_result_uses_rng", True))
        self.assertFalse(self.contract.get("role_strike_in_grade_calculation", True))
        self.assertFalse(self.contract.get("role_strike_applies_without_role_stat", True))

    def test_direct_forging_playtest_distribution_is_a_target_not_rng(self) -> None:
        self.assertEqual(
            {"BELOW_EXPECTED": 20, "EXPECTED": 60, "ABOVE_EXPECTED": 20},
            self.contract.get("novice_role_result_target_percent"),
        )
        self.assertEqual(
            {
                "BELOW_EXPECTED": [10, 30],
                "EXPECTED": [50, 70],
                "ABOVE_EXPECTED": [10, 30],
            },
            self.contract.get("novice_role_result_allowed_percent"),
        )
        self.assertEqual("HUMAN_DIFFICULTY_TUNING_TARGET", self.contract.get("distribution_semantics"))

    def test_initial_function_recipe_catalog_is_exact(self) -> None:
        self.assertEqual(
            "ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY",
            self.contract.get("function_recipe_model"),
        )
        self.assertEqual(
            {
                "ARCANE_CONDUCTION": {
                    "profiles": ["MAGIC_IMPLEMENT"],
                    "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
                    "primary_materials": ["silver", "meteor_iron"],
                    "minimum_recognized_weight": 5,
                    "bound_context": None,
                    "capacity_cost": 1,
                },
                "ELEMENTAL_WARD": {
                    "profiles": ["MAGIC_IMPLEMENT"],
                    "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
                    "primary_materials": ["silver"],
                    "minimum_recognized_weight": 5,
                    "bound_context": "ONE_ELEMENT",
                    "capacity_cost": 1,
                },
                "ARCANE_SENSING": {
                    "profiles": ["MAGIC_IMPLEMENT"],
                    "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
                    "primary_materials": ["meteor_iron"],
                    "minimum_recognized_weight": 10,
                    "bound_context": "ONE_MAGIC_SIGNATURE",
                    "capacity_cost": 2,
                },
                "ENVIRONMENTAL_SEALING": {
                    "profiles": ["UTILITY_IMPLEMENT", "UTILITY_GARMENT"],
                    "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
                    "primary_materials": ["iron", "silver"],
                    "minimum_recognized_weight": 5,
                    "bound_context": "ONE_ENVIRONMENT",
                    "capacity_cost": 1,
                },
                "FIELD_SERVICEABILITY": {
                    "profiles": ["UTILITY_IMPLEMENT"],
                    "equipment_groups": ["TOOL"],
                    "primary_materials": ["iron"],
                    "minimum_recognized_weight": 5,
                    "bound_context": None,
                    "capacity_cost": 1,
                },
                "TASK_INTEGRATION": {
                    "profiles": ["UTILITY_IMPLEMENT", "UTILITY_GARMENT"],
                    "equipment_groups": ["TOOL", "CLOTHING_OR_ROBE"],
                    "primary_materials": ["iron", "silver", "meteor_iron"],
                    "minimum_recognized_weight": 5,
                    "bound_context": "ONE_TASK",
                    "capacity_cost": 1,
                },
            },
            self.contract.get("initial_function_recipes"),
        )
        self.assertTrue(self.contract.get("initial_recipe_success_is_deterministic"))
        self.assertFalse(self.contract.get("random_function_generation_allowed", True))

    def test_rework_tags_and_current_availability_are_exact(self) -> None:
        self.assertEqual(
            {
                "ARCANE_CONDUCTION": {"add_replace": "arcane_matrix", "rebind": None},
                "ELEMENTAL_WARD": {"add_replace": "element:<BOUND_ELEMENT>", "rebind": "element:<NEW_ELEMENT>"},
                "ARCANE_SENSING": {"add_replace": "signature:<BOUND_SIGNATURE>", "rebind": "signature:<NEW_SIGNATURE>"},
                "ENVIRONMENTAL_SEALING": {"add_replace": "environment:<BOUND_ENVIRONMENT>", "rebind": "environment:<NEW_ENVIRONMENT>"},
                "FIELD_SERVICEABILITY": {"add_replace": "service", "rebind": None},
                "TASK_INTEGRATION": {"add_replace": "task:<BOUND_TASK>", "rebind": "task:<NEW_TASK>"},
            },
            self.contract.get("rework_catalyst_requirements"),
        )
        self.assertEqual(
            {"fire": ["element:fire", "environment:fire"]},
            self.contract.get("catalyst_tag_projection"),
        )
        self.assertEqual(
            ["ELEMENTAL_WARD_FIRE", "ENVIRONMENTAL_SEALING_FIRE"],
            self.contract.get("current_available_bound_reworks"),
        )
        self.assertEqual(
            ["ARCANE_CONDUCTION", "ARCANE_SENSING", "FIELD_SERVICEABILITY", "TASK_INTEGRATION"],
            self.contract.get("content_not_available_reworks"),
        )
        self.assertFalse(self.contract.get("guardian_powder_is_neutral_function_catalyst", True))
        self.assertTrue(self.contract.get("remove_consumes_any_catalyst"))
        self.assertTrue(self.contract.get("remove_consumes_precision_milestone"))
        self.assertTrue(self.contract.get("replace_is_atomic"))

    def test_human_playtest_gate_is_exact(self) -> None:
        self.assertEqual(48, self.contract.get("solo_playtest_case_count"))
        self.assertEqual(
            {"material_fit": 27, "role_strike": 9, "initial_recipes": 6, "rework_cases": 6},
            self.contract.get("solo_playtest_case_breakdown"),
        )
        self.assertEqual(3, self.contract.get("external_playtester_minimum"))
        self.assertEqual(5, self.contract.get("external_playtester_maximum"))
        self.assertEqual([45, 60], self.contract.get("external_session_minutes"))
        self.assertEqual(
            [
                "NO_DOUBLE_COUNT",
                "NO_RECIPELESS_FUNCTION_GENERATION",
                "NO_REPLACE_INTERMEDIATE_STATE_LOSS",
            ],
            self.contract.get("playtest_integrity_zero_requirements"),
        )
        self.assertEqual(6, self.contract.get("pass_required_quantitative_metrics_of_seven"))
        self.assertEqual(["PASS", "REVISE", "REJECT"], self.contract.get("playtest_outcomes"))
        self.assertEqual("NOT_RUN", self.contract.get("human_playtest_status"))

    def test_authority_documents_refinements_and_product_protection_exist(self) -> None:
        for path in (CANON, SPEC, PLAN, EVIDENCE):
            self.assertTrue(path.exists(), f"missing authority document: {path}")
        canon = read_or_empty(CANON)
        for token in (
            "BS-ITEM-20260806-06",
            "R2_BATCH_005_10_OF_10",
            "EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP",
            "DETERMINISTIC_ROLE_STRIKE_THREE_ZONE",
            "ELEMENTAL_WARD(FIRE)",
            "ENVIRONMENTAL_SEALING(FIRE)",
            "48",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)
        self.assertIn("BS-ITEM-20260806-06", read_or_empty(CURRENT))
        self.assertIn("R2_BATCH_005_CLOSED_10_OF_10", read_or_empty(CURRENT))
        self.assertIn("사람 플레이테스트", read_or_empty(BIBLE))
        for path in (INITIAL_OWNERSHIP_CANON, ITEM_FUNCTION_CANON, PRECISION_CANON):
            text = read_or_empty(path)
            self.assertIn("REFINED_BY_BS-ITEM-20260806-06", text)
            self.assertIn("R2_BATCH_005_10_OF_10", text)
        for path in (MATERIALS, WEAPON_BASES, FORGING_BALANCE, CRAFTSMANSHIP_GRADES):
            text = read_or_empty(path)
            self.assertNotIn("BS-ITEM-20260806-06", text)
            self.assertNotIn("primary_material_role_fit", text)
            self.assertNotIn("function_recipe_model", text)

    def test_sheet_reference_and_tdd_evidence_are_declared(self) -> None:
        self.assertEqual("42_능력치_강화_참조표", self.contract.get("sheet_reference_tab"))
        self.assertEqual(
            [
                "PRIMARY_MATERIAL_ROLE_FIT",
                "DIRECT_FORGING_ROLE_RESULT",
                "FUNCTION_RECIPE_CATALOG",
                "HUMAN_PLAYTEST_PLAN",
            ],
            self.contract.get("sheet_reference_sections"),
        )
        self.assertFalse(self.contract.get("sheet_is_authority", True))
        self.assertEqual("BLOCKED", self.contract.get("product_implementation"))
        evidence = self.contract.get("tdd_evidence", {})
        self.assertEqual("PASS", evidence.get("red_verified"))
        self.assertEqual("PASS", evidence.get("green_verified"))
        self.assertEqual(0, evidence.get("protected_product_path_changes"))

    def test_exact_red_green_evidence_is_recorded(self) -> None:
        evidence = self.contract.get("tdd_evidence", {})
        self.assertEqual("f90dcdf70eabd30ecdde4def11a2ef30112a3caa", evidence.get("red_head"))
        self.assertEqual(283, evidence.get("red_planning_first_run"))
        self.assertEqual(76, evidence.get("red_existing_pass"))
        self.assertEqual(10, evidence.get("red_expected_fail"))
        evidence_text = read_or_empty(EVIDENCE)
        for token in (
            "GREEN_SYNC_HEAD=b9ba179232d7d3a35da7da3e85ce55fee1583503",
            "GREEN_ONE_SHOT_RUN=31064922435",
            "GREEN_FOCUSED_PASS=86",
            "GREEN_CORE_ALIGNMENT=PASS",
            "GREEN_BASE_OPERATING_AUDIT=PASS",
            "GREEN_PROTECTED_PRODUCT_PATH_CHANGES=0",
        ):
            self.assertIn(token, evidence_text)
        self.assertEqual(0, evidence.get("protected_product_path_changes"))


if __name__ == "__main__":
    unittest.main()
