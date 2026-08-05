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
| 현재 승인 Decision | `CURRENT_CONFIRMED_DECISIONS.md` | `CURRENT / R2_BATCH_005_5_OF_10` |
| 현재 기계 정본 | `docs/planning/CURRENT_R2_CANON_REGISTRY.json` | `CURRENT / SCHEMA_8` |
| 현재 통합 GDD | `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md` | `CURRENT` |
| 현재 세션 상태 | `ACTIVE_CONTEXT.md` | `CURRENT` |
| Gate·순서 | `DEVELOPMENT_GATES.md` / `ROADMAP.md` | `CURRENT` |
| 작업 규칙 | `AGENTS.md` | `CURRENT / BENCHMARK_TDD_CHECKPOINT` |

## 체크포인트

```text
R2_CHECKPOINT_004
PR106_HEAD_227b2dabf0d98832811415156e72f65d601332a9
MERGE_789c73f38003f40dde5e9a99cd7dcb3ca03863f7
CLOSURE_PR107
R2_BATCH_004_CLOSED_2_OF_10
R2_BATCH_005_4_OF_10
```

## 분야별 책임 원본

| 질문 | 책임 원본 | Decision |
|---|---|---|
| 제작 등급 5단계 | `docs/planning/BLACKSMITH_R2_FIVE_TIER_CRAFTING_GRADE_AND_BIRTH_LEGEND_CANON_2026.md` | `BS-CRAFT-20260804-07 / MERGED_PR106` |
| 예술성 원수치 능력치 | `docs/planning/BLACKSMITH_R2_ARTISTRY_AS_NUMERIC_WEAPON_STAT_CANON_2026.md` | `BS-CRAFT-20260805-01 / MERGED_PR106` |
| 예술성 생성·성장·가치 평가 | `docs/planning/BLACKSMITH_R2_ARTISTRY_GENERATION_GROWTH_AND_VALUATION_CANON_2026.md` | `BS-CRAFT-20260805-02 / R2_BATCH_005_4_OF_10` |
| 예술성 설계 명세 | `docs/superpowers/specs/2026-08-05-artistry-generation-growth-economy-design.md` | `BS-CRAFT-20260805-02 / APPROVED_INPUT` |
| 예술성 구현 계획 | `docs/superpowers/plans/2026-08-05-artistry-generation-growth-economy.md` | `BS-CRAFT-20260805-02 / EXECUTION_PLAN` |
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
제작 등급: 보통 / 우수 / 명품 / 걸작 / 전설
예술성: 0 이상의 정수, 고정 설계 최대치 없음, 예술성 27 원수치 표기
```

## 예술성 책임 경계

```text
artistry = UID persisted stat
artistry_value = context derived, not persisted
customer_artistry_fit = context derived, not persisted
```

- 최초 생성: 설계 미적 성향·재료 시각/가공 적합성·직접 단조 미적 결과
- 후천 성장: `ARTISTIC_FINISH`·예술성 책임 촉매·승인된 세공/마감·의미 있는 재작업
- 가치: 구성요소별 가산 + 예술성 구간별 한계 가치 점감
- 고객: `IGNORE / SECONDARY / PRIMARY / REQUIREMENT`
- 정확한 수치: `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`

## 구형 라우팅

| 문서·모델 | 상태 | 대체 |
|---|---|---|
| 4등급 제작 문서 | `[대체됨]` | 5등급 정본 |
| `STANDARD / GOOD / PERFECT` runtime | `[역사 증거]` | 현재 제품 구현 아님 |
| bounded 예술성·named visual tiers | `[대체됨]` | 고정 상한 없는 예술성 정본 |
| R1 Game Bible | `[부분 대체됨]` | Current R2 Game Bible |
| PR #81 | 전체 병합 `[폐기]` / 선별 `[보류]` | 별도 소형 PR |

## 배치·검증

- `R2_BATCH_004: CLOSED_MERGED_PR107 / 2/10`
- `R2_BATCH_005: ACTIVE / 1/10`
- 최대 배치 크기: 10
- TDD RED: Planning-first `109`
- GREEN exact-head: `PENDING`
- 제품 구현: `BLOCKED`

## 고객 능력·장비 적합성 승인

- Decision: `BS-CUSTOMER-20260805-01`
- 고객: 근력·기량·체력·판단력 `1~10`, 희소 무기·갑옷 적성 `0~3`, 마력 적성 `0~10`
- 작품: `WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL`
- 파생: 총 중량·적정 하중·균형 상태·특수기능 적합도
- 상태: `R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE / PRODUCT_IMPLEMENTATION_BLOCKED`

<!-- BS-UX-20260805-01 -->
- 모바일 고객 카드 단계적 공개 정본: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`
- 승인 설계: `docs/superpowers/specs/2026-08-05-mobile-customer-card-progressive-disclosure-design.md`
- 정본 동기화 계획: `docs/superpowers/plans/2026-08-05-mobile-customer-card-progressive-disclosure.md`

<!-- BS-CUSTOMER-20260806-01 -->
### 강화 중심 단순 장비 판정

- Decision: `BS-CUSTOMER-20260806-01` / `R2_BATCH_005_4_OF_10`
- 최대 중량: `STRENGTH × 10 WEIGHT_POINT`
- 상태: `WITHIN_LIMIT / OVERWEIGHT`; 초과 시 배정 불가
- 성공률: 강화 레벨이 주효과, 고객 능력·적성은 작은 보조 보정
- 정본: `docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md`
- 제품 구현: `BLOCKED`

## BS-ITEM-20260806-01 현재 정제

- 활성 배치: `R2_BATCH_005_5_OF_10`
- 장비군 고정 기본 중량: `0 / 5 / 10 / 15 / 20 / 30 WEIGHT_POINT`
- 중량 전용 효과: `LIGHTWEIGHT -5 / NONE 0 / WEIGHTED +5`, 작품당 최대 하나
- 자동 중량 변경 금지: 재료·제작 등급·예술성·원수치·일반 강화 단계
- 정본: `docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md`
- 제품 구현: `BLOCKED`
