# Blacksmith Validation·Evidence·Telemetry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans after all feature implementation plans are approved and implemented in dependency order.
>
> **Execution Gate:** 사용자 `기획 완료`와 `검수 완료` 전 실행 금지. Android·사람·성능 단계는 실제 환경 없이 PASS 처리 금지.

**Goal:** 모든 승인 Decision을 validator·unit·integration·product flow·visual·Android·human evidence와 연결하고, 과거 PoC 증거를 역사 기준선으로 분리하며, 비식별 로컬 텔레메트리로 플레이테스트 문제를 재현한다.

**Authority:** `BS-VALIDATION-20260801-01`.

**Architecture:** `DecisionValidationRegistry`가 Decision ID별 canonical source, affected paths, validators, tests and external gates를 기록한다. `FixtureRegistry`는 committed randomness와 expected digests/envelopes/chronology를 보유한다. CI는 동일 head의 required lane을 실행한다. `LocalTelemetryRecorder`는 allowlist event만 JSONL로 rotation하고 수동 export만 제공한다.

## Zero-tolerance gates

```text
PASS_WITH_NOT_RUN = 0
CURRENT_HEAD_USING_OTHER_COMMIT_EVIDENCE = 0
HISTORICAL_POC_AS_CURRENT_V9_PASS = 0
RUNTIME_REROLL_FOR_TESTING = 0
PERSONAL_OR_STABLE_DEVICE_DATA = 0
NETWORK_AUTO_UPLOAD = 0
UNKNOWN_TELEMETRY_PAYLOAD_KEY = 0
MISSING_DECISION_VALIDATION_LINK = 0
```

## File Map

### Create

- `docs/validation/DECISION_VALIDATION_REGISTRY.json`
- `tests/fixtures/FIXTURE_REGISTRY.json`
- `docs/validation/EVIDENCE_INDEX.json`
- `docs/validation/evidence/`
- `scripts/diagnostics/local_telemetry_recorder.gd`
- `scripts/diagnostics/telemetry_event_allowlist.gd`
- `scripts/diagnostics/diagnostic_export_service.gd`
- `data/diagnostics/telemetry_event_schema.json`
- `tools/validate_decision_coverage.py`
- `tools/validate_fixture_registry.py`
- `tools/validate_evidence_index.py`
- `tools/validate_telemetry_contract.py`
- `tests/test_decision_coverage.py`
- `tests/test_fixture_registry.py`
- `tests/test_evidence_index.py`
- `tests/test_telemetry_contract.py`
- `tests/unit/test_local_telemetry_recorder.gd`
- `tests/integration/test_diagnostic_export_service.gd`
- product-flow headless runner and fixtures

### Modify

- `.github/workflows/godot-validation.yml`
- `tests/README.md`
- current implementation plans and status documents
- Settings UI for diagnostics consent/delete/export
- release packaging checks

---

### Task 1: Decision Validation Registry

- [ ] Write tests requiring every active implementation Decision to have canonical Markdown/JSON, affected paths, validator, automated tests and external gates.
- [ ] Register Save, Migration, Customer, Auto Enhance, Equipment Lifecycle, Visual Asset, UI Platform and Base Migration Decisions.
- [ ] Record current evidence maturity E0 for design-only systems.
- [ ] Reject superseded Decision IDs as active implementation authority.
- [ ] Commit: `docs: register Decision validation coverage`

### Task 2: Fixture Registry

- [ ] Define the approved fixture schema.
- [ ] Register save/recovery, legacy migration, customer8, auto boundaries, storage/sales and UI/platform families.
- [ ] Store committed random values and expected state digests rather than calling randomize.
- [ ] Validate unique fixture IDs and valid Decision links.
- [ ] Commit: `test: establish deterministic fixture registry`

### Task 3: Static validation lane

- [ ] Implement validators for canonical Decision uniqueness/supersedes, GitHub↔Sheet mapping export, Base release/hash, data references, placeholders, assets/licenses and registries.
- [ ] Keep network connector checks separate from local deterministic validators.
- [ ] Produce machine-readable result summaries with commit SHA.
- [ ] Commit: `ci: add authority and data static validation lane`

### Task 4: Unit and transaction integration lanes

- [ ] Assemble commands from the Save, Migration, Customer, Auto Enhance, Lifecycle and UI plans.
- [ ] Add unit tests by domain and integration tests by transaction boundary.
- [ ] Ensure transaction tests assert state digest, ResultEnvelope, chronology and idempotency together.
- [ ] Keep historical PoC tests under an explicit legacy lane.
- [ ] Commit: `ci: add v9 unit and transaction integration lanes`

### Task 5: Product-flow headless lane

- [ ] Create a headless runner for Boot→Main→App Shell→Forge→Enhance→Storage/Sale/Customer→World Result→Chronology→Restart.
- [ ] Add happy, failure, interruption and migration flows.
- [ ] Assert the product main Scene is not a test Scene before marking lane PASS.
- [ ] Capture deterministic state digests at each boundary.
- [ ] Commit: `test: add current v9 headless product-flow validation`

### Task 6: Evidence index and reports

- [ ] Implement evidence schema and index validator.
- [ ] Every run records Decision IDs, repo/branch/commit, command/procedure, environment, exit, result, artifact and limitations.
- [ ] Mark code-dependent evidence stale when current head changes.
- [ ] Preserve FAILED/BLOCKED/NOT_RUN entries.
- [ ] Generate concise evidence summary for PR and Sheet without copying full logs.
- [ ] Commit: `docs: track verifiable product evidence by commit`

### Task 7: Local telemetry schema and recorder

- [ ] Write contract tests for event allowlist, payload allowlist and forbidden data.
- [ ] Implement random per-session ID with no persistent device identifier.
- [ ] Write JSONL under `user://diagnostics/` with size, 20-session and 30-day rotation.
- [ ] Reject unknown event/payload keys instead of serializing arbitrary dictionaries.
- [ ] Hash internal equipment UID per session when needed.
- [ ] Keep network code absent.
- [ ] Commit: `feat: add privacy-first local diagnostic telemetry`

### Task 8: Consent, delete and manual export

- [ ] Development/internal builds default local on; external playtest requires explicit consent; general release defaults off.
- [ ] Add settings controls to view status, delete local records and manually export.
- [ ] Before export show categories, period and size.
- [ ] Export only telemetry JSONL/summary; exclude saves, license proofs and personal files.
- [ ] Write consent/off/delete/export tests.
- [ ] Commit: `feat: add explicit local diagnostics controls and export`

### Task 9: Visual, Android and human evidence procedures

- [ ] Link screenshot baselines from the visual asset plan.
- [ ] Define exact Android APK/AAB/device matrix and performance capture procedure.
- [ ] Define six-person scripts for main/save trust, risk/auto stop, customer fit/ownership, chronology and accessibility.
- [ ] Record actual results under E4–E7 only after execution.
- [ ] Never infer PASS from screenshots or automated logs alone.
- [ ] Commit: `docs: define external validation evidence procedures`

### Task 10: CI required checks and release gates

- [ ] Add required PR jobs:

```text
static_contracts
python_unit
Godot_import_and_unit
Godot_integration
product_flow_headless
protected_path_and_placeholder
```

- [ ] Add manual/scheduled evidence workflows without making unexecuted jobs appear green.
- [ ] Fail release packaging for Decision coverage gaps, stale evidence, placeholder leakage, invalid asset/license state or missing required device/human approval.
- [ ] Update tests README to separate current v9, legacy PoC and external gates.
- [ ] Commit: `ci: enforce evidence maturity and release validation gates`

### Task 11: Pass3 adversarial review

- [ ] Re-run all current-authority, data, plan, Sheet, path and evidence audits.
- [ ] Attack missing Decision coverage, stale PoC authority, false PASS, nondeterministic fixture, telemetry privacy and cross-source drift.
- [ ] Require new P0/P1 planning findings = 0 before planning-complete candidate.
- [ ] Publish exact unresolved runtime/device/human gates.
- [ ] Commit: `review: complete Blacksmith planning adversarial pass 3`

## Self-review

- Evidence levels separate design, automation, rendering, device and human proof.
- Historical PoC remains useful but cannot certify v9.
- Fixture randomness is committed and deterministic.
- Telemetry is local, allowlisted, non-personal and manually exported.
- PASS requires actual current-head evidence.
- Runtime execution authorization blocked.

```text
PLAN_STATUS: COMPLETE
IMPLEMENTATION_EXECUTION: BLOCKED
```
