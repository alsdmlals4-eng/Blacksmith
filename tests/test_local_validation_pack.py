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


def authoritative_manifest(head: str) -> dict[str, object]:
    return {
        "validation_mode": "LOCAL_EXACT_HEAD_NO_GITHUB_ACTIONS",
        "status": "PASS",
        "head_sha": head,
        "expected_head_sha": head,
        "exact_head": True,
        "clean_before": True,
        "clean_after": True,
        "authoring_surface_hash_unchanged": True,
        "environment": {
            "platform": "Windows-11-10.0.26100-SP0",
            "python_version_match": True,
        },
        "operating_base": {"pin_match": True, "workflow_pin_match": True},
        "contract_base": {"pin_match": True, "workflow_pin_match": True},
        "protected_base_valid": True,
        "godot_required": True,
        "godot_present": True,
    }


def lane_manifest(lane: str, head: str) -> dict[str, object]:
    platform_kind, version = module.REQUIRED_MATRIX_LANES[lane]
    return {
        "validation_mode": "LOCAL_PYTHON_MATRIX_LANE",
        "lane_id": lane,
        "platform_kind": platform_kind,
        "detected_platform_kind": platform_kind,
        "python_required": version,
        "python_version_match": True,
        "status": "PASS",
        "head_sha": head,
        "exact_head": True,
        "clean_before": True,
        "clean_after": True,
        "authoring_surface_hash_unchanged": True,
    }


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

    def test_detect_platform_kind_rejects_plain_linux_and_accepts_windows_wsl_ubuntu(self) -> None:
        self.assertEqual(
            module.detect_platform_kind(
                system="Windows", release="11", proc_version="", os_release=""
            ),
            "windows",
        )
        self.assertEqual(
            module.detect_platform_kind(
                system="Linux",
                release="6.6.87.2-microsoft-standard-WSL2",
                proc_version="Linux version microsoft WSL2",
                os_release='ID=ubuntu\nNAME="Ubuntu"\n',
            ),
            "wsl-ubuntu",
        )
        self.assertEqual(
            module.detect_platform_kind(
                system="Linux",
                release="6.8.0-generic",
                proc_version="Linux version generic",
                os_release="ID=ubuntu\n",
            ),
            "unsupported",
        )

    def test_pack_pass_requires_full_lane_and_every_matrix_lane(self) -> None:
        head = "a" * 40
        lanes = [
            lane_manifest(lane, head) for lane in module.REQUIRED_MATRIX_LANES
        ]
        result = module.evaluate_pack(authoritative_manifest(head), lanes, head)
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.missing_lanes, [])
        self.assertEqual(result.failed_lanes, [])
        self.assertEqual(result.unexpected_lanes, [])

    def test_pack_fails_closed_for_missing_failed_mismatched_or_unknown_lane(self) -> None:
        head = "b" * 40
        failed = lane_manifest("windows-py311", head)
        failed["status"] = "FAIL"
        mismatched = lane_manifest("windows-py312", head)
        mismatched["head_sha"] = "c" * 40
        mismatched["exact_head"] = False
        unknown = lane_manifest("windows-py313", head)
        unknown["lane_id"] = "macos-py312"
        lanes = [failed, mismatched, unknown]
        result = module.evaluate_pack(authoritative_manifest(head), lanes, head)
        self.assertEqual(result.status, "FAIL")
        self.assertIn("windows-py313", result.missing_lanes)
        self.assertIn("wsl-ubuntu-py312", result.missing_lanes)
        self.assertIn("windows-py311", result.failed_lanes)
        self.assertIn("windows-py312", result.failed_lanes)
        self.assertIn("macos-py312", result.unexpected_lanes)

    def test_authoritative_manifest_must_prove_windows_base_and_godot(self) -> None:
        head = "d" * 40
        lanes = [
            lane_manifest(lane, head) for lane in module.REQUIRED_MATRIX_LANES
        ]
        full = authoritative_manifest(head)
        full["environment"] = {
            "platform": "Linux-WSL2",
            "python_version_match": True,
        }
        self.assertEqual(module.evaluate_pack(full, lanes, head).status, "FAIL")
        full = authoritative_manifest(head)
        full["contract_base"] = {
            "pin_match": False,
            "workflow_pin_match": True,
        }
        self.assertEqual(module.evaluate_pack(full, lanes, head).status, "FAIL")
        full = authoritative_manifest(head)
        full["godot_present"] = False
        self.assertEqual(module.evaluate_pack(full, lanes, head).status, "FAIL")

    def test_lane_manifest_contract_rejects_spoofed_platform_or_python(self) -> None:
        head = "e" * 40
        lane = lane_manifest("wsl-ubuntu-py312", head)
        lane["detected_platform_kind"] = "windows"
        self.assertFalse(module.lane_is_valid(lane, head))
        lane = lane_manifest("wsl-ubuntu-py312", head)
        lane["python_required"] = "3.11"
        self.assertFalse(module.lane_is_valid(lane, head))

    def test_scripts_expose_all_required_entrypoints(self) -> None:
        powershell = (
            ROOT / "tools" / "run_local_validation_pack.ps1"
        ).read_text(encoding="utf-8")
        shell = (ROOT / "tools" / "run_wsl_python_lane.sh").read_text(
            encoding="utf-8"
        )
        for marker in (
            "-3.11",
            "-3.12",
            "-3.13",
            "wsl.exe",
            "run_local_validation_v2.py",
            "aggregate_local_validation_pack.py",
        ):
            self.assertIn(marker, powershell)
        for marker in (
            "3.12",
            "run_local_python_matrix_lane.py",
            "--lane-id",
            "wsl-ubuntu-py312",
        ):
            self.assertIn(marker, shell)

    def test_matrix_commands_match_reusable_python_validation_without_base_audit(self) -> None:
        commands_path = ROOT / "tools" / "local_validation_commands.py"
        spec_commands = importlib.util.spec_from_file_location(
            "local_validation_commands", commands_path
        )
        commands_module = importlib.util.module_from_spec(spec_commands)
        assert spec_commands.loader is not None
        spec_commands.loader.exec_module(commands_module)
        names = [
            name
            for name, _ in commands_module.python_matrix_commands(
                sys.executable, "code"
            )
        ]
        self.assertIn("local-validation-pack", names)
        self.assertIn("game-data", names)
        self.assertIn("enhancement-simulator-contract", names)
        self.assertNotIn("operating-audit", names)
        self.assertNotIn("project-base-adapter", names)


if __name__ == "__main__":
    unittest.main()
