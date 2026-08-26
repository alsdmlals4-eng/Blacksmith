from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.test_phase_c_live_continuation_contract import PhaseCLiveContinuationContractTests  # noqa: F401


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
LOOP_PROFILE = ROOT / "docs" / "operations" / "BLACKSMITH_LOOP_ENGINEERING_PROFILE.md"
LOOP_RUN = ROOT / "docs" / "operations" / "BLACKSMITH_LOOP_RUN_CONTRACT.json"
AI_WORKFLOW = ROOT / "[기획서]" / "00_프로젝트_허브" / "AI_WORKFLOW.md"


def read(name: str) -> str:
    return (WORKFLOWS / name).read_text(encoding="utf-8")


class CiWorkflowStructureTests(unittest.TestCase):
    def test_all_workflows_cancel_superseded_runs(self) -> None:
        for name in (
            "data-validation.yml",
            "python-validation.yml",
            "godot-validation.yml",
            "full-validation.yml",
        ):
            source = read(name)
            self.assertIn("concurrency:", source, name)
            self.assertIn("cancel-in-progress: true", source, name)
            self.assertIn("ci-${{ github.workflow }}-${{ github.ref }}", source, name)

    def test_top_level_and_reusable_groups_do_not_self_cancel(self) -> None:
        pr = read("data-validation.yml")
        full = read("full-validation.yml")
        python_workflow = read("python-validation.yml")
        godot = read("godot-validation.yml")
        exact = "group: ci-${{ github.workflow }}-${{ github.ref }}"
        self.assertIn(exact, pr)
        self.assertIn(exact, full)
        self.assertIn("-${{ inputs.runner }}-${{ inputs.python-version }}-${{ inputs.scope }}", python_workflow)
        self.assertIn("-godot-reusable", godot)
        self.assertNotIn(f"{exact}\n", godot)

    def test_automatic_triggers_are_enabled_at_the_correct_tier(self) -> None:
        pr = read("data-validation.yml")
        full = read("full-validation.yml")
        self.assertIn("\n  pull_request:", pr)
        self.assertIn("workflow_dispatch:", pr)
        self.assertNotIn("\n  push:", pr)
        self.assertNotIn("\n  schedule:", pr)
        self.assertIn("\n  push:", full)
        self.assertIn("- main", full)
        self.assertIn("\n  schedule:", full)
        self.assertIn('cron: "17 18 * * *"', full)
        self.assertIn("workflow_dispatch:", full)

    def test_pr_router_runs_only_relevant_scope(self) -> None:
        pr = read("data-validation.yml")
        self.assertIn("scope=docs", pr)
        self.assertIn("scope=code", pr)
        self.assertIn("uses: ./.github/workflows/python-validation.yml", pr)
        self.assertIn("uses: ./.github/workflows/godot-validation.yml", pr)
        self.assertIn("needs.classify.outputs.scope == 'docs'", pr)
        self.assertIn("needs.classify.outputs.scope == 'code'", pr)
        self.assertNotIn("libreoffice-writer", pr)
        self.assertNotIn("pnpm install", pr)

    def test_godot_is_reusable_and_owns_lifecycle_regression(self) -> None:
        godot = read("godot-validation.yml")
        self.assertIn("workflow_call:", godot)
        self.assertNotIn("\n  pull_request:", godot)
        self.assertNotIn("\n  push:", godot)
        self.assertIn("test_equipment_lifecycle_controller.gd", godot)
        self.assertIn("test_equipment_lifecycle_poc.gd", godot)
        self.assertIn("equipment_lifecycle_poc.tscn", godot)
        self.assertIn("scenes/main/main.tscn", godot)
        self.assertIn("Upload failure logs only", godot)

    def test_full_validation_owns_matrix_and_heavy_base_suite(self) -> None:
        full = read("full-validation.yml")
        self.assertIn("ubuntu-latest", full)
        self.assertIn("windows-latest", full)
        for version in ('"3.11"', '"3.12"', '"3.13"'):
            self.assertIn(version, full)
        self.assertIn("Validate full pinned Base operating system once", full)
        self.assertIn("uses: ./.github/workflows/godot-validation.yml", full)
        self.assertEqual(1, full.count("Validate full pinned Base operating system once"))

    def test_python_contracts_are_centralized(self) -> None:
        python_workflow = read("python-validation.yml")
        self.assertIn("workflow_call:", python_workflow)
        self.assertIn("inputs.scope == 'code'", python_workflow)
        self.assertIn("check_forging_quality_contract.py", python_workflow)
        self.assertIn("test_lifecycle_data_contract.py", python_workflow)
        self.assertIn("check_project_core_alignment_current.py", python_workflow)
        current_wrapper = (ROOT / "tests" / "check_project_core_alignment_current.py").read_text(encoding="utf-8")
        self.assertIn("import check_project_core_alignment as legacy", current_wrapper)
        self.assertIn("legacy.check_r2(failures)", current_wrapper)

    def test_project_base_adapter_uses_exact_approved_protected_change_gate(self) -> None:
        workflow = read("validate-project-base-adapter.yml")
        self.assertIn("ref: 43b3ffb2c5b026e3d4a38dab2338585894d36f61", workflow)
        self.assertIn("check_approved_project_operating_contract.py", workflow)
        self.assertIn("approved-protected-change", workflow)
        self.assertIn("docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json", workflow)
        self.assertNotIn("python .base-contract/tools/check_project_operating_contract.py", workflow)

    def test_first_item_forge_protected_change_manifest_is_retired(self) -> None:
        path = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
        self.assertFalse(path.exists(), "consumed first-item forge approval must not remain active")
        adapter = json.loads((ROOT / "skills" / "PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        self.assertEqual(
            "afb3fc1c0e78121470f8f56eccbb2b0d8217f601",
            adapter["protected_baseline"]["commit"],
        )
        self.assertEqual(
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
            adapter["protected_paths"],
        )

    def test_activation_policy_is_recorded(self) -> None:
        policy = (ROOT / "docs" / "CI_EXECUTION_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("ACTIONS_AVAILABLE", policy)
        self.assertIn("pull_request", policy)
        self.assertIn("schedule", policy)
        self.assertIn("Windows", policy)
        self.assertIn("Required Check", policy)
        self.assertIn("재사용 Workflow", policy)
        self.assertIn("test_equipment_lifecycle_poc.gd", policy)
        self.assertIn("equipment_lifecycle_poc.tscn", policy)


class LoopEngineeringPilotContractTests(unittest.TestCase):
    def test_profile_records_completed_shadow_and_fail_closed_a2(self) -> None:
        profile = LOOP_PROFILE.read_text(encoding="utf-8")
        for token in (
            "BS-OPS-20260813-LOOP-01",
            "BASE_LOOP_CONTRACT_COMMIT: 453f790821a108a1d4f6e1f4e45f6931c2396ee0",
            "adoption_baseline_sha: 8e9a9cf8b0b053b5bfc5667b9a1070d3b45c3486",
            "latest_shadow_source_main_sha: 50cd459964c274fdc46e5d0be25bb31d929452da",
            "shadow_checkpoint_status: COMPLETE_DEFERRED_BY_PROTECTED_PR158",
            "current_stage: SHADOW",
            "current_effective_autonomy: A0_OBSERVE",
            "default_autonomy_after_shadow: A2_EXECUTE_ISOLATED",
            "a3_auto_merge_allowlist: []",
            "scheduler_runtime_provider: NOT_CONFIGURED",
            "P0_LOCAL_EXECUTOR_BOOTSTRAP",
            "PRODUCT_WRITES_PROHIBITED_IN_SHADOW",
            "TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED",
        ):
            self.assertIn(token, profile)

        for protected in (
            "data/",
            "scripts/",
            "scenes/",
            "assets/",
            "addons/",
            "project.godot",
            "project_core",
            "save_compatibility",
            "major_ux_meaning",
        ):
            self.assertIn(protected, profile)

    def test_shadow_checkpoint_is_completed_deferred_and_read_only(self) -> None:
        run = json.loads(LOOP_RUN.read_text(encoding="utf-8"))
        self.assertEqual(1, run["schema_version"])
        self.assertEqual("loop-engineering-run", run["contract_role"])
        self.assertEqual("BS-OPS-20260813-LOOP-01", run["goal_id"])
        self.assertEqual("BLACKSMITH", run["project_id"])
        self.assertEqual("PLANNING_LOCKED", run["planning_gate"]["status"])
        self.assertTrue(run["planning_gate"]["loop_ready"])
        self.assertEqual("A0_OBSERVE", run["autonomy_tier"])
        self.assertEqual("50cd459964c274fdc46e5d0be25bb31d929452da", run["source_main_sha"])
        self.assertEqual("DEFERRED", run["loop_state"])
        self.assertEqual("NO_DRIFT", run["design_drift_status"])
        self.assertEqual([], run["leases"])
        self.assertEqual([], run["task_queues"]["ready_tasks"])
        self.assertEqual([], run["task_queues"]["deferred_tasks"])
        self.assertEqual(1, len(run["task_queues"]["completed_tasks"]))
        self.assertEqual("BS-LOOP-SHADOW-001", run["task_queues"]["completed_tasks"][0]["task_id"])
        self.assertEqual("COMPLETED", run["task_queues"]["completed_tasks"][0]["status"])

        allowed_changes = set(run["planning_gate"]["allowed_changes"])
        self.assertEqual(
            {
                "docs/operations/BLACKSMITH_LOOP_ENGINEERING_PROFILE.md",
                "docs/operations/BLACKSMITH_LOOP_RUN_CONTRACT.json",
                "[기획서]/00_프로젝트_허브/AI_WORKFLOW.md",
                "tests/test_ci_workflow_structure.py",
            },
            allowed_changes,
        )
        for protected_root in ("data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"):
            self.assertFalse(
                any(path == protected_root or path.startswith(protected_root) for path in allowed_changes),
                protected_root,
            )

        evidence = {item["evidence_id"]: item for item in run["evidence"]}
        self.assertEqual("PASS", evidence["BS-LOOP-E1-STATIC"]["status"])
        self.assertEqual("PASS", evidence["BS-LOOP-E2-TEST"]["status"])
        self.assertEqual("PASS", evidence["BS-LOOP-E3-RUNTIME"]["status"])
        self.assertEqual("NOT_RUN", evidence["BS-LOOP-E6-HUMAN"]["status"])

        finding_ids = {item["finding_id"] for item in run["findings"]}
        self.assertTrue({"BS-LOOP-F01-PR158", "BS-LOOP-F02-PR81"}.issubset(finding_ids))
        blocker_classes = {item["classification"] for item in run["blockers"]}
        self.assertIn("USER_DECISION_REQUIRED", blocker_classes)
        self.assertIn("PROTECTED_SURFACE", blocker_classes)
        self.assertIn("PR #158", run["next_action"])
        self.assertEqual(2, run["budget"]["used_ci_runs"])

    def test_ai_workflow_routes_to_the_pilot_with_current_base_release_pin(self) -> None:
        workflow = AI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("BLACKSMITH_LOOP_ENGINEERING_PROFILE.md", workflow)
        self.assertIn("BLACKSMITH_LOOP_RUN_CONTRACT.json", workflow)
        self.assertIn("SHADOW → A2_EXECUTE_ISOLATED", workflow)

        adapter = json.loads((ROOT / "skills" / "PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        self.assertEqual("9.4.4", adapter["base_release"]["version"])
        self.assertEqual(
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
            adapter["protected_paths"],
        )


if __name__ == "__main__":
    unittest.main()
