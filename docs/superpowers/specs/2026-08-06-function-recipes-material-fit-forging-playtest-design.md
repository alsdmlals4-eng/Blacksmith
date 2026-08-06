# Blacksmith R2 기능 레시피·주재료 적합·직접 단조·플레이테스트 설계

- Decision: `BS-ITEM-20260806-06`
- 승인 해석: 사용자의 `권장안대로 진행`
- 배치: `R2_BATCH_005_10_OF_10`
- 상태: `USER_APPROVED / APPROVED_PENDING_MERGE`
- 제품 구현: `BLOCKED`
- 수치 상태: `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`
- 선행 정본: `BS-ITEM-20260806-03 / BS-ITEM-20260806-04 / BS-ITEM-20260806-05 / BS-CRAFT-20260804-04`

## 1. 목표

이번 설계는 다음 네 공백을 하나의 마지막 배치 Decision으로 닫는다.

1. 주재료가 어떤 작품 역할에 적합한지 명시한다.
2. `DIRECT_FORGING_ROLE_MODIFIER`의 발생 조건을 확정한다.
3. 승인된 특수기능 6종의 최초 제작·재작업 레시피를 정의한다.
4. 수치가 제품 정본으로 넘어가기 전에 필요한 사람 플레이테스트 절차와 판정 기준을 정의한다.

장비별 모든 조합을 개별 레시피로 열거하지 않는다. 역할 프로필·재료 ID/태그·촉매 태그·결속 맥락으로 판정하는 작은 명시적 레시피 집합을 사용한다.

## 2. 채택 접근

### 2.1 채택

```text
FUNCTION_RECIPE
= FUNCTION_ID
+ ELIGIBLE_ROLE_PROFILE
+ ELIGIBLE_EQUIPMENT_GROUP
+ PRIMARY_MATERIAL_REQUIREMENT
+ MINIMUM_RECOGNIZED_WEIGHT
+ OPTIONAL_BOUND_CONTEXT
+ CAPACITY_COST
+ ACQUISITION_MODE
```

- 최초 제작은 기본 작품 설계와 주재료를 사용한다.
- 제작 후 변경은 정밀강화 이정표의 `FUNCTION_REWORK`만 사용한다.
- 재작업의 `ADD / REPLACE / REBIND`는 기능별 촉매 태그를 요구한다.
- `REMOVE`는 촉매 태그를 무시하지만 정밀 이정표와 촉매 1개를 소비한다.
- 현재 데이터에 없는 촉매 태그는 `CONTENT_NOT_AVAILABLE`로 표시한다.

### 2.2 비채택

- 장비 12종 × 기능 6종의 전수 개별 레시피
- 남는 용량에 따른 무작위 기능 생성
- 레시피 없는 자유 재결속
- 같은 이정표에서 수치 방식과 기능 재작업 동시 적용

## 3. 주재료 역할 적합

`PRIMARY_MATERIAL_ROLE_FIT_MODIFIER`는 역할 원수치가 있는 작품에만 적용한다.

```text
LOW_ROLE_FIT = -2
STANDARD_ROLE_FIT = 0
HIGH_ROLE_FIT = +2
```

### 3.1 철 `iron`

철은 범용 기준 재료다.

| 장비군 | 적합 |
|---|---|
| `SWORD` | `STANDARD_ROLE_FIT` |
| `AXE` | `STANDARD_ROLE_FIT` |
| `BLUNT` | `STANDARD_ROLE_FIT` |
| `POLEARM` | `STANDARD_ROLE_FIT` |
| `RANGED` | `STANDARD_ROLE_FIT` |
| `SHIELD_SUPPORT` | `STANDARD_ROLE_FIT` |
| `LIGHT_ARMOR` | `STANDARD_ROLE_FIT` |
| `MEDIUM_ARMOR` | `STANDARD_ROLE_FIT` |
| `HEAVY_ARMOR` | `STANDARD_ROLE_FIT` |

### 3.2 은 `silver`

은은 경량·정밀 역할에 유리하고 중량·충격 역할에 불리하다.

| 장비군 | 적합 |
|---|---|
| `SWORD` | `HIGH_ROLE_FIT` |
| `RANGED` | `HIGH_ROLE_FIT` |
| `LIGHT_ARMOR` | `HIGH_ROLE_FIT` |
| `SHIELD_SUPPORT` | `STANDARD_ROLE_FIT` |
| `MEDIUM_ARMOR` | `STANDARD_ROLE_FIT` |
| `AXE` | `LOW_ROLE_FIT` |
| `BLUNT` | `LOW_ROLE_FIT` |
| `POLEARM` | `LOW_ROLE_FIT` |
| `HEAVY_ARMOR` | `LOW_ROLE_FIT` |

### 3.3 운석철 `meteor_iron`

운석철은 중량·충격 역할에 유리하고 경량·기민 역할에 불리하다.

| 장비군 | 적합 |
|---|---|
| `AXE` | `HIGH_ROLE_FIT` |
| `BLUNT` | `HIGH_ROLE_FIT` |
| `POLEARM` | `HIGH_ROLE_FIT` |
| `HEAVY_ARMOR` | `HIGH_ROLE_FIT` |
| `SWORD` | `STANDARD_ROLE_FIT` |
| `SHIELD_SUPPORT` | `STANDARD_ROLE_FIT` |
| `MEDIUM_ARMOR` | `STANDARD_ROLE_FIT` |
| `RANGED` | `LOW_ROLE_FIT` |
| `LIGHT_ARMOR` | `LOW_ROLE_FIT` |

### 3.4 비역할 작품

`TOOL / CLOTHING_OR_ROBE / ACCESSORY`는 기본 공격·방어 역할 원수치가 없으므로 위 보정을 적용하지 않는다. 재료는 기능 레시피 자격과 가치·외형 맥락에서만 사용한다.

## 4. 직접 단조 역할 보정

`DIRECT_FORGING_ROLE_MODIFIER`는 전체 제작 등급과 분리된 마지막 역할 정밀 타격 1회의 결과다.

```text
ROLE_STRIKE_RESULT
= OUTSIDE_GOOD_ZONE
| GOOD_ZONE
| PERFECT_ZONE
```

| 결과 | 보정 |
|---|---:|
| `OUTSIDE_GOOD_ZONE` | `-1` |
| `GOOD_ZONE` | `0` |
| `PERFECT_ZONE` | `+1` |

보호 규칙:

- RNG로 결정하지 않는다.
- 전체 제작 등급을 다시 공격·방어 배율로 사용하지 않는다.
- 역할 정밀 타격은 제작 등급 산정 점수와 등급 확률 입력에서 제외한다.
- 같은 역할 정밀 타격을 등급과 역할 보정에 중복 합산하지 않는다.
- 자동 제작은 `EXPECTED_DIRECT_FORGING = 0`을 사용하며 `+1`을 자동 획득하지 않는다.
- 역할 원수치가 없는 작품에는 적용하지 않는다.

초보자 온보딩 후 목표 분포:

```text
BELOW_EXPECTED 20%
EXPECTED 60%
ABOVE_EXPECTED 20%
```

허용 관찰 범위:

```text
BELOW_EXPECTED 10~30%
EXPECTED 50~70%
ABOVE_EXPECTED 10~30%
```

이 분포는 런타임 확률표가 아니라 난이도 튜닝을 위한 사람 플레이테스트 목표다.

## 5. 최초 제작 기능 레시피

### 5.1 마법 기능

| 기능 | 역할 프로필 | 장비군 | 주재료 | 최소 인정 중량 | 결속 | 비용 |
|---|---|---|---|---:|---|---:|
| `ARCANE_CONDUCTION` | `MAGIC_IMPLEMENT` | `TOOL / CLOTHING_OR_ROBE` | `silver / meteor_iron` | 5 | 없음 | 1 |
| `ELEMENTAL_WARD` | `MAGIC_IMPLEMENT` | `TOOL / CLOTHING_OR_ROBE` | `silver` | 5 | 원소 1개 | 1 |
| `ARCANE_SENSING` | `MAGIC_IMPLEMENT` | `TOOL / CLOTHING_OR_ROBE` | `meteor_iron` | 10 | 마법 흔적 1개 | 2 |

- `MAGIC_IMPLEMENT`는 승인된 기본 작품 설계의 명시적 역할 프로필이어야 한다.
- 기본 중량 5인 작품은 비용 1 기능만 수용한다.
- `ARCANE_SENSING`은 최초 인정 중량 10 이상인 승인 작품 설계에서만 최초 제작 가능하다.

### 5.2 유틸리티 기능

| 기능 | 역할 프로필 | 장비군 | 주재료 | 최소 인정 중량 | 결속 | 비용 |
|---|---|---|---|---:|---|---:|
| `ENVIRONMENTAL_SEALING` | `UTILITY_IMPLEMENT / UTILITY_GARMENT` | `TOOL / CLOTHING_OR_ROBE` | `iron / silver` | 5 | 환경 1개 | 1 |
| `FIELD_SERVICEABILITY` | `UTILITY_IMPLEMENT` | `TOOL` | `iron` | 5 | 없음 | 1 |
| `TASK_INTEGRATION` | `UTILITY_IMPLEMENT / UTILITY_GARMENT` | `TOOL / CLOTHING_OR_ROBE` | `iron / silver / meteor_iron` | 5 | 작업 1개 | 1 |

최초 제작 기능은 레시피가 충족되면 결정적으로 생성한다. 무작위 기능 생성과 같은 ID 중복은 허용하지 않는다.

## 6. 재작업 기능 레시피

### 6.1 촉매 태그 계약

| 기능 | `ADD / REPLACE` 요구 태그 | `REBIND` 요구 태그 |
|---|---|---|
| `ARCANE_CONDUCTION` | `arcane_matrix` | 해당 없음 |
| `ELEMENTAL_WARD` | `element:<BOUND_ELEMENT>` | `element:<NEW_ELEMENT>` |
| `ARCANE_SENSING` | `signature:<BOUND_SIGNATURE>` | `signature:<NEW_SIGNATURE>` |
| `ENVIRONMENTAL_SEALING` | `environment:<BOUND_ENVIRONMENT>` | `environment:<NEW_ENVIRONMENT>` |
| `FIELD_SERVICEABILITY` | `service` | 해당 없음 |
| `TASK_INTEGRATION` | `task:<BOUND_TASK>` | `task:<NEW_TASK>` |

### 6.2 현재 촉매 콘텐츠 가용성

현재 촉매 데이터에서 `fire` 태그를 가진 촉매:

- `salamander_core`
- `berserker_ember`

촉매 태그 변환 규칙:

```text
fire -> element:fire
fire -> environment:fire
```

`fire`는 `arcane_matrix / signature:* / service / task:*`를 만족하지 않는다.

따라서 현재 정본에서 즉시 가용한 결속 재작업은 다음뿐이다.

```text
ELEMENTAL_WARD(FIRE)
ENVIRONMENTAL_SEALING(FIRE)
```

다음 기능 재작업은 레시피 계약은 승인하지만 대응 촉매 콘텐츠가 없어 `CONTENT_NOT_AVAILABLE`이다.

```text
ARCANE_CONDUCTION
ARCANE_SENSING
FIELD_SERVICEABILITY
TASK_INTEGRATION
```

`guardian_powder`는 기능 재작업 태그가 없으므로 임의의 중립 기능 촉매로 재해석하지 않는다.

### 6.3 행동별 원자성

- `ADD`: 변경 후 총 기능 비용이 용량 이하일 때만 성공한다.
- `REPLACE`: 기존 제거와 신규 추가를 하나의 원자 행동으로 처리한다.
- `REBIND`: 같은 기능 ID를 유지하고 결속만 변경한다.
- `REMOVE`: 어떤 촉매든 1개와 정밀 이정표 1회를 소비하고 기능을 제거한다.
- 실패하면 기존 기능 목록·비용·결속을 보존한다.
- 소비한 정밀 이정표는 반환하지 않는다.

## 7. 사람 플레이테스트 계획

### 7.1 Stage A — 솔로 설계자 검증

총 48케이스를 두 세션으로 수행한다.

| 영역 | 케이스 |
|---|---:|
| 재료 3종 × 역할 장비군 9종 | 27 |
| 역할 정밀 타격 3결과 × 대표 작품 3종 | 9 |
| 최초 기능 레시피 6종 | 6 |
| 재작업 기능 행동·가용성 대표 케이스 | 6 |
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

### 7.2 Stage B — 외부 3~5명

- 1인당 45~60분
- 재료 선택 3건
- 직접 단조 3건
- 기능 최초 제작·재작업 2건
- 결과 설명 인터뷰 5분

### 7.3 통과 기준

| 항목 | 통과 기준 |
|---|---|
| 재료 방향 이해 | 적합 방향 설명 정답률 `>= 80%` |
| 재료 독점 방지 | 중립 과제에서 단일 재료 선택률 `< 70%` |
| 직접 단조 이해 | `-1 / 0 / +1` 의미 정답률 `>= 80%` |
| 초보 결과 분포 | 각 결과가 허용 관찰 범위 안에 있음 |
| 일반 강화 소유권 | 원수치 자동 상승이 없음을 이해 `>= 80%` |
| 레시피 가시성 | 가용하지 않은 후보 선택 시도율 `<= 20%` |
| 이정표 비용 이해 | 실패해도 기회가 반환되지 않음을 이해 `>= 80%` |
| 장부 무결성 | 같은 원천 이중 합산 `0건` |
| 자동 기능 생성 | 레시피 없는 기능 생성 `0건` |

### 7.4 판정

필수 무결성 기준:

```text
같은 원천 이중 합산 = 0건
레시피 없는 기능 생성 = 0건
REPLACE 실패 중간상태 손실 = 0건
```

```text
PASS
= 모든 필수 무결성 기준 충족
+ 나머지 정량 지표 7개 중 6개 이상 충족

REVISE
= 필수 무결성 기준은 충족하지만 정량 지표가 미달

REJECT
= 필수 무결성 기준 중 하나 이상 실패
```

사람 플레이테스트 결과가 `PASS` 또는 승인된 `REVISE` 후속 Decision으로 정리되기 전에는 수치를 최종 밸런스로 승격하지 않는다.

## 8. Google Sheet

기존 `42_능력치_강화_참조표`에 다음 네 구역을 추가한다.

```text
PRIMARY_MATERIAL_ROLE_FIT
DIRECT_FORGING_ROLE_RESULT
FUNCTION_RECIPE_CATALOG
HUMAN_PLAYTEST_PLAN
```

시트는 GitHub 정본의 조회용 미러이며 권위 문서가 아니다.

## 9. 보호 범위

이번 Decision에서는 다음을 변경하지 않는다.

- `data/crafting/materials.json`
- `data/crafting/weapon_bases.json`
- `data/crafting/forging_balance.json`
- `data/crafting/craftsmanship_grades.json`
- `data/`
- `scripts/`
- `scenes/`
- `assets/`
- `addons/`
- `project.godot`

제품 데이터 스키마·UI·실제 수치 적용은 후속 구현 Gate까지 `BLOCKED`다.
