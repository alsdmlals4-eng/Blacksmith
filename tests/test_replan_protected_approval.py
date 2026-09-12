"""Run with BASE_VALIDATOR_ROOT pointing to the project's CI-pinned Base checkout."""
import importlib.util
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json"
PATHS = [
    "scripts/vertical_slice/domain/vs_replan_tag_rules.gd",
    "scripts/vertical_slice/domain/vs_replan_tag_rules.gd.uid",
]


class ReplanProtectedApprovalTests(unittest.TestCase):
    def test_approved_scope_and_fail_closed_boundaries(self):
        self.assertTrue(APPROVAL.is_file(), "Approved replan scope has no machine-readable manifest")
        configured = os.environ.get("BASE_VALIDATOR_ROOT")
        validator_root = Path(configured) if configured else ROOT / ".base-contract"
        if not (validator_root / "tools/check_approved_project_operating_contract.py").is_file():
            self.skipTest("Set BASE_VALIDATOR_ROOT to the CI-pinned Base checkout for gate integration")
        spec = importlib.util.spec_from_file_location(
            "approved_gate", validator_root / "tools/check_approved_project_operating_contract.py"
        )
        gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        approval = json.loads(APPROVAL.read_text(encoding="utf-8"))
        adapter = json.loads((ROOT / "skills/PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8"))
        baseline = adapter["protected_baseline"]["commit"]
        self.assertEqual([], gate.validate_approval_document(
            approval, protected_base=baseline, changed_paths=PATHS, externally_approved=True))
        for paths, base, external in [
            (PATHS, baseline, False),
            (PATHS + ["scripts/unapproved.gd"], baseline, True),
            (PATHS[:1], baseline, True),
            (PATHS, "0" * 40, True),
        ]:
            with self.subTest(paths=paths, baseline=base, external=external):
                self.assertTrue(gate.validate_approval_document(
                    approval, protected_base=base, changed_paths=paths, externally_approved=external))
        errors = ["Protected-path changes detected: " + ", ".join(PATHS), "unrelated failure"]
        self.assertEqual(["unrelated failure"], gate.reconcile_contract_errors(errors, approved_paths=PATHS))


if __name__ == "__main__":
    unittest.main()
