# Blacksmith 결과·콘텐츠 공통 데이터 계약

> 상태: `CURRENT_PLANNING_CONTRACT`
>
> 기준일: `2026-07-31`
>
> Work Mode: `PLAN`
>
> 구현 권한: `NONE`
>
> 추적 Issue: #79
>
> 상위 문서: `BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md`

## 1. 목적

검투사 카시아와 수집가 에르사가 서로 다른 콘텐츠처럼 보이면서도 동일한 고객 요청·제품 선택·판매·세계 결과·연대기 구조를 재사용하도록 논리 데이터 계약을 고정한다.

이 문서는 Godot 클래스·JSON 스키마·서버 API를 구현하지 않는다. 구현 단계에서 데이터를 설계할 때 지켜야 하는 필드 책임과 상태 전이를 정의한다.

## 2. 공통 콘텐츠 단위

하나의 고객 콘텐츠 세트는 다음 논리 단위로 구성한다.

```text
ContentSet
├─ CustomerProfile
├─ CustomerRequest
├─ EligibleEquipmentRules
├─ PublicFitRules
├─ PreparationChoices
├─ WorldOutcomeTable
├─ ContributionRules
├─ StateDeltas
└─ ChronicleTemplates
```

고객 이름·장비 이름·사건 이름을 시스템 분기 조건으로 사용하지 않는다.

## 3. 공통 필드

### 3.1 ContentSet

| 필드 | 책임 |
|---|---|
| content_set_id | 콘텐츠 세트 불변 식별자 |
| schema_version | 데이터 구조 버전 |
| customer_id | 고객 참조 |
| request_id | 요청 참조 |
| world_event_id | 판매 후 결과 사건 참조 |
| enabled_for_vertical_slice | 대표·증명 세트 포함 여부 |
| required_features | 필요한 공통 기능 목록 |

### 3.2 CustomerProfile

| 필드 | 책임 |
|---|---|
| customer_id | 고객 불변 식별자 |
| display_name | 표시 이름 |
| customer_type | 검투사·수집가 등 유형 |
| value_axes | 공개 가치 방향 |
| relationship_state | 현재 관계 상태 |
| biography_ref | 서사·카피 참조 |
| portrait_ref | 아트 참조 |

### 3.3 CustomerRequest

| 필드 | 책임 |
|---|---|
| request_id | 요청 식별자 |
| requested_category | 무기·방어구 같은 거래 자격 범주 |
| start_operating_day | 요청 시작 영업일 |
| deadline_operating_day | 마감 영업일 |
| public_value_axes | 플레이어에게 공개할 평가 방향 |
| budget_rule | 가격 예산·상한 규칙 |
| eligible_statuses | 판매 가능한 장비 상태 |
| completion_state | 활성·판매 완료·거절·만료 |

특정 장비 이름은 요청 자격으로 사용하지 않는다.

### 3.4 EquipmentSnapshot

판매·결과 판정 시점의 장비 정보를 복제하지 않고 불변 참조와 확정 스냅샷으로 기록한다.

| 필드 | 책임 |
|---|---|
| equipment_id | 장비 생애 불변 ID |
| equipment_category | 거래 자격 범주 |
| equipment_type | 장검·방패 등 세부 종류 |
| craftsmanship_grade | 제작 등급 |
| enhancement_level | 강화 단계 |
| lineage_id | 계보 ID |
| secondary_affix_ids | 보조 수식어 최대 2개 |
| evolution_id | +50 진화 형태 |
| fate_state | 정상·전투 흔적·분실·회수·영구 파괴 |
| owner_id | 판정 시점 소유자 |
| chronicle_summary | 판정에 필요한 연대기 요약 |
| ruleset_version | 해당 작품이 생성·변경된 규칙 버전 |

## 4. 거래 자격과 공개 적합도

### 거래 자격

```text
requested_category 일치
+ 제작 완료
+ 판매 가능 상태
+ 플레이어 소유
→ 거래 후보
```

낮은 제작 등급·강화 단계·수식어 부재·낮은 적합도는 거래 자격을 막지 않는다.

### 공개 적합 신호

적합도는 단일 숨은 점수만 보여주지 않고 이유 단위로 구성한다.

```text
FitReason[]
- source_type
- source_id
- matched_value_axis
- direction
- public_explanation_key
- price_effect_band
- relationship_effect_band
- world_result_effect_tag
```

`direction` 후보:

- STRONG_POSITIVE
- POSITIVE
- NEUTRAL
- NEGATIVE

숫자 내부값을 사용하더라도 플레이어에게 이유 없이 종합 별점 하나만 노출하지 않는다.

## 5. 판매 원자적 결과

판매 확정 시 다음을 분리 저장하지 않는다.

```text
판매 대상 장비
+ 판매 가격·즉시 보상
+ 플레이어 보관함 제거
+ 고객에게 소유권 이전
+ 요청 완료
+ 관계 초기 변화
+ 장비 연대기 판매 기록
+ 후속 사건 예약
```

금지 상태:

- 장비는 사라졌지만 보상 없음
- 보상은 받았지만 장비 소유권 유지
- 요청은 완료됐지만 후속 사건 대상 장비가 없음
- 동일 장비 중복 판매
- 앱 재실행으로 판매 취소·중복 보상

## 6. 준비 선택

판매 후 콘텐츠 세트는 0~1개의 대표 준비 선택을 가진다.

| 필드 | 책임 |
|---|---|
| preparation_choice_id | 선택 ID |
| content_set_id | 소속 세트 |
| cost_bundle | 비용 |
| deadline | 기한 |
| public_effect_direction | 예상 도움 방향 |
| contribution_tag | 결과에서 강조 가능한 장비 기여 태그 |
| relationship_context | 관계 반응 맥락 |
| completion_state | 미선택·선택 완료·만료 |

준비 선택은 결과를 보장하지 않으며 숨은 정답으로 만들지 않는다.

## 7. 공통 세계 결과

### 7.1 WorldResultRecord

| 필드 | 책임 |
|---|---|
| world_result_id | 결과 불변 ID |
| content_set_id | 콘텐츠 세트 |
| customer_id | 고객 |
| equipment_id | 장비 |
| outcome_code | 결과 유형 |
| operating_day | 결과 발생 영업일 |
| preparation_choice_id | 선행 선택 |
| equipment_contributions | 장비 기여 원인 1~2개 |
| external_causes | 장비 외 원인 0~2개 |
| relationship_delta | 관계 변화 방향 |
| reputation_delta | 명성 변화 방향 |
| intrinsic_value_delta | 보편적 작품 가치 변화 |
| fate_transition | 운명 상태 전이 |
| reward_bundle | 보상 |
| chronicle_entries | 연대기 기록 |
| pending_acknowledgement | 미확인 결과 여부 |
| ruleset_version | 판정 규칙 버전 |

### 7.2 기여 원인

```text
Contribution
- source_type: GRADE / LEVEL / LINEAGE / SECONDARY / EVOLUTION / HISTORY / PREPARATION
- source_id
- contribution_tag
- public_reason_key
- scene_cue_key
- value_band
```

장비 기여는 결과 전체를 단독 결정하지 않는다. 장비 외 원인을 별도 표시해 승패·성과를 장비 수치 하나로 환원하지 않는다.

### 7.3 상태 변화

관계·명성·가치 변화는 초기 기획에서 숫자를 확정하지 않고 방향과 강도 구간으로 저장한다.

- NONE
- LOW
- MEDIUM
- HIGH

정확한 수치는 밸런스 데이터에서 결정한다.

## 8. 카시아 검투사 결과 세트

### 8.1 대표 준비

```text
ARENA_TUNING_SUPPORT
```

- 비용을 사용해 작품 특징이 결정적 장면에서 드러날 가능성을 높인다.
- 경기 승리를 보장하지 않는다.
- 지원하지 않은 경로도 유효하다.

배팅은 별도 선택적 변형이며 대표 결과 계약에 필요하지 않다.

### 8.2 대표 결과 2종

#### ARENA_WIN_BREAKTHROUGH

```text
승리
+ 장비 기여 원인 1~2개
+ 외부 원인 0~1개
+ 관계 상승
+ 명성 상승
+ 장비 연대기 승리 기록
```

핵심 표현:

- 무엇이 승리에 기여했는지 공개
- 지원 선택이 어떤 장면을 만들었는지 공개
- 승리를 장비의 단일 전투력 때문이라고 단정하지 않음

#### ARENA_LOSS_WITH_PROOF

```text
패배
+ 장비 기여 원인 1개 이상
+ 패배 외부 원인 1개 이상
+ 관계 유지 또는 소폭 상승
+ 명성은 결과 맥락에 따라 유지·소폭 변화
+ 장비 연대기 실전 증명 기록
```

핵심 표현:

- 패배했다고 장비 가치가 0이 되지 않음
- 장비 기여와 패배 원인을 분리
- 카시아가 장비를 탓하는 단일 반응 금지
- 다음 경기·다음 작품 방향을 제공

### 8.3 진화별 기여 분포

| 진화 | 대표 기여 | 관계·명성 | 시장·연대기 |
|---|---|---|---|
| 성벽파쇄 | 방패·중장갑 돌파 | 보통 | 결정적 장면 기록 |
| 용광의 심장 | 연속 압박·잔열 | 보통 | 제작자 화로 정체성 |
| 투기장의 맹세 | 안정·관중 상징 | 높음 | 소유자·경기 기록 |

결과 총가치는 유사하게 유지하고 강조 축만 다르게 한다.

## 9. 에르사 수집가 결과 세트

### 9.1 전시 선택

#### EXHIBIT_CRAFT_TECHNIQUE

- 제작 등급
- 구조·마감
- 계보·보조 조합
- 제작자 기록

을 중심으로 전시한다.

#### EXHIBIT_LIVED_HISTORY

- 과거 소유자
- 전투 흔적
- 사건·회수 기록
- 장비 연대기

를 중심으로 전시한다.

### 9.2 대표 결과

#### EXHIBITION_CRAFT_ACCLAIM

```text
제작 기술 중심 전시 성공
→ 제작 등급·수식어 기여 공개
→ 보편 가치 상승
→ 에르사 관계 상승
→ 제작 기술 연대기 추가
```

#### EXHIBITION_HISTORY_RESONANCE

```text
사건 기록 중심 전시 성공
→ 소유·사건·운명 기록 기여 공개
→ 역사 가치 상승
→ 에르사 관계 상승
→ 전시·관람 반응 연대기 추가
```

두 결과는 다른 시스템이 아니다. 같은 WorldResultRecord와 Contribution 구조를 사용한다.

## 10. 수식어 범주 적합표

### 10.1 계보

| 계보 ID | 무기 | 방어구 | 방패 | 의식 장비 |
|---|---|---|---|---|
| 정밀 | 높음 | 높음 | 보통 | 높음 |
| 파쇄 | 높음 | 보통 | 높음 | 낮음 |
| 수호 | 보통 | 높음 | 높음 | 보통 |
| 기민 | 높음 | 높음 | 보통 | 낮음 |
| 잔화 | 높음 | 보통 | 보통 | 높음 |
| 명예 | 보통 | 보통 | 높음 | 높음 |

`낮음`은 금지가 아니라 기본 후보 가중치가 낮다는 뜻이다. 콘텐츠가 이유를 제공하면 사용할 수 있다.

### 10.2 보조 수식어

| 보조 | 무기 | 방어구 | 방패 | 의식 장비 | 제한 |
|---|---|---|---|---|---|
| 균형 잡힌 | 높음 | 보통 | 보통 | 낮음 | 없음 |
| 경량화된 | 높음 | 높음 | 보통 | 낮음 | 중량화된과 배타 |
| 중량화된 | 높음 | 보통 | 높음 | 보통 | 경량화된과 배타 |
| 견고한 | 높음 | 높음 | 높음 | 보통 | 없음 |
| 충격을 흘리는 | 보통 | 높음 | 높음 | 낮음 | 없음 |
| 손에 맞춘 | 높음 | 높음 | 높음 | 보통 | 소유자 맥락 필요 |
| 울림 있는 | 보통 | 낮음 | 보통 | 높음 | 없음 |
| 흔적을 새긴 | 보통 | 보통 | 보통 | 높음 | 연대기 맥락 권장 |
| 의식 각인의 | 낮음 | 보통 | 높음 | 높음 | 의식·명예 맥락 |
| 현장형 | 높음 | 높음 | 높음 | 낮음 | 없음 |

### 10.3 후보 생성

```text
장비 범주
+ 재료·촉매 태그
+ 기존 계보·보조
+ 이정표 단계
→ 유효 후보 풀
→ 의미 중복·배타 제거
→ 공개 후보 2~3개
```

- 유효 후보가 2개 미만이면 데이터 오류다.
- 동일 수식어 중복 선택 금지
- +30 계보 파생은 현재 계보를 버리고 무관한 계보로 무작위 변경하지 않음
- +50 진화는 현재 계보와 콘텐츠 세트에 맞는 후보만 제공

## 11. 연대기 문장 구조

연대기는 자유 텍스트만 저장하지 않고 원인·행동·결과를 분리한다.

```text
ChronicleEntry
- entry_id
- equipment_id
- operating_day
- event_type
- actor_ids
- location_id
- cause_tags
- action_key
- outcome_key
- public_summary_key
- detail_template_key
- immutable_snapshot
```

예시:

```text
[카시아 벨란]
[상위 투기장 예선]
[성벽파쇄가 상대 방패를 무너뜨림]
[첫 승리]
```

표시 문장은 현지화 템플릿으로 생성하고 장비 상태 판정은 구조화 필드를 사용한다.

## 12. 저장·복귀

결과 판정:

```text
영업 종료
→ 결과 정확히 1회 판정
→ WorldResultRecord 생성
→ 관계·명성·가치·운명·보상·연대기 원자적 저장
→ pending_acknowledgement = true
→ 결과 화면 표시
```

앱 중단:

- 저장 전: 이전 확정 상태 유지
- 저장 후: 같은 결과 표시
- 결과 화면 도중: 재판정 금지
- 확인 후: pending 상태 해제
- 보상·관계·연대기 중복 적용 금지

## 13. 검증 계약

1. 고객 이름을 확인하는 하드코딩 분기 없음
2. 카시아·에르사가 같은 요청·판매·결과 구조 사용
3. 판매 후 소유권과 보상 원자적 저장
4. 결과당 장비 기여 원인 최소 1개 표시
5. 패배도 유효한 연대기와 다음 행동 제공
6. 에르사 전시 선택이 새 핵심 엔진을 만들지 않음
7. 수식어 배타·중복 후보 자동 차단
8. 유효 후보 2개 미만 데이터 오류 탐지
9. 결과 복귀 시 같은 WorldResultRecord 사용
10. 파괴 장비는 결과 대상이 될 수 없고 역사 기록만 조회 가능

## 14. 현재 판정

```text
SHARED_CONTENT_DATA_MODEL: DEFINED
CUSTOMER_NAME_HARDCODING: FORBIDDEN
CASSIA_WIN_LOSS_RESULTS: DEFINED
ERSA_EXHIBITION_RESULTS: DEFINED
CONTRIBUTION_REASON_MODEL: DEFINED
AFFIX_ELIGIBILITY_MATRIX: DEFINED
AFFIX_CONFLICT_RULES: DEFINED
CHRONICLE_STRUCTURE: DEFINED
ATOMIC_RESULT_COMMIT: REQUIRED
IMPLEMENTATION_SCHEMA: DEFERRED_UNTIL_검수_완료
GOOGLE_SHEET_SYNC: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
