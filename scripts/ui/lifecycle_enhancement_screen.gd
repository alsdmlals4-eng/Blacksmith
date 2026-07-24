class_name LifecycleEnhancementScreen
extends "res://scripts/ui/enhancement_screen.gd"

const POC_MAX_LEVEL := 10
const DEFAULT_PRECISION_SPEED := 0.9
const DEFAULT_GOOD_RADIUS := 0.18
const DEFAULT_PERFECT_RADIUS := 0.07

var workshop_action_service
var precision_assist_enabled: bool = false
var reduced_motion_enabled: bool = false
var lifecycle_status_label: Label
var return_guard: Button


func _ready() -> void:
	super._ready()
	if session != null:
		session.config["max_level"] = POC_MAX_LEVEL
	_build_lifecycle_status()
	_build_return_guard()
	_apply_accessibility_options()
	if session != null:
		_refresh(session.snapshot())
	_update_lifecycle_status()


func _process(delta: float) -> void:
	super._process(delta)
	_update_lifecycle_status()


func set_workshop_action_service(service) -> void:
	workshop_action_service = service
	_update_lifecycle_status()


func set_accessibility_options(precision_assist: bool, reduced_motion: bool) -> void:
	precision_assist_enabled = precision_assist
	reduced_motion_enabled = reduced_motion
	_apply_accessibility_options()


func can_return_to_workshop() -> bool:
	return session != null and int(session.state) != 1


func return_block_reason() -> String:
	if session != null and int(session.state) == 1:
		return "특수 강화 타격을 완료한 뒤 대장간으로 돌아갈 수 있습니다."
	return ""


func _build_lifecycle_status() -> void:
	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_TOP_WIDE)
	panel.offset_left = 305.0
	panel.offset_top = 18.0
	panel.offset_right = -305.0
	panel.offset_bottom = 72.0
	panel.z_index = 125
	var style := StyleBoxFlat.new()
	style.bg_color = Color("#252932e6")
	style.corner_radius_top_left = 12
	style.corner_radius_top_right = 12
	style.corner_radius_bottom_left = 12
	style.corner_radius_bottom_right = 12
	style.content_margin_left = 12.0
	style.content_margin_right = 12.0
	panel.add_theme_stylebox_override("panel", style)
	lifecycle_status_label = Label.new()
	lifecycle_status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lifecycle_status_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	lifecycle_status_label.add_theme_font_size_override("font_size", 16)
	lifecycle_status_label.add_theme_color_override("font_color", Color("#f4f1e8"))
	panel.add_child(lifecycle_status_label)
	add_child(panel)


func _build_return_guard() -> void:
	return_guard = Button.new()
	return_guard.text = "특수 강화 타격을 먼저 완료하세요"
	return_guard.set_anchors_preset(Control.PRESET_TOP_LEFT)
	return_guard.position = Vector2(18.0, 18.0)
	return_guard.size = Vector2(270.0, 58.0)
	return_guard.z_index = 135
	return_guard.disabled = true
	return_guard.mouse_filter = Control.MOUSE_FILTER_STOP
	return_guard.add_theme_font_size_override("font_size", 15)
	return_guard.visible = false
	add_child(return_guard)


func _update_lifecycle_status() -> void:
	if lifecycle_status_label == null:
		return
	if return_guard != null:
		return_guard.visible = session != null and int(session.state) == 1
	if workshop_action_service == null or workshop_action_service.calendar == null:
		lifecycle_status_label.text = "PoC 상한 +10"
		return
	var calendar = workshop_action_service.calendar
	lifecycle_status_label.text = "현재 작업 %d / 기본 %d · PoC 상한 +10" % [
		int(calendar.current_fatigue),
		int(calendar.base_fatigue),
	]


func _apply_accessibility_options() -> void:
	if session == null:
		return
	var precision: Dictionary = session.config.get("precision", {})
	precision["speed"] = 0.55 if reduced_motion_enabled else DEFAULT_PRECISION_SPEED
	precision["good_radius"] = 0.28 if precision_assist_enabled else DEFAULT_GOOD_RADIUS
	precision["perfect_radius"] = DEFAULT_PERFECT_RADIUS
	session.config["precision"] = precision


func _on_normal_pressed() -> void:
	if session == null or int(session.state) != 0:
		return
	if int(session.enhancement_level) >= POC_MAX_LEVEL:
		return
	if session.uses_materials_for_level(int(session.enhancement_level) + 1):
		return
	if workshop_action_service == null:
		super._on_normal_pressed()
		return
	var transaction: Dictionary = workshop_action_service.try_begin_enhancement(session)
	if not bool(transaction.get("ok", false)):
		_show_transaction_error(transaction)
	_refresh(session.snapshot())
	_update_lifecycle_status()


func _on_special_start_pressed() -> void:
	if session == null or int(session.state) != 0:
		return
	if int(session.enhancement_level) >= POC_MAX_LEVEL:
		return
	if not session.uses_materials_for_level(int(session.enhancement_level) + 1):
		return
	if workshop_action_service == null:
		super._on_special_start_pressed()
		return
	var transaction: Dictionary = workshop_action_service.try_begin_enhancement(session)
	if not bool(transaction.get("ok", false)):
		_show_transaction_error(transaction)
	_refresh(session.snapshot())
	_update_lifecycle_status()


func _on_precision_pressed() -> void:
	if session == null or int(session.state) != 1:
		return
	if precision_assist_enabled:
		var precision: Dictionary = session.config.get("precision", {})
		var target := float(precision.get("target", 0.5))
		var perfect_radius := float(precision.get("perfect_radius", DEFAULT_PERFECT_RADIUS))
		var good_radius := float(precision.get("good_radius", 0.28))
		var assisted_offset := minf(maxf(perfect_radius + 0.02, perfect_radius * 1.1), good_radius * 0.8)
		session.precision_position = clampf(target + assisted_offset, 0.0, 1.0)
	super._on_precision_pressed()
	_update_lifecycle_status()


func _show_transaction_error(transaction: Dictionary) -> void:
	var status := str(transaction.get("status", "START_FAILED"))
	match status:
		"NO_FATIGUE":
			last_result_text = "작업량이 %d 부족합니다. 자동으로 날짜를 넘기지 않습니다." % int(transaction.get("missing", 0))
		"NO_GOLD":
			last_result_text = "골드가 %dG 부족합니다." % int(transaction.get("missing_gold", 0))
		"NO_MATERIAL":
			last_result_text = "특수 강화 재료가 부족합니다."
		_:
			last_result_text = "강화를 시작하지 못했습니다: %s" % status
	last_result_color = Color("#e36c62")
