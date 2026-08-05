# Blacksmith R2 작품 역할 원수치와 최초 기능 카탈로그 설계

- Decision 후보: `BS-ITEM-20260806-04`
- 목표 배치: `R2_BATCH_005_8_OF_10`
- 선행 Decision: `BS-ITEM-20260806-03 / BS-ITEM-20260806-02 / BS-CUSTOMER-20260805-01`
- Work Mode: `TOTAL_PLANNING`
- 제품 구현: `BLOCKED`

## 1. 목적

작품 종류마다 필요한 원수치만 저장하고, 마법·유틸리티 기능은 작은 승인 카탈로그로 분리한다. 플레이어가 여러 전투 수치와 자유 기능 조합을 관리하게 만들지 않으면서 제작·중량·강화 결과의 출처를 설명할 수 있어야 한다.

## 2. 검토한 접근

### A. 단일 역할 원수치 + 소형 기능 카탈로그 — 채택

- 무기는 `ATTACK`, 방패·갑옷은 `DEFENSE`를 주 역할 원수치로 가진다.
- 도구·의복·장신구는 공격·방어를 강제로 갖지 않는다.
- 마법·유틸리티 효과는 별도 승인 기능 ID로 저장한다.
- 장점: 강화 중심성, 모바일 가독성, 출처 추적, 장비군 정체성을 모두 유지한다.

### B. 다중 전투 원수치 — 비채택

- 공격·관통·명중·속도·치명타·방어·회피·막기 등을 장비군별로 배분한다.
- 장점: 세밀한 빌드가 가능하다.
- 단점: 제작과 강화보다 비교표·최적화가 중심이 되고 고객 카드와 모바일 UI가 복잡해진다.

### C. 기능 중심 장비 — 비채택

- 공격·방어보다 기능 태그를 장비 정체성의 중심으로 둔다.
- 장점: 마법 도구와 특수 장비에는 유리하다.
- 단점: 일반 무기·갑옷의 성능 판단이 흐려지고 중량 성능 예산의 역할이 약해진다.

## 3. 작품 역할 원수치 모델

```text
ITEM_ROLE_STAT_MODEL = SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS
```

### 3.1 작품군별 기본 원수치

| 작품군 | 필수 역할 원수치 | 조건부 원수치 |
|---|---|---|
| `SWORD / AXE / BLUNT / POLEARM / RANGED` | `ATTACK` | `SPECIAL_FUNCTIONS` |
| `SHIELD_SUPPORT` | `DEFENSE` | `STABILITY / SPECIAL_FUNCTIONS` |
| `LIGHT_ARMOR / MEDIUM_ARMOR / HEAVY_ARMOR` | `DEFENSE` | `ENVIRONMENTAL_RESPONSE / SPECIAL_FUNCTIONS` |
| `TOOL / CLOTHING_OR_ROBE / ACCESSORY` | 없음 | `SPECIAL_FUNCTIONS` |

공통 원수치는 기존 계약의 `WEIGHT / DURABILITY / HANDLING / ARTISTRY`를 유지한다. 적용되지 않는 수치는 `0`으로 채우지 않고 생략한다.

### 3.2 공격·방어 구성

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

- `CRAFTED_ATTACK / CRAFTED_DEFENSE`는 최초 제작 완료 시 한 번 확정되는 출생 원수치다.
- 출생 원수치는 기본 작품 설계·주재료·직접 단조 결과를 하나의 최종값으로 저장하되, 출처 장부에서 각 기여 원인을 추적한다.
- 제작 등급과 예술성은 공격·방어를 자동 증폭하지 않는다.
- `WEIGHT_*_OUTPUT`은 `BS-ITEM-20260806-03`의 중량 예산 환산만 사용한다.
- `APPROVED_ENHANCEMENT_*_OUTPUT`은 기존 일반·정밀강화 계약에서 명시적으로 승인된 증가만 포함한다.
- 같은 원인을 두 항목에서 중복 계산하지 않는다.

### 3.3 기본 비채택 수치

다음은 기본 작품 원수치로 추가하지 않는다.

```text
CRITICAL_CHANCE / CRITICAL_DAMAGE / PENETRATION / ACCURACY
ATTACK_SPEED / EVASION / BLOCK_RATE / ELEMENTAL_DAMAGE
```

필요한 개별 효과는 후속 승인된 촉매 수식어·정밀강화 방식·특수기능으로만 표현한다.

## 4. 특수기능 저장 모델

```text
SPECIAL_FUNCTIONS = [APPROVED_FUNCTION_INSTANCE]
APPROVED_FUNCTION_INSTANCE
= FUNCTION_ID + CAPACITY_COST + OPTIONAL_BOUND_CONTEXT
```

- 기능은 중량 기반 `MAGIC_FUNCTION_CAPACITY` 또는 `UTILITY_CAPACITY`를 소비한다.
- 같은 기능 ID를 중복 장착해 수치를 누적하지 않는다.
- 기능 용량은 기능 슬롯 수가 아니라 총 비용 상한이다.
- 기능 용량이 남아도 승인되지 않은 기능을 자동 생성하지 않는다.
- 기능은 일반 사건 성공률에 자동 합산하지 않는다.
- 기능의 효과는 `조건 충족`, `위험 완화`, `특정 상호작용 허용` 중 하나로 설명한다.

## 5. 최초 승인 마법 기능 카탈로그

### 5.1 `ARCANE_CONDUCTION` — 용량 1

```text
출력 태그: CAN_CHANNEL_MAGIC_THROUGH_ITEM
```

- 작품을 마법의 초점·매개체로 사용할 수 있게 한다.
- 고객의 마력 적성·관련 친화·판단력 검사를 대체하지 않는다.
- 자체적으로 공격·방어·일반 성공률을 올리지 않는다.

### 5.2 `ELEMENTAL_WARD` — 용량 1

```text
출력 태그: MITIGATES_ONE_BOUND_ELEMENTAL_HAZARD
필수 맥락: BOUND_ELEMENT
```

- 불·냉기·번개·독성 등 승인된 하나의 위험 맥락에만 결속한다.
- 위험을 완전히 무효화하지 않고 피해·손상·실패 위험을 완화한다.
- 정확한 완화량은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

### 5.3 `ARCANE_SENSING` — 용량 2

```text
출력 태그: CAN_DETECT_MATCHING_ARCANE_TRACE
필수 맥락: BOUND_TRACE_FAMILY
```

- 결속된 마법 흔적·이상 현상의 존재를 감지할 수 있게 한다.
- 정체·해법·안전 여부를 자동 판정하지 않는다.
- 실제 활용에는 고객 판단력과 마력 적합도가 필요하다.

## 6. 최초 승인 유틸리티 기능 카탈로그

### 6.1 `ENVIRONMENTAL_SEALING` — 용량 1

```text
출력 태그: RESISTS_ONE_BOUND_ENVIRONMENT
필수 맥락: BOUND_ENVIRONMENT
```

- 습기·먼지·부식성 기체·극한 온도 등 하나의 승인 환경에 대응한다.
- 내구도 손실 또는 환경 위험을 완화하되 완전 면역을 제공하지 않는다.

### 6.2 `FIELD_SERVICEABILITY` — 용량 1

```text
출력 태그: CAN_PERFORM_FIELD_MAINTENANCE
```

- 정식 공방이 아닌 일정·원정 중에도 제한된 유지보수를 가능하게 한다.
- 완전 복원·연대기 손상 삭제·무료 수리를 허용하지 않는다.
- 정확한 비용·회복량은 별도 테스트 프리셋에서 관리한다.

### 6.3 `TASK_INTEGRATION` — 용량 1

```text
출력 태그: SUPPORTS_ONE_BOUND_TASK
필수 맥락: BOUND_TASK
```

- 채굴·절단·등반·의식 준비 등 승인된 하나의 작업 맥락을 지원한다.
- 하나의 기능 인스턴스는 하나의 작업 태그만 가진다.
- 일반 사건 전체에 적용되는 범용 보너스로 사용하지 않는다.

## 7. 용량 3 기능 경계

```text
TRANSFORMATIVE_OR_RULE_BYPASS_FUNCTION
= CAPACITY_COST 3 + SEPARATE_DESIGN_APPROVAL
```

- 순간이동, 파괴 회피, 실패 무효화, 영구 자원 생성, 사건 단계 건너뛰기처럼 규칙을 바꾸는 기능은 최초 카탈로그에 포함하지 않는다.
- 용량 3을 확보했다는 이유만으로 해당 기능을 자동 승인하지 않는다.

## 8. 제작·중량화·강화 흐름

```text
기본 작품 설계 선택
→ 최초 제작 완료
→ 역할 원수치와 불변 PERFORMANCE_PROFILE 확정
→ 중량 예산 출력 합산
→ 승인된 특수기능이 있으면 용량 검증
→ 일반 강화 또는 정밀강화
→ 승인된 강화 출력만 역할 원수치에 합산
→ 고객 장비 선택 시 현재 중량·적성·기능 조건 판정
```

중량화로 새 기능 용량을 얻어도 자동으로 기능이 생기지 않는다. 후속 정밀강화·촉매·승인된 재작업에서 기능 생성 또는 강화 절차가 별도로 필요하다.

## 9. UI 원칙

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

- 존재하지 않는 수치는 표시하지 않는다.
- 기능 용량 숫자는 기본 카드에서 숨기고 기능 이름과 핵심 조건을 우선 표시한다.
- 상세 보기에서만 용량 비용·결속 맥락·출처를 설명한다.
- 전체 기능 카탈로그를 기본 장비 화면에 노출하지 않는다.

## 10. 적대적 보호 조건

- 모든 장비에 공격·방어·마법·유틸리티 수치를 강제로 넣지 않는다.
- 기본 작품 스키마에 다중 전투 보조 수치를 추가하지 않는다.
- 같은 제작·중량·강화 원인을 두 번 합산하지 않는다.
- 기능 태그를 일반 성공률 범용 보너스로 전환하지 않는다.
- 기능 중복 장착으로 같은 효과를 무한 누적하지 않는다.
- 환경·원소·작업 결속이 없는 범용 기능을 만들지 않는다.
- 기능 용량만으로 미승인 기능 또는 규칙 우회 기능을 자동 생성하지 않는다.
- 장비 기능이 고객 능력·적성·판단을 대체하지 않는다.

## 11. 검증 계획

- 새 계약 테스트가 Decision ID, 배치 `8/10`, 역할 원수치 스키마, 공격·방어 합산식, 6개 기능 카탈로그, 용량·중복·범용 보너스 금지를 검증한다.
- RED에서는 기존 계약이 통과하고 신규 계약만 정본 부재로 실패해야 한다.
- GREEN에서는 정본·레지스트리·현재 문서·허브·감사기가 같은 계약을 읽어야 한다.
- 최종 exact head에서 Planning-first, Base adoption, PR validation, Python 전체, 운영 감사, Godot 계약을 재실행한다.

## 12. 범위

- 기획 정본·검증 계약·권위 진입점·Google Sheet만 갱신한다.
- 런타임·게임 데이터·스크립트·Scene·이미지·에셋·addons·`project.godot`은 변경하지 않는다.
- 정확한 제작 공격·방어 분포, 강화 단계별 증가량, 환경 완화량, 현장 수리량은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.
- 제품 구현: `BLOCKED`.
