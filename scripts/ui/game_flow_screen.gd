extends Control

const ForgingScreenScript = preload("res://scripts/ui/forging_screen.gd")
const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")
const VERSION_TEXT := "POC v0.3.1 · main · 2026.07.21.1"

var current_screen: Control
var enhance_button: Button


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_build_enhance_button()
	_show_forging()
	_build_version_badge()
	set_process(true)


func _process(_delta: float) -> void:
	if current_screen == null or not is_instance_valid(current_screen):
		enhance_button.visible = false
		return
	if current_screen.get_script() == ForgingScreenScript:
		var forging_session = current_screen.get("session")
		enhance_button.visible = (
			forging_session != null
			and forging_session.state == ForgingSessionScript.State.COMPLETE
		)
	else:
		enhance_button.visible = false


func _build_enhance_button() -> void:
	enhance_button = Button.new()
	enhance_button.text = "완성한 철검 강화하기"
	enhance_button.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	enhance_button.position = Vector2(-270.0, -215.0)
	enhance_button.size = Vector2(540.0, 82.0)
	enhance_button.add_theme_font_size_override("font_size", 24)
	enhance_button.add_theme_color_override("font_color", Color("#241b0f"))
	enhance_button.add_theme_stylebox_override("normal", _button_style(Color("#f2c14e"), Color.WHITE, 20))
	enhance_button.add_theme_stylebox_override("pressed", _button_style(Color("#c99835"), Color.WHITE, 20))
	enhance_button.visible = false
	enhance_button.pressed.connect(_open_enhancement)
	add_child(enhance_button)


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


func _show_forging() -> void:
	_replace_screen(ForgingScreenScript.new())
	enhance_button.visible = false


func _open_enhancement() -> void:
	if current_screen == null:
		return
	var forging_session = current_screen.get("session")
	if forging_session == null:
		return
	var weapon_result: Dictionary = forging_session.result.duplicate(true)
	var enhancement_screen = EnhancementScreenScript.new()
	enhancement_screen.configure_weapon(weapon_result)
	enhancement_screen.restart_requested.connect(_show_forging)
	_replace_screen(enhancement_screen)
	enhance_button.visible = false


func _replace_screen(next_screen: Control) -> void:
	if current_screen != null and is_instance_valid(current_screen):
		current_screen.queue_free()
	current_screen = next_screen
	current_screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(current_screen)
	move_child(enhance_button, get_child_count() - 1)


func _button_style(color: Color, border_color: Color, radius: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.border_color = border_color
	style.set_border_width_all(3)
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	return style
