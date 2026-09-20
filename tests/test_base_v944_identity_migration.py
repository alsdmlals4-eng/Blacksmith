from __future__ import annotations

import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
PROJECT_ID = "blacksmith"


class BaseV944IdentityMigrationTests(unittest.TestCase):
    def test_adapter_declares_the_canonical_blacksmith_identity(self) -> None:
        """Fails if the adapter falls back to the v1 no-identity form."""
        # Full schema validation belongs to the CI-pinned operating validator,
        # never an arbitrary developer machine's latest Base module.
        adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual(2, adapter["schema_version"])
        self.assertEqual(PROJECT_ID, adapter["project"]["project_id"])


if __name__ == "__main__":
    unittest.main()
