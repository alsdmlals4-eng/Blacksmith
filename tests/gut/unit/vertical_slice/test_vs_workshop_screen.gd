# 작업대 화면이 현재 정본 내구도·수리 상태를 표시하고 실행하는지 검증한다.
extends "res://addons/gut/test.gd"

const SCREEN_PATH := "res://scripts/vertical_slice/ui/vs_workshop_screen.gd"
const SCREEN_SCENE := preload("res://scenes/vertical_slice/screens/vs_workshop_screen.tscn")
const ItemScript := preload("res://scripts/vertical_slice/domain/vs_item.gd")
const ResourcesScript := preload("res://scripts/economy/workshop_resources.gd")
const RunInitializerScript := preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const EnhancementActionServiceScript := preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const EquipmentCatalogScript := preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
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
	var next_save_error: Error = OK

	func save_envelope(envelope) -> Error:
		if next_save_error != OK:
			return next_save_error
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


func _precision_envelope(level: int = 9, tag_entries: Array = [], used_milestones: Array = [], backfill_pending: bool = false, weight_point: int = 2):
	var envelope = _enhancement_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	item.enhancement_level = level
	item.highest_checkpoint = 90 if level >= 90 else 60 if level >= 60 else 30 if level >= 30 else 10 if level >= 10 else 0
	item.catalyst_affix = {
		"schema_version": 1,
		"tag_entries": tag_entries.duplicate(true),
		"initial_tag_backfill_pending": backfill_pending,
		"unreadable_legacy_affix": "",
	}
	item.used_precision_milestones.clear()
	for milestone in used_milestones:
		item.used_precision_milestones.append(int(milestone))
	item.raw_role_stat = 12
	item.weight_point = weight_point
	return envelope


func _resources(gold: int = 20000, common_materials: int = 30, heart_of_flame: int = 64, earth_crystal: int = 64):
	return ResourcesScript.new(gold, {
		"common_reinforcement_material": common_materials,
		"heart_of_flame": heart_of_flame,
		"earth_crystal": earth_crystal,
	})


func _option_index_for_metadata(option: OptionButton, value: String) -> int:
	for index in range(option.item_count):
		if str(option.get_item_metadata(index)) == value:
			return index
	return -1


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


func test_workshop_exposes_one_native_handoff_action_only_for_an_eligible_level_ten_item() -> void:
	var envelope = _enhancement_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, _resources(), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)

	assert_true(screen.has_signal("handoff_requested"), "the app needs a native player-action signal instead of a hidden router entry")
	assert_true(bool(screen.view_state().get("handoff_allowed", false)))
	var handoff_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/HandoffButton") as Button
	assert_not_null(handoff_button)
	if handoff_button == null:
		return
	assert_true(handoff_button.visible)
	assert_false(handoff_button.disabled)
	assert_gte(handoff_button.custom_minimum_size.y, 48.0)
	assert_true(handoff_button.text.contains("인계"))
	assert_true(screen.has_signal("chronicle_requested"), "the same UID needs a visible route to its existing chronicle facts")
	var chronicle_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/ChronicleButton") as Button
	assert_not_null(chronicle_button)
	if chronicle_button != null:
		assert_true(chronicle_button.visible)
		assert_false(chronicle_button.disabled)
		assert_gte(chronicle_button.custom_minimum_size.y, 48.0)

	item.enhancement_level = 9
	screen.refresh_after_enhancement()
	assert_false(bool(screen.view_state().get("handoff_allowed", true)))
	assert_false(handoff_button.visible)
	if chronicle_button != null:
		assert_true(chronicle_button.visible)

	item.enhancement_level = 10
	item.current_durability = 0
	item.physical_state = "DESTROYED"
	screen.refresh_after_enhancement()
	assert_false(bool(screen.view_state().get("handoff_allowed", true)))
	assert_false(handoff_button.visible)


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


func test_workshop_keeps_precision_as_native_controls_without_a_dedicated_illustrated_background() -> void:
	var envelope = _precision_envelope(9)
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(envelope.get_item(str(envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)
	assert_null(screen.get_node_or_null("PrecisionIllustratedBackground"))
	var add_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button
	assert_not_null(add_button)
	if add_button != null:
		assert_true(add_button.visible)
		assert_gte(add_button.custom_minimum_size.y, 48.0)


func test_precision_gate_keeps_the_actual_next_target_visible_before_a_tag_action_is_selected() -> void:
	var envelope = _precision_envelope(9)
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(envelope.get_item(str(envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)

	var state: Dictionary = screen.view_state()
	assert_false(bool(state.get("enhancement_allowed", true)))
	assert_eq(state.get("enhancement_target_level", 0), 10, "the blocked precision resolver must not erase the player-facing +10 target")
	var quote := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementQuoteLabel") as Label
	assert_not_null(quote)
	if quote != null:
		assert_true(quote.text.contains("+10"), "the visible enhancement quote must keep the actual next target while tag action selection is pending")


func test_workshop_places_tall_precision_content_inside_a_vertical_scroll_container() -> void:
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)

	var scroll := screen.get_node_or_null("WorkshopScroll") as ScrollContainer
	assert_not_null(scroll, "the portrait workshop must scroll instead of centering overflowing content off-screen")
	if scroll == null:
		return
	assert_eq(scroll.horizontal_scroll_mode, ScrollContainer.SCROLL_MODE_DISABLED)
	assert_eq(scroll.vertical_scroll_mode, ScrollContainer.SCROLL_MODE_AUTO)
	assert_true(scroll.follow_focus)
	assert_eq(scroll.offset_left, 32.0, "the workshop copy needs the approved portrait side breathing room")
	assert_eq(scroll.offset_top, 24.0, "the title must not touch the portrait viewport edge")
	assert_eq(scroll.offset_right, -32.0)
	assert_eq(scroll.offset_bottom, -24.0)
	assert_not_null(scroll.get_node_or_null("WorkshopLayout") as VBoxContainer)


func test_workshop_wraps_portrait_copy_before_it_can_force_horizontal_clipping() -> void:
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	for node_path in [
		"WorkshopScroll/WorkshopLayout/EnhancementQuoteLabel",
		"WorkshopScroll/WorkshopLayout/EnhancementOutcomesLabel",
		"WorkshopScroll/WorkshopLayout/PrecisionActionLabel",
		"WorkshopScroll/WorkshopLayout/PrecisionPreviewLabel",
	]:
		var label := screen.get_node_or_null(node_path) as Label
		assert_not_null(label, node_path)
		if label == null:
			continue
		assert_eq(label.autowrap_mode, TextServer.AUTOWRAP_WORD_SMART, "%s must wrap within the portrait workshop width" % node_path)
		assert_eq(label.size_flags_horizontal, Control.SIZE_EXPAND_FILL, "%s must fill the available portrait width instead of growing beyond it" % node_path)


func test_workshop_displays_the_matching_workpiece_image_for_each_durability_state() -> void:
	var item = _item(5, 5)
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	var hero := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/WorkpieceDurabilityHero") as TextureRect
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
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/WorkshopTitle").text, "첫 작품 · 철검")
	assert_false(screen.get_node("WorkshopBackground").visible)
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityTitleLabel").text, "작품 상태")
	assert_gte(screen.get_node("WorkshopScroll/WorkshopLayout/RepairButton").custom_minimum_size.y, 64.0)


func test_workshop_title_uses_the_selected_equipment_catalog_identity() -> void:
	var selected_item = _item(5, 5)
	selected_item.equipment_group = "HELMET"
	selected_item.role_profile = "ARMOR_HEAD_DEFENSE"
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(selected_item, ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/WorkshopTitle").text, "첫 작품 · 철투구")


func test_workshop_binds_the_selected_equipment_identity_separately_from_the_durability_state_hero() -> void:
	for entry in EquipmentCatalogScript.all():
		var selected_item = _item(5, 5)
		selected_item.equipment_group = str(entry.get("equipment_group", ""))
		selected_item.role_profile = str(entry.get("role_profile", ""))
		var screen = SCREEN_SCENE.instantiate()
		add_child_autofree(screen)
		screen.configure_context(selected_item, ResourcesScript.new(100, {"common_reinforcement_material": 1}))
		var identity_hero := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/EquipmentIdentityHero") as TextureRect
		assert_not_null(identity_hero, str(entry.get("equipment_id", "")))
		if identity_hero == null:
			continue
		var image_path := str(entry.get("image_path", ""))
		assert_true(ResourceLoader.exists(image_path), image_path)
		assert_not_null(identity_hero.texture, str(entry.get("equipment_id", "")))
		assert_eq(identity_hero.texture.resource_path, image_path, str(entry.get("equipment_id", "")))
		assert_eq(identity_hero.texture.get_width(), 512, str(entry.get("equipment_id", "")))
		assert_eq(identity_hero.texture.get_height(), 512, str(entry.get("equipment_id", "")))
		assert_eq(identity_hero.mouse_filter, Control.MOUSE_FILTER_IGNORE, str(entry.get("equipment_id", "")))
		assert_eq(identity_hero.stretch_mode, TextureRect.STRETCH_KEEP_ASPECT_CENTERED, str(entry.get("equipment_id", "")))
		assert_ne(identity_hero, screen.get_node_or_null("WorkshopScroll/WorkshopLayout/WorkpieceDurabilityHero"), "identity and durability visuals must remain distinct")


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
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityStateLabel").text, "상태: 정상")
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/RepairQuoteLabel").text, "수리 불가: 실제 손상 후 수리 가능")


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
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityValueLabel").text, "3 / 5 / 5")
	item.apply_damage_event()
	screen.refresh_after_enhancement()
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/DurabilityValueLabel").text, "2 / 5 / 5")
	assert_true(screen.get_node("WorkshopScroll/WorkshopLayout/RepairButton").disabled == false)


func test_repair_button_uses_randomized_maintenance_path_not_test_rolls() -> void:
	var item = _item()
	var tracking_service = TrackingMaintenanceService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(100, {"common_reinforcement_material": 1}), tracking_service)
	screen._on_repair_pressed()
	assert_eq(tracking_service.random_repair_calls, 1)
	assert_eq(tracking_service.deterministic_repair_calls, 0)
	assert_eq(screen.get_node("WorkshopScroll/WorkshopLayout/RepairMessageLabel").text, "수리 불가: TRACKED_RANDOM_REPAIR")


func test_workshop_displays_next_enhancement_outcomes_and_commits_saved_attempt() -> void:
	var envelope = _enhancement_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var resources = _resources()
	envelope.workshop_resources = resources.snapshot()
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
	assert_true(screen.has_node("WorkshopScroll/WorkshopLayout/EnhancementButton"))
	assert_gte(screen.get_node("WorkshopScroll/WorkshopLayout/EnhancementButton").custom_minimum_size.y, 64.0)
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 99.0})
	assert_eq(result.get("outcome", ""), "SUCCESS")
	assert_not_null(save_service.saved_envelope)
	assert_eq(screen.view_state().get("enhancement_target_level", -1), 13)
	assert_eq(resources.snapshot(), save_service.saved_envelope.resource_snapshot())


func test_precision_plus_9_requires_add_action_before_a_valid_dictionary_selection() -> void:
	var envelope = _precision_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, _resources(), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)
	var initial: Dictionary = screen.view_state()
	assert_eq(initial.get("precision_target", ""), "+9 → +10")
	assert_eq(initial.get("precision_mode", ""), "ATTEMPT")
	assert_eq(initial.get("precision_action", ""), "")
	assert_false(bool(initial.get("enhancement_allowed", true)))
	var add_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button
	var upgrade_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button
	var lineage := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	assert_not_null(add_button)
	assert_not_null(upgrade_button)
	assert_not_null(lineage)
	assert_not_null(method)
	if add_button == null or upgrade_button == null or lineage == null or method == null:
		return
	assert_true(add_button.visible)
	assert_false(upgrade_button.visible)
	assert_false(lineage.visible)
	assert_false(method.visible)
	screen._on_precision_add_pressed()
	assert_eq(screen.view_state().get("precision_action", ""), "ADD_TAG")
	assert_true(lineage.visible)
	assert_true(method.visible)
	screen.set_precision_selection({
		"action": "ADD_TAG",
		"catalyst_id": "HEART_OF_FLAME",
		"method_id": "EDGE_REINFORCEMENT",
	})
	var selected: Dictionary = screen.view_state()
	assert_true(bool(selected.get("enhancement_allowed", false)))
	assert_eq(selected.get("precision_action", ""), "ADD_TAG")
	assert_true(str(selected.get("precision_preview_summary", "")).contains("불의 심장 · 예리함"))
	assert_true(str(selected.get("precision_preview_summary", "")).contains("불의 심장 1개 소모"))
	assert_true(str(selected.get("precision_catalyst_stock_summary", "")).contains("불의 심장 64개"))
	assert_false((screen.get_node("WorkshopScroll/WorkshopLayout/EnhancementButton") as Button).disabled)


func test_precision_shortage_is_explained_before_the_attempt_button_can_run() -> void:
	var envelope = _precision_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var resources = _resources(20000, 30, 0, 64)
	envelope.workshop_resources = resources.snapshot()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, resources, null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)
	screen.set_precision_selection({
		"action": "ADD_TAG",
		"catalyst_id": "HEART_OF_FLAME",
		"method_id": "EDGE_REINFORCEMENT",
	})
	var state: Dictionary = screen.view_state()
	assert_false(bool(state.get("enhancement_allowed", true)))
	assert_eq(str(state.get("enhancement_reason", "")), "INSUFFICIENT_PRECISION_CATALYST")
	assert_true(str(state.get("precision_preview_summary", "")).contains("보유 0개"))
	assert_true((screen.get_node("WorkshopScroll/WorkshopLayout/EnhancementButton") as Button).disabled)


func test_precision_add_option_signals_preserve_both_ids_in_either_selection_order() -> void:
	var lineage_then_method_envelope = _precision_envelope()
	var lineage_then_method_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(lineage_then_method_screen)
	lineage_then_method_screen.configure_context(lineage_then_method_envelope.get_item(str(lineage_then_method_envelope.active_run["selected_item_uid"])), _resources(), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), lineage_then_method_envelope)
	var lineage_option := lineage_then_method_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method_option := lineage_then_method_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	assert_not_null(lineage_option)
	assert_not_null(method_option)
	if lineage_option == null or method_option == null:
		return
	lineage_then_method_screen._on_precision_add_pressed()
	var ember_lineage_index := _option_index_for_metadata(lineage_option, "HEART_OF_FLAME")
	assert_gte(ember_lineage_index, 1)
	if ember_lineage_index < 1:
		return
	lineage_option.select(ember_lineage_index)
	lineage_option.item_selected.emit(ember_lineage_index)
	var edge_method_index := _option_index_for_metadata(method_option, "EDGE_REINFORCEMENT")
	assert_gte(edge_method_index, 1)
	if edge_method_index < 1:
		return
	method_option.select(edge_method_index)
	method_option.item_selected.emit(edge_method_index)
	var lineage_then_method_state: Dictionary = lineage_then_method_screen.view_state()
	assert_eq(lineage_then_method_state.get("precision_action", ""), "ADD_TAG")
	assert_eq(lineage_then_method_screen._precision_selection_data.get("catalyst_id", ""), "HEART_OF_FLAME")
	assert_eq(lineage_then_method_screen._precision_selection_data.get("method_id", ""), "EDGE_REINFORCEMENT")
	assert_true(bool(lineage_then_method_state.get("enhancement_allowed", false)))

	var method_then_lineage_envelope = _precision_envelope()
	var method_then_lineage_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(method_then_lineage_screen)
	method_then_lineage_screen.configure_context(method_then_lineage_envelope.get_item(str(method_then_lineage_envelope.active_run["selected_item_uid"])), _resources(), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), method_then_lineage_envelope)
	var reverse_lineage_option := method_then_lineage_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	var reverse_method_option := method_then_lineage_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	assert_not_null(reverse_lineage_option)
	assert_not_null(reverse_method_option)
	if reverse_lineage_option == null or reverse_method_option == null:
		return
	method_then_lineage_screen._on_precision_add_pressed()
	var reverse_edge_method_index := _option_index_for_metadata(reverse_method_option, "EDGE_REINFORCEMENT")
	assert_gte(reverse_edge_method_index, 1)
	if reverse_edge_method_index < 1:
		return
	reverse_method_option.select(reverse_edge_method_index)
	reverse_method_option.item_selected.emit(reverse_edge_method_index)
	var reverse_ember_lineage_index := _option_index_for_metadata(reverse_lineage_option, "HEART_OF_FLAME")
	assert_gte(reverse_ember_lineage_index, 1)
	if reverse_ember_lineage_index < 1:
		return
	reverse_lineage_option.select(reverse_ember_lineage_index)
	reverse_lineage_option.item_selected.emit(reverse_ember_lineage_index)
	var method_then_lineage_state: Dictionary = method_then_lineage_screen.view_state()
	assert_eq(method_then_lineage_state.get("precision_action", ""), "ADD_TAG")
	assert_eq(method_then_lineage_screen._precision_selection_data.get("catalyst_id", ""), "HEART_OF_FLAME")
	assert_eq(method_then_lineage_screen._precision_selection_data.get("method_id", ""), "EDGE_REINFORCEMENT")
	assert_true(bool(method_then_lineage_state.get("enhancement_allowed", false)))


func test_precision_plus_19_exposes_both_actions_and_allows_tag_upgrade_selection() -> void:
	var envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, _resources(), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)
	var initial: Dictionary = screen.view_state()
	assert_eq(initial.get("precision_target", ""), "+19 → +20")
	var add_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button
	var upgrade_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button
	var tag_option := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTagOption") as OptionButton
	assert_not_null(add_button)
	assert_not_null(upgrade_button)
	assert_not_null(tag_option)
	if add_button == null or upgrade_button == null or tag_option == null:
		return
	assert_true(add_button.visible)
	assert_true(upgrade_button.visible)
	assert_false(tag_option.visible)
	screen._on_precision_upgrade_pressed()
	assert_true(tag_option.visible)
	screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
	var selected: Dictionary = screen.view_state()
	assert_eq(selected.get("precision_action", ""), "UPGRADE_TAG")
	assert_true(bool(selected.get("enhancement_allowed", false)))
	assert_true(str(selected.get("precision_preview_summary", "")).contains("I → II"))
	assert_false(str(tag_option.get_item_text(1)).contains("TAG_"))


func test_precision_add_sources_keep_only_resolver_valid_pairs_and_localize_rejected_pairs() -> void:
	var envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(envelope.get_item(str(envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)
	var lineage_option := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method_option := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	assert_not_null(lineage_option)
	assert_not_null(method_option)
	if lineage_option == null or method_option == null:
		return
	screen._on_precision_add_pressed()
	for index in range(lineage_option.item_count):
		if str(lineage_option.get_item_metadata(index)) == "HEART_OF_FLAME":
			lineage_option.select(index)
			screen._on_precision_catalyst_selected(index)
			break
	assert_eq(method_option.item_count, 2)
	assert_eq(method_option.get_item_text(1), "경량 담금")
	screen.set_precision_selection({
		"action": "ADD_TAG",
		"catalyst_id": "HEART_OF_FLAME",
		"method_id": "EDGE_REINFORCEMENT",
	})
	var invalid_state: Dictionary = screen.view_state()
	assert_false(bool(invalid_state.get("enhancement_allowed", true)))
	assert_eq(invalid_state.get("precision_preview_summary", ""), "이미 선택된 정밀 태그입니다")
	assert_false(str(invalid_state.get("precision_preview_summary", "")).contains("DUPLICATE_PRECISION_TAG"))


func test_precision_candidate_filters_enforce_tag_cap_stage_cap_and_zero_weight_light_path() -> void:
	var three_tag_entries := [
		{"tag_id": "TAG_EMBER_EDGE", "stage": 1, "created_milestone": 10, "last_advanced_milestone": 10},
		{"tag_id": "TAG_EMBER_LIGHT", "stage": 1, "created_milestone": 20, "last_advanced_milestone": 20},
		{"tag_id": "TAG_ANVIL_EDGE", "stage": 1, "created_milestone": 30, "last_advanced_milestone": 30},
	]
	var capped_envelope = _precision_envelope(39, three_tag_entries, [10, 20, 30])
	var capped_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(capped_screen)
	capped_screen.configure_context(capped_envelope.get_item(str(capped_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), capped_envelope)
	var capped_add := capped_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button
	assert_not_null(capped_add)
	if capped_add == null:
		return
	assert_false(capped_add.visible)

	var mastered_envelope = _precision_envelope(49, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 4,
		"created_milestone": 10,
		"last_advanced_milestone": 40,
	}], [10, 20, 30, 40])
	var mastered_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(mastered_screen)
	mastered_screen.configure_context(mastered_envelope.get_item(str(mastered_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), mastered_envelope)
	var mastered_upgrade := mastered_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button
	assert_not_null(mastered_upgrade)
	if mastered_upgrade != null:
		assert_false(mastered_upgrade.visible)

	var zero_weight_envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10], false, 0)
	var zero_weight_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(zero_weight_screen)
	zero_weight_screen.configure_context(zero_weight_envelope.get_item(str(zero_weight_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), zero_weight_envelope)
	zero_weight_screen.set_precision_selection({
		"action": "ADD_TAG",
		"catalyst_id": "EARTH_CRYSTAL",
		"method_id": "LIGHTWEIGHTING",
	})
	var zero_weight_state: Dictionary = zero_weight_screen.view_state()
	assert_false(bool(zero_weight_state.get("enhancement_allowed", true)))
	for candidate in zero_weight_state.get("precision_candidates", []):
		assert_ne(str(candidate.get("method_display_name_ko", "")), "경량 담금")


func test_precision_controls_are_hidden_for_ordinary_targets_and_actionable_nodes_are_48dp() -> void:
	var ordinary_envelope = _enhancement_envelope()
	var ordinary_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(ordinary_screen)
	ordinary_screen.configure_context(ordinary_envelope.get_item(str(ordinary_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), ordinary_envelope)
	var ordinary_state: Dictionary = ordinary_screen.view_state()
	assert_eq(ordinary_state.get("precision_target", ""), "")
	assert_false(bool(ordinary_state.get("precision_visible", true)))
	for node_name in ["PrecisionActionAddButton", "PrecisionActionUpgradeButton", "PrecisionTagOption", "PrecisionLineageOption", "PrecisionMethodOption", "PrecisionPreviewLabel", "PrecisionBackfillButton"]:
		var control := ordinary_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/%s" % node_name) as Control
		assert_not_null(control)
		if control != null:
			assert_false(control.visible)

	var precision_envelope = _precision_envelope()
	var precision_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(precision_screen)
	precision_screen.configure_context(precision_envelope.get_item(str(precision_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), precision_envelope)
	for node_name in ["PrecisionActionAddButton", "PrecisionActionUpgradeButton", "PrecisionTagOption", "PrecisionLineageOption", "PrecisionMethodOption", "PrecisionBackfillButton"]:
		var control := precision_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/%s" % node_name) as Control
		assert_not_null(control)
		if control != null:
			assert_gte(control.custom_minimum_size.y, 48.0)


func test_saved_precision_hold_clears_attempt_selection_without_adopting_a_stage() -> void:
	var envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var save_service := FakeSaveService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var resources = _resources()
	envelope.workshop_resources = resources.snapshot()
	screen.configure_context(item, resources, null, EnhancementActionServiceScript.new(), save_service, envelope)
	var upgrade_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button
	assert_not_null(upgrade_button)
	if upgrade_button == null:
		return
	screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 99.0, "damage_roll_percent": 99.0})
	assert_eq(result.get("outcome", ""), "FAILED_HOLD")
	assert_null(screen.get_node_or_null("PrecisionIllustratedBackground"), "native Precision UI must not create a dedicated illustration after a saved hold")
	assert_eq(save_service.saved_envelope.get_item(item.uid).catalyst_tag_entries()[0].get("stage", 0), 1)
	assert_eq(screen.view_state().get("precision_action", ""), "")
	assert_eq(screen.view_state().get("precision_tag_entries", [])[0].get("stage_roman", ""), "I")


func test_saved_precision_success_rebinds_tag_collection_and_save_failure_retains_the_staged_selection() -> void:
	var success_envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	var success_item = success_envelope.get_item(str(success_envelope.active_run["selected_item_uid"]))
	var success_save := FakeSaveService.new()
	var success_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(success_screen)
	var success_resources = _resources()
	success_envelope.workshop_resources = success_resources.snapshot()
	success_screen.configure_context(success_item, success_resources, null, EnhancementActionServiceScript.new(), success_save, success_envelope)
	var success_upgrade := success_screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button
	assert_not_null(success_upgrade)
	if success_upgrade == null:
		return
	success_screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
	assert_eq(success_screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 99.0}).get("outcome", ""), "SUCCESS")
	assert_null(success_screen.get_node_or_null("PrecisionIllustratedBackground"), "native Precision UI must not create a dedicated illustration after a saved success")
	assert_eq(success_screen.view_state().get("precision_tag_entries", [])[0].get("stage_roman", ""), "II")
	assert_eq(success_save.saved_envelope.get_item(success_item.uid).catalyst_tag_entries()[0].get("stage", 0), 2)

	var failed_envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	var failed_save := FakeSaveService.new()
	failed_save.next_save_error = ERR_CANT_CREATE
	var failed_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(failed_screen)
	var failed_resources = _resources()
	failed_envelope.workshop_resources = failed_resources.snapshot()
	failed_screen.configure_context(failed_envelope.get_item(str(failed_envelope.active_run["selected_item_uid"])), failed_resources, null, EnhancementActionServiceScript.new(), failed_save, failed_envelope)
	failed_screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
	var failed_result: Dictionary = failed_screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 99.0})
	assert_eq(failed_result.get("reason", ""), "SAVE_FAILED:%d" % ERR_CANT_CREATE)
	assert_eq(failed_screen.view_state().get("precision_tag_entries", [])[0].get("stage_roman", ""), "I")
	assert_eq(failed_screen.view_state().get("precision_action", ""), "UPGRADE_TAG")


func test_pending_backfill_is_distinct_zero_cost_add_path_without_placeholder_text() -> void:
	var envelope = _precision_envelope(10, [], [], true)
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var save_service := FakeSaveService.new()
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), save_service, envelope)
	var initial: Dictionary = screen.view_state()
	assert_eq(initial.get("precision_mode", ""), "BACKFILL")
	assert_eq(initial.get("precision_target", ""), "+9 → +10")
	assert_false(bool(initial.get("enhancement_allowed", true)))
	var backfill_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionBackfillButton") as Button
	var add_button := screen.get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button
	assert_not_null(backfill_button)
	assert_not_null(add_button)
	if backfill_button == null or add_button == null:
		return
	assert_true(backfill_button.visible)
	assert_true(backfill_button.text.contains("비용 없음"))
	screen._on_precision_add_pressed()
	screen.set_precision_selection({
		"action": "ADD_TAG",
		"catalyst_id": "EARTH_CRYSTAL",
		"method_id": "LIGHTWEIGHTING",
	})
	assert_false(backfill_button.disabled)
	var result: Dictionary = screen.request_precision_backfill()
	assert_eq(result.get("outcome", ""), "APPLIED")
	assert_eq(result.get("gold_cost", -1), 0)
	assert_eq(result.get("reinforcement_units", -1), 0)
	assert_eq(save_service.saved_envelope.get_item(item.uid).catalyst_tag_entries()[0].get("tag_id", ""), "TAG_ANVIL_LIGHT")
	assert_false(str(screen.get_node("WorkshopScroll/WorkshopLayout/PrecisionPreviewLabel").text).contains("PRECISION_KEYWORD_PENDING_CONTENT"))


func test_precision_failed_damage_keeps_the_workshop_fallback_without_a_dedicated_art_layer() -> void:
	var envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var save_service := FakeSaveService.new()
	var resources = _resources()
	envelope.workshop_resources = resources.snapshot()
	screen.configure_context(envelope.get_item(str(envelope.active_run["selected_item_uid"])), resources, null, EnhancementActionServiceScript.new(), save_service, envelope)
	var fallback := screen.get_node_or_null("WorkshopIllustratedBackground") as TextureRect
	assert_not_null(fallback)
	if fallback == null:
		return
	assert_null(screen.get_node_or_null("PrecisionIllustratedBackground"))
	screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 99.0, "damage_roll_percent": 0.0})
	assert_eq(result.get("outcome", ""), "FAILED_DAMAGE", "the exact saved failure result must exercise the post-result visual boundary")
	assert_not_null(save_service.saved_envelope, "FAILED_DAMAGE must be persisted while native Precision controls remain factual")
	assert_null(screen.get_node_or_null("PrecisionIllustratedBackground"))
	assert_true(fallback.visible, "the ordinary Workshop illustration remains the fallback behind native result controls")


func test_fresh_precision_context_exposes_native_selection_without_a_dedicated_art_layer() -> void:
	var first_envelope = _precision_envelope(9)
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var first_save := FakeSaveService.new()
	var first_resources = _resources()
	first_envelope.workshop_resources = first_resources.snapshot()
	screen.configure_context(first_envelope.get_item(str(first_envelope.active_run["selected_item_uid"])), first_resources, null, EnhancementActionServiceScript.new(), first_save, first_envelope)
	assert_null(screen.get_node_or_null("PrecisionIllustratedBackground"))
	assert_true((screen.get_node("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button).visible, "new +9→+10 context exposes native tag selection")
	screen.set_precision_selection({"action": "ADD_TAG", "catalyst_id": "HEART_OF_FLAME", "method_id": "EDGE_REINFORCEMENT"})
	var resolved: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 99.0})
	assert_eq(resolved.get("outcome", ""), "SUCCESS")
	assert_not_null(first_save.saved_envelope, "the successful +9→+10 result must be persisted before a later context is opened")
	assert_null(screen.get_node_or_null("PrecisionIllustratedBackground"))
	var reopened_envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	screen.configure_context(reopened_envelope.get_item(str(reopened_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 30}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), reopened_envelope)
	assert_null(screen.get_node_or_null("PrecisionIllustratedBackground"))
	assert_true((screen.get_node("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button).visible, "a fresh +19→+20 context exposes native tag-upgrade selection")
