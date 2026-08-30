from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PR332_MERGE = "0122f0011b80ad55e04a57a14bccb89eb11bebc2"
CANONICAL_ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
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


class PR332PostmergeApprovalRetirementTests(unittest.TestCase):
    def test_postmerge_contract_adopts_pr332_and_rejects_an_unbound_replacement_approval(self) -> None:
        """PR #332's spent manifest is absent on main; a later PR must bind a new one exactly."""
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(PR332_MERGE, adapter["protected_baseline"]["commit"])
        if not APPROVAL.exists():
            return
        approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
        self.assertEqual(approval.get("schema_version"), 1)
        self.assertEqual(approval.get("artifact_role"), "PROJECT_PROTECTED_CHANGE_APPROVAL")
        self.assertEqual(approval.get("status"), "APPROVED")
        self.assertEqual(approval.get("protected_base_commit"), PR332_MERGE)
        self.assertTrue(approval.get("approved_paths"))
        approval_source = str(approval.get("approval_source", ""))
        self.assertIn("USER_APPROVED_", approval_source)
        self.assertIn("GITHUB_PR_LABEL_APPROVED_PROTECTED_CHANGE", approval_source)

    def test_generated_compatibility_views_track_the_rebased_canonical_adapter(self) -> None:
        canonical_sha = raw_sha256(CANONICAL_ADAPTER)
        for path, hash_key in COMPATIBILITY_VIEWS:
            with self.subTest(path=path.relative_to(ROOT)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(canonical_sha, nested_value(payload, hash_key))


if __name__ == "__main__":
    unittest.main()
