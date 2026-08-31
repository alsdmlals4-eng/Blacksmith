# Blacksmith 소모형 정밀 촉매 자원 설계

```text
STATUS = USER_APPROVED_DIRECTION / SPEC_REVIEW_PENDING
DESIGN_DATE = 2026-09-01
PROPOSED_DECISION_ID = BS-ENHANCE-20260901-40
SCOPE = CURRENT_CANON_AMENDMENT / PRECISION_CATALYST_RESOURCE
USER_DIRECTION = CATALYST_IS_A_CONSUMABLE_RESOURCE_NOT_A_LINEAGE_SELECTION
APPROVED_ITEM_NAMES = 불의 심장 / 대지의 결정
PRODUCT_IMPLEMENTATION = NOT_STARTED_FOR_THIS_AMENDMENT
```

## 1. Purpose and authority amendment

정밀강화의 촉매는 작품의 계보나 혈통을 고르는 추상 선택지가 아니다. 플레이어가
공방에 보유한 실제 자원이며, 정밀강화를 시도할 때 선택·소모하는 판타지 재료다.
정밀 target의 태그 추가/강화는 그대로 유지하되, 플레이어가 보게 되는 용어와
결제 경로를 `촉매 계보`에서 `정밀 촉매`로 전환한다.

| Current owner | Replaced field | New current meaning |
| --- | --- | --- |
| `BS-ENHANCE-20260830-38` | `lineage_id`, `lineages`, `MISSING_CATALYST_LINEAGE`, `NO_CATALYST_INVENTORY_OR_CONSUMPTION` | `catalyst_id`, `catalysts`, `MISSING_PRECISION_CATALYST`, 실제 `material_stock` 촉매 소모 |
| `BS-ENHANCE-20260830-38` | 불씨/모루 계보 선택 | 불의 심장/대지의 결정 아이템 선택 |
| `BS-ENHANCE-20260830-38` | 정밀성공만 tag action의 유일한 소비 | 시도 확정 시 골드·보강재·촉매를 하나의 원자적 결제로 차감 |

다음 계약은 보존한다.

```text
PRECISION_TARGETS = [10,20,30,40,50,60,70,80,90,100]
SUCCESS_LEVEL_DELTA = +1
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX = ONLY_AFFIX_OWNERS
MAX_ACTIVE_TAGS = 3
MAX_TAG_STAGE = IV
ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY
NO_RANDOM_TAG_REROLL_OR_UNRELATED_REPLACEMENT = TRUE
NO_GRADE_OR_EVENT_KEYWORD_MUTATION = TRUE
DECISION28/29/30_PROBABILITY_DURABILITY_REPAIR = UNCHANGED
```

`CATALYST_AFFIX`는 기존의 기계적 affix owner 이름으로만 남는다. 화면,
오류 문구, catalog의 player-facing 표현에는 `계보`라는 단어를 쓰지 않는다.
이는 네 번째 affix 슬롯이나 새 장비 저장 필드를 추가하는 변경이 아니다.

## 2. Player-facing catalyst model

### 2.1 Exact resources

| Catalog ID | `material_stock` key | Player-facing item name | Required by tags |
| --- | --- | --- | --- |
| `HEART_OF_FLAME` | `heart_of_flame` | **불의 심장** | `TAG_EMBER_EDGE`, `TAG_EMBER_LIGHT` |
| `EARTH_CRYSTAL` | `earth_crystal` | **대지의 결정** | `TAG_ANVIL_EDGE`, `TAG_ANVIL_LIGHT` |

기존 `TAG_EMBER_*`, `TAG_ANVIL_*`는 저장 호환성을 위한 내부 ID로 보존한다.
플레이어에게는 다음 이름으로 표시한다.

```text
TAG_EMBER_EDGE  = 불의 심장 · 예리함
TAG_EMBER_LIGHT = 불의 심장 · 경량
TAG_ANVIL_EDGE  = 대지의 결정 · 예리함
TAG_ANVIL_LIGHT = 대지의 결정 · 경량
```

정밀 방식과 효과는 현행 catalog를 유지한다.

```text
날 세우기  = RAW_ROLE_STAT +3
경량 담금  = WEIGHT_POINT -3 / floor 0
DURABILITY_DELTA = 0
```

### 2.2 Add versus upgrade flow

```text
정밀 target 진입
→ [태그 추가] 또는 [태그 강화]

태그 추가
→ 불의 심장 또는 대지의 결정 선택
→ 날 세우기 또는 경량 담금 선택
→ 태그/효과/골드/보강재/촉매 ×1 미리보기
→ 시도

태그 강화
→ 기존 태그 선택
→ 태그가 요구하는 촉매를 자동 해석하여 표시
→ 단계/효과/골드/보강재/촉매 ×1 미리보기
→ 시도
```

첫 `+9 -> +10`은 반드시 `ADD_TAG`다. 이후 +20부터 +100까지는 허용되는
새 태그를 추가하거나 I~III인 기존 태그 하나를 강화한다. `UPGRADE_TAG`에
촉매 선택기를 다시 보여 주지 않는다. 선택한 태그가 필요한 촉매를 이미
소유하므로, 화면에는 `소모: 불의 심장 ×1`처럼 읽기만 가능한 명세를 표시한다.

기본 선택, 무작위 선택, reroll, 기존 태그 교체, 태그와 무관한 촉매 사용은
허용하지 않는다.

## 3. Payment, inventory, and persistence

### 3.1 Atomic consumption

각 정밀 시도는 기존 일반 강화 결제와 동일한 순서를 따른다.

```text
PRE-ROLL GATE
  정확한 태그 행동/선택?
  골드 충분?
  보강재 충분?
  필요 촉매 1개 이상?
  → 하나라도 아니면 cost/roll/state mutation 없이 BLOCKED

ATTEMPT COMMIT
  candidate save에 gold, common_reinforcement_material, required catalyst를 함께 차감
  candidate save 성공 뒤에만 live resource snapshot에 반영

RESOLUTION
  SUCCESS        → +1, tag add/upgrade, effect 1회, milestone/ledger 1회
  FAILED_HOLD    → level/tag/effect/milestone 불변, 이미 결제한 촉매는 소모 유지
  FAILED_DAMAGE  → level/tag/effect/milestone 불변, 기존 damage만 적용, 촉매 소모 유지
  SAVE_FAILED    → gold/보강재/촉매를 모두 원복
```

촉매가 실패에서 사라지는지 성공에서만 사라지는지 숨기지 않는다. 이 사양은
**시도 확정 시 소모**를 채택한다. 현재 보강재 결제와 같은 원칙이고, 위험한
`STOP OR PUSH` 판단이 결과 이후에도 예측 가능하게 남는다.

### 3.2 Vertical-slice supply boundary

새 공방 상점, 채굴, 일일 과제, 드롭, 프리미엄 재화는 이번 변경 범위에 넣지
않는다. 현재 세로 슬라이스에서는 각 새 캠페인이 아래의 결정적 test budget을
받는다.

```text
STARTER_PRECISION_CATALYST_STOCK
heart_of_flame = 64
earth_crystal = 64
SOURCE = NEW_CAMPAIGN_STARTER_ALLOCATION_ONLY
PRICE = NONE
REPLENISHMENT_LOOP = NOT_IN_SCOPE
BALANCE_STATUS = TEMP_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

`64`는 촉매 한 종류가 합법적으로 만들 수 있는 최대 태그 성장 8회
(두 태그 × IV)와 현행 target별 최대 7회 hold 복구 상한을 곱한 값이다.
따라서 현재 구현된 hard-guarantee 계약 안에서 촉매 재고 자체가 모든
정밀강화를 soft-lock하지 않는다. 이 값은 장기 경제 가격이나 드롭 확률이
아니다.

### 3.3 Save migration

`VSSaveEnvelope`는 schema V4에서 V5로 올라간다. V4 저장은 Grade, Chronicle,
현재 금, 보강재, 장비 UID, durability, ledger를 그대로 보존하고, 누락된
두 촉매 key만 결정적으로 추가한다.

| Loaded source | Resulting catalyst stock |
| --- | --- |
| V5 with both keys | 저장된 정수값을 그대로 보존 |
| V4 missing both keys | `heart_of_flame=64`, `earth_crystal=64` 보완 |
| V3 이하 정상 마이그레이션 | V5 starter allocation으로 보완 |
| 음수/비정수 촉매 수량 | 기존 `INVALID_WORKSHOP_RESOURCE_QUANTITY` fail-closed 검증 |

V5 저장을 다시 열 때 starter allocation을 재지급하지 않는다. 이 migration은
idempotent여야 하며, 저장 재시작만으로 촉매·태그·효과·ledger가 중복되지 않는다.

## 4. Data and UI contract

### 4.1 Catalog V3

`BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`은 schema 3으로 올린다.
새 catalog는 `lineages` 대신 `catalysts` 배열을 가지며 각 태그는
`catalyst_id`를 가진다.

```json
{
  "id": "HEART_OF_FLAME",
  "material_stock_key": "heart_of_flame",
  "display_name_ko": "불의 심장",
  "units_per_precision_attempt": 1
}
```

기존 `method_id`, tag cap, stage, compatibility, effect boundary를 보존한다.
catalog validator는 정확히 두 촉매, 네 태그, 두 방식, 촉매별 1개 소모,
tag-to-catalyst 참조의 완전성을 fail-closed로 검사한다.

### 4.2 Native workshop UX

전용 정밀강화 배경이나 새 촉매 raster asset을 만들지 않는다. 기존 승인된
native Workshop UI 안에서만 다음 정보를 큰 Control로 표시한다.

```text
정밀강화 +20
태그 행동: [태그 추가] [태그 강화]
정밀 촉매: [불의 심장 · 보유 63]   # 추가에서만 선택 가능
정밀 방식: [날 세우기]
결과: 불의 심장 · 예리함 I → II / 공격 역할 수치 +3
비용: 000 Gold · 보강재 0개 · 불의 심장 1개
[정밀강화 시도]
```

촉매 부족일 때 시도 버튼은 비활성화하고 `불의 심장이 부족합니다`처럼 실제
아이템명을 쓴다. 선택하지 않았을 때는 `정밀 촉매를 고르세요`로 차단한다.
OptionButton metadata는 보이는 이름이 아닌 안정적인 `catalyst_id`를 저장한다.

Android 세로 UI에서는 기존의 `태그 행동 → 촉매 → 방식 → 결과` 순서를
유지하며, 태그 강화에서 촉매 선택기를 숨겨 중복 입력을 줄인다.

## 5. Explicit exclusions

```text
NO_NEW_GENERAL_INVENTORY_SCREEN
NO_VENDOR_OR_PURCHASE_SCREEN
NO_MINING_COMBAT_DAILY_OR_GACHA_SUPPLY_LOOP
NO_RANDOM_CATALYST_EFFECT
NO_REROLL_OR_TAG_REPLACEMENT
NO_NEW_AFFIX_SLOT
NO_GRADE_ARTISTRY_FUNCTION_OR_CHRONICLE_MUTATION
NO_DAMAGE_REPAIR_SUCCESS_RATE_OR_PRICE_CURVE_CHANGE
NO_NEW_CATALYST_IMAGE_ASSET
```

장기 촉매 경제와 실제 보급처는 정밀강화의 소비·저장·UI가 사람 플레이로
검증된 뒤 별도 balance decision으로 다룬다. 이번 사양의 64개 starter budget은
그 장기 경제를 미리 확정하지 않는다.

## 6. Benchmark disposition

이번 설계는 11개 대장장이 게임의 공개 제품 설명을 비교한 결과다. 재료가
제작 결과와 직접 연결되어야 한다는 원리는 채택하되, 전체 생산 체인·파밍·등급
도박으로 확장하지 않는다.

| Benchmark | Disposition | Applied rule |
| --- | --- | --- |
| [Blacksmith Master](https://store.steampowered.com/app/2292800/Blacksmith_Master/) | `ADAPT` | 재료 역할 분리; 촉매는 공방 stock, 태그는 장비 affix owner에만 기록 |
| [Anvil Saga](https://store.steampowered.com/app/1587540/) | `ADOPT` | 작품 선택은 기존 고객·세계·연대기 결과와 읽을 수 있게 연결 |
| [Blacksmith of the Sand Kingdom](https://store.steampowered.com/app/1445440/Blacksmith_of_the_Sand_Kingdom/) | `REJECT` | 촉매 확보를 위한 채집·전투 필수 루프는 넣지 않음 |
| [Medieval Blacksmith](https://store.steampowered.com/app/2732100/Medieval_Blacksmith/) | `ADOPT` | 재료, 결과 태그, 수치 변화, 고객 맥락을 시도 전 명시 |
| [Blacksmith Shop Simulator](https://store.steampowered.com/app/3563710) | `ADAPT` | 부족 재료와 결제량을 버튼 전 명시하고 숨은 확률 패널티 금지 |
| [Blacksmith Simulator](https://store.steampowered.com/app/1959120/Blacksmith_Simulator/) | `ADAPT` | 보강재와 정밀 촉매의 의미를 분리 |
| [My Little Blacksmith Shop](https://store.steampowered.com/app/980940/My_Little_Blacksmith_Shop/) | `ADOPT` | 장비 종류와 주문 중심 결과를 유지하고 별도 인벤토리 화면은 만들지 않음 |
| [Blacksmith: Ignite the Forge](https://store.steampowered.com/app/2651220/Blacksmith_Ignite_the_Forge/) | `ADAPT` | 특수 재료가 장비의 결정적 특수 성질과 연결되게 함 |
| [Fantasy Blacksmith](https://store.steampowered.com/app/959520/Fantasy_Blacksmith/) | `ADAPT` | 판타지 재료명과 공방 맥락은 채택, 다부품 조합·설비 체인은 제외 |
| [Heat ’n Hit](https://store.steampowered.com/app/3910800/Heat_n_Hit_The_Blacksmith_Simulator/) | `ADOPT` | 담금 시약처럼 실물 촉매를 소모하고 결과 효과를 결정적으로 표시 |
| [Ultimate Blacksmith Tycoon](https://store.steampowered.com/app/4687330/Ultimate_Blacksmith_Tycoon/) | `REJECT` | rarity 변동·다중 modifier·품질 도박은 현 3-affix 경계를 침범하므로 제외 |

## 7. Acceptance contract

구현은 RED → GREEN → REFACTOR 순서로 아래를 검증한다.

1. `+9 -> +10`부터 `+99 -> +100`까지의 10개 target만 촉매를 요구한다.
2. `ADD_TAG`는 명시 촉매·방식 없이 cost/roll 전에 차단된다.
3. `UPGRADE_TAG`는 선택한 tag의 촉매를 자동 해석하며, 다른 촉매로 우회할 수 없다.
4. 부족 촉매는 금·보강재·태그·확률 roll을 전혀 변경하지 않는다.
5. 정상 시도는 성공, hold, damage 모두 정확히 촉매 1개를 소모한다.
6. 저장 실패와 blocked outcome은 금·보강재·촉매를 모두 원복한다.
7. 성공 하나는 level +1, tag stage/effect/milestone/ledger를 각각 정확히 한 번만 바꾼다.
8. V4 save는 두 촉매의 64개 starter allocation을 한 번만 받고, V5 save의 실제 잔량을 보존한다.
9. 기존 tag ID, Grade, Chronicle, durability, repair, customer/world result, visual assets는 바뀌지 않는다.
10. Workshop의 실제 runtime consumer는 계보 문구를 표시하지 않고, 선택/부족/소모 상태를 모두 실제 아이템명으로 보인다.

자동 테스트 성공은 machine evidence일 뿐 Android 실기기, 접근성, 성능, 사람
플레이 UX 통과를 뜻하지 않는다.

## 8. Implementation ownership after spec review

사용자가 이 설계서를 검토·확정하면 다음 변경을 하나의 plan으로 실행한다.

1. Decision 38의 대체 필드와 새 Decision 40을 정본·catalog·contract test에 기록한다.
2. catalog V3와 precision resolver를 `catalyst_id` 계약으로 전환한다.
3. V5 save migration과 starter allocation, enhancement action service의 원자적 세 재화 결제를 구현한다.
4. workshop scene/script의 계보 selector를 촉매 selector와 read-only upgrade cost로 교체한다.
5. `[10,20,...,100]` 정밀 target을 preset, UI, resolver, GUT/Python test가 같은 값으로 읽도록 교정한다.
6. focused RED/GREEN tests, 전체 계약 검사, Godot runtime, 실제 인게임 capture, GitHub destination readback을 수행한다.

기존 사용자 변경, PR #196, 기존 승인 장비 raster asset, 전용 정밀 공방 배경의
폐기 결정은 이 변경의 소유물이 아니며 수정·복원하지 않는다.
