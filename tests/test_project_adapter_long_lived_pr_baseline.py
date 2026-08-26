from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/validate-project-base-adapter.yml"
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
APPROVAL = ROOT / "docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json"
HEALTH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
OPERATING_CONTRACT_BASELINE = "1bdf5f4b436b114253e86d897c7ef15514103f8f"
BASE_RELEASE_VERSION = "9.4.4"
HEALTH_EVIDENCE_HASHES = {
    "BS-ADAPTER-MIGRATION-20260806": "d4c1552d8800d7d31e748e329c4b9b75d72d5ae3eba1f37161c736dfbda330fa",
    "BS-CURRENT-DECISIONS": "c0e22413528db5d395e086fcd339f52fdc98d2130b7a2af069ccf390e8ddf487",
    "BS-R1-CANON-REGISTRY": "d7f4367b7148c4386d812e9f3f249bc4f3e3868cabb0e75cd00ec179636256d6",
    "BS-SHEET-AUTHORITY-20260806": "866a3540fc0d1e90eab19b66b3e9357484eb438f592726db747ad9f8c5ee1eee",
    "BS-STATIC-RECOVERY-REPORT": "bb8abe56a82c02d2578fba45e6a32258c64009d447db357469faed66f503a392",
}


class LongLivedPrAdapterBaselineContractTests(unittest.TestCase):
    def test_workflow_compares_actual_pr_head_not_merge_head(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("PR_HEAD_SHA: ${{ github.event.pull_request.head.sha }}", text)
        self.assertIn('"$PR_BASE_SHA"..."$PR_HEAD_SHA"', text)
        self.assertNotIn('"$PR_BASE_SHA"...HEAD', text)

    def test_normal_pr_reads_current_adapter_baseline(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('python -c \'import json, sys; payload = json.load(sys.stdin); print(payload["protected_baseline"]["commit"])\' < "$ADAPTER_PATH"', text)
        self.assertNotIn('git show "$PR_BASE_SHA:$ADAPTER_PATH"', text)

    def test_baseline_ancestry_uses_latest_base_tip(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("PR_BASE_REF: ${{ github.event.pull_request.base.ref }}", text)
        self.assertIn('LATEST_BASE_SHA="$(git rev-parse "origin/$PR_BASE_REF")"', text)
        self.assertIn('git merge-base --is-ancestor "$PROTECTED_BASE_SHA" "$LATEST_BASE_SHA"', text)
        self.assertNotIn('git merge-base --is-ancestor "$PROTECTED_BASE_SHA" "$PR_BASE_SHA"', text)

    def test_workflow_printf_newlines_remain_escaped_in_yaml(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("if printf '%s\\n' \"$ADAPTER_CHANGES\" | grep -Fxq \"$ADAPTER_PATH\"; then", text)
        self.assertIn("printf 'PROTECTED_BASE_SHA=%s\\n' \"$PROTECTED_BASE_SHA\" >> \"$GITHUB_ENV\"", text)
        self.assertNotIn("if printf '%s\n' \"$ADAPTER_CHANGES\"", text)
        self.assertNotIn("printf 'PROTECTED_BASE_SHA=%s\n' \"$PROTECTED_BASE_SHA\"", text)
        self.assertFalse(any(line.startswith("' \"") for line in text.splitlines()))

    def test_current_main_is_the_protected_baseline_and_retires_one_shot_approval(self) -> None:
        adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(OPERATING_CONTRACT_BASELINE, adapter["protected_baseline"]["commit"])
        self.assertFalse(APPROVAL.exists())

    def test_adapter_uses_the_released_reuse_first_base_contract(self) -> None:
        adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(BASE_RELEASE_VERSION, adapter["base_release"]["version"])

    def test_health_evidence_hashes_use_exact_raw_bytes(self) -> None:
        health = json.loads(HEALTH.read_text(encoding="utf-8"))
        records = {
            item["id"]: item
            for category in ("operating", "sheet")
            for item in health["evidence"][category]
        }
        static = health["evidence"]["gates"]["static"]
        records.update({item["id"]: item for item in static})
        self.assertEqual(set(HEALTH_EVIDENCE_HASHES), set(records))
        for record_id, expected_hash in HEALTH_EVIDENCE_HASHES.items():
            record = records[record_id]
            source = ROOT / record["source"]
            self.assertEqual(expected_hash, record["sha256"])
            self.assertEqual(expected_hash, hashlib.sha256(source.read_bytes()).hexdigest())

    def test_operating_maturity_has_three_valid_operating_records(self) -> None:
        health = json.loads(HEALTH.read_text(encoding="utf-8"))
        self.assertEqual("OM-L3", health["operating_maturity"])
        self.assertEqual(3, len(health["evidence"]["operating"]))


if __name__ == "__main__":
    unittest.main()
