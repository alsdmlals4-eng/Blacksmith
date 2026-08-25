# [현재 정본] Blacksmith 기획 권위 색인

- 상태: `CURRENT_AUTHORITY_INDEX`
- current decisions: `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-CHRONICLE-20260825-27 / BS-ART-20260825-03`
- current owner: `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## 1. 충돌 시 우선순위

1. 사용자의 최신 지시와 승인.
2. `AGENTS.md`.
3. `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` — Decisions25~27 / Art03의 같은 필드 current owner.
4. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`의 `2026-08-25 CURRENT OVERRIDE`.
5. 2026-08-20/24 개별 Canon 문서 — 새 owner와 충돌하지 않는 필드만 current; 충돌 필드는 역사·부분대체 evidence.
6. 실제 runtime/data/test evidence — 구현 사실을 증명하지만, 현재 PLAN Gate에서 남은 구현 drift가 최신 승인 기획을 덮어쓰지 않는다.
7. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 역사 원장.
8. R2/R3 Game Bible·과거 PoC·구형 data/runtime.

```text
CURRENT_OWNER = docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
BS-ENHANCE-20260825-25
BS-DAMAGE-20260825-26
BS-CHRONICLE-20260825-27
BS-ART-20260825-03
```

새 `기획 완료` 사용자 선언 전 제품 `data/scripts/scenes/assets/addons/project.godot` 변경은 금지한다.

## 2. 현재 핵심 계약

### Enhancement / Precision

```text
SUCCESS_LEVEL_DELTA = +1
TARGET = CURRENT + 1
+9 -> +10 = PRECISION_ENHANCEMENT
+10 PRECISION SUCCESS -> exactly one ITEM_KEYWORD
ITEM_KEYWORD machine owner = CATALYST_AFFIX
NO_FOURTH_AFFIX_SLOT
```

+20/+30/+40/+50은 current Precision Enhancement milestone이 아니다.

### Damage

```text
NORMAL -> MINOR -> MAJOR -> DESTROYED
ONE_DAMAGE_EVENT_ADVANCES_ONE_STATE
TARGET <= +10: ENHANCEMENT_DAMAGE = 0
TARGET >= +11: ENHANCEMENT_DAMAGE = POSSIBLE
MONOTONIC_NON_DECREASING_DAMAGE_RISK
CUSTOMER_WORLD_EVENT_DAMAGE = POSSIBLE_IF_EVENT_ELIGIBLE
PURCHASE_ITSELF_CAUSES_DAMAGE = FALSE
CURRENT_MAX_AUTHORITY = SUPERSEDED
```

정확 +11~+100 강화 실패 damage probability, customer-event damage probability, MINOR/MAJOR repair와 MAJOR enhancement eligibility는 아직 승인되지 않았다.

### Chronicle

```text
ROUTINE_ENHANCEMENT_HISTORY = NOT_PLAYER_CHRONICLE
MEANINGFUL_EVENT_HISTORY_ONLY
```

내부 ledger/day provenance는 causality/diagnostic을 위해 보존할 수 있으나 player-facing Chronicle에 routine `N days ago` 강화 로그를 강제하지 않는다.

### Art direction

```text
ART_DIRECTION = ILLUSTRATED_WORKSHOP_BOOK
ART_DIRECTION_STATUS = USER_APPROVED_DIRECTION
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
```

## 3. 현재 책임 원본

### 3.1 Current simplified owner

- `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` — enhancement cadence, +10 Precision Keyword, four-state damage, +11+ damage gate, customer/world damage hook, Chronicle inclusion, Illustrated Workshop Book direction.

### 3.2 Core / progression — preserved where non-conflicting

- `BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md` — PRIMARY CORE `강화 긴장감 + DDD`.
- `BLACKSMITH_ENHANCEMENT_PROGRESSION_ECONOMY_CANON_20260820.md` — +10 break-even / +100 range structure; exact economics need recheck after new damage/repair model.
- `BLACKSMITH_LEVEL_TO_EXPERIENCE_BAND_CANON_20260820.md` — target-level band mapping only; old band damage-family semantics superseded.
- `BLACKSMITH_CHECKPOINT_CADENCE_CANON_20260820.md` — `CHECKPOINT_FLOORS=[10,30,60,90]`, downgrade floor only.
- `BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md` — success/recovery/attempt-cost test budgets where independent of CURRENT/MAX; not final balance.
- `BLACKSMITH_COMMON_RESOURCE_SUPPLY_CANON_20260824.md` — common reinforcement material enhancement supply preserved; CURRENT/MAX repair mapping superseded.
- `BLACKSMITH_MAX_LEVEL_PAYOFF_CANON_20260824.md` — +100 terminal identity/payoff remains.

### 3.3 Damage / durability — historical or partially superseded

- `BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md` — recovery/disclosure principles may remain; numeric damage semantics are historical.
- `BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md` — checkpoint parts retained; CURRENT/MAX durability parts `PARTIALLY_SUPERSEDED`.
- `BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md` — `SUPERSEDED_FOR_CURRENT_DAMAGE_AUTHORITY / HISTORICAL_EVIDENCE`.
- `BLACKSMITH_DURABILITY_BALANCE_BUDGET_WORKING_20260820.md` — old CURRENT/MAX budget only.
- `BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md` — old DAMAGE/CRITICAL family ratios are not the new +11~+100 damage curve.

### 3.4 Repair / overhaul — reopened

- `BLACKSMITH_REPAIR_REFERENCE_AND_WORKLOAD_CANON_20260820.md` — old CURRENT/MAX repair formula historical.
- `BLACKSMITH_REPAIR_ABSOLUTE_ANCHOR_CANON_20260820.md` — old repair anchor historical.
- `BLACKSMITH_LATE_REPAIR_ECONOMY_CANON_20260824.md` — historical sensitivity evidence, not new four-state repair authority.
- `BLACKSMITH_MAX_OVERHAUL_CANON_20260824.md` — `SUPERSEDED_PENDING_NEW_REPAIR_MODEL`.

Current unresolved owner fields:

```text
MINOR_MAJOR_REPAIR_MODEL = USER_APPROVAL_REQUIRED
MAJOR_ENHANCEMENT_ELIGIBILITY = USER_APPROVAL_REQUIRED
```

### 3.5 Destruction / item life — principles retained, trigger updated

- `BLACKSMITH_DESTRUCTION_UX_CANON_20260824.md` — physical UID death, immutable archive, curated memorial, optional new-UID successor, zero power inheritance remain current principles. CURRENT/MAX zero-axis fields are historical.

Current terminal transition:

```text
MAJOR + DAMAGE_EVENT -> DESTROYED
```

Damage event may come from eligible +11+ enhancement failure or eligible delayed customer/world event.

### 3.6 First session / customer causality — partially superseded

- `BLACKSMITH_FIRST_10_MINUTES_CANON_20260824.md` — pacing and STOP/PUSH thesis retained; CURRENT/MAX teaching and old precision wording superseded.
- `BLACKSMITH_PRECISION_CUSTOMER_LINK_CANON_20260824.md` — customer context/no-Best/same-UID delayed result retained; current Precision cadence is +9→+10 only. Customer/world event may cause one-step damage only if that event is eligible.
- current existing `VSContentResultRecord` is implementation reuse evidence for delayed same-UID result shape, not runtime proof of Decision26 event damage.

### 3.7 Precision crafting — responsibilities reused at +10 only

- `BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md` — main-material/method/one-catalyst responsibility may be reused for +10 keyword generation; old +10/+20/+30/+40/+50 cadence and repeated catalyst evolution are partially superseded.
- three machine affix slots remain `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`; player-facing +10 keyword maps to the existing `CATALYST_AFFIX` owner.

### 3.8 Art / Visual

- `BLACKSMITH_ART_DIRECTION_REWORK_DECISION_20260825.md` (`BS-ART-20260825-02`) — historical bridge that reopened style selection.
- `BS-ART-20260825-03` in the current simplified owner supersedes the unresolved selection state with `ILLUSTRATED_WORKSHOP_BOOK / USER_APPROVED_DIRECTION`.
- old 8 approved Visual GDDs remain information-architecture references; CURRENT/MAX/old precision/date-log contents are `SYSTEM_SEMANTICS_STALE`.

## 4. Preserved progression anchors

```text
MIN_LEVEL = +0
MAX_LEVEL = +100
+0~+9 = INVESTMENT_RECOVERY_ZONE
+10 = BREAK_EVEN_RECOVERY_POINT
+11~+100 = PROFITABLE_ENHANCEMENT_ZONE
```

Experience bands remain:

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

Checkpoint floors remain:

```text
CHECKPOINT_FLOORS = [10,30,60,90]
BAND_BOUNDARY != CHECKPOINT_FLOOR
```

These do not restore old durability/failure-family semantics.

## 5. Success / recovery / enhancement supply status

Existing planning success curve and recovery are retained as non-final planning inputs unless a later balance Decision changes them:

```text
+1       100%
+2        97%
+3~+10    95% -> 86%
+11       82%
+12~+30   81% -> 72%
+31~+60   73% -> 69%
+61~+100  69% -> 64%

recovery = +6pp / same-target failure
soft cap 95%
hard guarantee = LEARN2 / BUILD4 / FIRST4 / TENSION5 / HIGH6 / MASTERY7
```

Common reinforcement material enhancement mapping remains current planning input:

```text
+1~20 1
+21~40 2
+41~60 3
+61~80 4
+81~100 5
```

Do not infer the new damage curve from these values.

## 6. Current unresolved gates

```text
DAMAGE_PROBABILITY_CURVE
- exact P(damage advance | enhancement failure, target) for +11~+100
- must be >0 from +11 and monotonic non-decreasing

CUSTOMER_EVENT_DAMAGE_POLICY
- event eligibility
- event-specific probability / deterministic causes
- exact content ownership

MINOR_MAJOR_REPAIR_MODEL
- MINOR repair result/cost
- MAJOR repair result/cost
- whether one repair can remove >1 state
- whether MAJOR needs special overhaul

MAJOR_ENHANCEMENT_ELIGIBILITY
- can MAJOR continue enhancement or require repair first
```

These are not implementation defaults. Old CURRENT/MAX formulas are prohibited as silent fallback.

## 7. Current work order

```text
1. CORE_SIMPLIFICATION_CANON_MIGRATION
2. DAMAGE_PROBABILITY_CURVE
3. MINOR_MAJOR_REPAIR_MODEL + MAJOR_ENHANCEMENT_ELIGIBILITY
4. CUSTOMER_EVENT_DAMAGE_POLICY
5. REPRESENTATIVE_VISUAL_REGENERATION_AFTER_SYSTEM_SYNC
6. CURRENT_PLANNING_COMPLETE user declaration
7. runtime implementation plan refresh and TDD migration
```

## 8. Runtime reality / drift

Current V2 runtime files still encode old fields such as `current_durability`, `max_durability`, `FAIL_CRITICAL_DAMAGE`, old destroyed-history zero axes, and multi-milestone precision. They are implementation facts on current main but **not current desired planning canon** after Decisions25~27.

```text
RUNTIME_IMPLEMENTATION_OF_NEW_CORE = NOT_RUN / BLOCKED
OLD_V2_RUNTIME = IMPLEMENTATION_DRIFT / HISTORICAL_RUNTIME_TRUTH
```

Do not mutate protected product paths while Work Mode remains PLAN.

## 9. Operational synchronization

Meaningful planning changes must update:

```text
GitHub
- BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md
- CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md
- this Authority Index
- directly conflicting current handoff docs

Notion Human
- Project Home
- Enhancement/Durability/Economy owner and L3 views
- Visual Bible

AI/System
- Decision IDs / PR / SHA / evidence ceiling / unresolved gates

Google Sheet
- same-ID compatibility rows only
```

Pre-existing PR #196 remains `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`.

## 10. Evidence ceiling

```text
PLANNING_DESIGN = USER_APPROVED
CURRENT_CANON_MIGRATION = IN_PROGRESS_UNTIL_PR_MERGE
DAMAGE_CURVE_NUMBERS = NOT_FINAL
REPAIR_MODEL = NOT_DECIDED
CUSTOMER_EVENT_DAMAGE_NUMBERS = NOT_FINAL
RUNTIME_IMPLEMENTATION = NOT_RUN / BLOCKED
HUMAN_PLAYTEST = NOT_RUN
ANDROID_ACCESSIBILITY = NOT_RUN
NOTION_CLIENT_GEOMETRY = NOT_RUN
```
