# [현재 정본] Blacksmith R2 기능 레시피·주재료 적합·직접 단조·플레이테스트 Canon

- Decision: `BS-ITEM-20260806-06`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_10_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-ITEM-20260806-03 / BS-ITEM-20260806-04 / BS-ITEM-20260806-05 / BS-CRAFT-20260804-04`
- 재료·수치 상태: `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`
- 사람 플레이테스트: `NOT_RUN`
- Google Sheet 미러: `42_능력치_강화_참조표`
- 제품 구현: `BLOCKED`

## 1. 핵심 결론

Blacksmith의 최초 작품 성능과 특수기능은 자유 조합이나 무작위 생성이 아니라 명시적 재료 적합·역할 프로필·기능 레시피로 결정한다.

```text
MATERIAL_ROLE_FIT
= EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP

DIRECT_FORGING_ROLE_RESULT
= DETERMINISTIC_ROLE_STRIKE_THREE_ZONE

FUNCTION_RECIPE
= ROLE_PROFILE
+ EQUIPMENT_GROUP
+ PRIMARY_MATERIAL
+ MINIMUM_RECOGNIZED_WEIGHT
+ OPTIONAL_BOUND_CONTEXT
+ CAPACITY_COST
+ ACQUISITION_MODE
```

- 철은 모든 역할 장비에서 기준 재료다.
- 은은 경량·정밀 역할에 유리하다.
- 운석철은 중량·충격 역할에 유리하다.
- 역할 정밀 타격은 `-1 / 0 / +1`만 소유하며 제작 등급 점수와 분리한다.
- 최초 기능은 레시피 충족 시 결정적으로 생성한다.
- 제작 후 기능 변경은 정밀 이정표의 `FUNCTION_REWORK`만 소유한다.
- 현재 촉매 콘텐츠로 즉시 가용한 결속 재작업은 불 계열 2종뿐이다.
- 사람 플레이테스트 통과 전에는 수치를 최종 밸런스로 승격하지 않는다.

## 2. 주재료 역할 적합

기본 보정:

```text
LOW_ROLE_FIT = -2
STANDARD_ROLE_FIT = 0
HIGH_ROLE_FIT = +2
```

기계 판정 식별자:

```text
EXPLICIT_PRIMARY_MATERIAL_BY_EQUIPMENT_GROUP
```

### 2.1 철 `iron`

철은 범용 기준 재료다.

| 장비군 | 역할 적합 | 보정 |
|---|---|---:|
| `SWORD` | `STANDARD_ROLE_FIT` | 0 |
| `AXE` | `STANDARD_ROLE_FIT` | 0 |
| `BLUNT` | `STANDARD_ROLE_FIT` | 0 |
| `POLEARM` | `STANDARD_ROLE_FIT` | 0 |
| `RANGED` | `STANDARD_ROLE_FIT` | 0 |
| `SHIELD_SUPPORT` | `STANDARD_ROLE_FIT` | 0 |
| `LIGHT_ARMOR` | `STANDARD_ROLE_FIT` | 0 |
| `MEDIUM_ARMOR` | `STANDARD_ROLE_FIT` | 0 |
| `HEAVY_ARMOR` | `STANDARD_ROLE_FIT` | 0 |

### 2.2 은 `silver`

| 장비군 | 역할 적합 | 보정 |
|---|---|---:|
| `SWORD` | `HIGH_ROLE_FIT` | +2 |
| `RANGED` | `HIGH_ROLE_FIT` | +2 |
| `LIGHT_ARMOR` | `HIGH_ROLE_FIT` | +2 |
| `SHIELD_SUPPORT` | `STANDARD_ROLE_FIT` | 0 |
| `MEDIUM_ARMOR` | `STANDARD_ROLE_FIT` | 0 |
| `AXE` | `LOW_ROLE_FIT` | -2 |
| `BLUNT` | `LOW_ROLE_FIT` | -2 |
| `POLEARM` | `LOW_ROLE_FIT` | -2 |
| `HEAVY_ARMOR` | `LOW_ROLE_FIT` | -2 |

### 2.3 운석철 `meteor_iron`

| 장비군 | 역할 적합 | 보정 |
|---|---|---:|
| `AXE` | `HIGH_ROLE_FIT` | +2 |
| `BLUNT` | `HIGH_ROLE_FIT` | +2 |
| `POLEARM` | `HIGH_ROLE_FIT` | +2 |
| `HEAVY_ARMOR` | `HIGH_ROLE_FIT` | +2 |
| `SWORD` | `STANDARD_ROLE_FIT` | 0 |
| `SHIELD_SUPPORT` | `STANDARD_ROLE_FIT` | 0 |
| `MEDIUM_ARMOR` | `STANDARD_ROLE_FIT` | 0 |
| `RANGED` | `LOW_ROLE_FIT` | -2 |
| `LIGHT_ARMOR` | `LOW_ROLE_FIT` | -2 |

### 2.4 적용 제외

```text
TOOL
CLOTHING_OR_ROBE
ACCESSORY
```

위 장비군은 기본 공격·방어 역할 원수치가 없으므로 역할 적합 보정을 적용하지 않는다. 재료 적합이 존재하지 않는 공격·방어를 새로 만들 수 없다.

## 3. 직접 단조 역할 결과

기계 판정 식별자:

```text
DETERMINISTIC_ROLE_STRIKE_THREE_ZONE
```

| 역할 정밀 타격 | `DIRECT_FORGING_ROLE_MODIFIER` |
|---|---:|
| `OUTSIDE_GOOD_ZONE` | -1 |
| `GOOD_ZONE` | 0 |
| `PERFECT_ZONE` | +1 |

자동 제작:

```text
AUTOMATIC_FORGING_ROLE_MODIFIER = 0
```

보호 규칙:

- 결과는 RNG로 정하지 않는다.
- 역할 정밀 타격은 제작 등급 산정 점수와 등급 확률 입력에서 제외한다.
- 제작 등급은 공격·방어 배율로 다시 사용하지 않는다.
- 같은 타격을 등급과 역할 보정에 이중 합산하지 않는다.
- 역할 원수치가 없는 작품에는 적용하지 않는다.
- 자동 제작은 `+1`을 자동 획득하지 않는다.

초보자 온보딩 후 난이도 튜닝 목표:

```text
BELOW_EXPECTED = 20%
EXPECTED = 60%
ABOVE_EXPECTED = 20%
```

허용 관찰 범위:

```text
BELOW_EXPECTED = 10~30%
EXPECTED = 50~70%
ABOVE_EXPECTED = 10~30%
```

이 값은 `HUMAN_DIFFICULTY_TUNING_TARGET`이며 런타임 확률표가 아니다.

## 4. 최초 제작 기능 레시피

기계 판정 모델:

```text
ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY
```

### 4.1 마법 기능

| 기능 | 역할 프로필 | 장비군 | 주재료 | 최소 인정 중량 | 결속 | 비용 |
|---|---|---|---|---:|---|---:|
| `ARCANE_CONDUCTION` | `MAGIC_IMPLEMENT` | `TOOL / CLOTHING_OR_ROBE` | `silver / meteor_iron` | 5 | 없음 | 1 |
| `ELEMENTAL_WARD` | `MAGIC_IMPLEMENT` | `TOOL / CLOTHING_OR_ROBE` | `silver` | 5 | 원소 1개 | 1 |
| `ARCANE_SENSING` | `MAGIC_IMPLEMENT` | `TOOL / CLOTHING_OR_ROBE` | `meteor_iron` | 10 | 마법 흔적 1개 | 2 |

### 4.2 유틸리티 기능

| 기능 | 역할 프로필 | 장비군 | 주재료 | 최소 인정 중량 | 결속 | 비용 |
|---|---|---|---|---:|---|---:|
| `ENVIRONMENTAL_SEALING` | `UTILITY_IMPLEMENT / UTILITY_GARMENT` | `TOOL / CLOTHING_OR_ROBE` | `iron / silver` | 5 | 환경 1개 | 1 |
| `FIELD_SERVICEABILITY` | `UTILITY_IMPLEMENT` | `TOOL` | `iron` | 5 | 없음 | 1 |
| `TASK_INTEGRATION` | `UTILITY_IMPLEMENT / UTILITY_GARMENT` | `TOOL / CLOTHING_OR_ROBE` | `iron / silver / meteor_iron` | 5 | 작업 1개 | 1 |

규칙:

- 레시피가 충족되면 최초 기능은 결정적으로 생성한다.
- 남는 용량이나 중량은 기능을 자동 생성하지 않는다.
- 같은 기능 ID 중복을 허용하지 않는다.
- `MAGIC_IMPLEMENT`는 승인된 기본 작품 설계의 명시적 역할 프로필이어야 한다.
- 비용 2의 `ARCANE_SENSING`은 최초 인정 중량 10 이상인 작품만 수용한다.

## 5. 재작업 기능 레시피

### 5.1 촉매 태그 요구

| 기능 | `ADD / REPLACE` | `REBIND` |
|---|---|---|
| `ARCANE_CONDUCTION` | `arcane_matrix` | 해당 없음 |
| `ELEMENTAL_WARD` | `element:<BOUND_ELEMENT>` | `element:<NEW_ELEMENT>` |
| `ARCANE_SENSING` | `signature:<BOUND_SIGNATURE>` | `signature:<NEW_SIGNATURE>` |
| `ENVIRONMENTAL_SEALING` | `environment:<BOUND_ENVIRONMENT>` | `environment:<NEW_ENVIRONMENT>` |
| `FIELD_SERVICEABILITY` | `service` | 해당 없음 |
| `TASK_INTEGRATION` | `task:<BOUND_TASK>` | `task:<NEW_TASK>` |

### 5.2 현재 촉매 태그 변환

```text
fire -> element:fire
fire -> environment:fire
```

`fire`는 다음을 만족하지 않는다.

```text
arcane_matrix
signature:*
service
task:*
```

현재 `fire` 태그 촉매:

```text
salamander_core
berserker_ember
```

따라서 현재 즉시 가용한 결속 재작업:

```text
ELEMENTAL_WARD(FIRE)
ENVIRONMENTAL_SEALING(FIRE)
```

현재 콘텐츠 미지원:

```text
ARCANE_CONDUCTION
ARCANE_SENSING
FIELD_SERVICEABILITY
TASK_INTEGRATION
```

`guardian_powder`는 기능 태그가 없으므로 중립 기능 촉매로 재해석하지 않는다.

### 5.3 행동 원자성

- `ADD`: 변경 후 총 기능 비용이 용량 이하일 때만 성공한다.
- `REPLACE`: 기존 제거와 신규 추가를 하나의 원자 행동으로 처리한다.
- `REBIND`: 같은 기능 ID를 유지하고 결속만 변경한다.
- `REMOVE`: 촉매 태그는 무시하지만 촉매 1개와 정밀 이정표 1회를 소비한다.
- 실패하면 기존 기능 목록·비용·결속을 보존한다.
- 사용한 정밀 이정표는 반환하지 않는다.

## 6. 사람 플레이테스트 Gate

### 6.1 Stage A — 솔로 설계자 검증

총 `48`케이스를 두 세션으로 수행한다.

| 영역 | 케이스 |
|---|---:|
| 재료 3종 × 역할 장비군 9종 | 27 |
| 역할 정밀 타격 3결과 × 대표 작품 3종 | 9 |
| 최초 기능 레시피 6종 | 6 |
| 재작업 행동·가용성 대표 케이스 | 6 |
| 합계 | 48 |

필수 기록:

```text
case_id
item_group
primary_material
role_fit
role_strike_result
initial_function_recipe
rework_action
candidate_visibility
expected_result
actual_result
confusion_note
ledger_rows
```

### 6.2 Stage B — 외부 검증

```text
외부 플레이어 = 3~5명
세션 = 1인당 45~60분
재료 선택 = 3건
직접 단조 = 3건
기능 최초 제작·재작업 = 2건
설명 인터뷰 = 5분
```

### 6.3 정량 기준

| 항목 | 통과 기준 |
|---|---|
| 재료 방향 이해 | `>= 80%` |
| 중립 과제 단일 재료 독점 | `< 70%` |
| 직접 단조 `-1 / 0 / +1` 이해 | `>= 80%` |
| 초보 결과 분포 | 허용 관찰 범위 안 |
| 일반 강화가 원수치를 자동 변경하지 않음을 이해 | `>= 80%` |
| 가용하지 않은 레시피 선택 시도 | `<= 20%` |
| 실패 시 이정표 비환급 이해 | `>= 80%` |

필수 무결성 기준:

```text
NO_DOUBLE_COUNT = 0건
NO_RECIPELESS_FUNCTION_GENERATION = 0건
NO_REPLACE_INTERMEDIATE_STATE_LOSS = 0건
```

판정:

```text
PASS
= 필수 무결성 기준 전부 충족
+ 정량 지표 7개 중 6개 이상 충족

REVISE
= 필수 무결성 기준은 충족하지만 정량 지표 미달

REJECT
= 필수 무결성 기준 중 하나 이상 실패
```

현재 사람 플레이테스트 상태는 `NOT_RUN`이다.

## 7. Google Sheet 참조

`42_능력치_강화_참조표`에 다음 구역을 둔다.

```text
PRIMARY_MATERIAL_ROLE_FIT
DIRECT_FORGING_ROLE_RESULT
FUNCTION_RECIPE_CATALOG
HUMAN_PLAYTEST_PLAN
```

시트는 GitHub 정본의 조회용 미러이며 권위 문서가 아니다.

## 8. 적대적 보호 규칙

다음을 금지한다.

1. 은·운석철의 가격이나 기존 `base_power`를 역할 적합 보정에 다시 합산
2. 역할 정밀 타격을 제작 등급에도 중복 반영
3. 기능 용량만으로 레시피 없는 기능 생성
4. 현재 데이터에 없는 촉매 태그를 있는 것처럼 표시
5. `guardian_powder`를 승인 없이 중립 기능 촉매로 재해석
6. `REPLACE` 실패 후 기존 기능이 사라지는 중간 상태
7. 플레이테스트 전 수치를 최종 밸런스로 선언
8. 시트 단독 편집으로 GitHub 정본 변경

## 9. 제품 구현 차단

이번 Decision에서는 다음을 변경하지 않는다.

```text
data/crafting/materials.json
data/crafting/weapon_bases.json
data/crafting/forging_balance.json
data/crafting/craftsmanship_grades.json
data/
scripts/
scenes/
assets/
addons/
project.godot
```

제품 데이터 스키마, 제작 미니게임 역할 타격, 기능 레시피 UI, 변동 장부 런타임 구현은 후속 구현 Gate까지 `BLOCKED`다.
