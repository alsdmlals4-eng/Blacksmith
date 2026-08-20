# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX`
- 기준: `BS-CORE-20260820-01 / BS-ENHANCE-20260820-02~13 / BS-PROGRESSION-20260820-14`
- 제품 구현: `BLOCKED`

## 1. 충돌 시 우선순위

1. 사용자의 최신 지시와 승인.
2. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`.
3. 2026-08-20 개별 Canon 문서.
4. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장.
5. R2/R3 Game Bible·과거 PoC·구형 data.

새 `기획 완료` 선언 전 `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 제품 구현 변경은 금지한다.

## 2. 현재 책임 원본

### 제품 코어
- `BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md` — 강화 긴장감 + DDD가 1차 코어.

### 실패·회복·내구도
- `BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md` — 02~04.
- `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` — 05~06.
- `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` — 07~09.
- `BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md` — CURRENT/MAX 첫 Balance Budget.
- `BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md` — 13 family 정확 비율.

### 수리 경제
- `BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md` — 10~11 수리 구조/작업량. 11의 optional-material 하위 규칙은 12가 대체.
- `BLACKSMITH_REPAIR_ABSOLUTE_ANCHOR_CANON_20260820.md` — 12 SWORD 800 + 골드·일반 구조재료 동시 소모.

### 강화 진행·수익 경제
- `BLACKSMITH_ENHANCEMENT_PROGRESSION_ECONOMY_CANON_20260820.md` — 14 `+10 본전 / +11 이후 수익 / +100 최대`.
- `BLACKSMITH_ENHANCEMENT_PROFIT_CURVE_2026.md` — 최신 구조 계약 + 2026-07 과거 가격표 재보정 증거.
- `BLACKSMITH_ENHANCEMENT_TENSION_AND_DDD_REWARD_LADDER_20260820.md` — 경험 밴드 역할/DDD Ladder. 세부 레벨 매핑은 아직 후속.

## 3. 현재 실패 결과군 권위 — 13

조건부 실패 family table:

```text
order = HOLD / DOWNGRADE / DAMAGE / CRITICAL

LEARN             100 /  0 /  0 /  0
BUILD_CONFIDENCE   90 /  0 / 10 /  0
FIRST_STOP_POINT   65 / 10 / 23 /  2
TENSION            45 / 10 / 35 / 10
HIGH_STAKES        30 / 15 / 39 / 16
MASTERY            20 / 20 / 40 / 20
```

핵심 불변식:

```text
P(CRITICAL | failure) = P(MAX scar | failure)
```

- CRITICAL 뒤 별도 MAX-scar roll 금지.
- 별도 destroy roll 금지.
- DOWNGRADE와 durability 손상 기본 중첩 금지.
- recovery는 첫 Vertical Slice에서 성공률만 변경하고 family severity는 밴드 안에서 고정.

상태: 구조 `USER_APPROVED`; 수치 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`.

## 4. 현재 진행·경제 권위 — 14

```text
MAX_ENHANCEMENT_LEVEL = 100

+0~+9      = INVESTMENT_RECOVERY_ZONE
+10        = BREAK_EVEN_RECOVERY_POINT
+11~+100   = PROFITABLE_ENHANCEMENT_ZONE
```

대표 평범한 작품의 기본 공개시장 기준:

```text
EXPECTED_NET_PROFIT(+10) ~= 0
EXPECTED_NET_PROFIT(+11..+100) > 0
```

`+10 본전` 누적 기대원가에는 제작/강화/실패 반복/DOWNGRADE 복구/강화 유발 CURRENT 수리/해당 구간 파괴·재제작 기대비용을 포함한다.

정밀제작·수식어·연대기·고객/거래 채널 프리미엄은 별도 가치축이며 기본 +10 회수선에 중복 포함하지 않는다.

`+100` 이후 +101/무한 초월/프레스티지는 별도 사용자 승인 없이는 추가하지 않는다.

상태: 구조 `USER_APPROVED / STRUCTURAL_CANON`; 세부 +0~+100 가격·성공률·비용 곡선은 `NOT_FINAL`.

## 5. 과거 수익곡선 처리

2026-07 POC의:

```text
+5 최초 흑자
+60 마지막 명시 가격 앵커
```

는 current canon이 아니다.

기존 +0~+60 가격표는:

```text
HISTORICAL_NUMERIC_EVIDENCE
RECALIBRATION_INPUT
DO_NOT_EXTRAPOLATE_TO_+100
```

으로만 사용한다.

## 6. 현재 수리 권위 요약

```text
missing = MAX - CURRENT

gold_cost
= (SWORD_BASE_R 800 × material_structure_mult × secured_band_mult)
× (0.05 + 0.65 × missing / 100)

common_material_units
= max(1, ceil(missing / 25))

PAYMENT = GOLD + COMMON_MATERIAL
REPAIR_JOB_FATIGUE_COST = 2
CURRENT -> MAX
MAX unchanged
recovery unchanged
```

주재료 첫 배율:

```text
iron 1.00 / silver 1.20 / meteor_iron 1.50
```

secured band 첫 배율:

```text
LEARN·BUILD 1.00
FIRST_STOP 1.10
TENSION 1.25
HIGH 1.50
MASTERY 1.80
```

## 7. 현재 열린 Critical Decision

우선순위:

1. **+0~+100 레벨 → 경험 밴드 매핑**.
2. 체크포인트 최종 간격과 +10 경제 이정표의 checkpoint 관계.
3. +0~+100 단계별 성공률/강화 비용/판매가/누적 기대원가.
4. 일반 구조재료 공급량·획득 경로.
5. CURRENT 손실 최종값 및 MASTERY 손실량.
6. 후기 HIGH_STAKES/MASTERY 수리 경제 스케일.
7. MAX 대수선 여부.
8. 파괴 작품 memorial/successor.
9. +100 비수치 payoff.
10. 첫 10분 강화 수치와 UX.

## 8. 상태 해석

| 상태 | 의미 |
|---|---|
| `USER_APPROVED` | 방향/구조 사용자 승인 |
| `USER_APPROVED_TEST_BUDGET` | 테스트 시작값, 출시 최종값 아님 |
| `HISTORICAL_NUMERIC_EVIDENCE` | 과거 수치 증거, current numeric canon 아님 |
| `PROPOSED_ONLY` | 사용자 승인 전 제안 |
| `BLOCKED` | 제품 구현 금지 |

## 9. 구현자 확인 순서

1. 최신 사용자 지시 확인.
2. Overlay와 13/14 Canon 확인.
3. 수리면 10~12, 실패면 13, 진행/경제면 14를 우선.
4. 구형 data는 `HISTORICAL_EVIDENCE / REUSE_CANDIDATE`로만 사용.
5. 새 `기획 완료` 전 제품 구현 금지.
