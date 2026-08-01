# Blacksmith 자동 단조 경계 승인 정본

> Decision ID: `BS-AUTOFORGE-20260801-01`
>
> 상태: `USER_PREAPPROVED_RECOMMENDED / CANONICAL_DESIGN_COMPLETE`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 선행 결정: `BS-SAVE-20260801-01`, `BS-GRADE-20260801-02`, `BS-ENH-20260731-01`, `BS-V9-20260731-02~03`

## 1. 목적

자동 단조는 이미 판단한 반복 작업을 줄이는 편의 기능이다. 작품의 완성·정체성·위험·특수재료·소유권 결정을 대신하지 않는다.

```text
자동화 가능한 것
= 같은 장비의 비결정 일반 강화 반복

자동화할 수 없는 것
= 제작 완성·정체성·정밀 입력·+50 경로·판매·인계·세계 결과·파괴 후 재시작 결정
```

## 2. 제품 명칭과 범위

제품 UI 명칭은 `자동 강화`로 사용한다. 구형 `자동 단조`는 과거 PoC 기능명으로만 보존한다.

이유:

- 제품 기능은 새 장비를 자동 생산하지 않는다.
- 단조·마감·제작 등급 판정은 수동 제작 결과다.
- 파괴 후 새 철검을 자동 생성해 반복하는 기능은 제거한다.

## 3. 시작 조건

자동 강화는 다음 조건을 모두 충족할 때만 시작한다.

- 플레이어가 보유한 제작 완료 장비
- 강화 화면의 `READY` 상태
- 미확인 ResultEnvelope 없음
- PREPARED 또는 미해결 Intent 없음
- 목표 단계가 현재 단계보다 높음
- 목표 단계가 다음 필수 정지점 이전 또는 해당 정지점으로 설정됨
- 시도 상한 1~100회 설정
- 최소 골드 잔액 또는 최대 지출 한도 중 하나 이상 설정
- 저장 공간·원자 저장 preflight 통과

## 4. 자동 강화 설정

```text
AutoEnhancePolicy
├─ equipment_uid
├─ requested_target_level
├─ max_attempts
├─ max_gold_spend
├─ minimum_gold_reserve
├─ allowed_normal_skill_id
├─ stop_on_hold
├─ stop_on_downgrade
└─ policy_created_revision
```

### 기본값

| 항목 | 기본값 |
|---|---|
| 최대 시도 | 10회 |
| 최대 지출 | 현재 UI에 입력된 값 또는 없음 |
| 최소 골드 잔액 | 0 |
| HOLD 시 정지 | 아니오 |
| DOWNGRADE 시 정지 | 예 |
| DESTROY 시 정지 | 항상 예·변경 불가 |
| 목표 달성 시 정지 | 항상 예 |

최대 시도와 지출·잔액 제한을 모두 무제한으로 둘 수 없다.

## 5. 필수 정지점

자동 강화는 다음 단계 **진입 전** 멈추고 사용자의 명시적 행동을 기다린다.

```text
+5  작품 완성·보관·판매·추가 강화 판단
+10 계보 선택
+20 보조1 선택
+30 계보 강화·파생 선택
+40 보조2 선택
+49→+50 일반 정밀 / 고위 정밀 경로 선택과 정밀 입력
판매·고객 인계
세계 결과 적용·운명 변경
```

### +60 이상

- 새 슬롯 선택이 없는 일반 단계만 자동화 가능하다.
- 계보·보조 심화 후보 선택이 발생하는 단계는 데이터가 `requires_player_choice=true`이면 필수 정지한다.
- 자동화 코드는 숫자 60·70·80을 하드코딩하지 않고 `EnhancementDecisionBoundary` 데이터를 조회한다.

## 6. 정밀 강화 경계

- 정밀 게이지 위치를 RNG로 지정하지 않는다.
- `requires_precision=true`인 시도는 자동 강화가 시작하지 않는다.
- 자동 강화는 `STOP_PRECISION_INPUT_REQUIRED`를 반환하고 정밀 화면을 연다.
- 접근성 정밀 보조가 있어도 플레이어 입력을 생략하거나 PERFECT를 자동 제공하지 않는다.

## 7. 재료 경계

- 필수 보조재료가 없으면 `STOP_REQUIRED_MATERIAL_MISSING`으로 멈춘다.
- `allow_empty_secondary=true` fallback을 제품 경로에서 금지한다.
- 재료 선택이 필요한 단계는 자동으로 가장 싼 재료·가장 높은 확률 재료를 선택하지 않는다.
- 사용자가 AutoEnhancePolicy에 허용한 일반 촉매가 있고 선택이 아닌 단순 반복 단계일 때만 같은 재료를 반복 사용한다.
- 고위 정밀강화 재료와 특수 수식어 후보는 자동 선택하지 않는다.

## 8. 결과별 처리

| 결과 | 처리 |
|---|---|
| SUCCESS | 다음 경계·예산·시도 상한 검사 후 계속 |
| HOLD | `stop_on_hold`에 따라 계속 또는 정지 |
| DOWNGRADE | 기본 정지; 사용자가 시작 전에 해제한 경우에만 계속 |
| DESTROY | 즉시 영구 정지; ResultEnvelope 확인 전 다음 행동 불가 |
| SAVE_FAILED | 즉시 정지; 시도 미적용 또는 저장된 이전 상태 복구 |
| RESULT_ERROR | 즉시 정지; 동일 commitment로 복구, 재추첨 금지 |

파괴 뒤 새 장비를 생성하거나 자동화를 재개하지 않는다.

## 9. 시도 트랜잭션

각 자동 시도도 수동 강화와 동일한 저장 계약을 사용한다.

```text
정지 조건 preflight
→ AttemptIntent PREPARED 저장
→ 비용·재료 소비·저장된 RNG commitment로 결과 판정
→ 장비·자원 변화 + ResultEnvelope APPLIED 동일 revision 저장
→ ResultEnvelope를 자동 큐에 누적
→ 다음 시도 전 정책·경계·예산 재검사
```

### 결과 표시

- SUCCESS/HOLD처럼 연속 가능한 일반 결과는 하나씩 적용하되, 자동 세션 종료 시 요약 Envelope를 우선 표시할 수 있다.
- DOWNGRADE·DESTROY·정체성 선택·+50 경로·오류는 즉시 개별 ResultEnvelope를 표시한다.
- 요약은 개별 시도 결과를 숨기지 않으며 연대기·자원 변화에 링크한다.

## 10. 정지 이유

```text
TARGET_REACHED
MAX_ATTEMPTS_REACHED
MAX_GOLD_SPEND_REACHED
MINIMUM_GOLD_RESERVE_REACHED
PLAYER_CHOICE_REQUIRED
PRECISION_INPUT_REQUIRED
REQUIRED_MATERIAL_MISSING
DOWNGRADE_OCCURRED
DESTROYED
STORAGE_OR_SAVE_UNAVAILABLE
UNACKNOWLEDGED_RESULT
USER_STOPPED
INVALID_POLICY
RESULT_ERROR
```

UI는 `자동 강화가 종료됐습니다`만 표시하지 않고 실제 정지 이유와 다음 행동을 표시한다.

## 11. UI 계약

### 설정 영역

- 대상 장비
- 현재 단계 / 목표 단계
- 다음 필수 정지점
- 최대 시도
- 최대 지출 또는 최소 잔액
- HOLD·DOWNGRADE 정지 옵션
- 예상 비용 범위와 결과 위험

### 실행 중

- 현재 단계
- 완료 시도 / 최대 시도
- 누적 지출
- 남은 골드
- 마지막 결과
- 다음 정지점
- `현재 시도 후 중지`

### 종료

- 정지 이유
- 시작·종료 단계
- 성공·유지·하락 횟수
- 총 지출·소비 재료
- 장비 최종 상태
- 확인해야 할 ResultEnvelope

자동 강화는 장비 추천·목표 단계 추천·최적 재료 추천을 하지 않는다.

## 12. 기존 PoC 이전

제거·변경 대상:

```text
repeat_until_full                         제거
파괴 후 _show_auto_enhancement() 재생성   제거
session.precision_position = rng.randf()  제거
allow_empty_secondary = true              제거
자동 철검 template 생성                    제거
보관함이 찰 때까지 무제한 반복             제거
```

보존 대상:

- 사용자 중지 요청은 현재 시도 후 멈춤
- 시도 상한 안전장치
- 골드 부족·오류의 명시적 정지
- 진행 상태 표시

## 13. 테스트 매트릭스

1. +1→+4 일반 반복 성공
2. +4에서 목표 +10 요청 시 +5 진입 전 정지
3. +9에서 +10 계보 선택 전 정지
4. +19/+29/+39 선택 경계 정지
5. +49에서 경로·정밀 입력 전 정지
6. `requires_precision` 시 RNG 호출 0
7. 필수재료 없음 시 빈 fallback 0
8. 파괴 후 신규 장비 생성 0
9. 최대 시도·최대 지출·최소 잔액 정지
10. DOWNGRADE 기본 정지와 명시 해제 시 계속
11. 사용자 중지 후 현재 시도만 원자 완료
12. 저장 실패 시 다음 시도 시작 0
13. 앱 종료 후 마지막 RESOLVED 결과 재표시·재추첨 0
14. 정체성 선택 후 새 정책 없이는 자동 재개 0
15. 고객 인계·판매를 자동으로 수행하지 않음

## 14. 감사 판정

```text
BS-AUD-F06_PLANNING_TARGET: RESOLVED
LEGACY_AUTO_FORGE_MIGRATION_TARGET: RESOLVED
RUNTIME_AUTO_ENHANCE: NOT_RUN
AUTOMATED_TESTS: NOT_RUN
P0_FINDING_COUNT: 유지
```

## 15. 현재 Gate

```text
PRODUCT_NAME: 자동 강화
AUTO_NEW_EQUIPMENT_CREATION: DISALLOWED
RANDOM_PRECISION_INPUT: DISALLOWED
EMPTY_REQUIRED_MATERIAL_FALLBACK: DISALLOWED
DESTRUCTION_AUTO_RESTART: DISALLOWED
DECISION_BOUNDARY_STOP: REQUIRED
ATTEMPT_AND_SPEND_LIMIT: REQUIRED
SAVE_AND_RESULT_CONTRACT: REQUIRED
PRODUCT_CODE_CHANGE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
