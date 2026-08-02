# BS-OPS-20260802-01 Baseline Recovery Record

- Decision ID: `BS-OPS-20260802-01`
- Decision status: `APPROVED / SYNC_IN_PROGRESS`
- Work Mode: `TOTAL_PLANNING`
- Implementation authority: `PLANNING_AND_DOCUMENTATION_ONLY`
- Recorded at: `2026-08-02 KST`

## Repository and Branch

| Item | Value | Status |
|---|---|---|
| Repository | `alsdmlals4-eng/Blacksmith` | `CONFIRMED` |
| Recovery base | `main@ac120fb146cea29bb5f8876682809f76779d86ad` | `CONFIRMED` |
| Recovery branch | `agent/blacksmith-planning-canon-recovery` | `CONFIRMED` |
| Draft PR | `#84` | `CONFIRMED` |
| Approved design commit | `8b7956e1961e711d70a9f3df5f5cc48c055101a8` | `CONFIRMED` |
| Execution-plan commit | `f719890547c09bf78a09cea6ea8b1bce8497caee` | `CONFIRMED` |
| PR #81 | `docs/blacksmith-v9-planning-audit@12c336f41f6bbbba57c31395db996481086850de` | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |

The recovery branch was created directly from the current main commit. Before this record, the branch contained only the approved design and execution plan. No product file had changed.

## Base Release and Project Adoption

| Item | Value | Status |
|---|---|---|
| Current released Base adopted by project | `9.4.0` | `CONFIRMED` |
| Base release commit | `a728712cb776ec98f4875914a580fcf7d0156593` | `CONFIRMED` |
| Base evidence commit | `ef1fba11167e4da0b298123b0c85ebd268191a42` | `CONFIRMED` |
| Blacksmith project adoption PR | `#83`, merged into current main | `CONFIRMED` |
| Canonical project adapter | `skills/PROJECT_BASE_ADAPTER.json` | `PRESENT / NEEDS_CORRECTION` |
| GDD Sheet adapter binding | role exists, URL missing, `sync_status=NOT_CONFIGURED` | `CONFLICTED` |
| Protected baseline in adapter | `500a5a7960146ef229ae172cf9e127306d23f073` | `STALE_REFERENCE` |
| Generated compatibility views | generator execution unavailable in this connector-only session | `BLOCKED_UNVERIFIED` |

Released Base adoption and current Blacksmith operating readiness are separate facts. Base v9.4 files existing in the repository do not mean current planning entrypoints, Sheet binding, product runtime, or human/device validation are complete.

## Current Product Reality

| Surface | Current fact | Status |
|---|---|---|
| Product engine | Godot `4.7`, GDScript | `CONFIRMED` |
| Primary platform | Android portrait mobile | `CONFIRMED` |
| PC | future compatibility consideration only | `FUTURE_PLATFORM_CONSIDERATION` |
| Current run entry | `res://scenes/test/enhancement_test.tscn` | `CONFIRMED / CANON_IMPLEMENTATION_GAP` |
| Approved product entry | separate main menu, then single `BlacksmithApp` shell | `APPROVED_PLANNING / NOT_IMPLEMENTED` |
| Save/continue/result recovery | approved planning contract | `NOT_IMPLEMENTED / NOT_VALIDATED` |
| Existing PoC code and tests | historical implementation baseline | `REFERENCE_IMPLEMENTATION` |
| Latest total-planning runtime validation | none | `NOT_RUN` |
| Android device validation | none | `NOT_RUN` |
| Accessibility human review | none | `NOT_RUN` |
| Performance profile | none | `NOT_RUN` |
| Current external human playtest | none | `NOT_RUN` |

Historical PoC automation, imports, scene smoke tests, and model tests may be used as regression evidence for the exact code-bearing commits where they ran. They are not evidence that the latest planning direction, separate main, app shell, save recovery, Android device behavior, accessibility, performance, or player experience has passed.

## Current Canonical Sources

### Existing current candidates

- Project repository and actual product files: implementation fact source.
- `skills/PROJECT_BASE_ADAPTER.json`: canonical Base adapter source, but its Sheet binding and protected baseline are stale.
- `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`: existing integrated game-planning source, subject to selective planning revalidation.
- Explicit approval records in Issue #79, PR #81 discussion/history, and Google Sheet `99_변경이력`: approval evidence sources.
- Google Sheet: `USER_FACING_GDD_WORKSPACE`, not the authority that may independently overrule GitHub canon.

### Missing or stale authority

- Root `CURRENT_CONFIRMED_DECISIONS.md`: `MISSING_CANON` on current main.
- `[기획서]/00_프로젝트_허브/START_HERE.md`: routes to Issue #34, PR #35, and an obsolete branch/head.
- `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`: dated `2026-07-24`, routes to PR #35 and historical PoC work.
- `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`: mixes historical PoC PASS with current project gates.
- Documentation and Roadmap ownership: current recovery, PR #81 reference role, and total-planning sequence are not yet represented consistently.

## Open Issue and PR Authority

| Surface | Current purpose | Recovery classification |
|---|---|---|
| Issue #79 | planning audit and Vertical Slice v9 umbrella | `ACTIVE_PLANNING_UMBRELLA / NEEDS_V9_4_UPDATE` |
| Issue #60 | Base v6 reset and full re-derivation | `HISTORY_ONLY_CANDIDATE / SUPERSEDED_BY_LATER_BASE_AND_USER_DIRECTION` |
| PR #81 | 181-commit, 88-file planning Draft based on old main | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |
| PR #84 | approved planning-canon recovery design and execution | `ACTIVE_RECOVERY_PR` |

PR #81 contains valuable planning and approval evidence. Its size, old base, stale Base v9.3 assumptions, intermediate-head Sheet records, and divergence from current main make whole-PR merging unsafe. It must be mined selectively after the current authority and approval-evidence ledger are restored.

## Google Sheet State

- Spreadsheet: `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`
- Role: `USER_FACING_GDD_WORKSPACE`
- Structure: 25 tabs, including project hub, work order, current decisions, audit, domain planning, production, Base candidates, and history.

### Confirmed operating drift

1. `00_프로젝트_허브` still reports `Base v9.3 migration target / adapter v9.1 drift` and `SYNCED_TO_DRAFT_PR81`.
2. `01_작업순서` routes active work to PR #62, PR #61, and a v9.3 migration.
3. `02_현재_확정결정` mixes current decisions, superseded decisions, Draft proposals, incomplete traceability, and one malformed row without a Decision ID.
4. PR #57, #58, and #59 rows remain `CURRENT` with `SHEET_UPDATE_PENDING_GITHUB` against an old commit.
5. Many later `CURRENT` rows have no canonical path, final-main commit, or readback status.
6. `05_GDD_요약` and `90_본제작_출시_사업` retain v9.3 and PR #81 as active operating direction.
7. `99_변경이력` preserves useful approval history but also contains many PR #81 intermediate heads marked for final-head recheck.

No formula error was observed in the bounded operating ranges read for this recovery. This does not validate every cell in all 25 tabs.

## Protected Decisions and Strengths

### Explicit approval-evidence promotion candidates

The following may be listed as current confirmed product decisions after their original evidence and GitHub owner paths are read back:

- `BS-ART-20260731-01`: stylized dark forge visual direction.
- `BS-MODAK-20260731-01`: bright fire-spirit Modak with the approved calm expression direction.
- `BS-MAIN-20260801-01`: separate main menu.
- `BS-SHELL-20260801-01`: single `BlacksmithApp` with View/Overlay division.
- `BS-GRADE-20260801-02`: five craftsmanship grades — 보통, 우수, 명품, 걸작, 전설.
- `BS-SAVE-20260801-01`: single campaign, two automatic backups, `SaveStatus`, `AttemptIntent`, and `ResultEnvelope` recovery contract.

These are planning decisions, not implementation or validation claims.

### Protected strengths

| Strength ID | Protected value | Regression boundary |
|---|---|---|
| `BS-STR-CORE-01` | one blacksmith directly creates one meaningful item and chooses whether to stop or challenge risk | do not turn the game into staff management, direct combat, or production queue management |
| `BS-STR-LIFE-01` | item UID, ownership, fate, and chronicle survive sale or delivery | do not reduce equipment to disposable inventory with erased history |
| `BS-STR-ENH-01` | one normal-enhancement input produces one result, without reroll or double application | screen transition, recovery, or automation may not change the decided result |
| `BS-STR-ID-01` | craftsmanship grade plus one lineage and at most two secondary affixes keeps each work memorable | do not introduce mobile-unreadable slot or property explosion |
| `BS-STR-UX-01` | portrait mobile, equipment-first presentation, disclosed material risk information | do not hide core probabilities or use color as the only information channel |
| `BS-STR-ART-01` | stylized dark forge with warm local firelight and bright Modak | do not regress to generic bright casual or charcoal-shell Modak |
| `BS-STR-VALID-01` | unexecuted validation is never reported as PASS | do not extend historical PoC evidence to latest product, Android, or human validation |

## Confirmed Conflicts

### `BS-OPS-F01` — Stale cold-start entrypoints

```yaml
attack: A new worker follows current repository entry documents and resumes obsolete PR #35 work.
factual_basis: START_HERE and ACTIVE_CONTEXT identify PR #35, Issue #34, a historical branch, and historical validation as current.
counterevidence: Current main is ac120fb1, active recovery is PR #84, and the user explicitly directed planning-first recovery.
impact: wrong branch, duplicate work, false current-state claims, and possible product work before planning completion.
verdict: MUST_FIX
classification: AUTO_FIX_ELIGIBLE
```

### `BS-OPS-F02` — Mixed Base authority

```yaml
attack: Workers choose v8, v9.1, v9.3, or v9.4 depending on which active document they encounter.
factual_basis: repository adapter carries v9.4 release data, while the Sheet and PR #81 planning still route through v9.3 and older adapter language.
counterevidence: current main contains merged Base v9.4 adoption.
impact: stale generation, wrong validation contract, duplicate migration work, and unreliable cold start.
verdict: MUST_FIX
classification: AUTO_FIX_ELIGIBLE
```

### `BS-OPS-F03` — PR #81 is valuable but unsafe as a merge unit

```yaml
attack: Valuable content is treated as evidence that the entire Draft can be merged.
factual_basis: PR #81 has 181 commits, 88 changed files, an old base, stale Base assumptions, and many Sheet references to intermediate heads.
counterevidence: explicit approvals and useful planning documents exist within it.
impact: merge conflict, stale authority restoration, accidental promotion of unapproved proposals, and high review cost.
verdict: MUST_FIX
classification: AUTO_FIX_ELIGIBLE
```

### `BS-OPS-F04` — Missing stable current-decision entrypoint

```yaml
attack: Current decisions are inferred from PR descriptions or Sheet rows rather than one GitHub authority entrypoint.
factual_basis: current main lacks root CURRENT_CONFIRMED_DECISIONS.md.
counterevidence: PR #81 contains a Draft decision set, but it is not safe current-main authority.
impact: conflicting approvals, repeated questions, and inability to perform reliable decision sync.
verdict: MUST_FIX
classification: AUTO_FIX_ELIGIBLE
```

### `BS-OPS-F05` — Sheet current ledger is not traceable enough

```yaml
attack: CURRENT labels are trusted despite missing canonical path, current commit, or approval evidence.
factual_basis: multiple current rows lack traceability; old PR57/58/59 rows remain pending; one row lacks a Decision ID.
counterevidence: 99_변경이력 preserves useful historical evidence for several decisions.
impact: false approval, accidental product-scope expansion, and cross-source drift.
verdict: MUST_FIX
classification: AUTO_FIX_ELIGIBLE
```

### `BS-OPS-F06` — Duplicate active Issue and PR authority

```yaml
attack: Issue #60, Issue #79, PR #81, and stale hub documents all appear able to direct the next work.
factual_basis: each contains a different Base version, planning sequence, or current-state claim.
counterevidence: the latest user direction and PR #84 define the active recovery sequence.
impact: duplicate work and incompatible planning baselines.
verdict: MUST_FIX
classification: AUTO_FIX_ELIGIBLE
```

### `BS-OPS-F07` — Approval-evidence inflation

```yaml
attack: USER_APPROVED or CURRENT in a Draft/Sheet is accepted as sufficient original user evidence.
factual_basis: later PR #81 decisions are widely labeled current, while the approval source is not consistently linked in the current-main authority.
counterevidence: original approval evidence is explicit for art, Modak, main menu, shell, grade, and save decisions.
impact: the assistant would silently decide important planning on the user's behalf.
verdict: MUST_FIX
classification: AUTO_FIX_ELIGIBLE
```

### `BS-OPS-F08` — Approved product entry conflicts with actual entry

```yaml
attack: Planning claims a separate main and shell while the actual app starts in a test scene.
factual_basis: project.godot points to res://scenes/test/enhancement_test.tscn.
counterevidence: the current stage is planning-only, so nonimplementation is not itself a planning failure.
impact: implementation handoff would be misleading if the gap is not explicit.
verdict: SHOULD_FIX
classification: DOCUMENT_GAP_ONLY_NOW / PRODUCT_FIX_BLOCKED
```

### `BS-OPS-F09` — False-pass operating health semantics

```yaml
attack: PASS_WITH_NOT_RUN_GATES is interpreted as an operating or product pass.
factual_basis: docs/PROJECT_OPERATING_HEALTH.json reports all critical gates NOT_RUN while using that integrity verdict.
counterevidence: the individual gate values are correctly NOT_RUN.
impact: false completion and premature Codex or production work.
verdict: MUST_FIX
classification: AUTO_FIX_ELIGIBLE
```

### `BS-OPS-F10` — Current planning and detailed numbers are not separated consistently

```yaml
attack: Draft capacity, probability, duration, spacing, and economic values become permanent product commitments because they appear in a CURRENT row.
factual_basis: Sheet contains numerous detailed Draft values without a uniform TEST_VALUE or RECOMMENDED_DEFAULT classification.
counterevidence: the latest user direction explicitly delegates detailed defaults while reserving important planning conflicts for Grill Me.
impact: overcommitment and unnecessary user questioning.
verdict: SHOULD_FIX
classification: AUTO_FIX_ELIGIBLE_FOR_LABELING / RESEARCH_OR_TEST_REQUIRED_FOR_FINAL_VALUES
```

## Grill Me Boundary

No operational conflict above requires a user preference decision. They concern stale paths, traceability, evidence status, and authority. They will be repaired without Grill Me.

A future finding becomes `USER_DECISION_REQUIRED` only when evidence confirms a real choice that changes at least one of:

- project core, player fantasy, or sharp fun;
- incompatible major system or UX principles;
- Vertical Slice or production scope;
- major failure, destruction, recovery, or reward meaning;
- replacement of an approved Decision;
- alternatives with materially different player experience or production cost.

Detailed technical values and trial balance values remain `RECOMMENDED_DEFAULT` or `TEST_VALUE` unless their effect crosses that boundary.

## Validation Evidence

| Layer | Status | Evidence or reason |
|---|---|---|
| Approved recovery design | `PASS` | user approved the design after commit `8b7956e1` |
| Written execution plan | `PASS` | committed at `f7198905`, self-reviewed for scope and placeholders |
| Current-main/branch relationship | `PASS` | branch is ahead of current main with no behind commits at the recorded checkpoint |
| Product protected-path diff | `PASS_AT_CHECKPOINT` | only design and plan documents differed before this baseline |
| GitHub/Sheet live read | `PASS_FOR_BOUNDED_AUDIT` | target operating surfaces were read and conflicts above were confirmed |
| Local Python validators | `NOT_RUN` | no local checkout execution surface in this connector-only session |
| Godot import/runtime | `NOT_RUN` | outside planning-document authority and not executed |
| Android device | `NOT_RUN` | no device execution |
| Accessibility human review | `NOT_RUN` | no human session |
| Performance | `NOT_RUN` | no profiling |
| External playtest | `NOT_RUN` | no current planning playtest |

`PASS_AT_CHECKPOINT` and `PASS_FOR_BOUNDED_AUDIT` are restricted to their named evidence and do not imply product readiness.

## Prohibited Changes

Until the user declares planning complete, adversarial final review is finished, and user review is complete:

- do not modify `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot`;
- do not implement the separate main, app shell, save system, migration, customer pipeline, auto-enhancement, UI theme, or final assets;
- do not create a Codex product implementation issue or claim Codex readiness;
- do not promote unverified PR #81 proposals to confirmed canon;
- do not report runtime, Android, accessibility, performance, or human validation as passed;
- do not expand PC into a simultaneous delivery platform.

## Rollback

- All changes remain on `agent/blacksmith-planning-canon-recovery` and Draft PR #84.
- Current main remains the rollback point: `ac120fb146cea29bb5f8876682809f76779d86ad`.
- PR #81 remains available as historical and planning evidence.
- Sheet updates must be reversible by the recorded Decision ID and exact changed ranges.
- No product files are in scope, so this recovery can be abandoned without altering the playable baseline.

## Next Gate

1. Create the root current-decision authority and classify evidence-backed, proposed, research-required, and historical decisions.
2. Repair cold-start documents and fail-closed gates.
3. Correct Base adapter and operating health without hand-editing generated compatibility views.
4. Synchronize `BS-OPS-20260802-01` to the Google Sheet and read it back.
5. Reconcile Issue #60/#79 and PR #81/#84 authority.
6. Run the final adversarial and exact-HEAD recovery review.
7. Begin `R1 Project Core and Player Promise`; do not begin product implementation.
