from __future__ import annotations

import json
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "docs/planning/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_INPUT_20260826.json"
TOOL = ROOT / "tools/run_repair_economy_sensitivity.py"


def load_tool():
    assert TOOL.exists(), f"missing analyzer: {TOOL.relative_to(ROOT)}"
    spec = importlib.util.spec_from_file_location("repair_economy_sensitivity", TOOL)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepairEconomySensitivityInputTests(unittest.TestCase):
    def test_input_fixes_one_uid_and_one_variable_sweep(self) -> None:
        self.assertTrue(INPUT.exists())
        payload = json.loads(INPUT.read_text(encoding="utf-8"))
        self.assertEqual("BS-REPAIR-SENS-001", payload["item_uid"])
        self.assertEqual(100, payload["r_band_normalized"])
        self.assertEqual([0.5, 0.65, 0.8], payload["loss_coefficients"])
        self.assertEqual(5, len(payload["events"]))
        self.assertTrue(all(event["base_max"] == 5 for event in payload["events"]))

    def test_cost_changes_only_with_loss_coefficient(self) -> None:
        analyzer = load_tool()
        payload = json.loads(INPUT.read_text(encoding="utf-8"))
        result = analyzer.analyze(payload)
        first = [row for row in result["rows"] if row["event_id"] == "E1"]
        self.assertEqual([15, 18, 21], [row["gold"] for row in first])
        self.assertEqual(1, len({row["new_current"] for row in first}))

    def test_blocking_scar_skips_and_job_cannot_repeat(self) -> None:
        analyzer = load_tool()
        payload = json.loads(INPUT.read_text(encoding="utf-8"))
        result = analyzer.analyze(payload)
        row = next(row for row in result["rows"] if row["event_id"] == "E5" and row["b"] == 0.65)
        self.assertTrue(row["scar_skipped"])
        self.assertGreater(row["new_current"], row["old_current"])
        self.assertEqual("BLOCKED_NO_REPAIR_JOB", row["repeat_repair_outcome"])


if __name__ == "__main__":
    unittest.main()
