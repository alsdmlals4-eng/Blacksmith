# Blacksmith 검증·증거·로컬 텔레메트리 승인 정본

> Decision ID: `BS-VALIDATION-20260801-01`
>
> 상태: `USER_PREAPPROVED_RECOMMENDED / CANONICAL_DESIGN_COMPLETE`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`

## 1. 목적

과거 PoC 자동 PASS, 최신 v9 설계 완료, 실제 제품 구현, Android 기기, 접근성, 성능, 외부 플레이를 서로 다른 증거 단계로 관리한다. 어떤 문서·Sheet·PR도 실행하지 않은 검사를 PASS로 표시하지 못하게 한다.

오프라인 제품 방향을 유지하면서 플레이테스트와 문제 재현에 필요한 텔레메트리를 로컬·비식별·수동 내보내기로 제공한다.

## 2. 증거 성숙도

```text
E0_DESIGN_ONLY
E1_STATIC_CONTRACT_VALIDATED
E2_AUTOMATED_UNIT_PASS
E3_HEADLESS_INTEGRATION_PASS
E4_RENDERED_SCENE_PASS
E5_ANDROID_DEVICE_PASS
E6_ACCESSIBILITY_AND_HUMAN_PASS
E7_EXTERNAL_PLAYTEST_PASS
E8_RELEASE_EVIDENCE_COMPLETE
```

### 규칙

- 높은 단계는 낮은 단계의 필수 증거를 포함한다.
- 문서·계획 작성은 E0다.
- JSON parse·schema validator만 통과하면 E1이다.
- 테스트 파일이 존재하는 것과 실행 PASS는 다르다.
- CI가 다른 commit에서 통과한 결과는 현재 head의 PASS가 아니다.
- Android·접근성·사람·성능은 자동 테스트로 대체할 수 없다.
- `NOT_RUN`, `FAILED`, `BLOCKED`, `PASS`를 명시한다.

## 3. 검증 Lane

### Lane A — Authority·Data Static

- JSON·Markdown 구조
- Decision ID uniqueness·supersedes
- GitHub↔Sheet same-ID binding
- Base adapter pin·hash·generated provenance
- Placeholder·Asset Manifest·License Ledger
- 데이터 참조·고객 ID·장비 UID schema

### Lane B — Domain Unit

- 제작 등급·마감 분리
- 강화 확률·위험·이정표
- SaveStatus·hash·backup rotation
- migration mapper
- customer eligibility/fit/relationship
- auto-enhance policy/boundary
- storage/archive/sale price
- settings/back-stack

### Lane C — Transaction Integration

- 단조 출력 예약
- 강화 PREPARED→APPLIED
- 판매·고객 인계
- 세계 결과·장비 운명
- 회수·보관함 full
- 저장·마이그레이션 실패 롤백
- 동일 transaction/event/envelope 멱등성

### Lane D — Product Flow Headless

```text
Boot→Main→New/Continue→BlacksmithApp
→Forge→Grade→Enhance→Identity/+50
→Storage/Sale/Customer→World Result→Chronology
→Save/Restart/Recovery
```

대표 경로와 실패·중단 경로를 결정론적 fixture로 실행한다.

### Lane E — Rendered UI·Visual

- 12 Screenshot Baseline
- 5 viewport/safe-area fixture
- text scale·reduced motion·precision assist
- focus/back/Overlay
- Modak·장비·CTA 가림
- 긴 한국어·색상 외 상태

### Lane F — Android Device

- 실제 APK/AAB 설치
- notch·gesture·3-button navigation
- home/app switch/lock/process kill
- vibration/audio focus
- 저장 공간 부족·권한·오프라인
- 대표·최악 장면 성능

### Lane G — Human·Playtest

- 최초 3초 행동 이해
- 저장·복구 신뢰
- 강화 위험·자동 강화 정지 이유
- 고객 eligibility/fit·소유권 이해
- 장비 연대기 가치
- 텍스트 확대·모션 감소·정밀 보조

## 4. 과거 PoC 증거 분리

과거 MVP-001~003·PR #35·validation #468 증거는 다음 상태로 보존한다.

```text
HISTORICAL_POC_BASELINE
```

증명하는 것:

- 당시 구형 제작·강화·자원·6칸 보관함·카일 생애 계약
- rollback·event ID·장비 Registry 패턴

증명하지 않는 것:

- 최신 제작 등급·계보·+50
- SaveCoordinator·App Shell
- 고객 8명 공통 파이프라인
- 자동 강화 경계
- 12칸·판매 3채널·연대기 UI
- Theme·safe area·Android lifecycle

구형 테스트는 삭제하지 않고 legacy migration·regression lane으로 재분류한다.

## 5. Decision→검증 추적

각 Decision에는 최소 다음을 연결한다.

```text
Decision ID
canonical Markdown/JSON
affected product paths
static validators
automated tests
headless flow fixtures
visual/device/human gates
latest evidence status
latest evidence commit
```

필수 연결 Decision:

- `BS-SAVE-20260801-01`
- `BS-MIGRATION-20260801-01`
- `BS-CUSTOMER-PIPELINE-20260801-01`
- `BS-AUTOFORGE-20260801-01`
- `BS-EQUIPMENT-LIFECYCLE-20260801-01`
- `BS-VISUAL-ASSET-GOV-20260801-01`
- `BS-UI-PLATFORM-20260801-01`
- `BS-BASE-MIGRATION-20260801-01`

## 6. Fixture Registry

```text
fixture_id
schema_version
purpose
source_decision_ids
initial_campaign_snapshot
committed_random_values
actions
expected_state_digests
expected_result_envelopes
expected_chronology
expected_stop_or_error
legacy_source_reference
```

### 핵심 Fixture Family

- 신규 캠페인·정상 이어하기·손상 복구
- PREPARED/RESOLVED process death
- 구형 등급5·affix0~3·level0~100 migration
- 고객 8명·대표4 E2E·legacy Kyle
- 자동 강화 모든 정지점·예산·파괴·저장 실패
- 보관함 0~12·full·회수 대기·판매 3채널
- UI viewport·text·safe inset·back stack
- 오류·오프라인·저장 공간 부족

RNG가 필요한 fixture는 실행 중 randomize하지 않고 저장된 commitment를 사용한다.

## 7. CI 구조

### Pull Request required

```text
static_contracts
python_unit
Godot_import_and_unit
Godot_integration
product_flow_headless
protected_path_and_placeholder
```

### Scheduled or manual evidence

```text
visual_baseline
Android_build_and_device
performance_capture
accessibility_human_review
external_playtest
license_release_audit
```

- required CI는 동일 PR head에서 실행한다.
- flaky 재시도는 원인과 횟수를 기록하며 단순 재실행 성공으로 숨기지 않는다.
- 환경 부재는 `BLOCKED/NOT_RUN`이며 PASS가 아니다.
- product main Scene이 테스트 Scene인 동안 product flow lane은 완료로 표시하지 않는다.

## 8. 증거 보고서 필수 필드

```text
evidence_id
evidence_type
decision_ids
repository
branch
commit_sha
command_or_procedure
started_at_utc
finished_at_utc
environment
exit_code
result
summary
artifact_paths_or_urls
known_limitations
reviewer
```

- 로그 전체를 장문 정본에 복제하지 않고 artifact 경로와 핵심 판정을 기록한다.
- 실패·NOT_RUN도 이력으로 보존한다.
- 최신 head가 바뀌면 code-dependent evidence는 stale이 될 수 있다.

## 9. 로컬 텔레메트리 원칙

```text
network_upload = false
stable_device_identifier = false
personal_data = false
raw_text_or_user_content = false
manual_export = explicit
```

### 빌드별 기본값

| 빌드 | 로컬 수집 | 내보내기 |
|---|---|---|
| 개발·내부 QA | 켜짐 | 수동 |
| 외부 플레이테스트 | 명시 동의 후 켜짐 | 참가자/테스터 수동 |
| 일반 릴리스 | 꺼짐 | 사용자가 진단 내보내기를 선택할 때만 |

현재 Scope에 서버 전송·광고 ID·계정 분석·원격 프로파일링을 추가하지 않는다.

## 10. 허용 이벤트

### 진입·저장

- `app_session_started`
- `main_menu_action`
- `save_status_detected`
- `continue_started`
- `backup_recovery_offered/completed/failed`
- `save_failed`
- `process_death_recovery_completed`

### 제작·강화

- `forging_started/completed`
- `craftsmanship_grade_assigned`
- `enhancement_attempt_resolved`
- `identity_boundary_reached/chosen`
- `plus50_route_chosen`
- `auto_enhance_started/stopped`

### 장비·고객

- `storage_full_encountered`
- `equipment_sold`
- `customer_contract_offered/accepted/delivered`
- `customer_fit_viewed`
- `world_result_presented/acknowledged`
- `chronology_opened`

### UX·성능

- `screen_opened`
- `blocking_error_shown`
- `settings_changed` — 값의 범주만
- `back_action_handled`
- `frame_time_summary`
- `memory_summary`

## 11. 금지 데이터

- 이름·이메일·연락처·계정
- Google Sheet·Drive·GitHub 토큰·URL의 개인 부분
- 사용자 입력 자유문·대화·파일 경로 원문
- 안정적 기기 ID·광고 ID·전화번호
- 정확한 위치·IP·네트워크 식별자
- 원본 save 전체
- 장비에 사용자가 직접 입력한 이름이 생길 경우 원문

장비는 내부 UID를 세션 범위 hash로 변환해 기록할 수 있다.

## 12. 텔레메트리 스키마

```text
telemetry_schema_version
event_id
event_name
session_id_random
event_sequence
build_version
commit_short
platform_class
screen_or_system
coarse_game_day
event_payload_allowlisted
created_at_monotonic_or_coarse_utc
```

- `session_id_random`은 설치 간 추적을 위한 영구 ID가 아니다.
- payload는 이벤트별 allowlist를 사용한다.
- 알 수 없는 key를 자동 기록하지 않는다.
- timestamp는 문제 재현에 필요한 수준으로만 저장한다.

## 13. 저장·보존·내보내기

- `user://diagnostics/telemetry.jsonl`
- 최대 20세션 또는 30일 중 먼저 도달한 기준
- 최대 파일 크기 제한과 rotation
- 설정에서 로컬 진단 기록 삭제
- 내보내기 전 포함 범주·기간·파일 크기 표시
- 내보내기는 zip 또는 JSONL이며 사용자가 직접 전달
- save·license proof·개인 파일을 자동 첨부하지 않는다.

## 14. 텔레메트리 검증 목적

텔레메트리는 다음 질문에만 사용한다.

- 메인에서 새 게임·이어하기·복구 상태를 이해했는가
- 단조→강화→멈춤/도전 흐름이 막히는가
- 자동 강화가 어떤 이유로 자주 멈추는가
- 보관함 full이 과도한가
- 고객 조건·fit·소유권 결과를 확인하는가
- ResultEnvelope가 중복·재표시되는가
- 화면·기기에서 성능·오류가 발생하는가

게임 내 숨은 난이도 조정, 동의 없는 행동 추적, 사용자 평가 점수화에 사용하지 않는다.

## 15. Pass3·완료 Gate

기획 완료 후보:

```text
모든 P0/P1 기획 목표 RESOLVED
Base migration execution plan 존재
CURRENT/History/Placeholder propagation PASS
Decision→validation matrix 완성
Pass3 신규 P0/P1 = 0
```

구현 완료 후보:

```text
required CI same head PASS
P0/P1 runtime findings = 0
Android/device evidence PASS
accessibility/human evidence PASS
asset/license release gate PASS
known limitations accepted
```

## 16. 감사 판정

```text
BS-AUD-F20_VALIDATION_TARGET: RESOLVED
BS-AUD-F26_TELEMETRY_TARGET: RESOLVED
CURRENT_V9_EXECUTION: NOT_RUN
ANDROID_HUMAN_PERFORMANCE: NOT_RUN
P1_P2_FINDING_COUNTS: 유지
```

## 17. 현재 Gate

```text
EVIDENCE_MATURITY_MODEL: APPROVED
VALIDATION_LANES: APPROVED
FIXTURE_REGISTRY: APPROVED
CI_STRUCTURE: APPROVED
EVIDENCE_REPORT_SCHEMA: APPROVED
LOCAL_PRIVACY_FIRST_TELEMETRY: APPROVED
NETWORK_TELEMETRY: DISALLOWED_CURRENT_SCOPE
CURRENT_V9_VALIDATION_EXECUTION: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
