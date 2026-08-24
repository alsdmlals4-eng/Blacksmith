# Blacksmith Release-near V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one complete Nadia-centered causal lifecycle vertical slice on a production-shaped V2 domain that supports the current +0~+100 enhancement canon, CURRENT/MAX durability, customer context, visitor standing/epithet, delayed world result, save/load, and same-UID return.

**Architecture:** Reuse the existing MainMenu/App shell, UID service, atomic save pattern, ledger concept, and ContentResultRecord primitive. Replace the pre-release V1 item/preset contract with an explicit V2 schema, keep the human-facing slice narrow (SWORD/iron + Nadia), and put gameplay rules in focused domain/resolver classes rather than UI scripts.

**Tech Stack:** Godot 4.7.1 / GDScript / GUT 9.7.1 / JSON data / GitHub Actions.

**Spec:** `docs/planning/BLACKSMITH_RELEASE_NEAR_VERTICAL_SLICE_CANON_20260824.md`, `docs/planning/BLACKSMITH_VISITOR_PUBLIC_STANDING_CANON_20260824.md`, Decisions 01~24.

## Global Constraints

- Current planning package is closed by the user's `기획 완료` declaration.
- Implement only current canon; historical PoC behavior is reference evidence, not authority.
- TDD is mandatory: failing test first, verified RED, minimal GREEN, then refactor.
- `SWORD / iron` is a slice fixture, not a global optimum or Nadia permanent preference.
- Product domain must accept enhancement `0..100`; human slice focuses on +0~+11.
- `CURRENT==0 or MAX==0` is causal physical destruction; no separate destroy roll.
- Checkpoints are `[10,30,60,90]`; precision milestones are `[10,20,30,40,50]`.
- Visitor grades are `COMMON / SKILLED / ELITE / RENOWNED / LEGENDARY`; grade gives no direct success/price/reward multiplier.
- Nadia starter baseline: `ELITE / 정예`, epithet `유적의 길잡이`, role `유적 탐사대장`.
- No universal fit score or Best badge.
- Customer enhancement contribution is `round(0.30 * enhancement_level)` pp as a non-final test budget.
- No image generation or new representative art without separate explicit visual approval.
- Human/Android/accessibility PASS cannot be inferred from CI.

---

### Task 1: V2 Item and Save Boundary

**Files:**
- Modify: `scripts/vertical_slice/domain/vs_item.gd`
- Modify: `scripts/vertical_slice/domain/vs_save_envelope.gd`
- Modify: `scripts/vertical_slice/services/vs_run_initializer_service.gd`
- Modify: `scripts/vertical_slice/services/vs_save_service.gd`
- Modify: `data/vertical_slice/vertical_slice_schema.json`
- Modify: `data/vertical_slice/vertical_slice_preset.json`
- Test: `tests/gut/unit/vertical_slice/test_vs_item.gd`
- Test: `tests/gut/unit/vertical_slice/test_vs_save_service.gd`
- Create test: `tests/gut/unit/vertical_slice/test_vs_v2_save_boundary.gd`

**Interfaces:**
- `VSItem.from_dict(Dictionary) -> VSItem`
- `VSItem.to_dict() -> Dictionary`
- `VSSaveEnvelope.from_dict(Dictionary) -> VSSaveEnvelope`
- V2 root `schema_version = 2`, `preset_version = "VS-2026.08.24-B"`.
- V1 root produces explicit legacy-pre-release status and is never silently parsed as V2.

- [ ] **Step 1: Write failing V2 item tests**

Add tests that require V2 fields:

```gdscript
func test_v2_item_accepts_current_canon_range_and_durability() -> void:
    var item := VSItem.from_dict(_valid_v2_item({
        "enhancement_level": 100,
        "highest_checkpoint": 90,
        "current_durability": 41,
        "max_durability": 57,
        "physical_state": "ACTIVE",
    }))
    assert_true(item.validation_errors.is_empty())

func test_v2_item_rejects_current_above_max() -> void:
    var item := VSItem.from_dict(_valid_v2_item({
        "current_durability": 80,
        "max_durability": 70,
    }))
    assert_has(item.validation_errors, "CURRENT_EXCEEDS_MAX")
```

- [ ] **Step 2: Verify RED**

Run the focused GUT file with the project-approved Godot 4.7.1 runner. Expected failure: V2 fields/range are missing and old max-level 10 validation rejects 100.

- [ ] **Step 3: Implement minimal V2 item schema**

Replace old damage enum ownership with:

```text
current_durability: int 0..100
max_durability: int 0..100
physical_state: ACTIVE | DESTROYED
highest_checkpoint: int in 0,10,30,60,90
overhaul_used: bool
max_enhancement_reached: bool
enhancement_recovery_by_target: Dictionary
```

Retain UID, birth seed, provenance, grade, artistry, raw role stat, weight, functions, affixes, owner, and ledger.

- [ ] **Step 4: Write failing V1 save rejection test**

```gdscript
func test_v1_pre_release_save_is_explicitly_legacy_not_silently_migrated() -> void:
    var result = VSSaveService.inspect_save_dict(_valid_v1_save())
    assert_eq(result.status, "LEGACY_PRE_RELEASE_SAVE")
```

- [ ] **Step 5: Verify RED, then implement V2 envelope/initializer/save service**

V2 new-game initialization must create empty valid V2 state. Existing atomic temp/backup behavior stays intact.

- [ ] **Step 6: Run focused and existing save/item suites**

Expected: all Task 1 tests GREEN; old tests updated only where V1 expectations are intentionally superseded.

- [ ] **Step 7: Commit**

`feat: migrate vertical slice item and save domain to v2`

---

### Task 2: Canonical Enhancement Resolver

**Files:**
- Create: `scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd`
- Create: `scripts/vertical_slice/domain/vs_enhancement_state.gd`
- Create: `data/vertical_slice/enhancement_v2.json`
- Create test: `tests/gut/unit/vertical_slice/test_vs_enhancement_resolver.gd`

**Interfaces:**

```gdscript
VS_EnhancementResolver.preview(item: VSItem, target_level: int) -> Dictionary
VS_EnhancementResolver.resolve(item: VSItem, target_level: int, rng: RandomNumberGenerator) -> Dictionary
```

Preview must expose target band, final success chance, cost, required reinforcement material, checkpoint, outcome family probabilities, CURRENT/MAX risk, recovery state, and next checkpoint.

- [ ] **Step 1: RED tests for target bands, checkpoints, costs and +100 ceiling**
- [ ] **Step 2: RED tests for same-target recovery +6pp, soft cap 95 and hard guarantees**
- [ ] **Step 3: RED tests for failure family tables and no separate destroy/scar roll**
- [ ] **Step 4: RED tests for CURRENT/MAX invariant and causal destruction**
- [ ] **Step 5: Implement minimal preview/resolve logic from Decisions 13~18**
- [ ] **Step 6: RED/GREEN +100 terminal test**

```gdscript
assert_eq(result.item.enhancement_level, 100)
assert_true(result.item.max_enhancement_reached)
assert_false(result.actions.has("ENHANCE_TO_101"))
```

- [ ] **Step 7: Run full focused resolver suite and commit**

`feat: add canonical v2 enhancement resolver`

---

### Task 3: Repair, Overhaul, Destruction Archive

**Files:**
- Create: `scripts/vertical_slice/resolvers/vs_repair_resolver.gd`
- Create: `scripts/vertical_slice/resolvers/vs_overhaul_resolver.gd`
- Create: `scripts/vertical_slice/domain/vs_destroyed_history_record.gd`
- Create test: `tests/gut/unit/vertical_slice/test_vs_repair_overhaul_destruction.gd`

**Interfaces:**

```gdscript
VSRepairResolver.quote(item, primary_material_id) -> Dictionary
VSRepairResolver.apply(item, wallet, reinforcement_units) -> Dictionary
VSOverhaulResolver.quote(item, primary_material_id) -> Dictionary
VSOverhaulResolver.apply(item, wallet, reinforcement_units) -> Dictionary
```

- [ ] **Step 1: RED repair quote tests** for `SWORD_BASE_R=800`, material multiplier, secured-band multiplier, missing-CURRENT formula, mandatory gold + reinforcement.
- [ ] **Step 2: GREEN repair logic**; repair sets `CURRENT=MAX`, never restores MAX.
- [ ] **Step 3: RED overhaul eligibility/cost/effect tests**.
- [ ] **Step 4: GREEN one-lifetime overhaul** with `MAX=min(60,MAX+15)`, `CURRENT=MAX`, `overhaul_used=true`.
- [ ] **Step 5: RED destruction record test**: zero CURRENT/MAX produces immutable archive snapshot and blocks repair/overhaul/enhancement.
- [ ] **Step 6: GREEN destruction/archive logic and commit**.

`feat: add repair overhaul and causal destruction v2`

---

### Task 4: Precision + Visitor Profile + Public Standing

**Files:**
- Create: `scripts/vertical_slice/domain/vs_customer_profile.gd`
- Create: `scripts/vertical_slice/domain/vs_customer_context_packet.gd`
- Create: `scripts/vertical_slice/resolvers/vs_precision_resolver.gd`
- Create: `scripts/vertical_slice/resolvers/vs_customer_context_resolver.gd`
- Create: `data/vertical_slice/customers/nadia_venn.json`
- Create test: `tests/gut/unit/vertical_slice/test_vs_customer_profile.gd`
- Create test: `tests/gut/unit/vertical_slice/test_vs_precision_customer_context.gd`

**Interfaces:**

```gdscript
VSCustomerProfile.from_dict(value) -> VSCustomerProfile
VSCustomerContextResolver.evaluate(customer, item, context) -> Dictionary
VSPrecisionResolver.preview(item, milestone, method, catalyst) -> Dictionary
```

Customer profile fields:

```text
customer_id
name
role
public_epithet
public_standing_grade
strength / dexterity / constitution / judgment
weapon_proficiency
maximum_load
```

- [ ] **Step 1: RED grade validation test**

Accept only `COMMON/SKILLED/ELITE/RENOWNED/LEGENDARY`; prove grade does not alter the event success calculation.

- [ ] **Step 2: RED Nadia identity test**

```text
NADIA_VENN
ELITE / 정예
유적의 길잡이
유적 탐사대장
```

- [ ] **Step 3: GREEN customer profile parser/data**.
- [ ] **Step 4: RED customer context tests** for hard load gate, enhancement contribution `round(0.30*level)`, ability/proficiency context, no universal fit score.
- [ ] **Step 5: GREEN context resolver**.
- [ ] **Step 6: RED precision preview tests** showing `DIRECT_HELP / GATE_CHANGE / TRADE_OFF / NOT_DIRECTLY_RELEVANT`, with catalyst selection itself giving no customer bonus.
- [ ] **Step 7: GREEN precision resolver and commit**.

`feat: connect precision crafting to visitor context`

---

### Task 5: Nadia Handoff, Day Progression, Delayed Result

**Files:**
- Create: `scripts/vertical_slice/resolvers/vs_nadia_schedule_resolver.gd`
- Create: `scripts/vertical_slice/services/vs_day_progression_service.gd`
- Modify: `scripts/vertical_slice/domain/vs_content_result_record.gd` only if V2-compatible fields require a schema bump.
- Create test: `tests/gut/unit/vertical_slice/test_vs_nadia_schedule_resolver.gd`

**Interfaces:**

```gdscript
VSNadiaScheduleResolver.handoff(customer, item, context) -> Dictionary
VSDayProgressionService.advance_day(save_envelope, rng) -> Dictionary
```

- [ ] **Step 1: RED handoff tests**: overweight blocked, active non-destroyed item required, STOP at +10 and PUSH result at +11 both legal.
- [ ] **Step 2: GREEN handoff**: owner/lifecycle and schedule state update atomically.
- [ ] **Step 3: RED delayed-result test**: handoff does not resolve expedition immediately.
- [ ] **Step 4: RED result-shape test** requiring exactly Nadia's three result axes, 2~4 causal reasons, same UID, one primary next action.
- [ ] **Step 5: GREEN day/schedule resolver and commit**.

`feat: add delayed Nadia lifecycle result`

---

### Task 6: Product Screens and Routing

**Files:**
- Modify: `scripts/vertical_slice/ui/vs_app.gd`
- Modify: `scenes/vertical_slice/screens/vs_workshop_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_forge_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_item_birth_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_enhancement_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_precision_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_customer_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_result_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_repair_screen.tscn`
- Create: `scenes/vertical_slice/screens/vs_item_detail_screen.tscn`
- Create corresponding focused UI scripts under `scripts/vertical_slice/ui/`.
- Test: `tests/gut/unit/vertical_slice/test_vs_app.gd`
- Create test: `tests/gut/unit/vertical_slice/test_vs_release_near_routing.gd`

- [ ] **Step 1: RED routing tests** for the Decision25 graph.
- [ ] **Step 2: GREEN routing only; no gameplay calculations in UI**.
- [ ] **Step 3: RED visitor-card header test** requiring text-readable `[정예]`, `「유적의 길잡이」`, `나디아 벤`, `유적 탐사대장` and no color-only state.
- [ ] **Step 4: GREEN minimal engine-native UI** with ≥48dp primary targets.
- [ ] **Step 5: RED enhancement disclosure tests** for +10 STOP/+11 PUSH and CURRENT/MAX.
- [ ] **Step 6: GREEN screens and commit**.

`feat: add release-near vertical slice screens`

---

### Task 7: End-to-End Functional Slice and Save/Load

**Files:**
- Create: `tests/gut/integration/vertical_slice/test_vs_release_near_lifecycle.gd`
- Modify focused services/resolvers only when the failing integration test demonstrates a gap.

- [ ] **Step 1: RED E2E path**

Prove:

```text
New Game V2
-> Nadia context
-> iron sword creation / UID
-> +1..+10
-> precision
-> STOP or +11 PUSH
-> handoff
-> save/load same UID
-> advance day(s)
-> Nadia result
-> same UID result state
-> repair/item detail
-> workshop
```

- [ ] **Step 2: Verify RED from the earliest missing integration seam**.
- [ ] **Step 3: Implement only required glue**.
- [ ] **Step 4: GREEN both STOP and PUSH fixture branches**.
- [ ] **Step 5: Add deterministic edge fixtures** for +100, overhaul, destruction archive without requiring human grind.
- [ ] **Step 6: Run all vertical-slice GUT + Python contract tests and commit**.

`test: verify complete causal lifecycle vertical slice`

---

### Task 8: Verification and Evidence Gate

**Files:**
- Update: `docs/operations/` with a new implementation evidence report.
- Update: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Update relevant Notion Production/Handoff and Registry surfaces.

- [ ] **Step 1: Exact-head CI**: all required project workflows GREEN.
- [ ] **Step 2: Fresh main/open-PR check** after merge.
- [ ] **Step 3: Runtime smoke** with the project-approved Godot 4.7.1 execution path.
- [ ] **Step 4: Save/reload/recovery smoke** including legacy V1 fail-closed behavior.
- [ ] **Step 5: Record evidence ceiling**:

```text
DOMAIN_VERIFIED only if automated domain evidence passes
FUNCTIONAL_SLICE_VERIFIED only if actual full path runs
RELEASE_NEAR_VERIFIED remains blocked until Human + Android + accessibility + performance/crash smoke
```

- [ ] **Step 6: Keep Issue #69 / human-platform backlog open until actual evidence exists**.

## Plan Self-Review

- Spec coverage: Decisions 13~26 that directly affect the slice are mapped to Tasks 1~8.
- No +11-only domain shortcut: Task 1/2 require +0~+100.
- No customer rank power leakage: Task 4 explicitly tests grade neutrality.
- No immediate Nadia result regression: Task 5 tests delayed schedule.
- No art-as-readiness substitution: Task 6 is engine-native functional UI first.
- Human/Android claims remain blocked in Task 8.
