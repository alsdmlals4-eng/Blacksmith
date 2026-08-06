from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md"


class ArtistryGenerationGrowthEconomyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_batch_005_contains_ten_approved_decisions(self) -> None:
        self.assertEqual("R2_BATCH_006_APPROVED_MAIN_CANON", self.registry["stage_status"])
        self.assertEqual("10/10", self.registry["next_approval_counter"])
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
    def test_artistry_sources_and_context_values_are_separated(self) -> None:
        contract = self.decisions["BS-CRAFT-20260805-02"]["contract"]
        self.assertEqual("ARTISTRY", contract["persisted_stat"])
        self.assertEqual(
            [
                "BASE_ITEM_DESIGN_AESTHETIC_TENDENCY",
                "MATERIAL_VISUAL_PROCESSING_FIT",
                "DIRECT_FORGING_AESTHETIC_RESULT",
            ],
            contract["initial_sources"],
        )
        self.assertEqual(
            [
                "ARTISTIC_FINISH",
                "ARTISTRY_OWNED_CATALYST_EFFECT",
                "APPROVED_FINISHING_OR_DECORATION_CONTENT",
                "MEANINGFUL_ARTISTIC_REWORK",
            ],
            contract["allowed_post_craft_growth_sources"],
        )
        self.assertEqual("CONTEXT_DERIVED_NOT_PERSISTED", contract["artistry_value_storage"])
        self.assertEqual("CONTEXT_DERIVED_NOT_PERSISTED", contract["customer_artistry_fit_storage"])

    def test_automatic_and_repeat_growth_sources_are_forbidden(self) -> None:
        contract = self.decisions["BS-CRAFT-20260805-02"]["contract"]
        self.assertEqual(
            [
                "GENERAL_ENHANCEMENT_LEVEL",
                "SALE",
                "GIFT",
                "EXHIBITION_COUNT",
                "APPRAISAL_COUNT",
                "OWNERSHIP_TRANSFER",
                "FAME",
                "CHRONICLE_EVENT",
                "LOW_COST_REPEAT_ACTION",
            ],
            contract["forbidden_automatic_growth_sources"],
        )
        for key in (
            "repair_loop_can_create_net_artistry",
            "damage_loop_can_create_net_artistry",
            "sale_loop_can_create_net_artistry",
            "exhibition_loop_can_create_net_artistry",
            "appraisal_loop_can_create_net_artistry",
            "gift_loop_can_create_net_artistry",
            "low_cost_repeat_can_create_net_artistry",
        ):
            self.assertFalse(contract[key])

    def test_valuation_is_additive_once_and_diminishing(self) -> None:
        contract = self.decisions["BS-CRAFT-20260805-02"]["contract"]
        self.assertEqual(
            "ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE",
            contract["valuation_model"],
        )
        self.assertEqual(
            [
                "FUNCTIONAL_VALUE",
                "CRAFTING_GRADE_VALUE",
                "DIMINISHING_ARTISTRY_VALUE",
                "CATALYST_AFFIX_VALUE",
                "CHRONICLE_VALUE",
                "CUSTOMER_OR_MARKET_DEMAND_ADJUSTMENT",
            ],
            contract["valuation_components"],
        )
        self.assertTrue(contract["artistry_value_monotonic"])
        self.assertTrue(contract["artistry_marginal_value_diminishes_by_band"])
        self.assertTrue(contract["piecewise_data_table_preferred"])
        self.assertFalse(contract["multiplicative_total_value_stack_allowed"])
        self.assertFalse(contract["same_source_double_count_allowed"])

    def test_customer_interest_roles_and_disclosure(self) -> None:
        contract = self.decisions["BS-CRAFT-20260805-02"]["contract"]
        self.assertEqual(["IGNORE", "SECONDARY", "PRIMARY", "REQUIREMENT"], contract["customer_interest_roles"])
        self.assertFalse(contract["uninterested_customer_penalizes_excess_artistry"])
        self.assertTrue(contract["uninterested_customer_may_cap_willingness_to_pay"])
        self.assertEqual(
            ["DIRECTION", "EXPECTED_RANGE_FOR_PROBABILISTIC_ACTION", "CUSTOMER_IMPORTANCE", "REQUIREMENT_STATUS"],
            contract["player_disclosure"],
        )

    def test_exact_values_and_product_implementation_remain_blocked(self) -> None:
        contract = self.decisions["BS-CRAFT-20260805-02"]["contract"]
        self.assertEqual("BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED", contract["exact_values"])
        self.assertEqual("BLOCKED", self.registry["product_implementation"])
        text = CANON.read_text(encoding="utf-8")
        for token in (
            "BS-CRAFT-20260805-02",
            "ARTISTIC_FINISH",
            "IGNORE / SECONDARY / PRIMARY / REQUIREMENT",
            "구간별 한계 가치",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
