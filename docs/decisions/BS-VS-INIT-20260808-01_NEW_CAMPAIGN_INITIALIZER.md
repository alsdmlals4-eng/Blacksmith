# BS-VS-INIT-20260808-01 — New Campaign Initializer Authority

Status: `USER_APPROVED / TASK2_SCOPED_AUTHORITY / PR131_DRAFT_PENDING_MERGE`

Approved: `2026-08-08 19:28 KST`

Task 2 Decision: `BS-VS-TASK2-20260807-01`

Baseline Blacksmith main: `a00e864ce5de7bdf872e8093d489c8a78c058afb`

Pre-authority PR #131 planning head: `1414cd466e2699a988456151823e8a8119a063fb`

Authority RED: `3ee92073168ed8bdfbb6d666ef75ba3026c39abe` — PR validation failed only because this Decision/design/Entry snapshot did not yet exist.

## Decision

The approved new-campaign initializer contract is:

```text
RUN_ID_FORMAT: RUN-<32_LOWER_HEX>
RUN_ID_SOURCE: CRYPTO_128_BIT_TOKEN
RUN_RNG_SEED_POLICY: RUN_RNG_SEED_FIRST_U32_OF_TOKEN
RUN_RNG_SEED_RANGE: RUN_RNG_SEED_RANGE_0_TO_4294967295
SAVED_AT_UTC_POLICY: UTC_ISO_8601_SECONDS_Z
INITIALIZER_OWNER: VS_RUN_INITIALIZER_SERVICE
FIRST_SAVE_GATE: FIRST_SAVE_REQUIRED_BEFORE_CAMPAIGN_READY
CORRUPT_PRIMARY_VALID_BACKUP_POLICY: PRESERVE_VALID_BACKUP_WHEN_PRIMARY_CORRUPT
GENERAL_PRODUCT_GATE: GENERAL_PRODUCT_BLOCKED
HERA_STATE: HERA_DISABLED_NON_AUTHORITATIVE
```

### 1. Run identity

A dedicated `VSRunInitializerService` obtains exactly 16 bytes from Godot `Crypto.generate_random_bytes(16)` once per New Game creation attempt.

- The 16-byte token is encoded with lowercase hexadecimal text.
- `active_run.run_id = "RUN-" + token.hex_encode()`.
- The resulting identifier is exactly `RUN-` plus 32 lowercase hexadecimal characters.
- The token is generated once for the candidate run and is not regenerated after a successful first save.

The token is an identity/seed initialization input only. Cryptographic randomness is not the gameplay roll engine.

### 2. Run RNG seed

`active_run.run_rng_seed` is the unsigned 32-bit value decoded from bytes 0..3 of the same 16-byte token using Godot `PackedByteArray.decode_u32(0)`.

```text
RUN_RNG_SEED_FIRST_U32_OF_TOKEN
RUN_RNG_SEED_RANGE_0_TO_4294967295
```

All later gameplay RNG that belongs to the run must instantiate/use the project-approved normal PRNG from this persisted seed or a separately approved deterministic derivation. Loading an existing save never regenerates this seed.

### 3. Save timestamp

`saved_at_utc` is produced from Godot system UTC time using second precision:

```gdscript
Time.get_datetime_string_from_system(true, false) + "Z"
```

Serialized contract:

```text
YYYY-MM-DDTHH:MM:SSZ
UTC_ISO_8601_SECONDS_Z
```

This timestamp is metadata, not an RNG source and not part of `run_id` generation.

### 4. Initializer ownership

The only Task 2 owner for creating a brand-new valid run envelope is:

```text
scripts/vertical_slice/services/vs_run_initializer_service.gd
VS_RUN_INITIALIZER_SERVICE
```

It creates the minimum valid current Task 1 envelope:

```text
schema_version = current VSSaveEnvelope schema
preset_version = current VS-2026.08.06-A preset
saved_at_utc = UTC timestamp above
active_run.run_id = RUN-<32 lowercase hex>
active_run.run_rng_seed = first u32 of the same token
active_run.current_day = 1
active_run.resolved_events = {}
items_by_uid = {}
customer_state = {}
schedule_state = {}
global_ledger_sequence = 0
```

It does not create an item, roll a crafting grade, choose a customer, resolve a schedule, or perform gameplay RNG.

### 5. First-save gate

A candidate campaign is not entered merely because an in-memory envelope exists.

```text
FIRST_SAVE_REQUIRED_BEFORE_CAMPAIGN_READY
```

New Game sequence:

1. User initiates New Game.
2. If save artifacts require destructive replacement, explicit overwrite confirmation is required first.
3. `VSRunInitializerService` creates and validates the candidate envelope.
4. `VSSaveService` persists it through the approved atomic path.
5. Only `OK` persistence may emit/enter `campaign_ready` / `BlacksmithApp`.

If validation or persistence fails:

- remain on MainMenu;
- show explicit error/status text;
- emit no `campaign_ready`;
- do not enter `BlacksmithApp`;
- do not regenerate repeatedly as an invisible fallback;
- do not modify gameplay state.

### 6. Safe destructive replacement

UI code never uses `FileAccess` or `DirAccess` for save replacement. Replacement remains owned by `VSSaveService` through a focused method such as `replace_envelope_after_confirmation(envelope)`.

The service validates the new candidate before mutating existing save artifacts.

#### Valid current primary

Use the existing atomic save rotation/rollback behavior: a valid primary may become the backup when the validated new primary is committed.

#### Corrupt primary + valid backup

```text
PRESERVE_VALID_BACKUP_WHEN_PRIMARY_CORRUPT
```

After explicit overwrite confirmation:

- stage and validate the new campaign in the temp path;
- do not delete, overwrite, rotate, or poison the known-valid backup;
- remove/replace only the corrupt primary as required to promote the validated temp;
- if primary promotion fails, the valid backup remains available for recovery;
- never move the corrupt primary over the valid backup.

#### No valid primary or backup

After confirmation where applicable, a validated temp may replace invalid/missing primary state. Failure must not be reported as success, and no invalid artifact may be relabeled as a valid backup.

### 7. Save-status interaction

Task 1 recovery authority remains unchanged:

- valid primary → Continue enabled;
- corrupt primary + valid backup recovered by `VSSaveService` → Continue enabled with explicit recovery status;
- missing save → Continue disabled;
- unrecoverable or unsupported save after recovery attempts → Continue disabled;
- New Game never silently repairs or overwrites without the required explicit confirmation.

## Benchmark record

Godot 4.7 stable APIs support the chosen separation:

- `Crypto.generate_random_bytes()` provides cryptographically secure bytes suitable for one-time identity/seed initialization.
- `PackedByteArray.hex_encode()` provides hexadecimal text and `decode_u32()` provides a bounded 32-bit integer.
- `RandomNumberGenerator`/seeded PRNG behavior is the appropriate deterministic gameplay stream after initialization.
- `Time.get_datetime_string_from_system(true, false)` supplies UTC ISO-style second-precision timestamp text.

Decision comparison:

- **채택:** one 128-bit Crypto token for run identity.
- **수정 채택:** derive the persisted gameplay seed once from the same token, then use the normal seeded PRNG for gameplay rather than Crypto for every roll.
- **채택:** UTC ISO second timestamp for save metadata.
- **비채택:** time-only identifiers/seeds; clock metadata must not be the uniqueness or gameplay-randomness source.
- **비채택:** persistent monotonic counter IDs; they require extra global state and collision/recovery policy outside Task 2.
- **차별점:** run identity and reproducible gameplay seed share one creation token while timestamp remains independent metadata.
- **남은 불확실성:** Android process-death/device filesystem validation and human playtest remain `NOT_RUN`.

## Implementation boundary opened by this Decision

This Decision opens only the following additional Task 2 scoped product surfaces after Entry Gate readback:

```text
scripts/vertical_slice/services/vs_run_initializer_service.gd
scripts/vertical_slice/services/vs_save_service.gd   # focused safe-replacement extension only
```

Existing Task 2 approved surfaces remain:

```text
scripts/vertical_slice/ui/
scenes/vertical_slice/
project.godot
focused tests and CI routing
```

It does **not** open general product implementation, `assets/`, `addons/`, unrelated data/scripts/scenes, image production, HiGodot production authoring authority, Hera activation, Android-device approval, or human-playtest approval.

## Validation requirements

- TDD `RED → GREEN → REFACTOR`.
- Contract must pin the exact strings in this Decision.
- Initializer tests must prove run ID format, seed range/persistence, UTC timestamp format, valid empty envelope, first-save gate, and no gameplay creation/roll side effects.
- Save-service tests must prove valid backup preservation for corrupt-primary replacement.
- Existing Task 1 save/recovery tests must remain GREEN.
- Exact-head PR CI is required before any merge readiness claim.
- PR #131 remains Draft/unmerged until separate explicit merge approval.
