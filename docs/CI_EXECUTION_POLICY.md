# CI 실행 정책과 GitHub Actions 비용 최적화

## 현재 상태

- 상태: `ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED`
- PR 자동 검증을 활성화했다.
- `main` push와 nightly 전체 검증을 활성화했다.
- 문서 전용 변경과 코드 변경을 분리해 불필요한 Godot·Windows·Base 전체 회귀를 PR마다 반복하지 않는다.
- 실제 Workflow 결과가 나오기 전에는 PASS를 주장하지 않는다.

## 최적화된 실행 계층

### 문서 전용 PR

실행 범위:

- Ubuntu 1개
- Python 3.12
- 미해결 Git 충돌 검사
- 프로젝트 코어 정합성 검사
- 프로젝트와 pinned Base 참조 감사

실행하지 않는 항목:

- Godot 다운로드와 Scene 실행
- Windows
- Python 매트릭스
- LibreOffice, pnpm, Base 전체 회귀

### 코드·데이터·테스트·Workflow 변경 PR

실행 범위:

- Ubuntu Python 3.12 전체 프로젝트 계약
- Ubuntu Godot 4.7.1 import
- `res://scenes/main/main.tscn` smoke
- `res://scenes/test/equipment_lifecycle_poc.tscn` smoke
- 기존·신규 모델 및 통합 테스트
- `res://tests/integration/test_equipment_lifecycle_poc.gd` 전체 생애 E2E

실행하지 않는 항목:

- Windows
- Python 전체 매트릭스
- pinned Base 전체 publication/governance 회귀

### `main` 병합 또는 nightly

실행 범위:

- Ubuntu·Windows
- Python 3.11·3.12·3.13 전체 프로젝트 계약 매트릭스
- Ubuntu Godot 전체 suite 1회
- Ubuntu pinned Base 전체 governance suite 1회

무거운 Base 의존성 설치는 매트릭스마다 반복하지 않고 전용 Ubuntu job에서 한 번만 수행한다.

## Workflow 책임

- `.github/workflows/data-validation.yml`
  - `pull_request`와 수동 실행 진입점
  - PR 변경 유형 분류와 라우팅
- `.github/workflows/python-validation.yml`
  - 문서·코드 Python 검증 재사용 Workflow
  - 독립 `pull_request`·`push` 트리거 없음
- `.github/workflows/godot-validation.yml`
  - Godot 검증 재사용 Workflow
  - 독립 `pull_request`·`push` 트리거 없음
- `.github/workflows/full-validation.yml`
  - `main` push, nightly, 수동 전체 매트릭스 책임

## 동시 실행 취소 계약

상위 PR와 full Workflow는 다음 키를 사용한다.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

새 커밋이 들어오면 같은 상위 Workflow와 ref의 이전 실행을 취소한다.

재사용 Workflow는 호출자의 `github.workflow` 값을 상속하므로 상위 Workflow와 동일한 group을 쓰면 호출자를 취소할 수 있다. 따라서 고유 suffix를 붙인다.

```yaml
# Python reusable
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}-${{ inputs.runner }}-${{ inputs.python-version }}-${{ inputs.scope }}
  cancel-in-progress: true

# Godot reusable
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}-godot-reusable
  cancel-in-progress: true
```

## PR 자동 라우팅

`.github/workflows/data-validation.yml`은 다음 이벤트를 사용한다.

```yaml
on:
  pull_request:
  workflow_dispatch:
```

변경 유형 classifier가 문서 전용이면 Python 문서 validator만, 코드·데이터·테스트·Workflow 변경이면 Python 코드 계약과 Godot을 한 번씩 호출한다.

## main·nightly 전체 검증

`.github/workflows/full-validation.yml`은 다음 이벤트를 사용한다.

```yaml
on:
  workflow_dispatch:
  push:
    branches:
      - main
  schedule:
    - cron: "17 18 * * *"
```

`18:17 UTC`는 한국 표준시 기준 다음 날 `03:17`이다.

## 현재 검증 항목

1. PR 변경 파일 classifier의 실제 `pull_request` 이벤트 동작
2. 재사용 Python Workflow 호출과 job 이름
3. 재사용 Godot Workflow 호출
4. Godot 4.7.1 다운로드·import
5. `equipment_lifecycle_poc.tscn`과 `main.tscn` smoke
6. `test_equipment_lifecycle_poc.gd`와 기존 전체 회귀
7. 새 커밋 push 시 `cancel-in-progress` 실제 취소 동작
8. 재사용 Workflow가 상위 Workflow를 취소하지 않는지 확인
9. PR 병합 후 Ubuntu·Windows × Python 3.11·3.12·3.13 매트릭스
10. pinned Base LibreOffice·Node·pnpm 전체 회귀
11. Branch protection의 Required Check 이름과 강제 여부

## Required Check 정리

첫 자동 PR 실행에서 생성된 실제 check 이름을 기준으로 Branch protection을 갱신한다. 과거 독립 `Data validation`과 `Godot validation` check를 그대로 강제하면 재사용 구조와 충돌할 수 있다. Required Check 변경은 실제 실행 이름을 확인한 뒤 판정한다.

## 로컬에서 가능한 검증

```bash
python -m unittest tests/test_ci_workflow_structure.py
python -m unittest tests/test_no_merge_conflicts.py
python tests/check_no_merge_conflicts.py .
python tools/validate_game_data.py
python tools/validate_lifecycle_data.py
python -m unittest tests/test_lifecycle_data_contract.py
python tests/check_forging_quality_contract.py
python tests/check_enhancement_failure_contract.py
python -m unittest tests/test_enhancement_balance_simulator.py
python tests/check_enhancement_balance_simulator_contract.py
python tests/check_project_core_alignment.py
```

Godot 4.7.1 실행 파일이 있는 개발 환경에서는 다음 핵심 명령과 `.github/workflows/godot-validation.yml`의 전체 목록을 실행한다.

```bash
./godot --headless --editor --path . --quit
./godot --headless --path . res://scenes/main/main.tscn --quit-after 2
./godot --headless --path . res://scenes/test/equipment_lifecycle_poc.tscn --quit-after 2
./godot --headless --path . --script res://tests/integration/test_equipment_lifecycle_poc.gd
```

## 완료 판정 제한

- Workflow YAML과 정적 테스트 추가만으로 CI PASS를 선언하지 않는다.
- PR 최신 head의 Python·Godot·E2E가 모두 Green이 되기 전 PR을 Ready 또는 병합 완료로 표시하지 않는다.
- Windows, cancellation, Required Check는 실제 Actions 증거 전까지 `NOT_RUN` 또는 `UNVERIFIED`다.
- Android·접근성 사람 검토·성능·외부 플레이는 별도 검증 상태로 유지한다.
