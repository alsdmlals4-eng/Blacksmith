from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".gutconfig.json"
SMOKE = ROOT / "tests/gut/unit/test_gut_framework_smoke.gd"
INTEGRATION_README = ROOT / "tests/gut/integration/README.md"
WORKFLOW = ROOT / ".github/workflows/gut-validation.yml"
JUNIT_VALIDATOR = ROOT / "tools/validate_gut_junit.py"
MANIFEST = ROOT / "docs/testing/GUT_9_7_1_FORMAL_ADOPTION_MANIFEST.json"
REMOVAL = ROOT / "docs/testing/GUT_9_7_1_REMOVAL_PROCEDURE.md"
PROJECT = ROOT / "project.godot"

ALLOWED_ADOPTION_PATHS = {
    ".gutconfig.json",
    ".github/workflows/gut-validation.yml",
    ".github/workflows/python-validation.yml",
    "docs/testing/GUT_9_7_1_FORMAL_ADOPTION_MANIFEST.json",
    "docs/testing/GUT_9_7_1_REMOVAL_PROCEDURE.md",
    "tests/gut/integration/README.md",
    "tests/gut/unit/test_gut_framework_smoke.gd",
    "tests/test_gut_formal_adoption_contract.py",
    "tests/test_higodot_gut_authority_gate.py",
    "tools/validate_gut_junit.py",
}


def _text(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"missing formal GUT adoption surface: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(_text(path))


def _load_junit_validator():
    if not JUNIT_VALIDATOR.is_file():
        raise AssertionError("missing tools/validate_gut_junit.py")
    spec = importlib.util.spec_from_file_location("validate_gut_junit", JUNIT_VALIDATOR)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load GUT JUnit validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GutFormalAdoptionContractTests(unittest.TestCase):
    def test_adoption_pr_has_a_separate_non_product_change_boundary(self) -> None:
        if not (ROOT / ".git").exists():
            return
        base_ref = os.environ.get("GITHUB_BASE_REF", "docs/higodot-gut-authority-gate")
        remote_base = f"origin/{base_ref}"
        merge_base = subprocess.run(
            ["git", "merge-base", "HEAD", remote_base],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        changed = {
            line.strip()
            for line in subprocess.run(
                ["git", "-c", "core.quotepath=false", "diff", "--name-only", f"{merge_base}..HEAD"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
            if line.strip()
        }
        self.assertLessEqual(changed, ALLOWED_ADOPTION_PATHS, sorted(changed - ALLOWED_ADOPTION_PATHS))
        self.assertNotIn("project.godot", changed)
        self.assertFalse(any(path.startswith(("scenes/", "scripts/", "data/", "assets/", "addons/gut/")) for path in changed))

    def test_gut_config_has_real_project_consumption_roots(self) -> None:
        payload = _json(CONFIG)
        self.assertEqual(
            payload["dirs"],
            ["res://tests/gut/unit", "res://tests/gut/integration"],
        )
        self.assertTrue(payload["include_subdirs"])
        self.assertTrue(payload["should_exit"])
        self.assertEqual(payload["prefix"], "test_")
        self.assertEqual(payload["suffix"], ".gd")

    def test_smoke_test_consumes_gut_framework(self) -> None:
        text = _text(SMOKE)
        self.assertIn('extends "res://addons/gut/test.gd"', text)
        self.assertIn("func test_gut_framework_is_consumed_by_ci()", text)
        self.assertIn("assert_eq", text)
        self.assertTrue(INTEGRATION_README.is_file())

    def test_editor_plugin_is_not_enabled_as_second_authoring_authority(self) -> None:
        project = _text(PROJECT)
        self.assertIn('res://addons/godot_ai/plugin.cfg', project)
        self.assertNotIn('res://addons/gut/plugin.cfg', project)

    def test_adoption_manifest_is_complete_and_fail_closed(self) -> None:
        manifest = _json(MANIFEST)
        self.assertEqual(manifest["schema_version"], "1.0.0")
        self.assertEqual(manifest["decision_id"], "BS-TEST-20260806-01")
        self.assertEqual(manifest["framework"], "GUT")
        self.assertEqual(manifest["version"], "9.7.1")
        self.assertEqual(manifest["source_repository"], "bitwes/Gut")
        self.assertEqual(
            manifest["source_commit"],
            "aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605",
        )
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["godot_compatibility"], "4.7.x")
        self.assertEqual(manifest["validated_engine"], "4.7.1")
        self.assertEqual(manifest["authority_role"], "GDSCRIPT_TEST_FRAMEWORK_ONLY")
        self.assertFalse(manifest["editor_plugin_enabled"])
        self.assertEqual(manifest["minimum_discovered_tests"], 1)
        self.assertEqual(manifest["zero_tests"], "FAIL")
        self.assertEqual(manifest["skipped_tests"], "FAIL")
        self.assertEqual(manifest["missing_junit"], "FAIL")
        self.assertEqual(manifest["tracked_authoring_mutation"], "FAIL")
        self.assertTrue(manifest["removal_procedure"])

    def test_runtime_workflow_executes_gut_and_proves_read_only_behavior(self) -> None:
        workflow = _text(WORKFLOW)
        for marker in (
            "name: Validate GUT 9.7.1 Formal Adoption",
            "Godot_v4.7.1-stable_linux.x86_64.zip",
            "./godot --headless --import --path .",
            "artifacts/gut/godot-import.log",
            "addons/gut/gut_cmdln.gd",
            "-gdir=res://tests/gut/unit",
            "-gdir=res://tests/gut/integration",
            "-ginclude_subdirs",
            "-gexit",
            "-gjunit_xml_file=res://artifacts/gut/junit.xml",
            "tools/validate_gut_junit.py",
            "authoring-surfaces.before.sha256",
            "authoring-surfaces.after.sha256",
            "diff -u",
            "actions/upload-artifact@v4",
        ):
            self.assertIn(marker, workflow)
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertNotIn("res://addons/gut/plugin.cfg", workflow)

    def test_junit_validator_accepts_passing_non_skipped_suite(self) -> None:
        module = _load_junit_validator()
        root = ElementTree.fromstring(
            '<testsuites tests="1" failures="0" errors="0" skipped="0">'
            '<testsuite tests="1" failures="0" errors="0" skipped="0">'
            '<testcase classname="Smoke" name="test_pass" />'
            '</testsuite></testsuites>'
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "junit.xml"
            ElementTree.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
            summary = module.validate_junit(path)
        self.assertEqual(summary["tests"], 1)
        self.assertEqual(summary["failures"], 0)
        self.assertEqual(summary["errors"], 0)
        self.assertEqual(summary["skipped"], 0)

    def test_junit_validator_rejects_zero_skipped_and_failures(self) -> None:
        module = _load_junit_validator()
        fixtures = (
            '<testsuite tests="0" failures="0" errors="0" skipped="0" />',
            '<testsuite tests="1" failures="0" errors="0" skipped="1">'
            '<testcase name="pending"><skipped /></testcase></testsuite>',
            '<testsuite tests="1" failures="1" errors="0" skipped="0">'
            '<testcase name="failed"><failure /></testcase></testsuite>',
        )
        for index, xml in enumerate(fixtures):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / "junit.xml"
                path.write_text(xml, encoding="utf-8")
                with self.assertRaises(ValueError):
                    module.validate_junit(path)

    def test_removal_procedure_has_consumers_clean_import_and_evidence_retention(self) -> None:
        text = _text(REMOVAL)
        for marker in (
            "SEPARATE_REVIEWED_CHANGE_ONLY",
            "addons/gut",
            ".gutconfig.json",
            "tests/gut",
            "gut-validation.yml",
            "consumer search",
            "clean import",
            "JUnit evidence",
            "HiGodot",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
