from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "vertical_slice" / "content_result_contract.json"
REGISTRY = ROOT / "docs" / "planning" / "CURRENT_R3_R7_CANON_REGISTRY.json"
DOMAIN = ROOT / "scripts" / "vertical_slice" / "domain" / "vs_content_result_record.gd"
SAVE = ROOT / "scripts" / "vertical_slice" / "domain" / "vs_save_envelope.gd"
GUT = ROOT / "tests" / "gut" / "unit" / "vertical_slice" / "test_vs_content_result_record.gd"
A2 = ROOT / "docs" / "operations" / "BLACKSMITH_P2_CONTENT_RESULT_FOUNDATION_A2_CONTRACT.json"

EXPECTED_POLICIES = {
    "ADVENTURER_01": "SINGLE_PRIMARY_ITEM",
    "ADVENTURER_02": "SINGLE_PRIMARY_ITEM",
    "SOLDIER_01": "BATCH_ITEMS_ONE_OR_MORE",
    "COLLECTOR_01": "SINGLE_PRIMARY_ITEM",
    "GLADIATOR_01": "SINGLE_PRIMARY_ITEM",
    "NOBLE_01": "SINGLE_PRIMARY_ITEM",
    "SOLDIER_02": "SINGLE_PRIMARY_ITEM",
    "COLLECTOR_02": "SINGLE_PRIMARY_ITEM",
    "GLADIATOR_02": "LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT",
}

REQUIRED_FIELDS = [
    "schema_version",
    "record_type",
    "event_id",
    "source_decision_id",
    "content_id",
    "customer_id",
    "occurred_at_game_day",
    "item_refs",
    "result_axes",
    "causal_reasons",
    "primary_next_action",
]

FORBIDDEN_FIELDS = {
    "score",
    "total_score",
    "fit_score",
    "prestige_score",
    "artistry_delta",
    "chronicle_affix_grant",
    "history_transfer",
    "result_probability",
    "reward_value",
}


class VerticalSliceContentResultContractTests(unittest.TestCase):
    def test_contract_mirrors_current_d01_d09_registry(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

        approved = {
            entry["contract"]["content_id"]: entry
            for entry in registry["current_decisions"]
        }
        declared = {
            entry["content_id"]: entry
            for entry in contract["content_contracts"]
        }

        self.assertEqual(set(declared), set(approved))
        self.assertEqual(set(declared), set(EXPECTED_POLICIES))
        for content_id, expected in approved.items():
            actual = declared[content_id]
            self.assertEqual(actual["decision_id"], expected["id"], content_id)
            self.assertEqual(
                actual["customer_id"],
                expected["contract"]["customer_id"],
                content_id,
            )
            self.assertEqual(
                actual["result_axes"],
                expected["contract"]["result_axes"],
                content_id,
            )
            self.assertEqual(
                actual["item_ref_policy"],
                EXPECTED_POLICIES[content_id],
                content_id,
            )

    def test_scope_is_foundation_only_and_backward_compatible(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(contract["schema_version"], 1)
        self.assertEqual(contract["record_type"], "CONTENT_RESULT_V1")
        self.assertEqual(contract["save_container"], "active_run.resolved_events")
        self.assertEqual(contract["required_fields"], REQUIRED_FIELDS)
        self.assertEqual(contract["item_ref_required_fields"], ["role", "uid"])
        self.assertEqual(contract["reason_count"], {"minimum": 2, "maximum": 4})
        self.assertEqual(contract["uid_pattern"], "^BSI-[0-9a-f]{32}$")
        self.assertEqual(contract["state_token_pattern"], "^[A-Z0-9_]+$")
        self.assertFalse(contract["implements_result_resolution"])
        self.assertFalse(contract["implements_customer_or_schedule_logic"])
        self.assertFalse(contract["changes_save_schema_version"])
        self.assertEqual(set(contract["forbidden_fields"]), FORBIDDEN_FIELDS)

    def test_contract_has_no_result_value_catalog_or_hidden_progression(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        for entry in contract["content_contracts"]:
            self.assertEqual(len(entry["result_axes"]), 3, entry["content_id"])
            self.assertNotIn("result_values", entry)
            self.assertNotIn("probability", entry)
            self.assertNotIn("reward", entry)
            self.assertNotIn("artistry", entry)
            self.assertNotIn("chronicle", entry)
            self.assertNotIn("score", entry)

    def test_runtime_and_gut_files_exist(self) -> None:
        for path in (DOMAIN, SAVE, GUT, A2):
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))

    def test_gdscript_contract_contains_every_registry_tuple_and_policy(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        source = DOMAIN.read_text(encoding="utf-8")
        self.assertIn("class_name VSContentResultRecord", source)
        self.assertIn('const RECORD_TYPE := "CONTENT_RESULT_V1"', source)
        self.assertIn("RESULT_AXIS_SET_MISMATCH", source)
        self.assertIn("DUPLICATE_ITEM_UID", source)
        self.assertIn("UNKNOWN_FIELD:", source)
        for entry in contract["content_contracts"]:
            for token in (
                entry["decision_id"],
                entry["content_id"],
                entry["customer_id"],
                entry["item_ref_policy"],
                *entry["result_axes"],
            ):
                self.assertIn(token, source)

    def test_save_envelope_selectively_validates_only_typed_records(self) -> None:
        source = SAVE.read_text(encoding="utf-8")
        self.assertIn("vs_content_result_record.gd", source)
        self.assertIn('record_type", ""', source)
        self.assertIn("CONTENT_RESULT_V1", source)
        self.assertIn("CONTENT_RESULT_EVENT_KEY_MISMATCH", source)
        self.assertIn("CONTENT_RESULT:%s:%s", source)


if __name__ == "__main__":
    unittest.main()
