#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_ID = "BS-UX-20260805-01"
CANON_PATH = "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md"
SPEC_PATH = "docs/superpowers/specs/2026-08-05-mobile-customer-card-progressive-disclosure-design.md"
PLAN_PATH = "docs/superpowers/plans/2026-08-05-mobile-customer-card-progressive-disclosure.md"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def write(relative: str, content: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def replace_required(text: str, old: str, new: str, *, count: int | None = None) -> str:
    if old not in text:
        raise RuntimeError(f"required token missing: {old!r}")
    if count is None:
        return text.replace(old, new)
    return text.replace(old, new, count)


def append_once(relative: str, marker: str, block: str) -> None:
    text = read(relative)
    if marker not in text:
        write(relative, text.rstrip() + "\n\n" + block.strip() + "\n")


CANON = r'''# [현재 정본] Blacksmith 모바일 고객 카드 단계적 정보 공개 Canon

- Decision: `BS-UX-20260805-01`
- 승인 상태: `USER_APPROVED / R2_BATCH_005_3_OF_10 / APPROVED_PENDING_MERGE`
- 정제 대상: `BS-CUSTOMER-20260805-01 / BS-CUSTOMER-20260803-02 / BS-UX-20260804-01`
- 대상 플랫폼: 모바일 우선, 이후 PC 적응
- 제품 구현: `BLOCKED`

## 1. 목적

고객 카드의 목적은 고객을 별도의 RPG 캐릭터처럼 육성·분석하게 만드는 것이 아니다. 플레이어가 **어떤 작품을 누구에게 맡길지** 빠르게 판단하고, 그 이유를 이해한 뒤 작품의 세계 생애로 보내는 결정을 돕는 것이다.

```text
기본 카드 → 장비 선택 후 판단층 → 상세 보기
```

기본 화면은 판단에 필요한 핵심 정보만 유지하고, 장비 선택 시 결과와 원인을 즉시 갱신하며, 전체 근거는 한 단계 깊은 상세 보기에서 확인한다.

## 2. 채택 구조: 3단계 단계적 공개

### 2.1 기본 카드 — `DEFAULT_CUSTOMER_CARD`

항상 표시한다.

- 고객 이름·역할·초상 또는 식별 이미지
- 현재 일정 요약과 주요 요구
- 근력 / 기량 / 체력 / 판단력
- 현재 일정과 관련된 주 적성·보조 적성만
- 마법 장비 또는 마력 요구가 관련된 고객에게만 마력 적성
- 장비 선택·배정의 주 행동 버튼

기본 화면에 모든 무기군·갑옷군 적성을 행렬로 펼치지 않는다. 관련 없는 마력 적성과 적용되지 않는 수치도 빈칸 또는 0으로 채우지 않는다.

### 2.2 장비 선택 후 판단층 — `POST_EQUIPMENT_DECISION_LAYER`

작품을 선택하면 같은 카드 안에서 즉시 갱신한다.

- 균형 상태: 부적합 / 불안정 / 안정 / 능숙
- 예상 성공률 또는 승인된 범위·방향
- 핵심 원인 2~4개
- 관련될 때만 특수기능 위험 또는 활성 가능성
- 장비 변경 전후에 바뀐 핵심 판단 원인

핵심 원인은 단순한 종합 점수 대신 다음처럼 설명한다.

```text
+ 검류 전문
+ 총 중량이 적정 하중 이내
- 방패 적성 미숙
- 화염 방출에 필요한 마력 적성 부족
```

적합도 결과만 보여주고 이유를 숨기는 불투명한 종합 점수는 허용하지 않는다.

### 2.3 상세 보기 — `DETAIL_VIEW`

카드당 하나의 명확한 상세 진입점으로 연다.

- 해당 고객의 전체 관련 무기·갑옷 적성
- 총 중량과 적정 하중
- 특수기능 적합도 구성 요인
- 선택 작품에 실제 적용되는 능력치 세부
- 예상 성공률 산출에 사용된 공개 가능한 원인
- 고객·장비 정본의 읽기 전용 상세 정보

미래 사건의 미확정 결과나 스포일러는 공개하지 않는다.

## 3. 상호작용 계약

- 주 행동 버튼은 접힌 상태에서도 항상 보인다.
- 카드마다 상세 공개 진입점은 하나만 둔다.
- 핵심 정보는 길게 누르기나 숨은 제스처만으로 열리지 않는다.
- PC에서 호버·툴팁을 보조로 사용할 수 있으나 핵심 정보가 호버에만 존재해서는 안 된다.
- 장비 선택 시 카드 전체를 새 화면으로 강제 전환하지 않고 판단층을 제자리 갱신한다.
- 상세 보기에서 돌아오면 선택 작품과 스크롤 위치를 유지한다.

## 4. 모바일 접근성 계약

- 모든 상호작용 목표는 최소 `48dp` 터치 영역을 확보한다.
- 상태를 색상만으로 전달하지 않는다.
- 상태명 텍스트 또는 아이콘+텍스트를 함께 사용한다.
- 성공률·균형·위험 상태는 스크린리더가 의미 있는 순서로 읽을 수 있어야 한다.
- 글자 확대 시 핵심 행동 버튼과 판단 원인이 겹치거나 잘리지 않아야 한다.
- 장식 이미지는 의미 정보와 분리하고 접근성 트리에서 제외할 수 있다.

## 5. PC 적응

PC판도 같은 정보 계층을 유지한다.

```text
SAME_INFORMATION_HIERARCHY_POINTER_ENHANCEMENTS_OPTIONAL
```

넓은 화면에서는 기본 카드와 판단층을 나란히 배치할 수 있고, 포인터 호버·비교 툴팁을 추가할 수 있다. 그러나 모바일에서 탭으로 확인할 수 없는 핵심 정보를 PC 호버 전용으로 만들지 않는다.

## 6. 벤치마킹 판정

### 채택

- Apple Human Interface Guidelines의 단계적 공개: 자주 쓰는 핵심 정보를 상단·기본 상태에 두고 고급 상세는 필요할 때 공개
- Android 접근성 가이드의 최소 48dp 터치 목표
- 선택 행과 상세 화면을 분리하는 모바일 리스트·카드 패턴

### 수정 채택

일반 앱처럼 상세를 단순히 숨기는 데 그치지 않는다. 게임에서는 작품을 선택하는 순간 **균형·예상 성공률·핵심 원인 2~4개**가 즉시 나타나야 한다. 따라서 단계적 공개를 의사결정 피드백과 결합한다.

### 비채택

- 모든 능력치·적성을 기본 화면에 펼치는 전체 행렬
- 결과만 보여주는 불투명한 종합 적합도 점수
- 색상만으로 적합·위험을 구분
- 길게 누르기·스와이프·호버에만 핵심 정보 배치
- 세부 수치마다 별도 팝업을 중첩하는 구조

### 차별화

고객 카드의 중심은 캐릭터 전투력 비교가 아니라 **작품의 적임자와 세계 생애를 결정하는 설명 가능한 선택**이다. 고객 수치보다 작품 UID, 장비 조합, 사건 목적과의 관계를 먼저 보여준다.

## 7. 적대적 검토

### 위험: 기본 카드가 다시 과밀해질 수 있음

대응: 기본 카드에는 4능력치와 관련 적성만 허용하고, 전체 적성·중량 세부·특수기능 근거는 상세 보기로 이동한다.

### 위험: 결과 중심 카드가 자동 추천 버튼으로 전락할 수 있음

대응: 성공률과 함께 핵심 원인 2~4개를 의무 표시하고, 플레이어가 다른 작품을 비교할 수 있게 한다.

### 위험: 색상·아이콘이 세계관 연출에 묻힐 수 있음

대응: 상태명 텍스트를 필수로 두며 색상은 보조 신호로만 사용한다.

### 위험: PC판에서 별도 UX를 다시 설계해 정본이 갈라질 수 있음

대응: 정보 계층은 공통 계약으로 고정하고 배치·포인터 보조만 플랫폼별로 허용한다.

최종 판정: 기획 충돌 없음. 고객 RPG 전도, 정보 과밀, 불투명 자동 추천, 접근성 단독 신호를 차단하면 핵심 재미와 정합하다.

## 8. 구현·검증 경계

현재는 기획 정본만 승인한다.

- UI 씬·런타임 모델·데이터 구현: `NOT_STARTED_BLOCKED`
- 실제 모바일 기기 테스트: `NOT_RUN`
- 접근성 스캐너·스크린리더 테스트: `NOT_RUN`
- 카드 이미지·애니메이션 HX 제작: 전체 관련 기획 검토 완료 후
- 정확한 레이아웃 크기·폰트·간격: 시각 설계 및 프로토타입 단계
- 제품 구현: `BLOCKED`
'''

SPEC = r'''# Mobile Customer Card Progressive Disclosure Design

- Decision: `BS-UX-20260805-01`
- Status: `USER_APPROVED / R2_BATCH_005_3_OF_10 / APPROVED_PENDING_MERGE`
- Product implementation: `BLOCKED`

## Goal

Design a mobile-first customer card that makes equipment assignment explainable without turning the customer system into a dense character-RPG screen.

## Design boundary

The feature owns information hierarchy and interaction disclosure only. It does not change customer stats, proficiency values, success formulas, equipment raw stats, event resolution, or item UID ownership.

## Surface model

### Default customer card

Shows identity, role, current schedule summary, four base stats, only the relevant primary/secondary proficiencies, context-relevant magic aptitude, and the persistent primary assignment action.

### Post-equipment decision layer

Appears in place after an item selection. Shows balance state, success forecast, two to four reason chips, and special-function risk only when applicable. Comparison feedback highlights the reasons that changed.

### Detail view

Opened through one explicit detail entry per card. Shows all relevant proficiencies, total weight and comfortable load, special-function fit factors, applicable item-stat breakdown, and disclosure-safe success inputs.

## Interaction rules

- Preserve selected item and scroll position when entering or leaving detail.
- Never require long press, swipe, or hover to access critical information.
- Keep the primary assignment action visible in collapsed and expanded states.
- Use in-place updates for item comparison rather than mandatory full-screen transitions.

## Accessibility

- Minimum interactive target: 48dp.
- Color is never the only state signal.
- State text or icon-plus-text is required.
- Reading order is identity → requirement → stats/proficiency → selected item result → reasons → action.
- Text scaling must not cover the primary action or reason chips.

## PC adaptation

Keep the same information hierarchy. Wider layouts and pointer tooltips are optional enhancements, but no critical information may be hover-only.

## Failure and empty states

- No item selected: show the requirement summary and a clear selection prompt; do not show a fake zero fit score.
- Non-applicable magic: omit the field rather than displaying zero.
- Unknown event modifier: label the forecast as uncertain and show known reasons only.
- Incompatible item: show `부적합` plus explicit reasons; do not silently disable comparison.

## Test contract

The planning contract must verify the three layers, required fields, 2–4 reason chips, one detail entry, 48dp target, non-color-only communication, no long-press/hover-only critical information, PC hierarchy parity, and blocked product implementation.
'''

PLAN = r'''# Mobile Customer Card Progressive Disclosure Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize the approved three-layer mobile customer card information hierarchy into Blacksmith canon without implementing product UI.

**Architecture:** Store the user-approved UX contract as a focused Decision and canon document, then route it through the current R2 Registry, Game Bible, project hub, validators, PR evidence, and Google Sheet. The mobile and future PC surfaces share one information hierarchy; platform-specific layout remains a later visual/implementation concern.

**Tech Stack:** Markdown canon and design documents, JSON registries, Python unittest contracts, GitHub Actions, Google Sheets authority mirror.

## Global Constraints

- Decision ID: `BS-UX-20260805-01`.
- Active batch: `R2_BATCH_005_3_OF_10`.
- Product implementation remains `BLOCKED`.
- Use RED → GREEN → REFACTOR evidence.
- Preserve historical 1/10 and 2/10 Decision markers; only active authority becomes 3/10.
- Do not change runtime, scenes, game data, images, or animation HX.

---

### Task 1: RED planning contract

**Files:**
- Create: `tests/test_r2_mobile_customer_card_progressive_disclosure.py`
- Modify: `.github/workflows/validate-base-v942-planning-first-adoption.yml`

**Interfaces:**
- Consumes: current R2 Registry and current authority documents.
- Produces: a failing contract requiring Decision `BS-UX-20260805-01` and batch 3/10.

- [x] Write the failing contract for the three layers, accessibility rules, and authority documents.
- [x] Add the test to Planning-first CI.
- [x] Run Planning-first and observe failure while the Decision is absent.
- [x] Record RED commit `e5d531417da28a12c687bfefb5cda0f624d69f40` and run `161`.

### Task 2: GREEN focused canon and registry

**Files:**
- Create: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`
- Create: `docs/superpowers/specs/2026-08-05-mobile-customer-card-progressive-disclosure-design.md`
- Create: `docs/superpowers/plans/2026-08-05-mobile-customer-card-progressive-disclosure.md`
- Modify: `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
- Modify: `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`

**Interfaces:**
- Consumes: customer capability/equipment compatibility and success-disclosure Decisions.
- Produces: canonical three-layer UX contract and machine-readable Decision fields.

- [x] Add Decision `BS-UX-20260805-01` with `THREE_LAYER_PROGRESSIVE_DISCLOSURE`.
- [x] Move active batch from 2/10 to 3/10 without rewriting historical Decision counters.
- [x] Record default, post-equipment, detail, accessibility, and PC-adaptation contracts.
- [x] Register the canon, design, and plan documents.

### Task 3: Authority and validator synchronization

**Files:**
- Modify: `CURRENT_CONFIRMED_DECISIONS.md`
- Modify: `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
- Modify: `docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md`
- Modify: `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
- Modify: `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Modify: `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
- Modify: `[기획서]/00_프로젝트_허브/START_HERE.md`
- Modify: `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- Modify: `tests/test_base_v942_planning_first_adoption.py`
- Modify: `tests/test_r2_artistry_generation_growth_economy.py`
- Modify: `tests/test_r2_customer_equipment_compatibility.py`
- Modify: `tests/check_project_core_alignment.py`
- Modify: `tools/audit_project_operating_system.py`

**Interfaces:**
- Consumes: focused canon and registry Decision.
- Produces: consistent active authority and no stale active 2/10 assertions.

- [x] Add current Decision summaries and core-fun protection.
- [x] Update active batch assertions to 3/10.
- [x] Keep `BS-CRAFT-20260805-02` at historical 1/10 and `BS-CUSTOMER-20260805-01` at historical 2/10.
- [x] Add focused canon assertions to project and operating audits.

### Task 4: Verification, PR, and Sheet evidence

**Files:**
- Modify after verification: PR #109 body and Google Sheet authority rows.

**Interfaces:**
- Consumes: final exact branch head and observed CI results.
- Produces: read-back evidence for the same Decision ID and commit.

- [ ] Run Planning-first, Base adoption, Python full contracts, operating audit, and Godot 4.7.1 headless.
- [ ] Confirm protected product path changes remain zero.
- [ ] Confirm PR comments and unresolved review threads remain zero.
- [ ] Write Decision `BS-UX-20260805-01`, batch 3/10, exact head, and CI results to Sheet.
- [ ] Read back all Sheet ranges.
- [ ] Update PR #109 while keeping Draft and unmerged.
'''


def update_registry() -> None:
    path = ROOT / "docs/planning/CURRENT_R2_CANON_REGISTRY.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["stage_status"] = "R2_BATCH_005_ACTIVE_3_OF_10"
    data["next_approval_counter"] = "3/10"
    decisions = data["current_decisions"]
    if not any(item.get("id") == DECISION_ID for item in decisions):
        insert_at = next(i + 1 for i, item in enumerate(decisions) if item.get("id") == "BS-CUSTOMER-20260805-01")
        decisions.insert(insert_at, {
            "id": DECISION_ID,
            "title": "모바일 고객 카드 3단계 정보 공개와 설명 가능한 장비 판단",
            "status": "USER_APPROVED_R2_BATCH_005_3_OF_10_APPROVED_PENDING_MERGE",
            "refines": ["BS-CUSTOMER-20260805-01", "BS-CUSTOMER-20260803-02", "BS-UX-20260804-01"],
            "canon": CANON_PATH,
            "spec": SPEC_PATH,
            "plan": PLAN_PATH,
            "contract": {
                "surface": "CUSTOMER_EQUIPMENT_CARD",
                "disclosure_model": "THREE_LAYER_PROGRESSIVE_DISCLOSURE",
                "layers": ["DEFAULT_CUSTOMER_CARD", "POST_EQUIPMENT_DECISION_LAYER", "DETAIL_VIEW"],
                "default_layer": [
                    "CUSTOMER_IDENTITY_AND_ROLE",
                    "CURRENT_SCHEDULE_SUMMARY",
                    "FOUR_BASE_STATS",
                    "RELEVANT_PRIMARY_AND_SECONDARY_PROFICIENCIES_ONLY",
                    "MAGIC_APTITUDE_ONLY_WHEN_RELEVANT"
                ],
                "post_equipment_layer": [
                    "BALANCE_STATE",
                    "SUCCESS_FORECAST",
                    "KEY_REASON_CHIPS",
                    "SPECIAL_FUNCTION_RISK_WHEN_RELEVANT"
                ],
                "reason_chip_minimum": 2,
                "reason_chip_maximum": 4,
                "detail_layer": [
                    "ALL_RELEVANT_PROFICIENCIES",
                    "TOTAL_WEIGHT_AND_COMFORTABLE_LOAD",
                    "SPECIAL_FUNCTION_FIT_FACTORS",
                    "APPLICABLE_ITEM_STAT_BREAKDOWN"
                ],
                "detail_entry_model": "ONE_DETAIL_DISCLOSURE_ENTRY_PER_CARD",
                "primary_assignment_action_always_visible": True,
                "full_proficiency_matrix_visible_by_default": False,
                "result_only_opaque_fit_score_allowed": False,
                "minimum_touch_target_dp": 48,
                "color_only_state_communication_allowed": False,
                "long_press_only_critical_information_allowed": False,
                "hover_only_critical_information_allowed": False,
                "text_label_or_icon_plus_text_required_for_states": True,
                "pc_adaptation": "SAME_INFORMATION_HIERARCHY_POINTER_ENHANCEMENTS_OPTIONAL",
                "product_implementation": "BLOCKED"
            }
        })
    active = data["active_batch"]
    active["approved_decisions"] = 3
    active["counter"] = "3/10"
    active["decisions"] = ["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", DECISION_ID]
    active["status"] = "ACTIVE_DRAFT_PR109_APPROVED_PENDING_MERGE"
    alignment = data.setdefault("implementation_alignment", {})
    alignment["current_mobile_customer_card_model"] = "THREE_LAYER_PROGRESSIVE_DISCLOSURE_DECISION_FIRST"
    alignment["mobile_customer_card_product_implementation"] = "NOT_STARTED_BLOCKED"
    tdd = data.setdefault("tdd_evidence", {})
    tdd["mobile_customer_card_red"] = {
        "commit": "e5d531417da28a12c687bfefb5cda0f624d69f40",
        "planning_first_run": 161,
        "status": "EXPECTED_FAILURE"
    }
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def update_design_registry() -> None:
    relative = "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json"
    path = ROOT / relative
    data = json.loads(path.read_text(encoding="utf-8"))
    data["current_batch"] = "R2_BATCH_005_3_OF_10"
    data["current_design_decision"] = DECISION_ID
    docs = data["documents"]
    additions = [
        {
            "document_id": "mobile-customer-card-progressive-disclosure-canon",
            "source_path": "../../" + CANON_PATH,
            "status": "ACTIVE",
            "source_role": "current_mobile_customer_card_information_hierarchy_contract"
        },
        {
            "document_id": "mobile-customer-card-progressive-disclosure-design",
            "source_path": "../../" + SPEC_PATH,
            "status": "ACTIVE",
            "source_role": "approved_design_input_for_bs_ux_20260805_01"
        },
        {
            "document_id": "mobile-customer-card-progressive-disclosure-plan",
            "source_path": "../../" + PLAN_PATH,
            "status": "ACTIVE",
            "source_role": "executed_canon_plan_for_bs_ux_20260805_01"
        }
    ]
    known = {item["document_id"] for item in docs}
    insert_at = next(i + 1 for i, item in enumerate(docs) if item["document_id"] == "customer-equipment-compatibility-plan")
    for item in reversed([item for item in additions if item["document_id"] not in known]):
        docs.insert(insert_at, item)
    guards = data["routing_guards"]
    replacement = "R2_BATCH_005_IS_ACTIVE_AT_3_OF_10_WITH_BS_CRAFT_20260805_02_BS_CUSTOMER_20260805_01_AND_BS_UX_20260805_01"
    guards[:] = [replacement if value.startswith("R2_BATCH_005_IS_ACTIVE_AT_2_OF_10") else value for value in guards]
    for value in (
        "MOBILE_CUSTOMER_CARD_USES_THREE_LAYER_PROGRESSIVE_DISCLOSURE",
        "CRITICAL_CUSTOMER_CARD_INFORMATION_MUST_NOT_BE_COLOR_LONG_PRESS_OR_HOVER_ONLY",
        "MOBILE_CUSTOMER_CARD_PRODUCT_IMPLEMENTATION_REMAINS_BLOCKED",
    ):
        if value not in guards:
            guards.insert(7, value)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_authority_docs() -> None:
    root = read("CURRENT_CONFIRMED_DECISIONS.md")
    root = replace_required(root, "현재 승인 배치: `R2_BATCH_005 / 2/10`", "현재 승인 배치: `R2_BATCH_005 / 3/10`", count=1)
    customer_line = "- `BS-CUSTOMER-20260805-01`: 근력·기량·체력·판단력, 희소 무기·갑옷 적성, 마력 적성, 장비 적합성 — `R2_BATCH_005_2_OF_10 / APPROVED_PENDING_MERGE`"
    ux_line = "- `BS-UX-20260805-01`: 모바일 고객 카드 3단계 정보 공개와 설명 가능한 장비 판단 — `R2_BATCH_005_3_OF_10 / APPROVED_PENDING_MERGE`"
    if ux_line not in root:
        root = replace_required(root, customer_line, customer_line + "\n" + ux_line, count=1)
    write("CURRENT_CONFIRMED_DECISIONS.md", root)
    append_once("CURRENT_CONFIRMED_DECISIONS.md", "<!-- BS-UX-20260805-01 -->", r'''<!-- BS-UX-20260805-01 -->
## 모바일 고객 카드 정보 계층

```text
기본 카드 → 장비 선택 후 판단층 → 상세 보기
```

- 기본: 고객 역할·일정, 4능력치, 관련 주·보조 적성, 관련 시 마력 적성
- 장비 선택 후: 균형·예상 성공률·핵심 원인 2~4개·관련 특수기능 위험
- 상세: 전체 관련 적성, 총 중량·적정 하중, 특수기능 근거, 적용 능력치
- 전체 적성 행렬 기본 노출 금지
- 불투명한 결과 전용 적합도 점수 금지
- 색상·길게 누르기·호버 단독 핵심 정보 금지
- 최소 `48dp` 터치 목표
- 제품 구현: `BLOCKED`''')

    bible = read("docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md")
    bible = replace_required(bible, "CURRENT_CANON / R2_BATCH_005_2_OF_10", "CURRENT_CANON / R2_BATCH_005_3_OF_10", count=1)
    current_line = "BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / BS-CRAFT-20260805-02 / BS-CUSTOMER-20260805-01 / BS-OPS-20260805-01"
    if DECISION_ID not in bible.splitlines()[3]:
        bible = replace_required(bible, current_line, "BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / BS-CRAFT-20260805-02 / BS-CUSTOMER-20260805-01 / BS-UX-20260805-01 / BS-OPS-20260805-01", count=1)
    write("docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md", bible)
    append_once("docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md", "<!-- BS-UX-20260805-01 -->", r'''<!-- BS-UX-20260805-01 -->
## 모바일 고객 카드와 장비 판단

```text
기본 카드 → 장비 선택 후 판단층 → 상세 보기
```

고객 카드의 목적은 고객 RPG 육성이 아니라 작품을 누구에게 맡길지 설명 가능한 판단을 제공하는 것이다. 기본 카드에는 4능력치와 관련 적성만 표시한다. 작품 선택 후 균형·예상 성공률·핵심 원인 2~4개를 즉시 보여주며, 전체 관련 적성·총 중량·적정 하중·특수기능 근거는 상세 보기로 보낸다. 핵심 상태는 색상만으로 전달하지 않으며 모바일 상호작용 목표는 최소 `48dp`다. 제품 구현: `BLOCKED`.''')

    for relative, replacements in {
        "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": [
            ("R2_BATCH_005_2_OF_10", "R2_BATCH_005_3_OF_10"),
            ("현재 승인 카운터: `2/10`", "현재 승인 카운터: `3/10`"),
        ],
        "[기획서]/00_프로젝트_허브/ROADMAP.md": [("R2_BATCH_005_ACTIVE_2_OF_10", "R2_BATCH_005_ACTIVE_3_OF_10")],
        "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": [("R2_BATCH_005_ACTIVE_2_OF_10", "R2_BATCH_005_ACTIVE_3_OF_10")],
        "[기획서]/00_프로젝트_허브/START_HERE.md": [("R2_BATCH_005_ACTIVE_2_OF_10", "R2_BATCH_005_ACTIVE_3_OF_10")],
        "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md": [("R2_BATCH_005_2_OF_10", "R2_BATCH_005_3_OF_10")],
    }.items():
        text = read(relative)
        for old, new in replacements:
            text = replace_required(text, old, new, count=1)
        write(relative, text)

    append_once("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", "<!-- BS-UX-20260805-01 -->", r'''<!-- BS-UX-20260805-01 -->
## 현재 UX 승인

- Decision: `BS-UX-20260805-01`
- 기본 카드 → 장비 선택 후 판단층 → 상세 보기
- 장비 선택 후 균형·성공률·핵심 원인 2~4개 표시
- 전체 적성 행렬 기본 노출 금지
- 모바일 최소 `48dp`, 색상·길게 누르기·호버 단독 핵심 정보 금지
- 제품 구현: `BLOCKED`''')
    append_once("[기획서]/00_프로젝트_허브/ROADMAP.md", "<!-- BS-UX-20260805-01 -->", r'''<!-- BS-UX-20260805-01 -->
### Mobile Customer Card Information Hierarchy Gate

`BS-UX-20260805-01` 승인. 3단계 정보 계층 정본은 완료했으나 시각 레이아웃·이미지·HX·제품 구현은 전체 관련 기획 검토 전까지 `BLOCKED`.''')
    append_once("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md", "<!-- BS-UX-20260805-01 -->", r'''<!-- BS-UX-20260805-01 -->
### Mobile Customer Card Progressive Disclosure Gate

- Decision: `BS-UX-20260805-01`
- 3단계 정보 계층: APPROVED
- 설명 가능한 이유 2~4개: REQUIRED
- 접근성 48dp·비색상 단독 신호: REQUIRED
- 이미지·애니메이션 HX: BLOCKED_UNTIL_REVIEW_COMPLETE
- CODEX_IMPLEMENTATION_GATE: BLOCKED''')
    append_once("[기획서]/00_프로젝트_허브/START_HERE.md", "<!-- BS-UX-20260805-01 -->", r'''<!-- BS-UX-20260805-01 -->
현재 UX Decision은 `BS-UX-20260805-01`: 모바일 고객 카드의 기본→장비 판단→상세 3단계 정보 공개. 제품 구현은 계속 `BLOCKED`.''')
    append_once("[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md", "<!-- BS-UX-20260805-01 -->", r'''<!-- BS-UX-20260805-01 -->
- 모바일 고객 카드 단계적 공개 정본: `docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`
- 승인 설계: `docs/superpowers/specs/2026-08-05-mobile-customer-card-progressive-disclosure-design.md`
- 정본 동기화 계획: `docs/superpowers/plans/2026-08-05-mobile-customer-card-progressive-disclosure.md`''')
    append_once("docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md", "<!-- REFINED_BY_BS-UX-20260805-01 -->", r'''<!-- REFINED_BY_BS-UX-20260805-01 -->
## 표시 구조 후속 정제

고객 능력·적성·장비 적합성 데이터 계약은 유지한다. 모바일 기본 공개 범위와 상세 진입 방식은 `BS-UX-20260805-01` 및 `BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md`가 정제한다.''')


def update_tests_and_audits() -> None:
    common_files = [
        "tests/test_r2_artistry_generation_growth_economy.py",
        "tests/test_r2_customer_equipment_compatibility.py",
        "tests/test_base_v942_planning_first_adoption.py",
    ]
    old_list = '["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01"]'
    new_list = '["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01"]'
    for relative in common_files:
        text = read(relative)
        text = text.replace("test_batch_005_contains_two_approved_decisions", "test_batch_005_contains_three_approved_decisions")
        text = text.replace("test_batch_005_is_active_at_two_of_ten", "test_batch_005_is_active_at_three_of_ten")
        text = text.replace('"R2_BATCH_005_ACTIVE_2_OF_10"', '"R2_BATCH_005_ACTIVE_3_OF_10"')
        text = text.replace('"2/10", self.registry["next_approval_counter"]', '"3/10", self.registry["next_approval_counter"]')
        text = text.replace('self.assertEqual(2, active["approved_decisions"])', 'self.assertEqual(3, active["approved_decisions"])')
        text = text.replace('self.assertEqual("2/10", active["counter"])', 'self.assertEqual("3/10", active["counter"])')
        text = text.replace(old_list, new_list)
        text = text.replace('self.assertIn("R2_BATCH_005_2_OF_10", game_bible)', 'self.assertIn("R2_BATCH_005_3_OF_10", game_bible)')
        text = text.replace('self.assertIn("R2_BATCH_005_2_OF_10", active)', 'self.assertIn("R2_BATCH_005_3_OF_10", active)')
        text = text.replace('self.assertIn("R2_BATCH_005 / 2/10", root)', 'self.assertIn("R2_BATCH_005 / 3/10", root)')
        write(relative, text)

    core = read("tests/check_project_core_alignment.py")
    targeted = {
        '"R2_BATCH_005 / 2/10",': '"R2_BATCH_005 / 3/10",',
        '"R2_BATCH_005_2_OF_10",\n        "BS-CRAFT-20260805-02",': '"R2_BATCH_005_3_OF_10",\n        "BS-CRAFT-20260805-02",',
        '"R2_BATCH_005_2_OF_10",\n        "현재 승인 카운터: `2/10`",': '"R2_BATCH_005_3_OF_10",\n        "현재 승인 카운터: `3/10`",',
        '"R2_BATCH_005_ACTIVE_2_OF_10",\n        "BS-CRAFT-20260805-02",': '"R2_BATCH_005_ACTIVE_3_OF_10",\n        "BS-CRAFT-20260805-02",',
        '"stage_status": "R2_BATCH_005_ACTIVE_2_OF_10",': '"stage_status": "R2_BATCH_005_ACTIVE_3_OF_10",',
        '"next_approval_counter": "2/10",': '"next_approval_counter": "3/10",',
        'active.get("counter") != "2/10"': 'active.get("counter") != "3/10"',
        'active batch must be R2_BATCH_005 at 2/10': 'active batch must be R2_BATCH_005 at 3/10',
        'active.get("approved_decisions") != 2 or active.get("decisions") != ["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01"]': 'active.get("approved_decisions") != 3 or active.get("decisions") != ["BS-CRAFT-20260805-02", "BS-CUSTOMER-20260805-01", "BS-UX-20260805-01"]',
        'active batch 005 must contain the two approved decisions': 'active batch 005 must contain the three approved decisions',
    }
    for old, new in targeted.items():
        core = replace_required(core, old, new, count=1)
    canon_required = '''    "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md": (\n        "BS-UX-20260805-01",\n        "R2_BATCH_005_3_OF_10",\n        "기본 카드 → 장비 선택 후 판단층 → 상세 보기",\n        "핵심 원인 2~4개",\n        "48dp",\n        "제품 구현: `BLOCKED`",\n    ),\n'''
    anchor = '    "docs/planning/BLACKSMITH_R2_CHECKPOINT_004_POSTMERGE_CLOSURE_2026.md": ('
    if "BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md" not in core:
        core = replace_required(core, anchor, canon_required + anchor, count=1)
    decision_check = '''\n    ux = decisions.get("BS-UX-20260805-01", {}).get("contract", {})\n    if ux.get("disclosure_model") != "THREE_LAYER_PROGRESSIVE_DISCLOSURE":\n        failures.append("mobile customer card disclosure model is missing")\n    if ux.get("reason_chip_minimum") != 2 or ux.get("reason_chip_maximum") != 4:\n        failures.append("mobile customer card reason chip bounds are incorrect")\n    if ux.get("minimum_touch_target_dp") != 48:\n        failures.append("mobile customer card minimum touch target must be 48dp")\n    if ux.get("color_only_state_communication_allowed") is not False:\n        failures.append("mobile customer card must not use color-only state communication")\n    if ux.get("product_implementation") != "BLOCKED":\n        failures.append("mobile customer card product implementation must remain blocked")\n'''
    insert_anchor = '    alignment = registry.get("implementation_alignment", {})'
    if 'mobile customer card disclosure model is missing' not in core:
        core = replace_required(core, insert_anchor, decision_check + "\n" + insert_anchor, count=1)
    write("tests/check_project_core_alignment.py", core)

    audit = read("tools/audit_project_operating_system.py")
    if CANON_PATH not in audit:
        audit = replace_required(
            audit,
            '    "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md",\n',
            '    "docs/planning/BLACKSMITH_R2_CUSTOMER_CAPABILITY_AND_EQUIPMENT_COMPATIBILITY_CANON_2026.md",\n    "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md",\n',
            count=1,
        )
    replacements = {
        '"R2_BATCH_005 / 2/10",': '"R2_BATCH_005 / 3/10",',
        '\'"stage_status":"R2_BATCH_005_ACTIVE_2_OF_10"\',': '\'"stage_status":"R2_BATCH_005_ACTIVE_3_OF_10"\',',
        '\'"next_approval_counter":"2/10"\',': '\'"next_approval_counter":"3/10"\',',
        '"R2_BATCH_005_2_OF_10",\n        "BS-CRAFT-20260805-02",': '"R2_BATCH_005_3_OF_10",\n        "BS-CRAFT-20260805-02",',
        '"R2_BATCH_005_ACTIVE_2_OF_10",\n        "BS-CRAFT-20260805-02",': '"R2_BATCH_005_ACTIVE_3_OF_10",\n        "BS-CRAFT-20260805-02",',
        '"R2_BATCH_005_2_OF_10",\n        "현재 승인 카운터: `2/10`",': '"R2_BATCH_005_3_OF_10",\n        "현재 승인 카운터: `3/10`",',
    }
    for old, new in replacements.items():
        audit = replace_required(audit, old, new, count=1)
    audit_block = '''    "docs/planning/BLACKSMITH_R2_MOBILE_CUSTOMER_CARD_PROGRESSIVE_DISCLOSURE_CANON_2026.md": (\n        "BS-UX-20260805-01",\n        "R2_BATCH_005_3_OF_10",\n        "기본 카드 → 장비 선택 후 판단층 → 상세 보기",\n        "핵심 원인 2~4개",\n        "48dp",\n        "제품 구현: `BLOCKED`",\n    ),\n'''
    audit_anchor = '    "docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md": ('
    if audit_block.strip() not in audit:
        audit = replace_required(audit, audit_anchor, audit_block + audit_anchor, count=1)
    write("tools/audit_project_operating_system.py", audit)


def main() -> None:
    write(CANON_PATH, CANON)
    write(SPEC_PATH, SPEC)
    write(PLAN_PATH, PLAN)
    update_registry()
    update_design_registry()
    update_authority_docs()
    update_tests_and_audits()
    print("Mobile customer card canon synchronization applied.")


if __name__ == "__main__":
    main()
