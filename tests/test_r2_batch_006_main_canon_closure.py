from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "docs/planning/BLACKSMITH_R2_BATCH_006_VERTICAL_SLICE_CANON_PROPOSAL_2026.md"
PROPOSAL_REGISTRY = ROOT / "docs/planning/R2_BATCH_006_VERTICAL_SLICE_PROPOSAL_REGISTRY.json"
CURRENT_REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CURRENT_DECISIONS = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"

MERGE_SHA = "a8a94343c78a68bf7bb14b411e7741f43b257138"
DECISIONS = {
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
}


class R2Batch006MainCanonClosureTests(unittest.TestCase):
    def test_proposal_is_promoted_to_approved_main_canon(self) -> None:
        text = PROPOSAL.read_text(encoding="utf-8")
        self.assertIn("USER_APPROVED_MERGED_PR120_MAIN_CANON", text)
        self.assertIn("VERTICAL_SLICE_IMPLEMENTATION_APPROVED", text)
        self.assertIn(MERGE_SHA, text)
        self.assertNotIn("DRAFT_PENDING_USER_APPROVAL", text)
        self.assertNotIn("PROPOSAL_ONLY_NOT_MAIN_CANON", text)

    def test_batch_registry_records_approved_decisions_and_merge(self) -> None:
        registry = json.loads(PROPOSAL_REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(registry["status"], "USER_APPROVED_MERGED_PR120_MAIN_CANON")
        self.assertEqual(registry["authority"], "MAIN_CANON")
        self.assertEqual(registry["merge_sha"], MERGE_SHA)
        self.assertEqual(registry["product_implementation"], "BLOCKED")
        self.assertEqual(registry["vertical_slice_implementation"], "APPROVED")
        self.assertEqual({item["id"] for item in registry["decisions"]}, DECISIONS)
        for item in registry["decisions"]:
            self.assertEqual(item["status"], "USER_APPROVED_MERGED_PR120_MAIN_CANON")
            self.assertEqual(item["authority"], "MAIN_CANON")

    def test_registry_snapshot_stays_r2_while_live_router_is_phase_c(self) -> None:
        current = json.loads(CURRENT_REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(current["stage_status"], "R2_BATCH_006_APPROVED_MAIN_CANON")
        self.assertEqual(current["product_implementation"], "BLOCKED")
        self.assertEqual(current["vertical_slice_implementation"], "APPROVED")
        batch = current["active_batch"]
        self.assertEqual(batch["id"], "R2_BATCH_006")
        self.assertEqual(batch["status"], "APPROVED_MERGED_PR120_MAIN_CANON")
        self.assertEqual(batch["counter"], "10/10")
        self.assertEqual(set(batch["decisions"]), DECISIONS)

        decisions = CURRENT_DECISIONS.read_text(encoding="utf-8")
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        for text in (decisions, active):
            self.assertIn("R2_BATCH_006_APPROVED_10_OF_10", text)
            self.assertNotIn("R2_BATCH_006_NOT_STARTED_0_OF_10", text)
            self.assertIn("PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON", text)
            self.assertIn("TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED", text)
            self.assertIn("P0_LOCAL_EXECUTOR_BOOTSTRAP: PASS", text)
            self.assertIn("P1_AUTHORITY_AND_CURRENT_STATE_READBACK: PASS", text)


if __name__ == "__main__":
    unittest.main()