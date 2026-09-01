# Phase 1 Workshop Wireframe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Make the existing current-canon Workshop read as a portrait-first wireframe hierarchy: current workpiece, next enhancement decision, conditional precision/repair context, and same-UID next destination.

**Architecture:** Keep the existing Workshop scene and every domain/service ownership unchanged. VSWorkshopScreen derives only player-facing summary strings from its existing view state, then dynamically adds native PanelContainer cards adjacent to the current controls. This preserves current NodePaths and the tested action controls while providing visible visual grouping without adding a new scene, generated raster, or precision-workshop background.

**Tech Stack:** Godot 4.x GDScript, existing VSWorkshopScreen scene, GUT 9.7.1, Python repository contracts, project-authoritative Godot runtime capture.

**Spec:** docs/superpowers/specs/2026-09-01-phase1-workshop-blueprint-design.md

## Global Constraints

- Current domain owners for enhancement, precision, catalyst consumption, durability, repair, handoff, customer result, and chronicle remain unchanged.
- Preserve every existing direct child NodePath under WorkshopScroll/WorkshopLayout; existing GUT callers and action wiring must continue to resolve.
- Use only native Godot Controls and StyleBoxFlat. Do not add assets, addons, a new inventory, a new background, SVG, or a generated screenshot.
- The precision area remains native UX only. It uses 불의 심장 and 대지의 결정 as consumable resources, never a lineage choice.
- Use the existing five transparent V2 equipment images, workshop background, durability atlas only when actual damage is present, and customer-result illustration at their existing consumers.
- Godot runtime is observed only through the isolated Windows capture recorded in the Phase 1 receipt. Android device, accessibility, performance, human player experience, and release remain NOT_RUN until separately observed.

---

### Task 1: Player-facing wireframe summaries

**Files:**

- Modify: scripts/vertical_slice/ui/vs_workshop_screen.gd
- Modify: tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd
- Test: tests/check_phase1_workshop_blueprint_contract.py

**Interfaces:**

- Consumes: VSWorkshopScreen.view_state(), VSItem.uid, existing equipment catalog display name, existing precision/repair/handoff fields.
- Produces: view-state strings workpiece_summary, decision_summary, precision_summary, and destination_summary. These strings do not mutate a resolver, item, resources, save envelope, or campaign envelope.

- [x] **Step 1: Write the failing GUT tests**

  Add tests that configure a real VSWorkshopScreen with the existing item/resource fixture and require the following fields:

  ~~~gdscript
  var state := screen.view_state()
  assert_true(str(state["workpiece_summary"]).contains("UID"))
  assert_true(str(state["decision_summary"]).contains("+%d" % int(item.enhancement_level + 1)))
  assert_true(str(state["destination_summary"]).contains("인계"))

  item.enhancement_level = 9
  screen.configure_context(item, resources, maintenance_service, action_service, save_service, envelope)
  assert_true(str(screen.view_state()["precision_summary"]).contains("정밀강화 +10"))
  assert_true(str(screen.view_state()["precision_summary"]).contains("불의 심장"))
  ~~~

- [x] **Step 2: Run the focused test to verify RED**

  Run:

  ~~~powershell
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -gtest=test_vs_workshop_screen.gd -ginclude_subdirs -gexit
  ~~~

  Expected: failure because the four summary keys do not exist yet.

- [x] **Step 3: Write the minimal summary implementation**

  In VSWorkshopScreen.view_state(), derive:

  - workpiece_summary from current equipment display name, UID, enhancement level, existing tag entries, and existing durability text;
  - decision_summary from the existing target level, cost summary, outcome summary, and player-facing block reason when disabled;
  - precision_summary only when precision_visible is true, including target, current action or action prompt, catalyst stock summary, and existing preview summary;
  - destination_summary from the existing repair, handoff, and chronicle allowed/reason fields.

  Use small private formatter functions named _workpiece_summary, _decision_summary, _precision_summary, and _destination_summary. They only receive already-produced state values or existing item metadata; they do not call action services.

- [x] **Step 4: Run focused verification**

  Re-run the focused GUT file and:

  ~~~powershell
  & 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tests/check_phase1_workshop_blueprint_contract.py
  ~~~

  Expected: both pass; normal enhancement shows no precision summary, while +9 → +10 uses actual catalyst names.

- [x] **Step 5: Commit**

  ~~~powershell
  git add scripts/vertical_slice/ui/vs_workshop_screen.gd tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd
  git commit -m "feat: add workshop wireframe summaries"
  ~~~

### Task 2: Native visual cards that preserve existing control paths

**Files:**

- Modify: scripts/vertical_slice/ui/vs_workshop_screen.gd
- Modify: tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd
- Test: tests/check_workshop_mobile_readability_contract.py

**Interfaces:**

- Consumes: the four Task 1 summaries and the direct WorkshopLayout children that already own actions.
- Produces: four sibling PanelContainer cards named WireframeWorkpieceCard, WireframeDecisionCard, WireframePrecisionCard, and WireframeDestinationCard. Existing buttons and OptionButtons remain direct WorkshopLayout children at their current paths.

- [x] **Step 1: Write the failing GUT tests**

  Require all four cards after a configured screen is ready:

  ~~~gdscript
  var workpiece_card := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/WireframeWorkpieceCard") as PanelContainer
  var decision_card := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/WireframeDecisionCard") as PanelContainer
  var precision_card := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/WireframePrecisionCard") as PanelContainer
  var destination_card := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/WireframeDestinationCard") as PanelContainer
  assert_not_null(workpiece_card)
  assert_not_null(decision_card)
  assert_false(precision_card.visible)
  assert_not_null(destination_card)
  assert_true((screen.get_node("WorkshopScroll/WorkshopLayout/EnhancementButton") as Button).is_visible_in_tree())
  ~~~

  Then set the real fixture item to level 9 and assert WireframePrecisionCard becomes visible and includes the target and required catalyst text.

- [x] **Step 2: Run the focused test to verify RED**

  Run the same focused GUT command. Expected: failure because the four PanelContainer cards do not exist.

- [ ] **Step 3: Write the minimal native card implementation**

  Add _ensure_wireframe_cards(layout) and call it after _ensure_enhancement_controls() in _ready() and _refresh_controls(). The helper creates only missing sibling PanelContainers and a child VBoxContainer with a title Label and body Label.

  Use a private _wireframe_card_style() that returns a StyleBoxFlat with warm parchment-compatible fill, a restrained brown border, 16px corners, 18px content margins, and no texture. Create cards at these positions:

  1. WireframeWorkpieceCard immediately after EquipmentIdentityHero.
  2. WireframeDecisionCard immediately before EnhancementTitleLabel.
  3. WireframePrecisionCard immediately before PrecisionTitleLabel.
  4. WireframeDestinationCard immediately before HandoffButton.

  Add _refresh_wireframe_cards(state) after the existing control refresh. It sets each body Label from Task 1 summaries, hides WireframePrecisionCard when precision_visible is false, may suppress only redundant non-interactive labels, and never hides, reparents, disables, or rewires an existing direct action control.

- [x] **Step 4: Run focused verification**

  Re-run:

  ~~~powershell
  godot --headless -d -s --path . addons/gut/gut_cmdln.gd -gdir=res://tests/gut/unit/vertical_slice -gtest=test_vs_workshop_screen.gd -ginclude_subdirs -gexit
  & 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tests/check_workshop_mobile_readability_contract.py
  ~~~

  Expected: cards exist, precision card changes only at a true 10-unit target, existing touch targets and direct NodePaths remain intact.

- [x] **Step 5: Refactor and commit**

  Use a single helper for card creation and a single helper for body-label lookup. Do not duplicate StyleBoxFlat configuration. Re-run the focused GUT test after the cleanup, then:

  ~~~powershell
  git add scripts/vertical_slice/ui/vs_workshop_screen.gd tests/gut/unit/vertical_slice/test_vs_workshop_screen.gd
  git commit -m "feat: build workshop wireframe cards"
  ~~~

### Task 3: Exact-head regression, actual runtime evidence, and delivery

**Files:**

- Modify: docs/operations/receipts/2026-09-01-phase1-workshop-blueprint.json
- Modify: docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md only if an exact runtime observation changes its accepted frontier.
- Do not modify: assets, project.godot, scenes, data, addons, or Base adapter.

**Interfaces:**

- Consumes: Task 1 and Task 2 exact-head code and test results.
- Produces: a receipt with separate machine/runtime/device/human ceilings and, if the exact Blacksmith runtime is successfully observed, a provenance-linked portrait capture.

- [x] **Step 1: Full machine verification**

  Run the focused GUT suite, full GUT unit/integration suites, Python discovery, current worktree operating-contract validator, Godot headless editor import, and whitespace audit.

  ~~~powershell
  & 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -p 'test_*.py'
  & 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\user\Documents\GitHub\Base\tools\check_approved_project_operating_contract.py' --project-root . --base-repository 'C:\Users\user\Documents\GitHub\Base' --protected-base 5560d8f0bdde9d900acc2bbbaf403ef3bdbc1b58 --approval docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json --external-approval true --check
  godot --headless --editor --path . --quit
  git diff --check origin/main...HEAD
  ~~~

  Completed locally: Phase 1 receipt contract PASS; Python discovery 333/333;
  GUT 245/245 and JUnit failures/errors/skips 0; headless editor import exited
  successfully. The generic validator correctly reports the one protected script
  path; the approved validator passes only when its external-label input is
  present. The real PR label remains a remote independent gate, not a local PASS.

- [x] **Step 2: Runtime capture**

  Use the project-authoritative Godot live-editor path only after verifying the opened process has the Blacksmith project path. Observe a normal Workshop and +9 → +10 precision state. Capture the actual window only if both the process and current scene are Blacksmith. Do not touch another project’s editor or call an image-generation candidate a runtime capture. Completed with an isolated profile and two local evidence captures; diagnostics were clean. This is runtime evidence, not Android or human-UX acceptance.

- [ ] **Step 3: Receipt and remote readback**

  Add the exact commit SHA, changed files, verification commands/results, capture provenance when present, and every unrun ceiling to the existing Phase 1 blueprint receipt. Push the existing PR #352 branch, re-read its headRefOid and CI at that exact SHA, and only mark the PR ready after machine verification plus a successful runtime observation or an explicit evidence-limited delivery decision. The protected-path manifest is prepared; remote CI additionally requires an independently applied `approved-protected-change` PR label and remains pending until that metadata exists.

## Plan self-review

- **Spec coverage:** Task 1 makes the four blueprint layers factual; Task 2 makes them visible without breaking existing action paths; Task 3 separates local/CI/runtime/human evidence and preserves asset decisions.
- **No scope expansion:** There is no new economy, customer management, inventory, scene, background, image, addon, or product rule.
- **Interface consistency:** every new summary is a read-only string; every new card is a sibling of existing direct controls; service and save boundaries remain unchanged.
- **Wireframe evidence:** the deliverable is native game UI, not a raster mockup. The visible final appearance still requires actual Blacksmith runtime observation.
