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
	var save_calls := 0

	func save_envelope(candidate) -> Error:
		save_calls += 1
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


func _legacy_v3_envelope_with_affix(affix: String) -> VSSaveEnvelope:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	item.catalyst_affix = affix
	var legacy_source := envelope.to_dict()
	legacy_source["schema_version"] = 3
	legacy_source["preset_version"] = "VS-2026.08.26-C"
	legacy_source.erase("workshop_resources")
	return SaveEnvelopeScript.from_dict(legacy_source)


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
		envelope, item.uid, 10, {"success_roll_percent": 0.0, "damage_roll_percent": 99.0}, 3, _precision_selection()
	)
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.catalyst_affix, "TAG_EMBER_EDGE")
	assert_eq(item.raw_role_stat, 3)
	assert_eq(result.get("precision_tag_id", ""), "TAG_EMBER_EDGE")


func test_missing_precision_selection_blocks_before_cost_material_roll_or_save() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	item.enhancement_level = 9
	item.highest_checkpoint = 0
	var resources = WorkshopResourcesScript.new(20000, {"common_reinforcement_material": 10})
	envelope.workshop_resources = resources.snapshot()
	var before_resources = resources.snapshot()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope,
		item.uid,
		10,
		{"success_roll_percent": 0.0, "damage_roll_percent": 0.0},
		3,
		resources,
		save_service
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "MISSING_CATALYST_LINEAGE")
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(save_service.save_calls, 0)
	assert_eq(item.enhancement_level, 9)
	assert_true(item.catalyst_affix.is_empty())


func test_placeholder_backfill_is_zero_cost_one_time_and_saved_atomically() -> void:
	var envelope = _legacy_v3_envelope_with_affix("PRECISION_KEYWORD_PENDING_CONTENT")
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var resources = WorkshopResourcesScript.new(20000, {"common_reinforcement_material": 10})
	envelope.workshop_resources = resources.snapshot()
	var before_resources = resources.snapshot()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().backfill_precision_tag_and_save(
		envelope, item.uid, _precision_selection(), save_service
	)
	assert_eq(result.get("outcome", ""), "APPLIED")
	assert_eq(result.get("gold_cost", -1), 0)
	assert_eq(result.get("reinforcement_units", -1), 0)
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(item.catalyst_affix, "PRECISION_KEYWORD_PENDING_CONTENT", "original envelope changes only after caller adopts saved envelope")
	assert_eq(save_service.save_calls, 1)
	var saved_item = save_service.saved_envelope.get_item(item.uid)
	assert_eq(saved_item.catalyst_affix, "TAG_EMBER_EDGE")
	assert_eq(saved_item.raw_role_stat, 3)
	var repeat = load(SERVICE_PATH).new().backfill_precision_tag_and_save(
		save_service.saved_envelope, item.uid, _precision_selection(), save_service
	)
	assert_eq(repeat.get("outcome", ""), "BLOCKED")
	assert_eq(repeat.get("reason", ""), "CATALYST_AFFIX_ALREADY_RESOLVED")
	assert_eq(save_service.save_calls, 1)


func test_unknown_nonempty_backfill_affix_fails_closed_before_save() -> void:
	var envelope = _legacy_v3_envelope_with_affix("UNKNOWN_NONEMPTY_AFFIX")
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var before_item = item.to_dict()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().backfill_precision_tag_and_save(
		envelope, item.uid, _precision_selection(), save_service
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "CATALYST_AFFIX_UNKNOWN_FAIL_CLOSED")
	assert_eq(save_service.save_calls, 0)
	assert_eq(item.to_dict(), before_item)


func test_v4_placeholder_backfill_fails_closed_before_save() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	item.catalyst_affix = "PRECISION_KEYWORD_PENDING_CONTENT"
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().backfill_precision_tag_and_save(
		envelope, item.uid, _precision_selection(), save_service
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "PRECISION_PLACEHOLDER_SOURCE_INELIGIBLE")
	assert_eq(save_service.save_calls, 0)
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


func _precision_selection() -> Dictionary:
	return {"lineage_id": "EMBER_LINEAGE", "method_id": "EDGE_REINFORCEMENT"}
