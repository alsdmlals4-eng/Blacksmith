# [현재 정본] Blacksmith +100 최대 강화 완료 Payoff

- Parent: `BS-PROGRESSION-20260820-14~17`, `BS-DESTRUCTION-20260824-21`
- Cross-reference: `BS-CRAFT-20260804-07`, `BS-CRAFT-20260805-01~02`
- Decision: `BS-MAX-20260824-22`
- 사용자 승인: `2026-08-24 KST / 권장안 B 승인`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Runtime mutation: `NOT_ALLOWED_IN_THIS_DECISION`
- Human/Player validation: `NOT_RUN`

## 1. 목적

+100은 현재 기본 강화의 진짜 종착점이다.

```text
MAX_ENHANCEMENT_LEVEL = 100
+101_OR_HIGHER = FORBIDDEN_WITHOUT_SEPARATE_USER_APPROVAL
PRESTIGE_RESET = FORBIDDEN_WITHOUT_SEPARATE_USER_APPROVAL
```

+100 이후 질문은 더 높은 숫자가 아니라 다음으로 전환한다.

```text
보유
판매
고객·세계 인계
작품 기록
후속 작품 제작
```

Decision22는 +100 성공이 단순히 숫자 `99 -> 100`으로 끝나지 않도록 **비수치 terminal identity payoff**를 승인한다.

## 2. 승인 구조 — MAX_ENHANCEMENT_COMPLETE

내부 상태:

```text
MAX_ENHANCEMENT_COMPLETE
```

플레이어 표시 권장 의미:

```text
최대 강화 완성
```

+100을 `걸작`, `전설` 등 제작 등급 이름으로 재명명하지 않는다.

이유:
- 제작 등급은 최초 직접 단조 시 고정되는 별도 축이다.
- `보통 / 우수 / 명품 / 걸작 / 전설` 제작 등급은 강화로 승격·강등하지 않는다.
- Artistry 역시 일반 강화 레벨만으로 자동 증가하지 않는다.

따라서:

```text
CRAFT_GRADE != MAX_ENHANCEMENT_COMPLETE
ARTISTRY != MAX_ENHANCEMENT_COMPLETE
```

## 3. +100 성공 순간

```text
target +100 SUCCESS
-> enhancement_level = 100
-> MAX_ENHANCEMENT_COMPLETE = true
-> further enhancement = disabled
-> MAX_ENHANCEMENT_REACHED lifecycle fact 1회 기록
-> one-time completion presentation
```

`MAX_ENHANCEMENT_REACHED`는 자동 gameplay modifier가 아니라 실제 작품 생애 사실이다.

### 3.1 1회 완성 연출

일반 강화 성공보다 명확하게 다른 1회 completion presentation을 제공한다.

표시 가능한 실제 데이터:
- 작품명
- ITEM_UID
- 제작 등급
- 최종 강화 `+100`
- CURRENT / MAX
- 최고 secured checkpoint
- MAX 대수선 사용 여부
- 실제 존재하는 대표 고객/세계/Chronicle 사실

실제 데이터에 없는 역사·고객·업적을 장식 목적으로 생성하지 않는다.

### 3.2 파괴 위험/상태를 가리지 않음

+100 도달 시 CURRENT/MAX를 자동 치유하지 않는다.

```text
+100 reached
!= CURRENT reset
!= MAX reset
!= immortality
!= overhaul reset
```

흉터 있는 +100도 유효한 `MAX_ENHANCEMENT_COMPLETE`다.

## 4. 영구 MAX_COMPLETION_MARK

+100 도달 UID에는 영구적으로 완료 사실을 표시한다.

```text
MAX_COMPLETION_MARK = true
MAX_ENHANCEMENT_REACHED = true
```

표현 후보:
- 작품 카드 badge/frame
- 이름 옆 MAX 완료 표식
- 절제된 완성 각인/VFX
- 작품 생애 화면의 완료 milestone

정확 Visual은 별도 Visual Brief/승인 후 결정한다.

접근성 경계:
- 색상만으로 완료 상태를 전달하지 않는다.
- 텍스트/아이콘/형태 중 최소 하나 이상의 비색상 cue를 함께 사용한다.

## 5. 추가 수치 보상 없음

+100 기본 경제에는 이미 승인된 static market value와 risk premium이 있다.

Decision22는 이를 다시 곱하지 않는다.

```text
+100 completion bonus attack = 0
+100 completion success bonus = 0
+100 automatic artistry = 0
+100 automatic new affix = 0
+100 extra market multiplier = 0
+100 CURRENT heal = 0
+100 MAX heal = 0
+100 overhaul reset = 0
```

기존 독립 가치축은 정상적으로 한 번만 적용될 수 있다.

```text
craft grade
Artistry
affixes
existing Chronicle/history
customer/context fit
```

하지만 `MAX_ENHANCEMENT_COMPLETE` 자체를 새 price/stat multiplier로 사용하지 않는다.

## 6. +100 이후 작품 생애

+100은 강화 여정의 완료이지 물리 작품의 생애 종료가 아니다.

- 작품은 계속 보유 가능.
- 판매 가능.
- 고객/세계에 인계 가능.
- 실제 인과 사건에서 CURRENT/MAX 손상 가능.
- 아직 사용하지 않았고 Decision20 조건을 만족하면 생애 1회 MAX 대수선 가능.
- 이후 CURRENT==0 또는 MAX==0이면 Decision21에 따라 DESTROYED.

파괴 시 Archive에는 다음 사실이 남는다.

```text
MAX_ENHANCEMENT_REACHED = true
highest_enhancement = 100
```

+100이 DESTROYED immunity를 만들지 않는다.

## 7. recognition hook

다른 시스템이 읽을 수 있는 사실:

```text
is_max_enhancement_complete = true
```

이 값은 후속 고객/세계/전시/기록 시스템이 **특별 반응 또는 선택지 eligibility 후보**로 사용할 수 있다.

Decision22가 직접 추가하지 않는 것:
- +100 전용 필수 고객
- +100만 입장 가능한 메인 콘텐츠
- 자동 명성
- 자동 고객 호감
- 자동 전시 성공
- 자동 특별 판매가
- 강제 은퇴/전시/인계

정확 고객/세계 연결은 후속 `PRECISION_CUSTOMER_LINK`가 소유한다.

## 8. 3안 비교

### A. 숫자 종착점만 — REJECT
- +100 숫자와 판매가만 남김.
- 14가 요구한 비수치 payoff를 충족하지 못함.
- 후기 장기 도달의 정체성이 약함.

### B. Terminal Identity Package — APPROVED
- +100 terminal 유지.
- 1회 완성 연출 + 영구 MAX 표식 + 생애 기록 + recognition hook.
- stat/economy 중복 보상 없음.
- 작품 생애를 보존하면서 강화 루프를 실제로 닫음.

### C. +101 / Prestige / 완벽 리롤 — REJECT
- 기존 `MAX_LEVEL=100`과 충돌.
- terminal을 끝없는 treadmill로 바꿈.
- 강화 완료 감각을 다시 다음 숫자로 미룸.

### D. +100 즉시 영구 역할 선택 — DEFER
- 전시/현역/계승 같은 선택은 표현력이 있지만 고객·세계·전시 책임을 선점함.
- 후속 lifecycle/customer 설계에서 실제 맥락으로 다룸.

## 9. 외부 벤치마크 흡수

구체 UI/수치를 복사하지 않고 원리만 사용한다.

- `Guild Wars 2 Legendary · ADAPT`: 장기 endgame 목표의 payoff를 단순 상위 raw-stat tier보다 고유 외형·prestige·편의·정체성으로 제공하는 원리. Blacksmith에서는 편의 power를 새로 추가하지 않고 완성 연출/identity mark/기록 원리만 흡수한다.
- `Sea of Thieves Pirate Legend · ADAPT`: 장기 달성 상태가 recognition의 근거가 되는 원리. Blacksmith에서는 +100을 메인 콘텐츠 gate가 아니라 후속 반응 eligibility fact로만 노출한다.
- `Diablo IV Masterworking · AVOID`: 반복 reset/비이정표 연출/자원 소모가 최종 progression의 반복 노동이 되는 문제를 피한다. +100 이후 새 RNG reroll ladder를 만들지 않는다.

## 10. 5회 전체 적대 검토

### Loop 1 — 제작 등급 충돌
- +100을 걸작/전설로 재명명하지 않음.
- `MAX_ENHANCEMENT_COMPLETE` 별도 상태.
- `PASS`.

### Loop 2 — 경제/파워 이중보상
- 새 attack/stat/price multiplier 없음.
- 기존 +100 static market/economic payoff를 중복 계산하지 않음.
- `PASS`.

### Loop 3 — 위험 무효화
- +100에서 CURRENT/MAX/overhaul state를 초기화하지 않음.
- 이후 causal damage와 DESTROYED 가능.
- `PASS`.

### Loop 4 — 무한 후게임 treadmill
- +101/Prestige/reset/reroll 없음.
- 강화 액션은 +100에서 terminal.
- `PASS`.

### Loop 5 — 보조 콘텐츠가 메인 gate가 되는가
- recognition hook만 제공.
- 필수 고객/콘텐츠 접근권을 Decision22에서 만들지 않음.
- `PASS`.

Human climax/만족감은 실제 플레이테스트 전 PASS를 주장하지 않는다.

## 11. Implementation Reality Gate

```text
+100 maximum/terminal planning canon = VERIFIED
+101/prestige forbidden boundary = VERIFIED
craft grade independence = VERIFIED
artistry independence = VERIFIED
+100 economic payoff = PLANNING_EVIDENCE
historical max_level=100 runtime primitive = EXISTS_HISTORICALLY
MAX_ENHANCEMENT_COMPLETE current runtime = IMPLEMENTATION_UNVERIFIED
MAX completion visual asset = NOT_CREATED
Human climax/satisfaction = NOT_RUN
PRODUCT_IMPLEMENTATION = BLOCKED
```

historical runtime의 `max_level=100` 또는 max 도달 시 `COMPLETE` 상태를 Decision22 구현 완료 증거로 재사용하지 않는다.

## 12. 구현 입력 계약

구현 Gate 이후 최소 상태 후보:

```text
max_enhancement_complete: bool
max_enhancement_reached_at: lifecycle/event reference
```

제품 구현 시 실제 save/UID owner를 fresh read한 뒤 기존 lifecycle/event 모델에 최소 증분으로 흡수한다. 새 별도 progression subsystem을 만들지 않는다.

## 13. Acceptance / Player Evidence

Technical acceptance 후보:
- +100 성공 후 추가 강화 불가.
- 제작 등급과 Artistry 불변.
- CURRENT/MAX/대수선 상태 불변.
- completion lifecycle fact가 같은 UID에 1회 기록.
- 영구 MAX 완료 표식이 save/load 후 유지.
- 새 stat/price multiplier 없음.
- DESTROYED 후에도 Decision21 archive에서 +100 도달 사실 유지.

Human evidence 필요:
- +100 성공 순간이 일반 강화와 구분되는가.
- 상시 MAX 표식이 가독성을 해치지 않는가.
- 흉터 있는 +100도 ‘완성된 작품’으로 이해되는가.
- +100 이후 다음 행동(보유/판매/인계/다음 작품)이 자연스럽게 읽히는가.

## 14. 다음 작업

```text
FIRST_10_MINUTES
-> PRECISION_CUSTOMER_LINK
-> RELEASE_NEAR_VERTICAL_SLICE
```

제품 구현 Gate는 계속 닫아 둔다.
