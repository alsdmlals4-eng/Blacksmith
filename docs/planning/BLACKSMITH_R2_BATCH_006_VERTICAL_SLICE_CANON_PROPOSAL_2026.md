# Blacksmith R2 Batch 006 — Godot Vertical Slice Canon

> 상태: `USER_APPROVED_MERGED_PR120_MAIN_CANON`
>
> 권위: `MAIN_CANON`
>
> 승인 병합 main: `a8a94343c78a68bf7bb14b411e7741f43b257138`
>
> PR: `#120`

```yaml
BATCH: R2_BATCH_006
COUNTER: 10/10
ALL_APPROVED_CONTRACTS_REQUIRED: true
REPRESENTATIVE_CONTENT_ONLY: true
PRODUCT_IMPLEMENTATION: BLOCKED
VERTICAL_SLICE_IMPLEMENTATION: APPROVED
HUMAN_PLAYTEST: NOT_RUN
BALANCE_AUTHORITY: BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED
```

## 1. 승인 목적

현재 승인된 기획을 모두 적용한 Godot 버티컬 슬라이스를 만들 수 있도록 다음 네 가지를 한 배치에서 잠근다.

1. 대표 end-to-end 플레이 경로
2. 동일 UID·SaveEnvelope·변동 장부
3. 데모에 필요한 최소 콘텐츠와 수치 프리셋
4. 기존 역사 POC와 신규 정본 구현의 경계

여기서 “모든 기획 적용”은 모든 승인 계약과 금지사항을 지키는 것을 의미한다. 모든 장비군·재료·고객·촉매·정밀강화 이정표를 한 번에 구현한다는 뜻이 아니다.

```text
모든 승인 계약·금지사항 = 전부 적용
콘텐츠 수량 = 대표 표본만 구현
정확한 수치 = 버전이 붙은 데모 프리셋
```

## 2. 변하지 않는 기존 정본

### 작품·제작

- 제작 등급은 `[보통] → [우수] → [명품] → [걸작] → [전설]`이다.
- 제작 등급은 최초 직접 단조 완료 시 확정되고 동일 UID에서 고정된다.
- 예술성은 `0` 이상의 정수이며 고정 설계 최대치가 없다.
- 수식어 슬롯은 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`다.
- 보조재료 슬롯 없음.
- 주재료는 장비군별 명시적 역할 적합성을 가진다.
- 직접 단조는 역할별 3구간 결과를 낸다.
- 최초 역할 수치 기준은 `5 / 10 / 15`다.
- 작품은 역할 원수치·중량·기능 용량을 분리해 보유한다.

### 강화

- 일반 강화 한 입력은 한 결과만 낸다.
- 일반 강화는 예술성이나 역할 원수치를 자동 증가시키지 않는다.
- 정밀강화 이정표 체계는 `+10 / +20 / +30 / +40 / +50`이다.
- 같은 이정표에서 수치 패키지와 기능 재작업은 상호배타다.
- 촉매 계보는 `EMPTY → SEED → DEVELOPED → EVOLVED → MASTERED`다.

### 고객·일정·UX

- 고객 능력은 근력·기량·체력·판단력 `1~10`이다.
- 최대 중량은 `STRENGTH × 10 WEIGHT_POINT`다.
- 초과 중량 작품은 고객에게 배정할 수 없다.
- 강화 단계가 고객 성공률의 주효과다.
- 고객 카드 정보는 기본 → 장비 선택 후 판단 → 상세 보기로 공개한다.
- 핵심 원인 2~4개를 텍스트와 아이콘으로 함께 설명한다.
- 개인 일정과 날짜 예고형 세계 일정을 분리한다.
- 고객 결과는 같은 작품 UID의 연대기·손상·복원·다음 판단으로 돌아온다.

## 3. 구현 경계

신규 버티컬 슬라이스는 다음 namespace를 사용한다.

```text
scripts/vertical_slice/
data/vertical_slice/
scenes/vertical_slice/
tests/vertical_slice/
```

기존 POC에서 선별 이식 가능한 것은 입력 유틸리티, 화면 전환 패턴, headless 테스트 러너, 접근성 헬퍼다.

다음 역사 구조는 신규 작품 Schema의 권위가 아니다.

- 3단계 구형 품질
- secondary 재료 데이터
- 범용 수식어 배열
- 구형 고객 고정 계약 일수
- 과거 정확한 공격·가치·강화 수치

한 작품 Dictionary 안에 구형 필드와 신규 필드를 동시에 넣지 않는다.

---

# Decision 1 — BS-VS-20260806-01

## 버티컬 슬라이스 완료 계약

### 대표 플레이 경로

```text
새 게임
→ 주재료와 검 설계 선택
→ 역할별 3구간 직접 단조
→ 작품 UID 생성
→ 제작 등급·예술성·공격·중량·기능 확정
→ 일반 강화 지속·중단
→ +10 정밀강화 방식과 촉매 선택
→ 고객 3명 중 한 명에게 배정
→ 개인 일정 또는 세계 일정 결과
→ 연대기·손상·복원
→ 저장·종료·불러오기
→ 동일 UID 작품 재방문
→ 다음 제작 판단 화면 복귀
```

### 완료 조건

- 신선한 테스트 계정으로 시작해 동일 UID 재방문까지 20~30분 안에 도달할 수 있다.
- 중간 단계 건너뛰기 없이 한 작품이 모든 대표 시스템을 통과한다.
- 저장 후 작품의 제작 등급·예술성·수식어·강화·손상·연대기가 변하지 않는다.
- 구형 POC 화면을 시작 씬으로 사용하지 않는다.

### 데모에서 제외

- 검 이외 장비군 전체
- 모든 주재료와 촉매
- +20 이상 정밀강화 콘텐츠
- 완전한 상점·광고·과금·대규모 경제
- 인력·건물·생산 체인
- 최종 아트·오디오·현지화
- Android 스토어 출시 품질

판정: `USER_APPROVED_MERGED_PR120_MAIN_CANON`.

---

# Decision 2 — BS-SAVE-20260806-01

## 작품 UID·변동 장부·SaveEnvelope

### UID

```text
BSI-<32_LOWER_HEX>
```

- 최초 작품 출생 시 한 번 생성한다.
- 복사·수리·고객 결과·불러오기로 UID를 바꾸지 않는다.
- 충돌 검사 후 작품 Registry에 등록한다.

### 저장 파일

```text
user://blacksmith_vertical_slice_v1.json
```

임시 파일은 다음 경로를 사용한다.

```text
user://blacksmith_vertical_slice_v1.tmp
```

### SaveEnvelope 최소 구조

```json
{
  "schema_version": 1,
  "preset_version": "VS-2026.08.06-A",
  "saved_at_utc": "ISO-8601",
  "active_run": {},
  "items_by_uid": {},
  "customer_state": {},
  "schedule_state": {},
  "global_ledger_sequence": 0
}
```

### 작품 최소 필드

```text
uid
birth_rng_seed
primary_material_id
equipment_group
role_profile
crafting_grade
artistry
raw_role_stat
weight_point
function_capacity
functions
grade_affix
catalyst_affix
chronicle_affix
enhancement_level
used_precision_milestones
damage_state
owner_id
ledger
```

### 변동 장부

각 항목은 다음 필드를 가진다.

```text
sequence
event_id
event_type
source_decision_id
before_digest
after_digest
occurred_at_game_day
payload
```

- 장부는 append-only다.
- 출생 사실은 수정하지 않는다.
- 저장·불러오기 재추첨을 막기 위해 RNG seed와 이미 확정된 결과를 함께 저장한다.
- 파일 쓰기 성공 후 임시 파일을 본 파일로 교체한다.

판정: `USER_APPROVED_MERGED_PR120_MAIN_CANON`.

---

# Decision 3 — BS-MATERIAL-20260806-01

## 대표 주재료 3종

| 재료 | 공격 적합 | 예술성 경향 | 중량 | 기능 용량 | 역할 |
|---|---:|---:|---:|---:|---|
| 철 | 0 | 0 | 15 | 0 | 균형 기준선 |
| 은 | -5 | +4 | 10 | 1 | 경량·예술·마법 |
| 운석철 | +5 | +2 | 20 | 1 | 고중량·공격·우주 |

### 의미

- 철은 추가 기능 없이 가장 읽기 쉬운 기준선이다.
- 은은 공격 원수치 일부를 포기하고 예술성·경량·기능 가능성을 얻는다.
- 운석철은 중량 부담을 감수하고 공격 적합과 기능 가능성을 얻는다.
- 세 재료 모두 `primary`만 사용한다.

재료 가격과 희귀도는 예술성으로 직접 변환하지 않는다.

판정: `USER_APPROVED_MERGED_PR120_MAIN_CANON`.

---

# Decision 4 — BS-CRAFT-20260806-01

## 제작 등급 5단계 데모 프리셋

직접 단조의 세 구간은 각 `0 / 1 / 2`점을 주며 합계는 `0~6`이다.

```text
LOW  = 0~2
MID  = 3~4
HIGH = 5~6
```

등급 확률은 `[보통, 우수, 명품, 걸작, 전설]` 순서다.

| 입력 티어 | 보통 | 우수 | 명품 | 걸작 | 전설 |
|---|---:|---:|---:|---:|---:|
| LOW | 85% | 14% | 1% | 0% | 0% |
| MID | 60% | 30% | 9% | 1% | 0% |
| HIGH | 30% | 40% | 24% | 5.5% | 0.5% |

### 규칙

- 출생 roll은 한 번만 수행한다.
- 사용한 seed와 결과를 동일 UID에 저장한다.
- 제작 등급은 공격·예술성·중량을 곱하지 않는다.
- `전설`은 HIGH에서만 가능하다.
- 정확한 확률은 최종 밸런스가 아니다.

판정: `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.

---

# Decision 5 — BS-ITEM-20260806-07

## 초기 공격·예술성·중량·기능 용량

### 공격

직접 단조 결과는 다음 세 값이다.

```text
5 / 10 / 15
```

최종 공격 원수치:

```text
MAX(0, 재료 공격 적합 + 직접 단조 공격 결과)
```

예시:

| 재료 | 낮은 단조 | 중간 단조 | 높은 단조 |
|---|---:|---:|---:|
| 철 | 5 | 10 | 15 |
| 은 | 0 | 5 | 10 |
| 운석철 | 10 | 15 | 20 |

### 예술성

직접 단조 미적 결과:

```text
0 / 3 / 6
```

초기 예술성:

```text
재료 예술성 경향 + 직접 단조 미적 결과
```

제작 등급은 예술성 보너스가 아니다.

### 중량·기능 용량

- 철: `15 WEIGHT_POINT / capacity 0`
- 은: `10 WEIGHT_POINT / capacity 1`
- 운석철: `20 WEIGHT_POINT / capacity 1`

판정: `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.

---

# Decision 6 — BS-ENHANCE-20260806-01

## 일반 강화 범위·위험·천장 보정

버티컬 슬라이스 범위는 `+0~+10`이다.

### 성공률

| 목표 단계 | 기본 성공률 |
|---|---:|
| +1~+3 | 100% |
| +4~+6 | 80% |
| +7~+9 | 65% |
| +10 | 50% |

### 실패 결과

| 목표 구간 | 유지 | 하락 | 파괴 |
|---|---:|---:|---:|
| +4~+6 | 100% | 0% | 0% |
| +7~+9 | 75% | 25% | 0% |
| +10 | 60% | 40% | 0% |

### 천장 보정

- 실패 1회당 성공률 `+5%p`
- 성공 시 실패 누적 초기화
- 최대 성공률 `95%`
- 실패 보정은 동일 작품 UID에 저장

### 범위 판단

버티컬 슬라이스에서는 파괴를 제외한다. 이유는 한 세션에서 고객·연대기·동일 UID 재방문까지 반드시 검증해야 하기 때문이다. 하락과 자원 소비만으로도 지속·중단 판단을 관찰할 수 있다.

파괴 제외는 최종 제품 규칙 확정이 아니라 데모 프리셋 범위다.

판정: `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.

---

# Decision 7 — BS-ENHANCE-20260806-02

## +10 정밀강화 대표 선택

+10에서 다음 중 하나만 선택한다.

| 선택 | 공격 변화 | 중량 변화 | 기능 변화 |
|---|---:|---:|---|
| ATTACK_PACKAGE | +5 | 0 | 없음 |
| LIGHTWEIGHT | 0 | -5 | 없음 |
| FUNCTION_REWORK | 0 | 0 | 기능 추가·교체 경로 |

### 공통 규칙

- 같은 +10 이정표를 다시 굴릴 수 없다.
- 선택 결과와 사용 이정표를 장부에 기록한다.
- `ATTACK_PACKAGE`와 `FUNCTION_REWORK`를 동시에 받을 수 없다.
- `LIGHTWEIGHT`는 기존 성능 기억을 삭제하지 않는다.
- 중량은 0 미만이 될 수 없다.

판정: `USER_APPROVED_MERGED_PR120_MAIN_CANON`.

---

# Decision 8 — BS-CATALYST-20260806-01

## 살라맨더 촉매 대표 계보

버티컬 슬라이스에서 사용하는 촉매는 `salamander_core` 한 종이다.

```text
EMPTY → SEED → DEVELOPED → EVOLVED → MASTERED
```

데모에서 도달 가능한 최대 단계는 `SEED`다.

### +10 결과

```text
CATALYST_AFFIX = EMBER_TOUCHED
```

기능 용량이 1 이상이면 다음 기능을 선택할 수 있다.

```text
ELEMENTAL_WARD(FIRE)
capacity_cost = 1
```

### 금지

- 제작 등급 변경 없음
- 예술성 직접 증가 없음
- 같은 +10 이정표 반복 적용 없음
- 용량 초과 기능 추가 없음
- 촉매 효과와 연대기 효과의 이중 계산 없음

철검은 capacity 0이므로 `FUNCTION_REWORK` 없이 화염 방호 기능을 받을 수 없다. 은검·운석검은 capacity 1이므로 재료 선택이 실제 기능 선택으로 이어진다.

판정: `USER_APPROVED_MERGED_PR120_MAIN_CANON`.

---

# Decision 9 — BS-CUSTOMER-20260806-02

## 고객 3종과 설명 가능한 적합도

### 검투사

```text
근력 8 / 기량 6 / 체력 8 / 판단력 4
공격 관심 PRIMARY
예술성 관심 IGNORE
화염 기능 관심 SECONDARY
최대 중량 80
```

### 병사

```text
근력 5 / 기량 6 / 체력 7 / 판단력 6
공격 관심 PRIMARY
예술성 관심 SECONDARY
화염 기능 관심 IGNORE
최대 중량 50
```

### 의전 귀족

```text
근력 1 / 기량 5 / 체력 4 / 판단력 8
공격 관심 SECONDARY
예술성 관심 REQUIREMENT
최소 예술성 6
화염 기능 관심 PRIMARY
최대 중량 10
```

의전 귀족은 은검 기본 중량 10만 즉시 배정 가능하다. 철검과 운석검은 LIGHTWEIGHT 결과 없이는 중량 Gate를 통과하지 못한다.

### 성공률 데모 공식

```text
CLAMP(5, 95,
  35
  + 강화 단계 × 4
  + 역할 적합 최대 +5
  + 재료 또는 기능 적합 최대 +5
  + 예술성 요구 충족 +5 / 미충족 -10
  + 판단력·위험 적합 최대 +5
)
```

UI는 최종 값을 10% 단위로 반올림해 보여준다.

### 고객 카드 원인

각 카드에는 다음 중 2~4개만 먼저 보여준다.

- 강화 단계
- 중량 Gate
- 공격 역할 적합
- 예술성 요구
- 화염 방호 기능
- 위험과 판단력

상세 보기에서 전체 계산을 읽을 수 있다.

판정: `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.

---

# Decision 10 — BS-CHRONICLE-20260806-01

## 일정·결과·손상·복원·연대기·플레이테스트

### 고객 개인 일정

```text
ARENA_BOUT_DAY_2
```

- 검투사가 배정된 작품을 사용한다.
- 공격과 강화 단계가 주효과다.
- 결과가 작품 UID에 기록된다.

### 세계 일정

```text
GRANARY_FIRE_DAY_4
```

- 날짜가 미리 예고된다.
- 화염 방호 기능이 있으면 주요 긍정 원인이 된다.
- 고객 개인 일정과 별도 장부를 사용한다.

### 손상 상태

```text
INTACT / WORN / DAMAGED
```

- 성공: `INTACT` 또는 기존 상태 유지
- 부분 성공: `WORN`
- 실패: `DAMAGED`

### 복원

- 복원은 게임 내 하루와 정해진 자원을 소비한다.
- 제작 등급과 예술성을 유지한다.
- 결과 사건을 삭제하지 않는다.
- 복원 사건을 새 장부 항목으로 추가한다.
- 결과 재추첨은 없다.

### 연대기 수식어

대표 사건을 충족하면 다음 중 하나를 `CHRONICLE_AFFIX`로 표시한다.

```text
ARENA_TESTED
FIRE_SAVED
RESTORED_AFTER_FAILURE
```

원본 사건 전체는 상세 연대기에서 읽는다.

### 사람 플레이테스트 Gate

외부 테스트 인원은 3~5명이다. 5명 기준 최소 통과 조건:

- 3명 이상이 end-to-end 경로 완료
- 3명 이상이 제작 등급·예술성·촉매·연대기의 차이를 설명
- 3명 이상이 강화 지속·중단을 고민한 이유를 설명
- 치명적 세이브 손상 0건

자동 검증과 사람 플레이테스트를 같은 PASS로 기록하지 않는다.

판정: `USER_APPROVED_MERGED_PR120_MAIN_CANON / HUMAN_PLAYTEST_NOT_RUN`.

---

## 4. 데이터 권위 분류

| 항목 | 권위 |
|---|---|
| 기존 R2 승인 계약 | MAIN_CANON |
| 이 문서의 10개 Decision | MAIN_CANON / MERGED_PR120 |
| `VS-2026.08.06-A` 수치 | BASELINE_TEST_PRESET |
| 기존 POC 정확 수치 | HISTORICAL_REFERENCE_ONLY |
| 실제 플레이 감각 | USER_PLAYTEST_REQUIRED |
| 일반 제품 구현 | BLOCKED |
| 버티컬 슬라이스 구현 | APPROVED / NAMESPACE_SCOPED |

## 5. 승인 후 구현 순서

```text
VS-0 Schema·SaveEnvelope
→ VS-1 App Shell
→ VS-2 직접 단조와 작품 출생
→ VS-3 일반·정밀강화
→ VS-4 고객·일정·설명 가능한 적합도
→ VS-5 결과·손상·복원·동일 UID 재방문
→ VS-6 자동 검증·Android 빌드·사람 플레이테스트
```

구현 상세는 `docs/superpowers/plans/2026-08-06-blacksmith-godot-vertical-slice.md`를 따른다.

## 6. 최종 적대적 검토

### 채택 이유

- 한 작품이 프로젝트 핵심 루프 전체를 통과한다.
- 최신 정본과 기존 POC를 물리적으로 분리한다.
- 모바일 세로형 정보 계층을 실제로 검증할 수 있다.
- 제작·강화·고객·세계·연대기를 단일 UID로 연결한다.
- 최종 밸런스와 데모 프리셋을 명확히 구분한다.

### 남은 위험

- 직접 단조가 반복해도 재미있는지는 아직 검증되지 않았다.
- +10까지의 자원 소모와 세션 길이는 실제 플레이에서 늘어질 수 있다.
- 고객 3종만으로 선택이 충분히 다르게 느껴질지 불확실하다.
- 카드형 세계 결과가 작품의 활약을 충분히 생생하게 전달할지 불확실하다.
- Android 저장 실패와 강제 종료 복구는 실제 기기 검증이 필요하다.

### 결론

기획 충돌로 인해 사용자에게 즉시 선택을 요구해야 하는 항목은 발견되지 않았다. 현재 값은 모두 수정 가능한 데모 기준선이며, 프로젝트 코어와 충돌하지 않는다.

판정:

```text
R2_BATCH_006_APPROVED_10_OF_10
MERGED_PR120_MAIN_CANON
PRODUCT_IMPLEMENTATION: BLOCKED
VERTICAL_SLICE_IMPLEMENTATION: APPROVED
HUMAN_PLAYTEST: NOT_RUN
```



## 구현 승인 범위

```yaml
GENERAL_PRODUCT_IMPLEMENTATION_REMAINS_BLOCKED: true
VERTICAL_SLICE_IMPLEMENTATION: APPROVED
APPROVED_NAMESPACES:
  - scripts/vertical_slice/
  - data/vertical_slice/
  - scenes/vertical_slice/
  - tests/vertical_slice/
FINAL_BALANCE_APPROVAL: false
HUMAN_PLAYTEST: NOT_RUN
```

이번 승인은 승인된 대표 버티컬 슬라이스 구현에만 적용한다. 다른 제품 경로, 전체 콘텐츠 생산, 최종 밸런스, 출시 승인은 열지 않는다.

## 승인·병합 증거

```yaml
USER_APPROVAL: PASS
SOURCE_PR: 120
SOURCE_EXACT_HEAD: 388eff03c61126d8021601c3ab84efaa2133253e
SQUASH_MERGE_SHA: a8a94343c78a68bf7bb14b411e7741f43b257138
AUTHORITY: MAIN_CANON
IMPLEMENTATION_SCOPE: VERTICAL_SLICE_ONLY
FINAL_BALANCE_APPROVAL: false
HUMAN_PLAYTEST: NOT_RUN
```

사용자 승인은 Batch 006의 10개 Decision과 승인된 namespace의 Godot 버티컬 슬라이스 구현 착수를 허용한다. 전체 제품 구현, 최종 밸런스 확정, 사람 플레이테스트 완료를 의미하지 않는다.
