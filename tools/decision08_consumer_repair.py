from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D07 = "BS-CONTENT-20260811-07"
D08 = "BS-CONTENT-20260811-08"


def load(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def save(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")


def required_replace(text: str, old: str, new: str, label: str, count: int = 1) -> str:
    if old not in text:
        raise RuntimeError(f"missing {label}: {old!r}")
    return text.replace(old, new, count)


# Prior content tests preserve their own historical contracts but must consume D08 as moving current.
for rel in (
    "tests/test_r3_collector_01_ersa_content.py",
    "tests/test_r3_gladiator_01_cassia_content.py",
    "tests/test_r3_noble_01_heirloom_succession_content.py",
):
    text = load(rel)
    text = text.replace("while_liana_is_current", "while_sedric_is_current")
    text = text.replace(f"현재 Decision은 `{D07}`", f"현재 Decision은 `{D08}`")
    text = text.replace(f"현재 연속 작업은 `{D07}`", f"현재 연속 작업은 `{D08}`")
    text = text.replace("현재 승인 카운터: `7/10`.", "현재 승인 카운터: `8/10`.")
    text = text.replace(f"Decision: `{D07}`.", f"Decision: `{D08}`.")
    save(rel, text)

# Active Context current header, next-execution routing, and first-read order.
rel = "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
text = load(rel)
text = required_replace(
    text,
    "> **R3_R7_DESIGN_ACTIVE / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
    "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
    "Active header",
)
start = text.index("## 다음 실행 순서")
end = text.index("## 먼저 읽을 파일", start)
next_section = '''## 다음 실행 순서

1. `BS-CONTENT-20260811-08`의 RED→GREEN 회귀, 적대 검토, exact-head CI, GitHub·Sheet 동일 Decision ID 동기화를 끝낸다.
2. Sedric archival accession이 Ersa exhibition과 Noble01 treatment-depth를 침범하지 않고, same-UID provenance/custody 3축과 anti-score·anti-fabrication·anti-management·anti-farming 경계를 유지하는지 검증한다.
3. 새 제품 Task는 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED`와 `TASK3_IMPLEMENTATION: NOT_APPROVED`가 별도 사용자 승인으로 해소되기 전 시작하지 않는다.
4. Decision08 merge·Sheet readback 뒤 다음 신규 R3–R7 Decision은 `9/10` 사용자 기획 승인 Gate에서 이어간다.

'''
text = text[:start] + next_section + text[end:]
start = text.index("## 먼저 읽을 파일")
end = text.index("## 현재 프로젝트 작업지시문 바인딩", start)
read_section = '''## 먼저 읽을 파일

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
9. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
10. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
11. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
12. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`
13. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
14. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
15. Google Sheet `00_프로젝트_허브`, `01_작업순서`, `02_현재_확정결정`, `04_누락_충돌_감사`, `13_주요인물`, `50_메인콘텐츠`

'''
text = text[:start] + read_section + text[end:]
save(rel, text)

# Roadmap must preserve the contiguous history 6/10 -> 7/10 -> 8/10.
rel = "[기획서]/00_프로젝트_허브/ROADMAP.md"
text = load(rel)
d06_tail = "- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`\n\n### 8/10 — `BS-CONTENT-20260811-08`"
d07 = '''- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`

### 7/10 — `BS-CONTENT-20260811-07`

```text
SOLDIER_02 / LIANA_BERG
FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY
MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE
```

목표:

- 공개된 지휘 책임·임무 위험·필요 장비 역할과 실제 작품 UID 근거를 비교해 한 작품을 맡긴다.
- Marek의 multi-UID 소량 표준화와 Cassia의 arena contribution 책임을 보존한다.
- 직접 전술전투·부대 이동/대형·실시간 병참·사상자 micromanagement를 추가하지 않는다.
- command/hero/leadership/mission-fit 총점, 최고 방어/강화 자동정답, 작품 단독 인과를 만들지 않는다.
- baseline Liana permadeath/replacement loop와 임무 반복 Artistry/Chronicle farming을 추가하지 않는다.
- 같은 UID를 인계·현장 결과·귀환/회수까지 보존한다.

책임 원본:

- `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`

### 8/10 — `BS-CONTENT-20260811-08`'''
text = required_replace(text, d06_tail, d07, "Roadmap 7/10 insertion")
save(rel, text)

# Strong guards for current/history separation.
active = load("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md")
roadmap = load("[기획서]/00_프로젝트_허브/ROADMAP.md")
if "1. `BS-CONTENT-20260811-07`의 RED→GREEN" in active:
    raise RuntimeError("Active next execution still routes to Decision07")
if "Decision07 merge·Sheet readback 뒤" in active:
    raise RuntimeError("Active next gate still routes from Decision07")
for token in (
    "BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED",
    "1. `BS-CONTENT-20260811-08`의 RED→GREEN",
    "Decision08 merge·Sheet readback 뒤 다음 신규 R3–R7 Decision은 `9/10`",
    "BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md",
):
    if token not in active:
        raise RuntimeError(f"Active missing {token}")
pos6 = roadmap.index("### 6/10 — `BS-CONTENT-20260811-06`")
pos7 = roadmap.index("### 7/10 — `BS-CONTENT-20260811-07`")
pos8 = roadmap.index("### 8/10 — `BS-CONTENT-20260811-08`")
if not pos6 < pos7 < pos8:
    raise RuntimeError("Roadmap Decision history is not 6 -> 7 -> 8")

print("Decision08 stale consumer repair complete")
