# 작업대 화면이 현재 정본 내구도·수리 상태를 표시하고 실행하는지 검증한다.
extends "res://addons/gut/test.gd"

const SCREEN_PATH := "res://scripts/vertical_slice/ui/vs_workshop_screen.gd"
const SCREEN_SCENE := preload("res://scenes/vertical_slice/screens/vs_workshop_screen.tscn")
const ItemScript := preload("res://scripts/vertical_slice/domain/vs_item.gd")
const ResourcesScript := preload("res://scripts/economy/workshop_resources.gd")
const RunInitializerScript := preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const EnhancementActionServiceScript := preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const WorkshopBackgroundTexture := preload("res://assets/ui/workshop/workshop_enhancement_background_v2.png")
const WorkpieceDurabilityStateAtlasTexture := preload("res://assets/ui/workshop/workpiece_durability_state_atlas_v1.png")


class TrackingMaintenanceService extends RefCounted:
	var random_repair_calls := 0
	var deterministic_repair_calls := 0


	func try_repair(_item, _resources, _calendar = null) -> Dictionary:
		random_repair_calls += 1
		return {"status": "BLOCKED", "reason": "TRACKED_RANDOM_REPAIR"}


	func try_repair_with_rolls(_item, _resources, _rolls: Dictionary) -> Dictionary:
		deterministic_repair_calls += 1
		return {"status": "BLOCKED", "reason": "TRACKED_DETERMINISTIC_REPAIR"}


class FakeSaveService extends RefCounted:
	var saved_envelope = null

	func save_envelope(envelope) -> Error:
		saved_envelope = envelope
		return OK


func _item(current: int = 3, maximum: int = 5):
	var item = ItemScript.new()
	item.uid = "UI-ITEM-001"
	item.primary_material_id = "iron"
	item.enhancement_level = 11
	item.highest_checkpoint = 10
	item.base_max_durability = 5
	item.max_durability = maximum
	item.current_durability = current
	item.repair_job_available = true
	return item


func _enhancement_envelope():
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	var item = _item(5, 5)
	item.uid = "BSI-11223344556677889900aabbccddeeff"
	envelope.items_by_uid[item.uid] = item
	envelope.active_run["selected_item_uid"] = item.uid
	return envelope


func _precision_envelope(level: int = 9, catalyst_affix: String = ""):
	var envelope = _enhancement_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	item.enhancement_level = level
	item.highest_checkpoint = 10 if level >= 10 else 0
	item.catalyst_affix = catalyst_affix
	item.raw_role_stat = 12
	item.weight_point = 2
	return envelope


func test_screen_exposes_current_durability_and_repair_quote() -> void:
	assert_true(ResourceLoader.exists(SCREEN_PATH), "Workshop screen controller must exist")
	if not ResourceLoader.exists(SCREEN_PATH):
		return
	var screen = load(SCREEN_PATH).new()
	screen.configure_context(_item(), ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	var state: Dictionary = screen.view_state()
	assert_eq(state["durability_text"], "3 / 5 / 5")
	assert_eq(state["durability_state"], "MINOR")
	assert_true(state["repair_allowed"])
	assert_eq(state["repair_gold_cost"], 39)
	assert_eq(state["repair_material_units"], 1)
	assert_eq(state.get("repair_quality_summary", ""), "예상 회복: 최상 100% / 표준 75% / 미흡 50%")
	assert_eq(state.get("repair_scar_summary", ""), "MAX 흉터 가능성: 10%")
	assert_eq(state.get("repair_job_summary", ""), "수리하면 다음 실제 손상 전까지 다시 수리할 수 없습니다")


func test_workshop_uses_the_illustrated_background_as_a_noninteractive_runtime_layer() -> void:
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var background := screen.get_node_or_null("WorkshopIllustratedBackground") as TextureRect
	assert_not_null(background)
	if background == null:
		return
	assert_eq(background.texture, WorkshopBackgroundTexture)
	assert_eq(background.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(background.z_index, -1)
	assert_eq(background.expand_mode, TextureRect.EXPAND_IGNORE_SIZE)
	assert_eq(background.stretch_mode, TextureRect.STRETCH_KEEP_ASPECT_COVERED)


func test_workshop_displays_the_matching_workpiece_image_for_each_durability_state() -> void:
	var item = _item(5, 5)
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	var hero := screen.get_node_or_null("WorkshopLayout/WorkpieceDurabilityHero") as TextureRect
	assert_not_null(hero)
	if hero == null:
		return
	assert_true(hero.texture is AtlasTexture)
	var normal_texture := hero.texture as AtlasTexture
	assert_eq(normal_texture.atlas, WorkpieceDurabilityStateAtlasTexture)
	assert_eq(normal_texture.region, Rect2(0, 0, 627, 627))

	item.current_durability = 3
	screen.refresh_after_enhancement()
	assert_eq((hero.texture as AtlasTexture).region, Rect2(627, 0, 627, 627))

	item.current_durability = 2
	screen.refresh_after_enhancement()
	assert_eq((hero.texture as AtlasTexture).region, Rect2(0, 627, 627, 627))

	item.current_durability = 0
	screen.refresh_after_enhancement()
	assert_eq((hero.texture as AtlasTexture).region, Rect2(627, 627, 627, 627))


func test_workshop_scene_keeps_the_first_item_hierarchy_and_large_repair_action() -> void:
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	assert_eq(screen.get_node("WorkshopLayout/WorkshopTitle").text, "첫 작품 · 철검")
	assert_false(screen.get_node("WorkshopBackground").visible)
	assert_eq(screen.get_node("WorkshopLayout/DurabilityTitleLabel").text, "작품 상태")
	assert_gte(screen.get_node("WorkshopLayout/RepairButton").custom_minimum_size.y, 64.0)


func test_workshop_uses_a_readability_veil_over_the_illustrated_background() -> void:
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var veil := screen.get_node_or_null("WorkshopReadabilityVeil") as ColorRect
	assert_not_null(veil, "bright illustrated background needs a dedicated readable text layer")
	if veil == null:
		return
	assert_eq(veil.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(veil.z_index, -1)
	assert_gt(veil.color.a, 0.0)


func test_workshop_localizes_durability_state_and_repair_block_reason() -> void:
	var item = _item(5, 5)
	item.repair_job_available = false
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	assert_eq(screen.get_node("WorkshopLayout/DurabilityStateLabel").text, "상태: 정상")
	assert_eq(screen.get_node("WorkshopLayout/RepairQuoteLabel").text, "수리 불가: 실제 손상 후 수리 가능")


func test_screen_repair_refreshes_the_bound_item_and_disables_repeat_repair() -> void:
	if not ResourceLoader.exists(SCREEN_PATH):
		fail_test("Workshop screen controller must exist")
		return
	var item = _item()
	var resources = ResourcesScript.new(100, {"common_reinforcement_material": 1})
	var screen = load(SCREEN_PATH).new()
	screen.configure_context(item, resources)
	var result: Dictionary = screen.request_repair_with_rolls({"quality_roll_percent": 0.0, "scar_roll_percent": 99.0})
	assert_eq(result["status"], "APPLIED")
	assert_eq(item.current_durability, 5)
	assert_false(screen.view_state()["repair_allowed"])
	assert_eq(screen.view_state()["repair_reason"], "REPAIR_JOB_UNAVAILABLE")
	screen.free()


func test_screen_hides_scar_risk_when_guard_must_skip_the_scar() -> void:
	var screen = load(SCREEN_PATH).new()
	screen.configure_context(_item(4, 5), ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	assert_eq(screen.view_state()["repair_scar_summary"], "MAX 흉터 가능성: 0%")
	screen.free()


func test_screen_refreshes_visible_durability_after_an_enhancement_damage_event() -> void:
	var item = _item()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	assert_eq(screen.get_node("WorkshopLayout/DurabilityValueLabel").text, "3 / 5 / 5")
	item.apply_damage_event()
	screen.refresh_after_enhancement()
	assert_eq(screen.get_node("WorkshopLayout/DurabilityValueLabel").text, "2 / 5 / 5")
	assert_true(screen.get_node("WorkshopLayout/RepairButton").disabled == false)


func test_repair_button_uses_randomized_maintenance_path_not_test_rolls() -> void:
	var item = _item()
	var tracking_service = TrackingMaintenanceService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}), tracking_service)
	screen._on_repair_pressed()
	assert_eq(tracking_service.random_repair_calls, 1)
	assert_eq(tracking_service.deterministic_repair_calls, 0)
	assert_eq(screen.get_node("WorkshopLayout/RepairMessageLabel").text, "수리 불가: TRACKED_RANDOM_REPAIR")


func test_workshop_displays_next_enhancement_outcomes_and_commits_saved_attempt() -> void:
	var envelope = _enhancement_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var resources = ResourcesScript.new(20000, {"common_reinforcement_material": 10})
	var save_service := FakeSaveService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(
		item,
		resources,
		null,
		EnhancementActionServiceScript.new(),
		save_service,
		envelope
	)
	var state: Dictionary = screen.view_state()
	assert_true(state.get("enhancement_allowed", false))
	assert_eq(state.get("enhancement_target_level", -1), 12)
	assert_true(str(state.get("enhancement_outcomes_summary", "")).contains("성공"))
	assert_true(str(state.get("enhancement_cost_summary", "")).contains("Gold"))
	assert_true(screen.has_node("WorkshopLayout/EnhancementButton"))
	assert_gte(screen.get_node("WorkshopLayout/EnhancementButton").custom_minimum_size.y, 64.0)
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 99.0})
	assert_eq(result.get("outcome", ""), "SUCCESS")
	assert_not_null(save_service.saved_envelope)
	assert_eq(screen.view_state().get("enhancement_target_level", -1), 13)
	assert_eq(resources.snapshot(), save_service.saved_envelope.resource_snapshot())


func test_workshop_requires_two_korean_precision_choices_and_previews_the_resolved_tag() -> void:
	var envelope = _precision_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var resources = ResourcesScript.new(20000, {"common_reinforcement_material": 10})
	var save_service := FakeSaveService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, resources, null, EnhancementActionServiceScript.new(), save_service, envelope)
	var initial: Dictionary = screen.view_state()
	assert_true(bool(initial.get("precision_visible", false)))
	assert_eq(initial.get("precision_mode", ""), "ATTEMPT")
	assert_false(bool(initial.get("enhancement_allowed", true)))
	assert_eq(initial.get("enhancement_reason", ""), "MISSING_CATALYST_LINEAGE")
	var lineage := screen.get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method := screen.get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
	assert_not_null(lineage)
	assert_not_null(method)
	assert_true(screen.get_node("WorkshopLayout/EnhancementButton").disabled)
	if lineage == null or method == null:
		return
	assert_eq(lineage.get_item_text(1), "불씨 계보")
	assert_eq(method.get_item_text(1), "날 세우기")
	screen.set_precision_selection("EMBER_LINEAGE", "EDGE_REINFORCEMENT")
	var selected: Dictionary = screen.view_state()
	assert_true(bool(selected.get("enhancement_allowed", false)))
	assert_eq(selected.get("precision_tag_id", ""), "TAG_EMBER_EDGE")
	assert_true(str(selected.get("precision_preview_summary", "")).contains("불씨의 예리함"))
	assert_true(str(selected.get("precision_preview_summary", "")).contains("12 → 15"))
	assert_true(str(selected.get("precision_preview_summary", "")).contains("내구도 변화 없음"))
	assert_false(screen.get_node("WorkshopLayout/EnhancementButton").disabled)
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 0.0})
	assert_eq(result.get("outcome", ""), "SUCCESS")
	assert_eq(save_service.saved_envelope.get_item(item.uid).catalyst_affix, "TAG_EMBER_EDGE")
	assert_eq(lineage.get_selected(), 0, "attempt-local selection must clear after the result")
	assert_eq(method.get_selected(), 0, "attempt-local selection must clear after the result")


func test_workshop_clears_precision_selection_after_hold_without_writing_a_tag() -> void:
	var envelope = _precision_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var resources = ResourcesScript.new(20000, {"common_reinforcement_material": 10})
	var save_service := FakeSaveService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, resources, null, EnhancementActionServiceScript.new(), save_service, envelope)
	screen.set_precision_selection("ANVIL_LINEAGE", "LIGHTWEIGHTING")
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 99.0, "damage_roll_percent": 0.0})
	assert_eq(result.get("outcome", ""), "FAILED_HOLD")
	assert_eq(save_service.saved_envelope.get_item(item.uid).enhancement_level, 9)
	assert_true(save_service.saved_envelope.get_item(item.uid).catalyst_affix.is_empty())
	assert_eq((screen.get_node("WorkshopLayout/PrecisionLineageOption") as OptionButton).get_selected(), 0)
	assert_eq((screen.get_node("WorkshopLayout/PrecisionMethodOption") as OptionButton).get_selected(), 0)


func test_workshop_exposes_one_zero_cost_placeholder_correction_without_showing_the_placeholder() -> void:
	var envelope = _precision_envelope(10, "PRECISION_KEYWORD_PENDING_CONTENT")
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var resources = ResourcesScript.new(20000, {"common_reinforcement_material": 10})
	var save_service := FakeSaveService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, resources, null, EnhancementActionServiceScript.new(), save_service, envelope)
	var initial: Dictionary = screen.view_state()
	assert_eq(initial.get("precision_mode", ""), "BACKFILL")
	assert_false(bool(initial.get("enhancement_allowed", true)))
	assert_eq(initial.get("enhancement_reason", ""), "PRECISION_PLACEHOLDER_REQUIRES_BACKFILL")
	var lineage := screen.get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method := screen.get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
	var backfill_button := screen.get_node_or_null("WorkshopLayout/PrecisionBackfillButton") as Button
	assert_not_null(backfill_button)
	if lineage == null or method == null or backfill_button == null:
		return
	assert_true(backfill_button.visible)
	assert_true(backfill_button.disabled)
	screen.set_precision_selection("ANVIL_LINEAGE", "LIGHTWEIGHTING")
	assert_false(backfill_button.disabled)
	var result: Dictionary = screen.request_precision_backfill()
	assert_eq(result.get("outcome", ""), "APPLIED")
	assert_eq(result.get("gold_cost", -1), 0)
	assert_eq(result.get("reinforcement_units", -1), 0)
	assert_eq(save_service.saved_envelope.get_item(item.uid).catalyst_affix, "TAG_ANVIL_LIGHT")
	assert_false(str(screen.get_node("WorkshopLayout/PrecisionPreviewLabel").text).contains("PRECISION_KEYWORD_PENDING_CONTENT"))
