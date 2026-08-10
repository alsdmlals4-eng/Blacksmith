extends "res://addons/gut/test.gd"

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const SaveServiceScript = preload("res://scripts/vertical_slice/services/vs_save_service.gd")

const TEST_SAVE_PATH := "user://blacksmith_vertical_slice_task2_replace_gut.json"


func before_each() -> void:
	_cleanup()


func after_each() -> void:
	_cleanup()


func _make_valid_envelope(run_id: String, day: int):
	var envelope = SaveEnvelopeScript.new()
	envelope.saved_at_utc = "2026-08-08T10:00:00Z"
	envelope.active_run = {
		"run_id": run_id,
		"run_rng_seed": 123456789,
		"current_day": day,
		"resolved_events": {},
	}
	envelope.customer_state = {}
	envelope.schedule_state = {}
	envelope.global_ledger_sequence = 0
	return envelope


func _read_text(path: String) -> String:
	var file := FileAccess.open(path, FileAccess.READ)
	assert_true(file != null, "expected file to be readable: %s" % path)
	if file == null:
		return ""
	var text := file.get_as_text()
	file.close()
	return text


func test_safe_replacement_surface_exists() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	assert_true(
		service.has_method("replace_envelope_after_confirmation"),
		"VSSaveService must own confirmed destructive replacement",
	)


func test_invalid_candidate_does_not_mutate_existing_primary() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	assert_eq(service.save_envelope(_make_valid_envelope("RUN-11111111111111111111111111111111", 3)), OK)
	var before := _read_text(TEST_SAVE_PATH)
	if not service.has_method("replace_envelope_after_confirmation"):
		fail_test("replace_envelope_after_confirmation is missing")
		return

	var invalid_candidate = SaveEnvelopeScript.new()
	var result = service.replace_envelope_after_confirmation(invalid_candidate)
	assert_eq(result, ERR_INVALID_DATA, "invalid new campaign must be rejected before mutation")
	assert_eq(_read_text(TEST_SAVE_PATH), before, "invalid candidate must not mutate existing primary")


func test_corrupt_primary_replacement_preserves_known_valid_backup_bytes() -> void:
	var service = SaveServiceScript.new(TEST_SAVE_PATH)
	var backup_envelope = _make_valid_envelope("RUN-22222222222222222222222222222222", 3)
	var primary_envelope = _make_valid_envelope("RUN-33333333333333333333333333333333", 5)
	assert_eq(service.save_envelope(backup_envelope), OK)
	assert_eq(service.save_envelope(primary_envelope), OK)
	assert_true(FileAccess.file_exists(service.backup_path), "second committed save must create backup")
	var backup_before := _read_text(service.backup_path)

	var primary_file := FileAccess.open(TEST_SAVE_PATH, FileAccess.WRITE)
	assert_true(primary_file != null, "primary must open for corruption fixture")
	if primary_file != null:
		primary_file.store_string("{broken-primary")
		primary_file.close()

	var recovered = service.load_envelope()
	assert_true(recovered.recovered_from_backup, "fixture must prove valid backup recovery before replacement")
	assert_eq(int(recovered.active_run.get("current_day", 0)), 3, "fixture backup must be the known-valid committed run")

	if not service.has_method("replace_envelope_after_confirmation"):
		fail_test("replace_envelope_after_confirmation is missing")
		return
	var candidate = _make_valid_envelope("RUN-44444444444444444444444444444444", 1)
	assert_eq(service.replace_envelope_after_confirmation(candidate), OK, "confirmed replacement should commit candidate")
	assert_eq(_read_text(service.backup_path), backup_before, "known-valid backup bytes must remain unchanged")
	var restored = service.load_envelope()
	assert_true(restored.validation_errors.is_empty(), "new primary must be valid")
	assert_true(not restored.recovered_from_backup, "new primary should load directly")
	assert_eq(str(restored.active_run.get("run_id", "")), "RUN-44444444444444444444444444444444")


func _cleanup() -> void:
	for path in [TEST_SAVE_PATH, TEST_SAVE_PATH + ".tmp", TEST_SAVE_PATH + ".bak"]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
