from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / "docs/operations/loop"
PHASE_C = ROOT / "docs/operations/BLACKSMITH_PHASE_C_LIVE_CONTINUATION.json"
SOURCE = "5267f542ef6ce99f98b3b407e42b146b5672335b"
PROJECT = "BLACKSMITH"
PACKAGE = "BS_A2_BURNIN_TEST_ONLY_PKG_001"
REQUIREMENT = "BS_A2_BURNIN_TEST_ONLY_001"
IMMUTABLE = "runs/BS_A2_BURNIN_AUTHORITY_001.json"
MARKER = "docs/operations/loop/burnin/BS_A2_BURNIN_MARKER.txt"
MARKER_CONTENT = "BLACKSMITH_A2_BURNIN_V1\n"
APPROVAL = "USER_APPROVAL_RECOMMENDED_UNATTENDED_A2_BURNIN_20260815"


def load(relative: str):
    path = LOOP / relative
    if not path.is_file():
        raise AssertionError(f"missing Universal Loop contract: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


class UniversalLoopA2BurninAuthorityTests(unittest.TestCase):
    def test_bundle_is_rebased_to_exact_current_main_without_opening_a3_or_scheduler(self) -> None:
        capsule = load("PROJECT_EXECUTION_CAPSULE.json")
        planning = load("PLANNING_LOCK.json")
        visual = load("VISUAL_LOCK.json")
        package = load("IMPLEMENTATION_PACKAGE.json")
        coverage = load("REQUIREMENT_COVERAGE_LEDGER.json")
        active = load("ACTIVE_LOOP_RUN.json")
        immutable = load(IMMUTABLE)

        self.assertEqual(capsule["project_id"], PROJECT)
        self.assertEqual(capsule["source_main_sha"], SOURCE)
        self.assertEqual(capsule["immutable_run_path"], IMMUTABLE)
        self.assertEqual(capsule["autonomy"], "A2_EXECUTE_ISOLATED")
        self.assertEqual(capsule["a3_auto_merge_allowlist"], [])
        self.assertEqual(capsule["scheduler_runtime_provider"], "NOT_CONFIGURED")
        self.assertEqual(active["contract_role"], "LOOP_ACTIVE_RUN_POINTER")
        self.assertIsNone(active["active_run"])

        for value, key in (
            (planning, "source_commit"),
            (visual, "source_commit"),
            (package, "source_main_sha"),
            (coverage, "source_main_sha"),
            (active, "source_main_sha"),
            (immutable, "source_main_sha"),
        ):
            self.assertEqual(value[key], SOURCE)
            self.assertEqual(value["project_id"], PROJECT)

    def test_planning_lock_approves_transport_burnin_only_and_preserves_product_decision_gate(self) -> None:
        planning = load("PLANNING_LOCK.json")
        phase = json.loads(PHASE_C.read_text(encoding="utf-8"))

        self.assertEqual(planning["status"], "PLANNING_LOCKED")
        self.assertEqual(planning["user_review"], {"status": "APPROVED", "approval_ref": APPROVAL})
        self.assertEqual(
            [item["requirement_id"] for item in planning["approved_requirements"]],
            [REQUIREMENT],
        )
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
            "ART_DIRECTION",
            "UNSELECTED_USER_DECISION_REQUIRED",
            "TASK3",
        ):
            self.assertIn(marker, protected)

        self.assertEqual(phase["phase_c"]["next_package"], "UNSELECTED_USER_DECISION_REQUIRED")
        self.assertEqual(phase["phase_c"]["product_writer_gate"], "CLOSED_NO_ACTIVE_A2")
        self.assertEqual(phase["phase_c"]["task3"], "NOT_SEPARATELY_APPROVED")

    def test_package_allows_exactly_one_non_product_runtime_marker(self) -> None:
        visual = load("VISUAL_LOCK.json")
        package = load("IMPLEMENTATION_PACKAGE.json")

        self.assertEqual(visual["status"], "VISUAL_NOT_APPLICABLE")
        self.assertEqual(visual["provider"], "NONE")
        self.assertEqual(package["package_id"], PACKAGE)
        self.assertEqual(package["requirement_ids"], [REQUIREMENT])
        self.assertEqual(package["allowed_paths"], [MARKER])
        self.assertEqual(package["visual_impact"], "NONE")
        self.assertEqual(package["visual_lock_requirement"], "VISUAL_NOT_APPLICABLE")
        self.assertEqual(package["execution_gate"], "AUTONOMOUS_IMPLEMENTATION_READY")
        self.assertEqual(package["required_evidence_levels"], ["E1_STATIC", "E2_TEST"])

        forbidden = set(package["forbidden_paths"])
        self.assertTrue(
            {"data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"}.issubset(forbidden)
        )
        for authority in (
            "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
            "docs/operations/loop/PLANNING_LOCK.json",
            "docs/operations/loop/VISUAL_LOCK.json",
            "docs/operations/loop/RUNTIME_ADAPTER.json",
            "docs/operations/loop/IMPLEMENTATION_PACKAGE.json",
            "docs/operations/loop/REQUIREMENT_COVERAGE_LEDGER.json",
            "docs/operations/loop/ACTIVE_LOOP_RUN.json",
        ):
            self.assertIn(authority, forbidden)
        self.assertFalse((ROOT / MARKER).exists(), "burn-in marker must be runtime-generated, not committed authority")

    def test_coverage_maps_only_runtime_marker_and_runtime_adapter_checks_exact_content(self) -> None:
        coverage = load("REQUIREMENT_COVERAGE_LEDGER.json")
        adapter = load("RUNTIME_ADAPTER.json")

        self.assertEqual(coverage["package_id"], PACKAGE)
        self.assertEqual(coverage["status"], "INITIALIZED")
        self.assertEqual(len(coverage["requirements"]), 1)
        entry = coverage["requirements"][0]
        self.assertEqual(entry["requirement_id"], REQUIREMENT)
        self.assertEqual(entry["status"], "MAPPED")
        self.assertEqual(entry["outputs"], [MARKER])
        self.assertTrue(entry["tasks"] and entry["tests"] and entry["evidence"])

        self.assertEqual(adapter["contract_role"], "LOOP_RUNTIME_ADAPTER")
        self.assertEqual(adapter["status"], "PROJECT_ADAPTER_VALIDATED")
        self.assertEqual(len(adapter["test_commands"]), 1)
        command = adapter["test_commands"][0]
        self.assertEqual(command["command_id"], "A2_BURNIN_MARKER_EXACT")
        self.assertEqual(command["argv"][:2], ["python", "-c"])
        self.assertEqual(command["working_directory"], ".")
        self.assertEqual(command["network"], "DENIED")
        script = command["argv"][2]
        self.assertIn(MARKER, script)
        self.assertIn(repr(MARKER_CONTENT), script)
        self.assertTrue(
            {"data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"}.issubset(
                set(adapter["protected_paths"])
            )
        )

    def test_authority_run_is_not_a_claim_of_live_execution_and_legacy_migration_run_remains(self) -> None:
        immutable = load(IMMUTABLE)
        active = load("ACTIVE_LOOP_RUN.json")
        legacy = load("runs/BS_LOOP_MIGRATION_001.json")

        self.assertEqual(immutable["run_id"], "BS_A2_BURNIN_AUTHORITY_001")
        self.assertEqual(immutable["package_id"], PACKAGE)
        self.assertEqual(immutable["state"], "CREATED")
        self.assertEqual(immutable["evidence"], [])
        self.assertEqual(immutable["findings"], [])
        self.assertEqual(immutable["design_drift_status"], "NOT_CHECKED")
        self.assertEqual(immutable["receipt_sha256"], "0" * 64)
        self.assertIsNone(active["active_run"])

        self.assertEqual(legacy["run_id"], "BS_LOOP_MIGRATION_001")
        self.assertEqual(legacy["package_id"], "BS_LOOP_MIGRATION_PKG_001")
        self.assertEqual(legacy["source_main_sha"], "c969c8ed9c6306f60c851fc85ed97e0ffa885305")


if __name__ == "__main__":
    unittest.main()
