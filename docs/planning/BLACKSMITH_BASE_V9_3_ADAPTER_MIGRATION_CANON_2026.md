# Blacksmith Base v9.3 프로젝트 어댑터 이관 정본

> Decision ID: `BS-BASE-MIGRATION-20260801-01`
>
> 상태: `USER_PREAPPROVED_RECOMMENDED / DESIGN_COMPLETE / EXECUTION_BLOCKED_BY_LOCAL_VALIDATION_ENVIRONMENT`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 제품 구현 권한: `NONE`
>
> 선행 감사: `BS-BASE-AUDIT-20260801-01`

## 1. 목적

Blacksmith의 Base 공용 Skill 연결을 검증된 Base v9.3 릴리스에 맞추고, canonical adapter·Snapshot·Router·Health·호환 뷰·Sheet binding·결정 진입점·보호 기준선을 하나의 생성 계약으로 정합화한다.

Base 최신 main이나 미출시 v9.4 제안을 프로젝트 릴리스 핀으로 사용하지 않는다.

## 2. 고정 대상

```text
Base version: 9.3.0
release_commit: 30ca6c7b5f93521f0eb0eed42d01437cd43c50ae
release_evidence_commit: 462a86db192d23d0f386281a1eb54b0a8cbad62e
SKILL_REGISTRY raw-byte SHA-256:
9847bb2b225c776ad7916930f0f48c490bc2a898bea8e02ea1fdd0e6caac60c1
```

Base latest main observed `90ec6f33953f80f607d4e79f58cc2174eb178f73`은 분석 근거일 뿐 핀이 아니다.

## 3. 생성 원칙

- `skills/PROJECT_BASE_ADAPTER.json`이 canonical 프로젝트 입력·결과다.
- Adapter·Snapshot·Router·Health·compatibility view는 Base generator로만 생성한다.
- 생성물 수동 편집을 금지한다.
- generator 실행 전·후 Git diff를 비교하고 제품 코드·Scene·data가 바뀌지 않았음을 확인한다.
- 기존 프로젝트 로컬 Skill 3개는 삭제하지 않고 adapter의 local registry와 연결한다.
- Base 공용 Skill 본문을 Blacksmith로 복제하지 않는다.

## 4. 실행 전 동결

실행 시점에 다음을 다시 읽고 하나의 evidence pack으로 고정한다.

```text
origin/main HEAD
open PR #81 head
CURRENT_CONFIRMED_DECISIONS.md
latest canonical decision JSON
Google Sheet ID·URL·sync status
project local Skill Registry
current adapter·Snapshot·Router·Health
protected paths inventory
working tree clean status
```

`protected_baseline_commit`은 본 문서 작성 시점의 `500a5a7…`로 고정하지 않는다. **실제 generator 실행 직전의 검증된 `origin/main` HEAD**를 사용한다. PR branch commit을 baseline으로 사용하지 않는다.

## 5. 목표 Adapter 필드

```text
base:
  version: 9.3.0
  release_commit: 30ca6c7...
  release_evidence_commit: 462a86d...
  registry_sha256: 9847bb2...

project:
  repository: alsdmlals4-eng/Blacksmith
  engine: Godot
  engine_version: 4.7.1
  language: GDScript
  platform: Android portrait
  protected_baseline_commit: <execution-time origin/main HEAD>

gdd_sheet:
  role: USER_FACING_GDD_WORKSPACE
  spreadsheet_id: 1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg
  sync_status: PROJECT_SHEET_CONFIGURED
  canonical_decision_entrypoint: CURRENT_CONFIRMED_DECISIONS.md

local_skill_registry:
  path: [기획서]/00_프로젝트_허브/SKILL_REGISTRY.json
  expected_project_skill_count: 3
```

정확한 schema key는 Base v9.3 generator의 현재 입력 스키마를 따른다. 문서의 의도를 맞추기 위해 generator 출력 key를 수동으로 발명하지 않는다.

## 6. 생성·재생성 대상

```text
skills/PROJECT_BASE_ADAPTER.json
skills/PROJECT_SKILL_SNAPSHOT.json
.agents/skills/blacksmith-workflow-router/SKILL.md
docs/PROJECT_OPERATING_HEALTH.json
Base 호환 adapter views
선택적 운영 Dashboard generated artifact
```

### 사람이 갱신하는 연결 문서

- `docs/BASE_RULES_VERSION.md`
- `docs/BASE_ADOPTION_PROFILE.json`
- `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`의 Base provenance
- `DOCUMENTATION_MAP.md`
- `CURRENT_CONFIRMED_DECISIONS.md` adapter role binding
- `docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md`

사람 문서는 generator 결과와 release evidence를 확인한 뒤 갱신한다.

## 7. Sheet binding

Adapter는 다음을 한 상태로 표현해야 한다.

```text
role: USER_FACING_GDD_WORKSPACE
configured: true
spreadsheet_id: 1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg
current_decisions_tab: 02_현재_확정결정
history_tab: 99_변경이력
sync_policy: SAME_DECISION_ID_IMMEDIATE_SYNC
```

`NOT_CONFIGURED`와 `PROJECT_SHEET_CONFIGURED`가 동시에 활성인 상태를 허용하지 않는다.

## 8. 결정 복원 진입점

`CURRENT_CONFIRMED_DECISIONS.md`를 안정 진입점으로 바인딩한다.

- 상세 규칙을 복제하지 않는다.
- 현재 Decision ID·책임 원본·대체 관계·현재 Gate만 제공한다.
- cold start에서 START_HERE 이후 한 단계 안에 발견 가능해야 한다.
- adapter·Snapshot·Router가 이 경로를 현재 결정 source로 일관되게 참조해야 한다.

## 9. Protected Paths

최소 보호:

```text
project.godot
scenes/**
scripts/**
data/**
tests/**
assets/**
CURRENT_CONFIRMED_DECISIONS.md
approved planning canon and data
project local Skill Registry and local Skill bodies
```

운영체계 이관은 제품 코드·Scene·runtime data·test semantics를 수정하지 않는다. generator가 보호 범위를 넘으면 즉시 중단한다.

## 10. 검증 순서

```text
1. Base v9.3 release/evidence commit 존재 확인
2. lock file의 Registry SHA와 raw bytes 비교
3. Blacksmith origin/main·working tree·open PR 동결
4. 기존 adapter·generated outputs 백업 diff
5. Base generator dry-run 또는 출력 목록 확인
6. canonical adapter 생성
7. Snapshot·Router·Health·compatibility views 재생성
8. 사람 연결 문서·Registry provenance 갱신
9. operating-contract validator
10. reference freshness·duplicate active source 검사
11. cold-start route 검사
12. Sheet binding·Decision ID cross-source 검사
13. Git diff boundary 검사
14. 적대적 재검토
```

검증 도구를 실행하지 못하면 PASS 대신 `NOT_RUN`이다.

## 11. 통과 기준

```text
BASE_RELEASE_PIN_MATCH = true
REGISTRY_HASH_MATCH = true
PROTECTED_BASELINE_EQUALS_EXECUTION_ORIGIN_MAIN = true
CANONICAL_ADAPTER_COUNT = 1
CONFLICTING_BASE_PINS = 0
CONFLICTING_SHEET_STATUS = 0
GENERATED_DERIVATIVE_DRIFT = 0
LOCAL_SKILL_LOSS = 0
PRODUCT_PATH_CHANGES = 0
CURRENT_DECISION_ENTRYPOINT_DISCOVERABLE = true
OPERATING_VALIDATOR = PASS
REFERENCE_FRESHNESS = PASS
COLD_START = PASS
```

## 12. 실패·롤백

- hash 불일치: 이관 중단, Base 핀 재확인
- generator schema 불일치: 수동 JSON 수정 금지, v9.3 도구·입력 계약 재확인
- protected path 변경: 생성 결과 폐기
- local Skill 누락: 생성 결과 폐기, adapter input 수정
- Sheet binding 누락: PASS 금지
- validator 실패: 기존 adapter 상태 유지, diff와 오류 보고
- partial generation: commit 금지

## 13. 기존 충돌 해결 목표

| Finding | 목표 |
|---|---|
| BASE-F01 | adapter v9.3 단일 핀 |
| BASE-F02 | execution-time origin/main baseline |
| BASE-F03 | configured Sheet 단일 상태 |
| BASE-F04 | Base Rules 현행화 |
| BASE-F05 | Adoption Profile 중복 핀 제거·역사화 |
| BASE-F06 | local Registry provenance 일치 |
| BASE-F07 | Snapshot·Router generator 재생성 |
| BASE-F08 | CURRENT_CONFIRMED_DECISIONS binding |
| BASE-F09 | Health 재생성·실제 증거 반영 |
| BASE-F10 | Sheet CURRENT/History 정리 |
| BASE-F11 | latest main 직접 pin 금지 유지 |

## 14. 현재 상태

```text
BASE_TARGET: V9_3_RELEASED_PIN
MIGRATION_DESIGN: COMPLETE
CURRENT_DECISION_ENTRYPOINT: CREATED
SHEET_CURRENT_HISTORY_INITIAL_REMEDIATION: COMPLETE
LOCAL_BASE_CHECKOUT: UNAVAILABLE_DNS
GENERATOR_EXECUTION: NOT_RUN
VALIDATOR: NOT_RUN
COLD_START_RECHECK: NOT_RUN
PRODUCT_PATH_CHANGE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
