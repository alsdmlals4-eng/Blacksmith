from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
ADAPTER = TOOLS / "export_repair_economy_rm_tool_003.py"
RUNNER = TOOLS / "run_repair_economy_sensitivity.py"
CANON = ROOT / "docs" / "planning" / "BLACKSMITH_REPAIR_ECONOMY_REBASE_20260826.json"
INPUT = ROOT / "docs" / "planning" / "BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_INPUT_20260826.json"
EXPECTED_BASE_COMMIT = "aaa94caf5772c262f023dd9e80fd4b8bbffd85db"
EXPECTED_BASE_ANALYZER_BLOB = "a99ae419fd755b6e19f3dee232dd3a11cd74d4ae"
EXPECTED_VARIANTS = {
    0.5: "loss_b_0p5",
    0.65: "loss_b_0p65",
    0.8: "loss_b_0p8",
}


def load_module(path: Path, name: str):
    if not path.is_file():
        raise AssertionError(f"required module does not exist: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()


class RepairEconomyRmTool003IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = load_module(RUNNER, "blacksmith_repair_economy_runner")
        cls.canon = json.loads(CANON.read_text(encoding="utf-8"))
        cls.sensitivity_input = json.loads(INPUT.read_text(encoding="utf-8"))

    def load_adapter(self):
        return load_module(ADAPTER, "blacksmith_repair_economy_rm_tool_003_adapter")

    def build_manifest(self, *, sensitivity_input=None, source_commit: str = "a" * 40):
        adapter = self.load_adapter()
        return adapter.build_manifest(
            copy.deepcopy(self.canon),
            copy.deepcopy(sensitivity_input or self.sensitivity_input),
            source_commit=source_commit,
            canon_path=CANON.relative_to(ROOT).as_posix(),
            input_path=INPUT.relative_to(ROOT).as_posix(),
        )

    def load_base_analyzer(self):
        raw = os.environ.get("BASE_RM_TOOL_003_PATH")
        if not raw:
            self.skipTest("BASE_RM_TOOL_003_PATH is required only for exact-Base integration")
        path = Path(raw).resolve()
        self.assertTrue(path.is_file(), path)
        self.assertEqual(EXPECTED_BASE_ANALYZER_BLOB, git_blob_sha1(path))
        return load_module(path, "exact_base_rm_tool_003_analyzer")

    def test_adapter_exists_and_pins_the_exact_observed_base_analyzer(self) -> None:
        adapter = self.load_adapter()
        self.assertEqual(EXPECTED_BASE_COMMIT, adapter.BASE_SOURCE_COMMIT)
        self.assertEqual(EXPECTED_BASE_ANALYZER_BLOB, adapter.BASE_ANALYZER_BLOB_SHA)
        self.assertEqual("BS-REPAIR-20260826-31", adapter.DECISION_ID)

    def test_manifest_preserves_current_owner_and_claim_ceiling(self) -> None:
        manifest = self.build_manifest()
        context = manifest["integration_context"]

        self.assertEqual("BLACKSMITH", manifest["project_id"])
        self.assertEqual("loss_b_0p65", manifest["baseline_variant"])
        self.assertEqual("MATHEMATICAL_MODEL", manifest["analysis_context"]["adapter_evidence_mode"])
        self.assertEqual("NOT_VERIFIED", manifest["analysis_context"]["adapter_equivalence"]["status"])
        self.assertEqual(
            [
                "PLANNING_MODEL_ONLY",
                "RUNTIME_EQUIVALENCE_NOT_VERIFIED",
                "FINAL_PRODUCT_BALANCE_NOT_APPROVED",
                "HUMAN_PLAYER_EVIDENCE_NOT_RUN",
            ],
            manifest["evidence_ceiling"],
        )
        self.assertEqual("BS-REPAIR-20260826-31", context["decision_id"])
        self.assertEqual(EXPECTED_BASE_COMMIT, context["base_source_commit"])
        self.assertEqual(EXPECTED_BASE_ANALYZER_BLOB, context["base_analyzer_blob_sha"])
        self.assertEqual(
            "READ_ONLY_EXACT_ANALYZER_NOT_PROJECT_BASE_RELEASE_ADOPTION",
            context["base_dependency_role"],
        )
        self.assertEqual(
            "MANUAL_REVALIDATION_REQUIRED_BEFORE_PIN_CHANGE",
            context["base_update_policy"],
        )
        self.assertEqual(
            "DETERMINISTIC_PROJECT_CASE_PAIRING_ID_NOT_RNG_SAMPLE",
            context["seed_semantics"],
        )
        self.assertEqual(
            "TEMPORARY_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE",
            context["numeric_status"],
        )

    def test_all_coefficient_variants_use_the_same_stable_event_sample(self) -> None:
        manifest = self.build_manifest()
        self.assertEqual(15, len(manifest["runs"]))

        by_variant: dict[str, list[dict[str, object]]] = {}
        for run in manifest["runs"]:
            by_variant.setdefault(run["variant"], []).append(run)

        self.assertEqual(set(EXPECTED_VARIANTS.values()), set(by_variant))
        expected_metric_keys = {
            "gold",
            "recovery",
            "loss_ratio",
            "new_current",
            "post_scar_max",
            "material_use",
            "scar_skip_flag",
        }
        reference_seed_to_case = None
        for variant in EXPECTED_VARIANTS.values():
            runs = by_variant[variant]
            self.assertEqual(5, len(runs))
            seed_to_case = {run["seed"]: run["project_case_id"] for run in runs}
            self.assertEqual(5, len(seed_to_case))
            if reference_seed_to_case is None:
                reference_seed_to_case = seed_to_case
            else:
                self.assertEqual(reference_seed_to_case, seed_to_case)
            for run in runs:
                self.assertEqual(expected_metric_keys, set(run["metrics"]))
                self.assertEqual(["REPAIR_NOW"], run["choices"])
                self.assertEqual([], run["failures"])

    def test_event_seed_identity_survives_input_reordering(self) -> None:
        original = self.build_manifest()
        reordered_input = copy.deepcopy(self.sensitivity_input)
        reordered_input["events"] = list(reversed(reordered_input["events"]))
        reordered = self.build_manifest(sensitivity_input=reordered_input)

        def identity_map(manifest):
            return {
                (run["variant"], run["project_case_id"]): run["seed"]
                for run in manifest["runs"]
            }

        self.assertEqual(identity_map(original), identity_map(reordered))

    def test_canon_and_input_sweep_mismatch_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.sensitivity_input)
        invalid["loss_coefficients"] = [0.5, 0.65]
        with self.assertRaisesRegex(ValueError, "loss coefficient sweep"):
            self.build_manifest(sensitivity_input=invalid)

    def test_exact_base_analyzer_consumes_the_manifest(self) -> None:
        base = self.load_base_analyzer()
        report = base.analyze_manifest(self.build_manifest())
        sweep = report["parameter_sweeps"][0]

        self.assertTrue(sweep["seed_set_equal_across_points"])
        self.assertTrue(sweep["metric_seed_set_equal_across_points"])
        self.assertEqual(5, sweep["seed_count_per_point"])
        self.assertEqual(5, sweep["metric_seed_count_per_point"])
        self.assertEqual(
            [(0.5, 25.0), (0.65, 31.0), (0.8, 37.0)],
            [(point["parameter_value"], point["metric_value"]) for point in sweep["series"]],
        )
        self.assertIn("same_deterministic_project_case_set", sweep["locked_parameters"])
        self.assertEqual(1, sweep["threshold_crossing_count"])
        crossing = sweep["threshold_crossings"][0]
        self.assertEqual("EXACT_OBSERVED_POINT", crossing["kind"])
        self.assertEqual(0.65, crossing["estimated_parameter_value"])
        self.assertEqual("OBSERVED_POINT_NOT_PROJECT_TRUTH", crossing["evidence_ceiling"])
        self.assertFalse(sweep["automatic_best_value"])
        self.assertEqual(
            "MATHEMATICAL_MODEL_ONLY_RUNTIME_EQUIVALENCE_NOT_VERIFIED",
            report["adapter_evidence"]["claim_ceiling"],
        )

    def test_cli_writes_a_manifest_consumable_by_the_exact_base_cli(self) -> None:
        base_path_raw = os.environ.get("BASE_RM_TOOL_003_PATH")
        if not base_path_raw:
            self.skipTest("BASE_RM_TOOL_003_PATH is required only for exact-Base integration")
        base_path = Path(base_path_raw).resolve()
        self.assertEqual(EXPECTED_BASE_ANALYZER_BLOB, git_blob_sha1(base_path))

        with tempfile.TemporaryDirectory() as temporary:
            manifest_path = Path(temporary) / "repair-rm-tool-003-manifest.json"
            export = subprocess.run(
                [
                    sys.executable,
                    str(ADAPTER),
                    "--project-root",
                    str(ROOT),
                    "--source-commit",
                    "b" * 40,
                    "--output",
                    str(manifest_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, export.returncode, export.stderr)
            self.assertTrue(manifest_path.is_file())

            analyzed = subprocess.run(
                [sys.executable, str(base_path), str(manifest_path)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, analyzed.returncode, analyzed.stderr)
            report = json.loads(analyzed.stdout)
            self.assertEqual(15, sum(item["run_count"] for item in report["variants"].values()))
            self.assertEqual(
                "MATHEMATICAL_MODEL_ONLY_RUNTIME_EQUIVALENCE_NOT_VERIFIED",
                report["adapter_evidence"]["claim_ceiling"],
            )


if __name__ == "__main__":
    unittest.main()
