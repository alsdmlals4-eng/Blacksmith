# SOLDIER_01 Marek Small-Lot Standard Order Design

## Status

- Decision: `BS-CONTENT-20260811-03`
- R3–R7 slot: `3/10`
- Scope: planning canon only
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`
- User direction: approve recommended Marek-first sequence and allow roughly ten low-enhancement items per order without turning Blacksmith into three-digit mass production.

## Goal

Promote `MAREK_OLDEN` as the first Soldier representative and prove that Blacksmith's customer/world-feedback pipeline can support a small standardized military order without becoming a factory, logistics, or tactical-combat game.

## PRE_WORK_RESEARCH_PACKET

### Fresh project evidence

- Base observed main: `315c66eea9614c284b9c11c4d522141065dfa4b0`.
- Blacksmith observed main: `6cabc340dc67e6eac8571a2d9bcb5a80bd6f4dea`.
- Open PR inventory: PR #81 remains `REFERENCE ONLY · DO NOT MERGE`.
- Live Sheet before promotion: `R3_R7_2_OF_10`, current `BS-CONTENT-20260811-02`, `PRODUCT_IMPLEMENTATION_BLOCKED`, `TASK3_NOT_APPROVED`.

### Benchmarks and professional practice

- `Blacksmith Master`: ADAPT small-order/production-throughput context; REJECT employee/production-line/resource-chain expansion as this content's core.
- `Anvil Saga`: ADAPT customer order → crafted output → world/relationship consequence; REJECT broad shop-simulation drift.
- `Battle Brothers`: ADAPT the principle that equipment choice and supply suitability affect a military group's outcomes; REJECT player-controlled tactical combat and permanent-soldier management.
- Lean standardized work: ADAPT explicit common requirements and repeatable process to reduce needless variation; REJECT industrial statistical-control simulation.
- DIFFERENTIATOR: every delivered unit remains an individually authored Blacksmith item with its own UID and lifecycle even when order setup is compressed.

## Player promise

Marek does not ask for the single highest-enhanced masterpiece. He asks the smith to establish a practical standard and deliver a small lot that satisfies the same public service requirements. The player decides what standard to build toward, how much enhancement is enough, and which completed UIDs are fit to hand over.

## Order model

```text
MAREK_OLDEN visit
→ public standard requirements
→ reference item crafted directly
→ player accepts a SMALL_LOT_STANDARD_ORDER
→ repeated setup may be reused
→ each item still consumes its own resources/work and produces its own result/UID
→ eligible UIDs selected for delivery
→ off-screen garrison mission/use
→ batch result + notable UID lifecycle results
→ next craft/repair/replacement reason
```

### Quantity

- Release canon does not permanently hard-code every Soldier order to exactly ten items.
- The first noncanonical baseline fixture uses `ORDER_QUANTITY = 10`.
- The intended family is a small lot, not three-digit industrial volume.
- Quantity tuning must preserve one-blacksmith daily opportunity cost and may not make production-line staffing or passive factory throughput necessary.

## Reference item plus repeated production

The first item is crafted as the `REFERENCE_ITEM_UID`. It establishes the player's chosen interpretation of the public requirement. Remaining items may reuse repetitive setup such as category, material family, and declared standard, but they are not free clones.

Each produced unit must retain:

- an independent item UID;
- its own material/resource costs;
- its own work/fatigue consequences where the current production contract applies them;
- its own forging and enhancement outcomes;
- its own provenance and lifecycle history.

The system may compress repeated input, but it may not duplicate a successful item state without normal production consequences.

## Standard requirement contract

Marek's requirements consume existing item evidence only. Candidate axes may include:

- item category/role eligibility;
- `WEIGHT` or other currently owned load requirement where relevant;
- current enhancement level;
- `DURABILITY` where relevant;
- existing approved context functions when the request explicitly calls for them.

Do not create `STANDARDIZATION_SCORE`, `SUPPLY_EFFICIENCY_SCORE`, `UNIT_READINESS_SCORE`, or another opaque aggregate raw stat.

The intended rule is:

> Items in the lot do not have to be statistically identical; each delivered UID must satisfy the same disclosed standard.

## Low-enhancement baseline and automation relationship

- Marek's first fixture is a low-enhancement small-lot order.
- Exact low-enhancement numbers are `NON_CANONICAL_BASELINE_TEST_PRESET` until playtest/economy validation.
- The separate auto-enhancement-cap system may reduce repetitive enhancement input on already-mastered low-risk bands, but every auto attempt must preserve normal chance, cost, resource use, stop conditions, and per-UID history.
- Marek content does not itself grant or raise the auto-enhancement cap.

## World result

Marek's delivery resolves outside direct player combat or logistics control.

Result axes are kept decomposed:

- `UNIT_MISSION_STATE`
- `STANDARD_ADOPTION_STATE`
- `BATCH_ITEM_LIFECYCLE_STATE`

A valid result can therefore be, for example, mission success while standard adoption is deferred, with one or more specific UIDs returning damaged or becoming notable. One scalar `batch success %` must not replace these axes.

## UID presentation

A batch is a presentation/grouping object, not a replacement identity.

```text
SMALL_LOT_ORDER_ID
→ references N item UIDs
→ summary result
→ notable UID callouts
→ full per-UID history remains queryable
```

Routine UI should collapse uninteresting duplicate history, but underlying item events are not deleted. A notable UID can later return for repair, recovery, exhibition, customer memory, or Chronicle consequences under existing rules.

## Protected boundaries

- `NO_THREE_DIGIT_MASS_PRODUCTION_CORE`
- `NO_WORKER_OR_PRODUCTION_LINE_SYSTEM_FROM_THIS_DECISION`
- `NO_REALTIME_LOGISTICS_CONTROL`
- `NO_DIRECT_TACTICAL_COMBAT`
- `NO_FREE_ITEM_CLONING`
- `PER_ITEM_UID_PRESERVED`
- `PER_ITEM_COST_AND_RESULT_PRESERVED`
- `NO_OPAQUE_STANDARDIZATION_SCORE`
- `NO_SINGLE_HIGHEST_ENHANCEMENT_ALWAYS_BEST`
- `PRODUCT_IMPLEMENTATION_BLOCKED`
- `TASK3_IMPLEMENTATION_NOT_APPROVED`

## Information and playtest contract

Before delivery, show mandatory requirements separately from preferences. When an item is rejected, expose the concrete reason rather than a hidden score. The batch summary must identify how many UIDs were delivered, how the common standard was interpreted, and which exceptional UIDs matter for follow-up.

Human validation remains `NOT_RUN`. Later tests should observe whether players can explain:

1. why they selected the reference specification;
2. why a higher-enhancement item might still be a poor standard candidate;
3. whether repeated production feels like reduced friction rather than a factory idle loop;
4. whether they understand that every delivered item remains a distinct work.

## Adversarial review

### Attack

1. Ten items may become ten identical chores.
2. Input compression may silently become free cloning or factory automation.
3. Ten independent UIDs may overwhelm result/history UI.
4. Players may simply enhance every item as high as possible.
5. Soldier content may expand into tactical combat or logistics simulation.

### Validated response

- `MUST_FIX`: preserve per-item cost/result/UID; compress only repeated setup/input.
- `MUST_FIX`: keep result axes decomposed and batch presentation collapsible.
- `MUST_FIX`: require disclosed standard criteria instead of one aggregate score.
- `MUST_FIX`: keep direct combat, worker lines, and real-time logistics outside scope.
- `SHOULD_FIX`: use target-based auto enhancement only for already-mastered bands through the separate system decision.
- `REJECTED_CRITIQUE`: requiring all ten pieces to be numerically identical would erase authored-item variation and is not necessary for a shared standard.

## Acceptance criteria

- `MAREK_OLDEN / SOLDIER_01 / SMALL_LOT_STANDARD_ORDER` becomes the current R3–R7 `3/10` planning decision.
- Ten-item quantity is a baseline fixture, not a universal permanent order size.
- Reference item + repeated production preserves individual UID/cost/result.
- Result uses the three decomposed axes above.
- No product or Task3 implementation permission opens.
- Nadia and Toren remain approved history.
