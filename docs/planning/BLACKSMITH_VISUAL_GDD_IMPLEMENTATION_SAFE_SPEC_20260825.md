# Blacksmith Visual GDD Implementation-Safe UI Spec · 2026-08-25

- Status: `IMPLEMENTATION_SAFE_PLANNING_SPEC / REBOUND_TO_CORE_SIMPLIFICATION`
- Current gameplay owner: `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- Current art owner: `BS-ART-20260825-03 / ILLUSTRATED_WORKSHOP_BOOK`
- Consumes: the 8 previously user-approved explanatory Visual GDD boards **for information architecture only** plus the user-selected Illustrated Workshop Book style evidence.
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. Authority boundary

```text
VISUAL -> layout / hierarchy / interaction intent / visual-language reference
CURRENT GAME CANON -> values / states / eligibility / probability / results
```

Never resolve gameplay by reading a rasterized image.

```text
IMAGE_TEXT_AUTHORITY = NEVER
RUNTIME_IMAGE_PARSING = FORBIDDEN
PNG_OCR_TO_GAME_LOGIC = FORBIDDEN
```

The previously approved boards remain useful references for questions such as:

- where the item hero belongs;
- how STOP/PUSH actions separate;
- how risk and cost are foregrounded;
- how state change is shown with icon/text/shape redundancy;
- how customer context and same-UID causality are presented.

Their old CURRENT/MAX, five structural bands, MAX penalties, dated enhancement rows, and multi-precision wording are not current semantics.

## 2. Current mechanic contract for all future Visuals

### Enhancement

```text
SUCCESS_LEVEL_DELTA = +1
TARGET_LEVEL = CURRENT_LEVEL + 1
NO_MULTI_LEVEL_SUCCESS
```

Every enhancement surface must show exactly the next level. Do not show multi-level jump rewards.

### Precision / keyword

```text
+9 -> +10 = ONLY_PRECISION_ENHANCEMENT
SUCCESS +10 -> ITEM_KEYWORD exactly one
ITEM_KEYWORD machine owner = CATALYST_AFFIX
NO_FOURTH_AFFIX_SLOT
```

Normal enhancement UI is used for all other targets.

### Damage

```text
NORMAL -> MINOR -> MAJOR -> DESTROYED
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE
CURRENT_MAX_AUTHORITY = SUPERSEDED
```

Do not show CURRENT/MAX bars, MAX percentages, STABLE/STRESSED/DAMAGED/FRACTURED/CRITICAL five-band state, MAX penalty, or structural-scar multipliers as current UI.

### Enhancement damage gate

```text
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
MONOTONIC_NON_DECREASING_DAMAGE_RISK
```

Until exact probabilities are approved:

- +10-or-below screen must not imply damage from enhancement failure;
- +11+ screen can say damage is possible;
- do not invent an exact damage percent;
- high-level risk can increase in wording/icon/frame emphasis as target rises, but visual emphasis must not pretend to be a numeric probability scale.

### Customer/world damage

```text
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
```

Customer handoff/purchase UI must not show automatic wear. Event-result UI can show a one-step damage delta only when the actual event resolver/content owner produced it.

### Chronicle

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY
```

No default timeline of `+6 success / 25 days ago`, etc. Internal timestamps can exist without player-facing routine rows.

## 3. Current art direction · Illustrated Workshop Book

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

Visual grammar:

- hand-drawn workshop notebook / field-guide feeling;
- paper, leather, iron, wood, graphite/ink and restrained wash material cues;
- warm localized forge atmosphere, not full-screen orange glow;
- large functional shapes before micro-decoration;
- modern readable Korean text hierarchy even when frames look handmade;
- item/workpiece remains the visual hero;
- states use text + icon/shape/mark redundancy, not color alone;
- ornament budget is limited and tied to workshop tools, maker marks, paper clips, stamps, sketches, or material evidence;
- generated pseudo-text, random runes, gratuitous black/gold fantasy filigree, and dense AI-style annotation clutter are forbidden.

## 4. Representative screen set after mechanic sync

Do not bulk-regenerate all old Visuals. Validate these five first.

### 4.1 Main Menu

Purpose:

```text
identity + resume/new-game entry + workshop fantasy
```

Requirements:

- hand-drawn workshop environment or notebook/workbench framing;
- title readable without ornate gold treatment;
- primary actions unmistakable;
- Modak may act as warm companion if consistent with approved mascot direction;
- no CURRENT/MAX or system-heavy diagnostic information.

### 4.2 Enhancement Main · ordinary +1

Player question:

> 이번 +1 시도를 할 것인가, 멈출 것인가?

P0 information:

```text
item identity / current enhancement
next target = current + 1
final success expectation
cost = gold + reinforcement material
current DamageState
failure outcome summary
recovery state when relevant
STOP / ENHANCE(+1)
```

For target <=+10, do not list enhancement-damage risk.
For target >=+11, disclose `실패 시 손상 가능`; exact percent only after approved curve exists.

### 4.3 +9 -> +10 Precision Keyword

P0:

```text
current +9 -> target +10
material context
method
one catalyst
compatible keyword direction / trade-off
success expectation
cost
success creates one ITEM_KEYWORD
```

No later Precision milestone teaser implying +20/+30/+40/+50 repeat.

### 4.4 Four-state Damage / Repair decision

P0 state display:

```text
NORMAL
MINOR
MAJOR
DESTROYED
```

Use at least two non-color signals among text, icon silhouette, cracks/marks, edge treatment, stamp, paper note, item drawing change.

Repair action is `PENDING_NEW_REPAIR_MODEL`. Do not draw exact repair cost or exact state recovery until approved.

### 4.5 Event-only Item Chronicle

Show meaningful events such as:

```text
제작됨
+10 정밀강화 키워드 획득
경미/중대 손상 사건
중요 수리 (future approved model)
고객 인계
고객/세계 결과
파괴
Memorial / successor relation
```

Do not pad the page with every enhancement click or relative-day labels for routine attempts.

## 5. Previous approved Visual GDD status

| Visual ID | Prior role | Current safe use |
|---|---|---|
| `BS-VIS-20260820-01` | Enhancement Main | `LAYOUT_REFERENCE`; values/states must be regenerated |
| `BS-VIS-20260820-02` | DDD Feedback Ladder | `FEEDBACK_REFERENCE`; remove old damage-family semantics |
| `BS-VIS-20260820-04` | Tension Band Matrix | `HIERARCHY_REFERENCE`; no old damage %/CURRENT/MAX |
| `BS-VIS-20260820-05` | First 10 Minutes | `FLOW_REFERENCE`; +10 keyword/+11 damage gate needs regeneration |
| `BS-VIS-20260820-06` | CURRENT/MAX | `SYSTEM_SEMANTICS_STALE`; do not implement dual durability |
| `BS-VIS-20260820-08` | MAX Penalty | `SYSTEM_SEMANTICS_STALE`; no current MAX penalty system |
| `BS-VIS-20260820-09` | Repair Decision | `LAYOUT_REFERENCE`; repair semantics/cost pending |
| `BS-VIS-20260824-10` | Precision -> Customer Context | `CAUSAL_LAYOUT_REFERENCE`; precision cadence must be +9->+10 only |

These existing Asset records remain historical/user-approved explanatory references; `Approved=true` does not mean their old system text is current game canon or current product art.

## 6. Data binding contract

Runtime/UI implementation after the product Gate opens must bind to structured view models, never image text.

Proposed semantic properties:

```text
item.uid
item.enhancement_level
item.item_keyword
item.damage_state
item.physical_state

EnhancementPreview.target_level
EnhancementPreview.final_success_percent
EnhancementPreview.gold_cost
EnhancementPreview.reinforcement_units
EnhancementPreview.damage_possible
EnhancementPreview.damage_probability_percent?  # only after approval
EnhancementPreview.recovery

CustomerResult.item_uid
CustomerResult.result_axes
CustomerResult.causal_reasons
CustomerResult.damage_state_before?
CustomerResult.damage_state_after?
CustomerResult.primary_next_action
```

Question-mark fields are optional until their owner is approved/implemented.

## 7. Accessibility / mobile

For Android portrait:

- important state name is written, not only colored;
- primary actions target ≥48dp in implementation;
- paper texture cannot reduce text contrast below acceptable readability;
- handwritten decorative lettering is not used for dense body text;
- damage state needs semantic text plus shape/icon signal;
- STOP vs PUSH/ENHANCE must remain distinguishable in grayscale;
- actual client/device validation remains `NOT_RUN` until observed.

## 8. Forbidden implementation interpretations

```text
read numbers from approved PNG
restore CURRENT/MAX because old Visual has two bars
restore +20/+30/+40/+50 Precision because old Visual mentions milestones
show exact +11+ damage % before approval
make purchase itself damage an item
reuse old MAX penalty table for MINOR/MAJOR
show routine dated enhancement rows as Chronicle canon
add a fourth keyword/affix slot
copy old black/gold ornament into the new current style
```

## 9. Current unresolved visual inputs

```text
DAMAGE_PROBABILITY_CURVE = NOT_FINAL
MINOR_MAJOR_REPAIR_MODEL = NOT_DECIDED
CUSTOMER_EVENT_DAMAGE_POLICY = NOT_FINAL
MAJOR_ENHANCEMENT_ELIGIBILITY = NOT_DECIDED
```

The representative Visual set can be regenerated only to the level supported by these decisions. Missing numbers must be omitted/placeholder-labelled rather than invented.

## 10. Evidence ceiling

```text
ART_DIRECTION_SELECTION = USER_APPROVED
REPRESENTATIVE_STYLE_BOARD = HUMAN_APPROVED_DIRECTION_EVIDENCE
CURRENT_SYSTEM_VISUAL_REGENERATION = NOT_RUN_AFTER_MECHANIC_SYNC
PRODUCT_ASSET_APPROVAL = NOT_GRANTED
RUNTIME_BINDING = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_RENDER = NOT_RUN
```
