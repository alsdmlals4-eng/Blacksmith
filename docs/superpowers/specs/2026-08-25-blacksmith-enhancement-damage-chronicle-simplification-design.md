# Blacksmith Enhancement / Damage / Chronicle Simplification Design

- Date: 2026-08-25 KST
- Classification: ARCHITECTURAL
- Work Mode: PLAN
- Baseline Blacksmith main: `a0a0b5026a602759a7a06463c22f23af587110ed`
- Base fresh-read: `210ec78292fa12ed7563ba743b322dd36103ae4a` (`#669 reuse-first preflight`)
- Existing open PR: `#196 OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- User approval basis: 2026-08-25 KST explicit approval of the simplified design presented in chat

## 1. Decision packet

This spec materializes four already user-approved directions. IDs are reserved for same-ID GitHub / Notion / Sheet synchronization after spec review.

| Decision ID | Scope | Approved direction |
|---|---|---|
| `BS-ENHANCE-20260825-25` | Enhancement / precision | Every successful enhancement increases the enhancement level by exactly `+1`. Only the `+9 -> +10` transition uses Precision Enhancement. A successful +10 Precision Enhancement creates exactly one item keyword. |
| `BS-DAMAGE-20260825-26` | Damage / destruction | Replace numeric `CURRENT/MAX` durability with one authoritative four-state damage model: `NORMAL -> MINOR -> MAJOR -> DESTROYED`. |
| `BS-CHRONICLE-20260825-27` | Item history | Stop recording/displaying routine per-attempt enhancement history such as `+7 success / N days ago`. Preserve only meaningful item-life events in the player-facing Chronicle. |
| `BS-ART-20260825-03` | Art direction | Adopt the user-selected `ILLUSTRATED_WORKSHOP_BOOK` hand-drawn workshop-note direction as the current style direction. The generated style-comparison/Main Menu board is style evidence, but its pre-change system values are not gameplay canon. |

These decisions do not open the product implementation gate.

## 2. What remains unchanged

The following existing product thesis remains current unless explicitly superseded below:

- PRIMARY CORE = enhancement tension + DDD.
- The player repeatedly decides whether to STOP or PUSH.
- Items keep stable UID identity through crafting, ownership, customer/world consequences, repair, and destruction records.
- One input resolves one enhancement attempt/result.
- Failure recovery remains item-UID + target-level scoped unless a later balance decision changes it.
- `FAIL_DOWNGRADE`, where still used, remains bounded by the current checkpoint floor and at most one level of downgrade.
- Checkpoint floors `[10, 30, 60, 90]` remain downgrade floors only.
- +10 remains the first economic secured/break-even milestone unless a later economy rebalance explicitly changes it.
- +11 remains the first major STOP/PUSH risk decision unless a later onboarding decision explicitly changes it.
- Customer/world delayed causality remains support for the same UID item.
- No tutorial-only odds, hidden success boost, scripted failure, or forced +11.

## 3. Enhancement contract

### 3.1 Single-level success only

Canonical invariant:

```text
SUCCESS_LEVEL_DELTA = +1
NO_MULTI_LEVEL_SUCCESS
```

For any successful enhancement attempt:

```text
new_level = target_level
and target_level = current_level + 1
```

No normal or special success may skip from +9 to +11, +20 to +22, or otherwise grant multiple enhancement levels from one attempt.

This refines the older wording `one input -> one result` into an explicit level-delta contract.

### 3.2 Only +9 -> +10 is Precision Enhancement

New cadence:

```text
+0 -> +1 ... +8 -> +9 = NORMAL_ENHANCEMENT
+9 -> +10             = PRECISION_ENHANCEMENT
+10 -> +11 ... +99 -> +100 = NORMAL_ENHANCEMENT
```

The old precision cadence:

```text
+10 / +20 / +30 / +40 / +50
```

is superseded by this decision. +20/+30/+40/+50 are no longer separate Precision Enhancement milestones.

### 3.3 +10 keyword generation

The successful +9 -> +10 Precision Enhancement creates exactly one item keyword.

To avoid inventing a fourth affix slot, the implementation mapping reuses the existing single `CATALYST_AFFIX` identity slot:

```text
PLAYER_FACING_NAME = ITEM_KEYWORD
MACHINE_OWNER = CATALYST_AFFIX
CARDINALITY = 0..1
CREATION_GATE = successful +9 -> +10 Precision Enhancement
```

The existing Precision Enhancement inputs may still supply the keyword-generation context:

```text
main material context
+ enhancement method
+ one catalyst
-> compatible keyword family/result
```

But they do not create extra slots, extra enhancement levels, or a guaranteed exact keyword before resolution.

After a keyword is created:

- ordinary enhancement does not create another keyword;
- +20/+30/+40/+50 do not reopen Precision Enhancement;
- exact keyword evolution/mutation after +10 is NOT decided by this spec;
- old multi-milestone catalyst-affix growth/evolution is therefore stale for new implementation until a separate decision redefines it.

### 3.4 Failure at +9 -> +10

A failed +10 Precision Enhancement attempt does not create a keyword.

If an existing failure outcome downgrades the item below +9, the item must return to +9 through ordinary one-level enhancement before it may attempt +10 Precision Enhancement again.

Recovery remains scoped to the same item UID + target +10 unless later changed.

## 4. Four-state damage authority

### 4.1 Replace CURRENT/MAX, do not hide it

New item damage authority:

```text
NORMAL
  -> MINOR
  -> MAJOR
  -> DESTROYED
```

Canonical enum proposal:

```text
DamageState.NORMAL
DamageState.MINOR
DamageState.MAJOR
DamageState.DESTROYED
```

The prior numeric contract is superseded for new planning/implementation:

```text
CURRENT_DURABILITY_PERCENT
MAX_DURABILITY_PERCENT
STABLE / STRESSED / DAMAGED / FRACTURED / CRITICAL
MAX-based success-rate penalty
MAX-based new-enhancement-effect multiplier
MAX overhaul percentage restoration
```

There must not be a hidden numeric CURRENT/MAX layer that continues to own gameplay while the UI merely shows four labels. The four states are the actual gameplay authority.

### 4.2 Damage transition

Recommended simple transition contract for spec review:

```text
one DAMAGE event = advance exactly one damage state
NORMAL    -> MINOR
MINOR     -> MAJOR
MAJOR     -> DESTROYED
DESTROYED -> DESTROYED
```

`DESTROYED` is terminal for the physical item. UID/history provenance remains archived.

To preserve the current failure-family frequency without carrying the old hidden numeric severity system, the old `FAIL_DAMAGE` and `FAIL_CRITICAL_DAMAGE` probabilities should initially be aggregated into one `FAIL_DAMAGE` family. No new probabilities are invented by the aggregation.

Derived current test-budget migration, conditional on failure:

| Band | HOLD | DOWNGRADE | DAMAGE |
|---|---:|---:|---:|
| LEARN | 100 | 0 | 0 |
| BUILD_CONFIDENCE | 90 | 0 | 10 |
| FIRST_STOP_POINT | 65 | 10 | 25 |
| TENSION | 45 | 10 | 45 |
| HIGH_STAKES | 30 | 15 | 55 |
| MASTERY | 20 | 20 | 60 |

These are `MIGRATION_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`. They are obtained only by `old DAMAGE + old CRITICAL`; they are not a new final balance approval.

### 4.3 No automatic hidden stat penalty

`MINOR` and `MAJOR` do not automatically inherit the old MAX-based success-rate penalties or new-effect multipliers.

Until the user explicitly approves a new categorical penalty model:

```text
DAMAGE_STATE_SUCCESS_PENALTY = NONE_BY_DEFAULT
DAMAGE_STATE_NEW_EFFECT_MULTIPLIER = NONE_BY_DEFAULT
```

The immediate gameplay pressure of damage is that each subsequent damaging event moves the same item closer to irreversible destruction.

This avoids silently importing the complexity that the four-state change is intended to remove.

### 4.4 Repair and overhaul are reopened

The following old formulas depend on CURRENT/MAX and are therefore stale:

- `missing = MAX - CURRENT` normal repair formula;
- `CURRENT -> MAX / MAX unchanged` semantics;
- MAX-state secured repair multipliers;
- one-life MAX overhaul `MAX + 15` / cap 60 logic;
- MAX-based repair UI and Visual GDD values.

This spec does NOT invent replacement repair economics.

Required follow-up decision before product implementation:

```text
MINOR repair result?
MAJOR repair result?
Can one repair remove more than one state?
Does MAJOR require a special overhaul action?
Repair costs/materials/fatigue by state?
Can enhancement continue while MAJOR, or must repair happen first?
```

Until that decision is made, old CURRENT/MAX repair/overhaul formulas must not be used as the implementation fallback.

## 5. Chronicle / item history contract

### 5.1 Remove routine enhancement attempt history from player-facing Chronicle

Do not create player-facing rows for routine events such as:

```text
+6 success - 25 days ago
+7 success - 24 days ago
+8 failure - 23 days ago
```

Do not show relative-age labels such as `N days ago` for ordinary enhancement attempts.

Routine attempt success/failure may still exist in test telemetry, save diagnostics, or economy simulation evidence if technically required, but that operational evidence is not the item's player-facing Chronicle canon.

### 5.2 Chronicle keeps meaningful life events

Player-facing Chronicle should preserve events that change item identity, life state, ownership, or world meaning. Initial approved event classes:

```text
ITEM_CREATED
PRECISION_KEYWORD_CREATED (+10)
DAMAGE_STATE_CHANGED (when useful to explain a lasting item event)
SIGNIFICANT_REPAIR_OR_OVERHAUL (exact repair model pending)
OWNER_OR_CUSTOMER_HANDOFF
CUSTOMER_WORLD_CONSEQUENCE
DESTROYED
MEMORIAL_OR_SUCCESSOR_LINK
```

Exact copy, ordering, and which non-terminal repair events deserve a row are presentation details; the rule is event significance, not exhaustive attempt logging.

### 5.3 Preserve causality without clutter

Internal provenance may keep stable event sequence IDs and absolute world-time/day fields when delayed customer/world resolution needs them. Those fields must not force the player-facing Chronicle to display `N days ago` for every enhancement action.

This preserves delayed-result causality while removing management-log clutter.

## 6. Onboarding impact

The first-10-minutes thesis remains:

```text
craft first item
-> learn ordinary +1 enhancement
-> reach +9
-> +9 -> +10 Precision Enhancement
-> create first item keyword
-> +10 secured/economic stop state
-> preview +11 as first major STOP/PUSH risk
-> STOP or PUSH
-> same UID consequence
```

Changes from the old onboarding:

- CURRENT introduction at +3 is removed.
- MAX/CRITICAL structural-scar tutorial at +11 is removed.
- +10 Precision Enhancement becomes explicitly the one-time keyword-creation moment.
- +11 can remain the first high-salience risk decision, but its risk copy must use the four-state damage model rather than MAX structural-scar language.

## 7. Visual/UI impact

### 7.1 Current art direction

The user selected style C from the three style explorations:

```text
ILLUSTRATED_WORKSHOP_BOOK
hand-drawn workshop notebook
paper / leather / iron / wood material cues
warm workshop atmosphere
modern readable interaction hierarchy
```

This supersedes `ART_STYLE_REWORK_REQUIRED` as the direction-selection state, but not as final runtime asset approval. Proposed state after sync:

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

### 7.2 Existing/new Visual GDD interpretation

The generated Illustrated Workshop Book board is approved for style direction, but system labels/values shown before this mechanic change are stale where they contain:

- CURRENT/MAX values;
- five structural damage bands;
- MAX penalty table;
- routine dated enhancement history;
- any precision cadence other than +9 -> +10.

The board must therefore be marked:

```text
STYLE_DIRECTION_APPROVED
SYSTEM_CONTENT_REQUIRES_REGENERATION
```

Representative regeneration after mechanic canon sync should cover at minimum:

```text
Main Menu
Enhancement Main (+1 only)
+9 -> +10 Precision Keyword screen
Four-state Damage / Repair decision surface
Item Chronicle with event-only history
```

Do not bulk-regenerate all assets before these representative screens are reviewed.

## 8. Existing canon conflicts and supersession map

| Existing owner | Conflict | New disposition |
|---|---|---|
| `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md` sections 2-5, 7, 9 | CURRENT/MAX, CRITICAL, MAX penalties, repair formulas, failure family | PARTIALLY_SUPERSEDED; preserve recovery/checkpoint/success/economy pieces that do not require CURRENT/MAX |
| `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` | entire numeric dual-durability authority | SUPERSEDED_FOR_NEW_PLANNING; historical evidence retained |
| `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` | durability portions | PARTIALLY_SUPERSEDED; checkpoint floor portions retained |
| `BLACKSMITH_MAX_OVERHAUL_CANON_20260824.md` | MAX restoration semantics | SUPERSEDED_PENDING_NEW_REPAIR_DECISION |
| current repair canon | missing-percent formulas and CURRENT->MAX | SUPERSEDED_PENDING_NEW_REPAIR_DECISION |
| `BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md` | +10/+20/+30/+40/+50 precision cadence and repeated catalyst evolution | PARTIALLY_SUPERSEDED; material/method/catalyst responsibility may be reused at +10 only |
| `BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md` | CURRENT/MAX onboarding and +11 structural scar copy | PARTIALLY_SUPERSEDED; core pacing/STOP-PUSH structure retained |
| approved Visual GDD 06/08 and related implementation-safe bindings | CURRENT/MAX visual semantics | SYSTEM_SEMANTICS_STALE; layout may remain reference only |
| player-facing item history visuals | routine dated enhancement rows | SUPERSEDED by event-only Chronicle |

Historical source files should not be rewritten to pretend they never existed. Current authority entrypoints must explicitly route to the new decisions and mark old owners as superseded/partial.

## 9. Alternatives considered

### Alternative A - Keep numeric CURRENT/MAX internally, show only four labels

Advantages:
- minimal code migration;
- old repair/balance formulas keep working.

Rejected because:
- violates the approved simplification goal;
- creates hidden complexity and future UI/data drift;
- the same old system would remain authoritative under a cosmetic wrapper.

Disposition: `REJECT`.

### Alternative B - One authoritative four-state model + one-time +10 keyword + event-only Chronicle

Advantages:
- directly matches user-approved direction;
- reduces mobile information load;
- removes duplicated durability semantics;
- preserves STOP/PUSH and UID identity;
- simpler to explain, test, and draw in Illustrated Workshop Book style.

Cost:
- repair/overhaul/economy formulas must be redesigned;
- old runtime model cannot be treated as current implementation truth.

Disposition: `ADOPT`.

### Alternative C - Four visible states backed by a hidden damage-point meter

Advantages:
- easier balance tuning than a pure state machine.

Rejected because:
- reintroduces a second authority;
- risks thresholds and hidden points becoming the real game while labels become decoration;
- contradicts the explicit removal of CURRENT/MAX-style numeric durability.

Disposition: `REJECT`.

### Alternative D - Keep five Precision Enhancement milestones but generate the keyword only at +10

Advantages:
- preserves old catalyst evolution content.

Rejected because:
- user approved `+9 -> +10 only` as the Precision Enhancement moment;
- later special screens would dilute the identity of the first keyword event.

Disposition: `REJECT`.

## 10. Benchmark / primary-source review

Research does not override explicit user approval. It is used to test failure modes.

### Diablo IV - Masterworking / item journey

Official Blizzard material shows ordinary item improvement separated from a distinct high-salience special/capstone outcome. Earlier Masterworking also used regular tiers with periodic larger affix upgrades.

Disposition: `ADAPT` only the principle `ordinary progression -> distinct identity/prestige event`; do not copy ranks, percentages, affix values, or economy.

Sources checked 2026-08-25:
- Blizzard News, "Sanctuary Ignites with Itemization & Systems Changes"
- Blizzard News, Season 4 / Masterworking material

### Black Desert - enhancement and maximum durability

Official Pearl Abyss beginner guidance confirms failed enhancement can reduce maximum durability and requires separate restoration.

Disposition: `REJECT` as the new Blacksmith durability model. This is a useful counterexample showing exactly the dual repair/max-durability complexity the user wants removed from Blacksmith's mobile decision surface.

Source checked 2026-08-25:
- Black Desert NA/EU GM Notes, new-adventurer enhancement/repair guidance.

### The Legend of Zelda: Breath of the Wild - condition warning and breakage

Nintendo's official Explorer's Guide communicates weapon condition at a glance with visible qualitative signals (new / badly damaged) and terminal breakage rather than making a durability spreadsheet the primary player decision.

Disposition: `ADAPT` the principle `glanceable condition signal -> clear terminal break`; do not copy Zelda's replacement-heavy weapon economy.

Source checked 2026-08-25:
- Nintendo, Breath of the Wild Explorer's Guide.

## 11. Five full adversarial loops

### Loop 1 - fourth-slot creep

Attack: "keyword" could accidentally create a fourth affix slot on top of `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`.

Refinement: human-facing item keyword reuses the existing single `CATALYST_AFFIX` identity slot. No fourth slot.

Result: `PASS_FOR_SPEC_REVIEW`.

### Loop 2 - fake simplification

Attack: UI could show NORMAL/MINOR/MAJOR while hidden CURRENT/MAX still determines outcomes.

Refinement: numeric CURRENT/MAX authority is explicitly superseded. Four-state enum is the gameplay owner.

Result: `PASS_FOR_SPEC_REVIEW`.

### Loop 3 - repair fallback resurrects old system

Attack: implementation could keep old percentage repair because new repair costs are not decided.

Refinement: old repair/overhaul formulas are explicitly stale and cannot be fallback. Repair becomes a separate blocking follow-up decision.

Result: `PASS_FOR_SPEC_REVIEW`.

### Loop 4 - Chronicle simplification breaks delayed causality

Attack: removing enhancement logs could remove data needed to resolve delayed customer/world results.

Refinement: remove routine rows only from player-facing Chronicle. Internal stable event IDs/time provenance may remain where causality requires them.

Result: `PASS_FOR_SPEC_REVIEW`.

### Loop 5 - balance collapses after CRITICAL/MAX removal

Attack: removing MAX penalties/critical severity may make late enhancement too safe.

Refinement: aggregate old DAMAGE+CRITICAL frequency only as an initial migration test budget, but do not invent replacement state penalties. Require simulation + Human test before final balance.

Result: `PASS_WITH_VALIDATION_GATE`.

### Loop 6 - old Visual GDD becomes false canon

Attack: approved boards still visibly show CURRENT/MAX, five damage bands, dated logs, and could be mistaken for implementation requirements.

Refinement: preserve layout/style evidence but mark system content stale; regenerate representative screens only after this mechanic canon is synchronized.

Result: `PASS_FOR_SPEC_REVIEW`.

## 12. Validation and evidence ceiling

After implementation planning, required automated checks must prove at least:

```text
all enhancement targets = current + 1
only target +10 from current +9 routes to Precision Enhancement
successful +10 creates exactly one keyword in existing single keyword/affix owner
other levels cannot create another keyword
DamageState has exactly NORMAL/MINOR/MAJOR/DESTROYED
no CURRENT/MAX fields remain in current gameplay authority or new UI binding
DAMAGE advances one state; DESTROYED is terminal
old MAX success/effect penalty cannot silently execute
player-facing Chronicle excludes routine per-attempt dated rows
meaningful item-life events remain representable
```

Evidence ceiling remains:

- new repair economics: `NOT_DECIDED`;
- replacement balance after four-state migration: `TEST_BUDGET_ONLY`;
- Human/player validation: `NOT_RUN`;
- Android readability/accessibility: `NOT_RUN`;
- local Godot Editor session: `NOT_RUN`;
- final product asset/runtime art validation: `NOT_RUN`;
- Notion client visual geometry: `NOT_RUN`.

## 13. Next sequence after written-spec approval

```text
1. Write implementation plan with TDD migration order.
2. Create new current authority decisions and supersession map.
3. RED contracts for enhancement cadence / keyword / damage enum / Chronicle filtering.
4. Migrate structured/runtime model only after planning gate authorizes product implementation work; until then planning/document surfaces only.
5. Redesign repair/overhaul state transitions and economy as a separate user decision before runtime repair migration.
6. Sync Human Home + Enhancement/Durability detail + Visual Bible.
7. Mirror the same Decision IDs to Google Sheet compatibility surface.
8. Regenerate representative Illustrated Workshop Book screens with corrected system semantics.
9. Human review before bulk visual production or final balance claims.
```
