# [현재 정본] Blacksmith 시작 지점

## 프로젝트 약속

> 제한된 하루 작업량 안에서 작품을 만들고 강화 위험 앞에서 멈출지 더 도전할지 선택하며, 같은 UID 작품이 고객과 세계에서 겪은 생애 결과를 돌려받는 Android 세로형 제작 게임.

```yaml
WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R2_CHECKPOINT_003: PR103 / CLOSURE_PR104 / CANON_AUDIT_PR105
R2_CHECKPOINT_004: PR106 / CLOSURE_PR107 / CANON_AUDIT_PR108
R2_STATUS: R2_BATCH_005_ACTIVE_4_OF_10
CURRENT_DECISIONS: BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / BS-CRAFT-20260805-02 / BS-OPS-20260805-01
PRODUCT_IMPLEMENTATION: BLOCKED
```

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
5. `ACTIVE_CONTEXT.md`
6. `DEVELOPMENT_GATES.md`
7. `ROADMAP.md`
8. `DOCUMENTATION_MAP.md`
9. `DESIGN_DOCUMENT_REGISTRY.json`
10. 분야별 최신 정본
11. 실제 구현·data·tests — 역사 구현과 현재 제품 상태 구분

## 현재 규칙

```text
제작 등급: [보통] → [우수] → [명품] → [걸작] → [전설]
예술성: 0 이상의 정수, 고정 설계 최대치 없음, 예술성 27 원수치 표기
수식어: GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

- 제작 등급은 최초 직접 단조 완료 시 확정하고 동일 UID에서 고정
- 예술성은 전투력을 기본적으로 올리지 않고 범용 속성 배율이 아님
- 일반 강화는 한 입력에 한 결과
- 정밀강화는 주재료 맥락 + 강화 방식 + 촉매 한 개
- 연대기 수식어를 누르면 UID 기반 읽기 전용 상세
- 보조재료 슬롯과 일반 수식어 A·B는 현재 구조 아님

## 예술성 생성·성장·가치 평가

Decision: `BS-CRAFT-20260805-02`.

```text
초기 생성: 설계 미적 성향 / 재료 시각·가공 적합성 / 직접 단조 미적 결과
후천 성장: ARTISTIC_FINISH / 예술성 책임 촉매 / 승인된 세공·마감 / 의미 있는 재작업
가치 평가: ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE
고객 관심: IGNORE / SECONDARY / PRIMARY / REQUIREMENT
```

- 일반 강화·판매·증여·전시·감정·명성·연대기로 자동 증가 금지
- 수리·손상·판매·전시·감정·증여·저비용 반복으로 순증가 금지
- 동일 원인 이중 계산과 전체 가치 곱셈 중첩 금지
- 정확한 값은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`

## 체크포인트 상태

- R2_CHECKPOINT_004: `MAIN_CANON`
- 현재 배치 005: `ACTIVE / 1_OF_10`
- 제품 구현: `BLOCKED`

## 운영 규칙

- 질문·추천·설계 전 벤치마킹·현업 비교
- 승인 10건은 최대 배치 크기
- `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT` 조기 체크포인트
- 작업마다 `RED → GREEN → REFACTOR` TDD
- 명시적 사용자 승인 전 병합 금지

## 구형 문서

상태 원장: `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`.

- 이전 4등급 문서: `[대체됨]`
- 초기 bounded 예술성·named tier: `[대체됨]`
- 과거 3등급 runtime: `[역사 증거]`
- PR #81 전체 병합: `[폐기]`, 선별 이관: `[보류]`

## 고객 능력·장비 적합성 승인

- Decision: `BS-CUSTOMER-20260805-01`
- 고객: 근력·기량·체력·판단력 `1~10`, 희소 무기·갑옷 적성 `0~3`, 마력 적성 `0~10`
- 작품: `WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL`
- 파생: 총 중량·적정 하중·균형 상태·특수기능 적합도
- 상태: `R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE / PRODUCT_IMPLEMENTATION_BLOCKED`

<!-- BS-UX-20260805-01 -->
현재 UX Decision은 `BS-UX-20260805-01`: 모바일 고객 카드의 기본→장비 판단→상세 3단계 정보 공개. 제품 구현은 계속 `BLOCKED`.

<!-- BS-CUSTOMER-20260806-01 -->
### 강화 중심 단순 장비 판정

- Decision: `BS-CUSTOMER-20260806-01` / `R2_BATCH_005_4_OF_10`
- 최대 중량: `STRENGTH × 10 WEIGHT_POINT`
- 상태: `WITHIN_LIMIT / OVERWEIGHT`; 초과 시 배정 불가
- 성공률: 강화 레벨이 주효과, 고객 능력·적성은 작은 보조 보정
- 정본: `docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md`
- 제품 구현: `BLOCKED`
