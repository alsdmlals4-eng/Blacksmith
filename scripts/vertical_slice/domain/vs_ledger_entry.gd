class_name VSLedgerEntry
extends RefCounted

const SCHEMA_VERSION := 1

var schema_version: int = SCHEMA_VERSION
var sequence: int = 0
var event_id: String = ""
var event_type: String = ""
var source_decision_id: String = ""
var before_digest: String = ""
var after_digest: String = ""
var game_day: int = 0
var payload: Dictionary = {}
var validation_errors: Array[String] = []


static func create(
	entry_sequence: int,
	entry_event_id: String,
	entry_event_type: String,
	entry_source_decision_id: String,
	entry_before_digest: String,
	entry_after_digest: String,
	entry_game_day: int,
	entry_payload: Dictionary
) -> VSLedgerEntry:
	var entry := VSLedgerEntry.new()
	entry.sequence = entry_sequence
	entry.event_id = entry_event_id
	entry.event_type = entry_event_type
	entry.source_decision_id = entry_source_decision_id
	entry.before_digest = entry_before_digest
	entry.after_digest = entry_after_digest
	entry.game_day = entry_game_day
	entry.payload = entry_payload.duplicate(true)
	entry._validate()
	return entry


static func from_dict(value: Dictionary) -> VSLedgerEntry:
	var entry := VSLedgerEntry.new()
	entry.schema_version = int(value.get("schema_version", 0))
	entry.sequence = int(value.get("sequence", 0))
	entry.event_id = str(value.get("event_id", ""))
	entry.event_type = str(value.get("event_type", ""))
	entry.source_decision_id = str(value.get("source_decision_id", ""))
	entry.before_digest = str(value.get("before_digest", ""))
	entry.after_digest = str(value.get("after_digest", ""))
	entry.game_day = int(value.get("game_day", 0))
	var raw_payload: Variant = value.get("payload", {})
	if raw_payload is Dictionary:
		entry.payload = raw_payload.duplicate(true)
	else:
		entry.validation_errors.append("INVALID_LEDGER_PAYLOAD")
	entry._validate()
	return entry


func to_dict() -> Dictionary:
	return {
		"schema_version": schema_version,
		"sequence": sequence,
		"event_id": event_id,
		"event_type": event_type,
		"source_decision_id": source_decision_id,
		"before_digest": before_digest,
		"after_digest": after_digest,
		"game_day": game_day,
		"payload": payload.duplicate(true),
	}


func _validate() -> void:
	if schema_version != SCHEMA_VERSION:
		validation_errors.append("UNSUPPORTED_LEDGER_SCHEMA:%d" % schema_version)
	if sequence < 1:
		validation_errors.append("INVALID_LEDGER_SEQUENCE")
	if event_id.is_empty():
		validation_errors.append("MISSING_LEDGER_EVENT_ID")
	if event_type.is_empty():
		validation_errors.append("MISSING_LEDGER_EVENT_TYPE")
	if source_decision_id.is_empty():
		validation_errors.append("MISSING_LEDGER_SOURCE_DECISION")
	if game_day < 0:
		validation_errors.append("INVALID_LEDGER_GAME_DAY")
