"""User-approved appearances do not imply implemented aging mechanics."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "docs/design/candidates/modak-human-20260911"


class ModakGrowthDirection(unittest.TestCase):
    def test_growth_preparation_keeps_calendar_dependency_and_runtime_gate(self):
        owner = (ROOT / "docs/design/BLACKSMITH_HUMAN_BLUEPRINT_PRODUCTION_20260911.md").read_text(encoding="utf-8")
        for contract in ["MODAK_GROWTH_PREPARATION", "CALENDAR_INTEGRATION_REQUIRED",
                         "JOIN_RELATIVE_GAME_YEARS", "NO_WALL_CLOCK_AGING",
                         "NO_FORCED_RESOURCE_LOSS", "SAVE_MIGRATION_NOT_IMPLEMENTED",
                         "YEAR_3_RECOMMENDED_NOT_LOCKED"]:
            self.assertIn(contract, owner)

    def test_both_appearances_approved_with_distinct_growth_roles(self):
        for file, stage in [("younger-record.json", "EARLY"), ("record.json", "LATER")]:
            record = json.loads((FOLDER / file).read_text(encoding="utf-8"))
            self.assertTrue(record["user_approved"])
            self.assertEqual(record["growth_stage"], stage)
            self.assertFalse(record["runtime_verified"])
            self.assertEqual(record["growth_schedule"], "UNSPECIFIED_REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
