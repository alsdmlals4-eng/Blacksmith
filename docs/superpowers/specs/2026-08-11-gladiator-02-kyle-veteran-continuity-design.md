# Blacksmith R3 Gladiator 02 — Kyle Varen Veteran Comeback Equipment Continuity Design

## Decision status

- Decision: `BS-CONTENT-20260811-09`
- Content ID: `GLADIATOR_02`
- Customer: `KYLE_VAREN / 카일 바렌`
- Activity family: `VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION`
- Target R3–R7 approval slot: `9/10`
- Direction status: `USER_APPROVED_DIRECTION`
- Work mode: `PLANNING_ONLY`
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`
- Human playtest: `NOT_RUN`
- Android device validation: `NOT_RUN`
- Accessibility validation: `NOT_RUN`

이 문서는 사용자가 승인한 Decision09 방향의 written design spec이다. 아직 `CURRENT_CONFIRMED_DECISIONS.md`, `CURRENT_R3_R7_CANON_REGISTRY.json`, Google Sheet의 current pointer를 9/10으로 승격하지 않는다. written-spec review와 이후 implementation-plan/TDD/canonization Gate를 통과한 뒤에만 current canon으로 materialize한다.

## Work-start authority snapshot

이 spec 작성 직전 fresh preflight 기준:

- Base `main`: `23d5b292f619022cdd8ab7a33fb1debc2d294861`
- Blacksmith `main`: `80b35b9fc914853428e991c4130edc87dd260083`
- Blacksmith latest main decision: `BS-CONTENT-20260811-08 / R3_R7_8_OF_10`
- open mergeable same-goal Kyle/Decision09 branch: 없음
- open project PR: `#81` reference-only archive, merge 대상 아님
- Google Sheet current: `R3_R7_8_OF_10`, next `R3_R7_9_OF_10_USER_PLANNING_DECISION_REQUIRED`
- Sheet Kyle: `KYLE_VAREN / 검투사 유형 추가 고객·구형 PoC 계승`
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED` 유지

GitHub와 Google Sheet 사이에 Decision08 current 상태 충돌은 없다.

## Goal

Kyle를 Cassia의 두 번째 버전으로 만들지 않고, Blacksmith가 이미 만든 작품의 **현역 지속 여부와 교체 책임**을 판단하게 만드는 두 번째 검투사 상세 콘텐츠로 정의한다.

플레이어 판타지는 다음 한 문장으로 고정한다.

> 오래 함께했다는 이유로 계속 쓰는 것도, 새것이라는 이유로 갈아타는 것도 아니다. 이 작품의 실제 현재 상태와 살아온 기록을 보고, 다시 현역을 맡길지 역사를 보존하고 다음 작품으로 넘길지를 내가 결정한다.

이 콘텐츠의 핵심 재미는 `strongest-item selection`이 아니라 `continuity versus replacement responsibility`다.

## Existing authority and reuse

새 고객이나 새 검투사 시스템을 만들지 않는다.

재사용하는 현행 자산:

- `KYLE_VAREN`
- legacy customer identity `gladiator_kyle`
- legacy PoC item fixture `iron_sword`
- 기존 item UID / ownership / provenance / lifecycle / repair / restoration / Chronicle 기록
- 기존 고객 공통 handoff/result 구조
- 기존 non-direct world-event 구조
- 기존 repair/restoration owner
- 기존 Cassia `GLADIATOR_01` 책임 경계

legacy fixture의 존재는 역사 증거다. 그 고정 값과 점수식은 Decision09의 현재 권위가 아니다.

## Responsibility boundaries

### Cassia / GLADIATOR_01

질문:

> 이번 공개 경기 맥락에 어떤 실제 작품이 설명 가능하게 적합한가?

Cassia는 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`를 소유한다.

### Kyle / GLADIATOR_02

질문:

> 이미 실제 생애가 있는 이 작품을 다시 현역으로 맡길 것인가, 아니면 그 작품의 역사를 보존한 채 새 작품에 다음 역할을 맡길 것인가?

Kyle는 `VETERAN_RETURN_STATE / EQUIPMENT_CONTINUITY_STATE / ITEM_UID_LINEAGE_STATE`를 소유한다.

### Noble01 / CEREMONIAL_NOBLE

질문:

> 이 기존 가보 UID를 계승 목적에 맞게 물리적으로 어디까지 수리·복원·재작업할 것인가?

Noble01은 treatment depth를 소유한다.

### Ersa / COLLECTOR_01

질문:

> 이 작품의 실제 증거 중 공개 전시에 무엇을 강조할 것인가?

### Sedric / COLLECTOR_02

질문:

> 이 정확한 UID의 provenance/custody가 장기 기록 보관 인계를 설명할 수 있는가?

Decision09는 이 네 책임을 가져오지 않는다.

## Meaning of `SUCCESSION`

Decision09 activity family의 `SUCCESSION`은 귀족 가문 계승이나 치료 깊이를 뜻하지 않는다.

여기서 `equipment succession`은 다음만 뜻한다.

- 기존 작품이 계속 현역이면 같은 UID를 계속 사용한다.
- 기존 작품을 현역에서 물리면 그 UID와 역사를 그대로 보존한다.
- 교체 작품은 반드시 별도의 새 UID다.
- 두 작품 사이에 후계 관계를 보여줄 필요가 있으면 기존 event/provenance/Chronicle reference가 표현 가능한 범위에서만 연결한다.
- 과거 작품의 성능, enhancement, affix, Artistry, Chronicle, provenance를 새 UID에 복사하지 않는다.

따라서 `SUCCESSION`은 새로운 power system, lineage stat, dynasty system을 뜻하지 않는다.

## Activation contract

Decision09의 continuity 판단은 실제 과거 작품 증거가 있을 때만 열린다.

최소 활성 조건:

1. `KYLE_VAREN`이 현재 고객으로 존재한다.
2. Kyle에게 과거에 실제로 인계된 작품 UID 또는 승인된 migration으로 연결된 실제 legacy record가 존재한다.
3. comeback 목적 또는 현재 장비 역할이 플레이어에게 공개된다.

실제 과거 작품 기록이 없으면 과거를 생성해서 Decision09를 강제로 활성화하지 않는다.

```text
NO_FABRICATED_KYLE_HISTORY
NO_FAKE_LEGACY_ITEM_FOR_CONTENT_UNLOCK
```

새 캠페인에서 Kyle가 처음 등장하는 경우 standard customer request는 가능하지만, `VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION`의 continuity 분기는 실제 이전 인계 이후에만 의미를 가진다.

정확한 방문 순서·회차·기간은 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## Player flow

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

경기나 comeback을 직접 조작하지 않는다.

## Hard gate before sentiment

오래 사용했다는 감정은 hard eligibility보다 앞서지 않는다.

현행 item owner가 이미 제공하는 실제 상태를 우선 읽는다.

허용되는 hard evidence 예시:

- item 존재 여부
- `BROKEN_OR_LOST` 등 현행 lifecycle state
- 실제 current durability/state
- 공개된 현재 요청의 equipment category/role eligibility
- 현재 사용에 직접 관련된 기존 손상·수리 상태

Decision09를 위해 새 `SAFETY_SCORE`, `SERVICEABILITY_SCORE`, `VETERAN_SCORE`를 만들지 않는다.

기존 작품이 hard gate를 통과하지 못하면 `KEEP_IN_SERVICE`는 선택 불가능할 수 있다. 이것은 “새 작품이 항상 더 좋다”는 뜻이 아니라 현재 실제 상태가 현역 사용을 허용하지 않는다는 뜻이다.

## Contextual continuity evidence

hard gate를 통과한 뒤 continuity 판단은 실제 존재하는 정보만 소비한다.

허용되는 evidence family:

- 현재 durability/lifecycle state
- 기존 enhancement level
- 현재 공개 역할에 실제 관련된 기존 raw attributes
- 기존 approved special function/affix 중 이번 역할에 실제 관련된 것
- 과거 소유·인계 provenance
- 과거 손상·수리·복원 기록
- Kyle와 해당 UID 사이의 실제 사용 기록
- 승인된 arena/lifecycle/Chronicle 사건
- 동일 작품이 현재 comeback 요구와 얼마나 연속적으로 맞는지 설명할 수 있는 실제 기록

다음은 단독 정답 근거가 아니다.

- 가장 오래된 작품
- 가장 높은 enhancement
- 가장 높은 Artistry
- 가장 많은 Chronicle event
- 가장 비싼 작품
- 가장 높은 legacy PoC score
- Kyle와의 관계 수치 자체

```text
NO_OLD_ITEM_ALWAYS_BEST
NO_NEW_ITEM_ALWAYS_BEST
NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST
NO_HIGHEST_ARTISTRY_ALWAYS_BEST
NO_MOST_CHRONICLE_ALWAYS_BEST
NO_SENTIMENT_SCORE
NO_VETERAN_TOTAL_SCORE
```

## Defensible choice contract

hard gate 이후에는 두 선택이 모두 상황에 따라 방어 가능해야 한다.

### KEEP_IN_SERVICE

가능한 정당화 예시:

- 실제 상태가 현역 사용에 충분하다.
- 현재 comeback 역할과 실제 작품 기능이 잘 맞는다.
- 기존 Kyle 사용 이력이 현재 요구를 설명 가능하게 지지한다.
- 유지의 의미가 단순 감상이 아니라 실제 continuity evidence와 연결된다.

### RETIRE_AND_REPLACE

가능한 정당화 예시:

- 기존 작품은 사용할 수 있지만 현재 comeback 역할과 맞지 않는다.
- 상태 열화·기존 수리 이력이 현재 위험과 충돌한다.
- 과거에는 좋은 선택이었지만 이번 요구가 달라졌다.
- 기존 작품을 더 이상 위험에 노출하지 않고 그 실제 역사를 보존하는 판단이 합리적이다.

새 작품이 자동으로 강한 선택이 아니며, 오래된 작품도 자동으로 감성 보너스를 받지 않는다.

자동 `BEST` 추천은 제공하지 않는다.

## Repair and restoration ownership

Decision09는 “어디까지 수리/복원할 것인가”를 새로 설계하지 않는다.

필요한 repair/restoration은 기존 owner의 결과를 읽거나 기존 작업으로 넘긴다.

Kyle의 고유 질문은 treatment 이후에도 남는다.

```text
NOBLE01_OR_EXISTING_REPAIR_OWNER = HOW_FAR_TO_TREAT
KYLE_GLADIATOR02 = CONTINUE_IN_SERVICE_OR_RETIRE_AND_REPLACE
```

Decision09가 별도의 `COMEBACK_RESTORATION_DEPTH`, `VETERAN_REPAIR_SCORE`, `RETIREMENT_REPAIR_TREE`를 만들지 않는다.

## UID continuity and replacement contract

### Keep path

```text
OLD_UID -> KEEP_IN_SERVICE -> SAME_UID
```

- 같은 UID를 유지한다.
- 과거 provenance/lifecycle/Chronicle를 그대로 이어간다.
- comeback result는 같은 UID의 다음 실제 사건이 될 수 있다.

### Replace path

```text
OLD_UID -> RETIRED_FROM_THIS_ROLE
NEW_UID -> NEW_EQUIPMENT_ROLE
OLD_UID != NEW_UID
```

- 기존 UID를 새 UID로 rename하지 않는다.
- 기존 UID를 삭제하지 않는다.
- 새 작품에 옛 UID의 역사나 progression을 복사하지 않는다.
- 기존 작품은 inventory/archive/exhibition/other approved lifecycle owner가 허용하는 후속 판단으로 남을 수 있다.
- 새 작품은 자기 제작 provenance부터 시작한다.

```text
NO_UID_REWRITE
NO_HISTORY_TRANSFER_TO_REPLACEMENT
OLD_ITEM_HISTORY_PRESERVED
NEW_ITEM_GETS_NEW_UID
```

## `ITEM_UID_LINEAGE_STATE` boundary

`ITEM_UID_LINEAGE_STATE`는 power score가 아니다.

목적은 결과 화면과 후속 소비자가 다음 사실을 구분할 수 있게 하는 것이다.

- 기존 UID가 계속 현역인지
- 기존 UID가 이번 역할에서 은퇴했는지
- 새 UID가 후속 장비로 선택되었는지
- 실제로 두 작품 사이에 어떤 사건 reference가 기록되었는지

다음을 만들지 않는다.

- `LINEAGE_POWER`
- `SUCCESSION_SCORE`
- `VETERAN_LEGACY_SCORE`
- 이전 작품의 enhancement/affix/stat inheritance
- 자동 bonus inheritance

실제 event reference를 저장하는 구체적 schema는 product implementation Gate에서 Existing Solution First로 결정한다. 이 planning Decision이 새 글로벌 lineage subsystem을 선승인하지 않는다.

## Result contract

세 결과 축을 하나의 총점으로 합치지 않는다.

```text
VETERAN_RETURN_STATE
EQUIPMENT_CONTINUITY_STATE
ITEM_UID_LINEAGE_STATE
```

### VETERAN_RETURN_STATE

Kyle의 comeback/world event 자체가 어떻게 진행됐는지 나타낸다.

작품만으로 모든 결과를 설명하지 않는다.

### EQUIPMENT_CONTINUITY_STATE

선택한 keep/replace 판단이 공개된 comeback 목적과 실제 작품 상태·역사에 어떻게 맞았는지 나타낸다.

경기 승패와 동일하지 않다.

### ITEM_UID_LINEAGE_STATE

기존 UID와 필요 시 새 UID가 어떤 실제 lifecycle 관계를 갖게 되었는지 나타낸다.

정확 enum/state distribution은 테스트 프리셋이며 현재 확정하지 않는다.

## Causality contract

결과는 다음을 지켜야 한다.

- 실제 원인 2~4개
- 주 후속 행동 1개
- 결과 축별 의미 분리
- item이 sole cause라고 주장하지 않음
- Kyle의 career/comeback outcome과 equipment decision quality를 동일시하지 않음

가능한 원인 family:

- hard serviceability/eligibility
- current role fit
- actual durability/lifecycle history
- relevant prior Kyle use evidence
- actual repair/restoration history
- new item fit when replacement path selected

`win = correct item` 또는 `loss = wrong item`으로 축약하지 않는다.

## Follow-up actions

주 후속 행동은 기존 승인된 시스템으로만 연결한다.

예:

- same UID continued-service repair
- 기존 repair/restoration 검토
- follow-up enhancement 판단
- old UID preservation
- Ersa exhibition 후보
- Sedric archival review 후보
- 새 replacement 작품 제작
- 다음 Kyle request 준비

Decision09 자체가 archive/exhibition/restoration 결과를 자동 확정하지 않는다.

## Legacy Kyle migration boundary

현재 저장소의 historical fixture:

- customer id `gladiator_kyle`
- equipment id `iron_sword`
- fixed required/stretch enhancement levels
- fixed preferred affix list
- fixed deadline/report delay
- fixed payment/fame/relationship values
- grade/attack weighted score
- `DEFEAT / WIN / DECISIVE_WIN` score bands

이 값들은 Decision09 정본으로 승격하지 않는다.

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

재사용할 수 있는 것은 고유 역사와 구조적 강점이다.

- 실제 legacy customer relation이 있으면 `KYLE_VAREN`에 보존 가능한 migration evidence로 취급
- transaction/event/registry identity strength
- delivered item UID history
- result/handoff lifecycle 구조

실제 migration schema와 save compatibility 처리는 제품 구현 Gate에서 별도 검증한다. 이 planning spec만으로 legacy save migration을 실행했다고 주장하지 않는다.

## Cassia separation

Kyle를 Cassia arena fit의 재스킨으로 만들지 않는다.

Cassia:

```text
CURRENT MATCH CONTEXT
-> WHICH REAL ITEM FITS THIS MATCH?
```

Kyle:

```text
REAL PRIOR ITEM HISTORY + CURRENT CONDITION
-> KEEP THIS ITEM IN SERVICE OR RETIRE/REPLACE IT?
```

Decision09 결과의 중심에 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE`를 다시 복제하지 않는다.

## Direct combat and management boundary

다음은 scope 밖이다.

- 직접 arena combat
- Kyle 이동/행동 명령
- fighter tactics
- gladiator roster
- guild/team management
- training management
- injury-management RPG
- recruitment/replacement roster loop
- betting
- arena economy management
- baseline permadeath

```text
BLACKSMITH_EQUIPMENT_CONTINUITY_DECISION_MAKER_NOT_GLADIATOR_CONTROLLER
NO_DIRECT_ARENA_COMBAT
NO_GLADIATOR_ROSTER_OR_GUILD_MANAGEMENT
NO_TRAINING_OR_INJURY_MANAGEMENT
NO_BASELINE_PERMADEATH
NO_BETTING_SYSTEM
```

## Progression and farming boundary

comeback·retirement·replacement 자체가 무료 성장원이 아니다.

- comeback 횟수로 Artistry 자동 증가 없음
- keep 선택 횟수로 Artistry 자동 증가 없음
- replacement 횟수로 Artistry 자동 증가 없음
- retirement 사실만으로 Chronicle Affix 자동 부여 없음
- comeback 사실만으로 Chronicle Affix 자동 부여 없음
- old→new lineage reference만으로 gameplay bonus 없음
- repeated comeback farming multiplier 없음

```text
NO_COMEBACK_COUNT_ARTISTRY_GROWTH
NO_REPLACEMENT_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_COMEBACK_OR_RETIREMENT
NO_LINEAGE_POWER_BONUS
NO_COMEBACK_FARMING_MULTIPLIER
```

기존 Chronicle authority가 충분히 의미 있는 구체 사건을 Chronicle로 판정할 때만 그 사건을 실제 UID에 연결한다.

## Information contract

### Before decision

최소한 다음을 서로 다른 정보층에서 읽을 수 있어야 한다.

- Kyle comeback 목적
- 현재 요구 equipment category/role
- 실제 prior Kyle item UID
- hard eligibility/serviceability
- 실제 관련 상태·lifecycle evidence
- continuity를 지지하는 이유
- continuity와 충돌하는 이유
- replacement 후보가 있다면 해당 새 작품의 실제 증거

### Decision

명시적 행동:

- `이 작품을 다시 현역으로 맡긴다`
- `이 작품은 이번 역할에서 물리고 새 작품을 맡긴다`

정확 UI copy는 현재 비권위다.

### After result

- `VETERAN_RETURN_STATE`
- `EQUIPMENT_CONTINUITY_STATE`
- `ITEM_UID_LINEAGE_STATE`
- 실제 원인 2~4개
- 주 후속 행동 1개
- old/new UID가 함께 존재하면 둘을 혼동하지 않는 표시

색상만으로 keep/retire/result를 전달하지 않는다.

## Benchmark dispositions

### ADAPT — veteran continuity tension

오래된 숙련 자산을 계속 유지할지 교체할지 고민하게 만드는 외부 사례의 tension만 차용한다.

Blacksmith에서는 사람 roster가 아니라 **작품 lifecycle 책임**으로 변환한다.

### ADAPT — equipment inspection before reuse

감성/이력보다 실제 current condition과 eligibility를 hard gate로 먼저 본다.

새 안전 총점을 만들지 않고 기존 item state를 사용한다.

### AVOID — gladiator/team career management

검투사 팀·육성·전술·부상·경제·직접 전투를 가져오지 않는다.

### AVOID — legacy Blacksmith score resurrection

기존 `gladiator_kyle / iron_sword` PoC의 fixed score formula는 historical fixture로만 남긴다.

## Adversarial failure cases

1. **Cassia reskin**
   - 실패: Kyle도 단순히 이번 경기의 최적 무기를 고른다.
   - 방어: Kyle owner는 keep/retire-replace continuity다.
   - 판정: `MUST_FIX`.

2. **Noble01 treatment overlap**
   - 실패: Kyle가 복원 깊이를 선택한다.
   - 방어: repair/restoration depth는 기존 owner에 남긴다.
   - 판정: `MUST_FIX`.

3. **Old item sentimental auto-best**
   - 실패: 오래 쓴 작품에 hidden nostalgia bonus를 준다.
   - 방어: hard gate + actual evidence only.
   - 판정: `MUST_FIX`.

4. **New item power-creep auto-best**
   - 실패: 새 작품이면 항상 우월하다.
   - 방어: current role fit와 actual condition/history를 설명 가능하게 비교한다.
   - 판정: `MUST_FIX`.

5. **Legacy score resurrection**
   - 실패: +5/+10/affix/grade/attack score를 Decision09 current canon으로 사용한다.
   - 방어: historical fixture only.
   - 판정: `MUST_FIX`.

6. **UID/history overwrite**
   - 실패: replacement가 old UID 또는 old Chronicle/provenance를 그대로 상속한다.
   - 방어: old UID preserved, new UID new history.
   - 판정: `MUST_FIX`.

7. **Fake history for new players**
   - 실패: continuity 콘텐츠를 열기 위해 존재하지 않는 Kyle 과거 작품을 자동 생성한다.
   - 방어: actual prior record required.
   - 판정: `MUST_FIX`.

8. **Gladiator RPG drift**
   - 실패: 부상·훈련·roster·직접 전투를 만든다.
   - 방어: off-screen world event and blacksmith authority.
   - 판정: `MUST_FIX`.

9. **Lineage stat creep**
   - 실패: old→new 관계를 새 power/stat tree로 만든다.
   - 방어: `ITEM_UID_LINEAGE_STATE` is informational/result relation only.
   - 판정: `MUST_FIX`.

10. **Progression farming**
    - 실패: comeback/retirement/replacement 반복으로 Artistry/Chronicle 자동 성장.
    - 방어: event significance remains with existing authority.
    - 판정: `MUST_FIX`.

11. **Result collapse**
    - 실패: comeback 성공을 곧바로 item decision 정답으로 본다.
    - 방어: veteran return and equipment continuity separate axes.
    - 판정: `MUST_FIX`.

12. **Taxonomy scope hijack**
    - 실패: Decision09에서 `BS-CT-06 고객 4유형×8명` ambiguity를 몰래 재정의한다.
    - 방어: P1 deferred stays deferred.
    - 판정: `MUST_FIX`.

## P1 taxonomy ambiguity

Decision09는 다음 기존 모호성을 해결하지 않는다.

```text
P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED
```

`BS-CT-06`은 역사적으로 고객 4유형×8명을 기록하지만 현재 상세 설계에는 Noble이 별도 책임으로 존재한다.

Kyle/GLADIATOR_02 상세화는 이 taxonomy를 재분류하는 승인으로 해석하지 않는다.

10/10 또는 별도 승인된 whole-taxonomy/world-integration Decision에서만 해결한다.

## Exact-value policy

다음은 현재 canon 수치가 아니다.

- comeback unlock timing
- required equipment category distribution
- hard durability threshold
- replacement threshold
- deadline
- reward
- relationship delta
- economy value
- result distribution
- Chronicle trigger frequency
- visit/revisit cadence

모두:

```text
NON_CANONICAL_BASELINE_TEST_PRESET
USER_PLAYTEST_REQUIRED
```

legacy PoC 숫자를 초기값으로 자동 복원하지 않는다.

## Playtest contract

실제 사람 플레이테스트 전에는 `NOT_RUN`이다.

향후 검증할 핵심 질문:

1. 플레이어가 Cassia의 “이번 경기 적합”과 Kyle의 “계속 사용/교체”를 구분하는가?
2. 플레이어가 오래된 작품을 감정 때문에 자동 선택하지 않고 hard condition을 먼저 읽는가?
3. `KEEP_IN_SERVICE`와 `RETIRE_AND_REPLACE`가 둘 다 상황에 따라 방어 가능한 선택으로 느껴지는가?
4. replacement 선택 시 old UID history가 사라졌다고 오해하지 않는가?
5. 새 UID가 old UID progression을 상속하지 않는다는 점을 이해하는가?
6. 결과의 세 축을 하나의 승패/점수로 오해하지 않는가?
7. 후속 제작·보존·수리 판단 이유가 생기는가?

행동 관찰과 neutral recall을 함께 사용한다. 자기보고만으로 성공을 판정하지 않는다.

## Expected before / after

### Before

- Kyle는 이름과 legacy PoC 관계만 있는 추가 고객이다.
- historical fixture는 `gladiator_kyle / iron_sword`와 fixed score 중심이다.
- Cassia가 검투사 상세 책임을 사실상 단독 소유한다.
- 작품의 “계속 현역인가, 은퇴하고 새 작품으로 넘어가는가”는 상세 콘텐츠 owner가 없다.

### After canonization

- Kyle가 `GLADIATOR_02`의 독립 책임을 가진다.
- legacy history는 보존하지만 fixed PoC formula는 current canon으로 부활하지 않는다.
- old item continuity와 replacement가 실제 상태·역사 기반의 설명 가능한 대장장이 선택이 된다.
- keep path는 같은 UID를 더 오래 살리고, replace path는 old UID history를 보존하면서 새 UID의 새로운 생애를 시작한다.
- Cassia/Noble01/Ersa/Sedric 책임이 침범되지 않는다.
- 8명 이름 고객 전체가 상세 책임을 갖게 되는 9/10 기반이 완성된다.

## Acceptance criteria

Decision09 canonization 단계는 아래를 모두 만족해야 한다.

- [ ] `BS-CONTENT-20260811-09 / GLADIATOR_02 / KYLE_VAREN / VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION` canon 문서가 존재한다.
- [ ] current R3 registry와 current confirmed decisions가 D09 / `9/10`을 가리킨다.
- [ ] Decisions01–08은 승인 역사로 보존된다.
- [ ] Kyle와 `gladiator_kyle` legacy relation을 역사/migration evidence로 구분한다.
- [ ] `iron_sword`, fixed +5/+10, preferred affix, fixed day/economy, legacy score formula가 non-authoritative로 명시된다.
- [ ] `VETERAN_RETURN_STATE / EQUIPMENT_CONTINUITY_STATE / ITEM_UID_LINEAGE_STATE`가 독립 결과 축이다.
- [ ] old item hard gate가 sentiment보다 먼저다.
- [ ] old item always-best와 new item always-best를 둘 다 금지한다.
- [ ] keep path에서 same UID를 보존한다.
- [ ] replacement path에서 old UID history를 보존하고 new UID를 만든다.
- [ ] old history/progression을 new UID로 복사하지 않는다.
- [ ] Cassia arena-fit 책임이 보존된다.
- [ ] Noble01 treatment-depth 책임이 보존된다.
- [ ] Ersa exhibition 책임과 Sedric archival responsibility가 보존된다.
- [ ] direct arena combat, roster/guild/training/injury management, betting, baseline permadeath가 없다.
- [ ] comeback/replacement/retirement count로 Artistry 또는 Chronicle Affix가 자동 성장하지 않는다.
- [ ] P1 `BS-CT-06` taxonomy ambiguity가 별도 승인 없이 해결되지 않는다.
- [ ] semantic RED를 current 8/10 상태에서 먼저 확인한다.
- [ ] RED는 syntax/import/YAML/infrastructure failure가 아니라 D09/current 9/10 부재 때문에 실패한다.
- [ ] 최소 planning-only materialization 뒤 focused D09 contract가 GREEN이다.
- [ ] stale moving-current consumers는 역사 assertion을 보존한 채 9/10으로 이동한다.
- [ ] relevant D01–D08 historical contracts가 regression GREEN이다.
- [ ] Python/Godot/Base/BCA/GUT/HiGodot/Adapter required gates가 하나의 exact reviewed head에서 GREEN이다.
- [ ] Base `POST_CHANGE_MONITOR_LOOP`가 unresolved blocker 없이 닫힌다.
- [ ] same-goal open/recent PR과 untouched consumer 재검토가 완료된다.
- [ ] merged-main exact readback이 PASS다.
- [ ] Google Sheet에 정확히 같은 `BS-CONTENT-20260811-09`가 sync되고 readback된다.
- [ ] product implementation은 계속 `BLOCKED`다.
- [ ] Task3는 계속 `NOT_APPROVED`다.
- [ ] human playtest / Android device / accessibility는 실제 실행 전까지 `NOT_RUN`이다.

## Non-goals

Decision09는 다음을 승인하지 않는다.

- 제품 코드 구현
- Task3
- save migration 실행
- 새로운 combat simulation
- 새로운 gladiator career subsystem
- 새로운 injury system
- 새로운 lineage power/stat system
- BS-CT-06 taxonomy resolution
- 10/10 whole-batch closure
- exact economy/balance values

## Next gate

이 written spec을 사용자가 review한 뒤 변경이 없다고 승인해야 implementation plan을 작성할 수 있다.

그 다음 계획 단계에서만:

```text
implementation plan
→ semantic RED
→ planning canon/current materialization
→ focused GREEN
→ stale-current/historical consumer regression
→ adversarial POST_CHANGE_MONITOR_LOOP
→ exact-head CI
→ PR merge
→ postmerge readback
→ same-ID Google Sheet sync/readback
```

으로 진행한다.
