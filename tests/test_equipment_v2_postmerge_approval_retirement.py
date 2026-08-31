from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
CURRENT_PRODUCT_MERGE = "76b82967aacbef85484f9b0206d8194e09a9c9e3"
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
    def test_current_product_baseline_is_adopted_and_any_new_one_shot_approval_is_exact(self) -> None:
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))

        self.assertEqual(CURRENT_PRODUCT_MERGE, adapter["protected_baseline"]["commit"])
        if not APPROVAL.exists():
            return

        approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
        self.assertEqual("APPROVED", approval["status"])
        self.assertEqual(CURRENT_PRODUCT_MERGE, approval["protected_base_commit"])
        self.assertEqual(
            approval["decision_ids"],
            ["BS-IDENTITY-20260831-39", "BS-ART-20260826-04", "BS-OPS-20260828-36"],
        )
        self.assertEqual(
            approval["approved_paths"],
            [
                "assets/ASSET_MANIFEST.json",
                "assets/ui/identity/anvil_oath_logo_ao02_v1.png",
                "assets/ui/identity/anvil_oath_logo_ao02_v1.png.import",
                "scripts/vertical_slice/ui/vs_main_menu.gd",
            ],
        )

    def test_generated_compatibility_views_track_the_rebased_canonical_adapter(self) -> None:
        canonical_sha = raw_sha256(CANONICAL_ADAPTER)
        for path, hash_key in COMPATIBILITY_VIEWS:
            with self.subTest(path=path.relative_to(ROOT)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(canonical_sha, nested_value(payload, hash_key))


if __name__ == "__main__":
    unittest.main()
