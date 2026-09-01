from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
CURRENT_PRODUCT_MERGE = "5560d8f0bdde9d900acc2bbbaf403ef3bdbc1b58"
CANONICAL_ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
CURRENT_WIREFRAME_APPROVED_PATHS = [
    "scripts/vertical_slice/ui/vs_workshop_screen.gd",
]
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
    def test_precision_catalyst_approval_stays_retired_when_a_new_wireframe_scope_is_open(self) -> None:
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))

        self.assertEqual(CURRENT_PRODUCT_MERGE, adapter["protected_baseline"]["commit"])
        if not APPROVAL.exists():
            return

        approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
        self.assertNotIn("BS-ENHANCE-20260901-40", approval["decision_ids"])
        self.assertEqual(CURRENT_PRODUCT_MERGE, approval["protected_base_commit"])
        self.assertEqual(
            ["BS-OPS-20260825-08", "BS-OPS-20260828-36", "BS-ART-20260826-04"],
            approval["decision_ids"],
        )
        self.assertEqual(CURRENT_WIREFRAME_APPROVED_PATHS, approval["approved_paths"])

    def test_generated_compatibility_views_track_the_rebased_canonical_adapter(self) -> None:
        canonical_sha = raw_sha256(CANONICAL_ADAPTER)
        for path, hash_key in COMPATIBILITY_VIEWS:
            with self.subTest(path=path.relative_to(ROOT)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(canonical_sha, nested_value(payload, hash_key))


if __name__ == "__main__":
    unittest.main()
