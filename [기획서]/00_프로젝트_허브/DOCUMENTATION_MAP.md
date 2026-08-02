# Documentation Map

## 1. 원칙

- 한 질문에는 현행 책임 원본 하나만 둔다.
- Root Decision 상태는 `CURRENT_CONFIRMED_DECISIONS.md`가 책임진다.
- 분야의 상세 서술 계약은 등록된 Markdown 하나가 책임진다.
- ID·수치·관계·게임 데이터는 등록된 JSON 또는 실제 `data/**/*.json`이 책임진다.
- 실제 구현 사실은 Script·Scene·Resource·Data·Test가 책임진다.
- 완료 증거는 정확한 현재 HEAD의 테스트·런타임·캡처·프로파일·사람 검수가 책임진다.
- Google Sheet는 `USER_FACING_GDD_WORKSPACE`이며 GitHub 정본을 독립적으로 덮어쓰지 않는다.
- PDF·DOCX·Dashboard·이미지 보드는 사람용 파생본 또는 기획 Evidence이며 정본·실제 구현·검증과 구분한다.

## 2. 현재 시작 경로

```text
AGENTS.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ ROADMAP.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ SKILL_REGISTRY.json
→ 현재 기획 Bundle·분야 정본
→ 실제 구현·데이터·테스트
```

## 3. 현재 운영 책임 원본

| 질문 | 현행 책임 원본 | 상태 |
|---|---|---|
| 현재 승인 Decision은 무엇인가 | `CURRENT_CONFIRMED_DECISIONS.md` | `CURRENT` |
| 현재 프로젝트 단계·Branch·PR·다음 작업은 무엇인가 | `ACTIVE_CONTEXT.md` | `CURRENT` |
| 처음 무엇을 읽는가 | `START_HERE.md` | `CURRENT` |
| 무엇을 변경할 수 있고 어떤 절차를 따르는가 | `AGENTS.md` | `CURRENT` |
| 어떤 문서가 어떤 질문을 책임지는가 | `DOCUMENTATION_MAP.md` | `CURRENT` |
| 어떤 Gate가 통과·미실행·차단됐는가 | `DEVELOPMENT_GATES.md` | `CURRENT` |
| 총기획과 구현의 순서는 무엇인가 | `ROADMAP.md` | `CURRENT` |
| 운영 복구의 사실·Finding 기준선은 무엇인가 | `docs/operations/BS-OPS-20260802-01_BASELINE.md` | `CURRENT` |
| 승인된 복구 설계는 무엇인가 | `docs/superpowers/specs/2026-08-02-planning-canon-recovery-design.md` | `CURRENT` |
| 복구 실행 계획은 무엇인가 | `docs/superpowers/plans/2026-08-02-blacksmith-planning-canon-recovery.md` | `CURRENT` |
| Base 적용 입력은 무엇인가 | `skills/PROJECT_BASE_ADAPTER.json` | `CURRENT_INPUT / CORRECTION_IN_PROGRESS` |
| Base release·프로젝트 적용 구분은 무엇인가 | `docs/BASE_V9_4_ADOPTION.md` | `CURRENT / CORRECTION_IN_PROGRESS` |
| 프로젝트 운영 Health는 무엇인가 | `docs/PROJECT_OPERATING_HEALTH.json` | `CURRENT_DERIVATIVE / CORRECTION_IN_PROGRESS` |
| 문서 등록·발행 상태는 무엇인가 | `DESIGN_DOCUMENT_REGISTRY.json` | `CURRENT / CORRECTION_IN_PROGRESS` |
| Skill 라우팅은 무엇인가 | `SKILL_REGISTRY.json` | `CURRENT / CORRECTION_IN_PROGRESS` |

## 4. 기획 책임 구조

운영 복구 완료 전에는 기존 분야 문서를 전체 current canon으로 자동 승격하지 않는다. 각 Bundle이 한 영역의 책임 원본을 선별·통합·갱신한다.

| Bundle | 질문 | 현재 입력 | 목표 책임 원본 상태 |
|---|---|---|---|
| R1 | 이 게임은 누구에게 어떤 약속을 주며 무엇이 뾰족한 재미인가 | Project Core spec, Game Bible, 승인 Decision, 실제 구현, PR #81 | `CURRENT_CANON_AFTER_USER_REVIEW` |
| R2 | Core·Session·Meta Loop와 승패·복구·보상은 어떻게 이어지는가 | Game Bible, 강화·고객·세계 환류 자료 | `CURRENT_CANON_AFTER_USER_REVIEW` |
| R3 | 제작·강화·작품 정체성·실패·파괴·저장은 어떤 계약인가 | 승인 Grade/Save, 실제 crafting data/scripts, PR #81 proposals | `CURRENT_CANON_AFTER_USER_REVIEW` |
| R4 | 고객·판매·세계 결과·장비 연대기는 어떻게 이어지는가 | 기존 lifecycle PoC, customer proposals, world records | `CURRENT_CANON_AFTER_USER_REVIEW` |
| R5 | 경제·성장·장기 목표와 악용 방지는 무엇인가 | enhancement balance, simulations, endgame proposals | `CURRENT_CANON_AFTER_USER_REVIEW` |
| R6 | 모바일 UX·접근성·아트·오디오·피드백은 무엇인가 | 승인 Art/Modak/Main/Shell, UI proposals, actual scenes | `CURRENT_CANON_AFTER_USER_REVIEW` |
| R7 | 버티컬 슬라이스·데이터·Migration·검증·제작 계획은 무엇인가 | all approved bundles, actual repo, validation proposals | `CURRENT_CANON_AFTER_USER_REVIEW` |
| R8 | 전체 기획에 충돌·누락·과도한 범위가 남았는가 | R1~R7 canon and actual implementation | `FINAL_REVIEW` |

## 5. 승인 증거가 확인된 기획

현재 Root Decision entrypoint가 책임지는 승인 기획:

| Decision | 주제 | 상세 Draft source | 현재 상태 |
|---|---|---|---|
| `BS-ART-20260731-01` | 스타일라이즈드 다크 포지 | PR #81 art/Modak canon | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` |
| `BS-MODAK-20260731-01` | 밝은 불 정령 모닥 | PR #81 art/Modak canon | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` |
| `BS-MAIN-20260801-01` | 별도 메인 화면 | PR #81 main/app-shell canon | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` |
| `BS-SHELL-20260801-01` | 단일 BlacksmithApp | PR #81 main/app-shell canon | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` |
| `BS-GRADE-20260801-02` | 제작 등급 5단계 | PR #81 grade canon | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` |
| `BS-SAVE-20260801-01` | 저장·이어하기·ResultEnvelope | PR #81 save canon | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` |

상세 Draft source는 선별 승격 전까지 현행 main 책임 원본이 아니다. Root entrypoint가 결정의 현재 상태와 최소 계약을 책임진다.

## 6. 실제 구현 책임 원본

| 질문 | 실제 책임 원본 | 현재 상태 |
|---|---|---|
| 현재 앱 시작 Scene은 무엇인가 | `project.godot` | `enhancement_test.tscn / TEST_ENTRY` |
| 제작 데이터·규칙은 무엇인가 | `data/crafting/*.json`, 관련 scripts/tests | `REFERENCE_IMPLEMENTATION` |
| 강화 확률·실패·보정·가격은 무엇인가 | `data/crafting/enhancement_balance.json` | `REFERENCE_IMPLEMENTATION / R3·R5_REVIEW_REQUIRED` |
| 강화 이정표는 무엇인가 | `data/crafting/enhancement_milestones.json` | `REFERENCE_IMPLEMENTATION / R3_REVIEW_REQUIRED` |
| 기존 장비 생애 PoC는 무엇인가 | `docs/MVP-003_SCOPE.md`, actual lifecycle scripts/scenes/tests | `REFERENCE_IMPLEMENTATION` |
| 기존 자동 검증 이력은 무엇인가 | tests, workflow results, historical status docs | `HISTORICAL_EVIDENCE` |
| 승인 Main/Shell/Save는 구현됐는가 | actual Scene/Script/Data | `NO / NOT_IMPLEMENTED` |

기존 구현을 삭제하거나 되돌리지 않는다. 최신 기획과의 정합 여부는 분야별로 별도 판정한다.

## 7. PR·Issue·Sheet 책임

| Surface | 역할 | 상태 |
|---|---|---|
| Issue #79 | 총기획 Umbrella | `ACTIVE / V9_4_UPDATE_REQUIRED` |
| PR #84 | 운영·정본 복구 | `ACTIVE_DRAFT` |
| PR #81 | 기획·승인 Evidence Source | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |
| Issue #60 | Base v6 전면 재기획 이력 | `HISTORY_ONLY_CANDIDATE` |
| Google Sheet | 사용자용 GDD·운영·결정·감사·이력 Surface | `SYNC_IN_PROGRESS_BS-OPS-20260802-01` |

PR #81의 181 commits와 88 changed files는 전체 병합하지 않는다. 승인 증거·현행 코어·분야 충돌을 검토한 뒤 필요한 문서·계약만 current branch에 새 정본 또는 현행 정본 갱신으로 반영한다.

## 8. Base와 Skill 경계

- 현재 released Base adoption: `9.4.0`.
- 프로젝트 고유 기획·용어·수치·경로·에셋은 Blacksmith에 유지한다.
- 공용 절차는 Base Skill을 프로젝트 Adapter로 라우팅한다.
- 새 프로젝트 Skill은 기존 공용/프로젝트 책임에 흡수할 수 없고 반복 가능한 독립 계약일 때만 만든다.
- 모든 Skill을 로드하지 않고 Trigger 기반 최소 Skill만 사용한다.
- 생성 호환 뷰는 generator를 실행할 수 있을 때만 재생성한다.

## 9. 파생본·시각 자료

| Surface | 역할 | 현행 판정 |
|---|---|---|
| Google Sheet | 사용자용 계획·GDD·Decision·Audit | `ACTIVE_CONSUMER / SYNC_IN_PROGRESS` |
| PDF·DOCX | 배포용 파생본 | `NOT_CURRENTLY_AUDITED` |
| 비주얼 화면 보드 | 기획 Evidence·시각 후보 | `REFERENCE_OR_PROPOSED` |
| 최종 제품 아트 | 실제 제품 자산 | `NOT_CREATED_OR_NOT_APPROVED` |
| Manifest·License Ledger | 자산 추적 계약 | `PROPOSED_REVIEW_REQUIRED` |

이미지·문서 존재를 실제 엔진 구현이나 접근성·런타임 검증으로 오인하지 않는다.

## 10. 역사 자료

다음은 역사·비교·회귀 자료로 유지한다.

- 과거 DEC-001~DEC-025와 구현 기준선
- MVP-001·002·003 Scope와 상태 문서
- Issue #29·#34·#60
- PR #35·#57·#58·#59·#61·#62·#81
- 과거 Base v6·v8·v9.1·v9.3 적용 문서
- 과거 CI·Godot 자동 검증

역사 자료가 현재 시작 경로·다음 작업·현재 Base·현재 Decision을 지시하면 `STALE_REFERENCE`다.

## 11. 콜드 스타트 확인 질문

새 작업자는 저장소만으로 다음에 답할 수 있어야 한다.

1. Blacksmith는 무엇을 만드는가?
2. 현재 단계와 Work Mode는 무엇인가?
3. 현재 Decision·Branch·PR은 무엇인가?
4. 무엇을 수정하면 안 되는가?
5. 어떤 기획이 승인됐고 어떤 것은 제안인가?
6. PR #81과 Issue #60은 어떤 역할인가?
7. 다음 기획 Bundle은 무엇인가?
8. 어떤 경우에 Grill Me를 사용하는가?
9. 상세 수치는 어떻게 기록하는가?
10. 어떤 검증이 NOT_RUN인가?
11. 주요 Decision은 어디에 동기화하는가?

답을 찾을 수 없거나 두 활성 원본이 서로 다르면 Documentation Map 또는 진입 문서를 우선 수정한다.
