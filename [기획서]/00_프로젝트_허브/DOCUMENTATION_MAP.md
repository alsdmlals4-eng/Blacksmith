# Documentation Map

## 원칙

- 한 질문에는 현행 책임 원본 하나만 둔다.
- 구현 사실은 Script·Scene·Test, 수치는 `data/**/*.json`, 서술 기획은 등록된 Markdown이 책임진다.
- PDF와 DOCX는 사람용 파생본이며 Markdown·JSON 책임 원본을 대체하지 않는다.
- 현재 상태는 `ACTIVE_CONTEXT.md`, 작업 순서는 `ROADMAP.md`·Issue·Plan이 책임진다.
- 구현 작성 상태와 실행 검증 상태는 `docs/MVP-003_IMPLEMENTATION_STATUS.md`에서 분리한다.

## 시작 경로

```text
AGENTS.md
→ START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 Issue·MVP Scope·Plan·Implementation Status
→ 실제 구현·데이터·테스트
```

## 책임별 정본

| 질문 | 현행 책임 원본 | 역할 |
|---|---|---|
| 프로젝트가 어떤 게임인가 | `docs/superpowers/specs/2026-07-23-project-core-design.md` | 확정 코어, 불변·변경·재승인·제외 경계 |
| 통합 게임 구조는 무엇인가 | `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md` | 코어 기반 통합 시스템 설명, 구현/계획 분리 |
| 현재 무엇이 구현됐고 다음은 무엇인가 | `ACTIVE_CONTEXT.md` | 현재 상태, 다음 작업, 위험, 검증 상태 |
| 현재 개발 순서는 무엇인가 | `ROADMAP.md` | Prototype→PoC→확장 게이트 |
| 통과·미실행·차단 상태는 무엇인가 | `DEVELOPMENT_GATES.md` | 게이트별 증거와 판정 |
| 장비 생애 PoC의 상세 규칙은 무엇인가 | `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md` | 철검·검투사 첫 생애 통합 명세 |
| MVP-003의 구현 경계는 무엇인가 | `docs/MVP-003_SCOPE.md` | Issue #34 포함·제외·완료 기준 |
| 어떤 순서로 구현하는가 | `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md` | Task 1~9 TDD 구현계획 |
| Task 1~9는 어디까지 작성·검증됐는가 | `docs/MVP-003_IMPLEMENTATION_STATUS.md` | 파일별 작성 상태와 실행 증거 분리 |
| Actions 비용·실행 정책은 무엇인가 | `docs/CI_EXECUTION_POLICY.md` | 변경 유형별 CI, 비용 게이트, 재활성화 절차 |
| 수동 Godot 검증 경로는 무엇인가 | `docs/GODOT_PLAYTEST.md` | 기존 Prototype·장비 생애 PoC 사람 검증 절차 |
| 최종 적대적 검토의 증거는 무엇인가 | `docs/FINAL_ADVERSARIAL_REVIEW_REPORT.md` | 대화 원장, 5회 검토, finding, PR·검증 판정 |
| 강화 수치와 위험은 무엇인가 | `data/crafting/enhancement_balance.json` | 성공·보정·위험·성장·가격 수치 |
| 수식어 이정표는 무엇인가 | `data/crafting/enhancement_milestones.json` | `+10` 단위 수식어 성장 |
| Base 기준은 무엇인가 | `docs/BASE_RULES_VERSION.md` | 고정 commit과 적용 정책 |
| Base 적용 검증은 무엇인가 | `docs/BASE_ADOPTION_AUDIT.md` | 25 Skill 매핑과 CI 증거 |
| 문서 발행 정책은 무엇인가 | `DESIGN_DOCUMENT_REGISTRY.json` | source, status, output, manifest, policy |
| Skill 라우팅은 무엇인가 | `SKILL_REGISTRY.json` | trigger·mode·owner |

## MVP 정본

| MVP | 책임 원본 | 상태 |
|---|---|---|
| MVP-001 제작 | `docs/MVP-001_SCOPE.md` | 구현·자동 검증 PASS 이력, 사람/Android 미검증 |
| MVP-002 강화·보관·자동 단조 | `docs/MVP-002_SCOPE.md` | 구현·자동 검증 PASS 이력, 장기 플레이/Android 미검증 |
| MVP-003 장비 한 점의 생애 | `docs/MVP-003_SCOPE.md`, `docs/MVP-003_IMPLEMENTATION_STATUS.md` | `IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED` |
| MVP-004 상인 납품 | Game Bible·Roadmap의 후속 항목 | MVP-003 행동 증거 전 `DEFERRED` |

## 현재 Issue·PR

- 현재 Issue: #34
- 현재 구현 PR: #35 Draft
- 병합 완료: #31, #32, #33
- Actions 자동 실행: `DEFERRED_UNTIL_ACTIONS_AVAILABLE`
- 완료된 과거 Issue: #29, #14

## 역사 문서

`CHANGELOG.md`, 과거 Decision, 닫힌 Issue·PR은 당시 사실을 보존한다. 역사 표현은 현행 정본으로 사용하지 않으며, 활성 시작 문서가 역사 상태를 현재 상태처럼 가리키면 결함이다.
