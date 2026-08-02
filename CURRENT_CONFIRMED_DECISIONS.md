# Blacksmith Current Confirmed Decisions

> Current operating Decision: `BS-OPS-20260802-01`
>
> Status: `APPROVED / GITHUB_RECORDED / SHEET_SYNC_PENDING`
>
> Recovery branch: `agent/blacksmith-planning-canon-recovery`
>
> Draft PR: `#84`
>
> Authority rule: this file is the root entrypoint for current Decision status. Domain documents contain the detailed contract. Google Sheet is the connected user-facing planning workspace and does not independently override GitHub canon.

## 1. Reading Rules

- `CONFIRMED_WITH_APPROVAL_EVIDENCE`: original user approval evidence is identified; the decision is current planning canon.
- `CONFIRMED_BY_LATEST_USER_DIRECTION`: explicitly confirmed in the latest user instruction or approval.
- `RECOMMENDED_DEFAULT`: GPT-selected technical or detailed numeric default that remains revisable by evidence.
- `TEST_VALUE`: a trial value requiring simulation, runtime, device, or playtest evidence.
- `PROPOSED_REVIEW_REQUIRED`: useful Draft content without sufficient current-main approval traceability.
- `USER_DECISION_REQUIRED`: a verified important planning conflict requiring one-question Grill Me.
- `RESEARCH_OR_TEST_REQUIRED`: cannot be finalized through document reasoning alone.
- `REFERENCE_IMPLEMENTATION`: actual or historical implementation fact, not automatic current planning canon.
- `HISTORY_ONLY`: superseded or obsolete authority preserved for traceability.

An implementation fact, a passing historical test, a Draft PR label, and a Sheet `CURRENT` label are not interchangeable with user approval.

## 2. Operating Decision

### `BS-OPS-20260802-01` — Planning-first canonical recovery and Grill Me boundary

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION / APPROVED`
- Approval date: `2026-08-02 KST`
- Approval source: user approved `docs/superpowers/specs/2026-08-02-planning-canon-recovery-design.md` after directing the recommended approach.
- Canonical owner: this file and `docs/operations/BS-OPS-20260802-01_BASELINE.md`.
- Design: `docs/superpowers/specs/2026-08-02-planning-canon-recovery-design.md`.
- Execution plan: `docs/superpowers/plans/2026-08-02-blacksmith-planning-canon-recovery.md`.
- Draft PR: `#84`.
- Google Sheet: `SYNC_PENDING`.

Confirmed contract:

1. Start with planning authoring and canonical recovery, not product implementation.
2. Do not modify product code, Scene, runtime data, or assets before planning and review gates close.
3. Use GPT recommendations for detailed technical values and early numbers, labeled `RECOMMENDED_DEFAULT` or `TEST_VALUE`.
4. Use Grill Me only for verified important planning decisions or genuine conflicts.
5. Ask one independent Grill Me decision at a time.
6. Do not re-ask repository facts, already-approved decisions, technical details, or ordinary test values.
7. Apply `Attack → Validate Critique → options → classification → approved minimum change → sync → regression recheck` to each major planning bundle.
8. Synchronize major approvals to GitHub canon and the linked Google Sheet with the same Decision ID.
9. Keep current Android portrait mobile scope primary; treat PC as future consideration.
10. Keep Codex product implementation blocked until total planning, adversarial final review, and user review are complete.

## 3. Confirmed Product Decisions with Approval Evidence

These decisions are current planning canon. Their implementation and validation states are tracked separately.

### `BS-ART-20260731-01` — Stylized Dark Forge

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / PLANNING_CANON`
- Decision: combine the weight of a dark forge, readable equipment, and warm firelight in stylized 2D; equipment remains the visual protagonist.
- Approval evidence: `99_변경이력` records `USER+GPT` approval at `2026-07-31 22:20 KST`; PR #81 contains the synchronized Draft canon.
- Current GitHub owner during recovery: this entrypoint.
- Detailed Draft source: PR #81 art/Modak canon; selective main promotion pending.
- Implementation: `NOT_IMPLEMENTED_AS_FINAL_PRODUCT_ART`.
- Device/human visual QA: `NOT_RUN`.

### `BS-MODAK-20260731-01` — Bright fire-spirit Modak

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / PLANNING_CANON`
- Decision: use the approved calm C-expression direction with a bright yellow/orange fire-spirit body; do not use the charcoal-shell body as the default.
- Approval evidence: `99_변경이력` records `USER+GPT` approval at `2026-07-31 22:20 KST`.
- Current GitHub owner during recovery: this entrypoint.
- Detailed Draft source: PR #81 art/Modak canon; selective main promotion pending.
- Final product asset: `NOT_CREATED`.
- Runtime/device QA: `NOT_RUN`.

### `BS-MAIN-20260801-01` — Separate main menu

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / PLANNING_CANON`
- Decision: application launch uses a separate main menu with Continue, New Game, and Settings; Continue is disabled without a valid save, and New Game warns before replacement.
- Approval evidence: `99_변경이력` records `USER+GPT` approval at `2026-08-01 04:37 KST`.
- Current GitHub owner during recovery: this entrypoint.
- Detailed Draft source: PR #81 main-menu/app-shell canon; selective main promotion pending.
- Actual current entry: `res://scenes/test/enhancement_test.tscn`.
- Implementation: `NOT_IMPLEMENTED`.

### `BS-SHELL-20260801-01` — Single BlacksmithApp shell

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / PLANNING_CANON`
- Decision: after the separate main menu, one `BlacksmithApp` keeps campaign state while hub, work, customer, and result Views coexist with storage, settings, and `ResultEnvelope` Overlays.
- Approval evidence: `99_변경이력` records `USER+GPT` approval at `2026-08-01 04:37 KST`.
- Current GitHub owner during recovery: this entrypoint.
- Detailed Draft source: PR #81 main-menu/app-shell canon; selective main promotion pending.
- Implementation: `NOT_IMPLEMENTED`.

### `BS-GRADE-20260801-02` — Five craftsmanship grades

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / PLANNING_CANON`
- Decision: `보통 → 우수 → 명품 → 걸작 → 전설`; remove `양질`; Legendary is the highest craftsmanship grade but does not automatically unlock unrelated systems.
- Supersedes: `BS-GRADE-20260801-01` and the earlier grade wording in `BS-V9-20260731-01`.
- Approval evidence: `99_변경이력` records `USER+GPT` approval at `2026-08-01 05:34 KST`.
- Current GitHub owner during recovery: this entrypoint.
- Runtime IDs, distribution, multipliers, customer scores, and migration details: `RECOMMENDED_DEFAULT / TEST_VALUE / IMPLEMENTATION_BLOCKED` until their domain review.
- Implementation: current product data still uses historical grade contracts; migration not executed.

### `BS-SAVE-20260801-01` — Save, Continue, and ResultEnvelope

- Status: `CONFIRMED_WITH_APPROVAL_EVIDENCE / PLANNING_CANON`
- Decision: one campaign, two automatic backups, no manual load slots, save-aware Continue, corruption recovery, safe New Game replacement, `AttemptIntent`, and `ResultEnvelope` preventing reroll, double application, and resource loss without a result.
- Approval evidence: `99_변경이력` records `USER+GPT` approval at `2026-08-01 09:33 KST`.
- Current GitHub owner during recovery: this entrypoint.
- Detailed Draft source: PR #81 save canon and implementation plan; selective main promotion pending.
- Implementation: `NOT_IMPLEMENTED`.
- Process-death/Android/human validation: `NOT_RUN`.

## 4. Confirmed by Latest User Direction

### Planning authoring before implementation

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION`.
- Product code, Scene, data, assets, and Codex build work remain blocked.
- Existing implementation is preserved as a read-only fact and regression baseline.

### Detailed value delegation

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION`.
- The assistant selects initial detailed values when they do not change project identity or a major player-experience commitment.
- Such values must be marked `RECOMMENDED_DEFAULT` or `TEST_VALUE` and remain revisable.

### Important planning decisions use Grill Me

- Status: `CONFIRMED_BY_LATEST_USER_DIRECTION`.
- Grill Me is required only after audit proves a meaningful decision gap or conflict.
- The question must include the conflict, current canon and implementation, protected strength, option trade-offs, evidence/counterevidence, GPT recommendation, and sync targets.

## 5. Protected Current Direction Pending Domain Revalidation

The following are protected strengths and current working direction but will be re-articulated in `R1 Project Core and Player Promise` rather than treated as implementation-complete contracts:

- one blacksmith, not staff management;
- direct forging and visible enhancement risk decisions;
- equipment as a memorable work with identity, owner, fate, and chronicle;
- equipment remains meaningful after sale or delivery through world feedback;
- no direct player combat as the current core activity;
- portrait-mobile, one-hand-readable information hierarchy;
- normal enhancement input resolves exactly one result;
- automation may reduce repetition but may not bypass identity, precision, destruction, material, sale, or ownership decisions.

Status: `PROTECTED_WORKING_DIRECTION / R1_REVALIDATION_REQUIRED`.

This revalidation must preserve approval evidence and actual implementation facts. It is not permission to discard the current direction and invent an unrelated game.

## 6. Proposed — Approval Evidence Recovery Required

The following PR #81 and Sheet records contain substantial planning work but are not automatically current canon merely because they are labeled `CURRENT`, `USER+GPT`, or `DESIGN_COMPLETE`. Each must be checked against original user approval, current project core, and cross-domain conflicts before selective promotion.

| Decision or area | Recovery status | Reason |
|---|---|---|
| `PR57-PROB` | `APPROVAL_EVIDENCE_RECOVERY_REQUIRED` | old PR/commit and pending GitHub sync |
| `PR58-ENDGAME` | `APPROVAL_EVIDENCE_RECOVERY_REQUIRED / RESEARCH_OR_TEST_REQUIRED` | endgame protection and economy materially affect risk and progression |
| `PR59-CUSTOMER` | `USER_DECISION_CANDIDATE` | customer-owned permanent destruction affects attachment, fairness, and responsibility |
| `BS-V9-20260731-02` | `PROPOSED_REVIEW_REQUIRED` | lineage and affix cap needs source evidence and mobile UX review |
| `BS-V9-20260731-03` / `BS-ENH-20260731-01` | `PROPOSED_REVIEW_REQUIRED` | +50 routes may affect Vertical Slice scope and long-term identity |
| `BS-V9-20260731-04` | `PROPOSED_REVIEW_REQUIRED` | customer eligibility and fit disclosure require domain reconciliation |
| `BS-V9-20260731-05` | `PROPOSED_REVIEW_REQUIRED` | fate states and destruction/recovery semantics cross other decisions |
| `BS-V9-20260731-06` / `BS-CUST-20260731-01` | `PROPOSED_REVIEW_REQUIRED` | customer count and representative content affect production scope |
| `BS-V9-20260731-07` | `DEFERRED_FUTURE_REVIEW` | online Hall of Masterpieces is not current implementation scope |
| `BS-SCREEN-20260731-01/02` | `WORKFLOW_REFERENCE / PROPOSED_REVIEW_REQUIRED` | useful visual-planning workflow, not product canon by itself |
| `BS-MIGRATION-20260801-01` | `PROPOSED_REVIEW_REQUIRED` | design exists; actual source schema, fixtures, and validation remain unverified |
| `BS-CUSTOMER-PIPELINE-20260801-01` | `PROPOSED_REVIEW_REQUIRED` | common pipeline and eight customers require core/scope/evidence review |
| `BS-AUTOFORGE-20260801-01` | `PROPOSED_REVIEW_REQUIRED` | boundary intent aligns with protected strengths; exact rules need review |
| `BS-VISUAL-ASSET-GOV-20260801-01` | `PROPOSED_REVIEW_REQUIRED` | governance structure is useful; final assets/licenses remain absent |
| `BS-UI-PLATFORM-20260801-01` | `PROPOSED_REVIEW_REQUIRED / RESEARCH_OR_TEST_REQUIRED` | details need Android/device/accessibility evidence |
| `BS-EQUIPMENT-LIFECYCLE-20260801-01` | `PROPOSED_REVIEW_REQUIRED / RESEARCH_OR_TEST_REQUIRED` | capacity and sales-channel details affect economy and session flow |
| `BS-VALIDATION-20260801-01` | `PROPOSED_REVIEW_REQUIRED` | evidence model is useful; current runtime lanes are not executed |

No item in this section may be handed to Codex as an approved product contract.

## 7. Research or Test Required

- exact enhancement probabilities and pity behavior;
- +50 preparation, cost, failure, protection, and session placement;
- high-end protection economy and inflation;
- active storage capacity and expansion economy;
- customer count/content density within a 15–25 minute representative session;
- Android safe-area, touch, back, pause, process-death, and recovery behavior;
- accessibility alternatives and comprehension;
- performance and memory budgets;
- actual player understanding of risk, ownership, result recovery, and world feedback;
- PC input/data abstraction, without making PC a current UI-delivery requirement.

Status: `RESEARCH_OR_TEST_REQUIRED / NOT_FINAL`.

## 8. User Decision Required

Current count: `0 VERIFIED OPEN QUESTIONS`.

Potential questions identified in the approved design are not asked until their factual conflict and impact are revalidated during the relevant domain bundle. Examples include Vertical Slice placement of +50, customer-equipment destruction protection, direct-place/world-result scope, and long-term progression center.

When a verified question is opened, only one independent Decision is asked at a time through Grill Me.

## 9. History Only and Superseded

- Issue #60 Base v6 reset: `HISTORY_ONLY_CANDIDATE / SUPERSEDED_BY_LATER_BASE_AND_USER_DIRECTION`.
- PR #61 and PR #62 active-work references: `HISTORY_ONLY`.
- PR #81 as a whole: `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT`.
- `BS-GRADE-20260801-01`: `SUPERSEDED_BY_BS-GRADE-20260801-02`.
- Earlier `BS-V9-20260731-01` grade wording: `SUPERSEDED_FOR_GRADE_DECISION`.
- Historical PoC PASS records: `REFERENCE_IMPLEMENTATION`, not current product or total-planning validation.
- Base v8, v9.1, and v9.3 active migration instructions: `HISTORY_ONLY`; current release adoption is Base v9.4.0.

Historical records are retained in Git and the Sheet change history; they must not be deleted merely because they are no longer active.

## 10. Decision Synchronization Ledger

| Decision ID | GitHub status | GitHub canonical location | Commit | Google Sheet location | Readback | Sync status |
|---|---|---|---|---|---|---|
| `BS-OPS-20260802-01` | `APPROVED / RECORDED` | `CURRENT_CONFIRMED_DECISIONS.md`; `docs/operations/BS-OPS-20260802-01_BASELINE.md` | pending exact recovery HEAD | pending | pending | `SHEET_SYNC_PENDING` |
| `BS-ART-20260731-01` | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` | this file; PR #81 source | pending | existing history/current rows require trace repair | pending | `PARTIAL_SYNC` |
| `BS-MODAK-20260731-01` | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` | this file; PR #81 source | pending | existing history/current rows require trace repair | pending | `PARTIAL_SYNC` |
| `BS-MAIN-20260801-01` | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` | this file; PR #81 source | pending | existing history/current rows require trace repair | pending | `PARTIAL_SYNC` |
| `BS-SHELL-20260801-01` | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` | this file; PR #81 source | pending | existing history/current rows require trace repair | pending | `PARTIAL_SYNC` |
| `BS-GRADE-20260801-02` | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` | this file; PR #81 source | pending | existing history/current rows require trace repair | pending | `PARTIAL_SYNC` |
| `BS-SAVE-20260801-01` | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` | this file; PR #81 source | pending | existing history/current rows require trace repair | pending | `PARTIAL_SYNC` |

`SYNCED` may be written only after exact GitHub and Sheet readback agree on Decision ID, meaning, status, canonical path, and commit SHA.

## 11. Current Gates

```yaml
CANONICAL_RECOVERY_GATE: IN_PROGRESS
DECISION_SYNC_GATE: IN_PROGRESS
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

After the recovery gate and same-ID Sheet synchronization close, begin:

```text
R1 Project Core and Player Promise
```

R1 must compare protected direction, approval evidence, current implementation, PR #81 proposals, and cross-domain risks. It may use recommended detailed defaults, but any verified important conflict is escalated through one-question Grill Me before it becomes canon.
