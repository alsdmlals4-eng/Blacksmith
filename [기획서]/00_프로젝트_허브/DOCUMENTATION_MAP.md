# Documentation Map

| 질문 | 책임 원본 |
|---|---|
| 게임의 핵심 경험과 시스템은 무엇인가? | `../01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md` |
| 현재 무엇이 확정·구현·검증됐는가? | `ACTIVE_CONTEXT.md` |
| 다음 작업과 단계는 무엇인가? | `ROADMAP.md`, `DEVELOPMENT_GATES.md` |
| 최근 변경은 무엇인가? | `CHANGELOG.md` |
| 문서별 책임 원본은 어디인가? | `DESIGN_DOCUMENT_REGISTRY.json` |
| 반복 작업에 어떤 스킬을 쓰는가? | `SKILL_REGISTRY.json` |
| MVP-001 제작 범위는 무엇인가? | `../../../docs/MVP-001_SCOPE.md` |
| MVP-002 강화 범위와 수치는 무엇인가? | `../../../docs/MVP-002_SCOPE.md` |
| 재료·무기·강화 실제 값은 무엇인가? | `../../../data/crafting/*.json` |
| 고객·판매 실제 값은 무엇인가? | `../../../data/sales/*.json` |
| 제작 구현은 어디에 있는가? | `../../../scripts/forging/`, `../../../scripts/ui/forging_screen.gd` |
| 강화 구현은 어디에 있는가? | `../../../scripts/enhancement/`, `../../../scripts/ui/enhancement_screen.gd`, `../../../scripts/ui/game_flow_screen.gd` |
| 자동 검증은 무엇을 확인하는가? | `../../../tests/README.md`, `../../../tests/unit/`, `../../../.github/workflows/godot-validation.yml` |
| 모바일 기술 기준은 무엇인가? | `../../../project.godot`, `../../../docs/BASE_RULES_VERSION.md` |
| 데이터가 유효한가? | `../../../tools/validate_game_data.py` |
| 결정 이유는 무엇인가? | `DECISION_LOG.md` |

## 책임 원본 정책

- 설명과 규칙: Markdown
- ID, 수치, 관계, 게임 데이터: JSON
- 구현 사실: 실제 Scene·Script
- 완료 증거: 자동 테스트와 실제 Android 실행
- PDF/DOCX: 사람용 파생본이며 현재 `NOT_RUN`
