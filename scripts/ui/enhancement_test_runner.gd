extends Control

const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const VERSION_TEXT := "POC v0.3.1 · main · 2026.07.21.1"

var current_screen: Control


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_show_enhancement_test()
	_build_version_badge()


func _show_enhancement_test() -> void:
	if current_screen != null and is_instance_valid(current_screen):
		current_screen.queue_free()
	current_screen = EnhancementScreenScript.new()
	current_screen.configure_weapon({
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"quality_id": "TEST",
		"quality_label": "테스트용 철검",
		"quality_multiplier": 1.0,
	})
	current_screen.restart_requested.connect(_show_enhancement_test)
	current_screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(current_screen)


func _build_version_badge() -> void:
	var badge := PanelContainer.new()
	badge.name = "VersionBadge"
	badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	badge.z_index = 100
	badge.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	badge.offset_left = -315.0
	badge.offset_top = -52.0
	badge.offset_right = -12.0
	badge.offset_bottom = -12.0
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.06, 0.08, 0.88)
	style.border_color = Color(0.45, 0.49, 0.57, 0.8)
	style.set_border_width_all(1)
	style.corner_radius_top_left = 10
	style.corner_radius_top_right = 10
	style.corner_radius_bottom_left = 10
	style.corner_radius_bottom_right = 10
	style.content_margin_left = 12.0
	style.content_margin_right = 12.0
	style.content_margin_top = 7.0
	style.content_margin_bottom = 7.0
	badge.add_theme_stylebox_override("panel", style)
	var label := Label.new()
	label.text = VERSION_TEXT
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", Color("#d9dde6"))
	badge.add_child(label)
	add_child(badge)
