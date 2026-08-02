from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
PAYLOAD = "dd705d7f48a7919187bc0507610ba5fc5b43a658"
EVIDENCE = "0c6cdd128bf1f5782e96b3a6240c9585f8d1ef6d"
FINALIZATION = "ac9466edc2d93b59f274c9ac55ca719eba2809e3"
REGISTRY = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"


def load() -> dict:
    return json.loads(ADAPTER.read_text(encoding="utf-8"))


class BaseV942PlanningFirstAdoptionTests(unittest.TestCase):
    def test_release_identity(self) -> None:
        adapter = load()
        release = adapter["base_release"]
        self.assertEqual("9.4.2", release["version"])
        self.assertEqual(PAYLOAD, release["release_commit"])
        self.assertEqual(EVIDENCE, release["release_evidence_commit"])
        self.assertEqual(FINALIZATION, release["finalization_commit"])
        self.assertEqual(REGISTRY, adapter["skill_registry"]["base"]["sha256"])

    def test_intake_route_and_batch_contract(self) -> None:
        adapter = load()
        active = {route["skill_id"] for route in adapter["routing"]["base_routes"] if route.get("status") == "ACTIVE"}
        self.assertIn("managing-project-intake-and-work-contract", active)
        policy = adapter["shared_overrides"]["managing-project-intake-and-work-contract"]["planning_first_governance"]
        self.assertEqual("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md", policy["base_contract_source"])
        self.assertEqual("templates/project-operations/GRILL_ME_BATCH_CHECKPOINT.md", policy["checkpoint_template"])
        self.assertEqual("base-v9.4.2.lock.json", policy["base_release_lock"])
        self.assertEqual(10, policy["max_approved_decisions_per_batch"])
        self.assertEqual("RECOMMENDED_DEFAULT", policy["numeric_default_state"])
        self.assertEqual("GRILL_ME_REQUIRED", policy["planning_conflict_state"])
        self.assertEqual("APPROVED_PENDING_MERGE", policy["pre_merge_sheet_state"])
        self.assertEqual("SYNCED_TO_MAIN", policy["post_merge_sheet_state"])
        self.assertEqual("NOT_RUN", policy["actual_project_batch_execution"])

    def test_blacksmith_boundaries_remain_truthful(self) -> None:
        adapter = load()
        self.assertEqual("BLOCKED_UNVERIFIED", adapter["compatibility"]["view_freshness"])
        self.assertEqual("DO_NOT_HAND_EDIT_GENERATED_COMPATIBILITY_VIEWS", adapter["compatibility"]["manual_edit_policy"])
        self.assertEqual("BLOCKED", adapter["project_operating_state"]["product_implementation"])
        self.assertEqual("NOT_RUN", adapter["project_operating_state"]["human_playtest"])


if __name__ == "__main__":
    unittest.main()
