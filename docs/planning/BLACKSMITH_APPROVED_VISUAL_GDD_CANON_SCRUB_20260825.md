# Blacksmith Approved Visual GDD Canon Scrub · 2026-08-25

- Status: `CANON_SCRUB_COMPLETE / IMPLEMENTATION_SAFE_REFERENCE`
- Work Mode: `PLAN`
- Baseline Blacksmith main: `2c84793773e74a5b4cdcf9888f972d664d2b8060`
- Base main fresh-read: `3c3376845b9a1b7921a4260aa6259cd61533ffc4`
- User-approved Visual GDDs: `6`
- `STYLIZED_DARK_FORGE = CURRENT`
- `IMAGE_TEXT_NEVER_OVERRIDES_CANON`
- `PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Human / Android / accessibility / runtime validation: `NOT_RUN`

## 1. Why this scrub exists

The six generated boards are approved **visual explanations**. Their layout, information hierarchy, visual language, and explanation density are useful, but generative images also contain illustrative numbers, names, copy, and inferred states that were never promoted into Blacksmith product canon.

This scrub separates those two layers so implementation cannot accidentally treat rasterized example text as game data.

```text
APPROVED VISUAL GDD
= layout / hierarchy / visual language / explanatory intent

CURRENT CANON
= GitHub planning canon + structured current data

IMAGE_TEXT_NEVER_OVERRIDES_CANON
```

The images remain approved. This task does **not** regenerate them and does **not** downgrade their visual approval.

## 2. Classification vocabulary

| Class | Meaning | Implementation rule |
|---|---|---|
| `KEEP` | Approved visual structure or semantic presentation | Preserve unless later user decision changes it |
| `CANON_VALUE` | Meaning is valid but the displayed value must come from current canon/runtime | Bind to the owning resolver/data source; never bake the image value |
| `VARIABLE_PLACEHOLDER` | Illustrative name, number, copy, timing, UID, portrait detail, or scene content with no current exact canon | Replace with runtime/content data or approved copy later |
| `CONFLICT_REMOVE` | Generated example contradicts current canon | Must not be implemented; spec below supplies the current rule |

## 3. Authority used for the scrub

Primary current owners:

1. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
2. `docs/planning/BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md`
3. `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md`
4. `docs/planning/BLACKSMITH_COMMON_RESOURCE_SUPPLY_CANON_20260824.md`
5. `docs/planning/BLACKSMITH_LATE_REPAIR_ECONOMY_CANON_20260824.md`
6. `docs/planning/BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md`
7. `docs/planning/BLACKSMITH_PRECISION_CUSTOMER_LINK_CANON_20260824.md`
8. `data/vertical_slice/customers/nadia_venn.json`

The release-near canon remains useful implementation context, but the **current reactivated planning overlay and project state keep product implementation blocked** until the current planning-complete declaration.

## 4. Global scrub result

### KEEP globally

- `STYLIZED_DARK_FORGE`
- dark forge materiality + warm localized furnace light
- dark iron / brass UI language
- item / workpiece / decision as visual focus
- mobile portrait screen as the main product surface
- explanatory Visual-GDD density rather than decorative concept art
- non-color redundancy for risk / durability / state
- explicit STOP/PUSH decision language
- `anticipation -> impact -> result -> next question` as DDD sequence

### CANON_VALUE globally

The following may be shown in UI, but the image number is never authority:

- enhancement level / target level
- base and final success expectation
- recovery
- attempt gold cost
- reinforcement-material quantity
- CURRENT / MAX
- MAX structure state and penalties
- failure-family result and structural-scar risk
- repair gold/material cost
- customer load gate and context result
- any reward, market, relationship, progression, or delayed-result number

### VARIABLE_PLACEHOLDER globally

- `용사의 검` and other illustrative item names
- example UIDs such as `#NV-0001` or `WPN-SWD-000127`
- generated NPC dialogue
- generated scene/quest names not present in canon
- exact animation durations and camera values
- illustrative currency/resource inventories
- illustrative customer ability/proficiency numbers
- illustrative reward / trust / reputation values
- generated portraits as final runtime character art

### CONFLICT_REMOVE globally

- any image value that contradicts current target-level bands, success curve, repair rules, resource mapping, customer rules, or delayed-result timing
- any checkpoint representation as a save/restore checkpoint
- any success-only tutorial result
- any generated total suitability / hidden score
- any normal-repair claim that MAX or success probability is restored by repairing CURRENT

---

# 5. `BS-VIS-20260820-01` · 강화 메인 화면

## KEEP

- central item-first mobile enhancement screen
- `현재 단계 -> 다음 단계`
- final success expectation near the primary decision
- attempt cost and failure risk before commitment
- separate `CURRENT` and `MAX`
- large STOP/PUSH CTAs
- separate visual examples for normal attempt / risk entry / hold / damage / success / milestone

## CANON_VALUE

```text
current_level
TARGET_LEVEL
target_band
final_success_rate
attempt_gold_cost
required_common_reinforcement_material
CURRENT
MAX
failure_family_summary
structural_scar_risk_per_attempt
structural_scar_loss_range
same_target_recovery
next_checkpoint
```

These must be supplied by current domain/resolvers.

## CONFLICT_REMOVE

### A. First-risk level shown around +9 -> +10

Current canon:

```text
CURRENT +10 = FIRST_ECONOMIC_STOP_STATE
TARGET +11 = FIRST_STOP_POINT
```

Therefore:

```text
TARGET +11 = FIRST_STOP_POINT
```

The first structural-risk preview must be the `+10 -> +11` decision, not a generated `+9 -> +10` risk card.

### B. Generated success rates such as `63%`, `32%`, `35% -> 40%`

Do not implement them.

Current base anchors include:

```text
TARGET +10 base = 86%
TARGET +11 base = 82%
```

The UI must show the **final resolver output**, after applicable current recovery/MAX modifiers, not a raster number.

### C. Generated attempt costs such as `2,850` / `4,500`

Do not implement them. Current owner:

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)
```

Current representative values:

```text
TARGET +10 = 830G
TARGET +11 = 990G
```

Both also consume current `보강재` mapping.

### D. Milestone success-rate bonus

A checkpoint does **not** increase success rate, heal durability, clear recovery, or reset risk.

```text
CHECKPOINT_IS_DOWNGRADE_FLOOR_NOT_SAVE_POINT
CHECKPOINT_BONUS_SUCCESS_RATE = NONE
```

### E. Failure summary limited to `1단계 하락 또는 손상`

Current failure families are:

```text
HOLD / DOWNGRADE / DAMAGE / CRITICAL
```

The screen may summarize major outcomes, but detail must resolve from current band/failure-family data. `CRITICAL` is the path that can scar MAX.

---

# 6. `BS-VIS-20260820-02` · 강화 DDD Feedback Ladder

## KEEP

- risk rises -> feedback intensity rises
- safe repetition remains fast and restrained
- high-risk attempts receive stronger anticipation / impact / result emphasis
- `anticipation -> impact -> result`
- do not use the same giant presentation on every level
- UI readability stays visible during presentation

## CONFLICT_REMOVE

The generated five-stage probability/level ladder is not current canon.

Replace it conceptually with the current **target-level bands**:

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

Current base-success anchors are owned by Decision17 and are not the generated `80~100 / 60~79 / 30~59 / 10~29 / <=5` ladder.

## VARIABLE_PLACEHOLDER

Generated exact presentation times such as `0.6s`, `0.8s`, `1.0~1.2s`, `1.4~1.8s`, `2.0s+`, exact shake amplitudes, flash duration, zoom amount, and SFX loudness are **not approved runtime values**.

They remain qualitative visual examples until Human/accessibility/device validation.

## CANON_VALUE

- target band
- final success expectation
- failure severity possibilities
- MAX state
- checkpoint / +100 terminal status

`+100` also has its own one-time completion presentation through `MAX_ENHANCEMENT_COMPLETE`; do not reduce it to a generated low-probability generic tier.

---

# 7. `BS-VIS-20260820-05` · 첫 10분 DDD Storyboard

## KEEP

Canonical sequence:

```text
New Game
-> short first item
-> +1/+2 LEARN
-> +3~+9 BUILD_CONFIDENCE
-> +10 first precision + checkpoint + break-even anchor
-> +11 structural-risk Preview
-> STOP / PUSH
-> actual canonical outcome
-> short UID / Nadia acknowledgement
-> next question
```

The same item UID must continue through actual outcome and handoff.

## CONFLICT_REMOVE

### A. Success-only `+10 -> +11 성공!`

The first-session result is not scripted.

```text
NO_SCRIPTED_FAILURE
NO_HIDDEN_SUCCESS_BOOST
NO_TUTORIAL_ONLY_ODDS
NO_FORCED_+11
```

PUSH resolves with current real odds and real failure families. STOP and PUSH are both normal completion paths.

### B. Generated success numbers such as `95%`, `65%`, `40%`

Do not implement from the image. Use current resolver values. Current base anchors include `+2 = 97%`, `+10 = 86%`, `+11 = 82%` before current modifiers.

### C. Checkpoint represented as save progress

`+10 checkpoint` means downgrade floor, not save-slot restore semantics.

```text
CHECKPOINT_IS_DOWNGRADE_FLOOR_NOT_SAVE_POINT
```

Save/load is a separate system.

### D. Delayed world result inside the ten-minute promise

First 10 minutes end with the core thesis and Nadia acknowledgement. Full expedition/world resolution is delayed by the existing personal schedule.

```text
DELAYED_RESULT = POST_FIRST_10_MINUTES_SCHEDULE
```

A storyboard may visually show the later consequence as a **future continuation**, but it must not imply immediate completion inside the ten-minute pacing target.

## VARIABLE_PLACEHOLDER

- `#NV-0001` or any example UID
- generated reward `4,500`
- generated trust/reputation values such as `+15`, `+8`
- generated Nadia lines
- generated total workshop stats
- Modak board depiction as final runtime asset

## CANON_VALUE

Human pacing targets from Decision23 remain the current plan, but are `HUMAN_NOT_RUN` and must not become hard countdowns.

---

# 8. `BS-VIS-20260820-06` · CURRENT/MAX 이중 내구도

## KEEP

- two distinct values/gauges for CURRENT and MAX
- physical wear/cracks/frame/icon changes as non-color state signals
- state words `STABLE / STRESSED / DAMAGED / FRACTURED / CRITICAL / DESTROYED`
- repair preview must make `MAX unchanged` explicit

## Critical semantic correction

The generated board describes the six structure states as if they are based on CURRENT ratio. Current canon assigns the structure-state bands and future-enhancement penalties to **MAX**.

```text
MAX determines structure state
```

Current first test budget:

| MAX | State | success modifier | new enhancement effect |
|---:|---|---:|---:|
| 81~100 | STABLE | 0pp | 100% |
| 61~80 | STRESSED | -3pp | 100% |
| 41~60 | DAMAGED | -6pp | 95% |
| 21~40 | FRACTURED | -10pp | 90% |
| 1~20 | CRITICAL | -15pp | 80% |
| 0 | DESTROYED | unavailable | unavailable |

These numeric bands are `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

CURRENT remains the short-term damage buffer.

## CONFLICT_REMOVE

Generated normal-repair examples that stop below MAX, such as `15/80 -> 70/80`, are incompatible with current normal repair.

```text
NORMAL_REPAIR: CURRENT = MAX
MAX = unchanged
```

Also:

```text
CURRENT == 0 OR MAX == 0 -> DESTROYED
```

A MAX-based structure-state display must not hide the separate CURRENT-zero destruction condition.

Already-earned stats/affixes are not retroactively reduced by MAX damage; only newly gained enhancement effect is modified by the current MAX-state budget.

---

# 9. `BS-VIS-20260820-09` · 수리 판단 카드

## KEEP

- Before -> After comparison
- CURRENT and MAX shown separately
- explicit `MAX unchanged`
- gold + material + workshop burden visible before confirmation
- choices `later / repair / continue without repair`
- continuing without repair has visible physical-risk consequences
- no partial slider / no auto-repair default

## CANON_VALUE

```text
missing = MAX - CURRENT
R = 800 * MATERIAL_STRUCTURE_MULTIPLIER * SECURED_BAND_MULTIPLIER
gold_cost = round(R * (0.05 + 0.65 * missing / 100))
required_reinforcement_material = max(1, ceil(missing / 25))
REPAIR_JOB_FATIGUE_COST = 2
NORMAL_REPAIR: CURRENT = MAX
MAX unchanged
recovery unchanged
```

Player-facing material:

```text
PLAYER_REPAIR_MATERIAL = 보강재
```

The primary material (`iron / silver / meteor_iron`) modifies the **gold formula** but is not consumed as the standard repair material.

## CONFLICT_REMOVE

### A. Generated ingot / wood / leather repair recipe

Current ordinary repair requires `보강재`, not a generated three-resource bundle.

### B. Generated partial result such as `18/80 -> 54/80`

Normal repair is not partial.

```text
18/80 -> 80/80  # if the current MAX is 80
```

### C. Generated claim that CURRENT repair raises enhancement success probability

Current success penalty is tied to MAX structure state, not CURRENT. If normal repair changes CURRENT only and MAX is unchanged, the success calculation is unchanged.

```text
REPAIR_DOES_NOT_CHANGE_SUCCESS_RATE_WHEN_MAX_UNCHANGED
```

The benefit of normal CURRENT repair is **more immediate damage buffer / lower chance that a future loss reaches CURRENT 0**, not a hidden success bonus.

### D. Generated fixed `2,850G`

Cost must bind to the current repair formula and current item state. Do not hardcode the image value.

---

# 10. `BS-VIS-20260824-10` · 정밀강화 → 고객 Context

## KEEP

- Nadia is the starter customer anchor
- hard gate before soft estimate
- four non-total-score explanatory categories:
  - `직접 도움`
  - `Gate 변화`
  - `trade-off`
  - `직접 관련 없음`
- no `Best`, no 0~100 fit score, no opaque auto recommendation
- same UID connects later to multi-axis result
- result uses `2~4 causal reasons + primary next action`

## CANON_VALUE

Current starter identity:

```text
CUSTOMER_ID = NADIA_VENN
CONTENT_ID = ADVENTURER_01
CONTENT_GOAL = SURVIVAL_AND_RECOVERY
PRIMARY_NEED = SAFE_RETURN
SECONDARY_NEED = RECOVERY_POSSIBILITY
HARD_LOAD_GATE = CURRENT_TOTAL_WEIGHT <= NADIA_MAXIMUM_LOAD
REQUIRED_FUNCTION_IF_EXPLICIT = NONE
```

Current Nadia structured data says:

```text
NADIA_NUMERIC_CAPABILITY = SEPARATE_CANON_SOURCE_REQUIRED
```

Therefore no exact maximum load, ability score, or proficiency number may be invented by the UI spec.

Current enhancement contribution test budget:

```text
ENHANCEMENT_EVENT_BONUS_PP = round(0.30 * enhancement_level)
```

This remains `NOT_FINAL_PRODUCT_BALANCE`.

## CONFLICT_REMOVE / VARIABLE_PLACEHOLDER

- generated quest such as `잃어버린 기사단의 유물 회수`: `VARIABLE_PLACEHOLDER / NOT_CURRENT_CANON`
- generated weight `7/20`: no current exact Nadia numeric source; remove until data exists
- generated attack `+122 -> +138`: illustrative only
- generated row weights `3/5`, `2/5`, `1/5`: do not implement as hidden suitability score
- generated expedition outcome numbers / duration / reward: illustrative only
- generated portrait: approved Visual GDD reference, not final runtime character asset

First-session boundary:

```text
Nadia handoff
-> acknowledgement from actual choice data
-> PERSONAL_SCHEDULE
-> first-session core thesis may complete

later day progression
-> EXPEDITION_RETURN_STATE
-> RECOVERY_STATE
-> ITEM_UID_LIFECYCLE_STATE
-> causal reasons 2~4
-> same UID next action
```

No future result may be spoiled in the context preview.

---

## 11. Cross-visual implementation invariants

```text
IMAGE_TEXT_NEVER_OVERRIDES_CANON
NO_RUNTIME_OCR_OR_IMAGE_TEXT_PARSING
UI_READS_DOMAIN_AND_RESOLVER_OUTPUTS
TARGET_BAND_IS_TARGET_LEVEL_BASED
TARGET +11 = FIRST_STOP_POINT
CHECKPOINT_IS_DOWNGRADE_FLOOR_NOT_SAVE_POINT
NORMAL_REPAIR: CURRENT = MAX
MAX determines structure state
REPAIR_DOES_NOT_CHANGE_SUCCESS_RATE_WHEN_MAX_UNCHANGED
PLAYER_REPAIR_MATERIAL = 보강재
NADIA_NUMERIC_CAPABILITY = SEPARATE_CANON_SOURCE_REQUIRED
DELAYED_RESULT = POST_FIRST_10_MINUTES_SCHEDULE
```

## 12. Alternatives considered

### A. Implement the approved images literally — REJECT

Fastest visually, but generated values would silently become product rules. This directly violates current authority.

### B. Treat every image field as meaningless placeholder — REJECT

Safe numerically, but throws away the user-approved layout/hierarchy and makes the Visual GDD ineffective as an implementation reference.

### C. Hybrid semantic approval + canonical data binding — ADOPT

Keep visual structure and explanatory intent; bind every mutable/semantic value to current data/resolvers; explicitly blacklist generated conflicts. Lowest long-term drift risk.

### D. Regenerate all six images immediately with scrubbed values — DEFER

Possible later, but not required for implementation safety. Many values are dynamic or test budgets, so a perfectly current raster image would become stale again. The machine-readable binding contract is the durable fix.

## 13. Adversarial review loops

1. **Raster authority inversion** — image numbers could override GitHub. Fixed with `IMAGE_TEXT_NEVER_OVERRIDES_CANON`.
2. **First-risk inversion** — generated +9/+10 risk panel contradicted target +11 FIRST_STOP_POINT. Corrected.
3. **Repair semantic drift** — generated partial repair/material bundle/success uplift contradicted CURRENT repair canon. Corrected.
4. **Durability owner confusion** — generated structure states looked CURRENT-based; current penalties are MAX-based. Corrected.
5. **Tutorial rigging** — success-only storyboard could imply forced +11 success. Replaced by actual resolver branch.
6. **Customer score invention** — generated weights/quest/load values could become hidden fit score or invented Nadia data. Blocked.
7. **Evidence overclaim** — Visual approval is not runtime/device/accessibility/product-asset approval. Boundary retained.

## 14. Implementation Reality Gate

```text
VISUAL_GDD_USER_APPROVAL = VERIFIED
CANON_SCRUB = DOCUMENTED
IMPLEMENTATION_SAFE_BINDING_SPEC = DOCUMENTED
RUNTIME_MUTATION = NOT_RUN
LOCAL_GODOT_EDITOR = NOT_RUN
ANDROID_DEVICE = NOT_RUN
ACCESSIBILITY = NOT_RUN
HUMAN_PLAYTEST = NOT_RUN
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION
```

## 15. Next planning bundle after this scrub

The remaining P0 Visual gaps can now be reviewed without letting old raster numbers define mechanics:

1. `BS-VIS-20260820-04` · current target-band screen states
2. `BS-VIS-20260820-08` · MAX structural penalty comparison
3. then P1 `BS-VIS-20260820-03` / `07` for item-history damage and destruction/archive presentation

No implementation gate is opened by this scrub alone.
