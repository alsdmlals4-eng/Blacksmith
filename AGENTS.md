# Blacksmith AI 작업 규칙

Blacksmith는 Google Play 출시를 목표로 하는 Android 세로형 Godot 게임 프로젝트다. 프로젝트 고유 결정과 실제 구현은 이 저장소가 책임지고, 공용 작업 방법은 `docs/BASE_RULES_VERSION.md`에 고정된 Base 기준을 프로젝트에 맞게 분화해 사용한다.

## 최초 읽기

```text
AGENTS.md
→ [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 책임 원본
→ SKILL_REGISTRY.json
→ 현재 Issue·승인 요청
→ 실제 data/·scripts/·scenes/·tests/
```

전체 Base 저장소나 전체 `skills/`를 기본 로드하지 않는다. 현재 Prompt와 Registry trigger가 일치하는 책임 원본·Skill·검증만 읽는다.

## 우선순위

1. 사용자의 최신 지시
2. 이 문서의 보안·엔진·데이터 규칙
3. Active Context와 승인된 Issue·작업 계약
4. 등록된 책임 원본과 실제 코드·데이터·테스트
5. 프로젝트에 동기화된 Base 기준
6. Base 원격 원본과 외부 자료

외부 사례·리뷰·과거 대화는 개선 근거일 수 있지만 요구사항이나 구현 상태의 정본이 아니다.

## Work Mode와 자동 Skill 라우팅

- `PLAN`: 요구·근거·정본·순서 확정. 승인 전 제품 동작 변경 금지.
- `BUILD`: 승인 범위의 코드·데이터·문서·자산 구현.
- `REVIEW`: 실제 diff·반례·정적·런타임·회귀 증거 검수.

한 시점에는 주 Work Mode 하나만 둔다. `SKILL_REGISTRY.json`의 `automatic-trigger-match`로 필요한 최소 Skill만 선택하고, 사용자가 Skill 이름을 고르게 하지 않는다. L1 이상 완료 보고에는 실제 사용한 Work Mode·Skill·Skill Mode, 이유, 수행 내용, 증거, 미검증을 포함한다.

## 책임 원본

- 한 질문에는 등록된 Markdown 또는 JSON 책임 원본 하나만 둔다.
- 서술·정책은 Markdown, ID·수치·관계·런타임 데이터는 JSON이 소유한다.
- 구현 사실은 Scene·Script·데이터·테스트가 최종 증거다.
- PDF·DOCX는 독립 원본이 아니며 Registry 정책이 요구할 때만 생성한다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 정본·경로·ID·Schema를 바꾸면 START_HERE, Documentation Map, Registry, 테스트, Workflow와 파생본의 참조 최신성을 검사한다.

## 기술 기준

- Godot 4.7.1 stable / GDScript
- Android 모바일 / 세로형 720×1280 / `canvas_items` + `expand`
- Google Play / Android App Bundle
- API 36 이상 제출 준비
- 서명키·export credentials·개인 인증 정보는 커밋하지 않는다.
- 실제 Android 기기에서 확인하지 않은 동작은 `NOT_RUN` 또는 미검증으로 기록한다.

## 게임 보호 규칙

- 직원과 무기 수리를 임의로 추가하지 않는다.
- 광클은 불이익이 아니라 피버 보상으로 연결한다.
- 일반 강화와 +10 단위 특수 강화를 구분한다.
- 특수 강화용 보조재료·촉매·정밀 판정 효과가 일반 강화에 누출되지 않게 한다.
- 현재 +100 강화, 하락·파괴·실패 보정, 단조 기술, 가격·성장, 보관함·자동 단조 규칙을 변경하려면 데이터·문서·테스트를 함께 갱신한다.
- 범위 밖 판매·저장·결제·광고·서버 기능을 임의로 추가하지 않는다.

## 필수 검증

```bash
python tools/validate_game_data.py
python tools/check_project_governance.py
godot --headless --editor --path . --quit
godot --headless --path . res://scenes/test/enhancement_test.tscn --quit-after 2
godot --headless --path . --script res://tests/unit/test_forging_session.gd
godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
```

실행하지 않은 검사·렌더·Android 빌드·사람 검수는 PASS로 표시하지 않는다.
