from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CLOSURE = ROOT / "docs/planning/BLACKSMITH_R2_CHECKPOINT_005_POSTMERGE_CLOSURE_2026.md"
CURRENT_DOCS = (
    ROOT / "CURRENT_CONFIRMED_DECISIONS.md",
    ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    ROOT / "[기획서]/00_프로젝트_허브/ROADMAP.md",
    ROOT / "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
)

PLANNING_HEAD = "77eba15415bc9ede661639b45bb526d5ce4410a5"
PLANNING_MERGE = "31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9"


class R2Checkpoint005PostmergeClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_registry_records_pr109_as_merged_main_canon(self) -> None:
        self.assertEqual(
            "R2_CHECKPOINT_005_POSTMERGE_CLOSURE_PENDING",
            self.registry["stage_status"],
        )
        self.assertEqual("0/10", self.registry["next_approval_counter"])
        evidence = self.registry["immutable_merge_evidence"]["checkpoint_005"]
        self.assertEqual(109, evidence["planning_pr"])
        self.assertEqual(PLANNING_HEAD, evidence["planning_exact_head"])
        self.assertEqual(PLANNING_MERGE, evidence["planning_merge_sha"])
        self.assertEqual("MERGED_MAIN_CANON", evidence["planning_status"])
        self.assertEqual(
            "agent/r2-checkpoint-005-postmerge-closure",
            evidence["closure_branch"],
        )
        self.assertEqual("DRAFT_PR117_PENDING", evidence["closure_status"])
        self.assertEqual("SQUASH", evidence["merge_method"])

    def test_batch_005_decisions_no_longer_use_premerge_status(self) -> None:
        batch_ids = {
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
        }
        by_id = {item["id"]: item for item in self.registry["current_decisions"]}
        self.assertEqual(batch_ids, batch_ids & by_id.keys())
        for decision_id in sorted(batch_ids):
            status = by_id[decision_id]["status"]
            self.assertIn("MERGED_PR109", status, decision_id)
            self.assertIn("MAIN_CANON", status, decision_id)
            self.assertNotIn("APPROVED_PENDING_MERGE", status, decision_id)

    def test_current_authority_docs_route_to_checkpoint_005_closure(self) -> None:
        forbidden = (
            "APPROVED_PENDING_MERGE",
            "DRAFT_PR109",
            "PR #109 체크포인트 검토·명시적 병합 승인 대기",
        )
        required = (
            "R2_CHECKPOINT_005",
            "MERGED_PR109",
            PLANNING_MERGE,
            "제품 구현: `BLOCKED`",
        )
        for path in CURRENT_DOCS:
            text = path.read_text(encoding="utf-8")
            for token in required:
                self.assertIn(token, text, f"{path}: {token}")
            for token in forbidden:
                self.assertNotIn(token, text, f"{path}: {token}")

    def test_closure_document_preserves_unopened_gates(self) -> None:
        text = CLOSURE.read_text(encoding="utf-8")
        for token in (
            "R2_BATCH_005_CLOSED_10_OF_10",
            "R2_BATCH_006_NOT_STARTED_0_OF_10",
            "planning PR: `#109`",
            PLANNING_HEAD,
            PLANNING_MERGE,
            "제품 구현: `BLOCKED`",
            "사람 플레이테스트: `NOT_RUN`",
            "보호된 제품 경로 변경: `0`",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
