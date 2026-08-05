from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md"
LEGACY_CUSTOMER_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_SCHEDULE_AND_VISIBLE_CAPABILITY_CANON_2026.md"
GAME_BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"


class CustomerEquipmentCompatibilityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_batch_005_contains_seven_approved_decisions(self) -> None:
        self.assertEqual("R2_BATCH_005_ACTIVE_7_OF_10", self.registry["stage_status"])
        self.assertEqual("7/10", self.registry["next_approval_counter"])
        active = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_005", active["id"])
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
    def test_customer_axes_and_sparse_proficiencies_are_canonical(self) -> None:
        self.assertIn("BS-CUSTOMER-20260805-01", self.decisions)
        contract = self.decisions.get("BS-CUSTOMER-20260805-01", {}).get("contract", {})
        self.assertEqual(
            ["STRENGTH", "DEXTERITY", "CONSTITUTION", "JUDGMENT"],
            contract.get("base_stats"),
        )
        self.assertEqual("INTEGER_1_TO_10", contract.get("base_stat_scale"))
        self.assertEqual("SPARSE_PRIMARY_ONE_SECONDARY_MAX_ONE", contract.get("weapon_proficiency_storage"))
        self.assertEqual("SPARSE_PRIMARY_ONE_SECONDARY_MAX_ONE", contract.get("armor_proficiency_storage"))
        self.assertEqual("INTEGER_0_TO_3", contract.get("proficiency_scale"))
        self.assertEqual("INTEGER_0_TO_10", contract.get("magic_aptitude_scale"))
        self.assertEqual(2, contract.get("magic_affinity_tag_maximum"))

    def test_customer_archetype_stat_identifiers_follow_the_refined_schema(self) -> None:
        new_decision = self.decisions["BS-CUSTOMER-20260805-01"]
        self.assertIn("BS-CONTENT-20260804-02", new_decision.get("refines", []))
        archetype_contract = self.decisions["BS-CONTENT-20260804-02"]["contract"]
        self.assertEqual("DEXTERITY", archetype_contract["noble_optional_secondary_stat"])
        self.assertNotEqual("SKILL", archetype_contract["noble_optional_secondary_stat"])

    def test_equipment_taxonomy_and_applicable_stats_are_explicit(self) -> None:
        contract = self.decisions.get("BS-CUSTOMER-20260805-01", {}).get("contract", {})
        self.assertEqual(
            ["WEAPON", "SHIELD_OR_OFFHAND", "ARMOR", "ACCESSORY_OR_TOOL"],
            contract.get("equipment_categories"),
        )
        self.assertEqual(
            ["SWORD", "AXE", "BLUNT", "POLEARM", "RANGED", "SHIELD_SUPPORT"],
            contract.get("weapon_groups"),
        )
        self.assertEqual(
            ["CLOTHING_OR_ROBE", "LIGHT", "MEDIUM", "HEAVY"],
            contract.get("armor_classes"),
        )
        self.assertEqual(
            ["WEIGHT", "DURABILITY", "HANDLING", "ARTISTRY"],
            contract.get("common_item_stats"),
        )
        self.assertEqual(
            ["ATTACK", "DEFENSE", "STABILITY", "ENVIRONMENTAL_RESPONSE", "SPECIAL_FUNCTIONS"],
            contract.get("conditional_item_stats"),
        )
        self.assertTrue(contract.get("non_applicable_stats_are_omitted"))

    def test_fit_is_derived_without_double_counting_item_power(self) -> None:
        contract = self.decisions.get("BS-CUSTOMER-20260805-01", {}).get("contract", {})
        self.assertEqual(
            ["TOTAL_WEIGHT", "COMFORTABLE_LOAD", "BALANCE_STATE", "SPECIAL_FUNCTION_FIT"],
            contract.get("derived_loadout_states"),
        )
        self.assertEqual(
            ["UNSUITABLE", "UNSTABLE", "STABLE", "SKILLED"],
            contract.get("balance_states"),
        )
        self.assertEqual("NO_PENALTY_AT_OR_BELOW_COMFORTABLE_LOAD", contract.get("load_rule"))
        self.assertEqual("ESCALATING_OVERLOAD_PENALTY", contract.get("overload_rule"))
        self.assertFalse(contract.get("customer_stats_directly_add_to_item_attack_or_defense"))
        self.assertTrue(contract.get("raw_item_stats_remain_owned_by_item"))
        self.assertEqual(
            ["MAGIC_APTITUDE", "RELEVANT_AFFINITY", "JUDGMENT", "RELEVANT_PROFICIENCY", "ACTIVATION_CONDITIONS"],
            contract.get("special_function_fit_factors"),
        )

    def test_existing_disclosure_contract_and_product_gate_remain(self) -> None:
        prior = self.decisions["BS-CUSTOMER-20260803-02"]["contract"]
        self.assertEqual("INTEGER_1_TO_10", prior["event_risk_scale"])
        self.assertEqual("NEAREST_10_PERCENT", prior["success_forecast_rounding"])
        self.assertEqual("5_TO_95_PERCENT", prior["success_forecast_range"])
        self.assertEqual("BLOCKED", self.registry["product_implementation"])
        new_contract = self.decisions.get("BS-CUSTOMER-20260805-01", {}).get("contract", {})
        self.assertEqual("BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED", new_contract.get("exact_values"))

    def test_authority_documents_record_refinement_and_protection(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        legacy = LEGACY_CUSTOMER_CANON.read_text(encoding="utf-8")
        bible = GAME_BIBLE.read_text(encoding="utf-8")
        for token in (
            "BS-CUSTOMER-20260805-01",
            "근력 / 기량 / 체력 / 판단력",
            "WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL",
            "부적합 / 불안정 / 안정 / 능숙",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)
        self.assertIn("BS-CUSTOMER-20260805-01", legacy)
        self.assertIn("능력 구조는 후속 결정으로 정제", legacy)
        self.assertIn("BS-CUSTOMER-20260805-01", bible)
        self.assertIn("고객·장비 적합성", bible)


if __name__ == "__main__":
    unittest.main()
