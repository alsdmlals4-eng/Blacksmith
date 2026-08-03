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
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


class R2Batch003Tests(unittest.TestCase):
    def test_customer_disclosure_registry_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-CUSTOMER-20260803-02"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CUSTOMER-20260803-01", decision["refines"])
        self.assertEqual(
            ["EVENT_RISK_SCORE", "CUSTOMER_CORE_STATS", "APPROXIMATE_SUCCESS_CHANCE"],
            contract["public_fields"],
        )
        self.assertEqual("INTEGER_1_TO_10", contract["event_risk_display_scale"])
        self.assertEqual("INTEGER_1_TO_10", contract["customer_stat_display_scale"])
        self.assertFalse(contract["display_decimals"])
        self.assertEqual("APPROXIMATE_PERCENT_ROUNDED_TO_NEAREST_10", contract["success_display"])
        self.assertEqual(5, contract["success_display_min_percent"])
        self.assertEqual(95, contract["success_display_max_percent"])
        self.assertTrue(contract["post_equipment_recalculation"])
        self.assertFalse(contract["unknown_variable_notice"])
        self.assertFalse(contract["pre_sale_modifier_breakdown"])
        self.assertTrue(contract["result_causes_explained"])
        self.assertEqual("BASELINE_TEST_PRESET", contract["numeric_authority"])

        previous = decisions["BS-CUSTOMER-20260803-01"]["contract"]
        self.assertEqual("1_TO_5_HISTORICAL_PRESET", previous["display_scale"])
        self.assertEqual(
            "SUPERSEDED_FOR_PLAYER_DISPLAY_BY_BS-CUSTOMER-20260803-02",
            previous["display_scale_status"],
        )

    def test_schedule_priority_registry_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-SCHEDULE-20260804-01"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("NEAREST_MAJOR_WORLD_SCHEDULE_ONE", contract["pinned_world_schedule"])
        self.assertEqual(3, contract["important_news_visible_max"])
        self.assertEqual("BASELINE_TEST_PRESET", contract["important_news_numeric_authority"])
        self.assertEqual("GROUPED_END_OF_DAY_SUMMARY", contract["routine_personal_progress"])
        self.assertEqual("SCHEDULE_LEDGER", contract["full_history_access"])
        self.assertEqual(1, contract["tracked_personal_schedule_max"])
        self.assertFalse(contract["tracked_schedule_overrides_critical_priority"])
        self.assertFalse(contract["routine_progress_individual_popup"])
        self.assertEqual("SCHEDULE_LEDGER", contract["overflow_destination"])
        self.assertIn("PLAYER_DECISION_REQUIRED_TODAY", contract["immediate_alert_triggers"])
        self.assertIn("MAJOR_ITEM_DAMAGE_OR_LOSS", contract["immediate_alert_triggers"])
        self.assertIn("FOLLOW_UP_REQUEST_OR_REVISIT", contract["immediate_alert_triggers"])

    def test_content_composition_registry_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-CONTENT-20260804-01"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual(
            [
                "ACTIVITY_TYPE",
                "CUSTOMER_MOTIVATION",
                "EVENT_RISK_AND_REQUIREMENTS",
                "ITEM_USE_OUTCOME",
                "FOLLOW_UP_CRAFTING_RETURN",
            ],
            contract["personal_content_axes"],
        )
        self.assertEqual(
            "SITUATION_TO_EQUIPMENT_CHOICE_TO_RESULT_TO_ITEM_LEGACY_TO_NEXT_CRAFTING_DECISION",
            contract["personal_content_flow"],
        )
        self.assertIn("WORLD_AFTERMATH", contract["world_content_axes"])
        self.assertIn("CUSTOMER_AND_ITEM_FOLLOW_UP", contract["world_content_axes"])
        self.assertEqual(
            ["CUSTOMER_RESULT", "ITEM_UID_STATE_OR_LEGACY", "NEXT_CRAFTING_OR_REPAIR_DECISION"],
            contract["mandatory_result_outputs"],
        )
        self.assertFalse(contract["activity_name_and_reward_only_is_distinct_content"])
        self.assertFalse(contract["mandatory_long_form_quest"])
        self.assertTrue(contract["world_result_requires_customer_and_item_follow_up"])
        self.assertEqual("DEFERRED_TO_FOLLOW_UP_GATE", contract["exact_content_counts"])

    def test_visitor_archetypes_and_noble_content_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-CONTENT-20260804-02"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CONTENT-20260804-01", decision["refines"])
        self.assertEqual(
            ["GLADIATOR", "ADVENTURER", "SOLDIER", "NOBLE"],
            contract["visitor_archetypes"],
        )
        self.assertTrue(contract["schedule_requires_primary_visitor_fit"])
        self.assertEqual(5, len(contract["personal_content_families"]))
        self.assertIn("ARTISTRY_PRESTIGE_AND_PATRONAGE", contract["personal_content_families"])
        self.assertEqual(4, len(contract["world_content_families"]))
        self.assertIn("ROYAL_CEREMONY_AND_MASTERWORK_EXPOSITION", contract["world_content_families"])
        self.assertIn("ARTISTRY", contract["noble_request_focus"])
        self.assertIn("INHERITANCE", contract["noble_request_focus"])
        self.assertIn("HEIRLOOM_RESTORATION", contract["noble_item_scope"])
        self.assertEqual("JUDGMENT", contract["noble_primary_stat"])
        self.assertEqual("SKILL", contract["noble_optional_secondary_stat"])
        self.assertFalse(contract["new_customer_stats_added"])
        self.assertIn("GIFT_OR_INHERITANCE", contract["noncombat_item_legacy"])
        self.assertFalse(contract["noble_is_expensive_combat_reskin"])
        self.assertFalse(contract["general_non_metal_luxury_goods_in_scope"])
        self.assertEqual("FOLLOW_UP_TEST_PRESET", contract["exact_counts_and_numeric_weights"])

    def test_artistry_and_utility_crafting_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-CRAFT-20260804-01"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CONTENT-20260804-02", decision["refines"])
        self.assertEqual("ARTISTRY_ONLY", contract["new_item_value_stat"])
        self.assertFalse(contract["new_practicality_stat_added"])
        self.assertEqual(
            [
                "ITEM_GRADE",
                "AUXILIARY_MATERIALS",
                "CATALYSTS",
                "ENHANCEMENT_RESULTS",
                "ARTISTRY_ORIENTED_AFFIXES",
            ],
            contract["artistry_sources"],
        )
        self.assertIn("DURABILITY", contract["utility_representation"])
        self.assertEqual(
            [
                "EXPECTED_UTILITY_DIRECTION",
                "EXPECTED_ARTISTRY_DIRECTION",
                "EXPECTED_PRICE_DIRECTION",
                "EXPECTED_ENHANCEMENT_AND_AFFIX_BIAS",
            ],
            contract["pre_craft_preview_required"],
        )
        self.assertEqual(
            "UTILITY_ORIENTED_VS_ARTISTRY_VALUE_ORIENTED_WITH_HYBRIDS_ALLOWED",
            contract["crafting_choice"],
        )
        self.assertFalse(contract["separate_artistry_upgrade_loop"])
        self.assertTrue(contract["enhancement_remains_primary_loop"])
        self.assertEqual(
            "WEIGHTED_BY_MATERIAL_CATALYST_AND_CURRENT_ITEM_ORIENTATION",
            contract["affix_differentiation"],
        )
        self.assertIn("DURABILITY", contract["utility_affix_families"])
        self.assertIn("MASTERWORK", contract["artistry_affix_families"])
        self.assertIn("ARTISTRY", contract["price_inputs"])
        self.assertTrue(contract["visual_quality_scales_with_artistry"])
        self.assertTrue(contract["visual_readability_must_be_preserved"])
        self.assertEqual(
            "REFINED_BY_BS-CRAFT-20260804-02",
            contract["exact_artistry_scale_price_formula_affix_weights_and_visual_tiers"],
        )

    def test_artistry_minimum_preset_contract(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-CRAFT-20260804-02"]
        contract = decision["contract"]

        self.assertEqual("USER_APPROVED_PENDING_MERGE", decision["status"])
        self.assertEqual("BS-CRAFT-20260804-01", decision["refines"])
        self.assertEqual("INTEGER_1_TO_10", contract["artistry_display_scale"])
        self.assertFalse(contract["display_decimals"])
        self.assertEqual(1, contract["artistry_min"])
        self.assertEqual(10, contract["artistry_max"])
        self.assertTrue(contract["item_grade_influences_but_does_not_determine_artistry"])
        self.assertFalse(contract["enhancement_level_alone_raises_artistry"])
        self.assertEqual(["LOW", "MEDIUM", "HIGH"], contract["material_catalyst_preview_levels"])
        self.assertEqual(
            ["UTILITY_DIRECTION", "ARTISTRY_DIRECTION", "PRICE_DIRECTION", "ENHANCEMENT_AND_AFFIX_BIAS"],
            contract["preview_fields"],
        )
        self.assertTrue(contract["preview_text_required"])
        self.assertFalse(contract["color_icon_arrow_only_preview_allowed"])
        self.assertEqual(
            ["ITEM_GRADE", "UTILITY_PERFORMANCE"],
            contract["price_structure"]["base_value"],
        )
        self.assertIn("ARTISTRY_PREMIUM", contract["price_structure"]["additional_value"])
        self.assertTrue(contract["price_structure"]["customer_demand_can_modify_final_offer"])
        self.assertEqual(4, len(contract["utility_affix_families_minimum"]))
        self.assertEqual(3, len(contract["artistry_affix_families_minimum"]))
        self.assertFalse(contract["affix_pools_are_exclusive"])
        self.assertEqual(4, contract["visual_tier_count"])
        self.assertEqual(
            ["BASIC", "REFINED", "MASTERWORK", "MASTERPIECE"],
            [tier["id"] for tier in contract["visual_tiers"]],
        )
        self.assertTrue(contract["visual_tier_preserves_silhouette_and_function_readability"])
        self.assertFalse(contract["gold_gems_and_glow_only_progression"])
        self.assertEqual(
            "FOLLOW_UP_BASELINE_TEST_PRESET",
            contract["exact_material_values_price_weights_affix_probabilities"],
        )

    def test_gpt_role_boundary_is_non_batch(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        decision = decisions["BS-OPS-20260804-01"]
        contract = decision["contract"]

        self.assertEqual("USER_DIRECTIVE_OPERATING_BOUNDARY_NON_BATCH", decision["status"])
        self.assertEqual(
            ["CORE_FUN", "CONTENT_PLANNING", "IMAGE_AND_ART_DIRECTION", "ADVERSARIAL_DESIGN_REVIEW"],
            contract["gpt_primary_scope"],
        )
        self.assertIn("PRODUCT_IMPLEMENTATION", contract["default_excluded_scope"])
        self.assertEqual("CODEX_OR_IMPLEMENTATION_PHASE", contract["implementation_handoff"])

    def test_batch_counter_and_product_gate(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        active_batch = registry["active_batch"]
        self.assertEqual("R2_BATCH_003", active_batch["id"])
        self.assertEqual(6, active_batch["approved_decisions"])
        self.assertEqual("6/10", active_batch["counter"])
        self.assertEqual("APPROVED_PENDING_MERGE", active_batch["state"])
        self.assertEqual(
            [
                "BS-CUSTOMER-20260803-02",
                "BS-SCHEDULE-20260804-01",
                "BS-CONTENT-20260804-01",
                "BS-CONTENT-20260804-02",
                "BS-CRAFT-20260804-01",
                "BS-CRAFT-20260804-02",
            ],
            active_batch["decisions"],
        )
        self.assertEqual(["BS-OPS-20260804-01"], active_batch["non_batch_operating_directives"])
        self.assertEqual(103, active_batch["draft_pr"])
        self.assertEqual("PENDING_FOR_CURRENT_HEAD", active_batch["current_validation"])
        self.assertFalse(active_batch["product_paths_changed"])
        self.assertEqual("BLOCKED", registry["product_implementation"])
        self.assertEqual(
            "DEFINE_ARTISTRY_MATERIAL_VALUES_PRICE_COEFFICIENTS_AFFIX_PROBABILITIES_AND_VISUAL_MOCKUPS",
            registry["next_activity"],
        )

    def test_canon_and_entry_documents(self) -> None:
        customer = CUSTOMER_CANON.read_text(encoding="utf-8")
        schedule = SCHEDULE_CANON.read_text(encoding="utf-8")
        content = CONTENT_CANON.read_text(encoding="utf-8")
        visitor = VISITOR_CANON.read_text(encoding="utf-8")
        artistry = ARTISTRY_CANON.read_text(encoding="utf-8")
        artistry_preset = ARTISTRY_PRESET_CANON.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")

        for token in (
            "BS-CUSTOMER-20260803-02",
            "사건 위험도: 7/10",
            "기량 8/10 / 체력 6/10 / 판단력 7/10",
            "예상 성공률: 약 60%",
            "최소 5%, 최대 95%",
            "별도 경고는 표시하지 않는다",
            "1~5 표시는 병합 당시의 역사적 표시 프리셋",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, customer)

        for token in (
            "BS-SCHEDULE-20260804-01",
            "가장 가까운 주요 세계 일정 하나 고정",
            "오늘의 중요 소식 최대 3건",
            "일반 개인 일정은 하루 종료 묶음 요약",
            "관심 있는 개인 일정 하나를 선택 추적",
            "일정 장부",
            "BS-OPS-20260804-01",
            "핵심 재미와 플레이 동기",
            "이미지·아트 방향",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, schedule)

        for token in (
            "BS-CONTENT-20260804-01",
            "ACTIVITY_TYPE",
            "CUSTOMER_MOTIVATION",
            "ITEM_USE_OUTCOME",
            "FOLLOW_UP_CRAFTING_RETURN",
            "활동 이름과 보상만 다르고",
            "작품 UID에 남는 상태·흔적·연대기",
            "다음에 무엇을 만들거나 고칠 것인가",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, content)

        for token in (
            "BS-CONTENT-20260804-02",
            "검투사 / 모험가 / 군인 / 귀족",
            "예술·위신·후원",
            "왕실 의례·명품 박람회",
            "의장용 무기·갑주",
            "가문 귀속",
            "증여·상속 이력",
            "귀족 때문에 새 고객 능력치를 추가하지 않는다",
            "금색·보석 과잉으로 통일하지 않는다",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, visitor)

        for token in (
            "BS-CRAFT-20260804-01",
            "작품에는 `예술성` 단일 수치만 추가",
            "별도의 `실용성` 수치는 추가하지 않는다",
            "실전 성능 예상 방향",
            "예술성 예상 방향",
            "강화 시 붙기 쉬운 효과·수식어 성향",
            "실용형 작품",
            "예술형 작품",
            "혼합형 작품",
            "별도 강화 버튼이나 장식 미니게임",
            "예술성이 높을수록 작품 외형과 연출이 더 정교",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, artistry)

        for token in (
            "BS-CRAFT-20260804-02",
            "예술성: 정수 1~10",
            "실전 성능: 낮음 / 보통 / 높음",
            "기본 작품 가치",
            "추가 가치",
            "OFFENSE_AND_PRECISION",
            "FINISH_AND_CRAFTSMANSHIP",
            "BASIC / 기본",
            "MASTERPIECE / 걸작",
            "색상·아이콘·화살표는 보조 표현",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, artistry_preset)

        for token in (
            "BS-CUSTOMER-20260803-02",
            "BS-SCHEDULE-20260804-01",
            "BS-CONTENT-20260804-01",
            "BS-CONTENT-20260804-02",
            "BS-CRAFT-20260804-01",
            "BS-CRAFT-20260804-02",
            "BS-OPS-20260804-01",
            "R2_BATCH_003_6_OF_10",
            "APPROVED_PENDING_MERGE",
            "예술성 최소 표시·가격·수식어·시각 프리셋",
            "실전 성능: 낮음 / 보통 / 높음",
            "시각 4단계",
        ):
            self.assertIn(token, root)

        for token in (
            "BS-CUSTOMER-20260803-02",
            "BS-SCHEDULE-20260804-01",
            "BS-CONTENT-20260804-01",
            "BS-CONTENT-20260804-02",
            "BS-CRAFT-20260804-01",
            "BS-CRAFT-20260804-02",
            "BS-OPS-20260804-01",
            "사건 위험도: 정수 `1~10`",
            "오늘의 중요 소식 최대 3건",
            "검투사 / 모험가 / 군인 / 귀족",
            "제작 전 재료·촉매 예상 효과 계약",
            "예술성 최소 프리셋",
            "예술성: 정수 1~10",
            "기본 작품 가치 = 작품 등급 + 실전 성능",
            "승인 카운터: `6/10`",
            "행동 증거",
            "자동 단조",
            "MVP-001~003",
            "`+11`",
            "제작 모델 7건",
            "통합 6건",
            "enhancement_balance.json",
            "enhancement_milestones.json",
        ):
            self.assertIn(token, active)


if __name__ == "__main__":
    unittest.main()
