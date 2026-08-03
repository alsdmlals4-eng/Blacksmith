from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CUSTOMER_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_DISCLOSURE_MINIMUM_CANON_2026.md"
SCHEDULE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_MULTI_SCHEDULE_DISPLAY_AND_ALERT_CANON_2026.md"
CONTENT_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CONTENT_COMPOSITION_AND_ITEM_LEGACY_CANON_2026.md"
VISITOR_CANON = ROOT / "docs/planning/BLACKSMITH_R2_VISITOR_ARCHETYPES_AND_INITIAL_CONTENT_FAMILIES_CANON_2026.md"
ARTISTRY_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_VALUE_AND_UTILITY_CRAFTING_CANON_2026.md"
ARTISTRY_PRESET_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_MINIMUM_SCALE_PRICE_AFFIX_VISUAL_PRESET_CANON_2026.md"
MATERIAL_CANON = ROOT / "docs/planning/BLACKSMITH_R2_MATERIAL_CATALYST_ROLE_AND_REPRESENTATIVE_COMBINATIONS_CANON_2026.md"
PRECISION_METHOD_CANON = ROOT / "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md"
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


class R2Batch003Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_customer_disclosure_contract(self) -> None:
        decision = self.decisions["BS-CUSTOMER-20260803-02"]
        contract = decision["contract"]
        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CUSTOMER-20260803-01", decision["refines"])
        self.assertEqual("INTEGER_1_TO_10", contract["event_risk_display_scale"])
        self.assertEqual("INTEGER_1_TO_10", contract["customer_stat_display_scale"])
        self.assertFalse(contract["display_decimals"])
        self.assertEqual("APPROXIMATE_PERCENT_ROUNDED_TO_NEAREST_10", contract["success_display"])
        self.assertEqual((5, 95), (contract["success_display_min_percent"], contract["success_display_max_percent"]))
        self.assertTrue(contract["post_equipment_recalculation"])
        self.assertFalse(contract["unknown_variable_notice"])
        self.assertFalse(contract["pre_sale_modifier_breakdown"])

    def test_schedule_content_and_visitor_contracts(self) -> None:
        schedule = self.decisions["BS-SCHEDULE-20260804-01"]["contract"]
        content = self.decisions["BS-CONTENT-20260804-01"]["contract"]
        visitor = self.decisions["BS-CONTENT-20260804-02"]["contract"]
        self.assertEqual("NEAREST_MAJOR_WORLD_SCHEDULE_ONE", schedule["pinned_world_schedule"])
        self.assertEqual(3, schedule["important_news_visible_max"])
        self.assertEqual("GROUPED_END_OF_DAY_SUMMARY", schedule["routine_personal_progress"])
        self.assertFalse(schedule["routine_progress_individual_popup"])
        self.assertEqual("SCHEDULE_LEDGER", schedule["full_history_access"])
        self.assertIn("CUSTOMER_MOTIVATION", content["personal_content_axes"])
        self.assertIn("ITEM_USE_OUTCOME", content["personal_content_axes"])
        self.assertFalse(content["activity_name_and_reward_only_is_distinct_content"])
        self.assertFalse(content["mandatory_long_form_quest"])
        self.assertTrue(content["world_result_requires_customer_and_item_follow_up"])
        self.assertEqual(["GLADIATOR", "ADVENTURER", "SOLDIER", "NOBLE"], visitor["visitor_archetypes"])
        self.assertEqual(5, len(visitor["personal_content_families"]))
        self.assertEqual(4, len(visitor["world_content_families"]))
        self.assertFalse(visitor["noble_is_expensive_combat_reskin"])
        self.assertFalse(visitor["new_customer_stats_added"])

    def test_artistry_contracts(self) -> None:
        artistry = self.decisions["BS-CRAFT-20260804-01"]["contract"]
        preset = self.decisions["BS-CRAFT-20260804-02"]["contract"]
        self.assertEqual("ARTISTRY_ONLY", artistry["new_item_value_stat"])
        self.assertFalse(artistry["new_practicality_stat_added"])
        self.assertFalse(artistry["separate_artistry_upgrade_loop"])
        self.assertTrue(artistry["enhancement_remains_primary_loop"])
        self.assertNotIn("AUXILIARY_MATERIALS", artistry["artistry_sources"])
        self.assertIn("ENHANCEMENT_METHODS", artistry["artistry_sources"])
        self.assertEqual("INTEGER_1_TO_10", preset["artistry_display_scale"])
        self.assertEqual((1, 10), (preset["artistry_min"], preset["artistry_max"]))
        self.assertFalse(preset["display_decimals"])
        self.assertFalse(preset["enhancement_level_alone_raises_artistry"])
        self.assertEqual(["LOW", "MEDIUM", "HIGH"], preset["precision_input_preview_levels"])
        self.assertTrue(preset["preview_text_required"])
        self.assertFalse(preset["color_icon_arrow_only_preview_allowed"])
        self.assertEqual(4, len(preset["utility_affix_families_minimum"]))
        self.assertEqual(3, len(preset["artistry_affix_families_minimum"]))
        self.assertFalse(preset["affix_pools_are_exclusive"])
        self.assertEqual(4, preset["visual_tier_count"])
        self.assertFalse(preset["gold_gems_and_glow_only_progression"])

    def test_previous_material_structure_is_superseded(self) -> None:
        previous = self.decisions["BS-CRAFT-20260804-03"]
        self.assertEqual("SUPERSEDED_IN_STRUCTURE_BY_BS-CRAFT-20260804-04", previous["status"])
        self.assertEqual("HISTORICAL_DESIGN_EXPLORATION_ONLY", previous["retained_role"])
        self.assertEqual("BS-CRAFT-20260804-04", previous["superseded_by"])

    def test_precision_enhancement_method_and_catalyst_structure(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-04"]
        contract = decision["contract"]
        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CRAFT-20260804-03", decision["supersedes"])
        self.assertEqual(
            ["PRIMARY_MATERIAL_CONTEXT", "ENHANCEMENT_METHOD", "CATALYST_OR_ADDITIONAL_MATERIAL"],
            contract["precision_enhancement_inputs"],
        )
        self.assertFalse(contract["auxiliary_material_slot_exists"])
        self.assertEqual("PRECISION_MILESTONES_ONLY", contract["method_selection_timing"])
        self.assertFalse(contract["normal_enhancement_requires_method_selection"])
        self.assertFalse(contract["primary_material_overwrites_base_item_name"])
        self.assertEqual(
            [
                "EDGE_REINFORCEMENT",
                "SHOCK_ABSORPTION",
                "LIGHTWEIGHTING",
                "BALANCE_TUNING",
                "ARTISTIC_FINISH",
                "ENVIRONMENTAL_TREATMENT",
            ],
            contract["enhancement_methods"],
        )
        targets = contract["method_primary_stat_targets"]
        self.assertEqual(["ATTACK", "PRECISION"], targets["EDGE_REINFORCEMENT"])
        self.assertEqual(["DEFENSE", "DURABILITY"], targets["SHOCK_ABSORPTION"])
        self.assertEqual(["WEIGHT_REDUCTION", "HANDLING"], targets["LIGHTWEIGHTING"])
        self.assertEqual(["HANDLING", "STABILITY"], targets["BALANCE_TUNING"])
        self.assertEqual(["ARTISTRY", "VALUE"], targets["ARTISTIC_FINISH"])
        self.assertEqual(["ENVIRONMENT_RESPONSE", "SPECIALIZATION"], targets["ENVIRONMENTAL_TREATMENT"])
        self.assertTrue(contract["method_requires_primary_benefit_and_tradeoff"])
        self.assertTrue(contract["method_applicability_depends_on_item_type"])
        self.assertTrue(contract["successful_result_respects_selected_method_direction"])
        self.assertTrue(contract["exact_gain_and_side_effect_are_variable"])
        self.assertTrue(contract["catalyst_is_secondary_modifier_not_direction_owner"])
        self.assertFalse(contract["catalyst_guarantees_success_or_affix"])
        self.assertFalse(contract["first_completion_has_affix"])
        self.assertTrue(contract["precision_result_can_add_or_upgrade_affix"])
        self.assertEqual("BASELINE_TEST_PRESET", contract["exact_values_costs_risks_and_probabilities"])

    def test_precision_enhancement_adversarial_guards(self) -> None:
        guards = set(self.registry["adversarial_guards"])
        for guard in (
            "AUXILIARY_MATERIAL_SLOT_MUST_NOT_EXIST",
            "ENHANCEMENT_METHOD_MUST_OWN_STAT_DIRECTION",
            "METHOD_SELECTION_MUST_OCCUR_ONLY_AT_PRECISION_MILESTONES",
            "NORMAL_ENHANCEMENT_MUST_REMAIN_ONE_INPUT_ONE_RESULT",
            "PRIMARY_MATERIAL_CONTEXT_MUST_NOT_RENAME_EXISTING_ITEM",
            "METHOD_MUST_HAVE_PRIMARY_BENEFIT_AND_TRADEOFF",
            "METHOD_APPLICABILITY_MUST_RESPECT_ITEM_TYPE",
            "CATALYST_MUST_MODIFY_METHOD_WITHOUT_OWNING_DIRECTION",
            "CATALYST_MUST_NOT_GUARANTEE_SUCCESS_OR_AFFIX",
            "SELECTED_METHOD_DIRECTION_MUST_MATCH_SUCCESSFUL_RESULT",
            "RARE_PRIMARY_MATERIAL_MUST_NOT_BE_UNIVERSAL_BEST",
            "GPT_SCOPE_MUST_REMAIN_DESIGN_CONTENT_AND_ART_FOCUSED",
        ):
            self.assertIn(guard, guards)

    def test_batch_counter_and_product_gate(self) -> None:
        batch = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_003", batch["id"])
        self.assertEqual(8, batch["approved_decisions"])
        self.assertEqual("8/10", batch["counter"])
        self.assertEqual("APPROVED_PENDING_MERGE", batch["state"])
        self.assertEqual([
            "BS-CUSTOMER-20260803-02",
            "BS-SCHEDULE-20260804-01",
            "BS-CONTENT-20260804-01",
            "BS-CONTENT-20260804-02",
            "BS-CRAFT-20260804-01",
            "BS-CRAFT-20260804-02",
            "BS-CRAFT-20260804-03",
            "BS-CRAFT-20260804-04",
        ], batch["decisions"])
        self.assertEqual(103, batch["draft_pr"])
        self.assertEqual("PENDING_FOR_CURRENT_HEAD", batch["current_validation"])
        self.assertFalse(batch["product_paths_changed"])
        self.assertEqual("BLOCKED", self.registry["product_implementation"])
        self.assertEqual(
            "DEFINE_PRECISION_METHOD_STAT_PACKAGES_CATALYST_INTERACTIONS_COSTS_RISKS_AND_VISUAL_FEEDBACK",
            self.registry["next_activity"],
        )

    def test_canon_documents_preserve_prior_and_new_contracts(self) -> None:
        documents = {
            "customer": CUSTOMER_CANON.read_text(encoding="utf-8"),
            "schedule": SCHEDULE_CANON.read_text(encoding="utf-8"),
            "content": CONTENT_CANON.read_text(encoding="utf-8"),
            "visitor": VISITOR_CANON.read_text(encoding="utf-8"),
            "artistry": ARTISTRY_CANON.read_text(encoding="utf-8"),
            "preset": ARTISTRY_PRESET_CANON.read_text(encoding="utf-8"),
            "material": MATERIAL_CANON.read_text(encoding="utf-8"),
            "precision": PRECISION_METHOD_CANON.read_text(encoding="utf-8"),
            "root": ROOT_DECISIONS.read_text(encoding="utf-8"),
            "active": ACTIVE_CONTEXT.read_text(encoding="utf-8"),
        }
        expected_tokens = {
            "customer": ("BS-CUSTOMER-20260803-02", "사건 위험도: 7/10", "제품 구현: `BLOCKED`"),
            "schedule": ("BS-SCHEDULE-20260804-01", "오늘의 중요 소식 최대 3건", "일정 장부"),
            "content": ("BS-CONTENT-20260804-01", "CUSTOMER_MOTIVATION", "ITEM_USE_OUTCOME"),
            "visitor": ("BS-CONTENT-20260804-02", "검투사 / 모험가 / 군인 / 귀족", "왕실 의례·명품 박람회"),
            "artistry": ("BS-CRAFT-20260804-01", "작품에는 `예술성` 단일 수치만 추가", "별도 강화 버튼이나 장식 미니게임"),
            "preset": ("BS-CRAFT-20260804-02", "예술성: 정수 1~10", "MASTERPIECE / 걸작"),
            "material": ("BS-CRAFT-20260804-03", "BS-CRAFT-20260804-04", "SUPERSEDED"),
            "precision": (
                "BS-CRAFT-20260804-04",
                "보조재료 슬롯은 사용하지 않는다",
                "주재료 맥락 + 강화 방식 + 촉매·추가재료",
                "날 보강",
                "충격 흡수",
                "경량화",
                "예술 마감",
                "일반 강화는 한 입력 한 결과",
                "제품 구현은 계속 `BLOCKED`",
            ),
            "root": (
                "R2_BATCH_003_8_OF_10",
                "BS-CRAFT-20260804-04",
                "보조재료 슬롯을 제거",
                "정밀강화에서 주재료·강화 방식·촉매",
                "활성 배치 승인 카운터 `8/10`",
            ),
            "active": (
                "R1 최종 승인",
                "+10/+20/+30/+40/+50",
                "REFERENCE_IMPLEMENTATION / HISTORICAL_POC",
                "세계일정 진행 계약",
                "행동 증거",
                "BS-CRAFT-20260804-04",
                "보조재료 슬롯 없음",
                "현재 배치: `R2_BATCH_003 / 8_OF_10 / APPROVED_PENDING_MERGE`",
            ),
        }
        for document_name, tokens in expected_tokens.items():
            for token in tokens:
                with self.subTest(document=document_name, token=token):
                    self.assertIn(token, documents[document_name])


if __name__ == "__main__":
    unittest.main()
