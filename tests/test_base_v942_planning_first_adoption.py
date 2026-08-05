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
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
AGENTS = ROOT / "AGENTS.md"
GRADE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md"
ARTISTRY_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md"
BENCHMARK_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class PlanningFirstCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_json(R2_REGISTRY)
        cls.decisions = {item["id"]: item for item in cls.registry["current_decisions"]}

    def test_base_v943_contract_remains_pinned(self) -> None:
        adapter = load_json(ADAPTER)
        release = adapter["base_release"]
        self.assertEqual("9.4.3", release["version"])
        self.assertEqual("7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8", release["release_commit"])
        self.assertEqual("da33a350d61b8adc52df97fccc7001708a933370", release["release_evidence_commit"])
        self.assertEqual("0b7c94f38d959efc0fc9442274c60b2e268a3c97", release["finalization_commit"])
        self.assertEqual("BLOCKED", adapter["project_operating_state"]["product_implementation"])

    def test_r1_registry_remains_historical(self) -> None:
        registry = load_json(R1_REGISTRY)
        self.assertEqual("HISTORICAL_R1_APPROVED_BASELINE_R2_REFINED", registry["registry_status"])
        pr81 = next(item for item in registry["pull_request_status"] if item["number"] == 81)
        self.assertEqual("REFERENCE_ONLY_DO_NOT_MERGE_AS_UNIT", pr81["status"])
        self.assertEqual("REJECTED", pr81["whole_pr_merge"])

    def test_checkpoint_004_is_closed_and_batch_005_is_active(self) -> None:
        registry = self.registry
        self.assertEqual(8, registry["schema_version"])
        self.assertEqual("R2_BATCH_005_ACTIVE_0_OF_10", registry["stage_status"])
        self.assertEqual("0/10", registry["next_approval_counter"])
        self.assertEqual("BLOCKED", registry["product_implementation"])

        evidence = registry["immutable_merge_evidence"]
        checkpoint_003 = evidence["checkpoint_003"]
        self.assertEqual(103, checkpoint_003["planning_pr"])
        self.assertEqual(104, checkpoint_003["closure_pr"])
        self.assertEqual(105, checkpoint_003["canon_audit_pr"])
        self.assertEqual("PASS", checkpoint_003["github_readback"])
        self.assertEqual("PASS", checkpoint_003["sheet_readback"])

        checkpoint_004 = evidence["checkpoint_004"]
        self.assertEqual(106, checkpoint_004["planning_pr"])
        self.assertEqual("227b2dabf0d98832811415156e72f65d601332a9", checkpoint_004["planning_exact_head"])
        self.assertEqual("789c73f38003f40dde5e9a99cd7dcb3ca03863f7", checkpoint_004["planning_merge_sha"])
        self.assertEqual(107, checkpoint_004["closure_pr"])
        self.assertEqual("PENDING_EXPECTED_HEAD_MERGE", checkpoint_004["closure_status"])
        self.assertEqual("SQUASH", checkpoint_004["merge_method"])
        self.assertEqual("PASS", checkpoint_004["github_readback"])
        self.assertEqual("PASS", checkpoint_004["sheet_readback"])

        closed = registry["closed_batch"]
        self.assertEqual("R2_BATCH_004", closed["id"])
        self.assertEqual(2, closed["approved_decisions"])
        self.assertEqual("2/10", closed["counter"])
        self.assertEqual("USER_APPROVED_EARLY_CHECKPOINT", closed["closure_reason"])
        self.assertEqual(
            ["BS-CRAFT-20260804-07", "BS-CRAFT-20260805-01"],
            closed["decisions"],
        )

        active = registry["active_batch"]
        self.assertEqual("R2_BATCH_005", active["id"])
        self.assertEqual(0, active["approved_decisions"])
        self.assertEqual("0/10", active["counter"])
        self.assertEqual([], active["decisions"])
        self.assertEqual(10, active["maximum_size"])

    def test_customer_and_schedule_contracts_remain_current(self) -> None:
        customer = self.decisions["BS-CUSTOMER-20260803-02"]["contract"]
        self.assertEqual("INTEGER_1_TO_10", customer["event_risk_scale"])
        self.assertEqual("INTEGER_1_TO_10", customer["customer_stat_scale"])
        self.assertEqual("NEAREST_10_PERCENT", customer["success_forecast_rounding"])
        self.assertEqual("5_TO_95_PERCENT", customer["success_forecast_range"])

        schedule = self.decisions["BS-WORLD-20260803-03"]["contract"]
        self.assertEqual("CUSTOMER_VISIT_PLUS_SALE_OR_DELIVERY", schedule["personal_schedule_activation"])
        self.assertEqual("ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE", schedule["personal_schedule_progression"])
        self.assertFalse(schedule["universal_fixed_day3_result_day4_revisit"])

    def test_five_tier_birth_grade_is_merged_main_canon(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-07"]
        self.assertEqual("USER_APPROVED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON", decision["status"])
        contract = decision["contract"]
        self.assertEqual(5, contract["grade_count"])
        self.assertEqual(
            ["CRAFT_NORMAL", "CRAFT_SUPERIOR", "CRAFT_FINE", "CRAFT_MASTERWORK", "CRAFT_LEGENDARY"],
            contract["grade_ids"],
        )
        self.assertEqual(["보통", "우수", "명품", "걸작", "전설"], contract["korean_labels"])
        self.assertEqual("FIRST_DIRECT_FORGING_COMPLETION_ONLY", contract["determination_timing"])
        self.assertTrue(contract["immutable_for_same_item_uid"])
        self.assertFalse(contract["post_craft_promotion_allowed"])
        self.assertFalse(contract["post_craft_demotion_allowed"])
        self.assertEqual("EXTREMELY_RARE_FIRST_CRAFT_RESULT", contract["legendary_origin"])
        for key in (
            "legendary_can_be_granted_by_reputation_chronicle_appraisal_repair_or_enhancement",
            "legendary_guarantees_max_artistry",
            "legendary_guarantees_catalyst_affix",
            "legendary_guarantees_chronicle_affix",
            "legendary_guarantees_universal_best_performance",
        ):
            self.assertFalse(contract[key])

        canon = GRADE_CANON.read_text(encoding="utf-8")
        self.assertIn("MERGED_PR106", canon)
        self.assertIn("제작 후 등급 승격 금지", canon)

    def test_artistry_is_unbounded_merged_main_canon(self) -> None:
        decision = self.decisions["BS-CRAFT-20260805-01"]
        self.assertEqual(
            "USER_APPROVED_REFINED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON",
            decision["status"],
        )
        contract = decision["contract"]
        self.assertEqual("WEAPON_ITEM_STAT", contract["stat_role"])
        self.assertEqual("NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM", contract["domain"])
        self.assertEqual(0, contract["minimum"])
        self.assertIsNone(contract["fixed_design_maximum"])
        for key in (
            "decimals_allowed",
            "denominator_display_allowed",
            "named_tiers_exist",
            "technical_storage_limit_is_content_maximum",
            "grade_sets_fixed_artistry_maximum",
            "zero_means_incomplete_or_unusable",
            "combat_power_by_default",
            "universal_affix_multiplier",
        ):
            self.assertFalse(contract[key])

        canon = ARTISTRY_CANON.read_text(encoding="utf-8")
        self.assertIn("MERGED_PR106", canon)
        self.assertIn("예술성 27", canon)
        self.assertIn("고정 설계 최대치 없음", canon)
        self.assertNotIn("예술성 7/10", canon)
        self.assertNotIn("예술성 1~10", canon)

    def test_benchmark_and_tdd_governance_remain_current(self) -> None:
        contract = self.decisions["BS-OPS-20260805-01"]["contract"]
        self.assertTrue(contract["benchmarking_before_questions_and_recommendations"])
        self.assertTrue(contract["industry_comparison_required"])
        self.assertEqual(10, contract["maximum_approved_decisions_per_batch"])
        self.assertEqual(
            ["HIGH_RISK_CONFLICT", "SESSION_END", "LARGE_CANON_IMPACT"],
            contract["early_checkpoint_triggers"],
        )
        self.assertTrue(contract["tdd_required_for_every_change"])
        self.assertEqual(["RED", "GREEN", "REFACTOR"], contract["tdd_cycle"])

        agents = AGENTS.read_text(encoding="utf-8")
        for token in ("벤치마킹·현업 비교", "최대 배치 크기", "조기 체크포인트", "작업마다 TDD"):
            self.assertIn(token, agents)
        benchmark = BENCHMARK_CANON.read_text(encoding="utf-8")
        self.assertIn("Diablo IV", benchmark)
        self.assertIn("Dwarf Fortress", benchmark)

    def test_legacy_status_registry_prevents_stale_authority(self) -> None:
        registry = load_json(LEGACY_REGISTRY)
        self.assertEqual(2, registry["schema_version"])
        artistry_history = {item["source"]: item for item in registry["artistry_model_history"]}
        self.assertEqual(
            "SUPERSEDED",
            artistry_history["BS-CRAFT-20260805-01 initial bounded-stat draft"]["status"],
        )
        pr81 = registry["pull_requests"][0]
        self.assertEqual(81, pr81["number"])
        self.assertEqual("REJECTED", pr81["merge_unit_status"])

    def test_current_entrypoints_are_truthful(self) -> None:
        game_bible = CURRENT_GAME_BIBLE.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        for text in (game_bible, root, active):
            self.assertIn("예술성 27", text)
            self.assertIn("고정 설계 최대치 없음", text)
            self.assertIn("제품 구현: `BLOCKED`", text)
            self.assertNotIn("예술성 7/10", text)
            self.assertNotIn("예술성 1~10", text)
        self.assertIn("R2_BATCH_005_0_OF_10", game_bible)
        self.assertIn("R2_BATCH_005_0_OF_10", active)
        self.assertIn("R2_BATCH_005 / 0/10", root)
        self.assertNotIn("APPROVED_PENDING_MERGE", root)
        self.assertNotIn("Draft PR 유지", active)


if __name__ == "__main__":
    unittest.main()
