# BS-OPS-20260825-02 — Planning Reactivation + Human/AI Workspace Split

- Status: `APPROVED_CURRENT_OPERATIONAL_OVERRIDE`
- Approved by: user directive, 2026-08-25 KST
- Scope: planning/documentation/authority routing only
- Product rule delta: `NONE`
- Product implementation gate: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Base main observed: `ceb83c680f76fead5811956bd6503fd5e4da8577`
- Blacksmith baseline main: `f0a4bd525335566888c8123287ab2a1045f5d01b`
- Pre-existing PR: `#196 OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`

## Decision

Blacksmith planning work is reactivated by the current user request. The previous `BS-OPS-20260825-01 / PAUSED_HANDOFF_ONLY` state remains historical evidence but no longer blocks planning/documentation work.

The human and AI workspaces are split by audience and authority:

1. **Notion Project Home = human-facing game learning map**
   - player promise and pointed fun
   - whole-game flow and one-item lifecycle
   - meaningful choices and visible consequences
   - first-session learning path
   - system relationship map
   - approved visual/reference child pages
   - no PR/SHA/CI/task queue/pause/debug metadata in the main learning surface
2. **Existing Notion Project Registry / System Record = AI/automation operational surface**
   - current work state, SHA/PR/branch, blockers, next package, evidence and handoff
   - no second dashboard or duplicate GDD is created
3. **GitHub = structured/runtime authority**
   - Markdown/JSON decisions, code, data, Scene/Resource, tests, CI/runtime truth
4. **Google Sheet = migration/compatibility surface**
   - no new primary planning workflow is created there
   - this approved decision is mirrored with the same Decision ID because the Blacksmith project contract requires cross-surface Decision identity

## Authority / conflict correction

The current task observed these stale or conflicting surfaces:

- project-tracked total execution instruction still reported v4.5 r2 while the current user-supplied active contract is v4.8 r4;
- the Sheet hub still reported `PAUSED_HANDOFF_ONLY` even though the current user explicitly reactivated planning;
- Sheet legacy routing still contained project-dedicated Godot AI ports `8006/9506`, which are historical only under the current shared exact-pin + fixed default ports + exact session routing policy;
- the Notion Home mixed human-facing game explanation with operational pause/PR/SHA state and contained mutually stale status blocks.

This Decision does **not** rewrite historical evidence. It changes current routing and presentation so stale history cannot masquerade as current authority.

## Current product direction preserved

No product mechanic is added or removed here. Current product hierarchy remains:

- PRIMARY CORE: **reinforcement tension + decision-driven design (DDD)**
- SUPPORT: precision crafting; customer/world causal context; item UID/lifecycle/Chronicle; durability/repair/overhaul/destruction; economy/day-work constraints
- player does not directly fight or run a broad combat/adventure layer by default
- fun/usability remains a hypothesis until human/player evidence exists

The Home therefore teaches the game in this order:

`customer/situation → craft/spec choices → forge → STOP/PUSH reinforcement decision → immediate outcome → item delivery/use → delayed world result → repair/overhaul/destruction/archive/successor → next request`

## Decision trade study

### Alternative A — keep one monolithic Notion Home

- Benefit: zero migration effort.
- Cost: user-facing design, AI state, PR/SHA and historical status continue to compete for attention.
- Failure mode: stale operational text damages trust in the design surface and duplicates current-state owners.
- Disposition: `REJECT`.

### Alternative B — make GitHub the human-facing design home

- Benefit: strongest proximity to structured/runtime truth.
- Cost: poor scanning and visual learning for a non-technical game-design workflow; pushes raw operational detail into the primary human surface.
- Failure mode: correct but hard-to-learn project state; weaker visual/flow communication.
- Disposition: `REJECT_AS_PRIMARY_HUMAN_SURFACE`.

### Alternative C — domain split using existing surfaces

- Notion Home: human learning map.
- existing Notion System Record: AI/current work state.
- GitHub: structured/runtime authority.
- Sheet: migration compatibility + same-ID mirror only.
- Benefit: lowest long-term duplication and no new tool/dashboard.
- Failure mode: drift if the same fact is copied across surfaces instead of linked/routed.
- Guard: each domain keeps one owner; operational data is not recopied onto Home.
- Disposition: `ADOPT`.

### Alternative D — build a new Notion database/dashboard/knowledge graph

- Benefit: richer views and filters.
- Cost: new schema, migration and maintenance burden for a solo project; duplicates existing Project Registry/System Record.
- Failure mode: administration becomes a second product.
- Disposition: `REJECT` under Existing Solution First.

## Fresh benchmark / market evidence — 2026-08-25

Evidence is used as a design signal, not as proof of causality.

### Potion Craft: Alchemist Simulator — `ADAPT`

- Official Steam page: https://store.steampowered.com/app/1210320/Potion_Craft_Alchemist_Simulator/
- Current Steam observation: very positive overall; the store foregrounds physical crafting, customer problems, experimentation and consequences of what the player sells.
- Developer interview: https://www.gamereactor.eu/video/712993/Distilling%2BExcellence%2B-%2BInterview%2Babout%2BPotion%2BCraft%2BAlchemist%2BSimulator%2Bat%2BDevGAMM/
- Developer self-report emphasizes customer-need interpretation, multiple ways to reach an answer, and strong control/detail quality.
- Blacksmith use: **adapt customer/situation context as the readable reason behind a craft decision**, but keep reinforcement STOP/PUSH tension as the primary core.

### Blacksmith Master — `REFERENCE_ONLY / REJECT_BREADTH`

- Official Steam page: https://store.steampowered.com/app/2292800/Blacksmith_Master/
- Current store positioning centers the whole production chain, staffing, layout, resource acquisition and shop throughput.
- Community feedback repeatedly reports mid/late-game micromanagement, repetitive production, logistics burden and a forge that can feel more like a factory.
- Representative community sources:
  - https://steamcommunity.com/app/2292800/reviews/
  - https://steamcommunity.com/app/2292800/discussions/0/687494495670966260/
- Blacksmith use: reject management breadth as the main differentiator; keep the number of decisions smaller while making each item decision more consequential and memorable.

### While the Iron's Hot — `ADAPT_NARROWLY`

- Official Steam page: https://store.steampowered.com/app/1906830/
- It makes smithing a world-facing problem-solving verb across smelting, forging, assembly and non-combat exploration.
- Blacksmith use: adapt the principle that **crafted output should matter outside the crafting screen**, but do not import exploration/travel chores as core scope.

### Anvil Saga — `REFERENCE_ONLY`

- Official Steam page: https://store.steampowered.com/app/1587540/
- It combines shop management and story-impacting decisions.
- Blacksmith use: reference the value of visible consequence, but reject broad shop-management replication because Blacksmith's current pointed fun is reinforcement tension + item biography.

## Implementation Reality Gate

This Decision may claim only what is actually verified:

- repository/Sheet/Notion source discovery: `VERIFIED`
- information-architecture decision and current-work authorization: `VERIFIED_USER_DIRECTIVE`
- GitHub branch/file/PR/merge effects: verified only after write + readback + merge readback
- Notion update: verified only after update invocation + destination fetch/readback
- Notion visual geometry/client rendering: `NOT_RUN` unless directly observed
- game runtime: `NOT_RUN` for this planning-only task
- human usability / player fun: `NOT_RUN`; design benefit remains `HYPOTHESIS`

## Adversarial review targets

Minimum whole-state review attacks for this change:

1. authority/stale-state inversion;
2. human-vs-AI information pollution;
3. market differentiation and management-scope creep;
4. implementation/evidence overclaim;
5. long-term maintenance and duplicate-owner risk;
6. final post-change readback after merge.

## Revisit conditions

Revisit this routing only if one of these becomes true:

- the human Project Home cannot explain the game without operational metadata;
- the existing System Record cannot represent current-work state without a new structural surface;
- Notion child-page structure becomes too deep to navigate;
- a new domain requires a genuinely independent authority/validation boundary;
- player tests show that the current core-flow explanation does not match the experienced game.
