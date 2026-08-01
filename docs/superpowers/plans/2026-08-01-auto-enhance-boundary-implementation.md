# Blacksmith Auto Enhance Boundary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Apply TDD task-by-task.
>
> **Execution Gate:** 사용자 `기획 완료`와 `검수 완료` 전 실행 금지.

**Goal:** 구형 자동 단조를 한 장비의 비결정 일반 강화만 반복하는 `자동 강화`로 교체하고, 작품 완성·정체성·정밀·+50·소유권·파괴 경계에서 반드시 플레이어에게 제어권을 반환한다.

**Authority:** `BS-AUTOFORGE-20260801-01`.

**Architecture:** `AutoEnhancePolicy`는 목표·시도·지출·잔액·결과별 정지 설정만 보유한다. `EnhancementDecisionBoundaryRegistry`가 다음 필수 선택 경계를 데이터로 제공한다. `AutoEnhanceService`는 매 시도 전 경계를 검사하고, 수동 강화와 동일한 SaveCoordinator/AttemptIntent/ResultEnvelope 경로를 호출한다. UI는 서비스의 정지 이유를 표시할 뿐 결과를 계산하지 않는다.

**Tech Stack:** Godot 4.7.1, GDScript, JSON, Python validators, headless SceneTree tests.

## Zero-tolerance gates

```text
RANDOM_PRECISION_INPUT = 0
EMPTY_REQUIRED_MATERIAL_FALLBACK = 0
AUTO_NEW_EQUIPMENT_AFTER_DESTROY = 0
AUTO_IDENTITY_CHOICE = 0
AUTO_PLUS50_ROUTE_CHOICE = 0
AUTO_SALE_OR_DELIVERY = 0
ATTEMPT_AFTER_SAVE_FAILURE = 0
RESULT_REROLL = 0
```

## File Map

### Create

- `data/crafting/enhancement_decision_boundaries.json`
- `scripts/enhancement/enhancement_decision_boundary_registry.gd`
- `scripts/automation/auto_enhance_policy.gd`
- `scripts/automation/auto_enhance_service.gd`
- `scripts/ui/auto_enhance_panel.gd`
- `scenes/ui/auto_enhance_panel.tscn`
- `tools/validate_auto_enhance_contract.py`
- `tests/test_auto_enhance_contract.py`
- `tests/unit/test_enhancement_decision_boundary_registry.gd`
- `tests/unit/test_auto_enhance_policy.gd`
- `tests/integration/test_auto_enhance_service.gd`
- `tests/integration/test_auto_enhance_recovery.gd`

### Modify

- `scripts/ui/game_flow_screen.gd`
- `scripts/ui/enhancement_screen.gd`
- `scripts/enhancement/enhancement_session.gd`
- `scripts/economy/workshop_resources.gd`
- future `scripts/application/save/save_coordinator.gd`
- future `scripts/application/results/result_envelope_queue.gd`
- `tests/README.md`
- `.github/workflows/godot-validation.yml`

---

### Task 1: Decision-boundary data and validator

- [ ] Write failing Python tests for +5/+10/+20/+30/+40/+50 and data-driven late choices.
- [ ] Create `enhancement_decision_boundaries.json` with `before_level`, `boundary_type`, `requires_player_choice`, `requires_precision`, `requires_material_choice` and `display_reason`.
- [ ] Validate no automatic policy can cross an unresolved boundary.
- [ ] Run:

```bash
python tools/validate_auto_enhance_contract.py
python -m unittest tests/test_auto_enhance_contract.py
```

- [ ] Commit: `feat: define enhancement decision boundaries`

### Task 2: AutoEnhancePolicy validation

- [ ] Write tests for target below/equal current, max attempts 0/101, both spend controls unbounded, invalid skill and stale revision.
- [ ] Implement immutable policy creation and validation.
- [ ] Defaults: max attempts 10, stop on downgrade true, stop on hold false, stop on destroy always true.
- [ ] Require at least one finite attempt/spend/reserve constraint.
- [ ] Commit: `feat: validate bounded auto-enhance policies`

### Task 3: Boundary registry and preflight

- [ ] Write registry tests for the next unresolved boundary from every relevant level.
- [ ] Implement `next_boundary(current_level, target_level, equipment_identity)`.
- [ ] Preflight must reject unacknowledged envelopes, unresolved intent, missing save storage, missing equipment ownership and target beyond the next unresolved choice.
- [ ] Return an explicit stop reason rather than a generic error.
- [ ] Commit: `feat: stop auto enhancement before player decisions`

### Task 4: Replace legacy loop with AutoEnhanceService

- [ ] Write failing integration tests reproducing legacy `repeat_until_full`, random precision, empty material fallback and destroy restart.
- [ ] Implement one-equipment service loop with max attempts/spend/reserve accounting.
- [ ] Remove product calls to `_show_auto_enhancement()` and automatic iron-sword template creation.
- [ ] Remove `repeat_until_full` from product policy.
- [ ] Keep `현재 시도 후 중지` semantics.
- [ ] Commit: `feat: replace legacy auto forge with bounded auto enhance service`

### Task 5: Precision and material boundaries

- [ ] Write tests proving `requires_precision` returns `PRECISION_INPUT_REQUIRED` before beginning an attempt.
- [ ] Assert RNG call count zero in auto service for precision position.
- [ ] Remove `session.precision_position = session.rng.randf()` from product path.
- [ ] Call resource preview with `allow_empty_secondary=false`.
- [ ] Missing required material returns `REQUIRED_MATERIAL_MISSING`; do not auto-select best/cheapest material.
- [ ] Commit: `fix: require player precision and required materials in automation`

### Task 6: Result handling and save transactions

- [ ] Write result tests for SUCCESS/HOLD/DOWNGRADE/DESTROY/SAVE_FAILED/RESULT_ERROR.
- [ ] Route each attempt through PREPARED and APPLIED save states.
- [ ] Recheck policy and boundary after every resolved attempt.
- [ ] DESTROY always stops and opens its ResultEnvelope; no replacement equipment is created.
- [ ] SAVE_FAILED and RESULT_ERROR start no subsequent attempt.
- [ ] Recovery uses stored result commitment and never rerolls.
- [ ] Commit: `feat: make automatic enhancement crash-safe and result-aware`

### Task 7: Auto Enhance UI

- [ ] Write controller tests for required fields, risk summary and exact stop-reason rendering.
- [ ] Implement target level constrained to the next unresolved boundary.
- [ ] Display max attempts, max spend/min reserve, hold/downgrade options, expected cost range and risks.
- [ ] During execution show attempts, spend, remaining gold, last result and next boundary.
- [ ] End summary shows exact reason, start/end levels, outcomes, spend/materials and pending envelopes.
- [ ] Do not recommend target, materials or equipment.
- [ ] Commit: `feat: add transparent auto-enhance controls and stop summaries`

### Task 8: Legacy tests, CI and external validation

- [ ] Convert old auto-forge repeat-until-full tests into explicit legacy behavior regression tests that must fail or migrate.
- [ ] Add tests for every mandatory stop point and policy limit.
- [ ] Add CI:

```bash
python tools/validate_auto_enhance_contract.py
python -m unittest tests/test_auto_enhance_contract.py
godot --headless --path . --script res://tests/unit/test_enhancement_decision_boundary_registry.gd
godot --headless --path . --script res://tests/unit/test_auto_enhance_policy.gd
godot --headless --path . --script res://tests/integration/test_auto_enhance_service.gd
godot --headless --path . --script res://tests/integration/test_auto_enhance_recovery.gd
```

- [ ] Keep Android interruption, 48dp readability and human automation-trust tests `NOT_RUN` until executed.
- [ ] Commit: `ci: enforce automatic enhancement decision boundaries`

## Self-review

- Every player decision boundary covered.
- Precision RNG and empty material fallback prohibited.
- Destruction restart prohibited.
- Limits and stop reasons explicit.
- Save/result transaction reuse explicit.
- Runtime authorization blocked.

```text
PLAN_STATUS: COMPLETE
IMPLEMENTATION_EXECUTION: BLOCKED
```
