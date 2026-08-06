# HiGodot·GUT 9.7.1 권위 분리 및 필수 진입 게이트 설계

> 상태: `DESIGN_REVIEW_REQUIRED / GUT_9_7_1_DESIGN_ONLY / NO_PRODUCT_PATH_CHANGE`
>
> Decision ID: `BS-OPS-20260806-10`

## 목표

Godot 프로젝트 저작과 테스트의 책임을 파일 단위로 분리하고, 정본·미확정·이미지 상태를 실제로 읽지 않은 작업이 구현 단계에 진입하지 못하도록 한다.

- `HIGODOT_SOLE_AUTHORING_AUTHORITY`: HiGodot은 Scene·Node·Resource·Godot 프로젝트 설정의 단일 저작 권위다.
- `GUT_SOLE_TEST_AUTHORITY`: GUT은 GDScript 단위·통합 테스트의 정식 테스트 프레임워크 권위다.
- `ENTRY_GATE_FAIL_CLOSED`: 필수 근거가 없거나 낡았으면 작업을 차단한다.

현재 저장소의 Live-Editor는 임시 복사본의 scratch Scene만 수정하는 Pilot이다. 따라서 현재 상태는 `PILOT_ONLY_NOT_PRODUCTION_AUTHORING_AUTHORITY`이며, 이 설계 PR 병합만으로 실프로젝트 수정 권한이 생기지 않는다.

## 검토한 현재 상태

- `main`: `07f77041f85bde223768128949ad8dc587d5a003`
- 일반 제품 구현: `BLOCKED`
- 승인된 예외: 버티컬 슬라이스 전용 namespace만 개방
- PR #122: Draft·미병합, head `f4568468c2c04f29ea1472e2ac12329447f1a365`
- HiGodot/Live-Editor: Pilot-only, Production Adapter `NOT_READY`
- 제품 이미지: 방향만 승인, 이미지 생성·최종 화면·권리·런타임 검증 `NOT_RUN`

## 권위 모델

### HiGodot 저작 권위

HiGodot만 다음 변경을 생성·저장할 수 있다.

- `project.godot`의 프로젝트 설정, Plugin, Autoload, 시작 Scene
- `.tscn` Scene과 Node graph
- `.tres`·`.res` Resource
- 위 파일의 Godot Editor 직렬화 결과

일반 코드 편집기는 GDScript 생산 코드와 문서 작업을 계속 담당할 수 있지만, 위 Godot 저작 surface를 텍스트 치환으로 우회하지 않는다. HiGodot은 `tests/gut/**`, `.gutconfig.json`, `addons/gut/**`를 수정하지 않는다.

### GUT 테스트 권위

GUT 9.7.1을 Godot 4.7.x용 정식 GDScript 테스트 프레임워크로 채택하는 목표를 둔다. 그러나 이 PR에서는 설치하지 않는다.

고정 근거:

- 공식 저장소: `bitwes/Gut`
- 버전·태그: `9.7.1 / v9.7.1`
- 태그 commit: `aeb5d4f3f7f0a6c9b5e178876d6c99b791fda605`
- 라이선스: MIT, upstream `addons/gut/LICENSE.md`
- 공식 호환 범위: Godot 4.7.x

후속 설치 PR의 실제 소비 경로:

```text
addons/gut/**
.gutconfig.json
res://tests/gut/unit/**
res://tests/gut/integration/**
res://addons/gut/gut_cmdln.gd
JUnit XML CI artifact
```

GUT 런타임은 테스트 대상 파일을 읽기만 하며 `user://gut/**`와 CI의 비추적 artifact 외에는 쓰지 않는다. `GUT_RUNTIME_TRACKED_MUTATION_FORBIDDEN`을 위반하면 테스트 성공 여부와 무관하게 CI를 실패시킨다.

## 충돌 방지

1. 같은 추적 파일에 HiGodot과 GUT의 이중 권위를 선언하지 않는다.
2. Scene·Resource·프로젝트 설정 diff에는 HiGodot 저작 증거가 필요하다.
3. GUT vendor bytes·config·tests에는 GUT 채택/테스트 책임만 기록한다.
4. GUT 실행 전후에 저작 surface SHA-256을 비교한다.
5. 출처가 없는 변경은 `UNKNOWN_AUTHORITY / FAIL_CLOSED`다.
6. 채택 PR에서 여러 권위 surface가 함께 바뀌면 파일별 authority manifest를 필수로 둔다.

## CI 설계

현재 설계 PR:

- `authority-entry-contract`: 정책 JSON, 상태 snapshot, 문서 marker, 변경 경계만 검증
- GUT 설치·실행 없음
- `addons/`, `scenes/`, `scripts/`, `data/`, `assets/`, `project.godot` 변경 금지

후속 채택 PR:

- upstream tag·commit·license·vendor manifest 검증
- Godot 4.7.1 headless에서 `gut-runtime-read-only` 실행
- JUnit XML 보관
- 저작 surface 실행 전후 hash 동일성 검증
- 기존 custom runner는 즉시 삭제하지 않고, GUT smoke와 대표 버티컬 슬라이스 테스트를 먼저 이관한 뒤 중복 제거

## 필수 진입 게이트

작업 시작 전에 다음을 현재 HEAD와 Sheet 실데이터로 읽는다.

1. 결정 원장 `02_현재_확정결정`
2. 누락·충돌 감사 `04_누락_충돌_감사`
3. 이미지 검수 `72_이미지검수_승인로그`
4. 프로젝트 허브·작업순서의 현재 단계
5. 열린 PR의 Draft/merge/head 상태

`READY`나 `AWAITING` 같은 일반 문자열은 근거가 아니며 허용 aggregate state에서 제외한다. 현재 복원 결과는 다음과 같다.

- R0/R1/R2 작업순서 표식 일부는 stale이므로 현재 진입 판단에 사용 금지
- PR #122는 Green 테스트가 있어도 Draft·미병합
- 제품 이미지 Gate는 `BLOCKED_NOT_PRODUCT_READY`
- GUT 설치는 `BLOCKED_DESIGN_REVIEW_REQUIRED`
- 일반 제품 구현은 계속 `BLOCKED`

## 제거 절차

`REMOVAL_BY_SEPARATE_REVIEWED_CHANGE`로만 제거한다.

1. GUT 소비자와 CI job을 검색한다.
2. 테스트를 이관하거나 폐기 사유를 기록한다.
3. `addons/gut/**`, `.gutconfig.json`, GUT 전용 CI를 제거한다.
4. Plugin 설정 변경은 HiGodot만 수행한다.
5. 기존 JUnit·PR·실패/성공 증거는 보존한다.
6. Godot parse, 기존 회귀, 권위 경계 검증을 다시 실행한다.

## 비목표

- 이 PR에서 GUT vendor bytes 설치
- 이 PR에서 HiGodot Production Adapter 승격
- PR #122 수정·병합
- Scene·Resource·프로젝트 설정 변경
- 제품 이미지 생성 또는 승인

판정: `NO_PRODUCT_PATH_CHANGE / DESIGN_ONLY / USER_REVIEW_REQUIRED`.
