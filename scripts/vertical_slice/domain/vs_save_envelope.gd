class_name VSSaveEnvelope
extends RefCounted

const SCHEMA_VERSION := 4
const PRESET_VERSION := "VS-2026.08.27-D"
const LEGACY_V3_SCHEMA_VERSION := 3
const LEGACY_V3_PRESET_VERSION := "VS-2026.08.26-C"
const LEGACY_V2_SCHEMA_VERSION := 2
const LEGACY_V2_PRESET_VERSION := "VS-2026.08.24-B"
const LEGACY_PRE_RELEASE_SCHEMA_VERSION := 1
const LEGACY_PRE_RELEASE_PRESET_VERSION := "VS-2026.08.06-A"
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const ContentResultRecordScript = preload(
	"res://scripts/vertical_slice/domain/vs_content_result_record.gd"
)
const DestroyedHistoryRecordScript = preload(
	"res://scripts/vertical_slice/domain/vs_destroyed_history_record.gd"
)
const REQUIRED_FIELDS := [
	"schema_version",
	"preset_version",
	"saved_at_utc",
	"active_run",
	"items_by_uid",
	"customer_state",
	"schedule_state",
	"workshop_resources",
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
	"destroyed_at_game_day",
	"before_current_durability",
	"before_max_durability",
	"gold",
]

var schema_version: int = SCHEMA_VERSION
var preset_version: String = PRESET_VERSION
var saved_at_utc: String = ""
var active_run: Dictionary = {
	"run_id": "",
	"run_rng_seed": 0,
	"current_day": 1,
	"resolved_events": {},
	"selected_item_uid": "",
}
var items_by_uid: Dictionary = {}
var customer_state: Dictionary = {}
var schedule_state: Dictionary = {}
var workshop_resources: Dictionary = starter_workshop_resources()
var destroyed_history_by_uid: Dictionary = {}
var global_ledger_sequence: int = 0
var validation_errors: Array[String] = []
var recovered_from_backup: bool = false


static func from_dict(value: Dictionary) -> VSSaveEnvelope:
	var envelope := VSSaveEnvelope.new()
	var source_schema_version := int(value.get("schema_version", 0))
	for field_name in REQUIRED_FIELDS:
		if field_name == "workshop_resources" and source_schema_version < SCHEMA_VERSION:
			continue
		if not value.has(field_name):
			envelope.validation_errors.append("MISSING_REQUIRED_FIELD:%s" % field_name)

	envelope.schema_version = int(value.get("schema_version", 0))
	envelope.preset_version = str(value.get("preset_version", ""))
	envelope.saved_at_utc = str(value.get("saved_at_utc", ""))
	envelope.global_ledger_sequence = int(value.get("global_ledger_sequence", -1))

	var raw_active_run: Variant = value.get("active_run", {})
	if raw_active_run is Dictionary:
		envelope.active_run = _normalize_dictionary(raw_active_run)
		if not envelope.active_run.has("selected_item_uid"):
			envelope.active_run["selected_item_uid"] = ""
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

	if source_schema_version >= SCHEMA_VERSION:
		var raw_workshop_resources: Variant = value.get("workshop_resources", {})
		if raw_workshop_resources is Dictionary:
			envelope.workshop_resources = _normalize_workshop_resources(raw_workshop_resources)
		else:
			envelope.validation_errors.append("INVALID_FIELD_TYPE:workshop_resources")
	else:
		envelope.workshop_resources = starter_workshop_resources()

	var raw_destroyed_history: Variant = value.get("destroyed_history_by_uid", {})
	if raw_destroyed_history is Dictionary:
		for raw_uid in raw_destroyed_history.keys():
			var history_uid := str(raw_uid)
			var raw_record: Variant = raw_destroyed_history[raw_uid]
			if not raw_record is Dictionary:
				envelope.validation_errors.append("INVALID_DESTROYED_HISTORY_TYPE:%s" % history_uid)
				continue
			var record = DestroyedHistoryRecordScript.from_dict(_normalize_dictionary(raw_record))
			if record.uid != history_uid:
				record.validation_errors.append("DESTROYED_HISTORY_KEY_UID_MISMATCH")
			for error_code in record.validation_errors:
				envelope.validation_errors.append(
					"DESTROYED_HISTORY:%s:%s" % [history_uid, error_code]
				)
			if record.validation_errors.is_empty():
				envelope.destroyed_history_by_uid[history_uid] = record.to_dict().duplicate(true)
	else:
		envelope.validation_errors.append("INVALID_FIELD_TYPE:destroyed_history_by_uid")

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

	if (
		envelope.schema_version == LEGACY_V2_SCHEMA_VERSION
		and envelope.preset_version == LEGACY_V2_PRESET_VERSION
	) or (
		envelope.schema_version == LEGACY_V3_SCHEMA_VERSION
		and envelope.preset_version == LEGACY_V3_PRESET_VERSION
	):
		envelope.schema_version = SCHEMA_VERSION
		envelope.preset_version = PRESET_VERSION
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


static func starter_workshop_resources() -> Dictionary:
	return {
		"gold": 20000,
		"material_stock": {
			"common_reinforcement_material": 10,
		},
	}


static func _normalize_workshop_resources(value: Dictionary) -> Dictionary:
	var normalized := _normalize_dictionary(value)
	var raw_stock: Variant = normalized.get("material_stock", {})
	if raw_stock is Dictionary:
		var normalized_stock: Dictionary = {}
		for raw_material_id in raw_stock:
			var quantity: Variant = raw_stock[raw_material_id]
			if quantity is float and quantity == floor(quantity):
				quantity = int(quantity)
			normalized_stock[str(raw_material_id)] = quantity
		normalized["material_stock"] = normalized_stock
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
		"workshop_resources": resource_snapshot(),
		"destroyed_history_by_uid": destroyed_history_by_uid.duplicate(true),
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


func resource_snapshot() -> Dictionary:
	return workshop_resources.duplicate(true)


func archive_destroyed_record(record) -> Error:
	if record == null:
		return ERR_INVALID_PARAMETER
	if not record.validation_errors.is_empty():
		return ERR_INVALID_DATA
	var history_uid := str(record.uid)
	if history_uid.is_empty():
		return ERR_INVALID_DATA
	if destroyed_history_by_uid.has(history_uid):
		return ERR_ALREADY_EXISTS
	destroyed_history_by_uid[history_uid] = record.to_dict().duplicate(true)
	return OK


func _validate_values() -> void:
	if (
		schema_version == LEGACY_PRE_RELEASE_SCHEMA_VERSION
		and preset_version == LEGACY_PRE_RELEASE_PRESET_VERSION
	):
		validation_errors.append("LEGACY_PRE_RELEASE_SAVE")
		return
	if schema_version != SCHEMA_VERSION:
		validation_errors.append("UNSUPPORTED_SAVE_SCHEMA:%d" % schema_version)
	if preset_version != PRESET_VERSION:
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
	var selected_item_uid := str(active_run.get("selected_item_uid", ""))
	if not selected_item_uid.is_empty() and not items_by_uid.has(selected_item_uid):
		validation_errors.append("SELECTED_ITEM_NOT_FOUND:%s" % selected_item_uid)
	if global_ledger_sequence < 0:
		validation_errors.append("INVALID_GLOBAL_LEDGER_SEQUENCE")
	if not workshop_resources.has("gold"):
		validation_errors.append("MISSING_WORKSHOP_RESOURCE_GOLD")
	elif not workshop_resources.get("gold") is int or int(workshop_resources.get("gold", -1)) < 0:
		validation_errors.append("INVALID_WORKSHOP_RESOURCE_GOLD")
	var material_stock: Variant = workshop_resources.get("material_stock", null)
	if not material_stock is Dictionary:
		validation_errors.append("INVALID_WORKSHOP_RESOURCE_STOCK")
		return
	for raw_material_id in material_stock:
		var material_id := str(raw_material_id)
		var quantity: Variant = material_stock[raw_material_id]
		if material_id.is_empty():
			validation_errors.append("INVALID_WORKSHOP_RESOURCE_ID")
		if not quantity is int or int(quantity) < 0:
			validation_errors.append("INVALID_WORKSHOP_RESOURCE_QUANTITY:%s" % material_id)
