# [현재 정본] Blacksmith Core Simplification Canon · 2026-08-25

- Decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-DAMAGE-20260826-28 / BS-REPAIR-20260826-29 / BS-REPAIR-20260826-31 / BS-DAMAGE-20260826-30 / BS-ENHANCE-20260826-32 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03 / BS-ART-20260826-04 / BS-ENHANCE-20260828-34`
- Status: `USER_APPROVED / CURRENT_CANON_MVP_IMPLEMENTATION_AUTHORIZED`
- Work Mode: `IMPLEMENTATION_AND_REVIEW`
- Product implementation: `CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826`
- Runtime implementation: `PARTIALLY_IMPLEMENTED_HISTORICAL_EVIDENCE / CURRENT_SLICE_CONTRACT_REPAIR_ACTIVE`
- Human/Player validation: `NOT_RUN`

## 1. Current ownership

This document owns the integrated current meaning for enhancement cadence, precision keyword, visible durability, derived damage state, Decision28 enhancement-failure damage probability, Decision29 repair/scar model, Decision31 repair-economy sensitivity overlay, Decision30 customer/world-event damage policy, Chronicle inclusion, Art03 direction and Art04 actual-game image consumer gate.

For the `+10` keyword recipient, machine owner, player-title exclusion, and
unapproved-content boundary, `BS-ENHANCE-20260828-34` is the field owner and
overrides this integrated canon if any wording conflicts.

Decision-specific machine owners:

- `docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json`
- `docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json`
- `docs/planning/BLACKSMITH_REPAIR_ECONOMY_REBASE_20260826.json`
- `docs/planning/BLACKSMITH_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY_20260826.json`
- `docs/planning/BLACKSMITH_ACTUAL_GAME_IMAGE_CONSUMER_GATE_20260826.json`

Historical CURRENT/MAX values, MAX bands, old repair/overhaul formulas, old DAMAGE/CRITICAL ratios and multi-precision cadence are not fallback authority.

## 2. Enhancement / Precision · `BS-ENHANCE-20260825-25`

```text
SUCCESS_LEVEL_DELTA = +1
NO_MULTI_LEVEL_SUCCESS
TARGET_LEVEL = CURRENT_LEVEL + 1
+9 -> +10 = PRECISION_ENHANCEMENT
+10 PRECISION SUCCESS -> exactly one WEAPON_ITEM_KEYWORD
ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY
ITEM_KEYWORD machine owner = CATALYST_AFFIX
WEAPON_KEYWORD_TAXONOMY = GRADE_KEYWORD / TAG_KEYWORD / EVENT_KEYWORD
GRADE_KEYWORD_MACHINE_OWNER = GRADE_AFFIX
TAG_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX
EVENT_KEYWORD_MACHINE_OWNER = CHRONICLE_AFFIX
+10_PRECISION_OUTPUT_KEYWORD = TAG_KEYWORD
TAG_KEYWORD_SOURCE = CATALYST_LINEAGE_AND_PRECISION_METHOD
TAG_KEYWORD_RESOLUTION = CATALYST_LINEAGE_AND_PRECISION_METHOD_GOVERN_TAG_IDENTITY
PRECISION_METHOD_EFFECT_SCOPE = WEAPON_STATS_DURABILITY_AND_TAG_RESOLUTION_CONTEXT
PRECISION_METHOD_TAG_ROLE = TAG_IDENTITY_RESOLUTION
PRECISION_METHOD_CANNOT_AFFECT_GRADE_OR_EVENT_KEYWORD = TRUE
EMPTY_CATALYST_LINEAGE_BEHAVIOR = UNDECIDED / BLOCKS_TAG_WRITE_IMPLEMENTATION
PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10
NO_FOURTH_AFFIX_SLOT
```

`+10`의 하나는 **태그 키워드**다. 등급 키워드는 최초 제작의
`GRADE_AFFIX`, 사건 키워드는 의미 있는 작품 생애의 `CHRONICLE_AFFIX`가
각각 소유한다. 세 표현은 새 슬롯이 아니라 기존 세 field의 player-facing
분류이며, 사건 발생·handoff·표시만으로 사건 키워드를 자동 부여하지 않는다.

태그 키워드의 후보 가족과 정체성은 `CATALYST_AFFIX`의 촉매 계보와
정밀강화 방식의 조합으로 결정한다. 방식은 무기 능력치·내구도와 태그 해석
문맥에만 영향을 주며, 등급·사건 키워드의 생성·선택·변경·대체 권한이 없다.
빈 촉매 계보의 `+10` 동작은 아직 승인되지 않았으므로, 태그 content row와
함께 별도 선택/기본값 규칙이 정해지기 전에는 태그 write 또는 표시를 구현하지
않는다.

+20/+30/+40/+50 do not reopen Precision. Durability modifiers never change the +1 level delta or +10 keyword cardinality.

### 2.1 Craft-feedback milestones · user-approved 2026-08-28

```text
CRAFT_FEEDBACK_MILESTONES = EVERY_5_LEVELS
+5 = CRAFT_FEEDBACK_MILESTONE_ONLY
+10 = CRAFT_FEEDBACK_MILESTONE_PLUS_SOLE_PRECISION_ENHANCEMENT
NO_ADDITIONAL_PRECISION_AT_OTHER_5_LEVEL_MILESTONES = TRUE
NO_NEW_AFFIX_OR_PROBABILITY_OR_RESOURCE_RULE_AT_CRAFT_MILESTONE = TRUE
```

Every five levels may create a stronger crafted-item feedback beat: a clear
visual, audio, or presentation rise subject to a future approved consumer and
implementation plan. These are experience and presentation milestones only.
They do not add a success rule, a new Precision Enhancement, an additional
affix, a material slot, a probability change, or an economy rule. `+9 -> +10`
remains the one and only Precision Enhancement and keyword boundary.

## 3. Current durability authority · `BS-REPAIR-20260826-29`

Decision29 partially supersedes Decision26's no-numeric-authority/state-step fields. Numeric durability is now **visible and sole mechanical authority**.

```text
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
DAMAGE_STATE = DERIVED_PLAYER_FACING_VIEW
NO_HIDDEN_SECOND_DURABILITY_AUTHORITY = TRUE
BASE_MAX_DURABILITY = immutable birth durability
MAX_DURABILITY = current structural ceiling
CURRENT_DURABILITY = current durability
0 <= CURRENT_DURABILITY <= MAX_DURABILITY <= BASE_MAX_DURABILITY
MAX_DURABILITY_FLOOR = 1
REFERENCE_BASE_MAX_DURABILITY = 5  # reference/test item only
CURRENT_MAX_AUTHORITY = SUPERSEDED = HISTORICAL_DECISION26_ONLY
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE = SUPERSEDED_BY_DECISION29
```

### 3.1 Effective durability ratio

A perfect CURRENT repair does not erase a permanent MAX scar. Therefore current damage and structural scar are collapsed into **one** effective ratio rather than stacked as two penalties.

```text
CURRENT_CONDITION_RATIO = CURRENT_DURABILITY / MAX_DURABILITY
STRUCTURAL_CONDITION_RATIO = MAX_DURABILITY / BASE_MAX_DURABILITY
EFFECTIVE_DURABILITY_RATIO = min(CURRENT_CONDITION_RATIO, STRUCTURAL_CONDITION_RATIO)
```

State derivation:

```text
DESTROYED = CURRENT_DURABILITY == 0
NORMAL = EFFECTIVE_DURABILITY_RATIO == 1.00
MINOR = 0.50 < EFFECTIVE_DURABILITY_RATIO < 1.00
MAJOR = 0 < EFFECTIVE_DURABILITY_RATIO <= 0.50
```

Reference examples with `BASE_MAX=5`:

```text
5/5/5 -> NORMAL
4/5/5 -> MINOR
2/5/5 -> MAJOR
4/4/5 -> MINOR   # fully repaired, permanent scar remains
2/2/5 -> MAJOR   # fully repaired, severe structural scar remains
1/1/5 -> MAJOR
0/5/5 -> DESTROYED
```

This avoids both failure modes: MAX scar becoming cosmetic, and CURRENT damage + MAX scar being punished twice.

### 3.2 Damage event amount · temporary Budget

```text
DAMAGE_EVENT_CURRENT_LOSS = 1
TEMP_TEST_BUDGET = TRUE
```

A damage event lowers CURRENT by one, floored at zero; derived state is recalculated afterward. This amount is not final balance.

## 4. Enhancement-failure damage · `BS-DAMAGE-20260826-28`

Early safety gate remains:

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
```

Decision28 target-level base conditional curve remains unchanged:

```text
P(BASE_DAMAGE_EVENT | ENHANCEMENT_FAILURE, TARGET_LEVEL)
+11  = 5%
+30  = 6%
+60  = 7%
+90  = 8%
+100 = 10%
DAMAGE_CURVE_INTERPOLATION = PIECEWISE_LINEAR_EXACT_BETWEEN_ANCHORS
DAMAGE_CURVE_ROUNDING = NONE_CANON_EXACT_UI_ROUNDING_NOT_DECIDED
```

Decision29 applies one modifier from the current **effective** durability state:

| Effective state | Success delta | New ordinary effect | Decision28 risk multiplier |
|---|---:|---:|---:|
| `NORMAL` | `0pp` | `100%` | `×1.00` |
| `MINOR` | `-3pp` | `90%` | `×1.25` |
| `MAJOR` | `-7pp` | `75%` | `×1.75` |

```text
DURABILITY_MODIFIERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
P(FINAL_DAMAGE_EVENT | FAILURE, TARGET, EFFECTIVE_STATE)
= Decision28_base_probability(TARGET) * Decision29_state_multiplier(EFFECTIVE_STATE)
```

Hard guarantee stays real 100%. Effect multiplier applies only to newly added ordinary enhancement effect, not existing stats, +1 level delta or keyword count.

```text
BS-ENHANCE-20260826-32
FAILURE_CONSEQUENCE_COMPOSITION = USER_APPROVED_EXCLUSIVE_HOLD_OR_DAMAGE
FAILURE_OUTCOMES = SUCCESS / FAILED_HOLD / FAILED_DAMAGE
FAILED_DAMAGE_REPLACES_FAILED_HOLD = TRUE
FAILURE_LEVEL_DOWNGRADE = FORBIDDEN
FAILURE_SEPARATE_CRITICAL_OUTCOME = FORBIDDEN
UI_DAMAGE_PERCENT_ROUNDING = USER_APPROVED_FINAL_OUTCOME_ONE_DECIMAL_HALF_UP
UI_OUTCOME_DISPLAY = FINAL_PER_ATTEMPT_ONE_DECIMAL_HALF_UP
RUNTIME_PROBABILITY = EXACT_NO_ROUNDING
```

## 5. Repair / probabilistic MAX scar + economy overlay · `BS-REPAIR-20260826-29 / BS-REPAIR-20260826-31`

```text
REPAIR_JOB_AVAILABLE = true after a resolved actual damage event lowers CURRENT; one boolean per UID
REPAIR_ELIGIBLE = 0 < CURRENT_DURABILITY < MAX_DURABILITY AND REPAIR_JOB_AVAILABLE
REPAIR_JOB_CONSUMED_ON_REPAIR_START = TRUE
DESTROYED_REPAIR_ALLOWED = FALSE
FULL_DURABILITY_REPAIR_ALLOWED = FALSE
MAJOR_ENHANCEMENT_ELIGIBILITY = ALLOWED_WITH_DURABILITY_PENALTIES
MAX_DURABILITY_RECOVERY = NOT_APPROVED
```

MAJOR does not force repair; player may repair, push damaged/scarred, or stop/handoff.

### 5.1 Temporary repair quality

| Result | Chance | Target CURRENT after repair |
|---|---:|---:|
| EXCELLENT | 20% | 100% of post-scar MAX |
| STANDARD | 60% | 75% of post-scar MAX |
| POOR | 20% | 50% of post-scar MAX |

```text
REPAIR_MINIMUM_CURRENT_GAIN_WHEN_POSSIBLE = 1
REPAIR_QUALITY = TEMP_TEST_BUDGET
```

### 5.2 Temporary MAX -1 scar chance

| Pre-repair effective state | +0~10 | +11~30 | +31~60 | +61~90 | +91~100 |
|---|---:|---:|---:|---:|---:|
| MINOR | 10% | 15% | 20% | 25% | 30% |
| MAJOR | 25% | 30% | 35% | 40% | 45% |

```text
MAX_SCAR_AMOUNT_ON_TRIGGER = -1
MAX_DURABILITY_FLOOR = 1
MAX_SCAR_CHANCE = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

At MAX=1 scar chance becomes zero. Repair itself cannot destroy the item. A scarred full item cannot reroll MAX recovery because full-durability repair is ineligible and MAX recovery is not approved.

User reference:

```text
BASE_MAX=5, CURRENT/MAX=1/5
scar triggers -> MAX 5->4
EXCELLENT -> 4/4/5 -> MINOR
STANDARD  -> 3/4/5 -> MINOR
POOR      -> 2/4/5 -> MAJOR
```

Without scar: EXCELLENT `5/5/5 NORMAL`, STANDARD `4/5/5 MINOR`, POOR `3/5/5 MINOR`.

Decision31 locks a temporary test payment: `GOLD = ceil(R_BAND * (0.05 + 0.65 * ((MAX-CURRENT)/BASE_MAX)))`; each repair also uses exactly one always-available `common_reinforcement_material`. `R_BAND` is an authored secured enhancement-band reference, never sell price, next-attempt price, MAX, or scar multiplier. A scar that would make a positive Current gain impossible is skipped without reroll, then `NEW_CURRENT = min(POST_SCAR_MAX, max(OLD_CURRENT + 1, ceil(POST_SCAR_MAX * QUALITY_RATIO)))`. Final price tables remain open; run the controlled `b=0.50/0.65/0.80` sensitivity sweep before any product-balance decision. Old CURRENT→MAX price formulas and old `MAX +15 / cap60` overhaul are historical only.

## 6. Customer/world event damage · `BS-DAMAGE-20260826-30`

Purchase or handoff itself never damages the item. Damage requires actual use, an authored event damage profile and an authored causal reason.

```text
PURCHASE_OR_HANDOFF_ITSELF_CAUSES_DAMAGE = FALSE
ACTUAL_ITEM_USE_REQUIRED = TRUE
MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1
MISSION_OUTCOME_AND_ITEM_DAMAGE = INDEPENDENT_AXES
WORLD_EVENT_MAX_DURABILITY_DAMAGE = FALSE
NO_UNIVERSAL_CUSTOMER_DAMAGE_PERCENT
```

Temporary event profiles:

```text
NONE = 0%
LOW = 10%
MEDIUM = 20%
HIGH = 40%
DIRECT = 100%
EVENT_DAMAGE_PROFILE_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
PROBABILISTIC_DAMAGE_CAP = 95%
```

For `NONE/LOW/MEDIUM/HIGH`, final event damage chance uses the **same Decision29 effective-state damage-risk multiplier** and caps at 95%:

```text
P(EVENT_DAMAGE | PROFILE, EFFECTIVE_STATE)
= min(95%, PROFILE_BASE_PERCENT * Decision29_damage_risk_multiplier(EFFECTIVE_STATE))
```

Under current temporary Decision29 multipliers:

| Profile | NORMAL | MINOR | MAJOR |
|---|---:|---:|---:|
| LOW | 10% | 12.5% | 17.5% |
| MEDIUM | 20% | 25% | 35% |
| HIGH | 40% | 50% | 70% |

`DIRECT=100%` means one deterministic Decision29 damage event and does not use the probabilistic cap/multiplier. If triggered, Decision29 owns `CURRENT` damage and state re-derivation; world events never directly create `MAX -1` scar.

An explicitly relevant item keyword/function may reduce a probabilistic profile by at most one tier only when the event declares that causal relevance. There is no universal keyword damage bonus and a generic keyword does not mitigate `DIRECT`.

Detailed event profile numbers are temporary. Current-canon implementation may
proceed only through the unified contract, RED-first tests, and its protected
scope; this rule does not authorize a customer-flow expansion.

## 7. Chronicle · `BS-CHRONICLE-20260825-27`

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY
```

Player Chronicle may retain creation, +10 keyword, durability damage, meaningful repair, MAX scar, handoff, world consequence, destruction, memorial/successor. Routine attempt clicks and schedule ticks remain internal provenance/telemetry.

## 8. Preserved product thesis

```text
PRIMARY_CORE = ENHANCEMENT_TENSION + DDD
PLAYER_QUESTION = STOP_OR_PUSH
PRIMARY_PLAYABLE_CONTENT = REPEATED_ENHANCEMENT_JUDGMENT_AND_FEEDBACK
CUSTOMER_ITEM_LIFECYCLE = DIFFERENTIATING_CONTEXT_FOR_ENHANCEMENT_CHOICES
LIFECYCLE_ROLE = MAKE_ENHANCEMENT_OUTCOMES_PERSONAL_AND_MEMORABLE
SLICE_RULE = DO_NOT_REPLACE_ENHANCEMENT_PLAY_WITH_A_SINGLE_RISK_DEMO
ENHANCEMENT_CADENCE_AND_SESSION_LENGTH = USER_APPROVED_SLICE_B / 6_TO_8_MINUTES_PLAYTEST_HYPOTHESIS
ITEM_UID_IDENTITY = PRESERVED
RECOVERY_OWNER = ITEM_UID + TARGET_LEVEL
CHECKPOINT_FLOORS = [10,30,60,90]
+10 = FIRST_ECONOMIC_SECURED_BREAK_EVEN_STATE
+11 = FIRST_SALIENT_STOP_PUSH_RISK_DECISION
+100 = MAX_ENHANCEMENT_TERMINAL
CUSTOMER_WORLD_RESULT = DELAYED_SAME_UID_CAUSALITY_AFTER_MEANINGFUL_ENHANCEMENT_PLAY
```

Enhancement is the repeated, enjoyable main content. Customer and item-lifecycle
content is neither an alternative main loop nor a replacement for enhancement
play: it differentiates the game by carrying the same UID's enhancement choices
into ownership, actual use, repair, and Chronicle. The approved representative
Slice B therefore lets the player enjoy a meaningful run of enhancement judgment
and feedback before showing a same-UID lifecycle consequence; its 6–8 minute
duration is a Human-playtest hypothesis, not a runtime timer.

Decision29 adds a repair/push/stop choice inside the same core rather than creating a maintenance game as a second core. Decision30 makes world damage a causal result of actual use rather than a generic ownership tax.

Existing success/recovery/attempt-cost/resource/economic values remain planning inputs and require Decision29/30 sensitivity revalidation.

### 8.1 Phase-1 representative Slice · user-approved 2026-08-28

```text
PHASE_1_SLICE_VARIANT = B_ENHANCEMENT_FIRST_SAME_UID_LIFECYCLE
PHASE_1_ENHANCEMENT_PATH = +0_TO_+10_INDIVIDUAL_ATTEMPTS
PHASE_1_RISK_WINDOW = +11_TO_+15_MULTIPLE_STOP_PUSH_OPPORTUNITIES
PHASE_1_LIFECYCLE_CLOSURE = ONE_SAME_UID_CUSTOMER_ACTUAL_USE_RESULT
PHASE_1_CUSTOMER_SCOPE = ONE_CUSTOMER / ONE_EVENT / ONE_ITEM_UID
PHASE_1_REPAIR_SCOPE = ONE_ELIGIBLE_REPAIR_DECISION_IF_ACTUAL_DAMAGE
PHASE_1_TARGET_SESSION_DURATION = 6_TO_8_MINUTES
PHASE_1_DURATION_STATUS = EXPERIENCE_HYPOTHESIS_NOT_RUNTIME_TIMER
PHASE_1_RESULT_TIMING = HANDOFF_TO_ONE_WORKSHOP_RETURN_BEAT_TO_RESULT
PHASE_1_RETURN_BEAT = NON_ECONOMIC / NO_SECOND_ITEM / NO_CUSTOMER_MANAGEMENT
DO_NOT_REPLACE_ENHANCEMENT_PLAY_WITH_SINGLE_RISK_DEMO = TRUE
DO_NOT_FAKE_DAMAGE_FOR_DEMONSTRATION = TRUE
```

The player begins with one item UID and experiences ordinary enhancement as
individual +1 attempts through +10. `+9 -> +10` remains the sole Precision
Enhancement and produces exactly one item keyword on success. The Slice then
offers targets `+11` through `+15` as multiple STOP/PUSH opportunities; the
player may stop after any decision and is never forced to reach `+15`.

After the player chooses to hand off the item, one brief non-economic return
to the workshop separates the departure from the same UID's actual-use result.
It is a pacing and ownership beat, not a wait timer, customer-management
system, second-item task, or new economy. One customer actual-use result may
then close the same UID's lifecycle arc. Customer result is not an additional
enhancement substitute, nor is damage scripted merely to demonstrate repair.
If actual damage occurs, the existing one-job repair rule may present its
single recovery decision before the player returns to the enhancement loop.

This is a Phase-1 experience contract, not current runtime completion. The
approved 6–8 minute target is a playtest hypothesis, never a runtime countdown.
Attempt timing, resources, economy, and customer-event scheduling remain
unimplemented or undecided until their appropriate gates.

## 9. First-session interpretation

```text
NEW_GAME
-> FIRST_ITEM
-> ordinary +1 enhancement through +9
-> +9 -> +10 Precision
-> +10 success creates one keyword
-> +10 secured state
-> +11 first damage-eligible STOP/PUSH
-> if damaged/scarred: show CURRENT/MAX/BASE_MAX + effective state
-> REPAIR / PUSH DAMAGED / STOP
-> HANDOFF
-> later actual-use event may resolve event-specific same-UID damage
```

Do not teach obsolete hidden MAX bands; teach current visible numeric durability. Do not fake an immediate world event just to demonstrate damage.

## 10. Art direction + actual-game image consumer gate

Current style direction remains:

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

`BS-ART-20260826-04` changes the **visual delivery target**, not Art03's style:

```text
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
NEW_EXPLANATORY_GDD_SHEET_IMAGE_TARGET = FALSE
NO_NEW_EXPLANATORY_GDD_SHEET_IMAGE
PRIMARY_USE_GATE_REQUIRED = TRUE
NO_CONSUMER = CUT_OR_DEFER
GENERATED_UI_SCREENSHOT_MOCKUP_AS_PRODUCT_ASSET = FALSE
FULL_FRAME_IMAGE_ALLOWED_ONLY_IF_RUNTIME_CONSUMES_FULL_FRAME = TRUE
```

The existing 8 Visual GDD images remain `HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY`. New image work starts from an actual product consumer slot and required consumer metadata, not from a desire to create another explanation sheet.

Current consumer locators such as Main Menu, Enhancement, Precision +10, Durability/Repair, Customer World Result and Chronicle are **candidates only**. Each must pass Visual Requirement/Delete Test before generation. Under `BS-OPS-20260828-35`, generation after that requirement is user-preauthorized; only final direction lock or runtime promotion needs the user's post-generation approval. Structured repository/Figma/Godot layout work is preferred over fake generated screenshots for UI design.

## 11. Supersession boundary

- Decision26 no-numeric-authority and one-state-per-event fields: `PARTIALLY_SUPERSEDED_BY_BS-REPAIR-20260826-29`.
- Decision26 customer/world-event hook is refined by `BS-DAMAGE-20260826-30` for eligibility/profile/probability composition.
- Historical 0~100 CURRENT/MAX scale, old MAX bands/success/effect penalties: historical only.
- Old repair formulas and `MAX +15 / cap60` overhaul: historical/superseded; not fallback.
- Old DAMAGE/CRITICAL family ratios: historical; not Decision28/29 authority.
- Old multi-precision cadence: partially superseded; +10-only current.
- Historical Precision-method `FUNCTION_REWORK`, artistry, and environmental-function
  output lanes: superseded for current method effects. The current method scope is
  weapon stats and durability only.
- Old Visual GDD numeric durability values: `SYSTEM_SEMANTICS_STALE`.
- Existing Visual GDD 8: historical information-architecture references; not new image-batch templates or runtime assets.

## 12. Implementation Reality Gate

### 12.0 2026-08-28 Phase-1 recheck override

The 2026-08-26 implementation declaration and its merged runtime MVP are historical
implementation evidence. The user has since confirmed
`CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826`: implementation and review
of the approved current-canon MVP may proceed. New product scope, protected-path
changes outside the approved task, and unapproved system expansion remain blocked.

```text
CURRENT_2026-08-28_PHASE = IMPLEMENTATION_AND_REVIEW
CURRENT_ACCEPTED_FRONTIER = PHASE_2_UNIFIED_ENHANCEMENT_FIRST_SLICE_CONTRACT_REPAIR
CURRENT_PRODUCT_MUTATION = AUTHORIZED_WITHIN_CURRENT_CANON_MVP
PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10
ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY
HISTORICAL_RUNTIME_IMPLEMENTATION = AUTOMATED_EVIDENCE_ONLY_NOT_CURRENT_AUTHORITY
```

This override preserves factual repository evidence, but keeps Human play,
Android, accessibility, performance, and actual rendered-screen evidence at their
recorded ceilings. It does not relabel historical runtime behavior as current
product approval.

```text
PLANNING_DESIGN = USER_APPROVED
DAMAGE_CURVE_NUMBERS = USER_APPROVED / BS-DAMAGE-20260826-28
DURABILITY_REPAIR_STRUCTURE = USER_APPROVED / BS-REPAIR-20260826-29
DURABILITY_REPAIR_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
CUSTOMER_WORLD_EVENT_DAMAGE_POLICY = USER_APPROVED / BS-DAMAGE-20260826-30
CUSTOMER_EVENT_DAMAGE_PROFILE_NUMBERS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
VISUAL_DELIVERY_POLICY = USER_APPROVED / BS-ART-20260826-04
IMAGE_GENERATION = NOT_RUN
ACTUAL_RUNTIME_IMAGE_CONSUMPTION = IMPLEMENTED_STATIC_PROJECT_RASTER_BINDING / VISUAL_RUNTIME_VALIDATION_NOT_RUN
REPAIR_ECONOMY = USER_APPROVED_TEST_CONTRACT / B65_DEFAULT_PLAYTEST_REQUIRED
FAILURE_CONSEQUENCE_COMPOSITION = USER_APPROVED_EXCLUSIVE_HOLD_OR_DAMAGE
UI_DAMAGE_PERCENT_ROUNDING = USER_APPROVED_FINAL_OUTCOME_ONE_DECIMAL_HALF_UP
HISTORICAL_2026-08-26_PLANNING_COMPLETE_DECLARATION = RECORDED
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = HISTORICAL_MVP_IMPLEMENTED / GODOT_GUT_VERIFIED
RUNTIME_IMPLEMENTATION_SCOPE = ITEM_V3 + SAVE_V3_MIGRATION + ENHANCEMENT_FAILURE + REPAIR_ECONOMY
RUNTIME_UI_INTEGRATION = WORKSHOP_DURABILITY_REPAIR_BINDING_IMPLEMENTED / ITEM_SOURCE_CALLER_PENDING
CUSTOMER_WORLD_EVENT_RUNTIME = NOT_RUN
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_GEOMETRY = NOT_APPLICABLE / HISTORICAL_SURFACE_RETIRED_BY_BS-OPS-20260828-35
```

This implementation proof is limited to the listed MVP core paths. It does not prove customer/world-event integration, mobile UI, Android behavior, accessibility, performance, art consumption, or human play.

The current single owner for the approved Phase-1 implementation package is
`docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md`.
It converts the approved Slice B into a bounded implementation and validation
contract without opening a new-product-scope gate.

## 13. Next implementation order

```text
1. Treat `CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826` as the approved scope authority
2. Review the unified implementation contract against fresh main/open-PR/runtime reality
3. Execute its RED -> GREEN -> REFACTOR package on an isolated task branch
4. Run exact-head automated, Godot, portrait, and Human validation gates
```
