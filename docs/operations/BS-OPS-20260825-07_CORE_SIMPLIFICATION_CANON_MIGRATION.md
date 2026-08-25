# BS-OPS-20260825-07 · Core Simplification Canon Migration

- Date: `2026-08-25 KST`
- Work Mode: `PLAN`
- Status: `IN_PROGRESS / PREMERGE`
- Baseline Blacksmith main: `a0a0b5026a602759a7a06463c22f23af587110ed`
- Base fresh-read at task start: `210ec78292fa12ed7563ba743b322dd36103ae4a` (`#669 reuse-first preflight`)
- Existing open PR: `#196 OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`
- Current task PR: `#207`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. User-approved Decisions

```text
BS-ENHANCE-20260825-25
- success raises exactly +1 level
- +9 -> +10 is the only Precision Enhancement
- successful +10 creates exactly one item keyword
- item keyword reuses existing CATALYST_AFFIX machine owner; no fourth affix slot

BS-DAMAGE-20260825-26
- NORMAL -> MINOR -> MAJOR -> DESTROYED
- no hidden CURRENT/MAX authority
- target <= +10 enhancement failure cannot damage item
- target >= +11 failure can damage item
- conditional damage risk must rise monotonically/non-decrease with target
- exact curve remains NOT_FINAL / USER_APPROVAL_REQUIRED
- customer purchase/handoff itself does not cause damage
- eligible delayed customer/world event may damage the same UID by one state
- exact event policy/numbers remain NOT_FINAL

BS-CHRONICLE-20260825-27
- routine enhancement attempt / N-days-ago rows are not player-facing Chronicle
- meaningful item-life events only

BS-ART-20260825-03
- ILLUSTRATED_WORKSHOP_BOOK
- USER_APPROVED_DIRECTION
- final product asset/runtime approval not granted
```

## 2. Supersession scope

Current planning authority supersedes only conflicting fields. Historical source files remain evidence.

```text
CURRENT/MAX numeric durability = superseded current authority
STABLE/STRESSED/DAMAGED/FRACTURED/CRITICAL = superseded current damage state
MAX success penalty/new-effect multiplier = not inherited
CURRENT/MAX repair + MAX overhaul formulas = superseded pending new repair model
old DAMAGE/CRITICAL ratios = historical, not new +11~+100 damage curve
+10/+20/+30/+40/+50 Precision cadence = superseded
routine dated enhancement Chronicle = superseded
```

Preserved unless separately changed:

```text
PRIMARY CORE enhancement tension + DDD
STOP/PUSH
same UID lifecycle
same-target recovery
CHECKPOINT_FLOORS [10,30,60,90]
+10 economic secured/break-even role
+11 first salient risk decision
+100 terminal
Nadia/customer purpose-constraint + delayed causal result structure
```

## 3. Research / alternatives disposition

The explicit user Decision is not reopened by benchmarking. External cases were used only as failure-mode checks.

- Diablo IV item/capstone progression: `ADAPT` ordinary progression -> distinct high-salience identity event principle; no external numeric import.
- Black Desert maximum durability complexity: `REJECT` as a new mobile damage authority; it is a useful counterexample for why CURRENT/MAX should not survive behind four labels.
- Breath of the Wild/Nintendo qualitative condition/break principle: `ADAPT` glanceable state -> terminal break principle only; no UI/art copying.

Alternatives rejected in design review:

```text
A. four labels backed by hidden CURRENT/MAX -> REJECT
B. one authoritative four-state model -> ADOPT
C. hidden damage-point meter behind four labels -> REJECT
D. keep later Precision milestones after +10 -> REJECT
```

## 4. TDD receipt

### RED

Focused contract:

```text
tests/check_core_simplification_current_contract.py
.github/workflows/validate-core-simplification.yml
```

Observed GitHub Actions RED:

```text
run = 32817866109
job = 97709703314
failure = AssertionError: missing current owner: docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
```

This is the intended RED: existing current entrypoints had not yet been migrated.

### GREEN so far

After creating the new owner and routing `AGENTS.md`, the Overlay, and Authority Index, focused workflow run `32818645646` completed `SUCCESS` on branch head `d9119d5ca32f31cfd31d5f438c3669409f4b10d8`.

Final exact-head full workflow evidence is still `PENDING` because direct onboarding/customer/Visual bindings and destination sync are being completed in the same PR.

## 5. GitHub current-owner changes

Created:

```text
docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
docs/superpowers/specs/2026-08-25-blacksmith-enhancement-damage-chronicle-simplification-design.md
docs/superpowers/specs/2026-08-25-blacksmith-damage-source-amendment-design.md
docs/superpowers/plans/2026-08-25-blacksmith-core-simplification-canon-migration.md
tests/check_core_simplification_current_contract.py
.github/workflows/validate-core-simplification.yml
```

Updated current planning surfaces:

```text
AGENTS.md
CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md
docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md
docs/planning/BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md
docs/planning/BLACKSMITH_PRECISION_CUSTOMER_LINK_CANON_20260824.md
docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_SAFE_SPEC_20260825.md
docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_BINDINGS_20260825.json
```

No protected product path is intentionally changed in this PR.

## 6. Runtime reality

Current main runtime still contains old V2 structures such as:

```text
current_durability / max_durability
FAIL_CRITICAL_DAMAGE
CURRENT/MAX destroyed-history zero axes
precision milestones [10,20,30,40,50]
```

Those remain implementation facts/historical runtime truth and are now `IMPLEMENTATION_DRIFT` relative to the new planning canon.

This PR must not fix that runtime drift because the product implementation Gate remains closed and these design gates are unresolved:

```text
DAMAGE_PROBABILITY_CURVE
MINOR_MAJOR_REPAIR_MODEL
MAJOR_ENHANCEMENT_ELIGIBILITY
CUSTOMER_EVENT_DAMAGE_POLICY
```

## 7. Reuse-first receipt

- current Blacksmith owners were inspected first: overlay, precision canon, durability canon, first-10-minutes, customer link, V2 domain/resolver/result record.
- existing `CATALYST_AFFIX` slot is reused as the item-keyword machine owner instead of creating a fourth affix slot.
- existing `VSContentResultRecord`/same-UID delayed-result concept is the future reuse seam for customer/world damage; no second customer history system is introduced.
- existing checkpoint, recovery, common enhancement material and +100 terminal structures are preserved where non-conflicting.
- Base visual/reference principles were already used to select Illustrated Workshop Book; no project-foreign skin auto-adoption.
- `base_promotion_candidates = NONE` for this task.

## 8. Five-loop adversarial review checklist

1. **hidden complexity:** four labels cannot hide CURRENT/MAX or a hidden damage meter.
2. **numeric invention:** no exact +11~+100 damage curve, repair cost, or customer-event damage percentage before user/content-owner approval.
3. **cause confusion:** customer purchase itself never means automatic damage; damage must come from an actual eligible event.
4. **history clutter:** internal ledger/day provenance is allowed, but player Chronicle does not become an attempt-by-attempt telemetry log.
5. **style/system drift:** Illustrated Workshop Book direction is approved, but pre-change values in generated style boards are not current gameplay canon.

Final loop result remains `PENDING_FINAL_EXACT_HEAD_AND_DESTINATION_READBACK`.

## 9. Destination sync requirement

Before completion:

```text
Notion Home
Enhancement/Durability/Economy detail
Visual Bible
AI/System Record
Google Sheet same-ID rows / Hub
```

must reflect Decisions25~27/Art03 without claiming runtime implementation or final balance.

## 10. Evidence ceiling

```text
PLANNING_DESIGN = USER_APPROVED
GITHUB_CURRENT_CANON = PREMERGE_IN_PROGRESS
NOTION_SYNC = PENDING
SHEET_SYNC = PENDING
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = NOT_RUN / BLOCKED
DAMAGE_CURVE_NUMBERS = NOT_FINAL
REPAIR_MODEL = NOT_DECIDED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_GEOMETRY = NOT_RUN
```
