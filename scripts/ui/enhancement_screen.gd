# 일반/특수 강화 화면에 능력치 요약과 보관 동작을 추가하는 호환 진입점입니다.
class_name EnhancementScreen
extends "res://scripts/ui/special_enhancement_screen.gd"

signal store_requested(weapon: Dictionary)
signal inventory_requested

const BASE_ATTACK := 10
const ATTACK_PER_LEVEL := 3
const SPECIAL_ATTACK_BONUS := 5
const INVENTORY_CAPACITY := 6

var inventory_count: int = 0
var inventory_capacity: int = INVENTORY_CAPACITY
var store_buttons: Array[Button] = []
var inventory_buttons: Array[Button] = []

var normal_stat_label: Label
var normal_effect_label: Label
var special_current_label: Label
var special_next_label: Label
var special_effect_label: Label
var complete_stat_label: Label
var complete_effect_label: Label


func _ready() -> void:
	super._ready()
	_attach_effect_panels()
	if session != null:
		session.changed.connect(_on_session_snapshot_changed)
		_on_session_snapshot_changed(session.snapshot())
	_update_inventory_buttons()


func set_inventory_count(count: int, capacity: int = INVENTORY_CAPACITY) -> void:
	inventory_count = maxi(count, 0)
	inventory_capacity = maxi(capacity, 1)
	_update_inventory_buttons()


func build_weapon_record() -> Dictionary:
	if session == null:
		return {}
	var snapshot: Dictionary = session.snapshot()
	var level := int(snapshot.get("enhancement_level", 0))
	var affix_list: Array = snapshot.get("affixes", [])
	var bonus := _enhancement_bonus(level)
	return {
		"record_id": "%s-%d-%d" % [str(snapshot.get("weapon_id", "weapon")), level, Time.get_ticks_msec()],
		"weapon_id": str(snapshot.get("weapon_id", "iron_sword")),
		"base_weapon_name": str(snapshot.get("base_weapon_name", "철검")),
		"weapon_name": str(snapshot.get("display_name", "철검 +0")),
		"enhancement_level": level,
		"base_attack": BASE_ATTACK,
		"enhancement_bonus": bonus,
		"final_attack": _final_attack(level, affix_list),
		"affixes": affix_list.duplicate(true),
		"special_effect_text": _format_special_effects(affix_list),
		"quality_id": str(weapon_result.get("quality_id", "STANDARD")),
		"quality_label": str(weapon_result.get("quality_label", "보통 마감")),
		"quality_multiplier": float(weapon_result.get("quality_multiplier", 1.0)),
		"material_scores": snapshot.get("lifetime_material_scores", {}).duplicate(true),
	}


func _attach_effect_panels() -> void:
	var normal_layout := _layout_for(normal_root)
	if normal_layout != null:
		var normal_panel := _panel(PANEL_ALT)
		normal_layout.add_child(normal_panel)
		var normal_box := VBoxContainer.new()
		normal_box.add_theme_constant_override("separation", 8)
		normal_panel.add_child(normal_box)
		normal_box.add_child(_center_label("강화 효과", 22, GOLD))
		normal_stat_label = _center_label("기본 공격력 10 (+0)", 20, TEXT)
		normal_box.add_child(normal_stat_label)
		normal_effect_label = _center_label("특수 강화 효과: 없음", 17, MUTED)
		normal_effect_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		normal_box.add_child(normal_effect_label)
		_add_inventory_actions(normal_layout)

	var special_layout := _layout_for(special_root)
	if special_layout != null:
		var special_panel := _panel(PANEL_ALT)
		special_layout.add_child(special_panel)
		var special_box := VBoxContainer.new()
		special_box.add_theme_constant_override("separation", 8)
		special_panel.add_child(special_box)
		special_box.add_child(_center_label("특수 강화 효과 미리보기", 22, GOLD))
		special_current_label = _center_label("현재 기본 공격력 10 (+0)", 18, TEXT)
		special_box.add_child(special_current_label)
		special_next_label = _center_label("성공 시 기본 공격력 10 (+35)", 20, GOLD)
		special_box.add_child(special_next_label)
		special_effect_label = _center_label("특수 강화 효과: 재료 선택에 따라 결정", 17, MUTED)
		special_effect_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		special_box.add_child(special_effect_label)
		_add_inventory_actions(special_layout)

	var complete_layout := _layout_for(complete_root)
	if complete_layout != null:
		var complete_panel := _panel(PANEL_ALT)
		complete_layout.add_child(complete_panel)
		var complete_box := VBoxContainer.new()
		complete_box.add_theme_constant_override("separation", 8)
		complete_panel.add_child(complete_box)
		complete_box.add_child(_center_label("최종 강화 효과", 22, GOLD))
		complete_stat_label = _center_label("기본 공격력 10", 20, TEXT)
		complete_box.add_child(complete_stat_label)
		complete_effect_label = _center_label("특수 강화 효과", 17, MUTED)
		complete_effect_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		complete_box.add_child(complete_effect_label)
		_add_inventory_actions(complete_layout)


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
	if inventory_count >= inventory_capacity:
		return
	var record := build_weapon_record()
	if not record.is_empty():
		store_requested.emit(record)


func _on_session_snapshot_changed(snapshot: Dictionary) -> void:
	var level := int(snapshot.get("enhancement_level", 0))
	var target_level := int(snapshot.get("target_level", level))
	var affix_list: Array = snapshot.get("affixes", [])
	var bonus := _enhancement_bonus(level)
	var final_attack := _final_attack(level, affix_list)
	var effect_text := _format_special_effects(affix_list)

	if normal_stat_label != null:
		normal_stat_label.text = "기본 공격력 %d (+%d) · 강화 적용 %d" % [BASE_ATTACK, bonus, final_attack]
	if normal_effect_label != null:
		normal_effect_label.text = "특수 강화 효과: %s" % effect_text

	if special_current_label != null:
		special_current_label.text = "현재 기본 공격력 %d (+%d)" % [BASE_ATTACK, bonus]
	if special_next_label != null:
		var target_bonus := _enhancement_bonus(target_level)
		special_next_label.text = "성공 시 기본 공격력 %d (+%d) · 적용 %d" % [
			BASE_ATTACK,
			target_bonus,
			_final_attack(target_level, affix_list),
		]
	if special_effect_label != null:
		var preview: Dictionary = snapshot.get("milestone_preview", {})
		var preview_text := _format_milestone_preview(preview)
		special_effect_label.text = "현재 효과: %s\n성공 시: %s" % [effect_text, preview_text]

	if complete_stat_label != null:
		complete_stat_label.text = "기본 공격력 %d (+%d) · 강화 적용 %d" % [BASE_ATTACK, bonus, final_attack]
	if complete_effect_label != null:
		complete_effect_label.text = "특수 강화 효과: %s" % effect_text


func _update_inventory_buttons() -> void:
	for button in inventory_buttons:
		if is_instance_valid(button):
			button.text = "보관함 %d/%d" % [inventory_count, inventory_capacity]
	for button in store_buttons:
		if is_instance_valid(button):
			button.disabled = inventory_count >= inventory_capacity
			button.text = "보관함 가득 참" if button.disabled else "강화 종료 및 보관"


func _enhancement_bonus(level: int) -> int:
	return maxi(level, 0) * ATTACK_PER_LEVEL + maxi(level, 0) / 10 * SPECIAL_ATTACK_BONUS


func _final_attack(level: int, affix_list: Array) -> int:
	var attack_percent := 0.0
	for value in affix_list:
		if value is Dictionary:
			var affix: Dictionary = value
			var effects: Dictionary = affix.get("effects", {})
			attack_percent += float(effects.get("attack_percent", 0.0))
	return int(round(float(BASE_ATTACK + _enhancement_bonus(level)) * (1.0 + attack_percent)))


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
		parts.append("%s %d티어 · %s" % [
			str(affix.get("name", "수식어")),
			int(affix.get("tier", 1)),
			" / ".join(effect_parts),
		])
	return "\n".join(parts)
