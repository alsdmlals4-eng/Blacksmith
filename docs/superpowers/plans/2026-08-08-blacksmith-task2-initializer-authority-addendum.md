# Blacksmith Task 2 Initializer Authority Addendum

Decision ID: `BS-VS-INIT-20260808-01`

Parent Task 2 Decision: `BS-VS-TASK2-20260807-01`

Status: `USER_APPROVED / ENTRY_GATE_AUTHORITY_ADDENDUM`

This addendum supersedes only the Task 0 blocker and file-boundary portions of `docs/superpowers/plans/2026-08-08-blacksmith-task2-app-shell-routing.md`. All other Task 2 scope, TDD, validation, Android/human/image-rights, Hera, HiGodot, and merge gates remain unchanged.

## Resolved Task 0

The previously missing new-campaign authority is resolved by `BS-VS-INIT-20260808-01`:

```text
RUN_ID = RUN-<32_LOWER_HEX>
TOKEN_SOURCE = Crypto.generate_random_bytes(16)
RUN_RNG_SEED = token.decode_u32(0)
RUN_RNG_SEED_RANGE = 0..4294967295
SAVED_AT_UTC = Time.get_datetime_string_from_system(true, false) + "Z"
INITIALIZER_OWNER = VSRunInitializerService
FIRST_SAVE = REQUIRED_BEFORE_CAMPAIGN_READY
CORRUPT_PRIMARY_VALID_BACKUP = PRESERVE_VALID_BACKUP_WHEN_PRIMARY_CORRUPT
```

Authority RED evidence: `3ee92073168ed8bdfbb6d666ef75ba3026c39abe`.

## Additional approved product files

After same-ID Sheet readback and authority exact-head GREEN, Task 2 may additionally touch:

- Create `scripts/vertical_slice/services/vs_run_initializer_service.gd`
- Modify `scripts/vertical_slice/services/vs_save_service.gd` only for explicit safe replacement after confirmation
- Add focused GUT tests under `tests/gut/unit/vertical_slice/`

No other service/domain expansion is approved.

## Implementation insertion before MainMenu GREEN

### Task A: Initializer service — RED then GREEN

**Tests:** `tests/gut/unit/vertical_slice/test_vs_run_initializer_service.gd`

RED assertions must cover:

- `run_id` matches `^RUN-[0-9a-f]{32}$`;
- `run_rng_seed` is an integer in `0..4294967295`;
- `saved_at_utc` matches UTC second format ending `Z`;
- `current_day == 1` and `resolved_events == {}`;
- items/customer/schedule are empty and global ledger sequence is 0;
- resulting envelope has no validation errors;
- initializer creates no item and resolves no gameplay event.

GREEN implementation belongs only in `vs_run_initializer_service.gd` and may consume current `VSSaveEnvelope`.

### Task B: Safe replacement — RED then GREEN

**Tests:** extend `tests/gut/unit/vertical_slice/test_vs_save_service.gd` or add a focused sibling test.

RED/GREEN cases:

1. valid primary → confirmed new campaign commits and previous primary remains recoverable as backup;
2. corrupt primary + valid backup → confirmed replacement commits new primary while the known-valid backup bytes remain unchanged;
3. forced promotion failure → known-valid backup remains available and the operation returns non-OK;
4. invalid candidate envelope → no existing save artifact changes;
5. UI/direct caller never needs `FileAccess`/`DirAccess` access.

The safe-replacement method must be owned by `VSSaveService`; MainMenu only invokes it after confirmation.

### Task C: MainMenu integration

The parent plan's MainMenu task consumes `VSRunInitializerService` plus the safe replacement method. It may emit `campaign_ready` only after first persistence returns `OK`.

## Exact-head gate

Before implementation RED starts:

```text
BS-VS-INIT-20260808-01 USER_APPROVED
GitHub authority contract GREEN on exact PR head
Development Gates synchronized
Google Sheet same Decision ID synchronized and read back
PR #131 base still current main
no new unresolved reviews/threads/comments
```

If main or PR head changes unexpectedly during this gate, stop and re-read before continuing.
