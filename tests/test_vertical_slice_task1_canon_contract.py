from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.test_vertical_slice_content_result_contract import VerticalSliceContentResultContractTests  # noqa: F401
from tests.test_universal_loop_a2_burnin_authority import UniversalLoopA2BurninAuthorityTests  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
PRESET = ROOT / "data/vertical_slice/vertical_slice_preset.json"
SCHEMA = ROOT / "data/vertical_slice/vertical_slice_schema.json"

GRADE_IDS = [
    "CRAFT_NORMAL",
    "CRAFT_SUPERIOR",
    "CRAFT_FINE",
    "CRAFT_MASTERWORK",
    "CRAFT_LEGENDARY",
]
EXPECTED_PROBABILITIES = {
    "LOW": {
        "CRAFT_NORMAL": 0.85,
        "CRAFT_SUPERIOR": 0.14,
        "CRAFT_FINE": 0.01,
        "CRAFT_MASTERWORK": 0.0,
        "CRAFT_LEGENDARY": 0.0,
    },
    "MID": {
        "CRAFT_NORMAL": 0.60,
        "CRAFT_SUPERIOR": 0.30,
        "CRAFT_FINE": 0.09,
        "CRAFT_MASTERWORK": 0.01,
        "CRAFT_LEGENDARY": 0.0,
    },
    "HIGH": {
        "CRAFT_NORMAL": 0.30,
        "CRAFT_SUPERIOR": 0.40,
        "CRAFT_FINE": 0.24,
        "CRAFT_MASTERWORK": 0.055,
        "CRAFT_LEGENDARY": 0.005,
    },
}
EXPECTED_MATERIALS = {
    "iron": {
        "role_fit_delta": 0,
        "artistry_delta": 0,
        "weight_point": 15,
        "function_capacity": 0,
    },
    "silver": {
        "role_fit_delta": -5,
        "artistry_delta": 4,
        "weight_point": 10,
        "function_capacity": 1,
    },
    "meteor_iron": {
        "role_fit_delta": 5,
        "artistry_delta": 2,
        "weight_point": 20,
        "function_capacity": 1,
    },
}
ITEM_FIELDS = {
    "schema_version",
    "uid",
    "birth_rng_seed",
    "primary_material_id",
    "equipment_group",
    "role_profile",
    "crafting_grade",
    "artistry",
    "raw_role_stat",
    "weight_point",
    "function_capacity",
    "functions",
    "grade_affix",
    "catalyst_affix",
    "chronicle_affix",
    "enhancement_level",
    "enhancement_failure_streak",
    "used_precision_milestones",
    "damage_state",
    "owner_id",
    "ledger",
}
SAVE_FIELDS = [
    "schema_version",
    "preset_version",
    "saved_at_utc",
    "active_run",
    "items_by_uid",
    "customer_state",
    "schedule_state",
    "global_ledger_sequence",
]
FORBIDDEN_NEW_NAMESPACE_TOKENS = (
    "secondary_material",
    '"affixes"',
    '"STANDARD"',
    '"GOOD"',
    '"PERFECT"',
    '"RARE"',
)


class VerticalSliceTask1CanonContractTests(unittest.TestCase):
    def test_required_runtime_and_gut_files_exist(self) -> None:
        required = (
            PRESET,
            SCHEMA,
            ROOT / "scripts/vertical_slice/domain/vs_ledger_entry.gd",
            ROOT / "scripts/vertical_slice/domain/vs_item.gd",
            ROOT / "scripts/vertical_slice/domain/vs_save_envelope.gd",
            ROOT / "scripts/vertical_slice/services/vs_uid_service.gd",
            ROOT / "scripts/vertical_slice/services/vs_save_service.gd",
            ROOT / "tests/gut/unit/vertical_slice/test_vs_item.gd",
            ROOT / "tests/gut/unit/vertical_slice/test_vs_save_service.gd",
        )
        for path in required:
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))

    def test_preset_matches_approved_batch_006_values(self) -> None:
        preset = json.loads(PRESET.read_text(encoding="utf-8"))
        self.assertEqual(preset["schema_version"], 1)
        self.assertEqual(preset["preset_version"], "VS-2026.08.06-A")
        self.assertEqual(preset["authority"], "R2_BATCH_006_APPROVED_MAIN_CANON")
        self.assertFalse(preset["is_final_balance"])
        materials = {entry["id"]: entry for entry in preset["primary_materials"]}
        self.assertEqual(set(materials), set(EXPECTED_MATERIALS))
        for material_id, expected in EXPECTED_MATERIALS.items():
            for key, value in expected.items():
                self.assertEqual(materials[material_id][key], value, f"{material_id}.{key}")
        self.assertEqual(preset["crafting_grade_probabilities"], EXPECTED_PROBABILITIES)
        for tier in EXPECTED_PROBABILITIES.values():
            self.assertAlmostEqual(sum(tier.values()), 1.0)

    def test_schema_matches_save_item_and_ledger_canon(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["task1_active_namespaces"], [
            "scripts/vertical_slice/",
            "data/vertical_slice/",
            "tests/gut/unit/vertical_slice/",
        ])
        self.assertEqual(schema["future_planned_namespaces"], ["scenes/vertical_slice/"])
        self.assertTrue(schema["general_product_implementation_remains_blocked"])
        self.assertTrue(schema["vertical_slice_implementation_approved"])
        self.assertEqual(set(schema["item"]["required_fields"]), ITEM_FIELDS)
        self.assertEqual(schema["item"]["crafting_grades"], GRADE_IDS)
        self.assertEqual(schema["ledger_entry"]["game_day_field"], "occurred_at_game_day")
        self.assertIn("occurred_at_game_day", schema["ledger_entry"]["required_fields"])
        self.assertNotIn("game_day", schema["ledger_entry"]["required_fields"])
        self.assertEqual(schema["save_envelope"]["required_fields"], SAVE_FIELDS)
        self.assertEqual(schema["save_envelope"]["items_field"], "items_by_uid")
        self.assertFalse(schema["save_envelope"]["load_may_reroll_resolved_events"])

    def test_new_runtime_namespace_rejects_legacy_tokens(self) -> None:
        runtime_paths = [PRESET, SCHEMA, *sorted((ROOT / "scripts/vertical_slice").rglob("*.gd"))]
        self.assertGreaterEqual(len(runtime_paths), 7)
        for path in runtime_paths:
            source = path.read_text(encoding="utf-8")
            for token in FORBIDDEN_NEW_NAMESPACE_TOKENS:
                self.assertNotIn(token, source, f"{path.relative_to(ROOT)}: {token}")

    def test_validation_routes_to_python_and_gut_with_minimum_product_exemption(self) -> None:
        python_workflow = (ROOT / ".github/workflows/python-validation.yml").read_text(encoding="utf-8")
        base_gate = (ROOT / ".github/workflows/validate-base-v9-adoption.yml").read_text(encoding="utf-8")
        godot_workflow = (ROOT / ".github/workflows/godot-validation.yml").read_text(encoding="utf-8")
        gut_workflow = (ROOT / ".github/workflows/gut-validation.yml").read_text(encoding="utf-8")
        self.assertIn("tests.test_vertical_slice_task1_canon_contract", python_workflow)
        self.assertIn("^(src/|scripts/|scenes/|data/|assets/|addons/|project", base_gate)
        self.assertIn("^(scripts|data)/vertical_slice/", base_gate)
        self.assertNotIn("^(scripts|scenes|data)/vertical_slice/", base_gate)
        self.assertNotIn("scenes/vertical_slice/.*", base_gate)
        self.assertIn("approved-task2-published-product-paths.txt", base_gate)
        for exact_path in (
            "scenes/vertical_slice/main_menu.tscn",
            "scenes/vertical_slice/vertical_slice_app.tscn",
            "scenes/vertical_slice/screens/vs_workshop_screen.tscn",
        ):
            self.assertIn(exact_path, base_gate)
        self.assertIn("tests/gut/**", gut_workflow)
        self.assertNotIn("tests/vertical_slice/unit/test_vs_item.gd", godot_workflow)
        self.assertNotIn("tests/vertical_slice/unit/test_vs_save_service.gd", godot_workflow)

    def test_gut_tests_use_formal_authority(self) -> None:
        for relative in (
            "tests/gut/unit/vertical_slice/test_vs_item.gd",
            "tests/gut/unit/vertical_slice/test_vs_save_service.gd",
        ):
            source = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn('extends "res://addons/gut/test.gd"', source)


if __name__ == "__main__":
    unittest.main()
