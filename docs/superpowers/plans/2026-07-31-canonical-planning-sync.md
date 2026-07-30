# Canonical Planning Sync Execution Plan

> Decision ID: `BS-SYNC-20260731-01`
>
> Status: `ACTIVE_PLAN`
>
> Scope: planning authority, planning data, Google Sheet, and evidence logs only

## Objective

Apply every major or approved decision as one traceable change set across GitHub and the connected Blacksmith Google Sheet.

## Execution Order

### Task 1 — Recover Current Authority

- Read the current user-approved decision source.
- Read the current master, authority map, structured planning data, and affected Sheet ranges.
- Identify conflicts, stale values, and formula errors.

### Task 2 — Allocate Decision ID

- Use one immutable ID per independent decision.
- Reuse that same ID in Markdown, JSON, Sheet decision rows, audit rows, and change history.
- Do not reuse an ID for an unrelated decision.

### Task 3 — Commit GitHub Draft Authority

- Update or create the authority Markdown.
- Update machine-readable planning data.
- Update the documentation map.
- Commit to the active planning branch.

### Task 4 — Synchronize Google Sheet

- Write the same Decision ID into `02_현재_확정결정`.
- Update only directly affected GDD ranges.
- Add the same ID to `04_누락_충돌_감사` and `99_변경이력`.
- Record PR, branch commit, and exact ranges.
- Use `SYNCED_TO_DRAFT` before merge.

### Task 5 — Re-read and Verify

- Re-read every changed GitHub file.
- Re-read every changed Sheet range.
- Verify no written text beginning with `+` became a formula.
- Verify the Decision ID is identical across all targets.
- Verify product paths were not modified.

### Task 6 — Merge Follow-up

After merge:

- replace Draft commit evidence with merge commit evidence
- update Sheet status to `SYNCED_TO_MAIN`
- re-run cross-source comparison
- retain the original Decision ID

## Current Application

This plan is first applied to:

- the eight user-approved Blacksmith v9 decisions
- the benchmark-first working principle
- the immediate canonical synchronization rule itself
- stale v6/customer-four summaries and current formula errors in directly affected Sheet tabs

## Non-goals

- product code or Godot data implementation
- Scene or asset changes
- full repository legacy rewrite before review
- declaring `기획 완료` or `검수 완료` on the user's behalf
- Codex implementation authorization