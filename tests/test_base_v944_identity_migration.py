from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
BASE_ROOT = Path(r"C:\Users\user\Documents\GitHub\Base")
ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
PROJECT_ID = "blacksmith"
sys.path.insert(0, str(BASE_ROOT / "tools"))
import project_operating_contract as operating_contract


class BaseV944IdentityMigrationTests(unittest.TestCase):
    def test_adapter_declares_the_canonical_blacksmith_identity(self) -> None:
        """Fails if the adapter falls back to the v1 no-identity form."""
        adapter = operating_contract.load_object(ADAPTER)
        self.assertEqual(PROJECT_ID, adapter["project"]["project_id"])
        self.assertEqual("IDENTITY_VERIFIED", operating_contract.hub_identity_state(adapter))


if __name__ == "__main__":
    unittest.main()
