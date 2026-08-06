from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "tools" / "run_local_validation_v2.py"
spec = importlib.util.spec_from_file_location("run_local_validation_v2", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


class LocalValidationFallbackTests(unittest.TestCase):
    def test_authoring_surface_selection_is_fail_closed(self) -> None:
        self.assertTrue(module.is_authoring_surface("project.godot"))
        self.assertTrue(module.is_authoring_surface("scenes/main.tscn"))
        self.assertTrue(module.is_authoring_surface("resources/theme.tres"))
        self.assertTrue(module.is_authoring_surface("addons/godot_ai/plugin.cfg"))
        self.assertFalse(module.is_authoring_surface("tests/gut/test_smoke.gd"))

    def test_base_v9_path_gate_matches_workflow(self) -> None:
        self.assertTrue(module.base_v9_changed_paths_allowed(["docs/a.md", "tools/check.py"]))
        for path in ("project.godot", "scenes/main.tscn", "data/x.json", "assets/a.png", "addons/x/a.gd"):
            self.assertFalse(module.base_v9_changed_paths_allowed([path]))

    def test_sha256_file_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "evidence.txt"
            target.write_text("blacksmith", encoding="utf-8")
            self.assertEqual(
                module.sha256_file(target),
                "8eae6c54657e94be77a206e430054386a7391f99e2cea017b16d90661037a1ee",
            )

    def test_merge_pass_is_fail_closed(self) -> None:
        green = module.CommandResult("green", ["python"], 0, "a", "b", "log")
        self.assertEqual(module.summarize_status([green], True, True, True, True, True, True, True), "PASS")
        self.assertEqual(module.summarize_status([green], True, True, True, True, False, True, True), "PARTIAL")
        self.assertEqual(module.summarize_status([green], True, True, True, True, True, False, True), "PARTIAL")
        self.assertEqual(module.summarize_status([green], True, True, True, True, True, False, False), "PASS")
        self.assertEqual(module.summarize_status([green], True, True, True, True, True, True, True, False), "FAIL")
        failed = module.CommandResult("red", ["python"], 1, "a", "b", "log")
        self.assertEqual(module.summarize_status([failed], True, True, True, True, True, True, True), "FAIL")

    def test_logged_godot_contract_rejects_wrong_version_errors_and_missing_markers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "run.log"
            log.write_text("4.7.10.stable", encoding="utf-8")
            wrong = module.CommandResult("godot-version", ["godot"], 0, "a", "b", str(log))
            self.assertFalse(module.validate_logged_result(wrong).passed)
            log.write_text("4.7.1.stable.official", encoding="utf-8")
            correct = module.CommandResult("godot-version", ["godot"], 0, "a", "b", str(log))
            self.assertTrue(module.validate_logged_result(correct).passed)
            log.write_text("ERROR: broken", encoding="utf-8")
            broken = module.CommandResult("godot-import", ["godot"], 0, "a", "b", str(log))
            self.assertFalse(module.validate_logged_result(broken).passed)
            log.write_text("no success marker", encoding="utf-8")
            missing = module.CommandResult("godot-test_forging_session", ["godot"], 0, "a", "b", str(log))
            self.assertFalse(module.validate_logged_result(missing).passed)
            log.write_text("ForgingSession tests PASSED", encoding="utf-8")
            passed = module.CommandResult("godot-test_forging_session", ["godot"], 0, "a", "b", str(log))
            self.assertTrue(module.validate_logged_result(passed).passed)

    def test_runner_keeps_parity_with_current_pr_workflows(self) -> None:
        root = Path(__file__).parents[1]
        runner = "\n".join(
            (root / "tools" / name).read_text(encoding="utf-8")
            for name in ("run_local_validation_v2.py", "local_validation_commands.py", "local_validation_contract.py")
        )
        required_markers = (
            "tests/test_no_merge_conflicts.py",
            "tests.test_base_v9_adoption",
            "tests.test_bca_visual_sheet_adoption",
            "tests/test_project_base_adapter_thin_migration.py",
            "check_project_operating_contract.py",
            "res://scenes/main/main.tscn",
            "addons/gut/gut_cmdln.gd",
            "tools/validate_gut_junit.py",
            module.BASE_OPERATING_PIN,
            module.BASE_CONTRACT_PIN,
        )
        for marker in required_markers:
            self.assertIn(marker, runner)

    def test_workflow_pins_match_runner(self) -> None:
        root = Path(__file__).parents[1]
        operating = root / ".github" / "workflows" / "python-validation.yml"
        contract = root / ".github" / "workflows" / "validate-project-base-adapter.yml"
        if operating.is_file():
            self.assertTrue(module.workflow_has_exact_ref(operating, module.BASE_OPERATING_PIN))
        if contract.is_file():
            self.assertTrue(module.workflow_has_exact_ref(contract, module.BASE_CONTRACT_PIN))


if __name__ == "__main__":
    unittest.main()
