# Blacksmith 반복 정밀강화 태그 진화 설계

```text
STATUS = USER_APPROVED_DIRECTION / SPEC_REVIEW_PENDING
DESIGN_DATE = 2026-08-30
PROPOSED_DECISION_ID = BS-ENHANCE-20260830-38
SCOPE = CURRENT_CANON_AMENDMENT / TAG_GROWTH_ONLY
USER_DIRECTION = EVERY_10_LEVEL_PRECISION_ADD_OR_UPGRADE_TAGS
APPROVED_MODEL = MAX_3_ACTIVE_TAGS / TAG_STAGE_I_TO_IV
PRODUCT_IMPLEMENTATION = NOT_STARTED_FOR_THIS_AMENDMENT
```

## 1. Purpose and current-authority change

Blacksmith의 정밀강화는 `+9 -> +10` 한 번의 태그 부여로 끝나지 않는다.
모든 10단위 도달 시도(`+9 -> +10`부터 `+99 -> +100`까지)는 정밀강화이며,
성공할 때 플레이어는 같은 작품 UID의 태그를 **추가**하거나 기존 태그 하나를
**강화**한다. 이 변화는 같은 무기가 만든 선택을 누적해 기억하게 하되,
강화의 중심 질문인 `STOP OR PUSH`와 세 affix 슬롯 구조를 보존한다.

사용자 승인 뒤 이 사양이 대체할 활성 필드는 다음과 같다.

| Existing owner | Replaced field | New meaning |
| --- | --- | --- |
| `BS-ENHANCE-20260825-25` | `+9 -> +10 = PRECISION_ENHANCEMENT` 및 `+10` 단일 태그 cardinality | `PRECISION_TARGETS = [10,20,30,40,50,60,70,80,90,100]`; 각 성공은 하나의 태그 추가 또는 강화 |
| `BS-ENHANCE-20260828-34` | `+10` 성공은 정확히 하나의 태그만 기록 | `CATALYST_AFFIX`가 하나의 태그 계보판을 소유하며, 최대 세 태그의 ID·단계·생성 이정표를 기록 |
| `BS-ENHANCE-20260829-37` | entry 9/target 10 only, non-empty affix block, no new stored field | 첫 +10의 2×2 입력·빈 선택 차단은 보존하고, 이후 모든 정밀 이정표에서 명시적인 추가/강화 선택을 연다. 단일 문자열 저장 형식은 versioned record로 마이그레이션한다. |

다음은 유지한다.

```text
SUCCESS_LEVEL_DELTA = +1
NO_MULTI_LEVEL_SUCCESS = TRUE
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX = ONLY_AFFIX_OWNERS
ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY
FAILURE_OUTCOMES = SUCCESS / FAILED_HOLD / FAILED_DAMAGE
FAILED_DAMAGE_REPLACES_FAILED_HOLD = TRUE
NO_DOWNGRADE = TRUE
DURABILITY_AUTHORITY = CURRENT_MAX_BASE_MAX_NUMERIC
NO_CATALYST_INVENTORY_OR_CONSUMPTION = TRUE
NO_RANDOM_TAG_REROLL_OR_UNRELATED_REPLACEMENT = TRUE
```

`+10` 단일 정밀강화, +20 이후 미재개, 단일 문자열 태그, no-new-field
문구는 이 승인 범위에서 `[대체됨]`으로 표시한다. 과거 R2의 촉매 계보
진화 구조는 참고 근거로만 재사용하며, 그 시기의 보조재료, 기능 재작업,
예술성 효과, 환경 기능, 무작위 촉매 확률, 구형 내구도 수치와 실패 규칙은
복원하지 않는다.

## 2. Player-facing model

### 2.1 Precision targets

```text
PRECISION_TARGETS = 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
PRECISION_ENTRY = current_enhancement_level == target_level - 1
PRECISION_SUCCESS = one level increase + exactly one tag-growth action
```

각 대상은 여전히 하나의 강화 시도다. 강화 성공은 정확히 `+1`만 올린다.
`+11` 이후에는 현행 Decision28/29의 실패·손상 확률이 적용되며, 정밀강화
여부는 확률·비용·내구도·수리 권위를 새로 만들거나 수정하지 않는다.

### 2.2 One CATALYST_AFFIX, not a fourth affix slot

`CATALYST_AFFIX`는 여전히 무기 하나에 귀속된 **하나의** affix owner다.
이 owner 안에 최대 세 개의 활성 태그를 가진 계보판을 저장한다. `GRADE_AFFIX`와
`CHRONICLE_AFFIX`는 byte-for-byte 보존한다.

```text
CATALYST_AFFIX
  ├─ tag_entries: maximum 3
  │    └─ tag_id + stage + created_milestone + last_advanced_milestone
  └─ initial-tag backfill state when applicable

used_precision_milestones
  └─ the sole persisted list of successfully resolved precision targets
```

태그 하나는 다음 네 단계 중 하나다.

```text
I   = SEED      / 씨앗
II  = DEVELOPED / 성장
III = EVOLVED   / 진화
IV  = MASTERED  / 완성
```

같은 `tag_id`를 두 번 추가할 수 없다. 기존 태그는 강화만 가능하며,
무관한 태그로 기존 태그를 교체하지 않는다. 세 태그가 모두 IV에 도달해도
총 태그 성장 수용량은 12회라서 최대 10회의 정밀강화보다 작아지지 않는다.

### 2.3 Growth choice at every successful Precision attempt

각 정밀 이정표는 비용·재료 차감·확률 굴림 전에 다음 중 정확히 하나를
선택해야 한다. `ADD_TAG`에서는 새 태그를 해석하기 위해 계보와 방식을
고르고, `UPGRADE_TAG`에서는 이미 저장된 tag ID가 계보와 방식을 해석하므로
강화할 태그 하나만 고른다.

| Action | Availability | Success result |
| --- | --- | --- |
| `ADD_TAG` | 활성 태그가 3개 미만이고 선택한 태그 ID가 아직 없을 때 | 선택한 태그를 `SEED I`로 추가하고 해당 방식 효과를 한 번 적용 |
| `UPGRADE_TAG` | 선택한 활성 태그가 I~III일 때 | 선택한 태그를 다음 단계로 올리고 그 태그의 방식 효과를 한 번 더 적용 |

첫 `+9 -> +10`에서는 `ADD_TAG`만 허용한다. 기존 Decision37의 두 입력,
불씨/모루 계보와 날 세우기/경량 담금은 첫 태그의 2×2 후보로 그대로 쓴다.
후속 이정표에서도 모든 후보는 catalog가 명시한 호환 태그만 표시한다. 기본
계보, 임의 태그, 숨은 확률, 자동 선택은 없다.

후속 `ADD_TAG`에서 현재 첫 catalog의 서로 다른 태그는 서로 호환되는
후보로 취급한다. 향후 catalog에 비호환성이나 분기 규칙을 넣을 경우에는,
이미 보유한 태그를 없애거나 바꾸지 않고 **새 태그 추가 후보만** 제한한다.

### 2.4 Effects and balance boundary

첫 catalog의 효과 크기는 그대로 유지한다.

```text
EDGE_REINFORCEMENT = RAW_ROLE_STAT +3
LIGHTWEIGHTING = WEIGHT_POINT -3 / floor 0
DURABILITY_DELTA = 0
```

태그를 추가하거나 강화할 때마다, 선택한 태그의 `method_id`가 소유한
현재 효과를 정확히 한 번 적용한다. 따라서 I~IV 단계는 효과 누적 횟수와
작품의 읽을 수 있는 성장 이력을 나타내며, 같은 방법으로 이미 적용된 효과를
재계산하거나 두 배로 곱하지 않는다.

`LIGHTWEIGHTING`은 현재 무게가 0이면 실제 변화가 없으므로 선택 후보에서
제외한다. 플레이어가 수치 변화 없는 태그 성장을 비용·확률과 교환하지 않게
하기 위한 fail-closed 규칙이다. `RAW_ROLE_STAT`에는 별도 상한을 만들지 않는다.

이 `+3 / -3`은 현행 catalog의 `TEMP_TEST_BUDGET` 효과값으로 유지한다. 이
설계는 수치를 최종 밸런스로 선언하지 않는다. 구현 전과 후에 목표 +10/+20/
+50/+100 도달 분포, 3개 태그와 IV 단계 분포, 무게 0 도달률, 손상/복구 후
계속 시도율을 고정 시드 시뮬레이션과 사람 플레이테스트로 검증한다.

## 3. Resolution, failure, and edge cases

### 3.1 Pre-roll gate

다음 중 하나라도 참이면 정밀강화는 비용·보강재·확률 굴림 전에 차단된다.

```text
TARGET_NOT_PRECISION_MILESTONE
MISSING_TAG_GROWTH_ACTION
ADD_TAG: MISSING_CATALYST_LINEAGE
ADD_TAG: MISSING_PRECISION_METHOD
ADD_TAG: INVALID_PRECISION_TAG_COMBINATION
ADD_TAG: TAG_ALREADY_ACTIVE
ADD_TAG: TAG_CAPACITY_REACHED_FOR_ADD
UPGRADE_TAG: TAG_NOT_ACTIVE_FOR_UPGRADE
UPGRADE_TAG: TAG_ALREADY_MASTERED
LIGHTWEIGHTING_HAS_NO_MECHANICAL_CHANGE
PRECISION_MILESTONE_ALREADY_RESOLVED
```

### 3.2 Outcomes

| Outcome | Enhancement level | Tag collection | Effect | Milestone state |
| --- | --- | --- | --- | --- |
| `SUCCESS` | target까지 정확히 `+1` | `ADD_TAG` 또는 `UPGRADE_TAG` 결과를 한 번 기록 | 한 번 적용 | 해당 target을 resolved로 기록 |
| `FAILED_HOLD` | 변하지 않음 | 변하지 않음 | 적용하지 않음 | 미해결; 다시 선택 후 재시도 가능 |
| `FAILED_DAMAGE` | 변하지 않음 | 변하지 않음 | 적용하지 않음 | 미해결; 현재 Decision29 damage 후 다시 선택 가능 |
| `BLOCKED` | 변하지 않음 | 변하지 않음 | 적용하지 않음 | 비용·굴림 모두 없음 |

정밀 선택은 실패·차단 후 저장되지 않는다. 후속 시도에서 새롭게 선택해야 한다.
성공한 해당 target의 선택·결과만 같은 UID의 append-only ledger에 남긴다.
태그 추가/강화 성공은 `ROUTINE_ENHANCEMENT_HISTORY` 예외로서 하나의 의미 있는
태그 성장 사건이므로 Player Chronicle에 읽기 좋은 축약 기록을 남길 수 있다.
실패 클릭은 Chronicle에 기록하지 않는다.

### 3.3 Existing save migration

`VSItem.SCHEMA_VERSION`은 V3에서 V4로 올린다. V4 loader는 다음처럼
결정적으로 전환한다.

| V3 input | V4 CATALYST_AFFIX result | Required preservation |
| --- | --- | --- |
| 빈 문자열 | 빈 tag collection | Grade, Chronicle, stats, durability, ledger 보존 |
| catalog에 있는 단일 tag ID + level >= 10 | 해당 ID의 `SEED I`, `created_milestone=10`, `used_precision_milestones`에 10 | 기존에 이미 적용된 +3/-3을 다시 적용하지 않음 |
| `PRECISION_KEYWORD_PENDING_CONTENT` | initial-tag pending state | 기존 무상 backfill 선택을 한 번 제공; 정정 전에는 후속 정밀강화를 차단 |
| 알 수 없는 비어 있지 않은 문자열 | fail-closed unreadable catalyst state | 자동 덮어쓰기·효과 적용·정밀 재개 금지 |

V3의 `used_precision_milestones`가 비어 있어도, 알려진 V3 태그가 있고 level이
10 이상이면 성공한 첫 정밀강화였다는 기존 계약으로 `10`을 보완한다. 마이그레이션은
idempotent여야 하며, 저장/로드나 재시작으로 태그·효과·ledger가 중복되지 않는다.

## 4. Data, UI, and runtime boundaries

### 4.1 Data contract

기존 `BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`은 새 versioned catalog로
대체한다. 다음의 정본 데이터가 필요하다.

```text
precision_targets: [10,20,30,40,50,60,70,80,90,100]
max_active_tags: 3
max_tag_stage: 4
tag_id
lineage_id
method_id
display_name_ko
stage_display_names_ko
effect.axis
effect.delta
compatible_tag_ids
```

`used_precision_milestones`는 성공한 target 목록의 유일한 persisted source of
truth다. `CATALYST_AFFIX.tag_entries`의 생성/마지막 강화 이정표는 각 태그의
생애 설명을 위한 값이며, target 소비 여부를 독립적으로 다시 소유하지 않는다.
loader/validator는 태그 이정표가 `used_precision_milestones`에 포함되는지만
검증한다.

### 4.2 Workshop screen

정밀 target에서는 `VSWorkshopScreen`에 다음 순서의 native Control flow를
표시한다.

```text
1. 현재 강화 target과 현재 1~3개 태그 / 각 단계
2. 추가 또는 강화 action 선택
3. action에 맞는 유효 태그 카드 또는 OptionButton
4. 선택 뒤의 태그 단계, 수치 전후, 내구도 변화 없음,
   성공/유지/손상 확률, 비용, 보강재
5. 확인 버튼
6. 결과 후 같은 화면에서 갱신된 태그 계보판
```

`ADD_TAG`와 `UPGRADE_TAG`는 같은 화면의 두 큰 버튼으로 시작한다. 각 태그는
이름·계보·I~IV 단계·다음 효과를 한 줄로 보여 주며, 탭 영역은 세로 Android
한 손 입력에 맞게 48dp 이상으로 설계한다. 새 raster 이미지나 가짜 GDD
스크린샷은 필요하지 않다. 실제 native Workshop consumer만 확장한다.

### 4.3 Phase-1 boundary

현재 Phase-1 대표 플레이는 +0~+15이므로 실제 첫 세션에서 +10만 체험한다.
그 경계는 유지한다. Resolver, save migration, catalog, automated test는 모든
target 10~100을 지원하지만, +20 이상을 보여 주기 위해 고객/경제/콘텐츠를
조작하거나 빠른 진행을 강제하지 않는다.

회복 체크포인트 `[10, 30, 60, 90]`와 정밀 target 목록은 다른 개념이다.
정밀강화가 +20, +40, +50 등에 생긴다고 회복 floor나 가격 밴드가 자동으로
바뀌지 않는다.

## 5. Acceptance contract and tests

구현은 RED -> GREEN -> REFACTOR 순서로 다음 계약을 보호한다.

1. `9 -> 10`, `19 -> 20`, …, `99 -> 100`만 정밀 입력을 요구하고, 일반 target은 요구하지 않는다.
2. 첫 +10은 정확히 한 태그를 I로 추가하며, Grade/Event fields를 변경하지 않는다.
3. 이후 이정표마다 활성 태그 수 3 미만이면 새 고유 태그 추가가 가능하다.
4. 활성 태그는 I~III에서만 한 단계 강화되며 IV에서는 강화 대상이 될 수 없다.
5. 성공 하나는 tag stage/effect/milestone/ledger를 각각 한 번만 바꾼다.
6. Hold, damage, blocked, save/reload, repeated resolver call은 tag/effect/milestone 중복을 만들지 않는다.
7. V3 known tag, pending placeholder, unknown nonempty string을 각기 정의된 V4 상태로 안전하게 전환한다.
8. 모든 target에서 Decision28 exact probability와 Decision29 durability modifier, repair authority, level `+1`을 그대로 유지한다.
9. Workshop view는 정밀 target에서만 action selector와 유효 후보를 표시하고, 선택이 없으면 confirm을 비활성화한다.
10. catalog validator는 10개 target, 3개 cap, IV stage, unique tags, catalog compatibility, no new Grade/Event mutation을 검증한다.

자동 테스트 성공은 contract/implementation evidence일 뿐 Android device,
접근성, 성능, 사람 플레이테스트 PASS를 뜻하지 않는다.

## 6. Research and adversarial disposition

| Source / risk | Disposition | Blacksmith application |
| --- | --- | --- |
| Last Epoch의 현재 Forge는 아이템의 지속 제작 상태를 명시적으로 보여 준다. | `ADAPT` | 별도 Forging Potential 자원은 만들지 않고, 태그 1~3개·I~IV 단계·다음 정밀 target을 명확히 보여 준다. |
| Last Epoch의 룬/글리프와 무작위 affix 변경 | `REJECT` | Blacksmith의 태그는 선택 결과로만 추가·강화되며, 무작위 reroll·교체·소모 인벤토리를 만들지 않는다. |
| Android의 복수 입력·접근성 guidance | `ADAPT` | 긴 태그 목록/중첩 다중선택을 피하고, two-step selection과 큰 native controls를 사용한다. |
| 10회 정밀강화의 무한 누적 | `REJECT` | 최대 세 태그와 IV 상한으로 UI·밸런스·저장 복잡도를 제한한다. |

최종 수치와 체감은 자동 테스트로 확정하지 않는다. 시뮬레이션과 실제 세로
Android/사람 플레이 검증 전에는 `TEMP_TEST_BUDGET`으로 남긴다.

## 7. Planned ownership after spec review

사용자가 이 사양을 최종 검토·승인하면 다음 순서로 반영한다.

1. 새 Decision `BS-ENHANCE-20260830-38`과 versioned tag catalog를 current field owner로 추가한다.
2. integrated Core Canon, Decision34, Decision37, Phase-1 implementation contract, active handoff, human-facing GDD, AI production spec의 충돌 문구를 `[대체됨]` 또는 새 contract로 교정한다.
3. RED tests를 먼저 추가하고 V4 save migration, precision resolver, action service, Workshop screen을 구현한다.
4. GUT/Python contracts, Godot runtime, PDF render/readback, protected-path audit를 실행한다.
5. `BLACKSMITH_HUMAN_FACING_GDD_20260828.md`와 파생 Human Game Blueprint PDF에 태그 계보판·정밀 흐름·장면 계약·성공/실패/복구 분기를 사람용으로 반영한다.

기존 미커밋 GDD/PDF 변경, `.base-contract/`, `tmp/`, PR #196은 이 작업의
소유물이 아니며 변경하거나 병합 단위로 흡수하지 않는다.
