from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
CURRENT_PRODUCT_MERGE = "1686f8f164cba2abf0678d7b768f00699a3414dd"
RETIRED_WARNING_HYGIENE_PROTECTED_BASE = "48c73c37f5d8b7f3a436a51aeb96d78febd0fe02"
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


class ProductApprovalPostmergeClosureTests(unittest.TestCase):
    def test_postmerge_contract_retires_the_consumed_warning_hygiene_approval(self) -> None:
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))

        self.assertEqual(CURRENT_PRODUCT_MERGE, adapter["protected_baseline"]["commit"])
        if APPROVAL.exists():
            # The 2026-09-01 warning-hygiene one-shot approval was consumed at
            # 1686f8f. A later, independently approved protected change may use
            # the same one-shot path, but it must not reuse that older baseline.
            approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
            self.assertNotEqual(RETIRED_WARNING_HYGIENE_PROTECTED_BASE, approval["protected_base_commit"])

    def test_generated_compatibility_views_track_the_rebased_canonical_adapter(self) -> None:
        canonical_sha = raw_sha256(CANONICAL_ADAPTER)
        for path, hash_key in COMPATIBILITY_VIEWS:
            with self.subTest(path=path.relative_to(ROOT)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(canonical_sha, nested_value(payload, hash_key))


if __name__ == "__main__":
    unittest.main()
