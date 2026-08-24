extends "res://addons/gut/test.gd"

const REPAIR_PATH := "res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd"
const OVERHAUL_PATH := "res://scripts/vertical_slice/resolvers/vs_overhaul_resolver.gd"
const DESTROYED_RECORD_PATH := "res://scripts/vertical_slice/domain/vs_destroyed_history_record.gd"
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
