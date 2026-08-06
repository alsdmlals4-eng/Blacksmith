# Blacksmith HiGodot·GUT 저작/검증 권위 및 작업 진입 Gate 명세

```yaml
spec_id: BS-TEST-AUTH-20260806-01
status: DRAFT_REVIEW_REQUIRED
base_sha: 07f77041f85bde223768128949ad8dc587d5a003
product_implementation: BLOCKED
vertical_slice: OPEN_ONLY_FOR_APPROVED_NAMESPACES
higodot_current: PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY
gut_current: VENDORED_PRESENT_FORMAL_ADOPTION_PENDING
change_scope: NO_PRODUCT_PATH_CHANGE
```

## 1. 목적

HiGodot과 GUT가 같은 Godot 파일을 임의로 수정하거나 서로의 역할을 침범하지 않도록 권위를 분리한다. 또한 결정 원장·미확정 목록·이미지 검수 상태가 실제 증거와 맞지 않으면 작업 진입을 차단한다.

- `HIGODOT_SOLE_AUTHORING_AUTHORITY`: 정식 채택 뒤 HiGodot만 Scene·Node·Resource·Godot 프로젝트 설정을 저작한다.
- `GUT_SOLE_TEST_AUTHORITY`: 정식 채택 뒤 GUT만 GDScript 단위·통합 테스트 프레임워크 권위를 가진다.
- `ENTRY_GATE_FAIL_CLOSED`: 필수 증거가 없거나 stale·schema drift 상태면 구현 진입을 차단한다.

현재 Live-Editor Pilot은 임시 복사본의 scratch Scene만 수정하고 원본 소스 트리를 보존한다. 따라서 이 Draft가 병합되더라도 HiGodot의 실프로젝트 저작 권위는 자동 활성화되지 않는다.

## 2. 실제 상태 복원

### HiGodot

- 설치 surface: `addons/godot_ai`
- Plugin version: `3.0.5`
- upstream 표기: `hi-godot/godot-ai`
- License: MIT
- 요구 Godot: 4.5+, 4.7+ 권장
- 현재 Pilot: source mutation 금지, main Scene read-only, scratch Scene만 임시 변경
- 현재 판정: `PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY`

### GUT 9.7.1

저장소에는 이미 `addons/gut/**`가 존재한다. 그러나 단순 vendor 존재와 정식 테스트 권위 채택은 다르다.

검증된 vendor 사실:

- local `addons/gut/plugin.cfg`: version `9.7.1`
- local `addons/gut/LICENSE.md`: MIT
- local license blob SHA: `a38ac231fed3febe257c9e5fc31efb8ec7a39f90`
- upstream v9.7.1 license blob SHA와 일치
- CLI entry `res://addons/gut/gut_cmdln.gd` 존재

검증된 upstream pin:

- source: `bitwes/Gut`
- tag: `v9.7.1`
- tag commit: `aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605`
- official compatibility: Godot 4.7.x
- license: MIT

아직 없는 정식 소비 증거:

- `project.godot`에는 `res://addons/gut/plugin.cfg`가 활성화되어 있지 않음
- `.gutconfig.json` 없음
- `tests/gut/**` 없음
- 프로젝트 GUT smoke test 없음
- exact-HEAD GUT runtime CI 없음
- JUnit 결과와 테스트 수 검증 없음
- 전체 vendor inventory·upstream 취득 manifest 미완료

현재 판정: `VENDORED_PRESENT_FORMAL_ADOPTION_PENDING`.

## 3. 승인 Decision

### BS-OPS-20260806-10 — HiGodot/GUT 권위 분리

- HiGodot은 Scene, Node, Resource, `project.godot`, Plugin, Autoload, InputMap 등 Godot Editor 직렬화 surface의 단일 저작 권위다.
- GUT는 저작 결과를 읽고 실행하여 검증하는 테스트 권위다.
- 일반 코드 편집기는 GDScript 생산 코드와 문서를 편집할 수 있지만 Godot 저작 surface를 텍스트 치환으로 우회하지 않는다.
- GUT runtime은 테스트 결과를 만들 수 있지만 Git 추적 제품 파일을 수정할 수 없다.
- HiGodot은 GUT 테스트·fixture·vendor byte·JUnit 성공 결과를 직접 수정할 수 없다.
- `GUT_RUNTIME_TRACKED_MUTATION_FORBIDDEN`과 같은 파일의 이중 권위를 위반하면 CI를 실패시킨다.

### BS-TEST-20260806-01 — GUT 9.7.1 정식 테스트 프레임워크 채택 전제

정식 채택은 다음 증거가 모두 준비된 뒤에만 `ACTIVE_TEST_AUTHORITY`로 승격한다.

1. 출처: `bitwes/Gut@v9.7.1`, commit과 취득 방식
2. 버전: local Plugin `9.7.1`
3. 라이선스: MIT 파일·제3자 라이선스 원장·vendor manifest
4. 호환성: Godot 4.7.1 clean import, Plugin load, CLI smoke 실제 PASS
5. 실제 소비: `.gutconfig.json`, `tests/gut/unit`, `tests/gut/integration`
6. Runner: `res://addons/gut/gut_cmdln.gd`
7. CI: exact HEAD에서 테스트 수 1 이상, 0-test·skip·missing runner FAIL
8. 결과: JUnit XML artifact와 exit code 검증
9. 불변성: 실행 전후 Scene·Resource·`project.godot` hash 동일
10. 제거: 별도 검토 변경으로 Plugin·config·workflow·consumer 제거 후 clean import

### BS-GATE-20260806-01 — 누락 방지 작업 진입 차단 Gate

작업 시작 전에 다음 surface를 live read한다.

- `00_프로젝트_허브`
- `01_작업순서`
- `02_현재_확정결정`
- `04_누락_충돌_감사`
- `71_이미지기획_생성목록`
- `72_이미지검수_승인로그`
- GitHub current main과 열린 PR exact HEAD

다음이면 작업을 시작하지 않는다.

- 승인 Decision이 GitHub 정본과 Sheet에 같은 ID로 존재하지 않음
- `READY`, `AWAITING`, `IN_REVIEW`, `APPROVED`가 필수 증거 없이 표시됨
- 이미지가 미생성인데 검수 진행 또는 승인으로 표시됨
- 권리·가독성·구현·런타임 검증이 `NOT_RUN`인데 제품 준비로 표시됨
- 표의 열 정렬이 깨져 상태 열을 신뢰할 수 없음
- GitHub main SHA와 Sheet current SHA가 불일치함
- 열린 Draft PR을 병합 완료 또는 다음 Task READY로 해석함

차단 상태:

```text
ENTRY_BLOCKED_CANON_SYNC
ENTRY_BLOCKED_OPEN_FINDING
ENTRY_BLOCKED_VISUAL_NOT_GENERATED
ENTRY_BLOCKED_VISUAL_REVIEW_INCOMPLETE
ENTRY_BLOCKED_SHEET_SCHEMA_DRIFT
ENTRY_BLOCKED_UNVERIFIED
```

## 4. 파일 소유권 Matrix

| Surface | HiGodot | GUT runtime/framework | CI/Validator |
|---|---|---|---|
| `**/*.tscn` | WRITE | READ/LOAD ONLY | DIFF/HASH/GATE |
| `**/*.tres`, `**/*.res` | WRITE | READ/LOAD ONLY | DIFF/HASH/GATE |
| `project.godot` | WRITE | READ ONLY | DIFF/HASH/GATE |
| Plugin·Autoload·InputMap | WRITE | READ/ASSERT ONLY | DIFF/GATE |
| 생산 GDScript | NO EXCLUSIVE AUTHORITY | READ/TEST | LINT/TEST |
| `tests/gut/**` | FORBIDDEN | TEST AUTHORING SURFACE | RUN/GATE |
| `.gutconfig.json` | FORBIDDEN | TEST CONFIG SURFACE | VALIDATE |
| `addons/gut/**` | FORBIDDEN | VENDOR SURFACE, RUNTIME READ ONLY | VERSION/LICENSE/HASH |
| JUnit·test artifacts | FORBIDDEN | GENERATE IN UNTRACKED OUTPUT | READ/PUBLISH |
| `.github/workflows/**` | NO RUNTIME WRITE | NO RUNTIME WRITE | REVIEWED CONFIG |

여러 권위 surface가 한 PR에 포함되면 파일별 authority manifest를 제출한다. 출처가 없는 변경은 `UNKNOWN_AUTHORITY / FAIL_CLOSED`다.

## 5. 실제 소비 경로

후속 정식 채택 PR에서 다음 경로를 고정한다.

```text
addons/gut/**
.gutconfig.json
res://tests/gut/unit/**
res://tests/gut/integration/**
res://addons/gut/gut_cmdln.gd
user://gut/**
untracked CI JUnit artifact
```

기존 custom GDScript runner를 즉시 삭제하지 않는다. 먼저 GUT framework smoke와 버티컬 슬라이스 대표 테스트를 RED→GREEN으로 추가하고, 동일 계약을 중복 실행하는 구형 runner는 검증 후 별도 PR에서 정리한다.

## 6. CI Gate

### 현재 설계 Draft

- `authority-entry-contract` 정적 job만 추가한다.
- 정책 JSON, 상태 snapshot, 명세 marker, 허용 변경 경계를 검증한다.
- GUT runtime을 실행하지 않는다.
- `addons/`, `scenes/`, `scripts/`, `data/`, `assets/`, `project.godot`을 변경하지 않는다.

### 후속 정식 채택

- Gate A: HiGodot authoring evidence와 파일별 authority manifest
- Gate B: GUT upstream pin·version·license·vendor inventory
- Gate C: Godot 4.7.1 Plugin load·CLI·테스트 수 1 이상
- Gate D: zero tests, skipped runner, missing test root, JUnit 없음은 FAIL
- Gate E: GUT 실행 전후 tracked authoring surface SHA-256 동일
- Gate F: 기존 Python·Godot 회귀와 GUT 결과를 모두 exact HEAD에 연결

## 7. Sheet 실제 상태와 교정

교정 완료:

- `00_프로젝트_허브!E2`: `R2_BATCH_006_MAIN_CANON_SCOPED_VERTICAL_SLICE_TASK1_DRAFT`
- `01_작업순서` R0·R1을 main canon 완료로 교정
- `01_작업순서` R2 완료와 R3~R8 미완료·일반 제품 차단을 분리
- `71_이미지기획_생성목록!A1:L6`: 열 정렬과 상태 열 readback 완료
- `BS-IMG-004!L`: `BLOCKED_IMAGE_NOT_GENERATED`
- `BS-IMG-005!G/J/K/L`: `NOT_DEFINED / SOURCE_AND_LICENSE_NOT_RECORDED / UNSET / BLOCKED_IMAGE_NOT_GENERATED`
- `72_이미지검수_승인로그!K2`: `BLOCKED_IMAGE_NOT_GENERATED`
- 방향 승인 행: `DIRECTION_ONLY_NOT_PRODUCT_READY`
- 에셋 거버넌스 행: `GOVERNANCE_APPROVED_EXECUTION_BLOCKED`

현재 판정:

- 이미지 목록의 행·열 구조 오류는 `SCHEMA_ALIGNMENT_REPAIRED_READBACK_PASS`다.
- 구조 복구는 이미지 제품 Gate 개방을 뜻하지 않는다.
- `BS-IMG-004`는 이미지 미생성 및 원출처·라이선스 검수가 남아 있다.
- `BS-IMG-005`는 이미지 미생성, 해상도 미정, 출처·라이선스 미기록, 우선순위 미정이 남아 있다.
- PR #122는 Draft·미병합이며 다음 버티컬 슬라이스 Task를 자동 개방하지 않는다.
- 제품 이미지 생성·권리·실기기 런타임은 `NOT_RUN`이다.

판정: `SHEET_SCHEMA_REPAIRED / VISUAL_AND_RIGHTS_GATES_BLOCKED`.

## 8. 제거 절차

`SEPARATE_REVIEWED_CHANGE_ONLY`로 수행한다.

1. GUT consumer·config·workflow·문서 참조를 검색한다.
2. 테스트를 대체 권위로 이관하거나 중단 Decision을 기록한다.
3. GUT Plugin 비활성화는 HiGodot으로 수행한다.
4. `.gutconfig.json`, GUT CI, `tests/gut/**`, `addons/gut/**`를 순서대로 제거한다.
5. 제3자 라이선스 원장과 dependency registry를 갱신한다.
6. clean import, parse, 기존 회귀, 제품 smoke를 실행한다.
7. 과거 JUnit·PR·RED/GREEN 증거는 보존한다.
8. 남은 consumer 0건을 기계 검증한다.

## 9. 비목표

- 이 Draft에서 GUT을 활성화하거나 정식 테스트 권위로 승격
- HiGodot을 Production Adapter로 승격
- PR #122 수정·병합
- 제품 Scene·Resource·Script·data·asset·`project.godot` 변경
- 이미지 생성 또는 제품 에셋 승인

판정: `NO_PRODUCT_PATH_CHANGE / DRAFT_REVIEW_REQUIRED / FORMAL_ADOPTION_BLOCKED`.
