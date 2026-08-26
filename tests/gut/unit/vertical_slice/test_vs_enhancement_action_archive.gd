extends "res://addons/gut/test.gd"

const SERVICE_PATH := "res://scripts/vertical_slice/services/vs_enhancement_action_service.gd"
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")


func _item() -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-aabbccddeeff00112233445566778899"
	item.primary_material_id = "iron"
	item.enhancement_level = 30
	item.highest_checkpoint = 30
	item.current_durability = 1
	item.max_durability = 5
	return item


func test_action_service_surface_exists() -> void:
	assert_true(ResourceLoader.exists(SERVICE_PATH), "enhancement action service must own destruction archive coupling")


func test_causal_damage_destruction_archives_same_uid_in_one_action_boundary() -> void:
	var envelope = SaveEnvelopeScript.new()
	var item = _item()
	envelope.items_by_uid[item.uid] = item
	var result = load(SERVICE_PATH).new().resolve_with_rolls(
		envelope, item.uid, 31, {"success_roll_percent": 99.0, "damage_roll_percent": 0.0}, 3
	)
	assert_eq(result["outcome"], "FAILED_DAMAGE")
	assert_eq(item.physical_state, "DESTROYED")
	assert_eq(item.current_durability, 0)
	assert_eq(item.max_durability, 5)
	assert_true(result["destroyed_history_archived"])
	var archived: Dictionary = envelope.destroyed_history_by_uid[item.uid]
	assert_eq(archived["direct_cause"], "ENHANCEMENT_DAMAGE")
	assert_eq(archived["before_current_durability"], 1)
	assert_eq(archived["before_max_durability"], 5)
	assert_eq(archived["zero_axis"], "CURRENT")


func test_invalid_archive_precondition_blocks_before_item_mutation() -> void:
	var envelope = SaveEnvelopeScript.new()
	var item = _item()
	envelope.items_by_uid[item.uid] = item
	envelope.destroyed_history_by_uid[item.uid] = {"conflict": true}
	var before = item.to_dict()
	var result = load(SERVICE_PATH).new().resolve_with_rolls(
		envelope, item.uid, 31, {"success_roll_percent": 99.0, "damage_roll_percent": 0.0}, 3
	)
	assert_eq(result["outcome"], "BLOCKED")
	assert_eq(result["reason"], "DESTROYED_HISTORY_UID_CONFLICT")
	assert_eq(item.to_dict(), before)


func test_failed_hold_does_not_create_archive() -> void:
	var envelope = SaveEnvelopeScript.new()
	var item = _item()
	item.current_durability = 5
	envelope.items_by_uid[item.uid] = item
	var result = load(SERVICE_PATH).new().resolve_with_rolls(
		envelope, item.uid, 31, {"success_roll_percent": 99.0, "damage_roll_percent": 99.0}, 3
	)
	assert_eq(result["outcome"], "FAILED_HOLD")
	assert_false(result["destroyed_history_archived"])
	assert_false(envelope.destroyed_history_by_uid.has(item.uid))
