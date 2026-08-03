from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"


def load() -> dict:
    return json.loads(ADAPTER.read_text(encoding="utf-8"))


class PlanningFirstCompatibilityTests(unittest.TestCase):
    def test_v943_preserves_planning_first_contract(self) -> None:
        adapter = load()
        release = adapter["base_release"]
        self.assertEqual("9.4.3", release["version"])
        self.assertEqual("7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8", release["release_commit"])
        self.assertEqual("da33a350d61b8adc52df97fccc7001708a933370", release["release_evidence_commit"])
        self.assertEqual("0b7c94f38d959efc0fc9442274c60b2e268a3c97", release["finalization_commit"])
        self.assertEqual("693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59", adapter["skill_registry"]["base"]["sha256"])

    def test_intake_route_and_batch_contract(self) -> None:
        adapter = load()
        active = {
            route if isinstance(route, str) else route["skill_id"]
            for route in adapter["routing"]["base_routes"]
            if isinstance(route, str) or route.get("status") == "ACTIVE"
        }
        self.assertIn("managing-project-intake-and-work-contract", active)
        policy = adapter["shared_overrides"]["managing-project-intake-and-work-contract"]["planning_first_governance"]
        self.assertEqual("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md", policy["base_contract_source"])
        self.assertEqual("templates/project-operations/GRILL_ME_BATCH_CHECKPOINT.md", policy["checkpoint_template"])
        self.assertEqual("base-v9.4.3.lock.json", policy["base_release_lock"])
        self.assertEqual(10, policy["max_approved_decisions_per_batch"])
        self.assertEqual("RECOMMENDED_DEFAULT", policy["numeric_default_state"])
        self.assertEqual("GRILL_ME_REQUIRED", policy["planning_conflict_state"])
        self.assertEqual("APPROVED_PENDING_MERGE", policy["pre_merge_sheet_state"])
        self.assertEqual("SYNCED_TO_MAIN", policy["post_merge_sheet_state"])
        self.assertEqual("EXECUTED_R2_CHECKPOINT_001", policy["actual_project_batch_execution"])
        self.assertEqual("BS-OPS-20260803-06", policy["current_checkpoint"])
        self.assertEqual("BS-WORLD-20260803-02", policy["current_approved_decision"])
        self.assertEqual("AUTHORITY_DRIFT_EARLY_CHECKPOINT", policy["checkpoint_reason"])
        self.assertEqual("0/10", policy["next_counter"])

    def test_blacksmith_current_state_and_boundaries_remain_truthful(self) -> None:
        adapter = load()
        state = adapter["project_operating_state"]
        self.assertEqual("R2_CORE_SESSION_META_LOOP", state["stage"])
        self.assertEqual("R2_CHECKPOINT_001_CANON_NEXT_GRILL_ME_COUNTER_0_OF_10", state["stage_status"])
        self.assertEqual(98, state["last_merged_pr"])
        self.assertEqual("8df4a10241bfa0c07211402d7c8c0e3e1f1e1249", state["r1_final_approval_merge_commit"])
        self.assertEqual("R1_COMPLETE_R2_ACTIVE", state["planning_coverage"])
        self.assertEqual("BLOCKED_UNVERIFIED", adapter["compatibility"]["view_freshness"])
        self.assertEqual("DO_NOT_HAND_EDIT_GENERATED_COMPATIBILITY_VIEWS", adapter["compatibility"]["manual_edit_policy"])
        self.assertEqual("BLOCKED", state["product_implementation"])
        self.assertEqual("NOT_RUN", state["human_playtest"])

    def test_sheet_and_protected_baseline_are_current(self) -> None:
        adapter = load()
        sheet = adapter["gdd_sheet"]
        self.assertIn("BS-WORLD-20260803-02", sheet["sync_decision_ids"])
        self.assertIn("BS-OPS-20260803-06", sheet["sync_decision_ids"])
        self.assertEqual("SYNCED_TO_MAIN_AFTER_CHECKPOINT_MERGE", sheet["sync_status"])
        self.assertEqual("8df4a10241bfa0c07211402d7c8c0e3e1f1e1249", adapter["protected_baseline"]["commit"])
        self.assertEqual(
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
            adapter["protected_paths"],
        )


if __name__ == "__main__":
    unittest.main()
