from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
LEGACY_REGISTRY = ROOT / "docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json"
THREE_AFFIX_CANON = ROOT / "docs/planning/BLACKSMITH_R2_THREE_AFFIX_SLOT_ARCHITECTURE_CANON_2026.md"
FOUR_GRADE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_FOUR_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md"
CHRONICLE_DETAIL_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CHRONICLE_AFFIX_DETAIL_INTERACTION_CANON_2026.md"
AUDIT_CANON = ROOT / "docs/planning/BLACKSMITH_CANON_ADVERSARIAL_REVIEW_AND_LEGACY_STATUS_2026-08-04.md"
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
ROADMAP = ROOT / "[기획서]/00_프로젝트_허브/ROADMAP.md"
GATES = ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"


class R2Batch003And004RefinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_batch_003_is_closed_and_batch_004_has_one_approved_decision(self) -> None:
        for decision_id in (
            "BS-CUSTOMER-20260803-02",
            "BS-SCHEDULE-20260804-01",
            "BS-CONTENT-20260804-01",
            "BS-CONTENT-20260804-02",
            "BS-CRAFT-20260804-01",
            "BS-CRAFT-20260804-04",
            "BS-CRAFT-20260804-05",
        ):
            self.assertEqual("USER_APPROVED_MERGED_PR103", self.decisions[decision_id]["status"])

        self.assertEqual(
            "USER_APPROVED_MERGED_PR103_PENDING_REFINEMENT_OF_TIER_LABELS",
            self.decisions["BS-CRAFT-20260804-02"]["status"],
        )
        self.assertEqual(
            "USER_APPROVED_MERGED_PR103_REFINED_BY_BS-CRAFT-20260804-07",
            self.decisions["BS-CRAFT-20260804-06"]["status"],
        )

        historical = self.decisions["BS-CRAFT-20260804-03"]
        self.assertEqual("SUPERSEDED_IN_STRUCTURE_BY_BS-CRAFT-20260804-04", historical["status"])
        self.assertFalse(historical["contract"]["auxiliary_material_slot_is_current"])

        closed = self.registry["closed_batch"]
        self.assertEqual("R2_BATCH_003", closed["id"])
        self.assertEqual(10, closed["approved_decisions"])
        self.assertEqual("10/10", closed["counter"])
        self.assertEqual("CLOSED_MERGED_PR103_AND_CLOSURE_PR104", closed["state"])

        active = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_004", active["id"])
        self.assertEqual(1, active["approved_decisions"])
        self.assertEqual("1/10", active["counter"])
        self.assertEqual(["BS-CRAFT-20260804-07"], active["decisions"])
        self.assertEqual("1/10", self.registry["next_approval_counter"])

    def test_three_independent_affix_slots_remain(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-06"]
        contract = decision["contract"]
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

    def test_precision_structure_has_no_auxiliary_slot(self) -> None:
        contract = self.decisions["BS-CRAFT-20260804-04"]["contract"]
        self.assertFalse(contract["auxiliary_material_slot_exists"])
        self.assertEqual("ONE_INPUT_ONE_RESULT", contract["normal_enhancement_flow"])
        self.assertEqual([10, 20, 30, 40, 50], contract["precision_milestones"])
        self.assertEqual(
            ["PRIMARY_MATERIAL_CONTEXT", "ENHANCEMENT_METHOD", "ONE_CATALYST"],
            contract["precision_inputs"],
        )

    def test_grade_affix_has_current_four_tier_planning_and_historical_runtime_models(self) -> None:
        contract = self.decisions["BS-CRAFT-20260804-06"]["contract"]
        grade = contract["grade_affix"]
        catalyst = contract["catalyst_affix"]
        chronicle = contract["chronicle_affix"]

        self.assertEqual(
            ["CRAFT_NORMAL", "CRAFT_SUPERIOR", "CRAFT_MASTERWORK", "CRAFT_LEGENDARY"],
            grade["current_planning_grade_ids"],
        )
        self.assertEqual(["보통", "우수", "걸작", "전설"], grade["current_korean_labels"])
        self.assertEqual(["STANDARD", "GOOD", "PERFECT"], grade["historical_implemented_grade_ids"])
        self.assertEqual(
            "REFERENCE_IMPLEMENTATION_HISTORICAL_IMPLEMENTED_VALUE",
            grade["historical_implemented_grade_ids_status"],
        )
        self.assertTrue(grade["immutable_for_same_item_uid"])
        self.assertFalse(grade["adds_second_grade_multiplier"])
        self.assertEqual("PROBABILISTIC", catalyst["result_model"])
        self.assertFalse(catalyst["influenced_by_item_chronicle"])
        self.assertEqual("EVENT_DRIVEN", chronicle["result_model"])
        self.assertFalse(chronicle["influenced_by_catalyst"])
        self.assertFalse(chronicle["low_risk_repeat_farming_allowed"])

    def test_birth_only_legendary_grade_contract(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-07"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_R2_BATCH_004_1_OF_10_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual(4, contract["grade_count"])
        self.assertEqual(
            ["CRAFT_NORMAL", "CRAFT_SUPERIOR", "CRAFT_MASTERWORK", "CRAFT_LEGENDARY"],
            contract["grade_ids"],
        )
        self.assertEqual(["보통", "우수", "걸작", "전설"], contract["korean_labels"])
        self.assertEqual("FIRST_DIRECT_FORGING_COMPLETION_ONLY", contract["determination_timing"])
        self.assertTrue(contract["immutable_for_same_item_uid"])
        self.assertFalse(contract["post_craft_promotion_allowed"])
        self.assertFalse(contract["post_craft_demotion_allowed"])
        self.assertEqual("EXTREMELY_RARE_FIRST_CRAFT_RESULT", contract["legendary_origin"])
        self.assertFalse(
            contract["legendary_can_be_granted_by_reputation_chronicle_appraisal_repair_or_enhancement"]
        )
        for key in (
            "legendary_guarantees_max_artistry",
            "legendary_guarantees_catalyst_affix",
            "legendary_guarantees_chronicle_affix",
            "legendary_guarantees_universal_best_performance",
        ):
            self.assertFalse(contract[key])
        self.assertEqual("BASELINE_TEST_PRESET", contract["exact_probabilities_and_multipliers"])
        self.assertEqual(
            "REFERENCE_IMPLEMENTATION_NOT_CURRENT_PRODUCT_IMPLEMENTATION",
            contract["historical_three_grade_implementation_status"],
        )

    def test_chronicle_detail_contract_is_unchanged(self) -> None:
        decision = self.decisions["BS-UX-20260804-01"]
        contract = decision["contract"]
        self.assertEqual("USER_APPROVED_MERGED_PR103_CHECKPOINT_REFINEMENT", decision["status"])
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

    def test_checkpoint_merge_evidence_includes_canon_audit(self) -> None:
        evidence = self.registry["immutable_merge_evidence"]["checkpoint_003"]
        self.assertEqual("228f409c3043bf1618172985a288dc656b0f05b9", evidence["planning_exact_head"])
        self.assertEqual("674ee21013cb5d41f89a1a3f3b10ecfc31238295", evidence["planning_merge_sha"])
        self.assertEqual("d09ed504e9ab66384e4a7f675731674c1f7f5871", evidence["closure_exact_head"])
        self.assertEqual("d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9", evidence["closure_merge_sha"])
        self.assertEqual("99a4c0bba23eb922dc7c803407cce4e4ca078e4e", evidence["canon_audit_exact_head"])
        self.assertEqual("95f8fa33a645914578451af325afcaa32732c426", evidence["canon_audit_merge_sha"])
        self.assertEqual("PASS", evidence["github_readback"])
        self.assertEqual("PASS", evidence["sheet_readback"])

    def test_adversarial_guards_and_pr81_boundary(self) -> None:
        guards = set(self.registry["adversarial_guards"])
        for guard in (
            "EXACTLY_THREE_AFFIX_SLOTS_GRADE_CATALYST_CHRONICLE",
            "GENERAL_AFFIX_A_B_STRUCTURE_MUST_NOT_RETURN",
            "AUXILIARY_MATERIAL_SLOT_MUST_NOT_EXIST",
            "CRAFTING_GRADE_MUST_HAVE_FOUR_CURRENT_PLANNING_TIERS",
            "GRADE_AFFIX_MUST_NOT_DOUBLE_COUNT_GRADE_MULTIPLIERS",
            "LEGENDARY_GRADE_MUST_BE_BIRTH_RESULT_ONLY",
            "LEGENDARY_GRADE_MUST_NOT_BE_GRANTED_BY_POST_CRAFT_HISTORY_OR_REPUTATION",
            "LEGENDARY_GRADE_MUST_NOT_GUARANTEE_ARTISTRY_CATALYST_CHRONICLE_OR_UNIVERSAL_BEST",
            "HISTORICAL_THREE_GRADE_IMPLEMENTATION_MUST_NOT_BE_CURRENT_FOUR_GRADE_IMPLEMENTATION_PASS",
            "CHRONICLE_AFFIX_SUFFIX_MUST_OPEN_UID_BACKED_DETAIL",
            "LEGACY_DOCUMENTS_MUST_HAVE_EXPLICIT_STATUS",
            "PR81_MUST_NOT_BE_MERGED_AS_UNIT",
            "REGISTRY_MUST_NOT_PREDICT_ITS_OWN_FUTURE_MERGE_SHA",
        ):
            self.assertIn(guard, guards)

        pr81 = self.registry["legacy_reference_pull_request"]
        self.assertEqual(81, pr81["number"])
        self.assertEqual("REFERENCE_ONLY_DO_NOT_MERGE_AS_UNIT", pr81["status"])
        self.assertEqual("REJECTED", pr81["whole_pr_merge"])
        self.assertEqual("HOLD", pr81["selective_promotion"])

    def test_legacy_files_have_direct_status_markers(self) -> None:
        legacy = json.loads(LEGACY_REGISTRY.read_text(encoding="utf-8"))
        for item in legacy["documents"]:
            path = ROOT / item["path"]
            self.assertTrue(path.exists(), item["path"])
            text = path.read_text(encoding="utf-8")
            expected_markers = {
                "SUPERSEDED": "[대체됨]",
                "PARTIALLY_SUPERSEDED": "[부분 대체됨]",
                "HISTORICAL_EVIDENCE": "[역사 증거]",
            }
            marker = expected_markers.get(item["status"])
            if marker:
                self.assertIn(marker, text, item["path"])

    def test_current_documents_preserve_core_fun_and_current_structure(self) -> None:
        three_affix = THREE_AFFIX_CANON.read_text(encoding="utf-8")
        four_grade = FOUR_GRADE_CANON.read_text(encoding="utf-8")
        chronicle_detail = CHRONICLE_DETAIL_CANON.read_text(encoding="utf-8")
        audit = AUDIT_CANON.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        gates = GATES.read_text(encoding="utf-8")

        for token in (
            "[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어",
            "[걸작] 예리한 강철 장검 - 투기장의 승자",
            "BS-CRAFT-20260804-07",
            "BS-UX-20260804-01",
        ):
            self.assertIn(token, three_affix)

        for token in (
            "[보통] → [우수] → [걸작] → [전설]",
            "EXTREMELY_RARE_FIRST_CRAFT_RESULT" if "EXTREMELY_RARE_FIRST_CRAFT_RESULT" in four_grade else "극희귀",
            "제작 후 `걸작 → 전설` 승격 금지",
        ):
            self.assertIn(token, four_grade)

        for token in (
            "TAP_CHRONICLE_SUFFIX",
            "BOTTOM_SHEET",
            "수식어 진화 계보",
            "읽기 전용",
        ):
            self.assertIn(token, chronicle_detail)

        self.assertIn("CORE_FUN_DIRECTION: VALID", audit)
        self.assertIn("P0: 0", audit)
        self.assertIn("BS-OPS-20260804-02", root)
        self.assertIn("BS-CRAFT-20260804-07", root)
        self.assertIn("PR #81 전체 병합 단위는 `[폐기]`", root)
        self.assertIn("GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX", active)
        self.assertIn("현재 승인 카운터: `1/10`", active)
        self.assertIn("일반 수식어 A·B 재도입 금지", roadmap)
        self.assertIn("Three Affix Gate", gates)
        self.assertIn("제품 구현: `BLOCKED`", root)


if __name__ == "__main__":
    unittest.main()
