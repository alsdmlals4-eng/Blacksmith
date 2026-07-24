class_name PocTelemetry
extends RefCounted

var events: Array[Dictionary] = []
var sequence: int = 0


func record(event_name: String, payload: Dictionary = {}) -> Dictionary:
	sequence += 1
	var event := {
		"sequence": sequence,
		"name": event_name,
		"payload": payload.duplicate(true),
	}
	events.append(event)
	return event.duplicate(true)


func events_named(event_name: String) -> Array[Dictionary]:
	var matches: Array[Dictionary] = []
	for event in events:
		if str(event.get("name", "")) == event_name:
			matches.append(event.duplicate(true))
	return matches


func export_json() -> String:
	return JSON.stringify({"schema_version": 1, "events": events.duplicate(true)}, "  ")


func clear() -> void:
	events.clear()
	sequence = 0
