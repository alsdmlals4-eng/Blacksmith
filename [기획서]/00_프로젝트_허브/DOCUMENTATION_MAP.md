# Documentation Map

## 최초 읽기

```text
AGENTS.md
→ START_HERE.md
→ ACTIVE_CONTEXT.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 책임 원본
→ SKILL_REGISTRY.json
→ 실제 코드·데이터·테스트
```

## 질문별 책임 원본

| 질문 | 책임 원본·실제 증거 |
|---|---|
| 게임의 핵심 경험과 전체 시스템은? | `../01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md` |
| 현재 무엇이 구현·검증·미검증됐는가? | `ACTIVE_CONTEXT.md` |
| 다음 작업·선행 조건·Greenlight는? | `ROADMAP.md`, `DEVELOPMENT_GATES.md` |
| 결정과 대체 이력은? | `DECISION_LOG.md` |
| 최근 변경은? | `CHANGELOG.md` |
| 문서별 책임·발행 정책은? | `DESIGN_DOCUMENT_REGISTRY.json` |
| Work Mode와 Skill은? | `SKILL_REGISTRY.json`, `AI_WORKFLOW.md` |
| 변경 시 어떤 문서를 갱신하는가? | `DOCUMENT_UPDATE_MATRIX.md` |
| 세션 경계 인수인계는? | `HANDOFF.md` |
| Base 기준과 적용 차이는? | `../../docs/BASE_RULES_VERSION.md`, `../../docs/BASE_SYNC_AUDIT.md` |
| 운영체계 상태는? | `OPERATING_SYSTEM_HEALTH_REPORT.md` |
| 제작 POC는? | `../../docs/MVP-001_SCOPE.md` |
| 강화·위험·자동 단조 POC는? | `../../docs/MVP-002_SCOPE.md` |
| 재료·강화·수식어 실제 값은? | `../../data/crafting/*.json` |
| 고객·판매 실제 값은? | `../../data/sales/*.json` |
| 제작 구현은? | `../../scripts/forging/`, `../../scripts/ui/forging_screen.gd` |
| 강화 구현은? | `../../scripts/enhancement/`, `../../scripts/ui/enhancement_screen.gd` |
| 자동 단조·보관함 구현은? | `../../scripts/ui/enhancement_test_runner.gd`, `../../scripts/ui/game_flow_screen.gd` |
| 실행 진입점은? | `../../project.godot`, `../../scenes/test/enhancement_test.tscn`, `../../scenes/main/main.tscn` |
| 자동 검증은? | `../../tests/`, `../../.github/workflows/`, `../../tools/` |
| 사람이 직접 확인할 절차는? | `../../docs/GODOT_PLAYTEST.md` |

## 책임 원본 정책

- 설명·정책: Markdown
- ID·수치·관계·게임 데이터: JSON
- 구현 사실: Scene·Script
- 완료 증거: 자동 테스트·실제 실행·캡처·기기 기록
- PDF/DOCX: Registry 정책이 요구하는 사람용 파생본
- Active Context: 현재 상태의 기본 원본
- Handoff: 경계 스냅샷이며 두 번째 현재 상태 원본이 아님

## 상태 언어

`PASS / PARTIAL / FAIL / NOT_RUN / NOT_BUILT`를 사용한다. 파일 존재, Workflow 실행, Required Check 강제, 실제 Android 검증은 서로 다른 상태다.
