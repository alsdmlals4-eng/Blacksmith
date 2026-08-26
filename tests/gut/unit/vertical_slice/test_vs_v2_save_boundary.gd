extends "res://addons/gut/test.gd"

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const InitializerScript = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const SaveServiceScript = preload("res://scripts/vertical_slice/services/vs_save_service.gd")


func _v2_save() -> Dictionary:
	return {
		"schema_version": 2,
		"preset_version": "VS-2026.08.24-B",
		"saved_at_utc": "2026-08-24T00:00:00Z",
		"active_run": {"run_id": "RUN-11111111111111111111111111111111", "run_rng_seed": 123, "current_day": 1, "resolved_events": {}},
		"items_by_uid": {},
		"customer_state": {},
		"schedule_state": {},
		"global_ledger_sequence": 0,
	}


func _legacy_v1_save() -> Dictionary:
	var legacy := _v2_save()
	legacy["schema_version"] = 1
	legacy["preset_version"] = "VS-2026.08.06-A"
	return legacy


func test_new_save_envelope_uses_explicit_v4_schema_preset_and_temp_starter_resources() -> void:
	var envelope = SaveEnvelopeScript.new()
	assert_eq(envelope.schema_version, 4)
	assert_eq(envelope.preset_version, "VS-2026.08.27-D")
	assert_eq(envelope.workshop_resources.get("gold", -1), 20000)
	assert_eq(
		(envelope.workshop_resources.get("material_stock", {}) as Dictionary).get(
			"common_reinforcement_material", -1
		),
		10
	)


func test_initializer_creates_valid_v4_candidate_with_temp_starter_resources() -> void:
	var envelope = InitializerScript.new().create_candidate_envelope()
	assert_not_null(envelope)
	assert_true(envelope.validation_errors.is_empty())
	assert_eq(envelope.schema_version, 4)
	assert_eq(envelope.preset_version, "VS-2026.08.27-D")
	assert_eq(envelope.workshop_resources.get("gold", -1), 20000)


func test_v2_save_migrates_in_memory_to_v4_with_temp_starter_resources_without_validation_error() -> void:
	var restored = SaveEnvelopeScript.from_dict(_v2_save())
	assert_true(restored.validation_errors.is_empty())
	assert_eq(restored.schema_version, 4)
	assert_eq(restored.preset_version, "VS-2026.08.27-D")
	assert_eq(restored.workshop_resources.get("gold", -1), 20000)


func test_v3_save_migrates_in_memory_to_v4_with_temp_starter_resources_without_validation_error() -> void:
	var legacy_v3 := _v2_save()
	legacy_v3["schema_version"] = 3
	legacy_v3["preset_version"] = "VS-2026.08.26-C"
	var restored = SaveEnvelopeScript.from_dict(legacy_v3)
	assert_true(restored.validation_errors.is_empty())
	assert_eq(restored.schema_version, 4)
	assert_eq(restored.preset_version, "VS-2026.08.27-D")
	assert_eq(restored.workshop_resources.get("gold", -1), 20000)


func test_v4_save_without_workshop_resources_fails_closed() -> void:
	var malformed: Dictionary = InitializerScript.new().create_candidate_envelope().to_dict()
	malformed.erase("workshop_resources")
	var restored = SaveEnvelopeScript.from_dict(malformed)
	assert_true(restored.validation_errors.has("MISSING_REQUIRED_FIELD:workshop_resources"))


func test_legacy_v1_save_fails_closed_with_explicit_status() -> void:
	var envelope = SaveEnvelopeScript.from_dict(_legacy_v1_save())
	assert_true(envelope.validation_errors.has("LEGACY_PRE_RELEASE_SAVE"))


func test_save_service_default_paths_are_explicit_v4_and_v3_v2_legacy() -> void:
	assert_eq(SaveServiceScript.DEFAULT_SAVE_PATH, "user://blacksmith_vertical_slice_v4.json")
	assert_eq(SaveServiceScript.LEGACY_V3_SAVE_PATH, "user://blacksmith_vertical_slice_v3.json")
	assert_eq(SaveServiceScript.LEGACY_V2_SAVE_PATH, "user://blacksmith_vertical_slice_v2.json")
