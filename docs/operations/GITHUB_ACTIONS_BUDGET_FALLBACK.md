# GitHub Actions 예산 소진 시 로컬 exact-HEAD 검증

## 목적

GitHub-hosted Actions를 실행할 수 없을 때 검증 장소만 로컬로 바꾼다. v4.3의 TDD, exact HEAD, GUT 9.7.1, Godot 4.7.1, 저작 surface 불변, 리뷰·병합 Gate는 생략하지 않는다.

## 병합용 PASS 조건

- 검증 시작·종료 시 tracked working tree가 clean
- `HEAD == --expected-head`
- 프로젝트가 고정한 Base checkout을 `--base-root`로 제공
- Godot 4.7.1 executable을 `--godot`으로 제공
- `--require-godot` 사용
- Python 계약, Base 운영 감사, Godot import·Scene smoke·기존 모델 suite, GUT 9.7.1, JUnit이 모두 성공
- GUT 실행 전후 `project.godot`, Scene, Resource, `addons/godot_ai/**` hash 불변
- manifest의 최종 `status == PASS`

Godot 또는 Base가 빠지면 `PARTIAL`이며 병합 증거가 아니다.

## Windows PowerShell 실행

```powershell
Set-Location "C:/Users/user/Documents/GitHub/Ninza/Blacksmith"
git status --short --branch
$Head = (git rev-parse HEAD).Trim()
$Godot = "<Godot 4.7.1 executable 절대 경로>"
$Base = "C:/Users/user/Documents/GitHub/Base"
$Output = "$env:TEMP/blacksmith-local-validation-$($Head.Substring(0,12)).json"

python tools/run_local_validation.py `
  --repo-root . `
  --base-root $Base `
  --godot $Godot `
  --require-godot `
  --scope code `
  --expected-head $Head `
  --output $Output

Get-Content $Output
Get-FileHash $Output -Algorithm SHA256
git status --short --branch
```

## Actions 미실행 커밋

예산 소진 기간에는 검증 완료 뒤 마지막 커밋 메시지에 `[skip ci]` 또는 `skip-checks:true`를 사용한다. 이는 테스트 생략이 아니라 위 로컬 PASS Manifest로 실행 장소를 대체하는 것이다. branch protection 또는 Required Check가 활성화되면 우회하지 않고 병합을 차단한다.

## PR 증거

PR 설명 또는 댓글에 다음을 기록한다.

```text
validation_mode: LOCAL_EXACT_HEAD_NO_GITHUB_ACTIONS
exact_head: <40-char SHA>
manifest_status: PASS
manifest_sha256: <SHA256>
base_root_pin: 41a20584dd2ee51d917e5c9d7cab6838e1ceba7e
godot: 4.7.1
GUT: 9.7.1
tracked_authoring_surface_hash: UNCHANGED
GitHub Actions: NOT_RUN_BUDGET_EXHAUSTED
Windows/Android device: NOT_RUN 또는 별도 증거
```

Manifest가 검토 HEAD와 다르거나 HEAD가 바뀌면 즉시 무효다.
