from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
HANDOFF = ROOT / "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
ACTIVE_CONTEXT = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
OVERLAY = ROOT / "CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md"
AUTHORITY_INDEX = ROOT / "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md"
CURRENT_OWNER = ROOT / "docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md"


class CurrentActiveContextPriorityOverlayTests(unittest.TestCase):
    def test_current_resume_routes_handoff_and_successor_owner_before_legacy_active_context(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        handoff = HANDOFF.read_text(encoding="utf-8")
        overlay = OVERLAY.read_text(encoding="utf-8")
        authority = AUTHORITY_INDEX.read_text(encoding="utf-8")
        current_owner = CURRENT_OWNER.read_text(encoding="utf-8")

        self.assertIn("BS-OPS-20260825-08", agents)
        self.assertIn("SESSION_HANDOFF", agents)
        self.assertIn("LEGACY_COMPATIBILITY_ROUTER", agents)
        self.assertIn("BS-OPS-20260825-08", handoff)
        self.assertIn("BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md", handoff)
        self.assertIn("BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION", handoff)
        self.assertIn("CURRENT_PLANNING_WORK = REPAIR_ECONOMY_PLAYTEST_PREP + R_BAND_INPUT_EVIDENCE", handoff)

        self.assertIn("CURRENT_PRIORITY_OVERLAY", overlay)
        self.assertIn("BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION", overlay)
        for decision in (
            "BS-ENHANCE-20260825-25",
            "BS-DAMAGE-20260825-26",
            "BS-DAMAGE-20260826-28",
            "BS-REPAIR-20260826-29",
            "BS-REPAIR-20260826-31",
            "BS-DAMAGE-20260826-30",
            "BS-CHRONICLE-20260825-27",
            "BS-ART-20260825-03",
            "BS-ART-20260826-04",
        ):
            self.assertIn(decision, overlay)

        self.assertIn("BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md", authority)
        self.assertIn("BS-REPAIR-20260826-29", authority)
        self.assertIn("BS-REPAIR-20260826-31", authority)
        self.assertIn("BS-DAMAGE-20260826-30", authority)
        self.assertIn("BS-ART-20260826-04", authority)
        self.assertIn("DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC", authority)
        self.assertIn("ACTUAL_GAME_CONSUMER_REQUIRED = TRUE", authority)
        self.assertIn("BS-REPAIR-20260826-29", current_owner)
        self.assertIn("BS-REPAIR-20260826-31", current_owner)
        self.assertIn("BS-DAMAGE-20260826-30", current_owner)
        self.assertIn("BS-ART-20260826-04", current_owner)
        self.assertIn("DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW", current_owner)

        self.assertLess(
            agents.index("BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"),
            agents.index("ACTIVE_CONTEXT.md"),
        )

    def test_legacy_active_context_and_20260811_phase_c_records_are_preserved_as_history(self) -> None:
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        agents = AGENTS.read_text(encoding="utf-8")

        self.assertIn("CURRENT_PRIORITY_OVERLAY", active[:2500])
        self.assertIn("BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION", active[:2500])
        self.assertIn("BS-OPS-20260811-03", active)
        self.assertIn("HISTORICAL", active)
        self.assertIn(
            "HISTORICAL_PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON",
            active,
        )

        self.assertIn("ACTIVE_CONTEXT.md` — `LEGACY_COMPATIBILITY_ROUTER", agents)
        self.assertIn("Decisions25~30/Art03~04", agents)
        self.assertNotIn("25~27/Art03", agents)


if __name__ == "__main__":
    unittest.main()
