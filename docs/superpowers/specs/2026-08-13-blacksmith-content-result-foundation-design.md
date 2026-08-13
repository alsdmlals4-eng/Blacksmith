# Blacksmith P2 Content Result Foundation Design

Decision: `BS-VS-P2-20260813-01`

Status: `MERGED_MAIN_CANON / POSTMERGE_FULL_VALIDATION_PASS / PHASE_C_EXISTING_CANON_ONLY`

> 이 문서는 현재 설계 정본이다. 최초 구현 계획의 일회성 `PROJECT_PROTECTED_CHANGE_APPROVAL` 단계는 현행 어댑터의 하위 경로 감지 방식과 충돌하여 폐기됐다. 실제 처리와 후속 기준은 8절 및 A2 실행 계약을 우선한다.

## 0. Postmerge Closure

```text
IMPLEMENTATION_PR: 162
TDD_RED_HEAD: 3632f2efc8a48a9506f1ceae548891c9c95c07da
EXACT_HEAD: b0118e980df06c641c6b19372f364fa52a94b394
MERGED_MAIN_CANON: 78eeb4c442a917051b327ddc050f9337b41516b0
```

- Full Validation run `31653614060`: `PASS`
- Live-Editor Pilot run `31653614171`: `PASS`
- Base 보호 경로 후속: `alsdmlals4-eng/Base#314`
- Android 실기기·사람 플레이테스트·접근성·성능·Sheet 동기화: `NOT_RUN`

P2 A2 제품 Writer Lease는 병합과 postmerge 검증으로 폐쇄됐다. 다음 Phase C 제품 패키지는 자동 선택하지 않으며 별도 A0 SHADOW와 승인된 A2 계약이 필요하다.

## 1. Goal

승인된 R3–R7 콘텐츠 D01–D09의 결과를 새 게임플레이·확률·총점 없이 하나의 검증 가능한 JSON 레코드로 저장한다.

플레이어 가치는 다음과 같다.

- 결과 화면과 재방문에서 **같은 작품 UID**를 다시 식별할 수 있다.
- 서로 다른 세 결과 축이 하나의 승패·총점으로 합쳐지지 않는다.
- 실제 인과 이유 2~4개와 다음 행동 하나가 저장 후에도 유지된다.
- Batch·계승·교체처럼 UID 구조가 다른 콘텐츠도 history overwrite 없이 표현된다.

## 2. Existing Solution First

### REUSE

- `VSSaveEnvelope.active_run.resolved_events`: 이미 해결된 RNG/이벤트를 다시 굴리지 않고 저장하는 소유자.
- `VSItem` UID 형식: `^BSI-[0-9a-f]{32}$`.
- `VSSaveService`: JSON atomic write, backup recovery, no-reroll round trip.
- R3–R7 registry의 `decision_id / content_id / customer_id / result_axes`.
- GUT 9.7.1: GDScript 테스트 권위.

### ADAPT

기존 `resolved_events` Dictionary를 없애거나 새 top-level save 필드를 추가하지 않는다. 값이 명시적으로 `record_type: CONTENT_RESULT_V1`일 때만 새 typed validator를 적용한다.

### REJECT

- 모든 Dictionary를 그대로 신뢰: 잘못된 고객·결정·결과축·UID를 조기에 차단하지 못한다.
- SaveEnvelope schema version 즉시 상승: 현재 Task1 save와 불필요한 migration 부담을 만든다.
- 새 범용 `score`, `fit_score`, `prestige_score`: 승인된 세 축 분리 계약과 충돌한다.
- 커스텀 Object 전체 직렬화 또는 binary save 전환: 현재 JSON inspectability·기존 atomic save·명시적 encode/decode 계약을 버린다.
- 고객·일정·결과 확률 구현: Task3 및 개별 콘텐츠 제품 구현을 선승인한다.

Godot 4.7 공식 문서는 JSON parse 결과의 Variant 타입을 확인하고, JSON이 지원하지 않는 커스텀 타입은 명시적으로 encode/decode해야 한다고 설명한다. 이 설계는 `Dictionary/Array/String/int`만 저장하고 도메인 객체는 `from_dict()/to_dict()`에서 검증한다.

Primary references:

- `https://docs.godotengine.org/en/4.7/classes/class_json.html`
- `https://docs.godotengine.org/en/4.7/tutorials/io/saving_games.html`

## 3. Record Contract

```json
{
  "schema_version": 1,
  "record_type": "CONTENT_RESULT_V1",
  "event_id": "CONTENT-INSTANCE-001",
  "source_decision_id": "BS-CONTENT-20260811-01",
  "content_id": "ADVENTURER_01",
  "customer_id": "NADIA_VENN",
  "occurred_at_game_day": 4,
  "item_refs": [
    {"role": "PRIMARY_ITEM", "uid": "BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
  ],
  "result_axes": {
    "EXPEDITION_RETURN_STATE": "RETURNED",
    "RECOVERY_STATE": "PARTIAL_RECOVERY",
    "ITEM_UID_LIFECYCLE_STATE": "DAMAGED_RETURN"
  },
  "causal_reasons": [
    "LOAD_GATE_PASSED",
    "ENVIRONMENTAL_SEALING_MATCHED"
  ],
  "primary_next_action": "REPAIR_ITEM"
}
```

### Required fields

```text
schema_version
record_type
event_id
source_decision_id
content_id
customer_id
occurred_at_game_day
item_refs
result_axes
causal_reasons
primary_next_action
```

Unknown top-level fields are rejected. This prevents score/progression fields from silently entering the save contract.

### Result axis values

이 foundation은 axis **이름**만 소유한다. 각 값은 `^[A-Z0-9_]+$`를 만족하는 비어 있지 않은 대문자 토큰이어야 한다. 정확한 outcome enum, 임계값, 확률, 보상, 손실, 문구는 별도 콘텐츠 구현·플레이테스트 범위다.

### Reasons and next action

- `causal_reasons`: 2–4개의 서로 다른 비어 있지 않은 대문자 토큰.
- `primary_next_action`: 하나의 비어 있지 않은 대문자 토큰.
- 레코드는 이유를 계산하거나 행동을 선택하지 않고, 이미 해결된 출력을 검증·보존한다.

## 4. Approved D01–D09 Mapping

| Decision | Content | Customer | Result axes | Item reference policy |
|---|---|---|---|---|
| BS-CONTENT-20260811-01 | ADVENTURER_01 | NADIA_VENN | EXPEDITION_RETURN_STATE / RECOVERY_STATE / ITEM_UID_LIFECYCLE_STATE | SINGLE_PRIMARY_ITEM |
| BS-CONTENT-20260811-02 | ADVENTURER_02 | TOREN_MARCH | JOURNEY_ARRIVAL_STATE / ROUTE_EXPOSURE_STATE / ITEM_UID_LIFECYCLE_STATE | SINGLE_PRIMARY_ITEM |
| BS-CONTENT-20260811-03 | SOLDIER_01 | MAREK_OLDEN | UNIT_MISSION_STATE / STANDARD_ADOPTION_STATE / BATCH_ITEM_LIFECYCLE_STATE | BATCH_ITEMS_ONE_OR_MORE |
| BS-CONTENT-20260811-04 | COLLECTOR_01 | ERSA_ROEN | EXHIBITION_RECEPTION_STATE / EXHIBIT_THESIS_FIT_STATE / ITEM_UID_PUBLIC_LEGACY_STATE | SINGLE_PRIMARY_ITEM |
| BS-CONTENT-20260811-05 | GLADIATOR_01 | CASSIA_BELLAN | ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE | SINGLE_PRIMARY_ITEM |
| BS-CONTENT-20260811-06 | NOBLE_01 | CEREMONIAL_NOBLE | CEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE | SINGLE_PRIMARY_ITEM |
| BS-CONTENT-20260811-07 | SOLDIER_02 | LIANA_BERG | MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE | SINGLE_PRIMARY_ITEM |
| BS-CONTENT-20260811-08 | COLLECTOR_02 | SEDRIC_VAEL | ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE | SINGLE_PRIMARY_ITEM |
| BS-CONTENT-20260811-09 | GLADIATOR_02 | KYLE_VAREN | VETERAN_RETURN_STATE / EQUIPMENT_CONTINUITY_STATE / ITEM_UID_LINEAGE_STATE | LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT |

## 5. Item Reference Policies

### `SINGLE_PRIMARY_ITEM`

- 정확히 한 개.
- role은 `PRIMARY_ITEM`.
- UID 형식이 유효해야 한다.

### `BATCH_ITEMS_ONE_OR_MORE`

- 한 개 이상.
- 모든 role은 `BATCH_ITEM`.
- UID는 서로 달라야 한다.
- baseline 10개는 고정 canon이 아니므로 foundation에서 정확한 수량 10을 강제하지 않는다.

### `LEGACY_REQUIRED_OPTIONAL_DISTINCT_REPLACEMENT`

- `LEGACY_ITEM` 하나는 필수.
- `REPLACEMENT_ITEM`은 0개 또는 1개.
- replacement가 있으면 legacy UID와 달라야 한다.
- old history/progression을 new UID로 복사하는 필드는 존재하지 않는다.

## 6. SaveEnvelope Integration

`VSSaveEnvelope.from_dict()`는 `active_run.resolved_events`를 기존처럼 Dictionary로 보존한다.

- 일반 legacy event Dictionary: 변경 없이 통과.
- `record_type == CONTENT_RESULT_V1`: `VSContentResultRecord.from_dict()`로 검증.
- event map key와 record `event_id`가 다르면 `CONTENT_RESULT_EVENT_KEY_MISMATCH`.
- typed record 오류는 `CONTENT_RESULT:<event_id>:<error>` 형태로 envelope에 누적.
- valid typed record는 정규화된 `to_dict()` 결과로 저장.

기존 save fixture와 schema version 1은 유지한다.

## 7. Protected Boundaries

```text
NO_CUSTOMER_SUCCESS_FORMULA
NO_SCHEDULE_PROGRESS_RESOLVER
NO_RESULT_PROBABILITY
NO_REWARD_OR_ECONOMY_VALUE
NO_AGGREGATE_SCORE
NO_ARTISTRY_DELTA
NO_AUTOMATIC_CHRONICLE_AFFIX
NO_HISTORY_TRANSFER_TO_REPLACEMENT
NO_TASK3_IMPLEMENTATION
NO_SCENE_OR_PROJECT_SETTING_CHANGE
```

HiGodot-owned surfaces `project.godot`, `*.tscn`, `*.tres`, `*.res`, node graph, plugin/autoload settings은 변경하지 않는다.

## 8. Adapter Governance Observation

정확 head `6e1b17263be0ca9a33b1c1d99b3845716f027d2c`에서 다음 두 실패가 재현됐다.

1. 프로젝트 회귀 테스트는 이전 Task2에서 소비된 전역 일회성 파일 `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json`이 존재하면 실패한다.
2. Base validator commit `4ec410e611152294f3f2685570fca6019c7abcfa`의 현재 protected pattern `data/`, `scripts/`는 `fnmatch` 방식에서 하위 파일을 한 개의 protected-path error로 분류하지 못한다. 따라서 매니페스트와 라벨을 추가해도 승인 reconciler가 사용할 정확한 오류가 만들어지지 않는다.

PR #162의 최소 처리:

- 일회성 매니페스트 삭제.
- `approved-protected-change` 라벨 제거.
- 어댑터·워크플로·보호 정책 자체는 제품 PR에서 변경하지 않음.
- 사용자 승인 A2 계약, 정확 PR 변경 경로 감사, Python/GUT/Godot/기타 CI를 요구.
- 재귀적 보호 경로 의미 수정은 `alsdmlals4-eng/Base#314`로 분리.

이 처리로 보호 정책을 승인 없이 약화하거나 제품 범위를 확장하지 않았다. 현재 검증기가 실제로 적용하는 계약과 PR의 명시적 승인 범위를 일치시키고, 검증기 결함 수정은 독립 작업으로 남겼다.

## 9. Files

Create:

- `data/vertical_slice/content_result_contract.json`
- `scripts/vertical_slice/domain/vs_content_result_record.gd`
- `tests/gut/unit/vertical_slice/test_vs_content_result_record.gd`
- `tests/test_vertical_slice_content_result_contract.py`
- `docs/operations/BLACKSMITH_P2_CONTENT_RESULT_FOUNDATION_A2_CONTRACT.json`

Modify:

- `scripts/vertical_slice/domain/vs_save_envelope.gd`
- `tests/gut/unit/vertical_slice/test_vs_save_service.gd`
- `tests/test_vertical_slice_task1_canon_contract.py`

Documentation:

- `docs/superpowers/specs/2026-08-13-blacksmith-content-result-foundation-design.md`
- `docs/superpowers/plans/2026-08-13-blacksmith-content-result-foundation.md` — 최초 실행 계획 및 RED 절차 기록. 8절의 실제 gate deviation은 이 정본 설계를 우선한다.

No scene/resource/project settings files were changed.

## 10. Acceptance

확인된 완료 기준:

- Data contract가 current D01–D09 decision/content/customer/result-axis tuple을 정확히 반영한다.
- Valid D01, D03, D09 레코드가 통과한다.
- 잘못된 decision/customer/axis set이 실패한다.
- 정책별 invalid/duplicate UID 참조가 실패한다.
- unknown score/progression field가 실패한다.
- 기존 generic resolved event가 변경 없이 load된다.
- typed result record가 reroll이나 key drift 없이 save/load된다.
- Python, GUT, Godot import/parse, Project Base Adapter, Base adoption, BCA, Thin Adapter가 exact head에서 PASS했다.
- postmerge Full Validation과 Live-Editor Pilot이 PASS했다.
- PR changed paths는 승인된 A2 범위에만 있었고 HiGodot-owned surface는 없었다.

증거 한계:

- Android device: `NOT_RUN`
- visual result: `NOT_APPLICABLE_NO_VISUAL_CHANGE`
- accessibility: `NOT_RUN`
- performance: `NOT_RUN`
- human playtest: `NOT_RUN`
- Sheet synchronization: `NOT_RUN`

## 11. Rollback

PR #162 squash merge를 revert하면 생성된 contract/domain/test 파일과 `vs_save_envelope.gd`, `test_vs_save_service.gd`, Python test router 변경을 되돌릴 수 있다. Save schema remains version 1이므로 migration rollback은 필요하지 않다. Postmerge 폐쇄 문서는 별도 closure PR을 revert해 이전 운영 상태로 복원한다.
