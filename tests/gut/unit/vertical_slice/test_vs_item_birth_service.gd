extends "res://addons/gut/test.gd"

const SERVICE_PATH := "res://scripts/vertical_slice/services/vs_item_birth_service.gd"
const INITIALIZER_PATH := "res://scripts/vertical_slice/services/vs_run_initializer_service.gd"
const ItemScript := preload("res://scripts/vertical_slice/domain/vs_item.gd")


func _forge_result(crafting_grade: String = "CRAFT_SUPERIOR") -> Dictionary:
	return {
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"base_attack": 21,
		"crafting_grade": crafting_grade,
		"artistry": 2,
		"tap_count": 14,
		"fever_activation_count": 1,
		"fever_bonus_applied": true,
	}


func _new_envelope():
	return load(INITIALIZER_PATH).new().create_candidate_envelope()


func test_completed_first_forge_creates_selected_canonical_item() -> void:
	assert_true(
		ResourceLoader.exists(SERVICE_PATH),
		"completed forging needs the canonical item-birth service"
	)
	if not ResourceLoader.exists(SERVICE_PATH):
		return

	var service = load(SERVICE_PATH).new()
	var envelope = _new_envelope()
	var result: Dictionary = service.commit_first_forge(envelope, _forge_result())

	assert_eq(result.get("status", ""), "APPLIED")
	var item_uid := str(result.get("item_uid", ""))
	assert_true(item_uid.begins_with("BSI-"), "born item needs a canonical UID")
	assert_eq(str(envelope.active_run.get("selected_item_uid", "")), item_uid)
	assert_true(envelope.items_by_uid.has(item_uid), "born item must enter the save envelope")
	var item = envelope.get_item(item_uid)
	assert_eq(item.crafting_grade, "CRAFT_SUPERIOR")
	assert_eq(item.raw_role_stat, 21)
	assert_eq(item.current_durability, 5)
	assert_eq(item.max_durability, 5)
	assert_eq(item.ledger.size(), 1, "creation must be a player Chronicle event")
	assert_eq(item.ledger[0].get("event_type", ""), "ITEM_BORN")


func test_completed_first_forge_initializes_empty_v4_precision_tag_record() -> void:
	var service = load(SERVICE_PATH).new()
	var envelope = _new_envelope()
	var result: Dictionary = service.commit_first_forge(envelope, _forge_result())

	assert_eq(result.get("status", ""), "APPLIED")
	var item = envelope.get_item(str(result.get("item_uid", "")))
	assert_eq(item.catalyst_affix, ItemScript.empty_catalyst_affix())
	assert_true(item.catalyst_tag_entries().is_empty())
	assert_true(item.used_precision_milestones.is_empty())
	var restored = envelope.get_script().from_dict(envelope.to_dict())
	assert_true(restored.validation_errors.is_empty())


func test_second_first_forge_is_rejected_without_mutating_selected_item() -> void:
	if not ResourceLoader.exists(SERVICE_PATH):
		assert_true(false, "item-birth service must exist")
		return

	var service = load(SERVICE_PATH).new()
	var envelope = _new_envelope()
	var first: Dictionary = service.commit_first_forge(envelope, _forge_result("CRAFT_FINE"))
	var selected_uid := str(first.get("item_uid", ""))
	var second: Dictionary = service.commit_first_forge(envelope, _forge_result("CRAFT_NORMAL"))

	assert_eq(second.get("status", ""), "BLOCKED")
	assert_eq(second.get("reason", ""), "FIRST_ITEM_ALREADY_CREATED")
	assert_eq(str(envelope.active_run.get("selected_item_uid", "")), selected_uid)
	assert_eq(envelope.items_by_uid.size(), 1)


func test_selected_item_uid_survives_save_envelope_round_trip() -> void:
	if not ResourceLoader.exists(SERVICE_PATH):
		assert_true(false, "item-birth service must exist")
		return

	var service = load(SERVICE_PATH).new()
	var envelope = _new_envelope()
	var birth: Dictionary = service.commit_first_forge(envelope, _forge_result())
	var restored = envelope.get_script().from_dict(envelope.to_dict())

	assert_true(restored.validation_errors.is_empty())
	assert_eq(
		str(restored.active_run.get("selected_item_uid", "")),
		str(birth.get("item_uid", ""))
	)
