from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-06-enhancement-dominant-simple-load-gate-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-06-enhancement-dominant-simple-load-gate.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
CUSTOMER_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md"
UX_CANON = ROOT / "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md"


class EnhancementDominantSimpleLoadGateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_batch_005_contains_ten_approved_decisions(self) -> None:
        self.assertEqual("R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING", self.registry["stage_status"])
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
    def test_load_is_a_binary_strength_gate(self) -> None:
        contract = self.decisions["BS-CUSTOMER-20260806-01"]["contract"]
        self.assertEqual("BINARY_MAXIMUM_LOAD_GATE", contract["load_model"])
        self.assertEqual("STRENGTH_X_10_WEIGHT_POINT", contract["maximum_load_formula"])
        self.assertEqual(["WITHIN_LIMIT", "OVERWEIGHT"], contract["load_states"])
        self.assertEqual("NO_LOAD_BONUS_OR_PENALTY", contract["within_limit_effect"])
        self.assertEqual("ASSIGNMENT_BLOCKED", contract["overweight_effect"])
        self.assertFalse(contract["comfortable_load_is_current"])
        self.assertFalse(contract["four_state_balance_is_current"])
        self.assertFalse(contract["escalating_overload_penalty_exists"])
        self.assertFalse(contract["constitution_or_dexterity_changes_maximum_load"])

    def test_success_forecast_keeps_enhancement_dominant(self) -> None:
        contract = self.decisions["BS-CUSTOMER-20260806-01"]["contract"]
        self.assertEqual(
            "ENHANCEMENT_DOMINANT_AUXILIARY_MODIFIERS",
            contract["success_forecast_model"],
        )
        self.assertEqual("CLAMP_100_MINUS_RISK_X_10_TO_5_90", contract["risk_base_formula"])
        self.assertEqual(1, contract["enhancement_bonus_pp_per_level"])
        self.assertEqual(5, contract["relevant_stat_meets_risk_bonus_pp"])
        self.assertEqual({"0": -10, "1": 0, "2": 5, "3": 10}, contract["proficiency_bonus_pp"])
        self.assertEqual("BINARY_REQUIREMENT_WHEN_EVENT_REQUIRES", contract["special_function_requirement_model"])
        self.assertEqual("CLAMP_5_TO_95_PERCENT", contract["final_success_clamp"])
        self.assertEqual("NEAREST_10_PERCENT", contract["player_display_rounding"])
        self.assertFalse(contract["raw_item_attack_defense_handling_artistry_feed_general_forecast"])
        self.assertEqual("BLOCKED", contract["product_implementation"])

    def test_authority_documents_record_simplification(self) -> None:
        for path in (CANON, SPEC, PLAN):
            self.assertTrue(path.exists(), f"missing authority document: {path}")
        canon = CANON.read_text(encoding="utf-8")
        for token in (
            "BS-CUSTOMER-20260806-01",
            "근력 × 10",
            "WITHIN_LIMIT / OVERWEIGHT",
            "중량 초과 시 배정 불가",
            "강화 레벨 +1당 +1%p",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)

        current = CURRENT.read_text(encoding="utf-8")
        bible = BIBLE.read_text(encoding="utf-8")
        self.assertIn("BS-CUSTOMER-20260806-01", current)
        self.assertIn("R2_BATCH_005_CLOSED_10_OF_10", current)
        self.assertIn("강화가 주효과", bible)
        self.assertIn("중량 초과 시 배정 불가", bible)

    def test_previous_customer_and_mobile_contracts_are_refined(self) -> None:
        customer = CUSTOMER_CANON.read_text(encoding="utf-8")
        ux = UX_CANON.read_text(encoding="utf-8")
        self.assertIn("REFINED_BY_BS-CUSTOMER-20260806-01", customer)
        self.assertIn("COMFORTABLE_LOAD / BALANCE_STATE", customer)
        self.assertIn("HISTORICAL_SUPERSEDED", customer)
        self.assertIn("LOAD_STATUS", ux)
        self.assertIn("WITHIN_LIMIT / OVERWEIGHT", ux)
        self.assertIn("중량 초과 시 배정 불가", ux)


if __name__ == "__main__":
    unittest.main()
