# BS-ENHANCE-20260828-34 · +10 무기 키워드 귀속

> [대체됨] Recurring Precision cadence, collection cardinality/stage, migration, and tag-growth timing are now owned exclusively by `BS-ENHANCE-20260830-38_RECURRING_PRECISION_TAG_EVOLUTION.md`. This Decision retains only weapon recipient, three-affix taxonomy, and player-title exclusion evidence; it is not a competing current Tag cadence owner.

```text
STATUS = USER_APPROVED_CURRENT
DECISION_DATE = 2026-08-28
DECISION_SOURCE = USER_CLARIFICATION_IN_IMPLEMENTATION_CONTRACT_REVIEW
BENCHMARK = NOT_APPLICABLE / DIRECT_USER_CORRECTION_OF_EXISTING_OWNERSHIP_SEMANTICS
FIELD_OWNER = WEAPON_KEYWORD_OWNERSHIP
FIELD_PRECEDENCE = OVERRIDES_INTEGRATED_CORE_CANON_WHEN_KEYWORD_OWNERSHIP_FIELDS_CONFLICT
CONTENT_AND_EMPTY_SELECTION_OWNER = BS-ENHANCE-20260829-37
ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY
ITEM_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX
PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10
WEAPON_KEYWORD_CONTENT_ID = DATA_BACKED_FIRST_TAG_CATALOG / BS-ENHANCE-20260829-37
HISTORICAL_FIXTURE_OR_CUSTOMER_EPITHET_REUSE = FORBIDDEN
WEAPON_KEYWORD_TAXONOMY = GRADE_KEYWORD / TAG_KEYWORD / EVENT_KEYWORD
GRADE_KEYWORD_MACHINE_OWNER = GRADE_AFFIX
TAG_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX
EVENT_KEYWORD_MACHINE_OWNER = CHRONICLE_AFFIX
+10_PRECISION_OUTPUT_KEYWORD = TAG_KEYWORD
TAG_KEYWORD_SOURCE = CATALYST_LINEAGE_AND_PRECISION_METHOD
TAG_KEYWORD_RESOLUTION = CATALYST_LINEAGE_AND_PRECISION_METHOD_GOVERN_TAG_IDENTITY
PRECISION_METHOD_EFFECT_SCOPE = WEAPON_STATS_DURABILITY_AND_TAG_RESOLUTION_CONTEXT
PRECISION_METHOD_TAG_ROLE = TAG_IDENTITY_RESOLUTION
PRECISION_METHOD_CANNOT_AFFECT_GRADE_OR_EVENT_KEYWORD = TRUE
EMPTY_CATALYST_LINEAGE_BEHAVIOR = BLOCK_BEFORE_COST_OR_ROLL
NO_DEFAULT_LINEAGE = TRUE
PRECISION_SELECTION_PERSISTENCE = ATTEMPT_LOCAL_ONLY
NO_NEW_STORED_FIELD_OR_FOURTH_AFFIX_SLOT = TRUE
```

## 결정

성공한 `+9 -> +10` 정밀강화는 작품의 `CATALYST_AFFIX`에 정확히 하나의
**태그 키워드**를 기록한다. 이 키워드는 플레이어 자신에게 귀속되는 칭호나
능력치가 아니며, 무기의 정체성과 이후 같은 UID 생애 기록을 위한 정보다.

태그 키워드의 정체성은 **촉매 계보와 정밀강화 방식의 조합**이 결정한다.
유효한 촉매 계보가 태그의 후보 가족·계보 범위를, 정밀강화 방식이 그 범위
안에서의 태그 해석 문맥을 함께 소유한다. 방식은 무기 능력치·내구도에도
영향을 줄 수 있지만, 등급·사건 키워드를 생성·변경·대체하지 않는다.

플레이어 칭호 콘텐츠는 이후 별도 콘텐츠로 존재할 수 있으나, 이 Slice의
`+10` 성공으로 생성·지급·표시하지 않는다.

## 무기 키워드 분류 · 사용자 확인 2026-08-28

무기에는 정확히 다음 세 종류의 키워드가 있다. 이것은 새 data field나 네
번째 affix 슬롯을 만드는 변경이 아니라, 이미 저장·직렬화되는 세 독립
affix field의 플레이어 언어와 생성 원인을 명확히 하는 정정이다.

| 플레이어 언어 | 저장 machine owner | 생성 원인 | 불변 경계 |
| --- | --- | --- | --- |
| 등급 키워드 | `GRADE_AFFIX` | 최초 제작 등급 | UID 출생 후 변경하지 않는다. |
| 태그 키워드 | `CATALYST_AFFIX` | 촉매 계보 + 정밀강화 방식 | `+9 -> +10` 성공은 정확히 하나의 태그 키워드만 기록한다. 두 입력의 조합이 태그 정체성을 결정한다. |
| 사건 키워드 | `CHRONICLE_AFFIX` | 의미 있는 실제 사용·사건·손상·복원 등 작품 생애 | 모든 handoff·표시·사건이 자동으로 부여하지는 않는다. |

따라서 `+10`의 결과는 태그 키워드이지 사건 키워드·등급 키워드·플레이어
칭호가 아니다. 구형 문서의 `촉매 수식어`와 `연대기 수식어`는 각각 이
태그 키워드와 사건 키워드의 저장 owner를 가리키는 기술 용어로만 유지한다.

## 범위와 금지

- `+10` 태그 키워드는 정확히 하나이며 네 번째 affix 슬롯을 만들지 않는다.
- 실제 content ID·표시 문구·2×2 계보×방식 표와 빈 선택 흐름은
  `BS-ENHANCE-20260829-37` 및
  `BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`이 소유한다. 역사 fixture나
  예전 고객 이명을 자동 재사용하지 않는다.
- 계보 또는 방식이 비어 있으면 `+10` 시도는 비용·재료·굴림 전에 막힌다.
  기본 계보는 없고, 선택은 attempt-local이다. 성공 시에만 composite Tag가
  기존 `CATALYST_AFFIX`에 기록된다.
- 정밀강화 방식은 무기 능력치·내구도와 태그 identity resolution에만
  영향을 준다. 등급·사건 키워드를 생성·변경·대체하거나 기능 재작업·예술성·
  환경 기능을 산출하는 방식 효과는 current canon이 아니다.
- 일반 강화, `+20` 이후 milestone, 확률, 비용, 수리, 고객 피해 profile에
  새 효과를 추가하지 않는다.
- generic keyword가 고객 실제사용 피해를 보편적으로 경감하지 않는다.

## 정본 영향

- `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- `docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md`
- `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`

## 검증 계약

- `+10` 성공은 item-owned `CATALYST_AFFIX` 하나만 쓴다.
- 태그 identity는 촉매 계보와 정밀강화 방식의 조합으로만 해석한다.
- 플레이어 title/칭호 필드, 보상, UI를 생성하지 않는다.
- Decision37 catalog 이외의 값과 historical
  `PRECISION_KEYWORD_PENDING_CONTENT`를 플레이어에게 노출하지 않는다.
