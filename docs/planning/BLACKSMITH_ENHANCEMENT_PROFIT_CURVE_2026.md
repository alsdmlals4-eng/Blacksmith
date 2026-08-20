# Blacksmith 강화 수익곡선 기준 — 2026

> 상태: `CURRENT_TEST_BUDGET + HISTORICAL_NUMERIC_EVIDENCE`
>
> 최신 권위: `BS-PROGRESSION-20260820-14~17`
>
> 상세 수치 원본: `BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md`
>
> 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`

---

## 1. 현재 경제 구조

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

공방 피로도는 별도 workload 축이며 gold-equivalent에 강제 환산하지 않는다.

다음은 기본 강화 가격에 중복 포함하지 않는 별도 가치축이다.

```text
정밀제작/완성도
수식어/촉매
Chronicle/역사
특정 고객 적합도
거래 채널 프리미엄
```

## 3. 현재 성공률 Budget

```text
+1       100%
+2        97%
+3~+10    95% -> 86%
+11       82%
+12~+30   81% -> 72%
+31~+60   73% -> 69%
+61~+100  69% -> 64%
```

과거 `MASTERY 25~40%` working range는 current numeric authority가 아니다.

작품 UID + target별 recovery:

```text
+6%p / failure
soft cap 95%
```

Hard guarantee:

```text
LEARN 2 / BUILD 4 / FIRST 4 / TENSION 5 / HIGH 6 / MASTERY 7 failures
```

## 4. 현재 강화비 Budget

골드:

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)
```

일반 재료 accounting:

```text
shadow = 50G / balance unit
units = ceil(target / 20)
```

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

## 5. 승인 누적 기대원가 Anchor

20,000-run planning Monte Carlo와 독립 seed 검산을 사용했다. 후기 long-tail 때문에 raw mean은 seed마다 소폭 흔들리므로 아래 값은 **고정 planning anchor**이며, 독립 검산 허용오차는 약 `±1.5%`다.

| Level | Mean Expected Cost Anchor | P90 Reference |
|---:|---:|---:|
| +10 | 5,779 | 6,540 |
| +11 | 7,023 | 약 8,100 |
| +20 | 30,713 | 36,062 |
| +30 | 96,006 | 111,840 |
| +40 | 219,565 | 253,525 |
| +50 | 419,230 | — |
| +60 | 712,986 | 814,954 |
| +70 | 1,168,898 | — |
| +80 | 1,907,274 | 2,958,816 |
| +90 | 3,235,853 | 5,132,141 |
| +100 | 5,632,657 | 10,032,418 |

+100 planning reference:

```text
mean attempts ≈ 275~280
mean physical destruction/recraft ≈ 1.0~1.1
```

## 6. 승인 기본 공개시장 판매가 Anchor

```text
SALE_PRICE_RUNTIME != ACTUAL_PLAYER_SPEND
```

개별 플레이어의 실제 실패 횟수나 실제 지출로 판매가가 변하지 않는다. Offline Balance Lab가 expected-cost 분포를 이용해 static level table을 생성한다.

| Level | Base Market Value | Mean Expected Cost | Mean Expected Profit |
|---:|---:|---:|---:|
| +0 | 1,000 | 1,500 | -500 |
| +5 | 1,900 | 2,322 | 약 -422 |
| +9 | 4,600 | 4,759 | 약 -159 |
| +10 | **5,800** | **5,779** | **약 +21 / break-even** |
| +11 | 7,400 | 7,023 | 약 +377 |
| +20 | 34,400 | 30,713 | 약 +3,687 |
| +30 | 117,100 | 96,006 | 약 +21,094 |
| +40 | 285,400 | 219,565 | 약 +65,835 |
| +50 | 578,500 | 419,230 | 약 +159,270 |
| +60 | 1,055,200 | 712,986 | 약 +342,214 |
| +70 | 1,846,900 | 1,168,898 | 약 +678,002 |
| +80 | 3,204,200 | 1,907,274 | 약 +1,296,926 |
| +90 | 5,824,500 | 3,235,853 | 약 +2,588,647 |
| +100 | **11,265,300** | **5,632,657** | **약 +5,632,643** |

검증:

```text
+0~+9 expected profit < 0
+10 expected profit ~= 0
+11~+100 expected profit > 0
+11 이후 anchor expected profit 단조 비감소
```

## 7. 위험 프리미엄 목표

Static table 생성용 목표 margin:

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

이는 runtime cost-plus 공식이 아니다.

## 8. 과거 2026-07 수치 지위

과거 POC 가격표와 판정은 역사 증거로만 남긴다.

```text
[OLD] +5 최초 흑자
[OLD] +5~+60 평균 흑자
[OLD] +60 마지막 명시 가격 앵커
[OLD] decade success pattern
[OLD] multi-step downgrade
[OLD] destroy RNG
```

상태:

```text
HISTORICAL_NUMERIC_EVIDENCE
RECALIBRATION_INPUT
NOT_CURRENT_PRICE_CANON
DO_NOT_EXTRAPOLATE_TO_+100
```

## 9. 가치 보정 순서

1. 강화 단계 기본 market value
2. 제작 완성도/정밀제작
3. 수식어/촉매
4. 손상 상태 감액
5. Chronicle/history
6. 고객/거래 채널 배율·예산 상한

동일 요소를 기본가와 보정값에 중복 반영하지 않는다.

## 10. 현재 작업 순서

1. 일반 강화/수리 재료 실제 공급량·획득 경로·recipe mapping.
2. HIGH/MASTERY 수리 절대경제 재검증.
3. MAX 대수선 여부와 대가.
4. DESTROYED memorial/successor UX.
5. +100 비수치 payoff.
6. 첫 10분 pacing/UX/Visual 연결.
7. 정밀제작·고객/세계 payoff 연결.
8. release-near Vertical Slice 계약.

## 11. 증거 경계

- 14~16 구조: `USER_APPROVED / STRUCTURAL_CANON`.
- 17 numeric curve: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- Monte Carlo: `PLANNING_SIMULATION_EVIDENCE`.
- Runtime data: `NOT_UPDATED / BLOCKED`.
- Human/Player evidence: `NOT_RUN`.
