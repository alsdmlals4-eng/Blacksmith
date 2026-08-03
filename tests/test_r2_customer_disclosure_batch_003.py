from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CUSTOMER_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_DISCLOSURE_MINIMUM_CANON_2026.md"
SCHEDULE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_MULTI_SCHEDULE_DISPLAY_AND_ALERT_CANON_2026.md"
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
        self.assertEqual(2, active_batch["approved_decisions"])
        self.assertEqual("2/10", active_batch["counter"])
        self.assertEqual("APPROVED_PENDING_MERGE", active_batch["state"])
        self.assertEqual(
            ["BS-CUSTOMER-20260803-02", "BS-SCHEDULE-20260804-01"],
            active_batch["decisions"],
        )
        self.assertEqual(["BS-OPS-20260804-01"], active_batch["non_batch_operating_directives"])
        self.assertEqual(103, active_batch["draft_pr"])
        self.assertEqual("PENDING_FOR_CURRENT_HEAD", active_batch["current_validation"])
        self.assertFalse(active_batch["product_paths_changed"])
        self.assertEqual("BLOCKED", registry["product_implementation"])
        self.assertEqual("DEFINE_PERSONAL_AND_WORLD_SCHEDULE_CONTENT_FAMILIES", registry["next_activity"])

    def test_canon_and_entry_documents(self) -> None:
        customer = CUSTOMER_CANON.read_text(encoding="utf-8")
        schedule = SCHEDULE_CANON.read_text(encoding="utf-8")
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
            "BS-CUSTOMER-20260803-02",
            "BS-SCHEDULE-20260804-01",
            "BS-OPS-20260804-01",
            "R2_BATCH_003_2_OF_10",
            "APPROVED_PENDING_MERGE",
            "사건 위험도: `1~10`",
            "오늘의 중요 소식 최대 3건",
            "GPT 논의는 핵심 재미·콘텐츠 기획·이미지·아트 방향",
        ):
            self.assertIn(token, root)

        for token in (
            "BS-CUSTOMER-20260803-02",
            "BS-SCHEDULE-20260804-01",
            "BS-OPS-20260804-01",
            "사건 위험도: 정수 `1~10`",
            "오늘의 중요 소식 최대 3건",
            "GPT에서는 다음 영역을 중심으로 논의한다",
            "승인 카운터: `2/10`",
            "세계일정 진행 계약",
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
