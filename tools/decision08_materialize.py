from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D07 = "BS-CONTENT-20260811-07"
D08 = "BS-CONTENT-20260811-08"
LOC7 = "SOLDIER_02_LIANA_MISSION_FIT_APPROVED"
LOC8 = "COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED"
CANON_PATH = ROOT / "docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing expected token for {label}: {old!r}")
    return text.replace(old, new)


def replace_section(text: str, start: str, end: str, replacement: str, label: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        raise RuntimeError(f"cannot locate section {label}")
    return pattern.sub(replacement.rstrip() + "\n\n" + end, text, count=1)


CANON = r'''# Blacksmith R3 Collector 02 — Sedric Vael Archival Accession Canon 2026

Decision: `BS-CONTENT-20260811-08`.

```text
COLLECTOR_02 / SEDRIC_VAEL
ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
ARCHIVAL_STEWARDSHIP_THROUGH_EXPLAINABLE_PROVENANCE_AND_CUSTODY
```

상태: `USER_APPROVED / R3_R7_8_OF_10 / PLANNING_ONLY`.

제품 구현: `BLOCKED`.
Task3 구현: `NOT_APPROVED`.
사람 플레이테스트: `NOT_RUN`.
Android 실기기: `NOT_RUN`.
접근성: `NOT_RUN`.

## 1. 목적

기존 `SEDRIC_VAEL`을 두 번째 Collector-family 상세 고객으로 재사용한다. 플레이어는 가장 강하거나 가장 오래된 작품을 자동 선택하는 대신, 공개된 장기 보관 목적에 맞춰 **실제 작품 UID 한 점이 자기 역사와 custody를 충분히 설명할 수 있는지** 판단한다.

플레이어 역할은 `BLACKSMITH_ITEM_AND_HISTORY_DECISION_MAKER_NOT_ARCHIVE_MANAGER`다. 기록 보관소·박물관 운영자가 아니다.

## 2. 기존 책임과 분리

```text
ERSA_ROEN / COLLECTOR_01 / EXHIBITION_EVIDENCE_AND_PROVENANCE
= 공개 전시 의도에 어떤 실제 제작·생애 증거를 강조할지 판단

SEDRIC_VAEL / COLLECTOR_02 / ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
= 같은 UID의 실제 출처·custody 근거가 장기 보관 인계를 설명할 수 있는지 판단

CEREMONIAL_NOBLE / NOBLE_01 / HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY
= 같은 가보 UID에 물리적으로 어디까지 수리·복원·재작업할지 판단
```

보호 토큰:

- `ERSA_EXHIBITION_RESPONSIBILITY_PRESERVED`
- `NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED`
- `EXISTING_SEDRIC_VAEL_CUSTOMER_REUSED`

Sedric은 전시 reception/thesis, 복원 개입 깊이, storage/visitor/staff/loan logistics를 소유하지 않는다.

## 3. 플레이 흐름

```text
SEDRIC_VAEL 방문
→ archival category / keeping purpose 공개
→ 실제 작품 UID 후보 확인
→ 각 후보에 실제로 기록된 provenance·custody·생애 근거 확인
→ 작품 UID 한 점 선택
→ SAME_ITEM_UID_PRESERVED 상태로 인계
→ archival accession은 비직접 고객/세계 사건으로 해결
→ ARCHIVE_ACCESSION_STATE
 + PROVENANCE_DOCUMENTATION_STATE
 + ITEM_UID_CUSTODY_LEGACY_STATE
→ 실제 원인 2~4개 + 주 후속 행동 1개
```

플레이어는 문서를 타이핑하거나 출처를 창작하지 않고, 선반·수장고·방문객·직원·보존환경·대여 물류를 직접 운영하지 않는다.

## 4. 사용할 수 있는 근거

현재 작품/프로젝트에 이미 존재하고 이번 보관 목적과 실제 관련된 근거만 소비한다.

- item UID와 작품 범주
- 목적에 관련될 때만 재료 정체성
- 실제 제작 provenance
- 기록된 소유·custody 전환
- 해당 UID에 실제 연결된 손상·수리·복원·회수·전시·임무·여정·투기장·계승 등 승인 생애 이력
- 기존 Chronicle/provenance 기록
- 공개 목적상 관련될 때만 제작 등급/Artistry 등 실제 제작 근거
- 기존 eligibility/fit gate

기록되지 않은 소유·출처는 사실로 추론하지 않는다. 누락은 누락으로 보여주고 유리한 점수로 메우지 않는다.

## 5. 선택 구조

inventory가 허용하면 서로 다른 강점을 가진 둘 이상의 방어 가능한 선택을 만든다.

예:

- 비교적 새 작품이지만 provenance/custody가 매우 연속적인 경우
- 오래 사용됐고 중요한 생애가 있지만 소유 기록 일부가 비어 있는 경우
- Artistry는 높지 않지만 제작·회수·소유 전환이 명료한 경우
- 역사적 의미는 강하지만 unresolved custody gap이 있는 경우

다음 하나로 자동 정답을 만들지 않는다.

- 최고 Artistry
- 가장 오래된 작품
- 가장 많은 Chronicle 사건
- 최고 강화
- 단일 숨은 aggregate score

## 6. 결과 3축

### `ARCHIVE_ACCESSION_STATE`

현재 공개된 archival request가 실제 근거에 따라 accepted / conditional / deferred / declined 계열로 귀결되는 상태다. 전체 품질 총점이 아니다.

### `PROVENANCE_DOCUMENTATION_STATE`

선택한 UID의 실제 origin/custody evidence가 공개 목적을 얼마나 설명하는지 나타낸다. 누락·모순은 이유로 노출하며 하나의 총점으로 숨기지 않는다.

### `ITEM_UID_CUSTODY_LEGACY_STATE`

archival handoff 뒤 **같은 UID**의 custody/public-record 생애가 어떻게 바뀌었는지 나타낸다.

세 축은 서로 다를 수 있다. accession 성공이 완전 복원을 뜻하지 않고, documentation이 강해도 다른 작품이 특정 목적에 더 적합할 수 있다.

## 7. 후속 환류

실제 기존/후속 owner가 지원할 때만 다음 이유로 연결한다.

- 현 상태 보존
- 기존 treatment owner를 통한 수리·복원
- 승인된 새 근거가 생긴 뒤 재평가
- 후속 승인된 loan/exhibition hook
- farming이 아닌 research/appraisal hook
- 다음 archival request용 다른 작품 선택·신작

Decision08 자체가 이 미래 시스템을 제품 구현하지 않는다.

## 8. 같은 UID와 성장 경계

`SAME_ITEM_UID_PRESERVED`는 필수다.

- accession/review/custody transfer가 item clone 또는 새 replacement UID를 만들지 않는다.
- archive에 들어갔다는 이유만으로 Artistry가 증가하지 않는다.
- acceptance/storage/review/display 자체만으로 `CHRONICLE_AFFIX`를 자동 지급하지 않는다.

## 9. 명시적 금지선

- `NO_AUTHENTICITY_TOTAL_SCORE`
- `NO_PROVENANCE_COMPLETENESS_SCORE`
- `NO_ARCHIVE_PRESTIGE_SCORE`
- `NO_RARITY_SCORE_FOR_ARCHIVAL_ACCESSION`
- `NO_HIGHEST_ARTISTRY_ALWAYS_BEST`
- `NO_OLDEST_ITEM_ALWAYS_BEST`
- `NO_MOST_CHRONICLE_EVENTS_ALWAYS_BEST`
- `NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`
- `NO_DOCUMENT_FABRICATION`
- `NO_UNRECORDED_HISTORY_AUTOFILL`
- `NO_ACCESSION_COUNT_ARTISTRY_GROWTH`
- `NO_APPRAISAL_OR_REVIEW_COUNT_ARTISTRY_GROWTH`
- `NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_ARCHIVING`
- `NO_ARCHIVE_STORAGE_MANAGEMENT`
- `NO_MUSEUM_MANAGEMENT_SIM`
- `NO_VISITOR_MANAGEMENT`
- `NO_STAFF_OR_SHELF_MANAGEMENT`
- `NO_PRESERVATION_ENVIRONMENT_SIMULATION`
- `NO_LOAN_LOGISTICS_MANAGEMENT`

## 10. 정확 값과 taxonomy

정확 archive-purpose 분포, acceptance threshold, 기간, 경제 보상, 관계 보상, 후속 timing, 결과 분포는 모두 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

Decision08은 Sheet의 `BS-CT-06 / 고객 4유형×이름 고객 8명` 의미를 재정의하지 않는다. Sedric이 기존 8명 중 한 명이라는 사실만 재사용하며, `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 계속 열린다.

## 11. 기대 결과

Ersa는 **“무엇을 공개적으로 보여줄 것인가”**, Sedric은 **“이 작품의 실제 역사를 장기 보관 대상으로 책임지고 받아들일 수 있는가”**를 묻는다. 작품 가치는 archive score가 아니라 같은 UID에 실제 남은 출처·소유·생애를 플레이어가 읽고 방어할 수 있기 때문에 커진다.
'''


def materialize_registry() -> None:
    path = ROOT / "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("next_approval_counter") != "7/10":
        raise RuntimeError(f"unexpected pre-materialization R3 counter: {data.get('next_approval_counter')}")
    decisions = data.get("current_decisions")
    if not isinstance(decisions, list):
        raise RuntimeError("current_decisions must be a list")
    ids = [item.get("id") for item in decisions if isinstance(item, dict)]
    if D08 in ids:
        raise RuntimeError("Decision08 already exists before materialization")
    if D07 not in ids:
        raise RuntimeError("Decision07 history missing")
    decisions.append(
        {
            "id": D08,
            "title": "수집가 02 세드릭 바엘 기록 보관 인계·출처·custody 콘텐츠",
            "status": "USER_APPROVED_R3_R7_8_OF_10",
            "canon": "docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md",
            "refines": ["BS-CONTENT-20260804-01", "BS-CONTENT-20260804-02"],
            "depends_on": [
                "BS-CUSTOMER-20260803-02",
                "BS-CUSTOMER-20260805-01",
                "BS-UX-20260805-01",
                "BS-CRAFT-20260804-06",
                "BS-CRAFT-20260805-01",
                "BS-CRAFT-20260805-02",
                "BS-CONTENT-20260811-04",
                "BS-CONTENT-20260811-06",
                D07,
            ],
            "contract": {
                "content_id": "COLLECTOR_02",
                "customer_id": "SEDRIC_VAEL",
                "customer_archetype": "COLLECTOR",
                "activity_family": "ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY",
                "content_goal": "ARCHIVAL_STEWARDSHIP_THROUGH_EXPLAINABLE_PROVENANCE_AND_CUSTODY",
                "player_role": "BLACKSMITH_ITEM_AND_HISTORY_DECISION_MAKER_NOT_ARCHIVE_MANAGER",
                "existing_sedric_vael_customer_reused": True,
                "same_item_uid_preserved": True,
                "ersa_exhibition_responsibility_preserved": True,
                "noble01_treatment_depth_responsibility_preserved": True,
                "opaque_authenticity_provenance_or_archive_score": False,
                "oldest_item_always_best": False,
                "highest_artistry_always_best": False,
                "most_chronicle_events_always_best": False,
                "highest_enhancement_always_best": False,
                "document_fabrication": False,
                "unrecorded_history_autofill": False,
                "accession_count_artistry_growth": False,
                "appraisal_or_review_count_artistry_growth": False,
                "automatic_chronicle_affix_from_archiving": False,
                "archive_storage_management": False,
                "museum_management_sim": False,
                "visitor_management": False,
                "staff_or_shelf_management": False,
                "preservation_environment_simulation": False,
                "loan_logistics_management": False,
                "result_axes": [
                    "ARCHIVE_ACCESSION_STATE",
                    "PROVENANCE_DOCUMENTATION_STATE",
                    "ITEM_UID_CUSTODY_LEGACY_STATE",
                ],
                "feedback": "THREE_STATE_SUMMARY_TWO_TO_FOUR_ACTUAL_REASONS_ONE_PRIMARY_NEXT_ACTION",
                "exact_values": "NON_CANONICAL_BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
                "taxonomy_ambiguity": "P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED",
                "product_implementation": "BLOCKED",
                "task3_implementation": "NOT_APPROVED",
                "human_playtest": "NOT_RUN",
                "android_device": "NOT_RUN",
                "accessibility": "NOT_RUN",
                "planning_source_main": "7005a939e003f7248e7d2546c4266bb5d144f90a",
            },
        }
    )
    data["next_approval_counter"] = "8/10"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def materialize_current_decisions() -> None:
    path = "CURRENT_CONFIRMED_DECISIONS.md"
    text = read(path)
    text = must_replace(
        text,
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / R3_R7_7_OF_10 / PLANNING_ONLY**",
        "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-08 / R3_R7_8_OF_10 / PLANNING_ONLY**",
        "current decisions header",
    )
    text = must_replace(text, "R3_R7_APPROVAL_COUNTER: 7/10", "R3_R7_APPROVAL_COUNTER: 8/10", "current counter")
    text = must_replace(text, f"R3_R7_CURRENT_DECISION: {D07}", f"R3_R7_CURRENT_DECISION: {D08}", "current decision")
    anchor = "- `BS-CRAFT-20260804-04`:"
    if anchor not in text:
        raise RuntimeError("cannot find Decision08 insertion anchor in CURRENT_CONFIRMED_DECISIONS.md")
    bullet = (
        "- `BS-CONTENT-20260811-08`: `COLLECTOR_02` 세드릭 바엘 기록 보관 accession·출처·custody 콘텐츠. "
        "공개된 장기 보관 목적과 실제 작품 UID의 제작·소유·custody·생애 근거를 읽어 같은 UID 한 점을 인계한다. "
        "결과는 `ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE`로 분리한다. "
        "Ersa의 공개 전시 책임과 Noble01의 물리적 처치 깊이 책임을 보존하며, 진품성/출처/위신 총점, 최고 Artistry·가장 오래된 작품·최고 강화 자동정답, 기록 조작, archive/museum 관리, accession 반복 Artistry/Chronicle farming을 만들지 않는다. "
        "`P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 유지한다. — `USER_APPROVED / R3_R7_8_OF_10 / PLANNING_ONLY`\n"
    )
    text = text.replace(anchor, bullet + anchor, 1)
    write(path, text)


def common_current_replacements(text: str) -> str:
    text = text.replace("R3_R7_APPROVAL_COUNTER: 7/10", "R3_R7_APPROVAL_COUNTER: 8/10")
    text = text.replace(f"R3_R7_CURRENT_DECISION: {D07}", f"R3_R7_CURRENT_DECISION: {D08}")
    text = text.replace(LOC7, LOC8)
    return text


def materialize_active() -> None:
    path = "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
    text = common_current_replacements(read(path))
    text = text.replace("현재 R3–R7 승인 카운터: `7/10`", "현재 R3–R7 승인 카운터: `8/10`")
    text = text.replace("Blacksmith current main observed at Decision 07 start: `27365bc774508bea6a1a19221fb2a3dc2d093be5`", "Blacksmith current main observed at Decision 08 start: `7005a939e003f7248e7d2546c4266bb5d144f90a`")
    section = '''## 현재 R3–R7 기획 재개 상태

`BS-CONTENT-20260811-01`~`07`은 승인 완료 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-08`이다.

```text
COLLECTOR_02 / SEDRIC_VAEL
→ 기존 수집가 추가 고객·귀족 기록 보관가를 두 번째 Collector-family 상세 콘텐츠로 승격
→ ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
→ archival category / keeping purpose 공개
→ 실제 작품 UID와 기록된 provenance·custody·생애 근거 비교
→ 한 작품 UID 선택·같은 UID 인계
→ accession은 비직접 고객/세계 사건
→ ARCHIVE_ACCESSION_STATE
 + PROVENANCE_DOCUMENTATION_STATE
 + ITEM_UID_CUSTODY_LEGACY_STATE
→ 보존·기존 treatment·재평가·후속 전시/연구·다른 작품 제작 이유
```

- Ersa/Collector01의 공개 전시 증거·thesis 책임을 보존한다.
- Noble01의 물리적 수리·복원·재작업 개입 깊이 책임을 보존한다.
- 진품성·provenance completeness·archive prestige 같은 aggregate score를 만들지 않는다.
- 최고 Artistry·가장 오래된 작품·가장 많은 Chronicle·최고 강화가 자동 정답이 아니다.
- 기록되지 않은 provenance/custody를 생성하거나 자동 보완하지 않는다.
- archive storage·museum·visitor·staff/shelf·보존환경·loan logistics 관리 게임을 추가하지 않는다.
- accession/review 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 같은 작품 UID를 후보·인계·accession 결과·후속 custody까지 보존한다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`를 이번 Decision에서 재정의하지 않는다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`

이 승인은 **기획 재개 승인**이다. Task3 또는 일반 제품 구현 승인이 아니다.'''
    text = replace_section(text, "## 현재 R3–R7 기획 재개 상태", "## 현재 권위와 보호 경계", section, "ACTIVE current R3 section")
    # Add Decision08 historical/protection token before compatibility index if not present there.
    protection = "- `BS-CONTENT-20260811-08`은 Ersa 전시·Noble01 처치 책임을 침범하지 않고, 숨은 archive/provenance 총점·기록 조작·museum 관리·same-UID 훼손·accession farming을 금지한다.\n"
    marker = "## 승인 Decision 호환 인덱스"
    if protection not in text:
        text = text.replace(marker, protection + "\n" + marker, 1)
    idx_anchor = "BS-CONTENT-20260811-07 / R3_R7_7_OF_10\n"
    if "BS-CONTENT-20260811-08 / R3_R7_8_OF_10" not in text:
        text = text.replace(idx_anchor, idx_anchor + "BS-CONTENT-20260811-08 / R3_R7_8_OF_10\n", 1)
    write(path, text)


def materialize_start_here() -> None:
    path = "[기획서]/00_프로젝트_허브/START_HERE.md"
    text = common_current_replacements(read(path))
    text = text.replace("BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_07_START: 27365bc774508bea6a1a19221fb2a3dc2d093be5", "BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_08_START: 7005a939e003f7248e7d2546c4266bb5d144f90a")
    text = text.replace("현재 사용자 승인 Decision: `BS-CONTENT-20260811-07`.", "현재 사용자 승인 Decision: `BS-CONTENT-20260811-08`.")
    text = text.replace("현재 연속 작업은 `BS-CONTENT-20260811-07`이다.", "현재 연속 작업은 `BS-CONTENT-20260811-08`이다.")
    section = '''## 현재 R3–R7 설계 재개

`BS-CONTENT-20260811-01`~`07`은 승인 완료 이력으로 유지한다.

현재 사용자 승인 Decision: `BS-CONTENT-20260811-08`.
현재 연속 작업은 `BS-CONTENT-20260811-08`이다.

```text
COLLECTOR_02 / SEDRIC_VAEL
ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
→ 장기 보관 목적 공개
→ 실제 작품 UID와 provenance/custody evidence 비교
→ 한 작품 UID 선택·같은 UID 인계
→ 비직접 archival accession 결과
→ ARCHIVE_ACCESSION_STATE
 + PROVENANCE_DOCUMENTATION_STATE
 + ITEM_UID_CUSTODY_LEGACY_STATE
→ 보존·기존 treatment·재평가·후속 승인 콘텐츠·다른 작품 제작 판단
```

- Ersa는 공개 전시 증거/thesis, Sedric은 archival accession/provenance/custody, Noble01은 물리적 treatment depth를 각각 소유한다.
- 숨은 authenticity/provenance/archive 총점을 만들지 않는다.
- 최고 Artistry·가장 오래된 작품·가장 많은 Chronicle·최고 강화가 자동 정답이 아니다.
- 누락된 기록을 생성·자동 보완하지 않는다.
- archive/museum/storage/visitor/staff/loan logistics 관리 게임을 추가하지 않는다.
- accession/review 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- `SAME_ITEM_UID_PRESERVED`를 유지한다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 보류 상태를 유지한다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

책임 원본:

1. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
2. `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
3. `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
4. `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`
5. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`
6. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`
7. `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`
8. `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
9. `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`'''
    text = replace_section(text, "## 현재 R3–R7 설계 재개", "## 처음 읽을 순서", section, "START current R3 section")
    first_read = '''## 처음 읽을 순서

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
14. `ACTIVE_CONTEXT.md`
15. `DEVELOPMENT_GATES.md`
16. `ROADMAP.md`
17. 실제 code/data/Scene/tests
18. Google Sheet `00`, `01`, `02`, `04`, `13`, `50` current rows'''
    text = replace_section(text, "## 처음 읽을 순서", "## Task2 폐쇄 증거", first_read, "START read order")
    # Replace obsolete tail with a short current block, keeping earlier historical D07 material elsewhere.
    if "<!-- BS-CONTENT-20260811-07 CURRENT -->" in text:
        text = text.split("<!-- BS-CONTENT-20260811-07 CURRENT -->", 1)[0].rstrip() + "\n\n" + r'''<!-- BS-CONTENT-20260811-08 CURRENT -->
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

`COLLECTOR_02 / SEDRIC_VAEL / ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY`는 실제 작품 UID 한 점의 장기 보관 인계와 provenance/custody 판단을 소유한다. `ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE`는 서로 분리한다.

현재 연속 작업은 `BS-CONTENT-20260811-08`이다.
'''
    write(path, text)


def materialize_roadmap() -> None:
    path = "[기획서]/00_프로젝트_허브/ROADMAP.md"
    text = common_current_replacements(read(path))
    text = text.replace("CURRENT_STAGE_STATUS: R3_R7_7_OF_10_USER_APPROVED_PLANNING_ONLY", "CURRENT_STAGE_STATUS: R3_R7_8_OF_10_USER_APPROVED_PLANNING_ONLY")
    text = text.replace("현재 승인 카운터: `7/10`.", "현재 승인 카운터: `8/10`.")
    text = text.replace("`BS-CONTENT-20260811-01`부터 `BS-CONTENT-20260811-07`까지", "`BS-CONTENT-20260811-01`부터 `BS-CONTENT-20260811-08`까지")
    d08_section = r'''### 8/10 — `BS-CONTENT-20260811-08`

```text
COLLECTOR_02 / SEDRIC_VAEL
ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE
```

목표:

- 공개된 archival purpose와 작품 UID에 실제 기록된 provenance/custody/lifecycle evidence를 비교해 한 작품을 인계한다.
- Ersa의 공개 전시 책임과 Noble01의 물리적 treatment-depth 책임을 보존한다.
- 진품성·provenance completeness·archive prestige 총점과 최고 Artistry/가장 오래된 작품/가장 많은 Chronicle/최고 강화 자동정답을 만들지 않는다.
- 기록 조작·누락 이력 autofill과 archive/museum/storage/visitor/staff/loan-logistics management를 추가하지 않는다.
- 같은 UID를 보존하며 accession/review 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 별도 사용자 결정 전 유지한다.

책임 원본:

- `docs/planning/BLACKSMITH_R3_COLLECTOR_02_SEDRIC_VAEL_ARCHIVAL_ACCESSION_CANON_2026.md`
'''
    marker = "## R3 — 버티컬 슬라이스 기반"
    if "### 8/10 — `BS-CONTENT-20260811-08`" not in text:
        if marker not in text:
            raise RuntimeError("ROADMAP R3 marker missing")
        text = text.replace(marker, d08_section + "\n" + marker, 1)
    write(path, text)


def materialize_gates() -> None:
    path = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
    text = common_current_replacements(read(path))
    text = text.replace("- R3–R7 `7/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.", "- R3–R7 `8/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.")
    section = r'''## R3–R7 Planning-Only Gate

현재 Decision: `BS-CONTENT-20260811-08`.
Decision: `BS-CONTENT-20260811-08`.

첫 승인 완료 Decision: `BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`.

```text
COLLECTOR_02 / SEDRIC_VAEL
ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE
```

- `BS-CONTENT-20260811-01`~`07`은 승인 완료 이력으로 보존한다.
- `BS-CONTENT-20260811-07 / SOLDIER_02 / LIANA_BERG`는 7/10 승인 이력이며 current locator가 아니다.
- `BS-CONTENT-20260811-08 / COLLECTOR_02 / SEDRIC_VAEL`가 현재 8/10 Decision이다.
- 기존 `SEDRIC_VAEL` 고객을 재사용하고 새 Collector/Noble 대표를 만들지 않는다.
- Ersa의 `EXHIBITION_EVIDENCE_AND_PROVENANCE`와 Noble01의 `HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY` 책임을 보존한다.
- 같은 UID를 보존하고 accession·provenance documentation·custody legacy를 분리한다.
- authenticity/provenance/archive aggregate score와 최고 Artistry·가장 오래된 작품·가장 많은 Chronicle·최고 강화 자동정답을 만들지 않는다.
- 누락 provenance를 창작/autofill하지 않는다.
- archive storage·museum·visitor·staff/shelf·preservation environment·loan logistics management를 추가하지 않는다.
- accession/review 반복 Artistry/Chronicle farming을 추가하지 않는다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 이번 Decision으로 해결하지 않는다.
- 제품 구현은 `BLOCKED`, Task3 구현은 `NOT_APPROVED`다.'''
    text = replace_section(text, "## R3–R7 Planning-Only Gate", "## Canon Gate", section, "GATES planning section")
    write(path, text)


def update_moving_consumers() -> None:
    paths = [
        "tests/check_project_core_alignment_current.py",
        "tests/test_r3_soldier_01_marek_content.py",
        "tests/test_r3_soldier_02_liana_content.py",
        "tests/test_r3_collector_01_ersa_content.py",
        "tests/test_r3_gladiator_01_cassia_content.py",
        "tests/test_r3_noble_01_heirloom_succession_content.py",
        "tests/test_auto_enhancement_cap_unlock.py",
        "tests/test_hera_postmerge_closure_contract.py",
        "tests/test_project_operating_system_audit_runner.py",
        "tools/run_project_operating_system_audit.py",
    ]
    for path in paths:
        p = ROOT / path
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        text = common_current_replacements(text)
        # In current-pointer assertions only, the registry's moving counter advances.
        text = text.replace('self.assertEqual("7/10", registry.get("next_approval_counter"))', 'self.assertEqual("8/10", registry.get("next_approval_counter"))')
        text = text.replace("assert registry.get(\"next_approval_counter\") == \"7/10\"", "assert registry.get(\"next_approval_counter\") == \"8/10\"")
        text = text.replace("registry.get(\"next_approval_counter\") != \"7/10\"", "registry.get(\"next_approval_counter\") != \"8/10\"")
        # Moving current decision inventories should include D08 while immutable D07 status strings remain untouched.
        if D07 in text and D08 not in text and path not in {"tests/test_hera_postmerge_closure_contract.py"}:
            text = text.replace(f'            "{D07}",\n', f'            "{D07}",\n            "{D08}",\n')
        p.write_text(text, encoding="utf-8")


def update_python_validation() -> None:
    path = ".github/workflows/python-validation.yml"
    text = read(path)
    line = "          python -m unittest tests.test_r3_collector_02_sedric_content -v\n"
    if line not in text:
        anchor = "          python -m unittest tests.test_r3_collector_01_ersa_content -v\n"
        if anchor not in text:
            raise RuntimeError("python-validation Ersa anchor missing")
        text = text.replace(anchor, anchor + line, 1)
    write(path, text)


def refresh_operating_health_hash() -> None:
    current_bytes = (ROOT / "CURRENT_CONFIRMED_DECISIONS.md").read_bytes()
    digest = hashlib.sha256(current_bytes).hexdigest()
    path = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    found = False
    for item in data.get("evidence", {}).get("operating", []):
        if item.get("id") == "BS-CURRENT-DECISIONS":
            item["sha256"] = digest
            found = True
    if not found:
        raise RuntimeError("BS-CURRENT-DECISIONS health entry missing")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_materialized_files() -> None:
    required = {
        "CURRENT_CONFIRMED_DECISIONS.md": [D08, "R3_R7_APPROVAL_COUNTER: 8/10", "PRODUCT_IMPLEMENTATION: BLOCKED", "TASK3_IMPLEMENTATION: NOT_APPROVED"],
        "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md": [D08, "R3_R7_APPROVAL_COUNTER: 8/10", LOC8],
        "[기획서]/00_프로젝트_허브/START_HERE.md": [D08, "R3_R7_APPROVAL_COUNTER: 8/10", LOC8],
        "[기획서]/00_프로젝트_허브/ROADMAP.md": [D08, "R3_R7_APPROVAL_COUNTER: 8/10", LOC8],
        "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md": [D08, "R3_R7_APPROVAL_COUNTER: 8/10", LOC8],
    }
    for path, tokens in required.items():
        text = read(path)
        for token in tokens:
            if token not in text:
                raise RuntimeError(f"{path} missing required token {token}")
    if not CANON_PATH.is_file():
        raise RuntimeError("Sedric canon not created")
    canon = CANON_PATH.read_text(encoding="utf-8")
    for token in (
        "ARCHIVE_ACCESSION_STATE",
        "PROVENANCE_DOCUMENTATION_STATE",
        "ITEM_UID_CUSTODY_LEGACY_STATE",
        "SAME_ITEM_UID_PRESERVED",
        "ERSA_EXHIBITION_RESPONSIBILITY_PRESERVED",
        "NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED",
        "P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED",
    ):
        if token not in canon:
            raise RuntimeError(f"canon missing {token}")


def main() -> None:
    CANON_PATH.write_text(CANON, encoding="utf-8")
    materialize_registry()
    materialize_current_decisions()
    materialize_active()
    materialize_start_here()
    materialize_roadmap()
    materialize_gates()
    update_moving_consumers()
    update_python_validation()
    refresh_operating_health_hash()
    validate_materialized_files()
    print("Decision08 materialization complete")


if __name__ == "__main__":
    main()
