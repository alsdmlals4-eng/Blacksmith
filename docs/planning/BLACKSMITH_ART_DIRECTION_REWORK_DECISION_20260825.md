# Blacksmith Art Direction Rework Decision · 2026-08-25

- Decision ID: `BS-ART-20260825-02`
- Status: `USER_APPROVED / ART_STYLE_REWORK_REQUIRED`
- Work Mode: `PLAN`
- Replaces: the **final-style status only** of `BS-ART-20260731-01 / STYLIZED_DARK_FORGE`
- Does not replace: approved gameplay/UI information hierarchy, DDD semantics, durability semantics, or the eight approved Visual GDD information references
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## User decision

The currently generated Blacksmith visuals are approved as explanatory Visual GDDs, but the user explicitly wants the art style changed later because the current presentation reads as too generic/AI-generated and insufficiently distinctive.

Canonical status:

```text
ART_STYLE_STATUS = REWORK_REQUIRED
STYLIZED_DARK_FORGE = LEGACY_VISUAL_REFERENCE_NOT_FINAL_STYLE_CANON
APPROVED_VISUAL_SCOPE = INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD
REPLACEMENT_ART_STYLE = USER_DECISION_REQUIRED
```

## What remains approved

- item/workpiece as the visual hero
- tactile forge materiality and evidence of heat, wear, damage, repair
- warm localized forge light against darker surroundings
- clear STOP/PUSH, risk, durability, and context hierarchy
- non-color redundancy for warnings and state
- approved Visual GDD layout/information intent

## What is reopened

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

## Next art-direction gate

Do not generate a replacement style by simply changing a prompt adjective.

The next art-direction task must:

1. reuse the eight approved Visual GDDs only for information architecture;
2. inspect existing project Asset/Reference/Benchmark surfaces first;
3. inspect current Base visual reuse principles without auto-adopting project-foreign skins;
4. benchmark relevant commercial/indie UI and illustration directions;
5. present at least three materially different Blacksmith art-direction alternatives;
6. compare readability, uniqueness, mobile fit, production cost, animation/VFX compatibility, and AI-look risk;
7. obtain user approval before any style becomes current canon;
8. regenerate only representative Visuals first, not the whole asset set.

## Evidence boundary

This decision is a user preference/visual-quality direction, not a runtime validation result. Human comparative review of replacement directions is required before a new style becomes `CURRENT`.
