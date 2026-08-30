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
const APPROVED_PRECISION_BACKGROUND_PATH := "res://assets/ui/workshop/precision_tag_workshop_background_v1.png"


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


func test_workshop_shows_the_approved_precision_illustration_only_for_an_active_precision_target() -> void:
	assert_true(ResourceLoader.exists(APPROVED_PRECISION_BACKGROUND_PATH), "approved Precision illustration must be tracked before the recurring state can consume it")
	if not ResourceLoader.exists(APPROVED_PRECISION_BACKGROUND_PATH):
		return
	var ordinary = SCREEN_SCENE.instantiate()
	add_child_autofree(ordinary)
	ordinary.configure_context(_item(), ResourcesScript.new(100, {"common_reinforcement_material": 1}))
	var ordinary_precision := ordinary.get_node_or_null("PrecisionIllustratedBackground") as TextureRect
	assert_not_null(ordinary_precision, "dynamic Precision illustration layer must exist without a serialized scene node")
	if ordinary_precision == null:
		return
	assert_false(ordinary_precision.visible, "ordinary workshop state must retain its existing fallback background")
	var precision_envelope = _precision_envelope(9)
	var precision = SCREEN_SCENE.instantiate()
	add_child_autofree(precision)
	precision.configure_context(precision_envelope.get_item(str(precision_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), precision_envelope)
	var precision_background := precision.get_node_or_null("PrecisionIllustratedBackground") as TextureRect
	assert_not_null(precision_background)
	if precision_background == null:
		return
	assert_true(precision_background.visible, "an exact recurring Precision target must expose the approved neutral selection illustration")
	assert_eq(precision_background.texture.resource_path, APPROVED_PRECISION_BACKGROUND_PATH)
	assert_eq(precision_background.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(precision_background.z_index, -1)
	assert_eq(precision_background.expand_mode, TextureRect.EXPAND_IGNORE_SIZE)
	assert_eq(precision_background.stretch_mode, TextureRect.STRETCH_KEEP_ASPECT_COVERED)
	var precision_twenty_envelope = _precision_envelope(19, [{"tag_id": "TAG_EMBER_EDGE", "stage": 1, "created_milestone": 10, "last_advanced_milestone": 10}], [10])
	var precision_twenty = SCREEN_SCENE.instantiate()
	add_child_autofree(precision_twenty)
	precision_twenty.configure_context(precision_twenty_envelope.get_item(str(precision_twenty_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), precision_twenty_envelope)
	assert_true((precision_twenty.get_node("PrecisionIllustratedBackground") as TextureRect).visible, "each newly opened exact recurring target, including +19→+20, may show the neutral selection illustration")


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


func test_precision_plus_9_requires_add_action_before_a_valid_dictionary_selection() -> void:
	var envelope = _precision_envelope()
	var item = envelope.get_item(str(envelope.active_run["selected_item_uid"]))
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	screen.configure_context(item, ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)
	var initial: Dictionary = screen.view_state()
	assert_eq(initial.get("precision_target", ""), "+9 → +10")
	assert_eq(initial.get("precision_mode", ""), "ATTEMPT")
	assert_eq(initial.get("precision_action", ""), "")
	assert_false(bool(initial.get("enhancement_allowed", true)))
	var add_button := screen.get_node_or_null("WorkshopLayout/PrecisionActionAddButton") as Button
	var upgrade_button := screen.get_node_or_null("WorkshopLayout/PrecisionActionUpgradeButton") as Button
	var lineage := screen.get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method := screen.get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
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
		"lineage_id": "EMBER_LINEAGE",
		"method_id": "EDGE_REINFORCEMENT",
	})
	var selected: Dictionary = screen.view_state()
	assert_true(bool(selected.get("enhancement_allowed", false)))
	assert_eq(selected.get("precision_action", ""), "ADD_TAG")
	assert_true(str(selected.get("precision_preview_summary", "")).contains("불씨의 예리함"))
	assert_false((screen.get_node("WorkshopLayout/EnhancementButton") as Button).disabled)


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
	screen.configure_context(item, ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)
	var initial: Dictionary = screen.view_state()
	assert_eq(initial.get("precision_target", ""), "+19 → +20")
	var add_button := screen.get_node_or_null("WorkshopLayout/PrecisionActionAddButton") as Button
	var upgrade_button := screen.get_node_or_null("WorkshopLayout/PrecisionActionUpgradeButton") as Button
	var tag_option := screen.get_node_or_null("WorkshopLayout/PrecisionTagOption") as OptionButton
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
	screen.configure_context(envelope.get_item(str(envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), envelope)
	var lineage_option := screen.get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method_option := screen.get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
	assert_not_null(lineage_option)
	assert_not_null(method_option)
	if lineage_option == null or method_option == null:
		return
	screen._on_precision_add_pressed()
	for index in range(lineage_option.item_count):
		if str(lineage_option.get_item_metadata(index)) == "EMBER_LINEAGE":
			lineage_option.select(index)
			screen._on_precision_lineage_selected(index)
			break
	assert_eq(method_option.item_count, 2)
	assert_eq(method_option.get_item_text(1), "경량 담금")
	screen.set_precision_selection({
		"action": "ADD_TAG",
		"lineage_id": "EMBER_LINEAGE",
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
	capped_screen.configure_context(capped_envelope.get_item(str(capped_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), capped_envelope)
	var capped_add := capped_screen.get_node_or_null("WorkshopLayout/PrecisionActionAddButton") as Button
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
	mastered_screen.configure_context(mastered_envelope.get_item(str(mastered_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), mastered_envelope)
	var mastered_upgrade := mastered_screen.get_node_or_null("WorkshopLayout/PrecisionActionUpgradeButton") as Button
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
	zero_weight_screen.configure_context(zero_weight_envelope.get_item(str(zero_weight_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), zero_weight_envelope)
	zero_weight_screen.set_precision_selection({
		"action": "ADD_TAG",
		"lineage_id": "ANVIL_LINEAGE",
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
	ordinary_screen.configure_context(ordinary_envelope.get_item(str(ordinary_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), ordinary_envelope)
	var ordinary_state: Dictionary = ordinary_screen.view_state()
	assert_eq(ordinary_state.get("precision_target", ""), "")
	assert_false(bool(ordinary_state.get("precision_visible", true)))
	for node_name in ["PrecisionActionAddButton", "PrecisionActionUpgradeButton", "PrecisionTagOption", "PrecisionLineageOption", "PrecisionMethodOption", "PrecisionPreviewLabel", "PrecisionBackfillButton"]:
		var control := ordinary_screen.get_node_or_null("WorkshopLayout/%s" % node_name) as Control
		assert_not_null(control)
		if control != null:
			assert_false(control.visible)

	var precision_envelope = _precision_envelope()
	var precision_screen = SCREEN_SCENE.instantiate()
	add_child_autofree(precision_screen)
	precision_screen.configure_context(precision_envelope.get_item(str(precision_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), precision_envelope)
	for node_name in ["PrecisionActionAddButton", "PrecisionActionUpgradeButton", "PrecisionTagOption", "PrecisionLineageOption", "PrecisionMethodOption", "PrecisionBackfillButton"]:
		var control := precision_screen.get_node_or_null("WorkshopLayout/%s" % node_name) as Control
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
	screen.configure_context(item, ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), save_service, envelope)
	var upgrade_button := screen.get_node_or_null("WorkshopLayout/PrecisionActionUpgradeButton") as Button
	assert_not_null(upgrade_button)
	if upgrade_button == null:
		return
	screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 99.0, "damage_roll_percent": 99.0})
	assert_eq(result.get("outcome", ""), "FAILED_HOLD")
	assert_false((screen.get_node("PrecisionIllustratedBackground") as TextureRect).visible, "saved hold result must not re-open the Precision illustration")
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
	success_screen.configure_context(success_item, ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), success_save, success_envelope)
	var success_upgrade := success_screen.get_node_or_null("WorkshopLayout/PrecisionActionUpgradeButton") as Button
	assert_not_null(success_upgrade)
	if success_upgrade == null:
		return
	success_screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
	assert_eq(success_screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 99.0}).get("outcome", ""), "SUCCESS")
	assert_false((success_screen.get_node("PrecisionIllustratedBackground") as TextureRect).visible, "saved success result must hide the Precision illustration")
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
	failed_screen.configure_context(failed_envelope.get_item(str(failed_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), failed_save, failed_envelope)
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
	screen.configure_context(item, ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), save_service, envelope)
	var initial: Dictionary = screen.view_state()
	assert_eq(initial.get("precision_mode", ""), "BACKFILL")
	assert_eq(initial.get("precision_target", ""), "+9 → +10")
	assert_false(bool(initial.get("enhancement_allowed", true)))
	var backfill_button := screen.get_node_or_null("WorkshopLayout/PrecisionBackfillButton") as Button
	var add_button := screen.get_node_or_null("WorkshopLayout/PrecisionActionAddButton") as Button
	assert_not_null(backfill_button)
	assert_not_null(add_button)
	if backfill_button == null or add_button == null:
		return
	assert_true(backfill_button.visible)
	assert_true(backfill_button.text.contains("비용 없음"))
	screen._on_precision_add_pressed()
	screen.set_precision_selection({
		"action": "ADD_TAG",
		"lineage_id": "ANVIL_LINEAGE",
		"method_id": "LIGHTWEIGHTING",
	})
	assert_false(backfill_button.disabled)
	var result: Dictionary = screen.request_precision_backfill()
	assert_eq(result.get("outcome", ""), "APPLIED")
	assert_eq(result.get("gold_cost", -1), 0)
	assert_eq(result.get("reinforcement_units", -1), 0)
	assert_eq(save_service.saved_envelope.get_item(item.uid).catalyst_tag_entries()[0].get("tag_id", ""), "TAG_ANVIL_LIGHT")
	assert_false(str(screen.get_node("WorkshopLayout/PrecisionPreviewLabel").text).contains("PRECISION_KEYWORD_PENDING_CONTENT"))


func test_precision_art_closes_after_actual_failed_damage_and_keeps_the_workshop_fallback() -> void:
	var envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var save_service := FakeSaveService.new()
	screen.configure_context(envelope.get_item(str(envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), save_service, envelope)
	var art := screen.get_node_or_null("PrecisionIllustratedBackground") as TextureRect
	var fallback := screen.get_node_or_null("WorkshopIllustratedBackground") as TextureRect
	assert_not_null(art)
	assert_not_null(fallback)
	if art == null or fallback == null:
		return
	assert_true(art.visible)
	screen.set_precision_selection({"action": "UPGRADE_TAG", "tag_id": "TAG_EMBER_EDGE"})
	var result: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 99.0, "damage_roll_percent": 0.0})
	assert_eq(result.get("outcome", ""), "FAILED_DAMAGE", "the exact saved failure result must exercise the post-result visual boundary")
	assert_false(art.visible, "saved FAILED_DAMAGE must close the Precision illustration")
	assert_true(fallback.visible, "the ordinary Workshop illustration remains the fallback behind native result controls")


func test_precision_art_reopens_only_after_a_saved_result_then_explicit_fresh_context_open() -> void:
	var first_envelope = _precision_envelope(9)
	var screen = SCREEN_SCENE.instantiate()
	add_child_autofree(screen)
	var first_save := FakeSaveService.new()
	screen.configure_context(first_envelope.get_item(str(first_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), first_save, first_envelope)
	var art := screen.get_node_or_null("PrecisionIllustratedBackground") as TextureRect
	assert_not_null(art)
	if art == null:
		return
	assert_true(art.visible, "new +9→+10 context opens the neutral Precision illustration")
	screen.set_precision_selection({"action": "ADD_TAG", "lineage_id": "EMBER_LINEAGE", "method_id": "EDGE_REINFORCEMENT"})
	var resolved: Dictionary = screen.request_enhancement_with_rolls({"success_roll_percent": 0.0, "damage_roll_percent": 99.0})
	assert_eq(resolved.get("outcome", ""), "SUCCESS")
	assert_false(art.visible, "the same screen must close art after the saved result before a later context is opened")
	var reopened_envelope = _precision_envelope(19, [{
		"tag_id": "TAG_EMBER_EDGE",
		"stage": 1,
		"created_milestone": 10,
		"last_advanced_milestone": 10,
	}], [10])
	screen.configure_context(reopened_envelope.get_item(str(reopened_envelope.active_run["selected_item_uid"])), ResourcesScript.new(20000, {"common_reinforcement_material": 10}), null, EnhancementActionServiceScript.new(), FakeSaveService.new(), reopened_envelope)
	assert_true(art.visible, "explicitly opening a fresh +19→+20 Precision ATTEMPT may re-open the illustration")
