class_name VSApp
extends Control

signal state_changed(previous_state: String, current_state: String)

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
var _campaign_envelope = null
var _workshop_resources = null


func configure_campaign(envelope, resources, maintenance_service = null, enhancement_action_service = null, save_service = null) -> bool:
	if envelope == null or not envelope.validation_errors.is_empty() or resources == null:
		return false
	var selected_item_uid := str(envelope.active_run.get("selected_item_uid", ""))
	if selected_item_uid.is_empty():
		if not envelope.items_by_uid.is_empty():
			return false
		_campaign_envelope = envelope
		_workshop_resources = resources
		return configure_workshop_context(null, resources, maintenance_service, enhancement_action_service, save_service, envelope)
	var selected_item = envelope.get_item(selected_item_uid)
	if selected_item == null:
		return false
	_campaign_envelope = envelope
	_workshop_resources = resources
	return configure_workshop_context(selected_item, resources, maintenance_service, enhancement_action_service, save_service, envelope)


func apply_first_forge_completion(completion: Dictionary, resources, maintenance_service = null, enhancement_action_service = null, save_service = null) -> bool:
	if str(completion.get("status", "")) != "APPLIED":
		return false
	return configure_campaign(completion.get("envelope", null), resources, maintenance_service, enhancement_action_service, save_service)


func configure_workshop_context(item, resources, maintenance_service = null, enhancement_action_service = null, save_service = null, campaign_envelope = null) -> bool:
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	if workshop_screen == null or not workshop_screen.has_method("configure_context"):
		return false
	workshop_screen.call("configure_context", item, resources, maintenance_service, enhancement_action_service, save_service, campaign_envelope)
	if workshop_screen.has_signal("enhancement_saved") and not workshop_screen.enhancement_saved.is_connected(_on_workshop_enhancement_saved):
		workshop_screen.enhancement_saved.connect(_on_workshop_enhancement_saved)
	return true


func _on_workshop_enhancement_saved(envelope, _result: Dictionary) -> void:
	_campaign_envelope = envelope


func refresh_workshop_after_enhancement() -> bool:
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	if workshop_screen == null or not workshop_screen.has_method("refresh_after_enhancement"):
		return false
	workshop_screen.call("refresh_after_enhancement")
	return true


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
