from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/validate-bca-visual-sheet-adoption.yml"

CHECKOUT_SHA = "11bd71901bbe5b1630ceea73d27597364c9af683"
SETUP_PYTHON_SHA = "a26af69be951a213d495a4c3e4e4022e16d87065"
ESCAPED_REGISTRY_PATH = "      - '\\[기획서\\]/00_프로젝트_허브/SKILL_REGISTRY.json'"
UNESCAPED_REGISTRY_PATH = '      - "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json"'


class BCAWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_uses_canonical_block_yaml(self) -> None:
        self.assertIn("\non:\n", self.text)
        for compact in (
            "branches: [",
            "paths: [",
            "permissions: {",
            "with: {",
        ):
            self.assertNotIn(compact, self.text)
        self.assertIn("    branches:\n      - main\n", self.text)
        self.assertIn("    paths:\n", self.text)
        self.assertIn("permissions:\n  contents: read\n", self.text)

    def test_literal_bracket_registry_path_is_escaped_for_github_glob(self) -> None:
        self.assertIn(ESCAPED_REGISTRY_PATH, self.text)
        self.assertNotIn(UNESCAPED_REGISTRY_PATH, self.text)

    def test_job_steps_are_explicit(self) -> None:
        self.assertIn("jobs:\n  contract:\n", self.text)
        self.assertIn("    name: BCA visual Sheet adoption contract\n", self.text)
        self.assertIn("      - name: Checkout repository\n", self.text)
        self.assertIn("      - name: Set up Python\n", self.text)
        self.assertIn("      - name: Run BCA contracts\n", self.text)
        self.assertIn("      - name: Check diff whitespace\n", self.text)

    def test_actions_are_pinned_and_diff_has_full_history(self) -> None:
        self.assertIn(f"actions/checkout@{CHECKOUT_SHA}", self.text)
        self.assertIn(f"actions/setup-python@{SETUP_PYTHON_SHA}", self.text)
        self.assertIn("          fetch-depth: 0\n", self.text)
        self.assertIn("git diff --check origin/main...HEAD", self.text)
        self.assertNotIn("actions/checkout@v4", self.text)
        self.assertNotIn("actions/setup-python@v5", self.text)

    def test_workflow_runs_both_bca_contract_modules(self) -> None:
        for token in (
            '      - "tests/test_bca_visual_sheet_adoption.py"',
            '      - "tests/test_bca_workflow_contract.py"',
            "          tests.test_bca_visual_sheet_adoption",
            "          tests.test_bca_workflow_contract",
        ):
            self.assertIn(token, self.text)


if __name__ == "__main__":
    unittest.main()
