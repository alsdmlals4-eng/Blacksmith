# Progressive Auto-Enhancement Cap Unlock Design

## Status

- Decision: `BS-CORE-20260811-01`
- System: `AUTO_ENHANCEMENT_CAP_UNLOCK`
- Scope: planning refinement only
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`
- User direction: as low enhancement becomes routine in mid/late game, allow automatic enhancement to a player-specified target and unlock higher automatic maximums over progression.

## Goal

Reduce repetitive input in already-mastered enhancement bands without automating away Blacksmith's primary decision: whether to stop or take on the next meaningful risk.

## Existing authority preserved

The project already approved low-risk continuous enhancement in `BLACKSMITH_DECISION_LEDGER_ADDENDUM_07.md`:

- unlock after 15 manual enhancement attempts;
- initial automatic range `+1~+20`;
- `VERY_LOW / LOW` risk only;
- at most 10 attempts per request;
- stop on first failure, resource shortage, target reached, precision-enhancement wait, moderate-or-higher risk, damage, or manual protection choice;
- each attempt preserves independent result, cost, history, and telemetry;
- high-risk auto enhancement and automatic precision enhancement are rejected.

`BS-CORE-20260802-02` additionally protects enhancement as the main loop and forbids automation that removes the stop/continue decision.

This Decision refines those rules rather than introducing a parallel automation system.

## PRE_WORK_RESEARCH_PACKET

### Direct and adjacent benchmarks

- V4 official enhancement guide: ADAPT player-selected target level, batch/automatic attempts, explicit safe/destruction warnings, and ability to stop before target; REJECT industrial multi-item scale as Blacksmith's core.
- Uncharted Waters Origin July 2026 Director's Letter: ADAPT target-level auto-enhancement as mature-game QoL that removes repeated input; REJECT unrelated instant-growth simplification.
- Black Desert Mobile Ancient Anvil: ADAPT the principle that mature enhancement friction deserves systematic relief; REJECT importing a new pity gauge or guaranteed-success economy because Blacksmith already owns its failure/protection model.
- Google Play quality guidance: ADOPT intuitive, seamless UX and recognition of player progress.
- DIFFERENTIATOR: Blacksmith automation is earned through prior manual mastery and intentionally trails the player's current frontier while preserving each item's UID history and normal risk economy.

## Design choice

Three approaches were evaluated.

### A. Master first, automate the old band — ADOPT

Manual category progression opens higher auto caps one band behind the newly proven frontier. The player may choose a target at or below the unlocked cap.

### B. Global blacksmith-level cap — REJECT

Simple to explain, but it weakens current category-specific breakthrough ownership and allows mastery in one equipment family to automate another without proof.

### C. Automate to the current maximum — REJECT

Convenient, but it erases the frontier decision and conflicts with the project's enhancement-first core.

## Core rule

```text
MANUAL_MASTERY_FRONTIER
→ completed category breakthrough
→ previous 10-level band becomes eligible for auto-cap unlock
→ player chooses TARGET_ENHANCEMENT <= AUTO_CAP
→ normal attempts execute sequentially
→ any protected/manual-decision boundary returns control immediately
```

The initial legacy unlock remains:

```text
15 manual enhancement attempts
→ AUTO_CAP +20
```

For later progression, the recommended structural relationship is:

```text
category +40 breakthrough complete → AUTO_CAP +30
category +50 breakthrough complete → AUTO_CAP +40
category +60 breakthrough complete → AUTO_CAP +50
category +70 breakthrough complete → AUTO_CAP +60
...
```

This is the canonical relationship: `AUTO_CAP = highest completed category breakthrough - 10`, with the existing initial `+20` unlock retained as the early-game exception. Exact unlock presentation, counts beyond the initial 15-attempt requirement, and economy tuning may remain testable/tunable, but automation must never catch up to or exceed the current manually proven frontier.

## Ownership

- Auto cap is **category-specific**, matching the current weapon/armor/support/accessory breakthrough ownership.
- Completing a breakthrough in one category does not increase another category's auto cap.
- A category's unlocked cap is account-persistent and not tied to ownership of one specific item.
- Item UID state is never merged with category unlock state.

## Target selection

The player enters or chooses `TARGET_ENHANCEMENT`.

Validation order:

1. target must be above current item enhancement;
2. target must be at or below that category's unlocked `AUTO_CAP`;
3. required enhancement path must not cross a manual-only milestone without stopping;
4. the item must be eligible under normal enhancement rules;
5. resources must be available for the next attempt.

The UI must show current enhancement, target, unlocked cap, current risk band, expected per-attempt costs, and the next automatic-stop reason that is already knowable.

## Attempt semantics

Auto enhancement is repeated normal enhancement, not a new probability model.

Every attempt:

- uses the same success/failure distribution as manual enhancement at that state;
- consumes the same normal currency/materials;
- consumes fatigue/work opportunity exactly as the authoritative enhancement contract requires;
- emits the same item UID history/telemetry event;
- applies Great Success, Success, Maintain, downgrade, and protection logic through existing owners;
- does not create hidden success bonuses or discounts simply because it is automatic.

## Stop rules

Automation stops immediately on any of the following:

- target reached;
- resource shortage;
- a precision-enhancement milestone becomes pending;
- a category technical breakthrough becomes pending;
- the next attempt is above the unlocked auto cap;
- the next attempt is `HIGH` or `VERY_HIGH` risk;
- an item downgrade actually occurs;
- a protected-destruction outcome or equivalent large state change occurs;
- a protection choice, catalyst choice, high-tier precision choice, or another manual branch is required;
- the item becomes otherwise ineligible.

`MAINTAIN` by itself may continue if the next attempt is still eligible and the player has not reached another stop condition.

## Moderate-risk handling

The original early auto mode remains restricted to `VERY_LOW / LOW`. Midgame cap growth may expose a `MODERATE` band only when the authoritative risk curve and protection rules make it explicitly safe enough to automate without silent item destruction.

For any auto-eligible step where an unprotected destruction result is possible:

- automation may proceed only when the required valid protection mode has already been explicitly enabled for the run and sufficient protection resources exist for the next attempt;
- protection resources are consumed normally per attempt;
- if a protected-destruction result occurs, automation stops after resolving that attempt;
- if protection becomes unavailable, automation stops before the unsafe attempt.

This Decision does not permit automatic unprotected destruction.

## Manual-only frontier

The following remain manual regardless of cap:

- `HIGH / VERY_HIGH` risk attempts;
- precision-enhancement choice/result initiation;
- category technical breakthrough;
- new special/catalyst decisions that alter item identity or high-tier risk;
- any prompt that currently requires explicit permanent-risk confirmation.

The latest meaningful band must therefore remain a player decision rather than a background process.

## Small-lot interaction

`SOLDIER_01 / MAREK_OLDEN` may use unlocked auto enhancement to reduce repeated low-band input across a roughly ten-item order. This does not create batch item cloning.

For multiple UIDs:

- target can be applied as a convenience setting to selected eligible UIDs;
- each UID resolves its attempts independently;
- resources are consumed per UID/per attempt;
- one UID's failure or stop condition must not mutate another UID's history;
- UI may summarize the batch, but full underlying item events remain queryable.

Exact multi-UID execution UX remains a later implementation detail; this planning Decision only requires independent semantics.

## Protected boundaries

- `NO_AUTO_ENHANCEMENT_AT_OR_BEYOND_MANUAL_FRONTIER`
- `NO_HIGH_OR_VERY_HIGH_RISK_AUTO`
- `NO_AUTO_PRECISION_ENHANCEMENT`
- `NO_AUTO_TECHNICAL_BREAKTHROUGH`
- `NO_HIDDEN_SUCCESS_RATE_BONUS`
- `NO_RESOURCE_OR_FATIGUE_BYPASS`
- `NO_UNPROTECTED_AUTO_DESTRUCTION`
- `PER_ATTEMPT_UID_HISTORY_PRESERVED`
- `CATEGORY_SPECIFIC_AUTO_CAP`
- `PLAYER_SELECTED_TARGET_REQUIRED`
- `PRODUCT_IMPLEMENTATION_BLOCKED`
- `TASK3_IMPLEMENTATION_NOT_APPROVED`

## Adversarial review

### Attack

1. Auto cap may eventually automate the entire main loop.
2. A global cap may let one category's mastery trivialize another.
3. Automatic attempts may silently consume expensive resources or destroy a valued work.
4. Batch use may turn ten authored works into a single anonymous stack.
5. A second pity/guarantee system may accidentally be imported from benchmarks.

### Validated response

- `MUST_FIX`: cap trails manually cleared category frontier by at least one 10-level band.
- `MUST_FIX`: keep category ownership and per-attempt normal probability/cost/history.
- `MUST_FIX`: block `HIGH / VERY_HIGH`, precision enhancement, breakthroughs, and unprotected destructive attempts.
- `MUST_FIX`: batch presentation cannot merge item UIDs or their outcome histories.
- `REJECTED_CRITIQUE`: automatic handling of already-mastered low bands does not inherently violate the core if frontier choices remain manual.
- `REJECTED_IMPORT`: no Ancient Anvil/pity gauge is added by this Decision.

## Acceptance criteria

- Existing initial `15 manual attempts → AUTO_CAP +20` remains valid.
- Higher category breakthroughs unlock a category-specific auto cap one 10-level band behind the manual frontier.
- Player selects the target; target cannot exceed cap.
- All attempts use normal risk/cost/resource/fatigue/history semantics.
- Manual-only boundaries stop automation before or immediately after the relevant resolved state change.
- No product or Task3 implementation permission opens.
