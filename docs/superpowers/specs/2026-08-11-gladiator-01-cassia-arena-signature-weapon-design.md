# GLADIATOR_01 Cassia Arena Signature Weapon Design

## Status

- Decision: `BS-CONTENT-20260811-05`
- R3–R7 slot: `5/10`
- Scope: planning canon only
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`
- User direction: approved the recommended Cassia representative-gladiator design after pre-work research and adversarial review.

## Goal

Promote `CASSIA_BELLAN` as `GLADIATOR_01` and prove that a smith-made item can matter in a public arena result without turning Blacksmith into an arena-combat, team-management, or score-optimization game.

## PRE_WORK_RESEARCH_PACKET

```yaml
PRE_WORK_RESEARCH_PACKET:
  checked_at_kst: 2026-08-11
  base_main_sha: 8e7d85b1b1272002a8086c502a41073888cb3318
  project_main_sha: 98c0e1f26e51eeb01c04b742b535d7a3a1345c35
  open_pr_inventory: "PR #81 only; REFERENCE ONLY / DO NOT MERGE"
  google_sheet_state: "R3_R7_DESIGN_ACTIVE / 4_OF_10; Cassia COMPLETE_DRAFT; BS-CT-02 COMPLETE_DRAFT; product BLOCKED; Task3 NOT_APPROVED"
  work_type: "game content design / customer-world-result UX"
  benchmark_sources:
    - "Gladiator Guild Manager official Steam page"
    - "Battle Brothers official developer features and tactical-combat pages"
    - "Crusader Kings III: Tours & Tournaments official Paradox page"
  professional_or_official_sources:
    - "Apple Human Interface Guidelines — Feedback"
    - "Android Developers — What a great user experience looks like"
    - "Games User Research — playtest method guidance"
  adopt:
    - "explainable pre-event equipment choice with observable consequence"
    - "decomposed result feedback and evidence-based playtesting"
  adapt:
    - "arena event resolves outside player control; item contribution returns to the smith as world feedback"
    - "equipment matters through existing item properties and explicit context rather than one aggregate score"
  reject:
    - "direct arena combat, team positioning, behavior orders, squad/guild management, betting"
    - "legacy fixed iron_sword/+5/+10/3-day/score-weight formula as new canon"
    - "opaque ARENA_SCORE/FAME_SCORE or highest-enhancement automatic answer"
  differentiator: "Blacksmith separates match outcome from the same UID item's actual contribution and public legacy, then feeds that evidence back into future smithing decisions."
  canon_conflict_check: "No conflict with R3 1/10–4/10. Legacy gladiator PoC data is retained as historical fixture, not promoted as Decision05 authority."
  adversarial_precheck: "combat-RPG drift, score optimization, win=good-item collapse, fame farming, UID loss, automatic Artistry/Chronicle progression, legacy fixture resurrection"
  remaining_uncertainty: "exact match contexts, thresholds, reward values, timing, and result distributions remain NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED"
```

## Player promise

Cassia wants a weapon that can become associated with her name while helping her advance to a higher arena tier. The smith sees a clear weapon-category request and a clear match brief, compares real works, hands over one item UID, and later receives a result that distinguishes what happened in the match from what the item actually contributed.

The player remains `BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER`.

The player may:

- read Cassia's weapon-category request and disclosed match context;
- compare eligible works using existing item properties and provenance;
- choose one real item UID;
- hand it over and receive off-screen arena consequences;
- use the returned evidence for repair, restoration, further enhancement, a rematch work, sale, preservation, or later exhibition decisions.

The player does not control Cassia in combat, position fighters, issue behavior orders, manage a gladiator roster/guild, or bet on the match.

## Context and item fit

The match brief must disclose the relevant context before handoff. It may reference only current owners actually present in Blacksmith, such as:

- requested weapon category / hard eligibility;
- enhancement level and existing role-performance raw values;
- weight or other existing handling-relevant properties when actually applicable;
- approved affix/function fit where the context truly calls for it;
- `ARTISTRY`, provenance, or prior Chronicle evidence only when the request explicitly values signature/public identity rather than generic combat power.

No new `ARENA_SCORE`, `FAME_SCORE`, `GLADIATOR_SCORE`, `SIGNATURE_SCORE`, or hidden universal combat-power aggregate is created.

Multiple works must remain defensible. Highest enhancement is not automatically best, and the most famous or most storied work is not automatically best when the disclosed arena context points elsewhere.

## Result contract

The arena result is decomposed:

```text
ARENA_MATCH_STATE
EQUIPMENT_CONTRIBUTION_STATE
ITEM_UID_ARENA_LEGACY_STATE
```

- `ARENA_MATCH_STATE`: the match-level outcome.
- `EQUIPMENT_CONTRIBUTION_STATE`: what the handed-over item demonstrably helped or hindered, based on disclosed context and actual item properties.
- `ITEM_UID_ARENA_LEGACY_STATE`: the same UID's public/lifecycle consequence such as a decisive moment, visible damage, rival mark, reputation-bearing event, or no meaningful public legacy.

A match win does not prove the item was optimal. A loss does not prove the item was poor. Strong item contribution and match defeat may coexist; weak item contribution and match victory may coexist.

The result presents 2–4 concrete reasons and one primary next-action reason. It does not collapse the three axes into a percentage or star rating.

## Same-UID lifecycle

`SAME_ITEM_UID_PRESERVED`.

The handed-over item before, during, and after the arena event is the same UID. Arena use may create damage, repair needs, provenance, rivalry marks, or Chronicle-eligible events only through existing lifecycle/Chronicle authority. The event does not clone, replace, or silently reroll the item.

## Progression boundaries

Arena success is not a free progression faucet.

- Win count does not automatically raise `ARTISTRY`.
- Fame/renown does not automatically raise `ARTISTRY`.
- Winning or appearing in a match does not automatically grant `CHRONICLE_AFFIX`.
- If existing Chronicle authority judges a specific arena event sufficiently meaningful, the consequence is tied to that concrete event and same UID, not to match count.
- Repeated matches do not create an automatic farming multiplier.

## Legacy gladiator PoC boundary

The current repository still contains historical PoC fixtures such as `data/customers/gladiator_poc.json` and `data/world/gladiator_match_poc.json`. Decision05 does not make their old fixed item ID, +5/+10 thresholds, 3-day timing, preferred-affix list, grade-score table, score weights, or result bands current design authority.

```text
LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05
NO_FIXED_IRON_SWORD_CANON
NO_LEGACY_ARENA_SCORE_FORMULA_CANON
NO_UNIVERSAL_FIXED_DAY_COUNT
```

Those fixtures are not modified in this planning-only Decision.

## Information contract

Before handoff, Cassia's card exposes weapon-category eligibility and the match-context dimensions relevant to this request. After item selection, the decision layer shows the selected UID plus 2–4 supporting/conflicting reasons without an automatic `BEST` recommendation.

After the event, show the three result axes, 2–4 concrete reasons, and one primary next-action reason. Color alone cannot carry essential state.

Exact wording, thresholds, economy values, timing, and result distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`.

## Protected boundaries

- `NO_DIRECT_ARENA_COMBAT`
- `NO_GLADIATOR_TEAM_OR_GUILD_MANAGEMENT`
- `NO_BETTING_SYSTEM`
- `NO_OPAQUE_ARENA_SCORE`
- `NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`
- `NO_WIN_EQUALS_GOOD_ITEM_COLLAPSE`
- `NO_MATCH_COUNT_ARTISTRY_GROWTH`
- `NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_APPEARANCE`
- `NO_MATCH_FARMING_MULTIPLIER`
- `SAME_ITEM_UID_PRESERVED`
- `LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05`
- `BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER`
- `PRODUCT_IMPLEMENTATION_BLOCKED`
- `TASK3_IMPLEMENTATION_NOT_APPROVED`

## Adversarial review

### Attack

1. Cassia can pull the project into a direct combat RPG.
2. A hidden aggregate arena score can become the real answer.
3. Match win/loss can incorrectly become a proxy for item quality.
4. Highest enhancement can become the universal best choice.
5. Repeated wins can become Artistry/Chronicle/fame farming.
6. The same UID can be lost when a match returns a generic reward/result object.
7. Legacy Kyle/iron_sword PoC numbers can silently re-enter current canon.

### Validated response

- `MUST_FIX`: arena execution remains off-screen and player authority stays on smithing/item selection.
- `MUST_FIX`: result must separate match state from equipment contribution and UID legacy.
- `MUST_FIX`: no new opaque arena/fame/gladiator aggregate score.
- `MUST_FIX`: no highest-enhancement or win=good-item universal answer.
- `MUST_FIX`: no automatic Artistry/Chronicle progression from matches/wins.
- `MUST_FIX`: same UID remains visible and authoritative through the result.
- `MUST_FIX`: legacy PoC fixed values remain non-authoritative fixtures.
- `REJECTED_CRITIQUE`: adding player-controlled tactical combat for more drama would violate the established Blacksmith player-role boundary and broaden scope without need.

## Acceptance criteria

- `BS-CONTENT-20260811-05 / GLADIATOR_01 / CASSIA_BELLAN / ARENA_SIGNATURE_WEAPON_AND_LEGACY` becomes current R3–R7 `5/10` planning canon.
- Decisions 01–04 remain approved history.
- Result uses `ARENA_MATCH_STATE`, `EQUIPMENT_CONTRIBUTION_STATE`, and `ITEM_UID_ARENA_LEGACY_STATE`.
- Same item UID remains authoritative.
- No direct combat, team/guild management, betting, opaque arena score, automatic progression, or legacy PoC formula promotion occurs.
- Product implementation and Task3 remain blocked.
