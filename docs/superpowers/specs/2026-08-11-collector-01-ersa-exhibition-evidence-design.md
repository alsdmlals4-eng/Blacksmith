# COLLECTOR_01 Ersa Exhibition Evidence Design

## Status

- Decision: `BS-CONTENT-20260811-04`
- R3–R7 slot: `4/10`
- Scope: planning canon only
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`
- User direction: proceed with the recommended Ersa collector design that proves Blacksmith's authored-item lifecycle can create value through exhibition, provenance, and craft evidence without adding a hidden prestige score or turning the player into a curator.

## Goal

Promote `ERSA_ROEN` as `COLLECTOR_01` and prove that the existing Blacksmith loop still works when the world consequence is not combat performance but a public exhibition whose meaning comes from the item's actual craftsmanship and lived UID history.

## PRE_WORK_RESEARCH_PACKET

### Fresh project evidence

- Base observed main: `315c66eea9614c284b9c11c4d522141065dfa4b0`.
- Blacksmith observed main before this decision: `1e60cf163191d547b96ffc392e3da24d072b7956`.
- Open PR inventory: PR #81 remains `REFERENCE ONLY · DO NOT MERGE`.
- Live Sheet before promotion: `R3_R7_3_OF_10`, current `BS-CONTENT-20260811-03`, `PRODUCT_IMPLEMENTATION_BLOCKED`, `TASK3_NOT_APPROVED`.
- Live Sheet already defines `ERSA_ROEN` as the Collector representative whose goal is to exhibit either the item's making or its lived record, and `BS-CT-03` as the proof that the same structure works outside combat.

### Benchmarks and professional practice

- `Strange Horticulture`: `ADAPT` context-driven interpretation of a collection and customer-facing choice; `REJECT` exploration/puzzle/lore-quiz structure as Blacksmith's core.
- `Tiny Bookshop`: `ADAPT` matching a person and situation to the right object using understandable context; `REJECT` decoration-management and general cozy-shop expansion as this content's core.
- `Crusader Kings III: Royal Court`: `ADAPT` crafted relics, heirlooms, display, and history-bearing artifacts; `REJECT` a single grandeur/prestige axis as Blacksmith's exhibition answer.
- Apple Human Interface Guidelines feedback guidance: `ADAPT` clear status, action result, warning, and next-step feedback so exhibition outcome remains understandable.
- Google Play quality guidance: `ADAPT` meaningful, intuitive, responsive user experience; `REJECT` opaque score-chasing that hides why the player's choice worked.
- `DIFFERENTIATOR`: Blacksmith does not treat an exhibited item as a generic collectible card. The same authored item UID carries forging, ownership, damage, recovery, repair, and chronicle evidence into a new public context and then returns that consequence to future making decisions.

## Player promise

Ersa does not ask for the item with the highest generic rarity, prestige, enhancement, artistry, or chronicle count. She presents an exhibition intent and asks the smith to choose one real work whose existing evidence makes that intent credible.

The player remains the blacksmith and item decision maker:

- read Ersa's exhibition intent;
- compare eligible works;
- choose one item UID;
- choose which existing evidence to emphasize in a short maker statement;
- hand over the work;
- receive the off-screen exhibition result and the same UID's public-history consequence.

The player does not place exhibits, manage visitor traffic, decorate a gallery, run an auction, or control the exhibition in real time.

## Exhibition model

```text
ERSA_ROEN visit
→ exhibition intent disclosed
→ eligible work comparison
→ item UID selected
→ maker statement selects 2–4 existing evidence points to emphasize
→ item handed over
→ off-screen exhibition
→ decomposed result returned
→ same UID gains public-history context where the existing Chronicle/provenance rules permit it
→ next craft / restoration / sale / exhibition decision reason
```

The maker statement is an explanation layer, not a new power source. Selecting an evidence point does not create that evidence, modify raw stats, or guarantee a result.

## Exhibition intent and evidence fit

The first Collector proof uses two broad intent families already present in the project draft:

- `CRAFTSMANSHIP_EVIDENCE`: the exhibition foregrounds how the work was made.
- `LIVED_HISTORY_EVIDENCE`: the exhibition foregrounds what the same work has actually lived through.

These are context families, not universal answer categories and not permanent item types.

### Existing evidence only

`CRAFTSMANSHIP_EVIDENCE` may consume currently owned evidence such as:

- production grade / `GRADE_AFFIX` where canonically available;
- `ARTISTRY` and its approved authored sources;
- forging, finishing, catalyst, and approved rework provenance;
- concrete maker/production history already recorded on the UID.

`LIVED_HISTORY_EVIDENCE` may consume currently owned evidence such as:

- ownership/provenance chain;
- specific customer or world-use events;
- damage, loss, recovery, repair, restoration, or inheritance history;
- concrete `CHRONICLE_AFFIX` or Chronicle events where existing rules actually grant them.

Do not create `RARITY_SCORE`, `PRESTIGE_SCORE`, `COLLECTOR_SCORE`, `EXHIBITION_SCORE`, or any other opaque aggregate raw stat.

## Multiple defensible works

The system must not collapse into "the oldest item always wins" or "the highest artistry item always wins."

- A newly made item can be a strong answer when its craftsmanship evidence strongly matches the announced intent.
- A heavily lived-in item can be a strong answer when its concrete history matches the announced intent.
- A high-enhancement item can still be a weak exhibit if its enhancement has little connection to the exhibition thesis.
- A long Chronicle list can still be weak evidence if the events are irrelevant to the announced thesis.

The content therefore evaluates contextual evidence fit, not raw quantity.

## Result contract

Keep the exhibition result decomposed:

- `EXHIBITION_RECEPTION_STATE`
- `EXHIBIT_THESIS_FIT_STATE`
- `ITEM_UID_PUBLIC_LEGACY_STATE`

One scalar exhibition score or percentage must not replace these axes.

A valid result may therefore have strong public reception but weak thesis fit, or a modest reception while the item gains a meaningful public-history state. The result should surface 2–4 concrete reasons drawn from the selected work and the announced exhibition intent.

## Same-UID lifecycle

The exhibition references the same item UID before, during, and after the event.

- Exhibition does not clone or replace the item.
- Ownership/loan/return state follows the existing item-lifecycle authority.
- Public recognition must remain an event/provenance consequence, not a new hidden raw stat.
- Later repair, restoration, resale, return, inheritance, or another exhibition must be able to inspect the same UID's prior evidence.

## Artistry and Chronicle boundaries

Exhibition is not a free progression action.

- `EXHIBITION_COUNT` does not automatically raise `ARTISTRY`.
- Public reception does not automatically raise `ARTISTRY`.
- A Chronicle event does not automatically raise `ARTISTRY`.
- Displaying an item does not automatically grant a `CHRONICLE_AFFIX` merely because it was displayed.
- If existing Chronicle rules determine that a sufficiently meaningful exhibition event earns a Chronicle consequence, that consequence must be tied to the specific event and same UID rather than to an exhibition counter.

## Information contract

Before handoff, Ersa's card must disclose the exhibition intent and the relevant evidence dimensions without a `BEST` recommendation.

After selecting a work, the decision layer should expose:

- the selected UID;
- 2–4 relevant supporting or conflicting evidence points;
- the chosen maker-statement emphasis;
- any hard eligibility issue separately from contextual fit.

After the exhibition, show the three result axes and 2–4 concrete reasons. Color alone must not carry the result.

Exact wording, thresholds, economy values, and result distributions remain `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED` until later validation.

## Protected boundaries

- `NO_RARITY_SCORE`
- `NO_PRESTIGE_SCORE`
- `NO_COLLECTOR_SCORE`
- `NO_EXHIBITION_SCORE`
- `NO_CHRONICLE_COUNT_OPTIMIZATION`
- `NO_OLDEST_ITEM_ALWAYS_BEST`
- `NO_HIGHEST_ARTISTRY_ALWAYS_BEST`
- `NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`
- `NO_EXHIBITION_COUNT_ARTISTRY_GROWTH`
- `NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_DISPLAY`
- `SAME_ITEM_UID_PRESERVED`
- `BLACKSMITH_ITEM_DECISION_MAKER_NOT_CURATOR_CONTROLLER`
- `NO_DIRECT_EXHIBITION_MINIGAME`
- `NO_GALLERY_DECORATION_OR_VISITOR_MANAGEMENT_CORE`
- `PRODUCT_IMPLEMENTATION_BLOCKED`
- `TASK3_IMPLEMENTATION_NOT_APPROVED`

## Adversarial review

### Attack

1. Collector content can degenerate into a lore quiz detached from smithing.
2. A hidden prestige/rarity score can silently become the real answer.
3. Chronicle count can become a dominant optimization axis.
4. Old items can become universally superior, making new smithing irrelevant.
5. Exhibition can become a gallery-management minigame and move the player away from being a blacksmith.
6. Display can become a low-cost way to farm Artistry or Chronicle progression.

### Validated response

- `MUST_FIX`: every choice and result must cite actual existing UID evidence rather than hidden lore knowledge.
- `MUST_FIX`: prohibit new rarity/prestige/collector/exhibition aggregate scores.
- `MUST_FIX`: evaluate relevance of history, not Chronicle count.
- `MUST_FIX`: allow both strong new craftsmanship and strong lived history to be defensible depending on the exhibition intent.
- `MUST_FIX`: keep exhibition execution off-screen and keep player authority on item/evidence selection.
- `MUST_FIX`: preserve existing Artistry and Chronicle ownership rules; no automatic growth from exhibition count or display alone.
- `REJECTED_CRITIQUE`: requiring one universal deterministic best item would reduce explanatory choice and contradict the project's protected no-auto-BEST direction.

## Acceptance criteria

- `ERSA_ROEN / COLLECTOR_01 / EXHIBITION_EVIDENCE_AND_PROVENANCE` becomes the current R3–R7 `4/10` planning decision.
- Nadia, Toren, and Marek remain approved history.
- The Collector proof uses the two broad exhibition-intent families above without turning them into new item types or raw stats.
- Result uses `EXHIBITION_RECEPTION_STATE`, `EXHIBIT_THESIS_FIT_STATE`, and `ITEM_UID_PUBLIC_LEGACY_STATE`.
- Same UID and existing evidence remain authoritative.
- No rarity/prestige/collector/exhibition score is added.
- No automatic Artistry or Chronicle progression comes from exhibition count/display alone.
- No product or Task3 implementation permission opens.
