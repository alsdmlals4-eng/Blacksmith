# Blacksmith Core Simplification Canon Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Promote the user-approved +1-only enhancement, +9→+10 Precision Keyword, four-state damage, event-only Chronicle, and Illustrated Workshop Book direction into current Blacksmith planning canon without mutating protected product runtime paths.

**Architecture:** Add one new current planning owner for Decisions `BS-ENHANCE-20260825-25`, `BS-DAMAGE-20260825-26`, `BS-CHRONICLE-20260825-27`, and `BS-ART-20260825-03`; route current entrypoints to it and explicitly demote conflicting CURRENT/MAX and multi-precision material. Human-facing Notion surfaces show the simplified rules directly, while AI/System and Sheet mirror IDs, provenance, blockers, and evidence. Runtime migration is deliberately excluded until the planning-complete declaration plus damage-curve and repair gates are resolved.

**Tech Stack:** Markdown / Python contract tests / GitHub Actions / Notion / Google Sheets compatibility mirror.

**Spec:** `docs/superpowers/specs/2026-08-25-blacksmith-enhancement-damage-chronicle-simplification-design.md` and `docs/superpowers/specs/2026-08-25-blacksmith-damage-source-amendment-design.md`.

## Global Constraints

- `WORK_MODE = PLAN`.
- Product mutation remains `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`.
- Do not change `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot` in this plan.
- Enhancement success is exactly `+1` level; no multi-level success.
- `+9 -> +10` is the only Precision Enhancement transition.
- Successful +10 Precision Enhancement creates exactly one player-facing item keyword using existing `CATALYST_AFFIX` as machine owner; no fourth affix slot.
- Damage authority is exactly `NORMAL -> MINOR -> MAJOR -> DESTROYED`; no hidden CURRENT/MAX authority.
- Enhancement-failure damage is impossible through target +10 and possible from target +11 onward, with monotonic non-decreasing conditional probability as target rises.
- Exact +11~+100 damage probabilities are not approved and must remain `TUNABLE / NOT_FINAL_PRODUCT_BALANCE`.
- Customer purchase/handoff itself does not cause damage; an eligible delayed customer/world event may advance damage by one state.
- Routine enhancement success/failure and `N days ago` rows are not player-facing Chronicle entries.
- Art direction is `ILLUSTRATED_WORKSHOP_BOOK / USER_APPROVED_DIRECTION`; final product asset/runtime approval remains not granted.
- Existing PR #196 is `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`.
- Base fresh-read at plan creation: `210ec78292fa12ed7563ba743b322dd36103ae4a`.

---

### Task 1: RED Current-Authority Contract

**Files:**
- Create: `tests/check_core_simplification_current_contract.py`

**Interfaces:**
- Consumes: current repository text files only.
- Produces: one fail-closed Python contract that protects the new planning authority and prohibits stale current-entrypoint semantics.

- [ ] **Step 1: Write the failing contract test**

Create a Python test that reads `AGENTS.md`, `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`, `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`, and the future current owner `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`.

Require these tokens in the current owner / entrypoints:

```python
REQUIRED = [
    "BS-ENHANCE-20260825-25",
    "BS-DAMAGE-20260825-26",
    "BS-CHRONICLE-20260825-27",
    "BS-ART-20260825-03",
    "SUCCESS_LEVEL_DELTA = +1",
    "+9 -> +10 = PRECISION_ENHANCEMENT",
    "NORMAL -> MINOR -> MAJOR -> DESTROYED",
    "TARGET <= +10: ENHANCEMENT_DAMAGE = 0",
    "TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE",
    "MONOTONIC_NON_DECREASING_DAMAGE_RISK",
    "CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE",
    "PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE",
    "ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE",
    "ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK",
]
```

Also fail if current entrypoints claim any of these as current authority:

```python
FORBIDDEN_CURRENT = [
    "CURRENT/MAX = CURRENT_DURABILITY_AUTHORITY",
    "PRECISION_MILESTONES = [10, 20, 30, 40, 50]",
    "ART_STYLE_STATUS = REWORK_REQUIRED",
]
```

Historical source docs are exempt; the check targets current entrypoints/current owner only.

- [ ] **Step 2: Run RED**

Run:

```bash
python tests/check_core_simplification_current_contract.py
```

Expected: FAIL because `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` does not exist and current entrypoints still route to CURRENT/MAX / old art-direction state.

- [ ] **Step 3: Commit the RED test**

```bash
git add tests/check_core_simplification_current_contract.py
git commit -m "test: require simplified Blacksmith core canon"
```

---

### Task 2: Create the New Current Planning Owner

**Files:**
- Create: `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- Modify: `AGENTS.md`
- Modify: `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
- Modify: `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`

**Interfaces:**
- Consumes: Decisions 01~24 only where they do not conflict with 25~27 / Art03.
- Produces: the single current owner for enhancement cadence, damage-state semantics, player Chronicle filtering, and current art direction.

- [ ] **Step 1: Write the new current owner**

The document must state exactly:

```text
BS-ENHANCE-20260825-25
SUCCESS_LEVEL_DELTA = +1
NORMAL_ENHANCEMENT = every target except +10
+9 -> +10 = PRECISION_ENHANCEMENT
+10 SUCCESS -> exactly one ITEM_KEYWORD
ITEM_KEYWORD machine owner = CATALYST_AFFIX
NO_FOURTH_AFFIX_SLOT

BS-DAMAGE-20260825-26
DAMAGE_STATE = NORMAL / MINOR / MAJOR / DESTROYED
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
MONOTONIC_NON_DECREASING_DAMAGE_RISK
EXACT_DAMAGE_CURVE = TUNABLE_NOT_FINAL
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
CURRENT_MAX_AUTHORITY = SUPERSEDED

BS-CHRONICLE-20260825-27
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY

BS-ART-20260825-03
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

Preserve: STOP/PUSH, item UID, target-level recovery, checkpoint floors `[10,30,60,90]`, +10 break-even role, +11 first salient risk decision, delayed customer/world causality, +100 terminal.

Mark as unresolved rather than inventing:

```text
DAMAGE_PROBABILITY_CURVE = USER_APPROVAL_REQUIRED
CUSTOMER_EVENT_DAMAGE_POLICY = CONTENT_OWNER_DECISION_REQUIRED
MINOR_MAJOR_REPAIR_MODEL = USER_APPROVAL_REQUIRED
MAJOR_ENHANCEMENT_ELIGIBILITY = USER_APPROVAL_REQUIRED
```

- [ ] **Step 2: Route `AGENTS.md` to the new owner**

Update the current-state header and core protection section so AI workers cannot use old CURRENT/MAX or multi-milestone precision as current product intent. Keep protected runtime paths and PR #196 read-only rules unchanged.

- [ ] **Step 3: Add a top-priority override section to the current overlay**

Do not delete the old 01~24 evidence. Add a `2026-08-25 CURRENT OVERRIDE` section before the old detailed sections, explicitly stating which older fields are superseded and which remain valid.

- [ ] **Step 4: Update the authority index**

Make `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` the current owner for:

```text
enhancement cadence
precision cadence / keyword creation
damage-state authority
player-facing Chronicle inclusion
art-direction selection state
```

Keep older numeric docs as `HISTORICAL_OR_PARTIALLY_SUPERSEDED_EVIDENCE`.

- [ ] **Step 5: Run GREEN contract**

```bash
python tests/check_core_simplification_current_contract.py
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add AGENTS.md CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
git commit -m "docs: promote simplified enhancement and damage canon"
```

---

### Task 3: Reconcile Directly Conflicting Planning Owners and Visual Bindings

**Files:**
- Modify: `docs/planning/BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md`
- Modify: `docs/planning/BLACKSMITH_PRECISION_CUSTOMER_LINK_CANON_20260824.md`
- Modify: `docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_SAFE_SPEC_20260825.md`
- Modify: `docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_BINDINGS_20260825.json`
- Create: `docs/operations/BS-OPS-20260825-07_CORE_SIMPLIFICATION_CANON_MIGRATION.md`

**Interfaces:**
- Consumes: Task 2 current owner.
- Produces: no contradictory current handoff from onboarding/customer/Visual surfaces.

- [ ] **Step 1: Amend first-10-minutes current interpretation**

Current flow becomes:

```text
New Game
-> first item
-> ordinary +1 enhancement through +9
-> +9 -> +10 Precision Enhancement
-> one item keyword created on success
-> +10 secured/break-even state
-> +11 risk preview
-> STOP/PUSH
```

Remove CURRENT introduction and MAX/CRITICAL teaching from the current interpretation. State that +11 damage risk exists but exact probability is not yet final.

- [ ] **Step 2: Amend customer/precision current interpretation**

Replace `+10/+20/+30/+40/+50` precision cadence with `+9 -> +10 only`. Retain customer purpose/constraint/context, no universal fit score, same-UID delayed result, and catalyst contextual responsibility at the +10 keyword moment.

Add the new world-event damage hook:

```text
handoff/purchase != automatic damage
eligible delayed event -> optional one-step damage transition
```

- [ ] **Step 3: Mark current Visual system semantics stale where necessary**

In the implementation-safe spec/bindings, preserve layout/information-hierarchy evidence but invalidate fields that require CURRENT/MAX, five structural bands, old precision milestones, MAX penalty, or routine dated enhancement history.

Require regenerated representative set after mechanic sync:

```text
Main Menu
Enhancement Main (+1 only)
+9 -> +10 Precision Keyword
Four-state Damage / Repair
Event-only Item Chronicle
```

- [ ] **Step 4: Write the operations receipt**

Record fresh Base/main, Blacksmith baseline, PR #196 isolation, approved IDs, supersession map, unresolved balance/repair gates, and evidence ceiling.

- [ ] **Step 5: Run current Python document/authority contracts available in repository**

At minimum:

```bash
python tests/check_core_simplification_current_contract.py
python tests/check_current_authority_entrypoint_contract.py
python tests/check_project_core_alignment_current.py
```

Expected: PASS. If an older regression test requires CURRENT/MAX as current truth, update the regression contract to preserve history while validating the new current owner rather than restoring stale semantics.

- [ ] **Step 6: Commit**

```bash
git add docs/planning docs/operations tests
git commit -m "docs: reconcile onboarding customer and visual canon"
```

---

### Task 4: Human Notion + AI/System Projection

**Files / destinations:**
- Notion: `🔨 블랙스미스 · Home`
- Notion: `02 · Enhancement · Durability · Economy`
- Notion: `03 · UI · 제작 · 경제 Flow Map`
- Notion: `08 · 핵심 시스템 · 상세`
- Notion: `02 · 비주얼 바이블`
- Notion: `🔨 블랙스미스 (Blacksmith)` System Record

**Interfaces:**
- Consumes: merged-ready GitHub branch content, but records PR/head separately until merge.
- Produces: human-readable current game rules with no PR/SHA pollution on Home; AI/System keeps evidence/status metadata.

- [ ] **Step 1: Update Human Home**

Directly show:

```text
강화 성공 = 항상 +1
+9 -> +10 = 정밀강화 + 키워드 생성
+11부터 실패 시 손상 가능, 고강화일수록 위험 증가
손상 = 일반 / 경미 / 중대 / 파괴
고객에게 간 작품은 실제 고객/세계 이벤트에서 손상될 수 있음
강화 시도별 날짜 로그 없음; 의미 있는 작품 사건만 Chronicle
그림체 = Illustrated Workshop Book
```

Remove CURRENT/MAX and five structural-state claims from Home. Do not invent exact damage percentages or repair costs.

- [ ] **Step 2: Update Enhancement detail pages**

Make the four-state model and two damage sources the direct human canon. Old repair formulas should be clearly marked superseded/pending replacement rather than displayed as current instructions.

- [ ] **Step 3: Update Visual Bible**

Set `ILLUSTRATED_WORKSHOP_BOOK` to `USER_APPROVED_DIRECTION`. Mark prior generated boards and the new style board as references whose stale system content must not be implemented verbatim.

- [ ] **Step 4: Update AI/System Record**

Record Decision IDs, PR/head, current Base receipt, blockers, runtime `NOT_RUN`, and `PRODUCT_IMPLEMENTATION_BLOCKED`. Preserve the clarification that Notion Asset records may link Drive sources without direct Preview binary attachment.

- [ ] **Step 5: Server readback**

Fetch each changed Notion surface and verify there is no current `CURRENT/MAX` authority statement in the human current sections.

---

### Task 5: Google Sheet Same-ID Compatibility Mirror

**Files / destinations:**
- Sheet `00_프로젝트_허브`
- Sheet `02_현재_확정결정`
- Only other existing compatibility rows that directly claim CURRENT/MAX or old precision cadence as current, when needed for conflict removal.

**Interfaces:**
- Consumes: same four Decision IDs.
- Produces: migration mirror only; does not become runtime authority.

- [ ] **Step 1: Add/update same-ID rows**

Write rows for:

```text
BS-ENHANCE-20260825-25
BS-DAMAGE-20260825-26
BS-CHRONICLE-20260825-27
BS-ART-20260825-03
BS-OPS-20260825-07
```

Use status `USER_APPROVED / REPO_UPDATE_REQUIRED` before merge and explicitly record unresolved numeric damage/repair gates.

- [ ] **Step 2: Update Hub status**

Set planning state to simplified core canon migration; next approval bundle must be:

```text
DAMAGE_PROBABILITY_CURVE
MINOR_MAJOR_REPAIR_MODEL
CUSTOMER_EVENT_DAMAGE_POLICY
REPRESENTATIVE_VISUAL_REGENERATION_AFTER_SYSTEM_SYNC
```

- [ ] **Step 3: Read back exact rows**

Verify IDs, approval status, branch/head evidence, and no accidental claim that numeric probabilities or repair costs are final.

---

### Task 6: Exact-Head Verification, Merge, and Post-Merge Readback

**Files:**
- PR #207 only.
- No protected product runtime path changes.

**Interfaces:**
- Consumes: Tasks 1~5.
- Produces: merged planning canon and synchronized destinations.

- [ ] **Step 1: Inspect changed files**

Assert that no path begins with:

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

- [ ] **Step 2: Verify exact HEAD**

Run all current PR workflows. Required minimum evidence:

```text
core simplification contract = PASS
current authority contract = PASS
project core alignment = PASS
Base/adapter/BCA workflows = PASS where triggered
PR validation = PASS
```

Godot product behavior remains `NOT_RUN` for this planning-only migration; if the standard PR workflow performs headless import/smoke automatically, record that as regression evidence only, not implementation evidence for the new mechanics.

- [ ] **Step 3: Adversarial five-loop review**

Check:

```text
1. hidden CURRENT/MAX did not survive as current authority
2. +20/+30/+40/+50 precision did not survive as current cadence
3. exact damage percentages or repair economics were not invented
4. customer purchase is not misread as automatic damage
5. routine telemetry/ledger retention is not confused with player-facing Chronicle display
```

- [ ] **Step 4: Re-read Base/main, Blacksmith/main, and PR #196 before merge**

If Base advanced, inspect the changed scope before proceeding. PR #196 remains read-only.

- [ ] **Step 5: Mark PR #207 ready and squash merge only this PR**

Use expected head SHA to prevent merging an unreviewed head.

- [ ] **Step 6: Post-merge destination sync**

Replace pre-merge branch/head receipts in System Record and Sheet with the new Blacksmith `main` SHA and `POSTMERGE_READBACK_PASS` after actual readback.

- [ ] **Step 7: Final evidence ceiling**

Final report must say:

```text
PLANNING_CANON_SYNC = VERIFIED
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = NOT_RUN / BLOCKED
DAMAGE_CURVE_NUMBERS = NOT_FINAL
REPAIR_MODEL = NOT_DECIDED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_GEOMETRY = NOT_RUN
```

---

## Plan Self-Review

- Spec coverage: enhancement +1, +10 Precision Keyword, four-state damage, post-+10 rising damage risk, customer/world event damage, event-only Chronicle, and Illustrated Workshop Book are all assigned to explicit tasks.
- Scope: runtime code/data migration is intentionally excluded because the project implementation gate is closed and repair/damage numeric policy is unresolved.
- No placeholder runtime values are introduced; unresolved balance/economy items are named approval gates rather than implementation steps.
- Current authoritative surfaces and historical evidence are separated rather than rewriting history.
