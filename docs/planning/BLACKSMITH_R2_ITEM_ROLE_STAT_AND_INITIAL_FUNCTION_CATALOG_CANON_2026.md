# [현재 정본] Blacksmith R2 작품 역할 원수치와 최초 특수기능 카탈로그 Canon

- Decision: `BS-ITEM-20260806-04`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_8_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-ITEM-20260806-03 / BS-CUSTOMER-20260805-01 / BS-CRAFT-20260804-04 / BS-UX-20260805-01`
- 역할 원수치 모델: `SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS`
- 제품 구현: `BLOCKED`

## 1. 핵심 결론

작품은 장비군의 기본 역할을 설명하는 원수치 하나만 필수로 가진다. 무기는 공격, 방패·갑옷은 방어를 사용한다. 도구·의복·장신구는 공격·방어를 강제로 저장하지 않으며, 필요한 마법·유틸리티 기능만 별도 승인 기능 인스턴스로 가진다.

```text
ITEM_ROLE_STAT_MODEL = SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS
```

## 2. 작품군별 역할 원수치

| 작품군 | 필수 역할 원수치 | 조건부 원수치 |
|---|---|---|
| `SWORD / AXE / BLUNT / POLEARM / RANGED` | `ATTACK` | `SPECIAL_FUNCTIONS` |
| `SHIELD_SUPPORT` | `DEFENSE` | `STABILITY / SPECIAL_FUNCTIONS` |
| `LIGHT_ARMOR / MEDIUM_ARMOR / HEAVY_ARMOR` | `DEFENSE` | `ENVIRONMENTAL_RESPONSE / SPECIAL_FUNCTIONS` |
| `TOOL / CLOTHING_OR_ROBE / ACCESSORY` | 없음 | `SPECIAL_FUNCTIONS` |

공통 원수치는 기존 계약의 `WEIGHT / DURABILITY / HANDLING / ARTISTRY`를 유지한다. 적용되지 않는 수치는 `0`으로 채우지 않고 생략한다.

## 3. 공격·방어 출처

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

### 3.1 최초 제작 원수치

```text
CRAFTED_ROLE_STAT_DETERMINATION
= FIRST_CRAFT_COMPLETION_SINGLE_STORED_RESULT_WITH_SOURCE_LEDGER
```

최초 제작 원수치는 다음 기여를 하나의 결과로 저장하고 출처 장부에서 구분한다.

```text
BASE_ITEM_DESIGN
PRIMARY_MATERIAL
DIRECT_FORGING_RESULT
```

- 제작 등급과 예술성은 공격·방어를 자동 증폭하지 않는다.
- 중량 출력은 `BS-ITEM-20260806-03`의 환산만 사용한다.
- 강화 출력은 기존 강화 계약에서 명시적으로 승인된 결과만 사용한다.
- 같은 제작·중량·강화 원인을 두 번 합산하지 않는다.

## 4. 기본 스키마에 추가하지 않는 전투 수치

```text
CRITICAL_CHANCE
CRITICAL_DAMAGE
PENETRATION
ACCURACY
ATTACK_SPEED
EVASION
BLOCK_RATE
ELEMENTAL_DAMAGE
```

필요한 개별 효과는 후속 승인된 촉매 수식어·정밀강화 방식·특수기능으로만 표현한다. 기본 작품 비교 화면을 다중 전투 수치 최적화 화면으로 확장하지 않는다.

## 5. 특수기능 저장·용량 계약

```text
SPECIAL_FUNCTIONS = [APPROVED_FUNCTION_INSTANCE]

APPROVED_FUNCTION_INSTANCE
= FUNCTION_ID + CAPACITY_COST + OPTIONAL_BOUND_CONTEXT
```

- `MAGIC_FUNCTION_CAPACITY` 또는 `UTILITY_CAPACITY`는 기능 비용 총합의 상한이다.
- 용량은 고정 슬롯 수가 아니다.
- 같은 `FUNCTION_ID` 중복으로 효과를 누적하지 않는다.
- 남는 용량이 기능을 자동 생성하지 않는다.
- 중량화로 새 용량을 얻어도 기능이 자동 생성되지 않는다.
- 기능은 일반 사건 성공률에 자동 합산하지 않는다.
- 기능은 `ELIGIBILITY / RISK_MITIGATION / SPECIFIC_INTERACTION` 중 하나로 작동한다.

## 6. 최초 승인 마법 기능 카탈로그

### 6.1 `ARCANE_CONDUCTION` — 용량 1

```text
CAN_CHANNEL_MAGIC_THROUGH_ITEM
```

- 작품을 마법의 초점·매개체로 사용할 수 있게 한다.
- 고객의 마력 적성·친화·판단력 요구를 대체하지 않는다.
- 공격·방어·일반 성공률을 직접 올리지 않는다.

### 6.2 `ELEMENTAL_WARD` — 용량 1

```text
MITIGATES_ONE_BOUND_ELEMENTAL_HAZARD
BOUND_ELEMENT required
```

- 불·냉기·번개·독성 등 승인된 하나의 위험 맥락에만 결속한다.
- 피해·손상·실패 위험을 완화하지만 완전 면역을 제공하지 않는다.
- 정확한 완화량은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

### 6.3 `ARCANE_SENSING` — 용량 2

```text
CAN_DETECT_MATCHING_ARCANE_TRACE
BOUND_TRACE_FAMILY required
```

- 결속된 마법 흔적·이상 현상의 존재를 감지할 수 있게 한다.
- 정체·해법·안전 여부를 자동 판정하지 않는다.
- 실제 활용에는 고객 판단력과 마력 적합도가 필요하다.

## 7. 최초 승인 유틸리티 기능 카탈로그

### 7.1 `ENVIRONMENTAL_SEALING` — 용량 1

```text
RESISTS_ONE_BOUND_ENVIRONMENT
BOUND_ENVIRONMENT required
```

- 습기·먼지·부식성 기체·극한 온도 등 승인된 하나의 환경에 대응한다.
- 내구도 손실 또는 환경 위험을 완화하지만 완전 면역을 제공하지 않는다.

### 7.2 `FIELD_SERVICEABILITY` — 용량 1

```text
CAN_PERFORM_FIELD_MAINTENANCE
```

- 공방 밖 일정·원정 중 제한된 유지보수를 허용한다.
- 완전 복원·연대기 손상 삭제·무료 수리를 허용하지 않는다.
- 비용·회복량은 별도 테스트 프리셋에서 관리한다.

### 7.3 `TASK_INTEGRATION` — 용량 1

```text
SUPPORTS_ONE_BOUND_TASK
BOUND_TASK required
```

- 채굴·절단·등반·의식 준비 등 승인된 하나의 작업 맥락을 지원한다.
- 기능 인스턴스 하나는 작업 태그 하나만 가진다.
- 일반 사건 전체에 적용되는 범용 보너스로 사용하지 않는다.

## 8. 용량 3 기능 경계

```text
TRANSFORMATIVE_OR_RULE_BYPASS_FUNCTION
= CAPACITY_COST 3 + SEPARATE_DESIGN_APPROVAL
```

순간이동, 파괴 회피, 실패 무효화, 영구 자원 생성, 사건 단계 건너뛰기처럼 규칙을 바꾸는 기능은 최초 카탈로그에 포함하지 않는다. 용량 3을 확보해도 별도 기획 승인 없이는 생성할 수 없다.

## 9. 중량·강화·고객 연결

```text
최초 제작
→ 역할 원수치와 PERFORMANCE_PROFILE 확정
→ 중량 기반 출력 합산
→ 승인된 기능이 있으면 용량 검증
→ 일반·정밀강화에서 승인된 출력만 추가
→ 고객 장비 선택 시 현재 중량·적성·기능 조건 판정
```

- 중량화는 프로필에 따라 공격·방어 또는 기능 용량을 추가한다.
- 중량화가 기능 자체를 생성하지 않는다.
- 기능은 고객 능력·적성·판단을 대체하지 않는다.
- 기능 적합도는 관련 고객 능력과 활성 조건을 계속 사용한다.

## 10. 표시 원칙

기본 작품 카드:

```text
공격 24
중량 10
내구도 18
기능: 마력 전도
```

상세 출처:

```text
공격 24
- 최초 제작 9
- 중량 기반 10
- 강화 기반 5
```

- 존재하지 않는 원수치는 표시하지 않는다.
- 기능 용량 숫자는 기본 카드에서 숨긴다.
- 기본 카드에는 기능 이름과 핵심 조건을 우선 표시한다.
- 상세 보기에서만 용량 비용·결속 맥락·출처를 설명한다.
- 전체 기능 카탈로그를 기본 작품 화면에 노출하지 않는다.

## 11. 적대적 검토

### 채택

- 장비군별 단일 역할 원수치
- 최초 제작·중량·강화 출처의 가산 분리
- 기능 용량과 기능 인스턴스의 분리
- 결속 맥락이 있는 소형 기능 카탈로그

### 비채택

- 모든 장비에 공격·방어를 강제
- 치명타·관통·명중·속도·회피·막기 기본 스키마
- 기능 자유 배분과 중복 누적
- 용량만으로 기능 자동 생성
- 기능 태그의 일반 성공률 범용 보너스화
- 용량 3 규칙 우회 기능의 자동 승인

최종 판정: `P0 0 / P1 0`.

## 12. 구현 경계

- 기획 정본·검증 계약·권위 진입점·Google Sheet만 갱신한다.
- 런타임·게임 데이터·스크립트·Scene·이미지·에셋·addons·`project.godot`은 변경하지 않는다.
- `data/crafting/weapon_bases.json`은 변경하지 않는다.
- 정확한 최초 공격·방어 분포, 강화 단계 증가량, 위험 완화량, 현장 수리량은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.
- 제품 구현: `BLOCKED`.
