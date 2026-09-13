"""Keep user-requested style exploration separate from production approval."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / "docs/design/candidates/young-smith-spirit-20260911"


class YoungSmithCandidateContract(unittest.TestCase):
    def test_modak_refinement_does_not_imply_approval(self):
        record = json.loads((FOLDER / "record.json").read_text(encoding="utf-8"))
        fix = record["refinements"][0]
        self.assertEqual(fix["parent"], "modak-01.png")
        self.assertFalse(fix["user_approved"])
        self.assertFalse(fix["runtime_verified"])
        self.assertTrue(fix["prompt"])
        self.assertIn(fix["alpha_status"], ["ALPHA_PRESENT_REVIEW_REQUIRED", "FAILED_NO_ALPHA"])
        if fix.get("file"):
            self.assertEqual(hashlib.sha256((FOLDER / fix["file"]).read_bytes()).hexdigest(), fix["sha256"])

    def test_requested_candidates_are_review_only_and_source_bound(self):
        record = json.loads((FOLDER / "record.json").read_text(encoding="utf-8"))
        self.assertEqual(record["status"], "USER_REVIEW_PENDING")
        self.assertFalse(record["runtime_changed"])
        self.assertEqual(len(record["candidates"]), 4)
        self.assertEqual(sum(c["role"] == "young_smith" for c in record["candidates"]), 3)
        self.assertEqual(sum(c["role"] == "fire_spirit" for c in record["candidates"]), 1)
        for candidate in record["candidates"]:
            self.assertEqual(candidate["user_approved"], candidate["file"] == "smith-01.png")
            self.assertFalse(candidate["runtime_verified"])
            self.assertTrue(candidate["consumer"])
            self.assertTrue(candidate["prompt"])
            self.assertTrue(candidate["missing_states"])
            image = FOLDER / candidate["file"]
            self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), candidate["sha256"])


if __name__ == "__main__":
    unittest.main()
