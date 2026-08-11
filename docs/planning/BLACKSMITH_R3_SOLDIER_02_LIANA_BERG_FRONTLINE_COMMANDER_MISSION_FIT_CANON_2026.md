# Blacksmith R3–R7 SOLDIER_02 — Liana Berg Frontline Commander Mission-Fit Canon

- Decision: `BS-CONTENT-20260811-07`
- 상태: `USER_APPROVED_R3_R7_7_OF_10 / PLANNING_ONLY`
- Content ID: `SOLDIER_02`
- Customer ID: `LIANA_BERG`
- 고객: 리아나 베르크
- Activity Family: `FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY`
- Content Goal: `MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`
- 사람 플레이테스트: `NOT_RUN`

## 1. 목적

리아나 베르크는 기존 군인 유형 추가 고객·전선 지휘관이다. 이 콘텐츠는 마레크 올덴의 소량 표준 주문과 다른 Soldier 질문을 검증한다. 여러 UID가 같은 공개 규격을 만족하는지가 아니라, **한 명의 지휘관이 공개한 이번 임무·책임에 어떤 작품 한 점을 맡길 것인가**가 핵심이다.

```text
EXISTING_LIANA_BERG_CUSTOMER_REUSED
NO_NEW_PARALLEL_SOLDIER_COMMANDER
PLAYER_ROLE: BLACKSMITH_COMMANDER_EQUIPMENT_DECISION_MAKER_NOT_TACTICAL_OR_UNIT_CONTROLLER
```

플레이어는 전술 지휘관이나 병참 관리자처럼 전장을 조작하지 않는다. 대장장이로서 공개된 임무 맥락을 읽고 실제 작품 후보를 비교해 한 UID를 인계한 뒤, 그 선택이 고객과 작품의 후속 생애에 어떤 의미를 남겼는지 확인한다.

## 2. 기본 흐름

```text
리아나 방문
→ 이번 임무의 책임·위험·필요 장비 역할 공개
→ 실제 작품 UID 후보 비교
→ 한 작품 UID 선택
→ 같은 UID 인계
→ 전선 임무는 비직접 세계 사건으로 해결
→ MISSION_DUTY_STATE
 + COMMANDER_RETURN_STATE
 + ITEM_UID_FIELD_LEGACY_STATE
→ 수리·복원·후속 강화·신작·보존·재배정 판단
```

```text
NO_DIRECT_TACTICAL_COMBAT
NO_UNIT_MOVEMENT_OR_FORMATION_CONTROL
NO_REALTIME_LOGISTICS_CONTROL
NO_SOLDIER_CASUALTY_MICROMANAGEMENT
```

## 3. 임무 적합 증거 계약

Decision07은 새 Soldier 전용 원수치나 범용 전투 총점을 만들지 않는다. 임무 적합 판단은 현재 Blacksmith 권위가 이미 소유한 증거 중 이번 공개 임무에 실제 관련된 것만 사용한다.

허용 가능한 설명 근거 예시:

- 장비 범주·역할 eligibility
- 현재 `WEIGHT`와 고객 하중/호환 Gate
- 현재 `DURABILITY`
- 강화 단계
- 임무가 실제 요구할 때만 관련 공격·방어·취급 원수치
- 임무가 명시적으로 요구할 때만 승인된 특수기능 적합
- 리아나의 기존 고객 능력·적성 정보
- 같은 UID의 손상·수리·소유·provenance·생애 기록이 이번 판단에 실제 관련될 때의 근거

다음을 새로 만들지 않는다.

```text
NO_COMMAND_POWER_SCORE
NO_HERO_SCORE
NO_LEADERSHIP_SCORE
NO_MISSION_FIT_TOTAL_SCORE
```

하나의 숨은 점수로 작품과 고객을 압축하지 않는다. 결과 UI는 공개 임무와 실제 UID 증거에서 2~4개의 지지·충돌 이유를 설명한다.

## 4. 여러 방어 가능한 선택

```text
NO_HIGHEST_DEFENSE_ALWAYS_BEST
NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST
```

- 최고 방어 작품이 하중·역할·기능 맥락에 맞지 않으면 자동 정답이 아니다.
- 최고 강화 작품도 이번 임무의 실제 요구와 다른 역할이면 자동 정답이 아니다.
- 가장 가벼운 작품도 항상 정답이 아니다.
- 역사적으로 중요한 작품도 자동 정답이나 자동 오답이 아니다.
- 임무 성공은 선택한 작품이 유일한 정답이었다는 증명이 아니다.
- 작품이 손상되어 돌아왔다고 해서 그 선택이 자동으로 잘못된 것도 아니다. 맡은 책임을 실제로 수행하며 손상될 수 있다.

```text
NO_ITEM_AS_SOLE_CAUSE_OF_MISSION_RESULT
```

작품은 임무 결과에 의미 있게 기여할 수 있지만, 고객 능력·상황·위험 등 다른 원인을 지우고 작품 하나가 모든 성공/실패를 결정한 것처럼 표현하지 않는다.

## 5. 결과 구조

```text
MISSION_DUTY_STATE
COMMANDER_RETURN_STATE
ITEM_UID_FIELD_LEGACY_STATE
```

### MISSION_DUTY_STATE

공개됐던 이번 임무·책임이 비직접 현장 사건에서 어떻게 수행됐는지를 요약한다. 이 축은 지휘관의 귀환 상태나 작품 상태와 같은 값으로 합치지 않는다.

### COMMANDER_RETURN_STATE

리아나라는 이름 고객이 임무 뒤 어떤 상태로 돌아왔는지를 별도로 보여준다. 부상·피로·보호 성공 같은 비치명적 결과를 표현할 수 있지만 Decision07 baseline은 영구 사망을 요구하지 않는다.

### ITEM_UID_FIELD_LEGACY_STATE

선택한 같은 UID가 현장 사용에서 어떤 손상·보호·회수·사용 흔적과 후속 생애를 얻었는지 보여준다.

임무 성공, 리아나의 안전한 귀환, 작품의 무손상은 서로 독립적인 축이다. 하나의 총점이나 승패 메시지로 다른 축을 소거하지 않는다.

## 6. 같은 UID 생애

```text
SAME_ITEM_UID_PRESERVED
```

인계 전 작품, 전선에서 사용된 작품, 귀환·회수된 작품은 같은 UID다. 현장 손상·보호 사건·수리·회수·provenance·향후 Chronicle 관련 사건은 같은 작품의 생애에 이어진다. 전투 결과용 새 아이템 객체로 교체하지 않는다.

## 7. 마레크 Soldier01과의 책임 분리

`MAREK_OLDEN / SOLDIER_01 / SMALL_LOT_STANDARD_ORDER`는 여러 독립 UID의 **소량 표준화와 반복 생산 책임**을 소유한다.

마레크의 핵심 질문:

> 여러 작품이 같은 공개 규격을 안정적으로 만족하는가?

리아나의 핵심 질문:

> 이 한 작품이 이 한 지휘관의 이번 공개 임무와 책임에 적합한가?

Decision07은 기준품 복제·배치 주문·표준 채택 구조를 다시 소유하지 않는다. 반대로 Marek의 배치 결과를 리아나 개인 귀환 결과로 덮어쓰지 않는다.

## 8. 카시아 Gladiator01과의 책임 분리

`CASSIA_BELLAN / GLADIATOR_01 / ARENA_SIGNATURE_WEAPON_AND_LEGACY`는 경기 맥락, 경기 승패와 실제 장비 기여 분리, 공개된 대표 무기의 arena legacy를 소유한다.

리아나는 “전쟁 스킨을 씌운 카시아”가 아니다. 공개 명성·대표 무기 퍼포먼스가 아니라 **임무 책임·지휘관 귀환·현장 작품 생애**가 핵심이다.

```text
ARENA_SIGNATURE_WEAPON_AND_LEGACY: CASSIA_BELLAN_OWNER_PRESERVED
SMALL_LOT_STANDARD_ORDER: MAREK_OLDEN_OWNER_PRESERVED
FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY: LIANA_BERG_OWNER
```

## 9. 리아나 결과의 위험 경계

```text
NO_BASELINE_PERMADEATH_FOR_LIANA
NO_DEATH_FARMING_OR_RECRUIT_REPLACEMENT_LOOP
```

리아나는 이름 고객이자 재방문 가능한 관계 축이다. 이번 baseline은 영구 사망을 일반 결과로 추가하지 않는다. 영구 손실·사망을 다루려면 별도 고위험 기획 Decision과 사용자 승인이 필요하다.

Decision07은 병사 roster, 전사자 충원, 새 지휘관 모집, 사망 반복 보상 같은 관리 루프를 만들지 않는다.

## 10. 진행·파밍 경계

```text
NO_MISSION_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_SURVIVAL
NO_MISSION_FARMING_MULTIPLIER
```

- 임무 횟수는 `ARTISTRY`를 자동 증가시키지 않는다.
- 리아나 생환 횟수는 `ARTISTRY`를 자동 증가시키지 않는다.
- 승리·생환 자체만으로 `CHRONICLE_AFFIX`를 자동 지급하지 않는다.
- 기존 Chronicle 권위가 구체적으로 의미 있는 사건을 인정할 수는 있으나 N번째 임무/승리/생환이라는 이유만으로 성장하지 않는다.
- 반복 임무에 별도 파밍 배율을 만들지 않는다.

## 11. 정보 계약

인계 전에는 최소한 다음을 보여준다.

1. 리아나의 이번 임무 책임·필요 역할
2. 핵심 위험 또는 제약
3. 선택한 실제 작품 UID
4. hard eligibility / 하중 문제
5. 실제 관련 근거 2~4개

자동 `BEST` 장비 표시는 하지 않는다.

결과 후에는 세 결과 축, 2~4개의 실제 인과 이유, 같은 UID의 현장 상태, 다음 행동 이유 한 가지를 우선한다. 핵심 상태를 색상만으로 전달하지 않는다.

정확한 문구·임무 유형·기간·위험도·장비 임계값·부상 상태·경제값·보상·분포는 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 12. 보호 경계

```text
EXISTING_LIANA_BERG_CUSTOMER_REUSED
NO_NEW_PARALLEL_SOLDIER_COMMANDER
SAME_ITEM_UID_PRESERVED
NO_DIRECT_TACTICAL_COMBAT
NO_UNIT_MOVEMENT_OR_FORMATION_CONTROL
NO_REALTIME_LOGISTICS_CONTROL
NO_SOLDIER_CASUALTY_MICROMANAGEMENT
NO_COMMAND_POWER_SCORE
NO_HERO_SCORE
NO_LEADERSHIP_SCORE
NO_MISSION_FIT_TOTAL_SCORE
NO_HIGHEST_DEFENSE_ALWAYS_BEST
NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST
NO_ITEM_AS_SOLE_CAUSE_OF_MISSION_RESULT
NO_BASELINE_PERMADEATH_FOR_LIANA
NO_DEATH_FARMING_OR_RECRUIT_REPLACEMENT_LOOP
NO_MISSION_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_SURVIVAL
NO_MISSION_FARMING_MULTIPLIER
BLACKSMITH_COMMANDER_EQUIPMENT_DECISION_MAKER_NOT_TACTICAL_OR_UNIT_CONTROLLER
PRODUCT_IMPLEMENTATION_BLOCKED
TASK3_IMPLEMENTATION_NOT_APPROVED
```

## 13. 벤치마킹 판정

- Battle Brothers: `ADAPT` — 장비 준비가 개별 인물의 위험 대응에 의미를 갖고 부상·사건 결과가 지속되는 원리. 직접 전술전투·용병단 운영·permadeath baseline은 `REJECT`.
- Wartales: `ADAPT` — 인물별 장비 조합과 위험 전 준비의 중요성. 파티·캠프·턴제 전투 운영은 `REJECT`.
- The Banner Saga: `ADAPT` — 선택 결과가 이름 있는 인물과 이후 이야기 상태에 지속되는 원리. 캐러밴 경영·직접 전투·영구 사망 baseline은 `REJECT`.
- `DIFFERENTIATOR`: Blacksmith에서는 플레이어가 전투를 조작하지 않고 **대장장이가 어떤 한 작품을 누구의 어떤 책임에 맡겼는지**가 같은 UID 생애와 이름 고객의 후속 상태로 돌아온다.

## 14. 적대적 검토

1. Marek과 중복되는가 → `MUST_FIX`: Marek은 multi-UID standardization, Liana는 single-commander duty fit으로 분리한다.
2. Cassia의 전쟁 재스킨인가 → `MUST_FIX`: Cassia는 arena contribution/public legacy, Liana는 responsibility/return/field legacy를 소유한다.
3. 직접 전술전투로 샐 수 있는가 → `MUST_FIX`: 전선 사건은 비직접 resolution이며 위치·대형·타깃·스킬·병사 조작을 추가하지 않는다.
4. 최고 방어·최고 강화 자동정답인가 → `MUST_FIX`: 공개 임무와 실제 하중·역할·기능 맥락을 함께 설명한다.
5. 작품이 임무 결과의 유일 원인인가 → `MUST_FIX`: 세 결과 축과 2~4개 원인으로 단일 인과를 거부한다.
6. 리아나 사망이 감정 파밍/roster 관리가 되는가 → `MUST_FIX`: baseline permadeath와 replacement loop를 배제한다.
7. 전선 결과가 새 UID를 만드는가 → `MUST_FIX`: 같은 UID를 보존한다.
8. command/hero 점수로 다시 압축되는가 → `MUST_FIX`: 새 불투명 총점을 만들지 않는다.

직접 전투·부대 경영·지휘관 RPG 성장으로 넓히자는 비판은 Blacksmith의 대장장이/작품 생애 코어를 약화하므로 `REJECTED_CRITIQUE`다.

## 15. 플레이테스트

현재 사람 플레이테스트: `NOT_RUN`.

후속 관찰 질문:

- 플레이어가 왜 이 작품을 리아나에게 맡겼는지 공개 임무와 실제 근거로 설명할 수 있는가.
- 최고 방어·최고 강화가 아닌 작품도 방어 가능한 선택이 되는 이유를 이해하는가.
- 임무 성공과 리아나 귀환과 작품 상태가 서로 다른 결과라는 점을 기억하는가.
- 결과를 본 뒤 어떤 작품을 수리·복원·강화·교체·보존·재배정할지 이유를 만들 수 있는가.

Human/Android/accessibility evidence는 실제 관찰 전까지 `NOT_RUN`이다.
