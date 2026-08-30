class_name VSCustomerHandoffScreen
extends Control

signal handoff_confirmed
signal return_beat_continued

var _view_state: Dictionary = {
	"phase": "",
	"item_uid": "",
	"message": "",
	"action_label": "",
}


func _ready() -> void:
	_ensure_controls()
	_refresh_controls()


func configure_handoff(item_uid: String, enhancement_level: int) -> Dictionary:
	if item_uid.is_empty() or enhancement_level < 10:
		return {"status": "BLOCKED", "reason": "INVALID_HANDOFF_CONTEXT"}
	_view_state = {
		"phase": "HANDOFF",
		"item_uid": item_uid,
		"message": "나디아 벤에게 작품을 인계합니다. 인계 자체로는 손상이 발생하지 않습니다.",
		"action_label": "인계하고 작업대로 돌아가기",
	}
	_ensure_controls()
	_refresh_controls()
	return {"status": "APPLIED"}


func configure_return_beat(item_uid: String) -> Dictionary:
	if item_uid.is_empty():
		return {"status": "BLOCKED", "reason": "MISSING_ITEM_UID"}
	_view_state = {
		"phase": "RETURN",
		"item_uid": item_uid,
		"message": "작품이 작업대를 떠났습니다. 나디아의 실제 사용 결과를 확인합니다.",
		"action_label": "실제 사용 결과 확인",
	}
	_ensure_controls()
	_refresh_controls()
	return {"status": "APPLIED"}


func view_state() -> Dictionary:
	return _view_state.duplicate(true)


func _ensure_controls() -> void:
	var background := get_node_or_null("HandoffBackground") as ColorRect
	if background == null:
		background = ColorRect.new()
		background.name = "HandoffBackground"
		background.color = Color(0.15, 0.10, 0.07, 1.0)
		background.mouse_filter = Control.MOUSE_FILTER_IGNORE
		background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		add_child(background)
		move_child(background, 0)

	var margin := get_node_or_null("HandoffMargin") as MarginContainer
	if margin == null:
		margin = MarginContainer.new()
		margin.name = "HandoffMargin"
		margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		margin.add_theme_constant_override("margin_left", 32)
		margin.add_theme_constant_override("margin_top", 48)
		margin.add_theme_constant_override("margin_right", 32)
		margin.add_theme_constant_override("margin_bottom", 48)
		add_child(margin)

	var layout := margin.get_node_or_null("HandoffLayout") as VBoxContainer
	if layout == null:
		layout = VBoxContainer.new()
		layout.name = "HandoffLayout"
		layout.add_theme_constant_override("separation", 18)
		margin.add_child(layout)

	_ensure_label(layout, "TitleLabel", 32, Color(0.94, 0.84, 0.66, 1.0), HORIZONTAL_ALIGNMENT_CENTER)
	_ensure_label(layout, "UidLabel", 18, Color(0.82, 0.72, 0.55, 1.0), HORIZONTAL_ALIGNMENT_CENTER)
	_ensure_label(layout, "MessageLabel", 22, Color(0.96, 0.92, 0.83, 1.0), HORIZONTAL_ALIGNMENT_LEFT)
	var action := layout.get_node_or_null("ActionButton") as Button
	if action == null:
		action = Button.new()
		action.name = "ActionButton"
		action.custom_minimum_size = Vector2(0, 48)
		action.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		layout.add_child(action)
	if not action.pressed.is_connected(_on_action_pressed):
		action.pressed.connect(_on_action_pressed)


func _ensure_label(layout: VBoxContainer, node_name: String, font_size: int, font_color: Color, alignment: HorizontalAlignment) -> void:
	var label := layout.get_node_or_null(node_name) as Label
	if label == null:
		label = Label.new()
		label.name = node_name
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		layout.add_child(label)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", font_color)
	label.horizontal_alignment = alignment


func _refresh_controls() -> void:
	_set_label("HandoffMargin/HandoffLayout/TitleLabel", "작품 인계" if str(_view_state.get("phase", "")) == "HANDOFF" else "작업대 귀환")
	_set_label("HandoffMargin/HandoffLayout/UidLabel", "작품 UID: %s" % str(_view_state.get("item_uid", "")))
	_set_label("HandoffMargin/HandoffLayout/MessageLabel", str(_view_state.get("message", "")))
	var action := get_node_or_null("HandoffMargin/HandoffLayout/ActionButton") as Button
	if action != null:
		action.text = str(_view_state.get("action_label", ""))
		action.disabled = str(_view_state.get("phase", "")).is_empty()


func _set_label(path: String, value: String) -> void:
	var label := get_node_or_null(path) as Label
	if label != null:
		label.text = value


func _on_action_pressed() -> void:
	match str(_view_state.get("phase", "")):
		"HANDOFF":
			handoff_confirmed.emit()
		"RETURN":
			return_beat_continued.emit()
