# Adventurer 01 Nadia — information, result, and playtest refinement

Status: `USER_APPROVED_SUPPORTING_SPEC / NON_CANONICAL / SAME_DECISION_REFINEMENT`

Decision: `BS-CONTENT-20260811-01`
Canonical owner: `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
Approval counter: `R3_R7_1_OF_10` (unchanged)
Product implementation: `BLOCKED`
Task3 implementation: `NOT_APPROVED`

## Purpose

Refine the already-approved Nadia content without creating a second authority: make equipment handoff explainable on mobile, keep the three result axes readable, and define disposable fixture/playtest evidence before any product implementation.

## Approved refinement

```text
DEFAULT_CUSTOMER_CARD
→ POST_EQUIPMENT_DECISION_LAYER
→ DETAIL_VIEW
→ handoff
→ THREE_STATE_SUMMARY_TWO_TO_FOUR_REASONS_ONE_PRIMARY_NEXT_ACTION
→ same UID follow-up
```

Reason priority is `LOAD_GATE_THEN_ENHANCEMENT_THEN_RELEVANT_UTILITY_THEN_SMALL_CUSTOMER_CONTEXT`. `OVERWEIGHT` is a hard assignment failure and cannot be buried under an approximate success percentage. No auto-recommended best item, opaque total fit score, or default full comparison matrix is introduced.

## Test-only fixture boundary

`NON_CANONICAL_BASELINE_TEST_FIXTURE` uses at least three contrasting item candidates: high-enhancement/heavy, balanced/within-load, and lower-enhancement/context-utility. Unknown approved utility content is represented only by `APPROVED_RELEVANT_UTILITY_PLACEHOLDER`; the spec does not create a new product function.

## Evidence contract

Use `OBSERVED_BEHAVIOR_PLUS_NEUTRAL_RECALL`. Observe comparison behavior, non-enhancement checks, approximate-probability interpretation, overweight-gate comprehension, and same-UID follow-up intent. Neutral recall asks what item was entrusted, what information mattered, what caused the result, whether the returned item is the same work, and what the player wants to do next.

## Adversarial findings

- `MUST_FIX`: hard load gate must outrank success percentage.
- `MUST_FIX`: auto-recommended/Best UI would collapse the core equipment choice.
- `SHOULD_FIX`: result screen must summarize three axes with only 2–4 reasons and one primary next action before details.
- `TEST_REQUIRED`: item swapping may still cause excessive taps; measure before adding a matrix.
- `MUST_NOT`: fixture numbers, placeholder utility names, or playtest outcomes are not product canon.

## Implementation boundary

This supporting spec authorizes no Godot Scene, Resource, `project.godot`, Script, runtime data, asset, Task3, or general product implementation.
