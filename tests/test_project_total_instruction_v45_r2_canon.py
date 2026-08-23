from __future__ import annotations

import hashlib
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md"
DECISION = ROOT / "docs/decisions/BS-OPS-20260811-01_PROJECT_INSTRUCTION_V45_R2_CANON.md"
AGENTS = ROOT / "AGENTS.md"
ACTIVE = ROOT / "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
DOCMAP = ROOT / "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md"
EXPECTED_SOURCE_SHA256 = "3f898b7e2749a2e1900e9df48183f02d4fbc735fd0e80297f28bb09317144de4"


class ProjectTotalInstructionV45R2CanonTests(unittest.TestCase):
    def test_canonical_instruction_is_exact_v45_r2_source(self) -> None:
        self.assertTrue(CANON.is_file(), str(CANON))
        payload = CANON.read_bytes()
        self.assertEqual(hashlib.sha256(payload).hexdigest(), EXPECTED_SOURCE_SHA256)
        text = payload.decode("utf-8")
        for token in (
            "contract_name: PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION",
            "contract_version: '4.5'",
            "revision: '2026-08-11-r2'",
            "execution_scope_guard: INSTRUCTION_DOCUMENT_UPDATE_ONLY_UNLESS_EXPLICIT_FUTURE_EXECUTION_REQUEST",
            "current_conversation_merge_policy: RECOMMENDED_AUTO_APPROVAL_WITHIN_ALREADY_APPROVED_SCOPE",
        ):
            self.assertIn(token, text)

    def test_current_blacksmith_override_is_explicit_and_non_destructive(self) -> None:
        self.assertTrue(DECISION.is_file(), str(DECISION))
        decision = DECISION.read_text(encoding="utf-8")
        for token in (
            "BS-OPS-20260811-01",
            EXPECTED_SOURCE_SHA256,
            "SOURCE_VERBATIM_CANON",
            "SOURCE_PATH_CONFLICT_EXPLICIT_OVERRIDE",
            "alsdmlals4-eng/Blacksmith",
            r"C:\Users\user\Documents\GitHub\Ninza\Blacksmith",
            "C:/Users/user/Documents/GitHub/Ninza/Blacksmith",
            "Switchy-Express-Cargo-Puzzle",
            "DO_NOT_EDIT_SOURCE_TO_HIDE_CONFLICT",
        ):
            self.assertIn(token, decision)

    def test_historical_instruction_stays_reachable_without_overriding_current_overlay(self) -> None:
        # AGENTS/Documentation Map retain the immutable v4.5-r2 compatibility route.
        for path in (AGENTS, DOCMAP):
            text = path.read_text(encoding="utf-8")
            self.assertIn("PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md", text, str(path))
            self.assertIn("BS-OPS-20260811-01", text, str(path))

        # Active Context must still expose the stored instruction path for provenance,
        # but the current execution route is the newer 2026-08-20 planning overlay.
        active = ACTIVE.read_text(encoding="utf-8")
        self.assertIn("PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md", active)
        self.assertIn("CURRENT_PRIORITY_OVERLAY", active[:2500])
        self.assertIn("CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md", active[:2500])
        self.assertIn("WORK_INSTRUCTION: CURRENT_USER_TASK_OVERLAY_OVER_HISTORICAL_V4_5_R2", active)
        self.assertIn("PROJECT_LOCAL_PATH: C:\\Users\\user\\Documents\\GitHub\\Ninza\\Blacksmith", active)
        self.assertIn("GODOT_PROJECT_PATH: C:/Users/user/Documents/GitHub/Ninza/Blacksmith", active)
        self.assertIn("PRODUCT_IMPLEMENTATION: BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION", active)
        self.assertIn("TASK3_IMPLEMENTATION: NOT_APPROVED", active)
        self.assertNotIn("WORK_INSTRUCTION: V4_5_R2_CURRENT_CANON", active)


if __name__ == "__main__":
    unittest.main()
