from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/validate-project-base-adapter.yml"
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
HEALTH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"
CURRENT = ROOT / "CURRENT_CONFIRMED_DECISIONS.md"
OPERATING_CONTRACT_BASELINE = "2a920392aaedc6c602ea3b6d7f8e6f02805eeb7a"
BASE_RELEASE_VERSION = "9.4.4"
HEALTH_EVIDENCE_HASHES = {
    "BS-ADAPTER-MIGRATION-20260806": "f074e5c72cb7e8da2d89c5893daa2439db4111d97d92ca9a9a97bed5cfa85e65",
    "BS-CURRENT-DECISIONS": "21faa7af4ff651d9f6c20dba4830a89d077b3d8335552d720774055e49230f1b",
    "BS-R1-CANON-REGISTRY": "e7712f841e665f65b8634baa077085090ff916b34ba322eef6563c5f54d09051",
    "BS-SHEET-AUTHORITY-20260806": "7c935c3ae3afd0e2f24f8849bef6a1d6c1952fdd83be52043e5466148433f792",
    "BS-STATIC-RECOVERY-REPORT": "916ef973ffac0922f9c74c5233ed9421e1ed96767c14a3f0b7b5257f4e1616ad",
}
CANONICAL_LF_EVIDENCE_SOURCES = {
    "CURRENT_CONFIRMED_DECISIONS.md",
    "docs/operations/BLACKSMITH_ADAPTER_MIGRATION_STATE_2026-08-06.json",
    "docs/operations/BLACKSMITH_SHEET_AUTHORITY_EVIDENCE_2026-08-06.json",
    "docs/operations/BS-OPS-20260802-01_FINAL_REPORT.md",
    "docs/planning/CURRENT_R1_CANON_REGISTRY.json",
}


class LongLivedPrAdapterBaselineContractTests(unittest.TestCase):
    def test_workflow_compares_actual_pr_head_not_merge_head(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("ref: ${{ github.event.pull_request.head.sha }}", text)
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

    def test_adapter_uses_the_released_reuse_first_base_contract(self) -> None:
        adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(BASE_RELEASE_VERSION, adapter["base_release"]["version"])

    def test_health_evidence_hashes_use_canonical_git_bytes(self) -> None:
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
            canonical = subprocess.run(
                ["git", "show", f"HEAD:{source.relative_to(ROOT).as_posix()}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            self.assertEqual(expected_hash, hashlib.sha256(canonical).hexdigest())

    def test_health_evidence_sources_are_checked_out_with_lf(self) -> None:
        attributes = ROOT / ".gitattributes"
        self.assertTrue(attributes.exists())
        lines = set(attributes.read_text(encoding="utf-8").splitlines())
        for source in CANONICAL_LF_EVIDENCE_SOURCES:
            self.assertIn(f"{source} text eol=lf", lines)

    def test_operating_maturity_has_three_valid_operating_records(self) -> None:
        health = json.loads(HEALTH.read_text(encoding="utf-8"))
        self.assertEqual("OM-L3", health["operating_maturity"])
        self.assertEqual(3, len(health["evidence"]["operating"]))


if __name__ == "__main__":
    unittest.main()
