# GitHub Actions 예산 소진 시 로컬 exact-HEAD 검증

## 목적

GitHub-hosted Actions를 실행할 수 없을 때 검증 장소만 로컬로 바꾼다. v4.3의 TDD, exact HEAD, GUT 9.7.1, Godot 4.7.1, 저작 surface 불변, 리뷰·병합 Gate는 생략하지 않는다.

운영 Decision: `BS-OPS-20260807-01`

## 권장 검증팩

`WINDOWS_WSL2_LOCAL_VALIDATION_PACK`

| Lane | 실행 환경 | 책임 |
|---|---|---|
| `windows-authoritative-py312` | Windows Python 3.12 | PR/base·Base 2종·BCA·Base v9·Adapter·Godot 4.7.1·GUT/JUnit 전체 Gate |
| `windows-py311` | Windows Python 3.11 | reusable Python code validation |
| `windows-py312` | Windows Python 3.12 | reusable Python code validation |
| `windows-py313` | Windows Python 3.13 | reusable Python code validation |
| `wsl-ubuntu-py312` | WSL2 Ubuntu Python 3.12 | Ubuntu reusable Python code validation |

최종 pack은 authoritative lane과 네 matrix lane이 모두 같은 exact HEAD에서 `PASS`여야 `PASS`다. 누락·중복·예기치 않은 lane·실패·다른 HEAD·잘못된 Python/platform·tracked mutation은 모두 `FAIL`이다. 각 matrix runner는 전달받은 platform 문자열뿐 아니라 실제 Windows 또는 WSL2 Ubuntu 환경을 감지한다.

## 병합용 PASS 조건

- 검증 시작·종료 시 tracked working tree가 clean
- 모든 lane의 `HEAD == expected HEAD`
- 실제 PR base가 authoritative lane의 `--pr-base-sha`와 일치
- Windows Python 3.11/3.12/3.13과 WSL2 Ubuntu Python 3.12
- 모든 Python 환경의 pytest 8.3.5
- Base 운영 감사 checkout `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- Project Base Adapter validator checkout `bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1`
- PR validation, BCA, Base v9, Project Base Adapter, Thin Adapter 성공
- Godot 4.7.1 import·Scene smoke·모델 suite·GUT/JUnit 성공
- 실행 전후 `project.godot`, Scene, Resource, `addons/godot_ai/**` hash 불변
- authoritative Manifest가 실제 Windows·Base pin 2종·protected baseline·Godot 증거를 포함
- `windows-wsl2-validation-pack.json`의 최종 `status == PASS`

하나라도 빠지면 병합 증거가 아니다.

## Base 검증 worktree 준비

기존 Base working tree를 checkout으로 바꾸지 않는다. 별도 detached worktree를 사용한다.

```powershell
Set-Location "C:/Users/user/Documents/GitHub/Base"
git fetch --prune origin
$BaseOperating = "$env:TEMP/blacksmith-base-41a20584"
$BaseContract = "$env:TEMP/blacksmith-base-bfdc9e44"
git worktree add --detach $BaseOperating 41a20584dd2ee51d917e5c9d7cab6838e1ceba7e
git worktree add --detach $BaseContract bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1
```

이미 같은 경로의 worktree가 있으면 새로 만들지 말고 각각의 `git rev-parse HEAD`가 위 SHA와 정확히 같은지 확인한다.

## Windows + WSL2 실행

검증 대상은 PR의 exact HEAD를 checkout한 clean worktree여야 한다.

```powershell
$Repo = "C:/Users/user/Documents/GitHub/Ninza/Blacksmith"
$ExpectedHead = (git -C $Repo rev-parse HEAD).Trim()
$PrBase = "<GitHub PR의 현재 base SHA>"
$Godot = "<Godot 4.7.1 executable 절대 경로>"

& "$Repo/tools/run_local_validation_pack.ps1" `
  -RepoRoot $Repo `
  -ExpectedHead $ExpectedHead `
  -PrBaseSha $PrBase `
  -BaseOperatingRoot $BaseOperating `
  -BaseContractRoot $BaseContract `
  -Godot $Godot `
  -WslDistribution "Ubuntu"
```

`-WslDistribution`은 실제 `wsl.exe -l -q`에 표시되는 Ubuntu 배포판 이름으로 바꾼다. 기본 배포판을 쓸 경우 생략할 수 있다.

스크립트는 Windows Python 3종과 WSL Python 3.12용 격리 venv를 임시 출력 폴더에 만들고 pytest 8.3.5를 설치한다. WSL에는 `python3.12-venv`가 필요하다.

## 산출물

기본 출력 위치:

```text
%TEMP%/blacksmith-windows-wsl2-<HEAD12>/
```

필수 Manifest:

```text
windows-authoritative-py312.json
windows-py311.json
windows-py312.json
windows-py313.json
wsl-ubuntu-py312.json
windows-wsl2-validation-pack.json
```

최종 파일의 SHA-256을 PR 설명 또는 댓글에 기록한다. lane Manifest와 로그는 같은 출력 폴더에 보존한다.

## 단일 runner

`tools/run_local_validation_v2.py`는 authoritative Windows 3.12 lane의 구현이며 단독 진단에도 사용할 수 있다. 그러나 `BS-OPS-20260807-01` 적용 이후 code PR의 Actions 대체 병합 증거는 전체 Windows+WSL2 pack이다.

문서-only PR은 별도 범위 판정이 가능하지만 tests, tools, data, workflow, production 경로가 하나라도 바뀌면 `code`다.

## Actions 미실행 커밋

예산 소진 기간에는 커밋 메시지에 `[skip ci]` 또는 `skip-checks:true`를 사용한다. 이는 검증 생략이 아니라 로컬 PASS Manifest로 실행 장소를 대체하는 것이다. branch protection 또는 Required Check가 활성화되면 우회하지 않고 병합을 차단한다.

## PR 증거

```text
validation_mode: WINDOWS_WSL2_LOCAL_VALIDATION_PACK
decision_id: BS-OPS-20260807-01
exact_head: <40-char SHA>
pr_base_sha: <40-char SHA>
pack_status: PASS
pack_sha256: <SHA256>
windows_python: 3.11 / 3.12 / 3.13
wsl_ubuntu_python: 3.12
base_operating_pin: 41a20584dd2ee51d917e5c9d7cab6838e1ceba7e
base_contract_pin: bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1
godot: 4.7.1
GUT: 9.7.1
tracked_authoring_surface_hash: UNCHANGED
GitHub Actions: NOT_RUN_BUDGET_EXHAUSTED
Windows/Android device: NOT_RUN 또는 별도 증거
```

Manifest가 검토 HEAD/base와 다르거나 HEAD가 바뀌면 즉시 무효다.
