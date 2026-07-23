class_name EquipmentLifecyclePocScreen
extends Control

const WorkshopCalendarScript = preload("res://scripts/progression/workshop_calendar.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")
const WorkshopActionServiceScript = preload("res://scripts/poc/workshop_action_service.gd")
const CustomerContractScript = preload("res://scripts/customers/customer_contract.gd")
const EquipmentWorldRegistryScript = preload("res://scripts/world/equipment_world_registry.gd")
const WorldActivityResolverScript = preload("res://scripts/world/world_activity_resolver.gd")
const EquipmentLifecycleControllerScript = preload("res://scripts/poc/equipment_lifecycle_poc_controller.gd")
const CraftsmanshipGradeResolverScript = preload("res://scripts/forging/craftsmanship_grade_resolver.gd")
const PocTelemetryScript = preload("res://scripts/telemetry/poc_telemetry.gd")
const ForgingScreenScript = preload("res://scripts/ui/forging_screen.gd")
const LifecycleEnhancementScreenScript = preload("res://scripts/ui/lifecycle_enhancement_screen.gd")
const WorkshopHudScript = preload("res://scripts/ui/workshop_hud.gd")
const CustomerContractScreenScript = preload("res://scripts/ui/customer_contract_screen.gd")
const WorldReportScreenScript = preload("res://scripts/ui/world_report_screen.gd")

const BG := Color("#17191f")
const PANEL := Color("#252932")
const TEXT := Color("#f4f1e8")
const MUTED := Color("#b7b0a3")
const GOLD := Color("#f2c14e")
const GREEN := Color("#72b879")
const RED := Color("#e36c62")

var calendar
var resources
var action_service
var contract
var registry
var activity_resolver
var controller
var grade_resolver
var telemetry
var enhancement_screen
var current_equipment: Dictionary = {}
var status_message: String = ""
var equipment_sequence: int = 0


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_initialize_domain()
	_show_contract()


func _initialize_domain() -> void:
	var day_config := _read_json("res://data/progression/workshop_day_balance.json")
	var contract_config := _read_json("res://data/customers/gladiator_poc.json")
	var result_config := _read_json("res://data/world/gladiator_match_poc.json")
	calendar = WorkshopCalendarScript.new(day_config)
	resources = WorkshopResourcesScript.new(2500, {
		"iron": 5,
		"whetstone": 5,
		"flame_stone": 3,
		"spirit_heart": 2,
	})
	action_service = WorkshopActionServiceScript.new(calendar, resources)
	contract = CustomerContractScript.new(contract_config, result_config, calendar.day)
	registry = EquipmentWorldRegistryScript.new(6)
	activity_resolver = WorldActivityResolverScript.new(result_config)
	telemetry = PocTelemetryScript.new()
	controller = EquipmentLifecycleControllerScript.new(
		contract,
		registry,
		activity_resolver,
		calendar,
		resources,
		telemetry
	)
	grade_resolver = CraftsmanshipGradeResolverScript.new()


func _show_contract() -> void:
	_clear_children()
	_add_background()
	var layout := _root_layout()
	layout.add_child(_title("장비 한 점의 생애 PoC"))
	var contract_screen = CustomerContractScreenScript.new()
	contract_screen.configure(contract.config)
	contract_screen.accepted.connect(_on_contract_accepted)
	layout.add_child(_panel_wrap(contract_screen))
	layout.add_child(_note("이 PoC는 직원·직접 전투·자동 날짜 진행 없이 철검 한 점의 생애만 검증합니다."))
	_add_back_button()


func _on_contract_accepted() -> void:
	controller.accept_contract()
	status_message = "카일의 의뢰를 수락했습니다. 철검을 직접 제작하세요."
	_show_workshop()


func _show_workshop() -> void:
	_clear_children()
	_add_background()
	var layout := _root_layout()
	layout.add_child(_title("대장간 · 카일의 철검"))
	var hud = WorkshopHudScript.new()
	layout.add_child(hud)
	await get_tree().process_frame
	hud.update_snapshot(calendar.snapshot(), resources.snapshot(), contract.remaining_days(calendar.day))

	if status_message != "":
		var status := _note(status_message)
		status.add_theme_color_override("font_color", GREEN if not status_message.contains("부족") else RED)
		layout.add_child(status)

	if current_equipment.is_empty():
		layout.add_child(_panel_wrap(_build_empty_workshop()))
	else:
		layout.add_child(_panel_wrap(_build_equipment_workshop()))

	var end_day_button := _button("하루 마치기", 64)
	end_day_button.pressed.connect(_on_end_day_pressed)
	layout.add_child(end_day_button)
	layout.add_child(_note("날짜는 이 버튼으로만 진행됩니다. 남은 작업량의 50%가 다음 날로 이월됩니다."))
	_add_back_button()


func _build_empty_workshop() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 14)
	box.add_child(_label("제작할 장비가 없습니다.", 26, GOLD))
	box.add_child(_note("철 1개·100G·작업량 3을 사용합니다. 망치질 횟수에는 추가 피로도가 들지 않습니다."))
	var forge_button := _button("철검 제작 시작", 90)
	forge_button.pressed.connect(_on_start_forging)
	box.add_child(forge_button)
	return box


func _build_equipment_workshop() -> Control:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 13)
	box.add_child(_label(_equipment_title(current_equipment), 28, GOLD))
	box.add_child(_label(
		"영구 완성도: %s · 마감 정타: %s\n공격력 %d · 수식어 %s" % [
			str(current_equipment.get("craftsmanship_grade_label", "평범한")),
			str(current_equipment.get("precision_result_label", "보통 마감")),
			int(current_equipment.get("progression_attack", current_equipment.get("base_attack", 20))),
			_affix_text(current_equipment.get("affixes", [])),
		],
		18,
		TEXT
	))
	var fit: Dictionary = contract.evaluate_fit(current_equipment)
	box.add_child(_note("현재 적합도 %d점 · 예상 결과 %s" % [int(fit.get("score", 0)), _result_name(str(fit.get("band_id", "")))]))

	var enhance_button := _button("강화 화면 열기 · 버튼 입력당 1회 판정", 78)
	enhance_button.disabled = int(current_equipment.get("enhancement_level", 0)) >= 10
	enhance_button.pressed.connect(_show_enhancement)
	box.add_child(enhance_button)

	var eligibility: Dictionary = contract.can_deliver(current_equipment, calendar.day)
	var deliver_button := _button("현재 상태로 카일에게 납품", 78)
	deliver_button.disabled = not bool(eligibility.get("ok", false))
	deliver_button.pressed.connect(_on_deliver_pressed)
	box.add_child(deliver_button)
	if not bool(eligibility.get("ok", false)):
		box.add_child(_note("납품 불가: %s" % ", ".join(_string_array(eligibility.get("missing_conditions", [])))))
	return box


func _on_start_forging() -> void:
	var transaction: Dictionary = action_service.try_begin_forging(100, "iron", 1, func() -> bool: return true)
	if not bool(transaction.get("ok", false)):
		status_message = _transaction_error(transaction)
		_show_workshop()
		return
	_clear_children()
	var forging_screen = ForgingScreenScript.new()
	add_child(forging_screen)
	await get_tree().process_frame
	if forging_screen.session != null and not forging_screen.session.completed.is_connected(_on_forging_completed):
		forging_screen.session.completed.connect(_on_forging_completed)
	_add_back_button(false)


func _on_forging_completed(result: Dictionary) -> void:
	equipment_sequence += 1
	var resolved_grade: Dictionary = grade_resolver.resolve(str(result.get("quality_id", "STANDARD")), _grade_roll_for_precision(str(result.get("quality_id", "STANDARD"))))
	var equipment := result.duplicate(true)
	for key in resolved_grade:
		equipment[key] = resolved_grade[key]
	equipment["equipment_uid"] = "poc_sword_%03d" % equipment_sequence
	equipment["record_schema_version"] = 1
	equipment["enhancement_level"] = 0
	equipment["progression_attack"] = int(equipment.get("base_attack", 20))
	equipment["affixes"] = []
	equipment["destroyed"] = false
	equipment["lifecycle_state"] = "WORKSHOP"
	current_equipment = equipment
	controller.add_equipment(equipment)
	telemetry.record("forging_completed", {"equipment_uid": equipment["equipment_uid"], "grade": equipment.get("craftsmanship_grade_id", "")})
	status_message = "%s 철검이 완성됐습니다." % str(equipment.get("craftsmanship_grade_label", "평범한"))
	call_deferred("_show_workshop")


func _show_enhancement() -> void:
	_clear_children()
	enhancement_screen = LifecycleEnhancementScreenScript.new()
	enhancement_screen.configure_weapon(current_equipment)
	enhancement_screen.set_workshop_action_service(action_service)
	add_child(enhancement_screen)
	await get_tree().process_frame
	enhancement_screen.set_workshop_resources(resources)
	if enhancement_screen.session != null and not enhancement_screen.session.attempt_resolved.is_connected(_on_enhancement_resolved):
		enhancement_screen.session.attempt_resolved.connect(_on_enhancement_resolved)
	var return_button := _button("현재 장비로 대장간 복귀", 58)
	return_button.set_anchors_preset(Control.PRESET_TOP_LEFT)
	return_button.position = Vector2(18.0, 18.0)
	return_button.size = Vector2(270.0, 58.0)
	return_button.z_index = 120
	return_button.pressed.connect(_return_from_enhancement)
	add_child(return_button)


func _on_enhancement_resolved(result: Dictionary) -> void:
	telemetry.record("enhancement_attempted", {
		"target_level": int(result.get("target_level", 0)),
		"success": bool(result.get("success", false)),
		"special": bool(result.get("uses_materials", false)),
	})


func _return_from_enhancement() -> void:
	if enhancement_screen == null or enhancement_screen.session == null:
		return
	var record: Dictionary = enhancement_screen.build_weapon_record()
	for key in [
		"equipment_uid", "record_schema_version", "precision_result_id", "precision_result_label",
		"craftsmanship_grade_id", "craftsmanship_grade_label", "craftsmanship_score_bonus",
		"craftsmanship_attack_multiplier", "craftsmanship_value_multiplier",
	]:
		if current_equipment.has(key):
			record[key] = current_equipment[key]
	record["lifecycle_state"] = "WORKSHOP"
	current_equipment = record
	if controller.inventory.is_empty():
		controller.add_equipment(record)
	else:
		controller.inventory[0] = record.duplicate(true)
	telemetry.record("enhancement_stopped", {"level": int(record.get("enhancement_level", 0))})
	status_message = "+%d 상태로 강화를 멈췄습니다." % int(record.get("enhancement_level", 0))
	_show_workshop()


func _on_deliver_pressed() -> void:
	var uid := str(current_equipment.get("equipment_uid", ""))
	var result: Dictionary = controller.deliver(uid, "delivery:%s:%d" % [uid, calendar.day])
	if not bool(result.get("ok", false)):
		status_message = "납품 실패: %s" % str(result.get("status", "UNKNOWN"))
		_show_workshop()
		return
	current_equipment = {}
	status_message = "납품 완료. 경기 결과는 최소 하루 뒤 도착합니다."
	_show_workshop()


func _on_end_day_pressed() -> void:
	var result: Dictionary = controller.end_day()
	if not Array(result.get("resolved_results", [])).is_empty():
		_show_report()
		return
	status_message = "%d일차가 시작됐습니다. 아직 도착한 경기 결과가 없습니다." % calendar.day
	_show_workshop()


func _show_report() -> void:
	var target_uid := ""
	for uid in registry.records:
		if str(registry.records[uid].get("report_state", "")) == registry.REPORT_RESULT_READY:
			target_uid = str(uid)
			break
	if target_uid == "":
		status_message = "열 수 있는 경기 보고서가 없습니다."
		_show_workshop()
		return
	var opened: Dictionary = controller.open_report(target_uid)
	if not bool(opened.get("ok", false)):
		status_message = "보고서 열기 실패: %s" % str(opened.get("status", "UNKNOWN"))
		_show_workshop()
		return
	_clear_children()
	_add_background()
	var layout := _root_layout()
	var report = WorldReportScreenScript.new()
	layout.add_child(_title("세계에서 돌아온 장비의 역사"))
	layout.add_child(_panel_wrap(report))
	await get_tree().process_frame
	report.configure(opened.get("record", {}))
	report.continue_requested.connect(_show_follow_up)
	_add_back_button()


func _show_follow_up() -> void:
	_clear_children()
	_add_background()
	var layout := _root_layout()
	layout.add_child(_title("검투사 카일의 재방문"))
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 16)
	box.add_child(_label("“지난 경기에서 그 검이 어떤 역할을 했는지 잊지 않았소.”", 23, GOLD))
	box.add_child(_label("카일이 이전 장비의 결과를 언급하며 더 높은 수준의 의뢰를 제안합니다.", 19, TEXT))
	box.add_child(_label("누적 명성 %d · 카일 관계 %d · 세계 장비 기록 %d건" % [controller.fame, controller.relationship, registry.records.size()], 18, MUTED))
	var restart := _button("PoC 다시 시작", 74)
	restart.pressed.connect(_restart_poc)
	box.add_child(restart)
	layout.add_child(_panel_wrap(box))
	_add_back_button()


func _restart_poc() -> void:
	current_equipment = {}
	status_message = ""
	equipment_sequence = 0
	_initialize_domain()
	_show_contract()


func _transaction_error(transaction: Dictionary) -> String:
	match str(transaction.get("status", "")):
		"NO_FATIGUE": return "작업량이 %d 부족합니다." % int(transaction.get("missing", 0))
		"NO_GOLD": return "골드가 %dG 부족합니다." % int(transaction.get("missing_gold", 0))
		"NO_MATERIAL": return "재료가 부족합니다."
		_: return "작업을 시작하지 못했습니다."


func _equipment_title(equipment: Dictionary) -> String:
	return "%s +%d" % [str(equipment.get("weapon_name", "철검")), int(equipment.get("enhancement_level", 0))]


func _affix_text(values: Array) -> String:
	if values.is_empty():
		return "없음"
	var parts: Array[String] = []
	for value in values:
		if value is Dictionary:
			parts.append("%s %d티어" % [str(value.get("name", value.get("id", "수식어"))), int(value.get("tier", 1))])
	return ", ".join(parts)


func _grade_roll_for_precision(precision_id: String) -> float:
	match precision_id:
		"PERFECT": return 0.65
		"GOOD": return 0.50
		_: return 0.25


func _result_name(result_id: String) -> String:
	match result_id:
		"DEFEAT": return "패배"
		"WIN": return "승리"
		"DECISIVE_WIN": return "압도적 승리"
		_: return "미정"


func _string_array(values: Array) -> Array[String]:
	var result: Array[String] = []
	for value in values:
		result.append(str(value))
	return result


func _read_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("필수 PoC 데이터를 읽지 못했습니다: %s" % path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func _clear_children() -> void:
	for child in get_children():
		remove_child(child)
		child.queue_free()


func _add_background() -> void:
	var background := ColorRect.new()
	background.color = BG
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)


func _root_layout() -> VBoxContainer:
	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 28)
	margin.add_theme_constant_override("margin_bottom", 86)
	add_child(margin)
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	margin.add_child(scroll)
	var layout := VBoxContainer.new()
	layout.custom_minimum_size = Vector2(672.0, 0.0)
	layout.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	layout.add_theme_constant_override("separation", 16)
	scroll.add_child(layout)
	return layout


func _add_back_button(allow_during_action: bool = true) -> void:
	var back := _button("기존 Prototype으로 돌아가기", 54)
	back.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	back.offset_left = 24.0
	back.offset_right = -24.0
	back.offset_top = -70.0
	back.offset_bottom = -16.0
	back.z_index = 150
	back.disabled = not allow_during_action
	back.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://scenes/main/main.tscn"))
	add_child(back)


func _title(value: String) -> Label:
	return _label(value, 32, GOLD)


func _note(value: String) -> Label:
	var label := _label(value, 16, MUTED)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return label


func _label(value: String, size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = value
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return label


func _button(value: String, height: float) -> Button:
	var button := Button.new()
	button.text = value
	button.custom_minimum_size = Vector2(0.0, height)
	button.add_theme_font_size_override("font_size", 21)
	return button


func _panel_wrap(content: Control) -> PanelContainer:
	var panel := PanelContainer.new()
	var style := StyleBoxFlat.new()
	style.bg_color = PANEL
	style.corner_radius_top_left = 18
	style.corner_radius_top_right = 18
	style.corner_radius_bottom_left = 18
	style.corner_radius_bottom_right = 18
	style.content_margin_left = 20.0
	style.content_margin_right = 20.0
	style.content_margin_top = 18.0
	style.content_margin_bottom = 18.0
	panel.add_theme_stylebox_override("panel", style)
	panel.add_child(content)
	return panel
