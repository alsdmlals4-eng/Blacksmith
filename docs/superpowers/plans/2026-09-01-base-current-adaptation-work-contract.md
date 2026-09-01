# Base Current Adaptation Work Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a thin, repository-owned Blacksmith operating contract that adopts current Base practices without changing the adopted Base release, gameplay canon, or protected product paths.

**Architecture:** One current Blacksmith contract owns Base-current adaptation and work-mode routing. One JSON receipt records this L3 operation in the Base validator shape. One Python contract check proves the new owner, receipt, boundaries, and exact release lock exist, while existing current-authority and archive checks remain unchanged.

**Tech Stack:** Markdown, JSON, Python standard library, Base `validate_work_contract_receipt.py`, existing Blacksmith command-style contract checks.

**Spec:** `docs/superpowers/specs/2026-09-01-base-current-adaptation-work-contract-design.md`

## Global Constraints

- Keep Blacksmith adopted Base release exactly `v9.4.4 / 210ec78292fa12ed7563ba743b322dd36103ae4a`.
- Treat Base `main@19355b7ef065a21d0f2b685c7d9be64a4a3970f8` as an observed reference, never as an automatic pin update.
- Do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.
- Preserve `GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE`; Notion and Google Sheet remain historical/migration-only.
- Preserve existing `docs/BASE_ADOPTION_PROFILE.json` consumers and do not delete any legacy material.
- Use a branch and PR; never push directly to `main` or force-push.

---

### Task 1: Add the RED operating-contract check

**Files:**
- Create: `tests/check_base_current_adaptation_work_contract.py`
- Test: `tests/check_base_current_adaptation_work_contract.py`

**Interfaces:**
- Consumes: repository root, `skills/PROJECT_BASE_ADAPTER.json`, Base receipt validator, and future contract/receipt/current-owner paths.
- Produces: exit `0` only when all required current Base adaptation constraints are true; otherwise exit `1` with individual failures.

- [x] **Step 1: Write the failing test**

```python
EXPECTED_RELEASE = "9.4.4"
EXPECTED_RELEASE_COMMIT = "210ec78292fa12ed7563ba743b322dd36103ae4a"
REQUIRED_MODES = ("PLAN", "NONCODING_BUILD", "GODOT_PRODUCT_BUILD", "REVIEW")

for path in (CONTRACT, RECEIPT):
    if not path.exists():
        failures.append(f"missing required current Base adaptation path: {path}")
```

- [x] **Step 2: Run the test to verify RED**

Run:

```powershell
& $python tests/check_base_current_adaptation_work_contract.py
```

Expected: exit `1` and messages that the contract and receipt do not exist.

- [x] **Step 3: Do not add production content yet**

Keep the check as the only new executable file until the expected missing-owner failure has been observed.

- [x] **Step 4: Record the observed failure**

Record the exit code and missing-owner messages in the implementation report and commit only after Tasks 2–4 are green.

### Task 2: Add the thin current operating contract and L3 receipt

**Files:**
- Create: `docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md`
- Create: `docs/operations/receipts/2026-09-01-base-current-adaptation-work-contract.json`

**Interfaces:**
- Consumes: approved design spec, current Base observation, adopted adapter lock, current Blacksmith authority sources, and Base receipt-validator fields.
- Produces: the only current owner for Base-current adaptation and a machine-readable L3 receipt.

- [x] **Step 1: Write the contract with the four exact modes**

```text
PLAN -> current authority, research, reuse and approval boundary
NONCODING_BUILD -> document, contract, validator and metadata changes only
GODOT_PRODUCT_BUILD -> approved current-canon scope and protected-path authority
REVIEW -> adversarial review, exact-head validation, PR and remote readback
```

- [x] **Step 2: Write the receipt with validator-required fields**

```json
{
  "work_level": "L3",
  "benchmark_preflight_receipt": {"state": "PASS", "entries": []},
  "context_configuration_hygiene": {"scope": "...", "inventory": []}
}
```

Populate each receipt list with the exact nonempty evidence fields required by the Base validator; do not leave the illustrative empty lists in the final file.

- [x] **Step 3: Run the Base receipt validator**

Run:

```powershell
& $python C:\Users\user\Documents\GitHub\Base\tools\validate_work_contract_receipt.py --receipt docs/operations/receipts/2026-09-01-base-current-adaptation-work-contract.json
```

Expected: `WORK CONTRACT RECEIPT: PASS`.

- [x] **Step 4: Run the new check to verify GREEN for contract/receipt presence**

Run:

```powershell
& $python tests/check_base_current_adaptation_work_contract.py
```

Expected: no missing-owner failures; any remaining assertions identify only unsynchronized current entrypoints.

### Task 3: Connect the contract to current Blacksmith entrypoints

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`
- Modify: `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`
- Modify: `docs/BASE_RULES_VERSION.md`
- Create: `.github/workflows/validate-current-base-adaptation-work-contract.yml`

**Interfaces:**
- Consumes: the Task 2 contract path.
- Produces: a cold-start route that distinguishes current Base observation, adopted release lock, current product owners, and compatibility-only material.

- [x] **Step 1: Add the new contract to the active operating authority route**

```text
AGENTS.md -> current operational adaptation contract -> session handoff -> product owners
```

Do not move or weaken the latest-user-instruction, product owner, Decision35/36, or protected-path precedence.

- [x] **Step 2: Add a compact handoff and authority-index pointer**

```text
BASE_CURRENT_ADAPTATION_OWNER = docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md
BASE_RELEASE_LOCK = v9.4.4 / adapter-owned
BASE_CURRENT_MAIN = observation only / no automatic adoption
```

- [x] **Step 3: Mark the old Base-version document as historical/compatibility evidence**

Add a top-level current notice to `docs/BASE_RULES_VERSION.md` that points to the new contract and the generated adapter. Preserve all historical content and its original identifiers.

- [x] **Step 4: Run the new check to verify GREEN**

Run:

```powershell
& $python tests/check_base_current_adaptation_work_contract.py
```

Expected: `Base current adaptation work contract PASSED`.

- [x] **Step 5: Add the focused CI workflow**

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
  with:
    repository: alsdmlals4-eng/Base
    ref: 19355b7ef065a21d0f2b685c7d9be64a4a3970f8
    path: .base-current
env:
  BLACKSMITH_BASE_ROOT: ${{ github.workspace }}/.base-current
```

The workflow runs only when this contract's owner, receipt, linked entrypoints, test, adapter, or its own workflow changes. It checks out the observed Base SHA as a validator source and does not modify `skills/PROJECT_BASE_ADAPTER.json`.

### Task 4: Run exact-head contract validation and publish safely

**Files:**
- Modify: none beyond Tasks 1–3 if every validation is green.

**Interfaces:**
- Consumes: all Task 1–3 files.
- Produces: a clean branch, exact evidence, a PR-ready commit, and remote branch readback.

- [x] **Step 1: Run focused checks**

```powershell
& $python tests/check_base_current_adaptation_work_contract.py
& $python tests/check_current_authority_entrypoint_contract.py
& $python tools/check_archive_governance.py
& $python C:\Users\user\Documents\GitHub\Base\tools\check_project_operating_contract.py --project-root . --base-repository C:\Users\user\Documents\GitHub\Base --check
```

- [x] **Step 2: Run the project contract suite selected by the changed documentation paths**

```powershell
& $python -m unittest tests.test_base_v94_ai_operations_adoption tests.test_base_v944_identity_migration tests.test_current_active_context_priority_overlay -v
```

Expected: all selected tests pass with no product-path change.

- [x] **Step 3: Audit the diff and protected path boundary**

```powershell
git diff --check
git diff --name-only origin/main...HEAD
git status --short
```

Expected: only contract, receipt, current-owner documentation, plan/spec, and test paths; no protected product path.

- [x] **Step 4: Commit, push, and create the documentation-only PR**

```powershell
git add AGENTS.md docs tests
git commit -m "docs: adapt current Base work contract"
git push -u origin codex/base-current-work-contract-20260901
```

Create a PR against `main`, inspect the PR's exact head and required checks, then merge only after the current head passes. Read back `main` and the GitHub destination after merge.

## Self-Review

- Spec coverage: Tasks 1–3 cover the current Base observation, adopted release lock, four modes, receipt, legacy classification, GitHub-only boundary, entrypoint route, and historical version notice. Task 4 covers exact-head validation and remote readback.
- Placeholder scan: no `TODO`, `TBD`, or undefined implementation step remains. The illustrative empty JSON arrays in Task 2 are explicitly prohibited from the final artifact.
- Interface consistency: Task 1 defines the contract/receipt paths that Tasks 2–3 create and Task 4 validates. All validation commands use the same receipt and adapter release identity.
