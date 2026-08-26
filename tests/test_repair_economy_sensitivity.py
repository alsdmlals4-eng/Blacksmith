from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs/planning/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_INPUT_20260826.json"


class RepairEconomySensitivityInputTests(unittest.TestCase):
    def test_input_fixes_one_uid_and_one_variable_sweep(self) -> None:
        self.assertTrue(INPUT.exists())
        payload = json.loads(INPUT.read_text(encoding="utf-8"))
        self.assertEqual("BS-REPAIR-SENS-001", payload["item_uid"])
        self.assertEqual(100, payload["r_band_normalized"])
        self.assertEqual([0.5, 0.65, 0.8], payload["loss_coefficients"])
        self.assertEqual(5, len(payload["events"]))
        self.assertTrue(all(event["base_max"] == 5 for event in payload["events"]))


if __name__ == "__main__":
    unittest.main()
