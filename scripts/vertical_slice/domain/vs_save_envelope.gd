class_name VSSaveEnvelope
extends RefCounted

const SCHEMA_VERSION := 1
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const ContentResultRecordScript = preload(
	"res://scripts/vertical_slice/domain/vs_content_result_record.gd"
)
const REQUIRED_FIELDS := [
	"schema_version",
	"preset_version",
	"saved_at_utc",
	"active_run",
	"items_by_uid",
	"customer_state",
	"schedule_state",
	"global_ledger_sequence",
]
const ACTIVE_RUN_REQUIRED_FIELDS := [
	"run_id",
	"run_rng_seed",
	"current_day",
	"resolved_events",
]
const INTEGER_FIELDS := [
	"run_rng_seed",
	"current_day",
	"global_ledger_sequence",
	"rng_seed",
	"sequence",
	"occurred_at_game_day",
]

var schema_version: int = SCHEMA_VERSION
var preset_version: String = "VS-2026.08.06-A"
var saved_at_utc: String = ""
var active_run: Dictionary = {
	"run_id": "",
	"run_rng_seed": 0,
	"current_day": 1,
	"resolved_events": {},
}
var items_by_uid: Dictionary = {}
var customer_state: Dictionary = {}
var schedule_state: Dictionary = {}
var global_ledger_sequence: int = 0
var validation_errors: Array[String] = []
var recovered_from_backup: bool = false


static func from_dict(value: Dictionary) -> VSSaveEnvelope:
	var envelope := VSSaveEnvelope.new()
	for field_name in REQUIRED_FIELDS:
		if not value.has(field_name):
			envelope.validation_errors.append("MISSING_REQUIRED_FIELD:%s" % field_name)

	envelope.schema_version = int(value.get("schema_version", 0))
	envelope.preset_version = str(value.get("preset_version", ""))
	envelope.saved_at_utc = str(value.get("saved_at_utc", ""))
	envelope.global_ledger_sequence = int(value.get("global_ledger_sequence", -1))

	var raw_active_run: Variant = value.get("active_run", {})
	if raw_active_run is Dictionary:
		envelope.active_run = _normalize_dictionary(raw_active_run)
		for field_name in ACTIVE_RUN_REQUIRED_FIELDS:
			if not envelope.active_run.has(field_name):
				envelope.validation_errors.append("MISSING_ACTIVE_RUN_FIELD:%s" % field_name)
		_validate_typed_resolved_events(envelope)
	else:
		envelope.validation_errors.append("INVALID_FIELD_TYPE:active_run")

	var raw_customer_state: Variant = value.get("customer_state", {})
	if raw_customer_state is Dictionary:
		envelope.customer_state = _normalize_dictionary(raw_customer_state)
	else:
		envelope.validation_errors.append("INVALID_FIELD_TYPE:customer_state")

	var raw_schedule_state: Variant = value.get("schedule_state", {})
	if raw_schedule_state is Dictionary:
		envelope.schedule_state = _normalize_dictionary(raw_schedule_state)
	else:
		envelope.validation_errors.append("INVALID_FIELD_TYPE:schedule_state")

	var raw_items: Variant = value.get("items_by_uid", {})
	if raw_items is Dictionary:
		for item_id in raw_items:
			var raw_item: Variant = raw_items[item_id]
			if not raw_item is Dictionary:
				envelope.validation_errors.append("INVALID_ITEM_TYPE:%s" % str(item_id))
				continue
			var item = ItemScript.from_dict(raw_item)
			if item.uid != str(item_id):
				envelope.validation_errors.append("ITEM_KEY_UID_MISMATCH:%s" % str(item_id))
			for error_code in item.validation_errors:
				envelope.validation_errors.append("ITEM:%s:%s" % [str(item_id), error_code])
			envelope.items_by_uid[item.uid] = item
	else:
		envelope.validation_errors.append("INVALID_FIELD_TYPE:items_by_uid")

	envelope._validate_values()
	return envelope


static func _validate_typed_resolved_events(envelope: VSSaveEnvelope) -> void:
	var raw_resolved_events: Variant = envelope.active_run.get("resolved_events", {})
	if not raw_resolved_events is Dictionary:
		return

	for raw_event_key in raw_resolved_events.keys():
		var event_key := str(raw_event_key)
		var raw_event: Variant = raw_resolved_events[raw_event_key]
		if not raw_event is Dictionary:
			continue
		if str(raw_event.get("record_type", "")) != ContentResultRecordScript.RECORD_TYPE:
			continue

		var record = ContentResultRecordScript.from_dict(raw_event)
		if record.event_id != event_key:
			record.validation_errors.append("CONTENT_RESULT_EVENT_KEY_MISMATCH")
		for error_code in record.validation_errors:
			envelope.validation_errors.append(
				"CONTENT_RESULT:%s:%s" % [event_key, error_code]
			)
		if record.validation_errors.is_empty():
			envelope.active_run["resolved_events"][raw_event_key] = record.to_dict()


static func _normalize_dictionary(value: Dictionary) -> Dictionary:
	var normalized: Dictionary = {}
	for key in value:
		var child: Variant = value[key]
		if child is Dictionary:
			normalized[key] = _normalize_dictionary(child)
		elif child is Array:
			normalized[key] = _normalize_array(child)
		elif child is float and INTEGER_FIELDS.has(str(key)) and child == floor(child):
			normalized[key] = int(child)
		else:
			normalized[key] = child
	return normalized


static func _normalize_array(value: Array) -> Array:
	var normalized: Array = []
	for child in value:
		if child is Dictionary:
			normalized.append(_normalize_dictionary(child))
		elif child is Array:
			normalized.append(_normalize_array(child))
		else:
			normalized.append(child)
	return normalized


func to_dict() -> Dictionary:
	var serialized_items: Dictionary = {}
	for item_id in items_by_uid:
		var item: Variant = items_by_uid[item_id]
		if item != null and item.has_method("to_dict"):
			serialized_items[str(item_id)] = item.to_dict()
	return {
		"schema_version": schema_version,
		"preset_version": preset_version,
		"saved_at_utc": saved_at_utc,
		"active_run": active_run.duplicate(true),
		"items_by_uid": serialized_items,
		"customer_state": customer_state.duplicate(true),
		"schedule_state": schedule_state.duplicate(true),
		"global_ledger_sequence": global_ledger_sequence,
	}


func add_item(item) -> Error:
	if item == null:
		return ERR_INVALID_PARAMETER
	if not item.validation_errors.is_empty():
		return ERR_INVALID_DATA
	if item.uid.is_empty():
		return ERR_INVALID_DATA
	if items_by_uid.has(item.uid):
		return ERR_ALREADY_EXISTS
	items_by_uid[item.uid] = item
	return OK


func get_item(item_uid: String):
	return items_by_uid.get(item_uid)


func _validate_values() -> void:
	if schema_version != SCHEMA_VERSION:
		validation_errors.append("UNSUPPORTED_SAVE_SCHEMA:%d" % schema_version)
	if preset_version != "VS-2026.08.06-A":
		validation_errors.append("UNSUPPORTED_PRESET_VERSION:%s" % preset_version)
	if saved_at_utc.is_empty():
		validation_errors.append("MISSING_SAVED_AT_UTC")
	if str(active_run.get("run_id", "")).is_empty():
		validation_errors.append("MISSING_RUN_ID")
	if int(active_run.get("run_rng_seed", -1)) < 0:
		validation_errors.append("INVALID_RUN_RNG_SEED")
	if int(active_run.get("current_day", 0)) < 1:
		validation_errors.append("INVALID_CURRENT_DAY")
	if not active_run.get("resolved_events", {}) is Dictionary:
		validation_errors.append("INVALID_RESOLVED_EVENTS")
	if global_ledger_sequence < 0:
		validation_errors.append("INVALID_GLOBAL_LEDGER_SEQUENCE")
