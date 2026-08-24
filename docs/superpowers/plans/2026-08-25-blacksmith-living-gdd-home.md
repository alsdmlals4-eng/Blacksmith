# Blacksmith Living GDD Home Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the Blacksmith Notion Human Home into a Project Living GDD + Visual Dashboard without inventing product rules or promoting example images to approved art.

**Architecture:** Keep Notion Human Home as a rich projection of current human canon, reuse canonical linked views for structured data, keep raw AI/implementation evidence in the existing Project Registry/System Record, and protect the routing with a repository contract test. The approved art style is exposed directly, while the missing approved representative visual remains an explicit gap.

**Tech Stack:** GitHub Markdown/Python contract tests, Notion pages/linked database views, existing Google Sheet compatibility mirror.

**Spec:** `docs/superpowers/specs/2026-08-25-blacksmith-living-gdd-home-design.md`

## Global Constraints

- Decision ID: `BS-OPS-20260825-03`.
- Work mode: `PLAN`.
- Product implementation remains `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`.
- Blacksmith baseline main: `187cc46a49bec8b4534f1b030a62fc607551bd3a`.
- Base current main observed: `e3ee0fd5301b2f9631091e4df438f3eab996de77`.
- PR #196 remains read-only and is not absorbed.
- `STYLIZED_DARK_FORGE` is current approved style direction.
- Actual approved representative visual file is not available; no user example image is promoted to approved art.
- No image generation in this task.
- No `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot` mutation.
- Human/Android/accessibility/client-render evidence remains `NOT_RUN` unless actually observed.

---

### Task 1: Add Living-GDD authority contract under TDD

**Files:**
- Create: `tests/check_blacksmith_living_gdd_home_contract.py`
- Modify: `tests/check_project_core_alignment_current.py`

**Interfaces:**
- Consumes: current `AGENTS.md`, this spec, and future `BS-OPS-20260825-03` decision document.
- Produces: a failing-before/fixed-after machine contract invoked by the existing current alignment validator.

- [ ] **Step 1: Create failing contract**

Require these exact tokens in `AGENTS.md`:

```text
BS-OPS-20260825-03
HUMAN_PROJECT_HOME_IS_LIVING_GDD_VISUAL_DASHBOARD
HUMAN_RELEVANT_PROJECT_OUTPUTS_VIEWABLE_FROM_HOME
EXPLANATORY_VISUAL_GDD_BEFORE_DECORATIVE_ART
STYLIZED_DARK_FORGE
VISUAL_GDD_GAP
```

Require these files/tokens:

```text
docs/operations/BS-OPS-20260825-03_BLACKSMITH_LIVING_GDD_HOME.md
docs/superpowers/specs/2026-08-25-blacksmith-living-gdd-home-design.md
```

- [ ] **Step 2: Wire the contract into `check_project_core_alignment_current.py`**

Invoke the new checker and append one failure token if it returns non-zero.

- [ ] **Step 3: Run CI/validation and observe RED**

Expected failure: `AGENTS.md` and the decision document do not yet contain the new Living-GDD tokens.

### Task 2: Record current routing and visual-status decision

**Files:**
- Create: `docs/operations/BS-OPS-20260825-03_BLACKSMITH_LIVING_GDD_HOME.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: Base `HUMAN_HOME_SELF_CONTAINED_POLICY.md`, Blacksmith current overlay, Notion/Sheet visual status.
- Produces: durable repository authority for the Home role and evidence ceiling.

- [ ] **Step 1: Add Decision 03 document**

Record:

```text
HUMAN_PROJECT_HOME_IS_LIVING_GDD_VISUAL_DASHBOARD
HUMAN_RELEVANT_PROJECT_OUTPUTS_VIEWABLE_FROM_HOME
EXPLANATORY_VISUAL_GDD_BEFORE_DECORATIVE_ART
STYLIZED_DARK_FORGE = CURRENT
APPROVED_REPRESENTATIVE_VISUAL = NOT_AVAILABLE
VISUAL_GDD_GAP = OPEN
EXAMPLE_IMAGES = REFERENCE_ONLY_LAYOUT_DENSITY
```

- [ ] **Step 2: Update `AGENTS.md` routing**

Add Decision 03 and the Base current Human Home owner tokens without changing product mechanics.

- [ ] **Step 3: Run exact-head validation**

Expected: new contract and existing current alignment pass.

### Task 3: Create canonical linked Home views

**Notion surfaces:**
- Human Home: `3c41b237-eb1c-813f-a481-e415e3250d1c`
- CORE SYSTEM data source: `collection://b0b4e81d-2400-43f2-b02b-88f1d3c1cb79`
- ASSET LIBRARY data source: `collection://4c49f406-67a2-4524-97b9-f8f1aa730f16`
- Blacksmith Project Registry row: `3c01b237-eb1c-81a1-8cd0-f8bc7eb2f420`

**Interfaces:**
- Consumes: canonical Notion databases.
- Produces: project-filtered human views with no duplicate raw dataset.

- [ ] **Step 1: Create CORE SYSTEM linked table on Home**

Configuration:

```text
FILTER "Project" = "https://app.notion.com/p/3c01b237eb1c81a18cd0f8bc7eb2f420"
FILTER "Status" = "CONFIRMED"
SORT BY "Name" ASC
SHOW "Name", "Record Type", "Player Meaning", "Values", "Status"
WRAP CELLS true
```

- [ ] **Step 2: Create approved visual linked gallery on Home**

Configuration:

```text
FILTER "Project" = "https://app.notion.com/p/3c01b237eb1c81a18cd0f8bc7eb2f420"
FILTER "Approved" = TRUE
SORT BY "Name" ASC
SHOW "Name", "Category", "Status", "Approved"
COVER "Preview" SIZE medium ASPECT contain
```

Current expected gallery may be empty; that is valid `VISUAL_GDD_GAP` evidence.

### Task 4: Rebuild Human Home content

**Notion surface:**
- Replace body of `3c41b237-eb1c-813f-a481-e415e3250d1c`, preserving five child detail pages and the two newly created linked database blocks.

**Interfaces:**
- Consumes: spec, Visual Bible, Flow Map, Core System detail, Development Reality.
- Produces: Living GDD Home in the required scroll order.

- [ ] **Step 1: Replace the Home with sections 01–07**

Use this exact top-level order:

```text
01 · PROJECT NORTH STAR
02 · HOW THE GAME WORKS
03 · HOW IT SHOULD LOOK
04 · CORE GAME DATA
05 · CONTENT & DESIGN
06 · DEVELOPMENT REALITY
07 · DETAIL LIBRARY
```

- [ ] **Step 2: Put explanatory visuals before decorative-art gaps**

Use Mermaid for:

```text
Full Game Flow
Core System Relationship
One Item Lifecycle
First 10 Minutes
Nadia Causal Slice
```

- [ ] **Step 3: Put current human tables directly on Home**

Include:

```text
reinforcement experience bands
CURRENT/MAX structure bands
repair/overhaul anchor values
visual style rules
```

Label tunable numbers `TEST_BUDGET_NOT_FINAL`.

- [ ] **Step 4: Preserve detail pages**

Keep exact child page references for Direction, Enhancement, Visual, Production and Reference.

### Task 5: Update AI/System and Sheet same-ID mirror

**Surfaces:**
- Notion Project Registry/System Record: `3c01b237-eb1c-81a1-8cd0-f8bc7eb2f420`
- Sheet `00_프로젝트_허브`
- Sheet `02_현재_확정결정`

**Interfaces:**
- Consumes: merged/current decision and Notion readback.
- Produces: synchronized operational state without polluting Home.

- [ ] **Step 1: Update System Record notes**

Record Decision 03, Home role, visual gap, and current main after merge. Keep raw operational details here, not Home.

- [ ] **Step 2: Append `BS-OPS-20260825-03` to Sheet decision ledger**

State that product rule delta is none, style is current, representative visual is not yet approved/generated, and Home was expanded under current Base policy.

- [ ] **Step 3: Update Sheet hub current state**

Mark Living GDD Home synced while keeping implementation blocked and human visual/play validation not run.

### Task 6: Adversarial review, merge, and postmerge readback

**Files/surfaces:**
- PR branch exact head
- Notion Home/System Record
- Sheet Hub/Decision ledger

**Interfaces:**
- Consumes: all previous tasks.
- Produces: verified merged state and explicit evidence ceilings.

- [ ] **Step 1: Run adversarial review**

Attack:

```text
link-hub regression
human/AI boundary leakage
duplicate canon drift
example-image approval confusion
tunable-as-final overclaim
historical implementation overclaim
visual gap hidden by decorative references
management breadth scope creep
```

- [ ] **Step 2: Verify changed-file boundary**

No protected product/runtime surface may change.

- [ ] **Step 3: Run exact-head CI**

Require current-task workflows green before merge.

- [ ] **Step 4: Squash merge current PR only**

Do not touch PR #196.

- [ ] **Step 5: Read back new main, Notion Home/System Record and Sheet same-ID**

Only after durable readback may sync be marked complete.

## Self-review

- Spec coverage: all seven Home sections, visual gate, canonical views, AI separation, Sheet mirror, IRG and adversarial review have a task.
- Placeholder scan: no TBD/TODO/implement-later placeholders.
- Scope: documentation/Notion information architecture only; no product mechanic or Godot authoring change.
