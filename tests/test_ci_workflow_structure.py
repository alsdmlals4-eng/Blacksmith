from __future__ import annotations

import json
import unittest
from pathlib import Path


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
        self.assertIn("ref: 4ec410e611152294f3f2685570fca6019c7abcfa", workflow)
        self.assertIn("check_approved_project_operating_contract.py", workflow)
        self.assertIn("approved-protected-change", workflow)
        self.assertIn("docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json", workflow)
        self.assertNotIn("python .base-contract/tools/check_project_operating_contract.py", workflow)

    def test_consumed_task2_protected_change_manifest_is_retired(self) -> None:
        path = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
        self.assertFalse(path.exists(), "consumed one-shot protected-change approval must be retired")
        adapter = json.loads((ROOT / "skills" / "PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        self.assertEqual(
            "fa9595b2df95897c915331a1cb5d9b1a583611f0",
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
    def test_profile_is_shadow_first_and_a2_is_fail_closed(self) -> None:
        profile = LOOP_PROFILE.read_text(encoding="utf-8")
        for token in (
            "BS-OPS-20260813-LOOP-01",
            "BASE_LOOP_CONTRACT_COMMIT: 453f790821a108a1d4f6e1f4e45f6931c2396ee0",
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

    def test_initial_run_contract_is_locked_bounded_and_read_only(self) -> None:
        run = json.loads(LOOP_RUN.read_text(encoding="utf-8"))
        self.assertEqual(1, run["schema_version"])
        self.assertEqual("loop-engineering-run", run["contract_role"])
        self.assertEqual("BS-OPS-20260813-LOOP-01", run["goal_id"])
        self.assertEqual("BLACKSMITH", run["project_id"])
        self.assertEqual("PLANNING_LOCKED", run["planning_gate"]["status"])
        self.assertTrue(run["planning_gate"]["loop_ready"])
        self.assertEqual("A0_OBSERVE", run["autonomy_tier"])
        self.assertEqual("8e9a9cf8b0b053b5bfc5667b9a1070d3b45c3486", run["source_main_sha"])
        self.assertEqual("DISCOVER", run["loop_state"])
        self.assertEqual([], run["leases"])
        self.assertEqual([], run["planning_gate"]["allowed_product_write_roots"])
        self.assertGreaterEqual(run["budget"]["max_agents"], 1)
        self.assertEqual(1, run["budget"]["max_parallel_agents"])
        self.assertIn("NOT_RUN", {item["status"] for item in run["evidence"]})
        self.assertIn("USER_DECISION_REQUIRED", {item["classification"] for item in run["blockers"]})

    def test_ai_workflow_routes_to_the_pilot_without_changing_base_release_pin(self) -> None:
        workflow = AI_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("BLACKSMITH_LOOP_ENGINEERING_PROFILE.md", workflow)
        self.assertIn("BLACKSMITH_LOOP_RUN_CONTRACT.json", workflow)
        self.assertIn("SHADOW → A2_EXECUTE_ISOLATED", workflow)

        adapter = json.loads((ROOT / "skills" / "PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        self.assertEqual("9.4.3", adapter["base_release"]["version"])
        self.assertEqual(
            ["data/", "scripts/", "scenes/", "assets/", "addons/", "project.godot"],
            adapter["protected_paths"],
        )


if __name__ == "__main__":
    unittest.main()
