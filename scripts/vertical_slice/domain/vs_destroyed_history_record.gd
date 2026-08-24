class_name VSDestroyedHistoryRecord
extends RefCounted

const SCHEMA_VERSION := 1
const RECORD_TYPE := "DESTROYED_HISTORY_V1"

var schema_version: int = SCHEMA_VERSION
var record_type: String = RECORD_TYPE
var uid: String = ""
var destroyed_at_game_day: int = 0
var direct_cause: String = ""
var before_current_durability: int = -1
var before_max_durability: int = -1
var zero_axis: String = ""
var item_snapshot: Dictionary = {}
var validation_errors: Array[String] = []


static func from_item(
	item,
	destroyed_at_day: int,
	cause: String,
	before_current: int,
	before_max: int
) -> VSDestroyedHistoryRecord:
	var record := VSDestroyedHistoryRecord.new()
	if item == null:
		record.validation_errors.append("MISSING_ITEM")
		return record

	record.uid = str(item.uid)
	record.destroyed_at_game_day = destroyed_at_day
	record.direct_cause = cause
	record.before_current_durability = before_current
	record.before_max_durability = before_max
	record.item_snapshot = item.to_dict().duplicate(true)
	record.zero_axis = _zero_axis_from_snapshot(record.item_snapshot)
	record._validate_values()
	return record


static func from_dict(value: Dictionary) -> VSDestroyedHistoryRecord:
	var record := VSDestroyedHistoryRecord.new()
	record.schema_version = int(value.get("schema_version", 0))
	record.record_type = str(value.get("record_type", ""))
	record.uid = str(value.get("uid", ""))
	record.destroyed_at_game_day = int(value.get("destroyed_at_game_day", 0))
	record.direct_cause = str(value.get("direct_cause", ""))
	record.before_current_durability = int(value.get("before_current_durability", -1))
	record.before_max_durability = int(value.get("before_max_durability", -1))
	record.zero_axis = str(value.get("zero_axis", ""))
	var raw_snapshot: Variant = value.get("item_snapshot", {})
	if raw_snapshot is Dictionary:
		record.item_snapshot = raw_snapshot.duplicate(true)
	else:
		record.validation_errors.append("INVALID_ITEM_SNAPSHOT")
	record._validate_values()
	return record


func to_dict() -> Dictionary:
	return {
		"schema_version": schema_version,
		"record_type": record_type,
		"uid": uid,
		"destroyed_at_game_day": destroyed_at_game_day,
		"direct_cause": direct_cause,
		"before_current_durability": before_current_durability,
		"before_max_durability": before_max_durability,
		"zero_axis": zero_axis,
		"item_snapshot": item_snapshot.duplicate(true),
	}


static func _zero_axis_from_snapshot(snapshot: Dictionary) -> String:
	var current := int(snapshot.get("current_durability", -1))
	var maximum := int(snapshot.get("max_durability", -1))
	if current == 0 and maximum == 0:
		return "BOTH"
	if current == 0:
		return "CURRENT"
	if maximum == 0:
		return "MAX"
	return ""


func _validate_values() -> void:
	if schema_version != SCHEMA_VERSION:
		validation_errors.append("UNSUPPORTED_DESTROYED_HISTORY_SCHEMA")
	if record_type != RECORD_TYPE:
		validation_errors.append("INVALID_RECORD_TYPE")
	var uid_regex := RegEx.new()
	uid_regex.compile("^BSI-[0-9a-f]{32}$")
	if uid_regex.search(uid) == null:
		validation_errors.append("INVALID_UID_FORMAT")
	if destroyed_at_game_day < 1:
		validation_errors.append("INVALID_DESTROYED_GAME_DAY")
	if direct_cause.is_empty():
		validation_errors.append("MISSING_DIRECT_CAUSE")
	if before_current_durability < 0 or before_current_durability > 100:
		validation_errors.append("INVALID_BEFORE_CURRENT")
	if before_max_durability < 0 or before_max_durability > 100:
		validation_errors.append("INVALID_BEFORE_MAX")
	if not ["CURRENT", "MAX", "BOTH"].has(zero_axis):
		validation_errors.append("INVALID_ZERO_AXIS")
	if str(item_snapshot.get("uid", "")) != uid:
		validation_errors.append("SNAPSHOT_UID_MISMATCH")
	if str(item_snapshot.get("physical_state", "")) != "DESTROYED":
		validation_errors.append("SNAPSHOT_NOT_DESTROYED")
	if _zero_axis_from_snapshot(item_snapshot) != zero_axis:
		validation_errors.append("SNAPSHOT_ZERO_AXIS_MISMATCH")
