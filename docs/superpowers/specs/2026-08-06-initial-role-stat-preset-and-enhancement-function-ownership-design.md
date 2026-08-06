# Blacksmith R2 최초 역할 수치 프리셋·강화 변동·특수기능 소유권 설계

- 제안 Decision: `BS-ITEM-20260806-05`
- 목표 배치 상태: `R2_BATCH_005_9_OF_10`
- 사용자 지시: 권장안으로 계속 진행하고 구글 시트에 무기 능력치·고객/사용자 능력치·강화 변동을 표로 통합
- 제품 구현: `BLOCKED`
- 권위 원칙: GitHub 정본이 권위이며 Google Sheet는 동일 Decision ID를 사용하는 조회용 미러다.

## 1. 문제

현재 정본은 다음 경계를 확정했다.

- 작품군은 `ATTACK` 또는 `DEFENSE` 하나의 역할 원수치만 필수로 가진다.
- 중량 성능 예산은 역할에 따라 공격·방어 `+5` 또는 기능 용량 `+1`로 환산된다.
- 일반 강화 단계는 사건 성공률에 `+1%p`씩 반영된다.
- 정밀강화 방식과 최초 특수기능 카탈로그는 존재하지만 정확히 어떤 행동이 어떤 수치나 기능을 변경하는지 하나의 변동 장부로 묶이지 않았다.
- Google Sheet에는 관련 결정이 여러 탭에 흩어져 있어 무기 능력치, 고객 능력치, 강화 변동을 한 화면에서 비교하기 어렵다.

## 2. 검토안

### 안 A — 통합 변동 장부

일반 강화, 정밀강화 방식, 기능 재작업의 소유권을 분리하고 모든 변경을 한 행의 출처 장부로 기록한다.

장점:

- 같은 원인의 이중 계산을 차단한다.
- 강화 전후 비교가 간단하다.
- Google Sheet 한 탭에서 작품·고객·강화 규칙을 함께 찾을 수 있다.

### 안 B — 일반 강화가 모든 역할 수치를 자동 증가

장점은 단순함이지만 정밀강화 방식, 중량 예산, 작품 제작 결과의 의미가 약해진다.

### 안 C — 공격·방어·취급·예술성·기능을 독립 성장 시스템으로 분리

세밀하지만 강화 중심 게임을 다중 스탯 관리 게임으로 전도시킨다.

## 3. 선택

`안 A / 통합 변동 장부`를 사용한다.

```text
GENERAL_ENHANCEMENT
= ENHANCEMENT_LEVEL_AND_EVENT_SUCCESS_OWNER

PRECISION_ENHANCEMENT
= EXPLICIT_ITEM_STAT_DELTA_OWNER

FUNCTION_REWORK
= SPECIAL_FUNCTION_LIST_OWNER
```

한 행동은 자기 소유 범위만 변경한다.

## 4. 최초 제작 역할 수치 테스트 프리셋

### 4.1 공식

```text
CRAFTED_ROLE_STAT
= BASE_ITEM_ROLE_BASE
+ PRIMARY_MATERIAL_ROLE_FIT_MODIFIER
+ DIRECT_FORGING_ROLE_MODIFIER
```

최종값은 음수가 될 수 없다.

```text
CRAFTED_ROLE_STAT = max(0, 계산 결과)
```

### 4.2 장비군 기준값

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

### 4.3 주재료 적합 보정

```text
LOW_ROLE_FIT      = -2
STANDARD_ROLE_FIT =  0
HIGH_ROLE_FIT     = +2
```

이 보정은 주재료가 작품의 역할에 얼마나 적합한지를 나타낸다. 등급, 예술성, 중량 출력은 이 보정에 다시 포함하지 않는다.

### 4.4 직접 단조 보정

```text
BELOW_EXPECTED_DIRECT_FORGING = -1
EXPECTED_DIRECT_FORGING       =  0
ABOVE_EXPECTED_DIRECT_FORGING = +1
```

직접 단조 보정은 최초 제작 완료 시 한 번 확정되며 같은 UID에서 다시 굴리지 않는다.

### 4.5 상태

모든 수치는 `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`다. 제작 등급은 역할 수치를 자동 배율 증가시키지 않고, 예술성도 공격·방어를 자동 변경하지 않는다.

## 5. 표시 공격·방어

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

각 출력에는 독립된 출처 키가 있어야 한다.

```text
CRAFTED_ROLE_STAT_LEDGER
WEIGHT_OUTPUT_LEDGER
PRECISION_ENHANCEMENT_DELTA_LEDGER
```

같은 원천을 둘 이상의 장부에 기록하지 않는다.

## 6. 일반 강화 변동 소유권

일반 강화는 다음만 변경한다.

```text
ENHANCEMENT_LEVEL += 1 on successful level gain
GENERAL_EVENT_SUCCESS_BONUS = ENHANCEMENT_LEVEL × 1%p
```

일반 강화가 자동 변경하지 않는 값:

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

강화 성공, 유지, 하락, 손상·대파와 보호 변환 규칙은 기존 강화 정본을 유지한다. 이 Decision은 확률과 파괴 경제를 변경하지 않는다.

## 7. 정밀강화 방식별 테스트 변동

`+10/+20/+30/+40/+50` 이정표에서 성공한 정밀강화는 한 가지 출력 패키지만 선택한다. 선택은 해당 이정표 기회를 소비한다.

| 정밀강화 방식 | 출력 차선 | 적용 대상 | 테스트 변동 | 추가 규칙 |
|---|---|---|---|---|
| `EDGE_REINFORCEMENT` | `STAT_METHOD` | `ATTACK` 보유 작품 | `APPROVED_ENHANCEMENT_ATTACK_OUTPUT +5` | 방어 작품에는 표시하지 않음 |
| `SHOCK_ABSORPTION` | `STAT_METHOD` | `DEFENSE` 보유 작품 | `APPROVED_ENHANCEMENT_DEFENSE_OUTPUT +5` | 공격 전용 작품에는 표시하지 않음 |
| `BALANCE_TUNING` | `STAT_METHOD` | 취급 가능한 작품 | `HANDLING +5` | 공격·방어를 동시에 올리지 않음 |
| `ARTISTIC_FINISH` | `STAT_METHOD` | 모든 호환 작품 | `ARTISTRY +5` | 전투 출력 자동 증가 없음 |
| `LIGHTWEIGHTING` | `STAT_METHOD` | 중량 5 이상 작품 | `CURRENT_WEIGHT -5` | 이전 성능 예산·배분 출력 보존 |
| `WEIGHTING` | `STAT_METHOD` | 중량화 가능 작품 | `CURRENT_WEIGHT +5` | 새 인정 최고 중량일 때만 역할 출력 `+5` 또는 기능 용량 `+1` |
| `ENVIRONMENTAL_TREATMENT` | `FUNCTION_REWORK` | 승인된 환경 기능 레시피가 있는 작품 | 승인 환경 기능 `ADD / REPLACE / REBIND / REMOVE` 중 하나 | 같은 이정표에서 별도 수치 패키지를 받지 않음 |

이 수치 역시 `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`다.

## 8. 특수기능 소유권

### 8.1 최초 획득

최초 제작 시 기능은 다음 조건을 모두 만족할 때만 생성한다.

1. 기본 작품 설계가 승인된 기능 ID를 명시한다.
2. 초기 기능 용량 총합이 비용 합계 이상이다.
3. 필요한 결속 맥락이 정의되어 있다.

중량이나 남는 용량만으로 기능을 자동 생성하지 않는다.

### 8.2 제작 후 변경

제작 후 특수기능 변경의 유일한 소유자는 `FUNCTION_REWORK`다.

```text
PRECISION_OUTPUT_LANE
= STAT_METHOD
| FUNCTION_REWORK
```

- 정밀 이정표 한 번에 `STAT_METHOD`와 `FUNCTION_REWORK`를 동시에 적용하지 않는다.
- 기능 재작업은 해당 이정표 기회를 소비한다.
- `ENVIRONMENTAL_TREATMENT`는 승인된 환경 기능 레시피에 한해 `FUNCTION_REWORK` 차선을 사용한다.
- 다른 마법·유틸리티 기능은 작품별 승인 재작업 레시피가 있을 때만 `FUNCTION_REWORK` 후보가 된다.
- 일반 강화는 기능을 생성·교체·제거·결속 변경하지 않는다.
- 중량화는 용량만 늘릴 수 있고 기능 목록은 변경하지 않는다.

### 8.3 기능 재작업 행동

```text
ADD
REPLACE
REBIND
REMOVE
```

- `ADD`: 남은 용량 안에서 승인 기능을 추가한다.
- `REPLACE`: 기존 기능 제거와 새 기능 추가를 원자적으로 처리하고 최종 비용 합계를 검사한다.
- `REBIND`: 같은 기능 ID의 결속 맥락만 변경한다.
- `REMOVE`: 기능을 제거해 용량을 비우지만 이정표 기회는 반환하지 않는다.
- 실패한 정밀 재작업은 기존 기능 목록과 결속을 그대로 보존한다.
- 같은 기능 ID 중복은 허용하지 않는다.

### 8.4 강한 기능

숨은 기능 레벨이나 범용 배율은 사용하지 않는다. 더 강한 기능은 별도의 승인 기능 ID와 더 높은 용량 비용을 가진다.

```text
STANDARD = cost 1
STRONG_OR_MULTI_CONTEXT = cost 2
TRANSFORMATIVE_OR_RULE_BYPASS = cost 3 + separate design approval
```

현재 최초 기능 6종의 제작 후 획득 레시피는 제품 구현 전에 작품별로 승인해야 한다. 레시피가 없으면 기능 재작업 후보에 표시하지 않는다.

## 9. 변동 장부

모든 작품 수치·기능 변경은 다음 구조로 기록한다.

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

한 행동이 여러 필드를 변경할 수 있지만 각 필드는 한 행으로 기록한다. `WEIGHTING`처럼 중량과 역할 출력이 함께 변할 때도 `CURRENT_WEIGHT`와 역할 출력은 별도 행으로 기록하되 같은 `source_action_id`를 사용한다.

## 10. 고객/사용자 능력치 조회 계약

Google Sheet에서 사용자의 표현인 `유저능력치`는 게임 내 장비 사용자, 즉 고객 능력치로 명시한다.

| 능력 | 범위 | 장비 판정 역할 | 작품 원수치 변경 여부 |
|---|---:|---|---|
| `STRENGTH` | 1~10 | `MAXIMUM_LOAD = STRENGTH × 10` | 변경하지 않음 |
| `DEXTERITY` | 1~10 | 관련 사건 능력 조건 | 변경하지 않음 |
| `CONSTITUTION` | 1~10 | 관련 사건 능력 조건 | 변경하지 않음 |
| `JUDGMENT` | 1~10 | 관련 사건·특수기능 통제 조건 | 변경하지 않음 |
| 무기/방어구 적성 | 0~3 | `-10 / 0 / +5 / +10%p` | 변경하지 않음 |
| `MAGIC_APTITUDE` | 0~10 | 마법 기능 사용 자격·위험 | 변경하지 않음 |
| 마법 친화 태그 | 최대 2 | 결속 기능 호환 | 변경하지 않음 |

관련 능력치가 위험도 이상이면 기존대로 `+5%p`, 미만이면 `0%p`다. 고객 능력치는 작품 공격·방어에 직접 더하지 않는다.

## 11. Google Sheet 설계

새 탭:

```text
42_능력치_강화_참조표
```

한 탭에 다음 네 표를 둔다.

1. `작품·무기 능력치와 최초 제작 프리셋`
2. `고객/사용자 능력치와 판정 용도`
3. `일반·정밀강화 변동표`
4. `특수기능 용량·획득·재작업표`

탭 상단에는 Decision ID, 배치 카운터, exact head, 기획 전용 상태, 플레이테스트 상태를 표시한다. 표 값은 GitHub 정본의 조회용 미러이며 시트 단독 편집으로 정본을 변경하지 않는다.

시트 기본 시각 규칙:

- 제목 행: 진한 회색, 흰색 굵은 글씨
- 표 머리글: 기존 탭과 같은 연회색, 가운데 정렬, 굵은 글씨
- 본문: 흰 배경, 위쪽 정렬, 자동 줄바꿈
- 첫 3행 고정
- 수치 상태는 `APPROVED`, `BASELINE_TEST_PRESET`, `BLOCKED`, `NOT_RUN`을 텍스트로 함께 표시

## 12. 적대적 보호 조건

- 일반 강화 단계와 작품 공격·방어의 자동 이중 성장 금지
- 제작 등급·예술성·중량·정밀강화의 같은 원인 이중 계산 금지
- 한 정밀 이정표에서 수치 패키지와 기능 재작업 동시 획득 금지
- 남는 기능 용량 또는 중량화에 의한 기능 자동 생성 금지
- 기능 제거·재결속의 무료 무한 재굴림 금지
- 실패한 기능 재작업이 기존 기능을 임의 교체하는 구조 금지
- 고객 능력치를 작품 원수치에 직접 합산하는 구조 금지
- Google Sheet가 GitHub 권위 정본보다 앞서는 구조 금지
- 플레이테스트 전 테스트 프리셋을 최종 밸런스로 표현하는 행위 금지

## 13. 검증 계획

TDD RED 계약은 다음 부재 때문에 실패해야 한다.

- `BS-ITEM-20260806-05`
- `R2_BATCH_005_9_OF_10`
- 최초 역할 수치 기준값과 두 보정표
- 일반 강화 무변동 목록
- 정밀강화 7방식 변동표와 상호배타 출력 차선
- `FUNCTION_REWORK` 소유권과 행동 4종
- 변동 장부 필드
- Google Sheet 새 탭 동기화 상태

GREEN에서는 기존 계약 전체를 보존하고 신규 계약만 충족한다. 제품 보호 경로는 계속 0건이어야 한다.

## 14. 후속 Gate

- 작품별 특수기능 제작·재작업 레시피
- 정밀강화 수치의 사람 플레이테스트
- 주재료 역할 적합 목록
- 직접 단조 결과 분포
- 강화 변동 장부의 제품 데이터 스키마와 UI

제품 구현은 계속 `BLOCKED`다.
