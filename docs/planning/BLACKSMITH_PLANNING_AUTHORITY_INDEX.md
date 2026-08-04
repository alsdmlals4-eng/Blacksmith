# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX`
- 기준: `R2_CHECKPOINT_003 / BS-OPS-20260804-02`
- 제품 구현: `BLOCKED`

> 이 파일의 2026-07-26 버전은 `[대체됨]`이며 Git 이력 `d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9`에 보존됩니다.

## 1. 적용 우선순위

충돌 시 위에 있는 문서가 우선한다.

1. `CURRENT_CONFIRMED_DECISIONS.md`
2. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
3. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
4. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
5. `[기획서]/00_프로젝트_허브/ROADMAP.md`
6. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
7. `docs/planning/CURRENT_R1_CANON_REGISTRY.json` — 역사적 R1 기반
8. 상태가 표시된 과거 기획·PoC·연구·구현 계획

## 2. 현재 분야별 책임 원본

### 프로젝트 코어·현재 상태

- `CURRENT_CONFIRMED_DECISIONS.md`
- `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`

### 고객 정보 공개

- `docs/planning/BLACKSMITH_R2_CUSTOMER_DISCLOSURE_MINIMUM_CANON_2026.md`
- `docs/planning/BLACKSMITH_R2_CUSTOMER_SCHEDULE_AND_VISIBLE_CAPABILITY_CANON_2026.md`

### 개인·세계 일정과 알림

- `docs/planning/BLACKSMITH_R2_MULTI_SCHEDULE_DISPLAY_AND_ALERT_CANON_2026.md`
- `docs/planning/BLACKSMITH_R2_CONTENT_COMPOSITION_AND_ITEM_LEGACY_CANON_2026.md`

### 고객·콘텐츠 가족

- `docs/planning/BLACKSMITH_R2_VISITOR_ARCHETYPES_AND_INITIAL_CONTENT_FAMILIES_CANON_2026.md`

### 예술성·가격·시각 단계

- `docs/planning/BLACKSMITH_R2_ARTISTRY_VALUE_AND_UTILITY_CRAFTING_CANON_2026.md`
- `docs/planning/BLACKSMITH_R2_ARTISTRY_MINIMUM_SCALE_PRICE_AFFIX_VISUAL_PRESET_CANON_2026.md`

### 정밀강화·촉매

- `docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R2_CATALYST_AFFIX_SEED_EVOLUTION_AND_MUTATION_CANON_2026.md`

### 세 수식어·장비명·연대기 상세

- `docs/planning/BLACKSMITH_R2_THREE_AFFIX_SLOT_ARCHITECTURE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R2_CHRONICLE_AFFIX_DETAIL_INTERACTION_CANON_2026.md`

### 정본 감사·구형 문서 상태

- `docs/planning/BLACKSMITH_CANON_ADVERSARIAL_REVIEW_AND_LEGACY_STATUS_2026-08-04.md`
- `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`

## 3. 명시적으로 대체된 구조

### 수식어

```text
[대체됨]
일반 수식어 A + 일반 수식어 B + 사건 수식어

[현재 정본]
GRADE_AFFIX + CATALYST_AFFIX + CHRONICLE_AFFIX
```

### 재료·정밀강화

```text
[대체됨]
주재료 + 보조재료 + 촉매 슬롯

[현재 정본]
주재료 맥락 + 강화 방식 + 촉매 한 개
```

### 일정

```text
[대체됨]
모든 일정의 고정 3일 결과·4일 재방문

[현재 정본]
고객 개인 일정과 특정 날짜 예고형 세계 일정 분리
```

### 최초 제작 수식어

```text
[대체됨]
제작 완료 시 모든 수식어 없음

[현재 정본]
GRADE_AFFIX assigned
CATALYST_AFFIX empty
CHRONICLE_AFFIX empty
```

## 4. 문서 상태 해석

| 표시 | 의미 |
|---|---|
| `[현재 정본]` | 현재 구현·후속 기획의 직접 기준 |
| `[부분 대체됨]` | 일부 원칙은 유지되나 명시된 절은 최신 정본이 우선 |
| `[대체됨]` | 최신 정본이 같은 책임을 완전히 인수 |
| `[보류]` | 승인·채택 전 참고만 가능 |
| `[폐기]` | 재사용하지 않음 |
| `[역사 증거]` | 당시 구현·검증·승인 과정 보존용 |

정확한 파일별 상태는 `BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`을 따른다.

## 5. PR 권위

- PR #103: `MERGED_R2_CHECKPOINT_003_CANON`
- PR #104: `MERGED_POSTMERGE_CLOSURE`
- PR #81: `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT / SELECTIVE_PROMOTION_HOLD`

PR #81의 전체 병합 단위는 `[폐기]`이며, 브랜치의 고유 원문은 `[역사 증거]`다. Save·UI·Android·검증·비주얼 등의 분야별 선별 이관은 현재 main에서 시작한 별도 소형 PR만 허용한다.

## 6. 구현자 확인 순서

1. Current Decisions와 Current R2 Registry 확인
2. 이 색인에서 분야별 최신 책임 문서 확인
3. Legacy Status Registry에서 대상 문서 상태 확인
4. `[대체됨]`, `[보류]`, `[폐기]` 내용을 구현 요구로 사용하지 않음
5. 정확한 숫자는 `BASELINE_TEST_PRESET`, `CURRENT_VALIDATED`, `HISTORICAL_EVIDENCE`를 구분
6. 제품 경로를 수정하기 전에 R1~R8와 최종 사용자 승인 확인

## 7. 현재 열린 Decision

- 제작 등급 수식어와 예술성 시각 단계의 한국어 명칭 분리
- 연대기 수식어 효과 책임
- 작품 소유권 상태 머신
- 모바일 조합 이름 표시
- 첫 작품 정체성 보상 시점
- 완전 파괴와 작품 애착 검증
- PR #81 선별 이관 순서

승인 전에는 `PROPOSED_ONLY`다.
