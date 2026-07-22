# 일반/특수 강화 화면에 성장·가치·위험·보관 정보를 통합합니다.
class_name EnhancementScreen
extends "res://scripts/ui/special_enhancement_screen.gd"

signal store_requested(weapon: Dictionary)
signal inventory_requested
signal auto_forge_requested(options: Dictionary)

const INVENTORY_CAPACITY := 6
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")

var inventory_count: int = 0
var inventory_capacity: int = INVENTORY_CAPACITY
var store_buttons: Array[Button] = []
var inventory_buttons: Array[Button] = []
var skill_selectors: Array[OptionButton] = []
var skill_description_labels: Array[Label] = []

var normal_current_label: Label
var normal_next_label: Label
var normal_price_label: Label
var normal_cost_label: Label
var normal_risk_label: Label

var special_current_label: Label
var special_next_label: Label
var special_price_label: Label
var special_cost_label: Label
var special_risk_label: Label
var special_catalyst_label: Label
var special_effect_label: Label

var complete_title_label: Label
var complete_value_label: Label
var complete_effect_label: Label

var workshop_resources
var available_gold: int = 0
var material_stock: Dictionary = {}
var auto_running: bool = false
var auto_target_spins: Array[SpinBox] = []
var auto_repeat_checks: Array[CheckButton] = []
var auto_secondary_selectors: Array[OptionButton] = []
var auto_catalyst_selectors: Array[OptionButton] = []
var auto_skill_selectors: Array[OptionButton] = []
var auto_start_buttons: Array[Button] = []
var auto_status_labels: Array[Label] = []
var auto_resource_labels: Array[Label] = []


func _ready() -> void:
	super._ready()
	_attach_progression_panels()
	_populate_skill_selectors()
	if session != null:
		session.changed.connect(_on_session_snapshot_changed)
		_on_session_snapshot_changed(session.snapshot())
	_bind_workshop_resources()
	_update_inventory_buttons()


func set_inventory_count(count: int, capacity: int = INVENTORY_CAPACITY) -> void:
	inventory_count = maxi(count, 0)
	inventory_capacity = maxi(capacity, 1)
	_update_inventory_buttons()


func set_workshop_resources(resources) -> void:
	if workshop_resources != null and workshop_resources.changed.is_connected(_on_workshop_resources_changed):
		workshop_resources.changed.disconnect(_on_workshop_resources_changed)
	workshop_resources = resources
	_bind_workshop_resources()



func _bind_workshop_resources() -> void:
	if workshop_resources == null:
		return
	if not workshop_resources.changed.is_connected(_on_workshop_resources_changed):
		workshop_resources.changed.connect(_on_workshop_resources_changed)
	_on_workshop_resources_changed(workshop_resources.snapshot())


func _on_workshop_resources_changed(resources_snapshot: Dictionary) -> void:
	available_gold = maxi(int(resources_snapshot.get("gold", 0)), 0)
	material_stock = resources_snapshot.get("material_stock", {}).duplicate(true)
	_update_resource_controls()


func _update_resource_controls() -> void:
	_update_auto_resource_labels()
	_update_manual_material_selectors()
	_update_manual_attempt_buttons()


func set_auto_status(text_value: String) -> void:
	for label in auto_status_labels:
		if is_instance_valid(label):
			label.text = text_value


func set_auto_running(value: bool) -> void:
	auto_running = value
	for control in auto_target_spins:
		if is_instance_valid(control):
			control.editable = not value
	for control in auto_repeat_checks:
		if is_instance_valid(control):
			control.disabled = value
	for control in auto_secondary_selectors + auto_catalyst_selectors + auto_skill_selectors:
		if is_instance_valid(control):
			control.disabled = value
	for button in auto_start_buttons:
		if is_instance_valid(button):
			button.text = "자동 단조 중지" if value else "자동 단조 시작"
	if normal_button != null:
		normal_button.disabled = value
	if special_start_button != null:
		special_start_button.disabled = value
	if secondary_select != null:
		secondary_select.disabled = value or session.state == EnhancementSessionScript.State.PRECISION
	if catalyst_select != null:
		catalyst_select.disabled = value or session.state == EnhancementSessionScript.State.PRECISION
	_update_manual_attempt_buttons()
	_update_inventory_buttons()


func build_weapon_record() -> Dictionary:
	if session == null or bool(session.destroyed):
		return {}
	var snapshot: Dictionary = session.snapshot()
	return {
		"record_id": "%s-%d-%d" % [
			str(snapshot.get("weapon_id", "weapon")),
			int(snapshot.get("enhancement_level", 0)),
			Time.get_ticks_msec(),
		],
		"weapon_id": str(snapshot.get("weapon_id", "iron_sword")),
		"base_weapon_name": str(snapshot.get("base_weapon_name", "철검")),
		"weapon_name": str(snapshot.get("display_name", "철검 +0")),
		"enhancement_level": int(snapshot.get("enhancement_level", 0)),
		"raw_base_attack": int(snapshot.get("raw_base_attack", snapshot.get("base_attack", 10))),
		"base_attack": int(snapshot.get("base_attack", 10)),
		"quality_attack_multiplier": float(snapshot.get("quality_attack_multiplier", 1.0)),
		"quality_value_multiplier": float(snapshot.get("quality_value_multiplier", 1.0)),
		"progression_attack": int(snapshot.get("progression_attack", 10)),
		"enhancement_bonus": int(snapshot.get("enhancement_bonus", 0)),
		"final_attack": int(snapshot.get("final_attack", 10)),
		"sale_price": int(snapshot.get("sale_price", 0)),
		"total_spent": int(snapshot.get("total_spent", 0)),
		"estimated_profit": int(snapshot.get("sale_price", 0)) - int(snapshot.get("total_spent", 0)),
		"affixes": snapshot.get("affixes", []).duplicate(true),
		"special_effect_text": _format_special_effects(snapshot.get("affixes", [])),
		"catalyst_history": snapshot.get("catalyst_history", []).duplicate(true),
		"quality_id": str(weapon_result.get("quality_id", "STANDARD")),
		"quality_label": str(weapon_result.get("quality_label", "보통 마감")),
		"quality_multiplier": float(weapon_result.get("quality_multiplier", 1.0)),
		"material_scores": snapshot.get("lifetime_material_scores", {}).duplicate(true),
	}


func _attach_progression_panels() -> void:
	var normal_layout := _layout_for(normal_root)
	if normal_layout != null:
		normal_layout.add_child(_build_skill_panel())
		var panel := _panel(PANEL_ALT)
		normal_layout.add_child(panel)
		var box := VBoxContainer.new()
		box.add_theme_constant_override("separation", 8)
		panel.add_child(box)
		box.add_child(_center_label("현재 / 다음 강화", 22, GOLD))
		normal_current_label = _center_label("현재 공격력 10 · 가치 0G", 19, TEXT)
		normal_current_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(normal_current_label)
		normal_next_label = _center_label("다음 강화 효과", 19, GOLD)
		normal_next_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(normal_next_label)
		normal_price_label = _center_label("다음 가치", 17, TEXT)
		normal_price_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(normal_price_label)
		normal_cost_label = _center_label("강화 비용", 17, MUTED)
		box.add_child(normal_cost_label)
		normal_risk_label = _center_label("성공 / 유지 / 하락 / 파괴", 17, MUTED)
		normal_risk_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(normal_risk_label)
		normal_layout.add_child(_build_auto_panel())
		_add_inventory_actions(normal_layout)

	var special_layout := _layout_for(special_root)
	if special_layout != null:
		special_layout.add_child(_build_skill_panel())
		var panel := _panel(PANEL_ALT)
		special_layout.add_child(panel)
		var box := VBoxContainer.new()
		box.add_theme_constant_override("separation", 8)
		panel.add_child(box)
		box.add_child(_center_label("특수 강화 결과 미리보기", 22, GOLD))
		special_current_label = _center_label("현재 공격력 10 · 가치 0G", 18, TEXT)
		special_current_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(special_current_label)
		special_next_label = _center_label("성공 시 공격력", 20, GOLD)
		special_next_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(special_next_label)
		special_price_label = _center_label("성공 시 가치", 18, TEXT)
		special_price_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(special_price_label)
		special_catalyst_label = _center_label("촉매: 사용하지 않음 · 가격 0G", 17, MUTED)
		special_catalyst_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(special_catalyst_label)
		special_effect_label = _center_label("특수 강화 효과", 17, TEXT)
		special_effect_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(special_effect_label)
		special_cost_label = _center_label("총 강화 비용", 17, MUTED)
		box.add_child(special_cost_label)
		special_risk_label = _center_label("성공 / 유지 / 하락 / 파괴", 17, RED)
		special_risk_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(special_risk_label)
		special_layout.add_child(_build_auto_panel())
		_add_inventory_actions(special_layout)

	var complete_layout := _layout_for(complete_root)
	if complete_layout != null:
		if complete_layout.get_child_count() > 0:
			complete_title_label = complete_layout.get_child(0) as Label
		var panel := _panel(PANEL_ALT)
		complete_layout.add_child(panel)
		var box := VBoxContainer.new()
		box.add_theme_constant_override("separation", 8)
		panel.add_child(box)
		box.add_child(_center_label("최종 가치", 22, GOLD))
		complete_value_label = _center_label("공격력 · 판매가 · 누적비용", 19, TEXT)
		complete_value_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(complete_value_label)
		complete_effect_label = _center_label("특수 강화 효과", 17, MUTED)
		complete_effect_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		box.add_child(complete_effect_label)
		_add_inventory_actions(complete_layout)


func _build_auto_panel() -> PanelContainer:
	var panel := _panel(PANEL)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 9)
	panel.add_child(box)
	box.add_child(_center_label("자동 단조", 21, GOLD))

	var resource_label := _center_label("보유 골드 0G", 16, TEXT)
	resource_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(resource_label)
	auto_resource_labels.append(resource_label)

	var target_row := HBoxContainer.new()
	target_row.add_theme_constant_override("separation", 10)
	box.add_child(target_row)
	var target_label := _label("목표 단계", 17, MUTED)
	target_label.custom_minimum_size = Vector2(125.0, 0.0)
	target_row.add_child(target_label)
	var target_spin := SpinBox.new()
	target_spin.min_value = 1.0
	target_spin.max_value = 100.0
	target_spin.step = 1.0
	target_spin.value = 10.0
	target_spin.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	target_spin.custom_minimum_size = Vector2(0.0, 58.0)
	target_spin.add_theme_font_size_override("font_size", 18)
	target_row.add_child(target_spin)
	auto_target_spins.append(target_spin)

	var repeat_check := CheckButton.new()
	repeat_check.text = "보관함이 찰 때까지 자동 반복"
	repeat_check.add_theme_font_size_override("font_size", 17)
	box.add_child(repeat_check)
	auto_repeat_checks.append(repeat_check)

	var secondary := _auto_option_row(box, "보조재료")
	secondary.add_item("사용하지 않음")
	secondary.set_item_metadata(0, "")
	for item in secondary_materials:
		secondary.add_item("%s · 보유 %d" % [str(item.get("name", "재료")), int(material_stock.get(str(item.get("id", "")), 0))])
		secondary.set_item_metadata(secondary.item_count - 1, str(item.get("id", "")))
	if secondary.item_count > 1:
		secondary.select(1)
	auto_secondary_selectors.append(secondary)

	var catalyst := _auto_option_row(box, "촉매")
	catalyst.add_item("사용하지 않음")
	catalyst.set_item_metadata(0, "")
	for item in catalyst_materials:
		catalyst.add_item("%s · 보유 %d" % [str(item.get("name", "촉매")), int(material_stock.get(str(item.get("id", "")), 0))])
		catalyst.set_item_metadata(catalyst.item_count - 1, str(item.get("id", "")))
	auto_catalyst_selectors.append(catalyst)

	var skill := _auto_option_row(box, "단조 방식")
	var skills: Dictionary = session.config.get("skills", {}) if session != null else {}
	for skill_id_value in skills:
		var skill_id := str(skill_id_value)
		var skill_data: Dictionary = skills[skill_id_value]
		skill.add_item(str(skill_data.get("name", skill_id)))
		skill.set_item_metadata(skill.item_count - 1, skill_id)
	auto_skill_selectors.append(skill)

	var helper := _center_label("특수 강화에서 지정 재료가 부족하면 해당 재료 없이 계속 진행합니다.", 15, MUTED)
	helper.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(helper)

	var status := _center_label("목표와 재료를 정한 뒤 시작하세요.", 16, MUTED)
	status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(status)
	auto_status_labels.append(status)

	var start_button := Button.new()
	start_button.text = "자동 단조 시작"
	start_button.custom_minimum_size = Vector2(0.0, 78.0)
	start_button.add_theme_font_size_override("font_size", 21)
	start_button.add_theme_stylebox_override("normal", _button_style(Color("#3d7045"), GREEN, 17))
	start_button.pressed.connect(func() -> void: _on_auto_button_pressed(target_spin, repeat_check, secondary, catalyst, skill))
	box.add_child(start_button)
	auto_start_buttons.append(start_button)
	return panel


func _auto_option_row(parent: VBoxContainer, title: String) -> OptionButton:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 10)
	parent.add_child(row)
	var label := _label(title, 17, MUTED)
	label.custom_minimum_size = Vector2(125.0, 0.0)
	row.add_child(label)
	var option := _option_button()
	option.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(option)
	return option


func _on_auto_button_pressed(
	target_spin: SpinBox,
	repeat_check: CheckButton,
	secondary: OptionButton,
	catalyst: OptionButton,
	skill: OptionButton
) -> void:
	if auto_running:
		auto_forge_requested.emit({"stop": true})
		return
	var target_level := int(target_spin.value)
	if session != null:
		target_level = maxi(target_level, int(session.enhancement_level) + 1)
	auto_forge_requested.emit({
		"target_level": target_level,
		"repeat_until_full": repeat_check.button_pressed,
		"secondary_material_id": str(secondary.get_item_metadata(secondary.selected)),
		"catalyst_material_id": str(catalyst.get_item_metadata(catalyst.selected)),
		"skill_id": str(skill.get_item_metadata(skill.selected)),
	})


func _update_auto_resource_labels() -> void:
	var parts: Array[String] = []
	for item in secondary_materials + catalyst_materials:
		var material_id := str(item.get("id", ""))
		parts.append("%s %d" % [str(item.get("name", material_id)), int(material_stock.get(material_id, 0))])
	var text_value := "보유 골드 %sG\n%s" % [_money(available_gold), " · ".join(parts)]
	for label in auto_resource_labels:
		if is_instance_valid(label):
			label.text = text_value
	for selector in auto_secondary_selectors + auto_catalyst_selectors:
		if not is_instance_valid(selector):
			continue
		for index in range(selector.item_count):
			var material_id := str(selector.get_item_metadata(index))
			if material_id == "":
				continue
			var material_name := _material_display_name(material_id)
			selector.set_item_text(index, "%s · 보유 %d" % [material_name, int(material_stock.get(material_id, 0))])


func _material_display_name(material_id: String) -> String:
	for item in secondary_materials + catalyst_materials:
		if str(item.get("id", "")) == material_id:
			return str(item.get("name", material_id))
	return material_id



func _update_manual_material_selectors() -> void:
	if session == null:
		return
	_sync_material_selector_stock(secondary_select, false)
	_sync_material_selector_stock(catalyst_select, true)


func _sync_material_selector_stock(selector: OptionButton, allow_empty: bool) -> void:
	if selector == null or not is_instance_valid(selector):
		return
	var selected_id := str(session.selected_catalyst_id if allow_empty else session.selected_secondary_id)
	var selected_index := -1
	var first_available := 0 if allow_empty else -1
	for index in range(selector.item_count):
		var material_id := str(selector.get_item_metadata(index))
		if material_id == "":
			selector.set_item_disabled(index, false)
			if selected_id == "":
				selected_index = index
			continue
		var stock := int(material_stock.get(material_id, 0))
		selector.set_item_text(index, "%s · 보유 %d" % [_material_display_name(material_id), stock])
		selector.set_item_disabled(index, stock <= 0)
		if material_id == selected_id:
			selected_index = index
		if stock > 0 and first_available < 0:
			first_available = index
	if selected_index >= 0:
		selector.select(selected_index)
	var target_level := int(session.enhancement_level) + 1
	var can_change := (
		session.state == EnhancementSessionScript.State.READY
		and session.uses_materials_for_level(target_level)
	)
	if not can_change:
		return
	var selected_available := selected_id == "" and allow_empty
	if selected_id != "" and selected_index >= 0:
		selected_available = not selector.is_item_disabled(selected_index)
	if selected_available or first_available < 0:
		return
	selector.select(first_available)
	var fallback_id := str(selector.get_item_metadata(first_available))
	if allow_empty:
		session.set_catalyst_material(fallback_id)
	else:
		session.set_secondary_material(fallback_id)


func _update_manual_attempt_buttons() -> void:
	if session == null:
		return
	var transaction: Dictionary = {}
	if workshop_resources != null:
		transaction = workshop_resources.preview_attempt(session)
	var can_start := workshop_resources != null and bool(transaction.get("ok", false)) and not auto_running
	if normal_button != null and session.state == EnhancementSessionScript.State.READY and not session.uses_materials_for_level(session.enhancement_level + 1):
		normal_button.disabled = not can_start
	if special_start_button != null and session.state == EnhancementSessionScript.State.READY and session.uses_materials_for_level(session.enhancement_level + 1):
		special_start_button.disabled = not can_start


func _build_skill_panel() -> PanelContainer:
	var panel := _panel(PANEL)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 8)
	panel.add_child(box)
	box.add_child(_center_label("강화 기술", 20, GOLD))

	var selector := OptionButton.new()
	selector.custom_minimum_size = Vector2(0.0, 62.0)
	selector.add_theme_font_size_override("font_size", 18)
	selector.add_theme_stylebox_override("normal", _button_style(PANEL_ALT, BLUE, 14))
	selector.item_selected.connect(func(index: int) -> void: _on_skill_selected(selector, index))
	box.add_child(selector)
	skill_selectors.append(selector)

	var description := _center_label("", 15, MUTED)
	description.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(description)
	skill_description_labels.append(description)
	return panel


func _populate_skill_selectors() -> void:
	if session == null:
		return
	var skills_value = session.config.get("skills", {})
	if skills_value is not Dictionary:
		return
	var skills: Dictionary = skills_value
	for selector in skill_selectors:
		selector.clear()
		for skill_id_value in skills:
			var skill_id := str(skill_id_value)
			var skill: Dictionary = skills[skill_id_value]
			selector.add_item(str(skill.get("name", skill_id)))
			selector.set_item_metadata(selector.item_count - 1, skill_id)
	_sync_skill_selectors()


func _on_skill_selected(source: OptionButton, index: int) -> void:
	if session == null:
		return
	var skill_id := str(source.get_item_metadata(index))
	if session.set_skill(skill_id):
		_sync_skill_selectors()


func _sync_skill_selectors() -> void:
	if session == null:
		return
	var target_level := int(session.enhancement_level) + 1
	for selector in skill_selectors:
		for index in range(selector.item_count):
			var skill_id := str(selector.get_item_metadata(index))
			selector.set_item_disabled(index, not session.can_use_skill_for_level(skill_id, target_level))
			if skill_id == str(session.selected_skill_id):
				selector.select(index)
	var skill: Dictionary = session.config.get("skills", {}).get(str(session.selected_skill_id), {})
	var description := str(skill.get("description", ""))
	if str(session.selected_skill_id) == "overdrive" and not session.can_use_skill_for_level("overdrive", target_level):
		description += "\n현재 단계에서는 특수 강화를 건너뛸 수 있어 사용 불가"
	for label in skill_description_labels:
		if is_instance_valid(label):
			label.text = description


func _add_inventory_actions(layout: VBoxContainer) -> void:
	var actions := HBoxContainer.new()
	actions.add_theme_constant_override("separation", 10)
	layout.add_child(actions)

	var inventory_button := Button.new()
	inventory_button.text = "보관함 %d/%d" % [inventory_count, inventory_capacity]
	inventory_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	inventory_button.custom_minimum_size = Vector2(0.0, 76.0)
	inventory_button.add_theme_font_size_override("font_size", 19)
	inventory_button.add_theme_stylebox_override("normal", _button_style(PANEL, BLUE, 16))
	inventory_button.pressed.connect(func() -> void: inventory_requested.emit())
	actions.add_child(inventory_button)
	inventory_buttons.append(inventory_button)

	var store_button := Button.new()
	store_button.text = "강화 종료 및 보관"
	store_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	store_button.custom_minimum_size = Vector2(0.0, 76.0)
	store_button.add_theme_font_size_override("font_size", 19)
	store_button.add_theme_color_override("font_color", Color("#241b0f"))
	store_button.add_theme_stylebox_override("normal", _button_style(GOLD, Color.WHITE, 16))
	store_button.pressed.connect(_on_store_pressed)
	actions.add_child(store_button)
	store_buttons.append(store_button)


func _layout_for(root: Control) -> VBoxContainer:
	if root == null or root.get_child_count() == 0:
		return null
	var scroll := root.get_child(0) as ScrollContainer
	if scroll == null or scroll.get_child_count() == 0:
		return null
	return scroll.get_child(0) as VBoxContainer


func _center_label(text_value: String, font_size: int, color: Color) -> Label:
	var label := _label(text_value, font_size, color)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	return label


func _on_store_pressed() -> void:
	if inventory_count >= inventory_capacity or session == null or bool(session.destroyed):
		return
	var record := build_weapon_record()
	if not record.is_empty():
		store_requested.emit(record)



func _on_normal_pressed() -> void:
	if session == null or session.state != EnhancementSessionScript.State.READY:
		return
	if session.uses_materials_for_level(session.enhancement_level + 1):
		return
	_try_begin_paid_attempt()


func _on_special_start_pressed() -> void:
	if session == null or session.state != EnhancementSessionScript.State.READY:
		return
	if not session.uses_materials_for_level(session.enhancement_level + 1):
		return
	_try_begin_paid_attempt()


func _try_begin_paid_attempt() -> void:
	if workshop_resources == null:
		last_result_text = "대장간 자원 상태를 찾지 못해 강화를 시작할 수 없습니다."
		last_result_color = RED
		_update_result_labels()
		return
	var transaction: Dictionary = workshop_resources.try_begin_attempt(session)
	if not bool(transaction.get("ok", false)):
		_show_transaction_failure(transaction)
		return
	_refresh(session.snapshot())


func _show_transaction_failure(transaction: Dictionary) -> void:
	match str(transaction.get("status", "")):
		WorkshopResourcesScript.STATUS_NO_GOLD:
			last_result_text = "골드 부족 · 필요 %sG / 보유 %sG" % [
				_money(int(transaction.get("cost", 0))),
				_money(int(transaction.get("available_gold", available_gold))),
			]
		WorkshopResourcesScript.STATUS_NO_MATERIAL:
			var material_id := str(transaction.get("material_id", ""))
			last_result_text = "재료 부족 · %s 재고가 없어 특수 강화를 시작할 수 없습니다." % _material_display_name(material_id)
		_:
			last_result_text = "현재 상태에서는 강화를 시작할 수 없습니다."
	last_result_color = RED
	_update_result_labels()
	_update_manual_attempt_buttons()


func _on_attempt_resolved(result: Dictionary) -> void:
	var target_level := int(result.get("target_level", 0))
	var outcome := str(result.get("outcome", "HOLD"))
	match outcome:
		"SUCCESS":
			if bool(result.get("leap_triggered", false)):
				last_result_text = "폭주 도약 성공! +%d → +%d · 공격력 +%d · 비용 %dG" % [
					int(result.get("previous_level", 0)),
					int(result.get("result_level", target_level)),
					int(result.get("growth_gain", 0)),
					int(result.get("attempt_cost", 0)),
				]
			else:
				last_result_text = "강화 성공! +%d · 공격력 +%d · 비용 %dG" % [
					target_level,
					int(result.get("growth_gain", 0)),
					int(result.get("attempt_cost", 0)),
				]
			last_result_color = GREEN
		"DOWNGRADE":
			last_result_text = "강화 실패 · +%d → +%d · %d단계 하락" % [
				int(result.get("previous_level", 0)),
				int(result.get("result_level", 0)),
				int(result.get("downgrade_steps", 0)),
			]
			last_result_color = RED
		"DESTROY":
			last_result_text = "강화 실패 · 무기가 파괴됐습니다."
			last_result_color = RED
		_:
			last_result_text = "강화 실패 · 단계 유지 · 실패 보정이 누적됩니다."
			last_result_color = RED
	_refresh(session.snapshot())


func _on_session_snapshot_changed(snapshot: Dictionary) -> void:
	_sync_skill_selectors()
	var current_attack := int(snapshot.get("final_attack", 0))
	var current_price := int(snapshot.get("sale_price", 0))
	var total_spent := int(snapshot.get("total_spent", 0))
	var preview: Dictionary = snapshot.get("next_preview", {})
	var outcome: Dictionary = snapshot.get("outcome_probabilities", {})
	var target_level := int(snapshot.get("target_level", 0))
	var gain := int(preview.get("growth_gain", 0))
	var next_attack := int(preview.get("final_attack", current_attack))
	var next_price := int(preview.get("sale_price", current_price))
	var price_gain := int(preview.get("sale_price_gain", 0))
	var attempt_cost := int(preview.get("attempt_cost", snapshot.get("attempt_cost", 0)))
	var growth_percent := float(preview.get("growth_percent", 0.0)) * 100.0

	var current_text := "현재 공격력 %d · 판매가 %sG" % [current_attack, _money(current_price)]
	var next_text := "+%d 성공 시 공격력 +%d (%.1f%%) · %d → %d" % [
		target_level,
		gain,
		growth_percent,
		current_attack,
		next_attack,
	]
	var leap_chance := float(preview.get("leap_chance", 0.0))
	if leap_chance > 0.0:
		next_text += "\n폭주 도약 %d%% · 성공 시 +%d까지 · 공격력 %d" % [
			int(round(leap_chance * 100.0)),
			int(preview.get("leap_result_level", target_level)),
			int(preview.get("leap_final_attack", next_attack)),
		]
	var price_text := "판매가 %sG → %sG (+%sG)" % [
		_money(current_price),
		_money(next_price),
		_money(price_gain),
	]
	var cost_text := "시도 비용 %sG · 보유 %sG · 누적 사용 %sG" % [_money(attempt_cost), _money(available_gold), _money(total_spent)]
	var risk_text := _format_risk(outcome)

	if normal_current_label != null:
		normal_current_label.text = current_text
	if normal_next_label != null:
		normal_next_label.text = next_text
	if normal_price_label != null:
		normal_price_label.text = price_text
	if normal_cost_label != null:
		normal_cost_label.text = cost_text
	if normal_risk_label != null:
		normal_risk_label.text = risk_text

	if special_current_label != null:
		special_current_label.text = current_text
	if special_next_label != null:
		special_next_label.text = next_text
	if special_price_label != null:
		special_price_label.text = price_text
	if special_cost_label != null:
		special_cost_label.text = cost_text
	if special_risk_label != null:
		special_risk_label.text = risk_text
	if special_catalyst_label != null:
		special_catalyst_label.text = _format_catalyst(snapshot.get("selected_catalyst", {}))
	if special_effect_label != null:
		var current_effect := _format_special_effects(snapshot.get("affixes", []))
		var next_effect := _format_special_effects(preview.get("affixes", snapshot.get("affixes", [])))
		special_effect_label.text = "현재 특수 효과: %s\n성공 시 특수 효과: %s" % [current_effect, next_effect]

	if complete_title_label != null:
		complete_title_label.text = "무기 파괴" if bool(snapshot.get("destroyed", false)) else "최대 강화 완료"
	if complete_value_label != null:
		if bool(snapshot.get("destroyed", false)):
			complete_value_label.text = "공격력 0 · 판매가 0G · 누적 사용 %sG" % _money(total_spent)
		else:
			complete_value_label.text = "최종 공격력 %d · 판매가 %sG · 누적 사용 %sG" % [
				current_attack,
				_money(current_price),
				_money(total_spent),
			]
	if complete_effect_label != null:
		complete_effect_label.text = (
			"파괴된 무기는 보관할 수 없습니다."
			if bool(snapshot.get("destroyed", false))
			else "특수 강화 효과: %s" % _format_special_effects(snapshot.get("affixes", []))
		)
	for target_spin in auto_target_spins:
		if is_instance_valid(target_spin):
			target_spin.min_value = float(mini(int(snapshot.get("enhancement_level", 0)) + 1, int(snapshot.get("max_level", 100))))
	_update_auto_resource_labels()
	_update_manual_material_selectors()
	_update_manual_attempt_buttons()
	_update_inventory_buttons()


func _update_inventory_buttons() -> void:
	var destroyed_now := session != null and bool(session.destroyed)
	for button in inventory_buttons:
		if is_instance_valid(button):
			button.text = "보관함 %d/%d" % [inventory_count, inventory_capacity]
	for button in store_buttons:
		if is_instance_valid(button):
			button.disabled = inventory_count >= inventory_capacity or destroyed_now or auto_running
			if destroyed_now:
				button.text = "파괴된 무기"
			elif auto_running:
				button.text = "자동 단조 진행 중"
			elif inventory_count >= inventory_capacity:
				button.text = "보관함 가득 참"
			else:
				button.text = "강화 종료 및 보관"


func _format_risk(probabilities: Dictionary) -> String:
	var downgrade_steps := int(probabilities.get("downgrade_steps", 0))
	return "성공 %d%% · 유지 %d%% · 하락 %d%% (-%d) · 파괴 %d%%" % [
		int(round(float(probabilities.get("success", 0.0)) * 100.0)),
		int(round(float(probabilities.get("hold", 0.0)) * 100.0)),
		int(round(float(probabilities.get("downgrade", 0.0)) * 100.0)),
		downgrade_steps,
		int(round(float(probabilities.get("destroy", 0.0)) * 100.0)),
	]


func _format_catalyst(value) -> String:
	if value is not Dictionary or value.is_empty():
		return "촉매: 사용하지 않음 · 가격 0G · 추가 효과 없음"
	var catalyst: Dictionary = value
	return "촉매: %s · 가격 %sG\n%s" % [
		str(catalyst.get("name", "촉매")),
		_money(int(catalyst.get("price", 0))),
		str(catalyst.get("description", "추가 효과 없음")),
	]


func _format_special_effects(affix_list: Array) -> String:
	if affix_list.is_empty():
		return "없음"
	var parts: Array[String] = []
	for value in affix_list:
		if value is not Dictionary:
			continue
		var affix: Dictionary = value
		var effect_parts: Array[String] = []
		var effects: Dictionary = affix.get("effects", {})
		if effects.has("attack_percent"):
			effect_parts.append("공격력 +%d%%" % int(round(float(effects["attack_percent"]) * 100.0)))
		if effects.has("fire_damage"):
			effect_parts.append("화염 피해 +%d" % int(effects["fire_damage"]))
		if effects.has("special_trigger_chance"):
			effect_parts.append("특수 발동 확률 +%d%%" % int(round(float(effects["special_trigger_chance"]) * 100.0)))
		if effect_parts.is_empty():
			effect_parts.append("효과 없음")
		parts.append("%s %d티어 · %s" % [
			str(affix.get("name", "수식어")),
			int(affix.get("tier", 1)),
			" / ".join(effect_parts),
		])
	return "\n".join(parts)


func _money(value: int) -> String:
	var negative := value < 0
	var digits := str(absi(value))
	var chunks: Array[String] = []
	while digits.length() > 3:
		chunks.push_front(digits.right(3))
		digits = digits.left(digits.length() - 3)
	chunks.push_front(digits)
	return "%s%s" % ["-" if negative else "", ",".join(chunks)]
