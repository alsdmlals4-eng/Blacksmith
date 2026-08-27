# 첫 제작 화면이 승인된 공방 배경을 실제 런타임 레이어로 소비하는지 검증한다.
extends "res://addons/gut/test.gd"

const ForgingScreenScript := preload("res://scripts/ui/forging_screen.gd")
const FirstForgeBackgroundTexture := preload("res://assets/ui/workshop/first_forge_background_v1.png")


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
