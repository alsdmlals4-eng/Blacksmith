# Blacksmith 세이브·이어하기·ResultEnvelope 승인 정본

> Decision ID: `BS-SAVE-20260801-01`
>
> 상태: `USER_APPROVED / CANONICAL / DESIGN_COMPLETE`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 추적: Issue #79 / Draft PR #81

## 1. 결정 요약

Blacksmith는 **단일 캠페인 + 자동 백업 2개** 구조를 사용한다.

```text
user://campaign.save
user://campaign.backup1
user://campaign.backup2
user://settings.cfg
```

- 수동 저장·수동 불러오기·다중 슬롯은 제공하지 않는다.
- 백업은 강화 결과 재시도 수단이 아니라 저장 손상 복구 수단이다.
- 설정은 캠페인과 분리한다.
- 캠페인 파일 쓰기는 `SaveCoordinator`만 수행한다.
- 각 도메인 객체는 직렬화 가능한 Snapshot만 제공하고 직접 파일에 쓰지 않는다.

## 2. 책임 구조

```text
Boot
└─ SaveCoordinator
   ├─ SaveInspector
   ├─ CampaignSerializer
   ├─ CampaignValidator
   ├─ SaveMigrator
   ├─ AtomicSaveWriter
   ├─ RecoveryCoordinator
   └─ ResultEnvelopeQueue

BlacksmithApp
└─ AppStateCoordinator
   ├─ WorkshopResources
   ├─ WorkshopCalendar
   ├─ EquipmentStorage
   ├─ ForgingSession
   ├─ EnhancementSession
   ├─ CustomerRegistry
   ├─ CustomerRelationshipRegistry
   └─ EquipmentWorldRegistry
```

### 책임 경계

- `AppStateCoordinator`: 한 캠페인의 도메인 상태를 소유한다.
- `SaveCoordinator`: 상태 수집·검증·마이그레이션·원자 저장·백업 복구를 책임진다.
- `ScreenRouter`: 저장 상태를 만들거나 변경하지 않는다.
- View·Overlay: 도메인 결과를 재계산하거나 재추첨하지 않는다.
- 결과 화면: 이미 저장된 `ResultEnvelope`만 표시한다.

## 3. CampaignSnapshot 계약

```text
CampaignSnapshot
├─ schema_version
├─ save_revision
├─ campaign_id
├─ created_at_utc
├─ saved_at_utc
├─ game_day
├─ current_route
├─ last_safe_view
├─ workshop_resources
├─ workshop_calendar
├─ equipment_storage
├─ active_forging
├─ active_enhancement
├─ active_attempt_intent
├─ customers_and_contracts
├─ customer_relationships
├─ equipment_world_registry
├─ pending_result_envelopes
└─ integrity_metadata
```

### 필수 메타데이터

| 필드 | 규칙 |
|---|---|
| `schema_version` | 마이그레이션 판정 기준 |
| `save_revision` | 저장 성공마다 1 증가 |
| `campaign_id` | 새 게임마다 새 UUID |
| `saved_at_utc` | 메인 화면 표시·백업 비교용 |
| `last_safe_view` | 손상되지 않은 화면 경로만 저장 |
| `integrity_metadata.payload_hash` | 직렬화 본문 무결성 확인 |
| `integrity_metadata.writer_version` | 저장 생성 버전 기록 |

저장 파일에는 UI Node 경로, Scene 인스턴스, Signal 연결, Tween 상태 같은 런타임 객체를 넣지 않는다.

## 4. 저장 파일과 백업 회전

### 쓰기 파일

```text
campaign.save.tmp        임시 신규 저장
campaign.save            현재 정본
campaign.backup1         직전 정상 정본
campaign.backup2         그 이전 정상 정본
campaign.corrupt.<time>  손상 파일 격리본
```

### 원자 저장 순서

```text
1. 현재 AppState를 CampaignSnapshot으로 수집
2. 스키마·필수 ID·참조 무결성 검증
3. campaign.save.tmp 기록 후 닫기
4. tmp를 다시 읽어 JSON·hash·revision 재검증
5. 기존 campaign.save가 정상일 때만 backup1·backup2 회전
6. backup1 → backup2
7. campaign.save → backup1
8. campaign.save.tmp → campaign.save
9. 새 campaign.save 최종 재검증
10. 실패 시 기존 정상 파일 유지 및 오류 상태 반환
```

### 적대적 방어 규칙

- 손상된 `campaign.save`를 `backup1`로 회전하지 않는다.
- 신규 tmp 검증 전 기존 파일을 삭제하거나 이동하지 않는다.
- 백업 회전 중 실패하면 최소 한 개의 검증된 파일을 유지해야 한다.
- 같은 `save_revision`을 중복 확정하지 않는다.
- 저장 실패를 성공 Toast로 표시하지 않는다.

## 5. 자동 저장 시점

### 필수 이벤트 저장

- 새 게임 생성 직후
- 단조 작품 완성 직후
- 강화 시도 `PREPARED` 확정 직후
- 강화 결과 `RESOLVED` 직후
- 판매·고객 인계 직후
- 세계 결과 적용 직후
- 하루 종료 직후
- ResultEnvelope 확인 완료 직후
- 메인 화면 복귀 전
- 앱 일시중지·백그라운드 전환 시도 시

### 진행 중 체크포인트

- 단조 진행 중에는 최대 30초 간격의 안전 체크포인트를 허용한다.
- 매 타격·매 프레임·정밀 게이지 이동마다 저장하지 않는다.
- 저장 요청이 겹치면 직렬화하고, 동일 revision에 대한 중복 쓰기를 병합한다.

## 6. SaveStatus와 이어하기

부팅 시 세 캠페인 파일을 모두 검사하고 하나의 `SaveStatus`를 반환한다.

| 상태 | 이어하기 | 처리 |
|---|---:|---|
| `NO_SAVE` | 비활성 | 새 게임 가능 |
| `VALID_PRIMARY` | 활성 | 현재 정본 로드 |
| `RECOVERABLE_BACKUP` | 활성 | `복구 후 이어하기` 표시 |
| `MIGRATION_REQUIRED` | 활성 | 원본 보존 후 마이그레이션 |
| `MIGRATION_FAILED` | 비활성 | 원본 보존·실패 설명 |
| `UNSUPPORTED_VERSION` | 비활성 | 지원 버전 안내 |
| `UNRECOVERABLE_CORRUPTION` | 비활성 | 저장 손상 설명·새 게임 선택 가능 |

### 메인 화면 표시 메타데이터

- 마지막 정상 저장 시각
- 게임 내 날짜
- 마지막 안전 화면
- 보유 작품 수
- 미확인 결과 존재 여부
- 저장 스키마 버전

미확인 결과는 `확인하지 않은 결과가 있습니다`라고만 표시한다. 성공·실패·파괴 여부는 메인 화면에서 미리 공개하지 않는다.

## 7. 손상 복구

```text
campaign.save 손상
→ backup1 검증
→ 실패하면 backup2 검증
→ 가장 최신의 정상 백업 선택
→ 복구 영향 표시
→ 사용자 `복구하고 이어하기`
→ 손상 파일 격리
→ 선택 백업을 새 campaign.save로 원자 복사
→ 최종 검증
→ BlacksmithApp 진입
```

복구 안내에는 다음을 표시한다.

- 복구 대상 저장 시각
- 손상 정본보다 얼마나 이전인지
- 복구될 게임 내 날짜
- 미확인 ResultEnvelope 보존 여부
- 손상 파일이 진단용으로 격리된다는 점

다음은 금지한다.

- 사용자가 backup1·backup2를 임의 선택
- 결과 확인 후 과거 백업 불러오기
- 특정 강화 직전으로 되돌리기
- 손상 저장을 자동 삭제하고 새 게임 시작

## 8. 새 게임 교체

기존 캠페인이 있을 때 `새 게임`은 즉시 삭제하지 않는다.

```text
새 게임 선택
→ 기존 캠페인 요약 표시
→ `기존 기록을 교체합니다` 경고
→ 취소 / `기존 기록을 교체하고 새 게임`
→ 신규 캠페인을 tmp에 생성
→ 검증 성공
→ 기존 정본을 교체 대기 파일로 이동
→ 신규 campaign.save 확정
→ 신규 백업 체계 초기화
```

- 신규 캠페인 생성 또는 첫 저장 실패 시 기존 캠페인을 유지한다.
- 버튼은 결과가 명확한 문구를 사용하며 단순 `확인`을 금지한다.
- 텍스트 재입력·길게 누르기 같은 추가 마찰은 사용하지 않는다.
- 신규 캠페인 정상 확정 뒤 이전 캠페인을 일반 UI에서 복구할 수 없다.

## 9. AttemptIntent 계약

비가역·확률 행동은 적용 전에 `AttemptIntent`를 사용한다.

```text
AttemptIntent
├─ intent_id
├─ action_type
├─ equipment_uid
├─ target_level
├─ before_snapshot
├─ consumed_gold
├─ consumed_materials
├─ deterministic_rng_state_or_commitment
├─ created_revision
└─ state: PREPARED | RESOLVED | CANCELLED
```

### 강화 트랜잭션

```text
1. 행동 검증
2. AttemptIntent PREPARED 생성
3. PREPARED가 포함된 저장을 원자 확정
4. 비용·재료 소비 및 결과 판정
5. 도메인 변경 + ResultEnvelope APPLIED 구성
6. Intent RESOLVED + 변경 상태 + ResultEnvelope를 같은 revision에 원자 저장
7. 결과 화면 표시
```

### 중단 복구

- `PREPARED`: `before_snapshot`으로 복구하고 비용·재료가 중복 차감되지 않게 한다.
- `RESOLVED`: 결과를 다시 판정하지 않고 저장된 ResultEnvelope를 표시한다.
- 동일 `intent_id`는 한 번만 적용한다.
- `PREPARED`와 `RESOLVED` 사이에 종료돼도 결과 없는 자원 소실을 허용하지 않는다.

## 10. ResultEnvelope 계약

```text
ResultEnvelope
├─ envelope_id
├─ intent_id
├─ result_type
├─ subject_type
├─ subject_id
├─ source_action
├─ previous_snapshot_digest
├─ resulting_snapshot_digest
├─ outcome
├─ resource_changes
├─ ownership_changes
├─ relationship_changes
├─ fate_changes
├─ chronology_entries
├─ created_revision
├─ applied_revision
├─ presentation_route
└─ state: CREATED | APPLIED | PRESENTED | ACKNOWLEDGED
```

### 상태 규칙

```text
CREATED
→ 도메인 변경 준비

APPLIED
→ 도메인 변경과 Envelope가 같은 저장 revision에 확정

PRESENTED
→ 화면에 표시 시작

ACKNOWLEDGED
→ 사용자가 결과를 확인하고 닫음
```

- `APPLIED` 저장 전 결과 화면을 열지 않는다.
- `PRESENTED`만 저장되고 앱이 종료돼도 같은 결과를 다시 표시할 수 있다.
- `ACKNOWLEDGED` 후에는 일반 큐에서 제거하되 장비 연대기·감사 기록은 유지한다.
- 화면 진입·뒤로가기·앱 재실행으로 결과를 재추첨하지 않는다.
- 판매·소유권 이전·세계 결과·영구 파괴처럼 여러 시스템을 바꾸는 결과도 하나의 Envelope에 묶는다.

## 11. 이어하기 후 복구 우선순위

```text
1. APPLIED 또는 PRESENTED 상태의 미확인 ResultEnvelope
2. PREPARED 상태 AttemptIntent 롤백
3. 안전하게 재개 가능한 단조·강화 작업
4. last_safe_view
5. 대장간 허브
```

- 미확인 Envelope가 여러 개면 `applied_revision` 오름차순으로 표시한다.
- 화면 경로가 구버전·손상 상태면 허브로 이동하되 캠페인·작품·자원 상태는 유지한다.
- 단조 마감 게이지는 단계만 유지하고 위치는 안전 시작점으로 초기화한다.
- 결과가 확정되지 않은 강화 정밀 단계는 `PREPARED` 복구 규칙을 적용한다.

## 12. 설정 파일

`settings.cfg`는 캠페인과 분리하며 다음 범주만 저장한다.

- 음악·효과음 음량
- 진동
- 모션 감소
- 정밀 보조
- 텍스트 크기
- 접근성 표시 옵션

설정 손상은 캠페인 손상으로 취급하지 않는다. 설정 파일이 손상되면 기본값으로 재생성하고 사용자에게 간단히 알린다.

## 13. 오류 처리

| 오류 | 처리 |
|---|---|
| tmp 직렬화 실패 | 기존 정본 유지, 저장 실패 표시 |
| tmp 재검증 실패 | tmp 격리 또는 삭제, 기존 정본 유지 |
| backup 회전 실패 | 검증된 파일 유지, 다음 저장 재시도 |
| primary hash 불일치 | 백업 검사로 전환 |
| 마이그레이션 실패 | 원본 보존, 이어하기 차단 |
| ResultEnvelope 참조 누락 | 결과 재판정 금지, 복구 오류 화면 |
| 중복 intent/envelope ID | 두 번째 적용 차단, 진단 로그 기록 |
| 저장 공간 부족 | 비가역 행동 시작 차단 또는 기존 상태 유지 |

저장 공간 부족이나 쓰기 불가 상태에서 비가역 행동을 먼저 적용하지 않는다.

## 14. 테스트 매트릭스

### 자동 계약 테스트

1. 저장 없음 → 이어하기 비활성
2. 정상 primary → 이어하기 활성
3. primary 손상 + backup1 정상 → 복구 가능
4. primary·backup1 손상 + backup2 정상 → backup2 복구
5. 세 파일 모두 손상 → 새 게임 자동 시작 금지
6. 손상 primary가 backup으로 회전되지 않음
7. tmp 검증 실패 시 기존 primary 유지
8. 저장 성공마다 revision 1 증가
9. 동일 revision 중복 적용 차단
10. PREPARED 중 종료 → 자원·장비 before_snapshot 복구
11. RESOLVED 후 종료 → 동일 결과 재표시
12. 결과 화면 재진입 → RNG 재호출 0회
13. ResultEnvelope 중복 적용 0회
14. 판매·소유권·관계·연대기 변화가 한 revision에 함께 저장
15. 새 게임 생성 실패 → 기존 캠페인 유지
16. 새 게임 성공 → 기존 캠페인 일반 UI 복구 불가
17. 마이그레이션 실패 → 원본 바이트 보존
18. 설정 손상 → 캠페인 영향 없이 기본 설정 복구

### Android 실기기 테스트

- 단조 중 홈 이동·복귀
- 강화 PREPARED 직후 프로세스 종료
- RESOLVED 직후 결과 화면 전 프로세스 종료
- 고객 인계 직후 백그라운드 종료
- 세계 결과 적용 직후 강제 종료
- 저장 공간 부족 또는 파일 쓰기 실패 모의
- Android 뒤로가기 연타 중 중복 저장·중복 결과 없음

### 사람 검증

최소 6명에게 다음을 검증한다.

- 저장 없음과 이어하기 불가 상태를 3초 안에 이해
- 복구가 결과 재시도가 아니라 손상 복구임을 이해
- 새 게임이 기존 기록을 교체한다는 점을 오인하지 않음
- 미확인 결과 복구 후 같은 결과임을 신뢰

## 15. 통과 기준

```text
SAVE_STATE_DUPLICATION: 0
RESULT_REROLL_ON_RESTART: 0
RESULT_DOUBLE_APPLY: 0
RESOURCE_LOSS_WITHOUT_RESULT: 0
CORRUPT_PRIMARY_BACKUP_POISONING: 0
NEW_GAME_FAILURE_DATA_LOSS: 0
MIGRATION_FAILURE_SOURCE_OVERWRITE: 0
```

자동 계약·Android 실기기·사람 검증을 모두 실행하기 전에는 런타임 완료로 표시하지 않는다.

## 16. 기존 프로젝트와의 연결

보존할 기존 강점:

- `WorkshopResources`의 비용·재료 선검증과 실패 롤백
- `EquipmentWorldRegistry`의 거래·세계 결과 멱등성 ID
- 각 도메인의 `snapshot()` 패턴
- 강화 입력당 결과 1회 원칙

보완할 점:

- 현재 Snapshot은 복원용 스키마·버전·참조 검증이 부족하다.
- `EnhancementSession`은 RNG 상태와 PREPARED/RESOLVED 저장 경계가 없다.
- 세 PoC 흐름이 하나의 AppState를 공유하지 않는다.
- 제품용 파일 저장·백업·복구·마이그레이션 계층이 없다.

## 17. 감사 판정

```text
BS-AUD-F02_PLANNING_TARGET: RESOLVED_BY_BS-SAVE-20260801-01
BS-AUD-F09_PLANNING_TARGET: RESOLVED_BY_BS-SAVE-20260801-01
BS-AUD-F16_PARTIAL_PLANNING_TARGET: RESOLVED_FOR_PAUSE_AND_PROCESS_DEATH
RUNTIME_IMPLEMENTATION: OPEN
RUNTIME_VERIFICATION: NOT_RUN
P0_FINDING_COUNT: 유지
```

기획 목표는 해결됐지만 제품 구현·마이그레이션·테스트가 실행되지 않았으므로 감사 Finding 자체는 닫지 않는다.

## 18. 현재 Gate

```text
SAVE_SLOT_MODEL: SINGLE_CAMPAIGN_WITH_TWO_AUTOMATIC_BACKUPS
MANUAL_LOAD: DISALLOWED
CONTINUE_STATUS_MODEL: APPROVED
CORRUPTION_RECOVERY: APPROVED
NEW_GAME_REPLACEMENT: APPROVED
ATTEMPT_INTENT: APPROVED
RESULT_ENVELOPE: APPROVED
AUTOSAVE_BOUNDARIES: APPROVED
TEST_MATRIX: APPROVED
PRODUCT_CODE_CHANGE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
