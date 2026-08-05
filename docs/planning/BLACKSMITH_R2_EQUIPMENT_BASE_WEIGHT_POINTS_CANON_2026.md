# [현재 정본] Blacksmith R2 장비군 기본 중량 포인트 Canon

- Decision: `BS-ITEM-20260806-01`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_5_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-CUSTOMER-20260806-01 / BS-CUSTOMER-20260805-01 / BS-UX-20260805-01`
- 제품 구현: `BLOCKED`

## 1. 핵심 원칙

중량은 고객이 작품을 사용할 수 있는지만 판단하는 보조 정보다. 장비 중량 자체를 새로운 성장·전투력·경제 최적화 축으로 만들지 않는다.

```text
장비군 고정 기본 중량
+ 중량 전용 명시 효과 최대 1개
→ 총 중량
→ 근력 기반 최대 중량과 비교
```

## 2. 단위

- 현실 kg가 아닌 정수형 `WEIGHT_POINT`를 사용한다.
- 기본값과 변경값은 모두 5단위다.
- `0`은 중량 부담을 계산하지 않는 장신구 기본값이다.

## 3. 장비군 기본 중량표

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

현재 제품 데이터의 계획상 대응은 다음과 같다.

```text
sword -> SWORD -> 10
spear -> POLEARM -> 20
axe -> AXE -> 15
```

이번 Decision에서는 `data/crafting/weapon_bases.json`을 수정하지 않는다.

## 4. 계산식

```text
ITEM_WEIGHT = max(0, BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER)
TOTAL_WEIGHT = 모든 중량 적용 장비 ITEM_WEIGHT의 합
MAXIMUM_LOAD = STRENGTH × 10 WEIGHT_POINT
```

- `TOTAL_WEIGHT ≤ MAXIMUM_LOAD`: 사용 가능, 보너스·페널티 없음.
- `TOTAL_WEIGHT > MAXIMUM_LOAD`: 중량 초과, 배정 불가.
- 한도와 정확히 일치해도 보너스가 없다.

## 5. 중량 전용 명시 효과

```text
LIGHTWEIGHT: -5 WEIGHT_POINT
NONE: 0
WEIGHTED: +5 WEIGHT_POINT
```

- 작품 하나당 활성 중량 변경은 최대 하나다.
- 여러 출처를 합산하거나 곱하지 않는다.
- 최종 작품 중량 최솟값은 `0`이다.
- 경량화는 중량 한도를 통과시키는 보조 선택이며 성공률을 직접 올리지 않는다.
- 중량화에는 공격력·가치·성공률 자동 보상을 붙이지 않는다.
- 보상이 필요한 개별 강화 효과는 그 효과에 별도로 명시한다.

## 6. 자동 중량 변경 금지

다음 축은 작품 중량을 자동 변경하지 않는다.

```text
MATERIAL
CRAFTSMANSHIP_GRADE
ARTISTRY
ATTACK
DEFENSE
HANDLING
DURABILITY
GENERAL_ENHANCEMENT_LEVEL
```

- 재료 밀도·부피·부품 비율 계산 없음.
- 제작 등급이 높다고 더 무겁거나 가벼워지지 않음.
- 일반 강화 `+N`이 중량을 자동 증가·감소시키지 않음.
- 예술성·공격·방어·조작성·내구도와 중량을 이중 계산하지 않음.

## 7. 플레이어 표시

작품 정보:

```text
중량 15
```

중량 전용 효과가 있을 때만 이유 칩을 하나 표시한다.

```text
경량화 -5
중량화 +5
```

고객 배정 화면:

```text
총 중량 35 / 최대 중량 40 · 사용 가능
총 중량 45 / 최대 중량 40 · 중량 초과 · 배정 불가
```

초과율·속도·피로·명중·회피 페널티는 표시하거나 계산하지 않는다.

## 8. 강화 중심성 보호

```text
강화 성공·실패와 멈춤 판단
→ 필요하면 중량 전용 강화 선택
→ 고객 최대 중량 확인
→ 사건과 UID 생애 환류
→ 다음 강화·복원·제작 판단
```

- 중량은 강화보다 중요한 성장 축이 아니다.
- 높은 중량 자체를 품질·희귀도·공격력으로 취급하지 않는다.
- 고객 능력·장비 중량·작품 원수치를 종합 전투력 점수로 합치지 않는다.
- 장신구 슬롯 수 문제는 별도 장비 슬롯 규칙의 책임이며 중량으로 해결하지 않는다.

## 9. 벤치마킹·현업 비교

### D&D Basic Rules

힘 점수에 일정 계수를 곱해 운반 한도를 구하는 설명 가능한 구조는 채택한다. 선택 규칙의 단계별 이동·판정 불이익은 Blacksmith의 보조 시스템에는 과하므로 비채택한다.

- Adopt: 힘과 최대 중량의 단순 관계
- Reject: 여러 단계의 속도·공격·판정 페널티
- Source: https://www.dndbeyond.com/sources/dnd/basic-rules-2014/using-ability-scores

### Bethesda RPG support guidance

Oblivion Remastered의 `carry weight = Strength × 5`처럼 능력치와 한도를 직접 연결하는 방식은 수정 채택한다. Skyrim식 초과 이동 불이익은 고객을 직접 조작하지 않는 Blacksmith에는 필요하지 않다.

- Adapt: 직관적인 능력치×계수
- Reject: 초과 상태의 이동 속도 게임플레이
- Sources:
  - https://help.bethesda.net/app/answers/detail/a_id/69972/
  - https://help.bethesda.net/app/answers/detail/a_id/16579/

### Elden Ring Nightreign

제한된 인벤토리 구조에서는 무기 중량과 장비 하중을 제거해 판단 비용을 낮춘 사례가 있다. Blacksmith는 고객 배정 가능 여부를 설명할 가치가 있어 중량을 완전히 제거하지 않고 이진 게이트만 남긴다.

- Adopt: 핵심과 무관한 하중 최적화 축을 줄이는 방향
- Adapt: 완전 제거 대신 고정값·이진 게이트
- Source: https://en.bandainamcoent.eu/elden-ring/news/beginner-tips-elden-ring-nightreign

## 10. 적대적 검토

- `POLEARM 20 + HEAVY_ARMOR 30`은 근력 5부터 사용 가능하다. 별도 페널티 없이 최대 중량 게이트만으로 설명된다.
- `ACCESSORY 0`은 무제한 슬롯을 허용한다는 뜻이 아니다. 슬롯 수는 별도 책임이다.
- `LIGHTWEIGHT -5` 중첩은 최대 중량을 무력화하므로 작품당 하나로 제한한다.
- `WEIGHTED +5` 자동 보상은 중량을 필수 최적화 축으로 만들 수 있어 금지한다.
- 재료 무게 차이를 제거해 현실성이 낮아질 수 있으나 재료 개성은 공격·내구·특수기능·미학 등 직접적인 제작 결과로 표현한다.

최종 판정: `P0 0 / P1 0`.

## 11. 구현 경계

- 계획 정본·검증 계약만 갱신.
- 런타임·게임 데이터·Scene·이미지·에셋 변경 금지.
- 실제 밸런스 플레이테스트: `NOT_RUN`.
- 제품 구현: `BLOCKED`.
