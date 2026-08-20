# 블랙스미스 강화 수익곡선 기준 — 2026

> 상태: `CURRENT_STRUCTURAL_RULES + HISTORICAL_NUMERIC_EVIDENCE`
>
> 최신 권위: `BS-PROGRESSION-20260820-14`
>
> 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`

---

## 1. 최신 구조 계약

현재 강화 경제의 상위 제약은 다음이다.

```text
+0 ~ +9     = 투자 회수 전 구간
+10         = 누적 기대원가 회수선 / BREAK_EVEN_RECOVERY_POINT
+11 ~ +100  = 기본 기대수익 양수 가능 구간
+100        = MAX_ENHANCEMENT_LEVEL
```

따라서 과거 문서의 `+5 최초 흑자` 규칙은 현재 권위가 아니다.

## 2. 본전/수익 판정

대표 평범한 작품의 기본 공개시장 기준:

```text
expected_net_profit(level)
= base_public_market_value(level)
- expected_cumulative_cost(level)
```

`expected_cumulative_cost`에는 다음을 포함한다.

- 기본 제작 골드.
- 기본 제작 일반 재료의 승인 shadow value.
- 강화 시도 골드/재료.
- 실패 반복 시도.
- 제한 DOWNGRADE 복구 시도.
- 강화 실패 때문에 발생한 일반 CURRENT 수리의 골드+일반 구조재료 기대부담.
- 해당 구간에서 실제 발생 가능한 파괴/재제작 기대비용.

포함하지 않는 별도 가치축:

- 정밀제작/완성도.
- 수식어/촉매.
- Chronicle/역사 가치.
- 고객 적합도 및 거래 채널 프리미엄.

따라서 특수 품질이나 고객 조건 때문에 +10 전에 실제 이익이 생길 수는 있지만, 그것은 `강화 단계 기본 회수선`을 변경하지 않는다.

## 3. 현재 검증 계약

후속 +0~+100 Balance Curve는 다음을 만족해야 한다.

```text
MAX_LEVEL = 100
expected_profit(+0..+9) <= break-even threshold
expected_profit(+10) ~= 0
expected_profit(+11..+100) > 0
+100 -> no further normal enhancement
```

정수 가격과 Monte Carlo 오차 때문에 +10에 정확히 0골드를 강제하지 않고 작은 허용 오차를 사용한다.

+11 이후 기대수익 증가폭·곡률은 아직 `NOT_FINAL`이다.

## 4. 기존 기본 제작비 재사용 증거

대표 철검의 과거 POC 원가 기준은 현재 재보정 입력으로 유지한다.

```text
제작 골드 = 500
일반 재료 = 20개
일반 재료 shadow value = 50 gold / unit
기본 제작 기대원가 = 1,500 gold
```

`COMMON_MATERIAL_SHADOW_VALUE=50`은 `BS-ENHANCE-20260820-12`에서도 첫 테스트값으로 재사용됐다.

이 값은 출시 최종 경제가 아니라 `RECALIBRATION_INPUT / USER_APPROVED_TEST_BUDGET`다.

## 5. 2026-07-26 공개시장 수치의 현재 지위

과거 POC는 다음 가격 앵커를 사용했다.

| 강화 단계 | 과거 공개시장 기준가 |
|---:|---:|
| +0 | 1,000 |
| +1 | 1,300 |
| +2 | 1,550 |
| +3 | 1,800 |
| +4 | 2,200 |
| +5 | 3,000 |
| +10 | 5,000 |
| +15 | 8,500 |
| +20 | 14,000 |
| +25 | 24,000 |
| +30 | 42,000 |
| +35 | 72,000 |
| +40 | 125,000 |
| +45 | 220,000 |
| +50 | 400,000 |
| +55 | 750,000 |
| +60 | 1,500,000 |

상태:

```text
HISTORICAL_NUMERIC_EVIDENCE / RECALIBRATION_INPUT
NOT_CURRENT_PRICE_CANON
DO_NOT_EXTRAPOLATE_TO_+100
```

특히 과거 다음 판정은 폐기/대체됐다.

```text
[OLD] +5 = 최초 양의 기대수익
[OLD] +5~+60 모든 단계 평균 흑자
```

최신 판정은 14를 따른다.

```text
[CURRENT] +10 = 본전 회수
[CURRENT] +11~+100 = 기본 수익 가능
[CURRENT] +100 = 최대 강화
```

## 6. 가치 보정 적용 순서

기본 강화 가격은 강화 단계 자체 가치만 책임진다.

최종 거래 가치 후보 순서:

1. 강화 단계 기본 공개시장 가치
2. 제작 완성도·피버 가치 보정
3. 정밀 등급·수식어 가치 보정
4. 손상 상태 감액
5. 역사 가치 보정
6. 거래 채널 배율과 예산 상한

동일 요소를 기준가와 보정치에 중복 적용하지 않는다.

과거 거래 채널 배율 수치는 `HISTORICAL_EVIDENCE / RETUNE_REQUIRED`다.

## 7. 다음 재산정 작업

다음 Balance Decision에서 +0~+100 전체를 다시 계산한다.

필수 입력:

- 승인된 경험 밴드와 failure family 비율.
- 단계별 성공률/실패 누적 회복.
- CURRENT/MAX 손상과 수리 경제.
- 강화 골드/재료 비용.
- 체크포인트/단계 하락 구조.

필수 출력:

- 평균/P50/P75/P90 누적원가.
- 단계별 기본 공개시장가.
- 단계별 expected net profit.
- +10 break-even 검증.
- +11 이후 profit curve.
- +100 도달 기대비용/시간과 경제 충격.

## 8. 범위와 증거 경계

- `+10 본전 / +11 이후 수익 가능 / +100 최대`: `USER_APPROVED`.
- 과거 +0~+60 가격표: `HISTORICAL_NUMERIC_EVIDENCE`.
- 새 +0~+100 가격표: `NOT_STARTED / NOT_FINAL`.
- Runtime data 변경: `BLOCKED`.
- Human/Player validation: `NOT_RUN`.
