from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
HEALTH_PATH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"
STATE_PATH = ROOT / "docs/PROJECT_OPERATING_STATE.json"
MIGRATION_PATH = ROOT / "docs/operations/PROJECT_BASE_ADAPTER_MIGRATION_2026-08-06.md"
WORKFLOW_PATH = ROOT / ".github/workflows/validate-project-base-adapter.yml"

EXPECTED_ROOT_KEYS = {
    "artifact_role", "base_release", "compatibility", "gdd_sheet",
    "project", "protected_baseline", "protected_paths", "routing",
    "schema_version", "shared_overrides", "skill_registry", "validators",
}
FORBIDDEN_ROOT_KEYS = {
    "current_operating_decisions", "project_operating_state",
    "current_r1_canon", "validation_status",
}
BASE_KEYS = {
    "repository", "version", "release_commit",
    "release_evidence_commit", "finalization_commit",
}
COMPATIBILITY_KEYS = {"cycle", "views", "legacy_inputs"}
ROUTING_KEYS = {
    "base_routes", "project_routes", "inactive_routes", "aliases", "precedence",
}
BASELINE_KEYS = {
    "commit", "authority_kind", "authority_ref", "policy_source_type",
    "policy_source_path", "protected_paths_pointer", "policy_sha256",
}
REGISTRY_KEYS = {"path", "sha256", "hash_definition"}
HEALTH_KEYS = {
    "schema_version", "artifact_role", "operating_maturity",
    "product_evidence_maturity", "critical_gates", "integrity_verdict", "evidence",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
TRUSTED_BASE = "bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1"
PR_BASE = "b1dd945875568098b107815a03e88b0272d384e9"
DECISION = "DEC-BASE-20260805-001"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class BlacksmithThinAdapterMigrationTests(unittest.TestCase):
    def test_adapter_root_is_strict_and_project_state_is_removed(self) -> None:
        adapter = load_json(ADAPTER_PATH)
        self.assertEqual(EXPECTED_ROOT_KEYS, set(adapter))
        self.assertTrue(FORBIDDEN_ROOT_KEYS.isdisjoint(adapter))
        self.assertEqual(BASE_KEYS, set(adapter["base_release"]))
        self.assertEqual(COMPATIBILITY_KEYS, set(adapter["compatibility"]))
        self.assertEqual(ROUTING_KEYS, set(adapter["routing"]))
        self.assertEqual(BASELINE_KEYS, set(adapter["protected_baseline"]))

    def test_routes_and_validators_use_canonical_shapes(self) -> None:
        adapter = load_json(ADAPTER_PATH)
        for group in ("base_routes", "project_routes"):
            for route in adapter["routing"][group]:
                self.assertEqual({"route_id", "skill_id", "status"}, set(route))
                self.assertEqual("ACTIVE", route["status"])
        for route in adapter["routing"]["inactive_routes"]:
            self.assertIn(route["status"], {"INACTIVE", "HOLD", "RETIRED"})
        self.assertTrue(adapter["validators"])
        self.assertTrue(all(isinstance(value, str) for value in adapter["validators"]))
        self.assertFalse(any(value.startswith("manual:") for value in adapter["validators"]))

    def test_baseline_sheet_and_registries_are_current_and_complete(self) -> None:
        adapter = load_json(ADAPTER_PATH)
        baseline = adapter["protected_baseline"]
        self.assertEqual(PR_BASE, baseline["commit"])
        self.assertEqual("REMOTE_TRACKING_REF", baseline["authority_kind"])
        self.assertEqual("refs/remotes/origin/main", baseline["authority_ref"])
        self.assertEqual("CANONICAL_ADAPTER_SOURCE", baseline["policy_source_type"])
        self.assertEqual("skills/PROJECT_BASE_ADAPTER.json", baseline["policy_source_path"])
        self.assertRegex(baseline["policy_sha256"], SHA256)
        self.assertEqual("CURRENT", adapter["gdd_sheet"]["sync_status"])
        for registry in adapter["skill_registry"].values():
            self.assertEqual(REGISTRY_KEYS, set(registry))
            self.assertEqual("RAW_FILE_BYTES_SHA256", registry["hash_definition"])
            self.assertRegex(registry["sha256"], SHA256)

    def test_removed_state_and_original_health_are_preserved(self) -> None:
        state_doc = load_json(STATE_PATH)
        migration = state_doc["adapter_migration"]
        self.assertEqual(DECISION, migration["decision_id"])
        self.assertEqual(PR_BASE, migration["source_main_commit"])
        preserved = migration["preserved_from_adapter"]
        for key in FORBIDDEN_ROOT_KEYS:
            self.assertIn(key, preserved)
        state = preserved["project_operating_state"]
        self.assertEqual("R2_CORE_SESSION_META_LOOP", state["stage"])
        self.assertEqual("BS-WORLD-20260803-02", state["current_r2_decision"])
        self.assertEqual("BLOCKED", state["product_implementation"])
        self.assertEqual("NOT_RUN", state["new_r2_runtime_validation"])
        self.assertEqual("NOT_RUN", state["human_playtest"])
        self.assertEqual("PASS_5_OF_5", preserved["validation_status"]["pr_99_workflows"])
        self.assertIn("original_project_operating_health", migration)

    def test_health_uses_base_machine_contract_only(self) -> None:
        health = load_json(HEALTH_PATH)
        self.assertEqual(HEALTH_KEYS, set(health))
        self.assertEqual("PROJECT_OPERATING_HEALTH", health["artifact_role"])
        self.assertEqual("OM-L3", health["operating_maturity"])
        self.assertEqual("PE-0", health["product_evidence_maturity"])
        self.assertEqual("PASS_WITH_NOT_RUN_GATES", health["integrity_verdict"])
        self.assertEqual("PASS", health["critical_gates"]["static"])
        self.assertEqual("NOT_RUN", health["critical_gates"]["runtime"])
        self.assertEqual("NOT_RUN", health["critical_gates"]["human"])

    def test_migration_map_and_workflow_bind_the_approved_contract(self) -> None:
        migration = MIGRATION_PATH.read_text(encoding="utf-8")
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        for token in (
            DECISION, "/current_operating_decisions", "/project_operating_state",
            "/current_r1_canon", "/validation_status",
            "docs/PROJECT_OPERATING_STATE.json", "PRODUCT_FILES_UNCHANGED",
            "GOOGLE_SHEETS_UNCHANGED",
        ):
            self.assertIn(token, migration)
        self.assertIn(TRUSTED_BASE, workflow)
        self.assertIn("check_project_operating_contract.py", workflow)
        self.assertIn("test_project_base_adapter_thin_migration", workflow)


if __name__ == "__main__":
    unittest.main()
