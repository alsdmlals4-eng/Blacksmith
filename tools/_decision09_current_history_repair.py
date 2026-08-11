from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D08 = "BS-CONTENT-20260811-08"
D09 = "BS-CONTENT-20260811-09"
LOC08 = "COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED"
LOC09 = "GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED"
KYLE_CANON = "docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def repair_active() -> None:
    path = "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
    text = read(path)
    current_start = text.index("## 현재 R3–R7 기획 재개 상태")
    owners_start = text.index("책임 원본:\n\n", current_start)
    owners_end = text.index("\n\n이 승인은", owners_start)
    owners = """책임 원본:

- `docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md`
- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`"""
    text = text[:owners_start] + owners + text[owners_end:]

    next_start = text.index("## 다음 실행 순서")
    next_end = text.index("## 먼저 읽을 파일", next_start)
    next_section = """## 다음 실행 순서

1. `BS-CONTENT-20260811-09`의 focused GREEN 뒤 D01–D08 역사/current consumer 회귀를 닫는다.
2. Kyle continuity가 Cassia arena-fit과 Noble01 treatment-depth를 침범하지 않고 old/new UID history 경계를 지키는지 적대 검토한다.
3. 하나의 exact reviewed head에서 Python·Godot·Base·BCA·GUT·HiGodot·Adapter Gate를 모두 GREEN으로 만든다.
4. PR #154 병합과 같은 Decision ID의 Google Sheet sync/readback을 닫은 뒤에만 다음 신규 R3–R7 Decision `10/10` 사용자 기획 승인 Gate로 이동한다.
5. 새 제품 Task는 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED`와 `TASK3_IMPLEMENTATION: NOT_APPROVED`가 별도 사용자 승인으로 해소되기 전 시작하지 않는다.

"""
    text = text[:next_start] + next_section + text[next_end:]

    read_start = text.index("## 먼저 읽을 파일")
    read_end = text.index("## 현재 프로젝트 작업지시문 바인딩", read_start)
    read_section = """## 먼저 읽을 파일

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
9. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
10. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
11. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
12. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
13. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
14. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
15. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
16. Google Sheet `00_프로젝트_허브`, `01_작업순서`, `02_현재_확정결정`, `04_누락_충돌_감사`, `13_주요인물`, `50_메인콘텐츠`

"""
    text = text[:read_start] + read_section + text[read_end:]

    stale = "<!-- BS-CONTENT-20260811-08 CURRENT -->"
    current = "<!-- BS-CONTENT-20260811-09 CURRENT -->"
    if stale in text:
        a = text.index(stale)
        b = text.index(current, a)
        text = text[:a] + text[b:]
    write(path, text)


def repair_start_here() -> None:
    path = "[기획서]/00_프로젝트_허브/START_HERE.md"
    text = read(path)
    current_start = text.index("## 현재 R3–R7 설계 재개")
    owners_start = text.index("책임 원본:\n\n", current_start)
    owners_end = text.index("## 처음 읽을 순서", owners_start)
    owners = """책임 원본:

1. `docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md`
2. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
3. `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
4. `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
5. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
9. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
10. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`

"""
    text = text[:owners_start] + owners + text[owners_end:]

    order_start = text.index("## 처음 읽을 순서")
    order_end = text.index("## Task2 폐쇄 증거", order_start)
    order = """## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
9. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
10. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
11. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
12. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
13. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
14. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
15. `ACTIVE_CONTEXT.md`
16. `DEVELOPMENT_GATES.md`
17. `ROADMAP.md`
18. 실제 code/data/Scene/tests
19. Google Sheet `00`, `01`, `02`, `04`, `13`, `50` current rows

"""
    text = text[:order_start] + order + text[order_end:]

    d07_rule = "- `BS-CONTENT-20260811-07`은 Marek/Cassia 책임 경계를 보존하고 직접 전투·부대 지휘·baseline permadeath·숨은 총점·작품 단독 인과·임무 farming을 금지한다.\n"
    if "- `BS-CONTENT-20260811-08`은" not in text:
        text = text.replace(
            d07_rule,
            d07_rule
            + "- `BS-CONTENT-20260811-08`은 Ersa exhibition·Noble01 treatment-depth 책임을 보존하고 provenance fabrication·archive management·accession farming을 금지한다.\n"
            + "- `BS-CONTENT-20260811-09`은 Cassia arena-fit·Noble01 treatment-depth 책임을 보존하고 old/new UID history overwrite·legacy score 부활·gladiator-management drift·comeback farming을 금지한다.\n",
        )

    next_start = text.index("## 다음 작업")
    stale = "<!-- BS-CONTENT-20260811-08 CURRENT -->"
    next_end = text.index(stale, next_start) if stale in text else text.index("<!-- BS-CONTENT-20260811-09 CURRENT -->", next_start)
    next_section = """## 다음 작업

현재 연속 작업은 `BS-CONTENT-20260811-09`의 역사/current consumer 회귀, 적대 검토, exact-head CI, PR #154 병합, GitHub·Sheet same-ID 동기화와 postmerge readback까지다. 그 작업이 닫힌 뒤 다음 신규 R3–R7 Decision은 승인 카운터 `10/10`에서 별도 사용자 기획 승인을 받아 이어간다. 제품 코드·Scene·Resource·Task3는 별도 사용자 승인 전 시작하지 않는다.

"""
    text = text[:next_start] + next_section + text[next_end:]
    if stale in text:
        a = text.index(stale)
        b = text.index("<!-- BS-CONTENT-20260811-09 CURRENT -->", a)
        text = text[:a] + text[b:]
    write(path, text)


def repair_roadmap() -> None:
    path = "[기획서]/00_프로젝트_허브/ROADMAP.md"
    text = read(path)
    stale = "<!-- BS-CONTENT-20260811-07 CURRENT -->"
    if stale in text:
        a = text.index(stale)
        b = text.index("### 7/10 — `BS-CONTENT-20260811-07`", a)
        text = text[:a] + text[b:]
    write(path, text)


def repair_current_tests() -> None:
    replacements = {
        "R3_R7_APPROVAL_COUNTER: 8/10": "R3_R7_APPROVAL_COUNTER: 9/10",
        f"R3_R7_CURRENT_DECISION: {D08}": f"R3_R7_CURRENT_DECISION: {D09}",
        LOC08: LOC09,
        f"현재 Decision은 `{D08}`": f"현재 Decision은 `{D09}`",
        f"현재 연속 작업은 `{D08}`": f"현재 연속 작업은 `{D09}`",
        "현재 승인 카운터: `8/10`.": "현재 승인 카운터: `9/10`.",
        f"Decision: `{D08}`.": f"Decision: `{D09}`.",
        "현재 R3–R7 승인 카운터: `8/10`": "현재 R3–R7 승인 카운터: `9/10`",
    }
    paths = list((ROOT / "tests").glob("test_r3_*content.py")) + [
        ROOT / "tests/check_project_core_alignment_current.py",
        ROOT / "tests/test_auto_enhancement_cap_unlock.py",
        ROOT / "tests/test_hera_postmerge_closure_contract.py",
        ROOT / "tests/test_project_operating_system_audit_runner.py",
    ]
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            'self.assertEqual("8/10", registry.get("next_approval_counter"))',
            'self.assertEqual("9/10", registry.get("next_approval_counter"))',
        )
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    # Keep Decision08 explicitly required as history in core alignment.
    path = ROOT / "tests/check_project_core_alignment_current.py"
    text = path.read_text(encoding="utf-8")
    anchor = '            "BS-CONTENT-20260811-07",\n            "R3_R7_APPROVAL_COUNTER: 9/10",'
    if anchor in text:
        text = text.replace(
            anchor,
            '            "BS-CONTENT-20260811-07",\n            "BS-CONTENT-20260811-08",\n            "BS-CONTENT-20260811-09",\n            "R3_R7_APPROVAL_COUNTER: 9/10",',
        )
    path.write_text(text, encoding="utf-8")

    # Hera moves only its current R3 pointers.
    path = ROOT / "tests/test_hera_postmerge_closure_contract.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('R3_CURRENT_DECISION_ID = "BS-CONTENT-20260811-08"', 'R3_CURRENT_DECISION_ID = "BS-CONTENT-20260811-09"')
    text = text.replace('R3_CURRENT_RESUME_LOCATOR = "COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED"', 'R3_CURRENT_RESUME_LOCATOR = "GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED"')
    text = text.replace('R3_CURRENT_APPROVAL_COUNTER = "8/10"', 'R3_CURRENT_APPROVAL_COUNTER = "9/10"')
    path.write_text(text, encoding="utf-8")


def repair_operating_audit() -> None:
    path = ROOT / "tools/run_project_operating_system_audit.py"
    text = path.read_text(encoding="utf-8")
    if "R3_KYLE_CANON" not in text:
        text = text.replace(
            'R3_SEDRIC_CANON = "docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md"',
            'R3_SEDRIC_CANON = "docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md"\nR3_KYLE_CANON = "docs/planning/BLACKSMITH_R3_GLADIATOR_02_KYLE_VAREN_VETERAN_EQUIPMENT_CONTINUITY_CANON_2026.md"',
        )
    text = text.replace(
        'R3_CURRENT_DECISION = "BS-CONTENT-20260811-08"',
        'R3_EIGHTH_DECISION = "BS-CONTENT-20260811-08"\nR3_CURRENT_DECISION = "BS-CONTENT-20260811-09"',
    )
    text = text.replace('"next_approval_counter": "8/10"', '"next_approval_counter": "9/10"')
    text = text.replace(
        "        f'\"id\": \"{R3_SEVENTH_DECISION}\"',\n        f'\"id\": \"{R3_CURRENT_DECISION}\"',",
        "        f'\"id\": \"{R3_SEVENTH_DECISION}\"',\n        f'\"id\": \"{R3_EIGHTH_DECISION}\"',\n        f'\"id\": \"{R3_CURRENT_DECISION}\"',",
    )
    text = text.replace(
        "    assertions[R3_SEDRIC_CANON] = (\n        R3_CURRENT_DECISION,",
        "    assertions[R3_SEDRIC_CANON] = (\n        R3_EIGHTH_DECISION,",
    )
    if "assertions[R3_KYLE_CANON]" not in text:
        kyle = '''
    assertions[R3_KYLE_CANON] = (
        R3_CURRENT_DECISION,
        "GLADIATOR_02",
        "KYLE_VAREN",
        "VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION",
        "VETERAN_RETURN_STATE",
        "EQUIPMENT_CONTINUITY_STATE",
        "ITEM_UID_LINEAGE_STATE",
        "NO_UID_REWRITE",
        "NO_HISTORY_TRANSFER_TO_REPLACEMENT",
        "OLD_ITEM_HISTORY_PRESERVED",
        "NEW_ITEM_GETS_NEW_UID",
        "CASSIA_ARENA_FIT_RESPONSIBILITY_PRESERVED",
        "NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED",
        "LEGACY_GLADIATOR_KYLE_FIXTURE_NON_AUTHORITATIVE",
        "NO_FIXED_IRON_SWORD_CANON",
        "NO_LEGACY_ARENA_SCORE_FORMULA_CANON",
        "NO_DIRECT_ARENA_COMBAT",
        "NO_GLADIATOR_ROSTER_OR_GUILD_MANAGEMENT",
        "NO_TRAINING_OR_INJURY_MANAGEMENT",
        "P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED",
        "제품 구현: `BLOCKED`",
        "Task3 구현: `NOT_APPROVED`",
    )
'''
        text = text.replace('\n    gates_path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"', kyle + '\n    gates_path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"')
    text = text.replace('"R3_R7_APPROVAL_COUNTER: 8/10"', '"R3_R7_APPROVAL_COUNTER: 9/10"')
    text = text.replace(
        "            R3_SEVENTH_DECISION,\n            R3_CURRENT_DECISION,",
        "            R3_SEVENTH_DECISION,\n            R3_EIGHTH_DECISION,\n            R3_CURRENT_DECISION,",
    )
    text = text.replace('            "COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED",', '            "GLADIATOR_02_KYLE_VETERAN_CONTINUITY_APPROVED",')
    text = text.replace('"현재 R3–R7 승인 카운터: `8/10`"', '"현재 R3–R7 승인 카운터: `9/10`"')
    text = text.replace(
        "(R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON, R3_NOBLE_CANON, R3_LIANA_CANON, R3_SEDRIC_CANON)",
        "(R3_REGISTRY, R3_NADIA_CANON, R3_TOREN_CANON, R3_MAREK_CANON, R3_ERSA_CANON, R3_CASSIA_CANON, R3_NOBLE_CANON, R3_LIANA_CANON, R3_SEDRIC_CANON, R3_KYLE_CANON)",
    )
    path.write_text(text, encoding="utf-8")

    test_path = ROOT / "tests/test_project_operating_system_audit_runner.py"
    test = test_path.read_text(encoding="utf-8")
    if "runner.R3_KYLE_CANON" not in test:
        test = test.replace(
            "        sedric = audit.REQUIRED_ASSERTIONS[runner.R3_SEDRIC_CANON]\n",
            "        sedric = audit.REQUIRED_ASSERTIONS[runner.R3_SEDRIC_CANON]\n        kyle = audit.REQUIRED_ASSERTIONS[runner.R3_KYLE_CANON]\n",
        )
        test = test.replace(
            "            '\"id\": \"BS-CONTENT-20260811-08\"',\n        ):",
            "            '\"id\": \"BS-CONTENT-20260811-08\"',\n            '\"id\": \"BS-CONTENT-20260811-09\"',\n        ):",
        )
        test = test.replace(
            '        self.assertIn("NO_DOCUMENT_FABRICATION", sedric)\n',
            '        self.assertIn("NO_DOCUMENT_FABRICATION", sedric)\n'
            '        self.assertIn("BS-CONTENT-20260811-09", kyle)\n'
            '        self.assertIn("GLADIATOR_02", kyle)\n'
            '        self.assertIn("KYLE_VAREN", kyle)\n'
            '        self.assertIn("VETERAN_COMEBACK_EQUIPMENT_CONTINUITY_AND_SUCCESSION", kyle)\n'
            '        self.assertIn("VETERAN_RETURN_STATE", kyle)\n'
            '        self.assertIn("EQUIPMENT_CONTINUITY_STATE", kyle)\n'
            '        self.assertIn("ITEM_UID_LINEAGE_STATE", kyle)\n'
            '        self.assertIn("OLD_ITEM_HISTORY_PRESERVED", kyle)\n'
            '        self.assertIn("NEW_ITEM_GETS_NEW_UID", kyle)\n'
            '        self.assertIn("NO_LEGACY_ARENA_SCORE_FORMULA_CANON", kyle)\n',
        )
        test = test.replace(
            "            runner.R3_SEDRIC_CANON,\n        ):",
            "            runner.R3_SEDRIC_CANON,\n            runner.R3_KYLE_CANON,\n        ):",
        )
        test = test.replace(
            '                "BS-CONTENT-20260811-07",\n            ):',
            '                "BS-CONTENT-20260811-07",\n                "BS-CONTENT-20260811-08",\n                "BS-CONTENT-20260811-09",\n            ):',
        )
    test_path.write_text(test, encoding="utf-8")


def verify_structure() -> None:
    active = read("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md")
    start = read("[기획서]/00_프로젝트_허브/START_HERE.md")
    roadmap = read("[기획서]/00_프로젝트_허브/ROADMAP.md")
    for label, text in (("active", active), ("start", start), ("roadmap", roadmap)):
        if f"R3_R7_CURRENT_DECISION: {D09}" not in text:
            raise RuntimeError(f"{label}: D09 current missing")
    if "<!-- BS-CONTENT-20260811-08 CURRENT -->" in active or "<!-- BS-CONTENT-20260811-08 CURRENT -->" in start:
        raise RuntimeError("stale D08 current mirror remains")
    if "<!-- BS-CONTENT-20260811-07 CURRENT -->" in roadmap:
        raise RuntimeError("stale D07 current mirror remains")
    if "16. Google Sheet" not in active or "19. Google Sheet" not in start:
        raise RuntimeError("read-order reconstruction failed")
    audit = read("tools/run_project_operating_system_audit.py")
    for token in ("R3_EIGHTH_DECISION", "R3_CURRENT_DECISION", "R3_KYLE_CANON", '"next_approval_counter": "9/10"'):
        if token not in audit:
            raise RuntimeError(f"audit current/history split missing {token}")


def main() -> None:
    repair_active()
    repair_start_here()
    repair_roadmap()
    repair_current_tests()
    repair_operating_audit()
    verify_structure()
    Path(__file__).unlink()


if __name__ == "__main__":
    main()
