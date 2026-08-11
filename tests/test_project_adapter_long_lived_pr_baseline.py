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
TASK2_POSTMERGE_BASELINE = "fa9595b2df95897c915331a1cb5d9b1a583611f0"


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

    def test_completed_task2_protected_change_advances_baseline_and_retires_one_shot_approval(self) -> None:
        adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(TASK2_POSTMERGE_BASELINE, adapter["protected_baseline"]["commit"])
        self.assertFalse(APPROVAL.exists())

    def test_current_decisions_health_evidence_hash_is_exact(self) -> None:
        health = json.loads(HEALTH.read_text(encoding="utf-8"))
        records = {
            item["id"]: item
            for item in health["evidence"]["operating"]
        }
        record = records["BS-CURRENT-DECISIONS"]
        self.assertEqual("CURRENT_CONFIRMED_DECISIONS.md", record["source"])
        # Git's system-level core.autocrlf may materialize this tracked Markdown
        # file as CRLF on Windows even though the authoritative Git blob is LF.
        # Evidence hashes therefore use the canonical LF representation.
        canonical_bytes = CURRENT.read_bytes().replace(b"\r\n", b"\n")
        actual = hashlib.sha256(canonical_bytes).hexdigest()
        self.assertEqual(actual, record["sha256"])

    def test_operating_maturity_has_three_valid_operating_records(self) -> None:
        health = json.loads(HEALTH.read_text(encoding="utf-8"))
        self.assertEqual("OM-L3", health["operating_maturity"])
        self.assertEqual(3, len(health["evidence"]["operating"]))


if __name__ == "__main__":
    unittest.main()
