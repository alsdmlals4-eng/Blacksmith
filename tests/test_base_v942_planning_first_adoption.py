from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
MIGRATION_STATE = ROOT / "docs/operations/BLACKSMITH_ADAPTER_MIGRATION_STATE_2026-08-06.json"
R1_REGISTRY = ROOT / "docs/planning/CURRENT_R1_CANON_REGISTRY.json"
R2_REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
LEGACY_REGISTRY = ROOT / "docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json"
CURRENT_GAME_BIBLE = ROOT / "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
ROOT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
AGENTS = ROOT / "AGENTS.md"
GRADE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md"
ARTISTRY_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md"
ARTISTRY_FLOW_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md"
BENCHMARK_CANON = ROOT / "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md"
CLOSURE_CANON = ROOT / "docs/planning/BLACKSMITH_R2_CHECKPOINT_004_POSTMERGE_CLOSURE_2026.md"


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
        migration = load_json(MIGRATION_STATE)
        preserved = migration["migrated_adapter_root_fields"]["project_operating_state"]
        self.assertEqual("BLOCKED", preserved["product_implementation"])

    def test_r1_and_pr81_remain_historical(self) -> None:
        registry = load_json(R1_REGISTRY)
        self.assertEqual("HISTORICAL_R1_APPROVED_BASELINE_R2_REFINED", registry["registry_status"])
        pr81 = next(item for item in registry["pull_request_status"] if item["number"] == 81)
        self.assertEqual("REFERENCE_ONLY_DO_NOT_MERGE_AS_UNIT", pr81["status"])
        self.assertEqual("REJECTED", pr81["whole_pr_merge"])

        legacy = load_json(LEGACY_REGISTRY)
        self.assertEqual(2, legacy["schema_version"])
        self.assertEqual("REJECTED", legacy["pull_requests"][0]["merge_unit_status"])

    def test_checkpoint_004_evidence_is_immutable(self) -> None:
        self.assertEqual(9, self.registry["schema_version"])
        evidence = self.registry["immutable_merge_evidence"]["checkpoint_004"]
        self.assertEqual(106, evidence["planning_pr"])
        self.assertEqual("227b2dabf0d98832811415156e72f65d601332a9", evidence["planning_exact_head"])
        self.assertEqual("789c73f38003f40dde5e9a99cd7dcb3ca03863f7", evidence["planning_merge_sha"])
        self.assertEqual(107, evidence["closure_pr"])
        self.assertEqual("1ad791123eaf6c727e964380814ffb69f1357bbf", evidence["closure_exact_head"])
        self.assertEqual("7a46fa38586a42f268cd0432744203049649ddd5", evidence["closure_merge_sha"])
        self.assertEqual("MERGED_MAIN_CANON", evidence["closure_status"])
        self.assertEqual("PASS", evidence["github_readback"])
        self.assertEqual("PASS", evidence["sheet_readback"])
        closure = CLOSURE_CANON.read_text(encoding="utf-8")
        self.assertIn("CLOSURE_MERGED_PR107", closure)
        self.assertIn("7a46fa38586a42f268cd0432744203049649ddd5", closure)

    def test_batch_005_is_active_at_ten_of_ten(self) -> None:
        self.assertEqual("R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING", self.registry["stage_status"])
        self.assertEqual("10/10", self.registry["next_approval_counter"])
        self.assertEqual("BLOCKED", self.registry["product_implementation"])
        active = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_005", active["id"])
        self.assertEqual(10, active["approved_decisions"])
        self.assertEqual("10/10", active["counter"])
        self.assertEqual(
            [
                "BS-CRAFT-20260805-02",
                "BS-CUSTOMER-20260805-01",
                "BS-UX-20260805-01",
                "BS-CUSTOMER-20260806-01",
                "BS-ITEM-20260806-01",
                "BS-ITEM-20260806-02",
                "BS-ITEM-20260806-03",
                "BS-ITEM-20260806-04",
                "BS-ITEM-20260806-05",
                "BS-ITEM-20260806-06",
            ],
            active["decisions"],
        )
        self.assertEqual(10, active["maximum_size"])
    def test_customer_and_schedule_contracts_remain_current(self) -> None:
        customer = self.decisions["BS-CUSTOMER-20260803-02"]["contract"]
        self.assertEqual("INTEGER_1_TO_10", customer["event_risk_scale"])
        self.assertEqual("INTEGER_1_TO_10", customer["customer_stat_scale"])
        self.assertEqual("NEAREST_10_PERCENT", customer["success_forecast_rounding"])
        schedule = self.decisions["BS-WORLD-20260803-03"]["contract"]
        self.assertFalse(schedule["universal_fixed_day3_result_day4_revisit"])

    def test_five_tier_birth_grade_remains_main_canon(self) -> None:
        decision = self.decisions["BS-CRAFT-20260804-07"]
        self.assertEqual("USER_APPROVED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON", decision["status"])
        contract = decision["contract"]
        self.assertEqual(5, contract["grade_count"])
        self.assertEqual(["보통", "우수", "명품", "걸작", "전설"], contract["korean_labels"])
        self.assertTrue(contract["immutable_for_same_item_uid"])
        self.assertFalse(contract["post_craft_promotion_allowed"])
        self.assertFalse(contract["post_craft_demotion_allowed"])
        canon = GRADE_CANON.read_text(encoding="utf-8")
        self.assertIn("MERGED_PR106", canon)

    def test_artistry_stat_remains_unbounded(self) -> None:
        decision = self.decisions["BS-CRAFT-20260805-01"]
        contract = decision["contract"]
        self.assertEqual("NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM", contract["domain"])
        self.assertEqual(0, contract["minimum"])
        self.assertIsNone(contract["fixed_design_maximum"])
        self.assertFalse(contract["denominator_display_allowed"])
        self.assertFalse(contract["named_tiers_exist"])
        self.assertFalse(contract["grade_sets_fixed_artistry_maximum"])
        canon = ARTISTRY_CANON.read_text(encoding="utf-8")
        self.assertIn("예술성 27", canon)
        self.assertIn("고정 설계 최대치 없음", canon)
        self.assertNotIn("예술성 7/10", canon)

    def test_artistry_generation_growth_and_valuation_is_approved(self) -> None:
        decision = self.decisions["BS-CRAFT-20260805-02"]
        self.assertEqual("USER_APPROVED_R2_BATCH_005_1_OF_10_MERGED_PR109_MAIN_CANON", decision["status"])
        contract = decision["contract"]
        self.assertEqual("ARTISTRY", contract["persisted_stat"])
        self.assertEqual("CONTEXT_DERIVED_NOT_PERSISTED", contract["artistry_value_storage"])
        self.assertEqual("CONTEXT_DERIVED_NOT_PERSISTED", contract["customer_artistry_fit_storage"])
        self.assertEqual(
            "ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE",
            contract["valuation_model"],
        )
        self.assertEqual(["IGNORE", "SECONDARY", "PRIMARY", "REQUIREMENT"], contract["customer_interest_roles"])
        self.assertFalse(contract["same_source_double_count_allowed"])
        self.assertEqual("BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED", contract["exact_values"])
        canon = ARTISTRY_FLOW_CANON.read_text(encoding="utf-8")
        for token in ("ARTISTIC_FINISH", "구간별 한계 가치", "IGNORE / SECONDARY / PRIMARY / REQUIREMENT"):
            self.assertIn(token, canon)

    def test_benchmark_and_tdd_governance_remain_current(self) -> None:
        contract = self.decisions["BS-OPS-20260805-01"]["contract"]
        self.assertTrue(contract["benchmarking_before_questions_and_recommendations"])
        self.assertEqual(10, contract["maximum_approved_decisions_per_batch"])
        self.assertTrue(contract["tdd_required_for_every_change"])
        self.assertEqual(["RED", "GREEN", "REFACTOR"], contract["tdd_cycle"])
        agents = AGENTS.read_text(encoding="utf-8")
        for token in ("벤치마킹·현업 비교", "최대 배치 크기", "조기 체크포인트", "작업마다 TDD"):
            self.assertIn(token, agents)
        benchmark = BENCHMARK_CANON.read_text(encoding="utf-8")
        self.assertIn("Diablo IV", benchmark)
        self.assertIn("Dwarf Fortress", benchmark)

    def test_current_entrypoints_are_truthful(self) -> None:
        game_bible = CURRENT_GAME_BIBLE.read_text(encoding="utf-8")
        root = ROOT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        for text in (game_bible, root, active):
            self.assertIn("예술성 27", text)
            self.assertIn("고정 설계 최대치 없음", text)
            self.assertIn("BS-CRAFT-20260805-02", text)
            self.assertIn("제품 구현: `BLOCKED`", text)
            self.assertNotIn("예술성 7/10", text)
            self.assertNotIn("예술성 1~10", text)
        self.assertIn("R2_BATCH_005_7_OF_10", game_bible)
        self.assertIn("R2_BATCH_005_7_OF_10", active)
        self.assertIn("R2_BATCH_005_CLOSED_10_OF_10", root)


if __name__ == "__main__":
    unittest.main()
