from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md"
SPEC = ROOT / "docs/superpowers/specs/2026-08-05-mobile-customer-card-progressive-disclosure-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-05-mobile-customer-card-progressive-disclosure.md"
GAME_BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


class MobileCustomerCardProgressiveDisclosureContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_batch_005_contains_ten_approved_decisions(self) -> None:
        self.assertEqual("R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING", self.registry["stage_status"])
        self.assertEqual("0/10", self.registry["next_approval_counter"])
        active = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_005", active["id"])
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
    def test_three_layer_mobile_card_is_canonical(self) -> None:
        self.assertIn("BS-UX-20260805-01", self.decisions)
        decision = self.decisions["BS-UX-20260805-01"]
        self.assertEqual("USER_APPROVED_R2_BATCH_005_3_OF_10_MERGED_PR109_MAIN_CANON", decision["status"])
        self.assertIn("BS-CUSTOMER-20260805-01", decision.get("refines", []))
        contract = decision["contract"]
        self.assertEqual("THREE_LAYER_PROGRESSIVE_DISCLOSURE", contract["disclosure_model"])
        self.assertEqual(
            ["DEFAULT_CUSTOMER_CARD", "POST_EQUIPMENT_DECISION_LAYER", "DETAIL_VIEW"],
            contract["layers"],
        )

    def test_default_and_post_selection_layers_prioritize_decisions(self) -> None:
        contract = self.decisions["BS-UX-20260805-01"]["contract"]
        self.assertEqual(
            [
                "CUSTOMER_IDENTITY_AND_ROLE",
                "CURRENT_SCHEDULE_SUMMARY",
                "FOUR_BASE_STATS",
                "RELEVANT_PRIMARY_AND_SECONDARY_PROFICIENCIES_ONLY",
                "MAGIC_APTITUDE_ONLY_WHEN_RELEVANT",
            ],
            contract["default_layer"],
        )
        self.assertEqual(
            ["LOAD_STATUS", "SUCCESS_FORECAST", "KEY_REASON_CHIPS", "SPECIAL_FUNCTION_RISK_WHEN_RELEVANT"],
            contract["post_equipment_layer"],
        )
        self.assertEqual(2, contract["reason_chip_minimum"])
        self.assertEqual(4, contract["reason_chip_maximum"])
        self.assertTrue(contract["primary_assignment_action_always_visible"])

    def test_detail_layer_preserves_explainability_without_default_matrix(self) -> None:
        contract = self.decisions["BS-UX-20260805-01"]["contract"]
        self.assertEqual(
            [
                "ALL_RELEVANT_PROFICIENCIES",
                "TOTAL_WEIGHT_AND_MAXIMUM_LOAD",
                "SPECIAL_FUNCTION_REQUIREMENTS",
                "APPLICABLE_ITEM_STAT_BREAKDOWN",
            ],
            contract["detail_layer"],
        )
        self.assertFalse(contract["full_proficiency_matrix_visible_by_default"])
        self.assertFalse(contract["result_only_opaque_fit_score_allowed"])
        self.assertEqual("ONE_DETAIL_DISCLOSURE_ENTRY_PER_CARD", contract["detail_entry_model"])

    def test_mobile_accessibility_and_pc_adaptation_are_explicit(self) -> None:
        contract = self.decisions["BS-UX-20260805-01"]["contract"]
        self.assertEqual(48, contract["minimum_touch_target_dp"])
        self.assertFalse(contract["color_only_state_communication_allowed"])
        self.assertFalse(contract["long_press_only_critical_information_allowed"])
        self.assertFalse(contract["hover_only_critical_information_allowed"])
        self.assertTrue(contract["text_label_or_icon_plus_text_required_for_states"])
        self.assertEqual("SAME_INFORMATION_HIERARCHY_POINTER_ENHANCEMENTS_OPTIONAL", contract["pc_adaptation"])
        self.assertEqual("BLOCKED", contract["product_implementation"])

    def test_authority_documents_exist_and_record_the_contract(self) -> None:
        for path in (CANON, SPEC, PLAN):
            self.assertTrue(path.is_file(), str(path))
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        bible = GAME_BIBLE.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        for token in (
            "BS-UX-20260805-01",
            "기본 카드 → 장비 선택 후 판단층 → 상세 보기",
            "핵심 원인 2~4개",
            "48dp",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)
        self.assertIn("BS-UX-20260805-01", bible)
        self.assertIn("R2_BATCH_005_7_OF_10", bible)
        self.assertIn("BS-UX-20260805-01", active)
        self.assertIn("현재 승인 카운터: `10/10`", active)


if __name__ == "__main__":
    unittest.main()
