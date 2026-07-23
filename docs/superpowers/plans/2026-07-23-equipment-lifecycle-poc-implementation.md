# Blacksmith 장비 생애 PoC 구현계획

> **에이전트 실행 요구사항:** 구현 시 `superpowers:subagent-driven-development` 또는 `superpowers:executing-plans`를 사용한다. 각 Task는 Red→Green→Refactor→독립 커밋으로 끝난다.

**Goal:** 검투사 의뢰부터 철검 제작, +5 납품 또는 +10 추가 도전, 수동 날짜 진행, 지연 결과, 영구 장비 이력과 재방문까지 첫 장비 생애 PoC를 구현한다.

**Architecture:** 날짜·피로도, 영구 완성도, 고객 의뢰, 세계 기록, 결과 판정을 독립 도메인 모델로 분리한다. `GameFlowScreen`은 라우팅만 담당하고 `EquipmentLifecyclePocController`가 상태 전이를 조정한다.

**Tech Stack:** Godot 4.7.1 stable, GDScript, JSON, Python 검증, Godot headless test, Android 세로 UI.

## Global Constraints

- 일반 강화 버튼 입력 한 번당 판정 한 번.
- 일반 강화와 +10 특수 강화 분리.
- 골드·재료·피로도 사전조건 실패 시 무차감.
- 날짜는 사용자 입력으로만 진행. 작업 예약·자동 날짜 진행 금지.
- 잔여 피로도 50% 이월, 소수점 버림, 별도 상한 없음.
- PoC는 `iron_sword`, 검투사 카일, +0~+10, 경기 결과 1건만 지원.
- 난수는 결과 밴드를 바꾸지 않음.
- `quality_*`는 호환 별칭이며 legacy 제작 정밀 의미를 조용히 재해석하지 않음.
- 제품 구현 전 `record_schema_version: 1`을 모든 신규 장비·세계 기록에 포함.
- 직원·직접 전투·시장·전쟁·관전·베팅·복원·방어구·악세서리·저장 마이그레이션 제외.

## File Map

### Create

- `data/progression/workshop_day_balance.json`
- `data/crafting/craftsmanship_grades.json`
- `data/customers/gladiator_poc.json`
- `data/world/gladiator_match_poc.json`
- `scripts/progression/workshop_calendar.gd`
- `scripts/forging/craftsmanship_grade_resolver.gd`
- `scripts/customers/customer_contract.gd`
- `scripts/world/equipment_world_registry.gd`
- `scripts/world/world_activity_resolver.gd`
- `scripts/poc/workshop_action_service.gd`
- `scripts/poc/equipment_lifecycle_poc_controller.gd`
- `scripts/telemetry/poc_telemetry.gd`
- `scripts/ui/workshop_hud.gd`
- `scripts/ui/customer_contract_screen.gd`
- `scripts/ui/world_report_screen.gd`
- `scenes/test/equipment_lifecycle_poc.tscn`
- 신규 단위·통합 테스트

### Modify

- `scripts/forging/forging_session.gd`
- `scripts/ui/forging_screen.gd`
- `scripts/ui/enhancement_screen.gd`
- `scripts/ui/game_flow_screen.gd`
- `tools/validate_game_data.py`
- `.github/workflows/godot-validation.yml`
- Game Bible·Active Context·Development Gates·Registry

---

## Task 1: Lifecycle data contracts

**Files:** 신규 JSON 4종, `tools/validate_game_data.py`, `tests/test_lifecycle_data_contract.py`

**Produces:** 검증된 fatigue, craftsmanship, contract, result-band 데이터.

- [ ] **Red:** 정상 데이터, 분포 합계 오류, 중복 ID, 알 수 없는 수식어, 역순 결과 밴드, 도달 불가능한 결과 반례를 작성한다.

```bash
python -m pytest tests/test_lifecycle_data_contract.py -q
```

Expected: 신규 데이터와 `validate_lifecycle_poc()`가 없어 FAIL.

- [ ] **Green data:**

```json
{
  "schema_version": 1,
  "base_fatigue": 20,
  "carryover_ratio": 0.5,
  "action_costs": {
    "forge": 3,
    "normal_enhance": 1,
    "special_enhance": 3,
    "restore": 5
  }
}
```

- [ ] `craftsmanship_grades.json`에 5등급과 정밀 결과별 분포를 기록한다.
- [ ] `gladiator_poc.json`은 required 5, stretch 10, preferred `sharp/flaming`, deadline 3, report delay 1, payment 500을 사용한다.
- [ ] `gladiator_match_poc.json` 점수는 required 20, stretch 15, preferred 25, grade 0/5/10/15/20, attack 10을 사용한다.
- [ ] 밴드는 DEFEAT 0, WIN 35, DECISIVE_WIN 70이다.
- [ ] 대표 반례:
  - 미숙한 +5 철검 = 30 DEFEAT
  - 정교한 +5 철검 = 40 WIN
  - 명품 +10 선호 수식어 철검 = 85 DECISIVE_WIN
- [ ] Validator는 모든 밴드에 도달 가능한 fixture가 존재하는지 검사한다.

```bash
python tools/validate_game_data.py
python -m pytest tests/test_lifecycle_data_contract.py -q
```

Expected: exit 0, all PASS.

- [ ] **Commit:** `feat: add reachable equipment lifecycle data contracts`

---

## Task 2: Workshop calendar and fatigue

**Files:** `scripts/progression/workshop_calendar.gd`, `tests/unit/test_workshop_calendar.gd`

**Interface:** `preview_spend(action_id)`, `try_spend(action_id)`, `refund(amount)`, `end_day()`, `snapshot()`.

- [ ] **Red:** 제작 3, 일반 강화 1, 특수 강화 3, 부족 시 `NO_FATIGUE`, 잔여 17에서 다음 날 28, 무작업 반복의 40 미만 수렴을 검증한다.
- [ ] `try_spend()` 실패는 상태를 변경하지 않는다.
- [ ] `end_day()`는 `base + floor(remaining × 0.5)`를 계산한다.
- [ ] HUD snapshot은 `current_fatigue`, `base_fatigue`, `carryover`를 별도 제공한다.

```bash
./godot --headless --path . --script res://tests/unit/test_workshop_calendar.gd
```

Expected marker: `WorkshopCalendar tests PASSED`.

- [ ] **Commit:** `feat: add workshop day and fatigue model`

---

## Task 3: Precision result, craftsmanship and legacy compatibility

**Files:** Resolver, `forging_session.gd`, `forging_screen.gd`, `game_flow_screen.gd`, 제작 단위·통합 테스트.

**Interface:** `CraftsmanshipGradeResolver.resolve(precision_result_id: String, roll: float) -> Dictionary`.

- [ ] **Red:** 정밀 결과와 완성도 필드 동시 존재, 고정 roll 분포, `quality_*` 별칭, legacy record 변환을 검증한다.
- [ ] 신규 결과에 `record_schema_version: 1`, `precision_result_*`, `craftsmanship_grade_*`를 추가한다.
- [ ] 신규 `quality_*`는 완성도 별칭으로 기록한다.
- [ ] legacy `quality_id: STANDARD/GOOD/PERFECT/AUTO`는 정밀 결과로 읽고 별도 변환한다.
- [ ] **자동 단조 호환:** `game_flow_screen.gd`의 자동 철검 template은 `precision_result_id: AUTO`, `craftsmanship_grade_id: STANDARD`, `record_schema_version: 1`을 생성한다.
- [ ] 기존 보관 기록 fixture와 신규 기록 fixture를 모두 강화 화면에서 열 수 있어야 한다.
- [ ] UI는 `마감 정타`와 `영구 완성도`를 별도 표시한다.

```bash
./godot --headless --path . --script res://tests/unit/test_forging_session.gd
./godot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd
```

- [ ] **Commit:** `feat: separate craftsmanship from precision with legacy compatibility`

---

## Task 4: Customer contract and fit

**Files:** `scripts/customers/customer_contract.gd`, `tests/unit/test_customer_contract.gd`

**Interface:** `can_deliver(equipment, day)`, `evaluate_fit(equipment)`, `remaining_days(day)`.

- [ ] **Red:** +4 미달, +5 가능, +10 stretch, 선호 수식어, 기한 초과, 다른 무기, 파괴 기록을 각각 검증한다.
- [ ] `can_deliver()` 실패는 missing conditions를 반환하고 장비·자원을 변경하지 않는다.
- [ ] `evaluate_fit()`은 required/stretch/affix/grade/attack을 독립 contribution으로 반환한다.
- [ ] 세 결과 밴드 대표 fixture의 score를 정확히 검증한다.

```bash
./godot --headless --path . --script res://tests/unit/test_customer_contract.gd
```

- [ ] **Commit:** `feat: add gladiator delivery contract and fit evidence`

---

## Task 5: World registry and deterministic result resolver

**Files:** `equipment_world_registry.gd`, `world_activity_resolver.gd`, 단위 테스트 2개.

**Interfaces:**

- Registry: `deliver`, `due_records`, `apply_result`, `mark_report_opened`, `retry_result`.
- Resolver: `resolve(fit, detail_roll)`.

- [ ] **Red:** DEFEAT/WIN/DECISIVE_WIN, detail roll 불변 밴드, 이력 순서, 활동 상한 6, 중복 event 적용을 검증한다.
- [ ] **상태 이름공간:**
  - `lifecycle_state`: WORKSHOP, ACTIVE_OWNER, EVENT_ELIGIBLE, DORMANT, HISTORICAL, BROKEN_OR_LOST
  - `report_state`: NONE, PENDING, RESULT_READY, REPORT_OPENED, RESULT_ERROR
- [ ] `ARCHIVED`를 장비 생애 상태로 사용하지 않는다.
- [ ] 모든 납품 기록은 보존하고 상한 초과 시 가장 오래된 비대표 기록을 DORMANT로 전환한다.
- [ ] 결과 누락은 RESULT_ERROR로 기록하고 같은 결정적 입력으로 재시도한다.

```bash
./godot --headless --path . --script res://tests/unit/test_world_activity_resolver.gd
./godot --headless --path . --script res://tests/unit/test_equipment_world_registry.gd
```

- [ ] **Commit:** `feat: add namespaced persistent equipment world results`

---

## Task 6: Atomic actions and lifecycle controller

**Files:** `workshop_action_service.gd`, `equipment_lifecycle_poc_controller.gd`, 통합 테스트 2개.

**Interfaces:** Action Service `try_begin_forging`, `try_begin_enhancement`; Controller `deliver`, `end_day`, `open_report`, `snapshot`.

- [ ] **Red resource atomicity:** fatigue/gold/material 부족과 session 시작 실패에서 모든 선차감 복구.
- [ ] **Red 원자적 납품:** inventory 제거, owner 변경, payment, immediate fame, world record 생성의 각 단계에 실패를 주입한다.
- [ ] 실패 시 다섯 상태가 모두 원상 복구돼야 한다.
- [ ] `delivery_transaction_id` 중복 재시도는 대금·명성·기록을 중복 생성하지 않는다.
- [ ] Action Service 순서: 모든 preview → spend → begin → 실패 rollback.
- [ ] Controller 상태: CONTRACT, WORKSHOP, REPORT_READY, FOLLOW_UP.
- [ ] `open_report()`는 세계 명성·관계를 한 번만 적용한다.

```bash
./godot --headless --path . --script res://tests/integration/test_workshop_action_atomicity.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_controller.gd
```

- [ ] **Commit:** `feat: coordinate atomic lifecycle and delivery actions`

---

## Task 7: PoC telemetry

**Files:** `scripts/telemetry/poc_telemetry.gd`, `tests/unit/test_poc_telemetry.gd`

**Interface:** `record`, `events_named`, `export_json`, `clear`.

- [ ] 이벤트 순서, deep copy, 필터, 명시적 export를 검증한다.
- [ ] 네트워크 전송·개인정보 수집 없음.
- [ ] 필수 이벤트: contract viewed, forging completed, enhancement attempted/stopped, discarded, delivered, day ended, report opened, follow-up started.

```bash
./godot --headless --path . --script res://tests/unit/test_poc_telemetry.gd
```

- [ ] **Commit:** `feat: add local lifecycle poc telemetry`

---

## Task 8: Portrait UI and accessibility path

**Files:** 신규 HUD·계약·보고 UI, PoC Scene, `enhancement_screen.gd`, `game_flow_screen.gd`, `main.tscn`.

- [ ] 계약 화면: 고객, +5 필수, +10 선택, 선호 수식어, 기한, 대금, 단일 주 행동.
- [ ] HUD: 날짜, `현재 작업 가능량`, `기본 일일량`, 골드, 남은 기한, 하루 마치기.
- [ ] 보고 화면: 결과 ID·텍스트, 기여, 부족 조건, 사건, 이력, 명성·관계. 자동 닫힘 금지.
- [ ] 색상만으로 성공·위험·선택을 구분하지 않는다.
- [ ] 최소 48dp 상당 터치 영역.
- [ ] **정밀 입력 대안:** 느린 게이지·넓은 판정 구간과 `정밀 보조`를 제공한다. 보조는 GOOD 분포를 사용하고 PERFECT 희귀 보너스를 자동 제공하지 않는다.
- [ ] 모션·진동 감소 설정을 실제 제작 화면에 전달한다.
- [ ] NO_FATIGUE는 부족량과 하루 마치기 경로를 표시하되 날짜를 자동 진행하지 않는다.
- [ ] deliver 성공 후에만 보관함 제거.

```bash
./godot --headless --editor --path . --quit
./godot --headless --path . res://scenes/main/main.tscn --quit-after 2
./godot --headless --path . res://scenes/test/equipment_lifecycle_poc.tscn --quit-after 2
```

Expected: exit 0, no SCRIPT/Parse/Compile ERROR.

- [ ] **Commit:** `feat: add accessible equipment lifecycle poc screens`

---

## Task 9: E2E, CI and canonical synchronization

**Files:** E2E test, Godot Workflow, Game Bible, Active Context, Gates, Registry.

- [ ] E2E normal path:

```text
계약 수락
→ 정교한 철검 생성
→ 제작 피로도 3
→ +1~+5
→ +5 납품
→ 하루 종료
→ WIN
→ 보고 열기
→ 이력 확인
→ 재방문
```

- [ ] E2E boundary paths:
  - 미숙한 +5 DEFEAT
  - 명품 +10 preferred DECISIVE_WIN
  - NO_FATIGUE/NO_GOLD/NO_MATERIAL
  - delivery rollback and idempotent retry
  - RESULT_ERROR deterministic retry
  - legacy AUTO record compatibility
- [ ] Workflow에 모든 신규 test command, process exit, expected PASS marker를 추가한다.
- [ ] `python tests/check_project_core_alignment.py`를 유지한다.
- [ ] Game Bible에는 실제 구현 완료 뒤에만 구현 상태를 올린다.
- [ ] Active Context에 정확한 Workflow run과 미실행 검증을 기록한다.
- [ ] Android·접근성·성능·외부 플레이는 증거 전까지 NOT_RUN.

```bash
python tests/check_no_merge_conflicts.py .
python tools/validate_game_data.py
python tests/check_project_core_alignment.py
python -m pytest tests/test_lifecycle_data_contract.py -q
./godot --headless --editor --path . --quit
./godot --headless --path . res://scenes/test/enhancement_test.tscn --quit-after 2
./godot --headless --path . res://scenes/test/equipment_lifecycle_poc.tscn --quit-after 2
./godot --headless --path . res://scenes/main/main.tscn --quit-after 2
./godot --headless --path . --script res://tests/unit/test_forging_session.gd
./godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
./godot --headless --path . --script res://tests/unit/test_workshop_resources.gd
./godot --headless --path . --script res://tests/unit/test_workshop_calendar.gd
./godot --headless --path . --script res://tests/unit/test_customer_contract.gd
./godot --headless --path . --script res://tests/unit/test_world_activity_resolver.gd
./godot --headless --path . --script res://tests/unit/test_equipment_world_registry.gd
./godot --headless --path . --script res://tests/unit/test_poc_telemetry.gd
./godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd
./godot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd
./godot --headless --path . --script res://tests/integration/test_workshop_action_atomicity.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_controller.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_poc.gd
```

- [ ] **Commit:** `test: verify complete equipment lifecycle poc`

## Completion Gate

다음을 모두 확인하기 전에는 구현 완료를 선언하지 않는다.

1. 제작부터 재방문까지 E2E.
2. +5/+10 양 선택 유효.
3. 세 결과 밴드 도달.
4. 자원·납품 원자성.
5. 영구 장비 기록.
6. 신규·기존 회귀 전체 PASS.
7. Godot import·Scene smoke PASS.
8. Android·접근성·외부 플레이 미실행을 PASS로 표시하지 않음.

## Execution Handoff

1. PR #31→#32→#33을 병합하거나 #33 전체 head에서 격리 worktree를 만든다.
2. Issue #34를 기준으로 Task 1~9를 순차 실행한다.
3. 각 Task의 Red evidence, Green diff, regression 결과를 검토한 뒤 다음 Task로 진행한다.
4. 전체 Green 뒤 별도 구현 PR을 연다.
5. 사람 세로 UI 검토와 내부 콜드 스타트 전까지 구현 PR을 Draft로 유지한다.
