class_name LifecycleAccessibilityOverlay
extends PanelContainer

const ForgingScreenScript = preload("res://scripts/ui/forging_screen.gd")

var precision_assist_enabled: bool = false
var reduced_motion_enabled: bool = false
var assist_toggle: CheckButton
var motion_toggle: CheckButton


func _ready() -> void:
	set_anchors_preset(Control.PRESET_TOP_RIGHT)
	offset_left = -290.0
	offset_top = 82.0
	offset_right = -18.0
	offset_bottom = 210.0
	z_index = 220
	var style := StyleBoxFlat.new()
	style.bg_color = Color("#252932e6")
	style.corner_radius_top_left = 14
	style.corner_radius_top_right = 14
	style.corner_radius_bottom_left = 14
	style.corner_radius_bottom_right = 14
	style.content_margin_left = 14.0
	style.content_margin_right = 14.0
	style.content_margin_top = 10.0
	style.content_margin_bottom = 10.0
	add_theme_stylebox_override("panel", style)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 6)
	add_child(box)
	assist_toggle = CheckButton.new()
	assist_toggle.text = "정밀 보조 · GOOD 범위"
	assist_toggle.custom_minimum_size = Vector2(0.0, 48.0)
	assist_toggle.add_theme_font_size_override("font_size", 16)
	assist_toggle.toggled.connect(func(value: bool) -> void: precision_assist_enabled = value)
	box.add_child(assist_toggle)
	motion_toggle = CheckButton.new()
	motion_toggle.text = "모션 감소 · 느린 포인터"
	motion_toggle.custom_minimum_size = Vector2(0.0, 48.0)
	motion_toggle.add_theme_font_size_override("font_size", 16)
	motion_toggle.toggled.connect(func(value: bool) -> void: reduced_motion_enabled = value)
	box.add_child(motion_toggle)
	set_process(true)


func _process(_delta: float) -> void:
	var screen := get_parent().get_node_or_null("Screen")
	if screen == null:
		return
	for child in screen.get_children():
		if child.has_method("set_accessibility_options"):
			child.set_accessibility_options(precision_assist_enabled, reduced_motion_enabled)
			continue
		if child.get_script() != ForgingScreenScript:
			continue
		var session = child.session
		if session == null:
			continue
		if reduced_motion_enabled:
			session.config["precision_speed"] = 0.55
		else:
			session.config["precision_speed"] = float(session.DEFAULT_CONFIG.get("precision_speed", 0.85))
		if precision_assist_enabled:
			# 모든 타이밍을 GOOD으로 처리하고 PERFECT 자동 보너스는 제거합니다.
			session.config["precision_perfect_radius"] = 0.0
			session.config["precision_good_radius"] = 1.0
		else:
			session.config["precision_perfect_radius"] = float(session.DEFAULT_CONFIG.get("precision_perfect_radius", 0.07))
			session.config["precision_good_radius"] = float(session.DEFAULT_CONFIG.get("precision_good_radius", 0.18))
