# Blacksmith Session Handoff · Core Simplification

- Decision ID: `BS-OPS-20260825-08`
- Date: `2026-08-25 KST`, current update `2026-08-26 KST`
- Status: `CURRENT_SESSION_HANDOFF / GPT_WORK_TRANSFER / POSTMERGE_PLANNING_ONLY`
- Historical checkpoints: `PR #207 = MERGED_TO_MAIN / 5c29af1...`; `PR #208 = MERGED / R5_4_ROUTER`; `PR #209 = MERGED / BS-DAMAGE-20260826-28`; `PR #210 = MERGED / BS-REPAIR-20260826-29`; `PR #211 = MERGED / BS-DAMAGE-20260826-30 + BS-ART-20260826-04`
- `CURRENT_PLANNING_WORK = REPAIR_ECONOMY_REBASE + DURABILITY_ECONOMY_SENSITIVITY`
- `GPT_WORK_PRIMARY_EXECUTION_SURFACE = GPT_WORK`
- `GPT_WORK_MEMORY_MODE = DEFAULT_MEMORY`
- `IMAGE_GOAL_QUEUE = READY_FOR_GPT_WORK`
- Pre-existing protected PR: `#196 / OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 0. GPT Work transfer · 2026-08-26

User directive: future Blacksmith work moves from the current chat to **ChatGPT Work**. This changes the working surface, not project authority.

```text
GPT_WORK_PRIMARY_EXECUTION_SURFACE = GPT_WORK
GPT_WORK_MEMORY_MODE = DEFAULT_MEMORY
GPT_WORK_POLICY_OWNER = BASE_CURRENT
PROJECT_CANON_AUTHORITY = UNCHANGED
MEMORY_IS_NOT_CURRENT_TRUTH = TRUE
FRESH_READ_REQUIRED
```

Base current handoff checkpoint at transfer start: `06669fe9c6a3ccd6f3b0d19c5757540bfdcc0623` (`docs: default ChatGPT project memory for Work and reuse (#724)`). Blacksmith transfer baseline main: `d17a3e0f45337c8f3031c61780729bd7590d5d58`. These SHAs are historical checkpoints; Work must fresh-read live heads instead of treating them as permanent pointers.

The Base policy owns the generic Work/Default-memory rule. Blacksmith does not fork that policy. Project-specific Work startup remains:

```text
1. fresh-read Base current main + relevant owner docs
2. fresh-read Blacksmith AGENTS.md + this handoff + default branch/latest commit/open PRs
3. fresh-read Notion Human Home / Core Detail / Visual Bible / Production Handoff / AI System Record
4. fresh-read Google Sheet only as migration compatibility evidence
5. report GitHub/Notion/Sheet authority drift before mutation
6. preserve PR #196 as OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER
7. resume only the currently selected approved/queued work
```

### Image-work transfer state

The 2026-08-26 consumer-first image audit completed **without generating a new image**. The eight existing Visual GDD images remain historical information-architecture references, not product assets.

```text
HISTORICAL_APPROVED_VISUAL_GDD = 8
PRODUCT_IMAGE_ASSET_APPROVAL = 0
IMPLEMENTATION_READY_IMAGE_ASSET = 0
ACTUAL_RUNTIME_IMAGE_CONSUMPTION = 0
RUNTIME_VERIFIED_IMAGE_ASSET = 0
IMAGE_GENERATION = NOT_RUN
IMAGE_GOAL_QUEUE = READY_FOR_GPT_WORK
```

Current concrete runtime/planned consumers found in the repository:

- `scenes/vertical_slice/main_menu.tscn` — actual startup Main Menu surface.
- `scenes/vertical_slice/screens/vs_workshop_screen.tscn` — Workshop surface.
- portrait target: `720 × 1280` viewport.

Existing-solution result:

- Reuse current `ILLUSTRATED_WORKSHOP_BOOK` style canon as-is.
- Adapt old Visual GDDs only for layout/information hierarchy/feedback structure.
- Keep Godot native `Control`/`Button`/`Panel`/`ProgressBar` for UI structure instead of redrawing those controls as raster images.
- No current Blacksmith production PNG/JPG/WebP was found in the repository audit; GUT plugin SVGs are not Blacksmith product art.
- `docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_BINDINGS_20260825.json` is stale implementation-planning evidence where it still encodes Decision26-era categorical/no-numeric durability semantics. Do not use those fields over Decision29/30.
- Google Sheet `71_이미지기획_생성목록` and `72_이미지검수_승인로그` are migration/history surfaces. Old `BS-IMG-001~005` queue labels do not become the current production queue.

### Remaining Image Goal queue

| Order | Goal | Priority | Current state | Production intent |
| ---: | --- | --- | --- | --- |
| 1 | `IMG-01 · Workpiece Hero + lifecycle/damage state family` | P0 | `READY_FOR_USER_GOAL_APPROVAL / NOT_GENERATED` | Shared workpiece hero for Workshop, later enhancement/repair/inventory/customer-result/Chronicle. Required family: NORMAL/MINOR/MAJOR/DESTROYED. |
| 2 | `IMG-02 · Workshop Environment Layer Pack` | P0 | `READY_FOR_USER_GOAL_APPROVAL / NOT_GENERATED` | Reusable 9:16 workshop room base + workbench/anvil foreground + forge/firebox element for Main Menu and Workshop. |
| 3 | `IMG-03 · Functional Workshop Mark/Icon Family` | P1 | `DEFER_UNTIL_EXACT_CONSUMER_SLOT` | Enhancement/durability/repair/danger/Chronicle marks after exact UI nodes exist. |
| 4 | `IMG-04 · +9→+10 Precision Asset Pack` | P1 | `DEFER / CANON_AND_CONSUMER_DETAIL_REQUIRED` | Catalyst/keyword/focus assets only after exact current precision consumer/resource IDs exist. |
| 5 | `IMG-05 · Release Identity Pack` | P3 | `DEFER_RELEASE / PLATFORM_SPEC_RECHECK_REQUIRED` | App/store identity only after runtime visual lock; real runtime screenshots, not generated fake screenshots. |

The first future image action is **not automatic generation**. If the user explicitly selects `IMG-01` for production in Work, the first candidate is:

```text
NORMAL_WORKPIECE_HERO_MASTER
→ text brief against current item/style canon
→ Image Conversation Approval Gate
→ generate exactly one NORMAL master
→ review identity/readability
→ only then derive MINOR → MAJOR → DESTROYED by identity-preserving edits
```

Do not treat this transfer message as approval to generate `NORMAL_WORKPIECE_HERO_MASTER`, the remaining variants, or any other image.

### Codex integration handoff order after image approval

```text
CODEX-IMG-01 Workpiece State Integration
→ CODEX-IMG-02 Workshop Environment Integration
→ CODEX-IMG-03 Functional Icon Integration
→ CODEX-IMG-04 Precision Asset Integration
→ CODEX-IMG-05 Distribution Asset Packaging
```

Codex integration does not bypass the current product implementation gate. Approved images may be prepared/registered, but protected product paths remain blocked until the current planning-complete declaration opens implementation.

## 1. Cold-start rule

Do not resume from chat memory alone. Before mutation:

```text
1. fresh-read Base current main and relevant owner docs
2. fresh-read Blacksmith default branch / latest commit / open PRs
3. fresh-read Google Sheet only as migration compatibility evidence; never promote it to active canon
4. fresh-read Notion Human Home / Core Detail / Visual Bible / AI System Record
5. report authority conflicts before mutation
6. preserve #196 read-only unless user explicitly changes that boundary
```

Written SHAs are historical evidence checkpoints, not permanent live-head pointers.

## 2. Current planning authority

Current integrated owner:

`docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`

Decision-specific owners:

- `docs/decisions/BS-DAMAGE-20260826-30_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY.md`
- `docs/planning/BLACKSMITH_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY_20260826.json`
- `docs/decisions/BS-REPAIR-20260826-29_DURABILITY_REPAIR_SCAR_MODEL.md`
- `docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json`
- `docs/decisions/BS-DAMAGE-20260826-28_DAMAGE_PROBABILITY_CURVE.md`
- `docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json`
- `docs/decisions/BS-ART-20260826-04_ACTUAL_GAME_IMAGE_CONSUMER_GATE.md`
- `docs/planning/BLACKSMITH_ACTUAL_GAME_IMAGE_CONSUMER_GATE_20260826.json`

Current approved Decisions:

| Decision | Current meaning |
| --- | --- |
| `BS-ENHANCE-20260825-25` | Every enhancement success is exactly `+1`; only `+9 -> +10` is Precision; successful +10 creates one player-facing item keyword via existing `CATALYST_AFFIX`. |
| `BS-DAMAGE-20260825-26` | Historical structural simplification. Its no-numeric-authority and one-state-per-event fields are partially superseded by Decision29; its customer/world damage hook is refined by Decision30. |
| `BS-DAMAGE-20260826-28` | Target-level base conditional damage-event chance after enhancement failure: `+11 5% / +30 6% / +60 7% / +90 8% / +100 10%`, exact piecewise-linear between anchors. |
| `BS-REPAIR-20260826-29` | Visible `CURRENT/MAX/BASE_MAX` is sole durability authority. Current damage and permanent scar collapse into one effective durability state; low effective durability penalizes further enhancement; repair quality and probabilistic MAX -1 scar use temporary test budgets. MAJOR enhancement remains allowed with penalties. |
| `BS-DAMAGE-20260826-30` | Customer/world damage requires actual item use + authored event profile/cause. Purchase/handoff does not damage. One event/UID rolls at most once. `NONE/LOW/MEDIUM/HIGH/DIRECT = 0/10/20/40/100%` is temporary; probabilistic profiles use Decision29 effective-state multiplier with 95% cap; DIRECT is one deterministic Decision29 damage event. World events never directly damage MAX. |
| `BS-CHRONICLE-20260825-27` | Player Chronicle shows meaningful lifecycle events, not routine attempt logs or schedule ticks. |
| `BS-ART-20260825-03` | `ILLUSTRATED_WORKSHOP_BOOK / USER_APPROVED_DIRECTION`; final product asset/runtime approval remains separate. |
| `BS-ART-20260826-04` | New generated Blacksmith images require an actual game consumer and Primary Use Gate. No new standalone explanatory GDD-sheet images; generated UI screenshots are not product assets. Existing 8 Visual GDDs remain historical information-architecture references. |

Unchanged thesis:

```text
PRIMARY CORE = enhancement tension + DDD
PLAYER QUESTION = STOP or PUSH
ITEM IDENTITY = stable UID through crafting / ownership / world consequence / durability / repair / destruction archive
```

## 3. Current durability authority

```text
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
BASE_MAX_DURABILITY = immutable birth durability
0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
CURRENT_CONDITION_RATIO = CURRENT_DURABILITY / MAX_DURABILITY
STRUCTURAL_CONDITION_RATIO = MAX_DURABILITY / BASE_MAX_DURABILITY
EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)
DESTROYED = CURRENT_DURABILITY == 0
NORMAL = EFFECTIVE_DURABILITY_RATIO == 1.00
MINOR = 0.50 < EFFECTIVE_DURABILITY_RATIO < 1.00
MAJOR = 0 < EFFECTIVE_DURABILITY_RATIO <= 0.50
CURRENT_MAX_AUTHORITY = SUPERSEDED = HISTORICAL_DECISION26_ONLY
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
DAMAGE_EVENT_CURRENT_LOSS = 1 / TEMP_TEST_BUDGET
```

Numeric durability is visible and sole mechanical authority. Current damage and permanent structural scar are **not separate penalty stacks**; the worse ratio becomes one effective state.

Reference `BASE_MAX=5`:

```text
5/5/5 -> NORMAL
4/5/5 -> MINOR
2/5/5 -> MAJOR
4/4/5 -> MINOR
2/2/5 -> MAJOR
1/1/5 -> MAJOR
```

A perfect repair therefore does not erase a MAX scar mechanically.

## 4. Enhancement-failure damage

Decision28 target base probability remains unchanged:

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
+11 = 5%
+30 = 6%
+60 = 7%
+90 = 8%
+100 = 10%
INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
CANONICAL_ROUNDING = NONE
```

Decision29 effective-state modifier is temporary:

```text
NORMAL: success 0pp / new effect ×1.00 / damage risk ×1.00
MINOR:  success -3pp / new effect ×0.90 / damage risk ×1.25
MAJOR:  success -7pp / new effect ×0.75 / damage risk ×1.75
```

Final damage-event chance remains conditional on enhancement failure:

```text
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, EFFECTIVE_STATE)
= Decision28_target_base * Decision29_effective_state_multiplier
```

`FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED`; `UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED`.

## 5. Repair / probabilistic structural scar

```text
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY
DESTROYED_REPAIR_ALLOWED = FALSE
FULL_DURABILITY_REPAIR_ALLOWED = FALSE
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
MAX_DURABILITY_RECOVERY = NOT_APPROVED
```

Temporary quality Budget:

```text
EXCELLENT 20% -> post-scar MAX 100%
STANDARD  60% -> post-scar MAX 75%
POOR      20% -> post-scar MAX 50%
minimum CURRENT gain when possible = 1
```

Temporary MAX -1 scar chance uses **pre-repair effective state + enhancement band**:

| State | +0~10 | +11~30 | +31~60 | +61~90 | +91~100 |
|---|---:|---:|---:|---:|---:|
| MINOR | 10% | 15% | 20% | 25% | 30% |
| MAJOR | 25% | 30% | 35% | 40% | 45% |

All detailed Decision29 values are `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`. Repair gold/material/fatigue economy is not closed and requires a rebase.

## 6. Customer/world use · Decision30

```text
PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE
ACTUAL_ITEM_USE_REQUIRED = TRUE
MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1
MISSION_OUTCOME_AND_ITEM_DAMAGE = INDEPENDENT_AXES
WORLD_EVENT_MAX_DURABILITY_DAMAGE = FALSE
NO_UNIVERSAL_CUSTOMER_DAMAGE_PERCENT
```

Temporary event profile Budget:

```text
NONE = 0%
LOW = 10%
MEDIUM = 20%
HIGH = 40%
DIRECT = 100%
PROBABILISTIC_DAMAGE_CAP = 95%
```

`NONE/LOW/MEDIUM/HIGH` use the existing Decision29 effective-state damage-risk multiplier. `DIRECT` causes one deterministic Decision29 damage event. Actual event damage feeds the same numeric durability resolver and never directly reduces MAX.

Explicit event-specific relevant protection may reduce a probabilistic profile by at most one tier. There is no universal keyword damage bonus and generic protection does not mitigate DIRECT.

## 7. Explicitly historical / superseded material

Historical only where conflicting:

- Decision26 `CURRENT_MAX_AUTHORITY = SUPERSEDED` and `ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE` fields;
- old CURRENT/MAX 0~100 scale and old MAX structural-state bands;
- old MAX success/new-effect penalty tables;
- old `CURRENT -> MAX` repair-price formulas;
- old MAX overhaul `+15 / cap60`;
- old `HOLD / DOWNGRADE / DAMAGE / CRITICAL` percentages as current damage/failure-composition authority;
- old precision milestones +20/+30/+40/+50;
- dated routine enhancement Chronicle rows;
- existing explanatory Visual GDD boards as new-image batch templates.

Decision29 does not revive old durability values. Decision30 owns current customer/world-event damage policy. Decision04 owns current new-image consumer Gate.

## 8. Current runtime reality

Current V2 runtime/data still contains old durability/customer/failure logic. Similar field names are not Decision29/30 implementation evidence.

```text
NEW_CORE_RUNTIME = NOT_RUN / BLOCKED
OLD_V2_RUNTIME = IMPLEMENTATION_DRIFT / HISTORICAL_RUNTIME_TRUTH
```

Do not mutate protected product paths until explicit user `planning complete` opens the implementation gate.

## 9. Notion responsibility split

Human-facing current surfaces:

- Home: `3c41b237-eb1c-813f-a481-e415e3250d1c`
- Core Detail: `3c11b237-eb1c-8143-baef-ecf4e697a258`
- Visual Bible: `3c01b237-eb1c-8147-abdf-fab51a8f9ad3`
- UI/Flow: `3c01b237-eb1c-81a4-af26-c3057bfdcbbf`

AI/System Record:

- `3c01b237-eb1c-81a1-8cd0-f8bc7eb2f420`

Human pages show current gameplay/visual meaning; PR/SHA/test receipts and runtime evidence ceilings belong in the System Record/repository.

## 10. Visual state · Art03 + Decision04

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE
PRIMARY_USE_GATE_REQUIRED = TRUE
NO_CONSUMER = CUT_OR_DEFER
```

Existing 8 Visual GDDs are `HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY`. Future images are selected only after mapping to an actual game consumer. UI layout/prototype work should remain editable/structured instead of becoming a fake generated screenshot. Image generation still requires its separate conversation approval Gate.

## 11. Next planning Gates

```text
1. REPAIR_ECONOMY_REBASE + DURABILITY_ECONOMY_SENSITIVITY
2. FAILURE_CONSEQUENCE_COMPOSITION + UI_DAMAGE_PERCENT_ROUNDING if required
3. ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS
4. adversarial full-planning review
5. explicit user `planning complete`
6. runtime implementation-plan refresh + TDD migration
```

## 12. Evidence ceiling

```text
DAMAGE_PROBABILITY_CURVE = USER_APPROVED / BS-DAMAGE-20260826-28
DURABILITY_REPAIR_STRUCTURE = USER_APPROVED / BS-REPAIR-20260826-29
DURABILITY_REPAIR_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
CUSTOMER_WORLD_EVENT_DAMAGE_POLICY = USER_APPROVED / BS-DAMAGE-20260826-30
CUSTOMER_EVENT_DAMAGE_PROFILE_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
VISUAL_DELIVERY_POLICY = USER_APPROVED / BS-ART-20260826-04
IMAGE_GENERATION = NOT_RUN
ACTUAL_RUNTIME_IMAGE_CONSUMPTION = NOT_RUN
REPAIR_ECONOMY = NOT_FINAL
FAILURE_CONSEQUENCE_COMPOSITION = NOT_DECIDED
UI_DAMAGE_PERCENT_ROUNDING = NOT_DECIDED
NEW_CORE_RUNTIME = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_DEVICE = NOT_RUN
ACCESSIBILITY = NOT_RUN
PERFORMANCE = NOT_RUN
NOTION_CLIENT_GEOMETRY_RENDER = NOT_RUN
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

## 13. PR / merge rule

For any planning PR:

- fresh-read current Blacksmith main and Base before branching;
- preserve #196 `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`;
- exact-head required workflows GREEN;
- review changed files/protected paths;
- perform minimum five adversarial loops;
- synchronize human Notion current meaning;
- merge same approved scope without asking for redundant approval;
- postmerge read new main, update System Record SHA/Sync State, then same-ID Sheet compatibility row when needed.
