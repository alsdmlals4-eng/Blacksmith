from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PR338_MERGE = "b7ce7ee09f177ff49ce282c02d829154ab648b73"
PR338_APPROVAL_SOURCE = (
    "USER_APPROVED_2026-08-30_DIRECT_GODOT_IMPLEMENTATION_OF_CURRENT_"
    "RECURRING_PRECISION_TAG_WORKSHOP_FLOW_WITH_APPROVED_PROTECTED_CHANGE_LABEL"
)
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


class PR338PostmergeApprovalRetirementTests(unittest.TestCase):
    def test_postmerge_contract_retires_pr338_approval_and_adopts_pr338(self) -> None:
        if APPROVAL.exists():
            current_approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
            self.assertNotEqual(PR338_APPROVAL_SOURCE, current_approval["approval_source"])
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(PR338_MERGE, adapter["protected_baseline"]["commit"])

    def test_generated_compatibility_views_track_the_rebased_canonical_adapter(self) -> None:
        canonical_sha = raw_sha256(CANONICAL_ADAPTER)
        for path, hash_key in COMPATIBILITY_VIEWS:
            with self.subTest(path=path.relative_to(ROOT)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(canonical_sha, nested_value(payload, hash_key))


if __name__ == "__main__":
    unittest.main()
