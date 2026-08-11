# BS-CONTENT-20260811-08 Adversarial Audit Receipt

Decision: `BS-CONTENT-20260811-08 / COLLECTOR_02 / SEDRIC_VAEL / ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY`.

Base completion contract: `POST_CHANGE_MONITOR_LOOP` from Base main `23d5b292f619022cdd8ab7a33fb1debc2d294861`.

## Attack lenses

The branch was attacked for:

- Sedric becoming Ersa with archive-flavored prose;
- Sedric taking Noble01 physical repair/restoration authority;
- authenticity/provenance/archive aggregate scoring;
- oldest/highest-Artistry/most-Chronicle/highest-enhancement automatic best answer;
- fabricated or autofilled missing history;
- archive/museum/storage/visitor/staff/loan-logistics management drift;
- item UID cloning;
- accession/review Artistry or Chronicle farming;
- product-code or Task3 scope leakage;
- Decision01–07 history loss while moving current to Decision08;
- stale current routers and untouched current consumers.

## Validated findings and repairs

### 1. Current-router mixed state

After initial materialization, diff/readback found:

- `START_HERE.md`, `ROADMAP.md`, and `DEVELOPMENT_GATES.md` headers still named Decision07 while their body/locator had moved to Decision08;
- `ACTIVE_CONTEXT.md` bottom current block still had a Decision07 marker/title/prose while embedded YAML already named Decision08;
- `START_HERE.md` next-work prose still routed continuous work to Decision07 and called 8/10 the next gate;
- Roadmap did not explicitly retain the Decision07 / Liana 7/10 historical section between 6/10 and 8/10.

Classification: `CONFLICT + OMISSION / MUST_FIX`.

Repair workflow:

- run: `31476824738`
- result: SUCCESS
- repair commit: `fb81618ff7ab5d5fb72be2ac6e88d047247c653e`

### 2. Untouched historical tests still owned moving current

PR validation subsequently exposed old content tests whose historical content contract was correct but whose final current-router assertions still required Decision07 as current.

- run `31477097327`: stale Liana current assertion exposed;
- run `31477218410`: stale Ersa current assertion exposed after Liana repair.

Adversarial readback also pre-checked Cassia and Noble01 for the same pattern rather than waiting for serial CI failures.

Classification: `OMISSION / MUST_FIX`.

Repair preserved each old Decision's immutable domain contract and changed only the moving-current expectation to Decision08.

Focused repair workflow:

- run: `31477395439`
- result: SUCCESS
- commit: `4f6200341a129d2b0f263ef3a0f17b4ec443a76f`

The repaired suite verified Liana, Ersa, Cassia, Noble01 historical contracts while Sedric owns current 8/10.

### 3. Active Context derivative routing drift

Readback showed `ACTIVE_CONTEXT.md` still had a lower `다음 실행 순서` and first-read list centered on Decision07/Liana even after the top current block moved to D08.

Classification: `CONFLICT / MUST_FIX`.

The same stale-consumer repair moved the execution sequence to Decision08, next planning gate to 9/10, and first-read current content owner to Sedric canon while retaining Liana as 7/10 history.

### 4. Roadmap historical ordering needed a stronger regression

A simple token-presence check was insufficient because Decision07 strings could exist elsewhere while the 7/10 historical section itself was absent from the detailed sequence.

Classification: `COMPLEMENT_GAP / SHOULD_FIX`, accepted because it directly protects approved history.

The Decision08 focused test now requires:

`6/10 Noble01 → 7/10 Liana → 8/10 Sedric`

in Roadmap order, and confirms `SOLDIER_02 / LIANA_BERG` is inside the 7/10 historical section.

## Protected design result after repair

Current readback now states:

- `R3_R7_APPROVAL_COUNTER: 8/10`
- `R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-08`
- `R3_R7_RESUME_LOCATOR: COLLECTOR_02_SEDRIC_ARCHIVAL_ACCESSION_APPROVED`
- `PRODUCT_IMPLEMENTATION: BLOCKED`
- `TASK3_IMPLEMENTATION: NOT_APPROVED`

Roadmap explicitly preserves 6/10 Noble01, 7/10 Liana, then 8/10 Sedric.

Sedric remains separated from:

- Ersa: public exhibition evidence/thesis;
- Noble01: physical treatment-depth decision;
- archive/museum operational management.

Same-UID, anti-score, anti-fabrication, anti-management, anti-farming boundaries remain explicit.

`P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED` remains unresolved by Decision08.

## Monitor-loop status before exact-head

Resolved so far:

- `CONFLICT`: repaired.
- `OMISSION`: repaired.
- `COMPLEMENT_GAP`: repaired with stronger historical-order regression.
- `DUPLICATE_WORK`: none observed in the Decision08 branch work; final same-goal PR inventory is still required at exact-head.

Final classification is intentionally not closed yet. It requires fresh open/recent PR recheck, exact-head full CI, merge/main readback, postmerge PR/canon recheck, and Google Sheet same-ID readback.
