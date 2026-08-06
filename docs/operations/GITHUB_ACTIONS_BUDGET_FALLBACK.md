# GitHub Actions 예산 소진 시 로컬 exact-HEAD 검증

## 목적

GitHub-hosted Actions를 실행할 수 없을 때 검증 장소만 로컬로 바꾼다. v4.3의 TDD, exact HEAD, GUT 9.7.1, Godot 4.7.1, 저작 surface 불변, 리뷰·병합 Gate는 생략하지 않는다.

## 병합용 PASS 조건

- 검증 시작·종료 시 tracked working tree가 clean
- `HEAD == --expected-head`, 실제 PR base가 `--pr-base-sha`와 일치
- Python 3.12.x와 pytest 8.3.5
- Base 운영 감사 checkout `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- Project Base Adapter validator checkout `bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1`
- PR validation, BCA, Base v9, Project Base Adapter, Thin Adapter 명령 성공
- code scope는 Godot 4.7.1 import·Scene smoke·모델 suite·GUT/JUnit 성공
- 실행 전후 `project.godot`, Scene, Resource, `addons/godot_ai/**` hash 불변
- manifest 최종 `status == PASS`

필수 Base checkout이나 code scope의 Godot가 빠지면 `PARTIAL`이며 병합 증거가 아니다.

## Base 검증 worktree 준비

기존 Base working tree를 checkout으로 바꾸지 않는다. 별도 detached worktree를 사용한다.

```powershell
Set-Location "C:/Users/user/Documents/GitHub/Base"
git fetch --prune origin
$BaseOperating = "$env:TEMP/blacksmith-base-41a20584"
$BaseContract = "$env:TEMP/blacksmith-base-bfdc9e44"
git worktree add --detach $BaseOperating 41a20584dd2ee51d917e5c9d7cab6838e1ceba7e
git worktree add --detach $BaseContract bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1
python -m pip install pytest==8.3.5
python -m pip install -r "$BaseContract/.github/validation-requirements.txt"
```

## Windows PowerShell 실행

```powershell
Set-Location "C:/Users/user/Documents/GitHub/Ninza/Blacksmith"
git status --short --branch
$Head = (git rev-parse HEAD).Trim()
$PrBase = "<GitHub PR의 현재 base SHA>"
$Godot = "<Godot 4.7.1 executable 절대 경로>"
$Output = "$env:TEMP/blacksmith-local-validation-$($Head.Substring(0,12)).json"

python tools/run_local_validation_v2.py `
  --repo-root . `
  --pr-base-sha $PrBase `
  --base-root $BaseOperating `
  --base-contract-root $BaseContract `
  --godot $Godot `
  --require-godot `
  --scope code `
  --expected-head $Head `
  --output $Output

Get-Content $Output
Get-FileHash $Output -Algorithm SHA256
git status --short --branch
```

문서-only PR은 `--scope docs`를 사용하며 Godot를 생략할 수 있다. tests, tools, data, workflow, production 경로가 하나라도 바뀌면 `code`다.

## Actions 미실행 커밋

예산 소진 기간에는 마지막 커밋 메시지에 `[skip ci]` 또는 `skip-checks:true`를 사용한다. 이는 검증 생략이 아니라 위 로컬 PASS Manifest로 실행 장소를 대체하는 것이다. branch protection 또는 Required Check가 활성화되면 우회하지 않고 병합을 차단한다.

## PR 증거

```text
validation_mode: LOCAL_EXACT_HEAD_NO_GITHUB_ACTIONS
exact_head: <40-char SHA>
pr_base_sha: <40-char SHA>
manifest_status: PASS
manifest_sha256: <SHA256>
base_operating_pin: 41a20584dd2ee51d917e5c9d7cab6838e1ceba7e
base_contract_pin: bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1
python: 3.12.x
godot: 4.7.1
GUT: 9.7.1
tracked_authoring_surface_hash: UNCHANGED
GitHub Actions: NOT_RUN_BUDGET_EXHAUSTED
Windows/Android device: NOT_RUN 또는 별도 증거
```

Manifest가 검토 HEAD/base와 다르거나 HEAD가 바뀌면 즉시 무효다.
