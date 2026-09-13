# 첫 제작 화면이 승인된 공방 배경을 실제 런타임 레이어로 소비하는지 검증한다.
extends "res://addons/gut/test.gd"

const ForgingScreenScript := preload("res://scripts/ui/forging_screen.gd")
const FirstForgeBackgroundTexture := preload("res://assets/ui/workshop/first_forge_background_v1.png")
const EquipmentCatalogScript := preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")


func test_reading_before_first_hammer_does_not_start_or_lock_equipment() -> void:
	var screen = ForgingScreenScript.new()
	add_child_autofree(screen)
	screen._process(30.0)
	assert_eq(screen.session.progress, 0.0, "Reading is not consent to start forging")
	assert_true(screen.select_equipment("iron_shield"))
	screen._on_hammer_pressed()
	assert_eq(screen.state_label.text, "제작 중")
	var after_tap: float = screen.session.progress
	screen._process(1.0)
	assert_gt(screen.session.progress, after_tap, "Auto work continues after explicit first hammer")
	assert_false(screen.select_equipment("iron_bow"))


func test_all_five_selected_identities_reach_the_completed_result() -> void:
	for entry in EquipmentCatalogScript.all():
		var screen = ForgingScreenScript.new()
		add_child_autofree(screen)
		var equipment_id: String = entry["equipment_id"]
		assert_true(screen.select_equipment(equipment_id))
		screen.session.set_precision_enabled(false)
		screen._on_hammer_pressed()
		screen._process(1000.0)
		assert_eq(screen._completed_result.get("equipment_id"), equipment_id)
		assert_eq(screen.result_name_label.text, "%s 완성!" % entry["display_name_ko"])


func test_first_forge_has_scrollable_controls_and_reachable_confirmation() -> void:
	var screen = ForgingScreenScript.new()
	add_child_autofree(screen)
	var scroll := screen.find_child("ForgeScroll", true, false) as ScrollContainer
	assert_not_null(scroll, "Five equipment choices must not push actions outside the portrait viewport")
	if scroll == null:
		return
	assert_true(scroll.follow_focus)
	assert_eq(scroll.horizontal_scroll_mode, ScrollContainer.SCROLL_MODE_DISABLED)
	screen.session.set_precision_enabled(false)
	screen._on_hammer_pressed()
	screen._process(1000.0)
	await get_tree().process_frame
	await get_tree().process_frame
	scroll.ensure_control_visible(screen.result_commit_button)
	await get_tree().process_frame
	assert_true(scroll.get_global_rect().encloses(screen.result_commit_button.get_global_rect()))


func test_first_forge_uses_the_illustrated_workshop_background_with_a_readability_veil() -> void:
	var screen = ForgingScreenScript.new()
	add_child_autofree(screen)
	var background := screen.get_node_or_null("FirstForgeIllustratedBackground") as TextureRect
	assert_not_null(background)
	if background == null:
		return
	assert_eq(background.texture, FirstForgeBackgroundTexture)
	assert_eq(background.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(background.z_index, -2)
	var veil := screen.get_node_or_null("FirstForgeReadabilityVeil") as ColorRect
	assert_not_null(veil)
	if veil == null:
		return
	assert_eq(veil.mouse_filter, Control.MOUSE_FILTER_IGNORE)
	assert_eq(veil.z_index, -1)
	assert_gt(veil.color.a, 0.0)


func test_first_forge_exposes_five_48dp_equipment_choices_and_locks_the_choice_after_work_starts() -> void:
	var screen = ForgingScreenScript.new()
	add_child_autofree(screen)
	for entry in EquipmentCatalogScript.all():
		var equipment_id := str(entry.get("equipment_id", ""))
		var choice := screen.find_child("EquipmentChoice_%s" % equipment_id, true, false) as Button
		assert_not_null(choice, equipment_id)
		if choice != null:
			assert_gte(choice.custom_minimum_size.y, 48.0, equipment_id)
	assert_true(screen.select_equipment("iron_helmet"))
	assert_eq(screen.selected_equipment_id(), "iron_helmet")
	screen.session.advance(0.1)
	assert_false(screen.select_equipment("iron_sword"))
	assert_eq(screen.selected_equipment_id(), "iron_helmet")


func test_first_forge_binds_each_equipment_identity_illustration_without_replacing_the_choice_button() -> void:
	var screen = ForgingScreenScript.new()
	add_child_autofree(screen)
	for entry in EquipmentCatalogScript.all():
		var equipment_id := str(entry.get("equipment_id", ""))
		var choice := screen.find_child("EquipmentChoice_%s" % equipment_id, true, false) as Button
		assert_not_null(choice, equipment_id)
		if choice == null:
			continue
		var illustration := choice.get_node_or_null("EquipmentIdentityIllustration") as TextureRect
		assert_not_null(illustration, equipment_id)
		if illustration == null:
			continue
		var image_path := str(entry.get("image_path", ""))
		assert_true(ResourceLoader.exists(image_path), image_path)
		assert_not_null(illustration.texture, equipment_id)
		assert_eq(illustration.texture.resource_path, image_path, equipment_id)
		assert_eq(illustration.texture.get_width(), 512, equipment_id)
		assert_eq(illustration.texture.get_height(), 512, equipment_id)
		assert_eq(illustration.mouse_filter, Control.MOUSE_FILTER_IGNORE, equipment_id)
		assert_gte(choice.custom_minimum_size.y, 48.0, equipment_id)
