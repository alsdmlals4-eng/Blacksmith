# Documentation Map

## 최초 읽기

```text
AGENTS.md
→ START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ SKILL_REGISTRY.json
→ WORK_MODE_AND_SKILL_ROUTING.md
→ 현재 책임 원본·실제 파일
```

## 질문별 책임 원본

| 질문 | 책임 원본 |
|---|---|
| 게임의 핵심 경험과 전체 시스템은 무엇인가? | `../01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md` |
| 현재 무엇이 확정·구현·검증됐는가? | `ACTIVE_CONTEXT.md` |
| 다음 작업과 제품·작업 게이트는 무엇인가? | `ROADMAP.md`, `DEVELOPMENT_GATES.md` |
| 위험·가격 곡선 시뮬레이션의 입력·지표·판정·완료 기준은 무엇인가? | `../../docs/BALANCE_SIMULATION_SCOPE.md` |
| 최신 위험·가격 곡선 기준선 결과와 해석은 무엇인가? | `../../docs/BALANCE_SIMULATION_REPORT.md` |
| 최근 프로젝트 결정은 무엇인가? | `DECISION_LOG.md`, `CHANGELOG.md` |
| 문서별 책임 원본과 발행 정책은 무엇인가? | `DESIGN_DOCUMENT_REGISTRY.json` |
| Work Mode와 Skill을 어떻게 자동 선택하는가? | `WORK_MODE_AND_SKILL_ROUTING.md`, `SKILL_REGISTRY.json` |
| Base의 어느 버전을 어떻게 적용했는가? | `../../docs/BASE_RULES_VERSION.md`, `../../docs/BASE_ADOPTION_AUDIT.md` |
| 반복 작업의 프로젝트 Skill 계약은 어디인가? | `../../skills/*/SKILL.md`, `../../skills/SKILL_LEARNING_LOG.md` |
| 제작 범위와 구현은 어디인가? | `../../docs/MVP-001_SCOPE.md`, `../../scripts/forging/`, `../../scripts/ui/forging_screen.gd` |
| 강화·보관·자동 단조 범위와 구현은 어디인가? | `../../docs/MVP-002_SCOPE.md`, `../../scripts/enhancement/`, `../../scripts/ui/enhancement_screen.gd`, `../../scripts/ui/enhancement_test_runner.gd`, `../../scripts/ui/game_flow_screen.gd` |
| 제작→강화 기본 실행 진입점은 어디인가? | `../../project.godot`, `../../scenes/test/enhancement_test.tscn`, `../../scenes/main/main.tscn` |
| 재료·강화·수식어 실제 값은 무엇인가? | `../../data/crafting/*.json` |
| 고객·판매 실제 값은 무엇인가? | `../../data/sales/*.json` |
| 자동 검증은 무엇을 확인하는가? | `../../tests/README.md`, `../../tests/unit/`, `../../.github/workflows/godot-validation.yml` |
| 데이터가 유효한가? | `../../tools/validate_game_data.py` |
| 모바일 기술·출시 기준은 무엇인가? | `../../project.godot`, `../../docs/BASE_RULES_VERSION.md`, `DEVELOPMENT_GATES.md` |
| Godot AI 개발 연동과 검증 경계는 어디인가? | `../../project.godot`, `../../addons/godot_ai/README.md`, `ACTIVE_CONTEXT.md`, `DEVELOPMENT_GATES.md` |
| 사람용 PDF·DOCX·다이어그램 발행 상태는? | `DESIGN_DOCUMENT_REGISTRY.json`과 해당 Publication Manifest |

## 책임 원본 정책

- 서술·의도·규칙: 등록된 Markdown
- ID·수치·관계·상태·게임 데이터: JSON
- 구현 사실: 실제 Scene·GDScript
- 완료 증거: 자동 테스트·Godot 실행·Android 기기·캡처·프로파일
- 분석 범위·지표·판정 계약: 등록된 분석 Scope. 실제 수치와 런타임을 대체하지 않음
- PDF·DOCX·다이어그램: 사람용 파생본. 생성·해시·시각 검수가 없으면 `NOT_RUN`
- 과거 상태: Git 이력

한 질문에 활성 책임 원본을 여러 개 만들지 않는다. 외부 벤치마크·리뷰·과거 대화는 기획·구현 정본을 대체하지 않는다.

## 선택적 읽기

- 구형·중복 파일 정리: `../../docs/BASE_ADOPTION_AUDIT.md`와 Git 이력
- 위험·가격 곡선 시뮬레이션: `../../docs/BALANCE_SIMULATION_SCOPE.md`, 관련 JSON·런타임·테스트
- Android·AAB 검증: `DEVELOPMENT_GATES.md`, 관련 export 설정과 실제 기기 로그
- 접근성·성능: 실제 대상 화면·빌드·기기·프로파일이 있을 때만 검수
- 승인 아트: 승인 이미지와 Asset Manifest가 도입된 이후 읽기 경로에 추가
