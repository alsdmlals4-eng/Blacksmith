class_name VSSaveEnvelope
extends RefCounted

const SCHEMA_VERSION := 1
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const REQUIRED_FIELDS := [
	"schema_version",
	"preset_version",
	"run_id",
	"run_rng_seed",
	"current_day",
	"items",
	"resolved_events",
]

var schema_version: int = SCHEMA_VERSION
var preset_version: String = "VS-2026.08.06-A"
var run_id: String = ""
var run_rng_seed: int = 0
var current_day: int = 1
var items: Dictionary = {}
var resolved_events: Dictionary = {}
var validation_errors: Array[String] = []
var recovered_from_backup: bool = false


static func from_dict(value: Dictionary) -> VSSaveEnvelope:
	var envelope := VSSaveEnvelope.new()
	for field_name in REQUIRED_FIELDS:
		if not value.has(field_name):
			envelope.validation_errors.append("MISSING_REQUIRED_FIELD:%s" % field_name)

	envelope.schema_version = int(value.get("schema_version", 0))
	if envelope.schema_version != SCHEMA_VERSION:
		envelope.validation_errors.append("UNSUPPORTED_SAVE_SCHEMA:%d" % envelope.schema_version)
	envelope.preset_version = str(value.get("preset_version", ""))
	envelope.run_id = str(value.get("run_id", ""))
	envelope.run_rng_seed = int(value.get("run_rng_seed", 0))
	envelope.current_day = int(value.get("current_day", 0))

	var raw_events: Variant = value.get("resolved_events", {})
	if raw_events is Dictionary:
		envelope.resolved_events = raw_events.duplicate(true)
	else:
		envelope.validation_errors.append("INVALID_FIELD_TYPE:resolved_events")

	var raw_items: Variant = value.get("items", {})
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
			envelope.items[item.uid] = item
	else:
		envelope.validation_errors.append("INVALID_FIELD_TYPE:items")

	envelope._validate_values()
	return envelope


func to_dict() -> Dictionary:
	var serialized_items := {}
	for item_id in items:
		var item: Variant = items[item_id]
		if item != null and item.has_method("to_dict"):
			serialized_items[str(item_id)] = item.to_dict()
	return {
		"schema_version": schema_version,
		"preset_version": preset_version,
		"run_id": run_id,
		"run_rng_seed": run_rng_seed,
		"current_day": current_day,
		"items": serialized_items,
		"resolved_events": resolved_events.duplicate(true),
	}


func add_item(item) -> Error:
	if item == null:
		return ERR_INVALID_PARAMETER
	if not item.validation_errors.is_empty():
		return ERR_INVALID_DATA
	if item.uid.is_empty():
		return ERR_INVALID_DATA
	if items.has(item.uid):
		return ERR_ALREADY_EXISTS
	items[item.uid] = item
	return OK


func get_item(item_uid: String):
	return items.get(item_uid)


func _validate_values() -> void:
	if preset_version.is_empty():
		validation_errors.append("MISSING_PRESET_VERSION")
	if run_id.is_empty():
		validation_errors.append("MISSING_RUN_ID")
	if run_rng_seed < 0:
		validation_errors.append("INVALID_RUN_RNG_SEED")
	if current_day < 1:
		validation_errors.append("INVALID_CURRENT_DAY")
