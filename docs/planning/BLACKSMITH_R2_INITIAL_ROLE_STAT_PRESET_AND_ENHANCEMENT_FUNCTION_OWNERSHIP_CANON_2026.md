# [현재 정본] Blacksmith R2 최초 역할 수치 프리셋·강화 변동·특수기능 소유권 Canon

- Decision: `BS-ITEM-20260806-05`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_9_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-ITEM-20260806-04 / BS-CRAFT-20260804-04 / BS-CUSTOMER-20260806-01 / BS-ITEM-20260806-03 / BS-CRAFT-20260805-02`
- 밸런스 상태: `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`
- Google Sheet 미러: `42_능력치_강화_참조표`
- 제품 구현: `BLOCKED`

## 1. 핵심 결론

Blacksmith의 작품 변화는 한 행동이 자기 소유 범위만 변경하는 통합 변동 장부로 관리한다.

```text
GENERAL_ENHANCEMENT
= ENHANCEMENT_LEVEL_AND_EVENT_SUCCESS_OWNER

PRECISION_ENHANCEMENT
= EXPLICIT_ITEM_STAT_DELTA_OWNER

FUNCTION_REWORK
= SPECIAL_FUNCTION_LIST_OWNER
```

- 일반 강화는 강화 단계와 일반 사건 성공률 보정만 소유한다.
- 정밀강화의 `STAT_METHOD` 차선은 명시된 작품 수치만 변경한다.
- 정밀강화의 `FUNCTION_REWORK` 차선은 특수기능 목록만 변경한다.
- 한 정밀 이정표에서 두 차선을 동시에 적용하지 않는다.
- 모든 수치와 기능 변경은 `ITEM_CHANGE_LEDGER_ENTRY`로 출처를 남긴다.

## 2. 최초 제작 역할 수치

### 2.1 공식

```text
CRAFTED_ROLE_STAT
= max(
    0,
    BASE_ITEM_ROLE_BASE
    + PRIMARY_MATERIAL_ROLE_FIT_MODIFIER
    + DIRECT_FORGING_ROLE_MODIFIER
  )
```

기계 판정 식별자:

```text
MAX_ZERO_BASE_PLUS_MATERIAL_FIT_PLUS_DIRECT_FORGING
```

### 2.2 장비군 기준값

| 장비군 | 역할 수치 | `BASE_ITEM_ROLE_BASE` |
|---|---|---:|
| `SWORD` | `ATTACK` | 5 |
| `RANGED` | `ATTACK` | 5 |
| `AXE` | `ATTACK` | 10 |
| `BLUNT` | `ATTACK` | 10 |
| `POLEARM` | `ATTACK` | 15 |
| `SHIELD_SUPPORT` | `DEFENSE` | 5 |
| `LIGHT_ARMOR` | `DEFENSE` | 5 |
| `MEDIUM_ARMOR` | `DEFENSE` | 10 |
| `HEAVY_ARMOR` | `DEFENSE` | 15 |
| `TOOL` | 없음 | 없음 |
| `CLOTHING_OR_ROBE` | 없음 | 없음 |
| `ACCESSORY` | 없음 | 없음 |

### 2.3 주재료 적합 보정

```text
LOW_ROLE_FIT      = -2
STANDARD_ROLE_FIT =  0
HIGH_ROLE_FIT     = +2
```

주재료 적합 보정은 작품 역할에 대한 재료 적합만 표현한다. 제작 등급, 예술성, 중량 출력, 강화 단계는 이 보정에 포함하지 않는다.

### 2.4 직접 단조 보정

```text
BELOW_EXPECTED_DIRECT_FORGING = -1
EXPECTED_DIRECT_FORGING       =  0
ABOVE_EXPECTED_DIRECT_FORGING = +1
```

직접 단조 보정은 최초 제작 완료 시 한 번 확정하며 같은 UID에서 무료 재굴림하지 않는다.

### 2.5 예시

표준 재료와 기대 수준 단조를 기준으로 한다.

```text
검       CRAFTED_ATTACK 5  + WEIGHT_ATTACK_OUTPUT 10 = DISPLAY_ATTACK 15
도끼     CRAFTED_ATTACK 10 + WEIGHT_ATTACK_OUTPUT 15 = DISPLAY_ATTACK 25
장병기   CRAFTED_ATTACK 15 + WEIGHT_ATTACK_OUTPUT 20 = DISPLAY_ATTACK 35
경갑     CRAFTED_DEFENSE 5  + WEIGHT_DEFENSE_OUTPUT 10 = DISPLAY_DEFENSE 15
중갑     CRAFTED_DEFENSE 10 + WEIGHT_DEFENSE_OUTPUT 20 = DISPLAY_DEFENSE 30
중장갑   CRAFTED_DEFENSE 15 + WEIGHT_DEFENSE_OUTPUT 30 = DISPLAY_DEFENSE 45
```

이 예시는 최종 밸런스가 아니라 테스트 프리셋이다.

## 3. 표시 공격·방어와 출처 분리

기존 공식을 유지한다.

```text
DISPLAY_ATTACK
= CRAFTED_ATTACK
+ WEIGHT_ATTACK_OUTPUT
+ APPROVED_ENHANCEMENT_ATTACK_OUTPUT

DISPLAY_DEFENSE
= CRAFTED_DEFENSE
+ WEIGHT_DEFENSE_OUTPUT
+ APPROVED_ENHANCEMENT_DEFENSE_OUTPUT
```

출처 장부는 다음처럼 분리한다.

```text
CRAFTED_ROLE_STAT_LEDGER
WEIGHT_OUTPUT_LEDGER
PRECISION_ENHANCEMENT_DELTA_LEDGER
```

- 같은 주재료·중량·강화 원인을 둘 이상의 장부에 기록하지 않는다.
- 제작 등급은 역할 수치를 자동 배율 증가시키지 않는다.
- 예술성은 공격·방어를 자동 변경하지 않는다.
- 고객 능력치는 작품 공격·방어에 직접 더하지 않는다.

## 4. 일반 강화 소유권

일반 강화의 현재 소유 범위는 다음뿐이다.

```text
ENHANCEMENT_LEVEL += 1 on successful level gain
GENERAL_EVENT_SUCCESS_BONUS = ENHANCEMENT_LEVEL × 1%p
```

일반 강화가 자동 변경하지 않는 작품 필드:

```text
ATTACK
DEFENSE
WEIGHT
DURABILITY
HANDLING
ARTISTRY
MAGIC_FUNCTION_CAPACITY
UTILITY_CAPACITY
SPECIAL_FUNCTIONS
```

- 성공·유지·하락·손상·대파·보호 변환 규칙은 기존 강화 정본을 유지한다.
- 일반 강화 단계가 공격·방어를 다시 올려 중량 출력과 이중 성장하는 구조는 사용하지 않는다.
- `+20` 작품은 일반 사건 성공률에 기존대로 `+20%p`를 제공하지만 작품 `ATTACK / DEFENSE`에 자동 `+20`을 받지 않는다.

## 5. 정밀강화 출력 차선

```text
PRECISION_OUTPUT_LANE
= STAT_METHOD
| FUNCTION_REWORK
```

- 정밀 이정표: `+10 / +20 / +30 / +40 / +50`
- 한 이정표에서 한 차선만 선택한다.
- 성공한 선택은 해당 이정표 기회를 소비한다.
- 사용한 이정표 기회는 반환하지 않는다.

## 6. 정밀강화 방식별 테스트 변동

| 방식 | 출력 차선 | 적용 대상 | 테스트 변동 | 보호 규칙 |
|---|---|---|---|---|
| `EDGE_REINFORCEMENT` | `STAT_METHOD` | `ATTACK` 보유 작품 | `APPROVED_ENHANCEMENT_ATTACK_OUTPUT +5` | 방어 작품에는 표시하지 않음 |
| `SHOCK_ABSORPTION` | `STAT_METHOD` | `DEFENSE` 보유 작품 | `APPROVED_ENHANCEMENT_DEFENSE_OUTPUT +5` | 공격 전용 작품에는 표시하지 않음 |
| `BALANCE_TUNING` | `STAT_METHOD` | 취급 가능한 작품 | `HANDLING +5` | 공격·방어를 동시에 올리지 않음 |
| `ARTISTIC_FINISH` | `STAT_METHOD` | 호환 작품 | `ARTISTRY +5` | 전투 출력 자동 증가 없음 |
| `LIGHTWEIGHTING` | `STAT_METHOD` | 현재 중량 5 이상 | `CURRENT_WEIGHT -5` | 기존 성능 예산과 배분 출력 보존 |
| `WEIGHTING` | `STAT_METHOD` | 중량화 가능 작품 | `CURRENT_WEIGHT +5` | 새 인정 최고 중량일 때만 역할 출력 `+5` 또는 기능 용량 `+1` |
| `ENVIRONMENTAL_TREATMENT` | `FUNCTION_REWORK` | 승인 환경 기능 레시피 보유 작품 | 환경 기능 `ADD / REPLACE / REBIND / REMOVE` 중 하나 | 별도 수치 패키지 동시 획득 금지 |

정밀강화 수치는 모두 `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`다.

## 7. 특수기능 최초 획득

최초 제작 시 다음을 모두 만족해야 기능을 생성할 수 있다.

1. 기본 작품 설계가 승인된 기능 ID를 명시한다.
2. 초기 기능 용량이 기능 비용 합계 이상이다.
3. 결속이 필요한 기능은 결속 맥락을 가진다.

남는 용량이나 초기 중량만으로 기능을 자동 생성하지 않는다.

## 8. 제작 후 기능 재작업

제작 후 특수기능 변경의 유일한 소유자는 `FUNCTION_REWORK`다.

```text
FUNCTION_REWORK_ACTION
= ADD
| REPLACE
| REBIND
| REMOVE
```

### `ADD`

- 승인된 기능 레시피가 있어야 한다.
- 변경 후 총비용이 기능 용량을 넘지 않아야 한다.
- 같은 기능 ID를 중복 추가하지 않는다.

### `REPLACE`

- 기존 기능 제거와 새 기능 추가를 하나의 원자적 결과로 처리한다.
- 최종 기능 비용 합계를 다시 검사한다.
- 실패하면 기존 기능을 그대로 보존한다.

### `REBIND`

- 기능 ID는 유지하고 결속 맥락만 변경한다.
- 무료 재결속이 아니며 정밀 이정표 기회를 소비한다.

### `REMOVE`

- 기능을 제거하고 용량을 비운다.
- 사용한 정밀 이정표 기회는 반환하지 않는다.
- 제거가 새 기능을 자동 생성하지 않는다.

공통 규칙:

- 일반 강화는 기능을 생성·교체·제거·재결속하지 않는다.
- 중량화는 기능 용량만 늘릴 수 있고 기능 목록을 변경하지 않는다.
- 실패한 기능 재작업은 기존 기능 ID·비용·결속을 보존한다.
- 숨은 기능 레벨이나 같은 ID의 수치 누적은 사용하지 않는다.
- 강한 기능은 별도 승인 ID와 더 높은 기능 비용을 사용한다.
- 작품별 승인 재작업 레시피가 없으면 후보에 표시하지 않는다.

## 9. 기능 비용

기존 비용 계약을 유지한다.

```text
STANDARD_APPROVED_FUNCTION = 1
STRONG_OR_MULTI_CONTEXT_FUNCTION = 2
TRANSFORMATIVE_OR_RULE_BYPASS_FUNCTION = 3
```

용량 3의 규칙 변환·예외·우회 기능은 별도 기획 승인이 필요하다.

## 10. 통합 변동 장부

```text
ITEM_CHANGE_LEDGER_ENTRY
- item_uid
- source_action_id
- source_owner
- enhancement_level_before
- enhancement_level_after
- changed_field
- value_before
- value_after
- delta_or_operation
- precision_milestone
- decision_id
```

- 한 행은 변경 필드 하나만 기록한다.
- 한 행동이 여러 필드를 바꾸면 같은 `source_action_id`를 사용하는 여러 행으로 기록한다.
- `WEIGHTING`은 `CURRENT_WEIGHT` 행과 새 최고 인정 중량에서 발생한 역할 출력 행을 분리한다.
- `FUNCTION_REWORK`는 기능 ID 변경과 결속 변경을 필요한 만큼 별도 행으로 기록한다.
- 장부는 제품 데이터 구현 전에 스키마화하며 현재 제품 구현은 차단한다.

## 11. 고객/사용자 능력치 참조

여기서 `사용자`는 작품을 장비하는 게임 내 고객을 뜻한다.

| 능력 | 범위 | 장비·사건 판정 역할 | 작품 공격·방어 변경 |
|---|---:|---|---|
| `STRENGTH` | `1~10` | `MAXIMUM_LOAD = STRENGTH × 10` | 없음 |
| `DEXTERITY` | `1~10` | 관련 사건 능력 조건 | 없음 |
| `CONSTITUTION` | `1~10` | 관련 사건 능력 조건 | 없음 |
| `JUDGMENT` | `1~10` | 관련 사건·특수기능 통제 조건 | 없음 |
| `EQUIPMENT_PROFICIENCY` | `0~3` | `-10 / 0 / +5 / +10%p` | 없음 |
| `MAGIC_APTITUDE` | `0~10` | 마법 기능 사용 자격·위험 | 없음 |
| `MAGIC_AFFINITY_TAGS` | `0~2개` | 결속 기능 호환 | 없음 |

- 관련 능력이 사건 위험도 이상이면 `+5%p`, 미만이면 `0%p`다.
- 중량 초과 또는 필수 기능 미충족은 성공률 계산 전에 배정을 차단한다.
- 고객 능력·적성은 강화보다 작은 보조 판정으로 유지한다.

## 12. Google Sheet 미러 계약

조회용 탭:

```text
42_능력치_강화_참조표
```

필수 구역:

```text
ITEM_WEAPON_STATS
CUSTOMER_USER_STATS
ENHANCEMENT_DELTAS
SPECIAL_FUNCTION_REWORK
```

- GitHub 정본이 권위이며 시트는 조회용 미러다.
- 시트 단독 편집은 이 Decision을 변경하지 않는다.
- 상단에 Decision ID, `9/10`, exact head, 제품 차단, 플레이테스트 미실행 상태를 표시한다.
- 작품·무기 수치, 고객/사용자 수치, 강화 변동, 기능 획득·재작업 규칙을 한 탭의 네 표로 제공한다.

## 13. 적대적 보호 조건

- 일반 강화와 정밀강화가 같은 작품 수치를 자동 중복 증가시키는 구조 금지
- 제작·중량·강화의 같은 원천 이중 계산 금지
- 한 정밀 이정표에서 수치 패키지와 기능 재작업 동시 획득 금지
- 남는 기능 용량 또는 중량화에 의한 기능 자동 생성 금지
- 기능 제거·재결속의 무료 무한 재굴림 금지
- 실패한 기능 재작업이 기존 기능을 임의 교체하는 구조 금지
- 고객 능력치를 작품 공격·방어에 직접 합산하는 구조 금지
- 테스트 프리셋을 플레이테스트 없이 최종 밸런스로 선언하는 행위 금지
- Google Sheet가 GitHub 정본보다 우선하는 구조 금지

## 14. 검증·구현 경계

- 정본·레지스트리·현재 진입점·계약 테스트·운영 감사만 갱신한다.
- `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 변경 금지
- `data/crafting/weapon_bases.json` 변경 금지
- 실제 수치·기능 효과 사람 플레이테스트: `NOT_RUN`
- 제품 구현: `BLOCKED`

## 15. 후속 Gate

- 작품별 특수기능 최초 제작·재작업 레시피
- 주재료별 역할 적합 목록
- 직접 단조 결과 분포
- 정밀강화 수치 사람 플레이테스트 계획
- 통합 변동 장부 제품 데이터 스키마·UI
