# Canonical Planning Sync Design

> Decision ID: `BS-SYNC-20260731-01`
>
> Status: `USER_APPROVED / CURRENT`
>
> Date: `2026-07-31`
>
> Work Mode: `PLAN`

## Problem

Approved decisions have been recorded in chat or Draft planning documents while the authority map, machine-readable planning data, and connected Google Sheet remained on older v6 or Base v9.1-era summaries. This creates authority drift, duplicate interpretation, and formula errors caused by text beginning with `+`.

## Design Goal

Every major change or user-approved decision must become one traceable canonical change set with the same immutable Decision ID across:

1. GitHub narrative authority documents
2. GitHub machine-readable planning data
3. Documentation map or equivalent authority index
4. Connected Google Sheet decision index and directly affected tabs
5. Audit and change-history records

## State Model

```text
APPROVED_IN_CONVERSATION
→ GITHUB_DRAFT_COMMITTED
→ SHEET_SYNCED_TO_DRAFT
→ GITHUB_MAIN_MERGED
→ SHEET_SYNCED_TO_MAIN
→ CROSS_SOURCE_REVERIFIED
```

Before merge, Sheet entries must identify the PR, branch, and Draft commit and use `SYNCED_TO_DRAFT`. They must not claim that main already contains the decision.

After merge, the same Decision ID is updated with the merge commit and `SYNCED_TO_MAIN`.

## Trigger

Immediate canonical synchronization is required for:

- project core or scope
- major system rules
- content structure
- major UX flow
- economy, probability, protection, storage, or lifecycle rules
- platform, release, server, ranking, privacy, or operating policy
- explicit user approval of a proposed design

Minor copy edits, formatting, and implementation fixes that do not change a planning contract may use an existing Decision ID or a maintenance Change ID.

## Write Set

A complete synchronization writes or updates:

- one authoritative Markdown source
- one machine-readable JSON/data source when the decision affects structured consumers
- the documentation map or authority index
- `02_현재_확정결정`
- directly affected GDD tabs
- `04_누락_충돌_감사`
- `99_변경이력`

## Failure Handling

If any target cannot be updated:

- preserve completed writes
- mark the operation `PARTIAL_SYNC_BLOCKED`
- record the missing target and reason
- do not describe the decision as fully synchronized
- retry only the failed range after re-reading current values

## Relationship to Bulk Legacy Propagation

Immediate decision synchronization and bulk cleanup are different operations.

- Approved decisions: synchronize immediately to the decision index and directly affected current summaries.
- Historical document rewrites and repository-wide legacy cleanup: may remain gated behind planning-completion and merge review.

This distinction prevents Sheet drift without prematurely rewriting every historical source.