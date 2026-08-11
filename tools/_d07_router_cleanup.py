from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected 1 match, got {count}")
    return text.replace(old, new, 1)


def clean_active() -> None:
    path = "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
    text = read(path)
    text = replace_once(
        text,
        "- `BS-CONTENT-20260811-06`은 의미 있는 과거 생애 기록을 지우거나 복원/의식 반복으로 예술성·Chronicle을 자동 성장시키지 않는다.\n- 같은 UID의 작품 생애를 유지한다.",
        "- `BS-CONTENT-20260811-06`은 의미 있는 과거 생애 기록을 지우거나 복원/의식 반복으로 예술성·Chronicle을 자동 성장시키지 않는다.\n- `BS-CONTENT-20260811-07`은 Marek의 소량 표준화와 Cassia의 arena contribution 책임을 침범하지 않는다.\n- `BS-CONTENT-20260811-07`은 직접 전술전투·부대 이동/대형·실시간 병참·사상자 micromanagement·baseline Liana permadeath를 추가하지 않는다.\n- `BS-CONTENT-20260811-07`은 command/hero/leadership/mission-fit 총점, 최고 방어/강화 자동 정답, 작품 단독 인과, 임무 반복 Artistry/Chronicle 파밍을 만들지 않는다.\n- 같은 UID의 작품 생애를 유지한다.",
        "active D07 protections",
    )
    text = replace_once(
        text,
        "BS-CONTENT-20260811-06 / R3_R7_6_OF_10\nBS-OPS-20260811-02 / PRE_WORK_RESEARCH_GATE",
        "BS-CONTENT-20260811-06 / R3_R7_6_OF_10\nBS-CONTENT-20260811-07 / R3_R7_7_OF_10\nBS-OPS-20260811-02 / PRE_WORK_RESEARCH_GATE",
        "active D07 index",
    )

    start = text.index("## 다음 실행 순서")
    end = text.index("## 현재 프로젝트 작업지시문 바인딩", start)
    replacement = """## 다음 실행 순서

1. `BS-CONTENT-20260811-07`의 RED→GREEN 회귀, 적대 검토, exact-head CI, GitHub·Sheet 동일 Decision ID 동기화를 끝낸다.
2. Marek multi-UID 표준화와 Liana single-commander duty-fit이 분리되는지, 임무·귀환·same-UID field legacy 3축이 유지되는지 검증한다.
3. 새 제품 Task는 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED`와 `TASK3_IMPLEMENTATION: NOT_APPROVED`가 별도 사용자 승인으로 해소되기 전 시작하지 않는다.
4. Decision07 merge·Sheet readback 뒤 다음 신규 R3–R7 Decision은 `8/10` 사용자 기획 승인 Gate에서 이어간다.

## 먼저 읽을 파일

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
9. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
10. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
11. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
12. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
13. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
14. Google Sheet `00_프로젝트_허브`, `01_작업순서`, `02_현재_확정결정`, `04_누락_충돌_감사`, `13_주요인물`, `50_메인콘텐츠`

"""
    text = text[:start] + replacement + text[end:]

    marker = "<!-- BS-CONTENT-20260811-04 CURRENT -->"
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

`SOLDIER_02 / LIANA_BERG / FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY`는 공개된 임무 책임·위험·필요 장비 역할과 실제 작품 UID 증거를 비교해 한 작품을 인계한다. 전선 임무는 비직접 사건이며 `MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE`를 분리해 돌려준다.

Marek의 multi-UID 소량 표준화, Cassia의 arena contribution, Noble01의 heirloom restoration 책임은 각각 유지한다. 제품 구현과 Task3는 계속 차단한다.
"""
    if marker not in text:
        raise RuntimeError("active stale CURRENT marker missing")
    text = text[: text.index(marker)] + tail
    write(path, text)


def clean_start_here() -> None:
    path = "[기획서]/00_프로젝트_허브/START_HERE.md"
    text = read(path)
    start = text.index("## 처음 읽을 순서")
    end = text.index("## Task2 폐쇄 증거", start)
    replacement = """## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
9. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
10. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
11. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
12. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
13. `ACTIVE_CONTEXT.md`
14. `DEVELOPMENT_GATES.md`
15. `ROADMAP.md`
16. 실제 code/data/Scene/tests
17. Google Sheet `00`, `01`, `02`, `04`, `13`, `50` current rows

"""
    text = text[:start] + replacement + text[end:]
    text = replace_once(
        text,
        "- `BS-CONTENT-20260811-05`는 같은 작품 UID와 legacy POC 비권위 경계를 유지한다.\n- GUT 9.7.1은 GDScript test authority다.",
        "- `BS-CONTENT-20260811-05`는 같은 작품 UID와 legacy POC 비권위 경계를 유지한다.\n- `BS-CONTENT-20260811-06`은 same-UID 가보 생애와 절제된 복원 판단을 유지하고 history erasure·복원 farming을 금지한다.\n- `BS-CONTENT-20260811-07`은 Marek/Cassia 책임 경계를 보존하고 직접 전투·부대 지휘·baseline permadeath·숨은 총점·작품 단독 인과·임무 farming을 금지한다.\n- GUT 9.7.1은 GDScript test authority다.",
        "start D06 D07 protections",
    )
    marker = "## 다음 작업"
    tail = """## 다음 작업

현재 연속 작업은 `BS-CONTENT-20260811-07`의 회귀 검증, 적대 검토, exact-head CI, PR 병합, GitHub·Sheet same-ID 동기화와 postmerge readback까지다. 그 작업이 닫힌 뒤 다음 신규 R3–R7 Decision은 승인 카운터 `8/10`에서 사용자 기획 승인을 받아 이어간다. 제품 코드·Scene·Resource·Task3는 별도 사용자 승인 전 시작하지 않는다.

<!-- BS-CONTENT-20260811-07 CURRENT -->
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

`SOLDIER_02 / LIANA_BERG / FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY`는 한 명의 지휘관, 한 번의 공개 임무 책임, 한 작품 UID의 handoff와 결과를 소유한다. `MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE`는 서로 분리한다.

현재 연속 작업은 `BS-CONTENT-20260811-07`이다.
"""
    if marker not in text:
        raise RuntimeError("start next-work marker missing")
    text = text[: text.index(marker)] + tail
    write(path, text)


if __name__ == "__main__":
    clean_active()
    clean_start_here()
