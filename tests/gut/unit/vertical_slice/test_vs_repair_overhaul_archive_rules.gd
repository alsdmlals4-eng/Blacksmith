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
	item.current_durability = 80
	item.max_durability = 100
	item.enhancement_recovery_by_target = {"11": 2}
	item.physical_state = "ACTIVE"
	return item


func test_repair_quote_matches_current_formula_and_resource_mapping() -> void:
	var resolver = RepairScript.new()
	var item = _item()
	var quote = resolver.quote(item)
	assert_true(quote["allowed"])
	assert_eq(quote["missing_current"], 20)
	assert_eq(quote["gold_cost"], 158)
	assert_eq(quote["reinforcement_units"], 1)
	assert_eq(quote["fatigue_cost"], 2)
	assert_eq(quote["result_current"], 100)
	assert_eq(quote["result_max"], 100)

	item.primary_material_id = "silver"
	item.highest_checkpoint = 30
	item.current_durability = 65
	quote = resolver.quote(item)
	assert_eq(quote["gold_cost"], 333)
	assert_eq(quote["reinforcement_units"], 2)


func test_repair_apply_requires_gold_and_reinforcement_and_never_heals_max() -> void:
	var resolver = RepairScript.new()
	var item = _item()
	item.current_durability = 50
	item.max_durability = 70
	var blocked = resolver.apply(item, 999999, 0)
	assert_eq(blocked["status"], "BLOCKED")
	assert_eq(blocked["reason"], "INSUFFICIENT_REINFORCEMENT")
	assert_eq(item.current_durability, 50)
	assert_eq(item.max_durability, 70)

	var quote = resolver.quote(item)
	var applied = resolver.apply(item, quote["gold_cost"], quote["reinforcement_units"])
	assert_eq(applied["status"], "APPLIED")
	assert_eq(item.current_durability, 70)
	assert_eq(item.max_durability, 70)
	assert_eq(item.enhancement_recovery_by_target, {"11": 2})
	assert_eq(applied["fatigue_cost"], 2)


func test_repair_is_blocked_for_full_or_destroyed_item() -> void:
	var resolver = RepairScript.new()
	var full = _item()
	full.current_durability = 100
	assert_false(resolver.quote(full)["allowed"])
	assert_eq(resolver.quote(full)["reason"], "NO_CURRENT_DAMAGE")
	var destroyed = _item()
	destroyed.current_durability = 0
	destroyed.physical_state = "DESTROYED"
	assert_false(resolver.quote(destroyed)["allowed"])
	assert_eq(resolver.quote(destroyed)["reason"], "ITEM_DESTROYED")


func test_overhaul_quote_and_apply_match_one_lifetime_partial_rescue() -> void:
	var resolver = OverhaulScript.new()
	var item = _item()
	item.primary_material_id = "silver"
	item.enhancement_level = 65
	item.highest_checkpoint = 60
	item.current_durability = 22
	item.max_durability = 35
	var quote = resolver.quote(item)
	assert_true(quote["allowed"])
	assert_eq(quote["gold_cost"], 900000)
	assert_eq(quote["reinforcement_units"], 20)
	assert_eq(quote["fatigue_cost"], 5)
	assert_eq(quote["result_max"], 50)
	assert_eq(quote["result_current"], 50)

	var result = resolver.apply(item, 900000, 20)
	assert_eq(result["status"], "APPLIED")
	assert_eq(item.max_durability, 50)
	assert_eq(item.current_durability, 50)
	assert_true(item.overhaul_used)
	assert_eq(item.enhancement_level, 65)
	assert_eq(item.highest_checkpoint, 60)
	assert_eq(item.enhancement_recovery_by_target, {"11": 2})


func test_overhaul_eligibility_is_strict() -> void:
	var resolver = OverhaulScript.new()
	var item = _item()
	item.enhancement_level = 60
	item.highest_checkpoint = 60
	item.max_durability = 41
	item.current_durability = 41
	assert_eq(resolver.quote(item)["reason"], "MAX_ABOVE_OVERHAUL_THRESHOLD")
	item.max_durability = 40
	item.current_durability = 40
	item.highest_checkpoint = 30
	assert_eq(resolver.quote(item)["reason"], "CHECKPOINT_BELOW_60")
	item.highest_checkpoint = 60
	item.overhaul_used = true
	assert_eq(resolver.quote(item)["reason"], "OVERHAUL_ALREADY_USED")


func test_destroyed_history_record_preserves_cause_zero_axis_and_item_snapshot() -> void:
	var item = _item()
	item.enhancement_level = 31
	item.highest_checkpoint = 30
	item.current_durability = 0
	item.max_durability = 46
	item.physical_state = "DESTROYED"
	var record = DestroyedRecordScript.from_item(
		item,
		3,
		"ENHANCEMENT_CRITICAL",
		2,
		50
	)
	assert_true(record.validation_errors.is_empty())
	assert_eq(record.uid, item.uid)
	assert_eq(record.destroyed_at_game_day, 3)
	assert_eq(record.direct_cause, "ENHANCEMENT_CRITICAL")
	assert_eq(record.before_current_durability, 2)
	assert_eq(record.before_max_durability, 50)
	assert_eq(record.zero_axis, "CURRENT")
	assert_eq(record.item_snapshot["uid"], item.uid)
	assert_eq(record.item_snapshot["enhancement_level"], 31)
	assert_eq(record.item_snapshot["physical_state"], "DESTROYED")


func test_destroyed_archive_is_immutable_by_uid_and_round_trips_in_save() -> void:
	var item = _item()
	item.current_durability = 0
	item.max_durability = 46
	item.physical_state = "DESTROYED"
	var record = DestroyedRecordScript.from_item(item, 3, "ENHANCEMENT_CRITICAL", 2, 50)
	var envelope = SaveEnvelopeScript.new()
	assert_eq(envelope.archive_destroyed_record(record), OK)
	assert_eq(envelope.archive_destroyed_record(record), ERR_ALREADY_EXISTS)
	var serialized = envelope.to_dict()
	assert_true(serialized["destroyed_history_by_uid"].has(item.uid))
	var restored = SaveEnvelopeScript.from_dict(serialized)
	assert_eq(restored.destroyed_history_by_uid[item.uid]["direct_cause"], "ENHANCEMENT_CRITICAL")
