from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "[기획서]/00_프로젝트_허브"
DECISION = "BS-CONTENT-20260811-06"
LOCATOR = "NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED"
NOBLE_CANON = "docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md"
BLACKSMITH_MAIN_AT_DECISION06_START = "42469f6e2058efea464755ac44bec8bcd1154f0b"
BASE_MAIN_OBSERVED = "7ce96181d0a97930300fcc6d383dacc75ad08f6a"


def strip_materializer_note(text: str) -> str:
    return re.sub(r"\n<!-- BS-CONTENT-20260811-06 -->\n> `NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED`.*\Z", "\n", text, flags=re.S)


def replace_section(text: str, heading: str, next_heading: str, body: str) -> str:
    start = text.index(heading)
    end = text.index(next_heading, start)
    return text[:start] + body.rstrip() + "\n\n" + text[end:]


def update_active_context() -> None:
    path = HUB / "ACTIVE_CONTEXT.md"
    text = strip_materializer_note(path.read_text(encoding="utf-8"))
    text = text.replace(
        "> **R3_R7_DESIGN_ACTIVE / GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED / PLANNING_ONLY**",
        "> **R3_R7_DESIGN_ACTIVE / NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED / PLANNING_ONLY**",
        1,
    )
    text = re.sub(
        r"- Blacksmith current main observed at Decision 05 start: `[^`]+`",
        f"- Blacksmith current main observed at Decision 06 start: `{BLACKSMITH_MAIN_AT_DECISION06_START}`",
        text,
        count=1,
    )
    text = re.sub(
        r"- `BASE_CURRENT_MAIN_OBSERVED`: `[^`]+`",
        f"- `BASE_CURRENT_MAIN_OBSERVED`: `{BASE_MAIN_OBSERVED}`",
        text,
        count=1,
    )
    text = text.replace("- 현재 R3–R7 승인 카운터: `5/10`", "- 현재 R3–R7 승인 카운터: `6/10`", 1)
    text = text.replace(
        "R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED",
        f"R3_R7_RESUME_LOCATOR: {LOCATOR}",
        1,
    )
    current_body = """## 현재 R3–R7 기획 재개 상태

`BS-CONTENT-20260811-01` Nadia, `BS-CONTENT-20260811-02` Toren, `BS-CONTENT-20260811-03` Marek, `BS-CONTENT-20260811-04` Ersa, `BS-CONTENT-20260811-05` Cassia는 승인 완료 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-06`다.

```text
NOBLE_01 / CEREMONIAL_NOBLE
→ 귀족 유형 첫 상세 콘텐츠
→ HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY
→ 기존 가보 UID + 계승 목적 공개
→ 실제 상태·손상·과거 수리·소유·계승·Chronicle evidence 확인
→ 기존 수리·복원·재작업 권위 안에서 개입 깊이 선택
→ 같은 UID 인계
→ 의식은 비직접 세계 사건
→ CEREMONY_READINESS_STATE
 + HEIRLOOM_TREATMENT_FIT_STATE
 + ITEM_UID_DYNASTIC_LEGACY_STATE
→ 보존·재수리·재사용·전시·후속 계승 판단 이유
```

- 기존 `ceremonial_noble` representative fixture를 재사용하고 새 이름·가문 lore를 발명하지 않는다.
- 최대 복원·최고 Artistry를 자동 정답으로 만들지 않는다.
- 새 가문 위신·진품성·계승 총점을 만들지 않는다.
- 수리·복원으로 물리 흔적이 변해도 의미 있는 과거 생애 기록은 삭제하지 않는다.
- 복원/의식 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 직접 의식·귀족 가문·궁정·외교 경영을 추가하지 않는다.
- 같은 작품 UID를 처치 전·후·의식·반환까지 보존한다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`

이 승인은 **기획 재개 승인**이다. Task3 또는 일반 제품 구현 승인이 아니다."""
    text = replace_section(text, "## 현재 R3–R7 기획 재개 상태", "## 현재 권위와 보호 경계", current_body)
    anchor = "- `BS-CONTENT-20260811-05`는 경기 승패와 작품 기여를 분리하고 경기 반복으로 예술성 또는 Chronicle을 자동 성장시키지 않는다.\n"
    addition = (
        "- `BS-CONTENT-20260811-06`은 최대 복원·최고 Artistry·가문 위신/진품성 총점 자동 정답을 만들지 않는다.\n"
        "- `BS-CONTENT-20260811-06`은 의미 있는 과거 생애 기록을 지우거나 복원/의식 반복으로 예술성·Chronicle을 자동 성장시키지 않는다.\n"
    )
    if addition.splitlines()[0] not in text:
        text = text.replace(anchor, anchor + addition, 1)
    if "BS-CONTENT-20260811-06 / R3_R7_6_OF_10" not in text:
        text = text.replace(
            "BS-CONTENT-20260811-05 / R3_R7_5_OF_10\n",
            "BS-CONTENT-20260811-05 / R3_R7_5_OF_10\nBS-CONTENT-20260811-06 / R3_R7_6_OF_10\n",
            1,
        )
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_start_here() -> None:
    path = HUB / "START_HERE.md"
    text = strip_materializer_note(path.read_text(encoding="utf-8"))
    text = text.replace(
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-05 / GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED / PLANNING_ONLY**",
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-06 / NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED / PLANNING_ONLY**",
        1,
    )
    text = re.sub(
        r"BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_05_START: [0-9a-f]+",
        f"BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_06_START: {BLACKSMITH_MAIN_AT_DECISION06_START}",
        text,
        count=1,
    )
    text = re.sub(r"BASE_CURRENT_MAIN_OBSERVED: [0-9a-f]+", f"BASE_CURRENT_MAIN_OBSERVED: {BASE_MAIN_OBSERVED}", text, count=1)
    text = text.replace(
        "R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED",
        f"R3_R7_RESUME_LOCATOR: {LOCATOR}",
        1,
    )
    current_body = """## 현재 R3–R7 설계 재개

`BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`, `BS-CONTENT-20260811-02 / ADVENTURER_02 / TOREN_MARCH`, `BS-CONTENT-20260811-03 / SOLDIER_01 / MAREK_OLDEN`, `BS-CONTENT-20260811-04 / COLLECTOR_01 / ERSA_ROEN`, `BS-CONTENT-20260811-05 / GLADIATOR_01 / CASSIA_BELLAN`은 승인 완료 이력으로 유지한다.

현재 사용자 승인 Decision: `BS-CONTENT-20260811-06`.

```text
NOBLE_01 / CEREMONIAL_NOBLE
HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY
→ 기존 가보 UID + 계승 목적 공개
→ 실제 상태·과거 수리·소유·계승 증거 확인
→ 개입 깊이 판단
→ 같은 UID 인계
→ 비직접 계승 의식 결과
→ CEREMONY_READINESS_STATE
 + HEIRLOOM_TREATMENT_FIT_STATE
 + ITEM_UID_DYNASTIC_LEGACY_STATE
→ 같은 UID의 보존·재수리·사용·전시·후속 계승 판단
```

- 기존 `ceremonial_noble` representative fixture를 재사용한다.
- 최대 복원·최고 Artistry·가문 위신/진품성/계승 총점은 자동 정답이 아니다.
- 의미 있는 과거 생애 기록을 수리 과정에서 지우지 않는다.
- 복원/의식 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 직접 의식·가문·궁정·외교 경영은 추가하지 않는다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

책임 원본:

1. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
2. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
3. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
4. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
5. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`"""
    text = replace_section(text, "## 현재 R3–R7 설계 재개", "## 처음 읽을 순서", current_body)
    reading_old = """1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`"""
    reading_new = """1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`"""
    text = text.replace(reading_old, reading_new, 1)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_roadmap() -> None:
    path = HUB / "ROADMAP.md"
    text = strip_materializer_note(path.read_text(encoding="utf-8"))
    text = text.replace(
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-05 / GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED / PLANNING_ONLY**",
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-06 / NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED / PLANNING_ONLY**",
        1,
    )
    text = text.replace("CURRENT_STAGE_STATUS: R3_R7_5_OF_10_USER_APPROVED_PLANNING_ONLY", "CURRENT_STAGE_STATUS: R3_R7_6_OF_10_USER_APPROVED_PLANNING_ONLY", 1)
    text = text.replace(
        "R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED",
        f"R3_R7_RESUME_LOCATOR: {LOCATOR}",
        1,
    )
    if "### 6/10 — `BS-CONTENT-20260811-06`" not in text:
        section = """

### 6/10 — `BS-CONTENT-20260811-06`

```text
NOBLE_01 / CEREMONIAL_NOBLE
HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY
CEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE
```

목표:

- 기존 가보 UID의 실제 상태·손상·과거 수리·소유·계승·Chronicle evidence와 공개된 계승 목적을 읽고 개입 깊이를 판단한다.
- 최대 복원·최고 Artistry를 자동 정답으로 만들지 않고 새 가문 위신·진품성·계승 총점을 추가하지 않는다.
- 물리 흔적을 처치하더라도 의미 있는 과거 생애 기록을 삭제하지 않는다.
- 같은 UID를 처치 전·후·의식·반환까지 보존한다.
- 복원/의식 반복으로 Artistry 또는 Chronicle Affix를 자동 성장시키지 않는다.
- 직접 의식·귀족 가문·궁정·외교 경영을 추가하지 않는다.
- 정확 임계값·경제·보상·분포는 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
"""
        text = text.rstrip() + section
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_gates() -> None:
    path = HUB / "DEVELOPMENT_GATES.md"
    text = strip_materializer_note(path.read_text(encoding="utf-8"))
    text = text.replace(
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-05 / GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**",
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-06 / NOBLE_01_HEIRLOOM_SUCCESSION_RESTORATION_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**",
        1,
    )
    text = text.replace("- R3–R7 `5/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.", "- R3–R7 `6/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.", 1)
    planning_body = """## R3–R7 Planning-Only Gate

현재 Decision: `BS-CONTENT-20260811-06`.

첫 승인 완료 Decision: `BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`.

```text
NOBLE_01 / CEREMONIAL_NOBLE
HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY
CEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE
```

- `BS-CONTENT-20260811-01`~`05`는 승인 완료 이력으로 보존한다.
- 기존 `ceremonial_noble` 대표 fixture를 재사용한다.
- 최대 복원·최고 Artistry·가문 위신/진품성/계승 총점 자동 정답을 만들지 않는다.
- 의미 있는 과거 생애 기록을 수리·복원 과정에서 삭제하지 않는다.
- 같은 UID를 보존하고 복원/의식 반복으로 Artistry·Chronicle을 자동 성장시키지 않는다.
- 직접 의식·귀족 가문·궁정·외교 경영을 추가하지 않는다.
- 제품 구현은 `BLOCKED`, Task3 구현은 `NOT_APPROVED`다."""
    start = text.index("## R3–R7 Planning-Only Gate")
    next_heading = re.search(r"\n## ", text[start + len("## R3–R7 Planning-Only Gate"):])
    if next_heading:
        end = start + len("## R3–R7 Planning-Only Gate") + next_heading.start() + 1
        text = text[:start] + planning_body.rstrip() + "\n\n" + text[end:]
    else:
        text = text[:start] + planning_body.rstrip() + "\n"
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def update_operating_audit() -> None:
    path = ROOT / "tools/run_project_operating_system_audit.py"
    text = path.read_text(encoding="utf-8")
    if "R3_NOBLE_CANON" not in text:
        text = text.replace(
            'R3_CASSIA_CANON = "docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md"\n',
            'R3_CASSIA_CANON = "docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md"\nR3_NOBLE_CANON = "docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md"\n',
            1,
        )
    text = text.replace(
        'R3_CURRENT_DECISION = "BS-CONTENT-20260811-05"',
        'R3_FIFTH_DECISION = "BS-CONTENT-20260811-05"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-06"',
        1,
    )
    text = text.replace('"next_approval_counter": "5/10"', '"next_approval_counter": "6/10"', 1)
    registry_id_line = '        f\'"id": "{R3_CURRENT_DECISION}"\',\n'
    if 'f\'"id": "{R3_FIFTH_DECISION}"\'' not in text:
        text = text.replace(
            registry_id_line,
            '        f\'"id": "{R3_FIFTH_DECISION}"\',\n' + registry_id_line,
            1,
        )
    registry_anchor = '        \'"opaque_arena_score": false\',\n    )'
    if '\'"content_id": "NOBLE_01"\'' not in text:
        text = text.replace(
            registry_anchor,
            '        \'"opaque_arena_score": false\',\n'
            '        \'"content_id": "NOBLE_01"\',\n'
            '        \'"customer_id": "CEREMONIAL_NOBLE"\',\n'
            '        \'"activity_family": "HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY"\',\n'
            '        \'"same_item_uid_preserved": true\',\n'
            '        \'"full_restoration_always_best": false\',\n'
            '        \'"history_erasure_on_repair": false\',\n'
            '    )',
            1,
        )
    cassia_start = text.index("    assertions[R3_CASSIA_CANON] = (")
    gates_start = text.index("\n    gates_path =", cassia_start)
    cassia_segment = text[cassia_start:gates_start]
    cassia_segment = cassia_segment.replace("        R3_CURRENT_DECISION,", "        R3_FIFTH_DECISION,", 1)
    if "assertions[R3_NOBLE_CANON]" not in cassia_segment:
        cassia_segment = cassia_segment.rstrip() + """

    assertions[R3_NOBLE_CANON] = (
        R3_CURRENT_DECISION,
        "NOBLE_01",
        "CEREMONIAL_NOBLE",
        "HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY",
        "CEREMONY_READINESS_STATE",
        "HEIRLOOM_TREATMENT_FIT_STATE",
        "ITEM_UID_DYNASTIC_LEGACY_STATE",
        "SAME_ITEM_UID_PRESERVED",
        "NO_FULL_RESTORATION_ALWAYS_BEST",
        "NO_HISTORY_ERASURE_ON_REPAIR",
        "NO_NOBLE_HOUSE_MANAGEMENT",
        "제품 구현: `BLOCKED`",
        "Task3 구현: `NOT_APPROVED`",
    )
"""
    text = text[:cassia_start] + cassia_segment + text[gates_start:]
    text = text.replace('"R3_R7_APPROVAL_COUNTER: 5/10",', '"R3_R7_APPROVAL_COUNTER: 6/10",')
    router_sequence = "            R3_FOURTH_DECISION,\n            R3_CURRENT_DECISION,"
    if "            R3_FIFTH_DECISION,\n            R3_CURRENT_DECISION," not in text:
        text = text.replace(
            router_sequence,
            "            R3_FOURTH_DECISION,\n            R3_FIFTH_DECISION,\n            R3_CURRENT_DECISION,",
            1,
        )
    text = text.replace('            "GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED",', f'            "{LOCATOR}",', 1)
    text = text.replace(
        'if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `5/10`" not in tokens:\n            tokens.append("현재 R3–R7 승인 카운터: `5/10`")',
        'if path.endswith("ACTIVE_CONTEXT.md") and "현재 R3–R7 승인 카운터: `6/10`" not in tokens:\n            tokens.append("현재 R3–R7 승인 카운터: `6/10`")',
        1,
    )
    text = text.replace(
        "for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON):",
        "for path in (R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON, R3_NOBLE_CANON):",
        1,
    )
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    update_active_context()
    update_start_here()
    update_roadmap()
    update_gates()
    update_operating_audit()


if __name__ == "__main__":
    main()
