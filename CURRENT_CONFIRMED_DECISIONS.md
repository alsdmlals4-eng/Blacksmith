# Blacksmith Current Confirmed Decisions

> Current operating Decision: `BS-OPS-20260802-01`
>
> Status: `APPROVED / GITHUB_AND_SHEET_READBACK_VERIFIED`
>
> Recovery branch: `agent/blacksmith-planning-canon-recovery`
>
> Draft PR: `#84`
>
> Next planning bundle: `R1 Project Core and Player Promise`

## 1. Authority Rule

This file is the root entrypoint for the current status of Decisions. Detailed contracts live in registered domain canon. Actual implementation lives in code, Scene, Resource, data, and tests. Google Sheet is the connected `USER_FACING_GDD_WORKSPACE`; it cannot independently override GitHub canon.

An implementation fact, historical PASS, Draft label, and Sheet `CURRENT` label are not equivalent to user approval.

## 2. Status Vocabulary

- `CONFIRMED_WITH_APPROVAL_EVIDENCE`: original user approval evidence is identified.
- `CONFIRMED_BY_LATEST_USER_DIRECTION`: explicitly confirmed by the latest user instruction or approval.
- `RECOMMENDED_DEFAULT`: GPT-selected detailed or technical default, revisable by evidence.
- `TEST_VALUE`: trial value requiring simulation, runtime, device, or playtest evidence.
- `PROPOSED_REVIEW_REQUIRED`: useful Draft content without sufficient current approval traceability.
- `USER_DECISION_REQUIRED`: verified important conflict requiring one-question Grill Me.
- `RESEARCH_OR_TEST_REQUIRED`: cannot be finalized through documents alone.
- `REFERENCE_IMPLEMENTATION`: actual or historical implementation fact, not automatic planning canon.
- `HISTORY_ONLY`: superseded or obsolete authority preserved for traceability.

## 3. Current Operating Decision

### `BS-OPS-20260802-01` — Planning-first canonical recovery and Grill Me boundary

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED / SYNCED`.
- Approval date: `2026-08-02 KST`.
- Canonical locations:
  - this file;
  - `docs/operations/BS-OPS-20260802-01_BASELINE.md`;
  - `docs/operations/BS-OPS-20260802-01_FINAL_REPORT.md`.
- Approved design: `docs/superpowers/specs/2026-08-02-planning-canon-recovery-design.md`.
- Execution plan: `docs/superpowers/plans/2026-08-02-blacksmith-planning-canon-recovery.md`.
- Draft PR: `#84`.
- Sheet readback: `PASS` for `00·01·02·04·05·90·99` bounded recovery ranges.
- Exact final Draft HEAD: tracked by GitHub PR metadata and Sheet `99_변경이력`; it is not embedded into its own commit to avoid a self-referential commit loop.

Confirmed contract:

1. Start with planning authoring, not product implementation.
2. Keep product code, Scene, runtime data, and assets unchanged through planning and review.
3. Use `RECOMMENDED_DEFAULT` or `TEST_VALUE` for detailed technical and early numeric values.
4. Use Grill Me only for verified important planning decisions or genuine conflicts.
5. Ask one independent Grill Me decision at a time.
6. Do not re-ask repository facts, existing approvals, technical details, or ordinary trial values.
7. Apply `Attack → Validate Critique → options → classification → approved minimum change → sync → regression recheck` to every major planning bundle.
8. Synchronize major approvals to GitHub canon and the linked Sheet with the same Decision ID.
9. Keep Android portrait mobile as the current product platform; PC remains future consideration.
10. Keep Codex product implementation blocked until total planning, adversarial final review, and user review are complete.

## 4. Confirmed Product Decisions with Approval Evidence

These are current planning canon. Their implementation and validation states remain separate.

### `BS-ART-20260731-01` — Stylized Dark Forge

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / SELECTIVE_DOMAIN_PROMOTION_PENDING`.
- Decision: dark-forge weight, readable equipment, warm local firelight, stylized 2D, equipment as visual protagonist.
- Approval evidence: Sheet `99_변경이력`, `2026-07-31 22:20 KST`, `USER+GPT`.
- Detailed Draft source: PR #81; R6 selective promotion.
- Final product implementation and device/human visual QA: `NOT_RUN`.

### `BS-MODAK-20260731-01` — Bright fire-spirit Modak

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / SELECTIVE_DOMAIN_PROMOTION_PENDING`.
- Decision: approved calm expression, bright yellow/orange fire-spirit body; charcoal-shell body is not the default.
- Approval evidence: Sheet `99_변경이력`, `2026-07-31 22:20 KST`, `USER+GPT`.
- Detailed Draft source: PR #81; R6 selective promotion.
- Final product asset and runtime/device QA: `NOT_RUN`.

### `BS-MAIN-20260801-01` — Separate main menu

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / IMPLEMENTATION_NOT_STARTED`.
- Decision: separate Main Menu with Continue, New Game, and Settings; save-aware Continue and replacement warning.
- Approval evidence: Sheet `99_변경이력`, `2026-08-01 04:37 KST`, `USER+GPT`.
- Actual current run entry: `res://scenes/test/enhancement_test.tscn`.
- Detailed Draft source: PR #81; R6 selective promotion.

### `BS-SHELL-20260801-01` — Single BlacksmithApp shell

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / IMPLEMENTATION_NOT_STARTED`.
- Decision: after the separate Main Menu, one `BlacksmithApp` keeps campaign state while Views and Overlays divide navigation and interruption responsibilities.
- Approval evidence: Sheet `99_변경이력`, `2026-08-01 04:37 KST`, `USER+GPT`.
- Detailed Draft source: PR #81; R6 selective promotion.

### `BS-GRADE-20260801-02` — Five craftsmanship grades

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / DATA_MIGRATION_NOT_STARTED`.
- Decision: `보통 → 우수 → 명품 → 걸작 → 전설`; remove `양질`; Legendary does not unlock unrelated systems by itself.
- Supersedes: `BS-GRADE-20260801-01` and earlier grade wording in `BS-V9-20260731-01`.
- Approval evidence: Sheet `99_변경이력`, `2026-08-01 05:34 KST`, `USER+GPT`.
- IDs, distribution, multipliers, customer scores, and migration values: `RECOMMENDED_DEFAULT / TEST_VALUE` until R3.

### `BS-SAVE-20260801-01` — Save, Continue, and ResultEnvelope

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / IMPLEMENTATION_NOT_STARTED`.
- Decision: one campaign, two automatic backups, no manual load slots, corruption recovery, safe New Game replacement, `AttemptIntent`, and `ResultEnvelope` preventing reroll, double application, and resource loss without a result.
- Approval evidence: Sheet `99_변경이력`, `2026-08-01 09:33 KST`, `USER+GPT`.
- Android process-death and human validation: `NOT_RUN`.
- Detailed Draft source: PR #81; R3 selective promotion.

## 5. Protected Working Direction for R1 Revalidation

- one blacksmith, not staff management;
- direct forging and visible enhancement-risk decisions;
- equipment as a memorable work with identity, owner, fate, and chronicle;
- equipment remains meaningful after sale or delivery through world feedback;
- no direct player combat as the current core activity;
- portrait-mobile, one-hand-readable information hierarchy;
- one normal-enhancement input resolves exactly one result;
- automation may reduce repetition but may not bypass identity, precision, destruction, material, sale, or ownership decisions.

Status: `PROTECTED_WORKING_DIRECTION / R1_REVALIDATION_REQUIRED`.

R1 may clarify and strengthen this direction. It may not silently discard it and invent an unrelated game.

## 6. Proposed, Research-required, and Historical Content

PR #81 and old Sheet rows are classified before selective promotion.

| Decision or area | Current status | Next review |
|---|---|---|
| `PR57-PROB` | `APPROVAL_EVIDENCE_RECOVERY_REQUIRED` | R3/R5 |
| `PR58-ENDGAME` | `RESEARCH_OR_TEST_REQUIRED` | R5 |
| `PR59-CUSTOMER` | `USER_DECISION_CANDIDATE / EVIDENCE_REVIEW_REQUIRED` | R4 |
| lineage and affix cap | `PROPOSED_REVIEW_REQUIRED` | R3/R6 |
| +50 routes | `PROPOSED_REVIEW_REQUIRED` | R2/R3/R5/R7 |
| customer eligibility and fit | `PROPOSED_REVIEW_REQUIRED` | R4 |
| fate states and destruction/recovery | `PROPOSED_REVIEW_REQUIRED` | R3/R4 |
| customer count and representative content | `PROPOSED_REVIEW_REQUIRED` | R4/R7 |
| online Hall of Masterpieces | `DEFERRED_FUTURE_REVIEW` | R5/R7 |
| v9 data migration | `PROPOSED_REVIEW_REQUIRED` | R3/R7 |
| common customer pipeline | `PROPOSED_REVIEW_REQUIRED` | R4/R7 |
| Auto Forge boundary | `PROPOSED_REVIEW_REQUIRED` | R3/R5 |
| visual asset governance | `PROPOSED_REVIEW_REQUIRED` | R6/R7 |
| Android/accessibility detail | `PROPOSED_REVIEW_REQUIRED / RESEARCH_OR_TEST_REQUIRED` | R6/R7 |
| storage/sales/chronicle capacities | `PROPOSED_REVIEW_REQUIRED / TEST_VALUE_REVIEW_REQUIRED` | R4/R5 |
| validation evidence model | `PROPOSED_REVIEW_REQUIRED / EXECUTION_NOT_RUN` | R7 |
| Base v9.3 migration plans | `HISTORY_ONLY / SUPERSEDED_BY_BASE_V9_4` | do not execute |

No item in this table may be handed to Codex as an approved product contract before its domain gate closes.

## 7. Research or Test Required

- exact enhancement probabilities, pity, costs, and protection economy;
- +50 preparation and representative-session placement;
- active-storage capacity and expansion economy;
- customer count and content density within a representative session;
- Android safe-area, touch, Back, pause, process-death, and recovery behavior;
- accessibility alternatives and comprehension;
- performance and memory budgets;
- player understanding of risk, ownership, result recovery, and world feedback;
- PC input/data abstraction without expanding current UI delivery scope.

## 8. User Decision Required

Current verified open questions: `0`.

Potential important questions are not asked until the relevant domain audit proves a real conflict and compares alternatives. A verified question is asked alone through Grill Me.

## 9. History and Authority Boundaries

- Issue #79: current total-planning umbrella.
- PR #84: current canonical-recovery Draft.
- PR #81: `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`.
- Issue #60: `HISTORY_ONLY / SUPERSEDED_BY_BS-OPS-20260802-01` candidate; retained pending residual-scope check.
- PR #61/#62 active-work references: `HISTORY_ONLY`.
- Base v8, v9.1, and v9.3 active migration instructions: `HISTORY_ONLY`.
- historical PoC PASS: `REFERENCE_IMPLEMENTATION`, not latest product validation.

## 10. Synchronization Ledger

| Decision | GitHub | Sheet | Readback | Status |
|---|---|---|---|---|
| `BS-OPS-20260802-01` | this file, baseline, final report, PR #84 | `00·01·02·04·05·90·99` recovery ranges | same ID, meaning, PR, scope, and state verified | `SYNCED` |
| six approval-evidence product Decisions | this file; PR #81 detailed source | traceability repaired in `02` and preserved in `99` | classification verified | `PARTIAL_DOMAIN_SYNC / SELECTIVE_PROMOTION_PENDING` |

## 11. Current Gates

```yaml
CANONICAL_RECOVERY_GATE: PASS
DECISION_AUTHORITY_GATE: PASS
DECISION_SYNC_GATE: PASS
PLANNING_COVERAGE_GATE: NOT_STARTED
GRILL_ME_DECISION_GATE: NOT_STARTED
PLANNING_AND_REVIEW_COMPLETE_GATE: BLOCKED
CODEX_IMPLEMENTATION_GATE: BLOCKED
RUNTIME_VALIDATION_GATE: NOT_RUN
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST_GATE: NOT_RUN
```

## 12. Next Planning Bundle

`R1 Project Core and Player Promise`.

R1 compares approval evidence, protected direction, existing core documents, actual implementation, PR #81 proposals, benchmarks, player evidence, and counterevidence. Detailed values use recommended/test status; only a verified important conflict becomes one-question Grill Me.
