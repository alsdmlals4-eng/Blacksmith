from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = "BS-CONTENT-20260811-07"
CANON = "docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md"
BASE_MAIN = "23d5b292f619022cdd8ab7a33fb1debc2d294861"
PROJECT_MAIN_AT_START = "27365bc774508bea6a1a19221fb2a3dc2d093be5"
RESUME = "SOLDIER_02_LIANA_MISSION_FIT_APPROVED"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, got {count}: {old!r}")
    return text.replace(old, new, 1)


def update_registry() -> None:
    path = "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
    data = json.loads(read(path))
    if data.get("next_approval_counter") != "6/10":
        raise RuntimeError(f"registry counter drift: {data.get('next_approval_counter')!r}")
    data["next_approval_counter"] = "7/10"
    ids = [item.get("id") for item in data.get("current_decisions", [])]
    if DECISION in ids:
        raise RuntimeError("Decision07 already exists before materialization")
    data["current_decisions"].append(
        {
            "id": DECISION,
            "title": "군인 02 리아나 베르크 전선 지휘관 임무 적합·보호 책임 콘텐츠",
            "status": "USER_APPROVED_R3_R7_7_OF_10",
            "canon": CANON,
            "refines": ["BS-CONTENT-20260804-01", "BS-CONTENT-20260804-02"],
            "depends_on": [
                "BS-CUSTOMER-20260803-02",
                "BS-CUSTOMER-20260805-01",
                "BS-CUSTOMER-20260806-01",
                "BS-ITEM-20260806-04",
                "BS-ITEM-20260806-05",
                "BS-UX-20260805-01",
                "BS-CONTENT-20260811-03",
                "BS-CONTENT-20260811-06",
            ],
            "contract": {
                "content_id": "SOLDIER_02",
                "customer_id": "LIANA_BERG",
                "customer_archetype": "SOLDIER",
                "activity_family": "FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY",
                "content_goal": "MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY",
                "player_role": "BLACKSMITH_COMMANDER_EQUIPMENT_DECISION_MAKER_NOT_TACTICAL_OR_UNIT_CONTROLLER",
                "existing_liana_berg_customer_reused": True,
                "same_item_uid_preserved": True,
                "direct_tactical_combat": False,
                "unit_movement_or_formation_control": False,
                "realtime_logistics_control": False,
                "soldier_casualty_micromanagement": False,
                "opaque_command_hero_leadership_or_mission_fit_score": False,
                "highest_defense_always_best": False,
                "highest_enhancement_always_best": False,
                "item_as_sole_cause_of_mission_result": False,
                "baseline_permadeath_for_liana": False,
                "death_farming_or_recruit_replacement_loop": False,
                "mission_count_artistry_growth": False,
                "automatic_chronicle_affix_from_win_or_survival": False,
                "mission_farming_multiplier": False,
                "result_axes": [
                    "MISSION_DUTY_STATE",
                    "COMMANDER_RETURN_STATE",
                    "ITEM_UID_FIELD_LEGACY_STATE",
                ],
                "immediate_feedback": "THREE_STATE_SUMMARY_WITH_2_TO_4_CAUSAL_REASONS_AND_ONE_PRIMARY_NEXT_ACTION",
                "exact_values": "NON_CANONICAL_BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
                "product_implementation": "BLOCKED",
                "task3_implementation": "NOT_APPROVED",
                "human_playtest": "NOT_RUN",
            },
        }
    )
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def update_current() -> None:
    path = "CURRENT_CONFIRMED_DECISIONS.md"
    text = read(path)
    text = replace_once(
        text,
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-06 / R3_R7_6_OF_10 / PLANNING_ONLY**",
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / R3_R7_7_OF_10 / PLANNING_ONLY**",
        "current header",
    )
    text = replace_once(text, "R3_R7_APPROVAL_COUNTER: 6/10", "R3_R7_APPROVAL_COUNTER: 7/10", "current counter")
    text = replace_once(
        text,
        "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-06",
        "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07",
        "current decision",
    )
    if "- `BS-CONTENT-20260811-07`:" not in text:
        lines = text.splitlines()
        idx = next(i for i, line in enumerate(lines) if line.startswith("- `BS-CONTENT-20260811-06`:"))
        lines.insert(
            idx + 1,
            "- `BS-CONTENT-20260811-07`: `SOLDIER_02` 리아나 베르크 전선 지휘관 임무 적합·보호 책임 콘텐츠. 공개된 임무·위험·장비 역할을 읽고 실제 작품 UID 한 점을 선택·인계하며 직접 전술전투 없이 결과를 `MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE`로 분리한다. Marek의 소량 표준화와 Cassia의 arena contribution 책임을 보존하고, 새 command/hero/leadership/mission-fit 총점·최고 방어/강화 자동정답·작품 단독 인과·baseline permadeath·임무 반복 Artistry/Chronicle 파밍을 만들지 않으며 같은 UID를 보존한다. — `USER_APPROVED / R3_R7_7_OF_10 / PLANNING_ONLY`",
        )
        text = "\n".join(lines) + "\n"
    write(path, text)


def update_active() -> None:
    path = "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
    text = read(path)
    text = replace_once(
        text,
        "> **R3_R7_DESIGN_ACTIVE / NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED / PLANNING_ONLY**",
        f"> **R3_R7_DESIGN_ACTIVE / {RESUME} / PLANNING_ONLY**",
        "active header",
    )
    text = replace_once(
        text,
        "- Blacksmith current main observed at Decision 06 start: `42469f6e2058efea464755ac44bec8bcd1154f0b`",
        f"- Blacksmith current main observed at Decision 07 start: `{PROJECT_MAIN_AT_START}`",
        "active project observation",
    )
    text = replace_once(
        text,
        "- `BASE_CURRENT_MAIN_OBSERVED`: `7ce96181d0a97930300fcc6d383dacc75ad08f6a`",
        f"- `BASE_CURRENT_MAIN_OBSERVED`: `{BASE_MAIN}`",
        "active base observation",
    )
    text = replace_once(text, "- 현재 R3–R7 승인 카운터: `6/10`", "- 현재 R3–R7 승인 카운터: `7/10`", "active counter prose")
    text = replace_once(text, "R3_R7_APPROVAL_COUNTER: 6/10", "R3_R7_APPROVAL_COUNTER: 7/10", "active yaml counter")
    text = replace_once(text, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-06", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07", "active yaml decision")
    text = replace_once(text, "R3_R7_RESUME_LOCATOR: NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED", f"R3_R7_RESUME_LOCATOR: {RESUME}", "active locator")
    start = text.index("## 현재 R3–R7 기획 재개 상태")
    owner = text.index("책임 원본:", start)
    section = """## 현재 R3–R7 기획 재개 상태

`BS-CONTENT-20260811-01` Nadia, `BS-CONTENT-20260811-02` Toren, `BS-CONTENT-20260811-03` Marek, `BS-CONTENT-20260811-04` Ersa, `BS-CONTENT-20260811-05` Cassia, `BS-CONTENT-20260811-06` Noble01은 승인 완료 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-07`다.

```text
SOLDIER_02 / LIANA_BERG
→ 기존 군인 추가 고객·전선 지휘관을 두 번째 Soldier 상세 콘텐츠로 승격
→ FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY
→ 임무 책임·위험·필요 장비 역할 공개
→ 실제 작품 UID 후보 비교
→ 한 작품 UID 선택·같은 UID 인계
→ 전선 임무는 비직접 세계 사건
→ MISSION_DUTY_STATE
 + COMMANDER_RETURN_STATE
 + ITEM_UID_FIELD_LEGACY_STATE
→ 수리·복원·후속 강화·신작·보존·재배정 판단 이유
```

- Marek/Soldier01의 `SMALL_LOT_STANDARD_ORDER` multi-UID 표준화 책임을 보존한다.
- Cassia/Gladiator01의 arena contribution/public legacy 책임을 보존한다.
- 직접 전술전투·부대 이동/대형·실시간 병참·사상자 micromanagement를 추가하지 않는다.
- command/hero/leadership/mission-fit 총점을 만들지 않는다.
- 최고 방어·최고 강화가 자동 정답이 아니며 작품 하나가 임무 결과의 유일 원인이 아니다.
- baseline Liana permadeath와 replacement loop를 추가하지 않는다.
- 임무/승리/생환 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 같은 작품 UID를 인계·현장 결과·귀환/회수까지 보존한다.

"""
    text = text[:start] + section + text[owner:]
    anchor = "- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`\n"
    if f"- `{CANON}`" not in text:
        text = text.replace(anchor, anchor + f"- `{CANON}`\n", 1)
    write(path, text)


def update_start_here() -> None:
    path = "[기획서]/00_프로젝트_허브/START_HERE.md"
    text = read(path)
    text = replace_once(
        text,
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-06 / NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED / PLANNING_ONLY**",
        f"> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / {RESUME} / PLANNING_ONLY**",
        "start header",
    )
    text = replace_once(
        text,
        "BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_06_START: 42469f6e2058efea464755ac44bec8bcd1154f0b",
        f"BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_07_START: {PROJECT_MAIN_AT_START}",
        "start project observation",
    )
    text = replace_once(text, "BASE_CURRENT_MAIN_OBSERVED: 7ce96181d0a97930300fcc6d383dacc75ad08f6a", f"BASE_CURRENT_MAIN_OBSERVED: {BASE_MAIN}", "start base observation")
    text = replace_once(text, "R3_R7_APPROVAL_COUNTER: 6/10", "R3_R7_APPROVAL_COUNTER: 7/10", "start counter")
    text = replace_once(text, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-06", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07", "start decision")
    text = replace_once(text, "R3_R7_RESUME_LOCATOR: NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED", f"R3_R7_RESUME_LOCATOR: {RESUME}", "start locator")
    start = text.index("## 현재 R3–R7 설계 재개")
    owner = text.index("책임 원본:", start)
    section = """## 현재 R3–R7 설계 재개

`BS-CONTENT-20260811-01`~`06`은 승인 완료 이력으로 유지한다.

현재 사용자 승인 Decision: `BS-CONTENT-20260811-07`.
현재 연속 작업은 `BS-CONTENT-20260811-07`이다.

```text
SOLDIER_02 / LIANA_BERG
FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY
→ 임무 책임·위험·장비 역할 공개
→ 실제 작품 UID 후보 비교
→ 한 작품 UID 선택·같은 UID 인계
→ 비직접 전선 결과
→ MISSION_DUTY_STATE
 + COMMANDER_RETURN_STATE
 + ITEM_UID_FIELD_LEGACY_STATE
→ 같은 UID의 수리·복원·강화·신작·보존·재배정 판단
```

- Marek의 소량 표준화와 Cassia의 arena contribution 책임을 보존한다.
- 최고 방어·최고 강화 또는 숨은 command/hero 점수를 자동 정답으로 만들지 않는다.
- 작품 한 점이 임무 결과의 유일한 원인인 것처럼 단순화하지 않는다.
- 직접 전술전투·부대 대형·실시간 병참·사상자 관리·baseline permadeath를 추가하지 않는다.
- 임무 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

"""
    text = text[:start] + section + text[owner:]
    anchor = "1. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`\n"
    if f"`{CANON}`" not in text:
        text = text.replace(anchor, anchor + f"2. `{CANON}`\n", 1)
    write(path, text)


def update_roadmap() -> None:
    path = "[기획서]/00_프로젝트_허브/ROADMAP.md"
    text = read(path)
    text = replace_once(
        text,
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-06 / NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED / PLANNING_ONLY**",
        f"> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / {RESUME} / PLANNING_ONLY**",
        "roadmap header",
    )
    text = replace_once(text, "CURRENT_STAGE_STATUS: R3_R7_6_OF_10_USER_APPROVED_PLANNING_ONLY", "CURRENT_STAGE_STATUS: R3_R7_7_OF_10_USER_APPROVED_PLANNING_ONLY", "roadmap status")
    text = replace_once(text, "R3_R7_APPROVAL_COUNTER: 6/10", "R3_R7_APPROVAL_COUNTER: 7/10", "roadmap counter")
    text = replace_once(text, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-06", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07", "roadmap decision")
    text = replace_once(text, "R3_R7_RESUME_LOCATOR: NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED", f"R3_R7_RESUME_LOCATOR: {RESUME}", "roadmap locator")
    text = replace_once(text, "현재 승인 카운터: `6/10`.", "현재 승인 카운터: `7/10`.", "roadmap prose counter")
    marker = "<!-- BS-CONTENT-20260811-05 CURRENT -->"
    if marker in text:
        tail = """<!-- BS-CONTENT-20260811-07 CURRENT -->
## R3–R7 current 7/10 — Liana Soldier02

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 7/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07
R3_R7_RESUME_LOCATOR: SOLDIER_02_LIANA_MISSION_FIT_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

Nadia 1/10, Toren 2/10, Marek 3/10, Ersa 4/10, Cassia 5/10, Noble01 6/10은 승인 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-07`이다.

### 7/10 — `BS-CONTENT-20260811-07`

```text
SOLDIER_02 / LIANA_BERG
FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY
MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE
```

목표:

- 기존 Liana 고객을 한 명의 전선 지휘관 책임 콘텐츠로 상세화한다.
- 공개된 임무·위험·필요 역할과 실제 작품 UID 증거를 비교해 한 작품을 인계한다.
- Marek의 multi-UID 소량 표준화와 Cassia의 arena contribution 책임을 침범하지 않는다.
- 임무 성공·리아나 귀환·같은 UID 작품 생애를 별도 결과로 유지한다.
- 최고 방어·최고 강화·command/hero/leadership/mission-fit 총점을 자동 정답으로 만들지 않는다.
- 직접 전술전투·대형/이동·실시간 병참·사상자 관리·baseline permadeath·replacement loop를 추가하지 않는다.
- 작품 단독 인과와 임무 반복 Artistry/Chronicle farming을 금지한다.
- 정확 임무·임계값·부상·경제·보상·분포는 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
"""
        text = text[: text.index(marker)] + tail
    write(path, text)


def update_gates() -> None:
    path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
    text = read(path)
    text = replace_once(
        text,
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-06 / NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**",
        f"> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / {RESUME} / PLANNING_ONLY / PRODUCT_BLOCKED**",
        "gates header",
    )
    text = replace_once(text, "R3_R7_APPROVAL_COUNTER: 6/10", "R3_R7_APPROVAL_COUNTER: 7/10", "gates counter")
    text = replace_once(text, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-06", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07", "gates decision")
    text = replace_once(text, "- R3–R7 `6/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.", "- R3–R7 `7/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.", "gates research state")
    start = text.index("## R3–R7 Planning-Only Gate")
    end = text.index("## Canon Gate", start)
    section = """## R3–R7 Planning-Only Gate

현재 Decision: `BS-CONTENT-20260811-07`.
Decision: `BS-CONTENT-20260811-07`.

첫 승인 완료 Decision: `BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`.

```text
SOLDIER_02 / LIANA_BERG
FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY
MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE
```

- `BS-CONTENT-20260811-01`~`06`은 승인 완료 이력으로 보존한다.
- 기존 `LIANA_BERG` 고객을 재사용하고 병렬 Soldier commander를 만들지 않는다.
- Marek의 `SMALL_LOT_STANDARD_ORDER`와 Cassia의 `ARENA_SIGNATURE_WEAPON_AND_LEGACY` 책임을 보존한다.
- 같은 UID를 보존하고 임무 성공·리아나 귀환·작품 현장 생애를 분리한다.
- 직접 전술전투·부대 이동/대형·실시간 병참·사상자 micromanagement를 추가하지 않는다.
- command/hero/leadership/mission-fit 총점과 최고 방어·최고 강화 자동정답을 만들지 않는다.
- 작품 하나를 임무 결과의 유일 원인으로 만들지 않는다.
- baseline Liana permadeath/replacement loop와 임무 반복 Artistry/Chronicle farming을 추가하지 않는다.
- 제품 구현은 `BLOCKED`, Task3 구현은 `NOT_APPROVED`다.

"""
    text = text[:start] + section + text[end:]
    write(path, text)


if __name__ == "__main__":
    update_registry()
    update_current()
    update_active()
    update_start_here()
    update_roadmap()
    update_gates()
