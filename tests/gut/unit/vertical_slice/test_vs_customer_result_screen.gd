extends "res://addons/gut/test.gd"

const SCREEN_PATH := "res://scripts/vertical_slice/ui/vs_customer_result_screen.gd"
const SCREEN_SCENE_PATH := "res://scenes/vertical_slice/screens/vs_customer_result_screen.tscn"
const APP_SCENE := preload("res://scenes/vertical_slice/vertical_slice_app.tscn")
const ResourcesScript := preload("res://scripts/economy/workshop_resources.gd")
const RunInitializerScript := preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")

const EVENT_ID := "nadia-actual-use-001"
const ITEM_UID := "BSI-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
const APPROVED_RESULT_ILLUSTRATION_PATH := "res://assets/ui/workshop/customer_result_return_illustration_v1.png"


func _resolved_result() -> Dictionary:
	return {
		"schema_version": 1,
		"record_type": "CONTENT_RESULT_V1",
		"event_id": EVENT_ID,
		"content_id": "ADVENTURER_01",
		"customer_id": "NADIA_VENN",
		"item_refs": [{"role": "PRIMARY_ITEM", "uid": ITEM_UID}],
		"primary_next_action": "REPAIR_ITEM",
		"durability_consequence": {
			"actual_item_use": true,
			"damage_applied": true,
			"damage_cause": "CAVE_IN_DIRECT_HIT",
			"declared_damage_profile": "DIRECT",
			"effective_damage_profile": "DIRECT",
			"before_current_durability": 5,
			"after_current_durability": 4,
			"before_max_durability": 5,
			"after_max_durability": 5,
			"repair_job_available": true,
		},
	}


func _new_screen():
	if not ResourceLoader.exists(SCREEN_SCENE_PATH):
		return null
	var scene = load(SCREEN_SCENE_PATH)
	return scene.instantiate() if scene != null else null


func test_customer_result_surface_exists_as_a_vertical_scene() -> void:
	assert_true(ResourceLoader.exists(SCREEN_PATH), "customer result controller must exist")
	assert_true(ResourceLoader.exists(SCREEN_SCENE_PATH), "customer result must have a concrete vertical screen")


func test_persisted_actual_use_damage_is_presented_without_recalculation() -> void:
	var screen = _new_screen()
	assert_true(screen != null, "customer result screen must instantiate")
	if screen == null:
		return
	add_child_autofree(screen)
	var stored_result := _resolved_result()
	var stored_before := stored_result.duplicate(true)
	var configured: Dictionary = screen.configure_resolved_result(stored_result)
	assert_eq(configured.get("status", ""), "APPLIED")
	assert_eq(stored_result, stored_before, "result presentation must not mutate the persisted fact")
	assert_eq(screen.view_state(), {
		"event_id": EVENT_ID,
		"item_uid": ITEM_UID,
		"summary_text": "고객의 실제 사용 결과입니다.",
		"damage_text": "실제 사용 중 손상이 발생했습니다.",
		"current_durability_text": "내구도: 5 → 4",
		"max_durability_text": "최대 내구도: 5 → 5",
		"next_action_text": "다음 행동: 수리하기",
		"repair_available": true,
	})
	assert_eq(screen.get_node("ResultLayout/CurrentDurabilityLabel").text, "내구도: 5 → 4")
	assert_eq(screen.get_node("ResultLayout/NextActionLabel").text, "다음 행동: 수리하기")
	assert_eq(screen.get_node("ResultLayout/RepairActionHint").text, "작업대에서 수리하기")


func test_customer_result_uses_the_approved_illustration_and_veil_only_after_a_valid_saved_result() -> void:
	assert_true(ResourceLoader.exists(APPROVED_RESULT_ILLUSTRATION_PATH), "approved customer-result illustration must be tracked before the saved fact can reveal it")
	if not ResourceLoader.exists(APPROVED_RESULT_ILLUSTRATION_PATH):
		return
	var screen = _new_screen()
	assert_not_null(screen)
	if screen == null:
		return
	add_child_autofree(screen)
	var illustration := screen.get_node_or_null("CustomerResultEventIllustration") as TextureRect
	var veil := screen.get_node_or_null("CustomerResultReadabilityVeil") as ColorRect
	var fallback := screen.get_node_or_null("ResultBackground") as ColorRect
	assert_not_null(illustration, "dynamic event illustration layer must exist without a serialized scene node")
	assert_not_null(veil, "dynamic readability veil must stay between illustration and native result controls")
	assert_not_null(fallback)
	if illustration == null or veil == null or fallback == null:
		return
	assert_false(illustration.visible, "no saved result must preserve the opaque fallback")
	assert_false(veil.visible)
	assert_true(fallback.visible)
	assert_eq(screen.configure_resolved_result(_resolved_result()).get("status", ""), "APPLIED")
	assert_true(illustration.visible)
	assert_true(veil.visible)
	assert_false(fallback.visible)
	assert_eq(illustration.texture.resource_path, APPROVED_RESULT_ILLUSTRATION_PATH)
	assert_eq(illustration.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(illustration.z_index, -1)
	assert_eq(illustration.expand_mode, TextureRect.EXPAND_IGNORE_SIZE)
	assert_eq(illustration.stretch_mode, TextureRect.STRETCH_KEEP_ASPECT_COVERED)
	assert_eq(veil.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(veil.z_index, -1)
	assert_gt(veil.color.a, 0.0)
	assert_gt(screen.get_node("ResultLayout").get_index(), veil.get_index(), "native factual controls must remain above the visual-only veil")
	var invalid := _resolved_result()
	invalid["durability_consequence"].erase("after_current_durability")
	assert_eq(screen.configure_resolved_result(invalid).get("status", ""), "BLOCKED")
	assert_false(illustration.visible, "invalid input must retain factual text but restore the opaque visual fallback")
	assert_false(veil.visible)
	assert_true(fallback.visible)


func test_invalid_result_fails_closed_and_preserves_the_last_visible_fact() -> void:
	var screen = _new_screen()
	assert_true(screen != null, "customer result screen must instantiate")
	if screen == null:
		return
	add_child_autofree(screen)
	assert_eq(screen.configure_resolved_result(_resolved_result()).get("status", ""), "APPLIED")
	var visible_before: Dictionary = screen.view_state().duplicate(true)
	var invalid := _resolved_result()
	invalid["durability_consequence"].erase("after_current_durability")
	assert_eq(screen.configure_resolved_result(invalid), {"status": "BLOCKED", "reason": "INVALID_DURABILITY_CONSEQUENCE"})
	assert_eq(screen.view_state(), visible_before, "invalid input must not replace the last confirmed result")


func test_app_only_presents_a_saved_result_from_customer_state() -> void:
	var app = APP_SCENE.instantiate()
	add_child_autofree(app)
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	envelope.active_run["resolved_events"] = {EVENT_ID: _resolved_result()}
	assert_true(app.configure_campaign(envelope, ResourcesScript.new()))
	assert_true(app.has_method("present_resolved_customer_result"), "app must expose the customer result presentation boundary")
	if not app.has_method("present_resolved_customer_result"):
		return
	assert_eq(app.present_resolved_customer_result(EVENT_ID), app.INVALID_TRANSITION)
	assert_eq(app.current_state, "WORKSHOP")
	app.current_state = "CUSTOMER"
	assert_eq(app.present_resolved_customer_result(EVENT_ID), app.OK_TRANSITION)
	assert_eq(app.current_state, "RESULT")
	assert_false(app.get_node("ScreenHost/WorkshopScreen").visible)
	assert_true(app.get_node("ScreenHost/CustomerResultScreen").visible)
	assert_eq(app.get_node("ScreenHost/CustomerResultScreen").view_state().get("item_uid", ""), ITEM_UID)
