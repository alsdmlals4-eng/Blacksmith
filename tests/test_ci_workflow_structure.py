from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


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
        self.assertIn("check_project_core_alignment.py", python_workflow)

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


if __name__ == "__main__":
    unittest.main()
