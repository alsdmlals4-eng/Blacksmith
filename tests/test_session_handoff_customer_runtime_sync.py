"""현재 고객 실제사용 결과 화면의 인수인계 상태를 고정한다."""

from pathlib import Path
import unittest


HANDOFF_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "operations"
    / "BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
)


class CustomerRuntimeHandoffSyncContractTest(unittest.TestCase):
    def test_handoff_separates_completed_result_surface_from_unimplemented_caller(self):
        handoff = HANDOFF_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "CURRENT_RUNTIME_FOLLOWUP = SELECT_NEXT_APPROVED_CURRENT_CANON_ISSUE / NO_SCOPE_AUTOMATICALLY_OPENED",
            handoff,
        )
        self.assertIn("CUSTOMER_WORLD_RESULT_SURFACE = IMPLEMENTED_PR278", handoff)
        self.assertIn(
            "CUSTOMER_WORLD_RESULT_FLOW_CALLER = IMPLEMENTED_PR286", handoff
        )
        self.assertIn("CUSTOMER_WORLD_EVENT_SCHEDULER = NOT_RUN", handoff)
        self.assertIn(
            "PHASE1_PLAYER_HANDOFF_ENTRY = IMPLEMENTED_PR334 / SAVE_FIRST_ONCE_PER_UID",
            handoff,
        )
        self.assertIn("same stored fact", handoff)

    def test_handoff_records_the_retired_approval_and_current_baseline(self):
        handoff = HANDOFF_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "OPERATING_CONTRACT_BASELINE = 004e519a8891e3ef897cb32f67c58082a9d6a696",
            handoff,
        )
        self.assertIn(
            "PROTECTED_CHANGE_APPROVAL = CONSUMED_AND_RETIRED_BY_PR294", handoff
        )

    def test_handoff_records_the_merged_phase1_player_flow_not_a_worktree_candidate(self):
        handoff = HANDOFF_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "IMPLEMENTATION_STATUS = MERGED_MAIN_MACHINE_VERIFIED / PR334 / a2489bf039c2080c7851959cc6582ab6a56645fc",
            handoff,
        )
        self.assertIn(
            "PROTECTED_CHANGE_APPROVAL = CONSUMED_AND_RETIRED_BY_PR335 / 4e9bbf7a4ac47cbbdf45b22e07322ae4d927e7cc",
            handoff,
        )


if __name__ == "__main__":
    unittest.main()
