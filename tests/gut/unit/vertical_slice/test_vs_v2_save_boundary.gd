extends "res://addons/gut/test.gd"

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const InitializerScript = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const SaveServiceScript = preload("res://scripts/vertical_slice/services/vs_save_service.gd")

const TEST_V2_PATH := "user://blacksmith_vertical_slice_v2_boundary_gut.json"
const TEST_V1_PATH := "user://blacksmith_vertical_slice_v1_boundary_gut.json"


func before_each() -> void:
	_cleanup()


func after_each() -> void:
	_cleanup()


func _legacy_v1_save() -> Dictionary:
	return {
		"schema_version": 1,
		"preset_version": "VS-2026.08.06-A",
		"saved_at_utc": "2026-08-24T00:00:00Z",
		"active_run": {
			"run_id": "RUN-11111111111111111111111111111111",
			"run_rng_seed": 123,
			"current_day": 1,
			"resolved_events": {},
		},
		"items_by_uid": {},
		"customer_state": {},
		"schedule_state": {},
		"global_ledger_sequence": 0,
	}


func test_new_save_envelope_uses_explicit_v2_schema_and_preset() -> void:
	var envelope = SaveEnvelopeScript.new()
	assert_eq(envelope.schema_version, 2, "current save schema must be V2")
	assert_eq(envelope.preset_version, "VS-2026.08.24-B", "current preset must be V2")


func test_initializer_creates_valid_v2_candidate() -> void:
	var initializer = InitializerScript.new()
	var envelope = initializer.create_candidate_envelope()
	assert_not_null(envelope)
	assert_true(envelope.validation_errors.is_empty(), "new V2 candidate must validate")
	assert_eq(envelope.schema_version, 2)
	assert_eq(envelope.preset_version, "VS-2026.08.24-B")


func test_legacy_v1_save_fails_closed_with_explicit_status() -> void:
	var envelope = SaveEnvelopeScript.from_dict(_legacy_v1_save())
	assert_true(
		envelope.validation_errors.has("LEGACY_PRE_RELEASE_SAVE"),
		"V1 pre-release saves must fail closed with an explicit legacy status"
	)


func test_save_service_default_paths_are_explicit_v2_and_legacy_v1() -> void:
	assert_eq(
		SaveServiceScript.DEFAULT_SAVE_PATH,
		"user://blacksmith_vertical_slice_v2.json",
		"current saves must not overwrite the pre-release V1 filename"
	)
	assert_eq(
		SaveServiceScript.LEGACY_V1_SAVE_PATH,
		"user://blacksmith_vertical_slice_v1.json",
		"legacy locator must remain explicit for fail-closed detection"
	)


func test_missing_v2_with_legacy_v1_file_reports_legacy_not_missing() -> void:
	var file := FileAccess.open(TEST_V1_PATH, FileAccess.WRITE)
	assert_not_null(file, "legacy fixture must open")
	if file != null:
		file.store_string(JSON.stringify(_legacy_v1_save(), "  "))
		file.close()

	var service = SaveServiceScript.new(TEST_V2_PATH, TEST_V1_PATH)
	var restored = service.load_envelope()
	assert_true(
		restored.validation_errors.has("LEGACY_PRE_RELEASE_SAVE"),
		"a legacy pre-release save must be surfaced explicitly instead of SAVE_NOT_FOUND"
	)
	assert_false(FileAccess.file_exists(TEST_V2_PATH), "legacy inspection must not silently migrate")
	assert_true(FileAccess.file_exists(TEST_V1_PATH), "legacy inspection must not silently delete")


func _cleanup() -> void:
	for path in [
		TEST_V2_PATH,
		TEST_V2_PATH + ".tmp",
		TEST_V2_PATH + ".bak",
		TEST_V1_PATH,
	]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
