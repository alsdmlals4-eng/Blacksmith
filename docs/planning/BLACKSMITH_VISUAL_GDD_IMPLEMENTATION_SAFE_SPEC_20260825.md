# Blacksmith Visual GDD Implementation-Safe UI Spec · 2026-08-25

- Status: `IMPLEMENTATION_SAFE_PLANNING_SPEC`
- Parent: `BLACKSMITH_APPROVED_VISUAL_GDD_CANON_SCRUB_20260825.md`
- Consumes: six `USER_APPROVED_VISUAL_GDD` boards
- Work Mode: `PLAN`
- `IMAGE_TEXT_NEVER_OVERRIDES_CANON`
- `PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. Core rule

Approved Visual GDDs define **what must be visually understandable**. They do not define runtime values.

```text
Visual GDD
  -> layout / hierarchy / feedback intent

Domain + resolver + content data
  -> names / numbers / availability / actual outcome

UI view-model
  -> presentation-ready canonical values
```

Runtime code must never OCR, parse, sample, or otherwise infer gameplay data from PNGs.

## 2. Authority boundary

```text
IMAGE_TEXT_AUTHORITY = NONE
DOMAIN_DATA_AUTHORITY = CURRENT_STRUCTURED_CANON
RESOLVER_AUTHORITY = CURRENT_RULE_OWNER
VISUAL_AUTHORITY = USER_APPROVED_VISUAL_GDD
```

When an approved image and current structured canon disagree:

```text
visual layout survives where possible
current canon value/meaning wins
conflicting raster text is ignored
```

## 3. Data-owner map

| UI concern | Current owner |
|---|---|
| target band | `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md` Decision15 |
| base success / attempt gold | `BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md` Decision17 |
| failure family | overlay Decision13 |
| CURRENT/MAX / structural state | `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` |
| reinforcement material | `BLACKSMITH_COMMON_RESOURCE_SUPPLY_CANON_20260824.md` |
| repair cost / fatigue | `BLACKSMITH_LATE_REPAIR_ECONOMY_CANON_20260824.md` |
| onboarding order | `BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md` |
| customer context | `BLACKSMITH_PRECISION_CUSTOMER_LINK_CANON_20260824.md` |
| Nadia identity | `data/vertical_slice/customers/nadia_venn.json` |
| +100 terminal | `BLACKSMITH_MAX_LEVEL_PAYOFF_CANON_20260824.md` |

## 4. Shared view-model requirements

All screens that render an item should consume a stable item identity rather than visual placeholder text.

```text
ItemIdentityVM
- item_uid
- display_name
- crafting_grade
- enhancement_level
- primary_material
- physical_lifecycle
```

If a field has no current exact source, the UI must either omit it or show approved non-numeric copy. Do not invent a value to fill the layout.

---

# 5. Enhancement Main VM · `BS-VIS-20260820-01`

## Required semantic fields

```text
EnhancementDecisionVM
- item: ItemIdentityVM
- current_level
- target_level
- target_band
- highest_checkpoint
- next_checkpoint
- base_success_rate
- recovery_bonus_pp
- max_structure_success_modifier_pp
- final_success_rate
- attempt_gold_cost
- reinforcement_material_required
- current_durability
- max_durability
- max_structure_state
- new_enhancement_effect_multiplier
- failure_outcomes[]
- structural_scar_probability_per_attempt
- structural_scar_loss_range
- stop_action
- push_action
```

### UI binding rules

- `final_success_rate` is the prominent player-facing rate.
- `base_success_rate`, recovery, and MAX modifier belong in detail disclosure, not duplicate headline numbers.
- `attempt_gold_cost` and `reinforcement_material_required` are separate mandatory costs.
- `current_durability` and `max_durability` are never merged.
- `failure_outcomes[]` must be sourced from current failure-family rules.
- first structural-risk decision is `current_level=10 / target_level=11`.

```text
TARGET +11 = FIRST_STOP_POINT
```

### CTA semantics

Generic enhancement can use concise STOP/PUSH wording. At the first-stop tutorial decision, the approved semantic copy is:

```text
STOP  = 이 작품을 지킨다
PUSH  = +11에 도전한다
```

Exact final copy may be polished later, but both actions remain legal progression.

---

# 6. DDD Feedback Presentation · `BS-VIS-20260820-02`

DDD presentation reads current target band; it must not own probability thresholds.

```text
FeedbackContext
- target_band
- success_or_failure
- failure_family_if_any
- structural_scar_occurred
- checkpoint_reached
- max_completion_reached
- reduced_motion_enabled
```

Required presentation sequence:

```text
anticipation
-> impact
-> result
-> next_question
```

Relative intensity should rise when the decision is materially more consequential, but **exact time, shake, flash, camera, and audio amplitude are not yet canonical**.

Do not encode generated `0.6s / 0.8s / 1.2s / 1.8s / 2.0s+` values as constants.

Current gameplay bands:

```text
LEARN +1~+2
BUILD_CONFIDENCE +3~+10
FIRST_STOP_POINT +11
TENSION +12~+30
HIGH_STAKES +31~+60
MASTERY +61~+100
```

Accessibility requirement: risk level cannot be communicated only by color, flash, or shake. Reduced-motion mode must retain information via copy/icon/frame/state changes.

---

# 7. First 10 Minutes State Machine · `BS-VIS-20260820-05`

```text
ONBOARDING_00_WORKSHOP
-> ONBOARDING_01_FIRST_CRAFT
-> ONBOARDING_02_LEARN_1_2
-> ONBOARDING_03_BUILD_3_9
-> ONBOARDING_04_PRECISION_10
-> ONBOARDING_05_FIRST_STOP_PREVIEW_11
-> ONBOARDING_06_STOP_OR_PUSH
-> ONBOARDING_07_ACTUAL_OUTCOME
-> ONBOARDING_08_NADIA_ACK
-> CORE_THESIS_FIRST_SESSION_COMPLETE
```

The delayed expedition result is **not** a required state before first-session completion.

```text
DELAYED_RESULT = POST_FIRST_10_MINUTES_SCHEDULE
```

### Invariants

```text
NO_SCRIPTED_FAILURE
NO_HIDDEN_SUCCESS_BOOST
NO_TUTORIAL_ONLY_ODDS
NO_FORCED_+11
CHECKPOINT_IS_DOWNGRADE_FLOOR_NOT_SAVE_POINT
```

The runtime `ITEM_UID` must persist across craft, enhancement, STOP/PUSH result, handoff, delayed result, repair/detail, and lifecycle history.

Any generated UID, reward, trust, reputation, or exact dialogue on the Visual GDD is a `VARIABLE_PLACEHOLDER` until an owner supplies it.

---

# 8. Durability VM · `BS-VIS-20260820-06`

```text
DurabilityVM
- current
- max
- is_destroyed
- max_structure_state
- max_success_modifier_pp
- new_effect_multiplier
- repair_available
- overhaul_available
```

Core invariant:

```text
0 <= CURRENT <= MAX <= 100
```

Destruction:

```text
is_destroyed = (CURRENT == 0) OR (MAX == 0)
```

Normal repair:

```text
NORMAL_REPAIR: CURRENT = MAX
MAX = unchanged
```

Structural state owner:

```text
MAX determines structure state
```

Current test-budget table:

```text
MAX 81~100 -> STABLE    /  0pp / new effect 100%
MAX 61~80  -> STRESSED  / -3pp / new effect 100%
MAX 41~60  -> DAMAGED   / -6pp / new effect 95%
MAX 21~40  -> FRACTURED / -10pp / new effect 90%
MAX 1~20   -> CRITICAL  / -15pp / new effect 80%
MAX 0      -> DESTROYED
```

These numbers remain current planning/test-budget values, not final release balance.

The UI must not imply that MAX damage retroactively reduces stats already earned.

---

# 9. Repair Decision VM · `BS-VIS-20260820-09`

```text
RepairDecisionVM
- item: ItemIdentityVM
- current_before
- max_before
- current_after
- max_after
- gold_cost
- reinforcement_material_required
- workshop_fatigue_cost
- continue_without_repair_allowed
- continue_without_repair_risk_summary
```

Canonical result:

```text
current_after = max_before
max_after = max_before
```

Player-facing payment:

```text
GOLD + 보강재
```

```text
PLAYER_REPAIR_MATERIAL = 보강재
```

Gold cost owner:

```text
missing = MAX - CURRENT
R = 800 * material_structure_multiplier * secured_band_multiplier
gold_cost = round(R * (0.05 + 0.65 * missing / 100))
reinforcement_material_required = max(1, ceil(missing / 25))
workshop_fatigue_cost = 2
```

### Success-rate guard

Normal repair changes CURRENT, not MAX. Current success penalties are MAX-based.

```text
REPAIR_DOES_NOT_CHANGE_SUCCESS_RATE_WHEN_MAX_UNCHANGED
```

Do not show a green success-rate increase caused solely by CURRENT repair.

Instead, explain the real benefit: more CURRENT buffer and lower immediate risk of reaching CURRENT 0 after future damage.

---

# 10. Precision Customer Context VM · `BS-VIS-20260824-10`

```text
CustomerContextVM
- customer_id
- content_id
- public_name
- public_role
- public_epithet
- public_standing_grade
- primary_need
- secondary_need
- known_context[]
- current_total_weight
- maximum_load_if_available
- hard_load_gate_state
- required_function_if_explicit
- direct_help_reasons[]
- gate_changes[]
- tradeoffs[]
- unrelated_reasons[]
- approximate_primary_estimate_if_assignable
```

Current starter:

```text
customer_id = NADIA_VENN
content_id = ADVENTURER_01
content_goal = SURVIVAL_AND_RECOVERY
primary_need = SAFE_RETURN
secondary_need = RECOVERY_POSSIBILITY
required_function_if_explicit = NONE
```

Nadia exact numeric profile remains unresolved:

```text
NADIA_NUMERIC_CAPABILITY = SEPARATE_CANON_SOURCE_REQUIRED
```

Therefore `maximum_load_if_available` is nullable until the real numeric owner exists.

### Decision order

```text
1. HARD GATE
2. enhancement bounded contribution
3. relevant precision/function fit
4. small ability/proficiency context if real data exists
```

Current test-budget contribution:

```text
round(0.30 * enhancement_level) pp
```

No total fit score is created from `direct_help / gate_change / trade-off / unrelated` rows. Generated `3/5`, `2/5`, `1/5`, `7/20`, attack deltas, and expedition numbers are not runtime values.

### Delayed result VM

```text
CustomerDelayedResultVM
- customer_id
- item_uid
- EXPEDITION_RETURN_STATE
- RECOVERY_STATE
- ITEM_UID_LIFECYCLE_STATE
- causal_reasons[2..4]
- primary_next_action
```

Preview cannot reveal future resolved result.

---

# 11. +100 terminal presentation

If an enhancement success reaches +100:

```text
MAX_ENHANCEMENT_COMPLETE
MAX_ENHANCEMENT_REACHED = true
```

Presentation is one-time and distinct, but grants no automatic power/heal/reset beyond the already-resolved +100 enhancement result.

The DDD layer must not map this to an invented probability tier or prestige loop.

---

# 12. Runtime consumption rules

Implementation, when the project gate opens, should follow this pattern:

```text
resolver/domain -> view-model adapter -> UI scene
```

Do not:

```text
PNG -> OCR -> UI values
Visual GDD number -> hardcoded constant
Visual GDD quest line -> content canon
Visual GDD portrait -> final release asset without separate approval
```

Suggested separation:

```text
DOMAIN
- item / durability / enhancement / customer result

RESOLVERS
- enhancement
- repair
- precision/customer context
- delayed Nadia result

VIEW-MODEL ADAPTERS
- EnhancementDecisionVM
- DurabilityVM
- RepairDecisionVM
- CustomerContextVM

UI
- renders approved hierarchy and style
```

## 13. Verification contract for future implementation

Automated tests must eventually prove:

- target +11 is FIRST_STOP_POINT
- final success displayed equals resolver output
- checkpoint does not mutate success/recovery/CURRENT/MAX
- normal repair produces CURRENT=MAX and leaves MAX unchanged
- repair uses gold + `common_reinforcement_material`
- normal repair alone does not change success probability when MAX is unchanged
- MAX band drives structure penalty
- CURRENT==0 or MAX==0 destroys the physical item
- first-session PUSH uses actual result, not scripted success
- Nadia hard gate executes before soft estimate
- no exact Nadia numeric capability is invented
- no total fit score / Best badge
- delayed result is schedule-driven and same-UID

Human/device tests must separately prove readability, timing, reduced-motion/accessibility, and first-session comprehension.

## 14. Evidence ceiling

```text
CANON_SCRUB = COMPLETE
IMPLEMENTATION_SAFE_SPEC = COMPLETE
RUNTIME_IMPLEMENTATION = NOT_RUN
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
HUMAN_PLAYTEST = NOT_RUN
ANDROID = NOT_RUN
ACCESSIBILITY = NOT_RUN
PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION
```
