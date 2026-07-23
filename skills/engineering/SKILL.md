---
name: blacksmith-engineering
description: Blacksmith의 Godot·GDScript·데이터·Android·저장·자동화 구현과 계약 보존 리팩터링·런타임 진단을 안전하게 계획하고 검증한다.
---

# Blacksmith Engineering Skill

## Skill Modes

- `plan-change`: 책임 경계·영향 파일·호환성·롤백을 설계한다.
- `implement`: 승인된 Scene·Script·데이터 변경을 구현한다.
- `data-migration`: JSON Schema·ID·기본값 변경을 소비자와 함께 이전한다.
- `runtime-check`: Godot 파싱·Scene·입력·상태 전환·Android 동작을 확인한다.
- `contract-preserving-refactor`: 동작·인터페이스·데이터 호환성을 고정한 뒤 구조 중복과 복잡성만 줄인다.
- `reproduce-runtime-failure`: 엔진 버전·진입 Scene·입력·로그·상태를 고정해 원래 실패를 재현한다.
- `isolate-cause`: 연쇄 오류와 근본 원인을 분리하고 최소 반례를 만든다.
- `minimal-fix`: 재현된 원인만 수정하며 기능 확대나 무관한 정리를 섞지 않는다.
- `rerun-engine-checks`: 원래 반례·관련 Scene·회귀·목표 플랫폼 검증을 다시 실행한다.

## Technical baseline

- Godot 4.7.1 stable / GDScript
- Android portrait / 720×1280 기준
- `canvas_items` + `expand`
- Google Play AAB / API 36 준비

## Read first

- `AGENTS.md`
- `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- 관련 책임 원본과 `data/`, `scripts/`, `scenes/`, `tests/`
- `project.godot`과 관련 Workflow

## Rules

- 게임 규칙은 UI 애니메이션이 아니라 도메인 코드가 소유한다.
- JSON ID·수치·기본값을 코드에 불필요하게 중복 하드코딩하지 않는다.
- 경로·ID·Schema 변경 시 Registry·문서·테스트·untouched 소비자를 검색한다.
- 리팩터링은 제품 기능·정책 변경과 분리하고 baseline·호환 계약·롤백 지점을 먼저 기록한다.
- 런타임 오류는 재현·로그·엔진 버전 없이 추측 수정하지 않는다.
- 자동 단조는 비용·재료·목표·보관함·파괴·중지 조건을 유한 상태로 처리한다.
- 특수 강화 재료가 없을 때의 fallback은 명시적으로 처리하고 이전 선택이 누출되지 않게 한다.
- 서명키·export credentials·개인 SDK 경로를 커밋하지 않는다.
- 실제 기기에서 확인하지 않은 모바일 동작은 미검증으로 기록한다.
- 새 Scene을 불필요하게 늘리지 않고 기존 진입점과 사용자 실행 경로를 유지한다.

## Output

- 영향 파일·데이터 계약·상태 전이
- 재현 절차·근본 원인·최소 반례
- 구현 또는 리팩터링 diff와 롤백 지점
- 정상·실패·경계 처리
- 실행한 검증과 미검증

## Validation

- `python tools/validate_game_data.py`
- Godot headless 프로젝트 import·parse
- 관련 Scene 스모크 테스트
- 제작·강화 모델 테스트
- 리팩터링 전후 동일 계약·출력·저장 호환성 비교
- 저장 변경 시 저장·불러오기·구버전 호환성
- Android debug/AAB와 실제 기기 터치·화면 비율은 환경이 있을 때만 실행

## Failure conditions

- 문서만 갱신하고 실제 소비자 코드를 놓친다.
- 원래 실패를 재현하지 않고 대규모 추측 수정을 한다.
- 리팩터링과 제품 기능 변경을 한 diff에 섞는다.
- 테스트 삭제나 기대값 완화로 구조 변경을 통과시킨다.
- 자동 단조가 골드·재료 부족 또는 보관함 가득 참에서 무한 반복한다.
- 폭주 도약이 특수 강화 이정표를 건너뛴다.
- Godot 파싱 없이 구현 완료를 주장한다.
- Android 미실행을 PASS로 표시한다.

## Learning

실제 실패·회귀·성능 병목·호환성 교훈이 생기면 `skills/SKILL_LEARNING_LOG.md`에 증거와 함께 기록한다.
