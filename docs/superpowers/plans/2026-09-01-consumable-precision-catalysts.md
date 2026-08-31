# Blacksmith 소모형 정밀강화 촉매 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 사용자가 확정한 대로 정밀강화의 선택 항목을 가상의 `촉매 계보`가 아니라 실제 보유·소모되는 자원 **불의 심장**과 **대지의 결정**으로 교체한다. 모든 `+10` 단위 정밀강화 시도는 유효한 태그 선택, 일반 강화 비용·보강재, 해당 촉매 1개를 원자적으로 처리하며, 실패 보류·실패 손상도 촉매를 소비하고 저장 실패는 전부 복구한다.

**Architecture:** 새 Decision40과 catalog schema V3가 촉매의 이름·태그 연결·소모 단위를 기계 정본으로 가진다. `VSSaveEnvelope` V5가 신규 캠페인과 V4 이전 저장에만 두 촉매의 테스트용 시작 재고를 제공하고, `VSPrecisionResolver`는 선택에서 촉매 요구사항을 해석한다. `VSEnhancementActionService`는 후보 저장본에 골드·보강재·촉매를 함께 차감한 뒤 저장 성공시에만 live 자원을 반영한다. 기존 Workshop native Control만 명칭과 재고/비용 표기로 갱신하므로 raster image 또는 scene serialization은 추가하지 않는다.

**Tech Stack:** Godot 4.x GDScript, GUT 9.7.1, repository JSON/Markdown contracts, Python unittest contracts, project-authoritative Godot live-editor runtime evidence.

**Spec:** [2026-09-01-precision-catalyst-resource-design.md](../specs/2026-09-01-precision-catalyst-resource-design.md)

## Global constraints

- `BS-ENHANCE-20260901-40`은 Decision38의 **lineage input / no-inventory / no-consumption** 필드만 부분 대체한다. 모든 10 단위 이정표, 최대 세 태그/각 IV, `CATALYST_AFFIX` 한 슬롯, `+1` 성공, 내구도·손상·수리·확률 계약은 보존한다.
- 촉매는 `HEART_OF_FLAME` / `heart_of_flame` / **불의 심장**, `EARTH_CRYSTAL` / `earth_crystal` / **대지의 결정** 두 종류다. 둘 모두 `units_per_precision_attempt = 1`이며, 판매 가격·드롭·상점·랜덤·재추첨·새 인벤토리 화면은 이번 slice에 포함하지 않는다.
- `ADD_TAG`은 정확히 `{ "action": "ADD_TAG", "catalyst_id": "…", "method_id": "…" }`이고, `UPGRADE_TAG`은 정확히 `{ "action": "UPGRADE_TAG", "tag_id": "…" }`이다. 후자는 저장 태그에서 촉매를 역산한다. 모든 선택은 attempt-local이고 저장하지 않는다.
- 후보 저장본의 재고는 `gold`, `common_reinforcement_material`, 필요한 촉매를 함께 차감한다. pre-roll의 잘못된 선택/부족 촉매는 저장 호출·roll·live 재고 변경 전에 막는다. 정상 `SUCCESS`/`FAILED_HOLD`/`FAILED_DAMAGE`는 촉매를 소비하며, `SAVE_FAILED`는 후보와 live 자원 모두 변경하지 않는다.
- V5는 정확히 두 촉매가 저장된 값으로 존재한다. V4 저장에서 두 키가 모두 빠졌을 때만 각 64개를 한 번 이관하고, V5를 다시 열어도 재지급하지 않는다. 단일 키만 빠진 V4나 음수/비정수 값은 fail-closed validation error다. 시작 64개는 `TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`이다.
- 정밀 태그 정정(backfill)은 과거 성공의 무료 정정 경로로 남고 촉매·골드·보강재를 소모하지 않는다. 단 선택 형식은 새 `catalyst_id`를 사용한다.
- 모든 새 UI는 기존 720×1280 Workshop의 native Controls이고 클릭 가능한 선택지는 최소 48dp를 유지한다. 신규 이미지, `assets/`, `.tscn`, `project.godot`, 새 economic loop를 만들지 않는다.
- 자동 테스트와 live runtime 관찰은 별개다. Android, 접근성, 성능, human playtest, release는 실행하지 않은 이상 `NOT_RUN`이다.

---

### Task 1: Current-canon amendment and catalyst catalog (RED → GREEN → REFACTOR)

**Files:**
- Create: `docs/decisions/BS-ENHANCE-20260901-40_CONSUMABLE_PRECISION_CATALYST_RESOURCES.md`
- Modify: `docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`
- Modify: `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- Modify: `docs/decisions/BS-ENHANCE-20260830-38_RECURRING_PRECISION_TAG_EVOLUTION.md`
- Modify: `docs/decisions/BS-ENHANCE-20260829-37_PRECISION_TAG_CATALOG_AND_SELECTION_GATE.md`
- Modify: `docs/decisions/BS-ENHANCE-20260828-34_WEAPON_KEYWORD_OWNERSHIP.md`
- Modify: `docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md`
- Modify: `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md`
- Modify: `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`
- Modify: `tests/check_precision_tag_catalog_contract.py`
- Modify: `tests/check_core_simplification_current_contract.py`

**Interfaces:** catalog schema V3 contains a two-entry `catalysts` array and each tag uses `catalyst_id`, never `lineage_id`.

- [ ] **Step 1 — RED:** add static assertions for Decision40, V3, exactly two item names/stock keys, all four tags, one unit use, and no current owner that still calls the input a `lineage`. Run:

  ```powershell
  python tests/check_precision_tag_catalog_contract.py
  python tests/check_core_simplification_current_contract.py
  ```

  Expected: FAIL because catalog V2 and current owners require `lineage_id` and expressly forbid inventory/consumption.

- [ ] **Step 2 — GREEN:** create the Korean Decision40 with supersession matrix, player-visible flow, exact V4→V5 migration, atomic charge truth table, benchmark `ADOPT / ADAPT / REJECT`, and evidence ceiling. Raise catalog to V3:

  ```json
  {
    "schema_version": 3,
    "source_decision_id": "BS-ENHANCE-20260901-40",
    "catalysts": [
      {"id": "HEART_OF_FLAME", "material_stock_key": "heart_of_flame", "display_name_ko": "불의 심장", "units_per_precision_attempt": 1},
      {"id": "EARTH_CRYSTAL", "material_stock_key": "earth_crystal", "display_name_ko": "대지의 결정", "units_per_precision_attempt": 1}
    ]
  }
  ```

  Change each tag’s `lineage_id` to its `catalyst_id`; preserve tag IDs, methods, effects, stages, and ten precision targets. Mark contrary historical claims `[부분 대체됨]`, rather than deleting their evidence.

- [ ] **Step 3 — REFACTOR / verification:** make the Python checks reject duplicate catalyst IDs, an unknown tag catalyst, nonpositive units, stale `lineage_id`, or an owner/canonical mismatch. Read all changed owners back and run the two checks GREEN. Commit this canon-only slice as `docs: define consumable precision catalysts`.

### Task 2: V5 workshop-resource migration and exact starter allocation (RED → GREEN → REFACTOR)

**Files:**
- Modify: `scripts/vertical_slice/domain/vs_save_envelope.gd`
- Modify: `data/vertical_slice/vertical_slice_preset.json` only if the active preset schema owner needs its starter resource data synchronized
- Modify: `tests/gut/unit/vertical_slice/test_vs_save_service.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_v2_save_boundary.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_action_archive.gd`
- Modify: relevant Python preset contract only if that data file changes

**Interfaces:** `VSSaveEnvelope.SCHEMA_VERSION = 5`; `starter_workshop_resources()` includes `heart_of_flame: 64` and `earth_crystal: 64`; a V5 serializes the quantities without a later grant.

- [ ] **Step 1 — RED:** add GUT fixtures for fresh V5, V4 with both catalyst keys missing, V4 with exactly one missing key, malformed catalyst quantities, and V5 re-open. Assert the two valid migrations produce 64 each only once, and the invalid shapes remain validation errors.

  ```gdscript
  func test_v4_without_both_catalyst_keys_migrates_once_to_v5_starter_stock() -> void:
      var envelope := VSSaveEnvelope.from_dict(_v4_payload_without_catalysts())
      assert_eq(envelope.schema_version, 5)
      assert_eq(envelope.workshop_resources["heart_of_flame"], 64)
      assert_eq(envelope.workshop_resources["earth_crystal"], 64)
      var reopened := VSSaveEnvelope.from_dict(envelope.to_dict())
      assert_eq(reopened.workshop_resources["heart_of_flame"], 64)
  ```

  Run the focused save/action GUT files; expected RED because V4 is current and starter stock lacks both resources.

- [ ] **Step 2 — GREEN:** add an explicit source-schema migration branch before generic resource normalization. Keep existing gold/common material values and every item/ledger field byte-equivalent. Apply the grant only when the source is V4 and both keys are absent, validate all V5 values as safe nonnegative integers, and retain dynamic snapshot restoration in `VSMainMenu`.

- [ ] **Step 3 — REFACTOR / verification:** remove duplicated fixture literals through a test helper, test load-save-load idempotence, verify existing pre-V4 migration still yields the same new-campaign allocation, and run the focused tests GREEN. Commit `feat: migrate precision catalyst resources`.

### Task 3: Catalyst-aware resolver and atomic enhancement service (RED → GREEN → REFACTOR)

**Files:**
- Modify: `scripts/vertical_slice/resolvers/vs_precision_resolver.gd`
- Modify: `scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd`
- Modify: `scripts/vertical_slice/services/vs_enhancement_action_service.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_precision_tag_catalog.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_resolver.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_resolution.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_enhancement_action_archive.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_precision_customer_context_runtime.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_precision_customer_context_adversarial.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_precision_isolated_runtime_qa.gd`

**Interfaces:** all precision preview results expose `precision_catalyst_id`, `precision_catalyst_stock_key`, `precision_catalyst_display_name_ko`, and `precision_catalyst_units`. The resolver has no resource mutation; the service owns the one-unit check/deduction.

- [ ] **Step 1 — RED:** change every selection fixture to the `catalyst_id` form and write acceptance tests for `ADD_TAG`, derived `UPGRADE_TAG`, insufficient catalyst pre-roll block, success/hold/damage consumption, save-failure restoration, and zero-cost backfill. Include a normal `+11` failure test proving no catalyst is charged outside precision milestones.

  ```gdscript
  func test_precision_hold_consumes_one_required_catalyst_after_save() -> void:
      var resources := _resources_with("heart_of_flame", 1)
      var result := service.resolve_and_save_with_rolls(
          envelope, _item_uid, 10, {"success_roll_percent": 99.0}, 1,
          resources, save_service,
          {"action": "ADD_TAG", "catalyst_id": "HEART_OF_FLAME", "method_id": "EDGE_REINFORCEMENT"}
      )
      assert_eq(result["outcome"], "FAILED_HOLD")
      assert_eq(resources.get_material_count("heart_of_flame"), 0)
  ```

  Run all listed focused GUT suites. Expected: RED because selection resolves an unowned `lineage_id` and no catalyst cost is present.

- [ ] **Step 2 — GREEN:** make the catalog resolver validate schema V3/catalyst relationships fail-closed. `ADD_TAG` requires catalyst+method; `UPGRADE_TAG` derives catalyst from the stored tag. Update enhancement preview/result payloads, and in the action service take the required stock key/unit from preview, reject shortage before candidate/roll/save, stage its deduction beside gold/common reinforcement, and synchronize live resources only after `save_envelope(candidate) == OK`. Attach Decision40 as the tag growth ledger provenance without changing ordinary enhancement history behavior.

- [ ] **Step 3 — REFACTOR / verification:** keep only one helper for preview catalyst metadata and one helper for staged resource deduction. Verify malformed data cannot fall back to a free default; `FAILED_HOLD`/`FAILED_DAMAGE` alter no tag state while consuming one saved catalyst; `SAVE_FAILED` leaves all three resources and item state unchanged. Run focused suites GREEN. Commit `feat: consume catalysts for precision attempts`.

### Task 4: Workshop native UX and player-facing contract (RED → GREEN → REFACTOR)

**Files:**
- Modify: `scripts/vertical_slice/ui/vs_workshop_screen.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd`
- Modify: `docs/planning/BLACKSMITH_RECURRING_PRECISION_VISUAL_REQUIREMENTS_20260830.json`
- Modify: `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md`
- Modify: `docs/design/PROJECT_AI_PRODUCTION_SPEC.md`
- Modify: `tests/check_human_facing_gdd_and_review_loop_contract.py`
- Modify generated `exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf` and its existing receipt only if its current publisher/checker requires source-PDF parity

**Interfaces:** UI controls are renamed `PrecisionCatalystLabel` / `PrecisionCatalystOption`; the state exposes current resource count, required name, and `소모: <name> ×1`; `UPGRADE_TAG` displays the derived catalyst read-only.

- [ ] **Step 1 — RED:** change workshop GUT references from lineage controls to catalyst controls and assert Korean text never contains `계보`, ADD cannot confirm without catalyst+method, UPGRADE exposes its derived catalyst, unavailable stock disables confirm with a player-facing shortage reason, and option controls remain at least 48dp.

- [ ] **Step 2 — GREEN:** replace only the dynamic native control labels/options and selection dictionary construction. In the existing precision preview show chosen/derived item, live count, one-unit cost, tag outcome, normal price/odds, and the existing selection requirements. Map `MISSING_PRECISION_CATALYST` to a Korean explanation; do not add a texture, separate inventory page, or new scene.

- [ ] **Step 3 — document / visual-consumer consistency:** revise the existing visual requirement so it declares native precision UX and no separate precision-forge image. Update human GDD/technical trace to say `불의 심장`/`대지의 결정`, one unit per attempt, all normal outcomes consume, and save failure restores; preserve all evidence ceilings. Regenerate/check the PDF only through its existing repository publisher and receipt workflow; otherwise leave unrelated PDF bytes untouched and document that source-only change is the verified scope.

- [ ] **Step 4 — REFACTOR / verification:** run focused UI and document contract tests. Inspect for stale current `불씨 계보`, `모루 계보`, `lineage_id`, and forbidden no-inventory language, allowing only clearly marked historical references. Commit `feat: present consumable precision catalysts`.

### Task 5: Exact-head regression, adversarial review, runtime capture, and delivery

**Files:**
- Modify: `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md` only for exact verified status/evidence
- Do not modify protected paths beyond the files from Tasks 1–4.

- [ ] **Step 1 — full machine verification:** run the project operating-contract validator, every modified Python contract, full Python discovery, Godot import/headless opening, and all GUT unit/integration suites. Run `git diff --check`, protected-path audit, and catalog/document source readback at exact `HEAD`.

  ```powershell
  & 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
    'C:\Users\user\Documents\GitHub\Base\Base-worktrees\blacksmith-validator-43b3\tools\check_project_operating_contract.py' `
    --project-root . --base-repository 'C:\Users\user\Documents\GitHub\Base\Base-worktrees\blacksmith-validator-43b3' --check
  python -m unittest discover -s tests -p 'test_*.py' -v
  godot --headless --editor --path . --quit
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit -gdir=res://tests/gut/integration -ginclude_subdirs -gexit
  git diff --check
  ```

- [ ] **Step 2 — adversarial acceptance readback:** verify each rejection and outcome against actual test results: wrong/empty catalyst, one-sided V4 migration, malformed stock, insufficient stock before roll, 10 milestones only, hold/damage consumption, save failure restoration, backfill free, no precision charge on ordinary levels, no fourth affix, no loss of durability/checkpoint rules.

- [ ] **Step 3 — live game evidence:** use the project-authoritative live editor/MCP to open the changed exact head, reach a `+9 → +10` ADD selection, capture the visible **불의 심장** count/cost state, then prepare an UPGRADE flow showing derived catalyst. Save screenshots as runtime evidence only after actual observation. Do not call static tests or generated art a runtime pass.

- [ ] **Step 4 — delivery:** fetch and recheck `origin/main`, rebase only if required and non-conflicting, push the isolated `codex/precision-catalysts-20260901` branch, verify its remote SHA/readback, create/update only the current narrow PR according to repository routing, and report exact machine/runtime/NOT_RUN evidence separately. Never change direct `main` or PR #196.

## Plan self-review

- **Coverage:** Tasks 1–2 establish authoritative language/catalog and lossless V5 save migration; Task 3 protects the game-affecting atomic deduction boundary; Task 4 makes the approved fantasy item names understandable in the existing mobile UX and human-facing contract; Task 5 distinguishes static, runtime, and human verification before delivery.
- **Dependencies:** current canon/catalog must precede migration; migration must precede resource action service; resolver/action service must precede UI; source documentation and live evidence are last so they describe the actual implementation.
- **Safety:** no random economy, art asset, image generation, scene serialization, project settings change, unapproved product expansion, or direct-main mutation is included. The only new resource quantities are V5-stored and are deliberately labelled temporary vertical-slice test allocation.
- **Type consistency:** `catalyst_id` is a catalog ID; `material_stock_key` is the persisted resource key; `tag_id` remains the item’s existing `CATALYST_AFFIX` identity. No catalyst choice is saved as a fourth affix or per-attempt field.
