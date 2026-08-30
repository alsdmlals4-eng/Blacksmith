from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_ROOT = Path(r"C:\Users\user\Documents\GitHub\Base")
VALIDATOR = BASE_ROOT / "tools" / "check_project_operating_contract.py"
APPROVAL = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PR330_MERGE = "464a9be4fe5fbd9aa5bc3692d73999d49fa86f71"


class PR330PostmergeApprovalRetirementTests(unittest.TestCase):
    def test_postmerge_standard_contract_uses_the_pr330_merge_baseline(self) -> None:
        """Fails if the one-shot approval survives its merged protected change."""
        self.assertFalse(APPROVAL.exists())
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--project-root",
                str(ROOT),
                "--base-repository",
                str(BASE_ROOT),
                "--protected-base",
                PR330_MERGE,
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
