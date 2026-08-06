from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "docs/planning/BLACKSMITH_R2_BATCH_006_VERTICAL_SLICE_CANON_PROPOSAL_2026.md"
REGISTRY = ROOT / "docs/planning/R2_BATCH_006_VERTICAL_SLICE_PROPOSAL_REGISTRY.json"
BENCHMARK = ROOT / "docs/planning/BLACKSMITH_R2_VERTICAL_SLICE_BENCHMARK_2026-08-06.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-06-blacksmith-godot-vertical-slice.md"

EXPECTED_DECISIONS = [
    "BS-VS-20260806-01",
    "BS-SAVE-20260806-01",
    "BS-MATERIAL-20260806-01",
    "BS-CRAFT-20260806-01",
    "BS-ITEM-20260806-07",
    "BS-ENHANCE-20260806-01",
    "BS-ENHANCE-20260806-02",
    "BS-CATALYST-20260806-01",
    "BS-CUSTOMER-20260806-02",
    "BS-CHRONICLE-20260806-01",
]


class R2Batch006VerticalSliceProposalTests(unittest.TestCase):
    def test_registry_is_a_ten_decision_unapproved_proposal(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(registry["schema_version"], 1)
        self.assertEqual(registry["batch_id"], "R2_BATCH_006")
        self.assertEqual(registry["status"], "DRAFT_PENDING_USER_APPROVAL")
        self.assertEqual(registry["counter"], "10/10")
        self.assertEqual(registry["product_implementation"], "BLOCKED")
        self.assertEqual(registry["human_playtest"], "NOT_RUN")
        self.assertEqual(
            [item["id"] for item in registry["decisions"]],
            EXPECTED_DECISIONS,
        )
        for decision in registry["decisions"]:
            self.assertEqual(decision["status"], "RECOMMENDED_PENDING_USER_APPROVAL")
            self.assertEqual(decision["authority"], "PROPOSAL_ONLY_NOT_MAIN_CANON")

    def test_proposal_preserves_all_current_canon_boundaries(self) -> None:
        text = PROPOSAL.read_text(encoding="utf-8")
        required = (
            "ALL_APPROVED_CONTRACTS_REQUIRED",
            "REPRESENTATIVE_CONTENT_ONLY",
            "BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED",
            "GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX",
            "보조재료 슬롯 없음",
            "동일 UID",
            "STRENGTH × 10 WEIGHT_POINT",
            "+10",
            "PRODUCT_IMPLEMENTATION: BLOCKED",
            "HUMAN_PLAYTEST: NOT_RUN",
            "scripts/vertical_slice/",
            "data/vertical_slice/",
            "scenes/vertical_slice/",
            "tests/vertical_slice/",
        )
        for marker in required:
            self.assertIn(marker, text)
        for stale in (
            "STANDARD / GOOD / PERFECT를 새 정본으로 사용",
            "보조재료 슬롯 재도입",
            "범용 affixes 배열 재사용",
            "최종 밸런스 확정",
        ):
            self.assertNotIn(stale, text)

    def test_save_uid_contract_is_versioned_and_non_rerolling(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        save = registry["save_contract"]
        self.assertEqual(save["schema_version"], 1)
        self.assertEqual(save["preset_version"], "VS-2026.08.06-A")
        self.assertEqual(save["path"], "user://blacksmith_vertical_slice_v1.json")
        self.assertTrue(save["persist_rng_seed"])
        self.assertTrue(save["append_only_item_ledger"])
        self.assertTrue(save["forbid_load_reroll"])
        self.assertEqual(save["uid_format"], "BSI-<32_LOWER_HEX>")

    def test_demo_values_are_explicit_but_not_product_balance(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        preset = registry["baseline_test_preset"]
        self.assertEqual(preset["version"], "VS-2026.08.06-A")
        self.assertEqual(preset["crafting_grade_rolls"]["high"], [30.0, 40.0, 24.0, 5.5, 0.5])
        self.assertEqual(preset["general_enhancement_cap"], 10)
        self.assertEqual(preset["general_enhancement_success_percent"]["10"], 50)
        self.assertEqual(preset["pity_percent_per_failure"], 5)
        self.assertEqual(preset["maximum_success_percent"], 95)
        self.assertFalse(preset["is_final_balance"])

    def test_benchmark_records_adopt_modify_and_reject_choices(self) -> None:
        text = BENCHMARK.read_text(encoding="utf-8")
        for marker in (
            "Potion Craft",
            "While the Iron's Hot",
            "Blacksmith Master",
            "Godot 4.7",
            "채택",
            "수정 채택",
            "비채택",
            "차별점",
            "남은 불확실성",
        ):
            self.assertIn(marker, text)

    def test_implementation_plan_is_tdd_and_separates_product_namespace(self) -> None:
        text = PLAN.read_text(encoding="utf-8")
        for marker in (
            "# Blacksmith Godot Vertical Slice Implementation Plan",
            "RED → GREEN → REFACTOR",
            "scripts/vertical_slice/",
            "data/vertical_slice/",
            "scenes/vertical_slice/",
            "tests/vertical_slice/",
            "Task 1: Vertical Slice Schema and Save Envelope",
            "Task 2: App Shell and Screen Routing",
            "Task 3: Direct Forging and Item Birth",
            "Task 4: General and Precision Enhancement",
            "Task 5: Customer, Schedule, and Explainable Fit",
            "Task 6: Chronicle, Repair, and Same-UID Return",
            "Task 7: End-to-End Validation and Playtest Build",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("PRODUCT_IMPLEMENTATION: APPROVED", text)


if __name__ == "__main__":
    unittest.main()
