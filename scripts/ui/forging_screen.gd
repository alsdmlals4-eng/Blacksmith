extends Control

const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")
const PrecisionGaugeScript = preload("res://scripts/ui/precision_gauge.gd")

const BG := Color("#17191f")
const PANEL := Color("#252932")
const PANEL_ALT := Color("#303641")
const TEXT := Color("#f4f1e8")
const MUTED := Color("#b7b0a3")
const ORANGE := Color("#d7772e")
const GOLD := Color("#f2c14e")
const FEVER := Color("#f05a3c")
const GREEN := Color("#72b879")

var session
var state_label: Label
var progress_bar: ProgressBar
var progress_value_label: Label
var fever_bar: ProgressBar
var fever_label: Label
var hammer_button: Button
var precision_toggle: CheckButton
var precision_panel: PanelContainer
var precision_gauge
var result_panel: PanelContainer
var result_name_label: Label
var result_quality_label: Label
var result_stats_label: Label
var helper_label: Label
var last_state: int = -1


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_build_interface()
	_start_new_session()
	set_process(true)


func _process(delta: float) -> void:
	if session == null:
		return
	session.advance(delta)
	_refresh(session.snapshot())


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("forge_tap"):
		if session.state == ForgingSessionScript.State.FINISHING:
			_on_precision_pressed()
		elif session.state == ForgingSessionScript.State.FORGING:
			_on_hammer_pressed()
		get_viewport().set_input_as_handled()


func _build_interface() -> void:
	var background := ColorRect.new()
	background.color = BG
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 28)
	margin.add_theme_constant_override("margin_right", 28)
	margin.add_theme_constant_override("margin_top", 34)
	margin.add_theme_constant_override("margin_bottom", 28)
	add_child(margin)

	var layout := VBoxContainer.new()
	layout.add_theme_constant_override("separation", 18)
	margin.add_child(layout)

	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation", 12)
	layout.add_child(header)

	var title_label := _label("대장간 · 첫 철검", 30, TEXT)
	title_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title_label)

	state_label = _label("제작 중", 18, GOLD)
	state_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	header.add_child(state_label)

	var material_panel := _panel(PANEL_ALT)
	layout.add_child(material_panel)
	var material_row := HBoxContainer.new()
	material_row.add_theme_constant_override("separation", 16)
	material_panel.add_child(material_row)
	var material_name := _label("주재료  철", 21, TEXT)
	material_name.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	material_row.add_child(material_name)
	var weapon_type := _label("무기  검", 21, TEXT)
	weapon_type.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	material_row.add_child(weapon_type)

	var work_panel := _panel(PANEL)
	layout.add_child(work_panel)
	var work_box := VBoxContainer.new()
	work_box.add_theme_constant_override("separation", 10)
	work_panel.add_child(work_box)

	var progress_header := HBoxContainer.new()
	work_box.add_child(progress_header)
	progress_header.add_child(_label("제작 진행", 18, TEXT))
	progress_value_label = _label("0%", 18, GOLD)
	progress_value_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	progress_value_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	progress_header.add_child(progress_value_label)

	progress_bar = _progress_bar(ORANGE)
	work_box.add_child(progress_bar)

	var fever_header := HBoxContainer.new()
	work_box.add_child(fever_header)
	fever_header.add_child(_label("피버", 18, TEXT))
	fever_label = _label("연속 터치로 충전", 16, MUTED)
	fever_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	fever_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	fever_header.add_child(fever_label)

	fever_bar = _progress_bar(FEVER)
	work_box.add_child(fever_bar)

	hammer_button = Button.new()
	hammer_button.text = "망치질\n빠르게 연타!"
	hammer_button.custom_minimum_size = Vector2(0.0, 330.0)
	hammer_button.size_flags_vertical = Control.SIZE_EXPAND_FILL
	hammer_button.add_theme_font_size_override("font_size", 34)
	hammer_button.add_theme_color_override("font_color", TEXT)
	hammer_button.add_theme_color_override("font_hover_color", Color.WHITE)
	hammer_button.add_theme_stylebox_override("normal", _button_style(Color("#8d4424"), Color("#d7772e"), 28))
	hammer_button.add_theme_stylebox_override("hover", _button_style(Color("#a85129"), GOLD, 28))
	hammer_button.add_theme_stylebox_override("pressed", _button_style(Color("#6f331d"), GOLD, 28))
	hammer_button.pressed.connect(_on_hammer_pressed)
	layout.add_child(hammer_button)

	precision_toggle = CheckButton.new()
	precision_toggle.text = "정밀 마감 사용"
	precision_toggle.button_pressed = true
	precision_toggle.add_theme_font_size_override("font_size", 21)
	precision_toggle.add_theme_color_override("font_color", TEXT)
	precision_toggle.toggled.connect(_on_precision_toggled)
	layout.add_child(precision_toggle)

	precision_panel = _panel(PANEL_ALT)
	precision_panel.visible = false
	layout.add_child(precision_panel)
	var precision_box := VBoxContainer.new()
	precision_box.add_theme_constant_override("separation", 12)
	precision_panel.add_child(precision_box)
	var precision_title := _label("마감 타격", 24, GOLD)
	precision_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	precision_box.add_child(precision_title)
	var precision_instruction := _label("흰 포인터가 황금 구간에 들어왔을 때 누르세요.", 17, MUTED)
	precision_instruction.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	precision_instruction.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	precision_box.add_child(precision_instruction)
	precision_gauge = PrecisionGaugeScript.new()
	precision_box.add_child(precision_gauge)
	var precision_button := Button.new()
	precision_button.text = "마감 타격!"
	precision_button.custom_minimum_size = Vector2(0.0, 90.0)
	precision_button.add_theme_font_size_override("font_size", 27)
	precision_button.add_theme_color_override("font_color", Color("#241b0f"))
	precision_button.add_theme_stylebox_override("normal", _button_style(GOLD, Color.WHITE, 20))
	precision_button.add_theme_stylebox_override("pressed", _button_style(Color("#c99835"), Color.WHITE, 20))
	precision_button.pressed.connect(_on_precision_pressed)
	precision_box.add_child(precision_button)

	result_panel = _panel(PANEL_ALT)
	result_panel.visible = false
	layout.add_child(result_panel)
	var result_box := VBoxContainer.new()
	result_box.add_theme_constant_override("separation", 10)
	result_panel.add_child(result_box)
	result_name_label = _label("철검 완성!", 30, GOLD)
	result_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	result_box.add_child(result_name_label)
	result_quality_label = _label("", 22, TEXT)
	result_quality_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	result_box.add_child(result_quality_label)
	result_stats_label = _label("", 17, MUTED)
	result_stats_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	result_box.add_child(result_stats_label)
	var restart_button := Button.new()
	restart_button.text = "다시 제작"
	restart_button.custom_minimum_size = Vector2(0.0, 82.0)
	restart_button.add_theme_font_size_override("font_size", 24)
	restart_button.add_theme_color_override("font_color", TEXT)
	restart_button.add_theme_stylebox_override("normal", _button_style(Color("#3d7045"), GREEN, 18))
	restart_button.pressed.connect(_start_new_session)
	result_box.add_child(restart_button)

	helper_label = _label("터치하지 않아도 천천히 진행됩니다. 빠르게 두드리면 피버가 발동합니다.", 16, MUTED)
	helper_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	helper_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	layout.add_child(helper_label)


func _start_new_session() -> void:
	var config := _load_session_config()
	session = ForgingSessionScript.new(config)
	session.precision_enabled = precision_toggle.button_pressed if precision_toggle != null else true
	session.fever_started.connect(_on_fever_started)
	session.fever_ended.connect(_on_fever_ended)
	last_state = -1
	_refresh(session.snapshot())


func _load_session_config() -> Dictionary:
	var file := FileAccess.open("res://data/crafting/forging_balance.json", FileAccess.READ)
	if file == null:
		push_warning("forging_balance.json을 읽지 못해 기본 수치를 사용합니다.")
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary and parsed.get("session", {}) is Dictionary:
		return parsed["session"]
	push_warning("forging_balance.json 형식이 올바르지 않아 기본 수치를 사용합니다.")
	return {}


func _on_hammer_pressed() -> void:
	if session == null or not session.register_tap():
		return
	hammer_button.pivot_offset = hammer_button.size * 0.5
	var tween := create_tween()
	tween.tween_property(hammer_button, "scale", Vector2(0.97, 0.97), 0.04)
	tween.tween_property(hammer_button, "scale", Vector2.ONE, 0.07)
	_refresh(session.snapshot())


func _on_precision_toggled(enabled: bool) -> void:
	if session != null:
		session.set_precision_enabled(enabled)


func _on_precision_pressed() -> void:
	if session == null:
		return
	session.finish_precision()
	_refresh(session.snapshot())


func _on_fever_started() -> void:
	helper_label.text = "피버타임! 터치와 자동 작업이 크게 빨라집니다."


func _on_fever_ended() -> void:
	helper_label.text = "피버 종료. 다시 빠르게 연타해 게이지를 채우세요."


func _refresh(snapshot: Dictionary) -> void:
	progress_bar.value = float(snapshot["progress_ratio"]) * 100.0
	progress_value_label.text = "%d%%" % int(round(float(snapshot["progress_ratio"]) * 100.0))
	fever_bar.value = float(snapshot["fever_ratio"]) * 100.0
	precision_gauge.set_pointer(float(snapshot["precision_position"]))

	if bool(snapshot["fever_active"]):
		fever_label.text = "피버 %.1f초 · ×%.1f" % [float(snapshot["fever_time_left"]), float(snapshot["work_multiplier"])]
		state_label.text = "피버!"
		state_label.add_theme_color_override("font_color", FEVER)
	else:
		fever_label.text = "연속 터치로 충전"
		state_label.add_theme_color_override("font_color", GOLD)

	var new_state := int(snapshot["state"])
	if new_state != last_state:
		last_state = new_state
		_apply_state(new_state, snapshot)


func _apply_state(new_state: int, snapshot: Dictionary) -> void:
	match new_state:
		ForgingSessionScript.State.FORGING:
			state_label.text = "제작 중"
			hammer_button.visible = true
			hammer_button.disabled = false
			precision_toggle.visible = true
			precision_panel.visible = false
			result_panel.visible = false
			helper_label.text = "터치하지 않아도 천천히 진행됩니다. 빠르게 두드리면 피버가 발동합니다."
		ForgingSessionScript.State.FINISHING:
			state_label.text = "마무리"
			hammer_button.visible = false
			precision_toggle.visible = false
			precision_panel.visible = true
			result_panel.visible = false
			precision_gauge.configure(
				float(session.config["precision_target"]),
				float(session.config["precision_perfect_radius"]),
				float(session.config["precision_good_radius"])
			)
			helper_label.text = "정밀 마감은 추가 보너스입니다. 실패해도 무기는 사라지지 않습니다."
		ForgingSessionScript.State.COMPLETE:
			state_label.text = "완성"
			hammer_button.visible = false
			precision_toggle.visible = false
			precision_panel.visible = false
			result_panel.visible = true
			var finished: Dictionary = snapshot["result"]
			result_name_label.text = "%s 완성!" % finished.get("weapon_name", "철검")
			result_quality_label.text = str(finished.get("quality_label", "보통 마감"))
			result_stats_label.text = "기본 공격력 %d → %d · 제작 가치 ×%.2f\n망치질 %d회 · 피버 %d회" % [
				int(finished.get("raw_base_attack", 10)),
				int(finished.get("base_attack", 10)),
				float(finished.get("quality_value_multiplier", 1.0)),
				int(finished.get("tap_count", 0)),
				int(finished.get("fever_activation_count", 0)),
			]
			helper_label.text = "MVP-001에서는 완성까지 검증합니다. 강화와 판매는 다음 수직 범위입니다."


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
