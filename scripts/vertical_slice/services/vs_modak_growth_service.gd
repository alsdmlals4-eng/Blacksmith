extends RefCounted

const RULESET = "BLACKSMITH_REPLAN_TAGS_20260912"
const POLICY = "GROWTH_LOCKED_V1"
const KEYS = ["schema_version", "policy_id", "joined_day", "productive_day_ids", "committed_stage"]
const MAX_SAFE_INTEGER = 9007199254740991

static func _whole(value) -> bool:
	return typeof(value) in [TYPE_INT, TYPE_FLOAT] and is_finite(float(value)) and abs(float(value)) <= MAX_SAFE_INTEGER and float(value) == floor(float(value))

static func validate(envelope) -> String:
	if envelope == null: return "INVALID_MODAK_ENVELOPE"
	var run = envelope.active_run
	if not run.has("modak"): return ""
	if run.get("tag_ruleset_id", "") != RULESET or not _whole(run.get("current_day")) or run.current_day < 1:
		return "INVALID_MODAK_CAMPAIGN"
	var bucket = run.modak
	if not bucket is Dictionary or bucket.size() != KEYS.size() or not bucket.has_all(KEYS):
		return "INVALID_MODAK_BUCKET"
	if not _whole(bucket.schema_version) or bucket.schema_version != 1 or bucket.policy_id != POLICY or bucket.committed_stage != "EARLY":
		return "INVALID_MODAK_POLICY"
	if not _whole(bucket.joined_day) or bucket.joined_day < 1 or bucket.joined_day > run.current_day:
		return "INVALID_MODAK_JOINED_DAY"
	if not bucket.productive_day_ids is Array: return "INVALID_MODAK_PRODUCTIVE_DAYS"
	var previous = int(bucket.joined_day) - 1
	for day in bucket.productive_day_ids:
		if not _whole(day) or day < bucket.joined_day or day > run.current_day or day <= previous:
			return "INVALID_MODAK_PRODUCTIVE_DAYS"
		previous = int(day)
	return ""

func view(envelope) -> Dictionary:
	if not validate(envelope).is_empty(): return {"stage":"UNAVAILABLE", "productive_days":0}
	if not envelope.active_run.has("modak"): return {"stage":"NOT_JOINED", "productive_days":0}
	var bucket = envelope.active_run.modak
	return {"stage":bucket.committed_stage, "productive_days":bucket.productive_day_ids.size(), "joined_day":int(bucket.joined_day)}

# Candidate-only mutation: the commissioning transaction owns the one disk commit.
func record_productive_day(candidate) -> String:
	var error = validate(candidate)
	if not error.is_empty(): return error
	if not candidate.active_run.has("modak"): return ""
	var day = int(candidate.active_run.current_day)
	if day not in candidate.active_run.modak.productive_day_ids:
		candidate.active_run.modak.productive_day_ids.append(day)
	return ""

func join(envelope, save) -> Dictionary:
	if envelope == null or save == null or not save.has_method("load_envelope") or not save.has_method("save_envelope"):
		return _blocked("INVALID_CONTEXT")
	if envelope.recovered_from_backup or not envelope.validation_errors.is_empty(): return _blocked("INVALID_SOURCE")
	var parser = load("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
	var source = parser.from_dict(envelope.to_dict())
	if not source.validation_errors.is_empty(): return _blocked("INVALID_SOURCE")
	var current = save.load_envelope()
	if current == null or current.recovered_from_backup or not current.validation_errors.is_empty(): return _blocked("SAVE_UNAVAILABLE")
	current = parser.from_dict(current.to_dict())
	if not current.validation_errors.is_empty() or current.active_run.get("tag_ruleset_id", "") != RULESET:
		return _blocked("INVALID_CAMPAIGN")
	if not _same(source, current): return _blocked("STALE_SOURCE")
	if current.active_run.has("modak"): return {"status":"ALREADY_APPLIED", "envelope":current}
	current.active_run.modak = {"schema_version":1, "policy_id":POLICY, "joined_day":int(current.active_run.current_day), "productive_day_ids":[], "committed_stage":"EARLY"}
	var candidate = parser.from_dict(current.to_dict())
	if not candidate.validation_errors.is_empty(): return _blocked("INVALID_CANDIDATE")
	if save.save_envelope(candidate) != OK:
		var after_error = save.load_envelope()
		if after_error != null and not after_error.recovered_from_backup and after_error.validation_errors.is_empty() and _same(source, after_error):
			return _blocked("SAVE_FAILED_UNCHANGED")
		return {"status":"COMMIT_UNCERTAIN", "reason":"SAVE_ERROR_STATE_UNKNOWN"}
	var actual = save.load_envelope()
	if actual == null or actual.recovered_from_backup or not actual.validation_errors.is_empty():
		return {"status":"COMMIT_UNCERTAIN", "reason":"READBACK_UNAVAILABLE"}
	actual = parser.from_dict(actual.to_dict())
	if not actual.validation_errors.is_empty() or not _same(candidate, actual):
		return {"status":"COMMIT_UNCERTAIN", "reason":"READBACK_MISMATCH"}
	return {"status":"APPLIED", "envelope":actual}

func _same(a, b) -> bool:
	return load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").serialized_equal(a.to_dict(), b.to_dict())

func _blocked(reason: String) -> Dictionary:
	return {"status":"BLOCKED", "reason":reason}
