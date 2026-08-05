#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-ITEM-20260806-02"
BATCH_STATUS = "R2_BATCH_005_6_OF_10"
ACTIVE_STATUS = "R2_BATCH_005_ACTIVE_6_OF_10"
APPROVED_DECISIONS = [
    "BS-CRAFT-20260805-02",
    "BS-CUSTOMER-20260805-01",
    "BS-UX-20260805-01",
    "BS-CUSTOMER-20260806-01",
    "BS-ITEM-20260806-01",
    DECISION_ID,
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(read(path))


def dump_json(path: str, value: dict) -> None:
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def append_once(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def replace_method(text: str, name_pattern: str, replacement: str) -> str:
    pattern = rf"    def {name_pattern}\(self\) -> None:\n.*?(?=\n    def |\n\nif __name__)"
    updated, count = re.subn(pattern, replacement.rstrip(), text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"method replacement failed for {name_pattern}: {count}")
    return updated


def update_registry() -> None:
    path = "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
    registry = load_json(path)
    registry["stage_status"] = ACTIVE_STATUS
    registry["next_approval_counter"] = "6/10"
    active = registry["active_batch"]
    active["approved_decisions"] = 6
    active["counter"] = "6/10"
    active["decisions"] = APPROVED_DECISIONS

    decisions = registry["current_decisions"]
    by_id = {item.get("id"): item for item in decisions if isinstance(item, dict)}
    previous = by_id.get("BS-ITEM-20260806-01")
    if previous is not None:
        previous["refined_by"] = DECISION_ID
        previous["contract"]["single_active_modifier_rule_status"] = (
            "HISTORICAL_SUPERSEDED_BY_PRECISION_MILESTONE_WEIGHT_ADJUSTMENTS"
        )
        previous["contract"]["weighted_modifier_has_automatic_compensation"] = False
        previous["contract"]["weight_budget_refined_by"] = DECISION_ID

    customer = by_id.get("BS-CUSTOMER-20260806-01")
    if customer is not None:
        customer["weight_budget_refined_by"] = DECISION_ID

    ux = by_id.get("BS-UX-20260805-01")
    if ux is not None:
        ux["weight_budget_refined_by"] = DECISION_ID

    precision = by_id.get("BS-CRAFT-20260804-04")
    if precision is not None:
        methods = precision["contract"].setdefault("enhancement_methods", [])
        if "WEIGHTING" not in methods:
            methods.append("WEIGHTING")
        precision["weight_adjustment_refined_by"] = DECISION_ID

    contract = {
        "weight_performance_budget_model": "PEAK_RECOGNIZED_WEIGHT_MONOTONIC_SINGLE_SOURCE",
        "weight_performance_budget_formula": "MAX_INITIAL_OR_HIGHEST_SUCCESSFUL_CURRENT_WEIGHT_DIVIDED_BY_5",
        "weight_points_per_budget_point": 5,
        "initial_weight_grants_initial_budget": True,
        "lightweighting_preserves_existing_budget": True,
        "budget_recognized_weight_is_monotonic": True,
        "current_weight_drives_customer_load_gate": True,
        "weighting_grants_budget_only_above_previous_peak": True,
        "weight_adjustment_owner": "PRECISION_ENHANCEMENT_METHOD",
        "weight_delta_by_operation": {"LIGHTWEIGHTING": -5, "WEIGHTING": 5},
        "precision_milestones": [10, 20, 30, 40, 50],
        "maximum_weight_adjustments_per_precision_milestone": 1,
        "weight_adjustments_accumulate_across_distinct_milestones": True,
        "same_milestone_weight_adjustment_replay_allowed": False,
        "used_precision_milestone_refund_allowed": False,
        "budget_lanes": [
            "ATTACK_BUDGET",
            "DEFENSE_BUDGET",
            "MAGIC_FUNCTION_BUDGET",
            "UTILITY_BUDGET",
        ],
        "budget_point_allocates_to_exactly_one_lane": True,
        "equipment_lane_compatibility": {
            "WEAPON": ["ATTACK_BUDGET", "MAGIC_FUNCTION_BUDGET", "UTILITY_BUDGET"],
            "ARMOR": ["DEFENSE_BUDGET", "MAGIC_FUNCTION_BUDGET", "UTILITY_BUDGET"],
            "SHIELD_OR_OFFHAND": [
                "DEFENSE_BUDGET",
                "MAGIC_FUNCTION_BUDGET",
                "UTILITY_BUDGET",
            ],
            "TOOL": ["MAGIC_FUNCTION_BUDGET", "UTILITY_BUDGET"],
            "ACCESSORY": [],
        },
        "accessory_weight_budget_enabled_by_default": False,
        "weight_budget_directly_changes_generic_success_rate": False,
        "weight_budget_multiplied_by_other_progression_axes": False,
        "exact_stat_conversion": "BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
        "product_implementation": "BLOCKED",
    }
    new_decision = {
        "id": DECISION_ID,
        "title": "중량 성능 예산 기억과 정밀강화 경량화·중량화 기회비용",
        "status": "USER_APPROVED_R2_BATCH_005_6_OF_10_APPROVED_PENDING_MERGE",
        "refines": [
            "BS-ITEM-20260806-01",
            "BS-CRAFT-20260804-04",
            "BS-CUSTOMER-20260806-01",
        ],
        "canon": "docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md",
        "spec": "docs/superpowers/specs/2026-08-06-weight-performance-budget-and-lightweight-tradeoff-design.md",
        "plan": "docs/superpowers/plans/2026-08-06-weight-performance-budget-and-lightweight-tradeoff.md",
        "contract": contract,
    }
    if DECISION_ID in by_id:
        index = next(i for i, item in enumerate(decisions) if item.get("id") == DECISION_ID)
        decisions[index] = new_decision
    else:
        decisions.append(new_decision)
    dump_json(path, registry)


def update_design_registry() -> None:
    path = "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    registry = load_json(path)
    registry["current_batch"] = BATCH_STATUS
    registry["current_design_decision"] = DECISION_ID
    documents = registry["documents"]
    additions = [
        {
            "document_id": "weight-performance-budget-lightweight-tradeoff-canon",
            "source_path": "../../docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md",
            "status": "ACTIVE",
            "source_role": "current_weight_budget_memory_and_precision_adjustment_contract",
        },
        {
            "document_id": "weight-performance-budget-lightweight-tradeoff-design",
            "source_path": "../../docs/superpowers/specs/2026-08-06-weight-performance-budget-and-lightweight-tradeoff-design.md",
            "status": "ACTIVE",
            "source_role": "approved_design_input_for_bs_item_20260806_02",
        },
        {
            "document_id": "weight-performance-budget-lightweight-tradeoff-plan",
            "source_path": "../../docs/superpowers/plans/2026-08-06-weight-performance-budget-and-lightweight-tradeoff.md",
            "status": "ACTIVE",
            "source_role": "executed_canon_plan_for_bs_item_20260806_02",
        },
    ]
    existing = {item.get("document_id") for item in documents}
    for item in additions:
        if item["document_id"] not in existing:
            documents.append(item)
    dump_json(path, registry)


def create_canon() -> None:
    write(
        "docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md",
        """# [현재 정본] Blacksmith R2 중량 성능 예산 기억과 경량화·중량화 Canon

- Decision: `BS-ITEM-20260806-02`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_6_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-ITEM-20260806-01 / BS-CRAFT-20260804-04 / BS-CUSTOMER-20260806-01`
- 조정 소유권: `PRECISION_ENHANCEMENT_METHOD`
- 제품 구현: `BLOCKED`

## 1. 핵심 결론

중량이 높은 작품은 초기부터 더 큰 성능 예산을 가진다. 이후 경량화 작업을 해도 이미 작품에 확보된 공격·방어·마법 기능 등의 예산은 사라지지 않는다.

```text
최초 제작 중량 5당 초기 성능 예산 +1
경량화 -5 중량 / 기존 예산 유지
중량화 +5 중량 / 과거 최고 인정 중량 초과분만 예산 추가
정밀강화 +10 / +20 / +30 / +40 / +50
```

## 2. 저장값과 계산

```text
INITIAL_WEIGHT = 최초 제작 완료 시 장비군 기본 중량
CURRENT_WEIGHT = max(0, INITIAL_WEIGHT + 성공한 정밀강화 중량 조정 누계)
BUDGET_RECOGNIZED_WEIGHT = max(INITIAL_WEIGHT, UID가 성공적으로 달성한 역대 최고 CURRENT_WEIGHT)
WEIGHT_PERFORMANCE_BUDGET = BUDGET_RECOGNIZED_WEIGHT / 5
```

- 고객의 최대 중량 판정에는 `CURRENT_WEIGHT`만 사용한다.
- 성능 예산에는 `BUDGET_RECOGNIZED_WEIGHT`만 사용한다.
- 인정 중량과 성능 예산은 같은 UID에서 감소하지 않는다.
- 최초 제작 시점의 중량이 초기 예산을 즉시 만든다.
- 중량을 낮춰도 기존 예산과 이미 배분된 능력치는 유지한다.
- 중량화로 현재 중량이 과거 최고 인정 중량을 넘을 때만 초과분 5마다 예산 +1을 얻는다.

## 3. 성능 예산 축

한 예산점은 다음 호환 축 하나에만 배분한다.

```text
ATTACK_BUDGET
DEFENSE_BUDGET
MAGIC_FUNCTION_BUDGET
UTILITY_BUDGET
```

- 무기: 공격 / 마법 기능 / 유틸리티
- 방어구·방패: 방어 / 마법 기능 / 유틸리티
- 도구: 마법 기능 / 유틸리티
- 장신구: 기본적으로 중량 예산 없음
- 한 점을 여러 능력치에 동시에 중복 적용하지 않는다.
- 정확한 공격력·방어력·마력 기능 환산량은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 4. 정밀강화 기회비용

중량 조정은 촉매 수식어가 아니라 정밀강화 방식이다.

```text
+10 / +20 / +30 / +40 / +50
각 이정표에서 중량 조정 최대 1회
서로 다른 이정표의 조정은 누적 가능
같은 이정표 반복·환불·재선택 불가
```

경량화나 중량화를 선택하면 해당 이정표에서 공격·방어·마법·예술 마감 등 다른 강화 방식을 선택할 기회를 사용한다. 총 다섯 번뿐인 정밀강화 기회가 반복 조정의 자연스러운 비용이다.

## 5. 예시

### 장병기 경량화

```text
최초 중량 20 / 인정 중량 20 / 성능 예산 4
+10 경량화 성공
현재 중량 15 / 인정 중량 20 / 성능 예산 4 유지
```

### 같은 중량으로 복귀

```text
+20 중량화 성공
현재 중량 20 / 기존 인정 중량 20
추가 예산 0
```

### 새 최고 중량 달성

```text
+30 중량화 성공
현재 중량 25 / 기존 인정 중량 20
새 인정 중량 25 / 추가 예산 +1
```

### 중장갑 반복 경량화

```text
최초 중량 30 / 성능 예산 6
+10 경량화 → 현재 25 / 예산 6
+20 경량화 → 현재 20 / 예산 6
```

두 번의 정밀강화 기회를 소비해 낮은 근력 고객에게도 강한 장비를 사용할 가능성을 연다.

## 6. 고객 판정 경계

```text
MAXIMUM_LOAD = STRENGTH × 10
CURRENT_WEIGHT 합계 <= MAXIMUM_LOAD → 사용 가능
CURRENT_WEIGHT 합계 > MAXIMUM_LOAD → 배정 불가
```

`WITHIN_LIMIT / OVERWEIGHT` 이진 판정은 유지한다. 이동속도·피로·명중·회피 등의 추가 중량 페널티는 만들지 않는다.

## 7. 강화 중심성 보호

```text
일반 강화 성공·실패와 멈춤 판단
→ 정밀강화 기회를 성능 방향 또는 중량 조정에 사용
→ 작품 성능과 고객 근력을 함께 비교
→ 고객·사건·UID 생애 결과 환류
→ 다음 강화·복원·제작 판단
```

- 경량화는 성능 손실이 아니라 희소 정밀강화 기회를 지불하는 후가공이다.
- 중량화는 실제 새 최고 중량을 만들 때만 추가 성능 예산을 준다.
- 일반 강화 `+N`은 중량이나 예산을 자동 변경하지 않는다.
- 중량 예산은 일반 고객 사건 성공률에 직접 더하지 않는다.
- 재료·등급·예술성·촉매·연대기와 곱하지 않는다.

## 8. 적대적 검토

- 경량화 시 예산 감소: 사용자 의도와 작품 보존 판타지를 훼손하므로 폐기.
- 경량화·중량화 왕복 예산 복제: 과거 최고 인정 중량 이하의 중량화는 예산 0으로 차단.
- 무제한 경량화: 정밀강화 다섯 이정표와 이정표당 1회 제한으로 차단.
- 모든 능력치 동시 상승: 한 예산점은 한 호환 축에만 배분해 차단.
- 고객 판정에서 인정 중량 사용: 경량화 효용을 없애므로 금지하고 현재 중량만 사용.
- 장신구 중량화 파밍: 장신구는 기본 제외.

최종 판정: `P0 0 / P1 0`.

## 9. 구현 경계

- 계획 정본·검증 계약·권위 진입점·시트만 갱신한다.
- 런타임·게임 데이터·Scene·이미지·에셋은 변경하지 않는다.
- `data/crafting/weapon_bases.json`은 변경하지 않는다.
- 실제 밸런스 플레이테스트: `NOT_RUN`.
- 제품 구현: `BLOCKED`.
""",
    )


def update_authority_documents() -> None:
    root_path = "CURRENT_CONFIRMED_DECISIONS.md"
    root = read(root_path)
    root = re.sub(r"> 현재 승인 배치: `R2_BATCH_005 / \d+/10`", "> 현재 승인 배치: `R2_BATCH_005 / 6/10`", root, count=1)
    if f"- `{DECISION_ID}`:" not in root:
        anchor = "- `BS-ITEM-20260806-01`:"
        index = root.find(anchor)
        if index >= 0:
            line_end = root.find("\n", index)
            root = root[: line_end + 1] + (
                f"- `{DECISION_ID}`: 중량 성능 예산 기억과 정밀강화 경량화·중량화 기회비용 — "
                "`R2_BATCH_005_6_OF_10 / APPROVED_PENDING_MERGE`\n"
            ) + root[line_end + 1 :]
    root = re.sub(r"현재 `R2_BATCH_005 / \d+/10`이다\.", "현재 `R2_BATCH_005 / 6/10`이다.", root)
    write(root_path, root)
    append_once(
        root_path,
        "<!-- BS-ITEM-20260806-02 -->",
        """<!-- BS-ITEM-20260806-02 -->
## 중량 성능 예산 기억과 정밀강화 중량 조정

```text
최초 제작 중량 5당 초기 성능 예산 +1
경량화 -5 중량 / 기존 예산 유지
중량화 +5 중량 / 과거 최고 인정 중량 초과분만 예산 추가
```

고객 배정은 현재 중량을 사용하고 성능 예산은 UID의 역대 최고 인정 중량을 사용한다. 중량 조정은 `+10/+20/+30/+40/+50` 정밀강화에서만 선택하며 이정표당 최대 한 번, 서로 다른 이정표에서는 누적할 수 있다. 같은 이정표의 반복·환불은 허용하지 않는다. 중량 성능 예산은 공격·방어·마법 기능·유틸리티 중 호환 축 하나에만 배분하며 일반 사건 성공률에는 직접 더하지 않는다.

제품 구현: `BLOCKED`.
""",
    )

    bible_path = "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
    bible = read(bible_path)
    bible = bible.replace("R2_BATCH_005_5_OF_10", "R2_BATCH_005_6_OF_10", 1)
    write(bible_path, bible)
    append_once(
        bible_path,
        "<!-- BS-ITEM-20260806-02 -->",
        """<!-- BS-ITEM-20260806-02 -->
## 중량 성능 예산

- 최초 제작 중량 5당 초기 성능 예산 +1.
- 경량화는 현재 중량만 5 낮추고 기존 예산과 능력치를 유지한다.
- 중량화는 현재 중량이 UID의 과거 최고 인정 중량을 넘을 때만 초과분 5당 예산 +1.
- 고객 중량 판정은 현재 중량, 성능 예산은 인정 중량을 사용한다.
- 중량 조정은 정밀강화 `+10/+20/+30/+40/+50`에서만 이정표당 한 번 가능하다.
- 공격·방어·마법 기능·유틸리티 중 한 예산점은 한 호환 축에만 배분한다.
- 일반 사건 성공률 직접 보정과 다른 성장축 배율은 금지한다.
- 제품 구현: `BLOCKED`.
""",
    )

    refinement_blocks = {
        "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md": """<!-- REFINED_BY_BS-ITEM-20260806-02 -->
## [현재 후속 정제] 중량 예산 기억

- `REFINED_BY_BS-ITEM-20260806-02`
- `R2_BATCH_005_6_OF_10`
- 본문의 작품당 활성 중량 변경 최대 1개와 중량화 무보상 규칙은 `HISTORICAL_SUPERSEDED`다.
- 최초 제작 중량은 5당 초기 성능 예산 +1을 만든다.
- 경량화는 현재 중량을 5 낮추되 기존 예산을 유지한다.
- 중량화는 과거 최고 인정 중량을 실제로 넘어선 초과분에만 예산을 추가한다.
- 중량 조정은 정밀강화 이정표당 최대 1회이며 서로 다른 이정표에서는 누적 가능하다.
""",
        "docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md": """<!-- REFINED_BY_BS-ITEM-20260806-02 -->
## [현재 후속 정제] 정밀강화 방식의 중량 조정

- `REFINED_BY_BS-ITEM-20260806-02`
- `R2_BATCH_005_6_OF_10`
- 경량화와 중량화의 소유권은 `정밀강화 방식 / PRECISION_ENHANCEMENT_METHOD`이다.
- `+10/+20/+30/+40/+50` 각 이정표에서 중량 조정은 최대 1회다.
- 서로 다른 이정표의 경량화·중량화는 누적 가능하지만 같은 이정표 반복·환불은 금지한다.
- 경량화는 기존 성능 예산을 보존하고, 중량화는 새 최고 인정 중량 초과분만 예산을 추가한다.
- 촉매는 계속 `CATALYST_AFFIX` 계보·변형만 담당한다.
""",
        "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md": """<!-- REFINED_BY_BS-ITEM-20260806-02 -->
## [현재 후속 정제] 현재 중량과 인정 중량 분리

- `REFINED_BY_BS-ITEM-20260806-02`
- `R2_BATCH_005_6_OF_10`
- 고객 배정은 `CURRENT_WEIGHT`와 `MAXIMUM_LOAD`를 비교한다.
- 성능 예산의 `BUDGET_RECOGNIZED_WEIGHT`는 고객 하중 판정에 사용하지 않는다.
- `WITHIN_LIMIT / OVERWEIGHT` 이진 게이트와 강화 중심 성공률 공식은 유지한다.
- 중량 예산은 일반 사건 성공률에 직접 더하지 않는다.
""",
        "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md": """<!-- REFINED_BY_BS-ITEM-20260806-02 -->
## [현재 후속 정제] 고객 근력과 작품 중량 예산

- `REFINED_BY_BS-ITEM-20260806-02`
- `R2_BATCH_005_6_OF_10`
- 고객 근력은 현재 장착 중량의 사용 가능 여부만 결정한다.
- 경량화된 작품은 기존 성능 예산을 유지하면서 더 낮은 근력 고객에게 배정될 수 있다.
- 작품 공격·방어·마법 기능 원수치는 계속 작품 UID가 소유한다.
""",
        "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md": """<!-- REFINED_BY_BS-ITEM-20260806-02 -->
## [현재 후속 정제] 중량 조정 미리보기

- `REFINED_BY_BS-ITEM-20260806-02`
- `R2_BATCH_005_6_OF_10`
- 정밀강화 미리보기에는 `현재 중량 전후`, `인정 중량`, `성능 예산`, `새로 획득하는 예산`, `사용 가능 고객 변화`를 표시한다.
- 경량화 시 예산 감소를 표시하지 않는다.
- 고객 카드의 배정 가능 여부는 현재 중량을 사용한다.
""",
    }
    for path, block in refinement_blocks.items():
        append_once(path, "REFINED_BY_BS-ITEM-20260806-02", block)

    hub_paths = [
        "[기획서]/00_프로젝트_허브/START_HERE.md",
        "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
        "[기획서]/00_프로젝트_허브/ROADMAP.md",
        "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
        "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md",
    ]
    for path in hub_paths:
        text = read(path)
        text = text.replace("R2_BATCH_005_ACTIVE_5_OF_10", ACTIVE_STATUS)
        text = text.replace("R2_BATCH_005_5_OF_10", BATCH_STATUS)
        text = text.replace("현재 승인 카운터: `5/10`", "현재 승인 카운터: `6/10`")
        if path.endswith("ROADMAP.md"):
            text = re.sub(r"NEXT_APPROVAL_COUNTER: \d+/10", "NEXT_APPROVAL_COUNTER: 6/10", text, count=1)
        write(path, text)
        append_once(
            path,
            "BS-ITEM-20260806-02",
            """## BS-ITEM-20260806-02 — 중량 성능 예산 기억

- 상태: `R2_BATCH_005_6_OF_10 / APPROVED_PENDING_MERGE`
- 최초 제작 중량 5당 초기 성능 예산 +1.
- 경량화는 현재 중량만 감소하고 기존 예산을 유지.
- 중량화는 과거 최고 인정 중량 초과분만 예산 추가.
- 정밀강화 다섯 이정표에서 이정표당 중량 조정 최대 1회.
- 제품 구현: `BLOCKED`.
""",
        )


def update_focused_tests() -> None:
    common_method = """    def test_batch_005_contains_six_approved_decisions(self) -> None:
        self.assertEqual("R2_BATCH_005_ACTIVE_6_OF_10", self.registry["stage_status"])
        self.assertEqual("6/10", self.registry["next_approval_counter"])
        active = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_005", active["id"])
        self.assertEqual(6, active["approved_decisions"])
        self.assertEqual("6/10", active["counter"])
        self.assertEqual(
            [
                "BS-CRAFT-20260805-02",
                "BS-CUSTOMER-20260805-01",
                "BS-UX-20260805-01",
                "BS-CUSTOMER-20260806-01",
                "BS-ITEM-20260806-01",
                "BS-ITEM-20260806-02",
            ],
            active["decisions"],
        )
"""
    focused = [
        "tests/test_r2_artistry_generation_growth_economy.py",
        "tests/test_r2_customer_equipment_compatibility.py",
        "tests/test_r2_mobile_customer_card_progressive_disclosure.py",
        "tests/test_r2_enhancement_dominant_simple_load_gate.py",
        "tests/test_r2_equipment_base_weight_points.py",
    ]
    for path in focused:
        text = read(path)
        text = replace_method(
            text,
            r"test_batch_005_contains_(?:five|six)_approved_decisions",
            common_method,
        )
        text = text.replace('self.assertIn("R2_BATCH_005 / 5/10", current)', 'self.assertIn("R2_BATCH_005 / 6/10", current)')
        text = text.replace('self.assertIn("R2_BATCH_005 / 5/10", root)', 'self.assertIn("R2_BATCH_005 / 6/10", root)')
        write(path, text)

    base_path = "tests/test_base_v942_planning_first_adoption.py"
    base = read(base_path)
    base_method = """    def test_batch_005_is_active_at_six_of_ten(self) -> None:
        self.assertEqual("R2_BATCH_005_ACTIVE_6_OF_10", self.registry["stage_status"])
        self.assertEqual("6/10", self.registry["next_approval_counter"])
        self.assertEqual("BLOCKED", self.registry["product_implementation"])
        active = self.registry["active_batch"]
        self.assertEqual("R2_BATCH_005", active["id"])
        self.assertEqual(6, active["approved_decisions"])
        self.assertEqual("6/10", active["counter"])
        self.assertEqual(
            [
                "BS-CRAFT-20260805-02",
                "BS-CUSTOMER-20260805-01",
                "BS-UX-20260805-01",
                "BS-CUSTOMER-20260806-01",
                "BS-ITEM-20260806-01",
                "BS-ITEM-20260806-02",
            ],
            active["decisions"],
        )
        self.assertEqual(10, active["maximum_size"])
"""
    base = replace_method(
        base,
        r"test_batch_005_is_active_at_(?:five|six)_of_ten",
        base_method,
    )
    base = base.replace('self.assertIn("R2_BATCH_005_5_OF_10", game_bible)', 'self.assertIn("R2_BATCH_005_6_OF_10", game_bible)')
    base = base.replace('self.assertIn("R2_BATCH_005_5_OF_10", active)', 'self.assertIn("R2_BATCH_005_6_OF_10", active)')
    base = base.replace('self.assertIn("R2_BATCH_005 / 5/10", root)', 'self.assertIn("R2_BATCH_005 / 6/10", root)')
    write(base_path, base)


def update_core_alignment() -> None:
    path = "tests/check_project_core_alignment.py"
    text = read(path)
    text = text.replace('"R2_BATCH_005 / 5/10",', '"R2_BATCH_005 / 6/10",', 1)
    text = text.replace('"R2_BATCH_005_5_OF_10",', '"R2_BATCH_005_6_OF_10",', 1)
    text = text.replace('"R2_BATCH_005_ACTIVE_5_OF_10",', '"R2_BATCH_005_ACTIVE_6_OF_10",')
    text = text.replace('"현재 승인 카운터: `5/10`",', '"현재 승인 카운터: `6/10`",')
    text = text.replace('"stage_status": "R2_BATCH_005_ACTIVE_5_OF_10",', '"stage_status": "R2_BATCH_005_ACTIVE_6_OF_10",')
    text = text.replace('"next_approval_counter": "5/10",', '"next_approval_counter": "6/10",')

    active_pattern = re.compile(
        r'    active = registry\.get\("active_batch", \{\}\)\n.*?(?=    if active\.get\("maximum_size"\))',
        re.S,
    )
    active_block = '''    active = registry.get("active_batch", {})
    if active.get("id") != "R2_BATCH_005" or active.get("counter") != "6/10":
        failures.append("active batch must be R2_BATCH_005 at 6/10")
    if active.get("approved_decisions") != 6 or active.get("decisions") != [
        "BS-CRAFT-20260805-02",
        "BS-CUSTOMER-20260805-01",
        "BS-UX-20260805-01",
        "BS-CUSTOMER-20260806-01",
        "BS-ITEM-20260806-01",
        "BS-ITEM-20260806-02",
    ]:
        failures.append("active batch 005 must contain the six approved decisions")
'''
    text, count = active_pattern.subn(active_block, text, count=1)
    if count != 1:
        raise RuntimeError(f"core alignment active block replacement failed: {count}")

    required_marker = '    "docs/planning/BLACKSMITH_R2_CHECKPOINT_004_POSTMERGE_CLOSURE_2026.md": ('
    if "BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md" not in text:
        entry = '''    "docs/planning/BLACKSMITH_R2_WEIGHT_PERFORMANCE_BUDGET_AND_LIGHTWEIGHT_TRADEOFF_CANON_2026.md": (
        "BS-ITEM-20260806-02",
        "R2_BATCH_005_6_OF_10",
        "최초 제작 중량 5당 초기 성능 예산 +1",
        "경량화 -5 중량 / 기존 예산 유지",
        "중량화 +5 중량 / 과거 최고 인정 중량 초과분만 예산 추가",
        "PRECISION_ENHANCEMENT_METHOD",
        "제품 구현: `BLOCKED`",
    ),
'''
        text = text.replace(required_marker, entry + required_marker, 1)

    if "weight budget memory contract is incomplete" not in text:
        insertion = '''
    weight_budget = decisions.get("BS-ITEM-20260806-02", {}).get("contract", {})
    if weight_budget.get("weight_performance_budget_model") != "PEAK_RECOGNIZED_WEIGHT_MONOTONIC_SINGLE_SOURCE":
        failures.append("weight budget memory contract is incomplete")
    if weight_budget.get("weight_performance_budget_formula") != "MAX_INITIAL_OR_HIGHEST_SUCCESSFUL_CURRENT_WEIGHT_DIVIDED_BY_5":
        failures.append("weight budget formula is incorrect")
    if weight_budget.get("lightweighting_preserves_existing_budget") is not True:
        failures.append("lightweighting must preserve existing budget")
    if weight_budget.get("weighting_grants_budget_only_above_previous_peak") is not True:
        failures.append("weighting must grant budget only above the previous peak")
    if weight_budget.get("precision_milestones") != [10, 20, 30, 40, 50]:
        failures.append("precision weight milestones are incomplete")
    if weight_budget.get("maximum_weight_adjustments_per_precision_milestone") != 1:
        failures.append("precision milestone weight adjustment limit must be one")
    if weight_budget.get("same_milestone_weight_adjustment_replay_allowed") is not False:
        failures.append("same milestone weight adjustment replay must be false")
    if weight_budget.get("product_implementation") != "BLOCKED":
        failures.append("weight budget product implementation must remain blocked")
'''
        text = text.replace("\ndef check_legacy", insertion + "\n\ndef check_legacy", 1)
    write(path, text)


def update_operating_audit() -> None:
    path = "tools/audit_project_operating_system.py"
    text = read(path)
    text = text.replace("R2_BATCH_005_ACTIVE_5_OF_10", ACTIVE_STATUS)
    text = text.replace("R2_BATCH_005 / 5/10", "R2_BATCH_005 / 6/10")
    text = text.replace("R2_BATCH_005_5_OF_10", BATCH_STATUS, 1)
    write(path, text)


def main() -> None:
    update_registry()
    update_design_registry()
    create_canon()
    update_authority_documents()
    update_focused_tests()
    update_core_alignment()
    update_operating_audit()


if __name__ == "__main__":
    main()
