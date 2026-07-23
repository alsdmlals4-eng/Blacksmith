# Blacksmith 장비 생애 PoC 구현계획

> **에이전트 실행 요구사항:** 구현 시 `superpowers:subagent-driven-development`(권장) 또는 `superpowers:executing-plans`를 사용한다. 각 작업은 Red→Green→Refactor와 독립 커밋으로 끝낸다.

**목표:** 검투사 의뢰 확인부터 철검 제작, +5 납품 또는 +10 추가 도전, 수동 날짜 진행, 지연 경기 결과, 영구 장비 이력, 같은 고객의 재방문까지 첫 장비 생애 PoC를 구현한다.

**아키텍처:** 날짜·피로도, 완성도, 고객 평가, 세계 기록, 결과 판정을 독립 도메인 모델로 분리한다. `GameFlowScreen`은 화면 라우팅만 담당하고 `EquipmentLifecyclePocController`가 시스템 간 상태 전이를 조정한다.

**기술:** Godot 4.7.1 stable, GDScript, JSON, Python 검증, Godot headless 테스트, Android 세로 UI.

## 1. 구현 불변 조건

- 강화 버튼 입력 한 번당 판정 한 번.
- 일반 강화와 +10 특수 강화 분리.
- 골드·재료·피로도 사전조건 실패 시 무차감.
- 날짜는 사용자 입력으로만 진행. 작업 예약·자동 날짜 진행 금지.
- 남은 피로도 50% 이월, 소수점 버림, 별도 상한 없음.
- PoC는 iron_sword, 검투사 카일, +0~+10, 경기 결과 1건만 지원.
- 난수는 결과 밴드를 바꾸지 않고 같은 밴드 내부의 문장·보상 강도만 변경.
- 기존 quality_* 필드는 호환 별칭으로 유지.
- 직원, 직접 전투, 시장, 전쟁, 관전, 베팅, 복원, 방어구, 악세서리, 저장 마이그레이션 제외.

## 2. 목표 구조

```text
GameFlowScreen
  ├─ EquipmentLifecyclePocController
  │    ├─ WorkshopCalendar
  │    ├─ WorkshopResources
  │    ├─ CustomerContract
  │    ├─ EquipmentWorldRegistry
  │    └─ WorldActivityResolver
  ├─ ForgingScreen / ForgingSession
  ├─ EnhancementScreen / EnhancementSession
  ├─ CustomerContractScreen
  ├─ WorkshopHud
  └─ WorldReportScreen
```

## 3. 계획 파일 지도

### 신규 데이터

- Create: data/progression/workshop_day_balance.json
- Create: data/crafting/craftsmanship_grades.json
- Create: data/customers/gladiator_poc.json
- Create: data/world/gladiator_match_poc.json

### 신규 도메인 코드

- Create: scripts/progression/workshop_calendar.gd
- Create: scripts/forging/craftsmanship_grade_resolver.gd
- Create: scripts/customers/customer_contract.gd
- Create: scripts/world/equipment_world_registry.gd
- Create: scripts/world/world_activity_resolver.gd
- Create: scripts/poc/workshop_action_service.gd
- Create: scripts/poc/equipment_lifecycle_poc_controller.gd
- Create: scripts/telemetry/poc_telemetry.gd

### 신규 UI·테스트

- Create: scripts/ui/workshop_hud.gd
- Create: scripts/ui/customer_contract_screen.gd
- Create: scripts/ui/world_report_screen.gd
- Create: scenes/test/equipment_lifecycle_poc.tscn
- Create: tests/test_lifecycle_data_contract.py
- Create: tests/unit/test_workshop_calendar.gd
- Create: tests/unit/test_customer_contract.gd
- Create: tests/unit/test_world_activity_resolver.gd
- Create: tests/unit/test_equipment_world_registry.gd
- Create: tests/unit/test_poc_telemetry.gd
- Create: tests/integration/test_workshop_action_atomicity.gd
- Create: tests/integration/test_equipment_lifecycle_controller.gd
- Create: tests/integration/test_equipment_lifecycle_poc.gd

### 수정

- Modify: scripts/forging/forging_session.gd
- Modify: scripts/ui/forging_screen.gd
- Modify: scripts/ui/enhancement_screen.gd
- Modify: scripts/ui/game_flow_screen.gd
- Modify: tools/validate_game_data.py
- Modify: .github/workflows/godot-validation.yml
- Modify: [기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md
- Modify: [기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md
- Modify: [기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md
- Modify: [기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json

---

## Task 1. 장비 생애 데이터 계약과 검증

**파일:** 신규 JSON 4종, tools/validate_game_data.py, tests/test_lifecycle_data_contract.py

- [ ] 실패 테스트 작성: 정상 데이터 통과, 완성도 분포 합계 오류, 존재하지 않는 수식어 참조, 결과 밴드 역순을 검증한다.
- [ ] Red 실행:

```bash
python -m pytest tests/test_lifecycle_data_contract.py -q
```

Expected: 신규 파일과 함수가 없어 FAIL.

- [ ] workshop_day_balance.json 기준값:

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

- [ ] craftsmanship_grades.json에 ROUGH·STANDARD·REFINED·EXCELLENT·MASTERPIECE와 정밀 결과별 분포를 기록한다.
- [ ] gladiator_poc.json에 첫 의뢰와 재방문 의뢰를 기록한다. 첫 의뢰는 required_level 5, stretch_level 10, preferred_affix_ids sharp/flaming, deadline_day_offset 3, report_delay_days 1, base_payment 500이다.
- [ ] gladiator_match_poc.json에 required 25, stretch 15, preferred affix 25, attack 20과 DEFEAT 0·WIN 40·DECISIVE_WIN 70 밴드를 기록한다.
- [ ] tools/validate_game_data.py에 `validate_lifecycle_poc()`를 추가한다. 분포 합계, ID 중복, 참조 무결성, 밴드 오름차순을 검사한다.
- [ ] Green 실행:

```bash
python tools/validate_game_data.py
python -m pytest tests/test_lifecycle_data_contract.py -q
```

Expected: validator exit 0, pytest 전체 PASS.

- [ ] 커밋:

```bash
git add data/progression data/crafting/craftsmanship_grades.json data/customers data/world tools/validate_game_data.py tests/test_lifecycle_data_contract.py
git commit -m "feat: add equipment lifecycle poc data contracts"
```

---

## Task 2. 날짜·피로도 모델

**파일:** scripts/progression/workshop_calendar.gd, tests/unit/test_workshop_calendar.gd

**인터페이스:** `preview_spend`, `try_spend`, `refund`, `end_day`, `snapshot`.

- [ ] 실패 테스트: 제작 비용 3, 일반 강화 비용 1, 부족 시 NO_FATIGUE, 17 잔여 피로도에서 다음 날 28, 날짜 증가를 검증한다.
- [ ] Red 실행:

```bash
./godot --headless --path . --script res://tests/unit/test_workshop_calendar.gd
```

- [ ] 최소 구현: `end_day()`는 `base_fatigue + floor(remaining_fatigue * carryover_ratio)`를 계산한다. `try_spend()`는 부족 시 상태를 변경하지 않는다.
- [ ] Green·커밋:

```bash
./godot --headless --path . --script res://tests/unit/test_workshop_calendar.gd
git add scripts/progression/workshop_calendar.gd tests/unit/test_workshop_calendar.gd
git commit -m "feat: add workshop day and fatigue model"
```

Expected marker: `WorkshopCalendar tests PASSED`.

---

## Task 3. 정밀 결과와 영구 완성도 분리

**파일:** scripts/forging/craftsmanship_grade_resolver.gd, scripts/forging/forging_session.gd, scripts/ui/forging_screen.gd, 기존 제작 단위·통합 테스트.

**인터페이스:** `CraftsmanshipGradeResolver.resolve(precision_result_id, roll)`.

- [ ] 실패 테스트: GOOD 결과에서 주입 roll에 따라 STANDARD/REFINED가 결정되는지, 정밀 결과와 완성도 필드가 동시에 존재하는지, quality_* 별칭이 완성도와 일치하는지 검증한다.
- [ ] 판정기는 분포 누적합으로 완성도를 결정하고 등급 객체를 반환한다.
- [ ] ForgingSession 결과에 precision_result_id/label, craftsmanship_grade_id/label, craftsmanship_attack_multiplier, craftsmanship_value_multiplier를 추가한다.
- [ ] quality_id/label/attack_multiplier/value_multiplier는 완성도의 호환 별칭으로 기록한다.
- [ ] UI는 `마감 정타`와 `영구 완성도`를 별도 행으로 표시한다.
- [ ] 회귀·커밋:

```bash
./godot --headless --path . --script res://tests/unit/test_forging_session.gd
./godot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd
git add scripts/forging scripts/ui/forging_screen.gd tests/unit/test_forging_session.gd tests/integration/test_forging_quality_enhancement.gd
git commit -m "feat: separate precision result and craftsmanship grade"
```

---

## Task 4. 고객 의뢰와 납품 적합도

**파일:** scripts/customers/customer_contract.gd, tests/unit/test_customer_contract.gd

**인터페이스:** `can_deliver`, `evaluate_fit`, `remaining_days`.

- [ ] 실패 테스트: +4 미달, +5 납품 가능, +10 stretch, 선호 수식어, 기한 초과, 다른 무기 ID를 각각 검증한다.
- [ ] `can_deliver()`는 missing_conditions 배열을 반환하고 장비 상태를 변경하지 않는다.
- [ ] `evaluate_fit()`은 required, stretch, preferred affix, grade, attack를 독립 기여 항목으로 반환한다.
- [ ] 실행·커밋:

```bash
./godot --headless --path . --script res://tests/unit/test_customer_contract.gd
git add scripts/customers/customer_contract.gd tests/unit/test_customer_contract.gd
git commit -m "feat: add gladiator delivery contract"
```

---

## Task 5. 세계 장비 기록과 결정적 결과 판정

**파일:** scripts/world/equipment_world_registry.gd, scripts/world/world_activity_resolver.gd, 대응 단위 테스트 2개.

**인터페이스:** Registry의 `deliver`, `due_records`, `apply_result`, `mark_report_opened`; Resolver의 `resolve`.

- [ ] 실패 테스트: +5 정교한 철검을 55점 WIN으로 판정, +10·선호 수식어·명품을 DECISIVE_WIN으로 판정, detail roll 변화가 밴드를 바꾸지 않음, 이력 순서 보존, 활동 상한 6을 검증한다.
- [ ] Resolver는 outcome_band, score, contributions, missing_conditions, fame_reward, relationship_delta를 반환한다.
- [ ] Registry 상태 전이는 ACTIVE→RESULT_READY→REPORT_OPENED→ARCHIVED로 제한한다.
- [ ] 모든 납품 기록은 보존하고 활동 상한 초과 시 오래된 비대표 기록만 ARCHIVED로 이동한다.
- [ ] 실행·커밋:

```bash
./godot --headless --path . --script res://tests/unit/test_world_activity_resolver.gd
./godot --headless --path . --script res://tests/unit/test_equipment_world_registry.gd
git add scripts/world tests/unit/test_world_activity_resolver.gd tests/unit/test_equipment_world_registry.gd
git commit -m "feat: add persistent equipment world results"
```

---

## Task 6. 원자 거래와 생애 컨트롤러

**파일:** scripts/poc/workshop_action_service.gd, scripts/poc/equipment_lifecycle_poc_controller.gd, 대응 통합 테스트 2개.

**인터페이스:** Action Service의 `try_begin_enhancement`; Controller의 `deliver`, `end_day`, `open_report`, `snapshot`.

- [ ] 원자성 실패 테스트: 피로도·골드·재료 부족과 session 시작 실패에서 모든 선차감이 복구되는지 검증한다.
- [ ] Action Service 순서: fatigue preview → resource preview → fatigue spend → resource begin → 실패 시 fatigue refund.
- [ ] Controller 상태: CONTRACT, WORKSHOP, REPORT_READY, FOLLOW_UP.
- [ ] deliver 성공 시 기본 대금·즉시 명성·세계 기록을 한 번만 적용한다.
- [ ] end_day는 날짜 진행 후 due record만 판정한다.
- [ ] open_report는 세계 명성·관계를 적용하고 재방문을 해금한다.
- [ ] 실행·커밋:

```bash
./godot --headless --path . --script res://tests/integration/test_workshop_action_atomicity.gd
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_controller.gd
git add scripts/poc tests/integration/test_workshop_action_atomicity.gd tests/integration/test_equipment_lifecycle_controller.gd
git commit -m "feat: coordinate atomic lifecycle actions"
```

---

## Task 7. PoC 행동 로그

**파일:** scripts/telemetry/poc_telemetry.gd, tests/unit/test_poc_telemetry.gd

**인터페이스:** `record`, `events_named`, `export_json`, `clear`.

- [ ] 이벤트 순서, deep copy, 이름 필터, JSON 내보내기 실패 테스트를 먼저 작성한다.
- [ ] 최소 메모리 로그를 구현한다. 네트워크 전송·개인정보 수집은 하지 않는다.
- [ ] 필수 이벤트: contract_viewed, forging_completed, enhancement_attempted, enhancement_stopped, equipment_discarded, equipment_delivered, day_ended, world_report_opened, follow_up_started.
- [ ] 실행·커밋:

```bash
./godot --headless --path . --script res://tests/unit/test_poc_telemetry.gd
git add scripts/telemetry/poc_telemetry.gd tests/unit/test_poc_telemetry.gd
git commit -m "feat: add lifecycle poc telemetry"
```

---

## Task 8. 세로 UI와 기존 흐름 통합

**파일:** 신규 HUD·계약·보고 UI, 신규 PoC test scene, scripts/ui/enhancement_screen.gd, scripts/ui/game_flow_screen.gd, scenes/main/main.tscn.

- [ ] 계약 화면: 고객, 철검, +5 필수, +10 선택, 선호 수식어, 마감, 대금, 단일 `의뢰 수락` 버튼.
- [ ] 공통 HUD: 날짜, 남은/기본 피로도, 골드, 남은 기한, `하루 마치기`.
- [ ] 보고 화면: 결과 밴드, 효과 선택, 부족 조건, 사건, 이력, 명성·관계, 확인 버튼. 자동 닫힘 금지.
- [ ] EnhancementScreen의 직접 WorkshopResources 호출을 WorkshopActionService로 교체한다. NO_FATIGUE 시 부족량을 표시하고 날짜를 자동 진행하지 않는다.
- [ ] GameFlowScreen 초기 화면을 계약 화면으로 바꾸고 도메인 판정을 Controller에 위임한다.
- [ ] 보관 장비에 적합도 통과 시에만 `검투사에게 납품` 버튼을 표시한다. deliver 성공 후에만 보관함에서 제거한다.
- [ ] Smoke 실행:

```bash
./godot --headless --editor --path . --quit
./godot --headless --path . res://scenes/main/main.tscn --quit-after 2
./godot --headless --path . res://scenes/test/equipment_lifecycle_poc.tscn --quit-after 2
```

Expected: exit 0, SCRIPT/Parse/Compile ERROR 없음.

- [ ] 커밋:

```bash
git add scripts/ui scenes/test/equipment_lifecycle_poc.tscn scenes/main/main.tscn
git commit -m "feat: add equipment lifecycle poc screens"
```

---

## Task 9. 전체 생애 E2E·CI·정본 동기화

**파일:** tests/integration/test_equipment_lifecycle_poc.gd, .github/workflows/godot-validation.yml, Game Bible, Active Context, Development Gates, Design Document Registry.

- [ ] 결정 경로 E2E 작성:

```text
첫 의뢰 수락
→ REFINED 철검 생성
→ 제작 피로도 3 소비
→ +1~+5 성공 고정
→ +5 납품
→ 하루 종료
→ WIN 판정
→ 보고서 열기
→ 영구 이력 확인
→ 재방문 해금
```

- [ ] assertion: 강화당 피로도 1, 대금 500, 즉시 명성 1, 50% 이월, WIN, 기여·미충족 배열, 세계 명성·관계, 납품·경기 이력, 재방문.
- [ ] E2E 실행:

```bash
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_poc.gd
```

Expected marker: `Equipment lifecycle PoC integration tests PASSED`.

- [ ] Godot workflow에 신규 단위·통합 테스트 명령, PASS marker, process status를 모두 추가한다.
- [ ] 전체 로컬 검증:

```bash
python tests/check_no_merge_conflicts.py
python tools/validate_game_data.py
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

- [ ] Game Bible에는 구현된 행동만 반영한다. Active Context에는 정확한 테스트 수와 Workflow ID를 기록한다. Android·접근성·시각·성능·외부 플레이는 증거 전까지 NOT_RUN.
- [ ] 사람 검증: 720×1280 및 좁은 Android viewport, 터치·스크롤, 설명 없는 내부 콜드 스타트 1회, 외부 5명.
- [ ] 행동 통과 신호: +5/+10 고민, 보고서 자발 열람, 결과 원인 2개 회상, 낮은 등급 폐기율 50% 미만, 날짜 넘기기 전용 세션 20% 미만, 재방문 후 새 제작 시작.
- [ ] 커밋:

```bash
git add tests/integration/test_equipment_lifecycle_poc.gd .github/workflows/godot-validation.yml "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md" "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md" "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md" "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
git commit -m "test: verify complete equipment lifecycle poc"
```

## 4. 완료 선언 조건

다음을 모두 확인하기 전에는 구현 완료를 선언하지 않는다.

1. 철검 제작부터 검투사 재방문까지 E2E 완주.
2. +5 납품과 +10 도전이 모두 유효.
3. 골드·재료·피로도 원자성.
4. 결과 밴드의 결정성.
5. 납품 이후 장비 기록 유지.
6. 신규 테스트와 기존 회귀 전체 PASS.
7. Godot import와 main scene smoke PASS.
8. Android·접근성·외부 플레이 미실행 상태를 PASS로 표시하지 않음.

## 5. 실행 순서

1. PR 스택 #31→#32→#33을 병합하거나 전체 head에서 격리 worktree를 만든다.
2. Tasks 1~9를 순서대로 실행한다.
3. 각 Task의 diff와 테스트 증거를 검토한 뒤 다음 Task로 진행한다.
4. 전체 검증 세트가 통과한 뒤에만 별도 구현 PR을 연다.
5. 세로 UI와 내부 콜드 스타트 검토 전까지 구현 PR을 Draft로 유지한다.
