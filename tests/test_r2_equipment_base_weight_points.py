from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-06-equipment-base-weight-points-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-06-equipment-base-weight-points.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
LOAD_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md"
CUSTOMER_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md"
UX_CANON = ROOT / "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md"
WEAPON_BASES = ROOT / "data/crafting/weapon_bases.json"

EXPECTED_BASE_WEIGHTS = {
    "ACCESSORY": 0,
    "TOOL": 5,
    "CLOTHING_OR_ROBE": 5,
    "LIGHT_ARMOR": 10,
    "MEDIUM_ARMOR": 20,
    "HEAVY_ARMOR": 30,
    "SWORD": 10,
    "AXE": 15,
    "BLUNT": 15,
    "POLEARM": 20,
    "RANGED": 10,
    "SHIELD_SUPPORT": 10,
}


def read_or_empty(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class EquipmentBaseWeightPointsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_batch_005_contains_ten_approved_decisions(self) -> None:
        self.assertEqual("R2_BATCH_006_APPROVED_MAIN_CANON", self.registry["stage_status"])
        self.assertEqual("0/10", self.registry["next_approval_counter"])
        closed = self.registry["closed_batch"]
        self.assertEqual("R2_BATCH_005", closed["id"])
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
    def test_base_weight_table_is_exact_and_uses_five_point_steps(self) -> None:
        self.assertIn("BS-ITEM-20260806-01", self.decisions)
        contract = self.decisions.get("BS-ITEM-20260806-01", {}).get("contract", {})
        self.assertEqual("EQUIPMENT_GROUP_FIXED_BASE_WEIGHT", contract.get("base_weight_model"))
        self.assertEqual("WEIGHT_POINT", contract.get("weight_unit"))
        self.assertEqual(EXPECTED_BASE_WEIGHTS, contract.get("base_weight_points"))
        self.assertTrue(all(value % 5 == 0 for value in EXPECTED_BASE_WEIGHTS.values()))
        self.assertEqual(
            {"sword": "SWORD", "spear": "POLEARM", "axe": "AXE"},
            contract.get("current_weapon_base_group_mapping"),
        )

    def test_only_one_explicit_additive_modifier_can_change_weight(self) -> None:
        contract = self.decisions.get("BS-ITEM-20260806-01", {}).get("contract", {})
        self.assertEqual("BASE_WEIGHT_PLUS_ONE_EXPLICIT_MODIFIER", contract.get("item_weight_formula"))
        self.assertEqual(
            {"LIGHTWEIGHT": -5, "NONE": 0, "WEIGHTED": 5},
            contract.get("explicit_weight_modifiers"),
        )
        self.assertEqual(1, contract.get("maximum_active_weight_modifiers_per_item"))
        self.assertEqual(0, contract.get("minimum_final_item_weight"))
        self.assertFalse(contract.get("weight_modifiers_stack", True))
        self.assertFalse(contract.get("weight_modifier_multiplies_base_weight", True))
        self.assertFalse(contract.get("weight_modifier_directly_changes_success_rate", True))
        self.assertFalse(contract.get("weighted_modifier_has_automatic_compensation", True))

    def test_unrelated_item_axes_do_not_automatically_change_weight(self) -> None:
        contract = self.decisions.get("BS-ITEM-20260806-01", {}).get("contract", {})
        self.assertEqual(
            [
                "MATERIAL",
                "CRAFTSMANSHIP_GRADE",
                "ARTISTRY",
                "ATTACK",
                "DEFENSE",
                "HANDLING",
                "DURABILITY",
                "GENERAL_ENHANCEMENT_LEVEL",
            ],
            contract.get("forbidden_automatic_weight_sources"),
        )
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        weapon_bases = read_or_empty(WEAPON_BASES)
        self.assertNotIn('"weight"', weapon_bases)
        self.assertNotIn('"weight_point"', weapon_bases)

    def test_authority_documents_record_simple_weight_contract(self) -> None:
        for path in (CANON, SPEC, PLAN):
            self.assertTrue(path.exists(), f"missing authority document: {path}")
        canon = read_or_empty(CANON)
        for token in (
            "BS-ITEM-20260806-01",
            "R2_BATCH_005_5_OF_10",
            "장신구 | `ACCESSORY` | 0",
            "중장갑 | `HEAVY_ARMOR` | 30",
            "장병기류 | `POLEARM` | 20",
            "LIGHTWEIGHT: -5",
            "WEIGHTED: +5",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)

        current = read_or_empty(CURRENT)
        bible = read_or_empty(BIBLE)
        self.assertIn("BS-ITEM-20260806-01", current)
        self.assertIn("R2_BATCH_005_CLOSED_10_OF_10", current)
        self.assertIn("장비군 고정 기본 중량", bible)
        self.assertIn("재료·제작 등급·예술성", bible)

    def test_previous_load_customer_and_ux_canons_are_refined(self) -> None:
        load = read_or_empty(LOAD_CANON)
        customer = read_or_empty(CUSTOMER_CANON)
        ux = read_or_empty(UX_CANON)
        for text in (load, customer, ux):
            self.assertIn("REFINED_BY_BS-ITEM-20260806-01", text)
            self.assertIn("R2_BATCH_005_5_OF_10", text)
        self.assertIn("BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER", load)
        self.assertIn("경량화 -5", ux)
        self.assertIn("중량화 +5", ux)


if __name__ == "__main__":
    unittest.main()
