# Equipment Base Weight Points Design

- Decision ID: `BS-ITEM-20260806-01`
- Active batch target: `R2_BATCH_005_5_OF_10`
- Status: `USER_APPROVED / APPROVED_PENDING_MERGE`
- Refines: `BS-CUSTOMER-20260806-01`, `BS-CUSTOMER-20260805-01`, `BS-UX-20260805-01`
- Product implementation: `BLOCKED`

## 1. User intent

Blacksmith의 핵심은 장비 무게 최적화나 고객 스탯 육성이 아니라 강화 성공·실패와 강화 중단 판단이다. 장비 중량은 고객이 작품을 사용할 수 있는지만 빠르게 판단하는 보조 정보여야 한다.

## 2. Considered approaches

### A. 현실 중량과 재료 밀도 계산

장비 실측 kg, 부피, 재료 밀도, 부품 비율을 계산한다.

- 장점: 현실성
- 단점: 데이터·UI·밸런스 비용이 크고 강화 핵심을 흐린다.
- 판정: 비채택

### B. 장비마다 개별 중량 수치

모든 장비 베이스에 별도 중량을 지정한다.

- 장점: 세밀한 차별화
- 단점: 장비 추가 때마다 수치 설계가 필요하고 사실상 숨은 전투력 축이 된다.
- 판정: 비채택

### C. 장비군 고정 기본값 + 명시적 ±5 효과

기존 무기·갑옷군에 5단위 기본값을 한 번 지정하고, 중량을 직접 다루는 강화 효과만 정확히 `-5` 또는 `+5`를 한 번 적용한다.

- 장점: 설명 가능하고 유지 비용이 낮다.
- 장점: 강화가 중량 한도를 넘기는 문제를 해결할 수 있다.
- 장점: 재료·등급·예술성·공격력과 이중 계산하지 않는다.
- 판정: 채택

## 3. Canonical base-weight table

모든 수치는 현실 kg가 아닌 정수형 `WEIGHT_POINT`다.

| 장비군 | ID | 기본 중량 |
|---|---|---:|
| 장신구 | `ACCESSORY` | 0 |
| 도구 | `TOOL` | 5 |
| 의복·로브 | `CLOTHING_OR_ROBE` | 5 |
| 경갑 | `LIGHT_ARMOR` | 10 |
| 중갑 | `MEDIUM_ARMOR` | 20 |
| 중장갑 | `HEAVY_ARMOR` | 30 |
| 검류 | `SWORD` | 10 |
| 도끼류 | `AXE` | 15 |
| 둔기류 | `BLUNT` | 15 |
| 장병기류 | `POLEARM` | 20 |
| 원거리류 | `RANGED` | 10 |
| 방패·보조장비 | `SHIELD_SUPPORT` | 10 |

현재 런타임 베이스와의 계획상 대응:

```text
sword -> SWORD -> 10
spear -> POLEARM -> 20
axe -> AXE -> 15
```

이번 Decision은 계획 정본만 갱신하며 `data/crafting/weapon_bases.json`은 수정하지 않는다.

## 4. Weight calculation

```text
ITEM_WEIGHT = BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER
TOTAL_WEIGHT = sum(ITEM_WEIGHT for equipped weight-bearing items)
MAXIMUM_LOAD = STRENGTH × 10
```

- 기본 중량은 장비군에서만 온다.
- 재료·제작 등급·예술성·공격·방어·조작성·내구도는 기본 중량을 자동 변경하지 않는다.
- 일반 강화 레벨 `+N`도 중량을 자동 변경하지 않는다.
- 장신구는 기본 중량 `0`이며 사건이나 콘텐츠가 명시적으로 중량을 부여할 때만 예외가 생긴다.

## 5. Explicit weight modifier

중량을 직접 다루는 승인된 강화·촉매·수식어만 다음 중 하나를 적용한다.

```text
LIGHTWEIGHT: -5 WEIGHT_POINT
WEIGHTED: +5 WEIGHT_POINT
NONE: 0
```

- 작품 하나당 활성 중량 변경은 최대 하나다.
- 여러 출처를 합산하거나 곱하지 않는다.
- 최종 작품 중량 최솟값은 `0`이다.
- 일반 강화 레벨과 별개의 명시적 선택이다.
- 중량 감소는 고객의 최대 중량 한도를 통과시키는 보조 선택이며 성공률을 직접 올리지 않는다.
- 중량 증가는 별도 보상을 자동 제공하지 않는다. 보상이 필요하면 해당 강화 효과 자체에 명시한다.

## 6. Player-facing information

기본 작품 정보에는 정수 중량만 표시한다.

```text
중량 15
```

고객 배정 화면에서는 기존 단순 게이트를 유지한다.

```text
총 중량 35 / 최대 중량 40 · 사용 가능
총 중량 45 / 최대 중량 40 · 중량 초과 · 배정 불가
```

중량 변경 효과가 있을 때만 이유 칩을 하나 표시한다.

```text
경량화 -5
중량화 +5
```

재료 밀도, 초과율, 이동 속도, 피로, 명중 패널티는 표시하지 않는다.

## 7. Core-fun guardrails

- 장비군 중량은 강화보다 중요한 성장 축이 아니다.
- 높은 중량 자체를 품질·희귀도·공격력으로 취급하지 않는다.
- 중량 한도 이내에는 보너스나 추가 성공률이 없다.
- 고객 능력치·장비 중량·작품 원수치를 하나의 종합 전투력 점수로 합치지 않는다.
- 중량 변경은 강화 선택의 작은 보조 분기만 담당한다.

## 8. Adversarial review

- `POLEARM 20`과 `HEAVY_ARMOR 30`을 함께 사용하면 근력 5가 필요하다. 최대 중량 규칙과 자연스럽게 맞고 별도 페널티가 필요 없다.
- 장신구 0은 무제한 장신구 장착 문제를 만들 수 있으나 슬롯 수는 별도 장비 규칙의 책임이다. 중량으로 슬롯 문제를 해결하지 않는다.
- 재료가 무게에 영향을 주지 않아 현실성이 낮을 수 있으나, 재료 효과는 공격·내구·특수기능 등 더 직접적인 제작 결과로 표현한다.
- `LIGHTWEIGHT -5`가 반복 중첩되면 한도를 무력화하므로 작품당 최대 하나로 제한한다.
- `WEIGHTED +5`에 자동 보상을 붙이면 중량이 또 다른 필수 최적화 축이 되므로 금지한다.

최종 판정: `P0 0 / P1 0`.

## 9. Scope and verification

- Create planning canon and machine-readable registry contract.
- Refine current authority documents and mobile wording.
- Add TDD planning contracts and validator assertions.
- Synchronize the same Decision ID and exact head to the connected Google Sheet.
- Runtime, game data, scenes, images, and assets remain unchanged.
- Actual balance playtest: `NOT_RUN`.
- Product implementation: `BLOCKED`.
