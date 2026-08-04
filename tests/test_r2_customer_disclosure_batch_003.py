from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
THREE_AFFIX_CANON = ROOT / "docs/planning/BLACKSMITH_R2_THREE_AFFIX_SLOT_ARCHITECTURE_CANON_2026.md"
CHRONICLE_DETAIL_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CHRONICLE_AFFIX_DETAIL_INTERACTION_CANON_2026.md"
CLOSURE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CHECKPOINT_003_POSTMERGE_CLOSURE_2026.md"
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


class R2Batch003Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_batch_decisions_are_closed_in_pr103(self) -> None:
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
            self.assertEqual("USER_APPROVED_MERGED_PR103", self.decisions[decision_id]["status"])

        historical = self.decisions["BS-CRAFT-20260804-03"]
        self.assertEqual("SUPERSEDED_IN_STRUCTURE_BY_BS-CRAFT-20260804-04", historical["status"])
        self.assertEqual(103, historical["merged_in_pr"])
        self.assertFalse(historical["contract"]["auxiliary_material_slot_is_current"])

    def test_three_independent_affix_slots(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-06"]
        contract = decision["contract"]
        self.assertEqual("BS-UX-20260804-01", decision["refined_by"])
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
            "[GRADE_AFFIX] CATALYST_AFFIX BASE_ITEM_NAME - CHRONICLE_AFFIX",
            contract["name_composition"],
        )

    def test_grade_catalyst_and_chronicle_ownership(self) -> None:
        contract = self.decisions["BS-CRAFT-20260804-06"]["contract"]
        grade = contract["grade_affix"]
        catalyst = contract["catalyst_affix"]
        chronicle = contract["chronicle_affix"]

        self.assertTrue(grade["immutable_for_same_item_uid"])
        self.assertFalse(grade["adds_second_grade_multiplier"])
        self.assertEqual("PROBABILISTIC", catalyst["result_model"])
        self.assertFalse(catalyst["influenced_by_item_chronicle"])
        self.assertEqual("EVENT_DRIVEN", chronicle["result_model"])
        self.assertFalse(chronicle["influenced_by_catalyst"])
        self.assertFalse(chronicle["low_risk_repeat_farming_allowed"])

    def test_chronicle_detail_checkpoint_refinement_is_merged(self) -> None:
        decision = self.decisions["BS-UX-20260804-01"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_MERGED_PR103_CHECKPOINT_REFINEMENT", decision["status"])
        self.assertEqual("BS-CRAFT-20260804-06", decision["refines"])
        self.assertEqual("POST_BATCH_CHECKPOINT_REFINEMENT", decision["batch_role"])
        self.assertEqual(
            "[GRADE_AFFIX] CATALYST_AFFIX BASE_ITEM_NAME - CHRONICLE_AFFIX",
            contract["equipment_name_format"],
        )
        self.assertTrue(contract["empty_catalyst_omitted"])
        self.assertTrue(contract["empty_chronicle_suffix_and_hyphen_omitted"])
        self.assertTrue(contract["current_chronicle_only_in_name"])
        self.assertEqual("TAP_CHRONICLE_SUFFIX", contract["chronicle_affix_interaction"])
        self.assertEqual("CONTEXT_PRESERVING_BOTTOM_SHEET", contract["detail_presentation"])
        self.assertTrue(contract["detail_read_only"])
        self.assertEqual("SIGNIFICANT_RECORDS_ONLY", contract["timeline_scope"])
        self.assertFalse(contract["unresolved_future_spoilers_allowed"])
        self.assertFalse(contract["invented_unrecorded_history_allowed"])
        self.assertFalse(contract["interaction_triggers_gameplay_resolution_or_reward"])
        self.assertFalse(contract["color_only_interaction_cue_allowed"])
        self.assertTrue(contract["preserve_item_detail_context_on_close"])

    def test_checkpoint_003_closure(self) -> None:
        checkpoint = self.registry["checkpoint"]
        batch = self.registry["active_batch"]

        self.assertEqual("R2_CHECKPOINT_003", checkpoint["id"])
        self.assertEqual(103, checkpoint["merge_pr"])
        self.assertEqual("SQUASH", checkpoint["merge_method"])
        self.assertEqual("228f409c3043bf1618172985a288dc656b0f05b9", checkpoint["exact_head"])
        self.assertEqual("674ee21013cb5d41f89a1a3f3b10ecfc31238295", checkpoint["merge_sha"])
        self.assertEqual(104, checkpoint["postmerge_closure_pr"])
        self.assertEqual("P0_0_P1_0", checkpoint["adversarial_audit"])
        self.assertEqual("PASS", checkpoint["workflows"]["python_full_contracts"])
        self.assertEqual("PASS", checkpoint["workflows"]["godot_4_7_1_headless"])
        self.assertFalse(checkpoint["product_paths_changed"])
        self.assertEqual("NOT_RUN", checkpoint["focused_test_standalone"])

        self.assertEqual("R2_BATCH_003", batch["id"])
        self.assertEqual(10, batch["approved_decisions"])
        self.assertEqual("10/10", batch["counter"])
        self.assertEqual("CLOSED_MERGED_PR103", batch["state"])
        self.assertEqual(["BS-UX-20260804-01"], batch["checkpoint_refinements"])
        self.assertEqual("EXACT_HEAD_VALIDATED_AND_SQUASH_MERGED", batch["current_validation"])
        self.assertEqual(103, batch["merge_pr"])
        self.assertEqual(104, batch["postmerge_closure_pr"])
        self.assertEqual("0/10", self.registry["next_approval_counter"])
        self.assertEqual("BLOCKED", self.registry["product_implementation"])

    def test_adversarial_guards(self) -> None:
        guards = set(self.registry["adversarial_guards"])
        for guard in (
            "EXACTLY_THREE_AFFIX_SLOTS_GRADE_CATALYST_CHRONICLE",
            "GRADE_AFFIX_MUST_NOT_DOUBLE_COUNT_GRADE_MULTIPLIERS",
            "CATALYST_AFFIX_MUST_NOT_BE_INFLUENCED_BY_CHRONICLE",
            "CHRONICLE_AFFIX_MUST_NOT_BE_CREATED_OR_CHANGED_BY_CATALYST",
            "EQUIPMENT_NAME_MUST_COMPOSE_GRADE_CATALYST_BASE_AND_CHRONICLE_IN_APPROVED_ORDER",
            "EMPTY_CHRONICLE_MUST_OMIT_SUFFIX_AND_HYPHEN",
            "CURRENT_CHRONICLE_ONLY_IN_EQUIPMENT_NAME",
            "CHRONICLE_AFFIX_SUFFIX_MUST_OPEN_UID_BACKED_DETAIL",
            "CHRONICLE_DETAIL_MUST_USE_SIGNIFICANT_RECORDS_ONLY",
            "CHRONICLE_DETAIL_MUST_PRESERVE_EVOLUTION_CHAIN",
            "CHRONICLE_DETAIL_MUST_BE_READ_ONLY",
            "CHRONICLE_DETAIL_MUST_PRESERVE_ITEM_CONTEXT",
            "CHRONICLE_DETAIL_MUST_NOT_USE_COLOR_ONLY_CUE",
            "CHRONICLE_DETAIL_MUST_NOT_REVEAL_UNRESOLVED_FUTURE_RESULTS",
            "UNRECORDED_CHRONICLE_HISTORY_PROHIBITED",
        ):
            self.assertIn(guard, guards)

    def test_canon_documents_preserve_closure_and_interaction(self) -> None:
        three_affix = THREE_AFFIX_CANON.read_text(encoding="utf-8")
        chronicle_detail = CHRONICLE_DETAIL_CANON.read_text(encoding="utf-8")
        closure = CLOSURE_CANON.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")

        for token in (
            "[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어",
            "[명품] 예리한 강철 장검 - 투기장의 승자",
            "하단 상세 패널",
            "BS-UX-20260804-01",
        ):
            self.assertIn(token, three_affix)

        for token in (
            "TAP_CHRONICLE_SUFFIX",
            "BOTTOM_SHEET",
            "주요 연대기 타임라인",
            "수식어 진화 계보",
            "ITEM_UID",
            "읽기 전용",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, chronicle_detail)

        for token in (
            "R2_BATCH_003 / 10_OF_10 / CLOSED_MERGED_PR103",
            "R2_CHECKPOINT_003 / MAIN_CANON",
            "NEXT_GRILL_ME_COUNTER_0_OF_10",
            "post-merge closure PR: `#104`",
        ):
            self.assertIn(token, closure)

        for token in (
            "R2_CHECKPOINT_003_CANON",
            "NEXT_GRILL_ME_COUNTER_0_OF_10",
            "PR #103 squash merge",
            "post-merge closure PR: `#104`",
            "[명품] 예리한 강철 장검 - 투기장의 승자",
        ):
            self.assertIn(token, root)

        for token in (
            "세계일정 진행 계약",
            "자동 단조",
            "제작 모델 7건",
            "통합 6건",
            "enhancement_balance.json",
            "enhancement_milestones.json",
            "다음 승인 카운터: `0/10`",
            "연대기 수식어를 누르면 그 이름의 근거가 된 작품 기록을 확인할 수 있다",
        ):
            self.assertIn(token, active)


if __name__ == "__main__":
    unittest.main()
