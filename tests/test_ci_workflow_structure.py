from __future__ import annotations

import json
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

    def test_project_godot_protected_change_manifest_is_exact_and_one_shot(self) -> None:
        path = ROOT / "docs" / "operations" / "PROJECT_PROTECTED_CHANGE_APPROVAL.json"
        self.assertTrue(path.is_file(), "exact protected-change approval manifest is missing")
        manifest = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("PROJECT_PROTECTED_CHANGE_APPROVAL", manifest["artifact_role"])
        self.assertEqual("APPROVED", manifest["status"])
        self.assertEqual("2dddf864519a557152c6bbf0f0ee7fb94eadf11c", manifest["protected_base_commit"])
        self.assertEqual(["project.godot"], manifest["approved_paths"])
        self.assertIn("BS-HIGODOT-EXEC-20260808-01", manifest["decision_ids"])
        self.assertEqual("GITHUB_PR_LABEL_APPROVED_PROTECTED_CHANGE", manifest["approval_source"])
        self.assertFalse(any(any(char in item for char in "*?[]") for item in manifest["approved_paths"]))

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
