# [현재 정본] Blacksmith R2 중량 성능 예산 환산과 장비 역할 프리셋 Canon

- Decision: `BS-ITEM-20260806-03`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_7_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-ITEM-20260806-02 / BS-ITEM-20260806-01 / BS-CUSTOMER-20260806-01`
- 환산 모델: `ROLE_PRESET_AUTOMATIC_SINGLE_LANE`
- 제품 구현: `BLOCKED`

## 1. 핵심 결론

중량 성능 예산은 플레이어가 별도 포인트 화면에서 자유 배분하지 않는다. 작품의 기본 설계가 최초 제작 시 하나의 역할 프로필을 확정하고, 초기 예산과 이후 새 최고 중량으로 얻는 예산은 같은 프로필에 자동 배분한다.

```text
1 ATTACK_BUDGET = ATTACK +5
1 DEFENSE_BUDGET = DEFENSE +5
1 MAGIC_FUNCTION_BUDGET = MAGIC_FUNCTION_CAPACITY +1
1 UTILITY_BUDGET = UTILITY_CAPACITY +1
```

## 2. 역할 프로필

```text
PHYSICAL_WEAPON -> ATTACK_BUDGET
PROTECTIVE_GEAR -> DEFENSE_BUDGET
MAGIC_IMPLEMENT -> MAGIC_FUNCTION_BUDGET
UTILITY_IMPLEMENT -> UTILITY_BUDGET
UTILITY_GARMENT -> UTILITY_BUDGET
NONE -> 중량 예산 없음
```

- 프로필은 `FIRST_CRAFT_COMPLETION_FROM_BASE_ITEM_DEFINITION`에서 확정한다.
- 같은 UID에서 프로필은 변하지 않는다.
- 플레이어 자유 배분 UI와 제작 후 무료 재분배는 없다.
- 새 최고 인정 중량으로 얻는 예산도 기존 프로필을 따른다.
- 혼합 프로필은 기본 규칙이 아니다. 필요한 개별 작품군은 별도 승인된 설계에서만 명시한다.

## 3. 장비군 기본 프리셋

| 장비군 | 기본 프로필 | 초기 예산 결과 |
|---|---|---|
| `SWORD` | `PHYSICAL_WEAPON` | 중량 10 → 예산 2 → 공격 +10 |
| `AXE` | `PHYSICAL_WEAPON` | 중량 15 → 예산 3 → 공격 +15 |
| `BLUNT` | `PHYSICAL_WEAPON` | 중량 15 → 예산 3 → 공격 +15 |
| `POLEARM` | `PHYSICAL_WEAPON` | 중량 20 → 예산 4 → 공격 +20 |
| `RANGED` | `PHYSICAL_WEAPON` | 중량 10 → 예산 2 → 공격 +10 |
| `LIGHT_ARMOR` | `PROTECTIVE_GEAR` | 중량 10 → 예산 2 → 방어 +10 |
| `MEDIUM_ARMOR` | `PROTECTIVE_GEAR` | 중량 20 → 예산 4 → 방어 +20 |
| `HEAVY_ARMOR` | `PROTECTIVE_GEAR` | 중량 30 → 예산 6 → 방어 +30 |
| `SHIELD_SUPPORT` | `PROTECTIVE_GEAR` | 중량 10 → 예산 2 → 방어 +10 |
| `TOOL` | `UTILITY_IMPLEMENT` | 중량 5 → 예산 1 → 유틸리티 용량 +1 |
| `CLOTHING_OR_ROBE` | `UTILITY_GARMENT` | 중량 5 → 예산 1 → 유틸리티 용량 +1 |
| `ACCESSORY` | `NONE` | 중량 0 → 예산 0 |

일반 로브·의복의 기본값은 유틸리티다. 마법 도구·마법 로브처럼 정체성이 명확한 기본 작품은 승인된 작품 설계에서만 `MAGIC_IMPLEMENT`로 지정한다.

## 4. 마법 기능·유틸리티 용량

```text
표준 승인 기능 = 용량 1
강한 효과 또는 여러 맥락에서 작동하는 기능 = 용량 2
규칙 예외·변환·우회 기능 = 용량 3 + 별도 기획 승인
```

- 비용은 양의 정수만 사용한다.
- 용량이 있다고 해서 아직 승인되지 않은 효과를 자동으로 사용할 수 있는 것은 아니다.
- 규칙을 무시하거나 콘텐츠 구조를 바꾸는 효과는 예산 충족만으로 허용하지 않는다.
- 마법 기능·유틸리티 용량은 일반 사건 성공률에 직접 합산하지 않는다.

## 5. 중량화·경량화와 환산

```text
PHYSICAL_WEAPON 중량화 +5 -> 공격 +5
PROTECTIVE_GEAR 중량화 +5 -> 방어 +5
MAGIC_IMPLEMENT 중량화 +5 -> 마법 기능 용량 +1
UTILITY_IMPLEMENT 중량화 +5 -> 유틸리티 용량 +1
UTILITY_GARMENT 중량화 +5 -> 유틸리티 용량 +1
```

새 최고 인정 중량을 만들지 못하는 중량화는 새 예산을 얻지 못한다. 경량화는 현재 중량만 낮추고 이미 배분된 공격·방어·기능 용량을 유지한다.

## 6. 표시 원칙

기본 작품 화면에는 예산 배분표가 아니라 최종 결과를 표시한다.

```text
공격 24
중량 10
상세: 중량 기반 공격 +10
```

정밀강화 미리보기:

```text
중량화: 중량 10 -> 15 / 공격 +5
경량화: 중량 15 -> 10 / 공격 유지
```

- 별도 포인트 배분 화면은 만들지 않는다.
- 필요할 때만 상세 보기에서 `중량 기반` 출처를 한 번 설명한다.
- `base_progress`와 `base_value`를 공격·방어 수치로 재해석하지 않는다.

## 7. 강화 중심성 보호

- 일반 강화 `+N`의 사건 성공률 주효과는 유지한다.
- 중량 기반 공격·방어는 작품 원수치이며 일반 사건 성공률에 자동 합산하지 않는다.
- 중량 한 번을 기본 공격과 중량 예산 공격으로 이중 계산하지 않는다.
- 재료·등급·예술성·촉매·연대기 배율과 자동 곱셈하지 않는다.
- 자유 재분배와 혼합 최적화를 제거해 중량 예산 관리가 별도 빌드 게임으로 전도되지 않게 한다.

## 8. 적대적 검토

- `1점 = 공격·방어 +1`: 정밀강화 기회를 소비하는 중량화의 체감이 지나치게 약해 비채택.
- `1점 = 공격·방어 +10`: 기본 중량만으로 원수치 격차가 과도해질 위험이 있어 비채택.
- `1점 = +5`: 5단위 중량과 같은 눈금으로 설명 가능하고, 검 +10·장병기 +20·중장갑 +30의 직관적 초기 프리셋을 만든다.
- 플레이어 자유 배분: 모든 무기를 마법·유틸리티 최적화 대상으로 만들고 별도 UI를 요구하므로 비채택.
- 모든 로브를 마법 프로필로 고정: 일반 의복까지 마법 장비로 오인하게 하므로 기본 유틸리티, 명시 설계만 마법으로 정제.
- 용량 3 효과 자동 허용: 규칙 우회 콘텐츠가 예산만으로 생성될 위험이 있어 별도 승인 게이트 유지.

최종 판정: `P0 0 / P1 0`.

## 9. 구현 경계

- 기획 정본·검증 계약·권위 진입점·시트만 갱신한다.
- 런타임·게임 데이터·Scene·이미지·에셋은 변경하지 않는다.
- `data/crafting/weapon_bases.json`은 변경하지 않는다.
- 환산 수치는 권장 베이스라인이며 실제 밸런스 플레이테스트는 `NOT_RUN`.
- 제품 구현: `BLOCKED`.
