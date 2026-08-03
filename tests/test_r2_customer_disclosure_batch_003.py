from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
PRECISION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md"
CATALYST_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CATALYST_AFFIX_SEED_EVOLUTION_AND_MUTATION_CANON_2026.md"
THREE_AFFIX_CANON = ROOT / "docs/planning/BLACKSMITH_R2_THREE_AFFIX_SLOT_ARCHITECTURE_CANON_2026.md"
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


class R2Batch003Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_prior_batch_decisions_remain_registered(self) -> None:
        for decision_id in (
            "BS-CUSTOMER-20260803-02",
            "BS-SCHEDULE-20260804-01",
            "BS-CONTENT-20260804-01",
            "BS-CONTENT-20260804-02",
            "BS-CRAFT-20260804-01",
            "BS-CRAFT-20260804-02",
            "BS-CRAFT-20260804-04",
            "BS-CRAFT-20260804-05",
            "BS-CRAFT-20260804-06",
        ):
            self.assertEqual("USER_APPROVED_PENDING_MERGE", self.decisions[decision_id]["status"])

    def test_previous_material_structure_is_superseded(self) -> None:
        previous = self.decisions["BS-CRAFT-20260804-03"]
        self.assertEqual("SUPERSEDED_IN_STRUCTURE_BY_BS-CRAFT-20260804-04", previous["status"])
        self.assertEqual("HISTORICAL_DESIGN_EXPLORATION_ONLY", previous["retained_role"])
        self.assertFalse(previous["contract"]["auxiliary_material_slot_is_current"])

    def test_precision_role_ownership(self) -> None:
        contract = self.decisions["BS-CRAFT-20260804-04"]["contract"]
        self.assertFalse(contract["auxiliary_material_slot_exists"])
        self.assertEqual("ONE_INPUT_ONE_RESULT", contract["normal_enhancement_flow"])
        self.assertEqual([10, 20, 30, 40, 50], contract["precision_milestones"])
        self.assertEqual("FIXED_GRADE_AFFIX", contract["role_ownership"]["CRAFTING_GRADE"])
        self.assertEqual(
            "CATALYST_AFFIX_SEED_LINEAGE_AND_MUTATION_PROBABILITY",
            contract["role_ownership"]["CATALYST"],
        )
        self.assertEqual(
            "CHRONICLE_AFFIX_GENERATION_AND_EVOLUTION",
            contract["role_ownership"]["ITEM_CHRONICLE"],
        )
        self.assertTrue(contract["grade_affix_assigned_at_first_completion"])
        self.assertTrue(contract["catalyst_affix_empty_at_first_completion"])
        self.assertTrue(contract["chronicle_affix_empty_at_first_completion"])
        self.assertTrue(contract["precision_result_can_change_only_catalyst_affix"])

    def test_catalyst_affix_is_single_and_probabilistic(self) -> None:
        contract = self.decisions["BS-CRAFT-20260804-05"]["contract"]
        self.assertEqual("CATALYST_AFFIX", contract["owned_affix_slot"])
        self.assertFalse(contract["previous_general_affix_a_b_structure_current"])
        self.assertEqual(
            ["EMPTY", "SEED", "DEVELOPED", "EVOLVED", "MASTERED"],
            contract["affix_lifecycle"],
        )
        self.assertEqual("PROBABILISTIC_NOT_DETERMINISTIC", contract["catalyst_result_model"])
        self.assertFalse(contract["item_chronicle_influences_catalyst_affix"])
        self.assertEqual(1, contract["catalyst_input_slots_per_precision_attempt"])
        self.assertFalse(contract["unrelated_random_replacement_allowed"])
        self.assertTrue(contract["failed_precision_preserves_existing_affix_and_lineage"])
        self.assertFalse(contract["same_milestone_infinite_reroll_allowed"])

    def test_exactly_three_independent_affix_slots(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-06"]
        contract = decision["contract"]
        self.assertEqual("BS-CRAFT-20260804-05", decision["refines"])
        self.assertEqual(3, contract["affix_slot_count"])
        self.assertEqual(
            ["GRADE_AFFIX", "CATALYST_AFFIX", "CHRONICLE_AFFIX"],
            contract["affix_slots"],
        )
        self.assertFalse(contract["previous_general_affix_slots_current"])
        self.assertEqual(
            {"grade_affix": "ASSIGNED", "catalyst_affix": "EMPTY", "chronicle_affix": "EMPTY"},
            contract["first_completion_result"],
        )
        self.assertFalse(contract["cross_slot_overwrite_allowed"])
        self.assertEqual("THREE_SEPARATE_UID_FIELDS", contract["storage"])
        self.assertEqual(
            "SEPARATE_LABELED_ROWS_NOT_ONE_LONG_PREFIX_STRING",
            contract["mobile_display"],
        )
        self.assertFalse(contract["artistry_visual_tier_equals_grade_affix"])

    def test_grade_affix_is_fixed_without_double_counting(self) -> None:
        grade = self.decisions["BS-CRAFT-20260804-06"]["contract"]["grade_affix"]
        self.assertEqual("CRAFTING_GRADE", grade["source"])
        self.assertEqual("FIRST_CRAFT_COMPLETION", grade["creation_timing"])
        self.assertEqual(["STANDARD", "GOOD", "PERFECT"], grade["baseline_grade_ids"])
        self.assertTrue(grade["always_present_after_craft"])
        self.assertTrue(grade["immutable_for_same_item_uid"])
        self.assertFalse(grade["adds_second_grade_multiplier"])
        self.assertEqual(["NONE"], grade["changed_by"])

    def test_catalyst_and_chronicle_affixes_do_not_cross_influence(self) -> None:
        contract = self.decisions["BS-CRAFT-20260804-06"]["contract"]
        catalyst = contract["catalyst_affix"]
        chronicle = contract["chronicle_affix"]
        self.assertEqual("CURRENT_AND_CUMULATIVE_CATALYST_HISTORY", catalyst["source"])
        self.assertEqual("PROBABILISTIC", catalyst["result_model"])
        self.assertFalse(catalyst["influenced_by_item_chronicle"])
        self.assertFalse(catalyst["influenced_by_crafting_grade"])
        self.assertEqual("SIGNIFICANT_ITEM_CHRONICLE", chronicle["source"])
        self.assertEqual("EVENT_DRIVEN", chronicle["result_model"])
        self.assertFalse(chronicle["influenced_by_catalyst"])
        self.assertFalse(chronicle["influenced_by_crafting_grade"])
        self.assertFalse(chronicle["low_risk_repeat_farming_allowed"])

    def test_adversarial_guards(self) -> None:
        guards = set(self.registry["adversarial_guards"])
        for guard in (
            "EXACTLY_THREE_AFFIX_SLOTS_GRADE_CATALYST_CHRONICLE",
            "GENERAL_AFFIX_A_B_STRUCTURE_MUST_NOT_RETURN",
            "GRADE_AFFIX_MUST_BE_IMMUTABLE_FOR_SAME_UID",
            "GRADE_AFFIX_MUST_NOT_DOUBLE_COUNT_GRADE_MULTIPLIERS",
            "CATALYST_AFFIX_MUST_NOT_BE_INFLUENCED_BY_CHRONICLE",
            "CHRONICLE_AFFIX_MUST_NOT_BE_CREATED_OR_CHANGED_BY_CATALYST",
            "LOW_RISK_REPEAT_CHRONICLE_FARMING_PROHIBITED",
            "CROSS_AFFIX_SLOT_OVERWRITE_PROHIBITED",
            "ARTISTRY_VISUAL_TIER_MUST_NOT_EQUAL_GRADE_AFFIX",
            "THREE_AFFIXES_MUST_NOT_FORM_ONE_UNREADABLE_MOBILE_NAME_STRING",
        ):
            self.assertIn(guard, guards)

    def test_batch_counter_and_checkpoint_gate(self) -> None:
        batch = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_003", batch["id"])
        self.assertEqual(10, batch["approved_decisions"])
        self.assertEqual("10/10", batch["counter"])
        self.assertEqual("APPROVED_PENDING_MERGE", batch["state"])
        self.assertEqual("BS-CRAFT-20260804-06", batch["decisions"][-1])
        self.assertEqual(103, batch["draft_pr"])
        self.assertEqual("PENDING_FOR_CURRENT_HEAD", batch["current_validation"])
        self.assertEqual(
            "BATCH_COMPLETE_PENDING_EXACT_HEAD_VALIDATION_AND_USER_REVIEW",
            batch["checkpoint_readiness"],
        )
        self.assertFalse(batch["product_paths_changed"])
        self.assertEqual("BLOCKED", self.registry["product_implementation"])

    def test_canon_documents_preserve_contract(self) -> None:
        precision = PRECISION_CANON.read_text(encoding="utf-8")
        catalyst = CATALYST_CANON.read_text(encoding="utf-8")
        three_affix = THREE_AFFIX_CANON.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")

        for token in (
            "등급 수식어 1개 생성",
            "촉매 수식어 EMPTY",
            "연대기 수식어 EMPTY",
            "정밀강화는 촉매 수식어만",
        ):
            self.assertIn(token, precision)

        for token in (
            "촉매 수식어 / CATALYST_AFFIX",
            "과거 `일반 수식어 A·B` 표현",
            "작품 연대기는 촉매 수식어",
            "제품 구현은 계속 `BLOCKED`",
        ):
            self.assertIn(token, catalyst)

        for token in (
            "BS-CRAFT-20260804-06",
            "GRADE_AFFIX",
            "CATALYST_AFFIX",
            "CHRONICLE_AFFIX",
            "등급 수식어 자체가",
            "연대기가 촉매 수식어를 직접 성장·진화시키는 구조 금지",
            "승인 카운터: `10/10`",
        ):
            self.assertIn(token, three_affix)

        for token in (
            "R2_BATCH_003_10_OF_10",
            "BS-CRAFT-20260804-06",
            "등급 1 + 촉매 1 + 연대기 1",
            "R2_CHECKPOINT_002_CANON",
            "NEXT_GRILL_ME_COUNTER_0_OF_10",
        ):
            self.assertIn(token, root)

        for token in (
            "세계일정 진행 계약",
            "자동 단조",
            "제작 모델 7건",
            "통합 6건",
            "enhancement_balance.json",
            "enhancement_milestones.json",
            "현재 배치: `R2_BATCH_003 / 10_OF_10 / APPROVED_PENDING_MERGE`",
            "정확히 `등급 1 + 촉매 1 + 연대기 1`",
        ):
            self.assertIn(token, active)


if __name__ == "__main__":
    unittest.main()
