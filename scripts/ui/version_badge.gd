class_name VersionBadge
extends PanelContainer

const BuildInfoScript = preload("res://scripts/core/build_info.gd")


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 100
	set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	offset_left = -315.0
	offset_top = -52.0
	offset_right = -12.0
	offset_bottom = -12.0

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
	add_theme_stylebox_override("panel", style)

	var label := Label.new()
	label.text = BuildInfoScript.display_text()
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", Color("#d9dde6"))
	add_child(label)
