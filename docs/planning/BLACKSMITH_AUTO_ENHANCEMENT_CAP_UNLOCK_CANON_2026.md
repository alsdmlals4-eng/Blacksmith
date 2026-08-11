# Blacksmith Auto Enhancement Cap Unlock Canon — 2026

- Decision: `BS-CORE-20260811-01`
- System: `AUTO_ENHANCEMENT_CAP_UNLOCK`
- 상태: `USER_APPROVED_DIRECTION / PLANNING_ONLY`
- 기존 저위험 연속강화 권위: `BLACKSMITH_DECISION_LEDGER_ADDENDUM_07`
- 분야별 돌파 권위: `BLACKSMITH_GROWTH_SYSTEM_ADDENDUM_02`
- 강화 위험·확률 권위: `BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`

```text
BREAKTHROUGH_AUTHORITY: BLACKSMITH_GROWTH_SYSTEM_ADDENDUM_02
RISK_PROBABILITY_AUTHORITY: BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026
```

이 문서는 새 성공률 표나 새 돌파 비용을 소유하지 않는다. 기존 강화·돌파 책임 원본을 소비해 **이미 수동으로 숙련한 구간의 반복 입력만 줄이는 자동화 상한**을 정의한다.

## 1. 사용자 방향

중·후반 진행에서 과거의 저강화 구간이 반복 노가다가 되지 않도록 플레이어가 목표 강화 수치를 지정하면 그 수치까지 자동 강화를 진행할 수 있다. 자동으로 갈 수 있는 최대 수치는 성장에 따라 해금된다.

핵심 원칙은 다음과 같다.

> 먼저 수동으로 새로운 강화 구간을 정복하고, 그보다 낮은 과거 구간을 자동화한다.

즉 자동화는 현재 최고 도전 구간을 대신하지 않는다.

## 2. 기존 +20 연속강화 보존

기존 승인 규칙을 그대로 보존한다.

```text
15 manual attempts → AUTO_CAP +20
```

- 기존 표현의 `수동 강화 15회 뒤 해금`을 유지한다.
- 기존 초기 범위 `+1~+20`을 유지한다.
- 초기 저위험 연속강화의 요청 최대 10회와 기존 정지 규칙을 대체하지 않는다.
- 고위험 자동 강화와 정밀강화 자동 처리가 `REJECTED`인 기존 경계를 유지한다.

## 3. 중·후반 자동 상한 성장

분야별 기술 돌파가 이미 계정·분야별 영구 해금으로 존재하므로 자동 강화 상한도 같은 분야 소유권을 따른다.

```text
+40 breakthrough complete → AUTO_CAP +30
+50 breakthrough complete → AUTO_CAP +40
+60 breakthrough complete → AUTO_CAP +50
+70 breakthrough complete → AUTO_CAP +60
+80 breakthrough complete → AUTO_CAP +70
+90 breakthrough complete → AUTO_CAP +80
+100 frontier → 별도 후속 Decision 전 자동 상한 추가 승격 없음
```

구조식:

```text
AUTO_CAP = highest completed category breakthrough - 10
```

단, 초반의 기존 `15 manual attempts → AUTO_CAP +20`은 별도 early-game exception으로 유지한다.

```text
CATEGORY_SPECIFIC_AUTO_CAP
PLAYER_SELECTED_TARGET_REQUIRED
TARGET_ENHANCEMENT <= AUTO_CAP
```

자동 상한은 **해당 장비 분야별**이다. 무기 돌파가 방어구 자동 상한을 올리지 않는다.

## 4. 목표 지정

플레이어는 현재 강화보다 높은 목표값을 직접 지정한다.

검증 순서:

1. `TARGET_ENHANCEMENT > CURRENT_ENHANCEMENT`
2. `TARGET_ENHANCEMENT <= CATEGORY_AUTO_CAP`
3. 다음 시도가 현재 장비의 정상 강화 eligibility를 만족하는가
4. 수동 판단 전용 이정표를 자동으로 넘어가지 않는가
5. 다음 시도에 필요한 자원이 존재하는가

UI는 최소한 현재 강화, 목표 강화, 현재 해금 자동 상한, 현재 위험도, 다음 시도 비용, 이미 예측 가능한 정지 이유를 보여줘야 한다.

## 5. 자동 시도는 정상 강화의 반복 실행

자동 강화는 별도 확률 시스템이 아니다.

```text
NO_HIDDEN_SUCCESS_RATE_BONUS
NO_RESOURCE_OR_FATIGUE_BYPASS
PER_ATTEMPT_UID_HISTORY_PRESERVED
```

각 자동 시도는 반드시:

- 동일 단계의 수동 강화와 같은 자연 성공·실패 확률을 사용한다.
- 동일한 골드·재료·보호 자원을 소비한다.
- 현재 책임 원본이 강화에 작업량·피로도 기회비용을 부여하면 동일하게 소비한다.
- 같은 UID에 정상 강화 시도 이력을 남긴다.
- 대성공·성공·유지·1단계 하락·2단계 하락·파괴 및 보호 변환을 기존 책임 원본에 그대로 위임한다.
- 자동이라는 이유로 할인·확률 보너스·무료 보호·무료 복원을 주지 않는다.

## 6. 자동 정지 규칙

다음 조건에서는 즉시 자동 진행을 끝내고 플레이어에게 제어를 돌려준다.

- 목표 강화 도달
- 다음 시도 자원 부족
- 다음 시도가 자동 상한 초과
- 정밀강화 대기 지점에서 자동 진행을 멈춘다
- 기술 돌파 대기 지점에서 자동 진행을 멈춘다
- 다음 시도가 `HIGH / VERY_HIGH` 위험
- 실제 단계 하락이 발생하면 그 시도 해결 후 즉시 정지
- 보호 파괴 결과가 발생하면 그 시도 해결 후 즉시 정지
- 촉매·정밀강화 방식·특수 위험·영구 결과 등 별도 수동 선택이 필요함
- 장비가 더 이상 정상 강화 eligibility를 만족하지 않음

`유지` 결과만 발생했고 다음 시도가 계속 자동 eligibility를 만족하면 진행을 이어갈 수 있다.

## 7. 수동 전용 경계

```text
AUTO_HIGH_RISK: false
AUTO_VERY_HIGH_RISK: false
AUTO_PRECISION_ENHANCEMENT: false
AUTO_TECHNICAL_BREAKTHROUGH: false
```

다음은 자동 상한 이하더라도 수동으로 처리한다.

- `HIGH / VERY_HIGH` 강화
- 정밀강화 선택·시작
- 분야별 기술 돌파
- 작품 정체성·특수기능을 바꾸는 고위 선택
- 현재 규칙에서 영구 위험 확인을 요구하는 행동

따라서 플레이어의 최신 frontier는 계속 직접 도전하는 구간으로 남는다.

## 8. MODERATE 위험과 보호

초기 +20 저위험 자동 강화는 기존 `VERY_LOW / LOW` 경계를 유지한다. 중반 자동 상한이 올라가면서 `MODERATE` 구간이 자동 후보가 될 경우에도 무보호 영구 파괴는 자동으로 허용하지 않는다.

```text
NO_UNPROTECTED_AUTO_DESTRUCTION
```

자동 후보 단계에서 무보호 파괴 결과가 가능하다면:

- 해당 자동 실행에 사용할 유효 보호 모드를 플레이어가 사전에 명시적으로 선택해야 한다.
- 다음 시도에 필요한 보호 자원이 있어야 한다.
- 보호 자원은 시도마다 정상 소비한다.
- 보호가 부족해지는 순간 다음 위험 시도 전에 자동을 중지한다.
- 보호 파괴가 실제 발생하면 결과 적용 뒤 자동을 중지한다.

이 규칙은 보호석의 기존 자연 결과 변환과 비용을 변경하지 않는다.

## 9. Marek 소량 주문과의 결합

`BS-CONTENT-20260811-03 / SOLDIER_01 / MAREK_OLDEN`의 저강화 소량 주문은 **이미 계정에서 해금된 자동 범위**를 편의 기능으로 사용할 수 있다.

그러나:

- Marek 주문이 자동 상한을 해금하지 않는다.
- 여러 UID에 같은 목표를 지정해도 각 UID는 독립적으로 판정한다.
- 각 UID마다 비용·시도 횟수·결과·연대기 이벤트를 개별 기록한다.
- 한 UID의 실패·정지 결과가 다른 UID의 결과를 덮어쓰지 않는다.
- batch UI는 요약할 수 있지만 item UID를 stack 하나로 합치지 않는다.

## 10. 벤치마킹 판정

### V4 공식 강화 가이드

- `ADAPT`: 목표 강화 단계 지정, 자동 진행, 안전·파괴 위험의 명시적 표시, 목표 전 중지 가능.
- `REJECT`: Blacksmith를 수십 개 장비의 산업형 일괄 강화 게임으로 확장.

### Uncharted Waters Origin 2026-07 Director's Letter

- `ADAPT`: 장기 진행에서 목표 강화 수치를 지정하고 반복 강화를 자동화하는 QoL 원칙.
- `REJECT`: Blacksmith와 무관한 다른 성장축의 즉시 완료 구조를 그대로 가져오기.

### Black Desert Mobile Ancient Anvil

- `ADAPT`: 오래 지속되는 강화 부담에는 체계적인 friction relief가 필요하다는 문제 인식.
- `REJECT`: `ANCIENT_ANVIL_GAUGE`, `PITY_GAUGE`, 신규 보장 성공 경제를 Blacksmith에 도입.

### Google Play quality guidance

- `ADOPT`: 성장 진행을 인정하면서 직관적이고 끊김 없는 조작을 제공한다.

### DIFFERENTIATOR

Blacksmith의 자동화는 **수동 숙련을 먼저 요구하고 현재 frontier보다 뒤에서만 따라오며**, 작품 UID·위험·비용·실패 이력을 지우지 않는다.

## 11. 적대적 보호 경계

```text
NO_AUTO_ENHANCEMENT_AT_OR_BEYOND_MANUAL_FRONTIER
NO_HIGH_OR_VERY_HIGH_RISK_AUTO
NO_AUTO_PRECISION_ENHANCEMENT
NO_AUTO_TECHNICAL_BREAKTHROUGH
NO_HIDDEN_SUCCESS_RATE_BONUS
NO_RESOURCE_OR_FATIGUE_BYPASS
NO_UNPROTECTED_AUTO_DESTRUCTION
PER_ATTEMPT_UID_HISTORY_PRESERVED
CATEGORY_SPECIFIC_AUTO_CAP
PLAYER_SELECTED_TARGET_REQUIRED
PRODUCT_IMPLEMENTATION_BLOCKED
TASK3_IMPLEMENTATION_NOT_APPROVED
```

`ANCIENT_ANVIL_GAUGE`와 `PITY_GAUGE`는 이 Decision의 일부가 아니다.

## 12. 적대 검토 판정

1. 자동 상한이 결국 메인 루프 전체를 자동화할 위험 → `MUST_FIX`: 수동 frontier보다 최소 한 10강 밴드 뒤 유지.
2. 한 분야 숙련이 다른 분야 자동화를 해금할 위험 → `MUST_FIX`: category-specific ownership.
3. 자동으로 고가 자원을 무한 소비하거나 작품을 파괴할 위험 → `MUST_FIX`: 목표·상한·자원·위험·보호 정지 규칙과 무보호 자동 파괴 금지.
4. Marek 배치에서 작품이 익명 stack이 될 위험 → `MUST_FIX`: per-UID 독립 판정·비용·이력 유지.
5. 벤치마크에서 pity 경제를 가져올 위험 → `REJECTED_IMPORT`: 기존 확률·보호 책임 원본만 사용.

## 13. 검증 상태

- 사람 플레이테스트: `NOT_RUN`
- Android 실기기: `NOT_RUN`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`

후속 사람 검증에서는 플레이어가 자동화가 **과거 반복을 줄이는 기능**이고 현재 최고 위험 판단을 대신하지 않는다는 점을 이해하는지 관찰한다.
