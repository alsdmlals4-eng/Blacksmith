# 일반 강화와 +10 단위 특수 강화를 서로 다른 화면으로 표시합니다.
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

var normal_root: Control
var normal_level_label: Label
var normal_weapon_label: Label
var normal_progress_bar: ProgressBar
var normal_progress_label: Label
var normal_next_special_label: Label
var normal_chance_label: Label
var normal_result_label: Label
var normal_button: Button

var special_root: Control
var special_target_label: Label
var special_weapon_label: Label
var special_progress_bar: ProgressBar
var special_progress_label: Label
var special_milestone_label: Label
var secondary_select: OptionButton
var catalyst_select: OptionButton
var special_chance_label: Label
var special_result_label: Label
var special_start_button: Button
var precision_panel: PanelContainer
var precision_gauge

var complete_root: Control
var complete_name_label: Label
var complete_affix_label: Label
var complete_stats_label: Label

var last_result_text: String = "+1부터 일반 강화를 시작합니다."
var last_result_color: Color = MUTED


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
	if session == null or session.state != EnhancementSessionScript.State.PRECISION:
		return
	session.advance(delta)
	_refresh(session.snapshot())


func _unhandled_input(event: InputEvent) -> void:
	if not visible or session == null or not event.is_action_pressed("forge_tap"):
		return
	if session.state == EnhancementSessionScript.State.PRECISION:
		_on_precision_pressed()
	elif session.state == EnhancementSessionScript.State.READY:
		if session.uses_materials_for_level(session.enhancement_level + 1):
			_on_special_start_pressed()
		else:
			_on_normal_pressed()
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

	normal_root = _make_screen_root()
	add_child(normal_root)
	_build_normal_screen(_screen_layout(normal_root))

	special_root = _make_screen_root()
	add_child(special_root)
	_build_special_screen(_screen_layout(special_root))

	complete_root = _make_screen_root()
	add_child(complete_root)
	_build_complete_screen(_screen_layout(complete_root))


func _make_screen_root() -> MarginContainer:
	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 24)
	margin.add_theme_constant_override("margin_bottom", 24)
	return margin


func _screen_layout(root: MarginContainer) -> VBoxContainer:
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	root.add_child(scroll)
	var layout := VBoxContainer.new()
	layout.custom_minimum_size = Vector2(672.0, 0.0)
	layout.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	layout.add_theme_constant_override("separation", 15)
	scroll.add_child(layout)
	return layout


func _build_normal_screen(layout: VBoxContainer) -> void:
	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation", 12)
	layout.add_child(header)
	var title := _label("일반 강화", 32, TEXT)
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title)
	normal_level_label = _label("+0", 26, GOLD)
	normal_level_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	header.add_child(normal_level_label)

	var weapon_panel := _panel(PANEL_ALT)
	layout.add_child(weapon_panel)
	var weapon_box := VBoxContainer.new()
	weapon_box.add_theme_constant_override("separation", 8)
	weapon_panel.add_child(weapon_box)
	normal_weapon_label = _label("철검 +0", 29, GOLD)
	normal_weapon_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	normal_weapon_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	weapon_box.add_child(normal_weapon_label)
	normal_next_special_label = _label("다음 특수 강화: +10", 18, TEXT)
	normal_next_special_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	weapon_box.add_child(normal_next_special_label)

	var progress_panel := _panel(PANEL)
	layout.add_child(progress_panel)
	var progress_box := VBoxContainer.new()
	progress_box.add_theme_constant_override("separation", 8)
	progress_panel.add_child(progress_box)
	var progress_header := HBoxContainer.new()
	progress_box.add_child(progress_header)
	progress_header.add_child(_label("강화 단계", 18, TEXT))
	normal_progress_label = _label("0 / 100", 18, GOLD)
	normal_progress_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	normal_progress_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	progress_header.add_child(normal_progress_label)
	normal_progress_bar = _progress_bar(ORANGE)
	progress_box.add_child(normal_progress_bar)
	var rule := _label("+1~+9는 같은 일반 강화 화면에서 원클릭으로 진행합니다.", 16, MUTED)
	rule.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	rule.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	progress_box.add_child(rule)

	normal_chance_label = _label("원클릭 강화 성공률", 21, GOLD)
	normal_chance_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	normal_chance_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(normal_chance_label)

	normal_result_label = _label(last_result_text, 18, MUTED)
	normal_result_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	normal_result_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(normal_result_label)

	normal_button = Button.new()
	normal_button.text = "+1 일반 강화"
	normal_button.custom_minimum_size = Vector2(0.0, 150.0)
	normal_button.add_theme_font_size_override("font_size", 32)
	normal_button.add_theme_color_override("font_color", TEXT)
	normal_button.add_theme_stylebox_override("normal", _button_style(Color("#8d4424"), ORANGE, 24))
	normal_button.add_theme_stylebox_override("hover", _button_style(Color("#a85129"), GOLD, 24))
	normal_button.add_theme_stylebox_override("pressed", _button_style(Color("#6f331d"), GOLD, 24))
	normal_button.pressed.connect(_on_normal_pressed)
	layout.add_child(normal_button)

	var helper := _label("일반 강화에는 보조재료·촉매·정밀 판정이 표시되거나 적용되지 않습니다.", 16, MUTED)
	helper.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	helper.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(helper)


func _build_special_screen(layout: VBoxContainer) -> void:
	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation", 12)
	layout.add_child(header)
	var title := _label("[특수 강화]", 32, GOLD)
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title)
	special_target_label = _label("+10", 26, GOLD)
	special_target_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	header.add_child(special_target_label)

	var weapon_panel := _panel(PANEL_ALT)
	layout.add_child(weapon_panel)
	var weapon_box := VBoxContainer.new()
	weapon_box.add_theme_constant_override("separation", 8)
	weapon_panel.add_child(weapon_box)
	special_weapon_label = _label("철검 +9", 29, GOLD)
	special_weapon_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	special_weapon_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	weapon_box.add_child(special_weapon_label)
	special_milestone_label = _label("+10 첫 수식어 추가", 18, TEXT)
	special_milestone_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	special_milestone_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	weapon_box.add_child(special_milestone_label)

	var progress_panel := _panel(PANEL)
	layout.add_child(progress_panel)
	var progress_box := VBoxContainer.new()
	progress_box.add_theme_constant_override("separation", 8)
	progress_panel.add_child(progress_box)
	var progress_header := HBoxContainer.new()
	progress_box.add_child(progress_header)
	progress_header.add_child(_label("강화 단계", 18, TEXT))
	special_progress_label = _label("9 / 100", 18, GOLD)
	special_progress_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	special_progress_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	progress_header.add_child(special_progress_label)
	special_progress_bar = _progress_bar(GOLD)
	progress_box.add_child(special_progress_bar)
	var special_rule := _label("10단계 단위에서만 보조재료·촉매·정밀 판정을 사용합니다.", 16, MUTED)
	special_rule.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	special_rule.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	progress_box.add_child(special_rule)

	var material_panel := _panel(PANEL_ALT)
	layout.add_child(material_panel)
	var material_box := VBoxContainer.new()
	material_box.add_theme_constant_override("separation", 11)
	material_panel.add_child(material_box)
	var material_title := _label("특수 강화 재료", 23, GOLD)
	material_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	material_box.add_child(material_title)

	var secondary_row := HBoxContainer.new()
	secondary_row.add_theme_constant_override("separation", 12)
	material_box.add_child(secondary_row)
	var secondary_label := _label("보조재료", 18, MUTED)
	secondary_label.custom_minimum_size = Vector2(125.0, 0.0)
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
	catalyst_label.custom_minimum_size = Vector2(125.0, 0.0)
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

	special_chance_label = _label("특수 강화 성공률", 21, GOLD)
	special_chance_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	special_chance_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(special_chance_label)

	special_result_label = _label(last_result_text, 18, MUTED)
	special_result_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	special_result_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(special_result_label)

	special_start_button = Button.new()
	special_start_button.text = "+10 특수 강화 시작"
	special_start_button.custom_minimum_size = Vector2(0.0, 115.0)
	special_start_button.add_theme_font_size_override("font_size", 29)
	special_start_button.add_theme_color_override("font_color", TEXT)
	special_start_button.add_theme_stylebox_override("normal", _button_style(Color("#8d4424"), GOLD, 22))
	special_start_button.add_theme_stylebox_override("pressed", _button_style(Color("#6f331d"), Color.WHITE, 22))
	special_start_button.pressed.connect(_on_special_start_pressed)
	layout.add_child(special_start_button)

	precision_panel = _panel(PANEL_ALT)
	precision_panel.visible = false
	layout.add_child(precision_panel)
	var precision_box := VBoxContainer.new()
	precision_box.add_theme_constant_override("separation", 10)
	precision_panel.add_child(precision_box)
	var precision_title := _label("특수 강화 정밀 판정", 24, GOLD)
	precision_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	precision_box.add_child(precision_title)
	var precision_instruction := _label("흰 포인터가 황금 구간에 들어왔을 때 타격하세요.", 17, MUTED)
	precision_instruction.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	precision_instruction.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	precision_box.add_child(precision_instruction)
	precision_gauge = PrecisionGaugeScript.new()
	precision_box.add_child(precision_gauge)
	var precision_button := Button.new()
	precision_button.text = "특수 강화 타격!"
	precision_button.custom_minimum_size = Vector2(0.0, 90.0)
	precision_button.add_theme_font_size_override("font_size", 27)
	precision_button.add_theme_color_override("font_color", Color("#241b0f"))
	precision_button.add_theme_stylebox_override("normal", _button_style(GOLD, Color.WHITE, 20))
	precision_button.add_theme_stylebox_override("pressed", _button_style(Color("#c99835"), Color.WHITE, 20))
	precision_button.pressed.connect(_on_precision_pressed)
	precision_box.add_child(precision_button)


func _build_complete_screen(layout: VBoxContainer) -> void:
	var title := _label("최대 강화 완료", 34, GOLD)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	layout.add_child(title)
	var panel := _panel(PANEL_ALT)
	layout.add_child(panel)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 12)
	panel.add_child(box)
	complete_name_label = _label("철검 +100", 30, GOLD)
	complete_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	complete_name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(complete_name_label)
	complete_affix_label = _label("모든 수식어 4티어", 21, TEXT)
	complete_affix_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	complete_affix_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(complete_affix_label)
	complete_stats_label = _label("", 17, MUTED)
	complete_stats_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(complete_stats_label)
	var restart_button := Button.new()
	restart_button.text = "새 철검 제작"
	restart_button.custom_minimum_size = Vector2(0.0, 90.0)
	restart_button.add_theme_font_size_override("font_size", 25)
	restart_button.add_theme_color_override("font_color", TEXT)
	restart_button.add_theme_stylebox_override("normal", _button_style(Color("#3d7045"), GREEN, 18))
	restart_button.pressed.connect(func() -> void: restart_requested.emit())
	box.add_child(restart_button)


func _on_normal_pressed() -> void:
	if session == null or session.state != EnhancementSessionScript.State.READY:
		return
	if session.uses_materials_for_level(session.enhancement_level + 1):
		return
	session.begin_attempt()
	_refresh(session.snapshot())


func _on_special_start_pressed() -> void:
	if session == null or session.state != EnhancementSessionScript.State.READY:
		return
	if not session.uses_materials_for_level(session.enhancement_level + 1):
		return
	session.begin_attempt()
	_refresh(session.snapshot())


func _on_precision_pressed() -> void:
	if session == null or session.state != EnhancementSessionScript.State.PRECISION:
		return
	session.finish_precision()
	_refresh(session.snapshot())


func _on_secondary_selected(index: int) -> void:
	if session != null:
		session.set_secondary_material(str(secondary_select.get_item_metadata(index)))


func _on_catalyst_selected(index: int) -> void:
	if session != null:
		session.set_catalyst_material(str(catalyst_select.get_item_metadata(index)))


func _on_attempt_resolved(result: Dictionary) -> void:
	var target_level := int(result.get("target_level", 0))
	var is_special := bool(result.get("uses_materials", false))
	if bool(result.get("success", false)):
		last_result_text = (
			"특수 강화 성공! +%d 수식어 성장이 적용됐습니다." % target_level
			if is_special
			else "일반 강화 성공! %s" % str(session.get_display_name())
		)
		last_result_color = GREEN
	else:
		last_result_text = (
			"특수 강화 실패 · 단계 유지 · 재료를 다시 선택할 수 있습니다."
			if is_special
			else "일반 강화 실패 · 단계 유지 · 다음 성공률이 상승합니다."
		)
		last_result_color = RED
	_refresh(session.snapshot())


func _refresh(snapshot: Dictionary) -> void:
	var current_level := int(snapshot["enhancement_level"])
	var max_level := int(snapshot["max_level"])
	var target_level := int(snapshot["target_level"])
	var current_state := int(snapshot["state"])
	var is_special := bool(snapshot["uses_materials"])

	normal_root.visible = current_state == EnhancementSessionScript.State.READY and not is_special
	special_root.visible = current_state != EnhancementSessionScript.State.COMPLETE and (is_special or current_state == EnhancementSessionScript.State.PRECISION)
	complete_root.visible = current_state == EnhancementSessionScript.State.COMPLETE

	_update_result_labels()

	if complete_root.visible:
		complete_name_label.text = str(snapshot["display_name"])
		complete_affix_label.text = _format_affix_summary(snapshot["affixes"])
		complete_stats_label.text = "강화 시도 %d회 · 실패 %d회" % [int(snapshot["total_attempts"]), int(snapshot["total_failures"])]
		return

	if normal_root.visible:
		normal_level_label.text = "+%d" % current_level
		normal_weapon_label.text = str(snapshot["display_name"])
		normal_progress_label.text = "%d / %d" % [current_level, max_level]
		normal_progress_bar.value = float(snapshot["progress_ratio"]) * 100.0
		var next_special := int(ceil(float(target_level) / 10.0) * 10.0)
		normal_next_special_label.text = "다음 특수 강화: +%d" % next_special
		normal_button.text = "+%d 일반 강화" % target_level
		normal_chance_label.text = "원클릭 강화 성공률 %d%%" % int(round(float(snapshot["base_success_chance"]) * 100.0))
		if float(snapshot["pity_bonus"]) > 0.0:
			normal_chance_label.text += " · 실패 보정 +%d%%" % int(round(float(snapshot["pity_bonus"]) * 100.0))
		return

	special_target_label.text = "+%d" % target_level
	special_weapon_label.text = str(snapshot["display_name"])
	special_progress_label.text = "%d / %d" % [current_level, max_level]
	special_progress_bar.value = float(snapshot["progress_ratio"]) * 100.0
	special_milestone_label.text = _format_milestone_preview(snapshot["milestone_preview"])
	special_start_button.text = "+%d 특수 강화 시작" % target_level
	precision_gauge.set_pointer(float(snapshot["precision_position"]))

	var precision: Dictionary = session.config["precision"]
	var base_chance := float(snapshot["base_success_chance"])
	special_chance_label.text = "기본 %d%% · GOOD %d%% · PERFECT %d%%" % [
		int(round(base_chance * 100.0)),
		int(round(session.calculate_success_chance(float(precision["good_success_bonus"])) * 100.0)),
		int(round(session.calculate_success_chance(float(precision["perfect_success_bonus"])) * 100.0)),
	]
	if float(snapshot["pity_bonus"]) > 0.0:
		special_chance_label.text += " · 실패 보정 +%d%%" % int(round(float(snapshot["pity_bonus"]) * 100.0))

	var judging := current_state == EnhancementSessionScript.State.PRECISION
	special_start_button.visible = not judging
	precision_panel.visible = judging
	secondary_select.disabled = judging
	catalyst_select.disabled = judging
	if judging:
		precision_gauge.configure(float(precision["target"]), float(precision["perfect_radius"]), float(precision["good_radius"]))


func _update_result_labels() -> void:
	normal_result_label.text = last_result_text
	normal_result_label.add_theme_color_override("font_color", last_result_color)
	special_result_label.text = last_result_text
	special_result_label.add_theme_color_override("font_color", last_result_color)


func _format_milestone_preview(preview: Dictionary) -> String:
	if preview.is_empty():
		return "+100 모든 수식어 최종 승급"
	var level := int(preview.get("level", 0))
	var label := str(preview.get("label", "수식어 성장"))
	var effect := str(preview.get("effect", ""))
	if effect == "ASCEND_ALL":
		return "+%d 특수 강화 · %s" % [level, label]
	var affix: Dictionary = preview.get("affix", {})
	var affix_name := str(affix.get("name", "선택한 재료에 따라 결정"))
	if effect == "UPGRADE_AFFIX":
		return "+%d 특수 강화 · %s: %s" % [level, label, affix_name]
	return "+%d 특수 강화 · %s: %s 후보" % [level, label, affix_name]


func _format_affix_summary(affix_list: Array) -> String:
	if affix_list.is_empty():
		return "수식어 없음"
	var parts: Array[String] = []
	for item_value in affix_list:
		if item_value is Dictionary:
			var item: Dictionary = item_value
			parts.append("%s %d티어" % [str(item.get("name", "수식어")), int(item.get("tier", 1))])
	return "\n".join(parts)


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
