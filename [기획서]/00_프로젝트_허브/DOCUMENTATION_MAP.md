# Documentation Map

## 원칙

- 한 질문에는 현행 책임 원본 하나만 둔다.
- 구현 사실은 Script·Scene·Test, 수치는 `data/**/*.json`, 서술 기획은 등록된 Markdown이 책임진다.
- PDF와 DOCX는 사람용 파생본이며 Markdown·JSON 책임 원본을 대체하지 않는다.
- 현재 상태는 `ACTIVE_CONTEXT.md`, 작업 순서는 `ROADMAP.md`·Issue·Plan이 책임진다.
- 구현 작성·자동 실행·사람 검증 상태는 `docs/MVP-003_IMPLEMENTATION_STATUS.md`에서 분리한다.
- 주요 변경·승인 결정은 같은 Decision ID로 GitHub 권위 문서·계획 데이터·연결 Google Sheet에 동기화한다.
- 기존 승인 의미가 바뀌면 기존 ID를 덮어쓰지 않고 신규 ID와 `supersedes` 관계를 기록한다.
- 승인 전 설계는 Design ID, 감사 Finding은 Audit ID로 승인 결정과 분리한다.
- 비주얼 보드의 이미지 예시는 시스템 정본이 아니며, 승인 문서가 명시한 항목만 CURRENT가 된다.

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
| Blacksmith의 현행 저장·이어하기·결과 복구 규칙은 무엇인가 | `docs/planning/BLACKSMITH_SAVE_CONTINUE_RESULT_ENVELOPE_CANON_2026.md`, 연결 JSON | `BS-SAVE-20260801-01`; 단일 캠페인·자동 백업 2개·AttemptIntent·ResultEnvelope·손상 복구·새 게임 교체 |
| 저장·이어하기 구현은 어떤 순서로 진행해야 하는가 | `docs/superpowers/plans/2026-08-01-save-continue-result-envelope-implementation.md` | 11개 TDD Task; 전체 기획·검수 완료 전 실행 금지 |
| Blacksmith의 현행 제작 등급은 무엇인가 | `docs/planning/BLACKSMITH_CRAFTSMANSHIP_GRADE_CANON_2026-08-01.md`, 연결 JSON | `BS-GRADE-20260801-02`; 보통→우수→명품→걸작→전설 5단계 |
| Blacksmith Vertical Slice v9의 현행 통합 기획은 무엇인가 | `docs/planning/BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md` | Base v9.3·Vertical Slice v9 통합 초안. 저장·제작 등급 등 최신 별도 정본이 우선 |
| 승인된 별도 메인 화면과 제품 Shell은 무엇인가 | `docs/planning/BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md`, 연결 JSON | `BS-MAIN-20260801-01`, `BS-SHELL-20260801-01`, 시각 보드 승인 범위와 Placeholder 경계 |
| 기존 프로젝트 적대적 감사에서 무엇이 발견됐는가 | `docs/planning/BLACKSMITH_EXISTING_PROJECT_ADVERSARIAL_AUDIT_2026-08-01.md`, 연결 JSON, 최신 Addendum | main 문서·Scene·Script·Data·Test 대조, P0 10·P1 10·P2 6 Finding |
| 저장·ResultEnvelope 감사 목표가 어떻게 해결됐는가 | `docs/planning/BLACKSMITH_EXISTING_PROJECT_AUDIT_ADDENDUM_SAVE_2026-08-01.md` | F02·F09 기획 목표와 F16 중단 복구 목표 해결, 런타임·테스트는 OPEN |
| 제작 등급 감사 목표가 어떻게 갱신됐는가 | `docs/planning/BLACKSMITH_EXISTING_PROJECT_AUDIT_ADDENDUM_GRADE_2026-08-01.md` | F04 목표를 현행 5단계로 변경하되 실제 런타임·저장·테스트 마이그레이션은 OPEN |
| 비주얼 중심 화면 보드는 어떤 형식으로 작성하는가 | `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_WORK_ORDER_2026.md` | PART A~D, 필수 화면, 근거 태그, 적대적 검토 상위 계약 |
| 현재 비주얼 화면 작업 기준은 무엇인가 | `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_DESIGN_V1_2026.md`, 연결 JSON, `BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md` | 화면·시퀀스 설계와 `USER_ACCEPTED_WORKING_BASELINE` 승인 범위 연결 |
| 프로젝트 그림체와 모닥의 승인된 최신 방향은 무엇인가 | `docs/planning/BLACKSMITH_ART_STYLE_AND_MODAK_CANON_2026.md`, 연결 JSON | 스타일라이즈드 다크 포지와 밝은 불 정령 모닥의 사용자 승인 정본 |
| 기획 완료 전에 어떤 기술 화면·상황 중간점검을 수행하는가 | `docs/planning/BLACKSMITH_SITUATION_SCREEN_SPEC_WORK_ORDER_2026.md` | 필수 기준 화면·상황 P0~P3·P0 A~T Godot 명세 계약 |
| 초기 화면 중간점검에서 무엇이 확인됐는가 | `docs/planning/BLACKSMITH_SITUATION_SCREEN_MID_CHECK_2026.md`, 연결 JSON | 초기 Scene·Script·데이터 감사와 화면 Finding 이력 |
| 고객 4유형·유형별 복수 고객과 +50 두 경로의 최신 결정은 무엇인가 | `docs/planning/BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md` | 벤치마킹·적대적 검토를 거친 최신 보완 권위 |
| 사용자 승인 결정과 동일 ID 인덱스는 무엇인가 | `docs/planning/BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`, 연결 JSON | 승인 내용의 Markdown·기계 판독 정본 연결 |
| 주요 변경·승인 결정을 어떻게 즉시 동기화하는가 | `docs/planning/BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md` | Decision ID, GitHub·Sheet 쓰기 순서, 상태, 기록 의무 |
| 남은 구조적 기획과 완료 전 Gate는 무엇인가 | `docs/planning/BLACKSMITH_REMAINING_PLANNING_STATUS_2026.md` | 현재 감사 Finding, 보존 항목, 다음 작업과 차단 상태 |
| 연결 Google Sheet의 책임·편집 정책은 무엇인가 | `docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md` | Sheet ID, 탭 매핑, 즉시 동기화·검증 정책 |
| 프로젝트가 어떤 게임인가 | `docs/superpowers/specs/2026-07-23-project-core-design.md` | 확정 코어, 불변·변경·재승인·제외 경계 |
| 통합 게임 구조는 무엇인가 | `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md` | 코어 기반 통합 시스템 설명, 구현/계획 분리 |
| main에서 현재 무엇이 구현됐는가 | `ACTIVE_CONTEXT.md`, `docs/MVP-003_IMPLEMENTATION_STATUS.md`, 실제 Script·Scene·Test | 기존 Prototype·장비 생애 PoC 구현 사실. 시작 문서 stale Finding은 `BS-AUD-F11`로 추적 |
| 현재 개발 순서는 무엇인가 | `ROADMAP.md` | Prototype→PoC→확장 게이트. 최신 v9 계획은 `BLACKSMITH_REMAINING_PLANNING_STATUS_2026.md`가 우선 |
| 통과·미실행·차단 상태는 무엇인가 | `DEVELOPMENT_GATES.md` | 게이트별 증거와 판정. stale 상태는 `BS-AUD-F11`로 추적 |
| 장비 생애 PoC의 상세 규칙은 무엇인가 | `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md` | 철검·검투사 첫 생애 PoC 역사 명세 |
| MVP-003의 구현 경계는 무엇인가 | `docs/MVP-003_SCOPE.md` | Issue #34 포함·제외·완료 기준 |
| 어떤 순서로 구현했는가 | `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md` | Task 1~9 구현계획 이력 |
| Actions 비용·실행 정책은 무엇인가 | `docs/CI_EXECUTION_POLICY.md` | 변경 유형별 CI와 main/nightly 정책 |
| 수동 Godot 검증 경로는 무엇인가 | `docs/GODOT_PLAYTEST.md` | 기존 Prototype·장비 생애 PoC 사람 검증 절차 |
| 과거 최종 적대적 검토 증거는 무엇인가 | `docs/FINAL_ADVERSARIAL_REVIEW_REPORT.md` | 당시 PoC 범위의 검토 이력. 최신 v9 감사가 우선 |
| 현재 main 강화 수치와 위험은 무엇인가 | `data/crafting/enhancement_balance.json` | 구형 구현 수치. 최신 v9 마이그레이션 전까지 구현 사실만 책임 |
| 현재 main 제작 등급 데이터는 무엇인가 | `data/crafting/craftsmanship_grades.json` | 구형 5개 런타임 ID 구현 사실. 현행 제품 목표는 `BS-GRADE-20260801-02`; `BS-AUD-F04`로 충돌 추적 |
| 현재 main 수식어 이정표는 무엇인가 | `data/crafting/enhancement_milestones.json` | 구형 3슬롯 구현 데이터. `BS-AUD-F05`로 충돌 추적 |
| Base 기준은 무엇인가 | `docs/BASE_RULES_VERSION.md`, `skills/PROJECT_BASE_ADAPTER.json` | 버전 표기 drift는 `BS-AUD-F12`로 추적하며 Draft 목표는 Base v9.3 |
| Base 적용 검증은 무엇인가 | `docs/BASE_ADOPTION_AUDIT.md` | Base 기능 매핑과 CI 증거 |
| 문서 발행 정책은 무엇인가 | `DESIGN_DOCUMENT_REGISTRY.json` | source, status, output, manifest, policy |
| Skill 라우팅은 무엇인가 | `SKILL_REGISTRY.json` | trigger·mode·owner |

## MVP 정본

| MVP | 책임 원본 | 상태 |
|---|---|---|
| MVP-001 제작 | `docs/MVP-001_SCOPE.md` | 구현·자동 검증 PASS 이력, 사람/Android 미검증 |
| MVP-002 강화·보관·자동 단조 | `docs/MVP-002_SCOPE.md` | 구형 Prototype 구현. 최신 자동화 경계 충돌은 `BS-AUD-F06` |
| MVP-003 장비 한 점의 생애 | `docs/MVP-003_SCOPE.md`, `docs/MVP-003_IMPLEMENTATION_STATUS.md` | `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING` |
| MVP-004 상인 납품 | Game Bible·Roadmap의 후속 항목 | 최신 판매 채널 재정의 필요, `BS-AUD-F18` |

## 현재 Issue·PR

- 현재 기획 추적 Issue: #79
- 현재 기획 Draft PR: #81 · `SAVE_DESIGN_COMPLETE / FINDINGS_OPEN / NOT_MERGED`
- 최신 감사: `BS-REPO-AUDIT-20260801-01` · P0 10·P1 10·P2 6
- 최신 저장 결정: `BS-SAVE-20260801-01` · 단일 캠페인·자동 백업 2개·AttemptIntent·ResultEnvelope
- 최신 제작 등급: `BS-GRADE-20260801-02` · 보통→우수→명품→걸작→전설
- 구형 제작 등급 결정: `BS-V9-20260731-01`, `BS-GRADE-20260801-01` · `SUPERSEDED`
- 승인된 화면 결정: `BS-MAIN-20260801-01`, `BS-SHELL-20260801-01`
- 승인된 시각 결정: `BS-ART-20260731-01`, `BS-MODAK-20260731-01`
- 비주얼 보드: `BS-VISUAL-20260731-01 / USER_ACCEPTED_WORKING_BASELINE / FINAL_ASSET_NO`
- 현재 구현 검증 Issue: #34 · 사람·플랫폼·외부 플레이 검증까지 유지
- MVP-003 구현 PR: #35 · `MERGED`, merge commit `639c33611c203581c8dcbc08c85425455b16991a`
- 사람·Android·성능·외부 플레이: `NOT_RUN`
- Codex·제품 구현: `BLOCKED_UNTIL_기획완료_AND_검수완료`

## 역사 문서

`CHANGELOG.md`, 과거 Decision, 닫힌 Issue·PR은 당시 사실을 보존한다. 역사 표현은 현행 정본으로 사용하지 않으며, 활성 시작 문서가 역사 상태를 현재 상태처럼 가리키면 `BS-AUD-F11` 결함이다. 제작 등급의 과거 결정은 이력으로만 유지하고 현행 질문에는 `BS-GRADE-20260801-02`를 사용한다.
