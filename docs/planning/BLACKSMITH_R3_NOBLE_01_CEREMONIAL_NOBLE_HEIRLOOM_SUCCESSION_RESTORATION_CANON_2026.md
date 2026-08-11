# Blacksmith R3 Noble 01 — Ceremonial Noble Heirloom Succession Restoration Canon

## Authority

- Decision: `BS-CONTENT-20260811-06`
- Content ID: `NOBLE_01`
- Customer: `CEREMONIAL_NOBLE`
- Customer archetype: `NOBLE`
- Activity family: `HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY`
- R3–R7 approval slot: `6/10`
- Work mode: `PLANNING_ONLY`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`

이 정본은 기존 Vertical Slice가 이미 사용하는 `ceremonial_noble` 대표 고객을 첫 귀족 상세 콘텐츠로 승격한다. 새 이름·가문·귀족 정치 설정을 발명하지 않는다.

```text
EXISTING_CEREMONIAL_NOBLE_REPRESENTATIVE_REUSED
NO_NEW_NAMED_NOBLE_LORE_IN_DECISION06
```

## Core promise

```text
기존 가보 UID + 계승 의식 목적 공개
→ 현재 손상·과거 수리·소유·계보·연대기 증거 확인
→ 어떤 흔적을 남기고 어디까지 개입할지 판단
→ 기존 수리·복원·재작업 권위 안에서 처치
→ 같은 UID 인계
→ 계승 의식은 비직접 세계 사건으로 해결
→ CEREMONY_READINESS_STATE
 + HEIRLOOM_TREATMENT_FIT_STATE
 + ITEM_UID_DYNASTIC_LEGACY_STATE
→ 보존·재수리·재사용·전시·후속 계승 판단 이유
```

플레이어의 핵심 선택은 “최대로 새것처럼 만들기”가 아니라 **이 작품의 실제 상태·역사·용도에 비추어 어디까지 손대는가**다.

## Player authority boundary

플레이어는 `BLACKSMITH_HEIRLOOM_TREATMENT_DECISION_MAKER_NOT_HOUSE_OR_CEREMONY_CONTROLLER`다.

할 수 있는 일:

- 같은 가보 UID의 실제 상태와 생애 증거를 읽는다.
- 계승 의식에서 요구되는 상징·기능·착용·제시 맥락을 읽는다.
- 기존 수리·복원·재작업 권위 안에서 개입 깊이를 선택한다.
- 의미 있는 흔적 또는 과거 수리를 남길지, 구조적·기능적 이유로 개입할지 판단한다.
- 같은 UID를 돌려주고 비직접 의식 결과를 받는다.
- 결과를 이후 보존·재수리·사용·전시·재계승 또는 대체 신작 판단으로 환류한다.

다음은 이 Decision의 코어가 아니다.

- 직접 계승 의식 미니게임
- 귀족 가문 경영
- 궁정 정치·외교 경영
- 상속인·계승 후보 전략 게임
- 손님 배치·행사 연출 경영

```text
NO_DIRECT_CEREMONY_MINIGAME
NO_NOBLE_HOUSE_MANAGEMENT
NO_COURT_OR_DIPLOMACY_MANAGEMENT
```

## Existing evidence only

Decision06은 새 `진품성`, `가문 위신`, `계승 점수`, `복원도` 원수치를 만들지 않는다. 판단은 현재 정본이 실제로 소유한 정보에서만 가져온다.

사용 가능한 증거 예:

- 현재 손상·상태와 기존 수리·복원 이력
- 주재료·구조·제작 등급·예술성
- 실제 관련이 있을 때의 승인된 수식어·기능·역할 속성
- 같은 UID의 소유·증여·계승·전시·사용 provenance
- 같은 UID에 이미 기록된 구체적 Chronicle·생애 사건
- 이번 의식에서 공개된 기능·상징·착용·제시 목적

다음 새 총점은 만들지 않는다.

```text
NO_HOUSE_PRESTIGE_SCORE
NO_AUTHENTICITY_TOTAL_SCORE
NO_SUCCESSION_TOTAL_SCORE
```

## Contextual intervention depth

개입 깊이는 하나의 글로벌 단계표나 최적화 점수가 아니다. 실제 UID의 상태와 공개된 용도에 따라 여러 선택이 방어 가능해야 한다.

- 의미 있는 흠집·과거 수리가 provenance 증거라면 남기는 선택이 타당할 수 있다.
- 구조적 안전·기능 준비가 필요한 의식이라면 더 강한 수리나 복원이 타당할 수 있다.
- 외관상 새것처럼 보이게 하는 최대 개입이 항상 최선은 아니다.
- 아무것도 하지 않는 것이 언제나 최선도 아니다.
- 가장 높은 `ARTISTRY`의 가보 또는 가장 오래된 가보가 자동 정답이 아니다.

```text
NO_FULL_RESTORATION_ALWAYS_BEST
NO_HIGHEST_ARTISTRY_ALWAYS_BEST
```

## History-preservation contract

`NO_HISTORY_ERASURE_ON_REPAIR`.

수리·복원은 현재 물리 상태를 바꿀 수 있지만, 같은 UID에 이미 존재하는 의미 있는 과거 수리·소유·계승·손상·복원·Chronicle provenance를 조용히 삭제하지 않는다.

- 물리적 흔적을 실제 처치로 줄이거나 제거하는 선택이 있더라도 “그 사건이 존재했다”는 생애 기록은 남는다.
- 과거 수리 흔적을 보존하는 것과 과거 수리 기록을 보존하는 것은 구분한다.
- 새 가보 객체로 교체하거나 generic `RESTORED_VERSION` UID로 복제하지 않는다.

## Result contract

```text
CEREMONY_READINESS_STATE
HEIRLOOM_TREATMENT_FIT_STATE
ITEM_UID_DYNASTIC_LEGACY_STATE
```

- `CEREMONY_READINESS_STATE`: 공개된 계승 의식·기능 맥락에 작품이 어느 상태로 참여했는지.
- `HEIRLOOM_TREATMENT_FIT_STATE`: 선택한 개입 깊이가 실제 상태·역사·용도에 얼마나 방어 가능했는지.
- `ITEM_UID_DYNASTIC_LEGACY_STATE`: 같은 UID의 가문·계승 생애에 어떤 처치와 사건이 남았는지.

성공적인 의식이 곧 최적 처치였음을 의미하지 않는다. 반대로 의식의 일부 결과가 좋지 않아도 역사 보존 판단이 잘못이었다고 자동 단정하지 않는다.

결과 화면은 세 축을 하나의 퍼센트·별점·위신 수치로 합치지 않고, 실제 UID와 공개 맥락에서 가져온 구체적 원인 2~4개와 하나의 주요 다음 행동 이유를 보여준다.

## Same-UID lifecycle

`SAME_ITEM_UID_PRESERVED`.

처치 전·처치 후·의식 중·반환 후 모두 같은 작품 UID다. 현재 권위가 표현 가능한 범위에서 수리·복원 기록, 보존한 흔적, 상태 변화, 새 손상, 계승 provenance가 같은 작품 생애에 연결된다.

## Artistry and Chronicle boundaries

가보 복원과 계승 의식은 무료 성장 행동이 아니다.

- 복원 횟수만으로 `ARTISTRY`가 증가하지 않는다.
- 의식 횟수만으로 `ARTISTRY`가 증가하지 않는다.
- 계승 성공만으로 `CHRONICLE_AFFIX`를 자동 부여하지 않는다.
- 복원했다는 사실만으로 `CHRONICLE_AFFIX`를 자동 부여하지 않는다.
- 기존 Chronicle 권위가 충분히 의미 있는 구체 사건을 판정할 때만 그 사건과 같은 UID에 연결한다.
- 반복 복원·의식에 자동 파밍 배율을 만들지 않는다.

```text
NO_RESTORATION_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_CEREMONY_OR_RESTORATION
NO_RESTORATION_FARMING_MULTIPLIER
```

## Information contract

처치 전 정보 계층은 다음을 보여준다.

- 선택된 가보 UID
- 공개된 의식 목적과 hard requirement
- 현재 상태·손상·과거 수리·관련 provenance
- 개입 선택을 지지하거나 충돌하는 이유 2~4개
- 자동 `BEST` 처치 추천 없음

처치·의식 뒤에는 세 결과 축, 구체적 원인 2~4개, 하나의 주요 다음 행동 이유를 보여준다. 핵심 상태를 색상만으로 전달하지 않는다.

정확한 문구·처치 임계값·경제값·보상·일정·결과 분포는 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## Collector 01 separation

Ersa Roen의 `COLLECTOR_01 / EXHIBITION_EVIDENCE_AND_PROVENANCE`는 **이미 존재하는 작품 증거를 어떤 전시 의도에 맞춰 선택·설명할지**를 소유한다.

Noble01은 **계승 전에 이미 생애가 있는 한 작품에 물리적으로 어디까지 개입할지**를 소유한다.

```text
ERSA_OWNS_EXHIBITION_EVIDENCE_SELECTION
NOBLE01_OWNS_HEIRLOOM_INTERVENTION_DEPTH
NO_COLLECTOR01_OWNER_COLLISION
```

## Protected boundaries

```text
NO_FULL_RESTORATION_ALWAYS_BEST
NO_HIGHEST_ARTISTRY_ALWAYS_BEST
NO_HOUSE_PRESTIGE_SCORE
NO_AUTHENTICITY_TOTAL_SCORE
NO_SUCCESSION_TOTAL_SCORE
NO_HISTORY_ERASURE_ON_REPAIR
NO_RESTORATION_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_CEREMONY_OR_RESTORATION
NO_RESTORATION_FARMING_MULTIPLIER
SAME_ITEM_UID_PRESERVED
NO_DIRECT_CEREMONY_MINIGAME
NO_NOBLE_HOUSE_MANAGEMENT
NO_COURT_OR_DIPLOMACY_MANAGEMENT
EXISTING_CEREMONIAL_NOBLE_REPRESENTATIVE_REUSED
NO_NEW_NAMED_NOBLE_LORE_IN_DECISION06
BLACKSMITH_HEIRLOOM_TREATMENT_DECISION_MAKER_NOT_HOUSE_OR_CEREMONY_CONTROLLER
PRODUCT_IMPLEMENTATION_BLOCKED
TASK3_IMPLEMENTATION_NOT_APPROVED
```

## Adversarial decision report

1. **Collector overlap** — Ersa는 전시 증거 선택, Noble01은 가보 처치 깊이 판단으로 소유권을 분리한다. `MUST_FIX`.
2. **Prestige/authenticity score drift** — 새 가문 위신·진품성·계승 총점을 만들지 않는다. `MUST_FIX`.
3. **Full-restoration dominance** — 물리 상태·역사·선언된 용도에 따라 최소/강한 개입 모두 방어 가능하게 한다. `MUST_FIX`.
4. **Preserve-every-mark dogma** — 구조 안전이나 기능 목적이 실제로 요구하면 개입을 허용한다. `MUST_FIX`.
5. **History erasure** — 물리 흔적 변경과 역사 기록 삭제를 구분하고 UID 생애 기록을 보존한다. `MUST_FIX`.
6. **Progression farming** — 복원/의식 횟수로 Artistry·Chronicle·배율을 자동 성장시키지 않는다. `MUST_FIX`.
7. **UID replacement** — 처치 전후와 의식 결과 모두 같은 UID를 권위로 유지한다. `MUST_FIX`.
8. **Noble-management drift** — 의식은 비직접 사건이며 가문·궁정·외교 경영을 추가하지 않는다. `MUST_FIX`.
9. **Full conservation laboratory** 요구는 현재 Blacksmith의 작품 선택·생애 코어를 벗어나므로 `REJECTED_CRITIQUE`.

## Acceptance

- `BS-CONTENT-20260811-06 / NOBLE_01 / CEREMONIAL_NOBLE / HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY`가 R3–R7 `6/10` 현재 기획 Decision이 된다.
- Decisions01–05는 승인 이력으로 보존한다.
- 기존 `ceremonial_noble` 대표 fixture를 재사용하고 새 이름·가문 lore를 만들지 않는다.
- 결과는 `CEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE` 세 축으로 분리한다.
- 같은 UID와 기존 생애·provenance가 권위다.
- 최대 복원·최고 Artistry를 자동 정답으로 만들지 않는다.
- 가문 위신·진품성·계승 총점을 만들지 않는다.
- 과거 생애 기록을 수리 과정에서 삭제하지 않는다.
- 복원·의식 반복으로 Artistry 또는 Chronicle Affix를 자동 성장시키지 않는다.
- 직접 의식·가문·궁정·외교 경영을 추가하지 않는다.
- 제품 구현과 Task3 구현 Gate는 열리지 않는다.
