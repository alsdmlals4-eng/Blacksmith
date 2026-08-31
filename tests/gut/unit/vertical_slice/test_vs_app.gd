extends "res://addons/gut/test.gd"

const APP_PATH := "res://scripts/vertical_slice/ui/vs_app.gd"
const APP_SCENE := preload("res://scenes/vertical_slice/vertical_slice_app.tscn")
const ItemScript := preload("res://scripts/vertical_slice/domain/vs_item.gd")
const ResourcesScript := preload("res://scripts/economy/workshop_resources.gd")
const RunInitializerScript := preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const ItemBirthServiceScript := preload("res://scripts/vertical_slice/services/vs_item_birth_service.gd")


class FakeSaveService extends RefCounted:
	var saved_envelope = null
	var next_save_error: Error = OK

	func save_envelope(envelope) -> Error:
		if next_save_error != OK:
			return next_save_error
		saved_envelope = envelope
		return OK


func _nadia_actual_use_event(item_uid: String) -> Dictionary:
	return {
		"content_result": {
			"schema_version": 1,
			"record_type": "CONTENT_RESULT_V1",
			"event_id": "app-customer-actual-use-001",
			"source_decision_id": "BS-CONTENT-20260811-01",
			"content_id": "ADVENTURER_01",
			"customer_id": "NADIA_VENN",
			"occurred_at_game_day": 1,
			"item_refs": [{"role": "PRIMARY_ITEM", "uid": item_uid}],
			"result_axes": {
				"EXPEDITION_RETURN_STATE": "RETURNED",
				"RECOVERY_STATE": "PARTIAL_RECOVERY",
				"ITEM_UID_LIFECYCLE_STATE": "DAMAGED_RETURN",
			},
			"causal_reasons": ["LOAD_GATE_PASSED", "UTILITY_MATCHED"],
			"primary_next_action": "REPAIR_ITEM",
		},
		"actual_item_use": true,
		"damage_profile": "DIRECT",
		"damage_cause": "CAVE_IN_DIRECT_HIT",
	}


func _new_app():
	if not ResourceLoader.exists(APP_PATH):
		return null
	var script = load(APP_PATH)
	if script == null:
		return null
	return script.new()


func test_app_router_surface_exists() -> void:
	assert_true(ResourceLoader.exists(APP_PATH), "Task 2 app router must exist at the approved script path")


func test_workshop_is_initial_state() -> void:
	var app = _new_app()
	assert_true(app != null, "Task 2 app router must load")
	if app == null:
		return
	assert_eq(app.current_state, "WORKSHOP", "Task 2 shell must enter at WORKSHOP")
	app.free()


func test_declared_edge_is_distinct_from_implemented_destination() -> void:
	var app = _new_app()
	assert_true(app != null, "Task 2 app router must load")
	if app == null:
		return
	assert_true(app.can_transition("WORKSHOP", "FORGE"), "WORKSHOP→FORGE must be declared")
	assert_eq(app.transition_to("FORGE"), app.MISSING_DESTINATION, "declared but unimplemented state must fail closed")
	assert_eq(app.current_state, "WORKSHOP", "missing destination must not mutate current state")
	app.free()


func test_undeclared_edge_fails_closed() -> void:
	var app = _new_app()
	assert_true(app != null, "Task 2 app router must load")
	if app == null:
		return
	assert_false(app.can_transition("WORKSHOP", "RESULT"), "WORKSHOP→RESULT must not bypass the declared graph")
	assert_eq(app.transition_to("RESULT"), app.INVALID_TRANSITION, "undeclared edge must fail closed")
	assert_eq(app.current_state, "WORKSHOP", "invalid transition must not mutate current state")
	app.free()


func test_app_binds_workshop_context_and_refreshes_after_damage() -> void:
	var item = ItemScript.new()
	item.uid = "APP-UI-ITEM-001"
	item.primary_material_id = "iron"
	item.enhancement_level = 11
	item.highest_checkpoint = 10
	item.base_max_durability = 5
	item.max_durability = 5
	item.current_durability = 3
	item.repair_job_available = true
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	app.configure_workshop_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	var screen = app.get_node("ScreenHost/WorkshopScreen")
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityValueLabel").text, "3 / 5 / 5")
	item.apply_damage_event()
	app.refresh_workshop_after_enhancement()
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityValueLabel").text, "2 / 5 / 5")
	assert_false(screen.get_node("WorkshopScroll/WorkshopLayout/RepairButton").disabled)


func test_campaign_configuration_binds_the_persisted_selected_item_to_workshop() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)

	assert_true(app.configure_campaign(envelope, ResourcesScript.new()))
	var screen = app.get_node("ScreenHost/WorkshopScreen")
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityValueLabel").text, "5 / 5 / 5")
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityStateLabel").text, "상태: 정상")


func test_applied_first_forge_completion_rebinds_the_workshop_item() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 22,
		"crafting_grade": "CRAFT_SUPERIOR",
		"artistry": 3,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.has_method("apply_first_forge_completion"), "app needs an explicit first-forge completion boundary")
	if not app.has_method("apply_first_forge_completion"):
		return
	assert_true(app.apply_first_forge_completion({"status": "APPLIED", "envelope": envelope}, ResourcesScript.new()))
	var screen = app.get_node("ScreenHost/WorkshopScreen")
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityValueLabel").text, "5 / 5 / 5")


func test_campaign_adopts_the_saved_envelope_after_a_workshop_enhancement() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var resources = ResourcesScript.new(20000, {"common_reinforcement_material": 10})
	var save_service := FakeSaveService.new()
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(envelope, resources, null, null, save_service))
	var screen = app.get_node("ScreenHost/WorkshopScreen")
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 99.0})
	assert_eq(result.get("outcome", ""), "SUCCESS")
	assert_same(app._campaign_envelope, save_service.saved_envelope)
	var saved_item = app._campaign_envelope.get_item(str(app._campaign_envelope.active_run["selected_item_uid"]))
	assert_eq(saved_item.enhancement_level, 1)


func test_customer_actual_use_saves_then_presents_the_same_persisted_result() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var source_item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var save_service := FakeSaveService.new()
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(envelope, ResourcesScript.new(), null, null, save_service))
	app.current_state = "CUSTOMER"
	assert_true(app.has_method("resolve_customer_actual_use_with_roll"))
	if not app.has_method("resolve_customer_actual_use_with_roll"):
		return
	assert_eq(
		str(app.call("resolve_customer_actual_use_with_roll", _nadia_actual_use_event(str(source_item.uid)), 0.0)),
		app.OK_TRANSITION
	)
	assert_eq(app.current_state, "RESULT")
	assert_true(save_service.saved_envelope != null)
	assert_eq(source_item.current_durability, 5, "source envelope must remain unchanged until saved candidate is adopted")
	var saved_item = save_service.saved_envelope.get_item(str(source_item.uid))
	assert_eq(saved_item.current_durability, 4)
	assert_same(app._campaign_envelope, save_service.saved_envelope)
	var result_screen = app.get_node("ScreenHost/CustomerResultScreen")
	assert_eq(result_screen.view_state().get("item_uid", ""), str(source_item.uid))
	assert_eq(result_screen.view_state().get("current_durability_text", ""), "내구도: 5 → 4")


func test_customer_actual_use_save_failure_preserves_state_and_does_not_present_result() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var source_item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var save_service := FakeSaveService.new()
	save_service.next_save_error = ERR_CANT_CREATE
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(envelope, ResourcesScript.new(), null, null, save_service))
	app.current_state = "CUSTOMER"
	assert_true(app.has_method("resolve_customer_actual_use_with_roll"))
	if not app.has_method("resolve_customer_actual_use_with_roll"):
		return
	assert_eq(
		str(app.call("resolve_customer_actual_use_with_roll", _nadia_actual_use_event(str(source_item.uid)), 0.0)),
		"SAVE_FAILED:%d" % ERR_CANT_CREATE
	)
	assert_eq(app.current_state, "CUSTOMER")
	assert_same(app._campaign_envelope, envelope)
	assert_eq(source_item.current_durability, 5)
	assert_true(envelope.active_run["resolved_events"].is_empty())
	assert_false(app.get_node("ScreenHost/CustomerResultScreen").visible)


func test_phase1_handoff_routes_one_active_level_ten_item_through_one_return_beat_before_actual_use() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var source_item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	source_item.enhancement_level = 10
	source_item.highest_checkpoint = 10
	var save_service := FakeSaveService.new()
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(envelope, ResourcesScript.new(), null, null, save_service))

	assert_true(app.has_method("begin_phase1_customer_handoff"), "Phase-1 needs an explicit +10 handoff entry")
	assert_true(app.has_method("complete_phase1_return_beat"), "Phase-1 needs exactly one non-economic return beat")
	assert_true(app.has_method("resolve_phase1_customer_actual_use_with_roll"), "Phase-1 needs one Nadia actual-use result after return")
	if not app.has_method("begin_phase1_customer_handoff") or not app.has_method("complete_phase1_return_beat") or not app.has_method("resolve_phase1_customer_actual_use_with_roll"):
		return

	var handoff_button := app.get_node_or_null("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/HandoffButton") as Button
	assert_not_null(handoff_button, "the handoff flow must be reachable from the visible workshop")
	if handoff_button == null:
		return
	assert_true(handoff_button.visible)
	handoff_button.emit_signal("pressed")
	assert_eq(app.current_state, "CUSTOMER")
	var handoff_screen = app.get_node_or_null("ScreenHost/CustomerHandoffScreen")
	assert_not_null(handoff_screen, "handoff must have a real player-facing screen")
	if handoff_screen == null:
		return
	assert_eq(str(handoff_screen.view_state().get("phase", "")), "HANDOFF")
	assert_eq(str(handoff_screen.view_state().get("item_uid", "")), str(source_item.uid))
	assert_true(str(handoff_screen.view_state().get("message", "")).contains("손상"), "handoff must state that handoff itself does not damage the item")
	assert_eq(str(app.call("complete_phase1_return_beat")), app.OK_TRANSITION)
	assert_eq(app.current_state, "RETURN")
	assert_eq(str(handoff_screen.view_state().get("phase", "")), "RETURN")
	assert_false(str(handoff_screen.view_state().get("message", "")).contains("대기"), "return beat must not introduce a wait timer")

	assert_eq(str(app.call("resolve_phase1_customer_actual_use_with_roll", 99.0)), app.OK_TRANSITION)
	assert_eq(app.current_state, "RESULT")
	assert_true(save_service.saved_envelope != null)
	assert_eq(save_service.saved_envelope.active_run["resolved_events"].size(), 1)
	var persisted_event: Dictionary = save_service.saved_envelope.active_run["resolved_events"].values()[0]
	assert_eq(persisted_event.get("customer_id", ""), "NADIA_VENN")
	assert_eq(persisted_event.get("item_refs", [])[0].get("uid", ""), str(source_item.uid))
	assert_true(bool(persisted_event.get("durability_consequence", {}).get("actual_item_use", false)))
	assert_false(bool(persisted_event.get("durability_consequence", {}).get("damage_applied", true)), "a real high roll must not script damage for the demonstration")
	var chronicle_action := app.get_node_or_null("ScreenHost/CustomerResultScreen/ResultLayout/ChronicleActionButton") as Button
	assert_not_null(chronicle_action, "an intact actual-use result must offer its same-UID chronicle")
	if chronicle_action == null:
		return
	assert_true(chronicle_action.visible)
	chronicle_action.emit_signal("pressed")
	assert_eq(app.current_state, "ITEM_DETAIL")
	var chronicle_screen = app.get_node_or_null("ScreenHost/ItemChronicleScreen")
	assert_not_null(chronicle_screen)
	if chronicle_screen == null:
		return
	assert_true(chronicle_screen.visible)
	assert_eq(chronicle_screen.view_state().get("entries", []).filter(func(entry): return str(entry.get("kind", "")) == "ACTUAL_USE").size(), 1)
	(chronicle_screen.get_node("ChronicleMargin/ChronicleLayout/WorkshopReturnButton") as Button).emit_signal("pressed")
	assert_eq(app.current_state, "WORKSHOP")
	assert_eq(str(app.call("resolve_phase1_customer_actual_use_with_roll", 0.0)), app.INVALID_TRANSITION, "a committed return cannot make a second actual-use roll")
	assert_eq(save_service.saved_envelope.active_run["resolved_events"].size(), 1)
	var reloaded_app = APP_SCENE.instantiate()
	add_child_autofree(reloaded_app)
	assert_true(reloaded_app.configure_campaign(save_service.saved_envelope, ResourcesScript.new(), null, null, FakeSaveService.new()))
	var reloaded_handoff_button := reloaded_app.get_node_or_null("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/HandoffButton") as Button
	assert_not_null(reloaded_handoff_button)
	if reloaded_handoff_button != null:
		assert_false(reloaded_handoff_button.visible, "a saved result must not reopen a fresh handoff after reload")
	assert_eq(reloaded_app.begin_phase1_customer_handoff(), "EVENT_ALREADY_RESOLVED")


func test_phase1_handoff_blocks_before_level_ten_and_for_destroyed_or_already_resolved_item() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(envelope, ResourcesScript.new(), null, null, FakeSaveService.new()))
	assert_true(app.has_method("begin_phase1_customer_handoff"), "Phase-1 needs a fail-closed handoff entry")
	if not app.has_method("begin_phase1_customer_handoff"):
		return

	assert_eq(str(app.call("begin_phase1_customer_handoff")), "HANDOFF_REQUIRES_LEVEL_10")
	assert_eq(app.current_state, "WORKSHOP")
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	item.current_durability = 0
	item.physical_state = "DESTROYED"
	assert_eq(str(app.call("begin_phase1_customer_handoff")), "ITEM_DESTROYED")
	assert_eq(app.current_state, "WORKSHOP")


func test_phase1_handoff_damage_result_routes_to_the_existing_workshop_repair_control() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var source_item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	source_item.enhancement_level = 10
	source_item.highest_checkpoint = 10
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(envelope, ResourcesScript.new(), null, null, FakeSaveService.new()))
	assert_eq(app.begin_phase1_customer_handoff(), app.OK_TRANSITION)
	assert_eq(app.complete_phase1_return_beat(), app.OK_TRANSITION)
	assert_eq(app.resolve_phase1_customer_actual_use_with_roll(0.0), app.OK_TRANSITION)
	var repair_action := app.get_node_or_null("ScreenHost/CustomerResultScreen/ResultLayout/RepairActionButton") as Button
	assert_not_null(repair_action, "actual damage must offer an actionable repair route")
	if repair_action == null:
		return
	assert_true(repair_action.visible)
	repair_action.emit_signal("pressed")
	assert_eq(app.current_state, "REPAIR")
	assert_false(app.get_node("ScreenHost/CustomerResultScreen").visible)
	assert_true(app.get_node("ScreenHost/WorkshopScreen").visible)
	assert_false((app.get_node("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/RepairButton") as Button).disabled)


func test_phase1_handoff_save_failure_preserves_the_return_beat_without_a_result_or_reroll_record() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	var save_service := FakeSaveService.new()
	save_service.next_save_error = ERR_CANT_CREATE
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(envelope, ResourcesScript.new(), null, null, save_service))
	assert_eq(app.begin_phase1_customer_handoff(), app.OK_TRANSITION)
	assert_eq(app.complete_phase1_return_beat(), app.OK_TRANSITION)
	assert_eq(app.resolve_phase1_customer_actual_use_with_roll(0.0), "SAVE_FAILED:%d" % ERR_CANT_CREATE)
	assert_eq(app.current_state, "RETURN")
	assert_true(envelope.active_run["resolved_events"].is_empty())
	assert_true(save_service.saved_envelope == null)
	assert_eq(str(app.get_node("ScreenHost/CustomerHandoffScreen").view_state().get("phase", "")), "RETURN")


func test_workshop_chronicle_action_displays_the_same_uid_saved_result_and_returns_to_workshop() -> void:
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var birth: Dictionary = ItemBirthServiceScript.new().commit_first_forge(envelope, {
		"weapon_id": "iron_sword",
		"base_attack": 20,
		"crafting_grade": "CRAFT_NORMAL",
		"artistry": 0,
	})
	assert_eq(birth.get("status", ""), "APPLIED")
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	envelope.active_run["resolved_events"] = {
		"phase1-nadia-actual-use-%s" % str(item.uid): {
			"event_id": "phase1-nadia-actual-use-%s" % str(item.uid),
			"content_id": "ADVENTURER_01",
			"customer_id": "NADIA_VENN",
			"item_refs": [{"role": "PRIMARY_ITEM", "uid": str(item.uid)}],
			"durability_consequence": {
				"actual_item_use": true,
				"damage_applied": false,
				"before_current_durability": 5,
				"after_current_durability": 5,
				"before_max_durability": 5,
				"after_max_durability": 5,
				"repair_job_available": false,
			},
		},
	}
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(envelope, ResourcesScript.new(), null, null, FakeSaveService.new()))
	var chronicle_button := app.get_node_or_null("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/ChronicleButton") as Button
	assert_not_null(chronicle_button)
	if chronicle_button == null:
		return
	chronicle_button.emit_signal("pressed")
	assert_eq(app.current_state, "ITEM_DETAIL")
	var chronicle_screen = app.get_node_or_null("ScreenHost/ItemChronicleScreen")
	assert_not_null(chronicle_screen)
	if chronicle_screen == null:
		return
	assert_true(chronicle_screen.visible)
	assert_eq(str(chronicle_screen.view_state().get("item_uid", "")), str(item.uid))
	assert_eq(chronicle_screen.view_state().get("entries", []).filter(func(entry): return str(entry.get("kind", "")) == "ACTUAL_USE").size(), 1)
	var return_button := chronicle_screen.get_node_or_null("ChronicleMargin/ChronicleLayout/WorkshopReturnButton") as Button
	assert_not_null(return_button)
	if return_button == null:
		return
	return_button.emit_signal("pressed")
	assert_eq(app.current_state, "WORKSHOP")
	assert_false(chronicle_screen.visible)
	assert_true(app.get_node("ScreenHost/WorkshopScreen").visible)
