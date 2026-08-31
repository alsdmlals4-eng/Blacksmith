from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
CURRENT_PRODUCT_MERGE = "16e33b87b5c4880207466443b03beb3705ab8c57"
CANONICAL_ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
CURRENT_PRECISION_DECISION = "BS-ENHANCE-20260901-40"
CURRENT_PRECISION_APPROVED_PATHS = [
    "scripts/vertical_slice/domain/vs_save_envelope.gd",
    "scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd",
    "scripts/vertical_slice/resolvers/vs_precision_resolver.gd",
    "scripts/vertical_slice/services/vs_enhancement_action_service.gd",
    "scripts/vertical_slice/services/vs_save_service.gd",
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
    def test_postmerge_contract_retires_the_ao_logo_approval_and_records_only_current_precision_scope(self) -> None:
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))

        self.assertEqual(CURRENT_PRODUCT_MERGE, adapter["protected_baseline"]["commit"])
        self.assertTrue(APPROVAL.is_file())
        approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
        self.assertNotIn("BS-IDENTITY-20260831-39", approval["decision_ids"])
        self.assertIn(CURRENT_PRECISION_DECISION, approval["decision_ids"])
        self.assertEqual(CURRENT_PRODUCT_MERGE, approval["protected_base_commit"])
        self.assertEqual(CURRENT_PRECISION_APPROVED_PATHS, approval["approved_paths"])

    def test_generated_compatibility_views_track_the_rebased_canonical_adapter(self) -> None:
        canonical_sha = raw_sha256(CANONICAL_ADAPTER)
        for path, hash_key in COMPATIBILITY_VIEWS:
            with self.subTest(path=path.relative_to(ROOT)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(canonical_sha, nested_value(payload, hash_key))


if __name__ == "__main__":
    unittest.main()
