from __future__ import annotations

import hashlib
import json
import subprocess
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
    def assert_baseline_descends_from(self, historical_merge: str) -> None:
        baseline = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))["protected_baseline"]["commit"]
        result = subprocess.run(["git", "merge-base", "--is-ancestor", historical_merge, baseline],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_commission_delivery_retires_exact_sixteen_path_approval(self):
        receipt = json.loads((ROOT / 'docs/operations/receipts/2026-09-16-general-commissions.json').read_text(encoding='utf-8'))
        delivery = receipt['remote_delivery']
        self.assertEqual('ed6f8af37bb134288118a2d9bc7ce0e0fb0a997b', delivery['merge_commit'])
        self.assertEqual('f9301e82f0464780188a1ffc615ebc1fc53a4c12', delivery['reviewed_product_head'])
        archive = ROOT / delivery['approval_archive']
        self.assertIn(delivery['approval_archive'] + ' text eol=lf', (ROOT / '.gitattributes').read_text(encoding='utf-8').splitlines())
        self.assertEqual(delivery['approval_sha256'], raw_sha256(archive))
        approved = json.loads(archive.read_text(encoding='utf-8'))
        self.assertEqual(16, len(approved['approved_paths']))
        self.assertEqual('5a84c4b2f2e972262b66f34845d625fda736eb31', approved['protected_base_commit'])
        self.assert_baseline_descends_from(delivery['merge_commit'])
        self.assertEqual('RETIRED_ARCHIVED_NOT_DELETED', delivery['one_shot_approval_status'])

    def test_world5_delivery_retires_exact_scope_and_advances_verified_baseline(self):
        receipt = json.loads((ROOT / 'docs/operations/receipts/2026-09-13-five-equipment-world-use.json').read_text(encoding='utf-8'))
        self.assertIn('remote_delivery', receipt)
        delivery = receipt['remote_delivery']
        self.assertEqual('5a84c4b2f2e972262b66f34845d625fda736eb31', delivery['merge_commit'])
        self.assertEqual('d7f337a9765fd4c097de5ebfa5bef3b374cf7e4c', delivery['reviewed_product_head'])
        approved = json.loads((ROOT / delivery['approval_archive']).read_text(encoding='utf-8'))
        self.assertEqual(['scripts/vertical_slice/domain/vs_replan_tag_rules.gd','scripts/vertical_slice/ui/vs_workshop_screen.gd'], approved['approved_paths'])
        self.assertEqual('d50c24de07e68cbcefbc94a9cce0f715095efde0', approved['protected_base_commit'])
        self.assertEqual(delivery['merge_commit'], delivery['adapter_baseline_advanced_to'])
        self.assertEqual('RETIRED_ARCHIVED_NOT_DELETED', delivery['one_shot_approval_status'])

    def test_catalyst_exchange_retires_exact_four_paths_after_verified_merge(self):
        receipt = json.loads((ROOT / 'docs/operations/receipts/2026-09-13-catalyst-exchange.json').read_text(encoding='utf-8'))
        self.assertIn('remote_delivery', receipt)
        delivery = receipt['remote_delivery']
        self.assertEqual('d50c24de07e68cbcefbc94a9cce0f715095efde0', delivery['merge_commit'])
        self.assertEqual('a7158cf9804a4fdbc0ed2ffc76b4906e19fa3afb', delivery['reviewed_product_head'])
        archive = ROOT / delivery['approval_archive']
        self.assertTrue(archive.is_file())
        approved = json.loads(archive.read_text(encoding='utf-8'))
        self.assertEqual(4, len(approved['approved_paths']))
        self.assertEqual('1abd89ee6a46a31913f1ec05d466b3b8f6783979', approved['protected_base_commit'])
        self.assertEqual(delivery['merge_commit'], delivery['adapter_baseline_advanced_to'])
        self.assertEqual('RETIRED_ARCHIVED_NOT_DELETED', delivery['one_shot_approval_status'])

    def test_day_loop_delivery_retires_exact_two_path_approval(self):
        receipt = json.loads((ROOT / 'docs/operations/receipts/2026-09-13-recovery-day-loop.json').read_text(encoding='utf-8'))['remote_delivery']
        self.assertEqual('1abd89ee6a46a31913f1ec05d466b3b8f6783979', receipt['merge_commit'])
        self.assertEqual('6e4976cb0c50d1418aabd5cfc7be3503e55742d0', receipt['reviewed_product_head'])
        archive = ROOT / receipt['approval_archive']
        self.assertTrue(archive.is_file())
        approved = json.loads(archive.read_text(encoding='utf-8'))
        self.assertEqual(2, len(approved['approved_paths']))
        self.assertEqual('4976ae2ca9d1eae11a5fc8fc44f1f8e9c23a047d', approved['protected_base_commit'])
        self.assertEqual(receipt['merge_commit'], receipt['adapter_baseline_advanced_to'])

    def test_recovery_delivery_retires_five_path_approval_after_verified_merge(self):
        receipt = json.loads((ROOT / "docs/operations/receipts/2026-09-10-pixel-world-blueprint.json").read_text(encoding="utf-8"))["recovery_delivery"]
        self.assertEqual("4976ae2ca9d1eae11a5fc8fc44f1f8e9c23a047d", receipt.get("merge_commit"))
        self.assertEqual("fbfde8f218341b052db0aa62b61f04b7e61df1fb", receipt.get("reviewed_product_head"))
        archive = ROOT / "docs/archive/protected-approvals/recovery-order-pr375-20260913.json"
        self.assertTrue(archive.is_file())
        approved = json.loads(archive.read_text(encoding="utf-8"))
        self.assertEqual(5, len(approved["approved_paths"]))
        self.assertEqual("76ad0bb02af9e03e76f6accca8bf56d7d92945ad", approved["protected_base_commit"])
        self.assertEqual("RETIRED_ARCHIVED_NOT_DELETED", receipt.get("one_shot_approval_status"))
        self.assertEqual(receipt["merge_commit"], receipt["adapter_baseline_advanced_to"])

    def test_world_trials_delivery_retires_exact_approval_and_advances_only_baseline(self):
        receipt = json.loads((ROOT / "docs/operations/receipts/2026-09-10-pixel-world-blueprint.json").read_text(encoding="utf-8"))["world_trials_delivery"]
        self.assertEqual("76ad0bb02af9e03e76f6accca8bf56d7d92945ad", receipt.get("merge_commit"))
        self.assertEqual("278caffc972d9bae9b0306bd56c97edda850d946", receipt.get("reviewed_product_head"))
        self.assertEqual("RETIRED_ARCHIVED_NOT_DELETED", receipt.get("one_shot_approval_status"))
        archive = ROOT / "docs/archive/protected-approvals/world-trials-pr373-20260913.json"
        self.assertTrue(archive.is_file())
        if not archive.is_file():
            return
        approved = json.loads(archive.read_text(encoding="utf-8"))
        self.assertEqual("df48dd06bffa1df11287029d2c7f43815f84ad23", approved["protected_base_commit"])
        self.assertEqual(8, len(approved["approved_paths"]))
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(receipt["merge_commit"], receipt["adapter_baseline_advanced_to"])
        self.assertEqual("9.4.4", adapter["base_release"]["version"])

    def test_postmerge_contract_retires_the_consumed_protected_change_approval(self) -> None:
        adapter = json.loads(CANONICAL_ADAPTER.read_text(encoding="utf-8"))

        current_delivery = json.loads((ROOT / "docs/operations/receipts/2026-09-16-general-commissions.json").read_text(encoding="utf-8"))["remote_delivery"]
        self.assert_baseline_descends_from(current_delivery["adapter_baseline_advanced_to"])
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
            self.assertNotEqual("df48dd06bffa1df11287029d2c7f43815f84ad23", current["protected_base_commit"], "The consumed PR373 approval must not be resurrected")
            self.assertNotEqual("76ad0bb02af9e03e76f6accca8bf56d7d92945ad", current["protected_base_commit"], "The consumed PR375 approval must not be resurrected")
            self.assertNotEqual("4976ae2ca9d1eae11a5fc8fc44f1f8e9c23a047d", current["protected_base_commit"], "The consumed PR377 approval must not be resurrected")
            self.assertNotEqual("1abd89ee6a46a31913f1ec05d466b3b8f6783979", current["protected_base_commit"], "The consumed PR379 approval must not be resurrected")
            self.assertNotEqual("d50c24de07e68cbcefbc94a9cce0f715095efde0", current["protected_base_commit"], "The consumed PR381 approval must not be resurrected")
            self.assertNotEqual("5a84c4b2f2e972262b66f34845d625fda736eb31", current["protected_base_commit"], "The consumed PR384 approval must not be resurrected")
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
