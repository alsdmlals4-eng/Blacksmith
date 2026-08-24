extends "res://addons/gut/test.gd"

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const InitializerScript = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")


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
