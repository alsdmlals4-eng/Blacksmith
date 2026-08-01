# Blacksmith v9 Data·Legacy Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Apply TDD task-by-task.
>
> **Execution Gate:** 사용자 `기획 완료`와 `검수 완료` 전 실행 금지.

**Goal:** 구형 제작 등급·수식어 3슬롯·+50 이상 장비를 최신 5등급·계보+보조2·일반/고위 정밀 모델로 UID·수치·수식어·연대기 손실 없이 결정론적으로 이전한다.

**Authority:** `BS-MIGRATION-20260801-01`.

**Tech Stack:** Godot 4.7.1, GDScript, JSON, Python 3.12 validators, headless SceneTree tests.

## Global zero-tolerance gates

```text
EQUIPMENT_UID_CHANGED = 0
GRADE_RANK_CHANGED = 0
STORED_NUMERIC_VALUE_CHANGED = 0
AFFIX_LOSS = 0
RNG_CALLS_DURING_MIGRATION = 0
FREE_HIGH_PRECISION_REWARD = 0
DUPLICATE_MIGRATION = 0
SOURCE_OVERWRITE_ON_FAILURE = 0
PARTIAL_CAMPAIGN_COMMIT = 0
```

## File Map

### Create

- `scripts/migration/v9/legacy_grade_mapper.gd`
- `scripts/migration/v9/legacy_affix_mapper.gd`
- `scripts/migration/v9/legacy_equipment_mapper.gd`
- `scripts/migration/v9/v9_campaign_migration.gd`
- `data/migrations/v9/legacy_grade_map.json`
- `data/migrations/v9/legacy_milestone_map.json`
- `tools/validate_v9_migration_contract.py`
- `tests/test_v9_migration_contract.py`
- `tests/fixtures/migration/v9/*.json`
- `tests/unit/test_legacy_grade_mapper.gd`
- `tests/unit/test_legacy_affix_mapper.gd`
- `tests/integration/test_v9_campaign_migration.gd`

### Modify

- `data/crafting/craftsmanship_grades.json`
- `data/crafting/enhancement_milestones.json`
- `scripts/forging/craftsmanship_grade_resolver.gd`
- `scripts/enhancement/enhancement_session.gd`
- `scripts/world/equipment_world_registry.gd`
- future `scripts/application/save/save_migrator.gd`
- relevant validators, fixtures, tests, CI docs

---

### Task 1: Freeze target schemas and mappings

- [ ] Write failing Python contract tests for exact five target IDs and one-to-one legacy map.
- [ ] Create `legacy_grade_map.json` with:

```json
{
  "APPRENTICE": "NORMAL",
  "STANDARD": "SUPERIOR",
  "REFINED": "EXQUISITE",
  "MASTERWORK": "MASTERPIECE",
  "PERFECT": "LEGENDARY"
}
```

- [ ] Update target `craftsmanship_grades.json` schema to version 2 while preserving old score/multiplier/distribution values under remapped keys.
- [ ] Verify no `APPRENTICE|STANDARD|REFINED|MASTERWORK|PERFECT` remains in active runtime target data except migration fixtures/maps.
- [ ] Run:

```bash
python tools/validate_v9_migration_contract.py
python -m unittest tests/test_v9_migration_contract.py
```

- [ ] Commit: `feat: define v9 grade schema and legacy mapping`

### Task 2: Grade mapper and finish/grade separation

- [ ] Write `test_legacy_grade_mapper.gd` for all five grades, unknown ID, idempotent target ID and missing grade.
- [ ] Implement `LegacyGradeMapper.map_id()` without RNG.
- [ ] Add separate fields:

```text
crafting_finish_result_id
craftsmanship_grade_id
```

- [ ] Existing stored grade uses mapping directly; finish-only record uses deterministic resolver once only when all inputs exist.
- [ ] Insufficient inputs return `MIGRATION_REVIEW_REQUIRED`.
- [ ] Verify rank and numeric values unchanged.
- [ ] Commit: `feat: separate finish result and craftsmanship grade`

### Task 3: Affix role mapper

- [ ] Write fixtures for 0/1/2/3 legacy slots, duplicate affixes and missing definitions.
- [ ] Implement:

```text
slot1 → lineage_affix
slot2 → secondary_affixes[0]
slot3 → secondary_affixes[1]
```

- [ ] Preserve ID, tier, effects, material score and provenance.
- [ ] Do not fill empty slots, merge duplicates or grant special affix.
- [ ] Missing definition preserves unresolved reference and blocks campaign promotion.
- [ ] Commit: `feat: migrate legacy affix slots into identity roles`

### Task 4: Milestone and +50 provenance

- [ ] Write level fixtures for +0/+10/+20/+30/+40/+49/+50/+60/+100.
- [ ] Update target milestone schema version 3 to represent lineage/secondary role events and +49 route choice.
- [ ] For legacy level ≥50 set:

```text
enhancement_route_at_50 = LEGACY_GENERAL_PRECISION
special_material_uses_at_50 = []
special_affix_id = ""
high_precision_evolution_id = ""
```

- [ ] Verify old slot3 remains secondary2 and no high-precision benefit is granted.
- [ ] Level 49 or lower enters current route selection on its next +50 attempt.
- [ ] Commit: `feat: preserve legacy milestones and plus50 provenance`

### Task 5: Equipment and world-record migration

- [ ] Write fixtures for workshop, sold, active owner, result pending, result opened, lost/broken legacy states and duplicate UID.
- [ ] Implement equipment record schema 1 and world registry record schema 2 mapping.
- [ ] Preserve UID, owner, delivery transaction, event IDs, history and result state.
- [ ] Split ambiguous `BROKEN_OR_LOST` only when history proves one state; otherwise use `LEGACY_FATE_UNRESOLVED` and require review.
- [ ] Add one `LEGACY_MILESTONE_MIGRATED` chronology entry; do not fabricate historical choices.
- [ ] Commit: `feat: migrate equipment lifecycle records without identity loss`

### Task 6: Campaign-wide atomic migrator

- [ ] Write failing integration tests for valid migration, duplicate run, partial failure, unknown grade, missing affix, duplicate UID and source preservation.
- [ ] Implement migration ID:

```text
BS-MIGRATION-20260801-01:<campaign_id>:<source_revision>
```

- [ ] Deep-copy and transform entire campaign in memory.
- [ ] Validate all references before any promotion.
- [ ] Delegate tmp write/read-back/atomic promotion to `BS-SAVE-20260801-01` SaveMigrator/SaveCoordinator.
- [ ] Any item failure aborts whole campaign; source bytes remain unchanged.
- [ ] Run migration twice and verify second run is a no-op.
- [ ] Commit: `feat: migrate legacy campaign atomically and idempotently`

### Task 7: Update consumers, tests and CI

- [ ] Update resolver, enhancement, customer fit, equipment display and world registry to target IDs/roles.
- [ ] Convert old contract tests to explicit legacy migration fixture tests instead of deleting them.
- [ ] Add current runtime tests for all five target grades, lineage+secondary2, general/high precision +50 and legacy +50.
- [ ] Add CI commands:

```bash
python tools/validate_v9_migration_contract.py
python -m unittest tests/test_v9_migration_contract.py
godot --headless --path . --script res://tests/unit/test_legacy_grade_mapper.gd
godot --headless --path . --script res://tests/unit/test_legacy_affix_mapper.gd
godot --headless --path . --script res://tests/integration/test_v9_campaign_migration.gd
```

- [ ] Run existing full Python and Godot suites.
- [ ] Keep Android and actual historical-save validation `NOT_RUN` until executed.
- [ ] Commit: `ci: enforce v9 migration compatibility and no-loss gates`

## Self-review

- Exact target IDs and mappings: present.
- Unknown/missing/duplicate failure handling: present.
- No RNG and no retroactive high-precision reward: explicit.
- Atomic whole-campaign promotion and source preservation: explicit.
- Legacy tests retained as migration evidence: explicit.
- Runtime execution authorization: blocked.

```text
PLAN_STATUS: COMPLETE
IMPLEMENTATION_EXECUTION: BLOCKED
```
