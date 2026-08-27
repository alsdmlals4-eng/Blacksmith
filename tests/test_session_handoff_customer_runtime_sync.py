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
            "CURRENT_RUNTIME_FOLLOWUP = CUSTOMER_EVENT_SCHEDULER_AND_PLAYER_ENTRY_UNDECIDED",
            handoff,
        )
        self.assertIn("CUSTOMER_WORLD_RESULT_SURFACE = IMPLEMENTED_PR278", handoff)
        self.assertIn(
            "CUSTOMER_WORLD_RESULT_FLOW_CALLER = IMPLEMENTED_PR286", handoff
        )
        self.assertIn("CUSTOMER_WORLD_EVENT_SCHEDULER_AND_PLAYER_ENTRY = NOT_RUN", handoff)
        self.assertIn("same stored fact", handoff)

    def test_handoff_records_the_retired_approval_and_current_baseline(self):
        handoff = HANDOFF_PATH.read_text(encoding="utf-8")

        self.assertIn(
            "OPERATING_CONTRACT_BASELINE = b2f3b994c92eee68eafbab1a90a8084e2924553c",
            handoff,
        )
        self.assertIn(
            "PROTECTED_CHANGE_APPROVAL = CONSUMED_AND_RETIRED_BY_PR288", handoff
        )


if __name__ == "__main__":
    unittest.main()
