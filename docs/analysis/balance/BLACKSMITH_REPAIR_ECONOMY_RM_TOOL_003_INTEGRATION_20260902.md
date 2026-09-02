# Blacksmith Repair Economy → Base RM-TOOL-003 Integration — 2026-09-02

## 1. Authority and scope

- Project decision owner: `BS-REPAIR-20260826-31`
- Project model owner: `tools/run_repair_economy_sensitivity.py`
- Project input: `docs/planning/BLACKSMITH_REPAIR_ECONOMY_SENSITIVITY_INPUT_20260826.json`
- Thin projection adapter: `tools/export_repair_economy_rm_tool_003.py`
- Base analyzer: `tools/reuse_modules/balance_scenario_batch_simulator.py`
- Exact observed Base source: `aaa94caf5772c262f023dd9e80fd4b8bbffd85db`
- Exact analyzer Git blob SHA-1: `a99ae419fd755b6e19f3dee232dd3a11cd74d4ae`
- Tracking issue / PR: `#360` / `#361`

This integration does not change Decision31, the repair formula, the five sensitivity events, the current baseline coefficient, game data, GDScript, Scene, Resource, asset, adopted Base release lock, or final product balance. The project remains the only repair-rule owner. Base receives project-generated neutral run records and performs generic analysis only.

The exact Base checkout is a read-only analysis dependency, not a silent project Base-release adoption. Its commit/blob pin changes only through an explicit compatibility review and repeat execution of this integration contract.

## 2. Before → after

### Before

The 2026-08-22 interoperability Pilot established the intended split:

```text
project rule owner / run generator
→ optional neutral run records
→ Base RM-TOOL-003 shared analyzer
```

However, the optional project-to-Base record route was not implemented. The Base analyzer existed, and Blacksmith had project-owned simulations, but no current repair-economy consumer proved that one project model could generate records which the exact shared analyzer then consumed.

### After

The new adapter calls the current Decision31 sensitivity model and projects its rows into the RM-TOOL-003 manifest without reproducing the repair rules. A dedicated workflow checks out the exact observed Base commit with read-only credentials, verifies the analyzer blob, executes the project adapter, executes the Base CLI, and rejects any unexpected sample, result, or evidence promotion.

```text
Decision31 canon + existing five-event input
→ existing project sensitivity runner
→ 15 neutral run records
→ exact Base RM-TOOL-003 analyzer
→ distribution + same-sample sweep + observed crossing report
```

## 3. Stable sample and data contract

The current input has five named events and three loss coefficients: `0.50`, `0.65`, and `0.80`. The adapter emits `5 × 3 = 15` runs.

Each event receives a stable integer pairing key derived from `BS-REPAIR-20260826-31 + event_id`. The Base manifest field is named `seed`, but in this deterministic model it means **`DETERMINISTIC_PROJECT_CASE_PAIRING_ID_NOT_RNG_SAMPLE`**. It is not evidence that a random simulation occurred or that five events are a statistically representative player population.

Therefore:

- the same event has the same pairing key in every coefficient variant;
- all three variants use the same five-event sample;
- reordering the input array does not change event identity;
- missing or duplicate event/coefficient rows fail closed.

Each run exposes only reusable analysis fields:

- `gold`
- `recovery`
- `loss_ratio`
- `new_current`
- `post_scar_max`
- `material_use`
- `scar_skip_flag`
- project case ID, deterministic pairing key, choice tag, and failure tags

The adapter also preserves source commit, canonical/input payload hashes, Decision ID, project rule owner, Base source identity, dependency role, pin update policy, and evidence ceiling.

## 4. Actual analysis result

At implementation head `323e6258dde670f472d33b90b97ff620f7f52f34`, workflow run `33574124688` verified the exact Base checkout/blob, ran all seven focused tests, and executed the real adapter → Base CLI route.

| loss coefficient `b` | variant | median repair Gold over the same five events |
|---:|---|---:|
| `0.50` | `loss_b_0p5` | `25` |
| `0.65` | `loss_b_0p65` | `31` |
| `0.80` | `loss_b_0p8` | `37` |

The Base analyzer reported one `EXACT_OBSERVED_POINT` at `b=0.65`, because the sweep target is deliberately the current baseline median `31`.

This target is **not** a design target, desired player price, recommended optimum, or shipping threshold. It is a smoke oracle proving that the project baseline and shared analyzer remain connected. The analyzer keeps `automatic_best_value=false` and labels the crossing `OBSERVED_POINT_NOT_PROJECT_TRUTH`.

## 5. What improved

### Actual function

Blacksmith now has one reproducible path that converts current project-owned repair-economy model output into a Base-owned neutral analysis report. The route validates:

- exact project Decision and temporary-budget status;
- exact read-only Base source and analyzer blob;
- explicit manual revalidation before a Base pin change;
- deterministic case-pairing semantics rather than an RNG claim;
- same full seed/pairing sample and same metric sample across variants;
- stable identity under input reordering;
- expected 15-run shape and seven metrics;
- observed medians and crossing behavior;
- mathematical-model/runtime evidence ceiling.

### Expected production effect

This removes the previous manual gap between a project-specific model and the shared analyzer. Future planning comparisons using this current owner can reuse the same adapter contract instead of copying the repair formula into another script or manually reshaping rows.

It also makes sample drift visible. If one coefficient silently loses an event or one metric, the current Base analyzer rejects the sweep rather than calculating a misleading threshold from different samples.

The exact dependency pin prevents a future Base analyzer change from silently altering Blacksmith evidence. Updating that pin is a deliberate integration change with fresh tests, not an automatic Base migration.

### Player-value boundary

The integration can help a later designer compare how a coefficient changes repair cost consistently. It does not establish that `b=0.65` feels fair, produces the intended tension, improves retention, or should ship. Those conclusions still require current runtime linkage and Human/player evidence.

## 6. TDD and regression receipt

- RED head: `b08767929236e11a4860c41c3d3c8f1011ae7458`
- RED run: `33573818821`
- Expected RED: exact Base checkout and blob verification passed; focused integration failed because the project adapter did not exist.
- First implementation head: `ff3a6794fe2cdbfa369e39b5d524218a45741bd2`
- First GREEN attempt exposed one test-oracle wording mismatch: project canon uses `TEMPORARY_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE`, while the test expected the input artifact's shorter `TEMP_TEST...` label.
- Corrected GREEN head: `323e6258dde670f472d33b90b97ff620f7f52f34`
- Corrected GREEN run: `33574124688`
- Focused result: `7 tests / PASS`
- Actual adapter → exact Base CLI: `PASS`
- Same-head Base adoption, thin-adapter, and project-adapter validation: `PASS`

The wording correction changed the test to follow the canonical Decision status. It did not weaken the model or promote a temporary input artifact to canon.

## 7. Evidence ceiling and unverified scope

Verified:

- `PROJECT_MODEL_TO_BASE_ANALYZER_ROUTE_EXECUTED`
- `SAME_FIVE_EVENT_SAMPLE_ACROSS_VARIANTS`
- `EXACT_BASE_SOURCE_AND_BLOB_VERIFIED`
- `PLANNING_MATHEMATICAL_MODEL_OUTPUT_REPRODUCED`

Not verified:

- `RANDOM_OR_MONTE_CARLO_SAMPLE`
- `STATISTICAL_PLAYER_POPULATION_REPRESENTATIVENESS`
- `GODOT_RUNTIME_EQUIVALENCE`
- `REPAIR_UI_RUNTIME`
- `FINAL_PRODUCT_BALANCE`
- `HUMAN_PLAYER_FAIRNESS_OR_FUN`
- `RELEASE_ECONOMY`
- `USER_FINAL_APPROVAL`

The correct Base claim ceiling remains `MATHEMATICAL_MODEL_ONLY_RUNTIME_EQUIVALENCE_NOT_VERIFIED`.

## 8. Rollback

Revert this task's squash commit. The current Decision31 canon, sensitivity input and project model remain unchanged. Remove only the thin adapter, focused tests, dedicated workflow, and this integration report. Do not modify unrelated PM work, open PRs, game data, runtime code, or historical Pilot evidence.
