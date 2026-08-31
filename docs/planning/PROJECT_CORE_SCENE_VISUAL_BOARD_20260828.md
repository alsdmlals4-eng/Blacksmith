# PROJECT_CORE_SCENE_VISUAL_BOARD · Enhancement-first Slice B · current supplement 2026-08-30

## 1. Artifact identity

```text
ARTIFACT_CLASS = PLANNING_VISUALIZATION_ONLY
PURPOSE = AI_UNDERSTANDING_CHECK + USER_FLOW_REVIEW + VISUAL_DIRECTION_CONFIRMATION
RUNTIME_ASSET_STATUS = NOT_A_RUNTIME_ASSET
GODOT_SCENE_STATUS = NOT_A_GODOT_SCENE
HUMAN_USABILITY_STATUS = NOT_RUN
CURRENT_VISUAL_REQUIREMENTS = docs/planning/BLACKSMITH_RECURRING_PRECISION_VISUAL_REQUIREMENTS_20260830.json
GENERATED_CANDIDATES = MAIN_MENU + WORKSHOP_RECURRING_PRECISION + CUSTOMER_WORLD_RESULT
RUNTIME_PROMOTION = BLOCKED_PENDING_USER_LOCK
TARGET_PLAYER_TIME = 6_TO_8_MINUTES / PHASE_1_HYPOTHESIS
```

This is a structured planning board, not a group of implemented screens,
runtime images, generated fake screenshots, or a Human/Player Experience
pass. Exact descriptions belong to this structured text and the current
machine owners, never to pseudo-text inside an image.

The target measures a first player’s active path from committing to the item
through one same-UID customer actual-use result. It is a playtest hypothesis,
not a timer, a speedrun target, or a reason to batch/skip approved individual
enhancement feedback.

```text
FIVE_LEVEL_CRAFT_RHYTHM = EVERY_5_LEVEL_PRESENTATION_RISE / EVERY_10_LEVEL_PRECISION_TAG_GROWTH
```

The five-level rhythm marks cumulative crafting satisfaction without inventing
new systems. `+5` is a presentation-only rise; `+10`, `+20`, through `+100`
combine that rise with Precision Tag growth. The intervening five-level rises
must not reopen Precision or create extra affixes.

## 2. Slice B at a glance

```mermaid
flowchart TD
    A[01 Main Menu\nCommit to one workpiece] --> B[02 First Forge\nCreate one UID]
    B --> C[03 Enhancement Main\nordinary +1 feedback]
    C --> D[04 Recurring Precision Tag Choice\n+9→+10 through +99→+100]
    D -->|SUCCESS +1 / HOLD / DAMAGE| C
    C -->|Stop or handoff| H[Return Beat\nOne brief non-economic workshop moment]
    H --> E[05 Customer World Result\nOne same-UID actual-use result]
    C -->|Actual enhancement damage and eligible job| F[06 Repair and Chronicle\nOne eligible repair decision]
    E --> F
    F --> C
```

Every target remains a voluntary decision beat, not a forced outcome. At target
`10` the player adds the first Tag; at later ten-level targets the player adds
one Tag or advances one active Tag. There are at most three active Tags and all
successes remain exactly `+1`.
Customer actual use and damage remain independent axes. A demonstration must
not script damage simply to make the repair panel appear.

```text
POST_HANDOFF_TRANSITION = ONE_WORKSHOP_RETURN_BEAT
NO_FAKE_WAITING_OR_CUSTOMER_MANAGEMENT_SYSTEM = TRUE
```

The return beat creates a small sense of departure and return inside the
6–8-minute Slice. It does not add a timer, a customer list, a second item,
or a new economy action.

## 3. Panel contracts

### PANEL_01 = MAIN_MENU

| Field | Contract |
|---|---|
| Actual consumer | `res://scenes/vertical_slice/main_menu.tscn#MenuIllustratedBackground`; `VIS-REC-20260830-01` is generated candidate only, with runtime binding blocked pending user lock. |
| Player goal / action | Begin a first item journey; choose to enter First Forge. |
| Meaningful choice | None yet; this is commitment and expectation-setting, not a fake early game decision. |
| Required information | One workpiece can gain a history through enhancement, use, damage, and repair. |
| Feedback / emotion | Warm workshop invitation and anticipation. |
| Next | First Forge. |
| Current canon evidence | `PRIMARY_PLAYABLE_CONTENT = REPEATED_ENHANCEMENT_JUDGMENT_AND_FEEDBACK`. |
| Undecided | Final title copy, onboarding language, actual mobile layout/readability. |

### PANEL_02 = FIRST_FORGE

| Field | Contract |
|---|---|
| Actual consumer | First Forge dynamic background in `res://scripts/ui/forging_screen.gd`; downstream item handoff evidence exists. |
| Player goal / action | Create the single item UID that will carry the Slice. |
| Meaningful choice | The approved Slice does not invent a new craft-selection system here. Its purpose is ownership of the future enhancement subject. |
| Required information | The freshly forged item, starting level, and why it can become personally meaningful. |
| Feedback / emotion | A small ownership beat: “this is my workpiece,” not a reward substitute for enhancement. |
| Next | Enhancement Main. |
| Current canon evidence | UID persists through crafting, ownership, durability, repair, destruction archive, and world consequence. |
| Undecided | Starter item presentation and final forge interaction details. |

### PANEL_03 = ENHANCEMENT_MAIN

| Field | Contract |
|---|---|
| Actual consumer | `res://scenes/vertical_slice/screens/vs_workshop_screen.tscn`; existing workshop background and durability-atlas bindings. |
| Player goal / action | Enjoy individual ordinary enhancement feedback between ten-level Precision thresholds; reach the next voluntary Precision choice. |
| Meaningful choice | Continue a satisfying growth rhythm or preserve resources/stop. This is lower tension than the later risk run and must not falsely imply damage eligibility before `+11`. |
| Required information | Same item UID, current target, resource/cost state where implemented, visible `CURRENT / MAX / BASE_MAX`, and legible normal enhancement outcome. |
| Feedback / emotion | Crisp +1 confirmation, workpiece progression, a stronger craft-rise at each +5, then anticipation for the next ten-level Tag choice. |
| Next | Recurring Precision Tag Choice at `target - 1 -> target`, for target `10..100` in steps of 10. |
| Current canon evidence | Every ordinary success is exactly `+1`; enhancement damage is zero through target `+10`. |
| Undecided | Final attempt timing, resource pacing, audio/VFX, target-resolution UI composition. |

### PANEL_04 = RECURRING_PRECISION_TAG_CHOICE

| Field | Contract |
|---|---|
| Actual consumer | Dynamic recurring state inside `res://scripts/vertical_slice/ui/vs_workshop_screen.gd`; `VIS-REC-20260830-02` is generated candidate only and has no runtime binding until user lock. |
| Player goal / action | At each `target - 1 -> target` where target is `10,20,...,100`, choose exactly one action: first `+10` adds a Tag; later targets add a Tag or advance an active Tag. |
| Meaningful choice | Preserve the current item or make a disclosed choice before the attempt. On success the same UID gains exactly `+1` and exactly the chosen Tag growth; `FAILED_HOLD` or conditional `FAILED_DAMAGE` changes no Tag growth. |
| Required information | Exact success / hold / damage final-outcome probabilities; target level; active Tags and stages I–IV; candidate effect preview; visible durability state; repair consequence only when actually eligible. |
| Feedback / emotion | Every ten levels is a material authorship beat: a new Tag or a more mature existing Tag, without a fourth affix or player title. |
| Next | Handoff → one brief Workshop Return Beat → Customer World Result, or conditional Repair and Chronicle after actual damage. |
| Current canon evidence | Decision38 owns targets `10..100`, max three active Tags, stages I–IV, and success-only action-local growth. Three-affix taxonomy remains; failure is exclusively HOLD or DAMAGE; Decision28/29 own risk. |
| Undecided | Final probability copy, animation and audio language, costs, exact one-hand UI arrangement. |

### PANEL_05 = CUSTOMER_WORLD_RESULT

| Field | Contract |
|---|---|
| Actual consumer | `res://scenes/vertical_slice/screens/vs_customer_result_screen.tscn` and stored-result service evidence; `VIS-REC-20260830-03` is generated candidate only and has no runtime binding until user lock. The approved return beat and player-facing scheduler/entry remain `NOT_RUN`. |
| Player goal / action | See how the previously enhanced same UID performed in actual use; relate result to the item’s history. |
| Meaningful choice | The meaningful choice happened during enhancement and handoff. This panel explains consequence; it must not add a new unapproved customer-management system. |
| Required information | Customer/event cause, same UID, mission outcome and damage as separate axes, `CURRENT/MAX` before/after when damage occurred, repair-job availability. |
| Feedback / emotion | Pride, concern, or reflective ownership—“my enhancement choice travelled with this item.” |
| Next | Conditional repair, Chronicle, or return to Workshop for the next enhancement decision. The prior return beat is not a customer-management surface. |
| Current canon evidence | Purchase/handoff itself never causes damage; actual use is required; one damage roll maximum per event/UID; no forced damage. |
| Undecided | Scheduler and player entry, customer identity surface, actual client composition. |

### PANEL_06 = REPAIR_AND_CHRONICLE

| Field | Contract |
|---|---|
| Actual consumer | Workshop repair binding is historical implementation evidence; Chronicle is current product meaning. |
| Player goal / action | If actual damage creates an eligible job, decide whether to repair the same item and understand its enduring scar. |
| Meaningful choice | Spend the one available repair job and accept quality/scar consequences, push while damaged, or stop. |
| Required information | `CURRENT / MAX / BASE_MAX`, derived effective state, repair eligibility, cost/band marked temporary, and no repair for destroyed/full-durability items. |
| Feedback / emotion | Recovery is consequential but does not replace enhancement as the source of fun. Chronicle turns a meaningful event into a memory, not a routine-click log. |
| Next | Return to Enhancement Main or close the item’s meaningful history. |
| Current canon evidence | Repair job opens only after resolved actual damage; routine enhancement clicks are not player Chronicle. |
| Undecided | Final repair price table, repair visual treatment, full player-visible Chronicle layout. |

## 4. Style anchors across panels

| Need | Locked treatment | Evidence ceiling |
|---|---|---|
| Workpiece identity | Central, large, ink-contoured steel silhouette; condition variation must remain readable without color alone. | Atlas source and byte binding exist; client render `NOT_RUN`. |
| Enhancement information | Parchment-like light decision field over restrained workshop material; numeric odds outrank ornament. | Direction locked; exact UI layout `NOT_RUN`. |
| Customer consequence | Same visual grammar with a bounded customer/event accent; item UID remains the visual anchor. | Generated candidate exists; project asset approval, runtime binding and client composition remain `NOT_RUN` / blocked pending user lock. |
| Repair / Chronicle | Structural scar is a material/state difference, not an extra decorative penalty meter. | Current numeric rule approved; presentation `NOT_RUN`. |

## 5. Consistency and adversarial check

| Check | Result |
|---|---|
| Enhancement remains the main content | PASS — panels 03–04 own the session’s repeated action and decisions. |
| Player Promise chain is complete | PARTIAL — planned flow is complete; customer player entry and human evidence are `NOT_RUN`. |
| Support systems do not replace core | PASS — lifecycle explains enhancement consequence; repair is conditional. |
| New system or button invented by the board | PASS — all unconfirmed fields are explicitly marked undecided. |
| Visual comparison mistaken for runtime assets | PASS — the board is text-native; its three generated illustrations are separately recorded candidates, not fake screens or runtime assets. |
| Camera / density comparison fair | PASS — every planned panel uses the same portrait, workpiece-first, high-legibility grammar. |
| Damage forced to prove the repair screen | PASS — `DO_NOT_FAKE_DAMAGE_FOR_DEMONSTRATION = TRUE`. |
| Direction drift or cross-project contamination | PASS by document audit; actual runtime composition remains `NOT_RUN`. |
| Target resolution / UI composition approved | NOT_RUN. |
| Rights / provenance shipping clear | NOT_RUN / `RELEASE_BLOCKED_UNVERIFIED`. |

## 6. Required next validation

1. Decide final session timing and resource pacing without changing the +1 or risk authorities.
2. Review the three 9:16 consumer-first candidates against the actual native Control overlays; choose which, if any, to lock for runtime promotion.
3. Only after user lock: bind the selected raster to its named consumer, run client/Android readability checks, and retain the current fallback if the binding fails.
4. Phase-5: observe whether a player enjoys the enhancement run before they can explain why the same UID’s later result matters.
