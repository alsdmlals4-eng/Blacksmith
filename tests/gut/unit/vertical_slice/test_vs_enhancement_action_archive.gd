extends "res://addons/gut/test.gd"

const SERVICE_PATH := "res://scripts/vertical_slice/services/vs_enhancement_action_service.gd"
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const RunInitializerScript = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")


class FakeSaveService:
	extends RefCounted
	var save_error: Error = OK
	var saved_envelope = null

	func save_envelope(candidate) -> Error:
		saved_envelope = candidate
		return save_error


func _item() -> VSItem:
	var item = ItemScript.new()
	item.uid = "BSI-aabbccddeeff00112233445566778899"
	item.primary_material_id = "iron"
	item.enhancement_level = 30
	item.highest_checkpoint = 30
	item.current_durability = 1
	item.max_durability = 5
	return item


func _valid_envelope_with_item() -> VSSaveEnvelope:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var item = _item()
	envelope.items_by_uid[item.uid] = item
	envelope.active_run["selected_item_uid"] = item.uid
	return SaveEnvelopeScript.from_dict(envelope.to_dict())


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


func test_direct_precision_success_commits_the_single_catalyst_keyword() -> void:
	var envelope = SaveEnvelopeScript.new()
	var item = _item()
	item.enhancement_level = 9
	item.highest_checkpoint = 0
	envelope.items_by_uid[item.uid] = item
	var result = load(SERVICE_PATH).new().resolve_with_rolls(
		envelope, item.uid, 10, {"success_roll_percent": 0.0, "damage_roll_percent": 99.0}, 3
	)
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.catalyst_affix, "PRECISION_KEYWORD_PENDING_CONTENT")


func test_saved_enhancement_success_commits_result_and_resource_cost_together() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var resources = WorkshopResourcesScript.new(20000, {"common_reinforcement_material": 10})
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope,
		item.uid,
		31,
		{"success_roll_percent": 0.0, "damage_roll_percent": 99.0},
		3,
		resources,
		save_service
	)
	assert_eq(result["outcome"], "SUCCESS")
	assert_not_null(save_service.saved_envelope)
	assert_eq(item.enhancement_level, 30, "original envelope must remain unchanged until the caller adopts the saved result")
	var saved_item = save_service.saved_envelope.get_item(item.uid)
	assert_eq(saved_item.enhancement_level, 31)
	assert_eq(resources.gold, 20000 - int(result["gold_cost"]))
	assert_eq(
		resources.get_material_count("common_reinforcement_material"),
		10 - int(result["reinforcement_units"])
	)
	assert_eq(save_service.saved_envelope.resource_snapshot(), resources.snapshot())


func test_saved_enhancement_save_failure_keeps_item_and_resources_unchanged() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var resources = WorkshopResourcesScript.new(20000, {"common_reinforcement_material": 10})
	var before_resources = resources.snapshot()
	var save_service := FakeSaveService.new()
	save_service.save_error = ERR_CANT_CREATE
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope,
		item.uid,
		31,
		{"success_roll_percent": 0.0, "damage_roll_percent": 99.0},
		3,
		resources,
		save_service
	)
	assert_eq(result["outcome"], "BLOCKED")
	assert_eq(result["reason"], "SAVE_FAILED:%d" % ERR_CANT_CREATE)
	assert_eq(item.enhancement_level, 30)
	assert_eq(resources.snapshot(), before_resources)


func test_saved_enhancement_rejects_insufficient_material_without_saving() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var resources = WorkshopResourcesScript.new(20000, {"common_reinforcement_material": 0})
	envelope.workshop_resources = resources.snapshot()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope,
		item.uid,
		31,
		{"success_roll_percent": 0.0, "damage_roll_percent": 99.0},
		3,
		resources,
		save_service
	)
	assert_eq(result["outcome"], "BLOCKED")
	assert_eq(result["reason"], "INSUFFICIENT_REINFORCEMENT")
	assert_null(save_service.saved_envelope)
	assert_eq(item.enhancement_level, 30)
