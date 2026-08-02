# Documentation Map

## 1. 원칙

- 한 질문에는 현행 책임 원본 하나만 둔다.
- Root Decision 상태는 `CURRENT_CONFIRMED_DECISIONS.md`가 책임진다.
- 현재 R1 분야 정본의 라우팅은 `docs/planning/CURRENT_R1_CANON_REGISTRY.json`이 책임진다.
- 광역 문서·발행 인덱스는 `DESIGN_DOCUMENT_REGISTRY.json`이 책임지되, 현재 단계 메타데이터가 다르면 Root와 R1 overlay가 우선한다.
- 실제 구현 사실은 Script·Scene·Resource·data·tests가 책임진다.
- Google Sheet는 `USER_FACING_GDD_WORKSPACE`이며 GitHub 정본을 독립적으로 덮어쓰지 않는다.
- 문서 승인, 구현, 자동 검증, 런타임, Android, 접근성, 성능, 사람 플레이는 별도 상태다.

## 2. 현재 시작 경로

```text
AGENTS.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ docs/planning/CURRENT_R1_CANON_REGISTRY.json
→ START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ ROADMAP.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ SKILL_REGISTRY.json
→ 현재 R1 분야 정본
→ 실제 구현·data·tests
```

## 3. 현재 운영 책임 원본

| 질문 | 현행 책임 원본 | 상태 |
|---|---|---|
| 현재 승인 Decision은 무엇인가 | `CURRENT_CONFIRMED_DECISIONS.md` | `CURRENT` |
| 현재 R1 정본은 무엇인가 | `docs/planning/CURRENT_R1_CANON_REGISTRY.json` | `CURRENT` |
| 현재 단계·Branch·PR·다음 작업 | `ACTIVE_CONTEXT.md` | `CURRENT` |
| 처음 무엇을 읽는가 | `START_HERE.md` | `CURRENT` |
| 작업·보호·Grill Me·병합 규칙 | `AGENTS.md` | `CURRENT` |
| Gate 상태 | `DEVELOPMENT_GATES.md` | `CURRENT` |
| R1~R9 순서 | `ROADMAP.md` | `CURRENT` |
| R0 복구 기준선 | `docs/operations/BS-OPS-20260802-01_BASELINE.md` | `CURRENT_R0_EVIDENCE` |
| R0 최종 보고 | `docs/operations/BS-OPS-20260802-01_FINAL_REPORT.md` | `CURRENT_R0_EVIDENCE` |
| Base 적용 입력 | `skills/PROJECT_BASE_ADAPTER.json` | `CURRENT` |
| 운영 Health | `docs/PROJECT_OPERATING_HEALTH.json` | `CURRENT_DERIVATIVE` |
| 광역 문서·발행 인덱스 | `DESIGN_DOCUMENT_REGISTRY.json` | `R0_BROAD_INDEX / R1_OVERLAY_TAKES_PRECEDENCE` |
| Skill 라우팅 | `SKILL_REGISTRY.json` | `CURRENT` |

## 4. 현재 R1 책임 원본

| 질문 | 책임 원본 | Decision IDs |
|---|---|---|
| R1 승인 코어·세트 결정 원장 | `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md` | `BS-CORE-20260802-01~02`, `BS-SET-20260802-01~03` |
| 사건 연대기 세트 생성·보상 | `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md` | `BS-SET-20260802-02~03` |
| 실패 사건 세트·Grill Me 병합 운영 | `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md` | `BS-SET-20260802-04`, `BS-OPS-20260802-02` |
| 현재 R1 문서 라우팅 | `docs/planning/CURRENT_R1_CANON_REGISTRY.json` | 현재 R1 전체 |

## 5. 현재 승인된 R1 방향

- `BS-CORE-20260802-01`: 피로도·날짜 진행 핵심 불변.
- `BS-CORE-20260802-02`: 강화 메인, 고객·세계 환류는 휴식·장기 약속.
- `BS-SET-20260802-01`: 다양한 작품 제작 동기와 세트 시스템.
- `BS-SET-20260802-02`: 실제 기여 작품의 사건 연대기 세트.
- `BS-SET-20260802-03`: 범용 보정 + 상황 태그 + 역사 기록.
- `BS-SET-20260802-04`: 실패·참패도 실제 기여 시 세트 성립.

R1 전체 완료는 아니며 남은 코어·플레이어 약속 범위를 계속 작성한다.

## 6. 승인 증거가 확인된 기존 제품 기획

| Decision | 주제 | 현재 상태 |
|---|---|---|
| `BS-ART-20260731-01` | 스타일라이즈드 다크 포지 | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` |
| `BS-MODAK-20260731-01` | 밝은 불 정령 모닥 | `CONFIRMED / SELECTIVE_PROMOTION_PENDING` |
| `BS-MAIN-20260801-01` | 별도 Main Menu | `CONFIRMED / NOT_IMPLEMENTED` |
| `BS-SHELL-20260801-01` | 단일 BlacksmithApp | `CONFIRMED / NOT_IMPLEMENTED` |
| `BS-GRADE-20260801-02` | 제작 등급 5단계 | `CONFIRMED / DATA_MIGRATION_NOT_STARTED` |
| `BS-SAVE-20260801-01` | Save·Continue·ResultEnvelope | `CONFIRMED / NOT_IMPLEMENTED` |

## 7. 실제 구현 책임 원본

| 질문 | 실제 책임 원본 | 현재 상태 |
|---|---|---|
| 현재 앱 시작 Scene | `project.godot` | `enhancement_test.tscn / TEST_ENTRY` |
| 기존 제작 규칙 | `data/crafting/*.json`, scripts, tests | `REFERENCE_IMPLEMENTATION` |
| 기존 강화 규칙 | `data/crafting/enhancement_*.json`, scripts, tests | `REFERENCE_IMPLEMENTATION / R3·R5_REVIEW_REQUIRED` |
| 기존 장비 생애 PoC | `docs/MVP-003_SCOPE.md`, actual paths | `REFERENCE_IMPLEMENTATION` |
| 최신 피로도·날짜·세트 | actual runtime paths | `NOT_IMPLEMENTED` |
| 최신 Main/Shell/Save | actual runtime paths | `NOT_IMPLEMENTED` |

기존 구현을 삭제하거나 되돌리지 않는다. 최신 기획과의 정합 여부는 분야별로 별도 판정한다.

## 8. PR·Issue·Sheet 책임

| Surface | 역할 | 상태 |
|---|---|---|
| Issue #79 | 총기획 Umbrella | `ACTIVE` |
| PR #84 | R0 복구 + R1 승인 배치 01 | `ACTIVE_DRAFT / PREMERGE_AUDIT` |
| PR #81 | 기획·승인 Evidence Source | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |
| Issue #60 | 과거 Base v6 재기획 | `HISTORY_ONLY_CANDIDATE` |
| Google Sheet | 사용자용 GDD·Decision·Audit·History | `PREMERGE_RECHECK` |

## 9. Grill Me 병합 책임

`BS-OPS-20260802-02`:

- 이번 질문 5건은 PR #84 사전 감사 후 즉시 squash 병합.
- 병합 후 신규 카운터 `0/10`.
- 이후 새 승인 10건마다 같은 감사·병합 절차 반복.
- 병합 직전 GitHub 정본·Sheet·changed files·리뷰·CI·충돌·금지 경로 확인.
- P0/P1 발견 시 병합 중단.
- 병합 후 main SHA를 Root·Sheet·다음 진입점에 기록.

## 10. Base와 Skill 경계

- released Base adoption: `9.4.0`.
- 프로젝트 고유 기획·용어·수치·경로·assets는 Blacksmith에 유지한다.
- 공용 절차는 Base Skill을 프로젝트 Adapter로 라우팅한다.
- 새 Skill은 기존 책임에 흡수할 수 없고 반복 가능한 독립 계약일 때만 만든다.
- Trigger 기반 최소 Skill만 사용한다.

## 11. 검증 경계

현재 가능한 증거:

- GitHub PR metadata·changed filenames·diff·mergeability
- GitHub 파일 readback
- Google Sheet bounded readback
- Decision ID·경로·Commit 비교

현재 제한:

- local checkout/static validators: `BLOCKED_UNVERIFIED` — container GitHub DNS 실패
- Godot runtime: `NOT_RUN`
- Android: `NOT_RUN`
- accessibility human: `NOT_RUN`
- performance: `NOT_RUN`
- external playtest: `NOT_RUN`

## 12. 콜드 스타트 확인 질문

새 작업자는 저장소만으로 다음에 답할 수 있어야 한다.

1. 현재 단계와 Work Mode는 무엇인가?
2. 현재 운영 Decision은 무엇인가?
3. 승인된 R1 결정은 무엇인가?
4. 어떤 문서가 사건 연대기 세트를 책임지는가?
5. 실패 사건도 세트가 되는가?
6. Grill Me는 언제 병합하는가?
7. 무엇을 수정하면 안 되는가?
8. PR #81과 Issue #60은 어떤 역할인가?
9. 어떤 검증이 `NOT_RUN`인가?
10. 다음 작업은 병합인가, 제품 구현인가, R1 계속인가?

답이 두 활성 원본에서 다르면 Root·Map·Hub를 먼저 수정한다.
