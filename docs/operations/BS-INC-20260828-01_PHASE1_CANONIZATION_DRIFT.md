# BS-INC-20260828-01 · Phase-1 Canonization Drift

## Incident

Fresh-read on 2026-08-28 found that the current Phase-1 planning request, the
repository's historical runtime implementation receipts, and the human-facing
Notion pages were being read as one current claim. This overstated what had been
human-validated and made it possible to infer new product-mutation authority from
old merged implementation work.

## Evidence

- Project GitHub completed main: `a1799f910a27954c902297978fb79f81ca586e87`.
- Actual runtime assets, consumers, and automated contracts exist; client render,
  Android, accessibility, performance, and Human play are still `NOT_RUN`.
- Notion Home, Visual Bible, Flow, Production, and System Record contained older
  SHAs and pre-Decision29/31/32 claims alongside current overrides.
- `AGENTS.md` and the current user request require Phase-1 co-design before any
  new product mutation.

## Solution

The current planning owner and handoff now explicitly separate:

```text
CURRENT_PHASE = PHASE_1_PLANNING_CO_DESIGN
CURRENT_ACCEPTED_FRONTIER = CANONIZATION_AND_CORE_EXPERIENCE_REVIEW
HISTORICAL_RUNTIME_IMPLEMENTATION = AUTOMATED_EVIDENCE_ONLY_NOT_CURRENT_AUTHORITY
NEW_PRODUCT_MUTATION = BLOCKED_UNTIL_PHASE_1_AND_2_APPROVAL
```

Notion receives the same top-of-page override and current main identity. No
product path is changed by this incident resolution.

## Lesson

Historical implementation evidence must be retained as evidence, but it must not
silently widen the current planning gate or Human/Player evidence ceiling. Human
pages need a current override at their top whenever a later source reopens
planning.

## Base promotion

`NO_BASE_PROMOTION`: the failure is caused by Blacksmith's unusually deep mix of
legacy R2, Decision25–32, runtime-MVP, and Notion Living-GDD surfaces. The
general Base policy already requires owner precedence, fresh-read, and evidence
ceilings; no project-specific identifiers or added shared rule are warranted.
