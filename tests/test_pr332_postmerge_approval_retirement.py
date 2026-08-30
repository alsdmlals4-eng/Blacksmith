from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_ROOT = Path(r"C:\Users\user\Documents\GitHub\Base")
VALIDATOR = BASE_ROOT / "tools" / "check_project_operating_contract.py"
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PR332_MERGE = "0122f0011b80ad55e04a57a14bccb89eb11bebc2"


class PR332PostmergeApprovalRetirementTests(unittest.TestCase):
    def test_postmerge_standard_contract_retires_the_one_shot_approval_and_adopts_pr332(self) -> None:
        """Fails if the one-shot protected approval survives its merged change."""
        self.assertFalse(APPROVAL.exists())
        adapter = json.loads((ROOT / "skills" / "PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        self.assertEqual(PR332_MERGE, adapter["protected_baseline"]["commit"])
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--project-root",
                str(ROOT),
                "--base-repository",
                str(BASE_ROOT),
                "--protected-base",
                PR332_MERGE,
                "--check",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
