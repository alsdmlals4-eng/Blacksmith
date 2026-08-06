from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "tools" / "run_local_validation_pack.ps1"


class PowerShellCleanTreeGuardTests(unittest.TestCase):
    def test_clean_git_status_is_always_materialized_as_an_array(self) -> None:
        powershell = SCRIPT.read_text(encoding="utf-8")
        unsafe = "(git status --porcelain --untracked-files=no).Length"
        safe = "@(git status --porcelain --untracked-files=no).Count"

        self.assertNotIn(unsafe, powershell)
        self.assertEqual(powershell.count(safe), 2)


if __name__ == "__main__":
    unittest.main()
