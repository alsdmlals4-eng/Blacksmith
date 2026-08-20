# [현재 승인] Blacksmith 강화 진행·경제 기준

- Parent: `BS-CORE-20260820-01`, `BS-ENHANCE-20260820-05~13`
- Decision: `BS-PROGRESSION-20260820-14`
- 사용자 결정: `2026-08-20 KST / +10 본전 회수, 이후 수익 실현 가능, +100 최대 강화`
- 상태: `USER_APPROVED / STRUCTURAL_CANON / NUMERIC_CURVE_NOT_FINAL`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 강화 범위

```text
MIN_ENHANCEMENT_LEVEL = +0
MAX_ENHANCEMENT_LEVEL = +100
```

- `+100` 성공 상태가 현재 계획의 최대 강화다.
- 기본 강화 시스템에는 `+101` 이상을 두지 않는다.
- 프레스티지/초월/리셋형 무한 강화는 별도 사용자 승인 없이는 추가하지 않는다.
- +100 이후의 다음 질문은 더 높은 숫자가 아니라 `보유 / 판매 / 고객·세계 인계 / 기록 / 후속 작품` 쪽으로 넘긴다.

## 2. 경제 전환점

대표 기준 작품의 기본 공개시장 경제는 다음 구조를 따른다.

```text
+0 ~ +9   = INVESTMENT_RECOVERY_ZONE
+10       = BREAK_EVEN_RECOVERY_POINT
+11 ~ +100 = PROFITABLE_ENHANCEMENT_ZONE
```

### +10

`+10`은 강화 누적 기대원가를 회수하는 첫 경제 이정표다.

```text
EXPECTED_NET_PROFIT(+10) ≈ 0
```

정수 반올림·시뮬레이션 오차 때문에 정확히 0골드 한 점을 강제하지 않고, 실제 Balance Lab에서는 작은 허용 오차 밴드를 사용한다.

### +11 이후

기본 공개시장 기준에서는 +11부터 양의 기대수익을 만들 수 있어야 한다.

```text
EXPECTED_NET_PROFIT(level) > 0
for level >= +11
```

출시 최종 곡선에서는 +11 이후 기대수익이 장기적으로 성장해야 하지만, 정확한 단계별 증가폭·곡률은 후속 Balance Decision에서 정한다.

## 3. `본전`의 계산 경계

`+10 본전`은 단순히 제작비 1회만 비교하지 않는다.

대표 작품의 누적 기대원가에는 다음을 포함한다.

- 기본 제작 골드.
- 기본 제작 일반 재료의 승인 shadow value.
- +10까지의 강화 시도 골드/재료.
- 실패로 발생한 반복 시도.
- 체크포인트 위 제한 DOWNGRADE의 복구 시도.
- 강화 실패 때문에 실제로 발생한 일반 CURRENT 수리의 골드 + 일반 구조재료 기대부담.
- 현재 승인된 실패 누적 회복/성공률 구조가 반영된 평균 시도 횟수.

해당 구간에서 발생 가능할 경우에는 승인된 파괴/재제작 기대비용도 포함한다. 첫 안전 구간에서 실제 파괴가 0이면 항목 값은 0이다.

```text
EXPECTED_CUMULATIVE_COST(+10)
= craft
+ enhancement attempts
+ failure repetitions
+ downgrade recovery
+ enhancement-caused repair burden
+ destruction/recraft expectation if applicable
```

## 4. 회수선에서 제외되는 별도 가치 축

다음은 `+10 기본 강화 회수선`을 계산할 때 기본 강화 단계 가치에 중복 포함하지 않는다.

- 정밀제작/완성도 프리미엄.
- 수식어·촉매 프리미엄.
- Chronicle/역사 가치.
- 특정 고객 적합도.
- 군사 보급·밀수·수집가 등 거래 채널 프리미엄.
- 이벤트성 추가 보상.

따라서 개별 작품이 +10 이전에도 특수 품질/고객 조건으로 실제 이익을 낼 수는 있다. 그것은 **강화 단계 자체의 기본 회수선이 앞당겨진 것**으로 해석하지 않는다.

## 5. +10의 게임 디자인 역할

+10은 단순 숫자 이정표가 아니라 세 가지 역할을 가진다.

1. **경제:** 지금 팔면 평균적으로 투자금을 회수할 수 있다.
2. **심리:** 처음으로 `여기서 멈춰도 손해는 아니다`가 성립한다.
3. **강화 DDD:** +11부터는 수익을 얻을 가능성과 더 큰 실패 리스크가 정면 충돌한다.

따라서 +10은 `FIRST_ECONOMIC_STOP_POINT`다.

다만 `FIRST_STOP_POINT` 경험 밴드의 정확 레벨 매핑과 체크포인트 floor를 +10 하나로 동일시할지는 다음 레벨-밴드 매핑 Decision에서 확정한다.

## 6. +100의 게임 디자인 역할

+100은 최종 숫자만 큰 종착점으로 만들지 않는다.

후속 기획에서 다음 중 최소 하나 이상의 비수치 payoff가 연결되어야 한다.

- 작품명/등급/외형의 명확한 최고 단계 표현.
- 같은 UID의 완성 기록/연대기.
- 최고급 고객·세계 사건 접근.
- 특별 인계/전시/기념 가치.
- 다음 작품을 시작할 이유.

정확 보상은 아직 미확정이다.

## 7. 기존 July 수익곡선과의 충돌 처리

과거 `BLACKSMITH_ENHANCEMENT_PROFIT_CURVE_2026.md`에는 다음이 있었다.

```text
+5 = 최초 양의 기대수익
+60 = 마지막 명시 가격 앵커
```

이는 최신 사용자 결정과 충돌한다.

현재 권위:

```text
+10 = BREAK_EVEN_RECOVERY_POINT
+11 = first positive baseline-profit eligible level
+100 = MAX_ENHANCEMENT_LEVEL
```

기존 +0~+60 공개시장 숫자는 **HISTORICAL_NUMERIC_EVIDENCE / RECALIBRATION_INPUT**으로만 사용한다. 그대로 +100까지 외삽하지 않는다.

## 8. 다음 Balance Curve가 반드시 만족할 계약

후속 `+0~+100` 가격/비용 시뮬레이션은 최소 다음을 검사한다.

```text
1. max_level == 100
2. expected_profit(+0..+9) <= break-even threshold
3. expected_profit(+10) ~= 0
4. expected_profit(+11..+100) > 0
5. +100 cannot enhance further
6. repair/downgrade/failure recovery costs are included once, not double-counted
7. quality/affix/history/customer premium is not double-counted in base enhancement value
```

권장 후속 가드레일(아직 출시 수치 정본 아님):
- +11 이후 기대수익은 장기적으로 증가.
- 단일 성공으로 경제 전체가 붕괴하지 않도록 후기 수익 증가율과 재투자 소비처를 함께 검증.
- +100 도달이 일반 첫 플레이 완료에 필수인 구조를 피함.

## 9. 5회 적대적 검토

### Loop 1 — +10 전 판매가 무의미해지는가
공격:
- +0~+9가 평균 손실이면 플레이어가 이 구간 작품을 절대 인계하지 않을 수 있다.

방어:
- +0~+9는 기본 강화 경제 기준에서 투자 회수 전이지만, 고객 필요·품질·현금흐름·작업 슬롯 회전 등 별도 이유로 판매/인계가 가능하다.
- 정밀제작·고객 프리미엄은 별도 축으로 유지한다.

판정: `PASS_WITH_ECONOMY_DESIGN`.

### Loop 2 — +10에서 모두 팔고 +11을 안 누르는가
공격:
- 본전 회수 지점이 너무 명확하면 +10 판매가 자동 정답이 될 수 있다.

방어:
- +11부터 기본 기대수익이 양수로 전환되고, 강화의 핵심 재미가 `안전하게 회수 vs 수익을 위해 더 밀기`가 된다.
- +11 이후 보상 증가와 위험 증가는 함께 설계한다.

판정: `PASS / CORE_FIT`.

### Loop 3 — +100이 90단계 반복 노동이 되는가
공격:
- +10 이후 +100까지 90단계를 같은 리듬으로 반복하면 DDD가 아니라 장기 클릭 노동이 된다.

방어:
- 정확 레벨-밴드/체크포인트/보상 밀도는 별도 설계한다.
- MASTERY는 선택적 후기 목표이며 첫 세션/기본 완주 필수로 만들지 않는다.
- +100에는 비수치 payoff를 요구한다.

판정: `PASS_WITH_FUTURE_LEVEL_MAP_GATE`.

### Loop 4 — 과거 +60 가격을 그대로 늘려 경제가 폭발하는가
공격:
- July 곡선은 +60에 이미 큰 값이 있어 단순 외삽하면 +100이 비정상적으로 커질 수 있다.

방어:
- 과거 +0~+60 숫자를 역사/재보정 입력으로 강등한다.
- 새 +0~+100 곡선은 실패·수리·내구도·회복 계약을 포함해 처음부터 다시 시뮬레이션한다.

판정: `PASS`.

### Loop 5 — +10 회수선에 다른 가치축이 중복되는가
공격:
- 품질/수식어/연대기/특수 고객까지 +10 기본 가격에 포함하면 이후 같은 요소를 거래 배율로 또 보상할 수 있다.

방어:
- +10 회수선은 대표 평범한 작품의 **강화 단계 기본 가치**만 책임진다.
- 별도 가치축은 기존 적용 순서에서 한 번만 추가한다.

판정: `PASS`.

## 10. 외부 벤치마크 원리

- 강화 시스템은 초기 안전/완화 구간과 후기 위험 구간을 분리하는 것이 장기 사다리를 읽기 쉽게 만든다.
- 실패 비용이 재료 부족과 반복 노동으로만 누적되면 progression frustration이 커질 수 있으므로 실패 회복·공급·리스크를 함께 설계한다.
- Blacksmith는 외부 게임의 단계 수나 확률을 복사하지 않고, `+10 회수 → +11 이후 이익과 위험 → +100 선택적 최고 목표`라는 자체 경제 서사를 사용한다.

## 11. 미확정 / 다음 Decision

다음은 14가 고정하지 않는다.

- +0~+100 세부 레벨→경험 밴드 매핑.
- 체크포인트 최종 간격.
- +11~+100 단계별 판매가/누적 기대원가.
- 단계별 성공률.
- 단계별 강화 골드/재료 비용.
- +100 최종 비수치 보상.
- 후기 HIGH_STAKES/MASTERY 수리 경제 스케일.

## 12. 증거 경계

- `+10 본전`, `+100 최대`, `+11 이후 기본 수익 가능`: `USER_APPROVED`.
- 정확 가격/성공률/비용 곡선: `NOT_FINAL / FOLLOW_UP_BALANCE_DECISION_REQUIRED`.
- Runtime implementation: `BLOCKED`.
- Human/Player validation: `NOT_RUN`.
