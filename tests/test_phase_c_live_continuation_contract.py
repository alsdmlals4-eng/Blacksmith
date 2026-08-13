from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs" / "operations" / "BLACKSMITH_PHASE_C_LIVE_CONTINUATION.json"
GUIDE = ROOT / "docs" / "operations" / "BLACKSMITH_PHASE_C_LIVE_CONTINUATION.md"
AI_WORKFLOW = ROOT / "[기획서]" / "00_프로젝트_허브" / "AI_WORKFLOW.md"
A2 = ROOT / "docs" / "operations" / "BLACKSMITH_P2_CONTENT_RESULT_FOUNDATION_A2_CONTRACT.json"
DESIGN = ROOT / "docs" / "superpowers" / "specs" / "2026-08-13-blacksmith-content-result-foundation-design.md"
ADAPTER = ROOT / "skills" / "PROJECT_BASE_ADAPTER.json"
RECEIPT = (
    ROOT
    / "docs"
    / "superpowers"
    / "receipts"
    / "2026-08-12-bs-ops-20260811-03-local-runtime-and-bootstrap-fix.md"
)

P2_DECISION = "BS-VS-P2-20260813-01"
P2_MERGE_MAIN = "78eeb4c442a917051b327ddc050f9337b41516b0"
P2_EXACT_HEAD = "b0118e980df06c641c6b19372f364fa52a94b394"
P2_FULL_VALIDATION_RUN = 31653614060
P2_LIVE_EDITOR_PILOT_RUN = 31653614171
BASE_FOLLOW_UP = "alsdmlals4-eng/Base#314"


class PhaseCLiveContinuationContractTests(unittest.TestCase):
    def test_machine_state_records_p2_closure_and_fails_closed_on_next_scope(self) -> None:
        state = json.loads(STATE.read_text(encoding="utf-8"))

        self.assertEqual(1, state["schema_version"])
        self.assertEqual("BLACKSMITH_PHASE_C_LIVE_CONTINUATION", state["artifact_role"])
        self.assertEqual("BS-OPS-20260811-03", state["decision_id"])
        self.assertEqual("CLOSED_SUPERSEDED_UNMERGED", state["pr158"]["disposition"])
        self.assertEqual("HISTORICAL_REFERENCE_ONLY", state["pr158"]["branch_role"])

        checkpoint_sha = state["checkpoint"]["source_main_sha"]
        self.assertRegex(checkpoint_sha, re.compile(r"^[0-9a-f]{40}$"))
        self.assertEqual(P2_MERGE_MAIN, checkpoint_sha)
        self.assertEqual("FETCH_LATEST_MAIN_BEFORE_USE", state["checkpoint"]["resume_rule"])

        phase_c = state["phase_c"]
        self.assertEqual("APPROVED_WITHIN_EXISTING_CANON_ONLY", phase_c["scope"])
        self.assertEqual("UNSELECTED_USER_DECISION_REQUIRED", phase_c["next_package"])
        self.assertEqual("CLOSED_NO_ACTIVE_A2", phase_c["product_writer_gate"])
        self.assertEqual("NOT_SEPARATELY_APPROVED", phase_c["task3"])
        self.assertEqual("DEFERRED_BY_USER", phase_c["image_generation"])
        self.assertEqual(BASE_FOLLOW_UP, phase_c["base_follow_up_issue"])

        completed = phase_c["completed_package"]
        self.assertEqual("P2_CONTENT_RESULT_FOUNDATION", completed["package_id"])
        self.assertEqual(P2_DECISION, completed["decision_id"])
        self.assertEqual(162, completed["pr"])
        self.assertEqual(P2_EXACT_HEAD, completed["exact_head"])
        self.assertEqual(P2_MERGE_MAIN, completed["merge_main"])
        self.assertEqual(P2_FULL_VALIDATION_RUN, completed["postmerge_full_validation_run"])
        self.assertEqual("PASS", completed["postmerge_full_validation"])
        self.assertEqual(P2_LIVE_EDITOR_PILOT_RUN, completed["live_editor_pilot_run"])
        self.assertEqual("PASS", completed["live_editor_pilot"])

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
        self.assertEqual("A0_SHADOW", state["next_action"]["mode"])
        self.assertEqual(
            "SELECT_NEXT_EXISTING_CANON_PACKAGE_OR_REQUEST_NEW_DECISION",
            state["next_action"]["task"],
        )
        self.assertEqual("NOT_AUTHORIZED_BY_THIS_ARTIFACT", state["next_action"]["product_mutation"])

    def test_human_guide_records_p2_main_canon_and_no_inferred_next_package(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        for token in (
            "PR158_MERGE_UNIT: CLOSED_SUPERSEDED_UNMERGED",
            "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST",
            "P2_CONTENT_RESULT_FOUNDATION: MERGED_PR162_MAIN_CANON",
            f"P2_MERGE_MAIN: {P2_MERGE_MAIN}",
            f"P2_POSTMERGE_FULL_VALIDATION_RUN: {P2_FULL_VALIDATION_RUN}",
            "P2_POSTMERGE_FULL_VALIDATION: PASS",
            "NEXT_PHASE_C_PACKAGE: UNSELECTED_USER_DECISION_REQUIRED",
            "PRODUCT_WRITER_GATE: CLOSED_NO_ACTIVE_A2",
            "RECHECK_REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING",
            "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED",
            "TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE",
            BASE_FOLLOW_UP,
            "NO_MASS_ROUTER_REWRITE",
        ):
            self.assertIn(token, guide)
        self.assertNotIn("PHASE_C_NEXT_PACKAGE: P2_FOUNDATION_DATA_AND_STATE_CONTRACTS", guide)

    def test_ai_workflow_routes_to_closed_p2_and_user_selected_next_scope(self) -> None:
        workflow = AI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("BLACKSMITH_PHASE_C_LIVE_CONTINUATION.json", workflow)
        self.assertIn("BLACKSMITH_PHASE_C_LIVE_CONTINUATION.md", workflow)
        self.assertIn("RECHECK_REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING", workflow)
        self.assertIn("P2_CONTENT_RESULT_FOUNDATION: MERGED_PR162_MAIN_CANON", workflow)
        self.assertIn("NEXT_PHASE_C_PACKAGE: UNSELECTED_USER_DECISION_REQUIRED", workflow)
        self.assertIn("PRODUCT_WRITER_GATE: CLOSED_NO_ACTIVE_A2", workflow)
        self.assertIn(BASE_FOLLOW_UP, workflow)
        self.assertNotIn(
            "다음 기술 package는 `P2_FOUNDATION_DATA_AND_STATE_CONTRACTS`",
            workflow,
        )

    def test_p2_a2_contract_and_design_record_postmerge_truth(self) -> None:
        a2 = json.loads(A2.read_text(encoding="utf-8"))
        self.assertEqual(P2_DECISION, a2["decision_id"])
        self.assertEqual("MERGED_MAIN_VALIDATED", a2["status"])
        execution = a2["execution_state"]
        self.assertEqual(162, execution["implementation_pr"])
        self.assertEqual("SQUASH_MERGED", execution["branch_product_state"])
        self.assertEqual("PASS", execution["exact_head_validation"])
        self.assertEqual(P2_EXACT_HEAD, execution["exact_head"])
        self.assertEqual(P2_MERGE_MAIN, execution["main_canon"])
        self.assertEqual(P2_FULL_VALIDATION_RUN, execution["postmerge_full_validation_run"])
        self.assertEqual("PASS", execution["postmerge_full_validation"])
        self.assertEqual(P2_LIVE_EDITOR_PILOT_RUN, execution["live_editor_pilot_run"])
        self.assertEqual("PASS", execution["live_editor_pilot"])
        self.assertEqual(BASE_FOLLOW_UP, a2["adapter_governance_observation"]["follow_up_issue"])

        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("MERGED_MAIN_CANON", design)
        self.assertIn(P2_MERGE_MAIN, design)
        self.assertIn(f"Full Validation run `{P2_FULL_VALIDATION_RUN}`: `PASS`", design)
        self.assertIn(f"Live-Editor Pilot run `{P2_LIVE_EDITOR_PILOT_RUN}`: `PASS`", design)
        self.assertIn(BASE_FOLLOW_UP, design)

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
