# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX`
- 기준: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~11`
- 제품 구현: `BLOCKED`

## 1. 적용 우선순위

충돌 시 위에 있는 항목이 우선한다.

1. 사용자의 최신 지시와 승인
2. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md` — 2026-08-20 재기획 현재 상태
3. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 세부 Decision·역사 장기 원장
4. `docs/planning/BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md`
5. `docs/planning/BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md`
6. `docs/planning/BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md`
7. `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md`
8. `docs/planning/BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md`
9. `docs/planning/BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md`
10. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
11. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
12. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
13. `[기획서]/00_프로젝트_허브/ROADMAP.md`
14. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
15. 상태가 표시된 과거 기획·PoC·연구·구현 계획

`BS-CORE-20260820-01` 이후 재기획은 과거 `PLANNING_COMPLETE / PHASE_C_ENTRY_APPROVED`보다 우선한다. 새 `기획 완료` 선언 전 제품 구현은 열지 않는다.

## 2. 현재 책임 원본

### 프로젝트 코어·상태
- `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
- `docs/planning/BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md`

### 강화·DDD·실패·내구도·수리 경제
- `BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md` — 실패 누적 회복·정보 공개
- `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` — 체크포인트·CURRENT·0% 파괴
- `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` — CURRENT/MAX·구조 흉터·07~09
- `BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md` — 09 MAX scar + 10 수리 경제 승인 테스트 Budget
- `BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md` — 11 수리 참조 구조·재료 대체·공방 피로도
- `BLACKSMITH_ENHANCEMENT_TENSION_AND_DDD_REWARD_LADDER_20260820.md` — 긴장 곡선·Reward Ladder

구형 `data/crafting/enhancement_balance.json`, `data/progression/workshop_day_balance.json`과 과거 PoC 수치는 `HISTORICAL_EVIDENCE / REUSE_CANDIDATE`이며 현재 제품 확정 수치가 아니다. 특히 구형 `restore=5`는 11의 일반 수리 피로도 2보다 우선하지 않는다.

### 기존 R2/R3 분야
기존 고객·세계·정밀강화·수식어·연대기 Canon은 위 2026-08-20 Decision과 충돌하지 않는 범위에서만 소비한다. 정확 파일 상태는 `BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`을 따른다.

## 3. 현재 내구도 권위

```text
[역사]
DURABILITY = 정수형 작품 능력치

[정제]
단일 DURABILITY_PERCENT

[현재]
CURRENT_DURABILITY_PERCENT = 단기 생존 버퍼
MAX_DURABILITY_PERCENT = 누적 구조 건전성
0 <= CURRENT <= MAX <= 100
```

- 새 작품 `100 / 100`.
- 일반 수리 `CURRENT = MAX`, MAX 유지.
- `FAIL_DAMAGE`는 CURRENT 중심.
- `FAIL_CRITICAL_DAMAGE`만 MAX 구조 손상 후보.
- CURRENT 또는 MAX 0%면 물리 작품 `DESTROYED`.
- MAX 저하는 성공률과 미래 신규 강화 성장에 단계적 불이익을 줄 수 있다.
- 기존 획득 성능은 소급 삭감하지 않는다.

## 4. BS-ENHANCE-20260820-09 권위

MAX 구조 손상은 실패 후 conditional failure-family 판정이다.

```text
LEARN             scar|failure 0%      / MAX loss 0
BUILD_CONFIDENCE  scar|failure 0%      / MAX loss 0
FIRST_STOP_POINT  scar|failure 0~5%    / MAX loss 1~3
TENSION           scar|failure 8~12%   / MAX loss 2~5
HIGH_STAKES       scar|failure 12~20%  / MAX loss 4~10
MASTERY           scar|failure 15~25%  / MAX loss 6~15
```

상태: `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

- 첫 MAX 흉터는 FIRST_STOP_POINT 이후.
- 한 시도 MAX scar 최대 1회.
- DOWNGRADE와 CRITICAL 기본 중첩 금지.
- 별도 destroy roll 금지.
- UI에는 최종 per-attempt 구조 손상 가능성과 MAX 손실 범위를 공개.

## 5. BS-ENHANCE-20260820-10 권위

일반 수리 경제의 현재 기본 공식은 다음이다.

```text
missing_current_points = MAX - CURRENT
repair_cost
= REPAIR_REFERENCE_COST
× (setup_fraction + variable_fraction × missing_current_points / 100)
```

- 채택안: `C / stable repair reference cost + setup + absolute missing CURRENT`.
- 일반 수리 1회로 `CURRENT = MAX`, MAX unchanged.
- `(MAX-CURRENT)/MAX` 비율을 가격 배율로 쓰지 않는다.
- 낮은 MAX 자체에 일반 수리 할증 없음.
- 최종 시장가·수식어·예술성·연대기·고객 수요·실제 next-attempt cost를 런타임 공식에서 제외.
- 실패 누적 회복은 수리 후에도 유지.
- 부분수리·자동수리·수리 RNG·새 수리 화폐·일반 MAX 복구는 첫 Vertical Slice 제외.

승인된 첫 테스트 shell:

```text
setup_fraction = 0.05
variable_fraction = 0.65
```

상태: 구조 `USER_APPROVED`; 계수 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 6. BS-ENHANCE-20260820-11 권위

`REPAIR_REFERENCE_COST`의 현재 상대 구조는 다음이다.

```text
R
= STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER[primary_material]
× SECURED_BAND_MULTIPLIER[highest_secured_band]
```

주재료 구조 배율:

```text
iron         1.00
silver       1.20
meteor_iron  1.50
```

확보 밴드 배율:

```text
LEARN / BUILD_CONFIDENCE  1.00
FIRST_STOP_POINT          1.10
TENSION                   1.25
HIGH_STAKES               1.50
MASTERY                   1.80
```

추가 승인 첫 테스트값:

```text
OPTIONAL_COMMON_MATERIAL_OFFSET_CAP = 25%
REPAIR_JOB_FATIGUE_COST = 2
```

- 원시 재료 가격 비율을 그대로 수리비에 복사하지 않는다.
- R은 현재 +1 단계가 아니라 `highest_secured_band`가 바뀔 때만 변한다.
- 같은 확보 밴드 안 제한 하락은 R을 낮추지 않는다.
- 일반 재료는 선택적으로 견적 최대 25%를 고정 shadow value로 대체할 수 있다.
- 재료가 없어도 100% 골드로 수리 가능하다.
- 일반 수리 피로도 2는 구형 `restore=5` 또는 하루 전체 소비를 대체하는 최신 첫 테스트값이다.
- `STRUCTURAL_FAMILY_BASE_R` 절대 골드 기준은 후속 절대 경제 Budget에서 정한다.

상태: 구조 `USER_APPROVED`; 배율·상한·피로도는 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 7. 문서 상태 해석

| 표시 | 의미 |
|---|---|
| `[현재 정본]` | 현재 후속 기획의 직접 기준 |
| `USER_APPROVED` | 구조/방향 사용자 승인 |
| `USER_APPROVED_TEST_BUDGET` | 테스트 시작값으로 승인, 출시 최종 수치 아님 |
| `[부분 대체됨]` | 일부 원칙만 유지 |
| `[대체됨]` | 최신 정본이 책임 인수 |
| `[보류]` | 승인 전 참고 |
| `[폐기]` | 재사용 금지 |
| `[역사 증거]` | 당시 구현·승인 과정 보존 |

## 8. PR 권위

- PR #175: `MERGED_REPAIR_ECONOMY_CONTRACT / 03d7ed5fd47cb289ec31c6f446d316dc3b225b32`
- PR #174: `MERGED_MAX_DURABILITY_SCAR_BUDGET / 1dbbc9089d2953ad5e846b520d89caa01718e7b1`
- PR #173: `MERGED_MAX_DURABILITY_STRUCTURAL_SCAR / b23c6b6cb344eb968b943493902f2644c160c339`
- PR #172: `MERGED_ENHANCEMENT_CHECKPOINT_AND_DURABILITY / c9781e73141988ea46d80f3f8200941411d5a258`
- PR #171: `MERGED_ENHANCEMENT_RECOVERY_AND_DDD_PLANNING / e714b864ebbdbd73c0b0714f93296044dcf619ee`
- PR #81: `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT`

## 9. 구현자 확인 순서

1. 최신 사용자 지시 + Overlay 확인
2. 강화/내구도/수리면 2026-08-20 Canon과 승인 Budget 확인
3. 기존 R2/R3 문서는 최신 계약과 충돌하지 않는 범위에서만 사용
4. `TUNABLE / USER_APPROVED / USER_APPROVED_TEST_BUDGET / CURRENT_VALIDATED / HISTORICAL_EVIDENCE` 구분
5. 새 `기획 완료` 선언 전 `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 수정 금지

## 10. 현재 열린 Decision

- failure family 전체 정확 분배(HOLD/DOWNGRADE/DAMAGE)
- CURRENT 손실 최종값
- `STRUCTURAL_FAMILY_BASE_R` 절대 골드 기준값
- 검 이외 장비군별 base R
- 일반 재료 shadow value 최종값
- 하루 총 피로도/작업량 출시 최종값
- MAX 구조 복구/대수선 필요 여부와 대가
- 체크포인트 최종 간격
- 파괴 작품 memorial/successor 콘텐츠
- 첫 10분 강화 수치와 UX

승인 전에는 `PROPOSED_ONLY`다.
