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

## Refinement attempt readback · 2026-09-10

Continued the user-approved sword-identity/side-view refinement. Submitted only this project's original duelist and sword candidates to the image model. Two edits produced a closer bronze guard and fuller but both returned RGB1254×1254 with a baked checkerboard, not transparency. The second edit explicitly requested removal of that checkerboard and failed the same requirement. Neither output is a replacement candidate, native pixel sprite, animation frame or runtime asset.

| Attempt | SHA-256 of generated PNG | Observed disposition |
|---|---|---|
| exec-d6320d28-6b99-466c-bb9a-e2e77740dff7.png | 3d3823bf47e23e4652f3179226307a199f8708859e78d0e6b5e72f6400401a67 | REJECTED_OPAQUE_CHECKERBOARD; sword alignment improved but side-view/grid still unresolved |
| exec-c39502a9-8782-446a-ba54-0935c5f5e8f8.png | 2a3b0d17ad6a803ac6d89c054bf1f824e6256feed52944d9682bef652c864581 | REJECTED_OPAQUE_CHECKERBOARD; alpha correction retry failed |

Generated originals remain in the host generation directory, not duplicated into Git or the candidate catalog. Existing three candidates and the10-page PDF remain unchanged. The rejected previews must not be interpreted as new blueprint content or in-game captures. Verification used Pillow read-only inspection of mode/dimensions plus raw SHA-256 and visual review. No image was programmatically drawn or edited.

Technical research: official Aseprite CLI and Sprite Size documentation (https://www.aseprite.org/docs/cli/ ; https://www.aseprite.org/docs/sprite-size/) describe resizing, but current restricted native MCP exposes no downscale, palette conversion or background-removal operation. Its scale1–8 limit and prohibition on arbitrary CLI/Lua remain in force. ADOPT bounded candidate import/inspection/export; DEFER resizing until a reviewed restricted operation is authorized; REJECT unrestricted CLI as a workaround. Resizing alone cannot repair a baked checkerboard or prove readable pixel clusters.

Next safe decision: approve a narrowly restricted candidate-only resizing/alpha-inspection tool extension, preserving path/size/link/no-overwrite boundaries, before native-grid production. It must not include arbitrary Lua, general shell, automatic background removal or canonical asset writes. Actual artistic background correction remains an image-model task; if repeated generation cannot provide alpha, request a genuinely transparent source rather than silently color-keying character pixels. Motion generation stays pending a technically usable identity anchor. No paid tools or configuration changes were made.

## Approved tool extension and style refinement · 2026-09-10

The latest user approved that bounded tool extension and requested a more stylish look. This supersedes the pending tool-approval sentence above, not final image/runtime approval. Reused PX-DUEL-ACTOR-01, same planned WorldEventPanel consumer and fallback. No new gameplay or characters were added.

Style brief used for the single new built-in generation: original fantasy adult swordsman; athletic4.5-head target proportions, swept dark hair, angular face, fitted brown leather vest, muted teal split tunic, small sculpted steel shoulder plate, practical gloves/boots; bronze-guard short steel sword with fuller and round pommel. Ready stance facing right, clean readable silhouette, restrained material facets, medium pixel clusters, transparent alpha; no cape, extra weapon, text, scenery or shadow. No image inputs or external reference bytes. Model identity not exposed. Output source: exec-1cfbbfe5-4425-403b-a20c-ef28468b1ae3.png, saved to candidates/pixel-stylish-20260910/actor-source.png.

ADAPT Anvil Saga and Weapon Shop Fantasy's forge/adventure readability and material contrast (official pages above re-read); do not copy characters or claim hands-on testing. New proportional/material refinement is our design judgment, not a benchmark finding. ADOPT official Aseprite CLI fixed scale operation; REJECT arbitrary CLI/Lua surface, background removal and canonical writes.

Restricted local implementation: mcp branch codex/aseprite-local-candidate-boundary commit b128a92. `ASEPRITE_ENABLE_REFINEMENT=1` exposes resize_candidate_png and inspect_candidate_alpha; unmodified default sessions expose10tools. Single-frame PNG only, fixed width/aspect-preserving nearest sampling, fresh output, source-hash readback, same candidate/link/input/output budgets. No shared Codex configuration or other-project session was changed. Actual opt-in stdio discovery12tools and calls succeeded. Existing native MCP also exported128px preview successfully. Native desktop discovery of the two new tools remains NOT_RUN; explicit restricted stdio is verified. Local tool source is not pushed to third-party upstream; Base promotion is a reusable candidate only.

TDD: missing functions produced4 intended test failures; implementation plus added aspect/stdio regression yielded30passes. UTF-8 launch corrected an initial cp949 read error in legacy stdio test.8 dependency/deprecation warnings remain. No production-game files changed. Readback: original1242×1266 RGBA; nearest64×65 and128×130 outputs, not64×64. Source remains unchanged.64px loses face/material separation;128px retains more detail, but both need native cluster/alpha cleanup and show small colored edge artifacts. No filtering/thresholding was silently added. Single-frame .aseprite and JSON export prove packaging only, not animation.

Human-facing comparison is now blueprint sections13-15. Final style approval, grid cleanup, connected motion and runtime remain pending. Reusable lesson: test real alpha and actual display scale before multiplying pose states; opt-in tool extensions must preserve other projects' default capability boundary.

Packaging correction: actor-sheet.json initially referenced the unretained duplicate actor-sheet.png. A missing-image contract test observed RED. Changed only meta.image to the byte-identical retained actor-64.png and rebound its normalized hash; no image bytes changed. The contract verifies both image existence and atlas dimensions. Local original export remains provenance; the repository JSON is an explicitly adapted packaging derivative.
