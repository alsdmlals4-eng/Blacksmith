# [현재 정본] Documentation Map

## 원칙

- 현재 Decision: `CURRENT_CONFIRMED_DECISIONS.md`
- 기계 판독 정본: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- 통합 설계: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- 구형 상태: `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`
- 실제 구현 사실: Script·Scene·Resource·data·tests
- Google Sheet는 GitHub 정본을 덮어쓰지 않으며 같은 Decision ID를 연결한다.

## 현재 운영 상태

| 질문 | 책임 원본 | 상태 |
|---|---|---|
| 현재 승인 Decision | `CURRENT_CONFIRMED_DECISIONS.md` | `CURRENT / R2_BATCH_004_2_OF_10` |
| 현재 기계 정본 | `docs/planning/CURRENT_R2_CANON_REGISTRY.json` | `CURRENT / SCHEMA_8` |
| 현재 통합 GDD | `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md` | `CURRENT` |
| 현재 세션 상태 | `ACTIVE_CONTEXT.md` | `CURRENT` |
| Gate·순서 | `DEVELOPMENT_GATES.md` / `ROADMAP.md` | `CURRENT` |
| 작업 규칙 | `AGENTS.md` | `CURRENT / BENCHMARK_TDD_CHECKPOINT` |

## 분야별 책임 원본

| 질문 | 책임 원본 | Decision |
|---|---|---|
| 제작 등급 5단계 | `docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md` | `BS-CRAFT-20260804-07` |
| 예술성 숫자형 능력치 | `docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md` | `BS-CRAFT-20260805-01` |
| 아이템화 벤치마킹 | `docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md` | `BS-OPS-20260805-01` |
| 세 수식어 | `docs/planning/BLACKSMITH_R2_THREE_AFFIX_SLOT_ARCHITECTURE_CANON_2026.md` | `BS-CRAFT-20260804-06` |
| 정밀강화 | `docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md` | `BS-CRAFT-20260804-04` |
| 촉매 계보 | `docs/planning/BLACKSMITH_R2_CATALYST_AFFIX_SEED_EVOLUTION_AND_MUTATION_CANON_2026.md` | `BS-CRAFT-20260804-05` |
| 장비명·연대기 상세 | `docs/planning/BLACKSMITH_R2_CHRONICLE_AFFIX_DETAIL_INTERACTION_CANON_2026.md` | `BS-UX-20260804-01` |
| 고객 정보 | `docs/planning/BLACKSMITH_R2_CUSTOMER_DISCLOSURE_MINIMUM_CANON_2026.md` | `BS-CUSTOMER-20260803-02` |
| 일정 표시 | `docs/planning/BLACKSMITH_R2_MULTI_SCHEDULE_DISPLAY_AND_ALERT_CANON_2026.md` | `BS-SCHEDULE-20260804-01` |

## 현재 작품 구조

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

```text
제작 등급: 보통 / 우수 / 명품 / 걸작 / 전설
예술성: 1~10, 단계명 없음
```

## 구형 라우팅

| 문서·모델 | 상태 | 대체 |
|---|---|---|
| 4등급 제작 문서 | `[대체됨]` | 5등급 정본 |
| `STANDARD / GOOD / PERFECT` runtime | `[역사 증거]` | 현재 제품 구현 아님 |
| 예술성 named visual tiers | `[대체됨]` | 숫자형 예술성 정본 |
| R1 Game Bible | `[부분 대체됨]` | Current R2 Game Bible |
| PR #81 | 전체 병합 `[폐기]` / 선별 `[보류]` | 별도 소형 PR |

## 배치·검증

- `R2_BATCH_004: 2/10`
- 최대 배치 크기: 10
- 조기 체크포인트: 고위험 충돌·세션 종료·정본 영향 큼
- TDD: `RED → GREEN → REFACTOR`
- TDD RED run `33`: expected failure observed
- GREEN exact-head: `PENDING`
- 제품 구현: `BLOCKED`
