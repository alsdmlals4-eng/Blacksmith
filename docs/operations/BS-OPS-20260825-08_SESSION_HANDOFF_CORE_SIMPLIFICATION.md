# Blacksmith Session Handoff · Core Simplification

- Decision ID: `BS-OPS-20260825-08`
- Date: `2026-08-25 KST`, current update `2026-08-26 KST`
- Status: `CURRENT_SESSION_HANDOFF / CODEX_RUNTIME_MVP_IMPLEMENTATION_ACTIVE`
- Historical checkpoints: `PR #207 = MERGED_TO_MAIN / 5c29af1...`; `PR #208 = MERGED / R5_4_ROUTER`; `PR #209 = MERGED / BS-DAMAGE-20260826-28`; `PR #210 = MERGED / BS-REPAIR-20260826-29`; `PR #211 = MERGED / BS-DAMAGE-20260826-30 + BS-ART-20260826-04`
- `CURRENT_PLANNING_WORK = REPAIR_ECONOMY_HUMAN_PLAYTEST + ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS`
- `GPT_WORK_PRIMARY_EXECUTION_SURFACE = GPT_WORK`
- `GPT_WORK_MEMORY_MODE = DEFAULT_MEMORY`
- `IMAGE_GOAL_QUEUE = READY_FOR_GPT_WORK`
- Pre-existing protected PR: `#196 / OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`
- Product implementation: `CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826`

## 0. Runtime MVP checkpoint · 2026-08-26

The user declared the current planning complete and authorized Godot implementation against the current canon. GitHub Issue `#224` owns the first runtime slice.

```text
RUNTIME_MVP = ITEM_V3 + SAVE_V3_MIGRATION + ENHANCEMENT_FAILURE + REPAIR_ECONOMY
ITEM_DURABILITY = CURRENT / MAX / BASE_MAX = 5
FAILURE_OUTCOMES = FAILED_HOLD | FAILED_DAMAGE
REPAIR = one actual-damage job + R_BAND gold + one common reinforcement material
OVERHAUL = SUPERSEDED
V2_SAVE = READ_MIGRATE_TO_V3 / NEXT_WRITE_V3
GODOT_GUT_CORE_VERIFICATION = PASS
RUNTIME_UI_INTEGRATION = WORKSHOP_DURABILITY_REPAIR_BINDING_IMPLEMENTED / ITEM_SOURCE_CALLER_PENDING
CUSTOMER_WORLD_EVENT_RUNTIME = NOT_RUN
HUMAN_PLAYTEST = NOT_RUN
OPERATING_CONTRACT_BASELINE = 103e0a52bee1e0b4e3e72a8410eff5cc7c25ab24
PROTECTED_CHANGE_APPROVAL = CONSUMED_AND_RETIRED_BY_PR_229
```

## 1. GPT Work transfer · 2026-08-26

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

### Operating-contract recovery · Issue #214

`BS-OPS-20260826-32 / MERGED_PR215` restores the Work entry gate after current Base validation exposed an obsolete protected baseline and stale raw-byte health-evidence records. The repair advanced only the metadata baseline to merged Blacksmith main `1bdf5f4b436b114253e86d897c7ef15514103f8f`, adopted released Base v9.4.4 and current Base validator `43b3ffb2c5b026e3d4a38dab2338585894d36f61`, and regenerated derived adapter views. PR #215 merged at `c51c1c358714dde3fc5c04156c9e77e28c8f4b10`; runtime, Android, accessibility, performance, and human-play evidence remain `NOT_RUN`. The Google Sheet remains `MIGRATION_ONLY_COMPATIBILITY` and is not written by this repair. No `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot` path is in scope; PR #196 remains read-only.

### Decision31 deterministic sensitivity · Issues #216, #218

`BS-OPS-20260826-33 / DECISION31_SENSITIVITY_DELIVERY` records the approved planning-only Decision31 sweep: one fixed item UID, `R_BAND = 100` normalized input, five 5-point actual-damage/repair cycles, and `b = 0.50 / 0.65 / 0.80` as the only varied economic input. The result must report Gold, one-material use, recovery, scar skip, consumed repair job, blocked repeat repair, and player decision outcome separately. `b=.65 / USER_APPROVED_FIRST_TEST_DEFAULT`; `R_BAND=100 / HISTORICAL_NORMALIZED_SENSITIVITY_INPUT_ONLY`; `b=.50/.80` remain comparison curves only. `R_BAND_TEST_TABLE = USER_APPROVED_MUTABLE_BASELINE`: +0~10 `125/145/170`, +11~30 `160/185/215`, +31~60 `220/255/295`, +61~90 `300/345/405`, +91~100 `400/460/540` for iron/silver/meteor iron. The table may change after human playtesting or new balance evidence; it is not a shipping price table. `HUMAN_PLAYTEST = NOT_RUN` until the first controlled experience check. This cannot create a product implementation approval. Future user-approved images require a dual-storage receipt: Notion record plus exact project-local binary path with SHA-256 and actual-game consumer ID. No image is created or written to `assets/` until the current product gate permits it.

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
- `docs/decisions/BS-REPAIR-20260826-31_REPAIR_ECONOMY_REBASE_AND_SENSITIVITY.md`
- `docs/planning/BLACKSMITH_REPAIR_ECONOMY_REBASE_20260826.json`
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
| `BS-REPAIR-20260826-31` | Approved planning-only repair-economy overlay: one repair job per actual-damage cycle, initial normalized loss curve plus one common material, and a no-zero-recovery scar guard. The final price table remains a controlled sensitivity decision. |
| `BS-DAMAGE-20260826-30` | Customer/world damage requires actual item use + authored event profile/cause. Purchase/handoff does not damage. One event/UID rolls at most once. `NONE/LOW/MEDIUM/HIGH/DIRECT = 0/10/20/40/100%` is temporary; probabilistic profiles use Decision29 effective-state multiplier with 95% cap; DIRECT is one deterministic Decision29 damage event. World events never directly damage MAX. |
| `BS-ENHANCE-20260826-32` | Enhancement failure is exactly `FAILED_HOLD` or `FAILED_DAMAGE`; damage replaces hold, never stacks with downgrade or separate CRITICAL. The preview shows final per-attempt success/hold/damage outcomes at one decimal; resolver probability stays exact. |
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

`FAILURE_CONSEQUENCE_COMPOSITION = USER_APPROVED_EXCLUSIVE_HOLD_OR_DAMAGE`; `UI_DAMAGE_PERCENT_ROUNDING = USER_APPROVED_FINAL_OUTCOME_ONE_DECIMAL_HALF_UP`.

## 5. Repair / probabilistic structural scar

```text
REPAIR_JOB_AVAILABLE = true after a resolved actual damage event lowers CURRENT; one boolean per UID
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY AND REPAIR_JOB_AVAILABLE
REPAIR_JOB_CONSUMED_ON_REPAIR_START = TRUE
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

Decision29 values remain `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`. Decision31 has now approved the planning test contract: `ceil(R_BAND * (0.05 + 0.65 * ((MAX-CURRENT)/BASE_MAX))) + 1 common_reinforcement_material`, one repair job per actual-damage cycle, no MAX/scar price multiplier, and a no-zero-recovery scar skip. Final prices require controlled sensitivity, not runtime work.

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
1. REPAIR_ECONOMY_HUMAN_PLAYTEST + MUTABLE_R_BAND_BASELINE_REVIEW
2. ACTUAL_GAME_CONSUMER_VISUAL_REQUIREMENT_PASS
3. adversarial full-planning review
4. explicit user `planning complete`
5. runtime implementation-plan refresh + TDD migration
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
REPAIR_ECONOMY = USER_APPROVED_TEST_CONTRACT / B65_DEFAULT_PLAYTEST_REQUIRED
FAILURE_CONSEQUENCE_COMPOSITION = USER_APPROVED_EXCLUSIVE_HOLD_OR_DAMAGE
UI_DAMAGE_PERCENT_ROUNDING = USER_APPROVED_FINAL_OUTCOME_ONE_DECIMAL_HALF_UP
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
