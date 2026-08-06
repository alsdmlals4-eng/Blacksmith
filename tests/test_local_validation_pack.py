from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
MODULE = ROOT / "tools" / "local_validation_pack_contract.py"
spec = importlib.util.spec_from_file_location("local_validation_pack_contract", MODULE)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


class LocalValidationPackTests(unittest.TestCase):
    def test_required_lane_contract_matches_windows_and_wsl_matrix(self) -> None:
        self.assertEqual(
            module.REQUIRED_MATRIX_LANES,
            {
                "windows-py311": ("windows", "3.11"),
                "windows-py312": ("windows", "3.12"),
                "windows-py313": ("windows", "3.13"),
                "wsl-ubuntu-py312": ("wsl-ubuntu", "3.12"),
            },
        )

    def test_pack_pass_requires_full_lane_and_every_matrix_lane(self) -> None:
        head = "a" * 40
        full = {
            "status": "PASS", "head_sha": head, "expected_head_sha": head,
            "exact_head": True, "clean_before": True, "clean_after": True,
            "authoring_surface_hash_unchanged": True,
        }
        lanes = [
            {
                "lane_id": lane, "platform_kind": platform,
                "python_required": version, "python_version_match": True,
                "status": "PASS", "head_sha": head, "exact_head": True,
                "clean_before": True, "clean_after": True,
                "authoring_surface_hash_unchanged": True,
            }
            for lane, (platform, version) in module.REQUIRED_MATRIX_LANES.items()
        ]
        result = module.evaluate_pack(full, lanes, head)
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.missing_lanes, [])
        self.assertEqual(result.failed_lanes, [])

    def test_pack_fails_closed_for_missing_failed_or_mismatched_lane(self) -> None:
        head = "b" * 40
        full = {
            "status": "PASS", "head_sha": head, "expected_head_sha": head,
            "exact_head": True, "clean_before": True, "clean_after": True,
            "authoring_surface_hash_unchanged": True,
        }
        lanes = [
            {
                "lane_id": "windows-py311", "platform_kind": "windows",
                "python_required": "3.11", "python_version_match": True,
                "status": "FAIL", "head_sha": head, "exact_head": True,
                "clean_before": True, "clean_after": True,
                "authoring_surface_hash_unchanged": True,
            },
            {
                "lane_id": "windows-py312", "platform_kind": "windows",
                "python_required": "3.12", "python_version_match": True,
                "status": "PASS", "head_sha": "c" * 40,
                "exact_head": False, "clean_before": True,
                "clean_after": True,
                "authoring_surface_hash_unchanged": True,
            },
        ]
        result = module.evaluate_pack(full, lanes, head)
        self.assertEqual(result.status, "FAIL")
        self.assertIn("windows-py313", result.missing_lanes)
        self.assertIn("wsl-ubuntu-py312", result.missing_lanes)
        self.assertIn("windows-py311", result.failed_lanes)
        self.assertIn("windows-py312", result.failed_lanes)

    def test_lane_manifest_contract_rejects_wrong_platform_or_python(self) -> None:
        head = "d" * 40
        lane = {
            "lane_id": "wsl-ubuntu-py312", "platform_kind": "windows",
            "python_required": "3.11", "python_version_match": True,
            "status": "PASS", "head_sha": head, "exact_head": True,
            "clean_before": True, "clean_after": True,
        }
        self.assertFalse(module.lane_is_valid(lane, head))

    def test_scripts_expose_all_required_entrypoints(self) -> None:
        powershell = (ROOT / "tools" / "run_local_validation_pack.ps1").read_text(encoding="utf-8")
        shell = (ROOT / "tools" / "run_wsl_python_lane.sh").read_text(encoding="utf-8")
        for marker in (
            "-3.11", "-3.12", "-3.13", "wsl.exe",
            "run_local_validation_v2.py", "aggregate_local_validation_pack.py",
        ):
            self.assertIn(marker, powershell)
        for marker in (
            "3.12", "run_local_python_matrix_lane.py",
            "--lane-id", "wsl-ubuntu-py312",
        ):
            self.assertIn(marker, shell)

    def test_matrix_commands_match_reusable_python_validation_without_base_audit(self) -> None:
        commands_path = ROOT / "tools" / "local_validation_commands.py"
        spec_commands = importlib.util.spec_from_file_location("local_validation_commands", commands_path)
        commands_module = importlib.util.module_from_spec(spec_commands)
        assert spec_commands.loader is not None
        spec_commands.loader.exec_module(commands_module)
        names = [name for name, _ in commands_module.python_matrix_commands(sys.executable, "code")]
        self.assertIn("local-validation-pack", names)
        self.assertIn("game-data", names)
        self.assertIn("enhancement-simulator-contract", names)
        self.assertNotIn("operating-audit", names)
        self.assertNotIn("project-base-adapter", names)


if __name__ == "__main__":
    unittest.main()
