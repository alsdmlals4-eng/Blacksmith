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
	item.current_durability = 2
	item.max_durability = 50
	item.physical_state = "ACTIVE"
	return item


func test_action_service_surface_exists() -> void:
	assert_true(ResourceLoader.exists(SERVICE_PATH), "enhancement action service must own destruction archive coupling")


func test_causal_destruction_archives_same_uid_in_one_action_boundary() -> void:
	if not ResourceLoader.exists(SERVICE_PATH):
		return
	var service_script = load(SERVICE_PATH)
	assert_not_null(service_script)
	if service_script == null:
		return
	var envelope = SaveEnvelopeScript.new()
	var item = _item()
	envelope.items_by_uid[item.uid] = item
	var result = service_script.new().resolve_with_rolls(
		envelope,
		item.uid,
		31,
		{
			"success_roll_percent": 99.0,
			"failure_family_roll": 99,
			"current_loss": 2,
			"max_scar_loss": 4,
		},
		3
	)
	assert_eq(result["outcome"], "FAILURE")
	assert_eq(result["failure_family"], "CRITICAL")
	assert_eq(item.physical_state, "DESTROYED")
	assert_eq(item.current_durability, 0)
	assert_true(result["destroyed_history_archived"])
	assert_true(envelope.destroyed_history_by_uid.has(item.uid))
	var archived = envelope.destroyed_history_by_uid[item.uid]
	assert_eq(archived["direct_cause"], "ENHANCEMENT_CRITICAL")
	assert_eq(archived["before_current_durability"], 2)
	assert_eq(archived["before_max_durability"], 50)
	assert_eq(archived["zero_axis"], "CURRENT")


func test_invalid_archive_precondition_blocks_before_item_mutation() -> void:
	if not ResourceLoader.exists(SERVICE_PATH):
		return
	var service_script = load(SERVICE_PATH)
	if service_script == null:
		return
	var envelope = SaveEnvelopeScript.new()
	var item = _item()
	envelope.items_by_uid[item.uid] = item
	envelope.destroyed_history_by_uid[item.uid] = {"conflict": true}
	var before = item.to_dict()
	var result = service_script.new().resolve_with_rolls(
		envelope,
		item.uid,
		31,
		{
			"success_roll_percent": 99.0,
			"failure_family_roll": 99,
			"current_loss": 2,
			"max_scar_loss": 4,
		},
		3
	)
	assert_eq(result["outcome"], "BLOCKED")
	assert_eq(result["reason"], "DESTROYED_HISTORY_UID_CONFLICT")
	assert_eq(item.to_dict(), before)


func test_non_destroying_failure_does_not_create_archive() -> void:
	if not ResourceLoader.exists(SERVICE_PATH):
		return
	var service_script = load(SERVICE_PATH)
	if service_script == null:
		return
	var envelope = SaveEnvelopeScript.new()
	var item = _item()
	item.current_durability = 50
	envelope.items_by_uid[item.uid] = item
	var result = service_script.new().resolve_with_rolls(
		envelope,
		item.uid,
		31,
		{
			"success_roll_percent": 99.0,
			"failure_family_roll": 0,
		},
		3
	)
	assert_eq(result["outcome"], "FAILURE")
	assert_eq(result["failure_family"], "HOLD")
	assert_false(result["destroyed_history_archived"])
	assert_false(envelope.destroyed_history_by_uid.has(item.uid))
