# Blacksmith Visual Direction Lock Packet · 2026-08-28

## 1. Status and boundary

```text
LOCKED_VISUAL_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
SELECTION_STATUS = USER_APPROVED_EXISTING_DIRECTION / PHASE_1_READBACK
PACKET_ROLE = VISUAL_CANON_FOR_FUTURE_APPROVED_CONSUMERS
NO_NEW_GENERATED_RASTER_FOR_THIS_PACKET = TRUE
NO_RUNTIME_ASSET_CREATED_BY_THIS_PACKET = TRUE
GODOT_APPLICATION_STATUS = NOT_APPLIED_BY_THIS_PACKET
```

This packet reads and consolidates the existing approved direction. It does
not promote a comparison board, generated screenshot, reference image, or
planning diagram into a runtime asset.

## 2. Selected direction

| Field | Locked meaning |
|---|---|
| Selected candidate | `ILLUSTRATED_WORKSHOP_BOOK` |
| Selection reason | A warm, hand-drawn workshop makes an item feel crafted and worth risking, while paper-like information surfaces keep enhancement odds readable on portrait mobile. |
| Adopted elements | parchment value field; wood/leather/iron material cues; ink-like contours; localized forge light; a central workpiece; modern readable control hierarchy. |
| Rejected elements | `STYLIZED_DARK_FORGE`, generic black-and-gold fantasy, dense decorative UI, pseudo-text, copied game imagery, and full-frame art with no actual consumer. |
| Superseded references | Existing eight Visual GDD images remain `HISTORICAL_INFORMATION_ARCHITECTURE_REFERENCE_ONLY`; they do not set final style or runtime readiness. |

## 3. Global and layer anchors

| Layer | Anchor |
|---|---|
| Mood / emotion | Quiet concentration before a risk, followed by a warm, crisp resolution; the forge is intimate rather than monumental. |
| Rendering language | Illustrated workshop book: tactile paper, leather, wood, iron, and restrained ink outlines. |
| Palette / value / lighting | Warm parchment and brown material family; charcoal text; one local orange forge light; clear light panel behind decision information. Avoid an all-orange fog or crushed dark values. |
| Shape / silhouette / proportion | The workpiece is the hero silhouette. Tools frame it; ornament never obscures its condition or level. |
| Camera / density | Android portrait, near-frontal workshop presentation, generous central interaction field, dense only where a choice needs comparison. |
| UI / icon / VFX | Modern high-legibility layer sits on the illustrated material surface. State, not decoration, drives icon and VFX contrast. |
| Character / environment variation | Customer, region, time, and condition may vary only through restrained material, accent, and lighting changes while keeping the same ink/material/value grammar. |

## 4. Keep / Avoid / Do Not Drift

```text
KEEP = workpiece-as-protagonist + paper/wood/leather/iron tactility + readable probability hierarchy
AVOID = black-gold template + visual noise + color-only state signaling + AI pseudo-text + decorative fake buttons
DO_NOT_DRIFT = portrait camera + warm localized forge light + ink/material language + current/max/base-max readability
ALLOWED_VARIATION = customer, location, time, and durability state may alter bounded accents, props, and local light only
```

## 5. Confirmed screen anchors and source provenance

| Anchor | Current evidence | Consumer / status |
|---|---|---|
| Main menu workshop field | `assets/ui/workshop/workshop_enhancement_background_v2.png`, 941×1672, SHA-256 `A3D305…25382B5` | Main Menu dynamic plus Workshop static binding; client render `NOT_RUN`. |
| First Forge field | `assets/ui/workshop/first_forge_background_v1.png`, 941×1672, SHA-256 `A575D0…4E64954` | `forging_screen.gd` dynamic binding; client render `NOT_RUN`. |
| Workpiece condition family | `assets/ui/workshop/workpiece_durability_state_atlas_v1.png`, 1254×1254, SHA-256 `FA2969…73258FA` | Workshop dynamic NORMAL/MINOR/MAJOR/DESTROYED atlas binding; client render `NOT_RUN`. |
| Production reference | `assets/visual_reference/illustrated_workshop_book_reference_v1.png` | Production reference only; no runtime consumer by design. |

The exact game target is `720×1280` portrait. These source images and their
declared byte bindings prove neither composition at target resolution nor
human readability.

## 6. Rights and delivery boundary

```text
PROVENANCE_OWNER = docs/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md
RUNTIME_ASSET_APPROVAL = PROJECT_ASSET_APPROVED_WHERE_MANIFESTED
RELEASE_RIGHTS_STATUS = RELEASE_BLOCKED_UNVERIFIED
REFERENCE_SIMILARITY_STATUS = NOT_APPLICABLE_FOR_CURRENT_ORIGINAL_TEXT_BRIEFS
NEXT_VISUAL_ASSET_GATE = CONSUMER_METADATA + USER_PREAUTHORIZED_GENERATION + POST_GENERATION_USER_LOCK
```

All three runtime-consumed generated asset records have unresolved current
commercial/distribution terms, actual client render, Android readability,
accessibility, and human visual review. The reference image is not a runtime
or marketing asset. No later visual production may treat this packet as a
rights clearance.

## 7. Destination and readback requirement

Repository owner: this file,
`PROJECT_CORE_SCENE_VISUAL_BOARD_20260828.md`, and the GitHub human-facing GDD.
`BS-OPS-20260828-35` retires Notion mirrors. Every future change to this packet
must read back the exact repository head and its repository destination.
