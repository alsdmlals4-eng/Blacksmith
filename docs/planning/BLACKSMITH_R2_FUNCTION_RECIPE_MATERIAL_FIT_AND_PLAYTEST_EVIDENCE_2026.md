# Blacksmith R2 Batch 005 Material Recipe Verification Evidence

- Decision: `BS-ITEM-20260806-06`
- Batch: `R2_BATCH_005_10_OF_10`
- Status: `APPROVED_PENDING_MERGE / BATCH_FULL`
- Product implementation: `BLOCKED`

## RED

```text
RED_HEAD=f90dcdf70eabd30ecdde4def11a2ef30112a3caa
RED_PLANNING_FIRST_RUN=283
RED_EXISTING_PASS=76
RED_EXPECTED_FAIL=10
RED_FAILURE_SCOPE=DECISION_10_OF_10_CANON_MATERIAL_FORGING_RECIPE_PLAYTEST_SHEET_ABSENT
```

## GREEN

```text
GREEN_SYNC_HEAD=b9ba179232d7d3a35da7da3e85ce55fee1583503
GREEN_ONE_SHOT_RUN=31064922435
GREEN_FOCUSED_PASS=86
GREEN_CORE_ALIGNMENT=PASS
GREEN_BASE_OPERATING_AUDIT=PASS
GREEN_PROTECTED_PRODUCT_PATH_CHANGES=0
GREEN_PROTECTED_CRAFTING_FILES=UNCHANGED
```

## Initial exact-head validation

```text
INITIAL_EXACT_HEAD=065f3bfd424c79c66a241ccd9d042bef6a939a51
PLANNING_FIRST_RUN=292
PLANNING_FIRST_PASS=87
BASE_ADOPTION_RUN=795
PR_VALIDATION_RUN=1386
PYTHON_OPERATING_GODOT=PASS
```

`Validate Project Base Adapter #39` failed because the pull request merge ref used the pre-#115 adapter workflow and an obsolete protected-baseline selection. Blacksmith main subsequently merged PR #115 (`42bd0b8981567d0c6ccfadfb29654416bb0098da`), which selects the adapter-recorded historical baseline for ordinary planning PRs.

## Long-lived PR adapter correction

```text
ADAPTER_RED_HEAD=a4779f4cd6bc96c57d576adbdeb1a4661d6e969a
ADAPTER_RED_PLANNING_FIRST_RUN=298
ADAPTER_RED_TOTAL_TESTS=92
ADAPTER_RED_PASS=88
ADAPTER_RED_EXPECTED_FAIL=4
ADAPTER_GREEN_MERGE_HEAD=834e8659aa5ce4e9296197e9fdb82ab8d1bf6019
ADAPTER_GREEN_ONE_SHOT_RUN=31066394991
ADAPTER_GREEN_FOCUSED_PASS=92
ADAPTER_GREEN_CONTRACT=PASS
ADAPTER_GREEN_PROTECTED_PRODUCT_PATHS=PASS
```

The correction compares the original pull-request base with the actual pull-request head, reads the current adapter-recorded protected baseline for ordinary planning PRs, checks ancestry against the latest base tip, and refreshes the raw-byte health evidence hash for `CURRENT_CONFIRMED_DECISIONS.md`.

## Final PR validation trigger

```text
CURRENT_MAIN_SYNCED=308cd42bbd4d86e0ca5d91d43e570017ac9a985b
PREVIOUS_REF_MOVE_DID_NOT_EMIT_PULL_REQUEST_SYNCHRONIZE=true
CURRENT_TRIGGER=HUMAN_AUTHORED_CONNECTOR_COMMIT
REQUIRED_RESULT=PLANNING_THIN_BASE_PR_PROJECT_ADAPTER_ALL_PASS_ON_ONE_HEAD
```

The evidence test reads this document rather than accepting constant self-comparisons. Merge approval remains blocked until the corrected Project Base Adapter workflow and the complete PR validation set pass on the same final head.

## Protection

```text
HUMAN_PLAYTEST=NOT_RUN
PRODUCT_IMPLEMENTATION=BLOCKED
PR_STATE=DRAFT_UNMERGED
```
