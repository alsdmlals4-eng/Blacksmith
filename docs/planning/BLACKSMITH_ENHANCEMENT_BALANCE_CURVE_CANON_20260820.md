# [현재 승인 테스트 Budget] Blacksmith +0~+100 강화 Balance Curve

- Parent: `BS-ENHANCE-20260820-02~13`, `BS-PROGRESSION-20260820-14~16`
- Decision: `BS-PROGRESSION-20260820-17`
- 사용자 위임/승인: `2026-08-20 KST / 성공률·강화비·판매가·누적 기대원가는 권장안대로 진행`
- 상태: `USER_APPROVED / USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`
- Simulation evidence: `20,000-run planning Monte Carlo + independent seed reproduction`

## 1. 목적

대표 평범한 철검 기준으로 다음 네 축을 하나의 Balance Model로 묶는다.

```text
성공률
강화 시도비
누적 기대원가
기본 공개시장 판매가
```

상위 불변식:

```text
+0~+9       = 투자 회수 전
+10         = 평균 본전 회수
+11~+100    = 기본 기대수익 양수 가능
+100        = 최대 강화
CHECKPOINTS = [10, 30, 60, 90]
```

정밀제작·수식어·촉매·Chronicle·특수 고객/거래 채널 프리미엄은 기본 강화 곡선과 분리한다.

## 2. 핵심 교정 — 극저확률을 긴장감의 주수단으로 쓰지 않는다

과거 working design의 `MASTERY 25~40%` 성공률 범위는 current authority가 아니다.

이유:
- MASTERY 실패 중 `CRITICAL 20%`.
- CRITICAL은 MAX 구조 흉터 `6~15`와 결합.
- CURRENT 일반/심각 손상도 존재.
- 성공률까지 극단적으로 낮추면 강화보다 파괴·재제작 반복이 메인이 된다.

따라서 17은 다음을 채택한다.

```text
TENSION
= 낮은 성공률 하나가 아니라
  시도비 + DAMAGE + CRITICAL + MAX scar + 누적 작품가치
```

## 3. 기본 성공률 — target level 기준

```text
TARGET +1       = 100%
TARGET +2       = 97%
TARGET +3~+10   = 95% -> 86% 선형 감소
TARGET +11      = 82%
TARGET +12~+30  = 81% -> 72% 선형 감소
TARGET +31~+60  = 73% -> 69% 선형 감소
TARGET +61~+100 = 69% -> 64% 선형 감소
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
| +31 | HIGH | 73% |
| +60 | HIGH | 69% |
| +61 | MASTERY | 69% |
| +90 | MASTERY | 약 65.3% |
| +100 | MASTERY | 64% |

이 수치는 `BASE_SUCCESS`다. MAX 내구도 상태 페널티가 최종 성공 기대에 추가 적용된다.

현재 MAX 페널티:

```text
MAX 81~100:  0pp
MAX 61~80 : -3pp
MAX 41~60 : -6pp
MAX 21~40 : -10pp
MAX 1~20  : -15pp
```

## 4. 작품 UID별 실패 회복

```text
RECOVERY_SUCCESS_BONUS_PER_FAILURE = +6%p
RECOVERY_SOFT_CAP = 95%
owner = ITEM_UID + TARGET_LEVEL
cross_item_transfer = FORBIDDEN
```

같은 target 실패 시 회복이 누적된다. DOWNGRADE로 이전 단계를 복구하는 동안에도 원래 target의 recovery는 같은 작품 UID에 남는다.

Hard guarantee:

| Band | 같은 target 실패 상한 | 다음 시도 |
|---|---:|---:|
| LEARN | 2 | 100% |
| BUILD | 4 | 100% |
| FIRST_STOP | 4 | 100% |
| TENSION | 5 | 100% |
| HIGH | 6 | 100% |
| MASTERY | 7 | 100% |

- 성공 시 해당 target recovery는 소비/초기화.
- recovery가 높아졌다고 failure family severity를 몰래 올리지 않는다.
- guarantee 시도는 실제 100% 성공으로 처리한다.

## 5. 강화 시도비 — 골드

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)
```

대표값:

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

이 곡선은 checkpoint 직전/직후에 인위적인 decade jump를 만들지 않는다.

## 6. 강화 시도비 — 일반 재료

새 화폐를 만들지 않는다.

```text
COMMON_ENHANCEMENT_MATERIAL_SHADOW_VALUE = 50G / balance unit
COMMON_ENHANCEMENT_MATERIAL_UNITS(target) = ceil(target / 20)
```

| Target | Balance Unit |
|---:|---:|
| +1~+20 | 1 |
| +21~+40 | 2 |
| +41~+60 | 3 |
| +61~+80 | 4 |
| +81~+100 | 5 |

`balance unit`은 새 player-facing token이 아니다. 실제 existing ordinary material recipe/공급량 매핑은 다음 Resource Supply Decision이 소유한다.

## 7. MASTERY CURRENT 손상 첫 Budget

17 계산에 필요한 첫 테스트값:

```text
MASTERY FAIL_DAMAGE
CURRENT -15~-25

MASTERY FAIL_CRITICAL_DAMAGE
CURRENT -35~-60

MASTERY MAX scar
MAX -6~-15  # BS-ENHANCE-09 유지
```

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 8. 누적 기대원가 계산 경계

대표 철검 기본 제작비:

```text
craft gold = 500
craft ordinary material = 20 units
shadow value = 50G/unit
BASE_CRAFT_EXPECTED_COST = 1,500G-equivalent
```

누적 기대원가:

```text
EXPECTED_CUMULATIVE_RESOURCE_COST
= craft
+ enhancement attempt gold
+ ordinary enhancement material shadow cost
+ failure repetitions
+ one-step DOWNGRADE recovery attempts
+ enhancement-caused CURRENT repair gold/material
+ physical destruction -> recraft expectation
```

공방 피로도는 별도 workload 축이며 gold-equivalent에 강제 환산하지 않는다.

## 9. Planning simulation의 기준 수리 정책

실제 플레이어에게 자동 수리를 강제하지 않는다. 비교 시뮬레이션에서만 사용하는 `REFERENCE_SAFE_REPAIR_POLICY`다.

```text
1. +11 / +31 / +61 / +91 위험 전환 전에 CURRENT < MAX이면 수리.
2. 그 외에는 다음 target의 CRITICAL CURRENT 최대손실 이하로 CURRENT가 내려가면 수리.
3. 수리는 CURRENT -> MAX만 수행하며 MAX는 복구하지 않는다.
```

수리비는 10~12 current Canon을 그대로 사용한다.

## 10. 20,000-run 검증 결과와 Canon anchor

Monte Carlo raw mean은 seed마다 후기 long-tail 때문에 소폭 흔들린다. 독립 seed 재검산은 승인 anchor를 약 `±1.5%` 범위에서 재현했다.

따라서:

```text
RAW_SIMULATION_MEAN != RUNTIME_PRICE
CANON_EXPECTED_COST_ANCHOR = 승인된 고정 planning anchor
```

승인 anchor:

| Level | Mean Expected Cost Anchor | P90 Reference | Mean Attempts Reference |
|---:|---:|---:|---:|
| +10 | 5,779 | 6,540 | 10.9 |
| +20 | 30,713 | 36,062 | 23.6 |
| +30 | 96,006 | 111,840 | 37.2 |
| +40 | 219,565 | 253,525 | 51.4 |
| +50 | 419,230 | — | 약 65.9 |
| +60 | 712,986 | 814,954 | 80.9 |
| +70 | 1,168,898 | — | 약 99.9 |
| +80 | 1,907,274 | 2,958,816 | 129.1 |
| +90 | 3,235,853 | 5,132,141 | 181.9 |
| +100 | 5,632,657 | 10,032,418 | 275.6 |

+100 reference:

```text
mean physical destruction/recraft ≈ 1.0~1.1
mean surviving MAX durability ≈ high-50s / low-60s
```

이는 runtime/human evidence가 아니라 planning simulation evidence다.

## 11. 기본 공개시장 판매가 산정 원칙

중요:

```text
SALE_PRICE_RUNTIME != ACTUAL_PLAYER_SPEND
```

개별 플레이어가 실제로 많이 실패했다고 판매가가 올라가지 않는다.

기본 시장가는 offline Balance Lab에서 expected-cost 분포를 이용해 **정적 level table**로 생성·검수한다.

따라서:
- 고의 실패로 판매가 상승 불가.
- 수리/강화 순서로 판매가 조작 불가.
- Chronicle/history는 별도 가치축.

## 12. 위험 프리미엄 목표

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

이는 runtime cost-plus 공식이 아니다. Static price table을 생성하기 위한 Balance target이다.

## 13. 승인 기본 공개시장 가격 Anchor

| Level | Base Market Value | Mean Expected Cost | Mean Expected Profit |
|---:|---:|---:|---:|
| +0 | 1,000 | 1,500 | -500 |
| +5 | 1,900 | 2,322 | 약 -422 |
| +9 | 4,600 | 4,759 | 약 -159 |
| +10 | **5,800** | **5,779** | **약 +21 / 사실상 본전** |
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

검증 계약:

```text
+0~+9 expected profit < 0
+10 expected profit ~= 0
+11~+100 expected profit > 0
+11 이후 anchor expected profit은 단조 비감소
```

앵커 사이 값은 후속 Balance Lab에서 보간·검증하되 위 구조를 깨지 않는다.

## 14. 5회 전체 적대 검토 결론

### Loop 1 — 저확률이 강화 시간을 부풀리는가
- MASTERY 25~40% old range 폐기.
- 후기 base 69% -> 64%로 유지.
- 긴장감은 실패 severity와 작품 가치에서 확보.
- `PASS`.

### Loop 2 — +10 본전이 실제로 성립하는가
- 기본 판매가 5,800 / expected cost anchor 5,779.
- 작은 rounding·simulation 오차 밴드를 허용.
- `PASS`.

### Loop 3 — 판매가가 실제 지출 환급 장치가 되는가
- runtime actual spend와 분리된 static table.
- 고의 실패 차익 금지.
- `PASS`.

### Loop 4 — 후기 long-tail이 과도한가
- +100 P90은 mean보다 크게 높다.
- recovery/hard guarantee와 +90 floor를 유지.
- Human pacing에서 과도하면 성공률보다 먼저 비용/손상·공급량을 재조정.
- `PASS_WITH_PLAYTEST`.

### Loop 5 — +100 한 번으로 macro economy가 무너지는가
- +100 sale 약 11.27M은 prestige premium.
- 고객 예산·거래 채널·후속 작품 비용과 함께 macro-economy 재검토 필요.
- `PASS_WITH_MACRO_REVIEW`.

## 15. 재검토 조건

다음이면 17을 재검토한다.

- +10이 실제 플레이에서 본전선으로 체감되지 않음.
- +11 이후에도 +10 판매가 지배전략.
- 반대로 +100까지 누르는 것이 항상 지배전략.
- MASTERY 수리/재제작 시간이 강화 판단보다 길어짐.
- 실제 ordinary material 공급이 골드보다 압도적 병목이 됨.
- +100 한 번 판매로 macro economy가 장기간 무력화됨.
- +100 도달 기대 시도수가 Human pacing에서 과도함.

## 16. 현재 작업 순서

`BS-PROGRESSION-17` 이후 current order:

1. `RESOURCE_SUPPLY` — 일반 강화/수리 재료의 실제 공급량·획득 경로·recipe mapping.
2. `LATE_REPAIR_ECONOMY` — HIGH/MASTERY 수리 절대경제와 SWORD_BASE_R 후기 스케일 재검증.
3. `MAX_OVERHAUL` — MAX 대수선 필요 여부·부분/완전 복구 대가.
4. `DESTRUCTION_UX` — DESTROYED memorial/successor/UID history UX.
5. `MAX_LEVEL_PAYOFF` — +100 비수치 payoff.
6. `FIRST_10_MINUTES` — 첫 10분 pacing/UX/Visual/feedback 실제 후보 수치 연결.
7. `PRECISION_CUSTOMER_LINK` — 정밀제작·고객/세계 payoff 연결.
8. `RELEASE_NEAR_VERTICAL_SLICE` — 기획 완료 직전 통합 계약.

## 17. 운영 동기화 규칙

사용자 최신 지시에 따라 의미 있는 기획 변경마다 다음을 함께 갱신한다.

```text
GitHub:
- CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md
- BLACKSMITH_PLANNING_AUTHORITY_INDEX.md
- 관련 Canon

Notion:
- Project Home
- 프로젝트 전체 작업계획
- 관련 핵심/Benchmark 페이지
- Repo Main SHA / Sync State
```

항상 **현재 작업 순서 + 승인사항 + 미확정/다음 작업**을 구분해 기록한다.

## 18. 증거 경계

- 14~16 구조: `USER_APPROVED / STRUCTURAL_CANON`.
- 17 numeric curve: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- 20,000-run model: `PLANNING_SIMULATION_EVIDENCE`.
- Human/Player: `NOT_RUN`.
- Runtime implementation: `BLOCKED`.
