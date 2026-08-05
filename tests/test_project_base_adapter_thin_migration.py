from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
HEALTH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"
MIGRATION = ROOT / "docs/operations/BLACKSMITH_ADAPTER_MIGRATION_STATE_2026-08-06.json"


class BlacksmithThinAdapterMigrationTests(unittest.TestCase):
    def test_project_state_is_preserved_outside_the_thin_adapter(self) -> None:
        adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
        state = json.loads(MIGRATION.read_text(encoding="utf-8"))
        for key in ("current_operating_decisions", "project_operating_state", "current_r1_canon"):
            self.assertNotIn(key, adapter)
            self.assertIn(key, state["migrated_adapter_root_fields"])
        self.assertIn("legacy_project_operating_health", state)
        self.assertEqual("DEC-BASE-20260805-001", state["decision_id"])

    def test_adapter_uses_canonical_route_validator_and_baseline_shapes(self) -> None:
        adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
        for key in ("base_routes", "project_routes", "inactive_routes"):
            for route in adapter["routing"][key]:
                self.assertEqual({"route_id", "skill_id", "status"}, set(route))
        self.assertTrue(all(isinstance(command, str) and command for command in adapter["validators"]))
        self.assertIn(adapter["protected_baseline"]["authority_kind"], {"REMOTE_TRACKING_REF", "GITHUB_PR_BASE"})
        self.assertIn(adapter["protected_baseline"]["policy_source_type"], {"FIRST_MIGRATION_LEGACY_SOURCE", "CANONICAL_ADAPTER_SOURCE"})
        self.assertEqual("CURRENT", adapter["gdd_sheet"]["sync_status"])

    def test_operating_health_is_the_strict_base_view_with_migration_evidence(self) -> None:
        health = json.loads(HEALTH.read_text(encoding="utf-8"))
        self.assertEqual("PROJECT_OPERATING_HEALTH", health["artifact_role"])
        self.assertEqual(1, health["schema_version"])
        self.assertEqual({"static", "runtime", "device", "accessibility", "human"}, set(health["critical_gates"]))
        sources = {item["source"] for item in health["evidence"]["operating"]}
        self.assertIn("docs/operations/BLACKSMITH_ADAPTER_MIGRATION_STATE_2026-08-06.json", sources)


if __name__ == "__main__":
    unittest.main()
