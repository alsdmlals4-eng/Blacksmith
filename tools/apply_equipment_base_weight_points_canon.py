#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-ITEM-20260806-01"
CANON_PATH = "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md"
SPEC_PATH = "docs/superpowers/specs/2026-08-06-equipment-base-weight-points-design.md"
PLAN_PATH = "docs/superpowers/plans/2026-08-06-equipment-base-weight-points.md"

BASE_WEIGHTS = {
    "ACCESSORY": 0,
    "TOOL": 5,
    "CLOTHING_OR_ROBE": 5,
    "LIGHT_ARMOR": 10,
    "MEDIUM_ARMOR": 20,
    "HEAVY_ARMOR": 30,
    "SWORD": 10,
    "AXE": 15,
    "BLUNT": 15,
    "POLEARM": 20,
    "RANGED": 10,
    "SHIELD_SUPPORT": 10,
}


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


CANON = r'''# [현재 정본] Blacksmith R2 장비군 기본 중량 포인트 Canon

- Decision: `BS-ITEM-20260806-01`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_5_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-CUSTOMER-20260806-01 / BS-CUSTOMER-20260805-01 / BS-UX-20260805-01`
- 제품 구현: `BLOCKED`

## 1. 핵심 원칙

중량은 고객이 작품을 사용할 수 있는지만 판단하는 보조 정보다. 장비 중량 자체를 새로운 성장·전투력·경제 최적화 축으로 만들지 않는다.

```text
장비군 고정 기본 중량
+ 중량 전용 명시 효과 최대 1개
→ 총 중량
→ 근력 기반 최대 중량과 비교
```

## 2. 단위

- 현실 kg가 아닌 정수형 `WEIGHT_POINT`를 사용한다.
- 기본값과 변경값은 모두 5단위다.
- `0`은 중량 부담을 계산하지 않는 장신구 기본값이다.

## 3. 장비군 기본 중량표

| 장비군 | ID | 기본 중량 |
|---|---|---:|
| 장신구 | `ACCESSORY` | 0 |
| 도구 | `TOOL` | 5 |
| 의복·로브 | `CLOTHING_OR_ROBE` | 5 |
| 경갑 | `LIGHT_ARMOR` | 10 |
| 중갑 | `MEDIUM_ARMOR` | 20 |
| 중장갑 | `HEAVY_ARMOR` | 30 |
| 검류 | `SWORD` | 10 |
| 도끼류 | `AXE` | 15 |
| 둔기류 | `BLUNT` | 15 |
| 장병기류 | `POLEARM` | 20 |
| 원거리류 | `RANGED` | 10 |
| 방패·보조장비 | `SHIELD_SUPPORT` | 10 |

현재 제품 데이터의 계획상 대응은 다음과 같다.

```text
sword -> SWORD -> 10
spear -> POLEARM -> 20
axe -> AXE -> 15
```

이번 Decision에서는 `data/crafting/weapon_bases.json`을 수정하지 않는다.

## 4. 계산식

```text
ITEM_WEIGHT = max(0, BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER)
TOTAL_WEIGHT = 모든 중량 적용 장비 ITEM_WEIGHT의 합
MAXIMUM_LOAD = STRENGTH × 10 WEIGHT_POINT
```

- `TOTAL_WEIGHT ≤ MAXIMUM_LOAD`: 사용 가능, 보너스·페널티 없음.
- `TOTAL_WEIGHT > MAXIMUM_LOAD`: 중량 초과, 배정 불가.
- 한도와 정확히 일치해도 보너스가 없다.

## 5. 중량 전용 명시 효과

```text
LIGHTWEIGHT: -5 WEIGHT_POINT
NONE: 0
WEIGHTED: +5 WEIGHT_POINT
```

- 작품 하나당 활성 중량 변경은 최대 하나다.
- 여러 출처를 합산하거나 곱하지 않는다.
- 최종 작품 중량 최솟값은 `0`이다.
- 경량화는 중량 한도를 통과시키는 보조 선택이며 성공률을 직접 올리지 않는다.
- 중량화에는 공격력·가치·성공률 자동 보상을 붙이지 않는다.
- 보상이 필요한 개별 강화 효과는 그 효과에 별도로 명시한다.

## 6. 자동 중량 변경 금지

다음 축은 작품 중량을 자동 변경하지 않는다.

```text
MATERIAL
CRAFTSMANSHIP_GRADE
ARTISTRY
ATTACK
DEFENSE
HANDLING
DURABILITY
GENERAL_ENHANCEMENT_LEVEL
```

- 재료 밀도·부피·부품 비율 계산 없음.
- 제작 등급이 높다고 더 무겁거나 가벼워지지 않음.
- 일반 강화 `+N`이 중량을 자동 증가·감소시키지 않음.
- 예술성·공격·방어·조작성·내구도와 중량을 이중 계산하지 않음.

## 7. 플레이어 표시

작품 정보:

```text
중량 15
```

중량 전용 효과가 있을 때만 이유 칩을 하나 표시한다.

```text
경량화 -5
중량화 +5
```

고객 배정 화면:

```text
총 중량 35 / 최대 중량 40 · 사용 가능
총 중량 45 / 최대 중량 40 · 중량 초과 · 배정 불가
```

초과율·속도·피로·명중·회피 페널티는 표시하거나 계산하지 않는다.

## 8. 강화 중심성 보호

```text
강화 성공·실패와 멈춤 판단
→ 필요하면 중량 전용 강화 선택
→ 고객 최대 중량 확인
→ 사건과 UID 생애 환류
→ 다음 강화·복원·제작 판단
```

- 중량은 강화보다 중요한 성장 축이 아니다.
- 높은 중량 자체를 품질·희귀도·공격력으로 취급하지 않는다.
- 고객 능력·장비 중량·작품 원수치를 종합 전투력 점수로 합치지 않는다.
- 장신구 슬롯 수 문제는 별도 장비 슬롯 규칙의 책임이며 중량으로 해결하지 않는다.

## 9. 벤치마킹·현업 비교

### D&D Basic Rules

힘 점수에 일정 계수를 곱해 운반 한도를 구하는 설명 가능한 구조는 채택한다. 선택 규칙의 단계별 이동·판정 불이익은 Blacksmith의 보조 시스템에는 과하므로 비채택한다.

- Adopt: 힘과 최대 중량의 단순 관계
- Reject: 여러 단계의 속도·공격·판정 페널티
- Source: https://www.dndbeyond.com/sources/dnd/basic-rules-2014/using-ability-scores

### Bethesda RPG support guidance

Oblivion Remastered의 `carry weight = Strength × 5`처럼 능력치와 한도를 직접 연결하는 방식은 수정 채택한다. Skyrim식 초과 이동 불이익은 고객을 직접 조작하지 않는 Blacksmith에는 필요하지 않다.

- Adapt: 직관적인 능력치×계수
- Reject: 초과 상태의 이동 속도 게임플레이
- Sources:
  - https://help.bethesda.net/app/answers/detail/a_id/69972/
  - https://help.bethesda.net/app/answers/detail/a_id/16579/

### Elden Ring Nightreign

제한된 인벤토리 구조에서는 무기 중량과 장비 하중을 제거해 판단 비용을 낮춘 사례가 있다. Blacksmith는 고객 배정 가능 여부를 설명할 가치가 있어 중량을 완전히 제거하지 않고 이진 게이트만 남긴다.

- Adopt: 핵심과 무관한 하중 최적화 축을 줄이는 방향
- Adapt: 완전 제거 대신 고정값·이진 게이트
- Source: https://en.bandainamcoent.eu/elden-ring/news/beginner-tips-elden-ring-nightreign

## 10. 적대적 검토

- `POLEARM 20 + HEAVY_ARMOR 30`은 근력 5부터 사용 가능하다. 별도 페널티 없이 최대 중량 게이트만으로 설명된다.
- `ACCESSORY 0`은 무제한 슬롯을 허용한다는 뜻이 아니다. 슬롯 수는 별도 책임이다.
- `LIGHTWEIGHT -5` 중첩은 최대 중량을 무력화하므로 작품당 하나로 제한한다.
- `WEIGHTED +5` 자동 보상은 중량을 필수 최적화 축으로 만들 수 있어 금지한다.
- 재료 무게 차이를 제거해 현실성이 낮아질 수 있으나 재료 개성은 공격·내구·특수기능·미학 등 직접적인 제작 결과로 표현한다.

최종 판정: `P0 0 / P1 0`.

## 11. 구현 경계

- 계획 정본·검증 계약만 갱신.
- 런타임·게임 데이터·Scene·이미지·에셋 변경 금지.
- 실제 밸런스 플레이테스트: `NOT_RUN`.
- 제품 구현: `BLOCKED`.
'''

write(CANON_PATH, CANON)

# Machine-readable R2 registry.
registry_path = "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
registry = json.loads(read(registry_path))
registry["stage_status"] = "R2_BATCH_005_ACTIVE_5_OF_10"
registry["next_approval_counter"] = "5/10"
active = registry["active_batch"]
active["approved_decisions"] = 5
active["counter"] = "5/10"
active["decisions"] = [
    "BS-CRAFT-20260805-02",
    "BS-CUSTOMER-20260805-01",
    "BS-UX-20260805-01",
    "BS-CUSTOMER-20260806-01",
    DECISION_ID,
]
new_decision = {
    "id": DECISION_ID,
    "title": "장비군 고정 기본 중량 포인트와 중량 전용 강화 효과",
    "status": "USER_APPROVED_R2_BATCH_005_5_OF_10_APPROVED_PENDING_MERGE",
    "refines": ["BS-CUSTOMER-20260806-01", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01"],
    "canon": CANON_PATH,
    "spec": SPEC_PATH,
    "plan": PLAN_PATH,
    "contract": {
        "base_weight_model": "EQUIPMENT_GROUP_FIXED_BASE_WEIGHT",
        "weight_unit": "WEIGHT_POINT",
        "base_weight_points": BASE_WEIGHTS,
        "current_weapon_base_group_mapping": {"sword": "SWORD", "spear": "POLEARM", "axe": "AXE"},
        "item_weight_formula": "BASE_WEIGHT_PLUS_ONE_EXPLICIT_MODIFIER",
        "explicit_weight_modifiers": {"LIGHTWEIGHT": -5, "NONE": 0, "WEIGHTED": 5},
        "maximum_active_weight_modifiers_per_item": 1,
        "minimum_final_item_weight": 0,
        "weight_modifiers_stack": False,
        "weight_modifier_multiplies_base_weight": False,
        "weight_modifier_directly_changes_success_rate": False,
        "weighted_modifier_has_automatic_compensation": False,
        "forbidden_automatic_weight_sources": [
            "MATERIAL",
            "CRAFTSMANSHIP_GRADE",
            "ARTISTRY",
            "ATTACK",
            "DEFENSE",
            "HANDLING",
            "DURABILITY",
            "GENERAL_ENHANCEMENT_LEVEL",
        ],
        "player_item_display": "INTEGER_WEIGHT_ONLY",
        "player_modifier_reason_chips": ["경량화 -5", "중량화 +5"],
        "product_implementation": "BLOCKED",
    },
}
registry["current_decisions"] = [item for item in registry["current_decisions"] if item.get("id") != DECISION_ID]
registry["current_decisions"].append(new_decision)
for item in registry["current_decisions"]:
    if item.get("id") == "BS-CUSTOMER-20260806-01":
        item["refined_by"] = DECISION_ID
    if item.get("id") in {"BS-CUSTOMER-20260805-01", "BS-UX-20260805-01"}:
        item["weight_refined_by"] = DECISION_ID
alignment = registry.setdefault("implementation_alignment", {})
alignment["current_item_weight_model"] = "EQUIPMENT_GROUP_FIXED_BASE_WEIGHT_PLUS_ONE_EXPLICIT_MODIFIER"
alignment["equipment_base_weight_product_implementation"] = "NOT_STARTED_BLOCKED"
write(registry_path, json.dumps(registry, ensure_ascii=False, separators=(",", ":")))

# Design-document registry.
design_path = "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
design = json.loads(read(design_path))
design["current_batch"] = "R2_BATCH_005_5_OF_10"
design["current_design_decision"] = DECISION_ID
new_docs = [
    {
        "document_id": "equipment-base-weight-points-canon",
        "source_path": "../../docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md",
        "status": "ACTIVE",
        "source_role": "current_equipment_group_base_weight_contract",
    },
    {
        "document_id": "equipment-base-weight-points-design",
        "source_path": "../../docs/superpowers/specs/2026-08-06-equipment-base-weight-points-design.md",
        "status": "ACTIVE",
        "source_role": "approved_design_input_for_bs_item_20260806_01",
    },
    {
        "document_id": "equipment-base-weight-points-plan",
        "source_path": "../../docs/superpowers/plans/2026-08-06-equipment-base-weight-points.md",
        "status": "ACTIVE",
        "source_role": "executed_canon_plan_for_bs_item_20260806_01",
    },
]
existing_ids = {item.get("document_id") for item in design["documents"]}
for item in new_docs:
    if item["document_id"] not in existing_ids:
        design["documents"].append(item)
design["routing_guards"] = [
    guard
    for guard in design["routing_guards"]
    if not guard.startswith("R2_BATCH_005_IS_ACTIVE_AT_")
]
design["routing_guards"].extend(
    [
        "R2_BATCH_005_IS_ACTIVE_AT_5_OF_10_WITH_BS_ITEM_20260806_01",
        "CURRENT_ITEM_WEIGHT_USES_EQUIPMENT_GROUP_FIXED_BASE_WEIGHT",
        "ONLY_ONE_EXPLICIT_PLUS_OR_MINUS_FIVE_WEIGHT_MODIFIER_IS_ALLOWED_PER_ITEM",
        "MATERIAL_GRADE_ARTISTRY_RAW_STATS_AND_GENERAL_ENHANCEMENT_DO_NOT_AUTOMATICALLY_CHANGE_WEIGHT",
        "EQUIPMENT_BASE_WEIGHT_PRODUCT_IMPLEMENTATION_REMAINS_BLOCKED",
    ]
)
write(design_path, json.dumps(design, ensure_ascii=False, indent=2))

# Current authority entrypoints.
current_path = "CURRENT_CONFIRMED_DECISIONS.md"
current = read(current_path)
current = replace_required(current, "현재 승인 배치: `R2_BATCH_005 / 4/10`", "현재 승인 배치: `R2_BATCH_005 / 5/10`", count=1)
needle = "- `BS-CUSTOMER-20260806-01`: 강화 중심 단순 장비 판정과 근력 기반 최대 중량 게이트 — `R2_BATCH_005_4_OF_10 / APPROVED_PENDING_MERGE`"
current = replace_required(
    current,
    needle,
    needle + "\n- `BS-ITEM-20260806-01`: 장비군 고정 기본 중량 포인트와 중량 전용 ±5 강화 효과 — `R2_BATCH_005_5_OF_10 / APPROVED_PENDING_MERGE`",
    count=1,
)
write(current_path, current)
append_once(
    current_path,
    "<!-- BS-ITEM-20260806-01 -->",
    r'''<!-- BS-ITEM-20260806-01 -->
## 장비군 기본 중량 포인트

```text
장신구 0 / 도구 5
의복·로브 5 / 경갑 10 / 중갑 20 / 중장갑 30
검·원거리·방패보조 10 / 도끼·둔기 15 / 장병기 20
```

`ITEM_WEIGHT = max(0, BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER)`다. 중량 전용 효과는 작품당 하나만 허용하며 `LIGHTWEIGHT -5 / NONE 0 / WEIGHTED +5`다. 재료·제작 등급·예술성·공격·방어·조작성·내구도·일반 강화 단계는 중량을 자동 변경하지 않는다. 제품 구현: `BLOCKED`.''',
)

bible_path = "docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md"
bible = read(bible_path)
bible = replace_required(bible, "상태: `CURRENT_CANON / R2_BATCH_005_4_OF_10`", "상태: `CURRENT_CANON / R2_BATCH_005_5_OF_10`", count=1)
bible = replace_required(
    bible,
    "BS-UX-20260805-01 / BS-CUSTOMER-20260806-01 / BS-OPS-20260805-01",
    "BS-UX-20260805-01 / BS-CUSTOMER-20260806-01 / BS-ITEM-20260806-01 / BS-OPS-20260805-01",
    count=1,
)
if "현재 `R2_BATCH_005_2_OF_10`" in bible:
    bible = bible.replace("현재 `R2_BATCH_005_2_OF_10`", "현재 `R2_BATCH_005_5_OF_10`", 1)
write(bible_path, bible)
append_once(
    bible_path,
    "<!-- BS-ITEM-20260806-01 -->",
    r'''<!-- BS-ITEM-20260806-01 -->
## 장비군 고정 기본 중량

```text
ACCESSORY 0 / TOOL 5
CLOTHING_OR_ROBE 5 / LIGHT_ARMOR 10 / MEDIUM_ARMOR 20 / HEAVY_ARMOR 30
SWORD 10 / AXE 15 / BLUNT 15 / POLEARM 20 / RANGED 10 / SHIELD_SUPPORT 10
```

작품 중량은 `BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER`이며 최솟값은 0이다. 작품당 중량 전용 효과는 하나만 허용한다. 재료·제작 등급·예술성·공격·방어·조작성·내구도·일반 강화 단계는 중량을 자동 변경하지 않는다. 장비군 고정 기본 중량은 고객 배정 가능 여부만 보조하며 강화보다 중요한 성장 축이 아니다. 제품 구현: `BLOCKED`.''',
)

refinement_block = r'''<!-- REFINED_BY_BS-ITEM-20260806-01 -->
## 장비군 기본 중량 후속 정제

현재 작품 중량 계약은 다음과 같다.

```text
ITEM_WEIGHT = max(0, BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER)
BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER
LIGHTWEIGHT -5 / NONE 0 / WEIGHTED +5
```

- 장비군 고정 기본값은 5단위다.
- 작품당 중량 전용 변경은 최대 하나다.
- 재료·등급·예술성·원수치·일반 강화 단계는 중량을 자동 변경하지 않는다.
- 현재 후속 정제 배치: `R2_BATCH_005_5_OF_10`
- 제품 구현: `BLOCKED`.'''
for path in (
    "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md",
    "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md",
):
    append_once(path, "REFINED_BY_BS-ITEM-20260806-01", refinement_block)
append_once(
    "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md",
    "REFINED_BY_BS-ITEM-20260806-01",
    refinement_block + r'''

모바일 작품 정보에는 `중량 N`만 기본 표시하고 중량 전용 효과가 있을 때만 `경량화 -5` 또는 `중량화 +5` 이유 칩을 표시한다.''',
)

# Hub documents: update only the first current marker and append a focused block.
hub_updates = {
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": [
        ("R2_BATCH_005_4_OF_10", "R2_BATCH_005_5_OF_10"),
        ("현재 승인 카운터: `4/10`", "현재 승인 카운터: `5/10`"),
    ],
    "[기획서]/00_프로젝트_허브/ROADMAP.md": [
        ("R2_BATCH_005_ACTIVE_4_OF_10", "R2_BATCH_005_ACTIVE_5_OF_10"),
    ],
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": [
        ("R2_BATCH_005_ACTIVE_4_OF_10", "R2_BATCH_005_ACTIVE_5_OF_10"),
    ],
    "[기획서]/00_프로젝트_허브/START_HERE.md": [
        ("R2_BATCH_005_ACTIVE_4_OF_10", "R2_BATCH_005_ACTIVE_5_OF_10"),
    ],
    "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": [
        ("R2_BATCH_005_4_OF_10", "R2_BATCH_005_5_OF_10"),
    ],
}
for path, replacements in hub_updates.items():
    text = read(path)
    for old, new in replacements:
        text = replace_required(text, old, new, count=1)
    write(path, text)
    append_once(
        path,
        "BS-ITEM-20260806-01",
        f'''## BS-ITEM-20260806-01 현재 정제\n\n- 활성 배치: `R2_BATCH_005_5_OF_10`\n- 장비군 고정 기본 중량: `0 / 5 / 10 / 15 / 20 / 30 WEIGHT_POINT`\n- 중량 전용 효과: `LIGHTWEIGHT -5 / NONE 0 / WEIGHTED +5`, 작품당 최대 하나\n- 자동 중량 변경 금지: 재료·제작 등급·예술성·원수치·일반 강화 단계\n- 정본: `{CANON_PATH}`\n- 제품 구현: `BLOCKED`''',
    )

# Upgrade current active-batch assertions in focused tests.
test_paths = [
    "tests/test_base_v942_planning_first_adoption.py",
    "tests/test_r2_artistry_generation_growth_economy.py",
    "tests/test_r2_customer_equipment_compatibility.py",
    "tests/test_r2_mobile_customer_card_progressive_disclosure.py",
    "tests/test_r2_enhancement_dominant_simple_load_gate.py",
]
for path in test_paths:
    text = read(path)
    text = text.replace("test_batch_005_contains_four_approved_decisions", "test_batch_005_contains_five_approved_decisions")
    text = text.replace("test_batch_005_is_active_at_four_of_ten", "test_batch_005_is_active_at_five_of_ten")
    text = text.replace("R2_BATCH_005_ACTIVE_4_OF_10", "R2_BATCH_005_ACTIVE_5_OF_10")
    text = text.replace('self.assertEqual("4/10", self.registry["next_approval_counter"])', 'self.assertEqual("5/10", self.registry["next_approval_counter"])')
    text = text.replace('self.assertEqual(4, active["approved_decisions"])', 'self.assertEqual(5, active["approved_decisions"])')
    text = text.replace('self.assertEqual("4/10", active["counter"])', 'self.assertEqual("5/10", active["counter"])')
    text = text.replace(
        '["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01", "BS-CUSTOMER-20260806-01"]',
        '["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01", "BS-CUSTOMER-20260806-01", "BS-ITEM-20260806-01"]',
    )
    text = text.replace(
        '                "BS-CUSTOMER-20260806-01",\n            ],',
        '                "BS-CUSTOMER-20260806-01",\n                "BS-ITEM-20260806-01",\n            ],',
    )
    if path.endswith("test_base_v942_planning_first_adoption.py"):
        text = text.replace('self.assertIn("R2_BATCH_005_4_OF_10", game_bible)', 'self.assertIn("R2_BATCH_005_5_OF_10", game_bible)')
        text = text.replace('self.assertIn("R2_BATCH_005_4_OF_10", active)', 'self.assertIn("R2_BATCH_005_5_OF_10", active)')
        text = text.replace('self.assertIn("R2_BATCH_005 / 4/10", root)', 'self.assertIn("R2_BATCH_005 / 5/10", root)')
    if path.endswith("test_r2_mobile_customer_card_progressive_disclosure.py"):
        text = text.replace('self.assertIn("R2_BATCH_005_4_OF_10", bible)', 'self.assertIn("R2_BATCH_005_5_OF_10", bible)')
        text = text.replace('self.assertIn("현재 승인 카운터: `4/10`", active)', 'self.assertIn("현재 승인 카운터: `5/10`", active)')
    write(path, text)

# Project core alignment validator.
core_path = "tests/check_project_core_alignment.py"
core = read(core_path)
for old, new in (
    ("R2_BATCH_005_ACTIVE_4_OF_10", "R2_BATCH_005_ACTIVE_5_OF_10"),
    ("R2_BATCH_005_4_OF_10", "R2_BATCH_005_5_OF_10"),
    ("R2_BATCH_005 / 4/10", "R2_BATCH_005 / 5/10"),
    ("현재 승인 카운터: `4/10`", "현재 승인 카운터: `5/10`"),
    ('"next_approval_counter": "4/10"', '"next_approval_counter": "5/10"'),
    ('active.get("counter") != "4/10"', 'active.get("counter") != "5/10"'),
    ("active batch must be R2_BATCH_005 at 4/10", "active batch must be R2_BATCH_005 at 5/10"),
    ('active.get("approved_decisions") != 4', 'active.get("approved_decisions") != 5'),
    ("active batch 005 must contain the four approved decisions", "active batch 005 must contain the five approved decisions"),
):
    core = core.replace(old, new)
core = core.replace(
    '["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01", "BS-CUSTOMER-20260806-01"]',
    '["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01", "BS-CUSTOMER-20260806-01", "BS-ITEM-20260806-01"]',
)
core = replace_required(
    core,
    '    "docs/planning/BLACKSMITH_R2_CHECKPOINT_004_POSTMERGE_CLOSURE_2026.md": (',
    '''    "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md": (
        "BS-ITEM-20260806-01",
        "R2_BATCH_005_5_OF_10",
        "장비군 고정 기본 중량",
        "LIGHTWEIGHT: -5",
        "WEIGHTED: +5",
        "제품 구현: `BLOCKED`",
    ),
    "docs/planning/BLACKSMITH_R2_CHECKPOINT_004_POSTMERGE_CLOSURE_2026.md": (''',
    count=1,
)
core = replace_required(
    core,
    '    alignment = registry.get("implementation_alignment", {})',
    '''    weight = decisions.get("BS-ITEM-20260806-01", {}).get("contract", {})
    if weight.get("base_weight_model") != "EQUIPMENT_GROUP_FIXED_BASE_WEIGHT":
        failures.append("equipment base-weight model is incorrect")
    if weight.get("base_weight_points") != {"ACCESSORY": 0, "TOOL": 5, "CLOTHING_OR_ROBE": 5, "LIGHT_ARMOR": 10, "MEDIUM_ARMOR": 20, "HEAVY_ARMOR": 30, "SWORD": 10, "AXE": 15, "BLUNT": 15, "POLEARM": 20, "RANGED": 10, "SHIELD_SUPPORT": 10}:
        failures.append("equipment base-weight table is incorrect")
    if weight.get("explicit_weight_modifiers") != {"LIGHTWEIGHT": -5, "NONE": 0, "WEIGHTED": 5}:
        failures.append("explicit weight modifiers are incorrect")
    if weight.get("maximum_active_weight_modifiers_per_item") != 1:
        failures.append("only one weight modifier may be active per item")
    if weight.get("product_implementation") != "BLOCKED":
        failures.append("equipment base-weight product implementation must remain blocked")

    alignment = registry.get("implementation_alignment", {})''',
    count=1,
)
write(core_path, core)

# Operating-system audit.
audit_path = "tools/audit_project_operating_system.py"
audit = read(audit_path)
audit = audit.replace(
    '    "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md",',
    '    "docs/planning/BLACKSMITH_R2_ENHANCEMENT_DOMINANT_SIMPLE_LOAD_GATE_CANON_2026.md",\n    "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md",',
    1,
)
for old, new in (
    ("R2_BATCH_005_ACTIVE_4_OF_10", "R2_BATCH_005_ACTIVE_5_OF_10"),
    ("R2_BATCH_005_4_OF_10", "R2_BATCH_005_5_OF_10"),
    ("R2_BATCH_005 / 4/10", "R2_BATCH_005 / 5/10"),
    ("현재 승인 카운터: `4/10`", "현재 승인 카운터: `5/10`"),
    ('"stage_status":"R2_BATCH_005_ACTIVE_4_OF_10"', '"stage_status":"R2_BATCH_005_ACTIVE_5_OF_10"'),
    ('"next_approval_counter":"4/10"', '"next_approval_counter":"5/10"'),
):
    audit = audit.replace(old, new)
audit = audit.replace(
    '        \'"id":"BS-CUSTOMER-20260806-01"\',',
    '        \'"id":"BS-CUSTOMER-20260806-01"\',\n        \'"id":"BS-ITEM-20260806-01"\',\n        \'"base_weight_model":"EQUIPMENT_GROUP_FIXED_BASE_WEIGHT"\',\n        \'"maximum_active_weight_modifiers_per_item":1\',',
    1,
)
audit = replace_required(
    audit,
    '    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": (',
    '''    "docs/planning/BLACKSMITH_R2_EQUIPMENT_BASE_WEIGHT_POINTS_CANON_2026.md": (
        "BS-ITEM-20260806-01",
        "R2_BATCH_005_5_OF_10",
        "장비군 고정 기본 중량",
        "LIGHTWEIGHT: -5",
        "WEIGHTED: +5",
        "제품 구현: `BLOCKED`",
    ),
    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": (''',
    count=1,
)
write(audit_path, audit)

# Mark plan progress through GREEN authority synchronization.
plan = read(PLAN_PATH)
plan = plan.replace("- [ ] Write tests for the active batch", "- [x] Write tests for the active batch")
plan = plan.replace("- [ ] Add the test module to Planning-first workflow", "- [x] Add the test module to Planning-first workflow")
plan = plan.replace("- [ ] Run Planning-first CI and verify failure", "- [x] Run Planning-first CI and verify failure")
plan = plan.replace("- [ ] Record the RED commit and run number.", "- [x] Record the RED commit `eca4f5d5ec203db9e83fbe7d47f4b5bb8e3b3fff` and Planning-first run `190`.")
for phrase in (
    "Add the new Decision and move the active batch",
    "Store all twelve equipment-group base values exactly.",
    "Store the modifier values, one-modifier limit, final minimum zero, and excluded automatic weight sources.",
    "Register canon, spec, and plan as active authority documents.",
    "Route total weight to base group weight plus one explicit modifier.",
    "State that general enhancement levels and unrelated item stats do not change weight.",
    "Add the player-facing `중량 N` and optional `경량화 -5` or `중량화 +5` reason-chip contract.",
    "Update active-batch validators to 5/10 while retaining prior historical evidence.",
    "Add the new canon to project and operating audits.",
):
    plan = plan.replace(f"- [ ] {phrase}", f"- [x] {phrase}")
write(PLAN_PATH, plan)

print("Equipment base weight points canon synchronization applied.")
