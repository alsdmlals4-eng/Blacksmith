# BS-INC-20260828-01 · Phase-1 Canonization Drift

`STATUS = HISTORICAL_PHASE1_CANONIZATION_DRIFT / SUPERSEDED_BY_CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826`

## Incident

Fresh-read on 2026-08-28 found that the then-current Phase-1 planning request, the
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
- At that time, `AGENTS.md` and the user request required Phase-1 co-design before
  any new product mutation. The later user declaration superseded that execution gate.

## Solution

At that time, the planning owner and handoff explicitly separated:

```text
CURRENT_PHASE = PHASE_1_PLANNING_CO_DESIGN
CURRENT_ACCEPTED_FRONTIER = CANONIZATION_AND_CORE_EXPERIENCE_REVIEW
HISTORICAL_RUNTIME_IMPLEMENTATION = AUTOMATED_EVIDENCE_ONLY_NOT_CURRENT_AUTHORITY
NEW_PRODUCT_MUTATION = BLOCKED_UNTIL_PHASE_1_AND_2_APPROVAL
```

Notion received the same top-of-page override and current main identity. No
product path was changed by this incident resolution. The current execution
authority is now `CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826`.

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
