# Blacksmith Storage·Sales·Chronology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Apply TDD task-by-task.
>
> **Execution Gate:** 사용자 `기획 완료`와 `검수 완료` 전 실행 금지.

**Goal:** 구형 6칸 세션 보관함을 12칸 Vertical Slice 활성 보관함·무손실 회수 대기·영구 Archive로 전환하고, 일반 시장·방문 상인·이름 고객 판매 채널과 장비 UID 연대기를 원자 저장한다.

**Authority:** `BS-EQUIPMENT-LIFECYCLE-20260801-01`.

**Architecture:** `EquipmentStorageService`는 활성 장비와 ForgeOutputReservation을 관리한다. `EquipmentArchive`는 모든 UID 기록을 보유한다. `EquipmentTransactionService`가 일반 시장·방문 상인·이름 고객 채널을 동일한 Intent/ResultEnvelope 저장 경로로 처리한다. ownership, fate, saleability, storage location은 별도 필드다.

**Tech Stack:** Godot 4.7.1, GDScript, JSON, Python validators, headless tests.

## Zero-tolerance gates

```text
GHOST_EQUIPMENT_OR_SLOT = 0
RECOVERED_EQUIPMENT_LOSS = 0
UID_OR_CHRONOLOGY_LOSS = 0
DUPLICATE_TRANSACTION_REWARD = 0
OWNERSHIP_FATE_COLLAPSE = 0
AUTO_SALE_OR_DELIVERY = 0
PLACEHOLDER_CAPACITY_128_150 = 0
PARTIAL_SALE_OR_RECOVERY_SAVE = 0
```

## File Map

### Create

- `scripts/equipment/equipment_record.gd`
- `scripts/equipment/equipment_archive.gd`
- `scripts/storage/equipment_storage_service.gd`
- `scripts/storage/forge_output_reservation.gd`
- `scripts/commerce/equipment_transaction_service.gd`
- `scripts/commerce/general_market_service.gd`
- `scripts/commerce/visiting_merchant_service.gd`
- `data/commerce/general_market_rules.json`
- `data/commerce/visiting_merchant_profiles.json`
- `scripts/ui/storage_controller.gd`
- `scripts/ui/equipment_detail_controller.gd`
- `scripts/ui/equipment_chronology_controller.gd`
- `scripts/ui/sale_channel_controller.gd`
- reusable Scenes for storage/detail/chronology/sales/recovery holding
- `tools/validate_equipment_lifecycle_contract.py`
- `tests/test_equipment_lifecycle_contract.py`
- `tests/unit/test_equipment_storage_service.gd`
- `tests/unit/test_equipment_archive.gd`
- `tests/unit/test_general_market_service.gd`
- `tests/unit/test_visiting_merchant_service.gd`
- `tests/integration/test_forge_output_reservation.gd`
- `tests/integration/test_equipment_sales_transactions.gd`
- `tests/integration/test_equipment_recovery_holding.gd`
- `tests/integration/test_legacy_six_slot_storage_migration.gd`

### Modify

- existing storage/inventory and game-flow PoC files
- forging completion pipeline
- customer delivery pipeline
- `EquipmentWorldRegistry`
- CampaignSnapshot/SaveMigrator
- `tests/README.md`
- `.github/workflows/godot-validation.yml`

---

### Task 1: Freeze equipment record and lifecycle schemas

- [ ] Write Python tests for required fields, ownership/fate separation and chronology event types.
- [ ] Create EquipmentRecord and ChronologyEntry schemas.
- [ ] Validate globally unique equipment UID and chronology entry ID.
- [ ] Require stable summary key+parameters rather than frozen display sentences.
- [ ] Commit: `feat: define equipment lifecycle and chronology schemas`

### Task 2: Active storage, archive and recovery holding

- [ ] Write tests for 12 active slots, unbounded Archive records and lossless recovery holding.
- [ ] Implement distinct services/collections for the three zones.
- [ ] Ensure sold, delivered, lost and destroyed equipment frees active capacity without deleting the record.
- [ ] Full recovery goes to `RECOVERY_HOLDING` and is never auto-sold/deleted.
- [ ] Commit: `feat: separate active storage recovery holding and archive`

### Task 3: Forge output reservation

- [ ] Write race/failure tests for full storage, reservation, sale during forging, cancellation and save failure.
- [ ] Reserve one output slot before forging starts.
- [ ] Consume the reservation in the same revision as UID creation, completion result and storage insertion.
- [ ] Release on cancellation/failure.
- [ ] Verify no empty consumed slot and no unplaced completed equipment.
- [ ] Commit: `feat: reserve forge output slots atomically`

### Task 4: General market service

- [ ] Write tests for eligibility, public price, ownership update, Archive record and duplicate transaction.
- [ ] Implement instant general market sale without relationship or delayed world result.
- [ ] Store `MARKET_SOLD`, sale chronology and final sale snapshot.
- [ ] Use SaleIntent PREPARED and APPLIED ResultEnvelope in one save revision.
- [ ] Commit: `feat: add general market equipment sales`

### Task 5: Visiting merchant service

- [ ] Define data-driven merchant profiles and public category/grade/tag purchase rules.
- [ ] Write tests for offer availability, public modifiers, expired offer and duplicate transaction.
- [ ] Implement no hidden price, bargaining minigame or unlimited reroll.
- [ ] Store `VISITING_MERCHANT_SOLD` and chronology.
- [ ] Commit: `feat: add data-driven visiting merchant sales`

### Task 6: Named customer channel integration

- [ ] Integrate `BS-CUSTOMER-PIPELINE-20260801-01` without creating a fourth transaction engine.
- [ ] Verify named customer equipment cannot be sold through market/merchant while customer-owned.
- [ ] Verify relationship, world result commitment and Archive record share the same UID.
- [ ] Commit: `feat: unify named customer delivery with equipment lifecycle`

### Task 7: Legacy six-slot migration

- [ ] Write fixtures for 0–6 occupied slots and archived/sold/destroyed records.
- [ ] Migrate active equipment into 12 slots preserving order and UID.
- [ ] Remove active product references to `128/150`.
- [ ] Verify no equipment is duplicated, lost or assigned two active slots.
- [ ] Commit: `feat: migrate legacy storage without equipment loss`

### Task 8: Storage, detail, chronology and channel UI

- [ ] Build reusable themed Scenes using `BS-UI-PLATFORM-20260801-01`.
- [ ] Display active/holding/archive counts separately.
- [ ] Provide filters and non-prescriptive sorts; default recent activity.
- [ ] Detail separates owner, fate and saleability.
- [ ] Sale CTA explicitly states channel and ownership consequence.
- [ ] Full-storage screen offers storage, market, customer requests and cancel.
- [ ] Commit: `feat: add equipment storage sales and chronology screens`

### Task 9: Recovery and crash boundaries

- [ ] Write world-result recovery tests with free/full storage and process death at PREPARED/APPLIED/PRESENTED.
- [ ] Assign `PLAYER_WORKSHOP` or `RECOVERY_HOLDING` in the same save revision as RECOVERED fate and chronology.
- [ ] Restart must show the same ResultEnvelope without moving/deleting the equipment twice.
- [ ] Commit: `feat: make equipment recovery lossless and crash-safe`

### Task 10: CI and playtest capacity gate

- [ ] Add validators and tests to CI.
- [ ] Run full save/migration/customer/auto-enhance suites because lifecycle touches all four.
- [ ] Test storage pressure with new players and record creation/sale frequencies.
- [ ] Keep production final capacity and expansion economy `NOT_RUN` until playtest evidence.
- [ ] Add commands:

```bash
python tools/validate_equipment_lifecycle_contract.py
python -m unittest tests/test_equipment_lifecycle_contract.py
godot --headless --path . --script res://tests/unit/test_equipment_storage_service.gd
godot --headless --path . --script res://tests/unit/test_equipment_archive.gd
godot --headless --path . --script res://tests/integration/test_forge_output_reservation.gd
godot --headless --path . --script res://tests/integration/test_equipment_sales_transactions.gd
godot --headless --path . --script res://tests/integration/test_equipment_recovery_holding.gd
godot --headless --path . --script res://tests/integration/test_legacy_six_slot_storage_migration.gd
```

- [ ] Commit: `ci: enforce equipment lifecycle and no-loss contracts`

## Self-review

- Capacity is a Vertical Slice baseline, not an untested production promise.
- Archive and recovery holding prevent destructive pressure.
- Three channels have distinct purpose but shared transaction safety.
- UID and chronology persist after ownership/fate changes.
- Placeholder capacity cannot leak into product.
- Runtime authorization blocked.

```text
PLAN_STATUS: COMPLETE
IMPLEMENTATION_EXECUTION: BLOCKED
```
