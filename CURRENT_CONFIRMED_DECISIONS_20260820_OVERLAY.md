# [현재 우선 Overlay] Blacksmith 2026-08-20 Confirmed Decisions

- 상태: `CURRENT_PRIORITY_OVERLAY`
- 기준: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~13 / BS-PROGRESSION-20260820-14~17 / BS-RESOURCE-20260824-18 / BS-REPAIR-20260824-19 / BS-OVERHAUL-20260824-20 / BS-DESTRUCTION-20260824-21 / BS-MAX-20260824-22 / BS-ONBOARD-20260824-23 / BS-LINK-20260824-24`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player validation: `NOT_RUN`

## 0. 운영 동기화 규칙

사용자 최신 지시에 따라 의미 있는 기획 변경마다 **현재 작업 순서 + 승인사항 + 미확정 항목**을 GitHub와 Notion 양쪽에 함께 갱신한다.

```text
GitHub
- 이 Overlay
- BLACKSMITH_PLANNING_AUTHORITY_INDEX.md
- 관련 Canon

Notion
- Project Home
- 프로젝트 전체 작업계획
- 관련 핵심 시스템/Benchmark 페이지
- Repo Main SHA / Sync State
```

승인 전은 `PROPOSED_ONLY`, 승인 후 main 병합 전은 `REPO_UPDATE_REQUIRED`, 병합/검증 완료 후 `SYNCED`로 구분한다.

## 1. 제품 계층 — 01

```text
PRIMARY CORE
강화의 긴장감 + DDD
= 지금 멈춤 / 한 번 더 도전

SUPPORT
작품 UID·생애
정밀제작
고객/세계 생애주기
경제·하루 작업량
```

DDD는 `행동 → 기대 → anticipation → 즉시 결과 → 보상/손실 → 다음 질문`의 밀도를 높이는 것이며 반복 클릭·자극량 자체를 의미하지 않는다.

## 2. 실패·회복·정보 공개 — 02~04

- 기본 골격: `RISK_PLUS_RECOVERY_PROGRESS`.
- 모든 실패는 실제 비용/손실과 같은 작품 UID의 recovery를 남긴다.
- account-wide transferable failstack은 기본 게임에서 금지.
- 강화 전 최종 성공률·시도비·최종 outcome·CURRENT/MAX 위험·recovery·다음 checkpoint를 공개한다.
- 숨은 위험 보정으로 긴장감을 만들지 않는다.

## 3. Checkpoint·CURRENT/MAX·파괴 — 05~09

```text
0 <= CURRENT <= MAX <= 100
new item = 100 / 100
normal repair = CURRENT -> MAX
MAX unchanged
CURRENT == 0 or MAX == 0 -> physical DESTROYED
```

- DOWNGRADE는 최대 1단계, 최근 checkpoint floor 아래로 내려가지 않음.
- `FAIL_DAMAGE`: CURRENT 중심 손상.
- `FAIL_CRITICAL_DAMAGE`: CURRENT 심각 손상 + MAX 구조 흉터.
- 파괴는 별도 destroy roll이 아니라 실제 CURRENT/MAX 0으로만 발생.
- 물리 파괴 후 UID·이름·강화/소유/사건/파괴 원인·Chronicle 기록은 보존.

MAX 상태 첫 테스트:

```text
81~100: success  0pp / new effect 100%
61~80 : success -3pp / new effect 100%
41~60 : success -6pp / new effect 95%
21~40 : success -10pp / new effect 90%
1~20  : success -15pp / new effect 80%
```

- 일반 CURRENT 수리는 MAX를 복구하지 않는다.
- Decision 20의 생애 1회 부분 대수선만 승인된 예외다.

## 4. 일반 CURRENT 수리 — 10~12 + 18~19

```text
missing = MAX - CURRENT

R
= SWORD_BASE_R 800
× MATERIAL_STRUCTURE_MULTIPLIER
× SECURED_BAND_MULTIPLIER

gold_cost
= R × (0.05 + 0.65 × missing / 100)

required_common_material
= max(1, ceil(missing / 25))

PAYMENT = GOLD + REQUIRED_COMMON_MATERIAL
CURRENT -> MAX
MAX unchanged
recovery unchanged
REPAIR_JOB_FATIGUE_COST = 2
```

현재 구조 배율:

```text
material: iron 1.00 / silver 1.20 / meteor_iron 1.50
secured: LEARN·BUILD 1.00 / FIRST 1.10 / TENSION 1.25 / HIGH 2.25 / MASTERY 3.00
```

- `HIGH 2.25 / MASTERY 3.00`은 `BS-REPAIR-20260824-19`가 11의 `1.50 / 1.80`을 부분 대체한 최신 테스트 Budget이다.
- 시장가·실제 다음 강화비·MAX 상태를 일반 CURRENT 수리 runtime 공식에 직접 연결하지 않는다.
- 19의 fresh 20,000-run에서 +100 평균 기대원가 변화는 pre-19 대비 약 `+0.095%`로 기존 거시경제 구조를 유지한다.

## 5. 실패 결과군 정확 비율 — 13

실패가 이미 확정된 뒤의 조건부 비율:

```text
order = HOLD / DOWNGRADE / DAMAGE / CRITICAL

LEARN             100 /  0 /  0 /  0
BUILD_CONFIDENCE   90 /  0 / 10 /  0
FIRST_STOP_POINT   65 / 10 / 23 /  2
TENSION            45 / 10 / 35 / 10
HIGH_STAKES        30 / 15 / 39 / 16
MASTERY            20 / 20 / 40 / 20
```

```text
P(CRITICAL | failure) = P(MAX scar | failure)
```

CRITICAL 뒤 별도 MAX-scar/destroy roll 금지.

## 6. 강화 범위·경제 전환점 — 14

```text
MIN_LEVEL = +0
MAX_LEVEL = +100

+0~+9      INVESTMENT_RECOVERY_ZONE
+10        BREAK_EVEN_RECOVERY_POINT
+11~+100   PROFITABLE_ENHANCEMENT_ZONE
```

+10 누적 기대원가에는 제작·강화·실패 반복·DOWNGRADE 복구·강화 유발 CURRENT 수리·해당 구간 실제 파괴/재제작 기대비용을 포함한다.

정밀제작·수식어·Chronicle·특수 고객/거래 채널 프리미엄은 별도 가치축이다.

## 7. Target level → 경험 밴드 — 15

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

밴드는 `current_level`이 아니라 **target_level** 기준.

```text
CURRENT +10 = FIRST_ECONOMIC_STOP_STATE
TARGET +11  = FIRST_STOP_POINT ATTEMPT
```

## 8. Checkpoint cadence — 16

```text
CHECKPOINT_FLOORS = [10, 30, 60, 90]
```

역할:

```text
+10 경제 본전 확보
+30 TENSION 완료
+60 HIGH_STAKES 완료
+90 FINAL MASTERY PUSH staging
+100 MAX terminal
```

Checkpoint는 오직 DOWNGRADE floor다. CURRENT/MAX/recovery/시도비/수리비를 복구하거나 초기화하지 않는다.

```text
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

## 9. 성공률·회복·강화비 — 17

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

기본 성공률:

```text
+1       100%
+2        97%
+3~+10    95% -> 86%
+11       82%
+12~+30   81% -> 72%
+31~+60   73% -> 69%
+61~+100  69% -> 64%
```

과거 `MASTERY 25~40%` working range는 17에서 대체됨.

Recovery:

```text
+6%p / same-target failure
soft cap 95%
owner = ITEM_UID + TARGET_LEVEL
hard guarantee = LEARN2 / BUILD4 / FIRST4 / TENSION5 / HIGH6 / MASTERY7
```

강화 시도비:

```text
GOLD_ATTEMPT_COST(target)
= round_to_10(12 * target^1.84)

ordinary material balance unit
= ceil(target / 20)
shadow = 50G/unit
```

대표 골드:

```text
+10 830 / +30 6,270 / +60 22,440 / +90 47,310 / +100 57,440
```

MASTERY CURRENT 손상 첫 Budget:

```text
DAMAGE    CURRENT -15~-25
CRITICAL  CURRENT -35~-60
MAX scar  MAX -6~-15
```

## 10. 누적 기대원가·기본 판매가 — 17

20,000-run planning Monte Carlo와 독립 seed 재검산을 사용한다. Seed별 raw mean은 후기 long-tail 때문에 소폭 흔들리므로 승인된 고정 anchor를 사용한다.

```text
independent reproduction tolerance ≈ ±1.5%
SALE_PRICE_RUNTIME != ACTUAL_PLAYER_SPEND
```

| Level | Mean Expected Cost Anchor | Base Market Value |
|---:|---:|---:|
| +0 | 1,500 | 1,000 |
| +5 | 2,322 | 1,900 |
| +9 | 4,759 | 4,600 |
| +10 | **5,779** | **5,800** |
| +11 | 7,023 | 7,400 |
| +20 | 30,713 | 34,400 |
| +30 | 96,006 | 117,100 |
| +40 | 219,565 | 285,400 |
| +50 | 419,230 | 578,500 |
| +60 | 712,986 | 1,055,200 |
| +70 | 1,168,898 | 1,846,900 |
| +80 | 1,907,274 | 3,204,200 |
| +90 | 3,235,853 | 5,824,500 |
| +100 | **5,632,657** | **11,265,300** |

검증 계약:

```text
+0~+9 expected profit < 0
+10 expected profit ~= 0
+11~+100 expected profit > 0
+11 이후 anchor expected profit 단조 비감소
```

## 11. 일반 강화·수리 Resource Supply — 18

사용자 승인: `2026-08-24 KST / 권장안 B`.

```text
CANONICAL_ID = common_reinforcement_material
PLAYER_NAME_KO = 보강재
UNIT_PRICE = 50G
SUPPLY = WORKSHOP_MATERIAL_VENDOR / ALWAYS_AVAILABLE / NO_CAP
```

강화 recipe:

```text
+1~+20   보강재 1
+21~+40  보강재 2
+41~+60  보강재 3
+61~+80  보강재 4
+81~+100 보강재 5
```

일반 CURRENT 수리 recipe:

```text
missing 1~25  -> 보강재 1
missing 26~50 -> 보강재 2
missing 51~75 -> 보강재 3
missing 76~99 -> 보강재 4
```

- 보강재는 새 화폐가 아니라 공통 공방 재료.
- 골드와 보강재를 모두 지불하며 상호 대체/할인하지 않음.
- `iron / silver / meteor_iron`을 일반 보강재로 직접 소비하지 않음.
- RNG·희귀 드롭·일일 cap·채굴/전투·고객 완료를 기본 공급 Gate로 사용하지 않음.
- salvage/customer/world-event 보너스 공급은 future hook이며 아직 제품 승인 아님.
- 제품 data/runtime는 현재 PLAN Gate 때문에 수정하지 않음.

책임 원본: `docs/planning/BLACKSMITH_COMMON_RESOURCE_SUPPLY_CANON_20260824.md`.

## 12. 후기 일반 CURRENT 수리 경제 — 19

사용자 승인: `2026-08-24 KST / 권장안 B`.

```text
SECURED_BAND_MULTIPLIER
LEARN / BUILD = 1.00
FIRST         = 1.10
TENSION       = 1.25
HIGH          = 2.25
MASTERY       = 3.00
```

- 19는 10~12의 수리 공식·Base R·주재료 배율·보강재 수량·피로도 2를 유지한다.
- 11의 `HIGH 1.50 / MASTERY 1.80`만 부분 대체한다.
- 12의 해당 값 기반 후기 예시는 `HISTORICAL_PRE_19_NUMERIC_EVIDENCE`다.
- fresh 20,000-run 재현: +60 `713,376`, +90 `3,246,947`, +100 `5,661,842` mean G-eq; +100 pre-19 대비 약 `+0.095%`.
- Human/Player 검증 전 출시 최종 밸런스로 주장하지 않는다.

책임 원본: `docs/planning/BLACKSMITH_LATE_REPAIR_ECONOMY_CANON_20260824.md`.

## 13. MAX 생애 1회 부분 대수선 — 20

사용자 승인: `2026-08-24 KST / 권장안 B`.

```text
eligibility:
  highest_checkpoint >= +60
  0 < MAX <= 40
  OVERHAUL_USED == false
  DESTROYED == false

effect:
  MAX = min(60, MAX + 15)
  CURRENT = MAX
  OVERHAUL_USED = true

cost:
  750,000G × material_structure_multiplier
  + 보강재 20
  + fatigue 5
```

- 같은 물리 UID 생애 1회만 허용한다.
- 강화 단계·checkpoint·수식어·기존 성능·failure recovery·Chronicle/history를 유지한다.
- DESTROYED 작품은 부활시키지 않는다.
- 반복/완전 MAX 복구와 전용 희귀 복구 화폐를 만들지 않는다.
- 대수선 후 MAX는 60을 넘지 않으므로 STRESSED/STABLE 상태로 복귀할 수 없다.
- 승인 전 비교와 승인 후 독립 20,000-run 재구성 모두 **생애 1회 부분복구는 거시경제 영향이 작고, 반복 완전복구는 위험 곡선을 크게 약화**하는 방향을 재현했다. 정확한 release balance는 Human test와 최종 Balance Lab 대상이다.

책임 원본: `docs/planning/BLACKSMITH_MAX_OVERHAUL_CANON_20260824.md`.

## 14. DESTROYED 기록·추모·후계 UX — 21

사용자 승인: `2026-08-24 KST / 권장안 B`.

```text
CAUSAL_DESTRUCTION
+ IMMUTABLE_HISTORY_ARCHIVE
+ CURATED_MEMORIAL
+ OPTIONAL_SUCCESSOR_PROVENANCE
+ ZERO_POWER_INHERITANCE
```

- `CURRENT==0 or MAX==0`이면 물리 작품은 영구 `DESTROYED`이며 일반 수리·대수선·강화·판매·정상 인계로 부활하지 않는다.
- 파괴 순간에는 `파괴 직전 CURRENT/MAX → 직접 손실 → 실제 0 도달 축 → 직접 원인`을 읽을 수 있게 표시한다.
- 모든 파괴 UID는 불변 `DESTROYED_HISTORY_RECORD`에 자동 보존한다.
- Archive는 오래됐다는 이유로 FIFO 삭제하지 않으며, Memorial은 Archive 중 플레이어가 중요하다고 선택한 작품을 강조하는 별도 view다.
- 후계 작품은 나중에 실제 새 작품을 제작한 뒤 선택적으로 predecessor 관계만 연결한다. `OLD_UID != NEW_UID`이며 새 UID는 자기 제작 provenance부터 시작한다.
- 강화 단계/checkpoint/stat/affix/Artistry/Chronicle/recovery/CURRENT/MAX/재료/가격 premium을 후계 UID에 상속하지 않는다.
- 고객 작품이 파괴돼도 고객 identity/관계 기록은 유지하며, 새 장비는 새 UID를 사용한다.
- 파괴 자체를 자동 Artistry/Chronicle 성장, 재료 환급, power inheritance, death-farming 보상으로 사용하지 않는다.
- historical `enhancement_session.gd`의 별도 destroy 확률 및 파괴 시 progression/affix clear는 현재 runtime 권위가 아니며 `IMPLEMENTATION_DRIFT`다.

책임 원본: `docs/planning/BLACKSMITH_DESTRUCTION_UX_CANON_20260824.md`.

## 15. +100 최대 강화 완료 Payoff — 22

사용자 승인: `2026-08-24 KST / 권장안 B`.

```text
MAX_ENHANCEMENT_COMPLETE
```

- +100은 기본 강화의 진짜 terminal이며 +101/Prestige/reset형 후속 강화는 별도 사용자 승인 없이는 만들지 않는다.
- +100 성공 시 같은 UID에 `MAX_ENHANCEMENT_REACHED` 생애 사실을 1회 기록하고 일반 강화와 구분되는 1회 완성 연출을 제공한다.
- 영구 `MAX_COMPLETION_MARK`로 작품 카드/이름/생애 화면에서 완료 사실을 식별 가능하게 하되 정확 Visual은 별도 승인 대상이다.
- +100을 제작 등급 `걸작/전설`로 재명명하지 않으며 제작 등급과 Artistry를 변경하지 않는다.
- CURRENT/MAX·대수선 사용상태·수식어·기존 성능·Chronicle/history를 초기화하지 않는다. 흉터 있는 +100도 정상 완료 상태다.
- completion 자체로 attack/success/artistry/affix/추가 market multiplier/CURRENT·MAX heal/overhaul reset을 지급하지 않는다.
- `is_max_enhancement_complete=true` recognition fact만 후속 고객/세계/전시 시스템이 읽을 수 있게 한다. Decision22가 필수 고객/메인 콘텐츠 gate·자동 명성/호감/전시 성공을 만들지는 않는다.
- +100 이후 작품은 보유/판매/고객·세계 인계/기록/후속 작품으로 이어지며, 이후 causal damage와 Decision21 DESTROYED 규칙을 그대로 적용받는다.

책임 원본: `docs/planning/BLACKSMITH_MAX_LEVEL_PAYOFF_CANON_20260824.md`.

## 16. 첫 10분 Core Thesis 온보딩 — 23

사용자 승인: `2026-08-24 KST / 권장안 B`.

```text
CORE_THESIS_FIRST_10_MINUTES
```

- `New Game → 짧은 첫 작품 제작 → +1/+2 안전 강화 → +3~+9 BUILD → +10 첫 정밀강화+checkpoint+평균 본전선 → +11 구조 위험 Preview → STOP vs PUSH → 실제 결과 → 짧은 UID/의뢰 payoff` 순서를 사용한다.
- 첫 강화 input은 약 3분 이내, 첫 STOP/PUSH 결정은 약 10분 이내를 Human pacing 목표로 둔다. 강제 countdown은 아니다.
- tutorial-only scripted failure, hidden success boost, 별도 tutorial odds를 만들지 않는다.
- 실제 첫 실패가 발생했을 때만 same-UID recovery를 just-in-time으로 설명한다.
- +10 첫 정밀강화는 full rules 접근을 유지하되 추천 방식/촉매를 먼저 보여주는 progressive disclosure를 사용한다. hard lock하지 않는다.
- +10 STOP와 +11 PUSH 모두 정상 first-session completion이며 +11을 튜토리얼 진행 조건으로 강제하지 않는다.
- +11 직전에 MAX/CRITICAL 구조 위험을 foreground한다.
- Decision23은 starter-order에 바인딩할 정확 고객/세계 owner와 보상 수치를 만들지 않는다. 다음 `PRECISION_CUSTOMER_LINK`가 소유한다.
- 후기 수리·대수선·Archive/Memorial/+100 payoff·전체 고객/세계 관리·고급 Artistry 경제는 첫 핵심 선택 전에 강제로 가르치지 않는다.
- 현재 MainMenu/App Shell은 reuse 가능하지만 최신 Forge/Enhancement 13~22 통합 runtime과 Decision23 onboarding은 `IMPLEMENTATION_UNVERIFIED / BLOCKED`다.

책임 원본: `docs/planning/BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md`.

## 17. 정밀강화·고객/세계 인과 연결 — 24

사용자 승인: `2026-08-24 KST / 권장안 B + Nadia starter + 0.30pp/level test budget`.

```text
DISCLOSED_CONTEXT_FIT_AND_CAUSAL_MULTI_AXIS_RESULT
```

- 첫 세션 starter-order owner는 `NADIA_VENN / ADVENTURER_01`이며 목표는 기존 `SURVIVAL_AND_RECOVERY`를 소비한다.
- 고객은 exact 강화 방식/촉매 정답이 아니라 `목적 / 제약 / 알려진 상황`을 공개한다.
- 정밀강화 미리보기는 `이번 의뢰에 직접 도움 / Gate 변화 / trade-off / 직접 관련 없음`을 설명하며 universal fit score·Best badge·불투명 자동추천을 만들지 않는다.
- 촉매 선택 자체는 고객 bonus가 아니다. 실제 승인된 affix/function 결과가 현재 context와 관련 있을 때만 고객 판단 원인으로 사용한다.
- `WEIGHT`는 hard gate, enhancement는 bounded primary contribution, 승인 function은 특정 eligibility/risk mitigation/interaction, 고객 능력·적성은 작은 context 보정이다.
- 구형 고객 `+1 enhancement level = +1pp event success`는 `HISTORICAL_PRE_24_NUMERIC_EVIDENCE`로 강등한다.
- 새 첫 테스트 Budget은 `ENHANCEMENT_EVENT_BONUS_PP = round(0.30 × enhancement_level)`, +100에서 최대 +30pp다. 출시 최종 수치가 아니다.
- Nadia 결과는 기존 `EXPEDITION_RETURN_STATE / RECOVERY_STATE / ITEM_UID_LIFECYCLE_STATE` 다중축을 유지하고 결과 원인 2~4개 + same UID + primary next action 1개를 사용한다.
- 첫 10분은 Nadia 인계 acknowledgement까지이며, 완전한 탐사 결과는 기존 delayed personal schedule에서 발생한다. 가짜 즉시 세계결과를 만들지 않는다.
- 현재 `VSContentResultRecord`는 결과 기록 primitive일 뿐 precision→customer preview/resolver, 0.30pp runtime, starter Nadia order 구현 증거가 아니다.

책임 원본: `docs/planning/BLACKSMITH_PRECISION_CUSTOMER_LINK_CANON_20260824.md`.

## 18. 과거 숫자의 지위

다음은 current numeric authority가 아니다.

```text
+5 최초 흑자
+60 마지막 가격 앵커
old decade success pattern
old MASTERY 25~40% working range
old multi-step downgrade
old destroy RNG
pre-19 HIGH repair multiplier 1.50
pre-19 MASTERY repair multiplier 1.80
pre-24 customer enhancement contribution +1.00pp / level
```

상태: `HISTORICAL_NUMERIC_EVIDENCE / RECALIBRATION_INPUT`.

## 19. 현재 승인사항 요약

```text
01     PRIMARY CORE = 강화 긴장감 + DDD
02~04  risk + item-UID recovery + disclosure
05~09  checkpoint / CURRENT-MAX / destroy-at-zero
10~12  repair economy / GOLD+MATERIAL
13     failure family ratio
14     +10 break-even / +100 max
15     target-level experience bands / +10 first floor
16     checkpoint [10,30,60,90]
17     success / recovery / attempt cost / expected cost / static market anchors
18     common reinforcement material / 50G / deterministic unlimited vendor supply / enhancement+repair recipe mapping
19     late repair economy / HIGH 2.25 / MASTERY 3.00 / fresh 20k Monte Carlo
20     one-lifetime partial MAX overhaul / +15 / ceiling 60 / 750k×material + reinforcement 20 + fatigue 5
21     causal destruction / immutable archive / curated memorial / optional new-UID successor provenance / zero power inheritance
22     +100 terminal identity / one-time completion presentation / permanent completion mark / lifecycle fact / zero extra power multiplier
23     first 10 minutes core-thesis sprint / real odds / +10 precision+checkpoint / +11 STOP vs PUSH / just-in-time teaching
24     Nadia starter / disclosed context fit / no universal fit score / customer enhancement +0.30pp per level test budget / causal multi-axis result
```

17·19·20·24의 숫자는 `NOT_FINAL_PRODUCT_BALANCE`; 18·21·22·23 및 24의 구조는 `USER_APPROVED / PLANNING_CANON`. 제품 data/runtime은 아직 변경하지 않는다.

## 20. 현재 작업 순서

1. `RELEASE_NEAR_VERTICAL_SLICE` — 기획 완료 직전 통합 계약.

## 21. 증거 경계

- 01~16 구조: `USER_APPROVED`.
- 17 숫자: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- 18 Resource Supply: `USER_APPROVED / PLANNING_CANON`.
- 19 Late Repair Economy: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- 20 MAX Overhaul: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- 21 Destruction UX: `USER_APPROVED / PLANNING_CANON`.
- 22 MAX Level Payoff: `USER_APPROVED / PLANNING_CANON`.
- 23 First 10 Minutes: `USER_APPROVED / PLANNING_CANON`; timing targets are `HUMAN_NOT_RUN`.
- 24 Precision-Customer Link structure: `USER_APPROVED / PLANNING_CANON`; `0.30pp/level`은 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.
- Monte Carlo: `PLANNING_SIMULATION_EVIDENCE`; exact delta is policy-sensitive.
- Human/Player: `NOT_RUN`.
- Runtime implementation: `BLOCKED`; content-result record primitive is reuse evidence, not Decision24 resolver implementation evidence.