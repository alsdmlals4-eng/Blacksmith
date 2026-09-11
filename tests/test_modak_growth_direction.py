"""User-approved appearances do not imply implemented aging mechanics."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "docs/design/candidates/modak-human-20260911"


class ModakGrowthDirection(unittest.TestCase):
    def test_both_appearances_approved_with_distinct_growth_roles(self):
        for file, stage in [("younger-record.json", "EARLY"), ("record.json", "LATER")]:
            record = json.loads((FOLDER / file).read_text(encoding="utf-8"))
            self.assertTrue(record["user_approved"])
            self.assertEqual(record["growth_stage"], stage)
            self.assertFalse(record["runtime_verified"])
            self.assertEqual(record["growth_schedule"], "UNSPECIFIED_REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
