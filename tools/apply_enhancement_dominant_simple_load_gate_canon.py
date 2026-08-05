#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-CUSTOMER-20260806-01"
CANON_PATH = "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md"
SPEC_PATH = "docs/superpowers/specs/2026-08-06-enhancement-dominant-simple-load-gate-design.md"
PLAN_PATH = "docs/superpowers/plans/2026-08-06-enhancement-dominant-simple-load-gate.md"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def write(relative: str, content: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def replace_required(text: str, old: str, new: str, *, count: int | None = None) -> str:
    if old not in text:
        raise RuntimeError(f"required token missing: {old!r}")
    return text.replace(old, new) if count is None else text.replace(old, new, count)


def append_once(relative: str, marker: str, block: str) -> None:
    text = read(relative)
    if marker not in text:
        write(relative, text.rstrip() + "\n\n" + block.strip() + "\n")


CANON = r'''# [현재 정본] Blacksmith R2 강화 중심 단순 최대 중량 게이트 Canon

- Decision: `BS-CUSTOMER-20260806-01`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-CUSTOMER-20260805-01 / BS-UX-20260805-01 / BS-CUSTOMER-20260803-02`
- 제품 구현: `BLOCKED`

## 1. 핵심 원칙

Blacksmith의 핵심은 고객 스탯 최적화가 아니라 작품을 강화하면서 더 도전할지 멈출지 판단하는 것이다. 고객 능력치·장비 능력치·적성은 작품을 누구에게 맡길지 이해시키는 보조 요소만 담당한다.

```text
강화 선택이 주효과
고객 능력·적성은 작은 보정
중량은 사용 가능 여부만 판정
```

## 2. 최대 중량

```text
최대 중량 = 근력 × 10
MAXIMUM_LOAD = STRENGTH × 10 WEIGHT_POINT
```

- 근력 `1~10`은 최대 중량 `10~100`에 대응한다.
- 중량은 현실 kg가 아닌 정수형 `WEIGHT_POINT`다.
- 총 중량은 배정한 무기·방패/보조장비·방어구·중량이 있는 도구의 합이다.
- 체력·기량·판단력은 최대 중량을 바꾸지 않는다.

## 3. 중량 상태

```text
WITHIN_LIMIT / OVERWEIGHT
사용 가능 / 중량 초과
```

- `총 중량 ≤ 최대 중량`: 사용 가능. 중량 보너스도 페널티도 없다.
- `총 중량 > 최대 중량`: 중량 초과 시 배정 불가.
- 최대 중량과 정확히 일치해도 추가 보너스가 없다.
- 초과량 비율·단계별 피로·명중·속도 페널티를 계산하지 않는다.

다음 이전 계약은 중량 판정에서 현재 사용하지 않는다.

```text
COMFORTABLE_LOAD / BALANCE_STATE
UNSUITABLE / UNSTABLE / STABLE / SKILLED
ESCALATING_OVERLOAD_PENALTY
HISTORICAL_SUPERSEDED
```

## 4. 강화 중심 성공률 베이스라인

내부 기준값은 다음처럼 단순화한다.

```text
위험도 기본 성공률 = clamp(100 - 위험도 × 10, 5, 90)
최종 성공률 = clamp(
  위험도 기본 성공률
  + 강화 레벨
  + 관련 능력 보정
  + 관련 적성 보정,
  5,
  95
)
```

### 강화 보정

```text
강화 레벨 +1당 +1%p
```

- `+20` 작품은 일반 사건 성공률에 `+20%p`를 제공한다.
- 강화는 플레이어가 가장 크게 통제하는 보정이다.
- 모든 강화 단계가 내부적으로 의미를 가진다.

### 고객 관련 능력 보정

- 사건이 지정한 관련 능력치가 위험도 이상이면 `+5%p`.
- 미만이면 `0%p`; 별도 음수 페널티는 없다.
- 한 사건은 기본적으로 관련 능력치 하나만 사용한다.

### 적성 보정

```text
적성 0: -10%p
적성 1:  0%p
적성 2: +5%p
적성 3: +10%p
```

고객 능력·적성은 강화보다 작은 보조 보정으로 유지한다.

### 최종 표시

- 내부 최종 범위: `5~95%`
- 고객 카드 표시: 가장 가까운 `10%` 단위
- 중량 초과 또는 필수 특수기능 미충족이면 성공률을 계산하기 전에 배정 불가를 표시한다.

## 5. 작품 능력치의 역할

다음 작품 원수치는 작품 UID에 남지만 일반 고객 사건 성공률 공식에는 자동 합산하지 않는다.

```text
ATTACK / DEFENSE / HANDLING / ARTISTRY
```

이 수치는 작품 정체성·판매 가치·특정 사건 요구·콘텐츠별 판정에 사용할 수 있다. 그러나 모든 사건에 범용 전투력처럼 다시 더하지 않는다.

## 6. 특수기능

특수기능은 복합 적합도 점수가 아니라 필요할 때만 확인하는 요구 조건이다.

```text
BINARY_REQUIREMENT_WHEN_EVENT_REQUIRES
```

- 사건이 특수기능을 요구하면 승인된 마력 적성·친화·활성 조건을 충족해야 한다.
- 충족하지 못하면 해당 특수기능은 사용할 수 없고, 필수 사건이면 배정 불가다.
- 사건이 특수기능을 요구하지 않으면 일반 성공률을 낮추지 않는다.

## 7. 모바일 표시

장비 선택 후 카드에는 다음만 보여준다.

```text
총 중량 32 / 최대 중량 50 · 사용 가능
총 중량 56 / 최대 중량 50 · 중량 초과 · 배정 불가
```

성공률 원인 우선순위:

1. 강화 레벨
2. 관련 능력치 충족 여부
3. 관련 적성
4. 필요한 경우에만 특수기능 요구

4단계 균형 상태나 초과 중량 퍼센트 페널티는 표시하지 않는다.

## 8. 예시

### 중량

- 근력 `4` → 최대 중량 `40`
- 총 중량 `40` → 사용 가능, 보너스·페널티 없음
- 총 중량 `41` → 배정 불가

### 성공률

위험도 `6`, 작품 `+20`, 관련 능력 충족, 적성 `2`:

```text
40 + 20 + 5 + 5 = 70%
```

플레이어에게 약 `70%`로 표시한다.

## 9. 적대적 검토

- 강화가 쉬운 사건에서 상한에 빨리 도달할 수 있음: 허용. 쉬운 사건에서 고객 스탯 최적화를 요구하지 않는다.
- 중량 초과가 하드 블록임: 허용. 불투명한 부분 페널티보다 명확하며 경량화 강화의 역할도 남긴다.
- 고객 능력 보정이 작게 느껴질 수 있음: 의도된 결과다. 고객 육성은 메인 루프가 아니다.
- 과거 4단계 균형 문구가 남을 수 있음: 역사 계약으로만 유지하고 현재 라우팅을 금지한다.

최종 판정: 핵심 재미와 정합하며 보조 시스템의 복잡도를 줄인다. `P0 0 / P1 0`.

## 10. 구현 경계

- 기획 정본·검증 계약만 갱신
- 런타임·게임 데이터·Scene·에셋: 변경 금지
- 실제 수치 플레이테스트: `NOT_RUN`
- 이미지·애니메이션 HX: 관련 기획 검토 완료 후
- 제품 구현: `BLOCKED`
'''

write(CANON_PATH, CANON)

# Current R2 registry.
registry_path = "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
registry = json.loads(read(registry_path))
registry["stage_status"] = "R2_BATCH_005_ACTIVE_4_OF_10"
registry["next_approval_counter"] = "4/10"
active = registry["active_batch"]
active["approved_decisions"] = 4
active["counter"] = "4/10"
active["decisions"] = [
    "BS-CRAFT-20260805-02",
    "BS-CUSTOMER-20260805-01",
    "BS-UX-20260805-01",
    DECISION_ID,
]

new_decision = {
    "id": DECISION_ID,
    "title": "강화 중심 단순 장비 판정과 최대 중량 게이트",
    "status": "USER_APPROVED_R2_BATCH_005_4_OF_10_APPROVED_PENDING_MERGE",
    "refines": ["BS-CUSTOMER-20260805-01", "BS-UX-20260805-01", "BS-CUSTOMER-20260803-02"],
    "canon": CANON_PATH,
    "spec": SPEC_PATH,
    "plan": PLAN_PATH,
    "contract": {
        "load_model": "BINARY_MAXIMUM_LOAD_GATE",
        "maximum_load_formula": "STRENGTH_X_10_WEIGHT_POINT",
        "load_states": ["WITHIN_LIMIT", "OVERWEIGHT"],
        "within_limit_effect": "NO_LOAD_BONUS_OR_PENALTY",
        "overweight_effect": "ASSIGNMENT_BLOCKED",
        "comfortable_load_is_current": False,
        "four_state_balance_is_current": False,
        "escalating_overload_penalty_exists": False,
        "constitution_or_dexterity_changes_maximum_load": False,
        "success_forecast_model": "ENHANCEMENT_DOMINANT_AUXILIARY_MODIFIERS",
        "risk_base_formula": "CLAMP_100_MINUS_RISK_X_10_TO_5_90",
        "enhancement_bonus_pp_per_level": 1,
        "relevant_stat_meets_risk_bonus_pp": 5,
        "relevant_stat_below_risk_bonus_pp": 0,
        "proficiency_bonus_pp": {"0": -10, "1": 0, "2": 5, "3": 10},
        "special_function_requirement_model": "BINARY_REQUIREMENT_WHEN_EVENT_REQUIRES",
        "final_success_clamp": "CLAMP_5_TO_95_PERCENT",
        "player_display_rounding": "NEAREST_10_PERCENT",
        "raw_item_attack_defense_handling_artistry_feed_general_forecast": False,
        "product_implementation": "BLOCKED",
    },
}
registry["current_decisions"] = [item for item in registry["current_decisions"] if item.get("id") != DECISION_ID]
registry["current_decisions"].append(new_decision)
for item in registry["current_decisions"]:
    if item.get("id") == "BS-CUSTOMER-20260805-01":
        item["refined_by"] = DECISION_ID
        item["contract"]["load_contract_status"] = "HISTORICAL_SUPERSEDED_BY_BS-CUSTOMER-20260806-01"
    if item.get("id") == "BS-UX-20260805-01":
        item["refined_by"] = DECISION_ID
        item["contract"]["post_equipment_layer"] = [
            "LOAD_STATUS",
            "SUCCESS_FORECAST",
            "KEY_REASON_CHIPS",
            "SPECIAL_FUNCTION_RISK_WHEN_RELEVANT",
        ]
        item["contract"]["detail_layer"] = [
            "ALL_RELEVANT_PROFICIENCIES",
            "TOTAL_WEIGHT_AND_MAXIMUM_LOAD",
            "SPECIAL_FUNCTION_REQUIREMENTS",
            "APPLICABLE_ITEM_STAT_BREAKDOWN",
        ]
alignment = registry.setdefault("implementation_alignment", {})
alignment["current_customer_load_model"] = "BINARY_MAXIMUM_LOAD_GATE_NOT_STARTED_BLOCKED"
alignment["current_customer_success_model"] = "ENHANCEMENT_DOMINANT_AUXILIARY_MODIFIERS_NOT_STARTED_BLOCKED"
write(registry_path, json.dumps(registry, ensure_ascii=False, separators=(",", ":")))

# Project design registry.
design_registry_path = "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
design_registry = json.loads(read(design_registry_path))
design_registry["current_batch"] = "R2_BATCH_005_4_OF_10"
design_registry["current_design_decision"] = DECISION_ID
new_docs = [
    {
        "document_id": "enhancement-dominant-simple-load-gate-canon",
        "source_path": "../../docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md",
        "status": "ACTIVE",
        "source_role": "current_binary_load_and_enhancement_dominant_forecast_contract",
    },
    {
        "document_id": "enhancement-dominant-simple-load-gate-design",
        "source_path": "../../docs/superpowers/specs/2026-08-06-enhancement-dominant-simple-load-gate-design.md",
        "status": "ACTIVE",
        "source_role": "approved_design_input_for_bs_customer_20260806_01",
    },
    {
        "document_id": "enhancement-dominant-simple-load-gate-plan",
        "source_path": "../../docs/superpowers/plans/2026-08-06-enhancement-dominant-simple-load-gate.md",
        "status": "ACTIVE",
        "source_role": "executed_canon_plan_for_bs_customer_20260806_01",
    },
]
existing_ids = {item.get("document_id") for item in design_registry["documents"]}
for doc in reversed(new_docs):
    if doc["document_id"] not in existing_ids:
        design_registry["documents"].insert(7, doc)
guards = [guard for guard in design_registry.get("routing_guards", []) if not guard.startswith("R2_BATCH_005_IS_ACTIVE_AT_")]
for guard in (
    "R2_BATCH_005_IS_ACTIVE_AT_4_OF_10_WITH_BS_CRAFT_20260805_02_BS_CUSTOMER_20260805_01_BS_UX_20260805_01_AND_BS_CUSTOMER_20260806_01",
    "CURRENT_LOAD_MODEL_IS_BINARY_MAXIMUM_LOAD_GATE",
    "ENHANCEMENT_IS_PRIMARY_CONTROLLABLE_CUSTOMER_SUCCESS_MODIFIER",
    "FOUR_STATE_LOAD_BALANCE_AND_ESCALATING_OVERLOAD_MUST_NOT_BE_ROUTED_AS_CURRENT",
):
    if guard not in guards:
        guards.insert(6, guard)
design_registry["routing_guards"] = guards
write(design_registry_path, json.dumps(design_registry, ensure_ascii=False, indent=2))

# Current decisions.
path = "CURRENT_CONFIRMED_DECISIONS.md"
text = read(path)
text = replace_required(text, "현재 승인 배치: `R2_BATCH_005 / 3/10`", "현재 승인 배치: `R2_BATCH_005 / 4/10`")
needle = "- `BS-UX-20260805-01`: 모바일 고객 카드 3단계 정보 공개와 설명 가능한 장비 판단 — `R2_BATCH_005_3_OF_10 / APPROVED_PENDING_MERGE`"
if DECISION_ID not in text:
    text = replace_required(
        text,
        needle,
        needle + "\n- `BS-CUSTOMER-20260806-01`: 강화 중심 단순 장비 판정과 근력 기반 최대 중량 게이트 — `R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE`",
    )
write(path, text)
append_once(
    path,
    "<!-- BS-CUSTOMER-20260806-01 -->",
    r'''<!-- BS-CUSTOMER-20260806-01 -->
## 강화 중심 단순 장비 판정

```text
최대 중량 = 근력 × 10
총 중량 ≤ 최대 중량 → 사용 가능, 보너스·페널티 없음
총 중량 > 최대 중량 → 중량 초과, 배정 불가
```

```text
위험도 기본 성공률
+ 강화 레벨(+1당 +1%p)
+ 관련 능력 충족(+5%p)
+ 적성 보정(-10/0/+5/+10%p)
```

- 강화가 주효과이며 고객 능력·적성은 작은 보조 보정이다.
- `COMFORTABLE_LOAD / BALANCE_STATE / 단계적 초과 페널티`는 현재 중량 계약이 아니다.
- 공격·방어·조작성·예술성 원수치를 일반 성공률에 범용 합산하지 않는다.
- 제품 구현: `BLOCKED`''',
)

# Game Bible.
path = "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
text = read(path)
text = replace_required(text, "R2_BATCH_005_3_OF_10", "R2_BATCH_005_4_OF_10", count=1)
if DECISION_ID not in text.split("\n", 8)[0:8]:
    text = text.replace("BS-UX-20260805-01 / BS-OPS-20260805-01", "BS-UX-20260805-01 / BS-CUSTOMER-20260806-01 / BS-OPS-20260805-01", 1)
write(path, text)
append_once(
    path,
    "<!-- BS-CUSTOMER-20260806-01 -->",
    r'''<!-- BS-CUSTOMER-20260806-01 -->
## 강화 중심 보조 판정

강화가 주효과다. 고객 능력치·적성·작품 원수치는 작품 배정을 설명하는 보조 요소만 담당한다.

```text
MAXIMUM_LOAD = STRENGTH × 10 WEIGHT_POINT
WITHIN_LIMIT → 보너스·페널티 없음
OVERWEIGHT → 중량 초과 시 배정 불가
```

```text
최종 성공률
= 위험도 기본 성공률
+ 강화 레벨(+1당 +1%p)
+ 관련 능력 충족(+5%p)
+ 적성 보정(-10/0/+5/+10%p)
```

공격·방어·조작성·예술성은 모든 고객 사건에 자동 합산하지 않는다. 제품 구현: `BLOCKED`.''',
)

# Refine previous customer canon.
path = "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md"
text = read(path)
text = text.replace("- **근력**: 총 장비 중량 감당, 무거운 작품 운용, 과중량 부담 완화", "- **근력**: 총 장비 중량의 최대 허용치 결정")
text = text.replace("## 6. 파생 장비 상태", "## 6. [역사적 계약] 파생 장비 상태\n\n`HISTORICAL_SUPERSEDED`: 아래 `COMFORTABLE_LOAD / BALANCE_STATE`와 단계적 초과 페널티는 `BS-CUSTOMER-20260806-01` 이전 계약이다.")
write(path, text)
append_once(
    path,
    "<!-- REFINED_BY_BS-CUSTOMER-20260806-01 -->",
    r'''<!-- REFINED_BY_BS-CUSTOMER-20260806-01 -->
## 단순 최대 중량 후속 정제

현재 중량 계약은 다음과 같다.

```text
TOTAL_WEIGHT / MAXIMUM_LOAD / LOAD_STATUS
MAXIMUM_LOAD = STRENGTH × 10 WEIGHT_POINT
WITHIN_LIMIT / OVERWEIGHT
```

- 한도 이내: 보너스·페널티 없음
- 중량 초과 시 배정 불가
- `COMFORTABLE_LOAD / BALANCE_STATE / ESCALATING_OVERLOAD_PENALTY`: `HISTORICAL_SUPERSEDED`
- 성공률은 강화가 주효과이며 고객 능력·적성은 작은 보조 보정만 제공한다.''',
)

# Refine mobile canon.
path = "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md"
text = read(path)
text = text.replace("- 균형 상태: 부적합 / 불안정 / 안정 / 능숙", "- 중량 상태: 사용 가능 / 중량 초과")
text = text.replace("- 총 중량과 적정 하중", "- 총 중량과 최대 중량")
text = text.replace("균형·예상 성공률·핵심 원인", "중량 상태·예상 성공률·핵심 원인")
write(path, text)
append_once(
    path,
    "<!-- REFINED_BY_BS-CUSTOMER-20260806-01 -->",
    r'''<!-- REFINED_BY_BS-CUSTOMER-20260806-01 -->
## 중량 표시 후속 정제

```text
LOAD_STATUS
WITHIN_LIMIT / OVERWEIGHT
총 중량 / 최대 중량
```

- `WITHIN_LIMIT`: 사용 가능, 중량 보너스·페널티 없음
- `OVERWEIGHT`: 중량 초과 시 배정 불가
- 기본 판단층에서 4단계 균형 상태와 단계적 중량 페널티를 표시하지 않는다.
- 상세 보기의 `TOTAL_WEIGHT_AND_COMFORTABLE_LOAD`는 `TOTAL_WEIGHT_AND_MAXIMUM_LOAD`로 정제한다.''',
)

# Hub authority documents: active batch and concise routing note.
hub_paths = [
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "[기획서]/00_프로젝트_허브/ROADMAP.md",
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
    "[기획서]/00_프로젝트_허브/START_HERE.md",
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md",
]
for path in hub_paths:
    text = read(path)
    text = text.replace("R2_BATCH_005_ACTIVE_3_OF_10", "R2_BATCH_005_ACTIVE_4_OF_10")
    text = text.replace("R2_BATCH_005_3_OF_10", "R2_BATCH_005_4_OF_10")
    text = text.replace("R2_BATCH_005_2_OF_10", "R2_BATCH_005_4_OF_10")
    text = text.replace("현재 승인 카운터: `3/10`", "현재 승인 카운터: `4/10`")
    text = text.replace("R2_BATCH_005 / 3/10", "R2_BATCH_005 / 4/10")
    write(path, text)
    append_once(
        path,
        "<!-- BS-CUSTOMER-20260806-01 -->",
        f'''<!-- BS-CUSTOMER-20260806-01 -->
### 강화 중심 단순 장비 판정

- Decision: `{DECISION_ID}` / `R2_BATCH_005_4_OF_10`
- 최대 중량: `STRENGTH × 10 WEIGHT_POINT`
- 상태: `WITHIN_LIMIT / OVERWEIGHT`; 초과 시 배정 불가
- 성공률: 강화 레벨이 주효과, 고객 능력·적성은 작은 보조 보정
- 정본: `{CANON_PATH}`
- 제품 구현: `BLOCKED`''',
    )

# Update existing test modules to current active batch and refined UX fields.
path = "tests/test_base_v942_planning_first_adoption.py"
text = read(path)
text = text.replace("test_batch_005_is_active_at_three_of_ten", "test_batch_005_is_active_at_four_of_ten")
text = text.replace("R2_BATCH_005_ACTIVE_3_OF_10", "R2_BATCH_005_ACTIVE_4_OF_10")
text = text.replace('self.assertEqual("3/10", self.registry["next_approval_counter"])', 'self.assertEqual("4/10", self.registry["next_approval_counter"])')
text = text.replace('self.assertEqual(3, active["approved_decisions"])', 'self.assertEqual(4, active["approved_decisions"])')
text = text.replace('self.assertEqual("3/10", active["counter"])', 'self.assertEqual("4/10", active["counter"])')
text = text.replace('["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01"]', '["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01", "BS-CUSTOMER-20260806-01"]')
text = text.replace('self.assertIn("R2_BATCH_005_3_OF_10", game_bible)', 'self.assertIn("R2_BATCH_005_4_OF_10", game_bible)')
text = text.replace('self.assertIn("R2_BATCH_005_3_OF_10", active)', 'self.assertIn("R2_BATCH_005_4_OF_10", active)')
text = text.replace('self.assertIn("R2_BATCH_005 / 3/10", root)', 'self.assertIn("R2_BATCH_005 / 4/10", root)')
write(path, text)

for path in ("tests/test_r2_artistry_generation_growth_economy.py", "tests/test_r2_customer_equipment_compatibility.py", "tests/test_r2_mobile_customer_card_progressive_disclosure.py"):
    text = read(path)
    text = text.replace("contains_three_approved_decisions", "contains_four_approved_decisions")
    text = text.replace("R2_BATCH_005_ACTIVE_3_OF_10", "R2_BATCH_005_ACTIVE_4_OF_10")
    text = text.replace('self.assertEqual("3/10", self.registry["next_approval_counter"])', 'self.assertEqual("4/10", self.registry["next_approval_counter"])')
    text = text.replace('self.assertEqual(3, active["approved_decisions"])', 'self.assertEqual(4, active["approved_decisions"])')
    text = text.replace('self.assertEqual("3/10", active["counter"])', 'self.assertEqual("4/10", active["counter"])')
    text = text.replace('["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01"]', '["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01", "BS-CUSTOMER-20260806-01"]')
    write(path, text)

path = "tests/test_r2_mobile_customer_card_progressive_disclosure.py"
text = read(path)
text = text.replace('["BALANCE_STATE", "SUCCESS_FORECAST", "KEY_REASON_CHIPS", "SPECIAL_FUNCTION_RISK_WHEN_RELEVANT"]', '["LOAD_STATUS", "SUCCESS_FORECAST", "KEY_REASON_CHIPS", "SPECIAL_FUNCTION_RISK_WHEN_RELEVANT"]')
text = text.replace('"TOTAL_WEIGHT_AND_COMFORTABLE_LOAD",', '"TOTAL_WEIGHT_AND_MAXIMUM_LOAD",')
text = text.replace('"SPECIAL_FUNCTION_FIT_FACTORS",', '"SPECIAL_FUNCTION_REQUIREMENTS",')
text = text.replace('self.assertIn("R2_BATCH_005_3_OF_10", bible)', 'self.assertIn("R2_BATCH_005_4_OF_10", bible)')
text = text.replace('self.assertIn("현재 승인 카운터: `3/10`", active)', 'self.assertIn("현재 승인 카운터: `4/10`", active)')
write(path, text)

# Project core alignment: active counters plus new decision assertions.
path = "tests/check_project_core_alignment.py"
text = read(path)
text = text.replace("R2_BATCH_005 / 3/10", "R2_BATCH_005 / 4/10")
text = text.replace("R2_BATCH_005_3_OF_10", "R2_BATCH_005_4_OF_10")
text = text.replace("R2_BATCH_005_ACTIVE_3_OF_10", "R2_BATCH_005_ACTIVE_4_OF_10")
text = text.replace("현재 승인 카운터: `3/10`", "현재 승인 카운터: `4/10`")
text = text.replace('"next_approval_counter": "3/10"', '"next_approval_counter": "4/10"')
text = text.replace('active.get("counter") != "3/10"', 'active.get("counter") != "4/10"')
text = text.replace('active batch must be R2_BATCH_005 at 3/10', 'active batch must be R2_BATCH_005 at 4/10')
text = text.replace('active.get("approved_decisions") != 3 or active.get("decisions") != ["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01"]', 'active.get("approved_decisions") != 4 or active.get("decisions") != ["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01", "BS-CUSTOMER-20260806-01"]')
text = text.replace('active batch 005 must contain the three approved decisions', 'active batch 005 must contain the four approved decisions')
entry_anchor = '    "docs/planning/BLACKSMITH_R2_CHECKPOINT_004_POSTMERGE_CLOSURE_2026.md": ('
new_entry = '''    "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md": (\n        "BS-CUSTOMER-20260806-01",\n        "R2_BATCH_005_4_OF_10",\n        "STRENGTH × 10 WEIGHT_POINT",\n        "WITHIN_LIMIT / OVERWEIGHT",\n        "강화 레벨 +1당 +1%p",\n        "제품 구현: `BLOCKED`",\n    ),\n'''
if CANON_PATH not in text:
    text = replace_required(text, entry_anchor, new_entry + entry_anchor)
check_anchor = '    alignment = registry.get("implementation_alignment", {})'
new_check = '''    simple = decisions.get("BS-CUSTOMER-20260806-01", {}).get("contract", {})\n    if simple.get("load_model") != "BINARY_MAXIMUM_LOAD_GATE":\n        failures.append("current customer load model must be the binary maximum-load gate")\n    if simple.get("maximum_load_formula") != "STRENGTH_X_10_WEIGHT_POINT":\n        failures.append("maximum load formula is incorrect")\n    if simple.get("load_states") != ["WITHIN_LIMIT", "OVERWEIGHT"]:\n        failures.append("current load states are incorrect")\n    if simple.get("overweight_effect") != "ASSIGNMENT_BLOCKED":\n        failures.append("overweight equipment must block assignment")\n    if simple.get("enhancement_bonus_pp_per_level") != 1:\n        failures.append("enhancement must contribute one percentage point per level")\n    if simple.get("raw_item_attack_defense_handling_artistry_feed_general_forecast") is not False:\n        failures.append("raw item support stats must not feed the general forecast")\n\n'''
if 'current customer load model must be the binary maximum-load gate' not in text:
    text = replace_required(text, check_anchor, new_check + check_anchor)
write(path, text)

# Operating audit: route new canon and active counters.
path = "tools/audit_project_operating_system.py"
text = read(path)
text = text.replace("R2_BATCH_005 / 3/10", "R2_BATCH_005 / 4/10")
text = text.replace("R2_BATCH_005_3_OF_10", "R2_BATCH_005_4_OF_10")
text = text.replace("R2_BATCH_005_ACTIVE_3_OF_10", "R2_BATCH_005_ACTIVE_4_OF_10")
text = text.replace("현재 승인 카운터: `3/10`", "현재 승인 카운터: `4/10`")
text = text.replace('"stage_status":"R2_BATCH_005_ACTIVE_3_OF_10"', '"stage_status":"R2_BATCH_005_ACTIVE_4_OF_10"')
text = text.replace('"next_approval_counter":"3/10"', '"next_approval_counter":"4/10"')
active_anchor = '    "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md",\n'
if CANON_PATH not in text:
    text = replace_required(text, active_anchor, active_anchor + f'    "{CANON_PATH}",\n', count=1)
required_anchor = '    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": ('
required_entry = f'''    "{CANON_PATH}": (\n        "BS-CUSTOMER-20260806-01",\n        "R2_BATCH_005_4_OF_10",\n        "STRENGTH × 10 WEIGHT_POINT",\n        "WITHIN_LIMIT / OVERWEIGHT",\n        "강화 레벨 +1당 +1%p",\n        "제품 구현: `BLOCKED`",\n    ),\n'''
if f'    "{CANON_PATH}": (' not in text:
    text = replace_required(text, required_anchor, required_entry + required_anchor)
text = text.replace('"부적합 / 불안정 / 안정 / 능숙",', '"HISTORICAL_SUPERSEDED",')
text = text.replace('"핵심 원인 2~4개",\n        "48dp",', '"핵심 원인 2~4개",\n        "LOAD_STATUS",\n        "WITHIN_LIMIT / OVERWEIGHT",\n        "48dp",')
text = text.replace('        \'"id":"BS-OPS-20260805-01"\',', '        \'"id":"BS-OPS-20260805-01"\',\n        \'"id":"BS-CUSTOMER-20260806-01"\',\n        \'"load_model":"BINARY_MAXIMUM_LOAD_GATE"\',\n        \'"maximum_load_formula":"STRENGTH_X_10_WEIGHT_POINT"\',')
write(path, text)

print("Enhancement-dominant simple load gate canon synchronization applied.")
