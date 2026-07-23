# MVP-003 구현·검증 상태 원장

- 갱신일: 2026-07-24
- Issue: #34
- Draft PR: #35
- 브랜치: `agent/implement-equipment-lifecycle-poc`
- 현재 판정: `IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED`
- GitHub Actions: `DEFERRED_UNTIL_ACTIONS_AVAILABLE`

이 문서는 구현계획 Task 1~9의 **작성 여부와 실행 증거를 분리**한다. 코드·테스트가 작성됐다는 사실만으로 PASS를 선언하지 않는다.

## Task 상태

| Task | 구현 산출물 | 작성 상태 | 실행 상태 |
|---:|---|---|---|
| 1 | lifecycle JSON 4종, validator, Python 계약 테스트 | 완료 후보 | 최신 head `NOT_RUN` |
| 2 | `WorkshopCalendar`, 피로도·날짜 단위 테스트 | 완료 후보 | 최신 head `NOT_RUN` |
| 3 | 영구 완성도 Resolver, legacy 변환 테스트 | 완료 후보 | 최신 head `NOT_RUN` |
| 4 | 검투사 계약·적합도 모델과 테스트 | 완료 후보 | 최신 head `NOT_RUN` |
| 5 | 세계 Registry·결정적 결과 Resolver와 테스트 | 완료 후보 | 최신 head `NOT_RUN` |
| 6 | 제작·강화·납품 원자 거래, Controller 통합 테스트 | 완료 후보 | 최신 head `NOT_RUN` |
| 7 | 로컬 PoC telemetry와 테스트 | 완료 후보 | 최신 head `NOT_RUN` |
| 8 | 계약·HUD·제작·강화·보고·재방문 세로 UI, 접근성 보조 | 완료 후보 | Scene·사람 검토 `NOT_RUN` |
| 9 | 전체 생애 E2E, CI 최적화, 정본 동기화 | 완료 후보 | 최신 E2E·전체 회귀 `NOT_RUN` |

## 구현 후보 파일군

### 데이터·검증

- `data/progression/workshop_day_balance.json`
- `data/crafting/craftsmanship_grades.json`
- `data/customers/gladiator_poc.json`
- `data/world/gladiator_match_poc.json`
- `tools/validate_lifecycle_data.py`
- `tests/test_lifecycle_data_contract.py`

### 도메인 모델

- `scripts/progression/workshop_calendar.gd`
- `scripts/forging/craftsmanship_grade_resolver.gd`
- `scripts/customers/customer_contract.gd`
- `scripts/world/equipment_world_registry.gd`
- `scripts/world/world_activity_resolver.gd`
- `scripts/poc/workshop_action_service.gd`
- `scripts/poc/equipment_lifecycle_poc_controller.gd`
- `scripts/telemetry/poc_telemetry.gd`

### UI·Scene

- `scripts/poc/equipment_lifecycle_poc_screen.gd`
- `scripts/ui/workshop_hud.gd`
- `scripts/ui/customer_contract_screen.gd`
- `scripts/ui/world_report_screen.gd`
- `scripts/ui/lifecycle_enhancement_screen.gd`
- `scripts/ui/lifecycle_accessibility_overlay.gd`
- `scripts/ui/poc_entry_button.gd`
- `scenes/test/equipment_lifecycle_poc.tscn`
- `scenes/main/main.tscn`

### 신규 테스트

- `tests/unit/test_workshop_calendar.gd`
- `tests/unit/test_craftsmanship_grade_resolver.gd`
- `tests/unit/test_customer_contract.gd`
- `tests/unit/test_world_activity_resolver.gd`
- `tests/unit/test_equipment_world_registry.gd`
- `tests/unit/test_poc_telemetry.gd`
- `tests/integration/test_workshop_action_atomicity.gd`
- `tests/integration/test_equipment_lifecycle_controller.gd`
- `tests/integration/test_equipment_lifecycle_poc.gd`
- `tests/test_ci_workflow_structure.py`

## 보호된 계약

- 제작 시작에만 피로도 3을 소비하며 탭마다 소비하지 않는다.
- 일반 강화 버튼 입력당 판정 1회와 피로도 1을 소비한다.
- +10 특수 강화는 피로도 3과 재료·정밀 판정을 사용한다.
- PoC 강화 상한은 +10이다.
- 특수 강화 정밀 판정 중에는 대장간으로 이탈할 수 없다.
- 작업량·골드·재료 부족은 어떤 상태도 부분 변경하지 않는다.
- 날짜는 `하루 마치기`로만 진행한다.
- 다음 날 작업량은 `20 + floor(남은 작업량 × 0.5)`다.
- +5는 납품 가능선, +10은 선택적 수식어 도전이다.
- 결과 밴드는 결정적 점수로 정하며 난수는 밴드를 바꾸지 않는다.
- 납품 기록은 판매 뒤에도 유지된다.
- 같은 거래와 같은 세계 사건 재시도는 중복 보상을 만들지 않는다.
- 정밀 보조는 GOOD 경로를 제공하며 PERFECT를 자동 제공하지 않는다.

## 이전 증거와 한계

과거 구현 중간 head에서 다음이 통과했다.

- Data validation #452: PASS
- Godot validation #379: PASS

이후 UI, 전체 생애 E2E, 접근성, CI 구조와 정본 변경이 추가됐으므로 위 실행은 최신 PR head의 PASS 증거가 아니다.

## Actions 재개 후 필수 실행

1. `data-validation.yml`의 `pull_request` 트리거 복원
2. 최신 head Ubuntu Python 코드 계약 실행
3. Godot 4.7.1 import·parse 실행
4. `main.tscn`과 `equipment_lifecycle_poc.tscn` smoke 실행
5. 기존·신규 Godot 단위·통합·E2E 전체 실행
6. 실패 수정 후 같은 범위를 재실행
7. `full-validation.yml`의 main/nightly 트리거 복원
8. Ubuntu·Windows × Python 3.11·3.12·3.13 실행
9. cancellation과 실제 Required Check 이름 확인
10. PR #35 코드 리뷰와 병합 판정

## 사람·플랫폼 검증

다음은 자동 검증과 별개로 남아 있다.

- Android 실제 기기와 안전 영역
- 정밀 보조·모션 감소의 실제 사용성
- 색상 비의존 정보 전달
- 대표·최악 장면 성능
- 외부 신규 플레이어 6명 권장 테스트

## 완료 판정

현재 구현계획의 Task 1~9에 해당하는 파일은 작성됐다. 그러나 최신 head의 자동·사람·플랫폼 증거가 없으므로 상태는 `IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED`이며 PR #35는 Draft를 유지한다.
