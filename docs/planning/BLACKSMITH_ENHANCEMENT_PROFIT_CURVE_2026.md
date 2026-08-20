# Blacksmith 강화 수익곡선 기준 — 2026

> 상태: `CURRENT_TEST_BUDGET + HISTORICAL_NUMERIC_EVIDENCE`
>
> 최신 권위: `BS-PROGRESSION-20260820-14~17`
>
> 상세 수치 원본: `BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md`
>
> 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`

---

## 1. 최신 구조 계약

```text
+0~+9      = 투자 회수 전
+10        = 평균 누적 기대원가 회수
+11~+100   = 기본 기대수익 양수 가능
+100       = 최대 강화
```

Checkpoint:

```text
+10 / +30 / +60 / +90
```

경험 밴드:

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

## 2. 누적 기대원가 정의

```text
EXPECTED_CUMULATIVE_RESOURCE_COST
= 기본 제작
+ 강화 시도 골드
+ 일반 강화 재료 shadow cost
+ 실패 반복
+ one-step DOWNGRADE 복구
+ 강화 유발 CURRENT 수리
+ 실제 파괴/재제작 기대비용
```

공방 피로도는 별도 workload 축으로 유지하고 gold-equivalent에 강제 환산하지 않는다.

별도 가치축:

```text
정밀제작/완성도
수식어/촉매
Chronicle/역사
특정 고객 적합도
거래 채널 프리미엄
```

위 항목은 기본 강화 판매가에 중복 포함하지 않는다.

## 3. 현재 강화비 Budget

골드:

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)
```

일반 재료 accounting:

```text
shadow = 50G / unit
units = ceil(target / 20)
```

대표:

| Target | Gold | Material Unit |
|---:|---:|---:|
| +1 | 10 | 1 |
| +5 | 230 | 1 |
| +10 | 830 | 1 |
| +20 | 2,970 | 1 |
| +30 | 6,270 | 2 |
| +40 | 10,640 | 2 |
| +50 | 16,040 | 3 |
| +60 | 22,440 | 3 |
| +70 | 29,800 | 4 |
| +80 | 38,090 | 4 |
| +90 | 47,310 | 5 |
| +100 | 57,440 | 5 |

## 4. 현재 기본 성공률 Budget

```text
+1       100%
+2        97%
+3~+10    95% -> 86%
+11       82%
+12~+30   81% -> 72%
+31~+60   71% -> 67%
+61~+100  66% -> 60%
```

작품 UID + target별 recovery:

```text
+6%p / failure
soft cap 95%
```

hard guarantee:

```text
LEARN 2 / BUILD 4 / FIRST 4 / TENSION 5 / HIGH 6 / MASTERY 7 failures
```

## 5. 최신 20,000-run expected-cost evidence

대표 평범한 철검, current 10~17 planning rules, reference safe-repair policy 기준.

| Level | Mean Cost | P50 | P75 | P90 |
|---:|---:|---:|---:|---:|
| +10 | 5,770 | 5,610 | 6,060 | 6,530 |
| +11 | 7,039 | 6,850 | 7,410 | 8,097 |
| +20 | 30,736 | 30,138 | 32,980 | 36,080 |
| +30 | 96,163 | 94,770 | 103,160 | 112,041 |
| +40 | 223,091 | 219,890 | 239,324 | 259,170 |
| +50 | 427,991 | 423,140 | 457,396 | 492,494 |
| +60 | 728,187 | 720,715 | 775,553 | 832,155 |
| +70 | 1,189,743 | 1,148,455 | 1,239,709 | 1,341,383 |
| +80 | 1,942,055 | 1,734,387 | 1,904,978 | 2,978,285 |
| +90 | 3,276,228 | 2,552,450 | 3,972,885 | 5,191,919 |
| +100 | 5,759,280 | 4,475,112 | 6,995,326 | 10,348,306 |

+100 planning evidence:

```text
mean attempts ≈ 282.7
mean destruction/recraft ≈ 1.07
```

## 6. 현재 기본 공개시장 판매가 Budget

기본 판매가는 actual player spend에 동적으로 연동하지 않는다.

```text
SALE_PRICE_RUNTIME != ACTUAL_PLAYER_SPEND
```

Balance Lab에서 expected-cost 분포를 이용해 static level table을 생성한다.

첫 앵커:

| Level | Base Market Value | Mean Expected Cost | Mean Expected Profit |
|---:|---:|---:|---:|
| +0 | 1,000 | 1,500 | -500 |
| +5 | 1,900 | 2,316 | 약 -416 |
| +9 | 4,600 | 4,753 | 약 -153 |
| +10 | **5,800** | **5,770** | **약 +30 / break-even** |
| +11 | 7,400 | 7,039 | 약 +361 |
| +20 | 34,400 | 30,736 | 약 +3,664 |
| +30 | 117,300 | 96,163 | 약 +21,137 |
| +40 | 290,000 | 223,091 | 약 +66,909 |
| +50 | 590,600 | 427,991 | 약 +162,609 |
| +60 | 1,077,700 | 728,187 | 약 +349,513 |
| +70 | 1,879,800 | 1,189,743 | 약 +690,057 |
| +80 | 3,262,700 | 1,942,055 | 약 +1,320,645 |
| +90 | 5,897,200 | 3,276,228 | 약 +2,620,972 |
| +100 | **11,518,600** | **5,759,280** | **약 +5,759,320** |

검증:

```text
+0~+9 expected profit < 0
+10 expected profit ~= 0
+11~+100 expected profit > 0
reference table의 expected profit은 +11 이후 단조 비감소
```

## 7. 위험 프리미엄 목표

reference expected-cost 대비 margin target:

```text
+10 0%
+11 5%
+20 12%
+30 22%
+40 30%
+50 38%
+60 48%
+70 58%
+80 68%
+90 80%
+100 100%
```

앵커 사이는 offline margin 보간 후 static table로 저장한다.

후기 margin이 커지는 이유:
- +60 이후 physical destruction/recraft long-tail 증가.
- +80 이후 mean보다 P90 cost가 훨씬 빠르게 증가.
- 실제 개인 지출 환급이 아니라 위험을 감수한 강화 단계 자체의 시장 프리미엄.

## 8. 과거 2026-07 수치의 현재 지위

과거 POC:

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
HISTORICAL_NUMERIC_EVIDENCE
RECALIBRATION_INPUT
NOT_CURRENT_PRICE_CANON
DO_NOT_EXTRAPOLATE_TO_+100
```

폐기/대체된 과거 판정:

```text
[OLD] +5 최초 흑자
[OLD] +5~+60 전체 평균 흑자
[OLD] low MASTERY success / old destroy RNG / multi-step downgrade
```

## 9. 가치 보정 순서

기본 공개시장 가격 이후에만 별도 보정을 적용한다.

1. 강화 단계 기본 market value
2. 제작 완성도/정밀제작
3. 수식어/촉매
4. 손상 상태 감액
5. Chronicle/history
6. 고객/거래 채널 배율·예산 상한

동일 요소를 기준가와 보정값에 중복 반영하지 않는다.

## 10. 재검토 조건

- +10이 실제 Human test에서 본전선으로 느껴지지 않음.
- +11 이후에도 대부분 +10에서만 판매함.
- 반대로 최고 강화까지 누르는 것이 항상 지배전략.
- HIGH/MASTERY 수리 반복이 강화 메인 루프를 덮음.
- +100 평균 282.7 attempts가 실제 pacing에서 과도함.
- +100 sale 한 번으로 macro economy가 무력화됨.
- 실제 재료 공급이 gold curve보다 더 큰 병목이 됨.

## 11. 증거 경계

- 14~17 구조: `USER_APPROVED`.
- 17 numeric curve: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- 20,000-run: `PLANNING_SIMULATION_EVIDENCE`.
- runtime data: `NOT_UPDATED / BLOCKED`.
- Human/Player evidence: `NOT_RUN`.
