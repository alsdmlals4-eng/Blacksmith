extends "res://addons/gut/test.gd"

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const UidServiceScript = preload("res://scripts/vertical_slice/services/vs_uid_service.gd")
const SaveServiceScript = preload("res://scripts/vertical_slice/services/vs_save_service.gd")

const TEST_SAVE_PATH := "user://blacksmith_vertical_slice_task1_gut.json"


func before_each() -> void:
	_cleanup()


func after_each() -> void:
	_cleanup()


func _make_item():
	var item = ItemScript.new()
	item.uid = "BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	item.birth_rng_seed = 818181
	item.primary_material_id = "meteor_iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.crafting_grade = "CRAFT_LEGENDARY"
	item.artistry = 8
	item.raw_role_stat = 20
	item.weight_point = 20
	item.function_capacity = 1
	item.functions.assign(["ELEMENTAL_WARD_FIRE"])
	item.grade_affix = "LEGENDARY_EDGE"
	item.catalyst_affix = "EMBER_TOUCHED"
	item.chronicle_affix = "ARENA_TESTED"
	item.enhancement_level = 10
	item.enhancement_failure_streak = 0
	item.used_precision_milestones.assign([10])
	item.damage_state = "DAMAGED"
	item.owner_id = "customer_gladiator"
	return item


func _make_envelope():
	var envelope = SaveEnvelopeScript.new()
	envelope.saved_at_utc = "2026-08-07T00:00:00Z"
	envelope.active_run = {
		"run_id": "run-task1",
		"run_rng_seed": 998877,
		"current_day": 4,
		"resolved_events": {
			"forge_birth": {"rng_seed": 818181, "grade": "CRAFT_LEGENDARY"},
			"arena_result": {"rng_seed": 414141, "result": "DAMAGED"},
		},
	}
	envelope.customer_state = {"gladiator": {"assigned_uid": "BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}
	envelope.schedule_state = {"arena": {"resolved": true}}
	envelope.global_ledger_sequence = 2
	assert_eq(envelope.add_item(_make_item()), OK, "valid item should enter envelope")
	return envelope


func test_uid_format_and_collision_avoidance() -> void:
	var service = UidServiceScript.new()
	var existing: Dictionary = {}
	for _index in range(32):
		var uid: String = service.create_uid(existing)
		assert_true(uid.begins_with("BSI-"), "UID prefix missing")
		assert_eq(uid.length(), 36, "UID must be BSI- plus 32 hex")
		assert_true(service.is_valid_uid(uid), "UID format rejected")
		assert_true(not existing.has(uid), "UID collision returned")
		existing[uid] = true


func test_save_load_preserves_resolved_state() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	var envelope = _make_envelope()
	assert_eq(service.save_envelope(envelope), OK, "save should succeed")
	var restored = service.load_envelope()
	assert_true(restored.validation_errors.is_empty(), "saved envelope should load without errors")
	assert_eq(restored.active_run["run_rng_seed"], 998877, "run seed rerolled")
	assert_eq(restored.active_run["resolved_events"], envelope.active_run["resolved_events"], "resolved events changed")
	assert_eq(restored.customer_state, envelope.customer_state, "customer state changed")
	assert_eq(restored.schedule_state, envelope.schedule_state, "schedule state changed")
	assert_eq(restored.global_ledger_sequence, 2, "global ledger sequence changed")
	var item = restored.get_item("BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	assert_true(item != null, "saved item missing")
	if item != null:
		assert_eq(item.birth_rng_seed, 818181, "birth seed rerolled")
		assert_eq(item.crafting_grade, "CRAFT_LEGENDARY", "crafting grade rerolled")
		assert_eq(item.enhancement_level, 10, "enhancement level changed")
		assert_eq(item.damage_state, "DAMAGED", "damage result changed")


func test_atomic_paths_are_clean_after_success() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	assert_eq(service.save_envelope(_make_envelope()), OK, "save should succeed")
	assert_true(FileAccess.file_exists(TEST_SAVE_PATH), "primary save missing")
	assert_true(not FileAccess.file_exists(service.temp_path), "temporary save must not remain")


func test_corrupt_primary_recovers_backup() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	var first = _make_envelope()
	first.active_run["current_day"] = 3
	assert_eq(service.save_envelope(first), OK, "first save should succeed")
	var second = _make_envelope()
	second.active_run["current_day"] = 5
	assert_eq(service.save_envelope(second), OK, "second save should succeed")
	var file := FileAccess.open(TEST_SAVE_PATH, FileAccess.WRITE)
	assert_true(file != null, "primary save should open for corruption test")
	if file != null:
		file.store_string("{broken-json")
		file.close()
	var restored = service.load_envelope()
	assert_true(restored.recovered_from_backup, "backup recovery flag missing")
	assert_eq(restored.active_run["current_day"], 3, "backup should preserve prior committed envelope")
	assert_eq(restored.active_run["run_rng_seed"], 998877, "backup recovery rerolled seed")


func test_missing_save_reports_validation_error() -> void:
	_cleanup()
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	var restored = service.load_envelope()
	assert_true(restored.validation_errors.has("SAVE_NOT_FOUND"), "missing save must report SAVE_NOT_FOUND")


func _cleanup() -> void:
	for path in [TEST_SAVE_PATH, TEST_SAVE_PATH + ".tmp", TEST_SAVE_PATH + ".bak"]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
