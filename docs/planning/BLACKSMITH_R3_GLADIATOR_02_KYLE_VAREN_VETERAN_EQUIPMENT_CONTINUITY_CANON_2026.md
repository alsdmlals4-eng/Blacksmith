# Blacksmith R3 Gladiator 02 — Kyle Varen Veteran Equipment Continuity Canon

## Authority

- Decision: `BS-CONTENT-20260811-09`
- Content ID: `GLADIATOR_02`
- Customer: `KYLE_VAREN / 카일 바렌`
- Activity family: `VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION`
- R3–R7 approval slot: `9/10`
- Work mode: `PLANNING_ONLY`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`
- Human playtest: `NOT_RUN`
- Android device: `NOT_RUN`
- Accessibility: `NOT_RUN`

이 정본은 검투사 전투를 직접 조작하거나 Kyle의 커리어를 경영하는 콘텐츠가 아니다. 플레이어는 대장장이로서 Kyle에게 실제로 존재하는 과거 작품의 현재 상태와 생애 기록을 읽고, 그 작품을 다시 현역으로 맡길지 또는 그 작품의 역사를 보존한 채 새 작품에 다음 역할을 맡길지 결정한다.

플레이어 권위는 `BLACKSMITH_EQUIPMENT_CONTINUITY_DECISION_MAKER_NOT_GLADIATOR_CONTROLLER`다.

## Core promise

```text
KYLE_VAREN 재방문
→ 실제 과거 Kyle item record 확인
→ comeback 목적 + 현재 필요한 장비 역할 공개
→ 과거 작품 UID의 현재 상태·실제 생애 증거 확인
→ hard serviceability / eligibility gate
→ 가능한 경우 KEEP_IN_SERVICE vs RETIRE_AND_REPLACE 비교
→ 플레이어 결정
→ 비직접 comeback/arena world event 해결
→ VETERAN_RETURN_STATE
 + EQUIPMENT_CONTINUITY_STATE
 + ITEM_UID_LINEAGE_STATE
→ 실제 원인 2~4개
→ 주 후속 행동 1개
```

핵심 선택은 가장 강한 장비 찾기가 아니라 `continuity versus replacement responsibility`다.

## Activation contract — real history only

Decision09의 continuity 분기는 실제 과거 증거가 있을 때만 열린다.

- `KYLE_VAREN`이 현재 고객으로 존재한다.
- Kyle에게 과거에 실제 인계된 작품 UID 또는 승인된 migration으로 연결되는 실제 legacy record가 존재한다.
- comeback 목적 또는 현재 장비 역할이 인계 판단 전에 공개된다.

실제 과거 기록이 없으면 콘텐츠를 열기 위해 Kyle의 과거나 작품을 새로 만들어내지 않는다.

```text
NO_FABRICATED_KYLE_HISTORY
NO_FAKE_LEGACY_ITEM_FOR_CONTENT_UNLOCK
```

신규 캠페인의 첫 Kyle 방문은 일반 고객 요청일 수 있지만, `VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION`의 continuity 선택은 실제 이전 인계가 생긴 뒤에만 의미를 갖는다.

## Hard gate before sentiment

작품을 오래 썼다는 감정이나 유명세는 현재 사용 가능성보다 앞서지 않는다.

판단은 기존 item/lifecycle 권위가 실제로 보유하는 정보만 소비한다.

허용되는 hard evidence 예시:

- item 존재 여부
- `BROKEN_OR_LOST` 등 현행 lifecycle state
- 실제 current durability/state
- 공개된 현재 요청의 equipment category/role eligibility
- 현재 사용에 직접 관련된 실제 손상·수리 상태

Decision09를 위해 새 `SAFETY_SCORE`, `SERVICEABILITY_SCORE`, `VETERAN_SCORE`를 만들지 않는다.

기존 작품이 hard gate를 통과하지 못하면 `KEEP_IN_SERVICE`가 선택 불가능할 수 있다. 이것은 새 작품이 항상 더 좋다는 규칙이 아니라 현재 작품 상태가 이번 현역 사용을 허용하지 않는다는 의미다.

## Contextual continuity evidence

hard gate 이후에는 다음과 같은 실제 존재 evidence만 비교한다.

- 현재 durability/lifecycle state
- 기존 enhancement level
- 현재 공개 역할에 실제 관련된 기존 raw attributes
- 현재 역할에 실제 관련된 승인 special function/affix
- 과거 소유·인계 provenance
- 과거 손상·수리·복원 기록
- Kyle와 해당 UID 사이의 실제 사용 기록
- 승인된 arena/lifecycle/Chronicle 사건

다음 하나만으로 자동 정답을 만들지 않는다.

```text
NO_OLD_ITEM_ALWAYS_BEST
NO_NEW_ITEM_ALWAYS_BEST
NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST
NO_HIGHEST_ARTISTRY_ALWAYS_BEST
NO_MOST_CHRONICLE_ALWAYS_BEST
NO_SENTIMENT_SCORE
NO_VETERAN_TOTAL_SCORE
```

Kyle와의 관계 수치 자체나 legacy PoC score도 자동 정답이 아니다.

## Defensible choice contract

### KEEP_IN_SERVICE

기존 작품이 hard gate를 통과하고, 이번 comeback 역할과 실제 기능·상태가 맞으며, 실제 Kyle 사용 이력이 현재 요구와 연속적으로 연결될 때 방어 가능한 선택이다.

오래 사용했다는 사실만으로 보너스를 얻지 않는다.

### RETIRE_AND_REPLACE

기존 작품이 사용할 수 있더라도 현재 역할과 맞지 않거나, 상태·기존 수리 이력이 현재 위험과 충돌하거나, 과거에는 좋은 선택이었지만 이번 요구가 달라졌을 때 방어 가능한 선택이다.

기존 작품을 더 이상 위험에 노출하지 않고 그 실제 역사를 보존하는 판단도 유효할 수 있다.

새 작품이라는 이유만으로 더 높은 정답 점수를 받지 않는다. 자동 `BEST` 추천은 제공하지 않는다.

## Cassia responsibility separation

```text
CASSIA_ARENA_FIT_RESPONSIBILITY_PRESERVED
```

Cassia / `CASSIA_BELLAN / GLADIATOR_01 / ARENA_SIGNATURE_WEAPON_AND_LEGACY`의 질문:

> 이번 공개 경기 맥락에 어떤 실제 작품이 설명 가능하게 적합한가?

Cassia는 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`를 소유한다.

Kyle / `GLADIATOR_02`의 질문:

> 실제 과거 생애가 있는 작품을 이번에도 현역으로 맡길 것인가, 아니면 그 작품을 이번 역할에서 물리고 새 작품으로 넘어갈 것인가?

Decision09는 Cassia의 경기 적합·장비 기여 결과 축을 복제하지 않는다.

## Noble01 and repair responsibility separation

```text
NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED
```

Noble01 / `CEREMONIAL_NOBLE / HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY`은 기존 가보를 물리적으로 어디까지 수리·복원·재작업할지 판단하는 treatment depth를 소유한다.

Decision09는 새로운 `COMEBACK_RESTORATION_DEPTH`, `VETERAN_REPAIR_SCORE`, `RETIREMENT_REPAIR_TREE`를 만들지 않는다. 필요한 repair/restoration은 기존 owner의 결과를 읽거나 기존 작업으로 넘긴다.

```text
NOBLE01_OR_EXISTING_REPAIR_OWNER = HOW_FAR_TO_TREAT
KYLE_GLADIATOR02 = CONTINUE_IN_SERVICE_OR_RETIRE_AND_REPLACE
```

Ersa의 공개 전시 책임과 Sedric의 archival provenance/custody 책임도 Decision09가 가져오지 않는다.

## UID continuity and replacement contract

### Keep path

```text
OLD_UID -> KEEP_IN_SERVICE -> SAME_UID
```

- 같은 UID를 유지한다.
- 기존 provenance/lifecycle/Chronicle를 그대로 이어간다.
- comeback 결과는 같은 UID의 다음 실제 사건이 될 수 있다.

### Replace path

```text
OLD_UID -> RETIRED_FROM_THIS_ROLE
NEW_UID -> NEW_EQUIPMENT_ROLE
OLD_UID != NEW_UID
```

- 기존 UID를 새 UID로 rename하지 않는다.
- 기존 UID를 삭제하지 않는다.
- 새 작품에 옛 UID의 history/progression을 복사하지 않는다.
- 기존 작품은 inventory/archive/exhibition/기타 승인 lifecycle의 후속 판단 대상으로 남을 수 있다.
- 새 작품은 자기 제작 provenance부터 시작한다.

```text
NO_UID_REWRITE
NO_HISTORY_TRANSFER_TO_REPLACEMENT
OLD_ITEM_HISTORY_PRESERVED
NEW_ITEM_GETS_NEW_UID
```

## ITEM_UID_LINEAGE_STATE boundary

`ITEM_UID_LINEAGE_STATE`는 전투력 또는 성장 점수가 아니다.

이 결과 축은 다음 실제 lifecycle 사실을 구분하기 위한 정보 상태다.

- 기존 UID가 계속 현역인지
- 기존 UID가 이번 역할에서 은퇴했는지
- 새 UID가 후속 장비로 선택되었는지
- 기존 기록 체계가 실제 old→new 사건 reference를 표현할 수 있다면 어떤 reference가 존재하는지

다음을 만들지 않는다.

```text
NO_LINEAGE_POWER_BONUS
NO_SUCCESSION_TOTAL_SCORE
NO_VETERAN_LEGACY_SCORE
```

이전 작품의 enhancement, affix, Artistry, Chronicle, provenance, stat을 새 UID에 상속하지 않는다. 새 글로벌 lineage subsystem도 이 Decision이 선승인하지 않는다.

## Result contract

결과는 하나의 승패나 총점으로 합치지 않는다.

```text
VETERAN_RETURN_STATE
EQUIPMENT_CONTINUITY_STATE
ITEM_UID_LINEAGE_STATE
```

- `VETERAN_RETURN_STATE`: Kyle의 comeback/world event 자체 결과.
- `EQUIPMENT_CONTINUITY_STATE`: keep/replace 판단이 공개 목적과 실제 작품 상태·역사에 어떻게 맞았는지.
- `ITEM_UID_LINEAGE_STATE`: 기존 UID와 필요 시 새 UID가 어떤 실제 lifecycle 관계를 갖게 되었는지.

comeback 성공과 장비 판단 품질은 동일 값이 아니다. 작품을 world-event의 유일 원인으로 주장하지 않는다.

결과 화면은 실제 원인 2~4개와 주 후속 행동 1개를 보여준다. 정확 enum과 결과 분포는 현재 비권위다.

## Legacy Kyle PoC boundary

현행 저장소의 `gladiator_kyle / iron_sword` 데이터와 고정 수치는 역사 PoC fixture다.

```text
LEGACY_GLADIATOR_KYLE_FIXTURE_NON_AUTHORITATIVE
NO_FIXED_IRON_SWORD_CANON
NO_LEGACY_REQUIRED_LEVEL_CANON
NO_LEGACY_STRETCH_LEVEL_CANON
NO_LEGACY_PREFERRED_AFFIX_CANON
NO_LEGACY_FIXED_DEADLINE_CANON
NO_LEGACY_PAYMENT_OR_FAME_CANON
NO_LEGACY_ARENA_SCORE_FORMULA_CANON
```

따라서 과거의 fixed required/stretch enhancement, preferred affix, deadline/report delay, payment/fame/relationship, grade/attack weighted score, `DEFEAT / WIN / DECISIVE_WIN` score band를 Decision09 현재 정본으로 승격하지 않는다.

재사용 가능한 것은 실제로 보존 가치가 있는 역사/구조적 강점이다.

- legacy customer relation의 승인 가능한 migration evidence
- transaction/event/registry identity
- 실제 delivered item UID history
- handoff/result lifecycle 구조

실제 save migration schema와 compatibility 구현은 제품 구현 Gate에서 별도 검증한다.

## Direct combat and management boundary

플레이어는 대장장이로 남는다.

```text
BLACKSMITH_EQUIPMENT_CONTINUITY_DECISION_MAKER_NOT_GLADIATOR_CONTROLLER
NO_DIRECT_ARENA_COMBAT
NO_GLADIATOR_ROSTER_OR_GUILD_MANAGEMENT
NO_TRAINING_OR_INJURY_MANAGEMENT
NO_BETTING_SYSTEM
NO_BASELINE_PERMADEATH
```

다음은 scope 밖이다.

- Kyle 직접 이동/행동 명령
- fighter tactics
- roster/recruitment management
- guild/team management
- training management
- injury-management RPG
- replacement fighter loop
- arena economy management

## Progression and farming boundary

comeback·retirement·replacement 자체가 무료 성장원이 아니다.

```text
NO_COMEBACK_COUNT_ARTISTRY_GROWTH
NO_REPLACEMENT_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_COMEBACK_OR_RETIREMENT
NO_LINEAGE_POWER_BONUS
NO_COMEBACK_FARMING_MULTIPLIER
```

기존 Chronicle 권위가 충분히 의미 있는 실제 특정 사건을 Chronicle로 판정할 때만 그 사건을 해당 실제 UID에 연결한다.

## Information contract

결정 전에는 최소한 다음을 구분해 읽을 수 있어야 한다.

- Kyle comeback 목적
- 현재 요구 equipment category/role
- 실제 prior Kyle item UID
- hard eligibility/serviceability
- 실제 관련 상태/lifecycle evidence
- continuity를 지지하는 이유
- continuity와 충돌하는 이유
- replacement 후보가 있다면 그 새 작품의 실제 증거

결정 행동은 의미상 다음 두 가지다.

- `이 작품을 다시 현역으로 맡긴다`
- `이 작품은 이번 역할에서 물리고 새 작품을 맡긴다`

정확 UI 문구는 현재 canon 수치/카피가 아니다.

결과는 세 축, 실제 원인 2~4개, 주 후속 행동 1개를 전달하고 old/new UID가 동시에 존재할 때 둘을 혼동하지 않게 해야 한다. 색상만으로 핵심 상태를 전달하지 않는다.

## Follow-up boundary

다음 후속 행동은 기존 승인 owner로 연결할 수 있다.

- same UID continued-service repair
- 기존 repair/restoration 검토
- follow-up enhancement 판단
- old UID preservation
- Ersa exhibition 후보
- Sedric archival review 후보
- 새 replacement 작품 제작
- 다음 Kyle request 준비

Decision09 자체가 repair/restoration/exhibition/archive 결과를 자동 확정하지 않는다.

## P1 taxonomy ambiguity

```text
P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED
```

`BS-CT-06`의 역사적 “고객 4유형×8명”과 현재 상세 책임에서 Noble이 별도 책임으로 존재하는 모호성은 Decision09에서 해결하지 않는다. Kyle/GLADIATOR_02 상세화는 전체 taxonomy 재정의 승인이 아니다.

## Exact-value policy

다음은 현재 canon 수치가 아니다.

- comeback unlock timing
- 방문/재방문 cadence
- required equipment category distribution
- hard durability/serviceability threshold
- replacement threshold
- deadline
- reward/economy/relationship delta
- result distribution
- Chronicle trigger frequency

모두:

```text
NON_CANONICAL_BASELINE_TEST_PRESET
USER_PLAYTEST_REQUIRED
```

legacy PoC 숫자를 초기값으로 자동 부활시키지 않는다.

## Protected boundaries

```text
NO_FABRICATED_KYLE_HISTORY
NO_FAKE_LEGACY_ITEM_FOR_CONTENT_UNLOCK
NO_UID_REWRITE
NO_HISTORY_TRANSFER_TO_REPLACEMENT
OLD_ITEM_HISTORY_PRESERVED
NEW_ITEM_GETS_NEW_UID
CASSIA_ARENA_FIT_RESPONSIBILITY_PRESERVED
NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED
NO_OLD_ITEM_ALWAYS_BEST
NO_NEW_ITEM_ALWAYS_BEST
NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST
NO_HIGHEST_ARTISTRY_ALWAYS_BEST
NO_MOST_CHRONICLE_ALWAYS_BEST
NO_SENTIMENT_SCORE
NO_VETERAN_TOTAL_SCORE
NO_LINEAGE_POWER_BONUS
LEGACY_GLADIATOR_KYLE_FIXTURE_NON_AUTHORITATIVE
NO_FIXED_IRON_SWORD_CANON
NO_LEGACY_ARENA_SCORE_FORMULA_CANON
NO_DIRECT_ARENA_COMBAT
NO_GLADIATOR_ROSTER_OR_GUILD_MANAGEMENT
NO_TRAINING_OR_INJURY_MANAGEMENT
NO_BETTING_SYSTEM
NO_BASELINE_PERMADEATH
NO_COMEBACK_COUNT_ARTISTRY_GROWTH
NO_REPLACEMENT_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_COMEBACK_OR_RETIREMENT
NO_COMEBACK_FARMING_MULTIPLIER
PRODUCT_IMPLEMENTATION_BLOCKED
TASK3_IMPLEMENTATION_NOT_APPROVED
P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED
```

## Adversarial decision report

1. **Cassia reskin** — Kyle는 current-match item fit이 아니라 keep/retire-replace continuity를 소유한다. `MUST_FIX`.
2. **Noble01 treatment overlap** — 복원 깊이는 기존 owner에 남긴다. `MUST_FIX`.
3. **Sentimental auto-best** — 오래된 작품은 hard gate와 실제 evidence를 우회하지 못한다. `MUST_FIX`.
4. **New-item auto-best** — 새 작품도 자동 정답이 아니다. `MUST_FIX`.
5. **Legacy score resurrection** — fixed Kyle/iron_sword score 공식은 historical fixture다. `MUST_FIX`.
6. **UID/history overwrite** — replacement는 old UID/history를 보존하고 new UID를 만든다. `MUST_FIX`.
7. **Fake history unlock** — 실제 prior record 없이 continuity를 만들지 않는다. `MUST_FIX`.
8. **Gladiator RPG drift** — direct combat/roster/training/injury management를 추가하지 않는다. `MUST_FIX`.
9. **Lineage stat creep** — lineage state는 정보/결과 관계이며 power system이 아니다. `MUST_FIX`.
10. **Progression farming** — 반복 comeback/retirement/replacement로 Artistry/Chronicle 자동 성장이 없다. `MUST_FIX`.
11. **Result collapse** — Kyle comeback 결과와 equipment continuity 판단을 별도 축으로 유지한다. `MUST_FIX`.
12. **Taxonomy hijack** — P1 BS-CT-06 ambiguity는 별도 승인까지 deferred다. `MUST_FIX`.

## Acceptance

- `BS-CONTENT-20260811-09 / GLADIATOR_02 / KYLE_VAREN / VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION`가 R3–R7 `9/10` planning Decision이 된다.
- Decisions01–08은 승인 역사로 보존한다.
- 실제 prior Kyle item record가 continuity branch의 근거다.
- hard eligibility/serviceability가 sentiment보다 먼저다.
- keep path는 same UID를 보존한다.
- replacement path는 old UID/history를 보존하고 distinct new UID를 사용한다.
- old history/progression을 new UID로 복사하지 않는다.
- Cassia의 arena-fit 책임과 Noble01의 treatment-depth 책임을 침범하지 않는다.
- legacy Kyle/iron_sword fixed data와 score formula를 현재 canon으로 승격하지 않는다.
- 직접 전투·roster/guild·training/injury management·betting·baseline permadeath를 추가하지 않는다.
- comeback/replacement 반복으로 Artistry/Chronicle을 자동 성장시키지 않는다.
- P1 taxonomy ambiguity를 해결하지 않는다.
- 제품 구현은 `BLOCKED`다.
- Task3 구현은 `NOT_APPROVED`다.
- 사람 플레이테스트·Android 실기기·접근성 검증은 실제 실행 전까지 `NOT_RUN`이다.
