from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
CLOSURE = ROOT / "docs/planning/BLACKSMITH_R2_CHECKPOINT_004_POSTMERGE_CLOSURE_2026.md"


class R2Checkpoint004CanonAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_closure_merge_evidence_is_immutable(self) -> None:
        evidence = self.registry["immutable_merge_evidence"]["checkpoint_004"]
        self.assertEqual(106, evidence["planning_pr"])
        self.assertEqual("227b2dabf0d98832811415156e72f65d601332a9", evidence["planning_exact_head"])
        self.assertEqual("789c73f38003f40dde5e9a99cd7dcb3ca03863f7", evidence["planning_merge_sha"])
        self.assertEqual(107, evidence["closure_pr"])
        self.assertEqual("1ad791123eaf6c727e964380814ffb69f1357bbf", evidence["closure_exact_head"])
        self.assertEqual("7a46fa38586a42f268cd0432744203049649ddd5", evidence["closure_merge_sha"])
        self.assertEqual("MERGED_MAIN_CANON", evidence["closure_status"])
        self.assertEqual("SQUASH", evidence["merge_method"])
        self.assertEqual("PASS", evidence["github_readback"])
        self.assertEqual("PASS", evidence["sheet_readback"])

    def test_closure_green_evidence_is_recorded(self) -> None:
        green = self.registry["tdd_evidence"]["closure_green"]
        self.assertEqual("1ad791123eaf6c727e964380814ffb69f1357bbf", green["commit"])
        self.assertEqual(101, green["planning_first_run"])
        self.assertEqual(579, green["base_run"])
        self.assertEqual(1170, green["pr_validation_run"])
        self.assertEqual("PASS", green["status"])

    def test_closure_document_matches_registry(self) -> None:
        text = CLOSURE.read_text(encoding="utf-8")
        self.assertIn("CLOSURE_MERGED_PR107", text)
        self.assertIn("1ad791123eaf6c727e964380814ffb69f1357bbf", text)
        self.assertIn("7a46fa38586a42f268cd0432744203049649ddd5", text)
        self.assertIn("Planning-first `101`", text)
        self.assertIn("Base `579`", text)
        self.assertIn("PR validation `1170`", text)
        self.assertIn("R2_BATCH_005: ACTIVE / 0_OF_10", text)
        self.assertIn("제품 구현: `BLOCKED`", text)


if __name__ == "__main__":
    unittest.main()
