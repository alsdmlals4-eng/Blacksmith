from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D09 = "BS-CONTENT-20260811-09"
D08 = "BS-CONTENT-20260811-08"
CANON = "docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def require_replace(text: str, old: str, new: str, *, label: str, minimum: int = 1) -> str:
    count = text.count(old)
    if count < minimum:
        raise RuntimeError(f"{label}: expected at least {minimum} occurrence(s) of {old!r}, got {count}")
    return text.replace(old, new)


def update_registry() -> None:
    path = "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
    data = json.loads(read(path))
    if data.get("next_approval_counter") != "8/10":
        raise RuntimeError(f"registry current counter drifted: {data.get('next_approval_counter')!r}")
    ids = [item.get("id") for item in data.get("current_decisions", [])]
    if ids[-1:] != [D08] or D09 in ids:
        raise RuntimeError(f"registry decision sequence unexpected: tail={ids[-2:]}")
    data["next_approval_counter"] = "9/10"
    data["current_decisions"].append(
        {
            "id": D09,
            "title": "검투사 02 카일 바렌 베테랑 복귀 장비 연속성·교체 콘텐츠",
            "status": "USER_APPROVED_R3_R7_9_OF_10",
            "canon": CANON,
            "refines": ["BS-CONTENT-20260804-01", "BS-CONTENT-20260804-02"],
            "depends_on": [
                "BS-CUSTOMER-20260803-02",
                "BS-CUSTOMER-20260805-01",
                "BS-CUSTOMER-20260806-01",
                "BS-ITEM-20260806-04",
                "BS-ITEM-20260806-05",
                "BS-UX-20260805-01",
                "BS-CONTENT-20260811-05",
                "BS-CONTENT-20260811-06",
                "BS-CONTENT-20260811-08",
            ],
            "contract": {
                "content_id": "GLADIATOR_02",
                "customer_id": "KYLE_VAREN",
                "customer_archetype": "GLADIATOR",
                "activity_family": "VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION",
                "content_goal": "EQUIPMENT_CONTINUITY_RESPONSIBILITY_THROUGH_KEEP_OR_REPLACE",
                "player_role": "BLACKSMITH_EQUIPMENT_CONTINUITY_DECISION_MAKER_NOT_GLADIATOR_CONTROLLER",
                "existing_kyle_varen_customer_reused": True,
                "actual_prior_record_required_for_continuity_branch": True,
                "keep_path_same_uid_preserved": True,
                "old_item_history_preserved": True,
                "new_item_gets_new_uid": True,
                "cassia_arena_fit_responsibility_preserved": True,
                "noble01_treatment_depth_responsibility_preserved": True,
                "fabricated_kyle_history": False,
                "fake_legacy_item_for_content_unlock": False,
                "history_transfer_to_replacement": False,
                "uid_rewrite": False,
                "old_item_always_best": False,
                "new_item_always_best": False,
                "highest_enhancement_always_best": False,
                "highest_artistry_always_best": False,
                "most_chronicle_always_best": False,
                "sentiment_score": False,
                "veteran_total_score": False,
                "lineage_power_bonus": False,
                "legacy_arena_score_formula_canon": False,
                "fixed_iron_sword_canon": False,
                "legacy_gladiator_kyle_fixture_status": "NON_AUTHORITATIVE_HISTORICAL_FIXTURE",
                "direct_arena_combat": False,
                "gladiator_roster_or_guild_management": False,
                "training_or_injury_management": False,
                "betting_system": False,
                "baseline_permadeath": False,
                "comeback_count_artistry_growth": False,
                "replacement_count_artistry_growth": False,
                "automatic_chronicle_affix_from_comeback_or_retirement": False,
                "comeback_farming_multiplier": False,
                "result_axes": [
                    "VETERAN_RETURN_STATE",
                    "EQUIPMENT_CONTINUITY_STATE",
                    "ITEM_UID_LINEAGE_STATE",
                ],
                "feedback": "THREE_STATE_SUMMARY_TWO_TO_FOUR_ACTUAL_REASONS_ONE_PRIMARY_NEXT_ACTION",
                "exact_values": "NON_CANONICAL_BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
                "taxonomy_ambiguity": "P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED",
                "product_implementation": "BLOCKED",
                "task3_implementation": "NOT_APPROVED",
                "human_playtest": "NOT_RUN",
                "android_device": "NOT_RUN",
                "accessibility": "NOT_RUN",
                "planning_source_main": "80b35b9fc914853428e991c4130edc87dd260083",
            },
        }
    )
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def replace_current_tokens(text: str, label: str) -> str:
    text = require_replace(text, "R3_R7_APPROVAL_COUNTER: 8/10", "R3_R7_APPROVAL_COUNTER: 9/10", label=label)
    text = require_replace(text, f"R3_R7_CURRENT_DECISION: {D08}", f"R3_R7_CURRENT_DECISION: {D09}", label=label)
    text = require_replace(
        text,
        "R3_R7_RESUME_LOCATOR: COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED",
        "R3_R7_RESUME_LOCATOR: GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED",
        label=label,
    )
    return text


def update_current_decisions() -> None:
    path = "CURRENT_CONFIRMED_DECISIONS.md"
    text = read(path)
    text = require_replace(
        text,
        f"> **R3_R7_DESIGN_ACTIVE / {D08} / R3_R7_8_OF_10 / PLANNING_ONLY**",
        f"> **R3_R7_DESIGN_ACTIVE / {D09} / R3_R7_9_OF_10 / PLANNING_ONLY**",
        label=path,
    )
    text = replace_current_tokens(text, path)
    lines = text.splitlines()
    if any(line.startswith(f"- `{D09}`:") for line in lines):
        raise RuntimeError("Decision09 bullet unexpectedly already exists")
    index = next(i for i, line in enumerate(lines) if line.startswith(f"- `{D08}`:"))
    d09_line = (
        f"- `{D09}`: `GLADIATOR_02` 카일 바렌 베테랑 복귀 장비 연속성·교체 콘텐츠. "
        "실제 prior Kyle 작품의 현재 상태와 생애 기록을 읽고 hard serviceability/eligibility 뒤 "
        "`KEEP_IN_SERVICE` 또는 `RETIRE_AND_REPLACE`를 선택한다. keep은 같은 UID를 보존하고, "
        "replace는 old UID/history를 보존한 채 distinct new UID로 시작한다. Cassia arena-fit과 Noble01 treatment-depth 책임을 보존하며 "
        "legacy `gladiator_kyle/iron_sword` fixed score는 historical fixture로만 남긴다. 결과는 "
        "`VETERAN_RETURN_STATE / EQUIPMENT_CONTINUITY_STATE / ITEM_UID_LINEAGE_STATE`로 분리한다. — "
        "`USER_APPROVED / R3_R7_9_OF_10 / PLANNING_ONLY`"
    )
    lines.insert(index + 1, d09_line)
    write(path, "\n".join(lines) + "\n")


def update_active() -> None:
    path = "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
    text = read(path)
    text = require_replace(
        text,
        f"> **R3_R7_DESIGN_ACTIVE / {D08} / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
        f"> **R3_R7_DESIGN_ACTIVE / {D09} / GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED / PLANNING_ONLY**",
        label=path,
    )
    text = require_replace(text, "Blacksmith current main observed at Decision 08 start: `7005a939e003f7248e7d2546c4266bb5d144f90a`", "Blacksmith current main observed at Decision 09 start: `80b35b9fc914853428e991c4130edc87dd260083`", label=path)
    text = require_replace(text, "현재 R3–R7 승인 카운터: `8/10`", "현재 R3–R7 승인 카운터: `9/10`", label=path)
    text = replace_current_tokens(text, path)
    start = text.index("## 현재 R3–R7 기획 재개 상태")
    end = text.index("## 현재 권위와 보호 경계", start)
    section = f'''## 현재 R3–R7 기획 재개 상태\n\n`BS-CONTENT-20260811-01`~`08`은 승인 완료 이력으로 유지한다. 현재 Decision은 `{D09}`이다.\n\n```text\nGLADIATOR_02 / KYLE_VAREN\n→ 기존 구형 PoC 계승 고객을 두 번째 Gladiator-family 상세 콘텐츠로 승격\n→ VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION\n→ 실제 prior Kyle item record + comeback 목적 공개\n→ old UID current state·실제 lifecycle evidence + hard serviceability/eligibility 확인\n→ KEEP_IN_SERVICE 또는 RETIRE_AND_REPLACE\n→ 비직접 comeback/arena world event\n→ VETERAN_RETURN_STATE\n + EQUIPMENT_CONTINUITY_STATE\n + ITEM_UID_LINEAGE_STATE\n→ 실제 원인 2~4개 + 주 후속 행동 1개\n```\n\n- Cassia/Gladiator01의 current-match arena fit·equipment contribution 책임을 보존한다.\n- Noble01/기존 repair owner의 treatment-depth 책임을 보존한다.\n- keep path는 같은 UID를 유지한다.\n- replacement는 old UID/history를 보존하고 new UID로 시작하며 history/progression을 복사하지 않는다.\n- 오래된 작품·새 작품·최고 강화·최고 Artistry·가장 많은 Chronicle이 자동 정답이 아니다.\n- sentiment/veteran/lineage 총점을 추가하지 않는다.\n- legacy `gladiator_kyle / iron_sword` fixed data와 score formula는 historical non-authoritative fixture다.\n- 직접 arena combat·roster/guild·training/injury management·betting·baseline permadeath를 추가하지 않는다.\n- comeback/replacement 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.\n- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`를 이번 Decision에서 재정의하지 않는다.\n\n책임 원본:\n\n- `{CANON}`\n- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`\n- `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`\n- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`\n- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`\n\n이 승인은 **기획 재개 승인**이다. Task3 또는 일반 제품 구현 승인이 아니다.\n\n'''
    text = text[:start] + section + text[end:]
    text = text.replace(f"현재 Decision은 `{D08}`이다.", f"현재 Decision은 `{D09}`이다.")
    if "GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED" not in text:
        raise RuntimeError("active locator missing after update")
    if f"{D09} / R3_R7_9_OF_10" not in text:
        marker = "BS-CONTENT-20260811-08 / R3_R7_8_OF_10"
        text = require_replace(text, marker, marker + f"\n{D09} / R3_R7_9_OF_10", label=path)
    text += f'''\n<!-- BS-CONTENT-20260811-09 CURRENT -->\n## R3–R7 current 9/10 — Kyle Gladiator02\n\n```text\nR3_R7_DESIGN_ACTIVE\nR3_R7_APPROVAL_COUNTER: 9/10\nR3_R7_CURRENT_DECISION: {D09}\nR3_R7_RESUME_LOCATOR: GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED\nPRODUCT_IMPLEMENTATION: BLOCKED\nTASK3_IMPLEMENTATION: NOT_APPROVED\n```\n\n현재 Decision은 `{D09}`이다. `GLADIATOR_02 / KYLE_VAREN`은 실제 prior item의 현역 지속 또는 은퇴·교체 판단을 소유한다.\n'''
    write(path, text)


def update_start_here() -> None:
    path = "[기획서]/00_프로젝트_허브/START_HERE.md"
    text = read(path)
    text = require_replace(
        text,
        f"> **R3_R7_DESIGN_ACTIVE / {D08} / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
        f"> **R3_R7_DESIGN_ACTIVE / {D09} / GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED / PLANNING_ONLY**",
        label=path,
    )
    text = require_replace(text, "BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_08_START: 7005a939e003f7248e7d2546c4266bb5d144f90a", "BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_09_START: 80b35b9fc914853428e991c4130edc87dd260083", label=path)
    text = replace_current_tokens(text, path)
    text = text.replace(f"현재 사용자 승인 Decision: `{D08}`.", f"현재 사용자 승인 Decision: `{D09}`.")
    text = text.replace(f"현재 연속 작업은 `{D08}`이다.", f"현재 연속 작업은 `{D09}`이다.")
    start = text.index("## 현재 R3–R7 설계 재개")
    end = text.index("## 처음 읽을 순서", start)
    section = f'''## 현재 R3–R7 설계 재개\n\n`BS-CONTENT-20260811-01`~`08`은 승인 완료 이력으로 유지한다.\n\n현재 사용자 승인 Decision: `{D09}`.\n현재 연속 작업은 `{D09}`이다.\n\n```text\nGLADIATOR_02 / KYLE_VAREN\nVETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION\n→ 실제 prior Kyle item record 확인\n→ comeback 목적 + 현재 역할 공개\n→ hard serviceability/eligibility + 실제 lifecycle evidence\n→ KEEP_IN_SERVICE 또는 RETIRE_AND_REPLACE\n→ 비직접 comeback 결과\n→ VETERAN_RETURN_STATE\n + EQUIPMENT_CONTINUITY_STATE\n + ITEM_UID_LINEAGE_STATE\n```\n\n- Cassia는 current-match arena fit, Kyle는 keep/retire-replace continuity를 소유한다.\n- Noble01/기존 repair owner는 treatment depth를 계속 소유한다.\n- keep path는 same UID, replacement path는 old UID/history 보존 + new UID다.\n- old history/progression을 new UID로 복사하지 않는다.\n- legacy `gladiator_kyle / iron_sword` fixed score는 current canon이 아니다.\n- 직접 arena/roster/training/injury/betting 범위로 확장하지 않는다.\n- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 유지한다.\n- 제품 구현: `BLOCKED`.\n- Task3 구현: `NOT_APPROVED`.\n\n책임 원본:\n\n1. `{CANON}`\n2. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`\n3. `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`\n4. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`\n5. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`\n\n'''
    text = text[:start] + section + text[end:]
    text = text.replace(
        "1. `AGENTS.md`\n2. `CURRENT_CONFIRMED_DECISIONS.md`\n3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`\n4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`",
        f"1. `AGENTS.md`\n2. `CURRENT_CONFIRMED_DECISIONS.md`\n3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`\n4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`\n5. `{CANON}`",
    )
    text += f'''\n<!-- BS-CONTENT-20260811-09 CURRENT -->\n## R3–R7 current 9/10 — Kyle Gladiator02\n\n```text\nR3_R7_DESIGN_ACTIVE\nR3_R7_APPROVAL_COUNTER: 9/10\nR3_R7_CURRENT_DECISION: {D09}\nR3_R7_RESUME_LOCATOR: GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED\nPRODUCT_IMPLEMENTATION: BLOCKED\nTASK3_IMPLEMENTATION: NOT_APPROVED\n```\n\n현재 연속 작업은 `{D09}`이다.\n'''
    write(path, text)


def update_roadmap() -> None:
    path = "[기획서]/00_프로젝트_허브/ROADMAP.md"
    text = read(path)
    text = require_replace(
        text,
        f"> **R3_R7_DESIGN_ACTIVE / {D08} / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
        f"> **R3_R7_DESIGN_ACTIVE / {D09} / GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED / PLANNING_ONLY**",
        label=path,
    )
    text = require_replace(text, "CURRENT_STAGE_STATUS: R3_R7_8_OF_10_USER_APPROVED_PLANNING_ONLY", "CURRENT_STAGE_STATUS: R3_R7_9_OF_10_USER_APPROVED_PLANNING_ONLY", label=path)
    text = replace_current_tokens(text, path)
    text = require_replace(text, "현재 승인 카운터: `8/10`.", "현재 승인 카운터: `9/10`.", label=path)
    insert_at = text.index("## R3 — 버티컬 슬라이스 기반")
    d09_section = f'''### 9/10 — `{D09}`\n\n```text\nGLADIATOR_02 / KYLE_VAREN\nVETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION\nVETERAN_RETURN_STATE / EQUIPMENT_CONTINUITY_STATE / ITEM_UID_LINEAGE_STATE\n```\n\n목표:\n\n- 실제 prior Kyle 작품의 현재 상태와 생애 기록을 읽고 현역 유지 또는 은퇴·교체를 판단한다.\n- hard serviceability/eligibility가 감성보다 먼저다.\n- keep path는 same UID를 보존하고 replacement path는 old UID/history를 보존한 채 distinct new UID로 시작한다.\n- Cassia의 arena-fit/equipment-contribution 책임과 Noble01의 treatment-depth 책임을 침범하지 않는다.\n- legacy Kyle/iron_sword fixed 수치·score formula를 current canon으로 부활시키지 않는다.\n- old/new item 자동정답·sentiment/veteran/lineage score·직접 arena/roster/training/injury 관리·반복 progression farming을 추가하지 않는다.\n- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 별도 승인까지 보류한다.\n\n책임 원본:\n\n- `{CANON}`\n- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`\n\n'''
    if f"### 9/10 — `{D09}`" in text:
        raise RuntimeError("roadmap D09 heading already exists")
    text = text[:insert_at] + d09_section + text[insert_at:]
    text = text.replace(f"`BS-CONTENT-20260811-01`부터 `{D08}`까지", f"`BS-CONTENT-20260811-01`부터 `{D09}`까지")
    gate_anchor = "BS-CONTENT-20260811-07: USER_APPROVED_PLANNING_ONLY"
    if gate_anchor in text and f"{D09}: USER_APPROVED_PLANNING_ONLY" not in text:
        text = text.replace(gate_anchor, gate_anchor + f"\nBS-CONTENT-20260811-08: USER_APPROVED_PLANNING_ONLY\n{D09}: USER_APPROVED_PLANNING_ONLY")
    text += f'''\n<!-- BS-CONTENT-20260811-09 CURRENT -->\n## R3–R7 current 9/10 — Kyle Gladiator02\n\n```text\nR3_R7_DESIGN_ACTIVE\nR3_R7_APPROVAL_COUNTER: 9/10\nR3_R7_CURRENT_DECISION: {D09}\nR3_R7_RESUME_LOCATOR: GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED\nPRODUCT_IMPLEMENTATION: BLOCKED\nTASK3_IMPLEMENTATION: NOT_APPROVED\n```\n'''
    write(path, text)


def update_gates() -> None:
    path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
    text = read(path)
    text = require_replace(
        text,
        f"> **R3_R7_DESIGN_ACTIVE / {D08} / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**",
        f"> **R3_R7_DESIGN_ACTIVE / {D09} / GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**",
        label=path,
    )
    text = replace_current_tokens(text, path)
    text = text.replace("R3–R7 `8/10`, 제품/Task3 차단", "R3–R7 `9/10`, 제품/Task3 차단")
    start = text.index("## R3–R7 Planning-Only Gate")
    end = text.index("## Canon Gate", start)
    section = f'''## R3–R7 Planning-Only Gate\n\n현재 Decision: `{D09}`.\nDecision: `{D09}`.\n\n첫 승인 완료 Decision: `BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`.\n\n```text\nGLADIATOR_02 / KYLE_VAREN\nVETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION\nVETERAN_RETURN_STATE / EQUIPMENT_CONTINUITY_STATE / ITEM_UID_LINEAGE_STATE\n```\n\n- `BS-CONTENT-20260811-01`~`08`은 승인 완료 이력으로 보존한다.\n- `BS-CONTENT-20260811-08 / COLLECTOR_02 / SEDRIC_VAEL`은 8/10 승인 이력이며 current locator가 아니다.\n- `{D09} / GLADIATOR_02 / KYLE_VAREN`가 현재 9/10 Decision이다.\n- actual prior Kyle item record가 continuity branch의 근거다. 존재하지 않는 history/item을 생성하지 않는다.\n- hard serviceability/eligibility가 sentiment보다 먼저다.\n- keep path는 same UID를 유지한다. replacement는 old UID/history를 보존하고 new UID로 시작한다.\n- old history/progression을 replacement UID에 복사하지 않는다.\n- Cassia arena-fit/equipment-contribution과 Noble01 treatment-depth 책임을 보존한다.\n- legacy `gladiator_kyle / iron_sword` fixed score formula는 historical non-authoritative fixture다.\n- old/new automatic-best, sentiment/veteran/lineage score, direct arena/roster/training/injury/betting, baseline permadeath, comeback farming을 추가하지 않는다.\n- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 이번 Decision으로 해결하지 않는다.\n- 제품 구현은 `BLOCKED`, Task3 구현은 `NOT_APPROVED`다.\n\n'''
    text = text[:start] + section + text[end:]
    write(path, text)


def main() -> None:
    update_registry()
    update_current_decisions()
    update_active()
    update_start_here()
    update_roadmap()
    update_gates()
    subprocess.run(["python", "-m", "unittest", "tests.test_r3_gladiator_02_kyle_content", "-v"], cwd=ROOT, check=True)
    # The helper is one-shot and must not remain in the retained diff.
    Path(__file__).unlink()


if __name__ == "__main__":
    main()
