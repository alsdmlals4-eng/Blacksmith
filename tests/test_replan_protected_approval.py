"""Run with BASE_VALIDATOR_ROOT pointing to the project's CI-pinned Base checkout."""
import importlib.util
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
APPROVAL = ROOT / "docs/archive/protected-approvals/replan-pr371-20260913.json"
PATHS = [
    "scripts/vertical_slice/domain/vs_replan_tag_rules.gd",
    "scripts/vertical_slice/domain/vs_replan_tag_rules.gd.uid",
    "scripts/vertical_slice/domain/vs_item.gd",
    "scripts/vertical_slice/resolvers/vs_precision_resolver.gd",
    "scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd",
    "scripts/vertical_slice/services/vs_enhancement_action_service.gd",
    "scripts/vertical_slice/services/vs_run_initializer_service.gd",
    "scripts/vertical_slice/services/vs_item_birth_service.gd",
    "scripts/vertical_slice/ui/vs_main_menu.gd",
    "scripts/vertical_slice/ui/vs_workshop_screen.gd",
    "scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd",
    "scripts/vertical_slice/domain/vs_save_envelope.gd",
    "scripts/vertical_slice/ui/vs_app.gd",
    "scripts/vertical_slice/ui/vs_item_chronicle_screen.gd",
    "scripts/vertical_slice/services/vs_workshop_maintenance_service.gd",
    "scripts/ui/forging_screen.gd",
]


class ReplanProtectedApprovalTests(unittest.TestCase):
    def test_approved_scope_and_fail_closed_boundaries(self):
        self.assertTrue(APPROVAL.is_file(), "Consumed replan approval must remain preserved as historical evidence")
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
        baseline = "c31e550fc8d5b27d4377aeb542fde3cbfe228c06"
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
