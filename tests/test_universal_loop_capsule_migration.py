from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / "docs/operations/loop"
SOURCE = "c969c8ed9c6306f60c851fc85ed97e0ffa885305"
PROJECT = "BLACKSMITH"
PACKAGE = "BS_LOOP_MIGRATION_PKG_001"
REQUIREMENT = "BS_LOOP_MIGRATION_001"


def load(name: str):
    path = LOOP / name
    if not path.is_file():
        raise AssertionError(f"missing Universal Loop contract: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


class UniversalLoopCapsuleMigrationTests(unittest.TestCase):
    def test_bundle_identity_authority_and_closed_autonomy(self) -> None:
        capsule = load("PROJECT_EXECUTION_CAPSULE.json")
        planning = load("PLANNING_LOCK.json")
        visual = load("VISUAL_LOCK.json")
        package = load("IMPLEMENTATION_PACKAGE.json")
        coverage = load("REQUIREMENT_COVERAGE_LEDGER.json")
        active = load("ACTIVE_LOOP_RUN.json")
        immutable = load("runs/BS_LOOP_MIGRATION_001.json")

        self.assertEqual(capsule["contract_role"], "LOOP_PROJECT_EXECUTION_CAPSULE")
        self.assertEqual(capsule["project_id"], PROJECT)
        self.assertEqual(capsule["source_main_sha"], SOURCE)
        self.assertEqual(capsule["autonomy"], "A2_EXECUTE_ISOLATED")
        self.assertEqual(capsule["a3_auto_merge_allowlist"], [])
        self.assertEqual(capsule["scheduler_runtime_provider"], "NOT_CONFIGURED")
        self.assertEqual(active["contract_role"], "LOOP_ACTIVE_RUN_POINTER")
        self.assertEqual(active["active_run"], None)
        for value, key in ((planning, "source_commit"), (visual, "source_commit"), (package, "source_main_sha"), (coverage, "source_main_sha"), (active, "source_main_sha"), (immutable, "source_main_sha")):
            self.assertEqual(value[key], SOURCE)
        for value in (planning, visual, package, coverage, active, immutable):
            self.assertEqual(value["project_id"], PROJECT)

    def test_planning_lock_points_to_existing_canon_without_selecting_new_product_scope(self) -> None:
        planning = load("PLANNING_LOCK.json")
        self.assertEqual(planning["status"], "PLANNING_LOCKED")
        self.assertEqual(planning["user_review"]["status"], "APPROVED")
        self.assertEqual([item["requirement_id"] for item in planning["approved_requirements"]], [REQUIREMENT])
        source_paths = {item["path"] for item in planning["authority_sources"]}
        self.assertTrue({
            "AGENTS.md",
            "CURRENT_CONFIRMED_DECISIONS.md",
            "docs/operations/BLACKSMITH_PHASE_C_LIVE_CONTINUATION.json",
        }.issubset(source_paths))
        for item in planning["authority_sources"]:
            self.assertEqual(item["source_commit"], SOURCE)
            self.assertTrue((ROOT / item["path"]).is_file())
        protected = "\n".join(planning["protected_meanings"] + planning["excluded_scope"])
        for marker in (
            "PROJECT_CORE",
            "CRAFTING",
            "ITEM_UID",
            "SAVE",
            "MAJOR_UX",
            "TASK3",
            "NEW_PRODUCT_SCOPE",
        ):
            self.assertIn(marker, protected)

    def test_migration_package_is_operations_only_and_visual_not_applicable(self) -> None:
        visual = load("VISUAL_LOCK.json")
        package = load("IMPLEMENTATION_PACKAGE.json")
        self.assertEqual(visual["status"], "VISUAL_NOT_APPLICABLE")
        self.assertEqual(visual["provider"], "NONE")
        self.assertEqual(package["package_id"], PACKAGE)
        self.assertEqual(package["requirement_ids"], [REQUIREMENT])
        self.assertEqual(package["visual_impact"], "NONE")
        self.assertEqual(package["visual_lock_requirement"], "VISUAL_NOT_APPLICABLE")
        self.assertEqual(package["execution_gate"], "AUTONOMOUS_IMPLEMENTATION_READY")
        allowed_tests = {
            "tests/test_universal_loop_capsule_migration.py",
            "tests/test_vertical_slice_task1_canon_contract.py",
        }
        for path in package["allowed_paths"]:
            self.assertTrue(path.startswith("docs/operations/loop/") or path in allowed_tests)
        forbidden = set(package["forbidden_paths"])
        self.assertTrue({"data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"}.issubset(forbidden))
        self.assertIn("docs/operations/BLACKSMITH_LOOP_ENGINEERING_PROFILE.md", forbidden)
        self.assertIn("docs/operations/BLACKSMITH_LOOP_RUN_CONTRACT.json", forbidden)

    def test_coverage_maps_every_package_requirement_and_output(self) -> None:
        package = load("IMPLEMENTATION_PACKAGE.json")
        coverage = load("REQUIREMENT_COVERAGE_LEDGER.json")
        self.assertEqual(coverage["package_id"], PACKAGE)
        self.assertEqual(coverage["status"], "INITIALIZED")
        self.assertEqual([item["requirement_id"] for item in coverage["requirements"]], package["requirement_ids"])
        mapped = {path for item in coverage["requirements"] for path in item["outputs"]}
        self.assertEqual(mapped, set(package["allowed_paths"]))
        entry = coverage["requirements"][0]
        self.assertTrue(entry["tasks"] and entry["tests"] and entry["evidence"])
        self.assertIn("tests/test_universal_loop_capsule_migration.py", entry["tests"])

    def test_runtime_adapter_preserves_product_protected_roots(self) -> None:
        adapter = load("RUNTIME_ADAPTER.json")
        self.assertEqual(adapter["contract_role"], "LOOP_RUNTIME_ADAPTER")
        self.assertEqual(adapter["status"], "PROJECT_ADAPTER_VALIDATED")
        self.assertEqual(adapter["engine"], {"name": "Godot", "version": "4.7.1"})
        self.assertTrue({"data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"}.issubset(set(adapter["protected_paths"])))
        self.assertEqual(len(adapter["test_commands"]), 1)
        self.assertEqual(adapter["test_commands"][0]["argv"], ["python", "-m", "unittest", "tests.test_universal_loop_capsule_migration", "-v"])
        self.assertEqual(adapter["test_commands"][0]["network"], "DENIED")

    def test_legacy_pilot_evidence_remains_present_and_new_run_is_not_active(self) -> None:
        self.assertTrue((ROOT / "docs/operations/BLACKSMITH_LOOP_ENGINEERING_PROFILE.md").is_file())
        self.assertTrue((ROOT / "docs/operations/BLACKSMITH_LOOP_RUN_CONTRACT.json").is_file())
        active = load("ACTIVE_LOOP_RUN.json")
        immutable = load("runs/BS_LOOP_MIGRATION_001.json")
        self.assertIsNone(active["active_run"])
        self.assertEqual(immutable["run_id"], "BS_LOOP_MIGRATION_001")
        self.assertEqual(immutable["state"], "CREATED")
        self.assertEqual(immutable["design_drift_status"], "NOT_CHECKED")


if __name__ == "__main__":
    unittest.main()
