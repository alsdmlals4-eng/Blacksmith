class_name EnhancementScreen
extends Control

signal restart_requested

const EnhancementSessionScript = preload("res://scripts/enhancement/enhancement_session.gd")
const PrecisionGaugeScript = preload("res://scripts/ui/precision_gauge.gd")

const BG := Color("#17191f")
const PANEL := Color("#252932")
const PANEL_ALT := Color("#303641")
const TEXT := Color("#f4f1e8")
const MUTED := Color("#b7b0a3")
const ORANGE := Color("#d7772e")
const GOLD := Color("#f2c14e")
const RED := Color("#e36c62")
const GREEN := Color("#72b879")
const BLUE := Color("#62a7d8")

var weapon_result: Dictionary = {}
var session
var secondary_materials: Array[Dictionary] = []
var catalyst_materials: Array[Dictionary] = []

var level_label: Label
var weapon_name_label: Label
var milestone_preview_label: Label
var progress_bar: ProgressBar
var progress_label: Label
var cadence_label: Label
var material_panel: PanelContainer
var secondary_select: OptionButton
var catalyst_select: OptionButton
var chance_label: Label
var attempt_button: Button
var attempt_result_label: Label
var precision_panel: PanelContainer
var precision_gauge
var complete_panel: PanelContainer
var complete_name_label: Label
var complete_affix_label: Label
var complete_stats_label: Label
var helper_label: Label
var last_state: int = -1


func configure_weapon(result: Dictionary) -> void:
	weapon_result = result.duplicate(true)


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var data := _load_enhancement_data()
	_build_interface()
	session = EnhancementSessionScript.new(data["config"], data["materials"], data["affixes"], weapon_result)
	session.attempt_resolved.connect(_on_attempt_resolved)
	_refresh(session.snapshot())
	set_process(true)


func _process(delta: float) -> void:
	if session == null:
		return
	session.advance(delta)
	_refresh(session.snapshot())


func _unhandled_input(event: InputEvent) -> void:
	if not visible or session == null or not event.is_action_pressed("forge_tap"):
		return
	if session.state == EnhancementSessionScript.State.PRECISION:
		_on_precision_pressed()
	elif session.state == EnhancementSessionScript.State.READY:
		_on_attempt_pressed()
	get_viewport().set_input_as_handled()


func _load_enhancement_data() -> Dictionary:
	var config_data := _read_json("res://data/crafting/enhancement_balance.json")
	var milestone_data := _read_json("res://data/crafting/enhancement_milestones.json")
	var materials_data := _read_json("res://data/crafting/materials.json")
	var affixes_data := _read_json("res://data/crafting/affixes.json")
	config_data["milestones"] = milestone_data.get("milestones", [])
	var materials: Array = materials_data.get("materials", [])
	secondary_materials.clear()
	catalyst_materials.clear()
	for item_value in materials:
		if item_value is not Dictionary:
			continue
		var item: Dictionary = item_value
		if "secondary" in item.get("slot_types", []):
			secondary_materials.append(item)
		if "catalyst" in item.get("slot_types", []):
			catalyst_materials.append(item)
	return {
		"config": config_data,
		"materials": materials,
		"affixes": affixes_data.get("affixes", []),
	}


func _read_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_warning("%s 파일을 읽지 못했습니다." % path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func _build_interface() -> void:
	var background := ColorRect.new()
	background.color = BG
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 26)
	margin.add_theme_constant_override("margin_right", 26)
	margin.add_theme_constant_override("margin_top", 28)
	margin.add_theme_constant_override("margin_bottom", 26)
	add_child(margin)

	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	margin.add_child(scroll)

	var layout := VBoxContainer.new()
	layout.custom_minimum_size = Vector2(660.0, 0.0)
	layout.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	layout.add_theme_constant_override("separation", 15)
	scroll.add_child(layout)

	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation", 12)
	layout.add_child(header)
	var title := _label("철검 강화 테스트", 30, TEXT)
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title)
	level_label = _label("+0", 25, GOLD)
	level_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	header.add_child(level_label)

	var weapon_panel := _panel(PANEL_ALT)
	layout.add_child(weapon_panel)
	var weapon_box := VBoxContainer.new()
	weapon_box.add_theme_constant_override("separation", 8)
	weapon_panel.add_child(weapon_box)
	weapon_name_label = _label("철검 +0", 28, GOLD)
	weapon_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	weapon_name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	weapon_box.add_child(weapon_name_label)
	milestone_preview_label = _label("+10 재료 이정표: 첫 수식어 추가", 18, TEXT)
	milestone_preview_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	milestone_preview_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	weapon_box.add_child(milestone_preview_label)

	var progress_panel := _panel(PANEL)
	layout.add_child(progress_panel)
	var progress_box := VBoxContainer.new()
	progress_box.add_theme_constant_override("separation", 8)
	progress_panel.add_child(progress_box)
	var progress_header := HBoxContainer.new()
	progress_box.add_child(progress_header)
	progress_header.add_child(_label("강화 단계", 18, TEXT))
	progress_label = _label("0 / 100", 18, GOLD)
	progress_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	progress_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	progress_header.add_child(progress_label)
	progress_bar = _progress_bar(ORANGE)
	progress_box.add_child(progress_bar)
	cadence_label = _label("4회 원클릭 → +5 정밀 → +10 재료 정밀", 16, MUTED)
	cadence_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cadence_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	progress_box.add_child(cadence_label)

	material_panel = _panel(PANEL_ALT)
	material_panel.visible = false
	layout.add_child(material_panel)
	var material_box := VBoxContainer.new()
	material_box.add_theme_constant_override("separation", 10)
	material_panel.add_child(material_box)
	var material_title := _label("+10 단위 강화 재료", 22, GOLD)
	material_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	material_box.add_child(material_title)
	var material_info := _label("보조재료와 촉매는 +10·+20·…·+100에서만 선택하고 적용합니다.", 16, MUTED)
	material_info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	material_info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	material_box.add_child(material_info)

	var secondary_row := HBoxContainer.new()
	secondary_row.add_theme_constant_override("separation", 12)
	material_box.add_child(secondary_row)
	var secondary_label := _label("보조재료", 18, MUTED)
	secondary_label.custom_minimum_size = Vector2(120.0, 0.0)
	secondary_row.add_child(secondary_label)
	secondary_select = _option_button()
	secondary_select.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	for item in secondary_materials:
		secondary_select.add_item(str(item.get("name", "재료")))
		secondary_select.set_item_metadata(secondary_select.item_count - 1, str(item.get("id", "")))
	secondary_select.item_selected.connect(_on_secondary_selected)
	secondary_row.add_child(secondary_select)

	var catalyst_row := HBoxContainer.new()
	catalyst_row.add_theme_constant_override("separation", 12)
	material_box.add_child(catalyst_row)
	var catalyst_label := _label("촉매", 18, MUTED)
	catalyst_label.custom_minimum_size = Vector2(120.0, 0.0)
	catalyst_row.add_child(catalyst_label)
	catalyst_select = _option_button()
	catalyst_select.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	catalyst_select.add_item("사용하지 않음")
	catalyst_select.set_item_metadata(0, "")
	for item in catalyst_materials:
		catalyst_select.add_item("%s · 성공률 +%d%%" % [
			str(item.get("name", "촉매")),
			int(round(float(item.get("success_bonus", 0.0)) * 100.0)),
		])
		catalyst_select.set_item_metadata(catalyst_select.item_count - 1, str(item.get("id", "")))
	catalyst_select.item_selected.connect(_on_catalyst_selected)
	catalyst_row.add_child(catalyst_select)

	chance_label = _label("원클릭 강화 성공률 98%", 20, GOLD)
	chance_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	chance_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(chance_label)

	attempt_result_label = _label("+1부터 시작합니다.", 18, MUTED)
	attempt_result_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	attempt_result_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(attempt_result_label)

	attempt_button = Button.new()
	attempt_button.text = "+1 원클릭 강화"
	attempt_button.custom_minimum_size = Vector2(0.0, 145.0)
	attempt_button.add_theme_font_size_override("font_size", 31)
	attempt_button.add_theme_color_override("font_color", TEXT)
	attempt_button.add_theme_stylebox_override("normal", _button_style(Color("#8d4424"), ORANGE, 24))
	attempt_button.add_theme_stylebox_override("hover", _button_style(Color("#a85129"), GOLD, 24))
	attempt_button.add_theme_stylebox_override("pressed", _button_style(Color("#6f331d"), GOLD, 24))
	attempt_button.pressed.connect(_on_attempt_pressed)
	layout.add_child(attempt_button)

	precision_panel = _panel(PANEL_ALT)
	precision_panel.visible = false
	layout.add_child(precision_panel)
	var precision_box := VBoxContainer.new()
	precision_box.add_theme_constant_override("separation", 10)
	precision_panel.add_child(precision_box)
	var precision_title := _label("정밀 강화", 24, GOLD)
	precision_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	precision_box.add_child(precision_title)
	var precision_instruction := _label("+5 단위에서 흰 포인터가 황금 구간에 들어왔을 때 타격하세요.", 17, MUTED)
	precision_instruction.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	precision_instruction.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	precision_box.add_child(precision_instruction)
	precision_gauge = PrecisionGaugeScript.new()
	precision_box.add_child(precision_gauge)
	var precision_button := Button.new()
	precision_button.text = "정밀 강화 타격!"
	precision_button.custom_minimum_size = Vector2(0.0, 90.0)
	precision_button.add_theme_font_size_override("font_size", 27)
	precision_button.add_theme_color_override("font_color", Color("#241b0f"))
	precision_button.add_theme_stylebox_override("normal", _button_style(GOLD, Color.WHITE, 20))
	precision_button.add_theme_stylebox_override("pressed", _button_style(Color("#c99835"), Color.WHITE, 20))
	precision_button.pressed.connect(_on_precision_pressed)
	precision_box.add_child(precision_button)

	complete_panel = _panel(PANEL_ALT)
	complete_panel.visible = false
	layout.add_child(complete_panel)
	var complete_box := VBoxContainer.new()
	complete_box.add_theme_constant_override("separation", 10)
	complete_panel.add_child(complete_box)
	complete_name_label = _label("철검 +100", 29, GOLD)
	complete_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	complete_name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	complete_box.add_child(complete_name_label)
	complete_affix_label = _label("최대 강화 완료", 21, TEXT)
	complete_affix_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	complete_affix_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	complete_box.add_child(complete_affix_label)
	complete_stats_label = _label("", 17, MUTED)
	complete_stats_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	complete_box.add_child(complete_stats_label)
	var restart_button := Button.new()
	restart_button.text = "새 철검 제작"
	restart_button.custom_minimum_size = Vector2(0.0, 84.0)
	restart_button.add_theme_font_size_override("font_size", 24)
	restart_button.add_theme_color_override("font_color", TEXT)
	restart_button.add_theme_stylebox_override("normal", _button_style(Color("#3d7045"), GREEN, 18))
	restart_button.pressed.connect(func() -> void: restart_requested.emit())
	complete_box.add_child(restart_button)

	helper_label = _label("+5 단위는 정밀 강화, +10 단위에서만 재료를 선택합니다.", 16, MUTED)
	helper_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	helper_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(helper_label)


func _on_secondary_selected(index: int) -> void:
	if session != null:
		session.set_secondary_material(str(secondary_select.get_item_metadata(index)))


func _on_catalyst_selected(index: int) -> void:
	if session != null:
		session.set_catalyst_material(str(catalyst_select.get_item_metadata(index)))


func _on_attempt_pressed() -> void:
	if session == null:
		return
	session.begin_attempt()
	_refresh(session.snapshot())


func _on_precision_pressed() -> void:
	if session == null:
		return
	session.finish_precision()
	_refresh(session.snapshot())


func _on_attempt_resolved(result: Dictionary) -> void:
	var target_level := int(result.get("target_level", 0))
	if bool(result.get("success", false)):
		attempt_result_label.text = "강화 성공! %s" % str(session.get_display_name())
		if bool(result.get("uses_materials", false)):
			attempt_result_label.text += " · +%d 재료 이정표 적용" % target_level
		attempt_result_label.add_theme_color_override("font_color", GREEN)
	else:
		attempt_result_label.text = "강화 실패 · 단계 유지 · 다음 시도 성공률 상승"
		attempt_result_label.add_theme_color_override("font_color", RED)


func _refresh(snapshot: Dictionary) -> void:
	var current_level := int(snapshot["enhancement_level"])
	var max_level := int(snapshot["max_level"])
	var target_level := int(snapshot["target_level"])
	var requires_precision := bool(snapshot["requires_precision"])
	var uses_materials := bool(snapshot["uses_materials"])
	var current_state := int(snapshot["state"])

	level_label.text = "+%d" % current_level
	weapon_name_label.text = str(snapshot["display_name"])
	progress_label.text = "%d / %d" % [current_level, max_level]
	progress_bar.value = float(snapshot["progress_ratio"]) * 100.0
	precision_gauge.set_pointer(float(snapshot["precision_position"]))
	milestone_preview_label.text = _format_milestone_preview(snapshot["milestone_preview"])
	material_panel.visible = uses_materials and current_state != EnhancementSessionScript.State.COMPLETE

	var base_chance := float(snapshot["base_success_chance"])
	if requires_precision:
		var precision: Dictionary = session.config["precision"]
		var prefix := "재료 이정표" if uses_materials else "정밀 강화"
		chance_label.text = "%s 기본 %d%% · GOOD %d%% · PERFECT %d%%" % [
			prefix,
			int(round(base_chance * 100.0)),
			int(round(session.calculate_success_chance(float(precision["good_success_bonus"])) * 100.0)),
			int(round(session.calculate_success_chance(float(precision["perfect_success_bonus"])) * 100.0)),
		]
		attempt_button.text = "+%d 정밀 강화" % target_level
		cadence_label.text = "+%d: %s" % [target_level, "재료 선택 + 정밀 강화" if uses_materials else "정밀 강화 · 재료 선택 없음"]
	else:
		chance_label.text = "원클릭 강화 성공률 %d%%" % int(round(base_chance * 100.0))
		attempt_button.text = "+%d 원클릭 강화" % target_level
		var next_precision := int(ceil(float(target_level) / 5.0) * 5.0)
		cadence_label.text = "+%d까지 원클릭 · +%d에서 정밀 강화" % [next_precision - 1, next_precision]

	if float(snapshot["pity_bonus"]) > 0.0:
		chance_label.text += " · 실패 보정 +%d%%" % int(round(float(snapshot["pity_bonus"]) * 100.0))

	if current_state != last_state:
		last_state = current_state
		_apply_state(current_state, snapshot)


func _apply_state(new_state: int, snapshot: Dictionary) -> void:
	var uses_materials := bool(snapshot["uses_materials"])
	match new_state:
		EnhancementSessionScript.State.READY:
			secondary_select.disabled = not uses_materials
			catalyst_select.disabled = not uses_materials
			attempt_button.visible = true
			precision_panel.visible = false
			complete_panel.visible = false
			helper_label.text = "+10 단위에서는 재료를 고른 뒤 정밀 강화합니다." if uses_materials else "현재 단계에는 보조재료와 촉매가 적용되지 않습니다."
		EnhancementSessionScript.State.PRECISION:
			secondary_select.disabled = true
			catalyst_select.disabled = true
			attempt_button.visible = false
			precision_panel.visible = true
			complete_panel.visible = false
			var precision: Dictionary = session.config["precision"]
			precision_gauge.configure(float(precision["target"]), float(precision["perfect_radius"]), float(precision["good_radius"]))
			helper_label.text = "선택한 재료는 이번 +10 단위 정밀 강화에만 적용됩니다." if uses_materials else "이번 +5 단위는 재료 없이 정밀 판정만 진행합니다."
		EnhancementSessionScript.State.COMPLETE:
			material_panel.visible = false
			attempt_button.visible = false
			precision_panel.visible = false
			complete_panel.visible = true
			complete_name_label.text = str(snapshot["display_name"])
			complete_affix_label.text = _format_affix_summary(snapshot["affixes"])
			complete_stats_label.text = "강화 시도 %d회 · 실패 %d회" % [int(snapshot["total_attempts"]), int(snapshot["total_failures"])]
			helper_label.text = "+100 최대 강화에 도달했습니다."


func _format_milestone_preview(preview: Dictionary) -> String:
	if preview.is_empty():
		return "+100 최종 이정표 완료"
	var level := int(preview.get("level", 0))
	var label := str(preview.get("label", "재료 이정표"))
	var effect := str(preview.get("effect", ""))
	if effect == "ASCEND_ALL":
		return "+%d %s" % [level, label]
	var affix: Dictionary = preview.get("affix", {})
	var affix_name := str(affix.get("name", "미정"))
	if effect == "UPGRADE_AFFIX":
		return "+%d %s: %s 티어 상승" % [level, label, affix_name]
	return "+%d %s: %s 후보" % [level, label, affix_name]


func _format_affix_summary(affix_list: Array) -> String:
	if affix_list.is_empty():
		return "수식어 없음"
	var parts: Array[String] = []
	for item_value in affix_list:
		if item_value is Dictionary:
			var item: Dictionary = item_value
			parts.append("%s %d티어 · %s" % [str(item.get("name", "수식어")), int(item.get("tier", 1)), _format_affix_effects(item.get("effects", {}))])
	return "\n".join(parts)


func _format_affix_effects(effects: Dictionary) -> String:
	if effects.has("attack_percent"):
		return "공격력 +%d%%" % int(round(float(effects["attack_percent"]) * 100.0))
	if effects.has("fire_damage"):
		return "화염 피해 +%d" % int(effects["fire_damage"])
	if effects.has("special_trigger_chance"):
		return "특수 발동 +%d%%" % int(round(float(effects["special_trigger_chance"]) * 100.0))
	return "고유 효과"


func _label(text_value: String, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	return label


func _panel(color: Color) -> PanelContainer:
	var panel := PanelContainer.new()
	panel.add_theme_stylebox_override("panel", _panel_style(color))
	return panel


func _panel_style(color: Color) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.corner_radius_top_left = 20
	style.corner_radius_top_right = 20
	style.corner_radius_bottom_left = 20
	style.corner_radius_bottom_right = 20
	style.content_margin_left = 22.0
	style.content_margin_right = 22.0
	style.content_margin_top = 18.0
	style.content_margin_bottom = 18.0
	return style


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


func _progress_bar(fill_color: Color) -> ProgressBar:
	var bar := ProgressBar.new()
	bar.min_value = 0.0
	bar.max_value = 100.0
	bar.value = 0.0
	bar.show_percentage = false
	bar.custom_minimum_size = Vector2(0.0, 28.0)
	bar.add_theme_stylebox_override("background", _button_style(Color("#16191f"), Color("#16191f"), 12))
	bar.add_theme_stylebox_override("fill", _button_style(fill_color, fill_color, 12))
	return bar


func _option_button() -> OptionButton:
	var option := OptionButton.new()
	option.custom_minimum_size = Vector2(0.0, 64.0)
	option.add_theme_font_size_override("font_size", 19)
	option.add_theme_color_override("font_color", TEXT)
	option.add_theme_stylebox_override("normal", _button_style(PANEL, BLUE, 14))
	return option
