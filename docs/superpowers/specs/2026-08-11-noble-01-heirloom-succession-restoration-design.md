# NOBLE_01 Heirloom Succession Restoration Design

## Status

- Decision: `BS-CONTENT-20260811-06`
- R3–R7 slot: `6/10`
- Scope: planning canon only
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`
- User direction: approved the recommended `NOBLE_01 / CEREMONIAL_NOBLE / HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY` direction after benchmark and adversarial review.

## Goal

Promote the existing `CEREMONIAL_NOBLE` representative into the first dedicated noble detailed content and prove that restoration can be a smithing decision about how much history to preserve, not a universal “restore everything to maximum” optimization.

## PRE_WORK_RESEARCH_PACKET

```yaml
PRE_WORK_RESEARCH_PACKET:
  checked_at_kst: 2026-08-11
  base_main_sha: 7ce96181d0a97930300fcc6d383dacc75ad08f6a
  project_main_sha: 42469f6e2058efea464755ac44bec8bcd1154f0b
  open_pr_inventory: "PR #81 only; REFERENCE ONLY / DO NOT MERGE"
  google_sheet_state: "R3_R7_DESIGN_ACTIVE / 5_OF_10; Decision05 synced; product BLOCKED; Task3 NOT_APPROVED; derived hub/product-direction drift observed"
  work_type: "game content design / heirloom lifecycle / restoration decision UX"
  benchmark_sources:
    - "American Institute for Conservation — Code of Ethics and Guidelines for Practice"
    - "The Metropolitan Museum of Art — Royal Presentation Sword / Arms and Armor collection context"
    - "Potion Craft: Alchemist Simulator — Steam product page"
    - "Blacksmith Master — Steam product page"
  adopt:
    - "examine actual object condition/history before intervention"
    - "document treatment and preserve evidence of prior life"
    - "customer request leads to a crafted/treatment decision and observable consequence"
  adapt:
    - "professional conservation's suitability/nonintervention idea becomes a game choice about justified smith intervention depth"
    - "ceremonial/presentation arms demonstrate value beyond combat performance without creating a prestige score"
  reject:
    - "literal museum-conservation simulation or specialist scientific workflow"
    - "production-chain/staff/shop-management expansion"
    - "house prestige, authenticity, succession, or restoration aggregate score"
    - "full restoration or highest Artistry as universal best answer"
  differentiator: "Blacksmith lets one existing UID carry visible repairs, damage, provenance, and ceremony consequences forward; the player chooses what to preserve and what to repair rather than maximizing a clean-state score."
  canon_conflict_check: "Ersa/Collector01 remains exhibition evidence/provenance selection authority; Noble01 owns intervention-depth judgment on an heirloom before succession. No direct content-owner collision when these boundaries are preserved."
  adversarial_precheck: "collector overlap, prestige-score drift, restoration-max dominance, history erasure, progression farming, UID replacement, noble-house/diplomacy drift"
  remaining_uncertainty: "exact treatment thresholds, timing, economy, ceremony contexts, rewards, and result distributions remain NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED"
```

## Existing-solution-first boundary

`CEREMONIAL_NOBLE` already exists in `data/vertical_slice/vertical_slice_preset.json`. Decision06 reuses that representative ID and does not invent a parallel customer fixture or a new named noble/family lore record.

```text
EXISTING_CEREMONIAL_NOBLE_REPRESENTATIVE_REUSED
NO_NEW_NAMED_NOBLE_LORE_IN_DECISION06
```

## Player promise

A ceremonial noble brings or commissions work on one existing heirloom for a succession ceremony. The smith sees the same item's actual condition, past repairs, provenance, relevant Artistry/affixes, and declared ceremonial purpose. The player decides how far to intervene using existing repair/restoration/rework authority, then later sees how the decision affected ceremony readiness, treatment fit, and the heirloom's ongoing dynastic life.

The player remains `BLACKSMITH_HEIRLOOM_TREATMENT_DECISION_MAKER_NOT_HOUSE_OR_CEREMONY_CONTROLLER`.

The player may:

- inspect one existing heirloom UID and its real lifecycle evidence;
- read the succession/ceremonial use context disclosed before treatment;
- choose a justified repair/restoration/rework depth using existing systems;
- preserve meaningful marks or prior repairs when removal would erase useful history;
- hand the same UID back and receive an off-screen ceremony result;
- use the returned evidence for preservation, further repair, reuse, exhibition, future succession, or replacement-craft decisions.

The player does not manage a noble house, court politics, inheritance strategy, ceremony staging, diplomacy, guests, or succession claimants.

## Evidence and treatment-fit contract

Decision06 creates no new universal “authenticity” or “prestige” raw stat. Treatment fit may only be explained from evidence that current Blacksmith authority actually owns, such as:

- current damage/condition and existing repair/restoration history;
- item material, construction, grade, Artistry, approved affixes/functions, and current role where actually relevant;
- ownership, gifting, inheritance, display, or other provenance already attached to the same UID;
- the disclosed ceremony purpose and whether the item is expected to be symbolic, functional, wearable, presentational, or safely preservable.

Possible intervention depth is contextual. “Do less” can be valid when a mark or repair is meaningful evidence; stronger intervention can be valid when structural/function readiness requires it. The design does not establish one fixed list as a new global restoration subsystem.

## Multiple defensible treatments

- Full cosmetic restoration is not automatically best.
- Highest Artistry is not automatically best.
- The oldest or most damaged heirloom is not automatically the most valuable choice.
- Preserving every mark is not automatically best when structural safety or declared function requires intervention.
- Removing every mark is not automatically best when the mark is meaningful provenance/history.

The result must explain 2–4 concrete reasons from the actual UID and disclosed ceremony context rather than a hidden score.

## Result contract

```text
CEREMONY_READINESS_STATE
HEIRLOOM_TREATMENT_FIT_STATE
ITEM_UID_DYNASTIC_LEGACY_STATE
```

- `CEREMONY_READINESS_STATE`: whether the heirloom was ready for its declared ceremonial/function context.
- `HEIRLOOM_TREATMENT_FIT_STATE`: whether the chosen intervention depth was defensible for the item's actual condition/history and intended use.
- `ITEM_UID_DYNASTIC_LEGACY_STATE`: what the same UID now carries forward from the treatment and ceremony.

A successful ceremony does not prove that the treatment was ideal, and an imperfect ceremony outcome does not automatically mean the smith made a poor preservation choice. The three axes remain separate.

## Same-UID lifecycle

`SAME_ITEM_UID_PRESERVED`.

The heirloom before treatment, after treatment, during ceremony, and after return is the same UID. Treatment records, preserved marks, removed/replaced material where already representable, new damage, and ceremony provenance attach to that same item's lifecycle. Decision06 does not clone the heirloom or replace it with a generic “restored version” object.

## History-preservation boundary

```text
NO_HISTORY_ERASURE_ON_REPAIR
```

Restoration may change the item's condition through existing authority, but it must not silently delete meaningful prior repair, ownership, provenance, Chronicle, or lifecycle records. A visible mark may be repaired or reduced when justified; the historical record of what happened remains.

## Progression boundaries

- Restoration count does not automatically raise `ARTISTRY`.
- Ceremony count does not automatically raise `ARTISTRY`.
- Successful succession does not automatically grant `CHRONICLE_AFFIX`.
- Existing Chronicle authority may recognize a specific meaningful event, but not because it is the Nth ceremony/restoration.
- Repeated heirloom work does not create a restoration-farming multiplier.

## Information contract

Before intervention, show the selected UID, ceremony purpose, actual condition/history, and 2–4 relevant support/conflict reasons. Do not show an automatic `BEST` treatment.

After the ceremony, show the three result axes, 2–4 concrete causal reasons, and one primary next-action reason. Essential state cannot rely on color alone.

Exact wording, thresholds, economy values, timing, rewards, and result distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.

## Protected boundaries

- `NO_FULL_RESTORATION_ALWAYS_BEST`
- `NO_HIGHEST_ARTISTRY_ALWAYS_BEST`
- `NO_HOUSE_PRESTIGE_SCORE`
- `NO_AUTHENTICITY_TOTAL_SCORE`
- `NO_SUCCESSION_TOTAL_SCORE`
- `NO_HISTORY_ERASURE_ON_REPAIR`
- `NO_RESTORATION_COUNT_ARTISTRY_GROWTH`
- `NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_CEREMONY_OR_RESTORATION`
- `NO_RESTORATION_FARMING_MULTIPLIER`
- `SAME_ITEM_UID_PRESERVED`
- `NO_DIRECT_CEREMONY_MINIGAME`
- `NO_NOBLE_HOUSE_MANAGEMENT`
- `NO_COURT_OR_DIPLOMACY_MANAGEMENT`
- `EXISTING_CEREMONIAL_NOBLE_REPRESENTATIVE_REUSED`
- `BLACKSMITH_HEIRLOOM_TREATMENT_DECISION_MAKER_NOT_HOUSE_OR_CEREMONY_CONTROLLER`
- `PRODUCT_IMPLEMENTATION_BLOCKED`
- `TASK3_IMPLEMENTATION_NOT_APPROVED`

## Adversarial review

### Attack

1. This can collapse into Ersa's exhibition/provenance content.
2. A hidden prestige/authenticity score can become the real answer.
3. Full restoration can become the universal optimum.
4. “Preserve history” can become a simplistic always-never-repair rule.
5. Repeated restoration/ceremony can farm Artistry or Chronicle.
6. The restored object can accidentally become a new UID.
7. Noble-house, court, diplomacy, or succession management can swallow the smithing loop.

### Validated response

- `MUST_FIX`: Ersa owns exhibition evidence selection; Noble01 owns intervention-depth judgment on an heirloom before succession.
- `MUST_FIX`: no opaque prestige/authenticity/succession score.
- `MUST_FIX`: both minimal and stronger interventions can be defensible depending on real condition/history and declared use.
- `MUST_FIX`: meaningful history remains in the record even when physical condition changes.
- `MUST_FIX`: no automatic Artistry/Chronicle progression or farming multiplier.
- `MUST_FIX`: same UID remains authoritative.
- `MUST_FIX`: ceremony resolves off-screen; no house/court/diplomacy management.
- `REJECTED_CRITIQUE`: turning the content into a full conservation laboratory or noble-politics simulator would broaden scope and weaken the established smith/item-lifecycle core.

## Acceptance criteria

- `BS-CONTENT-20260811-06 / NOBLE_01 / CEREMONIAL_NOBLE / HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY` becomes current R3–R7 `6/10` planning canon.
- Decisions01–05 remain approved history.
- Existing `CEREMONIAL_NOBLE` representative is reused without inventing new named noble lore.
- Result uses `CEREMONY_READINESS_STATE`, `HEIRLOOM_TREATMENT_FIT_STATE`, and `ITEM_UID_DYNASTIC_LEGACY_STATE`.
- Same item UID and prior lifecycle/provenance history remain authoritative.
- No full-restoration/highest-Artistry automatic answer, prestige/authenticity/succession aggregate score, progression farming, direct ceremony, noble-house, court, or diplomacy control is added.
- Product implementation and Task3 remain blocked.
