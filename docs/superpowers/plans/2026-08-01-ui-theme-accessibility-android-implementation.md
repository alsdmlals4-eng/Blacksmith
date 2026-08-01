# Blacksmith UI Theme·Accessibility·Android Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Apply TDD task-by-task.
>
> **Execution Gate:** 사용자 `기획 완료`와 `검수 완료` 전 실행 금지.

**Goal:** 런타임 조립·고정 크기 UI를 공통 Theme·재사용 Scene·safe area·설정·접근성·Android lifecycle 구조로 전환해 화면·입력·저장 상태를 일관되게 유지한다.

**Authority:** `BS-UI-PLATFORM-20260801-01`.

**Architecture:** `SafeAreaRoot` 아래 AppChrome·ScreenRouterViewport·GlobalOverlayLayer·SystemFeedbackLayer를 둔다. Theme, Accessibility, Settings, Lifecycle, Input Navigation은 각각 한 Coordinator가 책임진다. 화면 Controller는 데이터와 Signal을 연결할 뿐 스타일·저장·back·판정을 재구현하지 않는다.

**Tech Stack:** Godot 4.7.1, GDScript, Theme Resources, ConfigFile, Android portrait, Python/Godot tests.

## Zero-tolerance gates

```text
CORE_TOUCH_TARGET_BELOW_48PX = 0
COLOR_ONLY_CORE_STATE = 0
SAFE_AREA_CTA_OCCLUSION = 0
TEXT_SCALE_INFORMATION_LOSS = 0
BACK_DOUBLE_HANDLING = 0
UNACKNOWLEDGED_RESULT_DISMISS = 0
SETTINGS_CORRUPTION_CAMPAIGN_DAMAGE = 0
REDUCED_MOTION_GAMEPLAY_CHANGE = 0
PRECISION_ASSIST_AUTO_PERFECT = 0
PROCESS_DEATH_STATE_REROLL_OR_LOSS = 0
```

## File Map

### Create

- `assets/ui/theme/blacksmith_theme.tres`
- `assets/ui/theme/typography.tres`
- `assets/ui/theme/colors.tres`
- `assets/ui/theme/spacing.tres`
- `assets/ui/theme/control_sizes.tres`
- `scripts/application/ui/ui_theme_coordinator.gd`
- `scripts/application/ui/accessibility_coordinator.gd`
- `scripts/application/settings/settings_coordinator.gd`
- `scripts/application/platform/android_lifecycle_coordinator.gd`
- `scripts/application/input/input_navigation_coordinator.gd`
- `scripts/ui/layout/safe_area_root.gd`
- `scenes/application/safe_area_root.tscn`
- reusable scenes listed in the canon
- `tools/validate_ui_contract.py`
- `tests/test_ui_contract.py`
- `tests/unit/test_settings_coordinator.gd`
- `tests/unit/test_android_back_stack.gd`
- `tests/unit/test_accessibility_coordinator.gd`
- `tests/integration/test_safe_area_layouts.gd`
- `tests/integration/test_ui_state_recovery.gd`

### Modify

- future `scenes/application/blacksmith_app.tscn`
- current product UI scripts and scenes
- `project.godot` display/stretch/orientation/input settings
- future SaveCoordinator/AppStateCoordinator
- `.github/workflows/godot-validation.yml`
- `tests/README.md`

---

### Task 1: Freeze Theme tokens and reusable Scene contracts

- [ ] Write Python tests for required token IDs and reusable Scene inventory.
- [ ] Create Theme Resources for colors, typography, spacing, sizes and control styles.
- [ ] Add validator that detects direct duplicate product color/font/spacing constants outside approved dynamic cases.
- [ ] Define typed input/Signal contracts for each reusable Scene.
- [ ] Commit: `feat: establish Blacksmith UI theme tokens and components`

### Task 2: SafeAreaRoot and responsive fixtures

- [ ] Write layout tests for 360×640, 720×1280, 1080×2400 and tablet portrait.
- [ ] Add top/bottom/left/right cutout and gesture inset fixtures.
- [ ] Implement SafeAreaRoot using containers/anchors, not absolute offsets.
- [ ] Keep CTA above bottom gesture inset and all critical text within safe content rect.
- [ ] Reject landscape entry or lock orientation.
- [ ] Commit: `feat: add safe-area responsive application root`

### Task 3: Migrate common UI pieces

- [ ] Create AppChrome, status/resource bars, equipment hero, action bars, cards, modal, toast, blocking error, save status and ResultEnvelope scenes.
- [ ] Replace duplicated runtime StyleBox/layout code screen-by-screen.
- [ ] Preserve domain signals and existing PoC behavior until v9 services replace it.
- [ ] Verify no reusable Scene computes domain results.
- [ ] Commit: `refactor: migrate product UI to reusable themed scenes`

### Task 4: Text scale and long Korean strings

- [ ] Write fixtures for 1.0/1.15/1.30 text scale and worst-case Korean strings.
- [ ] Implement coordinated font, line-height, min-size and scroll/reflow changes.
- [ ] Verify probabilities, cost, stop reasons and result changes remain visible.
- [ ] Prohibit global screen shrink as an overflow solution.
- [ ] Commit: `feat: support accessible text scaling without information loss`

### Task 5: Color-independent states and focus/input

- [ ] Add screenshot/controller tests for success, hold, downgrade, destroy, selected, disabled and choice-required states.
- [ ] Pair color with text/icon/border or pattern.
- [ ] Implement deterministic focus order and restore previous focus after Overlay close.
- [ ] Lock duplicate input during transitions.
- [ ] Enforce 48px targets and 8px dangerous-button spacing.
- [ ] Commit: `feat: make UI states and navigation accessible`

### Task 6: SettingsCoordinator

- [ ] Write round-trip, range, missing-key, unsupported-device and corrupt-file tests.
- [ ] Implement `settings.cfg` separate from campaign save.
- [ ] Defaults: music80, sfx100, vibration on, reduced motion off, precision assist off, normal text, extra labels on.
- [ ] Apply immediately, debounce write and verify persisted values.
- [ ] Corruption restores defaults with one notice and no campaign impact.
- [ ] Commit: `feat: persist independent accessibility and audio settings`

### Task 7: Reduced motion and precision assist

- [ ] Write gameplay-equivalence tests comparing probabilities/outcomes with settings on/off.
- [ ] Reduce or remove repeated fire, shake, zoom and large movement; preserve meaning by text/icon/fade.
- [ ] Precision assist may enhance visibility, slow visual motion and add cues, but input remains required.
- [ ] Assert auto PERFECT, auto finish and probability bonus are zero.
- [ ] Commit: `feat: add non-advantage accessibility assists`

### Task 8: Android back-stack coordinator

- [ ] Write tests for every priority level: dialog, envelope, overlay, detail, work view, hub, main.
- [ ] Ensure one back event has exactly one consumer.
- [ ] ResultEnvelope cannot be discarded before acknowledgement.
- [ ] Merge repeated back presses during save/transition.
- [ ] Main uses Android system behavior; no required exit button.
- [ ] Commit: `feat: centralize Android back navigation`

### Task 9: Pause, resume and process-death integration

- [ ] Write integration tests for pause before/after PREPARED/APPLIED, focus loss, resume and process death without pause callback.
- [ ] Stop starting new irreversible actions on pause.
- [ ] Best-effort flush dirty safe state without making pause the only protection.
- [ ] Resume rechecks save revision, envelopes, intents, safe area, audio and focus.
- [ ] Process death follows Boot→SaveStatus→recovery→last safe view.
- [ ] Commit: `feat: recover Blacksmith UI and state across Android lifecycle`

### Task 10: Save indicators and error UX

- [ ] Test indicator only reports saved after verified revision.
- [ ] Use non-blocking indicator for normal saves and blocking error for failure/recovery/migration issues.
- [ ] Keep exact error and next action visible at max text scale.
- [ ] Spinner disappearance never implies success.
- [ ] Commit: `feat: expose verified save and recovery status`

### Task 11: CI, screenshots and device validation

- [ ] Add CI:

```bash
python tools/validate_ui_contract.py
python -m unittest tests/test_ui_contract.py
godot --headless --path . --script res://tests/unit/test_settings_coordinator.gd
godot --headless --path . --script res://tests/unit/test_android_back_stack.gd
godot --headless --path . --script res://tests/unit/test_accessibility_coordinator.gd
godot --headless --path . --script res://tests/integration/test_safe_area_layouts.gd
godot --headless --path . --script res://tests/integration/test_ui_state_recovery.gd
```

- [ ] Capture the visual governance baseline fixtures.
- [ ] Execute notch/gesture/3-button navigation, home/app switch/lock/process kill, vibration and audio focus on devices.
- [ ] Conduct six-person comprehension review.
- [ ] Keep each external gate NOT_RUN until evidence exists.
- [ ] Commit: `ci: enforce UI accessibility and Android lifecycle contracts`

## Self-review

- Theme/Scene responsibility: isolated.
- Safe area and text scaling: measurable.
- Settings corruption: separate from campaign.
- Back and lifecycle order: explicit.
- Accessibility does not change gameplay: explicit.
- Runtime authorization: blocked.

```text
PLAN_STATUS: COMPLETE
IMPLEMENTATION_EXECUTION: BLOCKED
```
