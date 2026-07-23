# CI 실행 정책과 GitHub Actions 비용 게이트

## 현재 상태

- 상태: `DEFERRED_UNTIL_ACTIONS_AVAILABLE`
- 사유: 현재 월 GitHub Actions 사용 가능량이 부족하므로 자동 PR, `main` push, nightly 실행을 중지한다.
- 사용자 승인 문구: 사용자가 **GitHub Actions를 다시 사용할 수 있다**고 명시한 뒤에만 자동 트리거를 활성화한다.
- 이 상태에서는 Workflow 파일 구조와 정적 계약만 구현하며, GitHub-hosted runner 결과를 PASS 증거로 주장하지 않는다.

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
- Ubuntu Godot 4.7.1 import, Scene smoke, 모델·통합 테스트

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
  - PR 변경 유형 분류와 라우팅
  - 현재는 `workflow_dispatch`만 허용
- `.github/workflows/python-validation.yml`
  - 문서·코드 Python 검증 재사용 Workflow
  - 독립 `pull_request`·`push` 트리거 없음
- `.github/workflows/godot-validation.yml`
  - Godot 검증 재사용 Workflow
  - 독립 `pull_request`·`push` 트리거 없음
- `.github/workflows/full-validation.yml`
  - `main`/nightly 전체 매트릭스 책임
  - 현재는 `workflow_dispatch`만 허용

## 동시 실행 취소 계약

상위 PR와 full Workflow는 요청된 기본 키를 그대로 사용한다.

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

## Actions 사용 가능 후 활성화 절차

### 1. PR 자동 검증 활성화

`.github/workflows/data-validation.yml`의 이벤트를 다음과 같이 변경한다.

```yaml
on:
  pull_request:
  workflow_dispatch:
```

변경 유형 classifier가 문서 전용이면 Python 문서 validator만, 코드 변경이면 Python 코드 계약과 Godot만 호출한다.

### 2. `main`과 nightly 전체 검증 활성화

`.github/workflows/full-validation.yml`의 이벤트를 다음과 같이 변경한다.

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

### 3. 첫 활성화 실행에서 확인할 항목

다음은 GitHub-hosted runner가 필요하므로 현재 `DEFERRED_UNTIL_ACTIONS_AVAILABLE`이다.

1. PR 변경 파일 classifier의 실제 `pull_request` 이벤트 동작
2. 재사용 Python Workflow 호출과 job 이름
3. 재사용 Godot Workflow 호출
4. Ubuntu·Windows × Python 3.11·3.12·3.13 매트릭스
5. Godot 4.7.1 다운로드·import·Scene smoke·전체 테스트
6. pinned Base LibreOffice·Node·pnpm 전체 회귀
7. 새 커밋 push 시 `cancel-in-progress` 실제 취소 동작
8. 재사용 Workflow가 상위 Workflow를 취소하지 않는지 확인
9. Branch protection의 Required Check 이름과 강제 여부

### 4. Required Check 정리

첫 자동 PR 실행 후 실제 생성된 check 이름을 기준으로 Branch protection을 갱신한다. 과거 독립 `Data validation`과 `Godot validation` check를 그대로 강제하면 재사용 구조와 충돌할 수 있다. Required Check 변경은 실제 실행 이름을 확인하기 전까지 `NOT_RUN`이다.

## 로컬에서 가능한 검증

Actions 사용량과 무관하게 다음 검증은 개발 환경에서 직접 실행할 수 있다.

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

Godot 4.7.1 실행 파일이 있는 개발 환경에서는 `.github/workflows/godot-validation.yml`에 열거된 Scene과 테스트를 같은 순서로 실행한다.

## 완료 판정 제한

다음 조건을 지킨다.

- Workflow YAML과 정적 테스트 추가만으로 CI PASS를 선언하지 않는다.
- Windows, GitHub event routing, cancellation, Required Check는 실제 Actions 증거 전까지 `NOT_RUN`이다.
- 현재 장비 생애 PoC 구현 PR은 Draft를 유지한다.
- 사용자가 Actions 사용 가능 상태를 알리면 이 문서의 활성화 절차부터 수행하고, 대기 검증을 실행한 뒤 구현 완료 여부를 다시 판정한다.
