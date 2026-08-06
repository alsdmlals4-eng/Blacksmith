extends SceneTree

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const UidServiceScript = preload("res://scripts/vertical_slice/services/vs_uid_service.gd")
const SaveServiceScript = preload("res://scripts/vertical_slice/services/vs_save_service.gd")

const TEST_SAVE_PATH := "user://blacksmith_vertical_slice_task1_test.json"

var failures: Array[String] = []


func _initialize() -> void:
	_cleanup()
	_run_tests()
	_cleanup()
	if failures.is_empty():
		print("VSSaveService tests PASSED (5 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_uid_format_and_collision_avoidance()
	_test_save_load_preserves_resolved_state()
	_test_atomic_paths_are_clean_after_success()
	_test_corrupt_primary_recovers_backup()
	_test_missing_save_reports_validation_error()


func _make_item():
	var item = ItemScript.new()
	item.uid = "BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	item.birth_rng_seed = 818181
	item.primary_material_id = "meteor_iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.crafting_grade = "LEGENDARY"
	item.artistry = 11
	item.raw_role_stat = 17
	item.weight_point = 15
	item.function_capacity = 2
	item.functions.assign(["DISPLAY_ATTACK", "ELEMENTAL_WARD_FIRE"])
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
	envelope.preset_version = "VS-2026.08.06-A"
	envelope.run_id = "run-task1"
	envelope.run_rng_seed = 998877
	envelope.current_day = 4
	envelope.resolved_events = {
		"forge_birth": {"rng_seed": 818181, "grade": "LEGENDARY"},
		"arena_result": {"rng_seed": 414141, "result": "DAMAGED"},
	}
	_expect(envelope.add_item(_make_item()) == OK, "valid item should enter envelope")
	return envelope


func _test_uid_format_and_collision_avoidance() -> void:
	var service = UidServiceScript.new()
	var existing := {}
	for _index in range(32):
		var uid: String = service.create_uid(existing)
		_expect(uid.begins_with("BSI-"), "UID prefix missing")
		_expect(uid.length() == 36, "UID must be BSI- plus 32 hex")
		_expect(service.is_valid_uid(uid), "UID format rejected")
		_expect(not existing.has(uid), "UID collision returned")
		existing[uid] = true


func _test_save_load_preserves_resolved_state() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	var envelope = _make_envelope()
	_expect(service.save_envelope(envelope) == OK, "save should succeed")
	var restored = service.load_envelope()
	_expect(restored.validation_errors.is_empty(), "saved envelope should load without errors")
	_expect(restored.run_rng_seed == 998877, "run seed rerolled")
	_expect(restored.resolved_events == envelope.resolved_events, "resolved events changed")
	var item = restored.get_item("BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	_expect(item != null, "saved item missing")
	if item != null:
		_expect(item.birth_rng_seed == 818181, "birth seed rerolled")
		_expect(item.crafting_grade == "LEGENDARY", "crafting grade rerolled")
		_expect(item.enhancement_level == 10, "enhancement level changed")
		_expect(item.damage_state == "DAMAGED", "damage result changed")


func _test_atomic_paths_are_clean_after_success() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	_expect(service.save_envelope(_make_envelope()) == OK, "save should succeed")
	_expect(FileAccess.file_exists(TEST_SAVE_PATH), "primary save missing")
	_expect(not FileAccess.file_exists(service.temp_path), "temporary save must not remain")


func _test_corrupt_primary_recovers_backup() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	var first = _make_envelope()
	first.current_day = 3
	_expect(service.save_envelope(first) == OK, "first save should succeed")
	var second = _make_envelope()
	second.current_day = 5
	_expect(service.save_envelope(second) == OK, "second save should succeed")
	var file := FileAccess.open(TEST_SAVE_PATH, FileAccess.WRITE)
	_expect(file != null, "primary save should open for corruption test")
	if file != null:
		file.store_string("{broken-json")
		file.close()
	var restored = service.load_envelope()
	_expect(restored.recovered_from_backup, "backup recovery flag missing")
	_expect(restored.current_day == 3, "backup should preserve prior committed envelope")
	_expect(restored.run_rng_seed == 998877, "backup recovery rerolled seed")


func _test_missing_save_reports_validation_error() -> void:
	_cleanup()
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	var restored = service.load_envelope()
	_expect(restored.validation_errors.has("SAVE_NOT_FOUND"), "missing save must report SAVE_NOT_FOUND")


func _cleanup() -> void:
	for path in [TEST_SAVE_PATH, TEST_SAVE_PATH + ".tmp", TEST_SAVE_PATH + ".bak"]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
