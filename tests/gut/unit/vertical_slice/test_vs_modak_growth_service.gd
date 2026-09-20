extends GutTest

const Envelope = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const Save = preload("res://scripts/vertical_slice/services/vs_save_service.gd")
const Initializer = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const SERVICE_PATH = "res://scripts/vertical_slice/services/vs_modak_growth_service.gd"
var save
var service

func before_each():
	save = Save.new("user://modak-test-" + str(Time.get_ticks_usec()) + ".json")
	assert_eq(save.save_envelope(Initializer.new().create_replan_candidate_envelope()), OK)
	service = load(SERVICE_PATH).new() if ResourceLoader.exists(SERVICE_PATH) else null

func after_each():
	for path in [save.save_path, save.temp_path, save.backup_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func _available() -> bool:
	assert_not_null(service, "Modak join transaction must exist")
	return service != null

func test_legacy_read_does_not_join_or_write_and_join_survives_restart():
	if not _available(): return
	var source = save.load_envelope()
	var original = source.to_dict()
	assert_eq(service.view(source).stage, "NOT_JOINED")
	assert_eq(save.load_envelope().to_dict(), original)
	var result = service.join(source, save)
	assert_eq(result.status, "APPLIED")
	assert_eq(source.to_dict(), original, "source is immutable")
	assert_eq(Save.new(save.save_path).load_envelope().active_run.modak.joined_day, 1)
	assert_eq(result.envelope.resource_snapshot(), source.resource_snapshot())
	assert_eq(service.join(result.envelope, save).status, "ALREADY_APPLIED")
	assert_eq(save.load_envelope().active_run.modak.committed_stage, "EARLY")

func test_late_join_does_not_retroactively_grow_and_stale_source_is_rejected():
	if not _available(): return
	var old = save.load_envelope()
	var current = Envelope.from_dict(old.to_dict())
	current.active_run.current_day = 241
	assert_eq(save.save_envelope(current), OK)
	assert_eq(service.join(old, save).status, "BLOCKED")
	var result = service.join(save.load_envelope(), save)
	assert_eq(result.status, "APPLIED")
	assert_eq(result.envelope.active_run.modak.joined_day, 241)
	assert_eq(service.view(result.envelope).productive_days, 0)
	assert_eq(service.view(result.envelope).stage, "EARLY")
	assert_eq(service.join(Initializer.new().create_replan_candidate_envelope(), save).status, "BLOCKED")

func test_malformed_optional_bucket_is_not_silently_treated_as_not_joined():
	if not _available(): return
	var joined = service.join(save.load_envelope(), save).envelope.to_dict()
	for malformed in [null, {}, [], "EARLY"]:
		var raw = joined.duplicate(true)
		raw.active_run.modak = malformed
		assert_false(Envelope.from_dict(raw).validation_errors.is_empty())
	for day in [-1, 0, 1.5, 2, true]:
		var raw = joined.duplicate(true)
		raw.active_run.modak.joined_day = day
		assert_false(Envelope.from_dict(raw).validation_errors.is_empty())
	for field in ["policy_id", "committed_stage", "schema_version"]:
		var raw = joined.duplicate(true)
		raw.active_run.modak[field] = "UNKNOWN"
		assert_false(Envelope.from_dict(raw).validation_errors.is_empty())
	var extra = joined.duplicate(true)
	extra.active_run.modak.unknown = 1
	assert_false(Envelope.from_dict(extra).validation_errors.is_empty())

func test_productive_days_are_unique_and_growth_remains_locked():
	if not _available(): return
	var joined = service.join(save.load_envelope(), save).envelope
	assert_eq(service.record_productive_day(joined), "")
	assert_eq(service.record_productive_day(joined), "")
	assert_eq(joined.active_run.modak.productive_day_ids, [1])
	joined.active_run.current_day = 241
	assert_eq(service.view(joined).stage, "EARLY")
	assert_eq(service.view(joined).productive_days, 1)
	assert_eq(service.record_productive_day(joined), "")
	assert_eq(joined.active_run.modak.productive_day_ids, [1, 241])
	for days in [[1, 1], [241, 1], [0], [242], [1.5], [true]]:
		var raw = joined.to_dict()
		raw.active_run.modak.productive_day_ids = days
		assert_false(Envelope.from_dict(raw).validation_errors.is_empty())

class FailingSave extends RefCounted:
	var real
	var write_then_error = false
	func load_envelope(): return real.load_envelope()
	func save_envelope(value):
		if write_then_error: real.save_envelope(value)
		return ERR_CANT_CREATE

func test_failed_write_preserves_source_and_uncertain_commit_can_be_read_back():
	if not _available(): return
	var source = save.load_envelope()
	var broken = FailingSave.new()
	broken.real = save
	assert_eq(service.join(source, broken).reason, "SAVE_FAILED_UNCHANGED")
	assert_false(save.load_envelope().active_run.has("modak"))
	broken.write_then_error = true
	assert_eq(service.join(source, broken).status, "COMMIT_UNCERTAIN")
	assert_false(source.active_run.has("modak"))
	assert_eq(service.join(save.load_envelope(), save).status, "ALREADY_APPLIED")

func test_unjoined_handoff_record_is_noop():
	if not _available(): return
	var source = save.load_envelope()
	var before = source.to_dict()
	assert_eq(service.record_productive_day(source), "")
	assert_eq(source.to_dict(), before)
