# Pixel candidate production · 2026-09-10

Project: BLACKSMITH / 모루의 서약. Owner: BLACKSMITH_PIXEL_WORLD_BLUEPRINT_20260910.md. User approved continuing its representative forge/equipment/duel candidate stage. These are GENERATED_CANDIDATE, never automatically approved runtime assets. No separate HTML. Keep existing source art unchanged.

## Selected first batch

| requirement_id / consumer_id | consumer_surface / implementation_owner_or_path | runtime_asset_role / primary_use | target_aspect_resolution | state_family_requirement | fallback_if_unconsumed |
|---|---|---|---|---|---|
| PX-FORGE-01-BG | Workshop scene illustration slot; scripts/vertical_slice/ui/vs_workshop_screen.gd, future split viewport | Static environment behind separately animated smith; communicate working forge | 3:2 generation candidate, intended 360×248 focus and cropped 360×136 split; native grid compliance reviewed later | Static base, no baked smith or floating UI; flame animation separate pending | Candidate archive, never auto-replace existing full-frame background |
| PX-EQUIP-SWORD-01 | First-forge/workshop item image; assets/ui/equipment/iron_sword_card_v2.png current slot | Isolated iron sword identity anchor; reusable transparent item | Square generation candidate; production goal64×64, grip pivot to be measured after output | Base only now; grade invariant, enhancement/tag/damage layers pending | Text/existing runtime asset remains until approval |
| PX-DUEL-ACTOR-01 | PLANNED_GAME_SURFACE WorldEventPanel under scripts/vertical_slice/ui/vs_app.gd | Side-view equipped duelist identity and action reference | Square generation candidate, production target48×64 body in64×64 action cell | ready anchor now; prepare/attack/guard/hit/recover/outcome planned next using identity lock | Existing factual text summary; no fake replay |

Delete test: without environment the planned forge has no place identity; without isolated sword item identity cannot be inspected; without duelist anchor consistent action production cannot begin. Only these three are generated now. Shield/bow/armor/helmet and other backgrounds remain needed, not silently treated complete. Coverage: title/settings/loading not in this batch; actual workshop/equipment/duel planned slots REQUIREMENT_LINKED; interaction controls text-native; empty/error use textual fallback.

## Continuity and prompts

Keep: warm metal/wood forge atmosphere, independent fantasy, medium-density pixel clusters, clear equipment silhouette, non-graphic combat. Change: old painted textures replaced in new candidates by deliberately stepped pixels. Avoid: copied benchmark town layouts, characters, logos, pseudo-UI/text, painterly softness, baked checkerboard, giant magic effects, grade-specific shapes. No external image bytes sent to generation; prior art inspected only for historical context.

Shared style: original fantasy pixel art, readable medium-density clusters, crisp square steps, restrained 3-tone materials, cool steel against muted warm oak/copper, no antialiasing/blur/photorealism/text/watermark. Outputs are style/identity candidates; a large pixel-looking image is not proof of a valid64×64 sprite.

Forge prompt: original 3:2 interior background for a portrait crafting game's upper panel. Fixed slightly elevated front-oblique camera. Compact stone forge on left, dark timber beams, tool rack to right, clear stone floor across lower half, a small anvil at lower center leaving room for a separate smith. Warm amber forge light, cool blue stone shadow, modest fantasy details. No people, weapons displayed as UI, menus, letters or decorative framing. Work area remains legible when the middle136/248 vertical region is shown.

Sword prompt: one original plain fantasy iron sword, centered diagonal tip upper right and pommel lower left. Broad short straight steel blade with simple fuller, modest bronze crossguard, dark brown leather grip, small rounded bronze pommel. Strong chunky silhouette, simple3-tone steel clusters. Entire object with generous clear margin. Genuine transparent background, no floor, shadow, glow, frame, checkerboard, lettering, extra weapons. Base tier without elemental tags.

Duelist prompt: one original adult fantasy arena fighter full body facing right in strict side view, grounded ready stance. Stocky readable proportions about3.5heads, short dark hair, simple muted teal tunic, brown leather vest and boots, light steel shoulder guard. Holding plain iron sword forward in right hand, left hand near torso, no shield. Crisp pixel clusters, no gore, no emblem, no text, no platform, no cast shadow. Genuine transparent background. Entire sword/feet/hair inside frame. This is one ready pose, not an animation sheet.

## Motion and export preparation

Candidate packaging uses discovered native aseprite-candidates MCP in a unique blacksmith task folder. Copy source PNG to .aseprite, inspect dimensions/layers/duration, export single frame + JSON without trim or scale, compare decoded RGBA exactly. This proves packaging only; do not duplicate stills and call them animation.

Next action loop specification: ready → prepare → active → recover → ready. Proposed120/160/80/160ms trial timing; no actual attack/hitbox event invented. Right-facing, constant handedness, boot-ground pivot and sword grip; same canvas and scale. Asset revision and pivot must be frozen after candidate review. Missing intermediate poses, native pixel-grid regularity, small-size readability and transparent edges must be reviewed before production readiness.

## Research, review and boundaries

2026-09-10 official Weapon Shop Fantasy and Anvil Saga pages: ADAPT workshop/adventure readability and material contrast; REJECT identifiable expression and staff/facility scope. Aseprite Animation and CLI docs: ADOPT frame/layer/duration and PNG+JSON workflow, not an animation-completion claim. Sources: https://store.steampowered.com/app/599460/Weapon_Shop_Fantasy/ ; https://store.steampowered.com/app/1587540/Anvil_Saga/ ; https://www.aseprite.org/docs/animation/ ; https://www.aseprite.org/docs/cli/ . Desk research, no hands-on study.

Adversarial pre-check: large pseudo-pixels may fail native grid; transparent request may return opaque pixels; sword proportions can drift in actor hand; backgrounds may contain baked props blocking motion. Review actual output and record revision needs. Do not fix artistic issues through coded drawings.

Service: built-in image_gen; exact model version not exposed. Input image rights: no reference files submitted. Candidate rights/release clearance UNKNOWN / RELEASE_BLOCKED_UNVERIFIED; no commercial-release assertion. User approval and runtime NOT_RUN.

CI recovery: previous PR failed because adding a latest-direction note changed the historical human GDD source hash without regenerating its bound PDF. Remove only that new note and keep latest routing in AGENTS/authority index/Active Context. Preserve historical PDF and source receipt; do not update a receipt hash to pretend an unrebuilt PDF contains changed source.
