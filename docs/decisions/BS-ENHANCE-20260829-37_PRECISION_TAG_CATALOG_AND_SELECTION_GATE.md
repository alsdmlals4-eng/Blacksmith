# BS-ENHANCE-20260829-37 · 정밀강화 태그 표와 선택 Gate

> [대체됨] Target-10-only, one resolved string Tag, and no-new-stored-field claims are replaced by `BS-ENHANCE-20260830-38_RECURRING_PRECISION_TAG_EVOLUTION.md`. Decision37 retains historical evidence for the first 2×2 불씨/모루 × 날 세우기/경량 담금 catalog and the empty-selection pre-roll gate only.

```text
STATUS = USER_APPROVED_CURRENT
DECISION_DATE = 2026-08-29
DECISION_SOURCE = USER_APPROVAL_OF_RECOMMENDED_CURRENT_CANON_CONTRACT
FIELD_OWNER = FIRST_PRECISION_TAG_CATALOG_AND_SELECTION_GATE
IMPLEMENTATION_ISSUE = #326
FIELD_PRECEDENCE = OVERRIDES_BS-ENHANCE-20260828-34_ONLY_FOR_TAG_CONTENT_AND_EMPTY_SELECTION_FIELDS
TAG_CATALOG_OWNER = BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json
ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY
ITEM_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX
NO_NEW_STORED_FIELD_OR_FOURTH_AFFIX_SLOT = TRUE
EMPTY_CATALYST_LINEAGE_BEHAVIOR = BLOCK_BEFORE_COST_OR_ROLL
NO_DEFAULT_LINEAGE = TRUE
PRECISION_SELECTION_PERSISTENCE = ATTEMPT_LOCAL_ONLY
HUMAN_PLAYTEST = DEFERRED_BY_USER / NOT_RUN
```

## 결정

`+9 → +10`의 유일한 정밀강화는 **시도 직전**에 촉매 계보 하나와 정밀강화
방식 하나를 고른다. 둘 다 고르지 않으면 강화 비용·재료 차감·확률 굴림은
시작되지 않는다. 기본 계보, 무명 태그, 무작위 태그는 없다.

첫 Slice에는 공방에서 항상 고를 수 있지만 소모되지 않는 두 촉매 계보와 두
방식을 제공한다. 이는 촉매 수집/인벤토리/소비 시스템이 아니다. 선택 자체가
태그의 출처를 읽게 하는 짧은 `+9 → +10` 선택이며, 강화의 주 질문인
`STOP OR PUSH`를 대체하지 않는다.

| 입력 | 첫 Slice 승인 내용 | 플레이어에게 보이는 역할 |
| --- | --- | --- |
| 촉매 계보 | `EMBER_LINEAGE` **불씨 계보**, `ANVIL_LINEAGE` **모루 계보** | 태그의 가족과 작품의 완성 분위기 |
| 정밀강화 방식 | `EDGE_REINFORCEMENT` **날 세우기**, `LIGHTWEIGHTING` **경량 담금** | 태그의 표현과 무기에 적용될 수치 변화 |
| 결과 태그 | 두 입력의 고정 2×2 표에서 하나 | 그 무기에만 남는 완성 경로의 이름 |

정밀강화 방식의 영향 범위는 계속 **무기 능력치·내구도·태그 해석 문맥만**이다.
첫 표에는 현재 닫힌 내구도/수리 계약을 덮어쓰지 않기 위해 직접 내구도 변화가
없다(`0`). 이것은 “방식마다 반드시 내구도를 바꿔야 한다”는 뜻이 아니라,
방식이 다른 시스템에 영향을 주지 못한다는 범위 제한이다. 이후 비영(0)이 아닌
내구도 효과는 Decision29/31을 건드리지 않는 별도 승인 없이는 추가하지 않는다.

```text
EDGE_REINFORCEMENT = RAW_ROLE_STAT +3
LIGHTWEIGHTING = WEIGHT_POINT -3 / floor 0
FIRST_CATALOG_DURABILITY_DELTA = 0
FUNCTION_REWORK = FORBIDDEN
ARTISTRY_EFFECT = FORBIDDEN
ENVIRONMENTAL_FUNCTION_EFFECT = FORBIDDEN
GRADE_OR_EVENT_KEYWORD_MUTATION = FORBIDDEN
UNIVERSAL_CUSTOMER_DAMAGE_MITIGATION = FORBIDDEN
```

## 선택·성공·실패 규칙

```text
ENTRY = ITEM_LEVEL_9 / NEXT_TARGET_10
REQUIRED_INPUT = ONE_VALID_LINEAGE + ONE_VALID_METHOD
MISSING_LINEAGE = BLOCKED:MISSING_CATALYST_LINEAGE / BEFORE_COST_OR_ROLL
MISSING_METHOD = BLOCKED:MISSING_PRECISION_METHOD / BEFORE_COST_OR_ROLL
INVALID_PAIR = BLOCKED:INVALID_PRECISION_TAG_COMBINATION / BEFORE_COST_OR_ROLL
SUCCESS = LEVEL_10 + ONE_COMPOSITE_TAG_IN_CATALYST_AFFIX + ONE_METHOD_DELTA_ONCE
FAILED_HOLD = NO_TAG / NO_METHOD_DELTA / CHOICE_NOT_PERSISTED
FAILED_DAMAGE = IMPOSSIBLE_FOR_TARGET_10
RETRY = PLAYER_MAY_SELECT_AGAIN / NO_HIDDEN_SELECTION_LOCK
```

선택은 새 저장 field가 아니다. 실패하면 태그도 방식 효과도 남지 않으며 다음
시도에서 다시 고른다. 성공했을 때만 조합된 태그 ID 하나를 기존
`CATALYST_AFFIX`에 쓴다. 저장된 태그 ID는 표를 통해 계보와 방식을 역으로
해석할 수 있으므로 계보·방식·보류 상태를 별도 field로 중복 저장하지 않는다.

## 기존 임시값 교정

현재 vertical-slice resolver의 `PRECISION_KEYWORD_PENDING_CONTENT`는
역사적 구현 드리프트이며 플레이어 태그가 아니다. pre-release V3 저장에서
이 값이 `+10` 작품에 남아 있다면, `정밀 태그 정정` 한 번을 보여 준다.
플레이어가 위 2×2 중 하나를 선택하면 기존 `CATALYST_AFFIX`를 실제 태그 ID로
한 번만 바꾸고 해당 방식 효과를 한 번 적용한다. 이 정정은 이미 성공한
`+9 → +10`을 다시 굴리거나 비용·재료를 청구하지 않는다. 실제 태그 ID 또는
알 수 없는 비어 있지 않은 값은 fail-closed로 처리해 중복 효과·덮어쓰기를 막는다.

## 대안 검토 · 조사 결론

| 대안 | 플레이어 가치 | 제작·유지비 / 위험 | 판정 |
| --- | --- | --- | --- |
| 2계보 × 2방식, +9에서 명시 선택 | 무기 완성의 출처가 읽히고 선택 부담이 작다 | 표 하나와 기존 `CATALYST_AFFIX`만 사용. 새로운 인벤토리 없음 | **ADOPT** |
| 기본 계보를 자동 부여하고 방식만 고르기 | 빠르지만 촉매 계보가 태그를 정한다는 약속이 흐려진다 | 구현은 짧지만 무명 기본값이 정본을 오염할 수 있음 | **REJECT** |
| 촉매를 획득·소비하는 인벤토리 시스템 | 장기 수집 동기는 생길 수 있다 | 자원·드롭·UI·경제·재진입 범위가 커져 강화 메인을 가림 | **REJECT** |
| 무작위 태그/재굴림 | 순간적 놀라움 | 선택의 출처·같은 UID의 책임을 약화하고 재굴림 경제를 부른다 | **REJECT** |

Shop Titans는 제작·상점·자원·멀티플레이를 결합하는 넓은 운영형 제품이다.
Blacksmith는 그 넓은 루프를 가져오지 않고, 고객의 목적이 무기 생애를 읽게
하는 역할만 남긴다. Moonlighter의 상점/탐험 이중 루프도 복제하지 않는다.
두 비교는 “제작 결과가 다음 맥락을 갖는다”는 원칙만 참고한다.
[Shop Titans 공식 Steam 페이지](https://store.steampowered.com/app/1258080/Shop_Titans/),
[Moonlighter 공식 Steam 페이지](https://store.steampowered.com/app/606150/Moonlighter/)

Godot 구현은 현재 Workshop의 `Control` 기반 레이아웃 안에서 한국어 Label,
두 선택 control, 확인 Button으로 구성한다. Godot의 `OptionButton`은 선택한
항목을 현재 값으로 표시하는 기본 `Control`이며, layout은 `Control`과
Container로 구성한다. 이는 구현 가능성 근거이지 UI·Android·사람 사용성
검증 통과 주장은 아니다. [Godot OptionButton 문서](https://docs.godotengine.org/en/stable/classes/class_optionbutton.html),
[Godot UI 문서](https://docs.godotengine.org/en/stable/tutorials/ui/index.html)

```text
ADOPT = EXPLICIT_2_BY_2_COMPOSITE_TAG_SELECTION
ADAPT = CUSTOMER_CONTEXT_AS_ITEM_LIFECYCLE_ONLY
REJECT = CATALYST_INVENTORY / RANDOM_REROLL / SHOP_TYCOON_SCOPE
DIFFERENTIATOR = ENHANCEMENT_FIRST_DECISION + SAME_UID_LIFECYCLE_MEMORY
```

## 적대적 검토와 경계

1. 태그가 +11 이후의 `STOP OR PUSH`를 대체하지 않는다. +10에서는 한 번의
   짧은 정체성 선택만 하고, 주 위험은 여전히 +11부터다.
2. 방식이 닫힌 내구도·수리 확률을 몰래 바꾸지 않는다. 첫 표의 내구도 변화는
   0이며 보편 고객 피해 경감도 없다.
3. 빈 선택은 비용과 굴림 전에 막히므로 임시 태그·반쪽 성공이 생기지 않는다.
4. 성공 이외에는 tag/stat을 쓰지 않고, historical placeholder 정정도 한 번만
   적용하므로 중복 저장·중복 효과를 막는다.
5. generated mockup이나 새 raster asset은 필요 없다. 실제 Workshop
   `Control` consumer만 확장 후보이며 visual/runtime evidence는 아직 없다.
6. 사람 플레이 검수는 사용자 지시로 이번 구현 계약의 완료 조건이 아니다.
   따라서 재미·Android·접근성·실제 손가락 조작 evidence는 `NOT_RUN`으로
   남고, 자동 계약·GUT·runtime 실행과 혼동하지 않는다.

## 구현·검증 경계

다음 구현은 현재 vertical-slice에만 한정한다.

- `docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`을 읽는
  정밀강화 resolver/UI 경로를 만든다.
- `+9 → +10` preview에서 두 선택·결과 태그·수치 전후·내구도 변화 없음·확률·비용을
  모두 보여 준다.
- 기존 placeholder write를 제거하고, 성공·실패·V3 placeholder backfill의
  단일 적용을 GUT로 검증한다.
- Grade/Event byte-for-byte 보존, no new field/slot, +20 이후 미재개,
  `FUNCTION_REWORK`/예술성/환경 기능 미생성을 자동 계약으로 보호한다.

`data/`, `scripts/`, `scenes/` 변경과 Godot runtime 실행은 별도 현재-canon
구현 작업에서만 한다. 이 Decision은 그 작업의 승인된 계약이며, 구현 완료
증거나 사람 플레이 PASS가 아니다.

```text
BASE_PROMOTION = NO_BASE_PROMOTION
REASON = BLACKSMITH_SPECIFIC_PLUS10_TAG_TAXONOMY_AND_UID_LIFECYCLE
```
