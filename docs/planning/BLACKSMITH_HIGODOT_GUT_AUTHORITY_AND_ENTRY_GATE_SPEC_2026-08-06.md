# Blacksmith HiGodot·GUT 저작/검증 권위 및 작업 진입 Gate 명세

```yaml
spec_id: BS-TEST-AUTH-20260806-01
status: DRAFT_REVIEW_REQUIRED
base_sha: 07f77041f85bde223768128949ad8dc587d5a003
product_implementation: BLOCKED
higodot_adoption: SPECIFIED_NOT_ENABLED
Gut_adoption: SPECIFIED_NOT_YET_CI_AUTHORITY
```

## 1. 목적

HiGodot과 GUT가 같은 Godot 파일을 임의로 수정하거나 서로의 역할을 침범하지 않도록 권위를 분리한다. 또한 결정 원장·미확정 목록·이미지 검수 상태가 실제 증거와 맞지 않으면 작업 진입을 차단한다.

## 2. 승인 Decision

### BS-OPS-20260806-10 — HiGodot/GUT 권위 분리

- HiGodot은 Godot Scene, Node, Resource, project.godot 및 프로젝트 설정을 실제로 편집하는 단일 저작 권위다.
- GUT는 저작 결과를 읽고 실행하여 검증하는 테스트 권위다.
- GUT 테스트·fixture·runner 설정은 테스트 surface에 한해 수정할 수 있지만 제품 Scene·Resource·project.godot을 자동 수정할 수 없다.
- HiGodot은 테스트 통과 여부를 위조하거나 GUT 결과 파일을 직접 성공 상태로 변경할 수 없다.

### BS-TEST-20260806-01 — GUT 9.7.1 정식 테스트 프레임워크 채택 전제

현재 저장소의 `addons/gut/plugin.cfg`는 GUT `9.7.1`을 선언한다. upstream GUT 문서는 9.7.1/godot_4_7 branch를 Godot 4.7.x용으로 분류하고 MIT 라이선스를 명시한다.

정식 채택은 다음 증거가 모두 준비된 뒤에만 `ACTIVE_TEST_AUTHORITY`로 승격한다.

1. 출처: `bitwes/Gut`, 정확한 tag/branch/commit 및 취득 방식
2. 버전: `addons/gut/plugin.cfg == 9.7.1`
3. 라이선스: `addons/gut/LICENSE.md` 존재, 배포 고지·제3자 라이선스 원장 연결
4. 호환성: Godot 4.7.1에서 plugin load, CLI, 최소 smoke test 실제 PASS
5. 실제 소비 경로: 테스트 디렉터리, runner 명령, project plugin 설정, JUnit 출력 경로
6. CI: exact HEAD에서 GUT job 실행, 테스트 0건·job skip·runner 미실행을 FAIL 처리
7. 제거 절차: plugin 비활성화, addon 제거, runner/workflow/config/reference 제거, clean import 검증

현재 상태는 `VENDORED_PRESENT / FORMAL_ADOPTION_PENDING`이다. 단순 보관을 정식 채택으로 오표기하지 않는다.

### BS-GATE-20260806-01 — 누락 방지 작업 진입 차단 Gate

작업 시작 전에 다음 세 surface를 live read하고 판정한다.

- 결정 원장: `02_현재_확정결정`
- 미확정·충돌 목록: `04_누락_충돌_감사`
- 이미지 검수: `71_이미지기획_생성목록`, `72_이미지검수_승인로그`

다음이면 작업을 시작하지 않는다.

- 승인 Decision이 GitHub 정본과 Sheet에 같은 ID로 존재하지 않음
- `READY`, `AWAITING`, `IN_REVIEW`, `APPROVED`가 필수 증거 없이 표시됨
- 이미지가 미생성인데 검수 진행 또는 승인으로 표시됨
- 권리·유사성, 실제 화면 가독성, 구현 가능성, 런타임 검증 중 필수 항목이 `NOT_RUN`인데 제품 준비 상태로 표시됨
- 표의 열 정렬이 깨져 상태 열을 신뢰할 수 없음
- GitHub main SHA와 Sheet current SHA가 불일치함

차단 상태:

```text
ENTRY_BLOCKED_CANON_SYNC
ENTRY_BLOCKED_OPEN_FINDING
ENTRY_BLOCKED_VISUAL_NOT_GENERATED
ENTRY_BLOCKED_VISUAL_REVIEW_INCOMPLETE
ENTRY_BLOCKED_SHEET_SCHEMA_DRIFT
ENTRY_BLOCKED_UNVERIFIED
```

## 3. 파일 소유권 Matrix

| Surface | HiGodot | GUT | CI/Validator |
|---|---|---|---|
| `scenes/**/*.tscn` | WRITE | READ/LOAD ONLY | DIFF/GATE |
| `resources/**/*` | WRITE | READ/LOAD ONLY | DIFF/GATE |
| `project.godot` | WRITE | READ ONLY | DIFF/GATE |
| Godot project settings/InputMap/autoload | WRITE | READ/ASSERT ONLY | DIFF/GATE |
| `tests/**/*.gd` | NO PRODUCT AUTHORING | WRITE | RUN/GATE |
| `addons/gut/**` | NO RUNTIME CONTENT AUTHORING | FRAMEWORK VENDOR SURFACE | VERSION/LICENSE HASH GATE |
| `.github/workflows/**` | NO | NO | WRITE/EXECUTE |
| test result/JUnit artifacts | NO | GENERATE | READ/PUBLISH |

## 4. CI Gate 설계

### Gate A — authority boundary

- 제품 Scene/Resource/project.godot 변경 PR에는 HiGodot authoring evidence ID가 필요하다.
- GUT 또는 test-only PR이 제품 저작 surface를 변경하면 FAIL한다.
- HiGodot 작업이 `tests/**`, GUT 결과, JUnit 파일을 성공 상태로 직접 수정하면 FAIL한다.

### Gate B — GUT adoption integrity

- plugin version, license, upstream pin, Godot compatibility evidence를 검사한다.
- GUT runner 명령이 실제 실행되고 테스트 수가 1 이상인지 검사한다.
- exit code 0이어도 테스트 0건, parse skip, missing test dir이면 FAIL한다.

### Gate C — work entry state

- GitHub 정본과 Sheet snapshot을 비교한다.
- 잘못된 `READY/AWAITING/IN_REVIEW/APPROVED`를 발견하면 validator가 non-zero로 종료한다.
- 이미지는 `GENERATED` 이전에 `IN_REVIEW`, 권리/런타임 미검증 상태에서 `APPROVED/READY`가 될 수 없다.

## 5. 이미지 상태 정상화 규칙

허용 흐름:

```text
PLANNED
→ BRIEF_READY
→ GENERATED_DRAFT
→ REVIEW_AWAITING
→ REVIEW_IN_PROGRESS
→ REVIEW_CHANGES_REQUIRED | REVIEW_PASSED
→ RIGHTS_VERIFIED
→ GODOT_IMPORTED
→ RUNTIME_VALIDATED
→ APPROVED_PRODUCTION_ASSET
```

`이미지 미생성` 행은 `IN_REVIEW`가 아니라 `BLOCKED_NOT_GENERATED`로 되돌린다. 방향 승인과 제품 에셋 승인은 별도다.

## 6. 도입·제거 절차

### 도입

1. upstream source/tag/commit과 SHA 기록
2. license ledger 반영
3. addon 파일 inventory/hash 생성
4. Godot 4.7.1 clean import와 plugin load
5. 최소 GUT smoke test RED→GREEN
6. 프로젝트 테스트 디렉터리·runner·JUnit 경로 고정
7. exact-HEAD CI required gate 등록
8. 제거 dry-run 문서 검증

### 제거

1. GUT plugin 비활성화
2. GUT runner/workflow/config 참조 제거
3. `addons/gut` 제거
4. 대체 테스트 권위 또는 테스트 중단 Decision 기록
5. clean import, parse, 기존 제품 smoke test
6. license ledger와 dependency registry 갱신

## 7. 현재 Sheet readback finding

- `72_이미지검수_승인로그`의 `BS-REV-INIT`은 이미지 미생성인데 `IN_REVIEW`다. `BLOCKED_NOT_GENERATED`로 rollback 대상이다.
- 아트·모닥 행은 방향 승인만 존재하며 제품 화면·권리·런타임 검증은 `NOT_RUN`이다. 제품 `READY/APPROVED`로 승격할 수 없다.
- `71_이미지기획_생성목록`의 일부 행은 헤더와 값 위치가 어긋나 있어 `ENTRY_BLOCKED_SHEET_SCHEMA_DRIFT` 대상이다.

## 8. 검토 완료 조건

- Decision 3건이 GitHub 정본과 Sheet에 동일 ID로 존재
- Sheet 오판정 rollback readback PASS
- GUT source/version/license/compatibility/consumer/CI/removal 증거 연결
- authority boundary validator와 CI job 설계 검토 승인
- Draft PR exact HEAD 검토 완료
- 이 단계에서는 제품 Scene·Resource·project.godot 변경 없음
