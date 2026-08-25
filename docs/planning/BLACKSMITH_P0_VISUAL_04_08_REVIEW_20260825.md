# Blacksmith P0 Visual GDD 04 / 08 Review · 2026-08-25

- Status: `REVIEW_COMPLETE / READY_FOR_USER_APPROVAL_FOR_GENERATION`
- Work Mode: `PLAN`
- Baseline Blacksmith main: `5117fa0af0f09c6be89d0eeadba53019b14cde96`
- Base fresh-read at task start: `0c5137d96b6a613687d9e8610ad4f26d4a38b75a`
- Reviewed Visual IDs: `BS-VIS-20260820-04`, `BS-VIS-20260820-08`
- `STYLIZED_DARK_FORGE = CURRENT`
- `IMAGE_GENERATION = NOT_RUN`
- `USER_APPROVED_FOR_GENERATION = NOT_GRANTED`
- `FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED`
- `PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`
- Human / Android / accessibility / local Editor / runtime validation: `NOT_RUN`

## 1. Review objective

The remaining two P0 Visual requirements are useful only if they explain something that the six already-approved Visual GDDs do not.

This review therefore applies an **Existing Solution First** rule:

```text
BS-VIS-01 = enhancement main-screen information hierarchy
BS-VIS-02 = dynamic DDD feedback intensity / anticipation-impact-result
BS-VIS-06 = CURRENT/MAX durability semantics and structure-state language

BS-VIS-04 must NOT duplicate 01 or 02.
BS-VIS-08 must NOT duplicate 06.
```

Result:

```text
BS-VIS-04
= STATIC_SCREEN_STATE_MATRIX
= same enhancement screen across all six target-level experience bands

BS-VIS-08
= MAX_PENALTY_STATE_COMPARISON
= same enhancement decision with MAX state as the comparison axis
```

No new mechanic, balance rule, currency, outcome family, or player-facing system is introduced by this review.

---

# 2. Authority used

Current owners consumed by this review:

1. `CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md`
2. `docs/planning/BLACKSMITH_LEVEL_TO_EXPERIENCE_BAND_CANON_20260820.md`
3. `docs/planning/BLACKSMITH_FAILURE_FAMILY_RATIO_CANON_20260820.md`
4. `docs/planning/BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md`
5. `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md`
6. `docs/planning/BLACKSMITH_APPROVED_VISUAL_GDD_CANON_SCRUB_20260825.md`
7. `docs/planning/BLACKSMITH_VISUAL_GDD_IMPLEMENTATION_SAFE_SPEC_20260825.md`
8. Notion `02 · 비주얼 바이블`

Current experience-band authority:

```text
LEARN / BUILD_CONFIDENCE / FIRST_STOP_POINT / TENSION / HIGH_STAKES / MASTERY
```

Current structural-state authority:

```text
MAX determines structure state
```

Current MAX penalty table is:

```text
USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

The review must not visually promote those numeric budgets into a claim of final release balance.

---

# 3. `BS-VIS-20260820-04` · 강화 긴장 밴드 화면 상태

## 3.1 Reviewed role

```text
ROLE = STATIC_SCREEN_STATE_MATRIX
DYNAMIC_FEEDBACK_OWNER = BS-VIS-20260820-02
MAIN_SCREEN_OWNER = BS-VIS-20260820-01
```

`04` should show **one canonical enhancement screen composition repeated across all six experience bands** so a designer or implementer can compare how information emphasis changes as risk rises.

It does **not** own exact animation timing, VFX amplitude, camera shake, or SFX loudness. Those remain `BS-VIS-20260820-02` territory.

## 3.2 Critical correction to the old brief

The old Notion text mentioned only:

```text
LEARN / FIRST_STOP_POINT / TENSION / HIGH_STAKES
```

That is incomplete. The reviewed board must contain all six current bands:

```text
TARGET +1~+2     LEARN
TARGET +3~+10    BUILD_CONFIDENCE
TARGET +11       FIRST_STOP_POINT
TARGET +12~+30   TENSION
TARGET +31~+60   HIGH_STAKES
TARGET +61~+100  MASTERY
```

The band is always determined by **TARGET level**, not current level.

## 3.3 Recommended board composition

16:9 explanatory Visual GDD board with:

1. title + short legend,
2. six equal state panels using the same enhancement screen skeleton,
3. a thin checkpoint strip below the states,
4. a short `what changes / what does not change` section,
5. generation-brief warning that exact runtime values come from current canon/resolvers.

Recommended representative target anchors for explanatory layout only:

| Band | Representative target | Why this anchor is useful |
|---|---:|---|
| LEARN | `+2` | end of safe learning band |
| BUILD_CONFIDENCE | `+10` | break-even/checkpoint state before first structural-risk attempt |
| FIRST_STOP_POINT | `+11` | exact first STOP/PUSH structural-risk attempt |
| TENSION | `+20` | neutral mid-band example |
| HIGH_STAKES | `+40` | avoids confusing band boundary with checkpoint |
| MASTERY | `+70` | demonstrates late mastery without conflating the board with +90 checkpoint or +100 terminal presentation |

These targets are **layout anchors**, not new balance decisions.

## 3.4 Information hierarchy by band

### LEARN

Foreground:

```text
current -> target
final success expectation
attempt gold + 보강재
primary enhance CTA
```

Risk interpretation:
- failure family is HOLD only in the current test budget,
- no durability horror framing,
- short/clean repeated-use presentation.

### BUILD_CONFIDENCE

Foreground:

```text
value/progress confidence
CURRENT when damage becomes relevant
final outcome summary
same-target recovery only after a real failure
```

Do not foreground MAX scar because current BUILD has CRITICAL `0%` in the test budget.

At +10 success, the UI may explain:

```text
break-even recovery point
checkpoint floor +10
next TARGET +11 opens first permanent structural risk
```

### FIRST_STOP_POINT

This must be the clearest STOP/PUSH state.

```text
CURRENT +10
TARGET +11
first structural-risk preview
final success expectation
final per-attempt outcome summary
CURRENT / MAX
same-target recovery
STOP vs PUSH
```

`+11` is the first `FIRST_STOP_POINT`; do not use +9 -> +10 as the risk-entry example.

### TENSION

Foreground:

```text
final success expectation
attempt cost
HOLD / DOWNGRADE / DAMAGE / CRITICAL final outcome summary
CURRENT / MAX
recovery progress
next checkpoint floor
continue / repair / stop when damage exists
```

### HIGH_STAKES

Use the same screen skeleton, but increase **information priority**, not decorative noise.

Foreground:

```text
high accumulated item stake
critical structural risk
CURRENT / MAX
failure consequences
checkpoint protection where applicable
cost / recovery / next meaningful decision
```

### MASTERY

The screen remains operable and readable for repeated attempts.

Foreground:

```text
late-game artifact stake
CURRENT / MAX scars
final success expectation
failure consequences
recovery / checkpoint context
progress toward +100 terminal
```

Do not turn every MASTERY attempt into the +100 completion ceremony. `+100` has its own one-time terminal presentation contract.

## 3.5 Canon-value rule

The generated board may display field labels and representative target anchors, but must not invent authoritative final numbers for:

```text
final_success_rate
attempt_gold_cost
required_common_reinforcement_material
recovery
CURRENT / MAX
final per-attempt family probabilities
structural-scar probability
```

If numbers are used to make the board understandable, they must be explicitly marked `VISUAL EXAMPLE / CURRENT TEST BUDGET` and later pass the same canon scrub rule:

```text
IMAGE_TEXT_NEVER_OVERRIDES_CANON
```

## 3.6 Required non-color differentiation

Each band must differ through at least two non-color channels, such as:

- warning icon shape,
- label / state word,
- panel border weight or break pattern,
- information block prominence,
- crack/wear motif,
- CTA wording / hierarchy,
- risk-summary density.

Color alone is insufficient.

## 3.7 Explicit exclusions

Do not add:

- a seventh gameplay band,
- a band-specific hidden success modifier,
- new checkpoint rules,
- new protection currency,
- different screen navigation per band,
- exact animation durations,
- mandatory unskippable long animation in late bands,
- a claim that checkpoint = save/restore.

### `BS-VIS-20260820-04` review state

```text
REVIEW_COMPLETE / READY_FOR_USER_APPROVAL_FOR_GENERATION
IMAGE_GENERATION = NOT_RUN
```

---

# 4. `BS-VIS-20260820-08` · 구조 손상에 따른 강화 페널티

## 4.1 Reviewed role

```text
ROLE = MAX_PENALTY_STATE_COMPARISON
DURABILITY_SEMANTICS_OWNER = BS-VIS-20260820-06
```

`08` must answer one question:

> 같은 강화 판단에서 MAX 구조 상태가 나빠지면 **무엇이 달라지고, 무엇은 그대로인가?**

It is not another CURRENT/MAX tutorial board.

## 4.2 Core semantic rule

```text
MAX determines structure state
```

MAX state affects:

1. final success expectation through the current MAX success modifier,
2. the amount of **new enhancement effect gained by the current successful attempt** through the current effect multiplier.

It does **not** retroactively reduce already-earned attack/defense/affixes/history.

```text
EXISTING_STATS_UNCHANGED
NEW_ENHANCEMENT_EFFECT_ONLY
```

CURRENT is a separate short-term damage buffer and must not be visually presented as the owner of the success penalty.

## 4.3 Recommended board composition

Use a 16:9 explanatory board with:

1. one same-item / same-target hero comparison,
2. five active MAX state columns,
3. a separate DESTROYED lockout card,
4. a clear `existing power unchanged / new gain modified` before-after strip,
5. a small detail-view decomposition showing where the MAX penalty enters final success expectation.

The board should keep the **same item identity and same TARGET** across comparisons. Do not imply that five different weapons are required to understand the mechanic.

## 4.4 Current active MAX state table

| MAX | State | success modifier | new enhancement effect |
|---:|---|---:|---:|
| `81~100` | `STABLE` | `0pp` | `100%` |
| `61~80` | `STRESSED` | `-3pp` | `100%` |
| `41~60` | `DAMAGED` | `-6pp` | `95%` |
| `21~40` | `FRACTURED` | `-10pp` | `90%` |
| `1~20` | `CRITICAL` | `-15pp` | `80%` |

Separate terminal state:

```text
MAX == 0 OR CURRENT == 0
-> DESTROYED
-> enhancement unavailable
```

The penalty table is:

```text
USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE
```

The board must visibly carry that evidence label. It is an implementation reference for the current test budget, not a release-final balance claim.

## 4.5 Final-success explanation

Basic visual decomposition:

```text
base success
+ same-target recovery
+ current applicable modifiers
+ MAX structure modifier
= final success expectation shown to player
```

The detailed arithmetic may be expanded in a detail view, but the default comparison should emphasize the **delta caused by MAX** rather than dump a formula table on the player.

Do not show an invented fixed final percentage when the actual value depends on target/recovery/current resolver state.

## 4.6 New-effect explanation

The board must show a concrete semantic contrast:

```text
BEFORE CURRENT ATTEMPT
existing attack / defense / affixes / past enhancement rewards
-> UNCHANGED by current MAX penalty

CURRENT SUCCESSFUL ATTEMPT
new enhancement gain
-> multiplied by current MAX state effect multiplier
```

For example, the visual may use a symbolic `new gain × 95%` treatment in DAMAGED state, but must not visually dim or subtract old acquired stats.

## 4.7 CURRENT/MAX separation

`08` must not accidentally suggest:

```text
low CURRENT -> success-rate penalty
```

That is false under current canon.

Recommended presentation:
- keep CURRENT visible as a separate survival buffer,
- label the structural modifier directly on MAX/state,
- use an arrow from `MAX state` to `success modifier` and `new effect multiplier`,
- do not draw that arrow from CURRENT.

## 4.8 Required non-color differentiation

The five active MAX states should use at least two of:

- state word,
- crack geometry,
- frame shape / break count,
- warning icon,
- texture wear,
- penalty label,
- new-gain multiplier label.

The player must not need red/orange/purple hue recognition to understand the state.

## 4.9 Explicit exclusions

Do not add:

- retroactive attack/defense reduction,
- affix degradation,
- hidden destroy probability from low MAX,
- independent MAX-scar roll after CRITICAL,
- CURRENT-based success penalty,
- automatic MAX recovery through normal repair,
- a sixth active penalty band beyond the current five,
- final release-balance claims,
- formula density that requires the player to calculate the decision manually.

### `BS-VIS-20260820-08` review state

```text
REVIEW_COMPLETE / READY_FOR_USER_APPROVAL_FOR_GENERATION
IMAGE_GENERATION = NOT_RUN
```

---

# 5. Alternatives reviewed

## `BS-VIS-04`

### A. Merge 04 into existing 01 + 02
- Advantage: fewer images.
- Failure: makes 01 own too many static states and makes 02 mix static UI hierarchy with motion feedback.
- Decision: `REJECT_AS_PRIMARY`.

### B. Separate six-band static state matrix
- Advantage: one board directly compares the same screen across every canonical target band while preserving 01/02 ownership.
- Maintenance: low, because it consumes existing band/resolver data rather than defining new values.
- Decision: `RECOMMENDED / REVIEWED`.

### C. Six independent full screen Visual GDDs
- Advantage: maximum detail.
- Failure: excessive duplication and future canon-scrub burden.
- Decision: `REJECT`.

## `BS-VIS-08`

### A. Merge penalty explanation into 06
- Advantage: one durability board.
- Failure: 06 becomes overloaded with durability semantics, repair behavior, structure-state signals, success penalties, and growth penalties.
- Decision: `REJECT_AS_PRIMARY`.

### B. Same-item / same-target MAX comparison + five-state strip
- Advantage: isolates MAX as the cause and explicitly shows existing stats unchanged versus new-gain modification.
- Decision: `RECOMMENDED / REVIEWED`.

### C. Formula/table-only documentation
- Advantage: precise.
- Failure: does not meet the Project Home / Visual GDD requirement to explain the mechanic visually in seconds.
- Decision: `REJECT_AS_VISUAL_GDD`.

---

# 6. Five full adversarial review loops

## Loop 1

**Full-scope attack:** owner duplication, canon conflicts, mobile UX, implementation drift, long-term maintenance.

Finding:
- 04 overlapped 01/02.
- 08 overlapped 06.

Validated:
- all three existing Visuals already have explicit owner roles.

Refinement:
- 04 narrowed to `STATIC_SCREEN_STATE_MATRIX`.
- 08 narrowed to `MAX_PENALTY_STATE_COMPARISON`.

Regression recheck:
- no product-rule change.
- no approved Visual is downgraded.

Better alternative search:
- merging boards saves asset count but increases owner ambiguity; rejected.

Long-term fit:
- isolated visual responsibilities reduce future regeneration/scrub cost.

Output: `PASS_WITH_REFINEMENT`.

## Loop 2

**Full-scope re-attack:** complete band/state coverage, numeric authority, user understanding, implementation consumers.

Finding:
- old 04 omitted `BUILD_CONFIDENCE` and `MASTERY`.

Validated:
- Decision15 has exactly six target-level bands.

Refinement:
- require all six bands and explicitly bind band ownership to TARGET level.

08 check:
- preserve five active MAX bands + separate DESTROYED terminal state.

Better alternative search:
- four-state simplification would be easier visually but would hide current canon distinctions; rejected.

Long-term fit:
- exact current enum/band vocabulary is preserved without creating another mapping.

Output: `PASS_WITH_REFINEMENT`.

## Loop 3

**Full-scope re-attack:** misleading visual numbers, final-balance overclaim, formula duplication, player-visible truthfulness.

Finding:
- a new generated board could accidentally turn representative percentages/costs/timings into apparent canon.

Validated:
- current success/MAX penalty values have mixed evidence levels; several are test budgets, not final balance.

Refinement:
- image text never becomes authority.
- 04 uses runtime/resolver fields rather than invented hardcoded rates/costs.
- 08 carries `USER_APPROVED_TEST_BUDGET / NOT_FINAL_PRODUCT_BALANCE` visibly.

Better alternative search:
- removing every number would reduce risk but make 08 less explanatory; retain only current budget labels with explicit evidence status.

Long-term fit:
- later balance tuning does not require changing the visual architecture.

Output: `PASS_WITH_REFINEMENT`.

## Loop 4

**Full-scope re-attack:** mobile readability, accessibility, decorative overload, user decision speed, overlap with DDD animation.

Finding:
- six panels can become an unreadable poster if each reproduces the full mobile screen at equal detail.

Validated:
- the goal is comparative Visual GDD, not six production screenshots.

Refinement:
- same skeleton, limited emphasis delta, concise band labels, shared legend.
- require non-color redundancy.
- exact animation timing remains owned by 02.

08 refinement:
- compare MAX using state label + crack/frame/icon + penalty text, not hue alone.

Better alternative search:
- vertical six-card strip is more mobile-like but worse for side-by-side comparison on a 16:9 internal board; keep 16:9 matrix.

Long-term fit:
- production mobile screens can consume the hierarchy without copying the whole board layout.

Output: `PASS_WITH_REFINEMENT`.

## Loop 5

**Full-scope re-attack:** current authority, same-goal PR collision, implementation boundary, future regeneration, evidence ceiling.

Findings:
- no new blocking visual/canon conflict found after the refinements.
- PR #196 is unrelated and remains read-only.
- no image exists for 04/08, so visual/readability/runtime claims cannot be made.

Verification:
- 04/08 roles are non-duplicative.
- all current band/state names come from current canon.
- test-budget labels are preserved.
- generation remains not run.
- product implementation remains blocked.

Better alternative search:
- no lower-maintenance option preserves the explanatory value without collapsing existing owners.

Long-term fit:
- both briefs can be generated later without introducing a new product dependency.

Output: `CLEAN_REVIEW_EXIT_CANDIDATE` after minimum five full loops.

---

# 7. Review conclusion

Both P0 briefs are now canon-aligned and non-duplicative.

```text
BS-VIS-20260820-04
= REVIEW_COMPLETE / READY_FOR_USER_APPROVAL_FOR_GENERATION

BS-VIS-20260820-08
= REVIEW_COMPLETE / READY_FOR_USER_APPROVAL_FOR_GENERATION
```

This is **not user approval to generate**.

Next gated action:

```text
USER_APPROVAL_FOR_GENERATION
-> generate 04 and 08
-> visual review
-> user approval/reject
-> asset registry / Human Home projection if approved
-> canon scrub if generated raster text introduces illustrative values
```

Until that explicit approval:

```text
IMAGE_GENERATION = NOT_RUN
USER_APPROVED_FOR_GENERATION = NOT_GRANTED
FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED
PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION
```
