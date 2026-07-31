# Documentation Map

## 원칙

- 한 질문에는 현행 책임 원본 하나만 둔다.
- 구현 사실은 Script·Scene·Test, 수치는 `data/**/*.json`, 서술 기획은 등록된 Markdown이 책임진다.
- PDF와 DOCX는 사람용 파생본이며 Markdown·JSON 책임 원본을 대체하지 않는다.
- 현재 상태는 `ACTIVE_CONTEXT.md`, 작업 순서는 `ROADMAP.md`·Issue·Plan이 책임진다.
- 구현 작성·자동 실행·사람 검증 상태는 `docs/MVP-003_IMPLEMENTATION_STATUS.md`에서 분리한다.
- 주요 변경·승인 결정은 같은 Decision ID로 GitHub 권위 문서·계획 데이터·연결 Google Sheet에 동기화한다.
- 승인 전 시각 설계는 Design ID와 `PROPOSED_REVIEW_REQUIRED` 상태로 분리한다.

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
| Blacksmith Vertical Slice v9의 현행 통합 기획은 무엇인가 | `docs/planning/BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md` | Base v9.3·Vertical Slice v9 기준 통합 기획 초안 |
| 비주얼 중심 화면 보드는 어떤 형식으로 작성하는가 | `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_WORK_ORDER_2026.md` | PART A~D, 필수 화면 4종, 근거 태그, 적대적 검토를 정의하는 상위 시각 계약 |
| 현재 비주얼 화면 설계 초안은 무엇인가 | `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_DESIGN_V1_2026.md`, `docs/planning/data/blacksmith_visual_situation_board_design_v1_2026.json` | 화면 4종·핵심 시퀀스 5종·전환도·최소 구현 부록의 Design ID 기반 초안 |
| 기획 완료 전에 어떤 기술 화면·상황 중간점검을 수행하는가 | `docs/planning/BLACKSMITH_SITUATION_SCREEN_SPEC_WORK_ORDER_2026.md` | 필수 기준 화면 4종, 상황 P0~P3, P0 A~T Godot 구현 명세 하위 계약 |
| 화면·상황 중간점검에서 무엇이 확인됐는가 | `docs/planning/BLACKSMITH_SITUATION_SCREEN_MID_CHECK_2026.md`, `docs/planning/data/blacksmith_situation_screen_mid_check_2026.json` | 실제 Scene·Script·데이터 감사, P0/P1 Finding, 상황 명세, 화면 연결 |
| 고객 4유형·유형별 복수 고객과 +50 일반/고위 정밀강화의 최신 결정은 무엇인가 | `docs/planning/BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md` | 벤치마킹·적대적 검토를 거친 최신 보완 권위 |
| 사용자 승인 결정과 동일 ID 인덱스는 무엇인가 | `docs/planning/BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`, `docs/planning/data/blacksmith_v9_canonical_decision_set_2026.json` | 승인 내용의 Markdown·기계 판독 정본 연결 |
| 주요 변경·승인 결정을 어떻게 즉시 동기화하는가 | `docs/planning/BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md` | Decision ID, GitHub·Sheet 쓰기 순서, 상태, 기록 의무 |
| 남은 구조적 기획과 완료 전 Review Gate는 무엇인가 | `docs/planning/BLACKSMITH_REMAINING_PLANNING_STATUS_2026.md` | 구조 기획 상태, 화면 Finding, 시각 결정, 다음 Gate 분리 |
| 연결 Google Sheet의 책임·편집 정책은 무엇인가 | `docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md` | Sheet ID, 탭 매핑, 즉시 동기화·검증 정책 |
| 프로젝트가 어떤 게임인가 | `docs/superpowers/specs/2026-07-23-project-core-design.md` | 확정 코어, 불변·변경·재승인·제외 경계 |
| 통합 게임 구조는 무엇인가 | `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md` | 코어 기반 통합 시스템 설명, 구현/계획 분리 |
| 현재 무엇이 구현됐고 다음은 무엇인가 | `ACTIVE_CONTEXT.md` | 현재 상태, 다음 작업, 위험, 검증 상태 |
| 현재 개발 순서는 무엇인가 | `ROADMAP.md` | Prototype→PoC→확장 게이트 |
| 통과·미실행·차단 상태는 무엇인가 | `DEVELOPMENT_GATES.md` | 게이트별 증거와 판정 |
| 장비 생애 PoC의 상세 규칙은 무엇인가 | `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md` | 철검·검투사 첫 생애 통합 명세 |
| `+5 납품 / +10 도전` 선택의 근거와 권장안은 무엇인가 | `docs/planning/BLACKSMITH_PLUS5_PLUS10_EVIDENCE_PACK_PILOT_2026.md` | 애착·위험·투명성·모바일 선택의 `PLANNING_INPUT / NOT_CANON` |
| `+5 납품 / +10 도전`을 어떤 세션과 기준으로 실행하는가 | `docs/superpowers/plans/2026-07-29-plus5-plus10-human-validation-artifact.md` | 기존 장비 생애 PoC에 결합한 `HUMAN_VALIDATION_INPUT / NOT_CANON` |
| 합성 테스터를 어떤 Skill·작업 구조로 적용하는가 | `docs/research/2026-07-29_SYNTHETIC_TESTER_STRUCTURE_ANALYSIS.md` | 현재 Registry·정본·보호 경로를 복원한 `T6_AI_INFERENCE / NOT_CANON` |
| `+5 / +10` 선택의 합성 위험 판정은 무엇인가 | `docs/research/2026-07-29_PLUS5_PLUS10_SYNTHETIC_TESTER_REPORT.md` | 후견 문구·scripted failure·경제 지배 전략의 `AI_SIMULATION_COMPLETED / HUMAN_NOT_RUN` |
| MVP-003의 구현 경계는 무엇인가 | `docs/MVP-003_SCOPE.md` | Issue #34 포함·제외·완료 기준 |
| 어떤 순서로 구현하는가 | `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md` | Task 1~9 TDD 구현계획 |
| Task 1~9는 어디까지 작성·검증됐는가 | `docs/MVP-003_IMPLEMENTATION_STATUS.md` | 파일별 작성·자동·사람 검증 상태 |
| Actions 비용·실행 정책은 무엇인가 | `docs/CI_EXECUTION_POLICY.md` | 변경 유형별 CI와 main/nightly 정책 |
| 수동 Godot 검증 경로는 무엇인가 | `docs/GODOT_PLAYTEST.md` | 기존 Prototype·장비 생애 PoC 사람 검증 절차 |
| 최종 적대적 검토의 증거는 무엇인가 | `docs/FINAL_ADVERSARIAL_REVIEW_REPORT.md` | 대화 원장, 5회 검토, finding, PR·검증 판정 |
| 강화 수치와 위험은 무엇인가 | `data/crafting/enhancement_balance.json` | 성공·보정·위험·성장·가격 수치 |
| 수식어 이정표는 무엇인가 | `data/crafting/enhancement_milestones.json` | 구형 구현 데이터. 최신 v9와 충돌 여부를 중간점검 Finding으로 추적 |
| Base 기준은 무엇인가 | `docs/BASE_RULES_VERSION.md` | 고정 commit과 적용 정책 |
| Base 적용 검증은 무엇인가 | `docs/BASE_ADOPTION_AUDIT.md` | 25 Skill 매핑과 CI 증거 |
| 문서 발행 정책은 무엇인가 | `DESIGN_DOCUMENT_REGISTRY.json` | source, status, output, manifest, policy |
| Skill 라우팅은 무엇인가 | `SKILL_REGISTRY.json` | trigger·mode·owner |

## MVP 정본

| MVP | 책임 원본 | 상태 |
|---|---|---|
| MVP-001 제작 | `docs/MVP-001_SCOPE.md` | 구현·자동 검증 PASS 이력, 사람/Android 미검증 |
| MVP-002 강화·보관·자동 단조 | `docs/MVP-002_SCOPE.md` | 구현·자동 검증 PASS 이력, 장기 플레이/Android 미검증 |
| MVP-003 장비 한 점의 생애 | `docs/MVP-003_SCOPE.md`, `docs/MVP-003_IMPLEMENTATION_STATUS.md` | `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING` |
| MVP-004 상인 납품 | Game Bible·Roadmap의 후속 항목 | MVP-003 행동 증거 전 `DEFERRED` |

## 현재 Issue·PR

- 현재 기획 추적 Issue: #79
- 현재 기획 Draft PR: #81 · `VISUAL_BOARD_DRAFT_COMPLETE / FINDINGS_OPEN / NOT_MERGED`
- 화면 중간점검: P0 Finding 6건, P1 Finding 4건
- 사용자 시각 결정: 3건
- 현재 구현 검증 Issue: #34 · 사람·플랫폼·외부 플레이 검증까지 유지
- MVP-003 구현 PR: #35 · `MERGED`, merge commit `639c33611c203581c8dcbc08c85425455b16991a`
- 사람·Android·성능·외부 플레이: `NOT_RUN`
- Codex·제품 구현: `BLOCKED_UNTIL_기획완료_AND_검수완료`
- Actions 자동 실행: `ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED`

## 역사 문서

`CHANGELOG.md`, 과거 Decision, 닫힌 Issue·PR은 당시 사실을 보존한다. 역사 표현은 현행 정본으로 사용하지 않으며, 활성 시작 문서가 역사 상태를 현재 상태처럼 가리키면 결함이다.
