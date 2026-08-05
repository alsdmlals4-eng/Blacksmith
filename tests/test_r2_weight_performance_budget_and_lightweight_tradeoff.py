from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-06-weight-performance-budget-and-lightweight-tradeoff-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-06-weight-performance-budget-and-lightweight-tradeoff.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
WEIGHT_CANON = ROOT / "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md"
PRECISION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md"
LOAD_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md"
UX_CANON = ROOT / "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md"
WEAPON_BASES = ROOT / "data/crafting/weapon_bases.json"


def read_or_empty(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class WeightPerformanceBudgetTradeoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_batch_005_contains_six_approved_decisions(self) -> None:
        self.assertEqual("R2_BATCH_005_ACTIVE_6_OF_10", self.registry["stage_status"])
        self.assertEqual("6/10", self.registry["next_approval_counter"])
        active = self.registry["active_batch"]
        self.assertEqual(6, active["approved_decisions"])
        self.assertEqual("6/10", active["counter"])
        self.assertEqual(
            [
                "BS-CRAFT-20260805-02",
                "BS-CUSTOMER-20260805-01",
                "BS-UX-20260805-01",
                "BS-CUSTOMER-20260806-01",
                "BS-ITEM-20260806-01",
                "BS-ITEM-20260806-02",
            ],
            active["decisions"],
        )

    def test_final_weight_produces_one_budget_point_per_five_weight(self) -> None:
        self.assertIn("BS-ITEM-20260806-02", self.decisions)
        contract = self.decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
        self.assertEqual("FINAL_WEIGHT_LINEAR_SINGLE_SOURCE", contract.get("weight_performance_budget_model"))
        self.assertEqual("EFFECTIVE_WEIGHT_DIVIDED_BY_5", contract.get("weight_performance_budget_formula"))
        self.assertEqual(5, contract.get("weight_points_per_budget_point"))
        self.assertTrue(contract.get("budget_point_allocates_to_exactly_one_lane"))
        self.assertFalse(contract.get("weight_budget_multiplied_by_other_progression_axes", True))

    def test_budget_lanes_are_explicit_and_compatible(self) -> None:
        contract = self.decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
        self.assertEqual(
            ["ATTACK_BUDGET", "DEFENSE_BUDGET", "MAGIC_FUNCTION_BUDGET", "UTILITY_BUDGET"],
            contract.get("budget_lanes"),
        )
        compatibility = contract.get("equipment_lane_compatibility", {})
        self.assertEqual(
            ["ATTACK_BUDGET", "MAGIC_FUNCTION_BUDGET", "UTILITY_BUDGET"],
            compatibility.get("WEAPON"),
        )
        self.assertEqual(
            ["DEFENSE_BUDGET", "MAGIC_FUNCTION_BUDGET", "UTILITY_BUDGET"],
            compatibility.get("ARMOR"),
        )
        self.assertEqual([], compatibility.get("ACCESSORY"))
        self.assertFalse(contract.get("accessory_weight_budget_enabled_by_default", True))

    def test_structural_weight_treatment_is_precision_enhancement_tradeoff(self) -> None:
        contract = self.decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
        self.assertEqual("PRECISION_ENHANCEMENT_METHOD", contract.get("structural_weight_treatment_owner"))
        self.assertEqual(
            {"LIGHTWEIGHT": -5, "NONE": 0, "WEIGHTED": 5},
            contract.get("weight_delta_by_treatment"),
        )
        self.assertEqual(
            {"LIGHTWEIGHT": -1, "NONE": 0, "WEIGHTED": 1},
            contract.get("budget_delta_by_treatment"),
        )
        self.assertEqual(1, contract.get("maximum_active_structural_weight_treatments_per_item"))
        self.assertFalse(contract.get("structural_weight_treatments_stack", True))
        self.assertEqual("REPLACE_AND_RECALCULATE_DERIVED_BUDGET", contract.get("rework_semantics"))

    def test_weight_budget_does_not_replace_enhancement_or_generic_success(self) -> None:
        contract = self.decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
        self.assertFalse(contract.get("weight_budget_directly_changes_generic_success_rate", True))
        self.assertEqual("BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED", contract.get("exact_stat_conversion"))
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        weapon_bases = read_or_empty(WEAPON_BASES)
        self.assertNotIn('"weight_performance_budget"', weapon_bases)
        self.assertNotIn('"structural_weight_treatment"', weapon_bases)

    def test_authority_documents_record_the_tradeoff(self) -> None:
        for path in (CANON, SPEC, PLAN):
            self.assertTrue(path.exists(), f"missing authority document: {path}")
        canon = read_or_empty(CANON)
        for token in (
            "BS-ITEM-20260806-02",
            "R2_BATCH_005_6_OF_10",
            "최종 중량 5당 성능 예산 +1",
            "경량화 -5 중량 / -1 예산",
            "중량화 +5 중량 / +1 예산",
            "PRECISION_ENHANCEMENT_METHOD",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)
        self.assertIn("BS-ITEM-20260806-02", read_or_empty(CURRENT))
        self.assertIn("R2_BATCH_005 / 6/10", read_or_empty(CURRENT))
        self.assertIn("중량 성능 예산", read_or_empty(BIBLE))

    def test_prior_canons_are_refined_without_reintroducing_overload_penalties(self) -> None:
        weight = read_or_empty(WEIGHT_CANON)
        precision = read_or_empty(PRECISION_CANON)
        load = read_or_empty(LOAD_CANON)
        ux = read_or_empty(UX_CANON)
        for text in (weight, precision, load, ux):
            self.assertIn("REFINED_BY_BS-ITEM-20260806-02", text)
            self.assertIn("R2_BATCH_005_6_OF_10", text)
        self.assertIn("정밀강화 방식", precision)
        self.assertIn("중량 예산 전후", ux)
        self.assertIn("WITHIN_LIMIT / OVERWEIGHT", load)
        self.assertNotIn("단계별 중량 초과 페널티 재도입", load)


if __name__ == "__main__":
    unittest.main()
