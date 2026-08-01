# Blacksmith v9 데이터·구형 장비 마이그레이션 승인 정본

> Decision ID: `BS-MIGRATION-20260801-01`
>
> 상태: `USER_PREAPPROVED_RECOMMENDED / CANONICAL_DESIGN_COMPLETE`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 선행 결정: `BS-GRADE-20260801-02`, `BS-V9-20260731-02`, `BS-ENH-20260731-01`, `BS-SAVE-20260801-01`

## 1. 목적

기존 PoC의 제작 등급·수식어 3슬롯·10단위 특수 강화·+50 장비를 최신 v9 정본으로 **재추첨·손실·과도한 보상 없이 결정론적으로 이전**한다.

이 계약은 저장된 작품의 과거 결과를 다시 판정하지 않는다. 구형 데이터의 순위·수치·수식어·강화 단계·소유권·연대기를 보존하면서 최신 스키마에 맞는 역할과 provenance를 부여한다.

## 2. 마이그레이션 불변 조건

```text
장비 UID 보존
제작 등급 순위 보존
공격력·가치·점수 보존
강화 단계 보존
수식어 ID·Tier·효과 보존
소유권·고객·연대기 보존
RNG 재호출 0회
신규 고위 정밀 보상 소급 지급 0회
원본 덮어쓰기 0회
중복 마이그레이션 0회
```

마이그레이션은 `BS-SAVE-20260801-01`의 원본 보존·tmp 검증·원자 승격 계약을 따른다.

## 3. 제작 등급 내부 ID

최신 제품 ID는 다음으로 고정한다.

| 순위 | Runtime ID | 표시명 |
|---:|---|---|
| 1 | `NORMAL` | 보통 |
| 2 | `SUPERIOR` | 우수 |
| 3 | `EXQUISITE` | 명품 |
| 4 | `MASTERPIECE` | 걸작 |
| 5 | `LEGENDARY` | 전설 |

- ID는 영문 대문자 고정값이다.
- 표시명 변경이 저장 ID를 바꾸지 않는다.
- `MASTERWORK`는 구형 ID로만 사용하고 최신 ID로 재사용하지 않는다.
- `LEGENDARY`는 제작 등급이며 아이템 희귀도·+50 경로·명작 전당 자격과 별개다.

## 4. 구형 제작 등급 변환표

| 구형 ID | 구형 표시명 | 신규 ID | 신규 표시명 | 이전 원칙 |
|---|---|---|---|---|
| `APPRENTICE` | 미숙한 | `NORMAL` | 보통 | 최하위 순위 보존 |
| `STANDARD` | 평범한 | `SUPERIOR` | 우수 | 2순위 보존 |
| `REFINED` | 정교한 | `EXQUISITE` | 명품 | 3순위 보존 |
| `MASTERWORK` | 명품 | `MASTERPIECE` | 걸작 | 4순위 보존; 이름 중복 회피 |
| `PERFECT` | 완벽한 | `LEGENDARY` | 전설 | 최상위 순위 보존 |

### 수치·분포 이전

1차 호환 마이그레이션에서는 구형 등급의 다음 값을 신규 ID로 그대로 이동한다.

- `score_bonus`
- `attack_multiplier`
- `value_multiplier`
- 정밀 결과별 확률 분포

즉, 키만 1:1 변환하고 수치는 재조정하지 않는다. 향후 밸런스 조정은 별도 Decision과 시뮬레이션으로 처리하며 저장된 작품 등급은 다시 추첨하지 않는다.

## 5. 제작 결과와 등급 판정 분리

구형 단조 화면의 `quality_id` (`AUTO`, `STANDARD`, `GOOD`, `PERFECT`)는 **정밀 마감 판정**이며 제작 등급 ID가 아니다.

최신 저장 구조는 다음을 분리한다.

```text
crafting_finish_result_id   # AUTO/STANDARD/GOOD/PERFECT 등 입력 결과
craftsmanship_grade_id      # NORMAL/SUPERIOR/EXQUISITE/MASTERPIECE/LEGENDARY
```

구형 장비에 `craftsmanship_grade_id`가 이미 있으면 변환표를 적용한다. 구형 장비에 마감 결과만 있고 제작 등급이 저장되지 않았다면 기존 결정론적 resolver와 저장된 입력값을 사용해 **한 번만** 계산하고 migration provenance를 남긴다. 입력값이 부족하면 임의 추첨하지 않고 `MIGRATION_REVIEW_REQUIRED`로 격리한다.

## 6. 수식어 역할 마이그레이션

### 최신 구조

```text
lineage_affix        정확히 0~1개
secondary_affixes    최대 2개
special_affix        고위 정밀강화 전용 0~1개
```

### 구형 3슬롯 변환

구형 수식어 배열의 슬롯과 획득 순서를 유지한다.

| 구형 | 신규 역할 |
|---|---|
| slot 1 | `lineage_affix` |
| slot 2 | `secondary_affixes[0]` |
| slot 3 | `secondary_affixes[1]` |

각 변환 객체는 다음 provenance를 가진다.

```text
source_schema: LEGACY_AFFIX_SLOT_MODEL
source_affix_id
source_slot
source_tier
migrated_role
migration_decision_id: BS-MIGRATION-20260801-01
```

### 보존 규칙

- affix ID·Tier·효과 수치·material score는 유지한다.
- 빈 슬롯은 새 수식어로 채우지 않는다.
- 중복 수식어도 구형 저장 사실이면 자동 합성·삭제하지 않는다.
- 최신 계보 후보군과 의미가 완전히 같지 않아도 `legacy_lineage` provenance로 보존한다.
- 이후 플레이에서 계보 강화·파생 선택이 필요하면 legacy lineage에 허용된 호환 분기를 별도 데이터로 제공한다.

## 7. 이정표·강화 단계 이전

| 구형 이정표 | 신규 해석 |
|---|---|
| +10 slot1 추가 | 계보 획득 이력 |
| +20 slot1 강화 | 계보 강화 이력 |
| +30 slot2 추가 | 보조1 획득 이력 |
| +40 slot2 강화 | 보조1 강화 이력 |
| +50 slot3 추가 | 보조2 획득 이력 |
| +60 slot3 강화 | 보조2 심화 이력 |
| +70 slot1 강화 | 계보 심화 이력 |
| +80 slot2 강화 | 보조1 심화 이력 |
| +90 slot3 강화 | 보조2 심화 이력 |
| +100 전체 승격 | 기존 세 역할의 legacy 전체 심화 이력 |

- 구형 +50의 slot3은 최신 `special_affix`가 아니다.
- +60 이상은 새 슬롯을 만들지 않고 기존 역할의 심화 이력으로 보존한다.
- 이정표 선택 UI가 존재하지 않았던 과거에 대해 선택 이유·후보 목록을 발명하지 않는다.
- 연대기에는 `LEGACY_MILESTONE_MIGRATED` 사건 하나와 변환 요약을 추가한다.

## 8. +49→+50 경로 이전

### 구형 +50 이상 장비

```text
enhancement_route_at_50 = LEGACY_GENERAL_PRECISION
special_material_uses_at_50 = []
special_affix_id = ""
high_precision_evolution_id = ""
```

- 구형 +50 장비는 정상 완성품이다.
- +51 이상 강화와 명작 전당 자격을 유지한다.
- 고위 정밀강화 성공·특수 수식어·진화를 소급 지급하지 않는다.
- 기존 slot3 수식어는 보조2로 보존한다.

### 구형 +49 이하 장비

- +49에서 멈춘 장비는 최신 일반/고위 정밀강화 선택 화면으로 진입한다.
- 구형에 소비됐던 재료나 시도 기록을 추정해 환급하지 않는다.
- 첫 최신 +50 시도부터 `BS-ENH-20260731-01`을 사용한다.

## 9. 대상 스키마

| 파일·도메인 | 구형 | 목표 |
|---|---:|---:|
| `craftsmanship_grades.json` | 1 | 2 |
| `enhancement_milestones.json` | 2 | 3 |
| 장비 identity record | 비정규/PoC | 1 |
| `EquipmentWorldRegistry.record_schema_version` | 1 | 2 |
| 제품 CampaignSnapshot | 없음 | 1 |

스키마 번호는 해당 도메인 내부에서만 비교한다. 서로 다른 파일의 `schema_version` 숫자가 같다고 동일 구조를 의미하지 않는다.

## 10. Migration Pipeline

```text
원본 바이트 읽기·격리
→ 구형 스키마 검증
→ 대상 equipment UID·참조 인벤토리
→ 등급 ID 1:1 변환
→ 수식어 역할 변환
→ +50 route provenance 부여
→ 소유권·관계·연대기 참조 복원
→ 대상 스키마 validator
→ 결정론적 snapshot hash 생성
→ tmp 저장·재검증
→ 원본 보존 후 원자 승격
```

### 멱등성

```text
migration_id = BS-MIGRATION-20260801-01:<campaign_id>:<source_revision>
```

동일 `migration_id`는 한 번만 적용한다. 이미 대상 schema이고 migration ledger에 ID가 있으면 재실행하지 않는다.

## 11. 실패 처리

| 실패 | 처리 |
|---|---|
| 알 수 없는 제작 등급 ID | 원본 보존, `MIGRATION_REVIEW_REQUIRED` |
| affix ID 정의 누락 | 장비를 삭제하지 않고 unresolved reference로 격리 |
| equipment UID 중복 | 승격 중단, 충돌 보고 |
| owner/customer 참조 누락 | 작품 보존, 소유권 unresolved 상태로 격리 |
| hash·validator 실패 | tmp 폐기, 원본 유지 |
| 일부 장비만 성공 | 캠페인 전체 승격 금지; 부분 저장 금지 |

## 12. 검증 매트릭스

### Fixture

최소 다음 fixture를 제공한다.

1. 등급 5종 각각 1개
2. 수식어 0/1/2/3개 장비
3. +0/+10/+20/+30/+40/+49/+50/+60/+100 장비
4. 파괴 장비·판매 장비·세계 결과 대기 장비
5. 중복 UID·알 수 없는 grade·누락 affix 참조 실패 fixture
6. 동일 save를 두 번 마이그레이션하는 멱등성 fixture

### 통과 조건

```text
EQUIPMENT_UID_CHANGED: 0
GRADE_RANK_CHANGED: 0
STORED_NUMERIC_VALUE_CHANGED: 0
AFFIX_LOSS: 0
RNG_CALLS_DURING_MIGRATION: 0
FREE_HIGH_PRECISION_REWARD: 0
DUPLICATE_MIGRATION: 0
SOURCE_OVERWRITE_ON_FAILURE: 0
PARTIAL_CAMPAIGN_COMMIT: 0
```

## 13. 기존 데이터·테스트 영향

직접 영향:

- `data/crafting/craftsmanship_grades.json`
- `data/crafting/enhancement_milestones.json`
- `data/crafting/affixes.json`
- `scripts/forging/craftsmanship_grade_resolver.gd`
- `scripts/enhancement/enhancement_session.gd`
- 장비 record 생성·표시·고객 적합도·세계 Registry
- 제작·강화·고객·E2E fixture와 validator
- `BS-SAVE-20260801-01` SaveMigrator

기존 구형 계약 테스트는 삭제하지 않고 `legacy fixture migration tests`로 역할을 변경한다. 최신 런타임 테스트는 신규 ID·역할 모델을 사용한다.

## 14. 감사 판정

```text
BS-AUD-F04_PLANNING_TARGET: RESOLVED
BS-AUD-F05_MIGRATION_TARGET: RESOLVED
BS-AUD-F20_MIGRATION_TEST_TARGET: RESOLVED
RUNTIME_DATA_CHANGE: NOT_RUN
SAVE_MIGRATOR_IMPLEMENTATION: NOT_RUN
AUTOMATED_TESTS: NOT_RUN
P0_FINDING_COUNT: 유지
```

기획 목표는 해결됐지만 실제 데이터·코드·fixture·테스트를 이전하기 전에는 Finding을 닫지 않는다.

## 15. 현재 Gate

```text
GRADE_RUNTIME_IDS: APPROVED
LEGACY_GRADE_MAPPING: APPROVED
LEGACY_AFFIX_ROLE_MAPPING: APPROVED
LEGACY_PLUS50_ROUTE: APPROVED
NUMERIC_COMPATIBILITY_POLICY: APPROVED
MIGRATION_FAILURE_POLICY: APPROVED
MIGRATION_TEST_MATRIX: APPROVED
PRODUCT_DATA_CHANGE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
