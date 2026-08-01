# Blacksmith Customer Common Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Apply TDD task-by-task.
>
> **Execution Gate:** 사용자 `기획 완료`와 `검수 완료` 전 실행 금지.

**Goal:** 카일·철검·검투사 경기 중심 PoC를 수집가·모험가·검투사·군인 4유형과 이름 고객 8명이 공통 요청·적합도·인계·관계·세계 결과·저장 파이프라인을 재사용하는 구조로 전환한다.

**Authority:** `BS-CUSTOMER-PIPELINE-20260801-01`.

**Architecture:** 고객 이름은 정의 데이터, 유형 차이는 평가·세계 결과 Profile에 둔다. Core Engine은 `CustomerTypeDefinition`, `NamedCustomerDefinition`, `RequestTemplate`, `CustomerContract`, `CustomerRelationship`, `DeliveryIntent`, `WorldOutcomeProfile`만 이해한다. 고객 이름을 기준으로 switch하지 않는다. 인계와 세계 결과는 `BS-SAVE-20260801-01`의 AttemptIntent/ResultEnvelope와 동일 revision에 저장한다.

**Tech Stack:** Godot 4.7.1, GDScript, JSON, Python validators, headless SceneTree tests, Android portrait UI.

## Global zero-tolerance gates

```text
DUPLICATE_CUSTOMER_ID = 0
CUSTOMER_NAME_SWITCH_IN_CORE_ENGINE = 0
EXACT_ITEM_ID_HARDCODED_REQUEST = 0
AUTO_RECOMMEND_OR_AUTO_SELECT = 0
DUPLICATE_DELIVERY_REWARD = 0
DUPLICATE_WORLD_RESULT_APPLY = 0
RESULT_REROLL_AFTER_RESTART_OR_ERROR = 0
LEGACY_KYLE_HISTORY_LOSS = 0
PARTIAL_DELIVERY_SAVE = 0
```

## File Map

### Create

- `data/customers/customer_types.json`
- `data/customers/named_customers.json`
- `data/customers/request_templates.json`
- `data/customers/world_outcome_profiles.json`
- `scripts/customers/customer_definition_registry.gd`
- `scripts/customers/request_offer_service.gd`
- `scripts/customers/customer_fit_resolver.gd`
- `scripts/customers/customer_relationship_registry.gd`
- `scripts/customers/customer_delivery_service.gd`
- `scripts/world/common_world_outcome_resolver.gd`
- `scripts/ui/customer_board_controller.gd`
- `scripts/ui/customer_request_detail_controller.gd`
- `scripts/ui/customer_delivery_controller.gd`
- `scenes/ui/customer_board.tscn`
- `scenes/ui/customer_request_detail.tscn`
- `scenes/ui/customer_delivery.tscn`
- `tools/validate_customer_contract.py`
- `tests/test_customer_contract.py`
- `tests/unit/test_customer_definition_registry.gd`
- `tests/unit/test_customer_fit_resolver.gd`
- `tests/unit/test_customer_relationship_registry.gd`
- `tests/unit/test_common_world_outcome_resolver.gd`
- `tests/integration/test_customer_common_pipeline.gd`
- `tests/integration/test_legacy_kyle_customer_migration.gd`
- `tests/integration/test_customer_delivery_recovery.gd`

### Modify

- `scripts/customers/customer_contract.gd`
- `scripts/ui/customer_contract_screen.gd`
- `scripts/poc/equipment_lifecycle_poc_controller.gd`
- `scripts/world/equipment_world_registry.gd`
- `scripts/world/world_activity_resolver.gd`
- future `scripts/application/app_state_coordinator.gd`
- future `scripts/application/save/save_migrator.gd`
- future `scripts/application/results/result_envelope.gd`
- `tests/integration/test_equipment_lifecycle_poc.gd`
- `tests/README.md`
- `.github/workflows/godot-validation.yml`

---

### Task 1: Freeze customer definitions and schema

- [ ] Write failing Python contract tests for exact customer types and eight unique Customer IDs.
- [ ] Create customer type definitions for `COLLECTOR`, `ADVENTURER`, `GLADIATOR`, `SOLDIER`.
- [ ] Create named customer definitions:

```text
ERSA_ROEN / SEDRIC_VAEL
NADIA_VENN / TOREN_MARCH
CASSIA_BELLAN / KYLE_VAREN
MAREK_OLDEN / LIANA_BERG
```

- [ ] Validate minimum two named customers per type, one representative per type, valid profile references and no duplicate IDs.
- [ ] Record `gladiator_kyle → KYLE_VAREN` only in migration aliases, not as an active duplicate customer.
- [ ] Run:

```bash
python tools/validate_customer_contract.py
python -m unittest tests/test_customer_contract.py
```

- [ ] Commit: `feat: define customer types and named customer data`

### Task 2: Definition registry and request templates

- [ ] Write `test_customer_definition_registry.gd` for lookup, duplicate rejection, missing profile and minimum-per-type validation.
- [ ] Implement `CustomerDefinitionRegistry` as read-only indexed definitions.
- [ ] Define request templates by equipment category, required tags, preferred/disliked tags, duration and reward formula.
- [ ] Reject exact `iron_sword` item requirements in active templates.
- [ ] Keep default duration at two business days; template override must be explicit.
- [ ] Commit: `feat: load customer definitions and category request templates`

### Task 3: Eligibility and public fit resolver

- [ ] Write fixtures for eligible high fit, eligible low fit, ineligible category, non-owned, incomplete and non-sellable equipment.
- [ ] Implement eligibility as a boolean decision with explicit reason codes.
- [ ] Implement fit score 0–100 from grade, lineage, secondary affixes, special evolution, enhancement level, chronology/fate and value tags.
- [ ] Return at least one positive and one negative/neutral reason when applicable.
- [ ] Do not sort, recommend or select equipment automatically.
- [ ] Verify eligible low-fit equipment remains deliverable.
- [ ] Commit: `feat: separate customer eligibility from disclosed fit`

### Task 4: Contracts, offers and per-customer relationships

- [ ] Write state-transition tests for OFFERED→ACCEPTED→READY→DELIVERED→RESULT_PENDING→RESULT_READY→CLOSED and failure states.
- [ ] Implement active request limit two across all named customers.
- [ ] Implement relationship records keyed by `customer_id`, not one global integer.
- [ ] Store accepted-condition snapshot so later balance changes do not rewrite an existing contract.
- [ ] Use event IDs for idempotent acceptance, expiration and closure.
- [ ] Commit: `feat: add common contracts offers and per-customer relationships`

### Task 5: Atomic delivery transaction

- [ ] Write crash-boundary tests before and after `DeliveryIntent PREPARED` and APPLIED ResultEnvelope save.
- [ ] Implement order:

```text
revalidate contract/equipment/ownership/fit
→ DeliveryIntent PREPARED save
→ ownership/reward/relationship/registry changes in working state
→ contract RESULT_PENDING
→ ResultEnvelope APPLIED in same revision
→ result presentation
```

- [ ] Duplicate `delivery_transaction_id` must return the existing result without a second reward.
- [ ] Any save failure leaves ownership, gold, relationship and registry unchanged.
- [ ] Commit: `feat: make customer delivery atomic and idempotent`

### Task 6: Common world outcome resolver and profiles

- [ ] Write one profile test per customer type plus deterministic commitment/retry tests.
- [ ] Implement one resolver that consumes equipment snapshot, customer/type profile and committed random values.
- [ ] Keep result candidates and weights in `world_outcome_profiles.json`.
- [ ] Prohibit customer-name switches in resolver code.
- [ ] Store `RESULT_ERROR` with cause; retry must reuse the same commitment and event ID.
- [ ] Apply ownership, fate, relationship, reputation, resources and chronology in one ResultEnvelope/save revision.
- [ ] Commit: `feat: resolve type-specific world outcomes through one engine`

### Task 7: Customer Board, request detail and delivery UI

- [ ] Write controller tests for four-type filters, active limit, disclosed conditions and no automatic recommendation.
- [ ] Build reusable scenes with 48dp minimum targets and text/status alternatives to color.
- [ ] Customer Board shows name, role, type, deadline, category, reward kind and state.
- [ ] Request Detail separates required and preferred conditions.
- [ ] Delivery selection shows eligibility, fit, positive/negative reasons and ownership consequence.
- [ ] Final button text: `이 장비를 인계한다`.
- [ ] Result view consumes stored ResultEnvelope only.
- [ ] Commit: `feat: add common customer request and delivery screens`

### Task 8: Legacy Kyle migration and PoC preservation

- [ ] Write migration fixtures containing `gladiator_kyle`, relationship value, active contract, delivered equipment and world-event history.
- [ ] Map to `KYLE_VAREN` once while preserving contract IDs, relationship, equipment UID, delivery transaction and chronology.
- [ ] Convert old exact iron-sword contract into a legacy frozen condition snapshot without changing its historical result.
- [ ] Reclassify old Kyle tests as legacy migration evidence; do not delete them.
- [ ] Commit: `feat: preserve Kyle customer history during common-pipeline migration`

### Task 9: Representative vertical-slice fixtures

- [ ] Create complete reusable fixtures for Cassia, Ersa, Nadia and Marek.
- [ ] Create definition/contract fixtures for Sedric, Toren, Kyle and Liana.
- [ ] Assert the four representatives use the same service classes and result envelope structure.
- [ ] Assert adding a new named customer JSON does not require editing Core Engine files.
- [ ] Commit: `test: prove four customer types reuse the common pipeline`

### Task 10: Save integration, CI and external gates

- [ ] Add CampaignSnapshot fields for customer definition version, active/history contracts, relationships, offer rotation and world commitments.
- [ ] Add save migration validation for customer aliases and dangling references.
- [ ] Add CI commands:

```bash
python tools/validate_customer_contract.py
python -m unittest tests/test_customer_contract.py
godot --headless --path . --script res://tests/unit/test_customer_definition_registry.gd
godot --headless --path . --script res://tests/unit/test_customer_fit_resolver.gd
godot --headless --path . --script res://tests/unit/test_customer_relationship_registry.gd
godot --headless --path . --script res://tests/unit/test_common_world_outcome_resolver.gd
godot --headless --path . --script res://tests/integration/test_customer_common_pipeline.gd
godot --headless --path . --script res://tests/integration/test_legacy_kyle_customer_migration.gd
godot --headless --path . --script res://tests/integration/test_customer_delivery_recovery.gd
```

- [ ] Keep Android safe-area, visual readability and six-person comprehension tests `NOT_RUN` until executed.
- [ ] Commit: `ci: enforce customer pipeline reuse and idempotency`

## Self-review

- Four types and eight names: exact.
- Category eligibility vs fit: explicit.
- Low fit sale: preserved.
- No auto recommend/select: explicit.
- One resolver and no name switch: explicit.
- Save/recovery/idempotency: explicit.
- Legacy Kyle preservation: explicit.
- Runtime authorization: blocked.

```text
PLAN_STATUS: COMPLETE
IMPLEMENTATION_EXECUTION: BLOCKED
```
