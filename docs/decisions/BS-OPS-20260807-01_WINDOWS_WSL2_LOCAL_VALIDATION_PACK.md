# BS-OPS-20260807-01 — Windows + WSL2 로컬 검증팩

## 상태

```text
USER_APPROVED
DRAFT_PR_127
PENDING_EXACT_HEAD_LOCAL_EXECUTION
NOT_MAIN_CANON_UNTIL_MERGED
```

## 결정

GitHub Actions 예산이 소진된 기간의 code PR 검증은 다음 로컬 pack으로 실행 장소를 대체한다.

```text
Windows authoritative Python 3.12
+ Windows Python 3.11
+ Windows Python 3.12
+ Windows Python 3.13
+ WSL2 Ubuntu Python 3.12
```

Windows authoritative lane은 PR/base·Base 고정본 2종·BCA·Base v9·Project Base Adapter·Thin Adapter·Godot 4.7.1·GUT 9.7.1·JUnit·저작 surface 불변을 검증한다. 네 matrix lane은 기존 reusable Python code validation을 운영 감사 없이 재현한다.

## Fail-closed 조건

- 다섯 lane 모두 동일 exact HEAD
- authoritative lane과 네 matrix lane 모두 `PASS`
- Windows Python 3.11/3.12/3.13, WSL Ubuntu Python 3.12 정확 일치
- clean tracked worktree before/after
- authoring surface hash unchanged
- 누락·중복·다른 HEAD·실패 lane 없음
- 최종 aggregate Manifest `status: PASS`

하나라도 충족하지 못하면 `LOCAL_VALIDATION_PACK_FAILED`이며 Ready/merge 근거가 아니다.

## 범위

이 Decision은 검증 실행 장소와 증거 포맷만 바꾼다. 다음 상태는 변경하지 않는다.

```text
GENERAL_PRODUCT_IMPLEMENTATION_BLOCKED
VISUAL_AUDIO_GATE_BLOCKED
HIGODOT_PRODUCTION_ACTIVATION_PENDING
ANDROID_DEVICE_NOT_RUN
HUMAN_PLAYTEST_NOT_RUN
```

## 구현 위치

- `tools/run_local_validation_pack.ps1`
- `tools/run_wsl_python_lane.sh`
- `tools/run_local_python_matrix_lane.py`
- `tools/aggregate_local_validation_pack.py`
- `tools/local_validation_pack_contract.py`
- `tests/test_local_validation_pack.py`
- `docs/operations/GITHUB_ACTIONS_BUDGET_FALLBACK.md`

## 활성화 Gate

PR #127의 current exact HEAD에서 Windows+WSL2 pack Manifest가 `PASS`이고 pack SHA-256이 기록된 뒤 Ready/merge 검토를 수행한다. 병합 readback 전에는 main 정본 활성 상태로 표시하지 않는다.
