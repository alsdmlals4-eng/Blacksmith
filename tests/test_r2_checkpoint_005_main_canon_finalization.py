from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_DOCS = (
    ROOT / "[기획서]" / "00_프로젝트_허브" / "ACTIVE_CONTEXT.md",
    ROOT / "[기획서]" / "00_프로젝트_허브" / "ROADMAP.md",
    ROOT / "[기획서]" / "00_프로젝트_허브" / "DEVELOPMENT_GATES.md",
)
REGISTRY = ROOT / "docs" / "planning" / "CURRENT_R2_CANON_REGISTRY.json"


class Checkpoint005MainCanonFinalizationTest(unittest.TestCase):
    def test_current_authority_docs_use_final_closed_state(self) -> None:
        required = (
            "R2_CHECKPOINT_005_CLOSED_MAIN_CANON",
            "R2_BATCH_005_CLOSED_10_OF_10",
            "R2_BATCH_006_APPROVED_10_OF_10",
            "PRODUCT_IMPLEMENTATION: BLOCKED",
            "VERTICAL_SLICE_IMPLEMENTATION: APPROVED",
            "HUMAN_PLAYTEST: NOT_RUN",
        )
        forbidden = (
            "POSTMERGE_CLOSURE_PENDING",
            "DRAFT_PR117_PENDING",
            "PR #117 폐쇄 정본 검증·명시적 병합 승인 대기",
            "Draft PR #109",
            "R2_BATCH_005_ACTIVE_",
            "R2_BATCH_005 / 1/10",
            "R2_BATCH_005 / 2/10",
            "R2_BATCH_005 / 4/10",
            "R2_BATCH_005 / 8/10",
            "CURRENT_STAGE_STATUS: R2_CHECKPOINT_004_MAIN_CANON",
        )

        for path in AUTHORITY_DOCS:
            text = path.read_text(encoding="utf-8")
            for marker in required:
                self.assertIn(marker, text, f"{path} missing {marker}")
            for marker in forbidden:
                self.assertNotIn(marker, text, f"{path} retains stale marker {marker}")

    def test_registry_records_merged_closure_and_next_batch(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(
            registry["stage_status"],
            "R2_BATCH_006_APPROVED_MAIN_CANON",
        )
        checkpoint = registry["immutable_merge_evidence"]["checkpoint_005"]
        self.assertEqual(checkpoint["closure_pr"], 117)
        self.assertEqual(
            checkpoint["closure_merge_sha"],
            "06f03323c1309d8da0e6f5b9f4680a20ce388126",
        )
        self.assertEqual(checkpoint["closure_status"], "MERGED_MAIN_CANON")
        self.assertEqual(registry["active_batch"]["id"], "R2_BATCH_006")
        self.assertEqual(registry["active_batch"]["status"], "APPROVED_MERGED_PR120_MAIN_CANON")
        self.assertEqual(registry["active_batch"]["approved_count"], 10)
        self.assertEqual(registry["active_batch"]["maximum_count"], 10)
        self.assertEqual(registry["product_implementation"], "BLOCKED")
        self.assertEqual(registry["vertical_slice_implementation"], "APPROVED")
        self.assertEqual(registry["human_playtest"], "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
