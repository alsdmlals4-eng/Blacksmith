class_name LifecycleEnhancementScreen
extends "res://scripts/ui/enhancement_screen.gd"

var workshop_action_service


func set_workshop_action_service(service) -> void:
	workshop_action_service = service


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
