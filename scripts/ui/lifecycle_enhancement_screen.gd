class_name LifecycleEnhancementScreen
extends "res://scripts/ui/enhancement_screen.gd"

var workshop_action_service
var precision_assist_enabled: bool = false
var reduced_motion_enabled: bool = false


func _ready() -> void:
	super._ready()
	_apply_accessibility_options()


func set_workshop_action_service(service) -> void:
	workshop_action_service = service


func set_accessibility_options(precision_assist: bool, reduced_motion: bool) -> void:
	precision_assist_enabled = precision_assist
	reduced_motion_enabled = reduced_motion
	_apply_accessibility_options()


func _apply_accessibility_options() -> void:
	if session == null:
		return
	var precision: Dictionary = session.config.get("precision", {})
	if reduced_motion_enabled:
		precision["speed"] = minf(float(precision.get("speed", 0.9)), 0.55)
	if precision_assist_enabled:
		precision["good_radius"] = maxf(float(precision.get("good_radius", 0.18)), 0.28)
		precision["perfect_radius"] = minf(float(precision.get("perfect_radius", 0.07)), 0.07)
	session.config["precision"] = precision


func _on_normal_pressed() -> void:
	if session == null or int(session.state) != 0:
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


func _on_special_start_pressed() -> void:
	if session == null or int(session.state) != 0:
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


func _on_precision_pressed() -> void:
	if session == null or int(session.state) != 1:
		return
	if precision_assist_enabled:
		var precision: Dictionary = session.config.get("precision", {})
		var target := float(precision.get("target", 0.5))
		var perfect_radius := float(precision.get("perfect_radius", 0.07))
		var good_radius := float(precision.get("good_radius", 0.28))
		var assisted_offset := minf(maxf(perfect_radius + 0.02, perfect_radius * 1.1), good_radius * 0.8)
		session.precision_position = clampf(target + assisted_offset, 0.0, 1.0)
	super._on_precision_pressed()


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
