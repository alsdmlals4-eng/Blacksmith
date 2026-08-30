from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_ROOT = Path(r"C:\Users\user\Documents\GitHub\Base")
VALIDATOR = BASE_ROOT / "tools" / "check_approved_project_operating_contract.py"
APPROVAL = "docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PR330_BASE = "ab7ca9ba1bf6599bb96a16eb44688475a64a25bf"


class PR330ProtectedChangeApprovalTests(unittest.TestCase):
    def test_pr330_exact_approved_protected_contract_is_current(self) -> None:
        """Fails if the approved PR #330 path list or its base commit drifts."""
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--project-root",
                str(ROOT),
                "--base-repository",
                str(BASE_ROOT),
                "--protected-base",
                PR330_BASE,
                "--approval",
                APPROVAL,
                "--external-approval",
                "true",
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
