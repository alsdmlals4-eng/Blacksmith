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
	assert_eq(screen.get_node("WorkshopLayout/DurabilityValueLabel").text, "3 / 5 / 5")
	item.apply_damage_event()
	app.refresh_workshop_after_enhancement()
	assert_eq(screen.get_node("WorkshopLayout/DurabilityValueLabel").text, "2 / 5 / 5")
	assert_false(screen.get_node("WorkshopLayout/RepairButton").disabled)


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
	assert_eq(screen.get_node("WorkshopLayout/DurabilityValueLabel").text, "5 / 5 / 5")
	assert_eq(screen.get_node("WorkshopLayout/DurabilityStateLabel").text, "상태: 정상")


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
	assert_eq(screen.get_node("WorkshopLayout/DurabilityValueLabel").text, "5 / 5 / 5")


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
