# Blacksmith Art Direction Rework Decision · 2026-08-25

- Decision ID: `BS-ART-20260825-02`
- Status: `USER_APPROVED / ART_STYLE_REWORK_REQUIRED / HISTORICAL_BRIDGE`
- Work Mode: `PLAN`
- Replaces: the **final-style status only** of `BS-ART-20260731-01 / STYLIZED_DARK_FORGE`
- Does not replace: approved gameplay/UI information hierarchy, DDD semantics, durability semantics, or the eight approved Visual GDD information references
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Current style successor: `BS-ART-20260825-03 / ILLUSTRATED_WORKSHOP_BOOK`
- Current image-delivery successor: `BS-ART-20260826-04 / ACTUAL_GAME_IMAGE_CONSUMER_GATE`

## Current successor override · `BS-ART-20260826-04`

This file remains the historical bridge that reopened art direction. It is **not** the current image-delivery owner.

```text
BS-ART-20260826-04
ACTUAL_GAME_CONSUMER_REQUIRED = TRUE
NEW_EXPLANATORY_GDD_SHEET_IMAGE_TARGET = FALSE
GENERATED_UI_SCREENSHOT_MOCKUP_AS_PRODUCT_ASSET = FALSE
PRIMARY_USE_GATE_REQUIRED = TRUE
NO_CONSUMER = CUT_OR_DEFER
EXISTING_VISUAL_GDD_8 = HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY
```

The user's current rule is that Blacksmith does not produce new images merely to explain the design. A new generated image must map to an actual game consumer. Art03 owns style; Decision04 owns consumer/delivery eligibility.

## User decision at this historical bridge

The currently generated Blacksmith visuals were approved as explanatory Visual GDDs, but the user explicitly wanted the art style changed because the presentation read as too generic/AI-generated and insufficiently distinctive.

Historical canonical status at the time:

```text
ART_STYLE_STATUS = REWORK_REQUIRED
STYLIZED_DARK_FORGE = LEGACY_VISUAL_REFERENCE_NOT_FINAL_STYLE_CANON
APPROVED_VISUAL_SCOPE = INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD
REPLACEMENT_ART_STYLE = USER_DECISION_REQUIRED
```

`REPLACEMENT_ART_STYLE = USER_DECISION_REQUIRED` was later closed by `BS-ART-20260825-03`. `APPROVED_VISUAL_SCOPE` remains a description of the old eight reference boards, not a current production target.

## What remains useful as historical reference

- item/workpiece as the visual hero
- tactile forge materiality and evidence of heat, wear, damage, repair
- warm localized forge light against darker surroundings
- clear STOP/PUSH, risk, durability, and context hierarchy
- non-color redundancy for warnings and state
- approved Visual GDD layout/information intent as history/reference only

## What was reopened

- character/environment rendering language
- line/brush/shape language
- UI frame and ornament density
- typography family and title treatment
- icon family
- black/gold palette dominance
- glow treatment
- panel density and visual breathing room
- the overall degree of hand-authored/project-specific identity versus generic generated-fantasy presentation

## Normalized failure signals from the feedback

The phrase used by the user is treated as shorthand for a design-quality problem rather than a nationality/style label. The actionable issues are:

1. repeated black/gold ornamental frames make the UI feel template-like;
2. uniform amber glow and pseudo-medieval serif typography overpower the project identity;
3. generated iconography and dense annotation patterns read as synthetic kit-bashing;
4. multiple boards share an overly similar dark-fantasy AI presentation;
5. the forge/material idea is strong, but the project lacks a sufficiently ownable rendering and UI language.

## Historical next art-direction gate

The old gate below is preserved as history; Art03 and Decision04 now supersede its unresolved status.

1. reuse the eight approved Visual GDDs only for information architecture;
2. inspect existing project Asset/Reference/Benchmark surfaces first;
3. inspect current Base visual reuse principles without auto-adopting project-foreign skins;
4. benchmark relevant commercial/indie UI and illustration directions;
5. present materially different Blacksmith art-direction alternatives;
6. compare readability, uniqueness, mobile fit, production cost, animation/VFX compatibility, and AI-look risk;
7. obtain user approval before any style becomes current canon;
8. do not regenerate the whole asset set automatically.

Current replacement for item 8 is stronger: **new image work begins only after an actual game consumer requirement exists and a separate Image Conversation Approval Gate is passed.**

## Evidence boundary

This historical decision is a user preference/visual-quality direction, not a runtime validation result. `BS-ART-20260825-03` owns current style direction and `BS-ART-20260826-04` owns current image-consumer/delivery eligibility.
