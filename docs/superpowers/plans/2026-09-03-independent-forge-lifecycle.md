# Independent Forge Lifecycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the existing five-equipment first forge while making its completed workpiece visibly enter the Workshop, then present the current customer handoff, actual-use report, and item chronicle from the same saved UID facts.

**Architecture:** The first-forge UI becomes a two-stage presenter: `ForgingSession.completed` reveals the existing quality result, and a new one-shot confirmation signal hands that unchanged result to `VSMainMenu` for persistence. A small read-only customer-profile repository loads only the current Nadia profile. `VSApp` injects that profile into handoff, result, and chronicle presenters; none of those presenters calculates damage, rewards, odds, or new stored content.

**Tech Stack:** Godot 4.x GDScript, existing vertical-slice scenes, GUT 9.7.1, Python repository contracts, project-authoritative runtime capture.

**Spec:** `docs/superpowers/specs/2026-09-03-independent-forge-lifecycle-design.md`

## Global Constraints

- Preserve the current five equipment IDs and their existing transparent V2 art consumers. Do not add equipment types, grade-specific art, raster assets, third-party assets, addons, or a new scene.
- Preserve `ForgingSession` quality math, `CanonicalFirstItemInputAdapter` mapping, current save schema, birth ledger payload, enhancement odds, precision tags, catalyst consumption, durability, repair, and customer/world resolver behavior.
- Keep `PHASE1_HANDOFF_MINIMUM_LEVEL = 10`; handoff itself remains non-damaging, exactly one actual-use result remains authoritative, and the saved result stays the sole damage/next-action owner.
- The only current runtime customer is `NADIA_VENN` from `data/vertical_slice/customers/nadia_venn.json`. Do not create a roster, customer board, schedule, waiting system, combat, dungeon, reward table, ranking, advertising, gacha, or social system.
- Use independent Korean copy such as `작업 보고`; do not reuse foreign title, character, setting, dialogue, letter, UI composition, asset, or economy expression.
- Keep `ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE`; chronicle records only existing birth, precision tag, handoff, actual-use, damage, and repair facts.
- Test every production behavior RED → GREEN → REFACTOR. GUT remains the sole GDScript test authority. Modify production GDScript only after its corresponding failing GUT test is observed.
- Do not touch `scenes/`, `assets/`, `data/`, `addons/`, or `project.godot` in this implementation. Existing `.tscn` structure and direct action NodePaths remain intact.

---

### Task 1: Keep the completed first-forge result visible until the player enters the Workshop

**Files:**

- Modify: `scripts/ui/forging_screen.gd`
- Modify: `scripts/vertical_slice/ui/vs_main_menu.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_main_menu_first_forge_flow.gd`

**Interfaces:**

- Consumes: `ForgingSession.completed(result: Dictionary)` and its existing `result` payload.
- Produces: `ForgingScreen.forge_result_confirmed(result: Dictionary)`, emitted at most once after the player presses `ForgeResultCommitButton`.
- Preserves: `VSMainMenu.apply_completed_first_forge_result(completed_forge_result: Dictionary)` as the only persistence boundary.

- [ ] **Step 1: Write the failing first-forge confirmation test**

  Extend `test_vs_main_menu_first_forge_flow.gd` with a test that opens the real first-forge screen, completes a deliberately one-tap session, and asserts that the screen remains mounted and the Workshop is absent before confirmation.

  ```gdscript
  func test_completed_first_forge_waits_for_explicit_workshop_confirmation() -> void:
      var menu = await _new_menu_with_empty_campaign()
      var forge = menu._active_forge
      forge.session.config["target_progress"] = 1.0
      forge.session.set_precision_enabled(false)
      assert_true(forge.session.register_tap())
      await get_tree().process_frame
      assert_true(menu.has_active_first_forge())
      assert_false(menu.has_active_workshop())
      var commit_button := forge.get_node_or_null("ForgeResultCommitButton") as Button
      assert_not_null(commit_button)
      assert_true(commit_button.visible)
      commit_button.emit_signal("pressed")
      await get_tree().process_frame
      assert_false(menu.has_active_first_forge())
      assert_true(menu.has_active_workshop())
  ```

- [ ] **Step 2: Run the focused test and observe RED**

  Run:

  ```powershell
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -gtest=test_vs_main_menu_first_forge_flow.gd -ginclude_subdirs -gexit
  ```

  Expected: the assertion that the first-forge screen remains mounted fails because the current menu subscribes directly to `ForgingSession.completed` and removes the screen immediately.

- [ ] **Step 3: Implement the smallest two-stage first-forge presenter**

  In `scripts/ui/forging_screen.gd`:

  ```gdscript
  signal forge_result_confirmed(result: Dictionary)

  var _completed_result: Dictionary = {}
  var _result_confirmation_emitted := false

  func _on_session_completed(result: Dictionary) -> void:
      _completed_result = result.duplicate(true)
      _result_confirmation_emitted = false

  func _on_result_commit_pressed() -> void:
      if _completed_result.is_empty() or _result_confirmation_emitted:
          return
      _result_confirmation_emitted = true
      forge_result_confirmed.emit(_completed_result.duplicate(true))
  ```

  Connect the current `session.completed` signal to `_on_session_completed` inside `_start_new_session`. Replace the result-panel restart button with `ForgeResultCommitButton`, use the player-facing label `작품을 공방에 올리기`, and connect it to `_on_result_commit_pressed`. In the `COMPLETE` state, show the existing result statistics and set a next-action message that describes the existing Workshop decision; do not alter any quality result value.

  In `scripts/vertical_slice/ui/vs_main_menu.gd`, replace the direct `session.completed.connect(apply_completed_first_forge_result)` subscription with `forge_result_confirmed.connect(apply_completed_first_forge_result)`. Do not change `apply_completed_first_forge_result` or its save behavior.

- [ ] **Step 4: Run focused GUT GREEN and refactor signal guards**

  Re-run the Task 1 GUT command. Confirm that exactly one button press enters the Workshop and a second press cannot create another item.

- [ ] **Step 5: Commit Task 1**

  ```powershell
  git add scripts/ui/forging_screen.gd scripts/vertical_slice/ui/vs_main_menu.gd tests/gut/unit/vertical_slice/test_vs_main_menu_first_forge_flow.gd
  git commit -m "feat: confirm first forge before workshop entry"
  ```

### Task 2: Load the current customer profile once and present an original work report

**Files:**

- Create: `scripts/vertical_slice/services/vs_customer_profile_repository.gd`
- Modify: `scripts/vertical_slice/domain/vs_customer_profile.gd`
- Modify: `scripts/vertical_slice/ui/vs_customer_handoff_screen.gd`
- Modify: `scripts/vertical_slice/ui/vs_customer_result_screen.gd`
- Modify: `scripts/vertical_slice/ui/vs_app.gd`
- Create: `tests/gut/unit/vertical_slice/test_vs_customer_profile_repository.gd`
- Create: `tests/gut/unit/vertical_slice/test_vs_customer_handoff_screen.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_customer_result_screen.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_app.gd`

**Interfaces:**

- `VSCustomerProfileRepository.load_profile(customer_id: String) -> Dictionary` returns `{ "status": "APPLIED", "profile": VSCustomerProfile }` only when the registered JSON file parses and validates; otherwise it returns `{ "status": "BLOCKED", "reason": String }`.
- `VSCustomerProfile.work_request_summary_ko() -> String` maps the existing `SURVIVAL_AND_RECOVERY` token to `생환과 회수를 위한 탐사`, and returns `기록된 의뢰` for another valid token without inventing a new goal.
- `VSCustomerHandoffScreen.configure_handoff(item_uid, enhancement_level, customer_profile)` and `configure_return_beat(item_uid, customer_profile)` create display-only customer header/context facts.
- `VSCustomerResultScreen.configure_resolved_result(result, customer_profile = null)` accepts an optional display profile and never mutates `result`.
- `VSApp` is the only caller that loads the Phase 1 Nadia profile and injects it into the three presenters.

- [ ] **Step 1: Write failing repository, handoff, result, and app tests**

  Add repository tests that assert Nadia is loaded from the existing JSON with the current name, role, header, and `생환과 회수를 위한 탐사`, while an unregistered ID returns `UNKNOWN_CUSTOMER_ID`.

  Add a handoff-screen test that passes the real profile and requires:

  ```gdscript
  assert_eq(state["customer_header"], "[정예] 「유적의 길잡이」 나디아 벤")
  assert_true(state["customer_context"].contains("유적 탐사대장"))
  assert_true(state["customer_context"].contains("생환과 회수"))
  assert_true(state["message"].contains("인계 자체로는 손상이 발생하지 않습니다"))
  ```

  In `test_vs_customer_result_screen.gd`, pass the real profile to `_resolved_result()` presentation and require the displayed summary to contain `나디아 벤의 실제 사용 작업 보고`. Add an invalid-profile case that is blocked without replacing the last visible stored fact. In `test_vs_app.gd`, begin the real +10 handoff and require the active handoff state to expose the same profile-derived header.

- [ ] **Step 2: Run the focused files and observe RED**

  Run:

  ```powershell
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -gtest=test_vs_customer_profile_repository.gd -ginclude_subdirs -gexit
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -gtest=test_vs_customer_handoff_screen.gd -ginclude_subdirs -gexit
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -gtest=test_vs_customer_result_screen.gd -ginclude_subdirs -gexit
  ```

  Expected: missing repository/screen parameters and hard-coded text fail before implementation.

- [ ] **Step 3: Implement the data-first profile boundary**

  Create `VSCustomerProfileRepository` with a fixed current map:

  ```gdscript
  const CUSTOMER_DATA_PATHS := {
      "NADIA_VENN": "res://data/vertical_slice/customers/nadia_venn.json",
  }
  ```

  Read with `FileAccess.open`, parse with `JSON.parse_string`, construct through `VSCustomerProfile.from_dict`, and fail closed for missing file, non-dictionary JSON, invalid profile, or unknown customer. Do not scan directories or manufacture profiles.

  Add `work_request_summary_ko()` to `VSCustomerProfile`. In the handoff screen, add `customer_header` and `customer_context` to `_view_state`, then add native labels under the existing UID label; their source is only `player_header_ko`, `role`, and `work_request_summary_ko`. In the result screen, add the same display-only state and labels above the existing saved-result labels.

  In `VSApp`, preload the repository and add a private `_phase1_customer_profile()` helper that loads only `NADIA_VENN`. Pass that profile to handoff, return, and saved-result configuration. Preserve the existing `PHASE1_NADIA_EVENT_PREFIX`, event payload, resolver, result transition, and save candidate boundaries.

- [ ] **Step 4: Run all Task 2 focused tests and refactor repeated profile formatting**

  Re-run every command from Step 2 and the focused `test_vs_app.gd` command. Keep shared display formatting on `VSCustomerProfile`; do not duplicate Korean goal mappings across presenters.

- [ ] **Step 5: Commit Task 2**

  ```powershell
  git add scripts/vertical_slice/services/vs_customer_profile_repository.gd scripts/vertical_slice/domain/vs_customer_profile.gd scripts/vertical_slice/ui/vs_customer_handoff_screen.gd scripts/vertical_slice/ui/vs_customer_result_screen.gd scripts/vertical_slice/ui/vs_app.gd tests/gut/unit/vertical_slice/test_vs_customer_profile_repository.gd tests/gut/unit/vertical_slice/test_vs_customer_handoff_screen.gd tests/gut/unit/vertical_slice/test_vs_customer_result_screen.gd tests/gut/unit/vertical_slice/test_vs_app.gd
  git commit -m "feat: present customer work reports from profile data"
  ```

### Task 3: Make the item chronicle consume saved actual-use facts without a Nadia-specific filter

**Files:**

- Modify: `scripts/vertical_slice/ui/vs_item_chronicle_screen.gd`
- Modify: `scripts/vertical_slice/ui/vs_app.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_item_chronicle_screen.gd`
- Modify: `tests/gut/unit/vertical_slice/test_vs_app.gd`

**Interfaces:**

- `VSItemChronicleScreen.configure_item(item, resolved_events, customer_profile = null) -> Dictionary` remains read-only and keeps its two-argument callers valid.
- The chronicle includes an actual-use result when the stored event has one matching `PRIMARY_ITEM` UID and `actual_item_use = true`, regardless of a hard-coded customer ID.
- A matching injected profile provides the customer name. A missing/mismatched profile uses the neutral label `고객`; it never invents or stores an identity.

- [ ] **Step 1: Write failing chronicle tests**

  Extend `test_vs_item_chronicle_screen.gd` to pass the real Nadia profile and require `나디아 벤에게 작품 인계` and `나디아 벤 실제 사용 결과` for the saved current event. Add a second saved actual-use event with another syntactically valid customer ID and assert that it is visible as `고객에게 작품 인계`, rather than being silently dropped because it is not Nadia.

  Add an app-flow assertion after a normal Phase 1 return that the visible chronicle receives the real Nadia profile and still does not create any new ledger or resolved-event entry.

- [ ] **Step 2: Run the focused chronicle test and observe RED**

  Run:

  ```powershell
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -gtest=test_vs_item_chronicle_screen.gd -ginclude_subdirs -gexit
  ```

  Expected: the neutral actual-use event is omitted because `_is_matching_actual_use_result` currently requires `customer_id == "NADIA_VENN"`.

- [ ] **Step 3: Implement the smallest factual chronicle change**

  Remove only the Nadia-ID condition from `_is_matching_actual_use_result`. Thread the optional profile through `configure_item` and `_entries_from_existing_facts`. Use `profile.name` only when `profile.customer_id` equals the saved result `customer_id`; otherwise use `고객`. Keep the existing birth and precision-tag rendering, current damage wording, item UID matching, and no-new-storage rule.

  In `VSApp._show_item_chronicle`, obtain the current Phase 1 profile through the existing private helper and pass it as the third argument. Do not create profile persistence or load unknown customer data.

- [ ] **Step 4: Run focused GREEN and regression tests**

  Re-run the Task 3 GUT command, then run `test_vs_app.gd`, `test_vs_customer_result_screen.gd`, and `test_vs_customer_handoff_screen.gd`. Confirm the same result remains a read-only source and the neutral fallback has no new saved fact.

- [ ] **Step 5: Commit Task 3**

  ```powershell
  git add scripts/vertical_slice/ui/vs_item_chronicle_screen.gd scripts/vertical_slice/ui/vs_app.gd tests/gut/unit/vertical_slice/test_vs_item_chronicle_screen.gd tests/gut/unit/vertical_slice/test_vs_app.gd
  git commit -m "feat: connect factual work reports to item chronicle"
  ```

### Task 4: Exact-head regression, runtime evidence, and GitHub delivery

**Files:**

- Modify: `docs/operations/receipts/2026-09-03-independent-forge-lifecycle-design.json`
- Modify: `docs/superpowers/plans/2026-09-03-independent-forge-lifecycle.md`
- Do not modify: `data/`, `scenes/`, `assets/`, `addons/`, `project.godot`, Base adapter, or historical GDD owners.

**Interfaces:**

- Consumes: exact branch head, focused GUT results, Python contracts, Godot headless import, and an isolated actual Blacksmith runtime observation.
- Produces: a receipt that separates machine/runtime proof from Android, accessibility, performance, human-player, rights, and release evidence.

- [ ] **Step 1: Run full machine verification**

  Run the focused GUT files, all GUT unit/integration tests, Python discovery, the current authority contract, current Base operating contract, Godot headless import, and exact diff audit.

  ```powershell
  & $python -m unittest discover -s tests -p 'test_*.py'
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut -ginclude_subdirs -gexit
  & $python tests/check_current_authority_entrypoint_contract.py
  & $python C:\Users\user\Documents\GitHub\Base\tools\check_project_operating_contract.py --project-root . --base-repository C:\Users\user\Documents\GitHub\Base --check
  godot --headless --editor --path . --quit
  git diff --check origin/main...HEAD
  ```

- [ ] **Step 2: Capture the actual isolated runtime**

  Use the project-authoritative Godot live-editor path only after verifying the process has this Blacksmith worktree project path. Observe: completed first-forge result before confirmation, Workshop after confirmation, +10 handoff with the profile header, actual-use report, and item chronicle. Preserve user saves by using the established isolated profile approach. Capture only actual game frames; do not generate or commit a fake screenshot.

- [ ] **Step 3: Update the receipt and plan checkboxes**

  Record exact commit SHA, changed files, test commands/results, capture provenance, no-new-asset result, no-new-schema result, PR head, and all unrun ceilings. Mark only observed machine/runtime facts as PASS. Do not call Android, accessibility, performance, human-player, rights, or release PASS.

- [ ] **Step 4: Push, exact-head CI readback, and merge**

  Push the current PR #366 branch. Update its title/body from design review to implementation delivery, re-read `headRefOid`, and wait for CI on that exact head. When all required checks are green, mark the PR ready, merge through GitHub protection, fast-forward local `main`, and verify local/remote `main` point at the exact merge result. Do not force push, bypass rulesets, or alter unrelated PRs.

## Plan self-review

- **Spec coverage:** Task 1 implements the existing first-forge-to-workshop gap; Task 2 implements the profile-backed independent work report; Task 3 makes the same UID chronicle factual and avoids Nadia-only filtering; Task 4 proves and delivers the result.
- **No unapproved expansion:** new quality rewards, top-grade unlocks, multi-customer management, combat, schedules, rewards, ranks, ads, gacha, images, assets, and save-schema changes are all excluded explicitly.
- **Interface consistency:** `ForgingScreen` emits a confirmation while `VSMainMenu` remains the sole first-item persistence owner; the profile repository loads only the one existing JSON profile; presenters receive display data and do not own resolver facts.
- **Placeholder scan:** no task contains a deferred implementation instruction or undefined interface; all code behavior, test intention, commands, and completion boundaries are concrete.
