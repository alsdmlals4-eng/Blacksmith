# [현재 승인 테스트 Budget] Blacksmith +0~+100 강화 Balance Curve

- Parent: `BS-ENHANCE-20260820-02~13`, `BS-PROGRESSION-20260820-14~16`
- Decision: `BS-PROGRESSION-20260820-17`
- 사용자 위임/승인: `2026-08-20 KST / 성공률·강화비·판매가·누적 기대원가는 권장안대로 진행`
- 상태: `USER_APPROVED / USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`
- Simulation evidence: `20,000 Monte Carlo reference runs / planning-only model`

## 1. 목적

17은 대표 평범한 철검 기준으로 다음 네 축을 하나의 모델로 묶는다.

```text
성공률
강화 시도비
누적 기대원가
기본 공개시장 판매가
```

상위 불변식:

```text
+0~+9      = 투자 회수 전
+10        = 평균 본전 회수
+11~+100   = 기본 기대수익 양수 가능
+100       = 최대 강화
CHECKPOINT = +10 / +30 / +60 / +90
```

정밀제작·수식어·촉매·Chronicle·특수 고객/거래 채널 프리미엄은 **기본 강화 곡선과 분리**한다.

## 2. 설계 핵심 — 낮은 성공률 자체를 긴장감으로 쓰지 않는다

초기 working design의 `MASTERY 25~40%` 성공률 범위는 17에서 **대체**한다.

이유:
- 13의 MASTERY 실패 family는 실패 중 `CRITICAL 20%`.
- 09의 MASTERY MAX 흉터는 `6~15`.
- 낮은 성공률을 그대로 결합하면 +100 전에 누적 MAX 손상이 과도해져 `도전`보다 `재제작 반복`이 메인이 된다.

17의 원칙:

```text
TENSION = 실패율만이 아니라
          시도비 + DAMAGE + CRITICAL + MAX scar + 작품 가치로 만든다.
```

따라서 후반 기본 성공률을 과도하게 낮추지 않는다.

## 3. 기본 성공률 — target level 기준

정밀 수치 계산은 아래 선형 구간을 사용한다. 플레이어 UI는 필요 시 1%p 단위로 반올림 표시한다.

```text
TARGET +1       100%
TARGET +2        97%

TARGET +3~+10
95% -> 86% 선형 감소

TARGET +11
82%

TARGET +12~+30
81% -> 72% 선형 감소

TARGET +31~+60
71% -> 67% 선형 감소

TARGET +61~+100
66% -> 60% 선형 감소
```

대표 앵커:

| Target | Band | Base Success |
|---:|---|---:|
| +1 | LEARN | 100% |
| +2 | LEARN | 97% |
| +3 | BUILD | 95% |
| +10 | BUILD | 86% |
| +11 | FIRST_STOP | 82% |
| +20 | TENSION | 77% |
| +30 | TENSION | 72% |
| +31 | HIGH | 71% |
| +60 | HIGH | 67% |
| +61 | MASTERY | 66% |
| +90 | MASTERY | 약 61.5% |
| +100 | MASTERY | 60% |

이 곡선은 `BASE_SUCCESS`다. MAX 내구도 상태 페널티가 적용되면 최종 성공률이 내려갈 수 있다.

## 4. 작품 UID별 실패 회복 수치

첫 테스트:

```text
RECOVERY_SUCCESS_BONUS_PER_FAILURE = +6%p
RECOVERY_SOFT_CAP = 95%
```

회복 소유권:

```text
owner = ITEM_UID + TARGET_LEVEL
cross_item_transfer = FORBIDDEN
```

같은 target에서 실패할 때마다 +6%p가 누적된다. DOWNGRADE 때문에 다른 target을 다시 복구하더라도 원래 target의 회복 기록은 같은 작품 UID에 남는다.

확정 성공 상한:

| Band | 같은 target 연속 실패 상한 | 다음 시도 |
|---|---:|---|
| LEARN | 2 | 100% |
| BUILD | 4 | 100% |
| FIRST_STOP | 4 | 100% |
| TENSION | 5 | 100% |
| HIGH | 6 | 100% |
| MASTERY | 7 | 100% |

- 성공 시 해당 target의 회복 진전을 소비/초기화한다.
- 실패 family severity는 회복량에 따라 몰래 증가하지 않는다.
- 회복은 성공률 축만 개선한다.

## 5. 강화 시도비 — 골드

기본 일반 강화 골드는 연속 power curve를 사용한다.

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)
```

이 구조를 채택한 이유:
- 과거 decade multiplier처럼 +11/+21/+31에서 이유 없는 비용 급점프를 만들지 않는다.
- checkpoint 직전/직후 비용 최적화 메타를 줄인다.
- 고강화로 갈수록 비용은 충분히 convex하게 증가한다.

대표 골드:

| Target | Gold |
|---:|---:|
| +1 | 10 |
| +2 | 40 |
| +5 | 230 |
| +10 | 830 |
| +11 | 990 |
| +20 | 2,970 |
| +30 | 6,270 |
| +40 | 10,640 |
| +50 | 16,040 |
| +60 | 22,440 |
| +70 | 29,800 |
| +80 | 38,090 |
| +90 | 47,310 |
| +100 | 57,440 |

## 6. 강화 시도비 — 일반 재료

17은 새 화폐를 만들지 않는다.

기본 기대원가 계산에서는 기존 일반 재료 shadow accounting `50G/unit`을 재사용한다.

```text
COMMON_ENHANCEMENT_MATERIAL_SHADOW_VALUE = 50G / unit

COMMON_ENHANCEMENT_MATERIAL_UNITS(target)
= ceil(target / 20)
```

| Target | 일반 재료 수량 |
|---:|---:|
| +1~+20 | 1 |
| +21~+40 | 2 |
| +41~+60 | 3 |
| +61~+80 | 4 |
| +81~+100 | 5 |

이 `unit`은 **balance accounting bundle**이며 새 player-facing 토큰이 아니다. 실제 어떤 기존 일반 재료를 몇 개 요구할지는 공급량/획득 경로 Decision에서 매핑한다.

정밀제작·특수 촉매·수식어 재료 비용은 기본 +10 회수선과 기본 판매가에 넣지 않는다.

## 7. MASTERY CURRENT 손상 첫 계산값

누적 기대원가와 +100 생존성을 계산하기 위해 미확정이던 MASTERY CURRENT 손상량에 첫 테스트값을 둔다.

```text
MASTERY FAIL_DAMAGE          CURRENT -15~-25
MASTERY FAIL_CRITICAL_DAMAGE CURRENT -35~-60
MASTERY MAX scar             기존 09 유지: MAX -6~-15
```

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 8. 기대원가 계산 정책

대표 철검 기본 제작비:

```text
craft gold = 500
craft common material = 20 units
shadow value = 50G / unit
BASE_CRAFT_EXPECTED_COST = 1,500G-equivalent
```

누적 기대원가:

```text
EXPECTED_CUMULATIVE_RESOURCE_COST
= craft
+ enhancement attempt gold
+ enhancement ordinary material shadow cost
+ failure repetitions
+ one-step DOWNGRADE recovery attempts
+ enhancement-caused CURRENT repair gold/material
+ physical destruction -> recraft expectation
```

공방 피로도는 별도 workload 축이며 17의 gold-equivalent 값으로 강제 환산하지 않는다.

## 9. 기대원가용 기준 수리 정책

실제 플레이어에게 자동 수리를 강제하지 않는다. 17의 Monte Carlo 비교만을 위한 `REFERENCE_SAFE_REPAIR_POLICY`다.

```text
1. +11 / +31 / +61 / +91 위험 전환 진입 시
   CURRENT < MAX이면 CURRENT를 MAX까지 수리.

2. 그 외에는 다음 target의 CRITICAL CURRENT 최대 손실 이하로
   CURRENT가 내려갔을 때 수리.

3. 수리해도 MAX는 복구하지 않음.
```

수리비는 10~12의 현재 Canon을 그대로 사용한다.

## 10. 20,000-run Monte Carlo 결과 — 대표 철검

아래 값은 17의 첫 기준값이다. 실제 runtime evidence가 아니다.

| Level | 평균 누적 기대원가 | P50 | P75 | P90 | 평균 파괴/재제작 횟수 | 평균 시도 횟수 |
|---:|---:|---:|---:|---:|---:|---:|
| +10 | 5,770 | 5,610 | 6,060 | 6,530 | 0.000 | 10.8 |
| +11 | 7,039 | 6,850 | 7,410 | 8,097 | 0.000 | 12.0 |
| +20 | 30,736 | 30,138 | 32,980 | 36,080 | 0.000 | 23.5 |
| +30 | 96,163 | 94,770 | 103,160 | 112,041 | 0.000 | 37.1 |
| +40 | 223,091 | 219,890 | 239,324 | 259,170 | 0.000 | 51.7 |
| +50 | 427,991 | 423,140 | 457,396 | 492,494 | 0.000 | 66.7 |
| +60 | 728,187 | 720,715 | 775,553 | 832,155 | 0.001 | 82.0 |
| +70 | 1,189,743 | 1,148,455 | 1,239,709 | 1,341,383 | 0.033 | 101.1 |
| +80 | 1,942,055 | 1,734,387 | 1,904,978 | 2,978,285 | 0.157 | 131.0 |
| +90 | 3,276,228 | 2,552,450 | 3,972,885 | 5,191,919 | 0.457 | 184.1 |
| +100 | 5,759,280 | 4,475,112 | 6,995,326 | 10,348,306 | 1.073 | 282.7 |

해석:
- +10까지 영구 MAX 흉터가 없으므로 비용 분산이 작다.
- +60 이후 파괴/재제작 long-tail이 본격적으로 커진다.
- +100은 평균 약 1.07회의 물리 작품 파괴/재제작을 포함하는 prestige 목표다.
- +100은 첫 시도 100단계 직행을 의미하지 않으며 checkpoint와 실패 회복을 포함한 전체 작품 제작 경제다.

## 11. 기본 공개시장 판매가 — 산정 원칙

중요:

```text
SALE_PRICE_RUNTIME != actual_player_spend
```

플레이어가 실제로 많이 실패했다고 같은 강화 단계의 기본 판매가가 올라가지 않는다.

판매가는 **offline Balance Lab에서 expected cumulative cost 분포를 기준으로 미리 산정한 정적 level table**이다.

따라서:
- 실패를 일부러 많이 해서 판매가를 올릴 수 없음.
- 수리 먼저/강화 먼저 같은 작업 순서로 판매가를 조작할 수 없음.
- Chronicle/역사 가치는 별도 축에서만 반영.

## 12. 판매가 위험 프리미엄 Budget

+10 이후 reference expected-cost 대비 목표 margin:

```text
+10   0%
+11   5%
+20  12%
+30  22%
+40  30%
+50  38%
+60  48%
+70  58%
+80  68%
+90  80%
+100 100%
```

앵커 사이는 선형 margin 보간 후 offline expected cost에 적용하고 `100G` 단위로 반올림한다.

이 margin은 **runtime cost-plus pricing 공식이 아니다**. Balance table 생성용 목표다.

## 13. 승인 첫 기본 공개시장 가격 앵커

| Level | 기본 공개시장가 | 평균 기대원가 | 평균 예상 순이익 |
|---:|---:|---:|---:|
| +0 | 1,000 | 1,500 | -500 |
| +5 | 1,900 | 2,316 | 약 -416 |
| +9 | 4,600 | 4,753 | 약 -153 |
| +10 | **5,800** | **5,770** | **약 +30 / 사실상 본전** |
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

앵커가 아닌 단계의 static table은 동일 simulation snapshot + margin interpolation으로 생성한다.

검증 결과:

```text
+0~+9 expected profit < 0
+10 ~= break-even
+11~+100 expected profit > 0
+11~+100 expected profit is monotonic non-decreasing in the reference table
```

## 14. 왜 +80 이후 위험 프리미엄이 크게 커지는가

+80 이후에는 평균값만 보면 비용을 과소평가하기 쉽다.

대표 P90:

```text
+80  약 2.98M
+90  약 5.19M
+100 약 10.35M
```

승인 판매가:

```text
+80  약 3.26M
+90  약 5.90M
+100 약 11.52M
```

즉 후기 가격은 단순 공격력 배율보다 **파괴/재제작 long-tail 위험 프리미엄**을 크게 반영한다.

## 15. 5회 전체 적대 검토

### Loop 1 — 낮은 성공률이 MAX 파괴와 곱해져 +100을 사실상 막는가

공격:
- 과거 MASTERY 25~40%를 13/09 위험과 결합하면 평균 MAX 손실이 지나치게 커진다.

방어:
- MASTERY base success를 +61 66% → +100 60%로 재설정.
- 실패 자체는 여전히 DAMAGE/CRITICAL 비중이 높아 긴장은 유지.

판정: `PASS / OLD_MASTERY_SUCCESS_RANGE_SUPERSEDED`.

### Loop 2 — +10 본전이 수리·실패 비용을 숨기는가

공격:
- 성공 시도비만 더하면 실제 본전보다 낮게 계산된다.

방어:
- 20,000-run expected cumulative resource cost에 실패 반복·DOWNGRADE 복구·일반 수리·재제작을 포함.
- +10 평균 5,770 대비 static sale 5,800.

판정: `PASS`.

### Loop 3 — 비용 급점프 때문에 특정 레벨 직전 멈춤 메타가 생기는가

공격:
- decade multiplier/특수 단계 비용 급증은 `강화 전에 수리/판매` 같은 경계 메타를 만들 수 있다.

방어:
- 기본 gold cost를 `12 * target^1.84` 연속 곡선으로 단순화.
- 일반 재료만 20단위의 완만한 단계 증가.

판정: `PASS_WITH_PLAYTEST`.

### Loop 4 — unlucky player가 고강화에서 구조적으로 손해만 보는가

공격:
- 평균 가격만 맞추면 파괴 long-tail을 겪은 플레이어는 판매 자체가 무의미할 수 있다.

방어:
- +80/+90/+100 판매 앵커를 각 단계 P90 누적원가보다 높은 첫 테스트선으로 둔다.
- 그렇다고 실제 개인 지출을 판매가에 동적으로 환급하지 않는다.

판정: `PASS_WITH_MACRO_ECONOMY_REVIEW`.

### Loop 5 — +100 11.5M 판매가가 전체 경제를 무너뜨리는가

공격:
- 최고 작품 한 번 판매로 이후 모든 골드 선택이 무의미해질 수 있다.

방어:
- +100은 평균 282.7 attempts, 평균 1.07 destruction을 포함하는 prestige 목표.
- 특수 고객/거래 채널 예산·시장 유동성·후기 소비처를 후속 macro-economy에서 반드시 검증.
- +100 가격을 낮추기 전에 전체 도달 빈도와 후기 소비처를 같이 본다.

판정: `PASS_AS_BALANCE_START / MACRO_ECONOMY_REQUIRED`.

## 16. 외부 사례에서 채택하는 원리

### Diablo IV Masterworking — ADAPT
- 최신 공식 시스템은 item Quality가 올라갈수록 Masterworking 비용이 증가하고, 최대치/Capstone을 별도 가치 구간으로 둔다.
- Blacksmith는 `후기로 갈수록 convex cost`와 `최종 prestige payoff` 원리만 채택한다.
- 외부 자원명·수치·단계 수는 복사하지 않는다.

공식 참고:
- https://news.blizzard.com/en-us/article/24244466/diablo-iv-patch-notes-2-5
- https://news.blizzard.com/en-us/article/24243142/sanctuary-ignites-with-itemization-systems-changes

### Black Desert Enhancement — ADAPT / AVOID
- 공식 가이드는 실패가 다음 성공 확률 증가에 기여하고, 최대 내구도 손실이 별도 장기 리스크로 작동한다.
- Blacksmith는 실패 회복 + 영구 구조 흉터 분리 원리만 채택한다.
- MMO식 의도적 failstack 파밍과 긴 복구 노가다는 비채택한다.

공식 참고:
- https://www.kr.playblackdesert.com/ko-KR/Wiki?wikiNo=233
- https://www.kr.playblackdesert.com/ko-KR/Wiki?wikiNo=234

## 17. 재검토 조건

다음 중 하나면 17 수치를 재산정한다.

- 첫 10분에 +10 도달이 지나치게 빠르거나 느림.
- +10 판매가가 실제 플레이테스트에서 명확한 손실/과잉수익으로 체감됨.
- +11 이후 판매 기대가 약해 플레이어가 대부분 +10에서 멈춤.
- 반대로 판매가 증가가 너무 커 항상 끝까지 강화가 정답이 됨.
- HIGH/MASTERY에서 평균 수리 행동이 강화 결정보다 더 많은 시간을 차지.
- +100 평균 시도 횟수가 실제 pacing에서 과도함.
- +100 도달 작품의 MAX 상태가 지나치게 낮아 완성 보상이 훼손됨.
- +100 한 번의 매각이 전체 후기 경제를 무력화.
- 일반 강화 재료 공급이 비용 공식보다 실제 병목이 됨.

## 18. 증거/구현 경계

- 17 구조/수치: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- 20,000-run 결과: `PLANNING_SIMULATION_EVIDENCE`.
- Human/Player validation: `NOT_RUN`.
- 실제 Godot runtime/data 반영: `BLOCKED`.
- 새 `기획 완료` 사용자 선언 후 구현/Balance Lab 재실행 필요.
