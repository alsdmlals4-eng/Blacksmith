# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX`
- 기준: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~08`
- 제품 구현: `BLOCKED`

> 이 파일의 2026-07-26 버전은 `[대체됨]`이며 Git 이력 `d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9`에 보존됩니다.

## 1. 적용 우선순위

충돌 시 위에 있는 문서가 우선한다.

1. 사용자의 최신 지시와 승인
2. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md` — 현재 재기획 상태·2026-08-20 승인 요약
3. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 세부 Decision·역사 장기 원장
4. `docs/planning/BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md`
5. `docs/planning/BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md`
6. `docs/planning/BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md`
7. `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md`
8. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
9. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
10. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
11. `[기획서]/00_프로젝트_허브/ROADMAP.md`
12. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
13. `docs/planning/CURRENT_R1_CANON_REGISTRY.json` — 역사적 R1 기반
14. 상태가 표시된 과거 기획·PoC·연구·구현 계획

`BS-CORE-20260820-01` 이후 사용자의 최신 재기획 승인은 기존 장기 원장의 과거 `PLANNING_COMPLETE`보다 우선한다. 새 `기획 완료` 선언 전 제품 구현은 다시 열지 않는다.

## 2. 현재 분야별 책임 원본

### 프로젝트 코어·현재 상태

- `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
- `CURRENT_CONFIRMED_DECISIONS.md` — 세부 역사 원장
- `docs/planning/BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md`
- `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`

### 강화·DDD·실패·내구도

- `docs/planning/BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md` — 강화 긴장감/DDD 1차 코어
- `docs/planning/BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md` — 실패 누적 회복·UID 보존형 손상·정보 공개
- `docs/planning/BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` — 체크포인트·제한 단계 하락·CURRENT 내구도 0~100%·0% 물리 파괴
- `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` — CURRENT/MAX 이중 내구도·MAX 구조 손상·강화 확률/신규 효과 페널티
- `docs/planning/BLACKSMITH_ENHANCEMENT_TENSION_AND_DDD_REWARD_LADDER_20260820.md` — 튜닝 가능한 긴장 곡선/Reward Ladder

이 분야에서 구형 `data/crafting/enhancement_balance.json`과 과거 PoC 수치는 `HISTORICAL_EVIDENCE / REUSE_CANDIDATE`이며 현재 제품 확정 수치가 아니다.

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

## 3. 명시적으로 대체·정제된 구조

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

### 내구도

```text
[정제됨 1]
DURABILITY = 정수형 작품 능력치 (예: 내구도 18)

[정제됨 2]
DURABILITY_PERCENT = 단일 0~100 현재 상태

[현재 정본]
CURRENT_DURABILITY_PERCENT = 단기 현재 상태
MAX_DURABILITY_PERCENT = 누적 구조 건전성 한계
0 <= CURRENT <= MAX <= 100
새 작품 = 100 / 100
CURRENT 0 또는 MAX 0 = DESTROYED
```

일반 수리는 `CURRENT = MAX`까지만 회복하며 MAX를 올리지 않는다. 심각 강화 실패/직접 구조 손상 사건만 MAX를 감소시킨다. MAX가 낮아질수록 강화 성공 기대가 악화되고, 심각 손상 구간에서는 앞으로 새로 얻는 강화 성장량도 감소한다. 기존 획득 성능은 소급 삭감하지 않는다.

### 강화 실패

```text
[구형 구현/역사 증거]
큰 단계 하락 또는 item DESTROY/zeroed runtime state

[현재 기획]
주요 체크포인트 아래 하락 금지
+ 구간 내 최대 1단계 하락부터 테스트
+ FAIL_HOLD / FAIL_DOWNGRADE / FAIL_DAMAGE / FAIL_CRITICAL_DAMAGE 분리
+ FAIL_DAMAGE는 CURRENT 중심
+ FAIL_CRITICAL_DAMAGE만 MAX 구조 손상 후보
+ 모든 실패에 회복 진전
+ CURRENT 또는 MAX 0%일 때 물리 작품 DESTROYED
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

- PR #172: `MERGED_ENHANCEMENT_CHECKPOINT_AND_DURABILITY / c9781e73141988ea46d80f3f8200941411d5a258`
- PR #171: `MERGED_ENHANCEMENT_RECOVERY_AND_DDD_PLANNING / e714b864ebbdbd73c0b0714f93296044dcf619ee`
- PR #103: `MERGED_R2_CHECKPOINT_003_CANON`
- PR #104: `MERGED_POSTMERGE_CLOSURE`
- PR #81: `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT / SELECTIVE_PROMOTION_HOLD`

PR #81의 전체 병합 단위는 `[폐기]`이며, 브랜치의 고유 원문은 `[역사 증거]`다. Save·UI·Android·검증·비주얼 등의 분야별 선별 이관은 현재 main에서 시작한 별도 소형 PR만 허용한다.

## 6. 구현자 확인 순서

1. 최신 사용자 지시와 `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md` 확인
2. 기존 `CURRENT_CONFIRMED_DECISIONS.md`에서 세부 과거 Decision 확인
3. 이 색인에서 분야별 최신 책임 문서 확인
4. 강화/내구도면 2026-08-20 enhancement canon을 R2/R3의 구형 DURABILITY·failure 표현보다 우선
5. Legacy Status Registry에서 대상 문서 상태 확인
6. `[대체됨]`, `[보류]`, `[폐기]` 내용을 구현 요구로 사용하지 않음
7. 정확한 숫자는 `TUNABLE / BASELINE_TEST_PRESET / CURRENT_VALIDATED / HISTORICAL_EVIDENCE`를 구분
8. 새 `기획 완료` 선언 전 제품 경로를 수정하지 않음

## 7. 현재 열린 Decision

- 제작 등급 수식어와 예술성 시각 단계의 한국어 명칭 분리
- 연대기 수식어 효과 책임
- 작품 소유권 상태 머신
- 모바일 조합 이름 표시
- 첫 작품 정체성 보상 시점
- CURRENT/MAX 내구도 손실량·발생 확률·수리 비용의 정확 Balance Budget
- MAX 구조 복구/대수선 기능을 넣을지와 그 영구 대가
- 파괴된 작품을 도감/기념물/계승 콘텐츠에서 어떻게 활용할지
- PR #81 선별 이관 순서

승인 전에는 `PROPOSED_ONLY`다.
