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
	var legacy_source := envelope.to_dict()
	var legacy_item: Dictionary = legacy_source["items_by_uid"][item.uid]
	legacy_item["schema_version"] = 3
	legacy_item["catalyst_affix"] = affix
	legacy_source["schema_version"] = 3
	legacy_source["preset_version"] = "VS-2026.08.26-C"
	legacy_source.erase("workshop_resources")
	return SaveEnvelopeScript.from_dict(legacy_source)


func _seeded_ember_item_at_nineteen(envelope) -> VSItem:
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	item.enhancement_level = 19
	item.highest_checkpoint = 10
	item.current_durability = 5
	item.max_durability = 5
	item.catalyst_affix["tag_entries"] = [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}]
	item.used_precision_milestones.clear()
	item.used_precision_milestones.append(10)
	return item


func _resources(gold: int = 20000, common_materials: int = 10, heart_of_flame: int = 10, earth_crystal: int = 10):
	return WorkshopResourcesScript.new(gold, {
		"common_reinforcement_material": common_materials,
		"heart_of_flame": heart_of_flame,
		"earth_crystal": earth_crystal,
	})


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


func test_direct_precision_success_commits_the_catalyst_collection() -> void:
	var envelope = SaveEnvelopeScript.new()
	var item = _item()
	item.enhancement_level = 9
	item.highest_checkpoint = 0
	envelope.items_by_uid[item.uid] = item
	var result = load(SERVICE_PATH).new().resolve_with_rolls(
		envelope, item.uid, 10, {"success_roll_percent": 0.0, "damage_roll_percent": 99.0}, 3, _precision_add_ember()
	)
	assert_eq(result["outcome"], "SUCCESS")
	assert_eq(item.enhancement_level, 10)
	assert_eq(item.catalyst_tag_entries()[0]["tag_id"], "TAG_EMBER_EDGE")
	assert_eq(item.used_precision_milestones, [10])
	assert_eq(item.raw_role_stat, 3)
	assert_eq(result.get("precision_action", ""), "ADD_TAG")
	assert_eq(result.get("precision_tag_id", ""), "TAG_EMBER_EDGE")
	assert_eq(item.ledger.size(), 1)
	assert_eq(item.ledger[0]["source_decision_id"], "BS-ENHANCE-20260901-40")


func test_level_nineteen_missing_precision_selection_blocks_before_cost_material_roll_or_save() -> void:
	var envelope = _valid_envelope_with_item()
	var item := _seeded_ember_item_at_nineteen(envelope)
	var resources = _resources()
	envelope.workshop_resources = resources.snapshot()
	var before_resources = resources.snapshot()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope,
		item.uid,
		20,
		{"success_roll_percent": 0.0, "damage_roll_percent": 0.0},
		3,
		resources,
		save_service
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "INVALID_PRECISION_ACTION")
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(save_service.save_calls, 0)
	assert_eq(item.enhancement_level, 19)
	assert_eq(item.catalyst_tag_entries().size(), 1)
	assert_eq(item.used_precision_milestones, [10])


func test_armor_precision_blocks_before_cost_material_roll_or_save() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	item.enhancement_level = 9
	item.highest_checkpoint = 0
	item.current_durability = 5
	item.max_durability = 5
	item.equipment_group = "ARMOR"
	item.role_profile = "ARMOR_BODY_DEFENSE"
	var resources = _resources()
	envelope.workshop_resources = resources.snapshot()
	var before_resources = resources.snapshot()
	var before_item = item.to_dict()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope, item.uid, 10,
		{"success_roll_percent": 0.0, "damage_roll_percent": 0.0}, 3,
		resources, save_service, _precision_add_ember()
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "PRECISION_TAG_WEAPON_ONLY")
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(save_service.save_calls, 0)
	assert_eq(item.to_dict(), before_item)


func test_precision_attempt_without_required_catalyst_blocks_before_cost_roll_or_save() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	item.enhancement_level = 9
	item.highest_checkpoint = 0
	item.current_durability = 5
	item.max_durability = 5
	var resources = _resources(20000, 10, 0, 1)
	envelope.workshop_resources = resources.snapshot()
	var before_resources = resources.snapshot()
	var before_item = item.to_dict()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope, item.uid, 10,
		{"success_roll_percent": 0.0, "damage_roll_percent": 0.0}, 3,
		resources, save_service, _precision_add_ember()
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "INSUFFICIENT_PRECISION_CATALYST")
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(save_service.save_calls, 0)
	assert_eq(item.to_dict(), before_item)


func test_precision_save_failure_restores_staged_catalyst_resource() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	item.enhancement_level = 9
	item.highest_checkpoint = 0
	item.current_durability = 5
	item.max_durability = 5
	var resources = _resources(20000, 10, 1, 10)
	envelope.workshop_resources = resources.snapshot()
	var before_resources = resources.snapshot()
	var before_item = item.to_dict()
	var save_service := FakeSaveService.new()
	save_service.save_error = ERR_CANT_CREATE
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope, item.uid, 10,
		{"success_roll_percent": 0.0, "damage_roll_percent": 99.0}, 3,
		resources, save_service, _precision_add_ember()
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "SAVE_FAILED:%d" % ERR_CANT_CREATE)
	assert_eq(resources.snapshot(), before_resources)
	assert_eq(item.to_dict(), before_item)
	assert_eq(save_service.save_calls, 1)


func test_plus_twenty_hold_and_damage_charge_normally_without_tag_growth() -> void:
	var held_envelope = _valid_envelope_with_item()
	var held_item := _seeded_ember_item_at_nineteen(held_envelope)
	var held_resources = _resources()
	held_envelope.workshop_resources = held_resources.snapshot()
	var held_before_resources := held_resources.snapshot()
	var held_save := FakeSaveService.new()
	var held = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		held_envelope, held_item.uid, 20,
		{"success_roll_percent": 99.0, "damage_roll_percent": 99.0}, 3,
		held_resources, held_save, _precision_upgrade_ember()
	)
	assert_eq(held.get("outcome", ""), "FAILED_HOLD")
	assert_eq(held_save.save_calls, 1)
	assert_lt(held_resources.gold, int(held_before_resources["gold"]))
	assert_eq(held_resources.get_material_count("heart_of_flame"), 9)
	var held_saved = held_save.saved_envelope.get_item(held_item.uid)
	assert_eq(held_saved.catalyst_tag_entries()[0]["stage"], 1)
	assert_eq(held_saved.used_precision_milestones, [10])
	assert_eq(held_saved.ledger.size(), 0)

	var damaged_envelope = _valid_envelope_with_item()
	var damaged_item := _seeded_ember_item_at_nineteen(damaged_envelope)
	var damaged_resources = _resources()
	damaged_envelope.workshop_resources = damaged_resources.snapshot()
	var damaged_save := FakeSaveService.new()
	var damaged = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		damaged_envelope, damaged_item.uid, 20,
		{"success_roll_percent": 99.0, "damage_roll_percent": 0.0}, 3,
		damaged_resources, damaged_save, _precision_upgrade_ember()
	)
	assert_eq(damaged.get("outcome", ""), "FAILED_DAMAGE")
	assert_eq(damaged_save.save_calls, 1)
	assert_eq(damaged_resources.get_material_count("heart_of_flame"), 9)
	var damaged_saved = damaged_save.saved_envelope.get_item(damaged_item.uid)
	assert_eq(damaged_saved.catalyst_tag_entries()[0]["stage"], 1)
	assert_eq(damaged_saved.used_precision_milestones, [10])
	assert_eq(damaged_saved.ledger.size(), 0)


func test_plus_twenty_upgrade_saves_one_deep_copied_growth_and_ledger_entry() -> void:
	var envelope = _valid_envelope_with_item()
	var item := _seeded_ember_item_at_nineteen(envelope)
	var resources = _resources()
	envelope.workshop_resources = resources.snapshot()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope, item.uid, 20,
		{"success_roll_percent": 0.0, "damage_roll_percent": 99.0}, 3,
		resources, save_service, _precision_upgrade_ember()
	)
	assert_eq(result.get("outcome", ""), "SUCCESS")
	assert_eq(result.get("precision_action", ""), "UPGRADE_TAG")
	assert_eq(result.get("precision_tag_id", ""), "TAG_EMBER_EDGE")
	assert_eq(result.get("precision_stage_before", -1), 1)
	assert_eq(result.get("precision_stage_after", -1), 2)
	assert_eq(result.get("precision_effect_axis", ""), "RAW_ROLE_STAT")
	assert_eq(result.get("precision_effect_delta", 0), 3)
	assert_eq(item.catalyst_tag_entries()[0]["stage"], 1, "source item must remain untouched until candidate adoption")
	var saved_item = save_service.saved_envelope.get_item(item.uid)
	assert_eq(saved_item.catalyst_tag_entries()[0]["stage"], 2)
	assert_eq(saved_item.used_precision_milestones, [10, 20])
	assert_eq(saved_item.raw_role_stat, 3)
	assert_eq(saved_item.ledger.size(), 1)
	var entry: Dictionary = saved_item.ledger[0]
	assert_eq(entry["event_type"], "PRECISION_TAG_GROWTH")
	assert_eq(entry["source_decision_id"], "BS-ENHANCE-20260901-40")
	assert_eq(entry["payload"], {
		"target_level": 20,
		"action": "UPGRADE_TAG",
		"tag_id": "TAG_EMBER_EDGE",
		"stage_before": 1,
		"stage_after": 2,
		"effect_axis": "RAW_ROLE_STAT",
		"effect_delta": 3,
	})
	var restored = SaveEnvelopeScript.from_dict(save_service.saved_envelope.to_dict())
	assert_true(restored.validation_errors.is_empty(), str(restored.validation_errors))
	assert_eq(restored.get_item(item.uid).ledger, saved_item.ledger)
	var repeat = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		save_service.saved_envelope, item.uid, 20,
		{"success_roll_percent": 0.0, "damage_roll_percent": 99.0}, 3,
		resources, save_service, _precision_upgrade_ember()
	)
	assert_eq(repeat.get("outcome", ""), "BLOCKED")
	assert_eq(save_service.save_calls, 1)
	assert_eq(save_service.saved_envelope.get_item(item.uid).ledger.size(), 1)


func test_plus_twenty_add_saves_one_tag_growth_and_method_effect() -> void:
	var envelope = _valid_envelope_with_item()
	var item := _seeded_ember_item_at_nineteen(envelope)
	item.weight_point = 6
	var resources = _resources()
	envelope.workshop_resources = resources.snapshot()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().resolve_and_save_with_rolls(
		envelope, item.uid, 20,
		{"success_roll_percent": 0.0, "damage_roll_percent": 99.0}, 3,
		resources, save_service, _precision_add_anvil_light()
	)
	assert_eq(result.get("outcome", ""), "SUCCESS")
	assert_eq(result.get("precision_action", ""), "ADD_TAG")
	assert_eq(result.get("precision_tag_id", ""), "TAG_ANVIL_LIGHT")
	assert_eq(result.get("precision_stage_before", -1), 0)
	assert_eq(result.get("precision_stage_after", -1), 1)
	var saved_item = save_service.saved_envelope.get_item(item.uid)
	assert_eq(saved_item.catalyst_tag_entries().size(), 2)
	assert_eq(saved_item.catalyst_tag_entries()[1]["tag_id"], "TAG_ANVIL_LIGHT")
	assert_eq(saved_item.used_precision_milestones, [10, 20])
	assert_eq(saved_item.weight_point, 3)
	assert_eq(saved_item.ledger.size(), 1)


func test_placeholder_backfill_is_zero_cost_one_time_and_saved_atomically() -> void:
	var envelope = _legacy_v3_envelope_with_affix("PRECISION_KEYWORD_PENDING_CONTENT")
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var resources = _resources()
	envelope.workshop_resources = resources.snapshot()
	var before_resources = resources.snapshot()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().backfill_precision_tag_and_save(
		envelope, item.uid, _precision_add_ember(), save_service
	)
	assert_eq(result.get("outcome", ""), "APPLIED")
	assert_eq(result.get("gold_cost", -1), 0)
	assert_eq(result.get("reinforcement_units", -1), 0)
	assert_eq(resources.snapshot(), before_resources)
	assert_true(item.has_initial_tag_backfill_pending(), "original envelope changes only after caller adopts saved envelope")
	assert_eq(save_service.save_calls, 1)
	var saved_item = save_service.saved_envelope.get_item(item.uid)
	assert_eq(saved_item.catalyst_tag_entries()[0]["tag_id"], "TAG_EMBER_EDGE")
	assert_false(saved_item.has_initial_tag_backfill_pending())
	assert_eq(saved_item.raw_role_stat, 0, "backfill must not replay a tag effect")
	assert_eq(saved_item.ledger.size(), 0, "free migration must not create a growth ledger entry")
	var repeat = load(SERVICE_PATH).new().backfill_precision_tag_and_save(
		save_service.saved_envelope, item.uid, _precision_add_ember(), save_service
	)
	assert_eq(repeat.get("outcome", ""), "BLOCKED")
	assert_eq(repeat.get("reason", ""), "PRECISION_INITIAL_TAG_BACKFILL_NOT_PENDING")
	assert_eq(save_service.save_calls, 1)


func test_unknown_nonempty_backfill_affix_fails_closed_before_save() -> void:
	var envelope = _legacy_v3_envelope_with_affix("UNKNOWN_NONEMPTY_AFFIX")
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var before_item = item.to_dict()
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().backfill_precision_tag_and_save(
		envelope, item.uid, _precision_add_ember(), save_service
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "CATALYST_AFFIX_UNKNOWN_FAIL_CLOSED")
	assert_eq(save_service.save_calls, 0)
	assert_eq(item.to_dict(), before_item)


func test_known_resolved_v4_backfill_fails_closed_before_save() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	var save_service := FakeSaveService.new()
	var result = load(SERVICE_PATH).new().backfill_precision_tag_and_save(
		envelope, item.uid, _precision_add_ember(), save_service
	)
	assert_eq(result.get("outcome", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "PRECISION_INITIAL_TAG_BACKFILL_NOT_PENDING")
	assert_eq(save_service.save_calls, 0)
	assert_true(item.catalyst_tag_entries().is_empty())


func test_saved_enhancement_success_commits_result_and_resource_cost_together() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var resources = _resources(20000, 30)
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
	assert_eq(result["outcome"], "SUCCESS")
	assert_not_null(save_service.saved_envelope)
	assert_eq(item.enhancement_level, 30, "original envelope must remain unchanged until the caller adopts the saved result")
	var saved_item = save_service.saved_envelope.get_item(item.uid)
	assert_eq(saved_item.enhancement_level, 31)
	assert_eq(saved_item.ledger.size(), 0, "ordinary enhancement success must not create a tag-growth ledger entry")
	assert_eq(resources.gold, 20000 - int(result["gold_cost"]))
	assert_eq(
		resources.get_material_count("common_reinforcement_material"),
		30 - int(result["reinforcement_units"])
	)
	assert_eq(save_service.saved_envelope.resource_snapshot(), resources.snapshot())


func test_saved_enhancement_save_failure_keeps_item_and_resources_unchanged() -> void:
	var envelope = _valid_envelope_with_item()
	var item = envelope.get_item("BSI-aabbccddeeff00112233445566778899")
	var resources = _resources(20000, 30)
	envelope.workshop_resources = resources.snapshot()
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
	var resources = _resources(20000, 0)
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


func _precision_add_ember() -> Dictionary:
	return {"action": "ADD_TAG", "catalyst_id": "HEART_OF_FLAME", "method_id": "EDGE_REINFORCEMENT"}


func _precision_add_anvil_light() -> Dictionary:
	return {"action": "ADD_TAG", "catalyst_id": "EARTH_CRYSTAL", "method_id": "LIGHTWEIGHTING"}


func _precision_upgrade_ember() -> Dictionary:
	return {"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"}
