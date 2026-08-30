# Blacksmith AI Production Specification

> **한국어 안내:** 이 문서는 **기술·정본 추적용** AI/구현 명세다. 사람이 게임의 장르, 시점, 핵심 재미와 플레이 흐름을 읽는 기준은 [Blacksmith 사람용 게임 기획서](BLACKSMITH_HUMAN_FACING_GDD_20260828.md)와 연결 PDF다.

> **Document role:** machine-searchable current-canon planning and implementation contract. It is not a replacement for executable code, JSON owners, tests, or runtime evidence.
>
> **Source snapshot:** `main` / `2ba2496f0b8e259c446ae8ed1f09533012c3f303` plus current user routing/review overrides `BS-OPS-20260828-35 / BS-OPS-20260828-36` and precision-tag Decision37 / 2026-08-29 KST.
> **Generated scope:** this is a technical-trace companion to the human-facing GDD and `exports/blacksmith_MASTER_PRODUCTION_GDD_20260828.pdf`; it does not own the human reading experience. Notion is retired from future project work; no new raster, runtime asset, Scene, data, or GDScript change belongs to this document batch.

> **2026-08-30 recurring Precision trace:** `BS-ENHANCE-20260830-38` is the current owner for all ten Precision targets, `ADD_TAG` / `UPGRADE_TAG`, a maximum of three tags, and I–IV growth. The catalog is schema 2. Item V4 migrates the former single catalyst value to a versioned tag collection while preserving the existing `CATALYST_AFFIX` owner. Exact runtime consumers are Main Menu, recurring Precision Workshop, and Customer World Result; their three approved illustrations are locked, registered, and implemented with machine verification. This is not client, Android, accessibility, human visual, performance, or release verification: each remains `NOT_RUN`.

## 00A. RECURRING PRECISION IMPLEMENTATION TRACE

| Technical concern | Current source / evidence boundary |
|---|---|
| Rule owner | `BS-ENHANCE-20260830-38`; targets 10 through 100 at ten-level intervals. |
| Catalog | `BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json`, schema 2; `ADD_TAG` / `UPGRADE_TAG`, cap 3, stage 1–4. |
| Persistence | V4 item migration stores the versioned tag collection in `CATALYST_AFFIX`; old known values migrate without reapplying their effect, pending values remain gated, unknown values fail closed. |
| Runtime consumers | Main Menu background, Precision Workshop state illustration, Customer World Result illustration; exact bindings and asset hashes are registered in the repository visual requirements and asset records. |
| Machine evidence | Current catalog, V4 migration, resolver/action, UI binding, visual-requirement contract, and focused GUT checks are repository machine evidence at the recurring-Precision delivery head. The GUT runner summary is intentionally not repeated here because the known overall runner conclusion is INCONCLUSIVE. |
| Ceiling | Godot client observation, Android device, accessibility, performance, human play, human visual review, release and external rights completion are `NOT_RUN`. |

## 00. CANON SNAPSHOT

| Field | Current value |
|---|---|
| Project | Blacksmith - Android portrait Godot crafting game |
| Current product mode | `CURRENT_CANON_MVP_ACTIVE_BY_USER_DECLARATION_20260826 / IMPLEMENTATION_AND_REVIEW` |
| Primary core | Enhancement tension plus DDD; the recurring player question is `STOP OR PUSH`. |
| Differentiator | The same item UID carries ownership, damage, repair, handoff, actual use, meaningful events, and chronicle through a customer-facing life. |
| Current visual direction | `ILLUSTRATED_WORKSHOP_BOOK / USER_APPROVED_DIRECTION`; warm hand-drawn workshop book, paper/leather/iron/wood material language, readable modern controls. |
| Current project routing | `GITHUB_REPOSITORY_ONLY_CURRENT_CANON`; the repository is both the human-facing GDD and operational source. Notion is historical-only and receives no future read/write. |
| Image execution timing | Consumer metadata first, then `USER_PREAUTHORIZED_AFTER_CONSUMER_REQUIREMENT`; only final visual lock or runtime promotion asks the user. |
| Canonical current owners | `BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`; Decisions 28-32, 34 and 37 JSON/decision owners listed below. |
| Open PR boundary | PR [#196](https://github.com/alsdmlals4-eng/Blacksmith/pull/196) is `OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER`; it is not merged truth. |
| Evidence ceiling | Automated contracts and selected GUT/CI evidence exist. Godot client rendering, Android, accessibility, performance, Human usability, player experience, and release readiness remain `NOT_RUN`. |

### Status vocabulary

`DOCUMENTED` means this specification records the claim. `CONFIRMED` means it is approved by the current source owner. `IMPLEMENTED` means a current repository path exists, not that it matches all current canon. `AUTOMATED_TEST_PASS` needs named passed test evidence. `RUNTIME_VERIFIED`, `UX_VERIFIED`, and `RELEASE_READY` require their own direct evidence and must never be inferred from earlier states.

## 01. SOURCE REGISTRY

| ID | Source / use | Status |
|---|---|---|
| SRC-CAN-01 | `AGENTS.md` | Current authority order, protected scope, test and evidence rules. |
| SRC-CAN-02 | `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md` | Cold-start locator and accepted frontier. |
| SRC-CAN-03 | `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md` | Current player promise, enhancement-first loop and protected rules. |
| SRC-CAN-04 | `docs/planning/BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json` | Decision28 exact conditional damage curve and Decision32 outcome/display ownership. |
| SRC-CAN-05 | `docs/planning/BLACKSMITH_DURABILITY_REPAIR_MODEL_20260826.json` | Decision29 visible durability authority and repair/scar model. |
| SRC-CAN-06 | `docs/planning/BLACKSMITH_REPAIR_ECONOMY_REBASE_20260826.json` | Decision31 test-only repair-cost curve. |
| SRC-CAN-07 | `docs/planning/BLACKSMITH_CUSTOMER_WORLD_EVENT_DAMAGE_POLICY_20260826.json` | Decision30 actual-use event eligibility and damage composition. |
| SRC-CAN-08 | `docs/decisions/BS-ENHANCE-20260828-34_WEAPON_KEYWORD_OWNERSHIP.md` | Grade / Tag / Event taxonomy and `+9→+10` keyword ownership. |
| SRC-CAN-08A | `docs/decisions/BS-ENHANCE-20260829-37_PRECISION_TAG_CATALOG_AND_SELECTION_GATE.md` and `docs/planning/BLACKSMITH_PRECISION_TAG_CATALOG_20260829.json` | First 2×2 Tag content, explicit choice flow, empty-selection block, and placeholder backfill contract. |
| SRC-CAN-09 | `docs/planning/BLACKSMITH_ACTUAL_GAME_IMAGE_CONSUMER_GATE_20260826.json` and `assets/ASSET_MANIFEST.json` | Visual consumer, asset provenance, and validation state. |
| SRC-CAN-10 | `docs/decisions/BS-OPS-20260828-35_GITHUB_ONLY_CANON_AND_IMAGE_EXECUTION_ROUTING.md` | GitHub-only current-canon routing and post-generation visual lock policy. |
| SRC-CAN-11 | `docs/decisions/BS-OPS-20260828-36_EVIDENCE_RESEARCH_AND_ADVERSARIAL_REVIEW_LOOP.md` | Fresh-read, current research, adversarial review, feasibility, and evidence-ceiling procedure. |
| SRC-MIG-01 | `docs/migration/BLACKSMITH_NOTION_TO_GITHUB_MIGRATION_20260828.md` and `docs/migration/BLACKSMITH_NOTION_MIGRATION_MANIFEST_20260828.json` | One-time read-only Notion structure/work-product migration, GitHub destination map, and hash-verified historical visual archive. |
| SRC-IMP-01 | `project.godot`, `scenes/vertical_slice/**`, `scripts/vertical_slice/**` | Current vertical-slice implementation reality. |
| SRC-IMP-02 | `data/vertical_slice/**`, `data/crafting/**`, `tests/gut/unit/vertical_slice/**` | Current data and automated-test reality. |
| SRC-HIS-01 | `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`, R2/R3 Game Bibles, legacy POC scripts | Historical / compatibility evidence only where it conflicts with SRC-CAN owners. |
| SRC-BMK-01 | [Diablo IV itemization update](https://news.blizzard.com/en-us/article/24243142/sanctuary-ignites-with-itemization-systems-changes), accessed 2026-08-28 | Official comparative evidence for choosing an explicit single item-affix result and separate quality path. |
| SRC-BMK-02 | [Last Epoch Support: Forging Potential](https://support.lastepoch.com/hc/en-us/sections/46361196109339-General-Information), accessed 2026-08-28 | Official support index confirms a finite item-forging resource as a distinct craft boundary; no numeric import. |
| SRC-BMK-03 | [Shop Titans on Google Play](https://play.google.com/store/apps/details?id=com.ripostegames.shopr), accessed 2026-08-28 | Official market page for crafting, visitor sale, shop growth, and mobile production-loop comparison. |
| SRC-BMK-04 | [Moonlighter on Steam](https://store.steampowered.com/app/606150/Moonlighter/), accessed 2026-08-28 | Official product page for shopkeeper/day-life, price feedback, crafting/enchanting and villager relation comparison. |
| SRC-BMK-05 | [Potion Permit help](https://playdigious.helpshift.com/hc/en/21-potion-permit/faq/192-what-is-potion-permit-about/), accessed 2026-08-28 | Official example of customer need → diagnosis → gather → make → result loop. |
| SRC-PLT-01 | [Godot Android export](https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_android.html), accessed 2026-08-28 | Official Android export and signing/AAB requirements. |
| SRC-PLT-02 | [Android quality checklist](https://developer.android.com/games/pgs/quality?hl=en) and [Android vitals](https://developer.android.com/games/optimize/vitals), accessed 2026-08-28 | Platform quality, continuity, crash/ANR, memory and bitmap-risk evidence. |

### Source and conflict register

| Conflict ID | Competing claims | Actual implementation reality | Current disposition |
|---|---|---|---|
| DEC-DRIFT-01 | Historical single `+9→+10` Precision vs current recurring ten-gate Precision. | Old data and legacy code contain older milestone vocabulary. | `SUPERSEDED`: Decision38 owns targets `+10` through `+100` at every ten-level boundary. |
| DEC-DRIFT-02 | Historical CURRENT/MAX bands and overhaul formulas vs Decision29 `CURRENT/MAX/BASE_MAX`. | V2 field names may resemble current ones but do not establish semantic compliance. | `SUPERSEDED`: visible numeric authority and derived effective state are Decision29 only. |
| DEC-DRIFT-03 | Catalyst-only Tag identity vs latest direct user rule. | Current placeholder write and legacy method list do not implement the approved recurring flow. | `CONFIRMED`: Decision38 owns recurring add/upgrade cadence; the first 2×2 content and empty-selection behavior remain catalog inputs. |
| DEC-DRIFT-04 | Historical visual-GDD image production and pre-generation approval vs current consumer gate. | Three approved runtime asset families are dynamically bound; client visual review is not run. | `CONFIRMED`: no document gap creates an image. Once complete consumer metadata exists, generation is pre-authorized; final direction/runtime promotion still needs post-generation user lock. |
| DEC-DRIFT-05 | PR #196 proposed precision visitor context vs main. | Draft adds only a test file and has one failed authority check. | `OPEN_DRAFT_READ_ONLY`; do not merge, cite, or treat as implementation. |

## 02. CURRENT PROJECT STATE

### Work 5-stage readback

| Work stage | State | Evidence / boundary |
|---|---|---|
| 1. Intent and canon | `CONFIRMED` | Current owner files and Decisions 25-37. |
| 2. System contract | `CONFIRMED` | Enhancement, durability, repair, event, keyword boundaries, first Tag matrix, and empty-selection policy are current. |
| 3. Representative slice plan | `CONFIRMED` | Slice B: individual `+0→+10`, optional `+11→+15` risk, handoff, brief return beat, same-UID actual-use result. |
| 4. Machine implementation | `PARTIAL / IMPLEMENTATION_DRIFT_RISK` | Vertical-slice classes, scenes, save envelope, GUT contracts and assets exist; exact current-canon parity is not asserted. |
| 5. Player and production proof | `NOT_RUN` | No Godot client, Android, accessibility, performance, or human/player test evidence. |

### Actual playable-surface inventory

| UI ID | Surface | Existing locator | Implementation state |
|---|---|---|---|
| UI-MAIN-001 | Main Menu | `res://scenes/vertical_slice/main_menu.tscn`, `VSMainMenu` | `IMPLEMENTED`; new/continue/settings stub. |
| UI-FORGE-001 | First Forge | `scripts/ui/forging_screen.gd` and first-forge flow | `IMPLEMENTED` historical/V2 surface; current flow parity requires review. |
| UI-WORK-001 | Workshop | `res://scenes/vertical_slice/screens/vs_workshop_screen.tscn`, `VSWorkshopScreen` | `IMPLEMENTED` for numeric durability/repair surface; current canon parity not claimed. |
| UI-RESULT-001 | Customer Result | `res://scenes/vertical_slice/screens/vs_customer_result_screen.tscn`, `VSCustomerResultScreen` | `IMPLEMENTED` presentation surface; current event/content contract parity requires review. |
| UI-PREC-001 | +9→+10 Precision | Only locator / future consumer queue | `NOT_IMPLEMENTED` as an approved current screen. |
| UI-CHR-001 | Item Chronicle | Only locator / future consumer queue | `NOT_IMPLEMENTED`. |

## 03. CONFIRMED DECISIONS

| Decision ID | Confirmed rule | State |
|---|---|---|
| DEC-ENH-25 | Ordinary enhancement success is always `+1`; its single-Precision field is `SUPERSEDED` by Decision38. | `CONFIRMED / PARTIALLY_SUPERSEDED` |
| DEC-DMG-28 | Target `+11/+30/+60/+90/+100` conditional-on-failure damage anchors are `5/6/7/8/10%`; exact piecewise-linear interpolation. | `CONFIRMED / TEST_BUDGET` |
| DEC-REP-29 | `CURRENT/MAX/BASE_MAX` is the only visible durability authority; state is derived from the worse ratio. | `CONFIRMED / TEST_BUDGET` |
| DEC-REP-31 | One repair job after actual damage; current initial curve is a sensitivity-tested budget, not final economy. | `CONFIRMED / NOT_FINAL_BALANCE` |
| DEC-DMG-30 | Handoff itself causes no damage; actual use is required; one roll per event per UID; world event never directly damages MAX. | `CONFIRMED` |
| DEC-ENH-32 | A failed enhancement resolves to exactly `FAILED_HOLD` or `FAILED_DAMAGE`; no downgrade or separate critical. | `CONFIRMED` |
| DEC-CHR-27 | Only meaningful item events enter player Chronicle, never routine dated attempts. | `CONFIRMED` |
| DEC-ENH-34 | Weapon keywords are Grade / Tag / Event. Its single `+10` Tag cardinality is `SUPERSEDED`; Decision38 retains the existing `CATALYST_AFFIX` owner for up to three staged Tags. | `CONFIRMED / PARTIALLY_SUPERSEDED` |
| DEC-ENH-37 | The first 2×2 lineage/method content and empty-selection gate remain historical input. Its target-10-only and single-string fields are `SUPERSEDED` by Decision38 schema 2/V4. | `CONFIRMED / PARTIALLY_SUPERSEDED` |
| DEC-ART-03/04 | Illustrated Workshop Book direction; generated imagery needs actual runtime consumer and is not automatically a final asset. | `CONFIRMED` |

## 04. DESIGN PILLARS

1. **SYS-ENH-001 - Push matters because stopping is valid.** Every preview must make the next attempt's gain, cost, risk, and meaningful loss legible enough that stopping is a player decision, not a hidden-information trap.
2. **SYS-LIF-005 - One weapon remembers.** The UID connects forge, risk, repair, owner, actual use, outcome, and chronicle, so an item is not disposable spreadsheet output.
3. **SYS-CUS-006 - Customers provide purpose, not a combat minigame.** Player judgment is about which work to make and risk, while the world result returns causal evidence rather than an opaque score.
4. **SYS-FDB-009 - Five-level rises mark craft progress.** Every fifth level must visibly raise craft feeling; `+5` is feedback only and `+10` remains the sole special boundary.
5. **UI-UX-001 - Android portrait readability first.** Exact current/max/base-max, reason text, state labels, and touch targets carry the meaning; art cannot replace them.

## 05. PLAYER EXPERIENCE CONTRACT

### Promise chain

`Customer purpose` → `make one named UID work` → `read next enhancement preview` → `stop or push` → `gain +1 or receive a clear hold/damage consequence` → `hand off the same work` → `receive a delayed actual-use result with 2-4 causes` → `repair, continue, retire, or begin a new work`.

The target first memory is not “I clicked a forge many times.” It is “I chose to protect or push *this* weapon, and the world later showed what happened to it.” The emotion curve is anticipation, relief/pride, tension, responsibility, and curiosity about the returned life result.

### First 5 / 15 / 30 minute contract

| UX ID | Time | Player learns | Evidence state |
|---|---:|---|---|
| UX-ONB-001 | First 5 min | Make a first work and see ordinary `+1` feedback; `+1/+2` learn and `+3~+9` build. | `DOCUMENTED`; pacing `UX_VERIFIED: NOT_RUN`. |
| UX-ONB-002 | First 15 min | `+9→+10` is special: choose 불씨/모루 and 날 세우기/경량 담금, then the successful work gains one Tag before `+11` previews first damage-eligible risk. | `CONFIRMED`; precision screen/data content `NOT_IMPLEMENTED`. |
| UX-ONB-003 | First 30 min | Handoff produces a non-economic return beat and an actual same-UID result, causing the next repair/enhancement/new-work choice. | `DOCUMENTED / PARTIAL`; runtime/UX proof `NOT_RUN`. |

## 06. CORE / SESSION / META LOOP

```text
CORE: Forge UID → preview next +1 → STOP or PUSH → clear result → next decision
SESSION: customer purpose → make/upgrade a work → handoff → delayed actual-use result → choose repair/continue/new work
META: build a portfolio of remembered UIDs → unlock later title/content only through approved systems → deepen customer/world consequences
```

`+10` is a safe-no-damage boundary and a single identity moment. `+11` is the first salient voluntary risk. `+100` is terminal enhancement completion, not a reset/prestige loop. The 6-8 minute session figure is a playtest hypothesis, never a hard time limit.

## 07. SYSTEM REGISTRY

| System ID | Name | Current owner | Status |
|---|---|---|---|
| SYS-ENH-001 | Ordinary enhancement and STOP/PUSH | Core simplification canon | `CONFIRMED`; V2 implementation `PARTIAL` |
| SYS-PRE-002 | +9→+10 Precision and weapon Tag | Decision34 / unified contract | `CONFIRMED`; Tag content/write/UI `NOT_IMPLEMENTED` |
| SYS-DUR-003 | Durability and damage | Decision28/29 | `CONFIRMED / TEST_BUDGET`; V2 parity `NOT_CONFIRMED` |
| SYS-REP-004 | Repair and structural scar | Decision29/31 | `CONFIRMED / NOT_FINAL_BALANCE`; V2 parity `NOT_CONFIRMED` |
| SYS-LIF-005 | UID, ownership, destruction, archive | Core canon / save contract | `CONFIRMED`; V2 implementation `PARTIAL` |
| SYS-CUS-006 | Customer/world actual-use result | Decision30 / content contract | `CONFIRMED`; content breadth `PARTIAL` |
| SYS-CHR-007 | Meaningful Chronicle | Decision27 | `CONFIRMED`; player UI `NOT_IMPLEMENTED` |
| SYS-ECO-008 | Enhancement/repair economy | Decision31 and existing budgets | `PARTIAL / TEST_IN_PLAY` |
| SYS-FDB-009 | 5-level craft-rise feedback | Phase1 unified contract | `CONFIRMED`; visual/runtime proof `NOT_RUN` |

## 08. SYSTEM SPECIFICATIONS

### SYS-ENH-001 - Ordinary enhancement and STOP/PUSH

**Player contract.** The player sees a next target, cost, success possibility, failure consequence, and relevant durability state, then chooses STOP or PUSH. The immediate reward is `+1`; the long-term reward is a more capable, more meaningful work. The system exists so risk is a comprehensible judgment, not an optimization-only meter.

| Contract area | Current rule |
|---|---|
| Entry | A non-destroyed item UID and a legal next target. |
| Input | Explicit enhancement attempt; no auto-hidden outcome. |
| Success | Exactly `SUCCESS_LEVEL_DELTA = +1`. |
| Failure | `FAILED_HOLD` or `FAILED_DAMAGE` only. No level downgrade and no critical result. |
| Damage gate | Target `≤ +10`: no enhancement damage. Target `≥ +11`: only after failure, with Decision28 × Decision29 calculation. |
| Exit / recovery | Player may stop at any legal point; actual damage can unlock one repair job; destroyed item is not repairable. |
| Required feedback | Target, exact displayed final probabilities rounded to one decimal, resource cost, durable state, result, and next legal action. |
| Implementation locators | `scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd`, `scripts/vertical_slice/services/vs_enhancement_action_service.gd`, `scripts/vertical_slice/ui/vs_workshop_screen.gd`. Existing paths are implementation reality, not parity certification. |
| Acceptance | Same supplied deterministic rolls always resolve to one legal result; `+10` or lower cannot damage; `+11`+ never produces downgrade/critical; save is atomic. |

### SYS-PRE-002 - Recurring Precision and Tag growth

**Player contract.** At every ten-level Precision boundary from `+9→+10` through `+99→+100`, the player makes an attempt-local choice. The first gate permits `ADD_TAG`; later gates permit a compatible add below cap or `UPGRADE_TAG` for a stage I–III Tag. Each success gives exactly one weapon-owned growth action; it does not create player keywords, titles, Grade, Event, or a fourth slot.

| Field / rule | Contract |
|---|---|
| Trigger | `target_level` is one of `10,20,30,40,50,60,70,80,90,100`; entry is target minus one. |
| Storage | Existing `CATALYST_AFFIX` owns a V4 versioned collection of at most three unique staged Tag entries. |
| Resolution | First gate is `ADD_TAG` only; later gates use `ADD_TAG` or `UPGRADE_TAG`. A success advances exactly one selected Tag action. |
| Isolation | `GRADE_AFFIX` and `CHRONICLE_AFFIX` cannot be written, changed, or selected by the method. |
| Approved catalog | 불씨/모루 계보 × 날 세우기/경량 담금의 2×2 Tag 표. 선택은 every-Precision attempt-local input이며, 첫 gate의 빈 입력과 duplicate/cap/mastered choices are blocked before cost or roll. |
| Unresolved | 실제 UI/저장 write 구현, Godot runtime/Android/사람 사용성 증거. |
| Prohibited | Placeholder Tag, invented keyword, player title, event keyword, universal damage protection, fourth affix slot. |
| Required future tests | One valid combination returns one known Tag; invalid / absent lineage follows an explicitly approved policy; failure creates no Tag; Grade/Event remain byte-for-byte unchanged. |

### SYS-DUR-003 - Durability and damage

**Player contract.** The player can understand whether a work is normal, minor, major, or destroyed from visible numbers. They feel a worsening item life without hidden double penalties.

```text
0 <= CURRENT <= MAX <= BASE_MAX
current_ratio = CURRENT / MAX
structural_ratio = MAX / BASE_MAX
effective_ratio = min(current_ratio, structural_ratio)
NORMAL = 1.00; MINOR = (0.50, 1.00); MAJOR = (0, 0.50]; DESTROYED = CURRENT == 0
```

| State | Success modifier | New ordinary effect | Failure-damage multiplier |
|---|---:|---:|---:|
| NORMAL | 0pp | ×1.00 | ×1.00 |
| MINOR | -3pp | ×0.90 | ×1.25 |
| MAJOR | -7pp | ×0.75 | ×1.75 |

These values are `TEMP_TEST_BUDGET`, not release balance. A hard guarantee remains truly 100%. The UI must display a final attempt chance rounded to one decimal but resolve exact values. One actual event causes at most one damage event for the UID.

### SYS-REP-004 - Repair and scar

**Player contract.** A real loss opens one concrete chance to restore an item, but restoration may leave an understandable structural mark. It should motivate another decision, not add a routine tax.

| Rule | Contract |
|---|---|
| Eligibility | `0 < CURRENT < MAX` and `REPAIR_JOB_AVAILABLE`; destroyed and full-durability repair are forbidden. |
| Job consumption | Consume repair job at repair start. |
| Quality budget | Excellent 20% → MAX 100%; Standard 60% → MAX 75%; Poor 20% → MAX 50%. |
| Scar | Pre-repair effective state × enhancement band determines a temporary `MAX -1` trigger chance; skip scar with no positive CURRENT gain, no reroll. |
| Initial cost | `ceil(R_BAND * (0.05 + 0.65 * ((MAX-CURRENT)/BASE_MAX))) + 1 reinforcement`. Sensitivity `b=.50/.65/.80` remains required. |
| Future acceptance | Quote and apply share one resolver; no repair job can be duplicated with reload/retry; one repair cannot cause zero positive CURRENT recovery. |

### SYS-LIF-005 - UID, ownership, destruction, archive

An item UID is born once and retains birth facts, enhancement, meaningful change ledger, ownership/handoff, actual-use results, repair/scar, destruction reason, and predecessor relation. A destroyed physical item cannot be revived, but its history persists. A successor is a new UID and inherits no power or chronicle data.

`DAT-SAVE-001` uses the current V4 item schema in `data/vertical_slice/vertical_slice_preset.json`: deterministic birth/run seeds, append-only contiguous ledger, resolved events, temp-flush-rename backup, V3-to-V4 migration on read, and V1 fail-closed. Known legacy Tag effects do not apply twice; pending legacy placeholders remain gated; unknown values fail closed.

### SYS-CUS-006 - Customer/world actual-use result

Customers make the work meaningful before and after the forge; they do not turn Blacksmith into direct exploration or combat. A valid event requires actual use of the same UID. Purchase or handoff alone never damages the item. Mission outcome and damage are independent axes; an event has at most one damage roll for a UID.

`CNT-ADVENTURER-01 / NADIA_VENN` is the starter representative: `SURVIVAL_AND_RECOVERY` with `EXPEDITION_RETURN_STATE`, `RECOVERY_STATE`, and `ITEM_UID_LIFECYCLE_STATE`. A result needs 2-4 causal reasons and one primary next action. Generic Tag cannot reduce a DIRECT event; explicitly causal relevant item property may lower a probabilistic profile by at most one step.

### SYS-CHR-007 - Meaningful Chronicle

Chronicle is a player-facing explanation layer for creation, Tag/keyword, actual damage, MAX-scar repair, handoff, world result, destruction, and comparable meaningful events. Routine enhancement attempts and date-spam are prohibited. `UI-CHR-001` is not implemented; therefore this contract does not pretend that a current player can inspect the history surface.

### SYS-ECO-008 and SYS-FDB-009

Economy supports enhancement choices, not passive grind. Existing attempt cost and reinforcement supply are `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE`; legacy expected-cost tables require recalculation after current damage/repair play evidence. Every 5 levels must provide a craft-rise feedback beat; `+5` is feedback only, while every ten-level target from `+10` through `+100` is a Precision event. Required production proof is a representative animation/VFX/SFX and readability test, currently `NOT_RUN`.

## 09. CONTENT REGISTRY

| Content ID | Customer / content | Purpose | Current status |
|---|---|---|---|
| CNT-ADVENTURER-01 | Nadia Venn | Starter same-UID expedition survival/recovery result. | `DOCUMENTED / PARTIAL IMPLEMENTATION` |
| CNT-ADVENTURER-02 | Toren March | Journey arrival, route exposure and item lifecycle. | `DOCUMENTED` |
| CNT-SOLDIER-01 | Marek Olden | Small-lot standard order and mission result. | `DOCUMENTED` |
| CNT-COLLECTOR-01 | Ersa Roen | Exhibition reception, thesis fit, public item legacy. | `DOCUMENTED` |
| CNT-GLADIATOR-01 | Cassia Bellan | Arena result and equipment contribution, not direct combat. | `DOCUMENTED` |
| CNT-NOBLE-01 | Ceremonial Noble | Ceremony readiness and heirloom treatment. | `DOCUMENTED` |
| CNT-SOLDIER-02 | Liana Berg | Commander mission and field legacy. | `DOCUMENTED` |
| CNT-COLLECTOR-02 | Sedric Vael | Archive accession, provenance, custody legacy. | `DOCUMENTED` |
| CNT-GLADIATOR-02 | Kyle Varen | Veteran return / keep-in-service vs retire-replace. | `HISTORICAL_REUSE_REFERENCE / DOCUMENTED` |

## 10. CONTENT SPECIFICATIONS

### CNT-ADVENTURER-01 - Nadia Venn starter slice

| Item | Contract |
|---|---|
| Entry | First forged same UID is available for handoff; Nadia's public identity is `ELITE`, but exact numeric capability profile is explicitly `SEPARATE_CANON_SOURCE_REQUIRED`. |
| Player judgment | Read disclosed purpose, constraint, and known situation; decide whether the work is ready at `+10` or worth a voluntary `+11` risk. |
| Outcome | Handoff → one brief return beat → actual expedition use → `CONTENT_RESULT_V1` record with exactly 2-4 causal reasons and one next action. |
| Damage boundary | No damage at handoff. Eligible actual use may produce at most one UID damage event under SYS-CUS-006 and SYS-DUR-003. |
| Prohibited | Inventing Nadia's capability values, best badge, universal fit score, direct expedition play, automatic Tag/Chronicle farming. |
| Data / implementation locators | `data/vertical_slice/customers/nadia_venn.json`; `data/vertical_slice/content_result_contract.json`; `VSContentResultRecord`, `VSCustomerActualUseActionService`, `VSCustomerWorldEventResolver`. |
| Acceptance | Result rejects an unrelated UID, forbids a score/reward field, has valid axes/reasons/next action, and does not reroll on load. |

### Content production template

Each additional content row must specify: customer goal and visible constraint; trigger and exit; required work UID; allowed result axes; 2-4 causal reasons; one next action; event damage eligibility; no-direct-combat boundaries; required copy/UI/audio/visual consumers; data owner; save impact; acceptance tests; and `DOCUMENTED / IMPLEMENTED / RUNTIME_VERIFIED / UX_VERIFIED` evidence separately. No content may use a hidden total score, automatic artistry growth, automatic Chronicle grants, or fixed universal result dates.

## 11. UI/UX AND INPUT CONTRACT

| UI / UX ID | Goal and required information | Input / feedback | State |
|---|---|---|---|
| UI-MAIN-001 | Start/continue without misrepresenting save state. | New Game, Continue, Settings stub; visible save status. | `IMPLEMENTED / UX_NOT_RUN` |
| UI-FORGE-001 | Establish first work and ordinary forge feedback. | Touch forge; clear progress/result. | `PARTIAL IMPLEMENTATION` |
| UI-WORK-001 | Compare exact durability and repair availability before action. | Enhancement / repair actions; disabled/error states communicate why. | `IMPLEMENTED / CURRENT_PARITY_NOT_CONFIRMED` |
| UI-PREC-001 | Make the lineage + method choice and one resulting Tag intelligible. | Explicit lineage/method selection, preview, confirm/cancel; success/failure result. | `NOT_IMPLEMENTED` |
| UI-RESULT-001 | Explain returned customer outcome and next action. | Continue/back action; 2-4 reasons, damage state, next action. | `IMPLEMENTED / UX_NOT_RUN` |
| UI-CHR-001 | Browse only meaningful UID events. | Open detail, filter/read, close. | `NOT_IMPLEMENTED` |

**Accessibility and touch rules.** Portrait target is `720×1280` logical viewport with orientation locked portrait. Status must be text-plus-icon/shape, never color alone. A destructive or irreversible-looking push requires an explicit confirmation only when that interaction has been approved; duplicate taps must be prevented at resolver/service level. Every disabled control states why, error recovery retains the selected UID, and target touch size is at least the existing project 48dp policy. Current Android, screen-reader, contrast, large-text, motion, and device safe-area evidence is `NOT_RUN`.

## 12. VISUAL ASSET CONSUMER MATRIX

| AST ID | Asset | Actual consumer | Status and boundary |
|---|---|---|---|
| AST-WKS-001 | `ASSET-WORKSHOP-BACKGROUND-V2` | `VSWorkshopScreen`; `VSMainMenu` dynamic override | `PROJECT_ASSET_APPROVED`, static/dynamic binding recorded; Godot client/Android/accessibility/human visual validation `NOT_RUN`; release rights pending. |
| AST-DUR-002 | `ASSET-WORKPIECE-DURABILITY-STATE-ATLAS-V1` | `WorkshopLayout/WorkpieceDurabilityHero` | Four state cells; native numeric authority remains primary; dynamic binding recorded, visual validation `NOT_RUN`. |
| AST-FORGE-003 | `ASSET-FIRST-FORGE-BACKGROUND-V1` | `ForgingScreen / FirstForgeIllustratedBackground` | Project-approved runtime family; readability veil; client visual validation `NOT_RUN`. |
| AST-REF-004 | `ASSET-ILLUSTRATED-WORKSHOP-BOOK-REFERENCE-V1` | None by design | Approved production reference, never a runtime/marketing substitute. |
| AST-MKT-005 | Key art / app icon masters | None by design | Release drafts, not platform-ready; rights/terms/safe-zone work required. |
| AST-PREC-006 | Precision visual treatment | No exact consumer slot | `DEFERRED`; do not generate until UI-PREC-001 defines its consumer, states, aspect, and fallback. |
| AST-CHR-007 | Chronicle visual treatment | No exact consumer slot | `DEFERRED`; do not generate until UI-CHR-001 exists. |

All imagery follows the same grammar: warm illustrated workshop book; hand-drawn paper/leather/iron/wood; calm warm light; readable native Godot UI above it. Fake generated gameplay screenshots, image-only system truth, copied game identity, and promotion of reference art to runtime are prohibited. Current asset rights are `RELEASE_BLOCKED_UNVERIFIED` until terms and distribution rights are evidenced.

## 13. AUDIO CONSUMER MATRIX

No approved current music/SFX/voice asset manifest or runtime audio consumer is present in the fresh-read scope. Therefore:

| AUD ID | Required future consumer | Required feedback | State |
|---|---|---|---|
| AUD-FORGE-001 | Ordinary enhancement | anticipation, hit, success, hold, damage | `NOT_IMPLEMENTED` |
| AUD-PREC-002 | +9→+10 precision | choice lock, resolve, Tag reveal | `NOT_IMPLEMENTED` |
| AUD-REP-003 | Repair | quote accepted, quality, structural scar | `NOT_IMPLEMENTED` |
| AUD-RES-004 | Customer result | return, outcome polarity, next-action cue | `NOT_IMPLEMENTED` |

Audio must not be invented as an approved asset. Each future row needs source/provenance, player function, platform mix/readability, runtime path, and state-specific trigger before production.

## 14. TECHNICAL ARCHITECTURE

```text
MainMenu (VSMainMenu)
  → run initializer / first forge completion
  → BlacksmithApp (VSApp)
      → WorkshopScreen (VSWorkshopScreen)
          → VSEnhancementActionService → VSEnhancementResolver
          → VSWorkshopMaintenanceService → VSRepairResolver
          → VSSaveService / VSSaveEnvelope
      → CustomerResultScreen (VSCustomerResultScreen)
          → VSCustomerActualUseActionService → VSCustomerWorldEventResolver
```

| Layer | Current path(s) | Responsibility |
|---|---|---|
| Domain | `scripts/vertical_slice/domain/vs_item.gd`, `vs_save_envelope.gd`, `vs_ledger_entry.gd`, `vs_content_result_record.gd` | UID facts, durability/item state, serialized envelope, immutable result record. |
| Resolver | `scripts/vertical_slice/resolvers/**` | Pure-ish legality, damage, repair, precision, customer-context/event outcome calculations. |
| Service | `scripts/vertical_slice/services/**` | Coordinates action, ledger append, save, and state changes. |
| UI | `scripts/vertical_slice/ui/**` | Presents state and translates player input; must not become numeric source of truth. |
| Data | `data/vertical_slice/**`, `data/crafting/**` | Versioned preset, customer and content contracts, current/historical data fixtures. |
| Test | `tests/gut/unit/vertical_slice/**`, Python contracts | GUT unit/integration and document/canon regression contracts. |

Existing architecture is a reusable implementation baseline, not permission to import legacy semantics into current features. `.tscn`, resources, and project settings require the project-authoring provenance rules; this documentation task modifies none.

## 15. DATA CONTRACTS

| DAT ID | Owner / essential fields | Current contract |
|---|---|---|
| DAT-ITEM-001 | `VSItem` | UID, level, birth facts, `CURRENT/MAX/BASE_MAX`, lifecycle state, no invented Tag matrix. |
| DAT-SAVE-001 | `VSSaveEnvelope` | V3; deterministic seeds, resolved events, append-only ledger, backup recovery; V2 migrate on read, V1 fail closed. |
| DAT-RESULT-001 | `CONTENT_RESULT_V1` | event ID, source decision, content/customer, day, item refs, result axes, 2-4 causal reasons, one next action; score/total/reward probability prohibited. |
| DAT-PREC-001 | Future current Tag resolution | `catalyst_lineage_id`, `precision_method_id`, `tag_id`; exact enum content and empty-lineage behavior `USER_DECISION_REQUIRED`. |
| DAT-DUR-001 | Decision29 model | immutable `BASE_MAX`; legal `CURRENT/MAX` ranges; derived effective state is never separately persisted as hidden authority. |
| DAT-EVENT-001 | Decision30 event packet | actual-use flag, item UID, profile/cause, resolved-once identifier; direct/max-damage constraints. |

## 16. SCENE MAP

| Scene ID | Path | Entry / exit | State |
|---|---|---|---|
| SCN-MAIN-001 | `res://scenes/vertical_slice/main_menu.tscn` | Project entry → new/continue first forge/workshop | `IMPLEMENTED` |
| SCN-APP-002 | `res://scenes/vertical_slice/vertical_slice_app.tscn` | Hosts workshop/result screens | `IMPLEMENTED` |
| SCN-WORK-003 | `res://scenes/vertical_slice/screens/vs_workshop_screen.tscn` | Item state → enhancement/repair/result | `IMPLEMENTED / CURRENT_PARITY_REVIEW_REQUIRED` |
| SCN-RESULT-004 | `res://scenes/vertical_slice/screens/vs_customer_result_screen.tscn` | Resolved result → next action | `IMPLEMENTED / UX_NOT_RUN` |
| SCN-PREC-005 | Not yet approved | +9→+10 entry → outcome | `NOT_IMPLEMENTED` |
| SCN-CHR-006 | Not yet approved | UID detail → meaningful history | `NOT_IMPLEMENTED` |

## 17. SCRIPT RESPONSIBILITY MAP

| Script / class | Public responsibility | Do not own |
|---|---|---|
| `VSEnhancementResolver` | Resolve a legal attempt from item/target/rolls. | UI copy, hidden manual probability. |
| `VSEnhancementActionService` | Commit a resolved attempt, ledger, save boundary. | Drawing or player-facing styling. |
| `VSRepairResolver` | Quote/apply repair and structural consequence. | Store price tables beyond approved model. |
| `VSItem` | Item UID and durable state mutations with invariants. | Customer narrative or UI. |
| `VSSaveService` | Atomic persistence/load/migration boundary. | Rerolling resolved event outcomes. |
| `VSCustomerWorldEventResolver` | Actual-use event/damage eligibility and outcome packet. | Direct combat simulation or universal Tag bonus. |
| `VSWorkshopScreen` | Display current item and dispatch actions. | Durable numeric authority. |
| `VSApp` | Screen orchestration and app state transition. | Rule calculation. |

## 18. SIGNAL AND EVENT FLOW

| EVT ID | Emitter → receiver | Payload / timing | Required invariant |
|---|---|---|---|
| EVT-ENH-001 | UI → enhancement service/resolver | selected UID, next target, deterministic/live rolls | Disable duplicate input until resolution. |
| EVT-ENH-002 | resolver → UI/save | one of `SUCCESS`, `FAILED_HOLD`, `FAILED_DAMAGE` | Exactly one result and no downgrade/critical. |
| EVT-REP-001 | UI → maintenance/repair resolver | UID, resources, quality/scar rolls | Job consumed exactly once at start. |
| EVT-USE-001 | customer result flow → actual-use resolver | event ID, UID, actual-use profile, damage roll | Purchase/handoff alone rejected; UID result only once. |
| EVT-SAVE-001 | service → save service | candidate V3 envelope | Temp-flush-rename/backup; resolved results do not reroll. |
| EVT-UI-001 | app → hosted screens | state transition | One active surface; return preserves selected UID context. |

## 19. STATE MACHINES

### Item life state

```text
BIRTH → ACTIVE → HANDOFF → ACTUAL_USE_RESULT → ACTIVE
                          ↘ DAMAGE → REPAIR_ELIGIBLE → ACTIVE
ACTIVE / HANDOFF / RESULT → DESTROYED → ARCHIVED
ARCHIVED → optional NEW_UID_SUCCESSOR (no power/history transfer)
```

### Enhancement attempt state

```text
PREVIEW → CONFIRM → RESOLVE → SUCCESS(+1) | FAILED_HOLD | FAILED_DAMAGE
FAILED_DAMAGE → derived durability state → optional one repair job
```

### Precision state (future)

```text
ELIGIBLE_AT_PLUS9 → READ_LINEAGE_AND_METHOD → PREVIEW → CONFIRM
→ success at each eligible Precision target: exactly one selected add or upgrade | failure: no Tag growth
```

The precision state machine and first 2×2 catalog are `DOCUMENTED / CONFIRMED` at rule level but `NOT_IMPLEMENTED` at UI/data-content level.

## 20. SAVE/LOAD CONTRACT

Save/load must preserve UID, birth facts, level, exact durability fields, meaningful ledger, resolved events, repair-job state, ownership and content-result references. Load must not reroll a resolved attempt, repair quality, scar, or world event. The active item schema is V4 and migrates V3 catalyst values into the existing `CATALYST_AFFIX` versioned collection; V1 fails closed. A known legacy Tag becomes one seed entry without reapplying its old effect, a pending legacy placeholder remains gated for its defined no-cost correction, and an unknown value remains unreadable and fail closed. Never infer or synthesize a Tag from legacy method history.

## 21. IMPLEMENTATION TRACEABILITY

| Player need | System / content | UI / asset | Code/data/test evidence | State |
|---|---|---|---|---|
| Stop or push with clear risk | SYS-ENH-001 | UI-WORK-001 | `VSEnhancementResolver`, action service, `test_vs_enhancement_resolution.gd` | `IMPLEMENTED / CURRENT_PARITY_PARTIAL` |
| Understand damage/repair | SYS-DUR-003, SYS-REP-004 | UI-WORK-001, AST-DUR-002 | `VSItem`, `VSRepairResolver`, workshop screen, durability/repair GUT suites | `IMPLEMENTED / UX_NOT_RUN` |
| First work enters core loop | UX-ONB-001 | UI-MAIN-001, UI-FORGE-001, AST-FORGE-003 | `VSMainMenu`, `VSFirstForgeCompletionService`, first-forge tests | `IMPLEMENTED / UX_NOT_RUN` |
| Same UID returns from the world | SYS-CUS-006, CNT-ADVENTURER-01 | UI-RESULT-001 | content result JSON, event resolver/action service, result-screen tests | `PARTIAL` |
| One +10 Tag reflects player choice | SYS-PRE-002 | UI-PREC-001, AST-PREC-006 | Decisions34/37, JSON catalog, and unified contract | `CONFIRMED / NOT_IMPLEMENTED` |
| Player reads meaningful history | SYS-CHR-007 | UI-CHR-001, AST-CHR-007 | Decision27 and ledger concepts | `CONFIRMED / NOT_IMPLEMENTED` |

## 22. TEST AND QA CONTRACT

| QA ID | Verification | Current result |
|---|---|---|
| QA-CAN-001 | Python current-authority and core-simplification contracts | `AUTOMATED_TEST_PASS` in the snapshot’s recent document PR checks. |
| QA-VS-002 | GUT vertical slice domain/resolver/screen suites | Existing test files are present; exact full local rerun is required for any code change. |
| QA-SAVE-003 | Save migration, same UID, deterministic resolved events, backup recovery | Contract documented in preset; test evidence must be cited per exact run. |
| QA-PREC-004 | New Tag combination matrix, failure/no-write, Grade/Event isolation, empty-lineage policy | `CONTRACT_READY / RUNTIME_NOT_IMPLEMENTED`. |
| QA-UX-005 | Five-minute comprehension, +10 identity recognition, +11 STOP/PUSH understanding, returned-result causality | `NOT_RUN`. |
| QA-AND-006 | Android portrait safe area, 48dp targets, contrast/large text, rotation, device load | `NOT_RUN`. |
| QA-REL-007 | Rights/terms, AAB/signing, content rating and Google Play evidence | `NOT_RUN / RELEASE_BLOCKED_UNVERIFIED`. |

### Required manual test scenarios

1. New Game → First Forge → Workshop runs without losing the selected UID.
2. At `+9`, then again at every later Precision boundary, the player can read the legal add/upgrade choice before confirmation; at success exactly one valid Tag action is written; at failure none is written.
3. At `+11`, preview communicates success, hold, and damage outcome in mutually exclusive terms; player can stop without penalty.
4. Verify `5/5/5`, `4/4/5`, `2/2/5`, `1/1/5` presentation and actual modifiers.
5. Actual customer use only, not handoff, can produce one damage event; result has the same UID, 2-4 reasons, and one next action.
6. Kill/restart/load cannot duplicate repair jobs or reroll resolved outcomes.
7. On target Android devices, check 360×640 and 720×1280 logical layouts, font scaling, contrast, one-hand reach, and tap recovery.

## 23. VERTICAL SLICE DEFINITION

**Active playable slice: Slice B.** Make one UID weapon; progress ordinary `+0→+10`; experience craft-rise beats at each five levels; at `+9→+10` choose from the approved 2×2 Precision Tag catalog; choose STOP or PUSH at `+11→+15`; hand off; receive one brief actual-use result; use it to decide repair/continue/new work.

| Hypothesis | Risk | Evidence required |
|---|---|---|
| Fun | Does `+11` make stopping feel like agency, not avoidance? | 5+ human think-aloud tests, choice distribution and reasons. |
| Identity | Does a visible three-tag, I–IV growth board make the work memorable without turning it into a generic loot system? | Comprehension test and Tag recall after result return. |
| Production | Can customer return content be produced with 2-4 causal reasons and one next action without bespoke system drift? | Nadia slice plus two content rows using the same template. |
| Technical | Can V4 save preserve migrated Tags, results, and repair idempotently across restart? | Automated and Godot runtime save/load evidence. |
| Visual | Can native UI remain legible over approved workshop art at actual portrait gameplay size? | Client capture plus Android/accessibility/human visual QA. |

## 24. RISKS AND BLOCKERS

| Risk ID | Risk | Class | Disposition / next validation |
|---|---|---|---|
| RSK-001 | Current placeholder write and legacy method list can diverge from the approved 2×2 Tag catalog. | Product/technical | `IMPROVE`: replace only through Decision37's TDD, block empty selection, and backfill placeholder once. |
| RSK-002 | V2 runtime may drift from current durability/failure/precision canon despite similar field names. | Technical/canon | `TEST`: contract-to-code audit at exact head before implementation. |
| RSK-003 | Customer life becomes a feature list rather than returned consequence. | Fun/content | `TEST`: playtest causal recall and next-action comprehension. |
| RSK-004 | Repair economy is accepted test budget, not player-validated price. | Economy | `TEST_IN_PLAY`: sensitivity then human play. |
| RSK-005 | Runtime asset binding exists but visual usability is unverified. | UX/visual | `TEST`: client capture, Android, accessibility/human QA. |
| RSK-006 | AI asset commercial/distribution terms and platform profile are incomplete. | Release/rights | `MITIGATE`: current terms and per-asset rights evidence before shipping. |
| RSK-007 | PR #196 may be mistaken for accepted implementation. | Process | `MONITOR`: retain read-only, exclude from current architecture claims. |
| RSK-008 | Mobile production scope expands into shop tycoon, direct combat, or dense affix inventory. | Scope | `REJECT`: preserve enhancement-first, customer-causality support role. |

## 25. USER DECISION REQUIRED

| Decision | Why needed | Minimum options / recommended boundary |
|---|---|---|
| DEC-PREC-35/36 | **결정 완료** by `BS-ENHANCE-20260829-37`. | 2×2 composite Tag, explicit no-default selection, block before cost/roll, no fourth slot. |
| DEC-UI-37 | UI-PREC-001 entry/exit and required preview copy. | Keep screen as a short choice/confirm/result surface within Workshop flow; implementation contract now supplies required information. |
| DEC-UX-38 | Define Chronicle screen entry and readable event grouping. | Meaningful event timeline only; no routine attempt spam. |
| DEC-PLAY-39 | 사람 플레이 검수는 사용자 지시로 이번 구현 계약의 완료 조건에서 제외. | 실제 수행 전 `NOT_RUN`; 나중에 제품 재미 검증을 재개할 때만 protocol을 결정한다. |

## 26. IMPLEMENTATION QUEUE

1. Implement `DAT-PREC-001` and resolver/write isolation from Decision37's current JSON/contract owner; run GUT/Python and exact placeholder-backfill checks.
2. Implement UI-PREC-001 inside the current Workshop flow; use native `Control` UI and add no precision raster.
4. Audit V2 enhancement/durability/repair paths against Decisions28/29/31/32; correct only approved drift.
5. Deliver Nadia actual-use result to runtime with same-UID and causal reason validation; then author two reusable content rows.
6. 사람 플레이 검수는 사용자 지시로 이번 구현 계약의 완료 조건에서 제외한다. Android/UI visual QA는 실행할 때만 evidence를 추가한다.
7. Complete release rights/platform profile, AAB signing/export and store-quality gates last.

## 27. CHANGE LOG

| Date | Change | Scope |
|---|---|---|
| 2026-08-28 | Created source-snapshot AI production specification paired with the user PDF. | Documentation only; source main `b4a3b01`. |
| 2026-08-28 | Records Decision34 supersession: Tag is resolved by catalyst lineage plus precision method. | Current canon; no runtime Tag write/UI added. |
| 2026-08-28 | Records approved runtime asset families and their evidence ceiling. | No new image generation or Notion output. |
| 2026-08-28 | Adds `BS-OPS-20260828-35`: GitHub-only current canon and user-preauthorized candidate generation after consumer requirements. | Historical Notion records remain non-current; post-generation lock remains required for final direction/runtime promotion. |
| 2026-08-28 | Completes the one-time Notion-to-GitHub migration receipt and preserves eight historical Visual GDD binaries with exact hashes. | No future Notion read/write; archived boards are non-runtime and cannot override current canon. |
| 2026-08-29 | Adds `BS-ENHANCE-20260829-37`: first 2×2 Precision Tag catalog, explicit empty-selection block, no-new-field rule, and placeholder backfill contract. | Documentation/data contract only; no Godot code/data/Scene change yet. |

## Appendix A. Benchmark disposition

| Reference | Observation | ADOPT / ADAPT / REJECT | Blacksmith application and validation |
|---|---|---|---|
| Diablo IV Tempering/Masterworking | Official update separates explicit selected affix customization from a quality/masterwork path. | `ADAPT` | One explicit Tag result at +10, separated from ordinary enhancement. Reject its broad loot-scale, capstone randomness, and numeric economy. Validate Tag comprehension and no Grade/Event contamination. |
| Last Epoch Forging Potential | Crafting boundary is a distinct item-level resource in official support information. | `REJECT` as a new resource | Blacksmith already owns durability/repair risk; adding forging potential would duplicate the decision. Keep only the principle that the consequence boundary must be readable. |
| Shop Titans | Mobile craft/sell/shop expansion supports a broad tycoon loop. | `REJECT` broad tycoon/guild/market loop; `ADAPT` clear visitor-purpose framing | Do not add multiplayer market, guild, or expanding blueprint treadmill to MVP. Validate that customer purpose increases willingness to make a risk decision. |
| Moonlighter | Shopkeeping, careful price setting, crafting/enchanting and villagers create a repeated day-life identity. | `ADAPT` item-to-person return loop | Use same UID return and customer context, not dungeon combat or price-haggle simulation. Validate remembered causal result after one session. |
| Potion Permit | Diagnosis → gather → make → cure gives each resident a legible need/result chain. | `ADAPT` | Customer asks and returned result should expose a small causal chain, not a hidden total score. Validate players can name a cause and next action. |
| Android/Godot official guidance | AAB/signing/export, stability/ANR/memory/bitmap monitoring and quality are distinct release requirements. | `ADOPT` release gate | Preserve `NOT_RUN` until actual Android export/device telemetry exists; no release claim from headless tests. |

## Appendix B. Non-goals

- Direct player combat, dungeon exploration, army/guild micromanagement, betting, a general shop-tycoon market, player keyword/title from +10, generic affix A/B slots, and prestige/reset after +100.
- Any automatic current image generation for a planning/document gap in this two-artifact work package.
- Treating existing automation, an image file, or a Notion record as human UX, runtime visual, Android, or release evidence.
