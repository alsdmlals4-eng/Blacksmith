extends "res://addons/gut/test.gd"

const MAIN_MENU_SCENE := preload("res://scenes/vertical_slice/main_menu.tscn")
const INITIALIZER_PATH := "res://scripts/vertical_slice/services/vs_run_initializer_service.gd"
const RESOURCES_PATH := "res://scripts/economy/workshop_resources.gd"
const COMPLETION_PATH := "res://scripts/vertical_slice/services/vs_first_forge_completion_service.gd"


class FakeSaveService:
	extends RefCounted
	var envelope = null

	func load_envelope():
		return envelope

	func save_envelope(candidate) -> Error:
		envelope = candidate
		return OK

	func replace_envelope_after_confirmation(candidate) -> Error:
		envelope = candidate
		return OK


func _completed_result() -> Dictionary:
	return {
		"weapon_id": "iron_sword",
		"base_attack": 22,
		"quality_id": "GOOD",
		"tap_count": 12,
		"fever_activation_count": 1,
		"fever_bonus_applied": true,
	}


func test_first_forge_screen_completion_opens_workshop_with_saved_selected_item() -> void:
	var menu = MAIN_MENU_SCENE.instantiate()
	add_child_autofree(menu)
	await get_tree().process_frame
	var save_service := FakeSaveService.new()
	var initializer = load(INITIALIZER_PATH).new()
	menu.configure_flow_services(
		save_service,
		initializer,
		load(RESOURCES_PATH).new(),
		load(COMPLETION_PATH).new()
	)
	var envelope = initializer.create_candidate_envelope()
	assert_true(menu.begin_first_forge(envelope), "empty current campaign must open the first forge")
	assert_eq(menu._resources.gold, 20000, "first forge must restore saved TEMP_TEST_BUDGET gold")
	assert_eq(
		menu._resources.get_material_count("common_reinforcement_material"),
		30,
		"first forge must restore saved TEMP_TEST_BUDGET reinforcement material"
	)
	await get_tree().process_frame
	assert_true(menu.has_active_first_forge(), "first forge screen must be mounted")

	menu.apply_completed_first_forge_result(_completed_result())
	assert_false(menu.has_active_first_forge(), "completed forge screen must be released")
	assert_true(menu.has_active_workshop(), "saved first item must open the workshop")
	assert_eq(str(save_service.envelope.active_run.get("selected_item_uid", "")), str(menu.current_selected_item_uid()))
