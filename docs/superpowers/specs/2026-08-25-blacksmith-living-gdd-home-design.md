# Blacksmith Living GDD Home Design

- Decision: `BS-OPS-20260825-03`
- Work mode: `PLAN`
- Product rule delta: `NONE`
- Product implementation: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Baseline Blacksmith main: `187cc46a49bec8b4534f1b030a62fc607551bd3a`
- Base current main observed: `e3ee0fd5301b2f9631091e4df438f3eab996de77`
- Existing open PR #196: `READ_ONLY_DO_NOT_TAKE_OVER`

## Goal

Rebuild the Blacksmith Notion Human Project Home as a **Project Living GDD + Visual Dashboard**. A person should be able to scroll the Home and understand what game is being made, how it plays, how it should look, which core values currently matter, and what is or is not implemented without opening multiple detail pages first.

## Authority and boundaries

- Human Project Home: current human-readable game design, visuals, flows, core tables, and human-readable development reality.
- Human Detail Canon: deeper comparison/modification surfaces and full human-facing tables.
- AI/System Workspace: schema, IDs, source maps, assumptions, PR/commit/CI evidence, implementation paths, handoff, validation metadata.
- GitHub: structured/runtime truth, code, JSON, Scene/Resource, tests, implementation evidence.
- Google Sheet: migration/compatibility and same-ID decision mirror only.

The Home is a projection of canonical information, not a second independent canon. Large datasets should use linked canonical views where practical. Raw machine metadata does not move into the Home.

## Visual status gate

The project art style is already current-approved by `BS-ART-20260731-01`:

- `STYLIZED_DARK_FORGE`
- dark forge weight and physicality
- equipment remains the visual protagonist
- warm local firelight
- simplified/stylized 2D game illustration
- iron/brass UI language

`BS-MODAK-20260731-01` remains the mascot direction: bright yellow/orange fire spirit, dark shell body rejected, dark detail limited to supporting accents, calm/emotional expressions rather than constant cheerfulness.

However, the current image approval ledger still reports `BLOCKED_IMAGE_NOT_GENERATED`; no actual approved representative Blacksmith visual file is available. User-provided images in the 2026-08-25 conversation are **REFERENCE_ONLY for information density, layout, and Visual-GDD explanatory level** and must not be promoted to Blacksmith approved assets.

Therefore:

- no new image generation in this task;
- no example image is inserted as approved Blacksmith art;
- Home exposes the approved style rules directly;
- Home marks `VISUAL_GDD_GAP` for missing approved representative visuals;
- Mermaid/system diagrams are used as current explanatory visuals until an approved image exists.

## Selected architecture

### Rejected A — compact Home + link hub

Fails because the player loop, core tables, visual direction and project data remain hidden in detail pages.

### Rejected B — duplicate every detail table into Home

Fails because separate copies drift and violate single-owner authority.

### Adopted C — rich Home projection + canonical linked views

The Home directly contains the minimum complete human understanding, plus selected project-filtered linked canonical views. Detail pages remain owners of exhaustive human data; AI/System retains operational detail.

## Home information architecture

### 01. PROJECT NORTH STAR

Must answer immediately:

1. What is this game?
2. What does the player repeatedly do?
3. What must we actually build?
4. What should it look like?

Include:

- one-sentence fantasy;
- primary selling-point hypothesis;
- `PRIMARY = reinforcement tension + DDD`;
- `SUPPORT = precision crafting / customer-world causality / item UID-life / durability-repair / economy-day-work`;
- platform/form: Android portrait-first, PC future consideration;
- visual style summary and approved-visual gap.

### 02. HOW THE GAME WORKS

Show directly on Home:

- full game/session flow;
- one-item lifecycle;
- core system relationship map;
- first 10-minute learning flow;
- representative Nadia causal slice.

The flow must connect:

`customer/world situation → purpose/constraints → craft/spec → reinforcement preview → STOP/PUSH → success/damage/destruction → handoff → delayed result → repair/overhaul/archive/successor → next need`.

Direct combat/exploration must not be implied as the default proof surface.

### 03. HOW IT SHOULD LOOK

Show approved design rules as data, not only a link:

- Stylized Dark Forge art pillars;
- equipment-first composition;
- warm firelight and dark forge materiality;
- iron/brass UI;
- readability before decoration;
- Modak mascot constraints;
- prioritized Visual GDD needs: reinforcement screen, DDD feedback ladder, CURRENT/MAX state, repair decision card, first-10-min storyboard, precision→customer context.

No unapproved visual is presented as final art.

### 04. CORE GAME DATA

Show directly:

- reinforcement experience bands and base success test budget;
- CURRENT/MAX structure-state bands and penalties;
- repair/overhaul resource/economy anchors;
- destruction/+100 terminal rules.

Every tunable table must be labeled `TEST_BUDGET_NOT_FINAL` or equivalent where source canon says so.

Also provide a canonical linked view of confirmed Blacksmith CORE SYSTEM records when Notion can create the project-filtered view.

### 05. CONTENT & DESIGN

Show representative content rather than hiding all context:

- Nadia starter-order causal example;
- customer/world outcomes feed back into the same UID lifecycle;
- content breadth is support for the reinforcement decision, not a replacement core;
- named content families/details remain in their human detail canon.

### 06. DEVELOPMENT REALITY

Human-readable only:

- current stage: planning reopened/current canon review;
- product implementation gate closed until current planning-complete declaration;
- prior implementation exists but does not prove the newly documented whole-game experience;
- Human playtest, Android-device validation, accessibility and final visual validation remain `NOT_RUN` unless actually observed;
- actual approved representative visual is not yet available.

Do not expose raw SHA/ports/local paths/CI IDs on Home.

### 07. DETAIL LIBRARY

Keep direct navigation to:

- Direction · Planning
- Enhancement · Durability · Economy
- Visual · UX · Assets
- Production · Validation
- Reference · Benchmark

Links are drilldown, not substitutes for core understanding.

## Canonical linked views

Where supported without duplicating data:

1. `CORE SYSTEM · Master` → project-filtered Blacksmith confirmed systems table.
   - show: Name, Record Type, Player Meaning, Values, Status.
2. `ASSET LIBRARY · Master` → project-filtered approved visuals gallery.
   - show: Preview, Name, Category, Status, Approved.
   - current expected state may be empty; empty state is evidence of the visual gap, not a reason to insert examples.

## Acceptance criteria

The Home passes only if a first-time reader can scroll in this order:

`game identity → actual play structure → core systems → gameplay flow → UI/visual direction → core data → content context → development reality → detail drilldown`.

Specific checks:

- `HUMAN_PROJECT_HOME_IS_LIVING_GDD_VISUAL_DASHBOARD`
- top section is explanatory, not a link list;
- full loop and one-item lifecycle are visible;
- visual style is directly visible;
- core numeric tables are directly visible with evidence ceilings;
- human-useful data is not moved to AI/System merely because it is structured;
- AI/System raw metadata remains out of Home;
- example images are not promoted to approved assets;
- no new product mechanics are invented;
- no image is generated in this task;
- client-side Notion geometry/render remains `NOT_RUN` unless directly observed.

## Adversarial review targets

1. Link-hub regression.
2. Human data accidentally hidden in AI Workspace.
3. Duplicate canon/data drift.
4. Example image promoted as approved art.
5. Tunable budget presented as final balance.
6. Historical implementation presented as current whole-game PASS.
7. Management-scope creep that weakens reinforcement tension + item biography.
8. Home overcrowding with raw AI/technical evidence.

## Benchmark disposition

- Modern GDD practice: ADOPT visual flows/system relationships and living updates; reject monolithic design-bible behavior.
- Visual game-design workspaces: ADAPT connected flow/system/art views; reject adding a new paid dashboard because Notion already provides the canonical human surface.
- Current Blacksmith differentiation: keep narrower, consequential item decisions rather than expanding into broad logistics/staff management.
