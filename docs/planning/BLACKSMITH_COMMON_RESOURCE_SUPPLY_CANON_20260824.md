# [현재 정본] Blacksmith 일반 강화·수리 Resource Supply

- Decision: `BS-RESOURCE-20260824-18`
- 사용자 승인: `2026-08-24 KST / 권장안 B 승인`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Runtime mutation: `NOT_ALLOWED_IN_THIS_DECISION`
- Human/Player validation: `NOT_RUN`

## 1. 목적

`BS-PROGRESSION-20260820-17`에서 회계 단위로만 남아 있던 일반 강화 재료와 `BS-ENHANCE-20260820-10~12`의 일반 CURRENT 수리 재료를 하나의 실제 player-facing 공통 재료로 매핑한다.

핵심 목표는 재료 파밍을 새 메인 루프로 만드는 것이 아니라, 강화 전의 `멈춤 / 한 번 더` 판단과 작품 손실 압력을 지지하는 것이다.

```text
PRIMARY CORE
= 강화 긴장감 + DDD

COMMON RESOURCE SUPPLY
= CORE를 막지 않는 물리적 공방 자원 계층
```

## 2. 승인 자원

```text
CANONICAL_ID = common_reinforcement_material
PLAYER_NAME_KO = 보강재
CATEGORY = common_workshop_material
RARITY_ROLE = COMMON / DETERMINISTIC_SUPPLY
UNIT_SHADOW_VALUE = 50G
SHOP_UNIT_PRICE_TEST_ANCHOR = 50G
```

`보강재`는 새 화폐가 아니다. 실제 공방 재료 1종이며 강화와 일반 CURRENT 수리 recipe에서 소비한다.

다음 기존 주재료와는 별도 자원이다.

```text
iron
silver
meteor_iron
```

철/은/운석철을 일반 강화·수리 보강재로 직접 소모시키지 않는다. 희귀 주재료가 일반 유지·강화 접근을 soft-lock하거나 기존 material structure multiplier와 이중 과금되는 것을 방지한다.

## 3. 강화 recipe mapping

`BS-PROGRESSION-20260820-17`의 balance unit을 1:1로 실제 보강재 수량에 매핑한다.

```text
COMMON_REINFORCEMENT_MATERIAL_UNITS(target)
= ceil(target / 20)
```

| Target | 보강재 |
|---:|---:|
| +1~+20 | 1 |
| +21~+40 | 2 |
| +41~+60 | 3 |
| +61~+80 | 4 |
| +81~+100 | 5 |

강화의 기존 골드 시도비는 그대로 별도 지불한다.

```text
ENHANCEMENT_PAYMENT
= GOLD_ATTEMPT_COST
+ REQUIRED_COMMON_REINFORCEMENT_MATERIAL
```

보강재는 골드를 할인하지 않고, 골드가 보강재를 대체하지 않는다.

## 4. 일반 CURRENT 수리 recipe mapping

기존 `BS-ENHANCE-20260820-10~12` 수리 계약을 보존한다.

```text
missing = MAX - CURRENT

if missing <= 0:
    repair unavailable / no material consumption
else:
    REQUIRED_COMMON_REINFORCEMENT_MATERIAL
    = max(1, ceil(missing / 25))
```

| CURRENT 결손 | 보강재 |
|---:|---:|
| 1~25pt | 1 |
| 26~50pt | 2 |
| 51~75pt | 3 |
| 76~99pt | 4 |

```text
REPAIR_PAYMENT
= EXISTING_REPAIR_GOLD_COST
+ REQUIRED_COMMON_REINFORCEMENT_MATERIAL

CURRENT -> MAX
MAX unchanged
recovery unchanged
```

일반 수리의 `material_structure_multiplier`와 `secured_band_multiplier`는 골드 수리비 R에만 적용한다. 보강재 수량에 다시 곱하지 않는다.

## 5. 기본 공급 계약

첫 Vertical Slice 기준 공급은 다음을 채택한다.

```text
PRIMARY_SOURCE = WORKSHOP_MATERIAL_VENDOR
AVAILABILITY = ALWAYS_AVAILABLE_FROM_FIRST_RELEVANT_USE
PURCHASE_CAP = NONE
DAILY_CAP = NONE
RNG_GATE = NONE
RARE_DROP_REQUIREMENT = NONE
CUSTOMER_COMPLETION_REQUIREMENT = NONE
COMBAT_OR_MINING_REQUIREMENT = NONE
PREMIUM_CURRENCY = NONE
UNIT_PRICE = 50G
```

첫 강화/첫 수리 시점에 보강재 부족 때문에 플레이 루프가 막혀서는 안 된다.

`50G`는 새 환율이 아니라 17에서 이미 승인된 `COMMON_ENHANCEMENT_MATERIAL_SHADOW_VALUE = 50G / unit`을 실제 기본 공급 가격 anchor로 연결한 값이다.

## 6. 보너스 공급원 경계

다음은 향후 추가할 수 있는 hook이지만 이번 Decision에서 제품 기능으로 승인하지 않는다.

```text
DESTROYED_ITEM_SALVAGE
CUSTOMER_REWARD
WORKSHOP_CONTRACT
WORLD_EVENT_REWARD
```

상기 hook은 `OPTIONAL_FUTURE_BONUS_SOURCE / NOT_IMPLEMENTATION_APPROVED`다.

보너스 공급원을 추가할 때도 상점 확정 공급을 제거하거나 RNG-only 병목으로 대체하지 않는다. 별도 채굴·일일퀘스트·전투 farm을 일반 보강재의 필수 획득 루프로 만들지 않는다.

## 7. UX 계약

강화/수리 화면에는 실제 소모량을 직접 표시한다.

```text
골드 N
보강재 M
```

금지:

- `balance unit`이라는 내부 용어를 플레이어에게 노출.
- 재료를 골드 할인율처럼 표시.
- 골드 전액 결제 후 재료가 선택사항인 것처럼 표시.
- 희귀 catalyst와 보강재를 같은 의미로 표시.
- 보강재가 없을 때 실패 확률이 몰래 증가하는 hidden modifier.

상점 UX는 반복 구매 부담이 확인되면 묶음 구매/필요량 바로 구매 같은 편의 기능을 우선 검토한다. 이 편의 UX는 이번 Decision의 제품 구현 승인을 의미하지 않는다.

## 8. 기존 data/runtime와의 관계

현재 `data/crafting/materials.json`의 `iron / silver / meteor_iron / whetstone / flame_stone / spirit_heart / catalyst` 정의는 과거 runtime/PoC 구현 사실이다.

이번 PLAN Decision은 제품 data/runtime를 수정하지 않는다.

새 `기획 완료` 및 구현 Gate가 열릴 때 구현자는 다음을 수행해야 한다.

1. `common_reinforcement_material` 정의 추가.
2. 강화 recipe를 target band별 1~5개로 매핑.
3. 일반 CURRENT 수리를 결손별 1~4개로 매핑.
4. 공방 재료상 50G 상시·무제한 공급 경로 연결.
5. 기존 `iron/silver/meteor_iron` 및 catalyst 의미와 분리.
6. balance simulation에서 50G shadow value 중복 계상 여부 검증.

현재 구형 `materials.json` 가격은 이 Decision의 일반 보강재 가격 권위가 아니다.

## 9. 기대 소비 규모 검산

17의 planning simulation 평균 시도 횟수와 1~5 unit mapping을 이용한 개략적 강화 소비 규모:

```text
+10  ≈ 11 units
+20  ≈ 24 units
+30  ≈ 51 units
+60  ≈ 168 units
+100 ≈ 1,093 units
```

+100 기준 약 `54,650G` shadow value이며, 기존 +100 누적 기대원가 anchor `5,632,657G`의 약 1% 수준이다.

따라서 후기 강화 긴장감의 주 압력은 보강재 희소성이 아니라 기존의 강화비·실패·CURRENT/MAX·작품 가치여야 한다.

정확한 human pacing은 `USER_PLAYTEST_REQUIRED`다.

## 10. 대안 비교

### A. 기존 주재료 직접 소비 — REJECT

- 장점: 신규 자원 없음.
- 실패: 은/운석철 같은 고급·희귀 주재료가 일반 강화/수리를 막을 수 있음.
- 기존 수리의 material structure multiplier와 의미 중복 위험.

### B. 공통 보강재 1종 — APPROVED

- 강화/수리 공통 recipe.
- 50G 기존 shadow value 재사용.
- 상시 확정 공급.
- 코어 강화 판단을 막지 않음.

### C. 채굴/의뢰/드롭 중심 — REJECT_AS_BASELINE

- 별도 획득 루프가 강화보다 앞에 서는 위험.
- 반복 파밍 자체가 콘텐츠 분량이 되는 MMO식 구조를 피한다.

## 11. 벤치마크 흡수

원리는 외부 수치를 복사하지 않고 다음만 흡수한다.

- `FINAL FANTASY XIV repair material` — 공통 유지재를 안정적으로 구매 가능한 공급으로 두는 원리 `ADAPT`.
- `Elden Ring smithing stone supply adjustments` — 핵심 성장 재료 접근성이 진행을 불필요하게 막지 않게 하는 원리 `ADAPT`.
- `Lost Ark honing supply adjustments` — 반복 실패 + 재료 부족 자체를 콘텐츠 분량으로 사용하지 않는 원리 `ADAPT / AVOID`.

## 12. 5회 전체 적대 검토 결과

### Loop 1 — 코어 침범
- RNG/채굴/일퀘 필수 공급은 강화 판단 전에 파밍을 세움.
- 상시 확정 공급으로 교정.
- `PASS`.

### Loop 2 — existing material 재사용 강박
- 주재료 직접 소비는 희귀재 병목과 이중 의미를 만듦.
- 공통 보강재 1종으로 분리.
- `PASS`.

### Loop 3 — 기존 경제곡선 훼손
- 새 환율을 만들면 +10 본전/17 anchor를 흔듦.
- 기존 50G shadow value를 그대로 사용.
- `PASS_WITH_PLAYTEST`.

### Loop 4 — soft-lock
- 필수 재료 + RNG 공급은 손상 작품 수리/강화를 차단할 수 있음.
- 첫 관련 사용 이전부터 상시 판매, 구매 cap 없음.
- `PASS`.

### Loop 5 — 과설계
- salvage/customer/world-event 공급을 동시에 확정하면 후속 시스템을 선점함.
- 보너스 공급원은 hook만 남기고 미승인으로 유지.
- `PASS`.

## 13. Implementation Reality Gate

```text
DESIGN_CANON = USER_APPROVED
GITHUB_CANON_SYNC = REQUIRED
NOTION_SYNC = REQUIRED
RUNTIME_IMPLEMENTATION = BLOCKED
HUMAN_PLAYTEST = NOT_RUN
FINAL_PRODUCT_BALANCE = NOT_CLAIMED
```

## 14. 다음 작업

`RESOURCE_SUPPLY` 완료 뒤 다음 순서는:

```text
LATE_REPAIR_ECONOMY
→ HIGH_STAKES / MASTERY 일반 CURRENT 수리의 절대경제 재검증
```

이 다음 경제 숫자는 별도 Decision이며 이번 승인으로 자동 확정하지 않는다.
