# Blacksmith Thin Base Adapter Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace Blacksmith's project-state-heavy `PROJECT_BASE_ADAPTER.json` with a strict Base v1 thin adapter while preserving every removed project-owned field in explicit Blacksmith authority and proving no product, canon, or Google Sheet mutation.

**Architecture:** `skills/PROJECT_BASE_ADAPTER.json` will own only Base release identity, project binding, typed routes, registries, overrides, Sheet connection metadata, exact protected baseline, protected paths, executable validators, and compatibility views. Existing Blacksmith operating state will remain project-owned in `docs/PROJECT_OPERATING_HEALTH.json`, with a lossless migration snapshot and field map in `docs/operations/PROJECT_BASE_ADAPTER_MIGRATION_2026-08-06.md`. Base's immutable validator and official artifact generator at `bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1` are the sole contract and generation authority.

**Tech Stack:** JSON, Markdown, Python 3.12 `unittest`, GitHub Actions, Base v1 project adapter validator and generator.

## Global Constraints

- Governing decision: `DEC-BASE-20260805-001`.
- Protected baseline policy: exact equality with PR base `b1dd945875568098b107815a03e88b0272d384e9`.
- Trusted Base validator: `bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1`.
- `additionalProperties: false` at the adapter root remains enforced.
- All removed adapter-root information must be preserved before removal.
- Generated compatibility views must be produced only by Base `build_project_operating_artifacts.py --write`.
- No `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`, gameplay canon, or Google Sheet cell changes.
- Runtime, Android device, accessibility, performance, and human evidence remain `NOT_RUN` unless separately executed.

---

### Task 1: Establish RED migration contract

**Files:**
- Create: `tests/test_project_base_adapter_thin_migration.py`
- Create: `.github/workflows/validate-project-base-adapter.yml`

**Interfaces:**
- Consumes: current `skills/PROJECT_BASE_ADAPTER.json` and Base validator commit `bfdc9e...`.
- Produces: a failing contract that identifies every non-v1 ownership violation before migration.

- [ ] **Step 1: Add a failing test for adapter ownership**

The test must assert that the adapter root is exactly:

```python
EXPECTED_ROOT_KEYS = {
    "artifact_role", "base_release", "compatibility", "gdd_sheet",
    "project", "protected_baseline", "protected_paths", "routing",
    "schema_version", "shared_overrides", "skill_registry", "validators",
}
```

It must reject `current_operating_decisions`, `project_operating_state`, and `current_r1_canon` at the adapter root; reject noncanonical route statuses and metadata keys; reject null hashes; require executable validator strings; require `gdd_sheet.sync_status == "CURRENT"`; and require a migration snapshot in `docs/PROJECT_OPERATING_HEALTH.json`.

- [ ] **Step 2: Add immutable validator workflow**

The workflow checks out Base at exactly:

```text
bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1
```

It runs the focused migration test, then Base `check_project_operating_contract.py --check` against `${{ github.event.pull_request.base.sha }}`.

- [ ] **Step 3: Open a Draft PR and verify RED**

Expected failures include forbidden adapter-root fields, invalid route status, invalid baseline enums/null hash, invalid Registry evidence, stale generated views, and absent migration snapshot.

- [ ] **Step 4: Commit RED evidence**

```bash
git add tests/test_project_base_adapter_thin_migration.py .github/workflows/validate-project-base-adapter.yml
git commit -m "test: expose Blacksmith thin adapter drift"
```

### Task 2: Preserve project state before adapter removal

**Files:**
- Modify: `docs/PROJECT_OPERATING_HEALTH.json`
- Create: `docs/operations/PROJECT_BASE_ADAPTER_MIGRATION_2026-08-06.md`

**Interfaces:**
- Consumes: exact pre-migration adapter bytes at `main@b1dd945...`.
- Produces: `adapter_migration.preserved_from_adapter`, a lossless JSON snapshot of every removed or normalized field.

- [ ] **Step 1: Preserve root-owned state**

Store exact copies of:

```text
/current_operating_decisions
/project_operating_state
/current_r1_canon
```

under `docs/PROJECT_OPERATING_HEALTH.json#/adapter_migration/preserved_from_adapter`.

- [ ] **Step 2: Preserve normalized metadata**

Record the former `base_release.adoption_status`, compatibility generation statuses, routing selection policy, engineering route gate state, protected-baseline evidence statuses, Registry hash statuses, and detailed Sheet status in the same migration object.

- [ ] **Step 3: Advance health pointers without inventing evidence**

Set the health document's current stage and decision pointers from the preserved R2 adapter values. Keep product implementation blocked and all absent Runtime/device/human evidence as `NOT_RUN`.

- [ ] **Step 4: Write the field migration map**

The Markdown map must list every removed field, destination JSON pointer, normalization rule, and evidence ceiling. It must explicitly state that Sheet content and product files are unchanged.

- [ ] **Step 5: Run the focused test**

Expected: migration-preservation assertions pass; adapter-shape assertions still fail until Task 3.

- [ ] **Step 6: Commit state preservation**

```bash
git add docs/PROJECT_OPERATING_HEALTH.json docs/operations/PROJECT_BASE_ADAPTER_MIGRATION_2026-08-06.md
git commit -m "docs: preserve Blacksmith adapter-owned state"
```

### Task 3: Rebuild the strict Base v1 adapter

**Files:**
- Modify: `skills/PROJECT_BASE_ADAPTER.json`

**Interfaces:**
- Consumes: preserved project state from Task 2 and Base v1 Schema.
- Produces: one strict thin adapter accepted by the Base validator.

- [ ] **Step 1: Remove project-state root fields**

The new root contains only the twelve Schema-owned fields listed in Task 1.

- [ ] **Step 2: Normalize Base release and Sheet status**

Remove `base_release.adoption_status`. Preserve detailed Sheet metadata but map the contract status from `SYNCED_TO_MAIN` to `CURRENT`, recording the previous token in project health.

- [ ] **Step 3: Normalize routes**

Keep each Base and project route as `{route_id, skill_id, status}`. Convert `blacksmith-engineering` to route status `ACTIVE`; preserve its implementation block only in project health. Remove `selection_policy` and `load_all_skills` from the routing object after preserving them.

- [ ] **Step 4: Normalize protected baseline**

Use:

```json
{
  "authority_kind": "REMOTE_TRACKING_REF",
  "authority_ref": "refs/remotes/origin/main",
  "commit": "b1dd945875568098b107815a03e88b0272d384e9",
  "policy_source_type": "CANONICAL_ADAPTER_SOURCE",
  "policy_source_path": "skills/PROJECT_BASE_ADAPTER.json",
  "protected_paths_pointer": "/protected_paths"
}
```

Compute `policy_sha256` from UTF-8 bytes of the protected-path array serialized with `json.dumps(..., ensure_ascii=False, indent=2) + "\n"`.

- [ ] **Step 5: Refresh Registry evidence**

Keep Base Registry SHA `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`. Compute the project Registry SHA from raw bytes of `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`. Remove non-Schema `hash_status` keys after preserving them.

- [ ] **Step 6: Keep executable validators only**

Retain real Python/Godot command strings and remove `manual:` pseudo-commands. Manual evidence boundaries remain documented in health and the migration map.

- [ ] **Step 7: Run focused test**

Expected: adapter ownership and preservation tests pass; Base generated-view check may still fail until Task 4.

- [ ] **Step 8: Commit adapter rebuild**

```bash
git add skills/PROJECT_BASE_ADAPTER.json
git commit -m "fix: rebuild Blacksmith thin Base adapter"
```

### Task 4: Regenerate all Base-owned views

**Files:**
- Modify only files reported by Base `build_project_operating_artifacts.py --write`.

**Interfaces:**
- Consumes: strict adapter from Task 3.
- Produces: byte-consistent Snapshot, Dashboard, router, and compatibility views.

- [ ] **Step 1: Run official generator**

```bash
python .base-contract/tools/build_project_operating_artifacts.py \
  --project-root . \
  --base-repository .base-contract \
  --protected-base b1dd945875568098b107815a03e88b0272d384e9 \
  --write
```

- [ ] **Step 2: Inspect changed paths**

Reject any generated change outside declared generated outputs. Do not hand-edit generated files.

- [ ] **Step 3: Run Base validator**

```bash
python .base-contract/tools/check_project_operating_contract.py \
  --project-root . \
  --base-repository .base-contract \
  --protected-base b1dd945875568098b107815a03e88b0272d384e9 \
  --check
```

Expected: PASS.

- [ ] **Step 4: Commit generated outputs**

```bash
git add skills/ docs/PROJECT_OPERATING_DASHBOARD.html .agents/
git commit -m "chore: regenerate Blacksmith adapter views"
```

### Task 5: Exact-head adversarial closure

**Files:**
- Modify: PR description only unless a finding requires code changes.

**Interfaces:**
- Consumes: complete branch diff and exact-head workflows.
- Produces: reviewable Draft PR with truthful evidence limits.

- [ ] **Step 1: Run all project workflows**

Require the new adapter validator plus existing Blacksmith contract, planning, first-prompt, external-AI, platform-rights, publication, and project validation checks.

- [ ] **Step 2: Audit scope**

Verify protected product paths, Blacksmith canon documents, and Google Sheet bytes/cells are unchanged.

- [ ] **Step 3: Audit information preservation**

Compare the pre-migration adapter field inventory to project health and the migration map. Every removed value must have one destination.

- [ ] **Step 4: Review threads and drift**

Require `behind_by: 0`, mergeable state, and zero unresolved review threads.

- [ ] **Step 5: Record evidence ceiling**

Use:

```yaml
adapter_contract: PASS
project_state_preservation: PASS
product_files: UNCHANGED
google_sheets: UNCHANGED
runtime_validation: NOT_RUN
android_device_validation: NOT_RUN
human_validation: HUMAN_NOT_RUN
merge_authorization: NOT_GRANTED
```

- [ ] **Step 6: Leave Draft for explicit merge approval**
