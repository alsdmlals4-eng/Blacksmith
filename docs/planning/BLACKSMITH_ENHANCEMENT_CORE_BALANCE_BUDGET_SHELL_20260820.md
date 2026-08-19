# [제안] Blacksmith 강화 Core Balance Budget Shell

- Parent: `BS-CORE-20260820-01`
- 상태: `STRUCTURE_ONLY / NUMBERS_NOT_FINAL`

## 목적

정확한 강화 수치를 먼저 고정하지 않고, **강화 긴장감과 DDD가 유지되는 범위**를 데이터로 조정하기 위한 예산 틀이다.

## 강화 위험 구간

각 구간은 최종 단계 번호가 아니라 플레이 경험 역할로 먼저 정의한다.

```text
LEARN
→ BUILD_CONFIDENCE
→ FIRST_STOP_POINT
→ TENSION
→ HIGH_STAKES
→ MASTERY
```

## 구간별 관리 변수

```yaml
band:
  role:
  success_rate_default:
  success_rate_safe_range:
  expected_reward_gain:
  fail_hold_rate:
  fail_damage_rate:
  critical_break_rate:
  attempt_cost:
  work_cost:
  protection_available:
  protection_cost:
  protection_effect:
  recovery_progress_per_failure:
  recovery_cap_or_guarantee:
  expected_attempts_to_success:
  max_bad_luck_window:
  feedback_intensity:
  stop_value:
  continue_value:
```

## 튜닝 신호

### 위험이 너무 낮음
- 거의 모든 플레이어가 생각 없이 연속 강화
- 멈춤 선택이 드묾
- 강화 전 화면 체류 시간이 사실상 0

### 위험이 너무 높음
- 안전 확보 후 추가 강화 거의 안 함
- 실패 후 즉시 게임/강화 이탈
- 좋은 작품일수록 사용하지 않고 창고에만 보관

### 회복이 너무 강함
- 실패가 사실상 성공 게이지 충전으로만 인식
- 확률 결과에 대한 긴장 사라짐

### 회복이 너무 약함
- 실패 연속에서 진행감 0
- 재료 파밍만 남음

### 보조 콘텐츠가 과도함
- 정밀제작/고객 화면 체류가 강화보다 큼
- 강화 목표를 만들기보다 별도 메인 루프로 분리됨

## 초기 권장 정책

- LEARN/BULD_CONFIDENCE는 규칙 학습과 성공 피드백을 우선한다.
- FIRST_STOP_POINT에서 처음으로 '여기서 끝내도 가치 있음'을 제공한다.
- TENSION부터 실패 결과와 회복 누적을 체감시킨다.
- HIGH_STAKES는 보호/고위험 선택을 열 수 있으나 정확 수치는 플레이테스트 전 고정하지 않는다.
- MASTERY는 장기 목표이며 첫 Vertical Slice 필수 범위가 아니다.
