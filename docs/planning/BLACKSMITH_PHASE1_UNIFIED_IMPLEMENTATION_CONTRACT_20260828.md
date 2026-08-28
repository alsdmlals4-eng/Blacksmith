# Blacksmith Phase 1 Unified Implementation Contract · 2026-08-28

> This is the single implementation contract produced by the current Phase 1
> planning pass. The user has since opened current-canon MVP implementation;
> the contract remains the scope and verification boundary for that work.

```text
CONTRACT_STATUS = CURRENT_CANON_MVP_IMPLEMENTATION_AUTHORIZED
CURRENT_PHASE = IMPLEMENTATION_AND_REVIEW
CURRENT_ACCEPTED_FRONTIER = PHASE_2_UNIFIED_ENHANCEMENT_FIRST_SLICE_CONTRACT_REPAIR
PHASE_2_ENTRY = SATISFIED_BY_CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826
WEAPON_KEYWORD_OWNERSHIP_DECISION = BS-ENHANCE-20260828-34
```

## 1. Decision summary

```text
PRIMARY_PLAYABLE_CONTENT = REPEATED_ENHANCEMENT_JUDGMENT_AND_FEEDBACK
DIFFERENTIATOR = SAME_UID_CUSTOMER_ITEM_LIFECYCLE
PLAYER_QUESTION = STOP_OR_PUSH
PHASE_1_SLICE = +0_TO_+10 / +11_TO_+15 / ONE_SAME_UID_RESULT
TARGET_ACTIVE_SESSION = 6_TO_8_MINUTES / EXPERIENCE_HYPOTHESIS_NOT_TIMER
```

The player makes one item, personally completes ordinary `+1` enhancement
attempts through `+10`, and then decides whether the same item is good enough
to hand off or worth risking at `+11` through `+15`. A later actual-use result
gives those earlier decisions a human consequence. Customer content is neither
a production-management replacement nor a forced damage demonstration.

| Chain | Phase-1 contract |
| --- | --- |
| Player promise | “I made and dared to improve this one item; I can see what that choice meant when someone used it.” |
| Representative action | Read the next-attempt outcome, then press **enhance**, **stop/handoff**, or conditionally **repair**. |
| Meaningful trade-off | More level and craft satisfaction versus resource exposure, a hold result, and conditional damage from `+11` onward. |
| Observable result | Exactly `SUCCESS`, `FAILED_HOLD`, or `FAILED_DAMAGE`, with visible `CURRENT / MAX / BASE_MAX` where relevant. |
| Learning / next motive | A hold preserves the item; actual damage shows why condition matters; a same-UID result makes the next enhancement judgment personal. |

## 2. Locked rules and first-slice defaults

```text
SUCCESS_LEVEL_DELTA = +1
CRAFT_FEEDBACK_MILESTONE = EVERY_5_LEVELS
+5 = PRESENTATION_ONLY
+10 = PRESENTATION_PLUS_ONLY_PRECISION_AND_ONE_KEYWORD
ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY
ITEM_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX
PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10
WEAPON_KEYWORD_CONTENT_ID = UNDECIDED / USER_CONTENT_DECISION_REQUIRED
KEYWORD_PRESENTATION = DEFERRED_UNTIL_WEAPON_KEYWORD_CONTENT_ROW_APPROVED
WEAPON_KEYWORD_TAXONOMY = GRADE_KEYWORD / TAG_KEYWORD / EVENT_KEYWORD
GRADE_KEYWORD_MACHINE_OWNER = GRADE_AFFIX
TAG_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX
EVENT_KEYWORD_MACHINE_OWNER = CHRONICLE_AFFIX
+10_PRECISION_OUTPUT_KEYWORD = TAG_KEYWORD
TAG_KEYWORD_SOURCE = CATALYST_LINEAGE
TAG_KEYWORD_RESOLUTION = CATALYST_LINEAGE_GOVERNS_TAG_IDENTITY
PRECISION_METHOD_EFFECT_SCOPE = WEAPON_STATS_AND_DURABILITY_ONLY
PRECISION_METHOD_CANNOT_DETERMINE_OR_MUTATE_TAG_KEYWORD = TRUE
PRECISION_METHOD_CANNOT_AFFECT_GRADE_OR_EVENT_KEYWORD = TRUE
EMPTY_CATALYST_LINEAGE_BEHAVIOR = UNDECIDED / BLOCKS_TAG_WRITE_IMPLEMENTATION
NO_PRECISION_OR_AFFIX_OR_PROBABILITY_OR_RESOURCE_RULE_AT_+20_OR_LATER = TRUE
RETURN_BEAT = ONE_NON_ECONOMIC_WORKSHOP_MOMENT
NO_TIMER / NO_CUSTOMER_MANAGEMENT / NO_SECOND_ITEM / NO_FAKE_DAMAGE
```

1. Every success changes the level by exactly one. No multi-level success,
   downgrade, separate critical, or a fourth affix slot is allowed.
2. A successful `+9 -> +10` is the only Precision Enhancement. It writes
   exactly one **weapon-owned tag keyword** through the existing `CATALYST_AFFIX`
   owner. It is not a grade keyword or event keyword. The tag keyword belongs to
   the item and grants no player title; a player
   title is future content and is not granted by `+10`. Its content ID and copy
   remain unapproved, so this package must not manufacture a concrete keyword,
   persist an invented content ID, or present it to the player. The implementation
   placeholder `PRECISION_KEYWORD_PENDING_CONTENT` is never player-facing. A
   tag identity is resolved only from catalyst lineage, never from the selected
   Precision method. The method may affect only weapon stats and durability. A
   separate user-approved catalyst-lineage/content row **and** empty-lineage
   behavior are required before keyword write/presentation work enters scope;
   catalogue, function-rework, artistry, environmental-function, and mechanical
   keyword variations remain out of scope.
3. `+5`, `+15`, and every later multiple of five are presentation beats only.
   `+10` is intentionally two things at once: a craft-rise beat and the sole
   Precision/keyword boundary. No later multiple of five reopens Precision,
   changes odds/costs, consumes a catalyst, or creates an affix.
4. Target `<= +10` has no enhancement-damage result. At `+11` and above,
   failure resolves to hold or the existing Decision28/29 conditional damage
   event only. Displayed final outcomes round to one decimal; the resolver
   preserves exact values.
5. Visible `CURRENT / MAX / BASE_MAX` remains the only durability authority.
   Repair is available only after actual damage, has one job per damage cycle,
   and is unavailable for full durability or destroyed items.

### 2.1 Session budget and pacing

The current runtime fixture begins with 20,000 Gold and 10 reinforcement
materials. Its own current attempt rule consumes one material for every
attempt: an uninterrupted `+1` through `+15` already needs 15 materials.
Therefore the fixture cannot currently demonstrate the approved risk window.

```text
PHASE_1_STARTING_GOLD = 20000 / EXISTING_TEMP_TEST_BUDGET
PHASE_1_STARTING_REINFORCEMENT = 30 / TEMP_TEST_BUDGET
PURPOSE = PREVENT_RESOURCE_SOFT_LOCK_BEFORE_THE_PLAYER_CAN_MEET_+11_TO_+15
ECONOMY_STATUS = NOT_FINAL_PRODUCT_BALANCE
```

The 30-unit starting reserve is a vertical-slice experience allowance, not a
new economy loop or shipping reward. It must be visibly labeled as test
content only in technical evidence, not exposed to a player as a promise of
final balance. Gold costs and all approved probability authorities stay
unchanged in this contract.

## 3. Screen, information, and feedback contract

No new raster image is required. Phase 2 uses the current illustrated workshop
background, workpiece durability atlas, native Godot controls, and a
state-driven presentation layer. Any new image, sound, haptic, or VFX source
still requires its own approved consumer/provenance record.

| State | First attention | Player action | Required information | Feedback | Exit |
| --- | --- | --- | --- | --- | --- |
| First Forge | One owned workpiece | Create / continue | UID-bearing item and its journey promise | Small ownership beat | Enhancement |
| Ordinary `+0..+9` | Next level and main attempt action | Enhance or stop | Current/target level, cost, outcome summary, resources | One crisp `+1` confirmation | Next attempt |
| `+5` craft rise | Workpiece and `+5` mark | Continue or stop | “Craft rise” is presentation-only | Brief ink/metal accent plus result label; no modal and no new rule | Next attempt |
| `+9 -> +10` Precision | Target `+10` and weapon-affix ownership boundary | Execute the sole Precision attempt | Exact final outcome preview; concrete keyword copy remains unapproved | Stronger, interruptible Precision presentation only; keyword display deferred | `+10` secured state |
| `+11..+15` risk | STOP/HANDOFF and PUSH side by side | Push one target or hand off | Exact success/hold/damage outcome, durability, cost | Result is immediate and intelligible | Next risk or handoff |
| Return beat | The same item has left the workbench | Continue to result | Customer name, same UID, no timer | One brief non-economic workshop transition | Actual-use result |
| Result / repair | What happened to this UID | Read result; conditional repair or return | Event cause; mission result and item damage as separate axes; before/after durability; repair eligibility | Pride, concern, or recovery—not an extra customer system | Enhancement loop / Chronicle |

### 3.1 Feedback hierarchy and accessibility

- Normal attempts: a compact result line; no long cinematic, repeat input lock,
  or color-only state signal.
- `+5`: short visual rise only. It is derived from a successful target divisible
  by five and has no saved gameplay field, probability, item statistic, or
  resource effect.
- `+10`: may use a larger result panel, but it must be dismissible, safe under
  repeated taps, skippable/reduced under Reduced Motion, and leave the domain
  result committed exactly once.
- `+11..+15`: **Handoff at the current level** and **Push to the next target**
  must be separately labelled. The player must see the result probabilities
  before the commit. Handoff becomes available at level `+10` and remains
  available after a hold or non-terminal damage; it is blocked when the item is
  destroyed.
- Durability uses numeric values plus a state label and workpiece shape/atlas
  state. It never depends on colour alone.
- Motion, sound, and haptic are enhancement presentation only. Turning any of
  them off cannot change rolls, outcome, save behavior, or eligibility.

## 4. Same-UID lifecycle contract

```text
HANDOFF_ELIGIBILITY = ACTIVE_ITEM_AT_LEVEL_10_OR_HIGHER
CUSTOMER_SCOPE = NADIA_VENN / ADVENTURER_01 / ONE_EVENT / ONE_UID
ACTUAL_USE_PROFILE = MEDIUM / TEMP_TEST_BUDGET
PURCHASE_OR_HANDOFF_DAMAGE = NEVER
MAX_DAMAGE_ROLLS_PER_EVENT_PER_UID = 1
MISSION_OUTCOME_AND_ITEM_DAMAGE = INDEPENDENT
```

The Phase-1 authoring package must define one actual-use event for Nadia Venn's
ruin expedition. It has an authored cause and a `MEDIUM` profile; it does not
promise actual damage. The event resolves only after the single return beat,
saves before presentation, and presents the exact stored record. Test cases may
inject rolls to exercise damage and non-damage paths; no player-facing “force
damage” control is allowed.

If damage happens, offer the existing one eligible repair decision. If it does
not happen, state that the item returned intact and return to the enhancement
loop. If a rare chain destroys the item before handoff, show its meaningful
Chronicle/destruction closure instead of fabricating a customer result.

Routine attempt logs remain internal. Player Chronicle only receives creation,
the `+10` keyword, actual damage, repair/MAX scar, handoff, actual-use result,
or destruction.

## 5. Evidence-based review

### SWOT

| Class | Statement | Evidence / confidence | Player impact | Disposition / next validation |
| --- | --- | --- | --- | --- |
| STRENGTH | A single UID already persists through enhancement, durability, repair, and stored actual-use result. | `VSItem`, `VSEnhancementResolver`, customer resolver, and GUT contracts; `VERIFIED` at automated source level. | Earlier Push decisions can become memorable later. | `PROTECT`; run full handoff→result path. |
| STRENGTH | The core risk is legible: success/hold/damage is shown together and damage starts after `+10`. | Current resolver and current Decision28/29; `VERIFIED` at source level. | Player can identify why `+11` is the first real STOP/PUSH moment. | `PROTECT`; human comprehension test. |
| WEAKNESS | The existing player route does not connect handoff, return beat, and actual-use result. | `VSApp` supports a result caller but no current player entry/return state; `VERIFIED`. | The differentiator is not yet experienced. | `IMPROVE`; implement one bounded route. |
| WEAKNESS | Existing legacy data/modules still encode 10-level repeated Precision, old affix changes, downgrade, and extra materials. | `data/crafting/enhancement_milestones.json`, `data/crafting/enhancement_balance.json`, `scripts/enhancement/enhancement_session.gd`; `VERIFIED`. | A future UI could silently teach the wrong game. | `MITIGATE`; isolate the vertical Slice and label/retire active misuse. |
| WEAKNESS | Ten starting reinforcement units cannot cover the approved `+0..+15` path even with no failure. | Current resource fixture and resolver cost formula; `VERIFIED`. | Resource exhaustion could hide the core choice. | `IMPROVE`; use the Phase-1 temporary 30-unit reserve and test it. |
| OPPORTUNITY | Tactile crafting feedback and customer consequences can reinforce the same item without taking over the core loop. | [Potion Craft official Steam page](https://store.steampowered.com/app/1210320/Potion_Craft_Alchemist_Simulator/) presents direct tool interaction and customer consequences; `INFERENCE`. | Supports satisfying individual actions and a meaningful later consequence. | `ADAPT`; validate whether players remember the UID. |
| THREAT | A full forge-management production chain would dilute the short enhancement-first Slice. | [Blacksmith Master official Steam page](https://store.steampowered.com/app/2292800/Blacksmith_Master/) centers staffing, production chain, and shop throughput; `VERIFIED` comparison fact / `INFERENCE` for fit risk. | Too many management decisions would obscure STOP/PUSH. | `REJECT`; keep no staff, supply chain, customer roster, or shop-layout system in Phase 2. |
| THREAT | Generated art and current assets lack release-rights and human-render validation. | Rights/provenance record and current visual gate; `VERIFIED`. | None during planning; release use is unsafe to claim. | `MONITOR`; keep `RELEASE_BLOCKED_UNVERIFIED`. |

### Benchmark disposition

- **ADOPT:** Potion Craft's principle of a satisfying, readable repeated craft
  interaction and a later customer consequence. Do not copy its visuals,
  recipes, town structure, or surface expression.
- **ADAPT:** The workshop’s repeated enhancement feedback into a restrained
  two-tier rhythm: compact ordinary feedback, a stronger `+5`, and a distinct
  `+10` Precision presentation. Weapon-keyword copy is deferred until separately approved.
- **REJECT:** Blacksmith Master-style staffing, mining, throughput, shop
  layout, and full production-chain management from this Slice.
- **Differentiation:** Blacksmith turns a high-stakes enhancement decision into
  a personal item biography through one bounded same-UID actual-use result.
- **Remaining uncertainty:** Whether `+11..+15` produces enjoyable tension,
  whether the customer result is remembered, and whether the 6–8 minute path
  fits portrait mobile use all require human play.

## 6. Implementation drift and explicit boundary

```text
IMPLEMENTATION_DRIFT = LEGACY_MULTI_PRECISION_DATA_AND_NON_VERTICAL_SLICE_MODULES
P0_IMPLEMENTATION_GUARD = VERTICAL_SLICE_ONLY_CURRENT_CANON
OUT_OF_SCOPE = NEW_ART_ASSET_BATCH / ECONOMY_REBALANCE / MULTI_CUSTOMER_SYSTEM / RELEASE_WORK
```

### Incident / solution / lesson

```text
INCIDENT_ID = BS-OPS-20260828-37
CLASS = IMPLEMENTATION_DRIFT
STATEMENT = LEGACY_MULTI_PRECISION_AND_OLD_FAILURE_SEMANTICS_CAN_BE_SURFACED_BY_MISTAKE
EVIDENCE = data/crafting/** + scripts/enhancement/** versus current Decision25/28/29/32
SOLUTION = VERTICAL_SLICE_ONLY_CURRENT_CANON / RED_GUARDS / NO_LEGACY_IMPORT
LESSON = A_HISTORICAL_RUNTIME_MODULE_MUST_NEVER_BE_TREATED_AS_CURRENT_PRODUCT_AUTHORITY
NO_BASE_PROMOTION = PROJECT_SPECIFIC_LEGACY_AND_SLICE_BOUNDARY
```

This incident changes no legacy file in Phase 1. The corrective action is a
Phase-2 boundary check: only current vertical-slice owners may supply player
behavior, while legacy modules remain preserved historical evidence. The
lesson is reusable in principle, but its exact sources and product semantics
are Blacksmith-specific, so no Base promotion is warranted.

The current `scripts/vertical_slice/**` resolver has the approved one-precision
shape, but legacy `data/crafting/enhancement_milestones.json`,
`data/crafting/enhancement_balance.json`, and `scripts/enhancement/**` still
encode repeated ten-level Precision, extra affix changes, old material rules,
and downgrade/destruction behavior. They are historical implementation
evidence, not a fallback. Phase 2 must not import or surface them in the
vertical Slice. It may retain them untouched as historical modules unless a
separate migration/removal task is approved.

The current project-local art direction and declared binary consumers remain
usable only as existing runtime evidence. No art batch, fake screenshot,
marketing asset, rights clearance, or release work is contained here.

## 7. One implementation package

```text
TEST_ORDER = RED_CONTRACTS -> GREEN_MINIMUM_FLOW -> REFACTOR_LEGACY_BOUNDARIES
HUMAN_PLAYTEST = REQUIRED_AFTER_AUTOMATED_GREEN
```

### In scope within the current-canon MVP

1. Bind the vertical-slice Workshop UI to the current resolver so the player
   can complete individual attempts, read all outcomes, and see the `+5` and
   `+10` presentation states without changing game rules.
2. Preserve the `+10` weapon-affix ownership boundary using the existing
   item-owned `CATALYST_AFFIX` data owner. Until a first weapon-keyword content
   row and its empty-catalyst-lineage behavior are separately approved, do not
   create a concrete keyword, persist an invented content ID, or show any
   keyword/placeholder to the player. Do not create, grant, or display a player
   title in this package. Precision-method work may alter only weapon stats and
   durability; it may not choose or alter any keyword.
3. Add Handoff at `+10+`, exactly one non-economic return beat, and one Nadia
   actual-use result that resolves/saves once for the same UID.
4. Surface conditional repair/Chronicle from the existing durability owner,
   including no-damage and destroyed branches.
5. Change the vertical-slice temporary reinforcement fixture from 10 to 30;
   retain the existing temporary gold budget and all current probability and
   repair-economy owners.
6. Add tests before each behavior change, then exercise automated and manual
   portrait flow evidence at the exact implementation head.

### Explicitly out of scope

- New customer lists, scheduling, waiting timers, second items, staff,
  inventory/supply systems, shop layout, economy rebalance, new combat, or
  content farming.
- New raster assets, audio assets, marketing art, release submissions, or
  rights conclusions.
- Changing Decision28/29/30/31/32 values, changing success from `+1`, adding
  `+20` Precision, or reviving downgrade/critical/extra-affix rules.

### Required RED contracts

1. A success at `+5` emits only a presentation milestone; it cannot affect
   odds, costs, inventory, affixes, or the stored item schema.
2. Before a weapon-keyword content row is approved, `+10` may not expose
   `PRECISION_KEYWORD_PENDING_CONTENT`, invent a content ID, or grant a player
   title. Its `CATALYST_AFFIX` ownership boundary remains weapon-only; tag
   identity is catalyst-lineage-only; and a Precision method cannot determine
   or mutate tag, grade, or event keywords. `+20` and later never request
   Precision or add an affix.
3. The Slice cannot reach `+11..+15` only to be blocked by the old ten-unit
   material fixture under its success-path test.
4. Handoff is permitted for an active same UID at `+10+`, has no damage roll,
   and creates one return beat with no timer or customer-management state.
5. The post-return event makes at most one actual-use damage roll, saves before
   presentation, does not reroll after reload, and keeps mission outcome and
   damage separate.
6. Repair appears only after resolved actual damage; an intact return shows no
   repair CTA; a destroyed item is not offered handoff or repair.
7. Reduced Motion / mute / haptic-off and rapid repeat input cannot change the
   committed resolver result or produce a duplicate result record.

### Exact validation evidence

| Gate | Required evidence |
| --- | --- |
| Source contracts | Existing canon/decision checks plus this document test pass at the exact commit. |
| GDScript | GUT unit/integration tests for milestone, sole Precision, transition, save/no-reroll, no-damage, damage/repair, destroyed, and duplicate-input branches. |
| Runtime | Godot project opens and the 720×1280 route works: First Forge → `+0..+10` → `+11..+15` choice → handoff → return beat → result → conditional repair/return. |
| Human | A player can explain before pressing `+11`: “I can stop with this item, or push for one more level and risk hold/damage.” They can also explain that handoff did not damage the item. |
| Accessibility | Korean copy fits portrait safe area; probability, damage state, and CTA do not rely on colour, motion, or sound alone. |

## 8. Adversarial closure

| Failure assumption | Resolution |
| --- | --- |
| Enhancement was reduced to a feature list. | The contract binds promise → attempt → trade-off → outcome → UID consequence. |
| Five-level beats secretly create more systems. | `+5` is presentation-only; `+10` alone remains Precision/keyword. |
| Customer result becomes a timer or a fake damage tutorial. | One press-through return beat; actual use and real saved result only. |
| Existing runtime drift silently wins. | Vertical Slice only imports current resolvers; legacy multi-precision sources are explicit non-authority. |
| Generated art is mistaken for a completed UI. | No new art is in scope; runtime/human visual proof remains required. |
| Economy hides the risk decision. | Temporary 30-unit reserve guarantees the success-path can reach `+15`; final economy remains unclaimed. |

## 9. Promotion and next gate

```text
BASE_PROMOTION = NO_BASE_PROMOTION
REASON = THE_STOP_PUSH_CADENCE_AND_SAME_UID_CUSTOMER_FLOW_ARE_BLACKSMITH_SPECIFIC
NEXT_ACTION = CLOSE_P0_CONTRACT_REPAIR_THEN_CURRENT_CANON_MVP_TDD_IMPLEMENTATION
```

This contract is the active implementation boundary for the user-declared
current-canon MVP. It does not authorize a player-title system, a concrete
weapon-keyword content row or catalogue before separate user approval, or any
scope outside the current Slice.
