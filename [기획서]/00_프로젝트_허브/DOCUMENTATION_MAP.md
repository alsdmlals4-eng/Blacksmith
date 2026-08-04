# [현재 정본] Documentation Map

## 1. 원칙

- 한 질문에는 현행 책임 원본 하나만 둔다.
- 현재 Decision 상태는 `CURRENT_CONFIRMED_DECISIONS.md`가 책임진다.
- 현재 R2 분야 정본 라우팅은 `docs/planning/CURRENT_R2_CANON_REGISTRY.json`이 책임진다.
- 통합 현재 설계는 `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`가 책임진다.
- 광역 문서 라우팅은 `DESIGN_DOCUMENT_REGISTRY.json`이 책임진다.
- 구형 문서 상태는 `BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`이 책임진다.
- 실제 구현 사실은 Script·Scene·Resource·data·tests가 책임진다.
- Google Sheet는 사용자-facing 계획 작업공간이며 GitHub 정본을 독립적으로 덮어쓰지 않는다.
- 승인·병합·구현·자동 검증·runtime·Android·접근성·성능·사람 플레이는 별도 상태다.

## 2. 현재 시작 경로

```text
AGENTS.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ docs/planning/CURRENT_R2_CANON_REGISTRY.json
→ docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md
→ START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ ROADMAP.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 분야별 최신 R2 정본
→ 실제 구현·data·tests
```

## 3. 현재 운영 책임 원본

| 질문 | 현행 책임 원본 | 상태 |
|---|---|---|
| 현재 승인 Decision | `CURRENT_CONFIRMED_DECISIONS.md` | `CURRENT / R2_BATCH_004_1_OF_10` |
| 현재 기계 판독 정본 | `docs/planning/CURRENT_R2_CANON_REGISTRY.json` | `CURRENT / COUNTER_1_OF_10` |
| 통합 현재 Game Bible | `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md` | `CURRENT` |
| 현재 단계·최근 병합·다음 작업 | `ACTIVE_CONTEXT.md` | `CURRENT` |
| 처음 읽을 문서 | `START_HERE.md` | `CURRENT` |
| 작업·보호·병합 규칙 | `AGENTS.md` | `CURRENT` |
| Gate 상태 | `DEVELOPMENT_GATES.md` | `CURRENT` |
| R1~R9 순서 | `ROADMAP.md` | `CURRENT` |
| 문서 라우팅 | `DESIGN_DOCUMENT_REGISTRY.json` | `CURRENT_R2_ROUTER` |
| 구형 파일 상태 | `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json` | `CURRENT / SCHEMA_2` |
| 정본 적대적 감사 | `docs/planning/BLACKSMITH_CANON_ADVERSARIAL_REVIEW_AND_LEGACY_STATUS_2026-08-04.md` | `MERGED_PR105` |
| Base 적용 입력 | `skills/PROJECT_BASE_ADAPTER.json` | `CURRENT_BASE_ADAPTER` |
| 운영 Health | `docs/PROJECT_OPERATING_HEALTH.json` | `DERIVATIVE / REGENERATE_AFTER_CANON_MERGE` |

## 4. 분야별 현재 책임 원본

| 질문 | 책임 원본 | Decision |
|---|---|---|
| 고객 능력·위험·성공률 공개 | `docs/planning/BLACKSMITH_R2_CUSTOMER_DISCLOSURE_MINIMUM_CANON_2026.md` | `BS-CUSTOMER-20260803-02` |
| 개인·세계 일정 분리 | Current R2 Registry + 고객 일정 정본 | `BS-WORLD-20260803-03` |
| 다중 일정 표시·알림 | `docs/planning/BLACKSMITH_R2_MULTI_SCHEDULE_DISPLAY_AND_ALERT_CANON_2026.md` | `BS-SCHEDULE-20260804-01` |
| 콘텐츠 구성·작품 환류 | `docs/planning/BLACKSMITH_R2_CONTENT_COMPOSITION_AND_ITEM_LEGACY_CANON_2026.md` | `BS-CONTENT-20260804-01` |
| 방문 고객·콘텐츠 가족 | `docs/planning/BLACKSMITH_R2_VISITOR_ARCHETYPES_AND_INITIAL_CONTENT_FAMILIES_CANON_2026.md` | `BS-CONTENT-20260804-02` |
| 예술성·실용성·가격 | `docs/planning/BLACKSMITH_R2_ARTISTRY_VALUE_AND_UTILITY_CRAFTING_CANON_2026.md` | `BS-CRAFT-20260804-01` |
| 예술성 표시·임시 시각 프리셋 | `docs/planning/BLACKSMITH_R2_ARTISTRY_MINIMUM_SCALE_PRICE_AFFIX_VISUAL_PRESET_CANON_2026.md` | `BS-CRAFT-20260804-02 / TIER_LABEL_REFINEMENT_PENDING` |
| 정밀강화 역할 | `docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md` | `BS-CRAFT-20260804-04` |
| 촉매 수식어 계보 | `docs/planning/BLACKSMITH_R2_CATALYST_AFFIX_SEED_EVOLUTION_AND_MUTATION_CANON_2026.md` | `BS-CRAFT-20260804-05` |
| 세 수식어 슬롯 | `docs/planning/BLACKSMITH_R2_THREE_AFFIX_SLOT_ARCHITECTURE_CANON_2026.md` | `BS-CRAFT-20260804-06` |
| 제작 등급 4단계·출생 전설 | `docs/planning/BLACKSMITH_R2_FOUR_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md` | `BS-CRAFT-20260804-07` |
| 장비명·연대기 상세 | `docs/planning/BLACKSMITH_R2_CHRONICLE_AFFIX_DETAIL_INTERACTION_CANON_2026.md` | `BS-UX-20260804-01` |

## 5. 현재 작품 구조

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

제작 등급:

```text
[보통] → [우수] → [걸작] → [전설]
```

- 등급 수식어: 최초 제작 완성도, 동일 UID 고정
- `전설`: 최초 제작에서만 극희귀하게 발생, 후천 승격 없음
- 촉매 수식어: 정밀강화 촉매 이력, 확률적 성장
- 연대기 수식어: 실제 작품 생애, 사건 기반 성장
- 예술성: 미적 가치의 별도 `1~10` 축
- 보조재료 슬롯 없음
- 일반 수식어 A·B 현재 구조 아님

## 6. 제작 등급 권위 분리

| 모델 | 상태 | 사용 범위 |
|---|---|---|
| `STANDARD / GOOD / PERFECT` | `[역사 증거]` | 과거 runtime·data·자동 테스트 기준선 |
| `보통 / 우수 / 명품 / 걸작 / 전설` | `[대체됨]` | PR #81의 구형 5단계안 |
| `보통 / 우수 / 걸작 / 전설` | `[현재 정본]` | 현재 제품 기획, 구현은 `BLOCKED` |

과거 3단계 구현 PASS는 현재 4단계 제품 구현 PASS가 아니다.

## 7. R1·역사 문서 역할

| 문서 | 상태 | 사용 범위 |
|---|---|---|
| `docs/planning/CURRENT_R1_CANON_REGISTRY.json` | `[역사 증거] / R2_REFINED` | 승인된 R1 기반과 supersession 추적 |
| `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md` | `[부분 대체됨]` | R1 역사 진입점, 현재 R2 Game Bible 안내 |
| `docs/MVP-003_SCOPE.md` | `[역사 증거] [보류]` | 과거 Reference Implementation |
| 장비 생애 PoC 명세 | `[역사 증거] [보류]` | 과거 문제 정의·검증 흐름 |
| 과거 적대적 보고서 | `[대체됨]` | 당시 검토 과정 연구 |

역사 문서는 현재 R2 정본을 덮어쓰지 않는다.

## 8. PR #81 처리

```text
전체 병합 단위: [폐기]
브랜치·원 승인 원문: [역사 증거]
분야별 선별 이관: [보류]
```

`BS-GRADE-20260801-02`의 5단계 제작 등급은 `BS-CRAFT-20260804-07`의 4단계로 `[대체됨]`이다.

## 9. 실제 구현과 역사 명세

| 질문 | 책임 원본 | 현재 상태 |
|---|---|---|
| 현재 앱 시작 Scene | `project.godot` | `enhancement_test.tscn / TEST_ENTRY` |
| 기존 제작·강화 Script·data | 실제 경로 | `REFERENCE_IMPLEMENTATION / HISTORICAL_THREE_GRADE_BASELINE` |
| 기존 장비 생애 PoC | 상태 표시된 MVP-003·PoC 명세 | `HISTORICAL_EVIDENCE / HOLD` |
| 4단계 제작 등급 제품 구현 | 향후 R3 제품 경로 | `NOT_IMPLEMENTED / BLOCKED` |
| 최신 R2 기능 runtime | 향후 R3~R7 제품 경로 | `NOT_IMPLEMENTED / BLOCKED` |
| 최신 Android·접근성·성능·사람 플레이 | 향후 검증 증거 | `NOT_RUN` |

## 10. PR·Issue·Sheet 책임

| Surface | 역할 | 상태 |
|---|---|---|
| Issue #79 | 총기획 Umbrella | `ACTIVE` |
| PR #103 | R2 체크포인트 003 정본 | `MERGED / SQUASH` |
| PR #104 | 체크포인트 003 사후 폐쇄 | `MERGED / SQUASH` |
| PR #105 | 정본 적대적 감사·구형 상태 분류 | `MERGED / SQUASH` |
| R2 Batch 004 Draft PR | 승인 Decision 누적 | `1_OF_10 / DO_NOT_MERGE_YET` |
| PR #81 | v9 참고 자산 | `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT` |
| Google Sheet | GDD·Decision·Audit·History | `SAME_ID_SYNC_REQUIRED` |

## 11. 승인 배치 책임

- 체크포인트 003의 승인 10건은 PR #103으로 병합 완료했다.
- PR #104가 pending 상태를 폐쇄했고 PR #105가 정본 감사를 병합했다.
- 현재 `R2_BATCH_004` 카운터는 `1/10`이다.
- 현재 Decision은 `BS-CRAFT-20260804-07`이다.
- 새 승인 최대 10건마다 적대적 감사·정본 동기화·expected-head squash 절차를 반복한다.
- P0/P1이 열려 있으면 병합하지 않는다.

## 12. 검증 경계

- PR #103/#104/#105 exact-head Base·Python·Godot: `PASS`
- 현재 Batch 004 Draft PR: exact-head 검증 필요
- 제품 경로 변경: `0`
- focused planning test standalone: 직접 실행 전 `NOT_RUN`
- 최신 runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
- 제품 구현: `BLOCKED`

## 13. 콜드 스타트 질문

1. 현재 단계와 Decision은 무엇인가?
2. 현재 제작 등급 네 단계와 `전설` 생성 시점은 무엇인가?
3. 작품 수식어 세 슬롯은 무엇인가?
4. 제작 등급·예술성·촉매·연대기의 책임은 어떻게 다른가?
5. 개인 일정과 세계 일정은 어떻게 다른가?
6. 현재 승인 카운터와 병합 조건은 무엇인가?
7. PR #81과 과거 3단계 구현은 어떤 상태인가?
8. 어떤 검증이 아직 `NOT_RUN`인가?
9. 제품 구현이 왜 `BLOCKED`인가?

답이 활성 원본 사이에서 다르면 Current Decisions·R2 Registry·R2 Game Bible·Hub를 먼저 교정한다.
