# Blacksmith Project Base Adapter Migration — 2026-08-06

```yaml
decision_id: DEC-BASE-20260805-001
source_main: b1dd945875568098b107815a03e88b0272d384e9
trusted_base_validator: bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1
strategy: OPTION_A_EXACT_TRUSTED_BASE_EQUALITY
adapter_authority: BASE_V1_THIN_ADAPTER
project_state_authority: docs/PROJECT_OPERATING_STATE.json
machine_health_authority: docs/PROJECT_OPERATING_HEALTH.json
PRODUCT_FILES_UNCHANGED: true
GOOGLE_SHEETS_UNCHANGED: true
runtime_validation: NOT_RUN
android_device_validation: NOT_RUN
human_validation: HUMAN_NOT_RUN
```

## Field map

| Original field | Project-owned destination | Treatment |
|---|---|---|
| `/current_operating_decisions` | `/adapter_migration/preserved_from_adapter/current_operating_decisions` | verbatim |
| `/project_operating_state` | `/adapter_migration/preserved_from_adapter/project_operating_state` | verbatim and current pointers retained |
| `/current_r1_canon` | `/adapter_migration/preserved_from_adapter/current_r1_canon` | verbatim |
| `/validation_status` | `/adapter_migration/preserved_from_adapter/validation_status` | verbatim evidence; no promotion |
| `previous PROJECT_OPERATING_HEALTH` | `/adapter_migration/original_project_operating_health` | verbatim before Base Health normalization |
| `/base_release/adoption_status` | `/adapter_migration/preserved_nested_metadata/base_release_adoption_status` | removed from Base contract |
| `/compatibility/*_status` | `/adapter_migration/preserved_nested_metadata/compatibility_generation_status` | official generator becomes authority |
| `/routing/selection_policy` | `/adapter_migration/preserved_nested_metadata/routing_policy/selection_policy` | removed from strict routing |
| `/routing/load_all_skills` | `/adapter_migration/preserved_nested_metadata/routing_policy/load_all_skills` | removed from strict routing |
| `blacksmith-engineering route status` | `/adapter_migration/preserved_nested_metadata/routing_policy/blacksmith_engineering_original_status` | adapter ACTIVE; implementation gate remains project-owned |
| `/protected_baseline` | `/adapter_migration/preserved_nested_metadata/protected_baseline` | old evidence retained; canonical exact-base contract replaces it |
| `/skill_registry/*/hash_status` | `/adapter_migration/preserved_nested_metadata/skill_registry` | old evidence retained; raw-byte SHA used in adapter |
| `manual validators` | `/adapter_migration/preserved_nested_metadata/manual_validator_evidence` | not executable adapter commands |
| `/gdd_sheet/sync_status` | `/adapter_migration/preserved_nested_metadata/gdd_sheet/sync_status` | SYNCED_TO_MAIN retained; adapter token CURRENT |

## Evidence separation

- operating maturity: `docs/PROJECT_OPERATING_STATE.json`;
- Sheet-current contract: this migration record;
- static adapter gate: `skills/PROJECT_BASE_ADAPTER.json`.

Each health evidence ID and source is unique. One verified operating record caps the conservative machine maturity at `OM-L1`; no product evidence is promoted.

## Scope boundary

The migration changes the Base connection contract, standard machine health, project-owned state, and official generated views only. It does not edit `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`, Blacksmith gameplay canon, or Google Sheet cells. Historical PASS and NOT_RUN values are preserved verbatim and are not promoted.
