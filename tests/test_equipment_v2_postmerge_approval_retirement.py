from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
CURRENT_PRODUCT_MERGE = "c31e550fc8d5b27d4377aeb542fde3cbfe228c06"
CANONICAL_ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
INDEPENDENT_LOOP_RECEIPT = ROOT / "docs" / "operations" / "receipts" / "2026-09-03-independent-forge-lifecycle-design.json"
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
    def test_postmerge_contract_retires_the_consumed_protected_change_approval(self) -> None:
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))

        current_delivery = json.loads((ROOT / "docs/operations/receipts/2026-09-10-pixel-world-blueprint.json").read_text(encoding="utf-8"))["remote_delivery"]
        self.assertEqual(current_delivery["adapter_baseline_advanced_to"], adapter["protected_baseline"]["commit"])
        # Retirement belongs to the consumed approval, not this reusable path.
        # A later approved task may publish a new manifest against the merged base.
        if APPROVAL.exists():
            current = json.loads(APPROVAL.read_text(encoding="utf-8"))
            self.assertNotEqual(
                "1686f8f164cba2abf0678d7b768f00699a3414dd",
                current["protected_base_commit"],
                "The consumed independent-forge approval must not be resurrected",
            )
            self.assertNotEqual("c31e550fc8d5b27d4377aeb542fde3cbfe228c06", current["protected_base_commit"], "The consumed PR371 approval must not be resurrected")
            self.assertEqual(adapter["protected_baseline"]["commit"], current["protected_base_commit"])

    def test_replan_checkpoint_is_bound_to_the_merged_source_and_preserved_approval(self):
        receipt = json.loads((ROOT / "docs/operations/receipts/2026-09-10-pixel-world-blueprint.json").read_text(encoding="utf-8"))["remote_delivery"]
        self.assertEqual("df48dd06bffa1df11287029d2c7f43815f84ad23", receipt["merge_commit"])
        self.assertEqual("dc2c8bbc974d4ea1248361abe15bd0298d487632", receipt["reviewed_product_head"])
        self.assertEqual("RETIRED_ARCHIVED_NOT_DELETED", receipt["one_shot_approval_status"])
        archive = ROOT / receipt["approval_archive"]
        self.assertTrue(archive.is_file())
        self.assertEqual("c31e550fc8d5b27d4377aeb542fde3cbfe228c06", json.loads(archive.read_text(encoding="utf-8"))["protected_base_commit"])

    def test_independent_loop_receipt_records_merged_delivery_and_retirement(self) -> None:
        receipt = json.loads(INDEPENDENT_LOOP_RECEIPT.read_text(encoding="utf-8"))
        delivery = receipt["remote_delivery"]

        self.assertEqual(366, delivery["pull_request"])
        self.assertEqual("1713b64d22e0f830b6e980aa451df73158fcb2e4", delivery["source_head"])
        self.assertEqual(CURRENT_PRODUCT_MERGE, delivery["merge_commit"])
        self.assertEqual("ALL_GREEN_EXACT_HEAD", delivery["checks"])
        self.assertEqual("PASS", delivery["main_readback"])
        self.assertEqual("RETIRED", delivery["one_shot_approval_status"])
        self.assertEqual(CURRENT_PRODUCT_MERGE, delivery["adapter_baseline_advanced_to"])

    def test_generated_compatibility_views_track_the_rebased_canonical_adapter(self) -> None:
        canonical_sha = raw_sha256(CANONICAL_ADAPTER)
        for path, hash_key in COMPATIBILITY_VIEWS:
            with self.subTest(path=path.relative_to(ROOT)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(canonical_sha, nested_value(payload, hash_key))


if __name__ == "__main__":
    unittest.main()
