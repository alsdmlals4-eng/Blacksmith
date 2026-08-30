from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PR334_MERGE = "a2489bf039c2080c7851959cc6582ab6a56645fc"
CANONICAL_ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
CURRENT_APPROVAL_DECISIONS = {
    "BS-ENHANCE-20260830-38",
    "BS-ART-20260826-04",
    "BS-OPS-20260828-35",
    "BS-OPS-20260828-36",
}
CURRENT_APPROVAL_PATHS = {
    "assets/ASSET_MANIFEST.json",
    "scripts/vertical_slice/ui/vs_workshop_screen.gd",
}
COMPATIBILITY_VIEWS = (
    (ROOT / "skills" / "BASE_V9_ADAPTER.json", "canonical_source_sha256"),
    (ROOT / "skills" / "PROJECT_BASE_SKILL_ADAPTER.json", "canonical_source_sha256"),
    (ROOT / "skills" / "PROJECT_SKILL_SNAPSHOT.json", "source_registry.sha256"),
)


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nested_value(payload: dict[str, object], dotted_key: str) -> object:
    value: object = payload
    for key in dotted_key.split("."):
        if not isinstance(value, dict):
            raise TypeError(f"{dotted_key} cannot be read from {type(value)!r}")
        value = value[key]
    return value


class PR334PostmergeApprovalRetirementTests(unittest.TestCase):
    def test_postmerge_contract_retires_phase1_approval_and_adopts_pr334(self) -> None:
        if APPROVAL.exists():
            approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
            self.assertEqual("PROJECT_PROTECTED_CHANGE_APPROVAL", approval["artifact_role"])
            self.assertEqual("APPROVED", approval["status"])
            self.assertEqual(PR334_MERGE, approval["protected_base_commit"])
            self.assertEqual(CURRENT_APPROVAL_DECISIONS, set(approval["decision_ids"]))
            self.assertEqual(CURRENT_APPROVAL_PATHS, set(approval["approved_paths"]))
            self.assertIn("one-shot manifest", approval["scope_summary"])
            self.assertIn("post-merge closure", approval["scope_summary"])
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(PR334_MERGE, adapter["protected_baseline"]["commit"])

    def test_generated_compatibility_views_track_the_rebased_canonical_adapter(self) -> None:
        canonical_sha = raw_sha256(CANONICAL_ADAPTER)
        for path, hash_key in COMPATIBILITY_VIEWS:
            with self.subTest(path=path.relative_to(ROOT)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(canonical_sha, nested_value(payload, hash_key))


if __name__ == "__main__":
    unittest.main()
