# Blacksmith P2 Content Result Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a backward-compatible `CONTENT_RESULT_V1` record that validates approved D01–D09 decision/customer/UID/result-axis identity inside the existing vertical-slice `resolved_events` save container.

**Architecture:** Keep `VSSaveEnvelope` schema version 1 and its existing generic Dictionary events. Add a strict `VSContentResultRecord` domain object and a versioned JSON contract; `VSSaveEnvelope.from_dict()` invokes it only when an event explicitly declares `record_type: CONTENT_RESULT_V1`. Existing forge/arena fixtures remain pass-through.

**Tech Stack:** Godot 4.7.1, GDScript 2.0, GUT 9.7.1, JSON, Python `unittest`, GitHub Actions, existing protected-change adapter gate.

## Global Constraints

- Decision: `BS-VS-P2-20260813-01`.
- Source main: `35d86bf88497e09ebe59d37a2ab5a0b32f1e595f`.
- Work only on `feat/p2-content-result-foundation-20260813`.
- `RED → GREEN → REFACTOR` for every implementation task.
- Do not modify `project.godot`, scenes, resources, addons, plugin/autoload settings, or node graphs.
- Do not implement customer formulas, schedule progression, result probabilities, reward/economy values, UI, Task3, or Decision10.
- Do not change SaveEnvelope schema version 1 or add a new top-level save field.
- Existing generic `resolved_events` entries must remain valid and unchanged.
- Exact result values are non-canonical uppercase tokens; only axis identity is authoritative.
- Every content record has 2–4 distinct causal reasons and one primary next action.
- No aggregate score, Artistry delta, automatic Chronicle grant, or replacement history transfer field.
- Protected product changes require `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json` and PR label `approved-protected-change`.
- Android, accessibility, performance, actual play, and human playtest remain `NOT_RUN`.

---

## File Structure

### Data contract

- Create `data/vertical_slice/content_result_contract.json`: exact D01–D09 tuple, axis names, item-reference policy, required fields, and forbidden fields.

### Domain

- Create `scripts/vertical_slice/domain/vs_content_result_record.gd`: strict deserialize/serialize and validation.
- Modify `scripts/vertical_slice/domain/vs_save_envelope.gd`: validate only explicitly typed content-result events.

### Tests

- Create `tests/test_vertical_slice_content_result_contract.py`: compare JSON contract to current R3 registry and protect scope.
- Modify `tests/test_vertical_slice_task1_canon_contract.py`: import the new Python TestCase so existing CI executes it without workflow edits.
- Create `tests/gut/unit/vertical_slice/test_vs_content_result_record.gd`: domain behavior.
- Modify `tests/gut/unit/vertical_slice/test_vs_save_service.gd`: typed record round trip and legacy pass-through.

### Operations

- Create `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json`: one-shot exact protected path approval.
- Existing `docs/operations/BLACKSMITH_P2_CONTENT_RESULT_FOUNDATION_A2_CONTRACT.json` owns scope.

---

### Task 1: Lock the D01–D09 machine contract

**Files:**
- Create: `data/vertical_slice/content_result_contract.json`
- Create: `tests/test_vertical_slice_content_result_contract.py`
- Modify: `tests/test_vertical_slice_task1_canon_contract.py`

**Interfaces:**
- Consumes: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- Produces: JSON `content_contracts[]` indexed by `content_id`
- Produces constants: record fields, item roles, UID/state token regexes, reason-count bounds, forbidden fields

- [ ] **Step 1: Write the failing Python contract test**

Create `tests/test_vertical_slice_content_result_contract.py` with these checks:

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/vertical_slice/content_result_contract.json"
REGISTRY = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
DOMAIN = ROOT / "scripts/vertical_slice/domain/vs_content_result_record.gd"
SAVE = ROOT / "scripts/vertical_slice/domain/vs_save_envelope.gd"
GUT = ROOT / "tests/gut/unit/vertical_slice/test_vs_content_result_record.gd"


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
        for content_id, expected in approved.items():
            actual = declared[content_id]
            self.assertEqual(actual["decision_id"], expected["id"])
            self.assertEqual(actual["customer_id"], expected["contract"]["customer_id"])
            self.assertEqual(actual["result_axes"], expected["contract"]["result_axes"])

    def test_scope_is_foundation_only(self) -> None:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(contract["record_type"], "CONTENT_RESULT_V1")
        self.assertEqual(contract["reason_count"], {"minimum": 2, "maximum": 4})
        self.assertEqual(contract["save_container"], "active_run.resolved_events")
        self.assertFalse(contract["implements_result_resolution"])
        self.assertFalse(contract["implements_customer_or_schedule_logic"])
        self.assertFalse(contract["changes_save_schema_version"])

    def test_runtime_and_gut_files_exist(self) -> None:
        for path in (DOMAIN, SAVE, GUT):
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))
```

- [ ] **Step 2: Route the test through existing CI**

Add this import near the top of `tests/test_vertical_slice_task1_canon_contract.py`:

```python
from tests.test_vertical_slice_content_result_contract import VerticalSliceContentResultContractTests  # noqa: F401
```

Do not edit GitHub workflow files.

- [ ] **Step 3: Run/observe RED**

Run:

```bash
python -m unittest tests.test_vertical_slice_task1_canon_contract -v
```

Expected: errors because `content_result_contract.json`, `vs_content_result_record.gd`, and its GUT test do not exist.

- [ ] **Step 4: Create the machine contract**

Create `data/vertical_slice/content_result_contract.json` with:

```json
{
  "schema_version": 1,
  "record_type": "CONTENT_RESULT_V1",
  "authority": "BS-VS-P2-20260813-01_EXISTING_R3_D01_D09_CANON_ONLY",
  "save_container": "active_run.resolved_events",
  "implements_result_resolution": false,
  "implements_customer_or_schedule_logic": false,
  "changes_save_schema_version": false,
  "uid_pattern": "^BSI-[0-9a-f]{32}$",
  "state_token_pattern": "^[A-Z0-9_]+$",
  "reason_count": {"minimum": 2, "maximum": 4},
  "required_fields": [
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
    "primary_next_action"
  ],
  "item_ref_required_fields": ["role", "uid"],
  "allowed_item_roles": [
    "PRIMARY_ITEM",
    "BATCH_ITEM",
    "LEGACY_ITEM",
    "REPLACEMENT_ITEM"
  ],
  "forbidden_fields": [
    "score",
    "total_score",
    "fit_score",
    "prestige_score",
    "artistry_delta",
    "chronicle_affix_grant",
    "history_transfer",
    "result_probability",
    "reward_value"
  ],
  "content_contracts": []
}
```

Populate exactly nine `content_contracts` from the approved registry. Use the axis order in the registry. Set policies:

```text
ADVENTURER_01 SINGLE_PRIMARY_ITEM
ADVENTURER_02 SINGLE_PRIMARY_ITEM
SOLDIER_01 BATCH_ITEMS_ONE_OR_MORE
COLLECTOR_01 SINGLE_PRIMARY_ITEM
GLADIATOR_01 SINGLE_PRIMARY_ITEM
NOBLE_01 SINGLE_PRIMARY_ITEM
SOLDIER_02 SINGLE_PRIMARY_ITEM
COLLECTOR_02 SINGLE_PRIMARY_ITEM
GLADIATOR_02 LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT
```

- [ ] **Step 5: Run the focused Python contract**

```bash
python -m unittest tests.test_vertical_slice_task1_canon_contract -v
```

Expected: registry/scope checks pass; file-existence check still fails until Task 2 creates runtime files.

- [ ] **Step 6: Commit**

```bash
git add data/vertical_slice/content_result_contract.json tests/test_vertical_slice_content_result_contract.py tests/test_vertical_slice_task1_canon_contract.py
git commit -m "test: lock vertical slice content result contract"
```

---

### Task 2: Implement strict content-result domain validation

**Files:**
- Create: `scripts/vertical_slice/domain/vs_content_result_record.gd`
- Create: `tests/gut/unit/vertical_slice/test_vs_content_result_record.gd`

**Interfaces:**
- Produces: `VSContentResultRecord.from_dict(value: Dictionary) -> VSContentResultRecord`
- Produces: `VSContentResultRecord.to_dict() -> Dictionary`
- Produces: `validation_errors: Array[String]`
- Uses no scene, node, autoload, or project setting.

- [ ] **Step 1: Write the failing GUT tests**

The test file must cover:

```gdscript
extends "res://addons/gut/test.gd"

const RecordScript = preload("res://scripts/vertical_slice/domain/vs_content_result_record.gd")

func _uid(hex_char: String) -> String:
    return "BSI-" + hex_char.repeat(32)

func _nadia_record() -> Dictionary:
    return {
        "schema_version": 1,
        "record_type": "CONTENT_RESULT_V1",
        "event_id": "nadia-result-001",
        "source_decision_id": "BS-CONTENT-20260811-01",
        "content_id": "ADVENTURER_01",
        "customer_id": "NADIA_VENN",
        "occurred_at_game_day": 4,
        "item_refs": [{"role": "PRIMARY_ITEM", "uid": _uid("a")}],
        "result_axes": {
            "EXPEDITION_RETURN_STATE": "RETURNED",
            "RECOVERY_STATE": "PARTIAL_RECOVERY",
            "ITEM_UID_LIFECYCLE_STATE": "DAMAGED_RETURN"
        },
        "causal_reasons": ["LOAD_GATE_PASSED", "UTILITY_MATCHED"],
        "primary_next_action": "REPAIR_ITEM"
    }

func test_valid_single_item_record_round_trips() -> void:
    var record = RecordScript.from_dict(_nadia_record())
    assert_true(record.validation_errors.is_empty())
    assert_eq(record.to_dict(), _nadia_record())

func test_wrong_axis_set_is_rejected() -> void:
    var value := _nadia_record()
    value["result_axes"].erase("RECOVERY_STATE")
    value["result_axes"]["SCORE"] = "HIGH"
    var record = RecordScript.from_dict(value)
    assert_true(record.validation_errors.has("RESULT_AXIS_SET_MISMATCH"))

func test_batch_requires_unique_batch_items() -> void:
    var value := _nadia_record()
    value["event_id"] = "marek-result-001"
    value["source_decision_id"] = "BS-CONTENT-20260811-03"
    value["content_id"] = "SOLDIER_01"
    value["customer_id"] = "MAREK_OLDEN"
    value["item_refs"] = [
        {"role": "BATCH_ITEM", "uid": _uid("b")},
        {"role": "BATCH_ITEM", "uid": _uid("b")}
    ]
    value["result_axes"] = {
        "UNIT_MISSION_STATE": "COMPLETED",
        "STANDARD_ADOPTION_STATE": "CONDITIONAL",
        "BATCH_ITEM_LIFECYCLE_STATE": "MIXED_RETURN"
    }
    var record = RecordScript.from_dict(value)
    assert_true(record.validation_errors.has("DUPLICATE_ITEM_UID"))

func test_replacement_uid_must_differ_from_legacy_uid() -> void:
    var value := _nadia_record()
    value["event_id"] = "kyle-result-001"
    value["source_decision_id"] = "BS-CONTENT-20260811-09"
    value["content_id"] = "GLADIATOR_02"
    value["customer_id"] = "KYLE_VAREN"
    value["item_refs"] = [
        {"role": "LEGACY_ITEM", "uid": _uid("c")},
        {"role": "REPLACEMENT_ITEM", "uid": _uid("c")}
    ]
    value["result_axes"] = {
        "VETERAN_RETURN_STATE": "RETURNED",
        "EQUIPMENT_CONTINUITY_STATE": "RETIRE_AND_REPLACE",
        "ITEM_UID_LINEAGE_STATE": "OLD_RETIRED_NEW_ASSIGNED"
    }
    var record = RecordScript.from_dict(value)
    assert_true(record.validation_errors.has("DUPLICATE_ITEM_UID"))

func test_unknown_score_field_is_rejected() -> void:
    var value := _nadia_record()
    value["total_score"] = 99
    var record = RecordScript.from_dict(value)
    assert_true(record.validation_errors.has("UNKNOWN_FIELD:total_score"))
```

Also test wrong decision/customer tuple, reason counts 1 and 5, duplicate reasons, invalid state token, invalid UID, missing legacy item, and valid Kyle replacement.

- [ ] **Step 2: Observe RED in GUT**

Expected: parse/preload failure because `VSContentResultRecord` does not exist.

- [ ] **Step 3: Implement the domain class**

Create a RefCounted class with the exact public fields from the record contract. Use constants:

```gdscript
class_name VSContentResultRecord
extends RefCounted

const SCHEMA_VERSION := 1
const RECORD_TYPE := "CONTENT_RESULT_V1"
const REQUIRED_FIELDS := [ ... ]
const ITEM_REF_REQUIRED_FIELDS := ["role", "uid"]
const UID_PATTERN := "^BSI-[0-9a-f]{32}$"
const STATE_TOKEN_PATTERN := "^[A-Z0-9_]+$"
const CONTENT_CONTRACTS := {
    "ADVENTURER_01": {
        "decision_id": "BS-CONTENT-20260811-01",
        "customer_id": "NADIA_VENN",
        "result_axes": [
            "EXPEDITION_RETURN_STATE",
            "RECOVERY_STATE",
            "ITEM_UID_LIFECYCLE_STATE"
        ],
        "item_ref_policy": "SINGLE_PRIMARY_ITEM"
    },
    ...
}
```

Implementation rules:

- collect missing fields before reading values;
- reject every unknown top-level field as `UNKNOWN_FIELD:<name>`;
- arrays and dictionaries must have the expected Variant type;
- item ref dictionaries reject unknown fields and require exact `role`/`uid`;
- all UID values unique;
- result-axis key set equals the selected content contract exactly;
- all axis/reason/action values match the state-token regex;
- reasons count 2–4 and values unique;
- `to_dict()` emits only approved fields and deep duplicates arrays/dictionaries.

Do not load the JSON contract at runtime. The Python test is the drift detector between JSON/registry and the GDScript constants; this keeps runtime deterministic and avoids I/O during deserialization.

- [ ] **Step 4: Run GUT and Python tests**

```bash
python -m unittest tests.test_vertical_slice_task1_canon_contract -v
Godot_v4.7.1 --headless -d -s --path "$PWD" addons/gut/gut_cmdln.gd \
  -gdir=res://tests/gut/unit/vertical_slice \
  -ginclude_subdirs \
  -gtest=test_vs_content_result_record.gd \
  -gexit
```

Expected: all focused tests pass.

- [ ] **Step 5: Commit**

```bash
git add scripts/vertical_slice/domain/vs_content_result_record.gd tests/gut/unit/vertical_slice/test_vs_content_result_record.gd
git commit -m "feat: validate vertical slice content result records"
```

---

### Task 3: Integrate typed records into SaveEnvelope without breaking legacy events

**Files:**
- Modify: `scripts/vertical_slice/domain/vs_save_envelope.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_save_service.gd`

**Interfaces:**
- Consumes: `VSContentResultRecord.from_dict()`
- Preserves: existing `active_run.resolved_events` Dictionary values
- Adds validation only when `record_type == CONTENT_RESULT_V1`

- [ ] **Step 1: Add failing round-trip and compatibility tests**

Add helpers to `test_vs_save_service.gd` for a valid Nadia content result.

Add tests:

```gdscript
func test_typed_content_result_survives_save_load() -> void:
    var envelope = _make_envelope()
    envelope.active_run["resolved_events"]["nadia-result-001"] = _make_nadia_result()
    var service = SaveServiceScript.new(TEST_SAVE_PATH)
    assert_eq(service.save_envelope(SaveEnvelopeScript.from_dict(envelope.to_dict())), OK)
    var restored = service.load_envelope()
    assert_true(restored.validation_errors.is_empty())
    assert_eq(
        restored.active_run["resolved_events"]["nadia-result-001"],
        _make_nadia_result()
    )

func test_typed_content_result_key_mismatch_fails() -> void:
    var envelope = _make_envelope()
    envelope.active_run["resolved_events"]["wrong-key"] = _make_nadia_result()
    var restored = SaveEnvelopeScript.from_dict(envelope.to_dict())
    assert_true(
        restored.validation_errors.has(
            "CONTENT_RESULT:wrong-key:CONTENT_RESULT_EVENT_KEY_MISMATCH"
        )
    )

func test_legacy_generic_event_remains_pass_through() -> void:
    var envelope = _make_envelope()
    var restored = SaveEnvelopeScript.from_dict(envelope.to_dict())
    assert_true(restored.validation_errors.is_empty())
    assert_eq(
        restored.active_run["resolved_events"]["forge_birth"],
        envelope.active_run["resolved_events"]["forge_birth"]
    )
```

- [ ] **Step 2: Observe RED**

Expected: typed invalid records are not yet validated and key mismatch test fails.

- [ ] **Step 3: Implement selective integration**

At the top of `vs_save_envelope.gd`:

```gdscript
const ContentResultRecordScript = preload(
    "res://scripts/vertical_slice/domain/vs_content_result_record.gd"
)
```

After normalizing `active_run`, call a private method:

```gdscript
static func _validate_typed_resolved_events(envelope: VSSaveEnvelope) -> void:
    var resolved: Variant = envelope.active_run.get("resolved_events", {})
    if not resolved is Dictionary:
        return
    for event_key in resolved.keys():
        var raw_event: Variant = resolved[event_key]
        if not raw_event is Dictionary:
            continue
        if str(raw_event.get("record_type", "")) != "CONTENT_RESULT_V1":
            continue
        var record = ContentResultRecordScript.from_dict(raw_event)
        if record.event_id != str(event_key):
            record.validation_errors.append("CONTENT_RESULT_EVENT_KEY_MISMATCH")
        for error_code in record.validation_errors:
            envelope.validation_errors.append(
                "CONTENT_RESULT:%s:%s" % [str(event_key), error_code]
            )
        if record.validation_errors.is_empty():
            envelope.active_run["resolved_events"][event_key] = record.to_dict()
```

Do not mutate or validate legacy generic event shapes.

- [ ] **Step 4: Run full focused regressions**

```bash
python -m unittest tests.test_vertical_slice_task1_canon_contract -v
# GUT full unit/integration discovery
Godot_v4.7.1 --headless -d -s --path "$PWD" addons/gut/gut_cmdln.gd \
  -gdir=res://tests/gut/unit \
  -gdir=res://tests/gut/integration \
  -ginclude_subdirs \
  -gexit
```

Expected: new and existing save tests pass; no legacy fixture changes.

- [ ] **Step 5: Commit**

```bash
git add scripts/vertical_slice/domain/vs_save_envelope.gd tests/gut/unit/vertical_slice/test_vs_save_service.gd
git commit -m "feat: persist validated content result events"
```

---

### Task 4: Satisfy the protected-change gate and close exact-head evidence

**Files:**
- Create: `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json`
- Verify: `skills/PROJECT_BASE_ADAPTER.json`
- PR label: `approved-protected-change`

**Interfaces:**
- Consumes adapter `protected_baseline.commit`.
- Produces one-shot approval for the exact three protected paths only.

- [ ] **Step 1: Create the approval manifest**

Read `skills/PROJECT_BASE_ADAPTER.json#/protected_baseline/commit` and use it exactly as `protected_base_commit`.

```json
{
  "schema_version": 1,
  "artifact_role": "PROJECT_PROTECTED_CHANGE_APPROVAL",
  "status": "APPROVED",
  "protected_base_commit": "<exact current adapter protected baseline>",
  "decision_ids": [
    "BS-OPS-20260811-03",
    "BS-VS-P2-20260813-01"
  ],
  "approved_paths": [
    "data/vertical_slice/content_result_contract.json",
    "scripts/vertical_slice/domain/vs_content_result_record.gd",
    "scripts/vertical_slice/domain/vs_save_envelope.gd"
  ],
  "approval_source": "USER_REQUEST_AND_GITHUB_PR_LABEL_APPROVED_PROTECTED_CHANGE",
  "approval_time": "2026-08-13T00:00:00+09:00",
  "scope_summary": "Exact P2 content-result foundation only; no scene/resource/project settings, formulas, rewards, UI, Task3, or new product scope."
}
```

Use the actual KST timestamp rather than the sample midnight.

- [ ] **Step 2: Open a Draft PR and add the label**

PR body must contain:

- exact source main;
- allowed/forbidden scope;
- RED evidence;
- protected paths;
- non-claims;
- rollback;
- closure requirement to retire the manifest and advance the protected baseline after merge.

Add label `approved-protected-change`.

- [ ] **Step 3: Run exact-head validation**

Required checks:

```text
Validate Project Base Adapter
Validate Base v9 adoption
Validate Thin Adapter Migration
Validate Blacksmith BCA Adoption
PR validation
Validate GUT 9.7.1 Formal Adoption
```

All must reference the exact final head. Review threads must be zero. Current main must still equal the PR base or the branch must be rebased/recreated before merge.

- [ ] **Step 4: Adversarial review**

Attack the diff for:

- hidden score/probability/reward fields;
- result-axis drift from registry;
- D03 fixed quantity 10 accidentally canonized;
- D09 old/new UID equality or history transfer;
- legacy resolved-event rejection;
- save schema bump;
- scene/resource/project setting change;
- approval paths broader than actual protected diff.

Fix every P0/P1 finding and rerun exact-head checks.

- [ ] **Step 5: Squash merge**

Merge only when all checks pass and the PR is mergeable/up-to-date.

- [ ] **Step 6: Post-merge closure**

Create a separate closure PR from merged main that:

- updates `skills/PROJECT_BASE_ADAPTER.json#/protected_baseline/commit` to the implementation merge main;
- updates its policy hash if required by the adapter contract;
- removes `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json`;
- updates hard-coded baseline regression expectations;
- records exact implementation merge and full-validation evidence;
- runs full validation and merges;
- verifies main readback.

- [ ] **Step 7: Commit/merge reporting**

Report separately:

```text
actual product changes
contract/static/GUT/Godot evidence
post-merge closure evidence
NOT_RUN human/Android/accessibility/performance
remaining risk
rollback
```
