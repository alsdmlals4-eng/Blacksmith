# Blacksmith Project Pause Handoff

- Decision ID: `BS-OPS-20260825-01`
- Date: `2026-08-25 KST`
- Status: `USER_DIRECTIVE / PAUSED_HANDOFF_ONLY`
- Product implementation during this handoff: `NONE`

## 1. Operating decision

The user will work on at most **4 projects concurrently**. Blacksmith is paused until explicitly reactivated after another active project finishes.

While paused:

```text
NO_NEW_IMPLEMENTATION
NO_NEW_PLANNING
NO_NEW_VISUAL_WORK
NO_NEW_PRODUCT_VALIDATION
HANDOFF_AND_READBACK_ONLY
```

## 2. Current authority snapshot

Fresh shutdown readback before this handoff document was recorded:

```yaml
BASE_CURRENT_MAIN: ceb83c680f76fead5811956bd6503fd5e4da8577
BLACKSMITH_PRODUCT_MAIN_BEFORE_HANDOFF_DOC: a27fc0c882b8f397d3db8b5dbfff1a37804fa94b
LAST_COMPLETED_IMPLEMENTATION: TASK4_PRECISION_VISITOR_CONTEXT
LAST_COMPLETED_PR: 198
PREEXISTING_OPEN_DRAFT_PR: 196
HUMAN_PLAYTEST: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY: NOT_RUN
PERFORMANCE: NOT_RUN
```

PR #198 is the last merged product implementation. This pause handoff adds documentation only; the handoff commit does not change the last product implementation boundary.

## 3. Closed Task5 candidate

PR #199 is closed without merge and is **not authority**.

```yaml
PR: 199
STATE: CLOSED_NOT_MERGED
HEAD: e23322007839b5266e157f3f2c70d38a5599f10a
ROLE: NON_AUTHORITATIVE_COMPARISON_EVIDENCE_ONLY
CHANGED_FILES: 3
```

Changed files on the closed candidate:

- `scripts/vertical_slice/resolvers/vs_nadia_schedule_resolver.gd`
- `scripts/vertical_slice/services/vs_day_progression_service.gd`
- `tests/gut/unit/vertical_slice/test_vs_nadia_schedule_resolver.gd`

Exact-head GUT result before shutdown:

```text
132 tests
127 passing
5 failing
784 / 805 asserts passing
```

The already-passing portion proves only partial handoff/schedule-registration behavior on that closed branch. The remaining RED is centered on `VSDayProgressionService.advance_day(...)` and the explicit delayed-result resolution boundary:

1. day increment without implicit Nadia progression,
2. WAIT consuming at most one end-of-day check,
3. ADVANCE moving at most one Nadia schedule stage per day,
4. unknown schedule action blocking atomically before day mutation,
5. withdrawal/result transition requiring explicit resolution payload.

Therefore:

```text
DO_NOT_MERGE_PR199
DO_NOT_CALL_TASK5_IMPLEMENTED
DO_NOT_PORT_PR199_BLINDLY
```

## 4. Resume target

The next intended implementation target remains:

```text
TASK5_NADIA_DELAYED_RESULT
```

On reactivation, create a **new current branch/PR from fresh main**. PR #199 may be inspected only as comparison evidence and any useful code must be re-validated against current canon/tests before selective reuse.

## 5. Resume readback order

Before any new Blacksmith work:

1. Fresh-read Base repository current main and current shared runtime authority.
2. Fresh-read Blacksmith default branch, open PRs, and latest commit.
3. Fresh-read the Blacksmith Google Sheet.
4. Fresh-read Blacksmith Notion Home / Work Plan / Production Handoff / Registry.
5. Report any GitHub-vs-Sheet/Notion conflict before mutation.
6. Confirm PR #196 remains a pre-existing Draft/read-only surface unless the user explicitly changes that boundary.
7. Start Task5 from fresh main with TDD RED-first.

Past chat, memory, prior file snapshots, and closed PR #199 are not current authority by themselves.

## 6. Godot and port operating rule

Because the number of active projects has been reduced, future project operation uses the system's **shared fixed Godot executable + shared fixed ports**.

```text
NO_PROJECT_SPECIFIC_CLOSED_GODOT
NO_PROJECT_SPECIFIC_DEDICATED_GODOT
NO_PROJECT_SPECIFIC_ISOLATED_PORTS
SHARED_FIXED_GODOT_AND_PORTS = FRESH_READ_FROM_CURRENT_SYSTEM_AUTHORITY
```

The concrete shared executable path and port numbers are intentionally **not recorded as guessed values** in this handoff because no current authoritative concrete values were found during shutdown.

Historical Blacksmith-specific runtime values, including the prior dedicated `8006 / 9506` configuration, are:

```text
HISTORICAL_ONLY
DO_NOT_REUSE_AS_RESUME_DEFAULT
```

## 7. Evidence ceiling at pause

Verified before pause:

- Task4 is merged to product main through PR #198.
- PR #199 is closed and not merged.
- PR #196 is the only open Blacksmith PR at shutdown and remains pre-existing/read-only.
- Task5 has partial unmerged branch evidence only and still has 5 failing GUT tests.

Not verified / not run:

- complete Task5 delayed result,
- product screens/routing,
- complete end-to-end release-near lifecycle,
- Human playtest,
- Android device validation,
- accessibility validation,
- performance validation.

## 8. Shutdown rule

After this handoff is synchronized to GitHub, Notion, and Google Sheet, Blacksmith work stops. No further implementation is implied by this document.