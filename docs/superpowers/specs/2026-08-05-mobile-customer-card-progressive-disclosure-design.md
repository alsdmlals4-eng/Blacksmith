# Mobile Customer Card Progressive Disclosure Design

- Decision: `BS-UX-20260805-01`
- Status: `USER_APPROVED / R2_BATCH_005_3_OF_10 / APPROVED_PENDING_MERGE`
- Product implementation: `BLOCKED`

## Goal

Design a mobile-first customer card that makes equipment assignment explainable without turning the customer system into a dense character-RPG screen.

## Design boundary

The feature owns information hierarchy and interaction disclosure only. It does not change customer stats, proficiency values, success formulas, equipment raw stats, event resolution, or item UID ownership.

## Surface model

### Default customer card

Shows identity, role, current schedule summary, four base stats, only the relevant primary/secondary proficiencies, context-relevant magic aptitude, and the persistent primary assignment action.

### Post-equipment decision layer

Appears in place after an item selection. Shows balance state, success forecast, two to four reason chips, and special-function risk only when applicable. Comparison feedback highlights the reasons that changed.

### Detail view

Opened through one explicit detail entry per card. Shows all relevant proficiencies, total weight and comfortable load, special-function fit factors, applicable item-stat breakdown, and disclosure-safe success inputs.

## Interaction rules

- Preserve selected item and scroll position when entering or leaving detail.
- Never require long press, swipe, or hover to access critical information.
- Keep the primary assignment action visible in collapsed and expanded states.
- Use in-place updates for item comparison rather than mandatory full-screen transitions.

## Accessibility

- Minimum interactive target: 48dp.
- Color is never the only state signal.
- State text or icon-plus-text is required.
- Reading order is identity → requirement → stats/proficiency → selected item result → reasons → action.
- Text scaling must not cover the primary action or reason chips.

## PC adaptation

Keep the same information hierarchy. Wider layouts and pointer tooltips are optional enhancements, but no critical information may be hover-only.

## Failure and empty states

- No item selected: show the requirement summary and a clear selection prompt; do not show a fake zero fit score.
- Non-applicable magic: omit the field rather than displaying zero.
- Unknown event modifier: label the forecast as uncertain and show known reasons only.
- Incompatible item: show `부적합` plus explicit reasons; do not silently disable comparison.

## Test contract

The planning contract must verify the three layers, required fields, 2–4 reason chips, one detail entry, 48dp target, non-color-only communication, no long-press/hover-only critical information, PC hierarchy parity, and blocked product implementation.
