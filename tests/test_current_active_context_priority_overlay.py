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

        self.assertIn("CURRENT_PRIORITY_OVERLAY", overlay)
        self.assertIn("BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION", overlay)
        self.assertIn("BS-ENHANCE-20260825-25", overlay)
        self.assertIn("BS-DAMAGE-20260825-26", overlay)
        self.assertIn("BS-DAMAGE-20260826-28", overlay)
        self.assertIn("BS-CHRONICLE-20260825-27", overlay)
        self.assertIn("BS-ART-20260825-03", overlay)

        self.assertIn("BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md", authority)
        self.assertIn("BS-ENHANCE-20260825-25", current_owner)
        self.assertIn("BS-DAMAGE-20260825-26", current_owner)
        self.assertIn("BS-DAMAGE-20260826-28", current_owner)

        self.assertLess(
            agents.index("BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"),
            agents.index("ACTIVE_CONTEXT.md"),
        )

    def test_legacy_active_context_and_20260811_phase_c_records_are_preserved_as_history(self) -> None:
        active = ACTIVE_CONTEXT.read_text(encoding="utf-8")
        agents = AGENTS.read_text(encoding="utf-8")

        # The old router is retained for provenance/compatibility. It is not
        # rewritten to pretend its 2026-08-20 snapshot is today's authority.
        self.assertIn("CURRENT_PRIORITY_OVERLAY", active[:2500])
        self.assertIn("BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION", active[:2500])
        self.assertIn("BS-OPS-20260811-03", active)
        self.assertIn("HISTORICAL", active)
        self.assertIn(
            "HISTORICAL_PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON",
            active,
        )

        # Current routing explicitly demotes this frozen snapshot instead of
        # making history mutable every time a successor decision lands.
        self.assertIn("ACTIVE_CONTEXT.md` — `LEGACY_COMPATIBILITY_ROUTER", agents)
        self.assertIn("25~28/Art03", agents)
        self.assertNotIn("25~27/Art03", agents)


if __name__ == "__main__":
    unittest.main()
