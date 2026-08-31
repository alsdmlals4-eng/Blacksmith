# BS-ENHANCE-20260901-40 · 소모형 정밀강화 촉매 자원

> 현재 결정: 사용자 승인된 **불의 심장 / 대지의 결정**을 실제 정밀강화 자원으로 사용한다. 이 문서는 Decision38의 태그 성장 cadence·cardinality·stage를 대체하지 않는다. 대신 `lineage_id` 입력, 무재고·무소모 금지, 그리고 그에 따른 UI/저장 필드만 **부분 대체**한다.

```text
STATUS = USER_APPROVED_CURRENT
DECISION_DATE = 2026-09-01
FIELD_OWNER = CONSUMABLE_PRECISION_CATALYST_RESOURCES
FIELD_PRECEDENCE = PARTIALLY_SUPERSEDES_BS-ENHANCE-20260830-38_FOR_CATALYST_INPUT_INVENTORY_CONSUMPTION_AND_RESOURCE_MIGRATION
CATALOG_OWNER = docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json / SCHEMA_V3
ITEM_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX
PRECISION_SELECTION_PERSISTENCE = ATTEMPT_LOCAL_ONLY
NO_FOURTH_AFFIX_SLOT = TRUE
NO_DEFAULT_RANDOM_REROLL_OR_REPLACEMENT = TRUE
NO_NEW_INVENTORY_SCREEN = TRUE
```

## 1. 현재 촉매 표

| catalog ID | 저장 재고 키 | 플레이어 표기 | 연결 태그 | 시도당 소모 |
| --- | --- | --- | --- | --- |
| `HEART_OF_FLAME` | `heart_of_flame` | **불의 심장** | `TAG_EMBER_EDGE`, `TAG_EMBER_LIGHT` | `1` |
| `EARTH_CRYSTAL` | `earth_crystal` | **대지의 결정** | `TAG_ANVIL_EDGE`, `TAG_ANVIL_LIGHT` | `1` |

태그 ID, 방식 ID, `CATALYST_AFFIX`의 최대 세 태그/I~IV stage, ten-target cadence와 방식 효과(`RAW_ROLE_STAT +3`, `WEIGHT_POINT -3`, durability `0`)는 Decision38의 기존 권위를 보존한다. 촉매는 태그의 외형 등급이나 새 affix가 아니며, 일반 강화와 별도 드롭·상점·판매·랜덤 경제를 만들지 않는다.

## 2. 선택·차감·저장 원자성

```text
ADD_TAG = ONE_EXPLICIT_CATALYST_ID + ONE_EXPLICIT_METHOD_ID
UPGRADE_TAG = ONE_EXPLICIT_TAG_ID / CATALYST_DERIVED_FROM_STORED_TAG
MISSING_PRECISION_CATALYST = BLOCK_BEFORE_COST_OR_ROLL
INSUFFICIENT_PRECISION_CATALYST = BLOCK_BEFORE_COST_OR_ROLL_OR_SAVE
NORMAL_RESOLVED_ATTEMPT = GOLD + COMMON_REINFORCEMENT_MATERIAL + REQUIRED_CATALYST_ONE_UNIT
SUCCESS / FAILED_HOLD / FAILED_DAMAGE = CONSUME_REQUIRED_CATALYST_ONE_UNIT
SAVE_FAILED = RESTORE_ALL_STAGED_RESOURCES_AND_ITEM_STATE
LEGACY_INITIAL_TAG_BACKFILL = ZERO_COST_ZERO_CATALYST_ZERO_ROLL
```

`ADD_TAG` 선택은 `{ "action": "ADD_TAG", "catalyst_id": "HEART_OF_FLAME", "method_id": "EDGE_REINFORCEMENT" }`처럼 정확히 두 ID를 받는다. `UPGRADE_TAG`은 `{ "action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE" }`처럼 태그만 받고 catalog에서 해당 촉매를 역산한다. 선택은 성공 전 저장하지 않으며, 빈 촉매/방식, 모르는 ID, 재고 부족, 불가능한 tag action은 실제 roll, save, live resource mutation 전에 막는다.

골드·보강재·촉매는 동일한 candidate save envelope에서 먼저 stage한다. 정상 결과가 저장되면 후보 재고를 live workshop resource에 반영한다. 저장에 실패하면 item, tag, ledger, gold, 보강재, 촉매 모두 종전 상태다. 따라서 실패 보류·실패 손상은 태그 효과를 남기지 않아도 **시도 비용인 촉매 1개**를 소비한다.

## 3. V4 → V5 resource migration

```text
SAVE_ENVELOPE_SCHEMA = V5
NEW_CAMPAIGN_STARTER_ALLOCATION = heart_of_flame:64 / earth_crystal:64
V4_MIGRATION_WHEN_BOTH_KEYS_ABSENT = GRANT_64_EACH_ONCE
V5_REOPEN = PRESERVE_STORED_QUANTITIES_NO_REGRANT
V4_EXACTLY_ONE_KEY_ABSENT = FAIL_CLOSED_VALIDATION_ERROR
MALFORMED_OR_NEGATIVE_QUANTITY = FAIL_CLOSED_VALIDATION_ERROR
STARTER_ALLOCATION = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

64는 각 촉매가 연결한 두 태그가 IV까지 가능한 최대 8회 성공에 대해, hard guarantee 이전 최대 7회 보류와 성공 한 번을 모두 소모해도 progression을 촉매만으로 막지 않는 vertical-slice 테스트 상한이다. 이는 가격·획득처·경제 밸런스를 확정하지 않는다.

## 4. 대체·보존 표

| 원본 | 상태 | Decision40 이후 의미 |
| --- | --- | --- |
| Decision38 `lineage_id` / `lineages` | **[부분 대체됨]** | catalog V3의 `catalyst_id` / `catalysts`; 태그 성장 규칙은 보존 |
| Decision38 `NO_CATALYST_INVENTORY_OR_CONSUMPTION` | **[부분 대체됨]** | 기존 workshop resource snapshot 안에서 두 촉매를 보유·1개 소모 |
| Decision37의 첫 2×2 태그·empty pre-roll gate | 역사 evidence 보존 | 촉매+방식 입력 또는 derived upgrade 촉매의 pre-roll gate |
| Decision28/29/30/31/32 | 변경 없음 | 확률, damage, durability, repair, economy 진실값은 그대로 |
| Decision34 세 affix / weapon-only recipient | 변경 없음 | 촉매 재고는 새 affix·title·item field가 아님 |

## 5. 조사 반영과 범위 경계

`docs/superpowers/specs/2026-09-01-precision-catalyst-resource-design.md`의 11개 현행 대장간/강화 게임 조사에서, 재료의 명확한 정체성·즉시 비용 표기·결과 후 소모 피드백은 **ADOPT**, 복잡한 제작 체인과 별도 상점은 현재 single-workshop slice에 맞게 **REJECT**했다. 이는 Blacksmith의 `STOP OR PUSH`와 같은 UID 태그 성장만 강화하며, 확률·수리·등급·고객 사건의 값을 벤치마크에서 가져오지 않는다.

## 6. 완료 증거 경계

기계 정본/catalog contract, save migration GUT, resolver/action-service GUT, Workshop GUT, exact-head runtime screenshot은 서로 다른 증거다. Android, accessibility, performance, human playtest, release 및 실제 재획득 경제는 이 결정만으로 PASS가 되지 않으며 실행 전까지 `NOT_RUN`이다.
