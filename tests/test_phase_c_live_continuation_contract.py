from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs" / "operations" / "BLACKSMITH_PHASE_C_LIVE_CONTINUATION.json"
GUIDE = ROOT / "docs" / "operations" / "BLACKSMITH_PHASE_C_LIVE_CONTINUATION.md"
AI_WORKFLOW = ROOT / "[기획서]" / "00_프로젝트_허브" / "AI_WORKFLOW.md"
ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
RECEIPT = (
    ROOT
    / "docs"
    / "superpowers"
    / "receipts"
    / "2026-08-12-bs-ops-20260811-03-local-runtime-and-bootstrap-fix.md"
)


class PhaseCLiveContinuationContractTests(unittest.TestCase):
    def test_machine_state_preserves_scope_and_fails_closed_on_runtime_freshness(self) -> None:
        state = json.loads(STATE.read_text(encoding="utf-8"))

        self.assertEqual(1, state["schema_version"])
        self.assertEqual("BLACKSMITH_PHASE_C_LIVE_CONTINUATION", state["artifact_role"])
        self.assertEqual("BS-OPS-20260811-03", state["decision_id"])
        self.assertEqual("CLOSED_SUPERSEDED_UNMERGED", state["pr158"]["disposition"])
        self.assertEqual("HISTORICAL_REFERENCE_ONLY", state["pr158"]["branch_role"])

        checkpoint_sha = state["checkpoint"]["source_main_sha"]
        self.assertRegex(checkpoint_sha, re.compile(r"^[0-9a-f]{40}$"))
        self.assertEqual("FETCH_LATEST_MAIN_BEFORE_USE", state["checkpoint"]["resume_rule"])

        phase_c = state["phase_c"]
        self.assertEqual("APPROVED_WITHIN_EXISTING_CANON_ONLY", phase_c["scope"])
        self.assertEqual("P2_FOUNDATION_DATA_AND_STATE_CONTRACTS", phase_c["next_package"])
        self.assertEqual("SEPARATE_A2_CONTRACT_REQUIRED", phase_c["product_writer_gate"])
        self.assertEqual("NOT_SEPARATELY_APPROVED", phase_c["task3"])
        self.assertEqual("DEFERRED_BY_USER", phase_c["image_generation"])

        runtime = state["runtime"]
        self.assertEqual("PASS_AT_RECORDED_RECEIPT", runtime["last_observed_receipt_status"])
        self.assertEqual("NOT_RECHECKED_IN_THIS_GITHUB_SESSION", runtime["current_freshness"])
        self.assertEqual(
            "RECHECK_REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING",
            runtime["persistent_mutation_gate"],
        )
        self.assertNotEqual("OPEN", runtime["persistent_mutation_gate"])

        self.assertEqual(
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
            state["protected_paths"],
        )
        self.assertEqual([], state["leases"])
        self.assertEqual([], state["a3_auto_merge_allowlist"])
        self.assertEqual("NOT_CONFIGURED", state["scheduler_runtime_provider"])
        self.assertEqual(
            "TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE",
            state["sheet_sync_write_policy"],
        )

    def test_human_guide_preserves_compatibility_and_rejects_pr158_mass_rewrite(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        for token in (
            "PR158_MERGE_UNIT: CLOSED_SUPERSEDED_UNMERGED",
            "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST",
            "P2_FOUNDATION_DATA_AND_STATE_CONTRACTS",
            "RECHECK_REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING",
            "SEPARATE_A2_CONTRACT_REQUIRED",
            "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED",
            "TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE",
            "NO_MASS_ROUTER_REWRITE",
        ):
            self.assertIn(token, guide)

    def test_ai_workflow_routes_to_the_live_continuation_contract(self) -> None:
        workflow = AI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("BLACKSMITH_PHASE_C_LIVE_CONTINUATION.json", workflow)
        self.assertIn("BLACKSMITH_PHASE_C_LIVE_CONTINUATION.md", workflow)
        self.assertIn("RECHECK_REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING", workflow)
        self.assertIn("P2_FOUNDATION_DATA_AND_STATE_CONTRACTS", workflow)

    def test_existing_adapter_and_runtime_receipt_remain_unchanged_authorities(self) -> None:
        adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
        self.assertEqual("9.4.3", adapter["base_release"]["version"])
        self.assertEqual(
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
            adapter["protected_paths"],
        )

        receipt = RECEIPT.read_text(encoding="utf-8")
        self.assertIn("PERSISTENT_MUTATION_GATE: OPEN", receipt)
        self.assertIn("The current recheck was read-only", receipt)
        self.assertIn("HUMAN_PLAYTEST", receipt)
        self.assertIn("NOT_RUN", receipt)


if __name__ == "__main__":
    unittest.main()
