# [현재 우선 Overlay] Blacksmith 2026-08-20 Confirmed Decisions

- 상태: `CURRENT_PRIORITY_OVERLAY`
- 적용 시작: `2026-08-20 KST`
- 이유: 기존 `CURRENT_CONFIRMED_DECISIONS.md`는 2026-08-11 Phase C 진입과 다수 과거 Decision을 장기 원장으로 보존하므로, 최신 재기획을 과거 원장을 파괴하지 않고 우선 적용하기 위한 overlay다.
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`

## 현재 상태

사용자는 2026-08-20 Blacksmith 기획을 다시 열었다. 기존 `PLANNING_COMPLETE / PHASE_C_ENTRY_APPROVED`는 역사 상태이며 새 `기획 완료` 사용자 선언 전 제품 구현을 시작하지 않는다.

## 현재 승인 Decision

### `BS-CORE-20260820-01`
Blacksmith의 1차 코어는 **강화의 긴장감 + DDD**다. 작품 UID·생애는 강화 선택의 손실·애착·기억을 증폭하며 정밀제작·고객/세계 생애는 보조 계층이다.

### `BS-ENHANCE-20260820-02`
기본 실패/회복 골격은 `RISK_PLUS_RECOVERY_PROGRESS`다. 실패는 실제 비용/손실을 남기되 작품별 회복 진전을 남긴다.

### `BS-ENHANCE-20260820-03`
고위험 실패는 작품 손상을 만든다. UID와 역사를 보존하며 0% 파괴의 최신 경계는 06이 소유한다.

### `BS-ENHANCE-20260820-04`
강화 전 성공률·비용·주요 실패·회복·다음 체크포인트를 이해 가능하게 공개한다.

### `BS-ENHANCE-20260820-05`
주요 강화 이정표는 확보점으로 보호하고 체크포인트 사이에서만 제한 단계 하락을 사용한다.

### `BS-ENHANCE-20260820-06`
CURRENT 내구도는 `0~100%`. `0%`에서 물리 작품은 `DESTROYED`; UID·이름·강화·소유·사건·파괴 원인·Chronicle provenance는 기록으로 보존한다.

### `BS-ENHANCE-20260820-07`
첫 Vertical Slice 기본 강화에는 별도 `0% 파괴 방지 보험`을 두지 않는다. 일반 수리는 안전 선택이지만 작품을 새 상태로 초기화하지 않는다.

### `BS-ENHANCE-20260820-08`
내구도를 CURRENT/MAX 이중 상태로 정제한다.

```text
0 <= CURRENT_DURABILITY_PERCENT <= MAX_DURABILITY_PERCENT <= 100
```

- 새 작품 `100 / 100`.
- 일반 수리 `CURRENT = MAX`, MAX unchanged.
- `FAIL_DAMAGE`는 CURRENT 중심.
- `FAIL_CRITICAL_DAMAGE`만 MAX 구조 손상 후보.
- MAX가 CURRENT 아래로 내려가면 CURRENT도 clamp.
- CURRENT 또는 MAX 0%면 `DESTROYED`.
- MAX가 낮아지면 강화 성공 기대가 악화되고 심각 손상에서는 앞으로 새로 얻는 강화 성장량도 감소한다.
- 이미 획득한 성능은 MAX 손상만으로 소급 삭감하지 않는다.

### `BS-ENHANCE-20260820-09`
MAX 구조 손상은 **실패 뒤 2차 failure-family 판정**으로 사용한다. 성공한 시도에 별도 구조 손상 주사위를 붙이지 않는다.

승인된 첫 시뮬레이션/플레이테스트 Budget:

```text
LEARN             P(MAX scar | failure) 0%      / MAX loss 0
BUILD_CONFIDENCE  P(MAX scar | failure) 0%      / MAX loss 0
FIRST_STOP_POINT  P(MAX scar | failure) 0~5%    / MAX loss 1~3
TENSION           P(MAX scar | failure) 8~12%   / MAX loss 2~5
HIGH_STAKES       P(MAX scar | failure) 12~20%  / MAX loss 4~10
MASTERY           P(MAX scar | failure) 15~25%  / MAX loss 6~15
```

이 숫자는 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`다.

불변식:
- 첫 영구 MAX 흉터는 `FIRST_STOP_POINT` 이후에만 열린다.
- 한 시도에서 MAX scar는 최대 1회다.
- `FAIL_CRITICAL_DAMAGE`와 `FAIL_DOWNGRADE`는 기본 중첩하지 않는다.
- MAX 손실량을 CURRENT에 이중 차감하지 않는다.
- 파괴는 추가 즉사 주사위가 아니라 실제 CURRENT/MAX가 0에 도달했을 때만 발생한다.
- UI에는 이번 시도의 최종 구조 손상 가능성과 발생 시 MAX 손실 범위를 공개한다.

### `BS-ENHANCE-20260820-10`
일반 수리 경제는 **안정된 수리 참조비용 + 고정 준비비 + 절대 결손 CURRENT 포인트 비례** 구조를 사용한다.

```text
missing_current_points = MAX - CURRENT

repair_cost
= REPAIR_REFERENCE_COST
× (setup_fraction + variable_fraction × missing_current_points / 100)
```

승인된 첫 테스트 shell:

```text
setup_fraction = 0.05
variable_fraction = 0.65
```

- 일반 수리 1회로 `CURRENT = MAX`; MAX는 변하지 않는다.
- 수리량은 `(MAX-CURRENT)/MAX` 비율이 아니라 `MAX-CURRENT` 절대 포인트다.
- 낮은 MAX 자체에 일반 수리비 할증을 붙이지 않는다.
- 최종 시장가·예술성·수식어·연대기·고객 수요·실제 다음 강화비를 런타임 수리 공식에 직접 넣지 않는다.
- 부분수리·자동수리·수리 성공 RNG·수리 전용 화폐·일반 MAX 복구는 첫 Vertical Slice에서 제외한다.
- 수리는 실패 누적 회복 진전을 초기화하지 않는다.

구조는 `USER_APPROVED`; 첫 계수는 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`다.

### `BS-ENHANCE-20260820-11`
`REPAIR_REFERENCE_COST`는 **압축 구조 참조형**을 사용한다.

```text
R
= STRUCTURAL_FAMILY_BASE_R
× MATERIAL_STRUCTURE_MULTIPLIER[primary_material]
× SECURED_BAND_MULTIPLIER[highest_secured_band]
```

승인된 첫 테스트 Budget:

```text
MATERIAL_STRUCTURE_MULTIPLIER
iron         1.00
silver       1.20
meteor_iron  1.50

SECURED_BAND_MULTIPLIER
LEARN / BUILD_CONFIDENCE  1.00
FIRST_STOP_POINT          1.10
TENSION                   1.25
HIGH_STAKES               1.50
MASTERY                   1.80

REPAIR_JOB_FATIGUE_COST = 2
```

- 원시 재료 판매가 비율을 수리비에 그대로 복사하지 않는다.
- +1 현재 단계가 아니라 `highest_secured_band`가 바뀔 때만 수리 구조 복잡도가 변한다.
- 같은 확보 밴드 안 제한 하락은 R을 낮추지 않는다.
- 촉매·희귀 수식어 재료·MAX 복구재를 일반 CURRENT 수리에 요구하지 않는다.
- 일반 수리는 피로도 2의 한 번 `REPAIR_JOB`으로 `CURRENT = MAX`까지 끝난다.
- 구형 `restore=5` 또는 하루 전체 소비는 최신 일반 수리의 권위가 아니다.

11에서 승인했던 `OPTIONAL_COMMON_MATERIAL_OFFSET_CAP=25%`와 `100% GOLD-ONLY REPAIR`는 **12에서 대체됨**.

### `BS-ENHANCE-20260820-12`
첫 Vertical Slice 대표 검의 절대 수리 기준과 결제 구조를 확정한다.

```text
STRUCTURAL_FAMILY_BASE_R
SWORD = 800 gold

COMMON_MATERIAL_SHADOW_VALUE = 50 gold / unit

common_material_units
= max(1, ceil((MAX - CURRENT) / 25))

PAYMENT
= GOLD_COST + REQUIRED_COMMON_MATERIAL
```

- `SWORD_BASE_R=800`은 `FIRST_VERTICAL_SLICE_ABSOLUTE_ANCHOR`이며 후기 전체 경제 영구값이 아니다.
- `COMMON_MATERIAL_SHADOW_VALUE=50`은 기존 제작·강화 경제의 shadow value를 재사용한다.
- 모든 일반 CURRENT 수리는 **골드와 일반 구조재료를 둘 다** 소모한다.
- 재료는 골드를 할인하지 않고, 골드는 재료를 대체하지 않는다.
- 일반 구조재료는 절대 결손 CURRENT만 본다. 주재료 구조 배율·secured band·MAX 상태를 재료 수량에 다시 곱하지 않는다.
- 첫 테스트 재료 수량은 `1~25pt=1 / 26~50pt=2 / 51~75pt=3 / 76~99pt=4`다.
- 일반 구조재료는 희귀 드롭 전용이 아닌 공통 공급 자원으로 유지해야 한다.
- `REPAIR_JOB_FATIGUE_COST=2`는 유지한다.

구조는 `USER_APPROVED`; 800·50·25pt당 1개 수량표는 `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`다.

## 현재 승인된 테스트 Band

MAX 상태 페널티:

```text
MAX 81~100: success 0pp   / new effect 100%
MAX 61~80 : success -3pp  / new effect 100%
MAX 41~60 : success -6pp  / new effect 95%
MAX 21~40 : success -10pp / new effect 90%
MAX 1~20  : success -15pp / new effect 80%
```

모두 첫 시뮬레이션/플레이테스트 입력이며 출시 최종 수치가 아니다.

## 현재 미확정

- 세부 레벨→경험 밴드 최종 매핑
- failure family 전체 비율(HOLD/DOWNGRADE/DAMAGE의 정확 분배)
- CURRENT 손실 범위의 최종값
- MAX 구조 손상 Budget 최종값
- 검 이외 장비군별 base R
- 후기 HIGH_STAKES/MASTERY 절대 수리 경제 스케일
- 일반 구조재료 실제 공급량·획득 경로
- 하루 총 피로도/작업량 출시 최종값
- MAX 구조 복구/대수선 필요 여부와 대가
- 체크포인트 최종 간격
- 파괴된 작품 memorial/successor 콘텐츠

## 책임 원본

1. 이 Overlay — 현재 상태와 승인 요약
2. `docs/planning/BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md`
3. `docs/planning/BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md`
4. `docs/planning/BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md`
5. `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md`
6. `docs/planning/BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md`
7. `docs/planning/BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md`
8. `docs/planning/BLACKSMITH_REPAIR_ABSOLUTE_ANCHOR_CANON_20260820.md`
9. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 세부 Decision·역사 원장

## 검증 경계

- Human/Player validation: `NOT_RUN`
- Android device: `NOT_RUN`
- Accessibility: `NOT_RUN`
- Performance: `NOT_RUN`
- 출시 최종 Balance: `NOT_FINAL`
- 제품 구현: `BLOCKED`
