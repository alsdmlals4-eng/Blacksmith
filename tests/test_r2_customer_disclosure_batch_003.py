from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
PRECISION_CANON = ROOT / "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md"
AFFIX_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CATALYST_AFFIX_SEED_EVOLUTION_AND_MUTATION_CANON_2026.md"
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
        ):
            self.assertEqual("USER_APPROVED_PENDING_MERGE", self.decisions[decision_id]["status"])

    def test_previous_material_structure_is_superseded(self) -> None:
        previous = self.decisions["BS-CRAFT-20260804-03"]
        self.assertEqual("SUPERSEDED_IN_STRUCTURE_BY_BS-CRAFT-20260804-04", previous["status"])
        self.assertEqual("HISTORICAL_DESIGN_EXPLORATION_ONLY", previous["retained_role"])
        self.assertEqual("BS-CRAFT-20260804-04", previous["superseded_by"])
        self.assertFalse(previous["contract"]["auxiliary_material_slot_is_current"])

    def test_three_role_ownership(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-04"]
        contract = decision["contract"]
        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CRAFT-20260804-03", decision["supersedes"])
        self.assertFalse(contract["auxiliary_material_slot_exists"])
        self.assertEqual(
            {
                "PRIMARY_MATERIAL": "BASE_NAME_BASE_PERFORMANCE_AND_MATERIAL_IDENTITY",
                "ENHANCEMENT_METHOD": "DETAILED_STAT_ADJUSTMENT",
                "CATALYST": "AFFIX_SEED_LINEAGE_EVOLUTION_AND_MUTATION_PROBABILITY",
            },
            contract["role_ownership"],
        )
        self.assertEqual("PRECISION_MILESTONES_ONLY", contract["method_selection_timing"])
        self.assertEqual([10, 20, 30, 40, 50], contract["precision_milestones"])
        self.assertFalse(contract["normal_enhancement_requires_method_selection"])
        self.assertEqual("ONE_INPUT_ONE_RESULT", contract["normal_enhancement_flow"])
        self.assertFalse(contract["catalyst_owns_detailed_stat_direction"])
        self.assertFalse(contract["catalyst_guarantees_success_or_exact_affix"])
        self.assertEqual(1, contract["catalyst_input_slots_per_precision_attempt"])
        self.assertEqual(
            "ORDERED_CUMULATIVE_CATALYST_HISTORY_ACROSS_PRECISION_MILESTONES",
            contract["catalyst_combination_definition"],
        )

    def test_catalyst_affix_lifecycle(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-05"]
        contract = decision["contract"]
        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CRAFT-20260804-04", decision["refines"])
        self.assertEqual(["AFFIX_A", "AFFIX_B"], contract["general_affix_slots"])
        self.assertTrue(contract["chronicle_affix_slot_is_separate"])
        self.assertEqual(
            ["EMPTY", "SEED", "DEVELOPED", "EVOLVED", "MASTERED"],
            contract["affix_lifecycle"],
        )
        self.assertEqual("PROBABILISTIC_NOT_DETERMINISTIC", contract["catalyst_result_model"])
        self.assertIn("LINEAGE_WEIGHT_DISTRIBUTION", contract["catalyst_sets"])
        self.assertIn("REINFORCEMENT_BRANCH_AND_MUTATION_PROBABILITIES", contract["catalyst_sets"])
        self.assertIn("EXACT_AFFIX_NAME", contract["catalyst_does_not_guarantee"])
        self.assertIn("PRECISION_SUCCESS", contract["catalyst_does_not_guarantee"])
        self.assertEqual(1, contract["catalyst_input_slots_per_precision_attempt"])
        self.assertEqual(
            "ORDERED_CUMULATIVE_HISTORY_ACROSS_MILESTONES",
            contract["catalyst_combination"],
        )
        self.assertIn("SAME_LINEAGE_REINFORCEMENT", contract["allowed_transformations"])
        self.assertIn("COMPATIBLE_LINEAGE_BRANCH", contract["allowed_transformations"])
        self.assertIn("CHRONICLE_CONDITION_EVOLUTION", contract["allowed_transformations"])
        self.assertFalse(contract["unrelated_random_replacement_allowed"])
        self.assertTrue(contract["failed_precision_preserves_existing_affix_and_lineage"])
        self.assertFalse(contract["same_milestone_infinite_reroll_allowed"])
        self.assertTrue(contract["all_affix_changes_recorded_in_item_uid_history"])

    def test_current_adversarial_guards(self) -> None:
        guards = set(self.registry["adversarial_guards"])
        for guard in (
            "AUXILIARY_MATERIAL_SLOT_MUST_NOT_EXIST",
            "PRIMARY_MATERIAL_MUST_DEFINE_BASE_NAME_AND_PERFORMANCE_IDENTITY",
            "ENHANCEMENT_METHOD_MUST_OWN_DETAILED_STAT_DIRECTION",
            "CATALYST_MUST_SET_AFFIX_PROBABILITY_NOT_EXACT_RESULT",
            "ONE_CATALYST_INPUT_PER_PRECISION_ATTEMPT",
            "CATALYST_COMBINATION_MUST_MEAN_CUMULATIVE_HISTORY",
            "AFFIX_EVOLUTION_MUST_PRESERVE_LINEAGE_OR_COMPATIBLE_BRANCH",
            "UNRELATED_RANDOM_AFFIX_REPLACEMENT_PROHIBITED",
            "ENHANCEMENT_LEVEL_MUST_NOT_AUTOMATICALLY_COMPLETE_AFFIX",
            "ITEM_CHRONICLE_MUST_INFLUENCE_EVOLUTION_WITHOUT_REPLACING_CATALYST",
            "SAME_MILESTONE_INFINITE_AFFIX_REROLL_PROHIBITED",
            "GENERAL_AFFIXES_AND_CHRONICLE_AFFIX_MUST_REMAIN_DISTINCT",
            "ALL_AFFIX_CHANGES_MUST_BE_RECORDED_IN_ITEM_UID_HISTORY",
        ):
            self.assertIn(guard, guards)

    def test_batch_counter_and_product_gate(self) -> None:
        batch = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_003", batch["id"])
        self.assertEqual(9, batch["approved_decisions"])
        self.assertEqual("9/10", batch["counter"])
        self.assertEqual("APPROVED_PENDING_MERGE", batch["state"])
        self.assertEqual("BS-CRAFT-20260804-05", batch["decisions"][-1])
        self.assertEqual(103, batch["draft_pr"])
        self.assertEqual("PENDING_FOR_CURRENT_HEAD", batch["current_validation"])
        self.assertFalse(batch["product_paths_changed"])
        self.assertEqual("BLOCKED", self.registry["product_implementation"])
        self.assertEqual(
            "DEFINE_CATALYST_AFFIX_LINEAGES_BRANCHES_CHRONICLE_EVOLUTION_CONDITIONS_AND_PROBABILITY_PRESET",
            self.registry["next_activity"],
        )

    def test_canon_documents_preserve_contract(self) -> None:
        precision = PRECISION_CANON.read_text(encoding="utf-8")
        affix = AFFIX_CANON.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")

        for token in (
            "BS-CRAFT-20260804-05",
            "주재료 = 작품 기본 이름·기본 성능·재료 정체성",
            "강화 방식 = 세부 능력치 조정 방향",
            "촉매 = 수식어 씨앗·계보·진화·변형 확률",
            "일반 강화는 한 입력 한 결과",
        ):
            self.assertIn(token, precision)

        for token in (
            "PROBABILISTIC_NOT_DETERMINISTIC",
            "EMPTY",
            "SEED / 씨앗",
            "EVOLVED / 진화",
            "MASTERED / 완성",
            "누적 촉매 이력",
            "기존 계보와 무관한 완전 무작위 변형은 금지",
            "일반 수식어 A·B",
            "제품 구현은 계속 `BLOCKED`",
        ):
            self.assertIn(token, affix)

        for token in (
            "R2_BATCH_003_9_OF_10",
            "BS-CRAFT-20260804-05",
            "초기 촉매가 계보 씨앗",
            "활성 배치: `R2_BATCH_003 / 9_OF_10 / APPROVED_PENDING_MERGE`",
        ):
            self.assertIn(token, root)

        for token in (
            "세계일정 진행 계약",
            "자동 단조",
            "제작 모델 7건",
            "통합 6건",
            "현재 배치: `R2_BATCH_003 / 9_OF_10 / APPROVED_PENDING_MERGE`",
            "촉매가 정확한 수식어가 아닌 후보 계보와 확률을 정한다",
        ):
            self.assertIn(token, active)


if __name__ == "__main__":
    unittest.main()
