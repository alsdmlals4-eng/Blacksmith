from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.test_vertical_slice_content_result_contract import VerticalSliceContentResultContractTests  # noqa: F401
from tests.test_universal_loop_capsule_migration import UniversalLoopCapsuleMigrationTests  # noqa: F401

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

    def test_vertical_slice_preset_shape(self) -> None:
        preset = json.loads(PRESET.read_text(encoding="utf-8"))
        self.assertEqual(preset["schema_version"], 1)
        self.assertEqual(preset["preset_version"], "BS-VS-1")
        self.assertEqual(preset["crafting_grades"], GRADE_IDS)
        self.assertEqual(preset["crafting_grade_probabilities"], EXPECTED_PROBABILITIES)
        self.assertEqual(preset["materials"], EXPECTED_MATERIALS)

    def test_vertical_slice_schema_contract(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["schema_version"], 1)
        self.assertEqual(schema["preset_version"], "BS-VS-1")
        self.assertEqual(schema["item_fields"], sorted(ITEM_FIELDS))
        self.assertEqual(schema["save_fields"], SAVE_FIELDS)

    def test_item_fields_are_exact(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(set(schema["item_fields"]), ITEM_FIELDS)
        self.assertEqual(len(schema["item_fields"]), len(ITEM_FIELDS))

    def test_forbidden_new_namespace_tokens_absent(self) -> None:
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                PRESET,
                SCHEMA,
                ROOT / "scripts/vertical_slice/domain/vs_item.gd",
                ROOT / "scripts/vertical_slice/domain/vs_save_envelope.gd",
            )
        )
        for token in FORBIDDEN_NEW_NAMESPACE_TOKENS:
            self.assertNotIn(token, corpus)


if __name__ == "__main__":
    unittest.main()
