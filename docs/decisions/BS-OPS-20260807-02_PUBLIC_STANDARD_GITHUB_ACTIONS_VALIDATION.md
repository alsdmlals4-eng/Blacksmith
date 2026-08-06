# BS-OPS-20260807-02 — Public 표준 GitHub Actions 검증

## 상태

```text
USER_APPROVED
MAIN_CANON_ACTIVE
MERGED_PR_128
MAIN_SHA_AT_ACTIVATION_24fda421020bdf5b8f38cf09df6b3764c72cb1d9
PREMERGE_FULL_VALIDATION_102_PASS
POSTMERGE_FULL_VALIDATION_103_PASS
SUPERSEDES_BS_OPS_20260807_01
```

## 결정

Blacksmith의 공식 자동 검증 실행 장소는 public 저장소에서 제공되는 GitHub 표준 hosted runner로 복원한다.

```text
ubuntu-latest
windows-latest
```

현재 저장소의 `Full validation`, reusable Python validation, Godot validation, GUT validation을 재사용한다. 별도 Windows+WSL2 로컬 exact-HEAD pack은 공식 경로로 채택하지 않는다.

## 근거

- `alsdmlals4-eng/Blacksmith`는 public 저장소다.
- GitHub 공식 과금 정책상 public 저장소의 표준 GitHub-hosted runner 사용은 무료다.
- larger runner는 public 저장소에서도 유료이므로 사용하지 않는다.
- `full-validation.yml`은 이미 `workflow_dispatch`, Ubuntu·Windows, Python 3.11·3.12·3.13, Godot 전체 검증을 제공한다.
- 로컬 pack은 환경 준비와 증거 수집이 복잡해 운영 비용이 커졌으며, 기존 Actions와 기능이 중복된다.

## 공식 실행 경로

### Pull Request

PR 이벤트에 연결된 기존 validation router와 reusable workflow를 사용한다.

### 전체 수동 검증

GitHub의 Actions 화면에서 `Full validation`을 선택하고 검증할 branch를 지정해 `Run workflow`를 실행한다.

### main 검증

`main` push와 기존 schedule에 연결된 `Full validation`을 유지한다.

## 비용 안전장치

- 허용 runner: `ubuntu-latest`, `windows-latest`
- larger runner 사용 금지
- self-hosted runner는 별도 Decision 없이 도입 금지
- Actions artifact 보존기간: 1일
- 중복 실행은 `cancel-in-progress: true` 유지
- 실패 로그는 GitHub 로그를 우선 사용하고 artifact는 필요한 증거만 업로드

## 대체되는 결정

`BS-OPS-20260807-01`의 Windows+WSL2 로컬 검증팩은 다음 상태로 종료한다.

```text
SUPERSEDED
PR_127_CLOSED_WITHOUT_MERGE
HISTORICAL_EXPERIMENT_ONLY
NOT_MAIN_CANON
```

PR #127의 branch와 실패 manifest는 역사적 디버깅 증거로만 남기며 main에 병합하지 않는다.

## 검증 Gate

실행 장소만 단순화한다. 다음 Gate는 생략하거나 통합하지 않는다.

```text
EXACT_HEAD_VALIDATION_REQUIRED
BASE_PIN_VALIDATION_REQUIRED
GODOT_4_7_1_REQUIRED
GUT_9_7_1_REQUIRED
AUTHORING_SURFACE_READ_ONLY_PROOF_REQUIRED
PRODUCT_VISUAL_AUDIO_GATES_UNCHANGED
ANDROID_DEVICE_NOT_RUN
HUMAN_PLAYTEST_NOT_RUN
```

## 구현 위치

- `.github/workflows/full-validation.yml`
- `.github/workflows/python-validation.yml`
- `.github/workflows/godot-validation.yml`
- `.github/workflows/gut-validation.yml`
- `docs/operations/GITHUB_ACTIONS_PUBLIC_STANDARD_RUNNER_POLICY.md`

## 활성화 증거

### PR #128 exact-head

- exact head: `05d0e897925d93bf6c082daf8c567f5b5844d987`
- automatic PR workflows: 6/6 PASS
- Full validation #102: run `31131847266`, 8/8 jobs PASS
- comments: 0
- reviews: 0
- unresolved review threads: 0
- changed files: 7
- product authoring paths changed: 0

### main readback

- squash merge: PR #128
- activation main SHA: `24fda421020bdf5b8f38cf09df6b3764c72cb1d9`
- postmerge Full validation #103: run `31132114629`, 8/8 jobs PASS
- Sheet Decision `BS-OPS-20260807-02`: `MAIN_CANON_ACTIVE`
- `00_프로젝트_허브`: current main·GUT active·PR #128 merged 상태로 교정 완료

## 활성 상태

활성화 Gate는 충족됐다.

```text
MAIN_CANON_ACTIVE
PUBLIC_STANDARD_RUNNERS_ONLY
ARTIFACT_RETENTION_1_DAY
PR_127_SUPERSEDED
PRODUCT_VISUAL_AUDIO_GATES_UNCHANGED
ANDROID_DEVICE_NOT_RUN
HUMAN_PLAYTEST_NOT_RUN
```

Base main `4f98f968a377f7b6a11aafa4fc94d11bddbebedc`가 현재 project operating/contract pin보다 최신인 상태는 별도 Base adoption Decision까지 `DEFERRED`다.
