from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
R1_REGISTRY = ROOT / "docs/planning/CURRENT_R1_CANON_REGISTRY.json"
R2_REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CHECKPOINT_001 = ROOT / "docs/planning/BLACKSMITH_R2_WORLD_SCHEDULE_BASELINE_CHECKPOINT_001_2026.md"
CUSTOMER_SCHEDULE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CUSTOMER_SCHEDULE_AND_VISIBLE_CAPABILITY_CANON_2026.md"
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


def load_adapter() -> dict:
    return json.loads(ADAPTER.read_text(encoding="utf-8"))


class PlanningFirstCompatibilityTests(unittest.TestCase):
    def test_v943_preserves_planning_first_contract(self) -> None:
        adapter = load_adapter()
        release = adapter["base_release"]
        self.assertEqual("9.4.3", release["version"])
        self.assertEqual("7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8", release["release_commit"])
        self.assertEqual("da33a350d61b8adc52df97fccc7001708a933370", release["release_evidence_commit"])
        self.assertEqual("0b7c94f38d959efc0fc9442274c60b2e268a3c97", release["finalization_commit"])
        self.assertEqual(
            "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59",
            adapter["skill_registry"]["base"]["sha256"],
        )

    def test_intake_route_and_batch_contract(self) -> None:
        adapter = load_adapter()
        active = {
            route if isinstance(route, str) else route["skill_id"]
            for route in adapter["routing"]["base_routes"]
            if isinstance(route, str) or route.get("status") == "ACTIVE"
        }
        self.assertIn("managing-project-intake-and-work-contract", active)
        policy = adapter["shared_overrides"]["managing-project-intake-and-work-contract"]["planning_first_governance"]
        self.assertEqual("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md", policy["base_contract_source"])
        self.assertEqual("templates/project-operations/GRILL_ME_BATCH_CHECKPOINT.md", policy["checkpoint_template"])
        self.assertEqual("base-v9.4.3.lock.json", policy["base_release_lock"])
        self.assertEqual(10, policy["max_approved_decisions_per_batch"])
        self.assertEqual("RECOMMENDED_DEFAULT", policy["numeric_default_state"])
        self.assertEqual("GRILL_ME_REQUIRED", policy["planning_conflict_state"])
        self.assertEqual("APPROVED_PENDING_MERGE", policy["pre_merge_sheet_state"])
        self.assertEqual("SYNCED_TO_MAIN", policy["post_merge_sheet_state"])

    def test_base_adapter_boundaries_remain_stable(self) -> None:
        adapter = load_adapter()
        state = adapter["project_operating_state"]
        self.assertEqual("R2_CORE_SESSION_META_LOOP", state["stage"])
        self.assertEqual("BLOCKED_UNVERIFIED", adapter["compatibility"]["view_freshness"])
        self.assertEqual(
            "DO_NOT_HAND_EDIT_GENERATED_COMPATIBILITY_VIEWS",
            adapter["compatibility"]["manual_edit_policy"],
        )
        self.assertEqual("BLOCKED", state["product_implementation"])
        self.assertEqual("NOT_RUN", state["human_playtest"])
        self.assertEqual(
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
            adapter["protected_paths"],
        )

    def test_r1_checkpoint_history_remains_available(self) -> None:
        registry = json.loads(R1_REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual("BS-WORLD-20260803-02", registry["r2_world_schedule_baseline_decision"])
        self.assertEqual("BS-OPS-20260803-06", registry["r2_checkpoint_decision"])
        self.assertTrue(CHECKPOINT_001.exists())

    def test_current_r2_schedule_taxonomy(self) -> None:
        registry = json.loads(R2_REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}

        world = decisions["BS-WORLD-20260803-03"]
        contract = world["contract"]
        self.assertEqual("CUSTOMER_VISIT_PLUS_SALE_OR_DELIVERY", contract["personal_schedule_activation"])
        self.assertEqual("ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE", contract["personal_schedule_progression"])
        self.assertFalse(contract["repeat_visit_required_for_progress"])
        self.assertEqual("ANNOUNCED_FIXED_DATE_MAJOR_EVENT", contract["world_schedule_activation"])
        self.assertEqual(
            "PREPARATION_CHECKPOINTS_PLUS_SCHEDULED_EVENT_DATE",
            contract["world_schedule_progression"],
        )

        supersession = registry["supersession"][0]
        self.assertEqual("BS-WORLD-20260803-02", supersession["decision"])
        self.assertEqual(
            "SUPERSEDED_IN_SCOPE_BY_BS-WORLD-20260803-03",
            supersession["status"],
        )
        self.assertEqual(
            "HISTORICAL_BASELINE_EXAMPLE_FOR_ONE_PERSONAL_SCHEDULE",
            supersession["retained_role"],
        )

    def test_visible_customer_capability_forecast(self) -> None:
        registry = json.loads(R2_REGISTRY.read_text(encoding="utf-8"))
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        customer = decisions["BS-CUSTOMER-20260803-01"]["contract"]

        self.assertEqual(["SKILL", "ENDURANCE", "JUDGMENT"], customer["core_stats"])
        self.assertEqual("1_TO_5", customer["display_scale"])
        self.assertEqual("ONE_PRIMARY_PLUS_AT_MOST_ONE_SECONDARY", customer["schedule_stat_usage"])
        self.assertEqual(2, customer["traits_max"])
        self.assertEqual(1, customer["weaknesses_max"])
        self.assertEqual(
            ["VERY_LOW", "LOW", "MEDIUM", "HIGH", "VERY_HIGH"],
            customer["success_forecast"],
        )
        self.assertTrue(customer["forecast_reasons_required"])
        self.assertEqual("BASELINE_TEST_PRESET", customer["exact_modifiers"])

    def test_current_canon_text_is_linked_and_truthful(self) -> None:
        canon = CUSTOMER_SCHEDULE_CANON.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")

        for token in (
            "BS-WORLD-20260803-03",
            "BS-CUSTOMER-20260803-01",
            "BS-OPS-20260803-07",
            "기량",
            "체력",
            "판단력",
            "매우 낮음 / 낮음 / 보통 / 높음 / 매우 높음",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, canon)

        for token in (
            "CURRENT_R2_CANON_REGISTRY.json",
            "SUPERSEDED_IN_SCOPE_BY_BS-WORLD-20260803-03",
            "고객 개인 일정의 날짜 종료 진행 판정",
            "특정 날짜를 예고하는 대규모 세계 일정",
            "R2_CHECKPOINT_002_PENDING_MERGE",
        ):
            self.assertIn(token, root)

        for token in (
            "BS-WORLD-20260803-03",
            "BS-CUSTOMER-20260803-01",
            "고객 재방문 없이 하루 종료마다 최대 한 번 진행 판정",
            "매우 낮음 / 낮음 / 보통 / 높음 / 매우 높음",
        ):
            self.assertIn(token, active)


if __name__ == "__main__":
    unittest.main()
