extends "res://addons/gut/test.gd"

const CatalogScript = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
const BirthServiceScript = preload("res://scripts/vertical_slice/services/vs_item_birth_service.gd")
const CompletionServiceScript = preload("res://scripts/vertical_slice/services/vs_first_forge_completion_service.gd")
const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")
const InitializerScript = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")


class FakeSaveService:
	extends RefCounted
	var saved_envelope = null

	func save_envelope(envelope) -> Error:
		saved_envelope = envelope
		return OK


func test_birth_service_persists_every_catalog_identity_and_ledger_equipment_id() -> void:
	for entry in CatalogScript.all():
		var envelope = InitializerScript.new().create_candidate_envelope()
		var result: Dictionary = BirthServiceScript.new().commit_first_forge(envelope, _canonical_result(entry))
		assert_eq(result.get("status", ""), "APPLIED", str(entry.get("equipment_id", "")))
		if str(result.get("status", "")) != "APPLIED":
			continue
		var item = envelope.get_item(str(result.get("item_uid", "")))
		assert_eq(item.equipment_group, str(entry.get("equipment_group", "")))
		assert_eq(item.role_profile, str(entry.get("role_profile", "")))
		assert_eq(str(item.ledger[0].get("payload", {}).get("equipment_id", "")), str(entry.get("equipment_id", "")))


func test_completion_service_transfers_selected_armor_identity_through_save_candidate() -> void:
	var save_service := FakeSaveService.new()
	var result: Dictionary = CompletionServiceScript.new().complete_first_forge(
		InitializerScript.new().create_candidate_envelope(),
		{
			"weapon_id": "iron_sword",
			"equipment_id": "iron_armor",
			"equipment_name": "철갑옷",
			"base_attack": 22,
			"quality_id": "GOOD",
			"tap_count": 12,
			"fever_activation_count": 1,
			"fever_bonus_applied": true,
		},
		save_service
	)
	assert_eq(result.get("status", ""), "APPLIED")
	if str(result.get("status", "")) != "APPLIED":
		return
	assert_eq(result.get("item").equipment_group, "ARMOR")
	assert_eq(result.get("item").role_profile, "ARMOR_BODY_DEFENSE")


func test_forging_session_emits_the_selected_shield_identity() -> void:
	var session := ForgingSessionScript.new({
		"target_progress": 1.0,
		"tap_power": 1.0,
		"auto_work_per_second": 0.0,
		"equipment_id": "iron_shield",
	})
	session.set_precision_enabled(false)
	session.register_tap()
	assert_eq(session.result.get("equipment_id", ""), "iron_shield")
	assert_eq(session.result.get("equipment_group", ""), "SHIELD")
	assert_eq(session.result.get("role_profile", ""), "PHYSICAL_WEAPON_GUARD")


func _canonical_result(entry: Dictionary) -> Dictionary:
	return {
		"weapon_id": "iron_sword",
		"equipment_id": str(entry.get("equipment_id", "")),
		"equipment_name": str(entry.get("display_name_ko", "")),
		"base_attack": 21,
		"crafting_grade": "CRAFT_SUPERIOR",
		"artistry": 2,
		"tap_count": 14,
		"fever_activation_count": 1,
		"fever_bonus_applied": true,
	}
