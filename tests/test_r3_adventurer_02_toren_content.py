from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
CANON = ROOT / "docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
HUB = ROOT / "[기획서]/00_프로젝트_허브"
ACTIVE = HUB / "ACTIVE_CONTEXT.md"
START_HERE = HUB / "START_HERE.md"
ROADMAP = HUB / "ROADMAP.md"
GATES = HUB / "DEVELOPMENT_GATES.md"


class Adventurer02TorenContentContractTests(unittest.TestCase):
    def test_r3_registry_preserves_the_approved_second_content_decision(self) -> None:
        self.assertTrue(REGISTRY.is_file())
        registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.is_file() else {}
        self.assertEqual("R3_R7_DESIGN_ACTIVE", registry.get("stage_status"))
        self.assertEqual("BLOCKED", registry.get("product_implementation"))
        self.assertEqual("NOT_APPROVED", registry.get("task3_implementation"))
        self.assertEqual("4/10", registry.get("next_approval_counter"))

        decisions = {item["id"]: item for item in registry.get("current_decisions", [])}
        for decision_id in (
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
        ):
            self.assertIn(decision_id, decisions)

        decision = decisions.get("BS-CONTENT-20260811-02", {})
        self.assertIn("USER_APPROVED_R3_R7_2_OF_10", decision.get("status", ""))
        contract = decision.get("contract", {})
        self.assertEqual("ADVENTURER_02", contract.get("content_id"))
        self.assertEqual("TOREN_MARCH", contract.get("customer_id"))
        self.assertEqual("JOURNEY_CONTINUITY_AND_RELIABILITY", contract.get("content_goal"))
        self.assertEqual("BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_TRAVEL_CONTROLLER", contract.get("player_role"))
        self.assertFalse(contract.get("direct_travel_or_route_minigame"))
        self.assertFalse(contract.get("single_always_best_equipment_answer"))
        self.assertFalse(contract.get("new_reliability_or_repairability_raw_stat"))
        self.assertFalse(contract.get("routine_automatic_wear_tax"))
        self.assertEqual("ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE", contract.get("personal_schedule_progression"))
        self.assertFalse(contract.get("universal_fixed_day_count"))
        self.assertEqual(
            ["JOURNEY_ARRIVAL_STATE", "ROUTE_EXPOSURE_STATE", "ITEM_UID_LIFECYCLE_STATE"],
            contract.get("result_axes"),
        )
        self.assertEqual("NON_CANONICAL_BASELINE_TEST_FIXTURE", contract.get("test_fixture_status"))
        self.assertEqual("OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL", contract.get("playtest_evidence"))

    def test_canon_uses_existing_item_ownership_without_turning_into_travel_game(self) -> None:
        self.assertTrue(CANON.is_file())
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "BS-CONTENT-20260811-02",
            "ADVENTURER_02",
            "TOREN_MARCH",
            "토렌 마치",
            "JOURNEY_CONTINUITY_AND_RELIABILITY",
            "WEIGHT",
            "DURABILITY",
            "ENVIRONMENTAL_SEALING",
            "FIELD_SERVICEABILITY",
            "PREP_AND_DEPARTURE",
            "EXPOSURE_AND_ROUTE_ADAPTATION",
            "ARRIVAL_AND_ITEM_ASSESSMENT",
            "FIELD_MAINTAINED_UID_PRESERVED",
            "직접 이동·지도 경로 선택·실시간 생존 조작을 요구하지 않는다",
            "자동 매일 내구도 감소 금지",
            "BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED",
        ):
            self.assertIn(token, canon)

        for forbidden in (
            "RELIABILITY_RAW_STAT: true",
            "PORTABILITY_RAW_STAT: true",
            "REPAIRABILITY_RAW_STAT: true",
            "DIRECT_TRAVEL_MINIGAME: true",
            "ROUTINE_AUTOMATIC_WEAR_TAX: true",
            "TASK3_IMPLEMENTATION_APPROVED",
        ):
            self.assertNotIn(forbidden, canon)

    def test_information_and_playtest_contract_remain_explainable_and_noncanonical(self) -> None:
        canon = CANON.read_text(encoding="utf-8") if CANON.is_file() else ""
        for token in (
            "DEFAULT_CUSTOMER_CARD",
            "POST_EQUIPMENT_DECISION_LAYER",
            "DETAIL_VIEW",
            "작품 미선택 기본 예상 성공률",
            "OVERWEIGHT",
            "자동 추천·Best 배지·불투명 종합점수 금지",
            "NON_CANONICAL_BASELINE_TEST_FIXTURE",
            "FIXTURE_A_HIGH_ENHANCEMENT_HEAVY",
            "FIXTURE_B_BALANCED_DURABLE",
            "FIXTURE_C_CONTEXT_FUNCTION",
            "OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL",
            "FIELD_SERVICEABILITY",
            "완전 복원이나 상시 성공 보너스로 오해하지 않는가",
            "돌아온 작품은 이전 작품과 어떤 관계인가요?",
            "48dp",
        ):
            self.assertIn(token, canon)

    def test_current_entrypoints_preserve_toren_history_while_ersa_is_current(self) -> None:
        current = CURRENT.read_text(encoding="utf-8")
        active = ACTIVE.read_text(encoding="utf-8")
        start_here = START_HERE.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")
        gates = GATES.read_text(encoding="utf-8")

        for decision_id in (
            "BS-CONTENT-20260811-01",
            "BS-CONTENT-20260811-02",
            "BS-CONTENT-20260811-03",
            "BS-CONTENT-20260811-04",
        ):
            self.assertIn(decision_id, current)

        for text in (active, start_here, roadmap, gates):
            self.assertIn("R3_R7_DESIGN_ACTIVE", text)
            self.assertIn("R3_R7_APPROVAL_COUNTER: 5/10", text)
            self.assertIn("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05", text)
            self.assertIn("BS-CONTENT-20260811-02", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED", text)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", text)
            self.assertNotIn("TASK3_IMPLEMENTATION_APPROVED", text)

        for text in (active, start_here, roadmap):
            self.assertIn("GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED", text)

        self.assertIn("BS-CONTENT-20260811-02", active)
        self.assertIn("ADVENTURER_02 / TOREN_MARCH", start_here)
        self.assertIn("### 2/10 — `BS-CONTENT-20260811-02`", roadmap)
        self.assertIn("BS-CONTENT-20260811-02", gates)

    def test_current_routers_preserve_toren_boundaries_without_making_toren_current(self) -> None:
        active = ACTIVE.read_text(encoding="utf-8")
        start_here = START_HERE.read_text(encoding="utf-8")
        roadmap = ROADMAP.read_text(encoding="utf-8")

        for token in (
            "직접 이동·지도 경로 선택·실시간 생존 조작을 추가하지 않는다",
            "새 신뢰성·휴대성·수리 용이성 원수치를 만들지 않는다",
            "자동 매일 내구도 감소·루틴 수리세를 만들지 않는다",
        ):
            self.assertIn(token, active)
            self.assertIn(token, start_here)

        self.assertNotIn("사용자 승인 Decision: `BS-CONTENT-20260811-01`.", start_here)
        self.assertIn("첫 승인 완료 Decision: `BS-CONTENT-20260811-01`.", start_here)
        self.assertIn("10. `ACTIVE_CONTEXT.md`", start_here)
        self.assertIn("11. `DEVELOPMENT_GATES.md`", start_here)
        self.assertIn("12. `ROADMAP.md`", start_here)

        self.assertIn("현재 승인 카운터: `5/10`.", roadmap)
        self.assertNotIn("현재 승인 카운터: `1/10`.", roadmap)
        self.assertIn("### 2/10 — `BS-CONTENT-20260811-02`", roadmap)
        self.assertIn("BS-CONTENT-20260811-02: USER_APPROVED_PLANNING_ONLY", roadmap)
        self.assertIn("BS-CONTENT-20260811-04: USER_APPROVED_PLANNING_ONLY", roadmap)
        self.assertNotIn("CURRENT_STAGE_STATUS: R3_R7_2_OF_10_USER_APPROVED_PLANNING_CANON", roadmap)


if __name__ == "__main__":
    unittest.main()