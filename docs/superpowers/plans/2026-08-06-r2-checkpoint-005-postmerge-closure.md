# R2 Checkpoint 005 Postmerge Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize every current-authority planning surface from PR #109 premerge state to immutable main-canon closure evidence.

**Architecture:** Add one focused regression contract, then use an idempotent repository patch script to update only current-authority Markdown and JSON files. Preserve detailed canon documents and all product paths. Record closure evidence in a dedicated document and verify through PR Actions and readback.

**Tech Stack:** Python 3.12, `unittest`, JSON, Markdown, GitHub Actions.

## Global Constraints

- PR #109 source head: `77eba15415bc9ede661639b45bb526d5ce4410a5`.
- PR #109 squash merge: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9`.
- No game-design or balance changes.
- Product implementation remains `BLOCKED`.
- Human playtest remains `NOT_RUN`.
- Next batch is available at `0/10` but remains `NOT_STARTED`.
- Explicit user approval is required before merging the closure PR.

---

### Task 1: Add closure regression contract

**Files:**
- Create: `tests/test_r2_checkpoint_005_postmerge_closure.py`

**Interfaces:**
- Consumes: current authority Markdown and `CURRENT_R2_CANON_REGISTRY.json`.
- Produces: deterministic pass/fail evidence for PR #109 closure state.

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Trigger PR validation and confirm failure is caused by stale premerge state**
- [ ] **Step 3: Record RED run and exact head in the closure document**

### Task 2: Apply current-authority closure state

**Files:**
- Create: `tools/close_r2_checkpoint_005.py`
- Create: `docs/planning/BLACKSMITH_R2_CHECKPOINT_005_POSTMERGE_CLOSURE_2026.md`
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`

**Interfaces:**
- Consumes: PR #109 immutable merge evidence.
- Produces: idempotent closure state and next-batch routing.

- [ ] **Step 1: Implement exact replacement and JSON mutation rules**
- [ ] **Step 2: Run the script once and ensure only approved files change**
- [ ] **Step 3: Run the focused test and full planning contracts**
- [ ] **Step 4: Run the script a second time and verify no diff**

### Task 3: Synchronize operational mirrors

**Files:**
- Modify: Google Sheet standard status rows using the same merge evidence.
- Modify: PR body after exact-head validation.

**Interfaces:**
- Consumes: closure branch exact head and CI evidence.
- Produces: GitHub/Sheet readback parity.

- [ ] **Step 1: Update the six standard Sheet locations**
- [ ] **Step 2: Read back every changed range**
- [ ] **Step 3: Update the draft PR body with RED/GREEN evidence and protected-scope audit**

### Task 4: Final verification

**Files:**
- No additional product files.

- [ ] **Step 1: Confirm focused contract PASS**
- [ ] **Step 2: Confirm Planning-first, Base adoption, PR validation, Python, and Godot checks PASS**
- [ ] **Step 3: Confirm comments and unresolved review threads are zero or addressed**
- [ ] **Step 4: Leave the PR draft and unmerged pending explicit approval**