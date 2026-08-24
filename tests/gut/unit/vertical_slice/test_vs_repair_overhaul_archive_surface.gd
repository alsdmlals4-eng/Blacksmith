extends "res://addons/gut/test.gd"

const REPAIR_PATH := "res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd"
const OVERHAUL_PATH := "res://scripts/vertical_slice/resolvers/vs_overhaul_resolver.gd"
const DESTROYED_RECORD_PATH := "res://scripts/vertical_slice/domain/vs_destroyed_history_record.gd"
const SCHEMA_PATH := "res://data/vertical_slice/vertical_slice_schema.json"
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")


func test_task3_runtime_surfaces_exist() -> void:
	assert_true(ResourceLoader.exists(REPAIR_PATH), "current repair resolver must exist")
	assert_true(ResourceLoader.exists(OVERHAUL_PATH), "current overhaul resolver must exist")
	assert_true(ResourceLoader.exists(DESTROYED_RECORD_PATH), "destroyed history record domain must exist")


func test_v2_save_envelope_exposes_destroyed_history_archive() -> void:
	var envelope = SaveEnvelopeScript.new()
	var serialized: Dictionary = envelope.to_dict()
	assert_true(
		serialized.has("destroyed_history_by_uid"),
		"V2 save must own the immutable destroyed-history archive"
	)


func test_machine_schema_describes_archive_without_breaking_existing_v2_reads() -> void:
	var file := FileAccess.open(SCHEMA_PATH, FileAccess.READ)
	assert_not_null(file, "vertical-slice schema must be readable")
	if file == null:
		return
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	assert_true(parsed is Dictionary, "vertical-slice schema must parse")
	if not parsed is Dictionary:
		return
	var save_contract: Dictionary = parsed.get("save_envelope", {})
	assert_eq(save_contract.get("destroyed_history_field", ""), "destroyed_history_by_uid")
	assert_eq(save_contract.get("destroyed_history_record_type", ""), "DESTROYED_HISTORY_V1")
	assert_eq(save_contract.get("destroyed_history_write_policy", ""), "REQUIRED_ON_NEW_V2_WRITES")
	assert_eq(save_contract.get("destroyed_history_read_compatibility", ""), "MISSING_FIELD_DEFAULTS_EMPTY_FOR_EXISTING_V2")
	assert_eq(save_contract.get("destroyed_history_overwrite_policy", ""), "IMMUTABLE_UID_INSERT_ONLY")
	assert_false(
		Array(save_contract.get("required_fields", [])).has("destroyed_history_by_uid"),
		"existing V2 saves without the new archive field must remain readable"
	)
