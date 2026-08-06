from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRESET = ROOT / "data/vertical_slice/vertical_slice_preset.json"
SCHEMA = ROOT / "data/vertical_slice/vertical_slice_schema.json"
SCRIPT_ROOT = ROOT / "scripts/vertical_slice"

EXPECTED_ITEM_FIELDS = {
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
FORBIDDEN_TOKENS = (
    "secondary_material",
    '"affixes"',
    "STANDARD",
    "GOOD",
    "PERFECT",
)


class VerticalSliceDataContractTests(unittest.TestCase):
    def test_task_one_files_exist(self) -> None:
        required = (
            PRESET,
            SCHEMA,
            ROOT / "scripts/vertical_slice/domain/vs_ledger_entry.gd",
            ROOT / "scripts/vertical_slice/domain/vs_item.gd",
            ROOT / "scripts/vertical_slice/domain/vs_save_envelope.gd",
            ROOT / "scripts/vertical_slice/services/vs_uid_service.gd",
            ROOT / "scripts/vertical_slice/services/vs_save_service.gd",
        )
        for path in required:
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))

    def test_preset_and_schema_versions_match(self) -> None:
        preset = json.loads(PRESET.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(preset["schema_version"], 1)
        self.assertEqual(preset["preset_version"], "VS-2026.08.06-A")
        self.assertEqual(schema["schema_version"], 1)
        self.assertEqual(schema["preset_version"], preset["preset_version"])
        self.assertFalse(preset["is_final_balance"])
        self.assertEqual(preset["authority"], "R2_BATCH_006_APPROVED_MAIN_CANON")

    def test_item_schema_is_explicit_and_uid_is_stable(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        item = schema["item"]
        self.assertEqual(set(item["required_fields"]), EXPECTED_ITEM_FIELDS)
        self.assertEqual(item["uid_pattern"], r"^BSI-[0-9a-f]{32}$")
        self.assertTrue(re.fullmatch(item["uid_pattern"], "BSI-0123456789abcdef0123456789abcdef"))
        self.assertEqual(item["affix_fields"], ["grade_affix", "catalyst_affix", "chronicle_affix"])
        self.assertEqual(item["ledger_policy"], "APPEND_ONLY_CONTIGUOUS_SEQUENCE")

    def test_save_envelope_owns_rng_and_resolved_events(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        envelope = schema["save_envelope"]
        self.assertEqual(envelope["schema_version"], 1)
        self.assertEqual(
            envelope["required_fields"],
            [
                "schema_version",
                "preset_version",
                "run_id",
                "run_rng_seed",
                "current_day",
                "items",
                "resolved_events",
            ],
        )
        self.assertEqual(envelope["write_policy"], "TEMP_FLUSH_RENAME_WITH_BACKUP")
        self.assertFalse(envelope["load_may_reroll_resolved_events"])

    def test_no_historical_fields_enter_new_namespace(self) -> None:
        paths = [PRESET, SCHEMA, *sorted(SCRIPT_ROOT.rglob("*.gd"))]
        self.assertGreaterEqual(len(paths), 7)
        for path in paths:
            source = path.read_text(encoding="utf-8")
            for token in FORBIDDEN_TOKENS:
                self.assertNotIn(token, source, f"{path.relative_to(ROOT)}: {token}")

    def test_task_one_stays_inside_approved_namespaces(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(
            schema["approved_namespaces"],
            [
                "scripts/vertical_slice/",
                "data/vertical_slice/",
                "scenes/vertical_slice/",
                "tests/vertical_slice/",
            ],
        )
        self.assertTrue(schema["general_product_implementation_remains_blocked"])
        self.assertTrue(schema["vertical_slice_implementation_approved"])


if __name__ == "__main__":
    unittest.main()
