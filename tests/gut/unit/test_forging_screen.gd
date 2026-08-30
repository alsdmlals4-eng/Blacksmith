# 첫 제작 화면이 승인된 공방 배경을 실제 런타임 레이어로 소비하는지 검증한다.
extends "res://addons/gut/test.gd"

const ForgingScreenScript := preload("res://scripts/ui/forging_screen.gd")
const FirstForgeBackgroundTexture := preload("res://assets/ui/workshop/first_forge_background_v1.png")
const EquipmentCatalogScript := preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")


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
