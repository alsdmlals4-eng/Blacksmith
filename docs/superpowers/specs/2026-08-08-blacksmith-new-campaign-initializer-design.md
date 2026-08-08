# Blacksmith New Campaign Initializer Design

Decision ID: `BS-VS-INIT-20260808-01`

Status: `USER_APPROVED / TASK2_SCOPED_AUTHORITY`

## Goal

Create a brand-new Task 2 campaign envelope without inventing gameplay facts, while guaranteeing stable run identity, a persisted deterministic run RNG seed, UTC save metadata, a successful first atomic save before application entry, and preservation of a known-valid backup during destructive replacement.

## Architecture

`VSRunInitializerService` owns only in-memory creation of the minimal valid `VSSaveEnvelope`. It obtains one 16-byte `Crypto` token, derives `RUN-<32 lowercase hex>` plus the persisted unsigned 32-bit run seed, and stamps UTC second-precision metadata. `VSSaveService` remains the sole persistence/replacement owner; MainMenu coordinates confirmation/status but never manipulates files.

## Exact creation contract

```text
TOKEN = Crypto.generate_random_bytes(16)
RUN_ID = "RUN-" + TOKEN.hex_encode()
RUN_RNG_SEED = TOKEN.decode_u32(0)
SAVED_AT_UTC = Time.get_datetime_string_from_system(true, false) + "Z"
CURRENT_DAY = 1
RESOLVED_EVENTS = {}
ITEMS = {}
CUSTOMER_STATE = {}
SCHEDULE_STATE = {}
GLOBAL_LEDGER_SEQUENCE = 0
```

The run seed range is `0..4294967295`. A zero seed is valid because the existing save schema accepts non-negative run seeds.

The timestamp is metadata only. It is not used as a run ID or RNG seed source.

## Responsibilities

### VSRunInitializerService

- generate exactly one 128-bit creation token for one candidate run;
- construct the run ID and seed from that token;
- stamp UTC save metadata;
- create no items or gameplay outcomes;
- return a candidate only if `validation_errors` is empty.

### VSSaveService

- validate before mutation;
- perform first save and destructive replacement;
- preserve existing Task 1 load/recovery behavior;
- preserve a known-valid backup when primary is corrupt;
- report failure as failure with no app-entry side effect.

### VSMainMenu

- present missing/loadable/recovered/unrecoverable status;
- require overwrite confirmation when replacement is destructive;
- ask initializer/service to create/persist;
- enter `BlacksmithApp` only after save returns `OK`;
- never use `FileAccess` or `DirAccess` directly.

## Safe replacement state table

| Existing state | New Game action after confirmation | Required backup behavior |
| --- | --- | --- |
| no primary, no backup | stage validated candidate and promote | no backup invented |
| valid primary | existing atomic rotation/rollback | prior valid primary may become backup |
| corrupt primary + valid backup | stage candidate; replace corrupt primary only | valid backup remains untouched |
| missing primary + valid backup | stage/promote candidate | valid backup remains untouched |
| corrupt/unsupported with no valid recovery | stage validated candidate, then replace invalid primary state | never label invalid artifact as valid backup |

Any failed promotion keeps MainMenu active and emits no campaign-ready signal.

## Determinism boundary

Crypto is used once for run creation. Gameplay rolls do not repeatedly use Crypto. The persisted `run_rng_seed` is the deterministic authority consumed by later approved gameplay services, which must preserve resolved results and must not reroll on load.

## TDD boundary

Authority RED exact head: `3ee92073168ed8bdfbb6d666ef75ba3026c39abe`.

Observed RED: the routed Python authority contract failed because the approved Decision/design/Entry snapshot were absent; all earlier document/governance contracts in that step passed.

GREEN requires:

- Decision record exists and matches exact contract tokens;
- this design exists;
- Task 2 Entry Gate snapshot resolves only the initializer blocker;
- Development Gates records the same Decision and scoped RED permission;
- same Decision ID is written to Google Sheet and read back;
- exact-head PR workflows pass.

## Scope

Additional approved Task 2 implementation surfaces:

```text
scripts/vertical_slice/services/vs_run_initializer_service.gd
scripts/vertical_slice/services/vs_save_service.gd  # focused safe replacement extension
```

No general product, asset, addon, Hera, HiGodot-authority, Android-device, image-rights, or human-playtest gate is opened by this design.
