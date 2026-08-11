# Collector 02 Sedric Archival Accession Design

## Decision

`BS-CONTENT-20260811-08 / COLLECTOR_02 / SEDRIC_VAEL / ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY`

Status at spec authoring: `USER_APPROVED_DIRECTION / R3_R7_8_OF_10_TARGET / PLANNING_ONLY`.

This approval does not authorize product implementation or Task3. Those remain `PRODUCT_IMPLEMENTATION_BLOCKED / TASK3_NOT_APPROVED` until the existing project gate changes explicitly.

## Goal

Create a second Collector-family detailed content contract in which Sedric Vael decides whether one real item UID has sufficiently explainable provenance and custody history to enter long-term archival keeping, while preserving Blacksmith's same-UID lifecycle, explainable choice, and non-management boundaries.

The player fantasy is:

> I am not choosing the strongest or oldest object. I am deciding whether this exact work can stand behind its own history strongly enough to entrust it to long-term keeping.

## Existing Authority and Reuse

Decision08 refines, but does not replace, the following current authorities:

- `BS-CONTENT-20260804-01`: customer result, item UID state, and follow-up crafting loop.
- `BS-CONTENT-20260804-02`: current initial content-family authority.
- `BS-CUSTOMER-20260803-02`: customer and event readability baseline.
- `BS-CUSTOMER-20260805-01`: customer aptitude and item-fit ownership.
- `BS-UX-20260805-01`: layered customer-card and explainable decision presentation.
- `BS-CRAFT-20260804-06`, `BS-CRAFT-20260805-01`, `BS-CRAFT-20260805-02`: Artistry, provenance, lifecycle evidence, and anti-double-counting boundaries.
- `BS-CONTENT-20260811-04 / COLLECTOR_01 / ERSA_ROEN`: exhibition evidence and public legacy.
- `BS-CONTENT-20260811-06 / NOBLE_01 / CEREMONIAL_NOBLE`: heirloom treatment-depth and succession legacy.
- `BS-CONTENT-20260811-07`: latest R3-R7 current-state baseline and 7/10 history.

Existing `SEDRIC_VAEL` identity is reused. Decision08 does not create another named collector, another noble representative, or a new customer archetype.

## Responsibility Boundary

Sedric owns archival accession and custody judgment.

He does not own:

- public exhibition reception or exhibit thesis, which remains Ersa's responsibility;
- repair, restoration, or rework depth, which remains Noble01 and the existing item-treatment authorities;
- museum, archive, storage-room, visitor, staffing, shelving, preservation-environment, or loan logistics management;
- authenticity, prestige, rarity, provenance, archive, or heritage aggregate scoring systems.

The important separation is:

```text
ERSA_ROEN / COLLECTOR_01
= Which real evidence should be emphasized for a public exhibition intent?

SEDRIC_VAEL / COLLECTOR_02
= Does this exact UID have sufficiently explainable provenance and custody evidence for archival accession?

CEREMONIAL_NOBLE / NOBLE_01
= How far should this exact heirloom UID be physically repaired, restored, or reworked for succession?
```

## Player Flow

The content flow is:

```text
SEDRIC_VAEL visit
→ archival category and keeping purpose disclosed
→ real item UID candidates shown
→ player inspects real evidence on candidate UIDs
→ one UID selected and handed over
→ archival accession resolves as an off-screen world/customer event
→ three independent result axes shown
→ same UID becomes available for later preservation, loan, exhibition, research/appraisal, return, or re-evaluation hooks
```

The player does not fabricate paperwork, type provenance text, manage shelves, or manually catalog an archive.

## Evidence the Content May Consume

Decision08 consumes only evidence that already exists on the item or existing project systems and is relevant to the accession purpose. It does not invent a new hidden raw stat.

Allowed evidence families include:

- item UID identity;
- item category and material identity where relevant to the disclosed archive purpose;
- creation/provenance source already recorded by existing crafting systems;
- recorded owner or custody transitions already present in item history;
- recorded damage, repair, restoration, recovery, exhibition, mission, journey, arena, succession, or other approved lifecycle history actually attached to that UID;
- existing Chronicle/provenance records;
- existing creation quality/Artistry evidence only where the disclosed archival purpose makes it relevant;
- existing customer/item eligibility or fit gates where needed to prevent invalid handoff.

The content must not infer undocumented ownership history as fact. Missing evidence remains missing evidence rather than being auto-filled by a favorable score.

## Core Decision Shape

There must be multiple defensible choices when the current inventory supports them.

Examples of defensible contrast:

- a newer work with very clear provenance and custody records versus an older work with a rich but incomplete ownership history;
- a visually refined piece with modest lifecycle history versus a heavily used piece whose ownership and recovery history is unusually well documented;
- an item with strong historical relevance but one unresolved custody gap versus a less dramatic item with exceptionally continuous records.

Decision08 must not reduce these cases to `highest Artistry`, `oldest`, `most Chronicle events`, `highest enhancement`, or any single aggregate number.

## Result Contract

The content returns three separate result axes:

1. `ARCHIVE_ACCESSION_STATE`
   - whether the current archival request accepted, conditionally accepted, deferred, or declined the handoff according to disclosed criteria and actual evidence;
   - this is not a total quality score.

2. `PROVENANCE_DOCUMENTATION_STATE`
   - how well the selected UID's actual origin and custody evidence supports the disclosed archival purpose;
   - missing or contradictory evidence must be surfaced as reasons, not hidden inside a total score.

3. `ITEM_UID_CUSTODY_LEGACY_STATE`
   - what happened to the same UID's custody/public-record lifecycle as a result of the archival handoff;
   - the UID is preserved.

These axes may disagree. For example:

- accession may be conditional while the item's historical significance is high but documentation is incomplete;
- accession may succeed while the item remains physically worn because restoration was not part of Sedric's responsibility;
- documentation may be strong while the disclosed archive purpose still makes another item a better contextual fit.

## Feedback Contract

Immediate result presentation must use:

- the three result axes;
- two to four causal reasons drawn from actual disclosed request context and actual UID evidence;
- one primary follow-up action.

Follow-up actions may include, when supported by existing systems and later content ownership:

- preserve as-is;
- repair or restore through the existing treatment owner;
- return for missing-history re-evaluation if a later approved source resolves the gap;
- loan or exhibition through a later approved content hook;
- research/appraisal as a non-farming follow-up hook;
- choose or craft a different work for a future archival request.

Decision08 does not itself implement those future systems.

## Same-UID Lifecycle

`SAME_ITEM_UID_PRESERVED` is mandatory.

Archival acceptance, documentation review, custody transfer, exhibition, or later re-evaluation does not clone the item and does not create a replacement identity.

Archival participation does not automatically increase Artistry and does not automatically add a Chronicle Affix merely because the item was accepted, stored, reviewed, or displayed.

## Protected Boundaries

The following are explicit Decision08 protections:

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
- `SAME_ITEM_UID_PRESERVED`
- `ERSA_EXHIBITION_RESPONSIBILITY_PRESERVED`
- `NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED`
- `EXISTING_SEDRIC_VAEL_CUSTOMER_REUSED`
- `PRODUCT_IMPLEMENTATION_BLOCKED`
- `TASK3_NOT_APPROVED`

## Exact Values and Content Instances

Exact archive category distribution, acceptance thresholds, number of evidence reasons, economic rewards, relationship rewards, event duration, follow-up timing, and result distribution are not canonical fixed values in Decision08.

They remain:

`NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`

A future test fixture may use exact values for deterministic validation, but those values must be labelled as fixtures and must not silently become current game-design authority.

## Relationship to BS-CT-06 Taxonomy Ambiguity

Decision08 does not redefine the current meaning of the existing Sheet row `BS-CT-06 / 고객 4유형×이름 고객 8명`.

Sedric is already one of the eight named customers in that row, so this decision can detail him without deciding whether Collector remains a current top-level archetype, a legacy expansion grouping, or a derivative taxonomy label after Noble01 was separately detailed.

The existing `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED` finding remains open and must not be silently resolved in Decision08.

## Adversarial Failure Cases

The implementation plan and contract tests must attack at least these failures:

1. Sedric becomes Ersa with different prose.
2. Sedric becomes Noble01 with archival wording around restoration.
3. A hidden authenticity/provenance/archive total score decides the answer.
4. Oldest, highest Artistry, highest enhancement, or most Chronicle entries becomes the automatic best answer.
5. Missing provenance is silently invented or auto-filled.
6. Archival review itself raises Artistry or creates a Chronicle Affix.
7. The content introduces archive-storage, museum-management, visitor-management, or loan-logistics gameplay.
8. The selected item is cloned instead of preserving the same UID.
9. Product code or Task3 implementation is added under a planning-only approval.
10. Decision01-07 approved history or current responsibility ownership is damaged while moving the current pointer to Decision08.

## Acceptance Criteria

Decision08 is ready to become R3-R7 8/10 current canon only when all of the following are true:

- one canonical `COLLECTOR_02 / SEDRIC_VAEL` planning document exists;
- current registry and current-decision router identify `BS-CONTENT-20260811-08 / 8/10` without deleting Decision01-07 history;
- `ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE` are explicit and independent;
- Ersa exhibition and Noble01 treatment-depth responsibilities remain explicit and separate;
- same UID preservation and all protected anti-score/anti-management/anti-farming boundaries are explicit;
- a focused Decision08 test demonstrates semantic RED before the canonical decision/current-pointer materialization;
- relevant current-state consumers and audit assertions move from 7/10 to 8/10 without rewriting historical decision meaning;
- required Python, Godot, Base/BCA/GUT/HiGodot/Adapter validation is GREEN at one exact reviewed head;
- Base `POST_CHANGE_MONITOR_LOOP` returns no unresolved `OMISSION`, `CONFLICT`, `COMPLEMENT_GAP`, or `DUPLICATE_WORK` that blocks completion;
- merged-main readback confirms the Decision08 current state;
- Google Sheet uses the exact same Decision ID and passes exact readback;
- product implementation remains `BLOCKED` and Task3 remains `NOT_APPROVED`;
- human playtest, Android device, and accessibility remain `NOT_RUN` unless actually observed.

## Expected Player and Product Result

Before Decision08, Collector has a detailed public-exhibition owner through Ersa, but Sedric remains a thin named-customer fixture.

After Decision08, Collector-family content has two clearly different blacksmith responsibilities:

```text
Ersa: Can this work support the story we want to show publicly?
Sedric: Can this exact work support the history we are willing to preserve and stand behind?
```

This expands item attachment without adding a museum simulator. The item becomes valuable not because an archive score says so, but because the player can read and defend the real history attached to the same UID.
