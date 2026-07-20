# Blacksmith AI 작업 규칙

이 저장소는 Google Play 출시를 목표로 하는 Android 모바일용 Godot 게임 프로젝트다.

## 읽기 순서

1. `[기획서]/00_프로젝트_허브/START_HERE.md`
2. `ACTIVE_CONTEXT.md`
3. `DOCUMENTATION_MAP.md`
4. `DEVELOPMENT_GATES.md`
5. `DESIGN_DOCUMENT_REGISTRY.json`
6. 현재 작업에 필요한 기획 책임 원본과 실제 `data/`, `scripts/`, `scenes/`, `tests/`

## 기술 기준

- Godot 4.7.1 stable
- GDScript
- Android 모바일
- Google Play 배포
- 기본 세로 화면, 720×1280 기준
- 출시 빌드는 Android App Bundle(`.aab`)
- 2026년 8월 31일 이후 Google Play 제출 기준을 고려해 Android 16 / API 36 이상을 목표로 준비한다.

## 작업 원칙

- 최신 사용자 지시가 가장 우선한다.
- 한 질문에는 현행 책임 원본 하나만 둔다.
- 서술 기획은 Markdown, 실제 게임 값과 ID는 JSON으로 관리한다.
- 문서 존재를 구현 또는 검증 완료로 표시하지 않는다.
- 전체 Base 저장소나 전체 스킬을 복사하지 않는다.
- 범위 밖 기능, 직원 시스템, 무기 수리, 결제, 광고, 서버를 임의로 추가하지 않는다.
- 모바일 터치 조작과 작은 화면의 가독성을 우선한다.
- 광클은 불이익이 아니라 피버 보상으로 연결한다.
- 정밀작업은 마무리·강화에서 사용자가 켜고 끌 수 있어야 한다.
- 게임 데이터 변경 시 `python tools/validate_game_data.py`를 실행한다.
- 실제 Android 기기 검증 전에는 모바일 검증 완료로 표시하지 않는다.
