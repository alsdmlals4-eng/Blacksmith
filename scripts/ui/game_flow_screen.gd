extends Control

const ForgingScreenScript = preload("res://scripts/ui/forging_screen.gd")
const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")

var current_screen: Control
var enhance_button: Button


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_build_enhance_button()
	_show_forging()
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
