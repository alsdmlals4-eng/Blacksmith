# Blacksmith P2 Content Result Foundation Design

Decision: `BS-VS-P2-20260813-01`

Status: `USER_APPROVED / PHASE_C_EXISTING_CANON_ONLY / A2_SCOPE_LOCKED`

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

This foundation owns axis **names**, not outcome value catalogs. Each value must be a non-empty uppercase token matching `^[A-Z0-9_]+$`. Exact outcome enums, thresholds, probabilities, rewards, losses, and copy remain separate content implementation/playtest work.

### Reasons and next action

- `causal_reasons`: 2–4 distinct non-empty uppercase tokens.
- `primary_next_action`: one non-empty uppercase token.
- The record does not calculate reasons or choose the action; it only validates and persists already-resolved output.

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

## 8. Files

Create:

- `data/vertical_slice/content_result_contract.json`
- `scripts/vertical_slice/domain/vs_content_result_record.gd`
- `tests/gut/unit/vertical_slice/test_vs_content_result_record.gd`
- `tests/test_vertical_slice_content_result_contract.py`
- `docs/operations/BLACKSMITH_P2_CONTENT_RESULT_FOUNDATION_A2_CONTRACT.json`
- `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json`

Modify:

- `scripts/vertical_slice/domain/vs_save_envelope.gd`
- `tests/gut/unit/vertical_slice/test_vs_save_service.gd`
- `tests/test_vertical_slice_task1_canon_contract.py`

No scene/resource/project settings files are changed.

## 9. Acceptance

- Data contract is an exact structural mirror of current D01–D09 decision/content/customer/result-axis tuples.
- Valid D01, D03, and D09 records pass.
- Wrong decision/customer/axis set fails.
- Invalid/duplicate UID references fail according to policy.
- Unknown score/progression fields fail.
- Existing generic resolved events continue to load unchanged.
- Typed result records survive save/load without reroll or key drift.
- Python, GUT, Godot import/parse, adapter protected-change gate, and project regression suites pass at exact PR head.
- Android device, visual result, accessibility, performance, and human playtest remain `NOT_RUN`.

## 10. Rollback

Revert the created contract/domain/test files and restore `vs_save_envelope.gd`, `test_vs_save_service.gd`, and the Python test router. Save schema remains version 1, so no migration rollback is required. Any save containing `CONTENT_RESULT_V1` remains plain Dictionary data to older code, but release use is not authorized before the package is merged and validated.
