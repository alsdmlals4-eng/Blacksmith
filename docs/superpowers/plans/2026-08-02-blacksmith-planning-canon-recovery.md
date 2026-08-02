# Blacksmith Planning Canon Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore a single trustworthy Blacksmith planning operating state on current `main`, synchronize it to the linked Google Sheet with Decision ID `BS-OPS-20260802-01`, and open a safe path for adversarially reviewed total-planning authoring without changing product code.

**Architecture:** Work from the isolated branch `agent/blacksmith-planning-canon-recovery` based on `main@ac120fb146cea29bb5f8876682809f76779d86ad`. First freeze the evidence baseline, then repair authority entrypoints and registries, then synchronize the same operating decision to Google Sheet, then reconcile Issue/PR authority, and finally run adversarial, cold-start, and exact-HEAD verification. PR #81 remains a reference source rather than a merge unit; only evidence-backed planning decisions may be promoted in a later planning bundle.

**Tech Stack:** Markdown and JSON canonical documents, GitHub branches/commits/Draft PRs, Python operating-system validators already present in the repository, Google Sheets connector updates with bounded range readback, Godot 4.7 project facts used read-only.

## Global Constraints

- Decision ID for this recovery: `BS-OPS-20260802-01`.
- Work Mode: `TOTAL_PLANNING` with `REVIEW → PLAN → approved planning-document BUILD → REVIEW`.
- Implementation authority: `PLANNING_AND_DOCUMENTATION_ONLY`.
- Do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`.
- Do not merge PR #81 as a whole; preserve it as `REFERENCE_ONLY` until selective promotion is complete.
- Do not promote a Draft or Sheet row to `CURRENT_CONFIRMED` without user approval evidence or a latest explicit user direction.
- Treat detailed technical values, initial balance numbers, spacing, timings, probabilities, and capacity defaults as `RECOMMENDED_DEFAULT` or `TEST_VALUE` until validated.
- Use Grill Me only for project-core choices, incompatible major planning principles, vertical-slice scope, major failure/recovery/reward meaning, replacement of approved Decisions, or alternatives that materially change player experience or production scope.
- Ask one independent Grill Me decision at a time; do not re-ask repository facts, already approved Decisions, or technical test values.
- GitHub is authoritative; Google Sheet is the connected planning and operating surface.
- A synchronization is `SYNCED` only after the same Decision ID, meaning, status, GitHub location, and commit SHA are read back from both surfaces.
- Any unexecuted runtime, Android-device, accessibility, performance, or human-play validation remains `NOT_RUN`.
- Mobile portrait Android is the current product platform. PC remains `FUTURE_PLATFORM_CONSIDERATION`, not a simultaneous UI-delivery requirement.

---

## File Structure and Responsibility Map

| File or Surface | Responsibility after this plan |
|---|---|
| `docs/operations/BS-OPS-20260802-01_BASELINE.md` | Immutable recovery evidence snapshot, protected scope, authority conflicts, and validation status |
| `CURRENT_CONFIRMED_DECISIONS.md` | Root current-decision entrypoint and approval-evidence classification |
| `AGENTS.md` | Repository-wide operating rules, work mode, protected paths, and next-gate routing |
| `[기획서]/00_프로젝트_허브/START_HERE.md` | Cold-start reading order and current work pointer |
| `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md` | Current stage, branch/PR, product reality, blockers, and next planning action |
| `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md` | Planning, review, sync, implementation, and validation gates with fail-closed statuses |
| `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md` | One-owner responsibility map and PR #81 reference boundary |
| `[기획서]/00_프로젝트_허브/ROADMAP.md` | Canonical-recovery milestone followed by total-planning bundles; product work blocked |
| `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json` | Current canonical design-document registration and status |
| `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json` | Project-local skill routes aligned with Base v9.4 selective routing |
| `skills/PROJECT_BASE_ADAPTER.json` | Base v9.4 adapter source, exact GDD Sheet binding, current protected baseline, and validation truth |
| `docs/PROJECT_OPERATING_HEALTH.json` | Operating and product evidence health; must not report PASS when critical gates are NOT_RUN |
| `docs/BASE_V9_4_ADOPTION.md` | Adoption evidence and explicit distinction between released Base version and current project operating state |
| Google Sheet `00·01·02·04·05·90·99` | User-facing current status, ordered work, current decisions, audit findings, GDD overview, production boundary, and change history |
| Issue #60 and #79, PR #81 and #84 | Authority and supersession relationships; no duplicate active owner |

---

### Task 1: Freeze the Recovery Baseline and Failure Contract

**Files:**
- Create: `docs/operations/BS-OPS-20260802-01_BASELINE.md`
- Read: `project.godot`
- Read: `skills/PROJECT_BASE_ADAPTER.json`
- Read: `docs/PROJECT_OPERATING_HEALTH.json`
- Read: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Read: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Read: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Read: PR #81, Issue #60, Issue #79, and Google Sheet metadata/ranges

**Interfaces:**
- Consumes: approved design `docs/superpowers/specs/2026-08-02-planning-canon-recovery-design.md` and base commit `ac120fb146cea29bb5f8876682809f76779d86ad`.
- Produces: a stable evidence record used by every later task, with exact statuses `CONFIRMED`, `CONFLICTED`, `REFERENCE_ONLY`, `NOT_RUN`, or `BLOCKED_UNVERIFIED`.

- [ ] **Step 1: Re-read the exact recovery inputs**

Read the current branch versions of the operating entrypoints, adapters, health file, project entry scene, PR #81 metadata, Issue #60/#79, and the seven target Sheet tabs. Record exact GitHub blob SHAs and Sheet header ranges before any modification.

- [ ] **Step 2: Write the baseline evidence record**

The document must contain these exact sections:

```markdown
# BS-OPS-20260802-01 Baseline Recovery Record

## Repository and Branch
## Base Release and Project Adoption
## Current Product Reality
## Current Canonical Sources
## Open Issue and PR Authority
## Google Sheet State
## Protected Decisions and Strengths
## Confirmed Conflicts
## Validation Evidence
## Prohibited Changes
## Rollback
```

The `Current Product Reality` section must state that `project.godot` still opens `res://scenes/test/enhancement_test.tscn`, and must classify Android device, accessibility, performance, runtime against latest planning, and human play as `NOT_RUN` unless new evidence is actually found.

- [ ] **Step 3: Apply the adversarial baseline attack**

For every conflict, add:

```yaml
finding_id:
attack:
factual_basis:
counterevidence:
impact:
verdict: MUST_FIX | SHOULD_FIX | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED | REJECTED_CRITIQUE
```

At minimum cover stale entrypoints, mixed Base authority, PR #81 divergence, missing current-decision entrypoint, Sheet traceability gaps, duplicate Issue/PR authority, approval-evidence gaps, and current test-scene entry.

- [ ] **Step 4: Verify baseline completeness**

Search the new file for `TBD`, `TODO`, unqualified `PASS`, and unsupported `USER_APPROVED`. Expected result: zero placeholders, zero unqualified PASS claims, and every approval claim linked to evidence or classified for recovery.

- [ ] **Step 5: Commit the baseline**

```bash
git add docs/operations/BS-OPS-20260802-01_BASELINE.md
git commit -m "docs: freeze Blacksmith recovery baseline"
```

---

### Task 2: Establish the Current Decision Authority

**Files:**
- Create: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `[기획서]/00_프로젝트_허브/DECISION_LOG.md`
- Read: PR #81 decision contracts and approval comments
- Read: Issue #79 approval comments

**Interfaces:**
- Consumes: evidence classifications from Task 1.
- Produces: one root entrypoint listing current confirmed Decisions, proposed items requiring evidence review, and history-only records.

- [ ] **Step 1: Build the decision evidence table before writing canon**

Use these columns:

```markdown
| Decision ID | Summary | Approval evidence | Canonical owner | Status | Notes |
```

Recognize these as promotion candidates only after evidence readback: `BS-ART-20260731-01`, `BS-MODAK-20260731-01`, `BS-MAIN-20260801-01`, `BS-SHELL-20260801-01`, `BS-GRADE-20260801-02`, and `BS-SAVE-20260801-01`.

- [ ] **Step 2: Create the root current-decision entrypoint**

The file must separate these sections:

```markdown
## Operating Decision
## Confirmed Product Decisions with Approval Evidence
## Confirmed by Latest User Direction
## Proposed — Approval Evidence Recovery Required
## Research or Test Required
## History Only and Superseded
## Decision Synchronization Ledger
```

Record `BS-OPS-20260802-01` as `APPROVED / SYNC_IN_PROGRESS` until GitHub and Sheet readback is complete.

- [ ] **Step 3: Repair the decision log without rewriting history**

Append entries instead of deleting historical records. Every replacement must include `replaces`, `replaced_by`, or `supersedes` metadata. PR #81-only decisions without sufficient approval evidence remain `PROPOSED_REVIEW_REQUIRED`.

- [ ] **Step 4: Adversarially verify decision classification**

Attack these failure modes:

- a Sheet label is mistaken for user approval;
- a PR intermediate HEAD is mistaken for current canon;
- a later Draft silently overrides an earlier approved Decision;
- technical defaults are promoted into player-experience commitments;
- history-only records remain active consumers.

Expected result: no decision appears in more than one active status section.

- [ ] **Step 5: Commit decision authority**

```bash
git add CURRENT_CONFIRMED_DECISIONS.md "[기획서]/00_프로젝트_허브/DECISION_LOG.md"
git commit -m "docs: restore current decision authority"
```

---

### Task 3: Repair Cold-Start Entrypoints and Planning Gates

**Files:**
- Modify: `AGENTS.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`

**Interfaces:**
- Consumes: current-decision entrypoint from Task 2.
- Produces: a single cold-start path that routes a new worker to the current recovery PR and then to total-planning authoring.

- [ ] **Step 1: Update repository operating rules**

`AGENTS.md` must state:

```text
Current Work Mode: TOTAL_PLANNING
Current Decision: BS-OPS-20260802-01
Product implementation: BLOCKED until PLANNING_AND_REVIEW_COMPLETE_GATE
Protected paths: data/, scripts/, scenes/, assets/, addons/, project.godot
Detailed values: RECOMMENDED_DEFAULT or TEST_VALUE
Major planning conflict: one-question Grill Me
```

- [ ] **Step 2: Replace stale cold-start routing**

`START_HERE.md` must route in this order:

```text
AGENTS.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ current domain canon
→ current planning bundle
→ actual files and validators
```

Remove active routing to PR #35, obsolete branches, and superseded next tasks while retaining them only as history references where necessary.

- [ ] **Step 3: Write current context truthfully**

`ACTIVE_CONTEXT.md` must include:

- `main@ac120fb146cea29bb5f8876682809f76779d86ad` as the recovery base;
- active branch `agent/blacksmith-planning-canon-recovery`;
- Draft PR #84;
- Base release `9.4.0` and project-adoption status separately;
- product entry still being the enhancement test scene;
- planning-first direction and product implementation block;
- PR #81 as `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`;
- next action: complete operating recovery, then start the first total-planning bundle.

- [ ] **Step 4: Make gates fail closed**

`DEVELOPMENT_GATES.md` must define:

```yaml
CANONICAL_RECOVERY_GATE: IN_PROGRESS
PLANNING_COVERAGE_GATE: NOT_STARTED
GRILL_ME_DECISION_GATE: NOT_STARTED
DECISION_SYNC_GATE: IN_PROGRESS
PLANNING_AND_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

No aggregate status may imply PASS while a critical gate is NOT_RUN.

- [ ] **Step 5: Repair documentation ownership and roadmap**

`DOCUMENTATION_MAP.md` must assign one current owner per question. `ROADMAP.md` must order work as:

```text
R0 Operating and Canon Recovery
R1 Project Core and Player Promise
R2 Core / Session / Meta Loop
R3 Forging, Enhancement, Identity, Failure and Save
R4 Customers, World Feedback and Item Chronicle
R5 Economy, Growth and Long-Term Goals
R6 Mobile UX, Accessibility, Art, Audio and Feedback
R7 Vertical Slice Scope, Data, Migration and Validation
R8 Final Adversarial Review and User Review
R9 Codex Implementation Handoff
```

Every R1–R8 milestone remains planning/documentation work; R9 remains blocked until the completion gate closes.

- [ ] **Step 6: Run cold-start text checks**

Verify that a repository-only reader can answer: what the game is, current stage, current Decision, active PR, protected paths, next work, canonical owner for each domain, and what validations remain NOT_RUN.

- [ ] **Step 7: Commit entrypoint repairs**

```bash
git add AGENTS.md "[기획서]/00_프로젝트_허브/START_HERE.md" "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md" "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md" "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md" "[기획서]/00_프로젝트_허브/ROADMAP.md"
git commit -m "docs: repair Blacksmith planning entrypoints"
```

---

### Task 4: Align Registries, Base Adapter, and Operating Health

**Files:**
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`
- Modify: `skills/PROJECT_BASE_ADAPTER.json`
- Modify: `docs/BASE_V9_4_ADOPTION.md`
- Modify or regenerate: `docs/PROJECT_OPERATING_HEALTH.json`
- Verify: `skills/BASE_V9_ADAPTER.json`
- Verify: `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- Verify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: repaired owners and gates from Task 3.
- Produces: machine-readable routing and health that match the human-readable canon.

- [ ] **Step 1: Update the design-document registry**

Register `CURRENT_CONFIRMED_DECISIONS.md`, the baseline record, the approved design, the execution plan, and the current hub documents with exactly one status each. PR #81 documents must be `REFERENCE_ONLY`, `HISTORY_ONLY`, or `PROPOSED_REVIEW_REQUIRED`, never `CURRENT` by inheritance.

- [ ] **Step 2: Verify project-skill routing remains selective**

Preserve `routing_policy.default_selection = "automatic-trigger-match"` and `routing_policy.load_all_skills = false`. Confirm active project routes for engineering, game design, and QA still point to existing paths. Do not create a new project skill merely for this recovery.

- [ ] **Step 3: Correct the Base adapter source**

In `skills/PROJECT_BASE_ADAPTER.json`:

- retain Base release version `9.4.0` and release commits;
- bind the Google Sheet URL `https://docs.google.com/spreadsheets/d/1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg/edit`;
- retain role `USER_FACING_GDD_WORKSPACE`;
- change `gdd_sheet.sync_status` to `SYNC_IN_PROGRESS_BS-OPS-20260802-01` until Sheet readback completes;
- set the protected baseline commit to the actual recovery base `ac120fb146cea29bb5f8876682809f76779d86ad` with an authority description that does not pretend an obsolete migration source is current;
- preserve protected product paths;
- keep runtime and human statuses `NOT_RUN`.

- [ ] **Step 4: Preserve compatibility views**

Do not hand-edit generated or compatibility view files unless their repository contract explicitly permits it. If a generator is available, run the documented generation command and verify output. If no generator can be executed in the current environment, leave the views untouched, record `DERIVATIVE_STALE / BLOCKED_UNVERIFIED`, and do not claim full adapter synchronization.

- [ ] **Step 5: Correct operating health semantics**

`docs/PROJECT_OPERATING_HEALTH.json` must not use `PASS_WITH_NOT_RUN_GATES` as an integrity verdict. Use a fail-closed value such as `INCOMPLETE_NOT_RUN_GATES` while all critical gates remain `NOT_RUN`. Add operating evidence only for checks actually executed; keep product, runtime, device, accessibility, performance, and human evidence empty unless new evidence exists.

- [ ] **Step 6: Update Base adoption evidence**

`docs/BASE_V9_4_ADOPTION.md` must distinguish:

```text
Base release adoption: COMPLETE
Project canonical recovery: IN_PROGRESS
GDD Sheet binding: SYNC_IN_PROGRESS
Product runtime validation against latest planning: NOT_RUN
```

- [ ] **Step 7: Run static validators**

Run when a local checkout is available:

```bash
python tools/check_archive_governance.py
python -m unittest tests.test_archive_retention_governance -v
python tools/audit_project_operating_system.py
```

Expected: no new missing-entrypoint, routing, path, or stale-authority errors caused by this task. Any unavailable local execution is recorded as `NOT_RUN`, not PASS.

- [ ] **Step 8: Commit registry and adapter alignment**

```bash
git add "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json" "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json" skills/PROJECT_BASE_ADAPTER.json docs/BASE_V9_4_ADOPTION.md docs/PROJECT_OPERATING_HEALTH.json
git commit -m "docs: align Blacksmith Base v9.4 operating state"
```

---

### Task 5: Synchronize the Operating Decision to Google Sheet

**Files and Surfaces:**
- Read and update: `00_프로젝트_허브`
- Read and update: `01_작업순서`
- Read and update: `02_현재_확정결정`
- Read and update: `04_누락_충돌_감사`
- Read and update: `05_GDD_요약`
- Read and update: `90_본제작_출시_사업`
- Read and update: `99_변경이력`
- Modify after Sheet commit reference is known: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify after Sheet commit reference is known: `skills/PROJECT_BASE_ADAPTER.json`

**Interfaces:**
- Consumes: GitHub commit SHAs from Tasks 1–4.
- Produces: the same `BS-OPS-20260802-01` record on GitHub and Sheet with readback evidence.

- [ ] **Step 1: Load mandatory Google Sheets editing references**

Before any write, read the connector references for edit workflow, live-read safety, batch-update recipes, native cell structure when inserting rows, and visual-quality verification.

- [ ] **Step 2: Re-read bounded target ranges**

Read metadata and bounded used ranges for each target tab. Identify exact headers, Decision-ID column, status column, GitHub-path column, commit-SHA column, and history rows. Do not guess row numbers or overwrite formulas, validations, or merged cells.

- [ ] **Step 3: Update the project hub and work order**

Write the current state:

```text
Base release: 9.4.0
Current stage: CANONICAL_RECOVERY_IN_PROGRESS
Current Decision: BS-OPS-20260802-01
Current Draft PR: #84
Product implementation: BLOCKED
Next work: finish recovery, then R1 project core and player promise
```

Replace active v9.3 and PR #61/#62 instructions; preserve historical references only in history/audit fields.

- [ ] **Step 4: Repair the current-decision ledger**

Ensure exactly one current row for `BS-OPS-20260802-01` containing:

```text
status = APPROVED
summary = planning-first canonical recovery and Grill Me gates
GitHub canonical location = CURRENT_CONFIRMED_DECISIONS.md
Draft PR = #84
commit SHA = latest exact branch HEAD after Tasks 1–4
sync status = SYNCED only after readback
```

Rows without current canonical path or evidence must be reclassified to `APPROVAL_EVIDENCE_RECOVERY_REQUIRED`, `HISTORY_ONLY`, or the supported current status; do not silently delete historical content.

- [ ] **Step 5: Append the audit and change-history records**

In `04_누락_충돌_감사`, append the validated MUST_FIX and SHOULD_FIX findings with the same Decision ID. In `99_변경이력`, append GitHub paths, exact commit SHA, PR #84, affected tabs/ranges, and readback result.

- [ ] **Step 6: Update GDD and production boundary summaries**

`05_GDD_요약` must show planning-first status and separate confirmed canon from proposed/research-required content. `90_본제작_출시_사업` must replace the active v9.3 migration milestone with v9.4 canonical recovery and keep production implementation blocked.

- [ ] **Step 7: Read back every modified anchor**

Re-read the written rows and verify:

```text
same Decision ID
same decision meaning
same approval status
same PR number
same GitHub canonical path
same exact commit SHA
no overwritten formulas or validation
```

If any field differs, set `SYNC_CONFLICT` and stop before the next major planning bundle.

- [ ] **Step 8: Finalize GitHub sync status**

After successful Sheet readback, update `CURRENT_CONFIRMED_DECISIONS.md` and `skills/PROJECT_BASE_ADAPTER.json` from `SYNC_IN_PROGRESS` to `SYNCED`, record exact Sheet tabs/ranges, then commit:

```bash
git add CURRENT_CONFIRMED_DECISIONS.md skills/PROJECT_BASE_ADAPTER.json
git commit -m "docs: finalize BS-OPS-20260802-01 synchronization"
```

Re-read the Sheet commit-SHA field if this final commit changes the recorded exact HEAD. Update the Sheet once more so the final GitHub HEAD and Sheet record match.

---

### Task 6: Reconcile Issue and Pull Request Authority

**Files and Surfaces:**
- Comment or update: Issue #79
- Comment or update: Issue #60
- Comment: PR #81
- Update description: PR #84

**Interfaces:**
- Consumes: synchronized authority from Task 5.
- Produces: one active recovery PR and one active total-planning authority path without losing historical evidence.

- [ ] **Step 1: Update Issue #79 as the planning umbrella**

Add `BS-OPS-20260802-01`, PR #84, recovery status, product-implementation block, and the R1–R8 planning sequence. State that major planning conflicts will be raised one at a time through Grill Me.

- [ ] **Step 2: Classify Issue #60**

Mark it `HISTORY_ONLY / SUPERSEDED_BY_BS-OPS-20260802-01` if its active purpose is fully replaced. Close only after confirming no unique unresolved work would be lost; otherwise leave open with a superseded label and explicit residual scope.

- [ ] **Step 3: Preserve PR #81 as a reference source**

Comment that PR #81 is `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`. Link PR #84 and state that only evidence-backed planning content will be selectively promoted. Do not close PR #81 until the selective-promotion inventory has been recorded.

- [ ] **Step 4: Expand PR #84 status**

Update the PR body with completed task commits, exact changed-file inventory, Sheet ranges, sync status, validation commands and results, NOT_RUN gates, rollback, and the next total-planning bundle.

- [ ] **Step 5: Verify no duplicate active authority remains**

A new worker must identify PR #84 as the current recovery PR, Issue #79 as the planning umbrella, and PR #81 as reference-only. Any ambiguous active instruction is a `MUST_FIX` before continuing.

---

### Task 7: Run the Adversarial Review and Regression Recheck

**Files:**
- Modify: `docs/operations/BS-OPS-20260802-01_BASELINE.md`
- Modify when findings require safe corrections: files changed in Tasks 2–5

**Interfaces:**
- Consumes: all recovery changes and synchronization evidence.
- Produces: validated findings with no unapproved product-direction changes.

- [ ] **Step 1: Attack the recovered state**

Test these hypotheses:

1. the new root decision file conflicts with a domain canon;
2. PR #81 still appears as merge-ready current authority;
3. the Sheet and GitHub use the same Decision ID but different meanings;
4. `SYNCED` points to a non-final commit;
5. Base v9.4 release adoption is confused with product readiness;
6. a NOT_RUN gate is summarized as pass;
7. a technical default has become a player-experience commitment;
8. PC consideration has expanded mobile scope;
9. a protected product path changed;
10. the first total-planning bundle would start before recovery is actually complete.

- [ ] **Step 2: Validate every critique**

For each attack, record factual basis, counterevidence, probability, impact, fix cost, strengths at risk, and verdict. Reject preference-only or duplicate critiques as `REJECTED_CRITIQUE`.

- [ ] **Step 3: Apply only safe planning fixes**

Automatically correct broken paths, stale IDs, missing statuses, contradictory descriptions, and missing sync evidence. Do not decide project-core or major-system alternatives. Escalate those as `USER_DECISION_REQUIRED` for a future one-question Grill Me.

- [ ] **Step 4: Confirm protected-path integrity**

Compare the exact branch against `main@ac120fb146cea29bb5f8876682809f76779d86ad`. Expected product-path changes:

```text
0 files under data/
0 files under scripts/
0 files under scenes/
0 files under assets/
0 files under addons/
project.godot unchanged
```

- [ ] **Step 5: Commit any validated safe corrections**

```bash
git add <only validated planning and operating files>
git commit -m "docs: resolve canonical recovery review findings"
```

If no corrections are needed, record `NO_CHANGE_REQUIRED` in the baseline instead of creating an empty commit.

---

### Task 8: Exact-HEAD Verification and Planning Handoff

**Files and Surfaces:**
- Verify: all branch changes against `main`
- Verify: PR #84 metadata, comments, checks, and review threads
- Verify: Google Sheet readback
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: PR #84 body

**Interfaces:**
- Consumes: final recovery branch HEAD and synchronized Sheet.
- Produces: an exact-HEAD decision report and an unambiguous handoff to the first total-planning bundle.

- [ ] **Step 1: Capture exact final HEAD and changed-file inventory**

Compare `main` to `agent/blacksmith-planning-canon-recovery`. List every changed path, additions/deletions, and verify every path belongs to planning/operations scope.

- [ ] **Step 2: Inspect PR state**

Check PR #84 base/head, draft state, mergeability, checks, reviews, unresolved threads, behind status, and current main divergence. Do not claim merge-ready while mergeability or required checks remain unresolved.

- [ ] **Step 3: Run available validation commands**

Run repository validators when local execution is available. Record each command independently as `PASS`, `FAIL`, `NOT_RUN`, or `BLOCKED_UNVERIFIED`; never infer runtime or device validation from document checks.

- [ ] **Step 4: Run final cold-start validation**

Using repository files only, answer:

1. What is Blacksmith?
2. What is the current player promise?
3. What stage is the project in?
4. What is the current Decision and PR?
5. What must not be changed?
6. Where is each planning owner?
7. Which skills and Work Mode apply?
8. Which gates block implementation?
9. What must be synchronized after a decision?
10. Which risks and validations remain open?

Expected: all answers are discoverable without PR #81 or past chat context.

- [ ] **Step 5: Close the recovery gates truthfully**

Only after GitHub/Sheet readback and adversarial review pass:

```yaml
CANONICAL_RECOVERY_GATE: PASS
DECISION_SYNC_GATE: PASS
PLANNING_COVERAGE_GATE: NOT_STARTED
PLANNING_AND_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
```

- [ ] **Step 6: Define the next planning bundle**

Set the next task to `R1 Project Core and Player Promise`. Its input must include confirmed Decisions, protected strengths, actual implementation facts, planning gaps, benchmark/research questions, and potential Grill Me candidates. Do not begin product implementation.

- [ ] **Step 7: Commit final recovery status**

```bash
git add "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md" "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md" docs/operations/BS-OPS-20260802-01_BASELINE.md
git commit -m "docs: complete Blacksmith canonical recovery gate"
```

- [ ] **Step 8: Final readback**

Re-read the final GitHub files, PR #84 exact HEAD, Issue authority comments, and Sheet records. `BS-OPS-20260802-01` is complete only when all exact references agree.

---

## Plan Self-Review

### Spec Coverage

- Planning-first and product-code prohibition: Tasks 1, 3, 7, 8.
- Detailed values as `RECOMMENDED_DEFAULT / TEST_VALUE`: Global Constraints, Tasks 2 and 7.
- Important conflicts only through one-question Grill Me: Global Constraints, Tasks 3, 6, 8.
- PR #81 selective promotion rather than whole merge: Tasks 1, 2, 6.
- Operating recovery before total-planning writing: Tasks 1–8.
- GitHub and Google Sheet same-ID synchronization: Task 5 and Task 8.
- Base v9.4 authority repair: Task 4.
- Adversarial Attack/Validate/Regression loop: Tasks 1 and 7.
- Cold-start validation: Tasks 3 and 8.
- No false validation claims: Tasks 1, 3, 4, 8.
- Rollback and protected paths: Global Constraints, Tasks 1 and 7.

### Placeholder Scan

- `TBD`: absent.
- `TODO`: absent.
- Unsupported implementation directions: absent.
- Product changes: explicitly prohibited.
- Dynamic Sheet row positions: resolved by exact headers and Decision-ID keys before writes rather than guessed row numbers.

### Interface Consistency

- Every task uses Decision ID `BS-OPS-20260802-01`.
- Recovery base remains `ac120fb146cea29bb5f8876682809f76779d86ad`.
- Active branch remains `agent/blacksmith-planning-canon-recovery`.
- Active recovery PR remains #84.
- Final handoff remains R1 total-planning, not Codex implementation.
