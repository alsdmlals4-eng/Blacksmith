# Anvil Oath Title Identity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the user-approved product title `모루의 서약 / ANVIL OATH` to the player-facing main menu and human-facing GDD without changing gameplay, save data, technical identifiers, or unapproved logo assets.

**Architecture:** `BS-IDENTITY-20260831-39` is the sole title/lockup authority. The existing main-menu `Label` remains the runtime title surface and is edited through the authorized Godot editor path. The title contract is protected at the player-visible scene boundary and in the deterministic GDD/PDF publication pipeline; logo generation remains an unpromoted candidate workflow until the user locks one direction.

**Tech Stack:** Godot 4.7 scene authoring through Godot AI/HiGodot authority, GUT, Python `unittest`, ReportLab, `pypdf`, Poppler rendering, GitHub Actions contract checks.

**Spec:** `docs/decisions/BS-IDENTITY-20260831-39_ANVIL_OATH_PRODUCT_TITLE.md`

## Global Constraints

- Product title is exactly `모루의 서약`; Latin lockup is exactly `ANVIL OATH`.
- `대장간` remains a generic place/action word. Preserve `새 대장간 시작` and `대장간으로 돌아가기`.
- Do not change `project.godot`, save keys, UID values, scene node names, resource paths, `BLACKSMITH_*` machine identifiers, equipment data, tag data, probability, durability, repair, economy, or customer-event rules.
- Only Godot editor/HiGodot-authorized mutation may write `scenes/vertical_slice/main_menu.tscn`; do not text-edit the serialized scene.
- The user-approved art direction remains `ILLUSTRATED_WORKSHOP_BOOK`; `GRIMOIRE` is reference-only layout density and must not be copied.
- A logo candidate is `GENERATED_CANDIDATE`, never a runtime asset, until the user selects and locks it. `fallback_if_unconsumed = DO_NOT_PROMOTE_OR_SHIP`.
- `PUBLIC_BRAND_LEGAL_CLEARANCE = NOT_RUN`; no store publication, trademark clearance, or release claim is in this plan.
- Run `fetch → fast-forward pull → push → fetch/readback` at task start, before merge, and at completion. Do not force-push, direct-push `main`, or create a merge commit for synchronization.

---

### Task 1: Write the title-boundary tests first

**Files:**
- Modify: `tests/gut/unit/vertical_slice/test_vs_main_menu.gd:81-87`
- Modify: `tests/check_human_facing_gdd_and_review_loop_contract.py:50-105, 240-285`
- Create: `tests/test_anvil_oath_product_title_contract.py`

**Interfaces:**
- Consumes: `res://scenes/vertical_slice/main_menu.tscn`, the human GDD Markdown/PDF/receipt pipeline, and Decision39.
- Produces: a GUT player-visible main-menu assertion and a Python title-boundary contract usable by CI and local review.

- [ ] **Step 1: Add the failing GUT expectation for the title surface.**

  In `test_main_menu_keeps_native_korean_touch_actions_over_the_approved_background`, replace only the product-title assertion with:

  ```gdscript
  assert_eq(menu.get_node("MenuLayout/MenuTitleLabel").text, "모루의 서약")
  assert_eq(menu.get_node("MenuLayout/ContinueButton").text, "이어하기")
  assert_eq(menu.get_node("MenuLayout/NewGameButton").text, "새 대장간 시작")
  assert_eq(menu.get_node("MenuLayout/SettingsButton").text, "설정")
  ```

  This catches the player-visible regression where the official product title is not shown while preserving the generic workshop action.

- [ ] **Step 2: Run the focused GUT suite and observe RED.**

  Run the project’s approved GUT invocation for `test_vs_main_menu.gd`. Expected result: one assertion failure showing actual `대장간`, expected `모루의 서약`; the three action labels must remain unchanged.

- [ ] **Step 3: Add the failing cross-surface Python contract.**

  Create `tests/test_anvil_oath_product_title_contract.py` with a `unittest.TestCase` that reads the real decision, scene, human GDD, PDF receipt, and PDF metadata. It must assert all of the following independent boundary results:

  ```python
  self.assertIn("PRODUCT_TITLE_KO = 모루의 서약", decision_text)
  self.assertIn("PRODUCT_TITLE_LATIN = ANVIL OATH", decision_text)
  self.assertIn('text = "모루의 서약"', scene_text)
  self.assertIn('text = "새 대장간 시작"', scene_text)
  self.assertTrue(human_gdd.startswith("# 모루의 서약 — 사람용 게임 기획서"))
  self.assertEqual(reader.metadata.title, "모루의 서약 · 사람용 게임 기획서")
  self.assertEqual(receipt["product_identity"]["latin_lockup"], "ANVIL OATH")
  ```

  Name the test `test_player_facing_title_is_consistent_without_renaming_workshop_actions` so its failure names the accidental product-title or generic-action regression it catches.

- [ ] **Step 4: Extend the existing GDD contract before publication changes.**

  In `tests/check_human_facing_gdd_and_review_loop_contract.py`, add the required human GDD title token, the PDF metadata title, the receipt `product_identity` object, and `모루의 서약` / `ANVIL OATH` text extraction checks. Do not remove existing precision, equipment, evidence-ceiling, or image-provenance assertions.

- [ ] **Step 5: Run the new Python contract and observe RED.**

  Run:

  ```powershell
  C:\\Users\\user\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe -m unittest tests.test_anvil_oath_product_title_contract -v
  ```

  Expected result: FAIL because the real scene title, GDD heading, PDF metadata, and receipt still use the prior title state. A missing-file or import error is not an acceptable RED result.

- [ ] **Step 6: Commit the RED tests only.**

  ```powershell
  git add tests/gut/unit/vertical_slice/test_vs_main_menu.gd tests/check_human_facing_gdd_and_review_loop_contract.py tests/test_anvil_oath_product_title_contract.py
  git commit -m "test: define Anvil Oath title contract"
  git push
  ```

### Task 2: Apply the player-visible title through the authorized Godot editor

**Files:**
- Modify: `scenes/vertical_slice/main_menu.tscn` (editor-authored only)

**Interfaces:**
- Consumes: GUT RED expectation from Task 1 and Decision39 title boundary.
- Produces: `MenuLayout/MenuTitleLabel.text == "모루의 서약"`; all existing node names, layout metrics, button labels, background binding, and script binding remain unchanged.

- [ ] **Step 1: Attach to the exact worktree Godot session.**

  Use `session_manage.list`, select only a session whose `project_path` resolves to this worktree, then call `session_activate` with its exact id. If no session exists for this worktree, use the project’s approved Godot AI attach route and re-list sessions. Never mutate a different Blacksmith checkout.

- [ ] **Step 2: Open and read the actual main menu scene.**

  Use the editor scene-open/read path for `res://scenes/vertical_slice/main_menu.tscn`; verify the target is `/MainMenu/MenuLayout/MenuTitleLabel` and currently displays `대장간`.

- [ ] **Step 3: Set only the label text through the editor.**

  Call the Godot UI authoring surface:

  ```json
  {"op":"set_text","params":{"path":"/MainMenu/MenuLayout/MenuTitleLabel","text":"모루의 서약"}}
  ```

  Do not alter node names, fonts, font size, outline, offsets, background, or action-button text.

- [ ] **Step 4: Save through the editor and inspect the persisted result.**

  Call `scene_save`, then re-read the scene via the editor and verify the same node text equals `모루의 서약`.

- [ ] **Step 5: Run the focused GUT suite and observe GREEN.**

  Run the same suite from Task 1. Expected result: all `test_vs_main_menu.gd` tests pass, including the Korean product title and unchanged `새 대장간 시작` action.

- [ ] **Step 6: Run the scene static boundary tests.**

  ```powershell
  python -m unittest tests.test_vertical_slice_task2_app_shell_contract -v
  python -m pytest tests/test_higodot_task2_exact_diff_hygiene.py tests/test_higodot_task2_post_authoring_gate.py -q
  ```

  Expected result: PASS. A required provenance gate failure must be reported before continuing; do not text-edit the scene as a workaround.

- [ ] **Step 7: Commit and push the editor-authored scene.**

  ```powershell
  git add scenes/vertical_slice/main_menu.tscn
  git commit -m "feat: show Anvil Oath on main menu"
  git push
  ```

### Task 3: Publish a matching human-facing GDD and deterministic PDF

**Files:**
- Modify: `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md:1-5`
- Modify: `tools/publish_human_facing_gdd_pdf.py:70-76, 198-216`
- Modify: `exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf` (deterministic derivative)
- Modify: `docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json` (publisher output)

**Interfaces:**
- Consumes: Decision39, RED Python title contract, existing ReportLab publisher.
- Produces: a title-aligned Korean GDD heading, PDF metadata/footer, and receipt provenance without turning the PDF into runtime or human-UX evidence.

- [ ] **Step 1: Change the GDD’s player-facing heading only.**

  Replace the first line with:

  ```markdown
  # 모루의 서약 — 사람용 게임 기획서
  ```

  Preserve the document role, Korean-primary audience, game loop, numeric tables, evidence ceiling, and technical owner paths.

- [ ] **Step 2: Change only publication identity strings and receipt schema.**

  In `tools/publish_human_facing_gdd_pdf.py`, use:

  ```python
  PRODUCT_TITLE_KO = "모루의 서약"
  PRODUCT_TITLE_LATIN = "ANVIL OATH"
  PRODUCT_DOCUMENT_TITLE = f"{PRODUCT_TITLE_KO} · 사람용 게임 기획서"
  ```

  Use `PRODUCT_DOCUMENT_TITLE` in ReportLab metadata and the visible footer. Add this receipt member without removing existing provenance:

  ```python
  "product_identity": {
      "decision_id": "BS-IDENTITY-20260831-39",
      "korean_title": PRODUCT_TITLE_KO,
      "latin_lockup": PRODUCT_TITLE_LATIN,
      "legal_clearance": "NOT_RUN",
  },
  ```

- [ ] **Step 3: Publish with the bundled project Python runtime.**

  Use the runtime that contains ReportLab and Pillow:

  ```powershell
  C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe tools\publish_human_facing_gdd_pdf.py
  ```

  Expected result: two invariant publication passes with identical SHA-256 and an updated source/artefact receipt.

- [ ] **Step 4: Run the new title contract and existing GDD contract to observe GREEN.**

  ```powershell
  C:\\Users\\user\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe -m unittest tests.test_anvil_oath_product_title_contract -v
  C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe tests\check_human_facing_gdd_and_review_loop_contract.py
  ```

  Expected result: PASS with the regenerated PDF and receipt. The check remains static/document evidence only.

- [ ] **Step 5: Render and inspect the PDF.**

  Locate the approved Poppler `pdftoppm.exe`, render every PDF page to a temporary path outside tracked source, inspect the title page and a later page for title/footer legibility, then remove the temporary render directory. Record only `RENDERED_AND_VISUALLY_INSPECTED / NOT_PRODUCT_RUNTIME_EVIDENCE` in the receipt.

- [ ] **Step 6: Commit and push the human-facing publication set.**

  ```powershell
  git add docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md tools/publish_human_facing_gdd_pdf.py exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828_PDF_RECEIPT.json tests/check_human_facing_gdd_and_review_loop_contract.py tests/test_anvil_oath_product_title_contract.py
  git commit -m "docs: publish Anvil Oath human GDD"
  git push
  ```

### Task 4: Produce review-only title-logo candidates from the registered Visual Requirement

**Files:**
- No repository runtime-asset or scene file changes before user lock.
- Candidate outputs: managed generated-image output only, labeled `AO-LOGO-01`, `AO-LOGO-02`, `AO-LOGO-03` for user review.

**Interfaces:**
- Consumes: Decision39 `MAIN_MENU_PRODUCT_TITLE_LOCKUP` requirement and approved `ILLUSTRATED_WORKSHOP_BOOK` direction.
- Produces: three candidate transparent logotypes shown to the user; no runtime binding, asset manifest promotion, or public-release claim.

- [ ] **Step 1: Re-read the Decision39 Visual Requirement.**

  Confirm `consumer_id`, `target_aspect_resolution`, `fallback_if_unconsumed`, and `final_direction_lock` are still exactly the approved values before any image call.

- [ ] **Step 2: Generate `AO-LOGO-01` as an actual transparent title lockup candidate.**

  Use the image generation model, not SVG, Canvas, Godot primitive drawing, or a fake screenshot. Prompt for `ANVIL OATH` only, wide transparent 1600×640 lockup, refined fantasy serif typography, subtle circular anvil engraving, warm parchment/iron/woodcraft character, no weapon silhouette, no feather, no GRIMOIRE composition, no UI frame, no background.

- [ ] **Step 3: Generate `AO-LOGO-02` with balanced fantasy readability.**

  Keep the exact `ANVIL OATH` spelling, transparent wide output, restrained small anvil mark, warm illustrated workshop-book material cues, and clear medium-size reading. Exclude dark gold-on-black forge styling, a dominant sword/shield/bow, and generated screen mockups.

- [ ] **Step 4: Generate `AO-LOGO-03` for mobile reduction.**

  Keep the exact `ANVIL OATH` spelling, wide transparent output, heavy readability at 720-pixel portrait menu scale, one minimal engraved mark, and no fine filigree that collapses at small size.

- [ ] **Step 5: Show all three candidates and wait for the user lock.**

  State each candidate is `GENERATED_CANDIDATE / NOT_RUNTIME_ASSET / NOT_LEGAL_CLEARANCE`. Do not copy any candidate into `assets/`, modify `ASSET_MANIFEST.json`, or replace `MenuTitleLabel` until the user selects one.

### Task 5: Run exact-head verification, review, and synchronized delivery

**Files:**
- Verify: all changed files from Tasks 1–3 and no unexpected tracked files.

**Interfaces:**
- Consumes: all commits and test evidence from the previous tasks.
- Produces: a reviewable branch/PR with verified title changes; main remains unmodified until normal PR integration.

- [ ] **Step 1: Inspect the exact diff and protected paths.**

  ```powershell
  git diff --check origin/main...HEAD
  git diff --name-status origin/main...HEAD
  git status --short
  ```

  Expected changed product files: Decision39, GUT/Python tests, `main_menu.tscn`, GDD Markdown, PDF publisher, PDF, and receipt. Any unrelated data, save, asset, project, or temporary path is a blocker.

- [ ] **Step 2: Run the title-focused full verification set.**

  Run the focused GUT result, both Python title/GDD contracts, the vertical-slice static contract, Godot headless import/parse, and the project operating-contract validator against the current pinned Base. Record machine PASS separately from runtime, Android, accessibility, performance, human play, legal, and release states.

- [ ] **Step 3: Request independent code review if available and resolve only title-scope feedback.**

  Review Decision39 invariants: no generic action label rewrite, no data/identifier rename, no unapproved logo promotion, and no legal-clearance overclaim.

- [ ] **Step 4: Create a normal PR and wait for required checks.**

  Do not direct-push `main`, force-push, bypass rules, or merge unrelated open PRs. The PR body must identify title integration scope, document-only evidence versus runtime/UX evidence, the close `Oath and Anvil` naming risk, and the pending user logo lock.

- [ ] **Step 5: After normal merge, synchronize and read back both canon copies.**

  ```powershell
  git -C C:\Users\user\Documents\GitHub\Ninza\Blacksmith fetch --prune origin
  git -C C:\Users\user\Documents\GitHub\Ninza\Blacksmith pull --ff-only origin main
  git -C C:\Users\user\Documents\GitHub\Ninza\Blacksmith push origin main
  git -C C:\Users\user\Documents\GitHub\Ninza\Blacksmith fetch --prune origin
  git -C C:\Users\user\Documents\GitHub\Ninza\Blacksmith rev-list --left-right --count origin/main...main
  ```

  Expected result: `0 0`. Remove only disposable render/temporary directories after confirming their absolute paths; preserve the user-reviewable generated logo candidates until the user decides their disposition.
