extends "res://addons/gut/test.gd"

const SERVICE_PATH := "res://scripts/vertical_slice/services/vs_first_forge_completion_service.gd"
const INITIALIZER_PATH := "res://scripts/vertical_slice/services/vs_run_initializer_service.gd"


class FakeSaveService:
	extends RefCounted
	var save_error: Error = OK
	var saved_envelope = null

	func save_envelope(envelope) -> Error:
		saved_envelope = envelope
		return save_error


func _new_envelope():
	return load(INITIALIZER_PATH).new().create_candidate_envelope()


func _completed_result() -> Dictionary:
	return {
		"weapon_id": "iron_sword",
		"base_attack": 22,
		"quality_id": "GOOD",
		"tap_count": 12,
		"fever_activation_count": 1,
		"fever_bonus_applied": true,
	}


func test_completed_first_forge_persists_candidate_without_mutating_original_envelope() -> void:
	assert_true(ResourceLoader.exists(SERVICE_PATH), "first forge completion service must exist")
	if not ResourceLoader.exists(SERVICE_PATH):
		return
	var original = _new_envelope()
	var save_service := FakeSaveService.new()
	var result: Dictionary = load(SERVICE_PATH).new().complete_first_forge(
		original,
		_completed_result(),
		save_service
	)

	assert_eq(result.get("status", ""), "APPLIED")
	assert_true(original.items_by_uid.is_empty(), "save candidate must isolate the original until persistence succeeds")
	var saved = result.get("envelope", null)
	assert_true(saved != null, "successful completion must return its persisted candidate")
	assert_eq(save_service.saved_envelope, saved)
	assert_eq(str(saved.active_run.get("selected_item_uid", "")), str(result.get("item_uid", "")))
	assert_eq(saved.get_item(str(result.get("item_uid", ""))).crafting_grade, "CRAFT_SUPERIOR")


func test_save_failure_blocks_first_forge_without_mutating_original_envelope() -> void:
	if not ResourceLoader.exists(SERVICE_PATH):
		assert_true(false, "first forge completion service must exist")
		return
	var original = _new_envelope()
	var save_service := FakeSaveService.new()
	save_service.save_error = ERR_CANT_CREATE
	var result: Dictionary = load(SERVICE_PATH).new().complete_first_forge(
		original,
		_completed_result(),
		save_service
	)

	assert_eq(result.get("status", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "SAVE_COMMIT_FAILED")
	assert_true(original.items_by_uid.is_empty())
	assert_eq(str(original.active_run.get("selected_item_uid", "")), "")
