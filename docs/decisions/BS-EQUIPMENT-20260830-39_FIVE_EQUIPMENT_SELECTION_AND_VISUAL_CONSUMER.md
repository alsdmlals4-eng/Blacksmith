# BS-EQUIPMENT-20260830-39 · Five Equipment Selection and Visual Consumer

## Status

`USER_APPROVED_CURRENT_MVP_EXTENSION_20260830`

The user approved replacing the dedicated recurring-Precision workshop raster with native Precision UX and introducing exactly five selectable first-work equipment types: sword, shield, bow, armor, and helmet.

## Boundary

- `BS-ENHANCE-20260829-37` and `BS-ENHANCE-20260830-38` remain the only owners of Catalyst Tag content, cadence, selection, and mutation.
- `WEAPON_ITEM_ONLY` remains true. This decision does not introduce defensive Catalyst Tags, a defense balance curve, classes, new recipes, inventory, or combat simulation.
- Saved identity remains the existing `equipment_group + role_profile` pair. No save field is added.

## Current equipment catalog

| ID | Label | Group | Role profile | Precision Tags | Image consumer |
| --- | --- | --- | --- | --- | --- |
| `iron_sword` | 철검 | `SWORD` | `PHYSICAL_WEAPON_ATTACK` | Eligible | First forge choice and Workshop identity hero |
| `iron_shield` | 철방패 | `SHIELD` | `PHYSICAL_WEAPON_GUARD` | Eligible | First forge choice and Workshop identity hero |
| `iron_bow` | 철활 | `BOW` | `PHYSICAL_WEAPON_RANGED` | Eligible | First forge choice and Workshop identity hero |
| `iron_armor` | 철갑옷 | `ARMOR` | `ARMOR_BODY_DEFENSE` | Ineligible | First forge choice and Workshop identity hero |
| `iron_helmet` | 철투구 | `HELMET` | `ARMOR_HEAD_DEFENSE` | Ineligible | First forge choice and Workshop identity hero |

All five retain the existing first-forge activity, grade roll, durability, repair, and generic `raw_role_stat` storage. That value is player-facing as a role value; no new combat-stat simulation is introduced.

## Precision boundary

- Sword, shield, and bow must use the existing native tag-add or tag-upgrade UX at every exact target from `+9 -> +10` through `+99 -> +100`.
- Armor and helmet can use ordinary enhancement before the first exact Precision target. At `+9 -> +10`, `PRECISION_TAG_WEAPON_ONLY` blocks before cost, roll, item mutation, ledger append, or save.
- A defensive Precision progression needs a separately approved tag catalog and balance owner. It is not implied by this decision.

## Image lifecycle

- The existing `precision_tag_workshop_background_v1.png` has no actual runtime consumer under the user's direction. It must be removed from the build and recorded as `RETIRED_NO_CONSUMER_BY_USER_DIRECTION`; native labels, options, previews, and outcome controls remain.
- Five 1:1 item illustrations are `GENERATED_CANDIDATE` until their rendered results are reviewed and explicitly locked by the user. They may not contain UI, text, numerals, logos, watermarks, copied game expression, guaranteed success, or damage outcome.
- Only the post-generation user lock permits their asset-manifest registration and runtime binding.

## Evidence boundary

Machine checks cover catalog validation, legacy-sword round-trip, all five first-forge transfers, weapon-only Precision gating, native 48dp selection controls, retired Precision raster references, and asset hashes after user lock. Godot client, Android, accessibility, visual human review, performance, and release rights remain `NOT_RUN` until separately observed.
