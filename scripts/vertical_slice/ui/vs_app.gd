class_name VSApp
extends Control

signal state_changed(previous_state: String, current_state: String)

const OK_TRANSITION := "OK"
const INVALID_TRANSITION := "INVALID_TRANSITION"
const MISSING_DESTINATION := "MISSING_DESTINATION"
const INVALID_PAYLOAD := "INVALID_PAYLOAD"
const CustomerResultScene = preload("res://scenes/vertical_slice/screens/vs_customer_result_screen.tscn")
const WorkshopScreenScene = preload("res://scenes/vertical_slice/screens/vs_workshop_screen.tscn")
const CustomerHandoffScreenScript = preload("res://scripts/vertical_slice/ui/vs_customer_handoff_screen.gd")
const ItemChronicleScreenScript = preload("res://scripts/vertical_slice/ui/vs_item_chronicle_screen.gd")
const CustomerActualUseActionServiceScript = preload(
	"res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd"
)
const CustomerProfileRepositoryScript = preload(
	"res://scripts/vertical_slice/services/vs_customer_profile_repository.gd"
)
const PHASE1_HANDOFF_MINIMUM_LEVEL := 10
const PHASE1_CUSTOMER_ID := "NADIA_VENN"
const PHASE1_NADIA_EVENT_PREFIX := "phase1-nadia-actual-use-"

const DECLARED_TRANSITIONS := {
	"WORKSHOP": ["FORGE", "ITEM_DETAIL", "CUSTOMER"],
	"FORGE": ["ITEM_BIRTH"],
	"ITEM_BIRTH": ["ENHANCEMENT", "WORKSHOP"],
	"ENHANCEMENT": ["PRECISION", "CUSTOMER", "WORKSHOP"],
	"PRECISION": ["CUSTOMER", "WORKSHOP"],
	"CUSTOMER": ["RETURN", "RESULT"],
	"RETURN": ["RESULT"],
	"RESULT": ["REPAIR", "ITEM_DETAIL"],
	"REPAIR": ["ITEM_DETAIL"],
	"ITEM_DETAIL": ["WORKSHOP"],
}

var current_state := "WORKSHOP"
var _destinations: Dictionary = {}
var _campaign_envelope = null
var _workshop_resources = null
var _save_service = null
var _phase1_handoff_item_uid := ""


func _ready() -> void:
	register_destination("WORKSHOP", WorkshopScreenScene)
	register_destination("RESULT", CustomerResultScene)
	register_destination("CUSTOMER", CustomerHandoffScreenScript)
	register_destination("RETURN", CustomerHandoffScreenScript)
	register_destination("REPAIR", WorkshopScreenScene)
	register_destination("ITEM_DETAIL", ItemChronicleScreenScript)
	_connect_workshop_handoff()
	_connect_customer_result_actions()


func configure_campaign(envelope, resources, maintenance_service = null, enhancement_action_service = null, save_service = null) -> bool:
	if envelope == null or not envelope.validation_errors.is_empty() or resources == null:
		return false
	if not _synchronize_workshop_resources(resources, envelope):
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


func _synchronize_workshop_resources(resources, envelope) -> bool:
	if (
		not resources.has_method("snapshot")
		or not envelope.has_method("resource_snapshot")
		or not resources.get("gold") is int
		or not resources.get("material_stock") is Dictionary
	):
		return false
	var saved_resources: Dictionary = envelope.resource_snapshot()
	var saved_stock: Variant = saved_resources.get("material_stock", null)
	if not saved_resources.get("gold") is int or not saved_stock is Dictionary:
		return false
	if resources.snapshot() == saved_resources:
		return true
	resources.set("gold", int(saved_resources["gold"]))
	resources.set("material_stock", saved_stock.duplicate(true))
	if resources.has_signal("changed"):
		resources.emit_signal("changed", resources.snapshot())
	return resources.snapshot() == saved_resources


func apply_first_forge_completion(completion: Dictionary, resources, maintenance_service = null, enhancement_action_service = null, save_service = null) -> bool:
	if str(completion.get("status", "")) != "APPLIED":
		return false
	return configure_campaign(completion.get("envelope", null), resources, maintenance_service, enhancement_action_service, save_service)


func configure_workshop_context(item, resources, maintenance_service = null, enhancement_action_service = null, save_service = null, campaign_envelope = null) -> bool:
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	if workshop_screen == null or not workshop_screen.has_method("configure_context"):
		return false
	workshop_screen.call(
		"configure_context",
		item,
		resources,
		maintenance_service,
		enhancement_action_service,
		save_service,
		campaign_envelope,
		_customer_profile_or_null(PHASE1_CUSTOMER_ID)
	)
	if workshop_screen.has_signal("enhancement_saved") and not workshop_screen.enhancement_saved.is_connected(_on_workshop_enhancement_saved):
		workshop_screen.enhancement_saved.connect(_on_workshop_enhancement_saved)
	_connect_workshop_handoff()
	return true


func _on_workshop_enhancement_saved(envelope, _result: Dictionary) -> void:
	_campaign_envelope = envelope


func _on_workshop_handoff_requested() -> void:
	begin_phase1_customer_handoff()


func _on_workshop_chronicle_requested() -> void:
	begin_item_chronicle()


func _connect_workshop_handoff() -> void:
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	if workshop_screen == null:
		return
	if workshop_screen.has_signal("handoff_requested") and not workshop_screen.is_connected("handoff_requested", _on_workshop_handoff_requested):
		workshop_screen.connect("handoff_requested", _on_workshop_handoff_requested)
	if workshop_screen.has_signal("chronicle_requested") and not workshop_screen.is_connected("chronicle_requested", _on_workshop_chronicle_requested):
		workshop_screen.connect("chronicle_requested", _on_workshop_chronicle_requested)


func _connect_customer_result_actions() -> void:
	var result_screen := get_node_or_null("ScreenHost/CustomerResultScreen")
	if result_screen == null:
		return
	if result_screen.has_signal("repair_requested") and not result_screen.is_connected("repair_requested", _on_customer_repair_requested):
		result_screen.connect("repair_requested", _on_customer_repair_requested)
	if result_screen.has_signal("chronicle_requested") and not result_screen.is_connected("chronicle_requested", _on_customer_chronicle_requested):
		result_screen.connect("chronicle_requested", _on_customer_chronicle_requested)


func _on_customer_repair_requested() -> void:
	_present_result_followup("REPAIR", true)


func _on_customer_chronicle_requested() -> void:
	if current_state != "RESULT":
		return
	var result_screen := get_node_or_null("ScreenHost/CustomerResultScreen")
	if result_screen == null or not result_screen.has_method("view_state"):
		return
	var state: Dictionary = result_screen.call("view_state")
	if bool(state.get("repair_available", false)):
		return
	var item_uid := str(state.get("item_uid", ""))
	if item_uid.is_empty() or transition_to("ITEM_DETAIL", {"item_uid": item_uid}) != OK_TRANSITION:
		return
	_show_item_chronicle(item_uid)


func _present_result_followup(next_state: String, requires_repair: bool) -> void:
	if current_state != "RESULT":
		return
	var result_screen := get_node_or_null("ScreenHost/CustomerResultScreen")
	if result_screen == null or not result_screen.has_method("view_state"):
		return
	var state: Dictionary = result_screen.call("view_state")
	if bool(state.get("repair_available", false)) != requires_repair:
		return
	var item_uid := str(state.get("item_uid", ""))
	if item_uid.is_empty():
		return
	if transition_to(next_state, {"item_uid": item_uid}) != OK_TRANSITION:
		return
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	var handoff_screen := get_node_or_null("ScreenHost/CustomerHandoffScreen")
	result_screen.visible = false
	if handoff_screen != null:
		handoff_screen.visible = false
	if workshop_screen != null:
		workshop_screen.visible = true


func refresh_workshop_after_enhancement() -> bool:
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	if workshop_screen == null or not workshop_screen.has_method("refresh_after_enhancement"):
		return false
	workshop_screen.call("refresh_after_enhancement")
	return true


func present_resolved_customer_result(event_id: String) -> String:
	if not current_state in ["CUSTOMER", "RETURN"]:
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
	var configured: Dictionary = result_screen.call(
		"configure_resolved_result",
		result,
		_customer_profile_or_null(str(result.get("customer_id", "")))
	)
	if str(configured.get("status", "")) != "APPLIED":
		return INVALID_PAYLOAD
	var view_state: Dictionary = result_screen.call("view_state")
	var transition := transition_to("RESULT", {"item_uid": str(view_state.get("item_uid", ""))})
	if transition != OK_TRANSITION:
		return transition
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	if workshop_screen != null:
		workshop_screen.visible = false
	var handoff_screen := get_node_or_null("ScreenHost/CustomerHandoffScreen")
	if handoff_screen != null:
		handoff_screen.visible = false
	result_screen.visible = true
	_connect_customer_result_actions()
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


func begin_phase1_customer_handoff() -> String:
	if not current_state in ["WORKSHOP", "ENHANCEMENT", "PRECISION"]:
		return INVALID_TRANSITION
	var handoff_item = _phase1_handoff_item()
	if handoff_item == null:
		return INVALID_PAYLOAD
	if int(handoff_item.enhancement_level) < PHASE1_HANDOFF_MINIMUM_LEVEL:
		return "HANDOFF_REQUIRES_LEVEL_10"
	if int(handoff_item.current_durability) <= 0 or str(handoff_item.physical_state) == "DESTROYED":
		return "ITEM_DESTROYED"
	var item_uid := str(handoff_item.uid)
	if _has_phase1_resolved_event(item_uid):
		return "EVENT_ALREADY_RESOLVED"
	var handoff_screen: Control = _ensure_customer_handoff_screen()
	if handoff_screen == null:
		return INVALID_PAYLOAD
	var customer_profile = _customer_profile_or_null(PHASE1_CUSTOMER_ID)
	if customer_profile == null:
		return INVALID_PAYLOAD
	var configured: Dictionary = handoff_screen.call("configure_handoff", item_uid, int(handoff_item.enhancement_level), customer_profile)
	if str(configured.get("status", "")) != "APPLIED":
		return INVALID_PAYLOAD
	var transition := transition_to("CUSTOMER", {"item_uid": item_uid})
	if transition != OK_TRANSITION:
		return transition
	_phase1_handoff_item_uid = item_uid
	_set_phase1_handoff_visibility(true)
	return OK_TRANSITION


func complete_phase1_return_beat() -> String:
	if current_state != "CUSTOMER" or _phase1_handoff_item_uid.is_empty():
		return INVALID_TRANSITION
	var handoff_screen: Control = _ensure_customer_handoff_screen()
	if handoff_screen == null:
		return INVALID_PAYLOAD
	var customer_profile = _customer_profile_or_null(PHASE1_CUSTOMER_ID)
	if customer_profile == null:
		return INVALID_PAYLOAD
	var configured: Dictionary = handoff_screen.call("configure_return_beat", _phase1_handoff_item_uid, customer_profile)
	if str(configured.get("status", "")) != "APPLIED":
		return INVALID_PAYLOAD
	var transition := transition_to("RETURN", {"item_uid": _phase1_handoff_item_uid})
	if transition != OK_TRANSITION:
		return transition
	_set_phase1_handoff_visibility(true)
	return OK_TRANSITION


func resolve_phase1_customer_actual_use_with_roll(damage_roll_percent: float) -> String:
	if current_state != "RETURN" or _phase1_handoff_item_uid.is_empty():
		return INVALID_TRANSITION
	var item_uid := _phase1_handoff_item_uid
	if _has_phase1_resolved_event(item_uid):
		return "EVENT_ALREADY_RESOLVED"
	return resolve_customer_actual_use_with_roll_from_return(_phase1_customer_actual_use_event(item_uid), damage_roll_percent)


func resolve_phase1_customer_actual_use() -> String:
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	return resolve_phase1_customer_actual_use_with_roll(rng.randf_range(0.0, 100.0))


func resolve_customer_actual_use_with_roll_from_return(event: Dictionary, damage_roll_percent: float) -> String:
	if current_state != "RETURN":
		return INVALID_TRANSITION
	if _campaign_envelope == null or _save_service == null or _phase1_handoff_item_uid.is_empty():
		return INVALID_PAYLOAD
	var result: Dictionary = CustomerActualUseActionServiceScript.new().resolve_and_save_with_roll(
		_campaign_envelope,
		_phase1_handoff_item_uid,
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
	var saved_item = _campaign_envelope.get_item(_phase1_handoff_item_uid)
	configure_workshop_context(saved_item, _workshop_resources, null, null, _save_service, _campaign_envelope)
	_phase1_handoff_item_uid = ""
	return present_resolved_customer_result(str(result["event_id"]))


func _phase1_handoff_item():
	if _campaign_envelope == null or not _campaign_envelope.active_run is Dictionary:
		return null
	var item_uid := str(_campaign_envelope.active_run.get("selected_item_uid", ""))
	if item_uid.is_empty():
		return null
	return _campaign_envelope.get_item(item_uid)


func _customer_profile_or_null(customer_id: String):
	if customer_id.is_empty():
		return null
	var loaded: Dictionary = CustomerProfileRepositoryScript.new().load_profile(customer_id)
	return loaded.get("profile", null) if str(loaded.get("status", "")) == "APPLIED" else null


func _has_phase1_resolved_event(item_uid: String) -> bool:
	if _campaign_envelope == null or not _campaign_envelope.active_run is Dictionary:
		return false
	var resolved_events: Variant = _campaign_envelope.active_run.get("resolved_events", {})
	return resolved_events is Dictionary and resolved_events.has(_phase1_event_id(item_uid))


func _phase1_event_id(item_uid: String) -> String:
	return "%s%s" % [PHASE1_NADIA_EVENT_PREFIX, item_uid]


func _phase1_customer_actual_use_event(item_uid: String) -> Dictionary:
	var customer_profile = _customer_profile_or_null(PHASE1_CUSTOMER_ID)
	if customer_profile == null:
		return {}
	return {
		"content_result": {
			"schema_version": 1,
			"record_type": "CONTENT_RESULT_V1",
			"event_id": _phase1_event_id(item_uid),
			"source_decision_id": "BS-CONTENT-20260811-01",
			"content_id": customer_profile.content_id,
			"customer_id": customer_profile.customer_id,
			"occurred_at_game_day": int(_campaign_envelope.active_run.get("current_day", 1)),
			"item_refs": [{"role": "PRIMARY_ITEM", "uid": item_uid}],
			"result_axes": {
				"EXPEDITION_RETURN_STATE": "RETURNED",
				"RECOVERY_STATE": "STATUS_RECORDED",
				"ITEM_UID_LIFECYCLE_STATE": "ACTUAL_USE_RECORDED",
			},
			"causal_reasons": ["RUIN_EXPEDITION", "ACTUAL_ITEM_USE"],
			"primary_next_action": "REPAIR_ITEM",
		},
		"actual_item_use": true,
		"damage_profile": "MEDIUM",
		"damage_cause": "RUIN_EXPEDITION_HAZARD",
	}


func begin_item_chronicle() -> String:
	if not current_state in ["WORKSHOP", "REPAIR"]:
		return INVALID_TRANSITION
	var item = _phase1_handoff_item()
	if item == null:
		return INVALID_PAYLOAD
	var item_uid := str(item.uid)
	if transition_to("ITEM_DETAIL", {"item_uid": item_uid}) != OK_TRANSITION:
		return INVALID_TRANSITION
	return _show_item_chronicle(item_uid)


func _ensure_item_chronicle_screen() -> Control:
	var screen_host := get_node_or_null("ScreenHost") as Control
	if screen_host == null:
		return null
	var chronicle_screen: Control = screen_host.get_node_or_null("ItemChronicleScreen") as Control
	if chronicle_screen == null:
		chronicle_screen = ItemChronicleScreenScript.new() as Control
		chronicle_screen.name = "ItemChronicleScreen"
		chronicle_screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		chronicle_screen.visible = false
		screen_host.add_child(chronicle_screen)
	if chronicle_screen.has_signal("workshop_requested") and not chronicle_screen.is_connected("workshop_requested", _on_item_chronicle_workshop_requested):
		chronicle_screen.connect("workshop_requested", _on_item_chronicle_workshop_requested)
	return chronicle_screen


func _show_item_chronicle(item_uid: String) -> String:
	if _campaign_envelope == null or not _campaign_envelope.active_run is Dictionary:
		return INVALID_PAYLOAD
	var item = _campaign_envelope.get_item(item_uid)
	var raw_events: Variant = _campaign_envelope.active_run.get("resolved_events", {})
	if item == null or not raw_events is Dictionary:
		return INVALID_PAYLOAD
	var chronicle_screen: Control = _ensure_item_chronicle_screen()
	if chronicle_screen == null:
		return INVALID_PAYLOAD
	var configured: Dictionary = chronicle_screen.call(
		"configure_item",
		item,
		raw_events,
		_customer_profile_or_null(PHASE1_CUSTOMER_ID)
	)
	if str(configured.get("status", "")) != "APPLIED":
		return INVALID_PAYLOAD
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	var result_screen := get_node_or_null("ScreenHost/CustomerResultScreen")
	var handoff_screen := get_node_or_null("ScreenHost/CustomerHandoffScreen")
	if workshop_screen != null:
		workshop_screen.visible = false
	if result_screen != null:
		result_screen.visible = false
	if handoff_screen != null:
		handoff_screen.visible = false
	chronicle_screen.visible = true
	return OK_TRANSITION


func _on_item_chronicle_workshop_requested() -> void:
	if current_state != "ITEM_DETAIL":
		return
	var chronicle_screen := get_node_or_null("ScreenHost/ItemChronicleScreen") as Control
	if chronicle_screen == null:
		return
	var state: Dictionary = chronicle_screen.call("view_state")
	var item_uid := str(state.get("item_uid", ""))
	if item_uid.is_empty() or transition_to("WORKSHOP", {"item_uid": item_uid}) != OK_TRANSITION:
		return
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	chronicle_screen.visible = false
	if workshop_screen != null:
		workshop_screen.visible = true


func _ensure_customer_handoff_screen() -> Control:
	var screen_host := get_node_or_null("ScreenHost") as Control
	if screen_host == null:
		return null
	var handoff_screen: Control = screen_host.get_node_or_null("CustomerHandoffScreen") as Control
	if handoff_screen == null:
		handoff_screen = CustomerHandoffScreenScript.new() as Control
		handoff_screen.name = "CustomerHandoffScreen"
		handoff_screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		handoff_screen.visible = false
		screen_host.add_child(handoff_screen)
	if handoff_screen.has_signal("handoff_confirmed") and not handoff_screen.is_connected("handoff_confirmed", _on_handoff_confirmed):
		handoff_screen.connect("handoff_confirmed", _on_handoff_confirmed)
	if handoff_screen.has_signal("return_beat_continued") and not handoff_screen.is_connected("return_beat_continued", _on_return_beat_continued):
		handoff_screen.connect("return_beat_continued", _on_return_beat_continued)
	return handoff_screen


func _on_handoff_confirmed() -> void:
	complete_phase1_return_beat()


func _on_return_beat_continued() -> void:
	resolve_phase1_customer_actual_use()


func _set_phase1_handoff_visibility(should_show_handoff: bool) -> void:
	var workshop_screen := get_node_or_null("ScreenHost/WorkshopScreen")
	var result_screen := get_node_or_null("ScreenHost/CustomerResultScreen")
	var handoff_screen: Control = _ensure_customer_handoff_screen()
	if workshop_screen != null:
		workshop_screen.visible = not should_show_handoff
	if result_screen != null:
		result_screen.visible = false
	if handoff_screen != null:
		handoff_screen.visible = should_show_handoff


func can_transition(previous_state: String, next_state: String) -> bool:
	return next_state in DECLARED_TRANSITIONS.get(previous_state, [])


func register_destination(state: String, destination: Resource) -> void:
	if destination != null:
		_destinations[state] = destination


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
