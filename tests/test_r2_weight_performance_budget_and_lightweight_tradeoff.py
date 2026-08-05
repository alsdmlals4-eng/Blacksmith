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

RED_EVIDENCE = {
    "commit": "f6f9210e992ba11d7bda9c9b58fca7744a4236e2",
    "planning_first_run": 207,
    "focused_tests": 47,
    "expected_new_failures": 7,
}
GREEN_EVIDENCE = {
    "canon_sync_head": "fbbd2455e8c063ae20d2e60480946417cc812e9e",
    "operating_audit_repair_head": "dc3664024acf999a602a12719a50a9780d2e61c8",
    "focused_tests": 48,
    "focused_result": "PASS",
    "project_core_alignment": "PASS",
    "operating_audit": "PASS",
}


def read_or_empty(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


class WeightPerformanceBudgetTradeoffContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_tdd_evidence_is_recorded(self) -> None:
        self.assertEqual(207, RED_EVIDENCE["planning_first_run"])
        self.assertEqual(7, RED_EVIDENCE["expected_new_failures"])
        self.assertEqual("PASS", GREEN_EVIDENCE["focused_result"])
        self.assertEqual("PASS", GREEN_EVIDENCE["project_core_alignment"])
        self.assertEqual("PASS", GREEN_EVIDENCE["operating_audit"])

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

    def test_budget_uses_monotonic_recognized_weight_not_current_weight(self) -> None:
        self.assertIn("BS-ITEM-20260806-02", self.decisions)
        contract = self.decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
        self.assertEqual(
            "PEAK_RECOGNIZED_WEIGHT_MONOTONIC_SINGLE_SOURCE",
            contract.get("weight_performance_budget_model"),
        )
        self.assertEqual(
            "MAX_INITIAL_OR_HIGHEST_SUCCESSFUL_CURRENT_WEIGHT_DIVIDED_BY_5",
            contract.get("weight_performance_budget_formula"),
        )
        self.assertEqual(5, contract.get("weight_points_per_budget_point"))
        self.assertTrue(contract.get("initial_weight_grants_initial_budget"))
        self.assertTrue(contract.get("lightweighting_preserves_existing_budget"))
        self.assertTrue(contract.get("budget_recognized_weight_is_monotonic"))
        self.assertTrue(contract.get("current_weight_drives_customer_load_gate"))
        self.assertTrue(contract.get("weighting_grants_budget_only_above_previous_peak"))
        self.assertFalse(contract.get("weight_budget_multiplied_by_other_progression_axes", True))

    def test_budget_lanes_are_explicit_and_compatible(self) -> None:
        contract = self.decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
        self.assertEqual(
            ["ATTACK_BUDGET", "DEFENSE_BUDGET", "MAGIC_FUNCTION_BUDGET", "UTILITY_BUDGET"],
            contract.get("budget_lanes"),
        )
        self.assertTrue(contract.get("budget_point_allocates_to_exactly_one_lane"))
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

    def test_weight_adjustment_consumes_precision_milestone_opportunity(self) -> None:
        contract = self.decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
        self.assertEqual("PRECISION_ENHANCEMENT_METHOD", contract.get("weight_adjustment_owner"))
        self.assertEqual(
            {"LIGHTWEIGHTING": -5, "WEIGHTING": 5},
            contract.get("weight_delta_by_operation"),
        )
        self.assertEqual([10, 20, 30, 40, 50], contract.get("precision_milestones"))
        self.assertEqual(1, contract.get("maximum_weight_adjustments_per_precision_milestone"))
        self.assertTrue(contract.get("weight_adjustments_accumulate_across_distinct_milestones"))
        self.assertFalse(contract.get("same_milestone_weight_adjustment_replay_allowed", True))
        self.assertFalse(contract.get("used_precision_milestone_refund_allowed", True))

    def test_weight_budget_does_not_replace_enhancement_or_generic_success(self) -> None:
        contract = self.decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
        self.assertFalse(contract.get("weight_budget_directly_changes_generic_success_rate", True))
        self.assertEqual("BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED", contract.get("exact_stat_conversion"))
        self.assertEqual("BLOCKED", contract.get("product_implementation"))
        weapon_bases = read_or_empty(WEAPON_BASES)
        self.assertNotIn('"weight_performance_budget"', weapon_bases)
        self.assertNotIn('"budget_recognized_weight"', weapon_bases)

    def test_authority_documents_record_budget_preservation_and_peak_only_gain(self) -> None:
        for path in (CANON, SPEC, PLAN):
            self.assertTrue(path.exists(), f"missing authority document: {path}")
        canon = read_or_empty(CANON)
        for token in (
            "BS-ITEM-20260806-02",
            "R2_BATCH_005_6_OF_10",
            "최초 제작 중량 5당 초기 성능 예산 +1",
            "경량화 -5 중량 / 기존 예산 유지",
            "중량화 +5 중량 / 과거 최고 인정 중량 초과분만 예산 추가",
            "정밀강화 +10 / +20 / +30 / +40 / +50",
            "PRECISION_ENHANCEMENT_METHOD",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)
        self.assertIn("BS-ITEM-20260806-02", read_or_empty(CURRENT))
        self.assertIn("R2_BATCH_005 / 7/10", read_or_empty(CURRENT))
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
        self.assertIn("현재 중량 전후", ux)
        self.assertIn("인정 중량", ux)
        self.assertIn("WITHIN_LIMIT / OVERWEIGHT", load)
        self.assertNotIn("단계별 중량 초과 페널티 재도입", load)


if __name__ == "__main__":
    unittest.main()
