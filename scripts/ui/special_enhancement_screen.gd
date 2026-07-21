# 일반 강화와 +10 단위 특수 강화를 서로 다른 화면으로 표시합니다.
extends "res://scripts/ui/enhancement_screen.gd"

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
var special_chance_label: Label
var special_result_label: Label
var special_start_button: Button

var complete_root: Control
var last_result_text := "+1부터 일반 강화를 시작합니다."
var last_result_color := MUTED


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
	layout.add_child(normal_chance_label)
	normal_result_label = _label(last_result_text, 18, MUTED)
	normal_result_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	normal_result_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(normal_result_label)

	normal_button = Button.new()
	normal_button.text = "+1 일반 강화"
	normal_button.custom_minimum_size = Vector2(0.0, 145.0)
	normal_button.add_theme_font_size_override("font_size", 31)
	normal_button.add_theme_color_override("font_color", TEXT)
	normal_button.add_theme_stylebox_override("normal", _button_style(Color("#8d4424"), ORANGE, 24))
	normal_button.add_theme_stylebox_override("pressed", _button_style(Color("#6f331d"), GOLD, 24))
	normal_button.pressed.connect(_on_attempt_pressed)
	layout.add_child(normal_button)

	var note := _label("일반 강화에는 보조재료·촉매·정밀 판정이 적용되지 않습니다.", 16, MUTED)
	note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(note)


func _build_special_screen(layout: VBoxContainer) -> void:
	var header := HBoxContainer.new()
	layout.add_child(header)
	var title := _label("[특수 강화]", 32, GOLD)
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title)
	special_target_label = _label("+10", 27, GOLD)
	special_target_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	header.add_child(special_target_label)

	var weapon_panel := _panel(PANEL_ALT)
	layout.add_child(weapon_panel)
	var weapon_box := VBoxContainer.new()
	weapon_box.add_theme_constant_override("separation", 8)
	weapon_panel.add_child(weapon_box)
	special_weapon_label = _label("철검 +9", 29, GOLD)
	special_weapon_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	weapon_box.add_child(special_weapon_label)
	special_milestone_label = _label("+10 첫 수식어 추가", 18, TEXT)
	special_milestone_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	special_milestone_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	weapon_box.add_child(special_milestone_label)

	var progress_panel := _panel(PANEL)
	layout.add_child(progress_panel)
	var progress_box := VBoxContainer.new()
	progress_panel.add_child(progress_box)
	var progress_header := HBoxContainer.new()
	progress_box.add_child(progress_header)
	progress_header.add_child(_label("특수 강화 단계", 18, TEXT))
	special_progress_label = _label("9 / 100", 18, GOLD)
	special_progress_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	special_progress_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	progress_header.add_child(special_progress_label)
	special_progress_bar = _progress_bar(GOLD)
	progress_box.add_child(special_progress_bar)

	material_panel = _panel(PANEL_ALT)
	layout.add_child(material_panel)
	var material_box := VBoxContainer.new()
	material_box.add_theme_constant_override("separation", 10)
	material_panel.add_child(material_box)
	var material_title := _label("특수 강화 재료", 23, GOLD)
	material_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	material_box.add_child(material_title)
	var material_info := _label("보조재료와 촉매는 이번 특수 강화에만 적용됩니다.", 16, MUTED)
	material_info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	material_box.add_child(material_info)

	var secondary_row := HBoxContainer.new()
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
	special_start_button.custom_minimum_size = Vector2(0.0, 110.0)
	special_start_button.add_theme_font_size_override("font_size", 28)
	special_start_button.add_theme_color_override("font_color", TEXT)
	special_start_button.add_theme_stylebox_override("normal", _button_style(Color("#8d4424"), GOLD, 22))
	special_start_button.pressed.connect(_on_attempt_pressed)
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
	precision_box.add_child(precision_instruction)
	precision_gauge = PrecisionGaugeScript.new()
	precision_box.add_child(precision_gauge)
	var precision_button := Button.new()
	precision_button.text = "특수 강화 타격!"
	precision_button.custom_minimum_size = Vector2(0.0, 90.0)
	precision_button.add_theme_font_size_override("font_size", 27)
	precision_button.add_theme_color_override("font_color", Color("#241b0f"))
	precision_button.add_theme_stylebox_override("normal", _button_style(GOLD, Color.WHITE, 20))
	precision_button.pressed.connect(_on_precision_pressed)
	precision_box.add_child(precision_button)


func _build_complete_screen(layout: VBoxContainer) -> void:
	var title := _label("최대 강화 완료", 32, GOLD)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	layout.add_child(title)
	var panel := _panel(PANEL_ALT)
	layout.add_child(panel)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 12)
	panel.add_child(box)
	complete_name_label = _label("철검 +100", 30, GOLD)
	complete_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(complete_name_label)
	complete_affix_label = _label("", 20, TEXT)
	complete_affix_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	complete_affix_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(complete_affix_label)
	complete_stats_label = _label("", 17, MUTED)
	complete_stats_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(complete_stats_label)
	var restart_button := Button.new()
	restart_button.text = "새 철검 제작"
	restart_button.custom_minimum_size = Vector2(0.0, 84.0)
	restart_button.add_theme_font_size_override("font_size", 24)
	restart_button.add_theme_color_override("font_color", TEXT)
	restart_button.add_theme_stylebox_override("normal", _button_style(Color("#3d7045"), GREEN, 18))
	restart_button.pressed.connect(func() -> void: restart_requested.emit())
	box.add_child(restart_button)


func _refresh(snapshot: Dictionary) -> void:
	var current_level := int(snapshot["enhancement_level"])
	var max_level := int(snapshot["max_level"])
	var target_level := int(snapshot["target_level"])
	var state_value := int(snapshot["state"])
	var is_complete := state_value == EnhancementSessionScript.State.COMPLETE
	var is_special := bool(snapshot["uses_materials"]) and not is_complete

	normal_root.visible = not is_special and not is_complete
	special_root.visible = is_special and not is_complete
	complete_root.visible = is_complete

	if not is_complete and not is_special:
		normal_level_label.text = "+%d" % current_level
		normal_weapon_label.text = str(snapshot["display_name"])
		normal_progress_label.text = "%d / %d" % [current_level, max_level]
		normal_progress_bar.value = float(snapshot["progress_ratio"]) * 100.0
		var next_special := int(ceil(float(target_level) / 10.0) * 10.0)
		normal_next_special_label.text = "다음 특수 강화: +%d" % next_special
		normal_chance_label.text = "원클릭 강화 성공률 %d%%" % int(round(float(snapshot["base_success_chance"]) * 100.0))
		if float(snapshot["pity_bonus"]) > 0.0:
			normal_chance_label.text += " · 실패 보정 +%d%%" % int(round(float(snapshot["pity_bonus"]) * 100.0))
		normal_result_label.text = last_result_text
		normal_result_label.add_theme_color_override("font_color", last_result_color)
		normal_button.text = "+%d 일반 강화" % target_level

	if is_special:
		special_target_label.text = "+%d" % target_level
		special_weapon_label.text = str(snapshot["display_name"])
		special_progress_label.text = "%d / %d" % [current_level, max_level]
		special_progress_bar.value = float(snapshot["progress_ratio"]) * 100.0
		special_milestone_label.text = _format_milestone_preview(snapshot["milestone_preview"])
		var precision: Dictionary = session.config["precision"]
		var base_chance := float(snapshot["base_success_chance"])
		special_chance_label.text = "기본 %d%% · GOOD %d%% · PERFECT %d%%" % [
			int(round(base_chance * 100.0)),
			int(round(session.calculate_success_chance(float(precision["good_success_bonus"])) * 100.0)),
			int(round(session.calculate_success_chance(float(precision["perfect_success_bonus"])) * 100.0)),
		]
		special_result_label.text = last_result_text
		special_result_label.add_theme_color_override("font_color", last_result_color)
		special_start_button.text = "+%d 특수 강화 시작" % target_level
		special_start_button.visible = state_value == EnhancementSessionScript.State.READY
		material_panel.visible = true
		secondary_select.disabled = state_value != EnhancementSessionScript.State.READY
		catalyst_select.disabled = state_value != EnhancementSessionScript.State.READY
		precision_panel.visible = state_value == EnhancementSessionScript.State.PRECISION
		if state_value == EnhancementSessionScript.State.PRECISION:
			precision_gauge.configure(float(precision["target"]), float(precision["perfect_radius"]), float(precision["good_radius"]))
			precision_gauge.set_pointer(float(snapshot["precision_position"]))

	if is_complete:
		complete_name_label.text = str(snapshot["display_name"])
		complete_affix_label.text = _format_affix_summary(snapshot["affixes"])
		complete_stats_label.text = "강화 시도 %d회 · 실패 %d회" % [int(snapshot["total_attempts"]), int(snapshot["total_failures"])]


func _on_attempt_resolved(result: Dictionary) -> void:
	var target_level := int(result.get("target_level", 0))
	if bool(result.get("success", false)):
		last_result_text = "%s 성공! %s" % ["특수 강화" if bool(result.get("uses_materials", false)) else "일반 강화", str(session.get_display_name())]
		if bool(result.get("uses_materials", false)):
			last_result_text += " · +%d 수식어 성장" % target_level
		last_result_color = GREEN
	else:
		last_result_text = "강화 실패 · 단계 유지 · 다음 시도 성공률 상승"
		last_result_color = RED
	_refresh(session.snapshot())
