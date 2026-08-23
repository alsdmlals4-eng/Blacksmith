from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
OVERLAY = ROOT / "CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md"
AUTHORITY_INDEX = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"


class CurrentActiveContextPriorityOverlayTests(unittest.TestCase):
    def test_active_context_routes_latest_20260820_planning_overlay_before_historical_phase_c(self) -> None:
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        overlay = OVERLAY.read_text(encoding="utf-8")
        authority = AUTHORITY_INDEX.read_text(encoding="utf-8")

        self.assertIn("CURRENT_PRIORITY_OVERLAY", overlay)
        self.assertIn("BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION", overlay)
        self.assertIn("CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md", authority)

        head = active[:2500]
        self.assertIn("CURRENT_PRIORITY_OVERLAY", head)
        self.assertIn("WORK_MODE: PLAN", head)
        self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION", head)
        self.assertNotIn("CURRENT_STAGE: PHASE_C_IMPLEMENTATION_ENTRY", head)
        self.assertNotIn("PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON", head)

    def test_20260811_phase_c_record_is_preserved_as_history_not_current_gate(self) -> None:
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        self.assertIn("BS-OPS-20260811-03", active)
        self.assertIn("HISTORICAL", active)
        self.assertIn("CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md", active[:2500])


if __name__ == "__main__":
    unittest.main()
