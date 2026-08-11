from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION = "BS-CONTENT-20260811-05"
CANON_PATH = ROOT / "docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")


def replace_exact(text: str, old: str, new: str, *, expected: int = 1) -> str:
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"exact replacement count mismatch for {old!r}: expected {expected}, got {count}")
    return text.replace(old, new)


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    pattern = re.escape(start) + r".*?" + re.escape(end)
    new, count = re.subn(pattern, replacement + end, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"section replacement failed: {start!r} -> {end!r}")
    return new


CANON = r'''# Blacksmith R3 Gladiator 01 — Cassia Bellan Arena Signature Weapon Canon

## Authority

- Decision: `BS-CONTENT-20260811-05`
- Content ID: `GLADIATOR_01`
- Customer: `CASSIA_BELLAN / 카시아 벨란`
- Activity family: `ARENA_SIGNATURE_WEAPON_AND_LEGACY`
- R3–R7 approval slot: `5/10`
- Work mode: `PLANNING_ONLY`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`

이 정본은 검투사 경기를 직접 플레이하는 콘텐츠가 아니다. 카시아가 공개한 무기 범주와 경기 맥락을 읽고 대장장이가 작품 한 점을 선택·인계한 뒤, 경기 결과와 그 작품의 실제 기여와 같은 UID의 공개 생애를 분리해서 돌려받는 첫 검투사 대표 상세 콘텐츠다.

## Core promise

```text
CASSIA_BELLAN 방문
→ 요청 무기 범주 + 경기 맥락 공개
→ 후보 작품의 hard eligibility와 contextual fit 비교
→ 같은 작품 UID 한 점 선택·인계
→ 경기는 비직접 세계 사건으로 해결
→ ARENA_MATCH_STATE
 + EQUIPMENT_CONTRIBUTION_STATE
 + ITEM_UID_ARENA_LEGACY_STATE
→ 실제 원인 2~4개 + 주 후속 행동 1개
→ 같은 UID의 수리·복원·후속 강화·재대결 신작·보존·전시 판단
```

플레이어 권위는 `BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER`다.

## Request and fit contract

카시아는 최소한 요청 무기 **범주**와 이번 경기에서 중요한 맥락을 인계 전에 공개한다. 판정은 현재 Blacksmith가 실제로 소유하는 정보만 소비한다.

허용되는 예시는 다음과 같다.

- 무기 범주와 hard eligibility
- 일반 강화 단계와 승인된 역할 원수치
- 실제 관련성이 있을 때의 중량·취급 관련 기존 속성
- 맥락이 요구할 때의 승인된 수식어·기능 적합
- 카시아가 공개적으로 이름·상징·계보를 중시하는 요청일 때만 `ARTISTRY`, provenance, 기존 Chronicle 증거

새 `ARENA_SCORE`, `FAME_SCORE`, `GLADIATOR_SCORE`, `SIGNATURE_SCORE` 또는 숨은 범용 전투력 총점을 만들지 않는다.

`NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`. 최고 강화 작품이 항상 최선이 아니다. 공개된 경기 맥락과 작품의 실제 적합이 다르면 더 낮은 강화 작품도 방어 가능한 선택이어야 한다. 가장 유명하거나 가장 오래된 작품도 자동 정답이 아니다.

## Result contract

경기 결과와 장비 기여는 같은 값이 아니다.

```text
ARENA_MATCH_STATE
EQUIPMENT_CONTRIBUTION_STATE
ITEM_UID_ARENA_LEGACY_STATE
```

- `ARENA_MATCH_STATE`: 경기 자체가 어떤 결과로 끝났는지.
- `EQUIPMENT_CONTRIBUTION_STATE`: 공개된 경기 맥락과 실제 작품 속성에 근거해 작품이 무엇을 도왔거나 방해했는지.
- `ITEM_UID_ARENA_LEGACY_STATE`: 결정적 장면, 경기 손상, 라이벌 흔적, 공개적으로 기억될 사건 또는 의미 있는 공개 생애 없음 등 같은 UID에 남는 결과.

`NO_WIN_EQUALS_GOOD_ITEM_COLLAPSE`.

- 승리했다고 작품이 최적이었다고 단정하지 않는다.
- 패배했다고 작품이 나빴다고 단정하지 않는다.
- 강한 장비 기여와 경기 패배가 함께 존재할 수 있다.
- 약한 장비 기여와 경기 승리가 함께 존재할 수 있다.

결과 화면은 세 축을 하나의 `%`, 별점, 위신 총점으로 합치지 않는다. 실제 원인 2~4개와 다음 제작 판단에 가장 직접적인 주 행동 이유 1개를 보여준다.

## Same-UID lifecycle

`SAME_ITEM_UID_PRESERVED`.

인계 전·경기 중·귀환 뒤 작품은 같은 UID다. 경기 사용은 기존 작품 생애 권위가 허용하는 범위에서 손상·수리 필요·소유/인계 provenance·라이벌 흔적·Chronicle 후보 사건을 만들 수 있지만 작품을 복제·대체·재추첨하지 않는다.

후속 수리·복원·후속 강화·재판매·보존·재대결 의뢰·전시는 같은 UID의 과거 경기 증거를 다시 읽을 수 있어야 한다.

## Progression boundaries

경기는 무료 성장 파밍이 아니다.

- 경기 횟수만으로 `ARTISTRY`가 증가하지 않는다.
- 승리 횟수나 명성만으로 `ARTISTRY`가 증가하지 않는다.
- 경기 출전 또는 승리 사실만으로 `CHRONICLE_AFFIX`를 자동 부여하지 않는다.
- 기존 Chronicle 권위가 충분히 의미 있는 특정 경기 사건을 Chronicle 결과로 판정할 때만 그 사건과 같은 UID에 연결한다.
- 반복 경기는 자동 누적 보너스나 farming multiplier를 만들지 않는다.

```text
NO_MATCH_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_APPEARANCE
NO_MATCH_FARMING_MULTIPLIER
```

## Player authority boundary

다음은 이 Decision의 코어가 아니다.

- 직접 검투사 전투 조작
- 전투 중 위치 지정·행동 명령
- 검투사 팀·길드·로스터 경영
- 배팅 시스템
- 실시간 투기장 운영

```text
NO_DIRECT_ARENA_COMBAT
NO_GLADIATOR_TEAM_OR_GUILD_MANAGEMENT
NO_BETTING_SYSTEM
NO_OPAQUE_ARENA_SCORE
```

경기 실행은 Blacksmith 밖의 비직접 세계 사건이며 플레이어는 대장장이로 남는다.

## Legacy gladiator PoC boundary

현재 저장소의 `data/customers/gladiator_poc.json`과 `data/world/gladiator_match_poc.json`은 역사 POC fixture다. 이 Decision은 그 파일을 수정하거나 현재 설계 권위로 승격하지 않는다.

```text
LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05
NO_FIXED_IRON_SWORD_CANON
NO_LEGACY_ARENA_SCORE_FORMULA_CANON
NO_UNIVERSAL_FIXED_DAY_COUNT
```

따라서 과거의 `iron_sword`, +5/+10, preferred-affix 목록, 고정 3일, grade score, score weight, result band 수치는 Decision05의 정본 수치가 아니다.

## Information contract

카시아 기본 카드와 인계 전 판단층은 다음을 분리해 보여준다.

- 요청 무기 범주와 hard eligibility
- 이번 경기 맥락에서 실제 관련 있는 판단 차원
- 선택된 작품 UID
- 지지 또는 충돌 원인 2~4개

자동 `BEST` 추천은 제공하지 않는다.

결과는 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`, 실제 원인 2~4개, 주 후속 행동 1개를 보여준다. 색상만으로 핵심 상태를 전달하지 않는다.

정확한 문구·임계값·기간·경제값·보상·결과 분포는 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## Protected boundaries

```text
NO_DIRECT_ARENA_COMBAT
NO_GLADIATOR_TEAM_OR_GUILD_MANAGEMENT
NO_BETTING_SYSTEM
NO_OPAQUE_ARENA_SCORE
NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST
NO_WIN_EQUALS_GOOD_ITEM_COLLAPSE
NO_MATCH_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_APPEARANCE
NO_MATCH_FARMING_MULTIPLIER
SAME_ITEM_UID_PRESERVED
LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05
BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER
PRODUCT_IMPLEMENTATION_BLOCKED
TASK3_IMPLEMENTATION_NOT_APPROVED
```

## Adversarial decision report

1. **Combat-RPG drift** — 경기 실행은 비직접 세계 사건으로 유지하고 플레이어 권위를 작품 판단에 둔다. `MUST_FIX`.
2. **Opaque score drift** — 새 투기장/명성/검투사 총점을 만들지 않는다. `MUST_FIX`.
3. **Win=item quality collapse** — 경기 결과와 작품 기여를 별도 축으로 유지한다. `MUST_FIX`.
4. **Highest-enhancement dominance** — 공개 맥락과 기존 작품 속성의 설명 가능한 적합을 사용한다. `MUST_FIX`.
5. **Progression farming** — 경기/승리 횟수로 Artistry 또는 Chronicle을 자동 성장시키지 않는다. `MUST_FIX`.
6. **UID loss** — 경기 전·중·후 같은 작품 UID를 보존한다. `MUST_FIX`.
7. **Legacy fixture resurrection** — Kyle/iron_sword POC 수치와 점수식은 역사 fixture로만 남긴다. `MUST_FIX`.
8. 전투를 직접 조작해야 더 극적이라는 비판은 Blacksmith의 대장장이 역할을 무너뜨리는 범위 확대이므로 `REJECTED_CRITIQUE`.

## Acceptance

- `BS-CONTENT-20260811-05 / GLADIATOR_01 / CASSIA_BELLAN / ARENA_SIGNATURE_WEAPON_AND_LEGACY`가 R3–R7 `5/10` 현재 기획 Decision이 된다.
- Nadia 1/10, Toren 2/10, Marek 3/10, Ersa 4/10은 승인 이력으로 보존한다.
- 경기 결과와 작품 기여와 같은 UID 공개 생애를 세 축으로 분리한다.
- 직접 전투·팀/길드 경영·배팅·불투명 투기장 총점을 추가하지 않는다.
- 최고 강화와 경기 승리를 작품 품질의 자동 정답으로 만들지 않는다.
- 경기 횟수/승리만으로 Artistry 또는 Chronicle을 자동 성장시키지 않는다.
- legacy gladiator POC 고정 수치와 점수식을 현재 권위로 승격하지 않는다.
- 제품 구현과 Task3 구현 Gate는 열리지 않는다.
'''

CANON_PATH.write_text(CANON, encoding="utf-8")

# Registry: structural append, not text substitution.
registry_rel = "docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json"
registry = json.loads(read(registry_rel))
if registry.get("next_approval_counter") != "4/10":
    raise RuntimeError(f"expected pre-promotion registry counter 4/10, got {registry.get('next_approval_counter')!r}")
ids = [item.get("id") for item in registry.get("current_decisions", [])]
if ids != [
    "BS-CONTENT-20260811-01",
    "BS-CONTENT-20260811-02",
    "BS-CONTENT-20260811-03",
    "BS-CONTENT-20260811-04",
]:
    raise RuntimeError(f"unexpected current decision sequence: {ids!r}")
registry["next_approval_counter"] = "5/10"
registry["current_decisions"].append({
    "id": DECISION,
    "title": "검투사 01 카시아 벨란 투기장 대표 무기·공개 생애 콘텐츠",
    "status": "USER_APPROVED_R3_R7_5_OF_10",
    "canon": "docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md",
    "refines": ["BS-CONTENT-20260804-01", "BS-CONTENT-20260804-02"],
    "depends_on": [
        "BS-CUSTOMER-20260803-02",
        "BS-CUSTOMER-20260805-01",
        "BS-CUSTOMER-20260806-01",
        "BS-ITEM-20260806-04",
        "BS-UX-20260805-01",
        "BS-CRAFT-20260804-06",
        "BS-CONTENT-20260811-04",
    ],
    "contract": {
        "content_id": "GLADIATOR_01",
        "customer_id": "CASSIA_BELLAN",
        "customer_archetype": "GLADIATOR",
        "activity_family": "ARENA_SIGNATURE_WEAPON_AND_LEGACY",
        "content_goal": "ARENA_RENOWN_THROUGH_EXPLAINABLE_EQUIPMENT_CONTRIBUTION",
        "player_role": "BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER",
        "direct_arena_combat": False,
        "gladiator_team_or_guild_management": False,
        "betting_system": False,
        "opaque_arena_score": False,
        "single_highest_enhancement_always_best": False,
        "win_equals_good_item_collapse": False,
        "same_item_uid_preserved": True,
        "match_count_artistry_growth": False,
        "automatic_chronicle_affix_from_win_or_appearance": False,
        "match_farming_multiplier": False,
        "legacy_gladiator_poc_status": "NON_AUTHORITATIVE_HISTORICAL_FIXTURE",
        "result_axes": ["ARENA_MATCH_STATE", "EQUIPMENT_CONTRIBUTION_STATE", "ITEM_UID_ARENA_LEGACY_STATE"],
        "immediate_feedback": "THREE_STATE_SUMMARY_WITH_2_TO_4_CAUSAL_REASONS_AND_ONE_PRIMARY_NEXT_ACTION",
        "exact_values": "NON_CANONICAL_BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED",
        "product_implementation": "BLOCKED",
        "task3_implementation": "NOT_APPROVED",
        "human_playtest": "NOT_RUN",
    },
})
for entry in [
    {"source": "Gladiator Guild Manager official Steam page", "decision": "ADAPT", "use": "pre-event equipment choice with automated consequence", "avoid": "fighter positioning behavior orders and guild management"},
    {"source": "Battle Brothers official developer features", "decision": "ADAPT", "use": "equipment suitability materially affects combat outcome", "avoid": "direct tactical combat and mercenary-company control"},
    {"source": "Crusader Kings III: Tours & Tournaments official Paradox page", "decision": "ADAPT", "use": "public tournament renown and preparation context", "avoid": "tournament-hosting gameplay as Blacksmith core"},
    {"source": "Apple Human Interface Guidelines feedback guidance", "decision": "ADOPT", "use": "clear decomposed status outcome and next-action feedback", "avoid": "single opaque success score"},
    {"source": "Android Developers user experience quality guidance", "decision": "ADOPT", "use": "intuitive meaningful state hierarchy", "avoid": "score chasing that hides causal fit"},
    {"source": "Games User Research playtest method guidance", "decision": "ADOPT", "use": "observed choice behavior plus neutral recall of match-versus-item contribution", "avoid": "leading self-report-only validation"},
]:
    if entry not in registry["benchmark_context"]:
        registry["benchmark_context"].append(entry)
for boundary in [
    "NO_DIRECT_ARENA_COMBAT",
    "NO_GLADIATOR_TEAM_OR_GUILD_MANAGEMENT",
    "NO_BETTING_SYSTEM",
    "NO_OPAQUE_ARENA_SCORE",
    "NO_WIN_EQUALS_GOOD_ITEM_COLLAPSE",
    "NO_MATCH_COUNT_ARTISTRY_GROWTH",
    "NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_APPEARANCE",
    "NO_MATCH_FARMING_MULTIPLIER",
    "LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05",
    "BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER",
]:
    if boundary not in registry["protected_boundaries"]:
        registry["protected_boundaries"].append(boundary)
write(registry_rel, json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

# Current decisions: promote only current pointers, preserve the Decision04 history line, append Decision05.
current_rel = "CURRENT_CONFIRMED_DECISIONS.md"
current = read(current_rel)
current = replace_exact(current, "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-04 / R3_R7_4_OF_10 / PLANNING_ONLY**", "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-05 / R3_R7_5_OF_10 / PLANNING_ONLY**")
current = replace_exact(current, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10")
current = replace_exact(current, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05")
lines = current.splitlines()
needle_prefix = "- `BS-CONTENT-20260811-04`:"
matches = [i for i, line in enumerate(lines) if line.startswith(needle_prefix)]
if len(matches) != 1:
    raise RuntimeError(f"expected exactly one Decision04 current ledger line, got {len(matches)}")
insert_at = matches[0] + 1
lines.insert(insert_at, "- `BS-CONTENT-20260811-05`: `GLADIATOR_01` 카시아 벨란 투기장 대표 무기·공개 생애 콘텐츠. 요청 무기 범주와 경기 맥락을 공개하고 작품 한 점을 인계하며, 직접 전투 없이 결과를 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`로 분리한다. 새 투기장/명성 총점·최고 강화 자동정답·승리=좋은 작품 단순화·경기 반복 Artistry/Chronicle 파밍을 만들지 않고 같은 UID를 보존한다. legacy Kyle/iron_sword POC 고정 수치·점수식은 역사 fixture로만 유지한다. — `USER_APPROVED / R3_R7_5_OF_10 / PLANNING_ONLY`")
current = "\n".join(lines) + ("\n" if current.endswith("\n") else "")
current += r'''

## 22. R3–R7 다섯 번째 상세 콘텐츠 — 카시아 벨란 투기장 대표 무기·공개 생애

Decision: `BS-CONTENT-20260811-05`.

```text
GLADIATOR_01 / CASSIA_BELLAN
ARENA_SIGNATURE_WEAPON_AND_LEGACY
ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE
```

- 플레이어는 카시아를 직접 조작하지 않고 공개된 무기 범주·경기 맥락을 읽어 같은 작품 UID 한 점을 선택·인계한다.
- 경기 승패와 작품의 실제 기여를 분리한다. 승리=좋은 작품, 패배=나쁜 작품으로 단순화하지 않는다.
- 새 `ARENA_SCORE / FAME_SCORE / GLADIATOR_SCORE / SIGNATURE_SCORE`를 만들지 않는다.
- 최고 강화·최고 명성·가장 오래된 작품을 보편적 자동 정답으로 만들지 않는다.
- 경기/승리 횟수만으로 `ARTISTRY`를 올리거나 `CHRONICLE_AFFIX`를 자동 부여하지 않는다.
- `data/customers/gladiator_poc.json`, `data/world/gladiator_match_poc.json`의 Kyle/iron_sword 고정 수치와 점수식은 역사 POC fixture이며 Decision05 권위가 아니다.
- 책임 원본: `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.
'''
write(current_rel, current)

# Hub current pointers.
active_rel = "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md"
active = read(active_rel)
active = replace_exact(active, "> **R3_R7_DESIGN_ACTIVE / COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED / PLANNING_ONLY**", "> **R3_R7_DESIGN_ACTIVE / GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED / PLANNING_ONLY**")
active = replace_exact(active, "- Blacksmith current main observed at Decision 04 start: `1e60cf163191d547b96ffc392e3da24d072b7956`", "- Blacksmith current main observed at Decision 05 start: `98c0e1f26e51eeb01c04b742b535d7a3a1345c35`")
active = replace_exact(active, "- `BASE_CURRENT_MAIN_OBSERVED`: `315c66eea9614c284b9c11c4d522141065dfa4b0`", "- `BASE_CURRENT_MAIN_OBSERVED`: `8e7d85b1b1272002a8086c502a41073888cb3318`")
active = replace_exact(active, "- 현재 R3–R7 승인 카운터: `4/10`", "- 현재 R3–R7 승인 카운터: `5/10`")
active = replace_exact(active, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10")
active = replace_exact(active, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05")
active = replace_exact(active, "R3_R7_RESUME_LOCATOR: COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED", "R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED")
active_current = r'''## 현재 R3–R7 기획 재개 상태

`BS-CONTENT-20260811-01` Nadia, `BS-CONTENT-20260811-02` Toren, `BS-CONTENT-20260811-03` Marek, `BS-CONTENT-20260811-04` Ersa는 승인 완료 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-05`다.

```text
GLADIATOR_01 / CASSIA_BELLAN
→ 검투사 대표 고객
→ ARENA_SIGNATURE_WEAPON_AND_LEGACY
→ 요청 무기 범주 + 경기 맥락 공개
→ 같은 작품 UID 한 점 선택·인계
→ 경기는 비직접 세계 사건
→ ARENA_MATCH_STATE
 + EQUIPMENT_CONTRIBUTION_STATE
 + ITEM_UID_ARENA_LEGACY_STATE
→ 원인 2~4개 + 주 후속 행동 1개
```

- 직접 검투사 전투·위치 지정·행동 명령·팀/길드 경영·배팅을 추가하지 않는다.
- 경기 승패와 작품의 실제 기여를 분리하고 최고 강화/승리를 자동 정답으로 만들지 않는다.
- 새 투기장·명성·검투사·시그니처 총점을 만들지 않는다.
- 경기 횟수나 승리 자체로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 같은 작품 UID를 경기 전·중·후 보존한다.
- legacy Kyle/iron_sword POC 수치와 score formula는 현재 Decision05 권위가 아니다.

'''
active = replace_section(active, "## 현재 R3–R7 기획 재개 상태\n", "책임 원본:", active_current)
active = replace_exact(active, "- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`", "- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`\n- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`")
active = replace_exact(active, "- `BS-CONTENT-20260811-04`는 전시 횟수만으로 예술성 또는 Chronicle을 자동 성장시키지 않는다.", "- `BS-CONTENT-20260811-04`는 전시 횟수만으로 예술성 또는 Chronicle을 자동 성장시키지 않는다.\n- `BS-CONTENT-20260811-05`는 직접 투기장 전투·팀/길드 경영·배팅·불투명 투기장 총점을 추가하지 않는다.\n- `BS-CONTENT-20260811-05`는 경기 승패와 작품 기여를 분리하고 경기 반복으로 예술성 또는 Chronicle을 자동 성장시키지 않는다.")
active = replace_exact(active, "BS-CONTENT-20260811-04 / R3_R7_4_OF_10", "BS-CONTENT-20260811-04 / R3_R7_4_OF_10\nBS-CONTENT-20260811-05 / R3_R7_5_OF_10")
active_next = r'''## 다음 실행 순서

1. `BS-CONTENT-20260811-05`의 RED→GREEN 계약, 적대 검토, exact-head CI, GitHub·Sheet 동일 Decision ID 동기화를 끝낸다.
2. 경기 승패와 장비 기여가 실제로 분리되는지, same UID와 legacy POC 비권위 경계가 유지되는지 검증한다.
3. 새 제품 Task는 `NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED`와 `TASK3_IMPLEMENTATION: NOT_APPROVED`가 별도 사용자 승인으로 해소되기 전 시작하지 않는다.
4. 다음 R3–R7 신규 Decision은 현재 승인 카운터 `5/10`에서 이어간다.

'''
active = replace_section(active, "## 다음 실행 순서\n", "## 먼저 읽을 파일", active_next)
active = replace_exact(active, "4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`\n5. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`", "4. `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`\n5. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`\n6. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`")
write(active_rel, active)

start_rel = "[기획서]/00_프로젝트_허브/START_HERE.md"
start = read(start_rel)
start = replace_exact(start, "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-04 / COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED / PLANNING_ONLY**", "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-05 / GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED / PLANNING_ONLY**")
start = replace_exact(start, "BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_04_START: 1e60cf163191d547b96ffc392e3da24d072b7956", "BLACKSMITH_CURRENT_MAIN_OBSERVED_AT_DECISION_05_START: 98c0e1f26e51eeb01c04b742b535d7a3a1345c35")
start = replace_exact(start, "BASE_CURRENT_MAIN_OBSERVED: 315c66eea9614c284b9c11c4d522141065dfa4b0", "BASE_CURRENT_MAIN_OBSERVED: 8e7d85b1b1272002a8086c502a41073888cb3318")
start = replace_exact(start, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10", expected=2)
start = replace_exact(start, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05", expected=2)
start = replace_exact(start, "R3_R7_RESUME_LOCATOR: COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED", "R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED", expected=2)
start_current = r'''## 현재 R3–R7 설계 재개

`BS-CONTENT-20260811-01 / ADVENTURER_01 / NADIA_VENN`, `BS-CONTENT-20260811-02 / ADVENTURER_02 / TOREN_MARCH`, `BS-CONTENT-20260811-03 / SOLDIER_01 / MAREK_OLDEN`, `BS-CONTENT-20260811-04 / COLLECTOR_01 / ERSA_ROEN`은 승인 완료 이력으로 유지한다.

현재 사용자 승인 Decision: `BS-CONTENT-20260811-05`.

```text
GLADIATOR_01 / CASSIA_BELLAN
ARENA_SIGNATURE_WEAPON_AND_LEGACY
→ 요청 무기 범주 + 경기 맥락 공개
→ 같은 UID 작품 한 점 선택·인계
→ 비직접 경기 결과
→ ARENA_MATCH_STATE
 + EQUIPMENT_CONTRIBUTION_STATE
 + ITEM_UID_ARENA_LEGACY_STATE
→ 같은 UID의 수리·복원·후속 강화·재대결 신작·보존·전시 판단
```

- 직접 전투·위치 지정·행동 명령·팀/길드 경영·배팅은 추가하지 않는다.
- 새 투기장/명성/검투사/시그니처 총점을 만들지 않는다.
- 경기 승패와 작품 기여를 분리하고 최고 강화나 승리를 자동 정답으로 만들지 않는다.
- 경기 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 같은 작품 UID를 보존한다.
- legacy Kyle/iron_sword POC 고정 수치와 점수식은 Decision05 권위가 아니다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

'''
start = replace_section(start, "## 현재 R3–R7 설계 재개\n", "책임 원본:", start_current)
start = replace_exact(start, "5. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`", "5. `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`\n6. `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`", expected=2)
start = replace_exact(start, "- `BS-CONTENT-20260811-04`는 같은 작품 UID와 기존 제작·생애 증거를 권위로 유지한다.", "- `BS-CONTENT-20260811-04`는 같은 작품 UID와 기존 제작·생애 증거를 권위로 유지한다.\n- `BS-CONTENT-20260811-05`는 경기 승패와 작품 기여를 분리하고 직접 투기장 조작·불투명 총점·반복 파밍을 추가하지 않는다.\n- `BS-CONTENT-20260811-05`는 같은 작품 UID와 legacy POC 비권위 경계를 유지한다.")
start_tail = r'''## 다음 작업

현재 연속 작업은 `BS-CONTENT-20260811-05`의 GitHub·Sheet 동기화, exact-head 검증, 적대적 검토까지다. 다음 신규 R3–R7 Decision은 승인 카운터 `5/10`에서 이어간다. 제품 코드·Scene·Resource·Task3는 별도 사용자 승인 전 시작하지 않는다.

<!-- BS-CONTENT-20260811-05 CURRENT -->
## R3–R7 current 5/10 — Cassia Gladiator01

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 5/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05
R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

Nadia 1/10, Toren 2/10, Marek 3/10, Ersa 4/10은 승인 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-05`이다.

`GLADIATOR_01 / CASSIA_BELLAN / ARENA_SIGNATURE_WEAPON_AND_LEGACY`는 경기 승패와 작품 기여와 같은 UID 공개 생애를 분리해 돌려준다. 직접 전투·팀/길드 경영·배팅·불투명 총점·경기 반복 성장 파밍은 현재 범위가 아니다.

현재 연속 작업은 `BS-CONTENT-20260811-05`이다.
'''
start, count = re.subn(r"## 다음 작업\n.*\Z", start_tail, start, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("failed to replace START_HERE current tail")
write(start_rel, start)

road_rel = "[기획서]/00_프로젝트_허브/ROADMAP.md"
road = read(road_rel)
road = replace_exact(road, "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-04 / COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED / PLANNING_ONLY**", "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-05 / GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED / PLANNING_ONLY**")
road = replace_exact(road, "CURRENT_STAGE_STATUS: R3_R7_4_OF_10_USER_APPROVED_PLANNING_ONLY", "CURRENT_STAGE_STATUS: R3_R7_5_OF_10_USER_APPROVED_PLANNING_ONLY")
road = replace_exact(road, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10", expected=2)
road = replace_exact(road, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05", expected=2)
road = replace_exact(road, "R3_R7_RESUME_LOCATOR: COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED", "R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED", expected=2)
road = replace_exact(road, "현재 승인 카운터: `4/10`.", "현재 승인 카운터: `5/10`.")
section5 = r'''### 5/10 — `BS-CONTENT-20260811-05`

```text
GLADIATOR_01 / CASSIA_BELLAN
ARENA_SIGNATURE_WEAPON_AND_LEGACY
ARENA_RENOWN_THROUGH_EXPLAINABLE_EQUIPMENT_CONTRIBUTION
```

목표:

- 공개된 무기 범주·경기 맥락을 읽고 같은 작품 UID 한 점을 인계한다.
- 직접 전투 없이 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`를 분리한다.
- 새 투기장/명성/검투사/시그니처 총점, 최고 강화 자동정답, 승리=좋은 작품 단순화를 만들지 않는다.
- 경기/승리 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- legacy Kyle/iron_sword POC 수치와 점수식은 역사 fixture로 유지한다.

책임 원본:

- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`

'''
road = replace_exact(road, "## R3 — 버티컬 슬라이스 기반", section5 + "## R3 — 버티컬 슬라이스 기반")
road = replace_exact(road, "`BS-CONTENT-20260811-01`부터 `BS-CONTENT-20260811-04`까지는", "`BS-CONTENT-20260811-01`부터 `BS-CONTENT-20260811-05`까지는")
road = replace_exact(road, "BS-CONTENT-20260811-04: USER_APPROVED_PLANNING_ONLY", "BS-CONTENT-20260811-04: USER_APPROVED_PLANNING_ONLY\nBS-CONTENT-20260811-05: USER_APPROVED_PLANNING_ONLY")
road_tail = r'''<!-- BS-CONTENT-20260811-05 CURRENT -->
## R3–R7 current 5/10 — Cassia Gladiator01

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 5/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05
R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

Nadia 1/10, Toren 2/10, Marek 3/10, Ersa 4/10은 승인 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-05`이다.

경기 승패와 작품 기여와 같은 UID 공개 생애는 별도 결과 축이다. 직접 경기 조작·팀/길드 경영·배팅·불투명 arena score·반복 성장 파밍은 범위 밖이며 legacy gladiator POC 수치/점수식은 현재 권위가 아니다.
'''
road, count = re.subn(r"<!-- BS-CONTENT-20260811-04 CURRENT -->.*\Z", road_tail, road, count=1, flags=re.S)
if count != 1:
    raise RuntimeError("failed to replace ROADMAP current tail")
write(road_rel, road)

gates_rel = "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md"
gates = read(gates_rel)
gates = replace_exact(gates, "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-04 / COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**", "> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-05 / GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED / PLANNING_ONLY / PRODUCT_BLOCKED**")
gates = replace_exact(gates, "R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10")
gates = replace_exact(gates, "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05")
gates = replace_exact(gates, "- R3–R7 `4/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.", "- R3–R7 `5/10`, 제품/Task3 차단은 이 Gate로 변경되지 않는다.")
gate_section = r'''## R3–R7 Planning-Only Gate

현재 Decision: `BS-CONTENT-20260811-05`.

```text
GLADIATOR_01 / CASSIA_BELLAN
ARENA_SIGNATURE_WEAPON_AND_LEGACY
ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE
```

허용:

- 고객·경기 맥락·작품 선택·비직접 결과·같은 UID 생애 환류의 기획 정본 작성
- 벤치마킹·적대 검토·테스트 계약·Google Sheet 동기화
- 공개된 무기 범주·경기 맥락과 기존 작품 속성의 설명 가능한 적합 비교
- 결과를 경기 상태·장비 기여·같은 UID 공개 생애로 분해
- 비정본 exact timing/threshold/economy/result fixture와 사람 플레이테스트 설계

차단:

- Task3 제품 Script/Data/Scene/Resource 구현
- `project.godot` 또는 Godot persistent serialized surface 변경
- 직접 검투사 전투·위치 지정·행동 명령
- 검투사 팀/길드/로스터 경영과 배팅
- 새 `ARENA_SCORE / FAME_SCORE / GLADIATOR_SCORE / SIGNATURE_SCORE`
- 최고 강화 또는 경기 승리를 보편적 자동 정답으로 사용
- 경기/승리 반복으로 `ARTISTRY` 자동 증가 또는 `CHRONICLE_AFFIX` 자동 부여
- 같은 작품 UID를 경기용 복제/대체품으로 치환
- legacy Kyle/iron_sword POC 고정 수치·score formula를 Decision05 권위로 승격

판정: `R3_R7_DESIGN_ACTIVE / PRODUCT_IMPLEMENTATION_BLOCKED / TASK3_IMPLEMENTATION_NOT_APPROVED`.

'''
gates = replace_section(gates, "## R3–R7 Planning-Only Gate\n", "## Canon Gate", gate_section)
current_tail = r'''<!-- BS-CONTENT-20260811-05 CURRENT -->
## R3–R7 current 5/10 — Cassia Gladiator01

Decision: `BS-CONTENT-20260811-05`.

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 5/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05
R3_R7_RESUME_LOCATOR: GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

Decision05는 planning-only다. 직접 전투·team/guild management·betting·opaque arena score·match farming·legacy POC authority promotion은 차단한다.
'''
if "<!-- BS-CONTENT-20260811-04 CURRENT -->" in gates:
    gates, count = re.subn(r"<!-- BS-CONTENT-20260811-04 CURRENT -->.*\Z", current_tail, gates, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("failed to replace DEVELOPMENT_GATES current tail")
else:
    gates = gates.rstrip() + "\n\n" + current_tail
write(gates_rel, gates)

# Update only current-state consumers. Historical Decision/canon files are intentionally excluded.
consumer_files = [
    "tests/test_pre_work_research_gate.py",
    "tests/check_project_core_alignment_current.py",
    "tests/test_auto_enhancement_cap_unlock.py",
    "tests/test_r3_soldier_01_marek_content.py",
    "tests/test_r3_collector_01_ersa_content.py",
    "tests/test_r3_adventurer_02_toren_content.py",
    "tests/test_vertical_slice_new_campaign_initializer_authority.py",
    "tests/test_project_operating_system_audit_runner.py",
    "tests/test_hera_postmerge_closure_contract.py",
    "tools/run_project_operating_system_audit.py",
]
replacements = [
    ("R3_R7_APPROVAL_COUNTER: 4/10", "R3_R7_APPROVAL_COUNTER: 5/10"),
    ("R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-04", "R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-05"),
    ("COLLECTOR_01_ERSA_EXHIBITION_EVIDENCE_APPROVED", "GLADIATOR_01_CASSIA_ARENA_SIGNATURE_WEAPON_APPROVED"),
    ("현재 Decision은 `BS-CONTENT-20260811-04`", "현재 Decision은 `BS-CONTENT-20260811-05`"),
    ("현재 연속 작업은 `BS-CONTENT-20260811-04`", "현재 연속 작업은 `BS-CONTENT-20260811-05`"),
    ("현재 승인 카운터: `4/10`.", "현재 승인 카운터: `5/10`."),
    ("Decision: `BS-CONTENT-20260811-04`.", "Decision: `BS-CONTENT-20260811-05`."),
]
for rel in consumer_files:
    p = ROOT / rel
    if not p.exists():
        raise RuntimeError(f"expected current consumer missing: {rel}")
    text = p.read_text(encoding="utf-8")
    for old, new in replacements:
        text = text.replace(old, new)
    if rel == "tests/test_r3_collector_01_ersa_content.py":
        text = text.replace('self.assertEqual("4/10", registry.get("next_approval_counter"))', 'self.assertEqual("5/10", registry.get("next_approval_counter"))')
        text = text.replace("test_current_routers_move_to_four_of_ten_without_opening_product_code", "test_current_routers_preserve_ersa_history_while_cassia_is_current")
    p.write_text(text, encoding="utf-8")

# CURRENT_CONFIRMED_DECISIONS integrity hash.
health_rel = "docs/PROJECT_OPERATING_HEALTH.json"
health = json.loads(read(health_rel))
current_sha = hashlib.sha256((ROOT / current_rel).read_bytes()).hexdigest()
found = False
for item in health.get("evidence", {}).get("operating", []):
    if item.get("id") == "BS-CURRENT-DECISIONS":
        item["sha256"] = current_sha
        found = True
if not found:
    raise RuntimeError("BS-CURRENT-DECISIONS health entry missing")
write(health_rel, json.dumps(health, ensure_ascii=False, indent=2) + "\n")

# Self-remove one-shot authoring helpers so the resulting planning diff contains no permanent materializer.
for rel in ["tools/_materialize_cassia_5of10.py", ".github/workflows/_materialize-cassia-5of10.yml"]:
    p = ROOT / rel
    if p.exists():
        p.unlink()

print("Cassia 5/10 planning materialization complete")
