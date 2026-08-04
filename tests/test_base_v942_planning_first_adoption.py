from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
R1_REGISTRY = ROOT / "docs/planning/CURRENT_R1_CANON_REGISTRY.json"
R2_REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
LEGACY_REGISTRY = ROOT / "docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json"
CURRENT_GAME_BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
OLD_GAME_BIBLE = ROOT / "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md"
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class PlanningFirstCompatibilityTests(unittest.TestCase):
    def test_base_v943_contract_remains_pinned(self) -> None:
        adapter = load_json(ADAPTER)
        release = adapter["base_release"]
        self.assertEqual("9.4.3", release["version"])
        self.assertEqual("7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8", release["release_commit"])
        self.assertEqual("da33a350d61b8adc52df97fccc7001708a933370", release["release_evidence_commit"])
        self.assertEqual("0b7c94f38d959efc0fc9442274c60b2e268a3c97", release["finalization_commit"])
        self.assertEqual(10, adapter["shared_overrides"]["managing-project-intake-and-work-contract"]["planning_first_governance"]["max_approved_decisions_per_batch"])
        self.assertEqual("BLOCKED", adapter["project_operating_state"]["product_implementation"])
        self.assertEqual(
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
            adapter["protected_paths"],
        )

    def test_r1_registry_is_historical_and_r2_refined(self) -> None:
        registry = load_json(R1_REGISTRY)
        self.assertEqual("HISTORICAL_R1_APPROVED_BASELINE_R2_REFINED", registry["registry_status"])
        self.assertEqual("R2_CHECKPOINT_003_CANON", registry["stage_status"])
        historical = registry["historical_core_contract"]
        self.assertEqual(2, historical["general_affix_slots"])
        self.assertEqual(
            "SUPERSEDED_BY_EXACTLY_THREE_GRADE_CATALYST_CHRONICLE_SLOTS",
            historical["general_affix_slots_status"],
        )
        supersession = {item["historical_rule"]: item for item in registry["r2_supersession"]}
        self.assertEqual("SUPERSEDED", supersession["GENERAL_AFFIX_A_AND_B"]["status"])
        self.assertEqual("REJECTED", supersession["AUXILIARY_MATERIAL_SLOT"]["status"])
        pr81 = next(item for item in registry["pull_request_status"] if item["number"] == 81)
        self.assertEqual("REFERENCE_ONLY_DO_NOT_MERGE_AS_UNIT", pr81["status"])
        self.assertEqual("REJECTED", pr81["whole_pr_merge"])

    def test_r2_checkpoint_003_is_closed_without_self_reference(self) -> None:
        registry = load_json(R2_REGISTRY)
        self.assertEqual(6, registry["schema_version"])
        self.assertIn("R2_CHECKPOINT_003_CANON", registry["stage_status"])
        evidence = registry["immutable_merge_evidence"]["checkpoint_003"]
        self.assertEqual(103, evidence["planning_pr"])
        self.assertEqual("674ee21013cb5d41f89a1a3f3b10ecfc31238295", evidence["planning_merge_sha"])
        self.assertEqual(104, evidence["closure_pr"])
        self.assertEqual("d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9", evidence["closure_merge_sha"])
        self.assertEqual("PASS", evidence["github_readback"])
        self.assertEqual("PASS", evidence["sheet_readback"])
        serialized = R2_REGISTRY.read_text(encoding="utf-8")
        self.assertNotIn('"current_main"', serialized)
        self.assertNotIn("PENDING_POSTMERGE_CLOSURE_PR104", serialized)
        self.assertEqual("0/10", registry["next_approval_counter"])
        self.assertEqual("BLOCKED", registry["product_implementation"])

    def test_current_customer_and_schedule_contracts(self) -> None:
        registry = load_json(R2_REGISTRY)
        decisions = {item["id"]: item for item in registry["current_decisions"]}
        customer = decisions["BS-CUSTOMER-20260803-02"]["contract"]
        self.assertEqual("INTEGER_1_TO_10", customer["event_risk_scale"])
        self.assertEqual("INTEGER_1_TO_10", customer["customer_stat_scale"])
        self.assertEqual("NEAREST_10_PERCENT", customer["success_forecast_rounding"])
        self.assertEqual("5_TO_95_PERCENT", customer["success_forecast_range"])

        schedule = decisions["BS-WORLD-20260803-03"]["contract"]
        self.assertEqual("CUSTOMER_VISIT_PLUS_SALE_OR_DELIVERY", schedule["personal_schedule_activation"])
        self.assertEqual("ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE", schedule["personal_schedule_progression"])
        self.assertFalse(schedule["universal_fixed_day3_result_day4_revisit"])

    def test_legacy_status_registry_prevents_stale_authority(self) -> None:
        registry = load_json(LEGACY_REGISTRY)
        statuses = {item["path"]: item for item in registry["documents"]}
        self.assertEqual("SUPERSEDED", statuses["docs/planning/BLACKSMITH_PRECISION_ENHANCEMENT_BASELINE.md"]["status"])
        self.assertEqual("SUPERSEDED", statuses["docs/planning/BLACKSMITH_CORE_CANON_RESOLUTION_02_2026.md"]["status"])
        self.assertEqual("PARTIALLY_SUPERSEDED", statuses["[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md"]["status"])
        pr81 = registry["pull_requests"][0]
        self.assertEqual(81, pr81["number"])
        self.assertEqual("REJECTED", pr81["merge_unit_status"])
        self.assertEqual("HOLD", pr81["selective_promotion_status"])

    def test_current_entrypoints_are_truthful(self) -> None:
        current = CURRENT_GAME_BIBLE.read_text(encoding="utf-8")
        old = OLD_GAME_BIBLE.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")

        for token in (
            "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
            "[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어",
            "보조재료 슬롯 재도입 금지",
            "제품 구현: `BLOCKED`",
        ):
            self.assertIn(token, current)

        self.assertIn("[부분 대체됨]", old)
        self.assertIn("현재 구현·후속 기획의 직접 기준으로 사용하지 마십시오", old)
        self.assertIn("BS-OPS-20260804-02", root)
        self.assertIn("PR #81 전체 병합 단위는 `[폐기]`", root)
        self.assertIn("CANON_ADVERSARIAL_AUDIT", active)
        self.assertIn("다음 승인 카운터: `0/10`", active)


if __name__ == "__main__":
    unittest.main()
