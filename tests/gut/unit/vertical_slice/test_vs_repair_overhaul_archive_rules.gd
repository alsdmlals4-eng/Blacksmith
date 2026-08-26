extends "res://addons/gut/test.gd"

const RepairScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")
const OverhaulScript = preload("res://scripts/vertical_slice/resolvers/vs_overhaul_resolver.gd")
const DestroyedRecordScript = preload("res://scripts/vertical_slice/domain/vs_destroyed_history_record.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")


func _item() -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-00112233445566778899aabbccddeeff"
	item.primary_material_id = "iron"
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	item.current_durability = 3
	item.max_durability = 5
	item.repair_job_available = true
	return item


func test_repair_quote_uses_base_max_r_band_and_exactly_one_reinforcement() -> void:
	var resolver = RepairScript.new()
	var quote = resolver.quote(_item())
	assert_true(quote["allowed"])
	assert_eq(quote["missing_current"], 2)
	assert_eq(quote["base_max"], 5)
	assert_eq(quote["r_band"], 125)
	assert_eq(quote["gold_cost"], 39)
	assert_eq(quote["reinforcement_units"], 1)
	assert_false(quote.has("fatigue_cost"))


func test_repair_consumes_one_job_and_never_recovers_max() -> void:
	var resolver = RepairScript.new()
	var item = _item()
	var result = resolver.apply_with_rolls(item, 39, 1, {"quality_roll_percent": 50.0, "scar_roll_percent": 0.0})
	assert_eq(result["status"], "APPLIED")
	assert_eq(result["quality"], "STANDARD")
	assert_true(result["scar_triggered"])
	assert_eq(item.max_durability, 4)
	assert_eq(item.current_durability, 4)
	assert_false(item.repair_job_available)


func test_repair_is_blocked_without_job_for_full_or_destroyed_item() -> void:
	var resolver = RepairScript.new()
	var no_job = _item()
	no_job.repair_job_available = false
	assert_eq(resolver.quote(no_job)["reason"], "REPAIR_JOB_UNAVAILABLE")
	var full = _item()
	full.current_durability = 5
	assert_eq(resolver.quote(full)["reason"], "NO_CURRENT_DAMAGE")
	var destroyed = _item()
	destroyed.current_durability = 0
	destroyed.physical_state = "DESTROYED"
	assert_eq(resolver.quote(destroyed)["reason"], "ITEM_DESTROYED")


func test_overhaul_is_explicitly_superseded() -> void:
	var resolver = OverhaulScript.new()
	assert_eq(resolver.quote(_item())["reason"], "OVERHAUL_SUPERSEDED")
	assert_eq(resolver.apply(_item(), 999999, 99)["reason"], "OVERHAUL_SUPERSEDED")


func test_destroyed_history_record_preserves_damage_cause_zero_axis_and_item_snapshot() -> void:
	var item = _item()
	item.current_durability = 0
	item.physical_state = "DESTROYED"
	var record = DestroyedRecordScript.from_item(item, 3, "ENHANCEMENT_DAMAGE", 1, 5)
	assert_true(record.validation_errors.is_empty())
	assert_eq(record.direct_cause, "ENHANCEMENT_DAMAGE")
	assert_eq(record.before_current_durability, 1)
	assert_eq(record.before_max_durability, 5)
	assert_eq(record.zero_axis, "CURRENT")


func test_destroyed_archive_is_immutable_by_uid_and_round_trips_in_save() -> void:
	var item = _item()
	item.current_durability = 0
	item.physical_state = "DESTROYED"
	var record = DestroyedRecordScript.from_item(item, 3, "ENHANCEMENT_DAMAGE", 1, 5)
	var envelope = SaveEnvelopeScript.new()
	assert_eq(envelope.archive_destroyed_record(record), OK)
	assert_eq(envelope.archive_destroyed_record(record), ERR_ALREADY_EXISTS)
	var serialized = envelope.to_dict()
	var restored = SaveEnvelopeScript.from_dict(serialized)
	assert_eq(restored.destroyed_history_by_uid[item.uid]["direct_cause"], "ENHANCEMENT_DAMAGE")
