class_name VSApp
extends Control

signal state_changed(previous_state: String, current_state: String)
signal item_selected(uid: String)

const OK_TRANSITION := "OK"
const INVALID_TRANSITION := "INVALID_TRANSITION"
const MISSING_DESTINATION := "MISSING_DESTINATION"
const INVALID_PAYLOAD := "INVALID_PAYLOAD"

const DECLARED_TRANSITIONS := {
	"WORKSHOP": ["FORGE", "ITEM_DETAIL"],
	"FORGE": ["ITEM_BIRTH"],
	"ITEM_BIRTH": ["ENHANCEMENT", "WORKSHOP"],
	"ENHANCEMENT": ["PRECISION", "CUSTOMER", "WORKSHOP"],
	"PRECISION": ["CUSTOMER", "WORKSHOP"],
	"CUSTOMER": ["RESULT"],
	"RESULT": ["REPAIR", "ITEM_DETAIL"],
	"REPAIR": ["ITEM_DETAIL"],
	"ITEM_DETAIL": ["WORKSHOP"],
}

var current_state := "WORKSHOP"
var _destinations: Dictionary = {}


func can_transition(previous_state: String, next_state: String) -> bool:
	return next_state in DECLARED_TRANSITIONS.get(previous_state, [])


func register_destination(state: String, scene: PackedScene) -> void:
	if scene != null:
		_destinations[state] = scene


func transition_to(next_state: String, payload: Dictionary = {}) -> String:
	if not can_transition(current_state, next_state):
		return INVALID_TRANSITION
	if not _destinations.has(next_state):
		return MISSING_DESTINATION
	if not _is_payload_valid(payload):
		return INVALID_PAYLOAD

	var previous_state := current_state
	current_state = next_state
	state_changed.emit(previous_state, current_state)
	return OK_TRANSITION


func _is_payload_valid(payload: Dictionary) -> bool:
	if payload.has("item_uid") and not payload["item_uid"] is String:
		return false
	return true
