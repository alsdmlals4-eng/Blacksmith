# Five Equipment Visual Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make five equipment types selectable and persist their identities, preserve weapon-only Precision Tags, remove the unconsumed Precision raster, and promote five inspected item illustrations only after user lock.

**Architecture:** `vertical_slice_equipment_catalog_20260830.json` is the one owner for IDs, stored group/profile pairs, labels, Precision eligibility, and item image paths. The existing forge completion, item birth, and Workshop presentation read this catalog, so older sword saves remain valid without a schema expansion.

**Tech Stack:** Godot 4.7.1, GDScript, JSON, GUT, Python contracts, OpenAI ImageGen.

**Spec:** `docs/decisions/BS-EQUIPMENT-20260830-39_FIVE_EQUIPMENT_SELECTION_AND_VISUAL_CONSUMER.md`

## Global Constraints

- Android portrait baseline: 720x1280; selection actions are 48dp or larger.
- The `ILLUSTRATED_WORKSHOP_BOOK` images are object art, not rasterized screens or controls.
- `SWORD`, `SHIELD`, `BOW` are Precision eligible; `ARMOR`, `HELMET` block at a Precision target before cost, roll, mutation, ledger, or save.
- Existing sword saves round-trip unchanged. No serialized key is added.
- User review is mandatory before image candidates become runtime assets.

### Task 1: Catalog and save identity

**Files:** `data/vertical_slice/vertical_slice_equipment_catalog_20260830.json`, `scripts/vertical_slice/domain/vs_equipment_catalog.gd`, `scripts/vertical_slice/domain/vs_item.gd`, `data/vertical_slice/vertical_slice_schema.json`, `data/vertical_slice/vertical_slice_preset.json`, `tests/test_five_equipment_catalog_contract.py`, `tests/gut/unit/vertical_slice/test_vs_equipment_catalog.gd`.

- [x] Write contract tests requiring exactly the five approved IDs and weapon-only eligibility.
- [x] Run the Python contract before implementation; observed `FileNotFoundError` for the missing catalog.
- [x] Add the JSON catalog and GDScript query boundary, update item group/profile validation, and update structured group lists.
- [x] Run `python tests/test_five_equipment_catalog_contract.py -v` and the focused GUT catalog test; both pass.

### Task 2: First forge transfer

**Files:** `scripts/forging/forging_session.gd`, `scripts/forging/canonical_first_item_input_adapter.gd`, `scripts/vertical_slice/services/vs_item_birth_service.gd`, `tests/gut/unit/test_forging_session.gd`, `tests/gut/unit/vertical_slice/test_vs_item_birth_service.gd`, `tests/gut/unit/vertical_slice/test_vs_first_forge_completion_service.gd`.

- [ ] Write tests that complete sword, shield, bow, armor, and helmet and assert the item group/profile plus birth-ledger `equipment_id`.
- [ ] Observe RED because current completion and birth paths reject anything but `iron_sword`.
- [ ] Make `ForgingSession._complete` emit a catalog identity, make the modern completion adapter validate it, and make the birth service read catalog values. Preserve the legacy adapter's historical sword-only route.
- [ ] Run the three focused tests and verify all five selected identities save; unknown IDs fail closed.

### Task 3: Native selection and Precision UX

**Files:** `scripts/ui/forging_screen.gd`, `scripts/vertical_slice/resolvers/vs_precision_resolver.gd`, `scripts/vertical_slice/ui/vs_workshop_screen.gd`, `scenes/vertical_slice/screens/vs_workshop_screen.tscn`, `tests/gut/unit/test_forging_screen.gd`, `tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd`, `tests/gut/unit/vertical_slice/test_vs_precision_tag_catalog.gd`.

- [ ] Write RED tests for five native choice buttons, choice locking after progress begins, dynamic Workshop title/hero, armor/helmet `PRECISION_TAG_WEAPON_ONLY`, and absence of `PrecisionIllustratedBackground`.
- [ ] Implement the 48dp native choice buttons and dynamic label path; remove the Precision raster preload/state/layer while retaining tag controls for eligible equipment.
- [ ] Run focused UX/Precision GUT tests. Verify armor and helmet neither spend nor roll at `+9 -> +10`.

### Task 4: Candidate art and user lock

**Files:** five `assets/ui/equipment/*_card_v1.png` files after lock; `docs/planning/BLACKSMITH_RECURRING_PRECISION_VISUAL_REQUIREMENTS_20260830.json`, `docs/planning/BLACKSMITH_SCREEN_SURFACE_VISUAL_COVERAGE_20260827.json`, `assets/ASSET_MANIFEST.json`, `docs/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`, `tests/check_recurring_precision_visual_requirements_contract.py`.

- [ ] Write a visual contract that expects five consumer-first requirements and no live Precision-raster reference.
- [ ] Generate and inspect one 1:1 candidate each for sword, shield, bow, armor, and helmet; record `GENERATED_CANDIDATE` receipts only.
- [ ] Present all five candidates and their first-forge/Workshop consumers to obtain the required user lock.
- [ ] After explicit approval, register hashes and provenance, bind only the catalog paths, remove the retired Precision binary, and run the visual contract.

### Task 5: Full readback

**Files:** `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md`, generated owner PDF receipt only after its source update.

- [ ] Update the human GDD after catalog and asset lock agree; record the evidence ceiling.
- [ ] Run targeted Python contracts, full GUT, Godot import/editor parse, `git diff --check`, and a full active-reference search.
- [ ] Classify client render, Android, accessibility, visual human review, performance, and release rights as `NOT_RUN` unless directly observed.
