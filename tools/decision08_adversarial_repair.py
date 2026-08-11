from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D08 = "BS-CONTENT-20260811-08"
LOC8 = "COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED"


def path(rel: str) -> Path:
    return ROOT / rel


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing {label}: {old!r}")
    return text.replace(old, new, 1)


# START_HERE: current header and next-work paragraph must agree with D08.
p = path("[기획서]/00_프로젝트_허브/START_HERE.md")
text = p.read_text(encoding="utf-8")
text = replace_required(
    text,
    "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
    "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
    "START header",
)
old_next = "현재 연속 작업은 `BS-CONTENT-20260811-07`의 회귀 검증, 적대 검토, exact-head CI, PR 병합, GitHub·Sheet same-ID 동기화와 postmerge readback까지다. 그 작업이 닫힌 뒤 다음 신규 R3–R7 Decision은 승인 카운터 `8/10`에서 사용자 기획 승인을 받아 이어간다. 제품 코드·Scene·Resource·Task3는 별도 사용자 승인 전 시작하지 않는다."
new_next = "현재 연속 작업은 `BS-CONTENT-20260811-08`의 회귀 검증, 적대 검토, exact-head CI, PR 병합, GitHub·Sheet same-ID 동기화와 postmerge readback까지다. 그 작업이 닫힌 뒤 다음 신규 R3–R7 Decision은 승인 카운터 `9/10`에서 사용자 기획 승인을 받아 이어간다. 제품 코드·Scene·Resource·Task3는 별도 사용자 승인 전 시작하지 않는다."
text = replace_required(text, old_next, new_next, "START next-work")
p.write_text(text, encoding="utf-8")

# ACTIVE_CONTEXT: replace stale D07 current tail with D08 current tail.
p = path("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md")
text = p.read_text(encoding="utf-8")
marker = "<!-- BS-CONTENT-20260811-07 CURRENT -->"
if marker not in text:
    raise RuntimeError("ACTIVE stale current marker missing")
text = text.split(marker, 1)[0].rstrip() + "\n\n" + r'''<!-- BS-CONTENT-20260811-08 CURRENT -->
## R3–R7 current 8/10 — Sedric Collector02

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 8/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08
R3_R7_RESUME_LOCATOR: COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

Nadia 1/10, Toren 2/10, Marek 3/10, Ersa 4/10, Cassia 5/10, Noble01 6/10, Liana 7/10은 승인 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-08`이다.

`COLLECTOR_02 / SEDRIC_VAEL / ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY`는 공개된 archival purpose와 실제 작품 UID의 provenance·custody·생애 근거를 비교해 한 작품을 인계한다. accession은 비직접 사건이며 `ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE`를 분리해 돌려준다.

Ersa의 exhibition evidence/thesis, Noble01의 physical treatment depth, Liana의 commander mission-fit 책임은 각각 승인 이력으로 유지한다. 같은 UID, anti-score, anti-fabrication, anti-management, anti-farming 경계를 보존하며 제품 구현과 Task3는 계속 차단한다.
'''
p.write_text(text, encoding="utf-8")

# ROADMAP: current header must be D08 and Liana 7/10 must become explicit history before 8/10.
p = path("[기획서]/00_프로젝트_허브/ROADMAP.md")
text = p.read_text(encoding="utf-8")
text = replace_required(
    text,
    "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
    "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
    "ROADMAP header",
)
liana = r'''### 7/10 — `BS-CONTENT-20260811-07`

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

'''
anchor = "### 8/10 — `BS-CONTENT-20260811-08`"
if "### 7/10 — `BS-CONTENT-20260811-07`" not in text:
    if anchor not in text:
        raise RuntimeError("ROADMAP Decision08 anchor missing")
    text = text.replace(anchor, liana + anchor, 1)
p.write_text(text, encoding="utf-8")

# DEVELOPMENT_GATES: current header must be D08.
p = path("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md")
text = p.read_text(encoding="utf-8")
text = replace_required(
    text,
    "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**",
    "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**",
    "GATES header",
)
p.write_text(text, encoding="utf-8")

# Guard against the validated stale-current patterns.
checks = {
    "[기획서]/00_프로젝트_허브/START_HERE.md": [
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
        "다음 신규 R3–R7 Decision은 승인 카운터 `9/10`",
    ],
    "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": [
        "<!-- BS-CONTENT-20260811-08 CURRENT -->",
        "## R3–R7 current 8/10 — Sedric Collector02",
    ],
    "[기획서]/00_프로젝트_허브/ROADMAP.md": [
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY**",
        "### 7/10 — `BS-CONTENT-20260811-07`",
        "### 8/10 — `BS-CONTENT-20260811-08`",
    ],
    "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": [
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**",
    ],
}
for rel, tokens in checks.items():
    body = path(rel).read_text(encoding="utf-8")
    for token in tokens:
        if token not in body:
            raise RuntimeError(f"{rel} missing repair token: {token}")

print("Decision08 adversarial current-router repair complete")
