# Blacksmith AI 작업 규칙

이 저장소는 Google Play 출시를 목표로 하는 Android 세로형 Godot 게임 프로젝트다. 공용 작업 기준은 `alsdmlals4-eng/Base`에서 분화하되, Blacksmith의 실제 기획·수치·코드·자산·테스트가 항상 우선한다.

## 1. 우선순위

1. 사용자의 최신 지시
2. 이 문서와 보안·엔진·데이터 규칙
3. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`와 승인된 작업 계약
4. 등록된 책임 원본과 실제 코드·데이터·Scene·테스트
5. `docs/BASE_RULES_VERSION.md`에 기록된 Base 기준
6. Base 원격 원본과 외부 자료

정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다. 문서, 외부 사례, 과거 대화는 실제 구현 사실을 대체하지 않는다.

## 2. 시작 순서

```text
AGENTS.md
→ [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ SKILL_REGISTRY.json
→ 현재 책임 원본·Issue·Plan
→ 실제 data/·scripts/·scenes/·tests/
```

Base URL을 직접 지정한 요청은 `docs/BASE_RULES_VERSION.md`와 `docs/BASE_ADOPTION_AUDIT.md`를 함께 확인한다. 전체 Base를 그대로 복제하지 않고 현재 작업에 적용되는 책임 원본·Skill·Template·Test만 프로젝트 전용으로 분화한다.

## 3. Work Mode와 Skill

한 시점에는 주 Work Mode 하나를 사용한다.

- `PLAN`: 요구·근거·정본·실행 순서 확정. 기본 읽기·제안.
- `BUILD`: 승인 범위의 코드·데이터·문서·자산 구현.
- `REVIEW`: 적대적 검토·반례·검증. 기본 읽기 전용.

Skill은 `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`의 trigger로 최소 집합을 자동 선택한다. 사용자가 Skill 이름을 고를 필요가 없다. Skill 파일을 읽은 것과 실제 절차를 실행한 것을 구분한다.

L1 이상 작업 완료 보고에는 실제 사용한 Work Mode·Skill·Skill Mode, 사용 이유, 수행 내용, 결과·증거, 미검증을 포함한다.

## 4. 기술 기준

- Godot 4.7.1 stable / GDScript
- Android 모바일 / Google Play
- 기본 세로 화면 720×1280, 다양한 비율은 Expand 대응
- 출시 빌드는 Android App Bundle(`.aab`)
- Android 16 / API 36 이상 목표
- 모바일 터치·작은 화면 가독성·안전 영역 우선
- 실제 Android 기기 검증 전에는 모바일 검증 완료로 표시하지 않는다.

## 5. 프로젝트 고정 원칙

- 한 질문에는 등록된 현행 Markdown 또는 JSON 책임 원본 하나만 둔다.
- 서술 기획은 Markdown, ID·수치·관계·게임 데이터는 JSON이 책임진다.
- 구현 사실은 실제 Scene·Script, 완료 증거는 테스트·실행 캡처·프로파일이 책임진다.
- 직원 시스템, 일상적 무기 수리 관리, 결제, 광고, 서버를 범위 승인 없이 추가하지 않는다.
- 중요한 역사 장비의 선택형 복원은 일상 수리와 별개인 후속 기획이며 첫 장비 생애 PoC에서는 `DEFERRED`다.
- 광클은 불이익이 아니라 피버 보상으로 연결한다.
- 일반 강화와 +10 단위 특수 강화를 구분한다.
- 정밀 강화와 보조재료·촉매는 특수 강화에서만 사용한다.
- 문서 존재를 구현·승인·검증·발행 완료로 표시하지 않는다.

## 6. 기존 파일과 정본 변경

구형·중복·버전명 파일은 이름만 보고 삭제하지 않는다. `CURRENT / UPDATE_IN_PLACE / MERGE_TO_CANONICAL / COMPATIBILITY_STUB / ARCHIVE_HISTORY / DELETE_APPROVED / KEEP_UNRESOLVED` 중 하나로 판정하고, 고유 정보·참조·복구 경로를 확인한다.

경로·ID·Schema·정본·생성기를 변경하면 변경된 파일뿐 아니라 변경됐어야 하지만 untouched인 소비자, Registry, 테스트, 문서, 파생본을 함께 확인한다.

## 7. 최소 검증

```text
작업 계약·diff 대조
→ 정본·경로·ID·Schema 참조 최신성
→ 포맷·문법·정적 검사
→ 관련 자동 테스트
→ Godot Scene·런타임
→ 적용 시 접근성·성능
→ 정상·실패·경계·회귀
→ 상태 문서·Registry 동기화
```

게임 데이터 변경 시 `python tools/validate_game_data.py`를 실행한다. Godot 변경 시 프로젝트 파싱, 관련 Scene 스모크 테스트, 모델 테스트를 실행한다. 실행하지 못한 검사는 `NOT_RUN` 또는 `UNVERIFIED`로 기록한다.

## 8. 완료 조건

- 실제 결과와 승인·구현·검증 상태가 일치한다.
- 관련 책임 원본·Registry·Roadmap·Development Gates·Active Context가 최신이다.
- 오래된 활성 참조와 누락된 소비자가 없다.
- 자동·수동·시각·Android·접근성·성능 검증이 분리돼 있다.
- PR Required Checks와 파일별 재검토가 끝났다.
- 새 작업자가 저장소만으로 현재 상태, 다음 작업, 위험, 검증 경로를 찾을 수 있다.
