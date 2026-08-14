from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / "docs/operations/loop"
LEGACY_RUN = LOOP / "runs/BS_LOOP_MIGRATION_001.json"


class UniversalLoopCapsuleMigrationHistoricalTests(unittest.TestCase):
    def test_merged_migration_run_remains_as_historical_evidence(self) -> None:
        self.assertTrue(LEGACY_RUN.is_file())
        value = json.loads(LEGACY_RUN.read_text(encoding="utf-8"))
        self.assertEqual(value["contract_role"], "LOOP_IMMUTABLE_RUN")
        self.assertEqual(value["project_id"], "BLACKSMITH")
        self.assertEqual(value["run_id"], "BS_LOOP_MIGRATION_001")
        self.assertEqual(value["package_id"], "BS_LOOP_MIGRATION_PKG_001")
        self.assertEqual(value["source_main_sha"], "c969c8ed9c6306f60c851fc85ed97e0ffa885305")
        self.assertEqual(value["state"], "CREATED")
        self.assertEqual(value["evidence"], [])
        self.assertEqual(value["findings"], [])


if __name__ == "__main__":
    unittest.main()
