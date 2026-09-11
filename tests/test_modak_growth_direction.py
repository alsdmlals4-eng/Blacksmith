"""User-approved appearances do not imply implemented aging mechanics."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "docs/design/candidates/modak-human-20260911"


class ModakGrowthDirection(unittest.TestCase):
    def test_calendar_review_is_not_runtime_or_final_balance(self):
        path = ROOT / "docs/planning/BLACKSMITH_MODAK_CALENDAR_REVIEW_20260912.json"
        review = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(review["status"], "RECOMMENDED_TEST_ONLY")
        self.assertFalse(review["runtime_implemented"])
        self.assertFalse(review["final_user_approved"])
        self.assertEqual(review["clock"], "COMMITTED_GAME_DAY_ONLY")
        self.assertEqual(review["campaign_scope"], "SAME_SAVE_CAMPAIGN_NO_ANNUAL_RESET")
        for case in review["boundary_cases"]:
            elapsed = case["current_day"] - case["joined_day"]
            year = elapsed // review["recommended_days_per_year"] + 1
            self.assertEqual(year, case["expected_companion_year"])
            self.assertEqual("LATER" if year >= review["later_from_year"] else "EARLY", case["expected_appearance"])

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
