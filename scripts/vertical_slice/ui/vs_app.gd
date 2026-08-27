class_name VSApp
extends Control

signal state_changed(previous_state: String, current_state: String)

const OK_TRANSITION := "OK"
const INVALID_TRANSITION := "INVALID_TRANSITION"
const MISSING_DESTINATION := "MISSING_DESTINATION"
const INVALID_PAYLOAD := "INVALID_PAYLOAD"
const CustomerResultScene = preload("res://scenes/vertical_slice/screens/vs_customer_result_screen.tscn")
const CustomerActualUseActionServiceScript = preload(
	"res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd"
)

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
var _save_service = null


func _ready() -> void:
	register_destination("RESULT", CustomerResultScene)


func configure_campaign(envelope, resources, maintenance_service = null, enhancement_action_service = null, save_service = null) -> bool:
	if envelope == null or not envelope.validation_errors.is_empty() or resources == null:
		return false
	_save_service = save_service
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


func present_resolved_customer_result(event_id: String) -> String:
	if current_state != "CUSTOMER":
		return INVALID_TRANSITION
	if _campaign_envelope == null or not _campaign_envelope.active_run is Dictionary:
		return INVALID_PAYLOAD
	var resolved_events = _campaign_envelope.active_run.get("resolved_events", null)
	if event_id.is_empty() or not resolved_events is Dictionary or not resolved_events.has(event_id):
		return INVALID_PAYLOAD
	var result = resolved_events[event_id]
	var result_screen := get_node_or_null("ScreenHost/CustomerResultScreen")
	if not result is Dictionary or result_screen == null or not result_screen.has_method("configure_resolved_result"):
		return INVALID_PAYLOAD
	var configured: Dictionary = result_screen.call("configure_resolved_result", result)
	if str(configured.get("status", "")) != "APPLIED":
		return INVALID_PAYLOAD
	var view_state: Dictionary = result_screen.call("view_state")
	var transition := transition_to("RESULT", {"item_uid": str(view_state.get("item_uid", ""))})
	if transition != OK_TRANSITION:
		return transition
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	if workshop_screen != null:
		workshop_screen.visible = false
	result_screen.visible = true
	return OK_TRANSITION


func resolve_customer_actual_use_with_roll(event: Dictionary, damage_roll_percent: float) -> String:
	if current_state != "CUSTOMER":
		return INVALID_TRANSITION
	if _campaign_envelope == null or _save_service == null:
		return INVALID_PAYLOAD
	var item_uid := str(_campaign_envelope.active_run.get("selected_item_uid", ""))
	if item_uid.is_empty():
		return INVALID_PAYLOAD
	var result: Dictionary = CustomerActualUseActionServiceScript.new().resolve_and_save_with_roll(
		_campaign_envelope,
		item_uid,
		event,
		damage_roll_percent,
		_save_service
	)
	if str(result.get("status", "")) != "APPLIED":
		return str(result.get("reason", INVALID_PAYLOAD))
	var saved_envelope = result.get("envelope", null)
	if saved_envelope == null or str(result.get("event_id", "")).is_empty():
		return INVALID_PAYLOAD
	_campaign_envelope = saved_envelope
	var saved_item = _campaign_envelope.get_item(item_uid)
	configure_workshop_context(saved_item, _workshop_resources, null, null, _save_service, _campaign_envelope)
	return present_resolved_customer_result(str(result["event_id"]))


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
