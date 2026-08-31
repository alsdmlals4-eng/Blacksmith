# 작품의 제작·정밀 태그·실제 사용 결과를 기존 저장 사실에서 읽어 보여 준다.
class_name VSItemChronicleScreen
extends Control

signal workshop_requested

var _view_state: Dictionary = {
	"item_uid": "",
	"summary": "작품을 선택하세요.",
	"entries": [],
}


func _ready() -> void:
	_ensure_controls()
	_refresh_controls()


func configure_item(item, resolved_events: Dictionary) -> Dictionary:
	if item == null or str(item.uid).is_empty() or not resolved_events is Dictionary:
		return {"status": "BLOCKED", "reason": "INVALID_CHRONICLE_CONTEXT"}
	_view_state = {
		"item_uid": str(item.uid),
		"summary": "+%d · 내구도 %d / %d / %d" % [
			int(item.enhancement_level),
			int(item.current_durability),
			int(item.max_durability),
			int(item.base_max_durability),
		],
		"entries": _entries_from_existing_facts(item, resolved_events),
	}
	_ensure_controls()
	_refresh_controls()
	return {"status": "APPLIED"}


func view_state() -> Dictionary:
	return _view_state.duplicate(true)


func _entries_from_existing_facts(item, resolved_events: Dictionary) -> Array:
	var entries: Array = []
	var ledger: Variant = item.ledger
	if ledger is Array:
		for raw_entry in ledger:
			if not raw_entry is Dictionary:
				continue
			var event_type := str(raw_entry.get("event_type", ""))
			if event_type == "ITEM_BORN":
				entries.append({
					"kind": "BIRTH",
					"text": "제작 · %s" % _crafting_grade_text(str(raw_entry.get("payload", {}).get("crafting_grade", ""))),
				})
			elif event_type == "PRECISION_TAG_GROWTH":
				var payload: Variant = raw_entry.get("payload", {})
				entries.append({
					"kind": "PRECISION_TAG",
					"text": "정밀 태그 · %s 단계 %d → %d" % [
						str(payload.get("tag_id", "")),
						int(payload.get("stage_before", 0)),
						int(payload.get("stage_after", 0)),
					],
				})
	for raw_result in resolved_events.values():
		if not _is_matching_actual_use_result(raw_result, str(item.uid)):
			continue
		var result: Dictionary = raw_result
		var consequence: Dictionary = result.get("durability_consequence", {})
		entries.append({"kind": "HANDOFF", "text": "나디아 벤에게 작품 인계"})
		entries.append({
			"kind": "ACTUAL_USE",
			"text": "나디아 벤 실제 사용 결과 · %s" % ("손상 발생" if bool(consequence.get("damage_applied", false)) else "손상 없음"),
		})
	return entries


func _is_matching_actual_use_result(raw_result, item_uid: String) -> bool:
	if not raw_result is Dictionary or str(raw_result.get("customer_id", "")) != "NADIA_VENN":
		return false
	var consequence: Variant = raw_result.get("durability_consequence", {})
	if not consequence is Dictionary or not bool(consequence.get("actual_item_use", false)):
		return false
	var references: Variant = raw_result.get("item_refs", [])
	if not references is Array:
		return false
	for reference in references:
		if reference is Dictionary and str(reference.get("role", "")) == "PRIMARY_ITEM" and str(reference.get("uid", "")) == item_uid:
			return true
	return false


func _crafting_grade_text(grade: String) -> String:
	match grade:
		"CRAFT_NORMAL":
			return "보통"
		"CRAFT_SUPERIOR":
			return "우수"
		"CRAFT_MASTERPIECE":
			return "명품"
		"CRAFT_MASTERWORK":
			return "걸작"
		"CRAFT_LEGENDARY":
			return "전설"
		_:
			return "기록된 작품"


func _ensure_controls() -> void:
	var background := get_node_or_null("ChronicleBackground") as ColorRect
	if background == null:
		background = ColorRect.new()
		background.name = "ChronicleBackground"
		background.color = Color(0.15, 0.10, 0.07, 1.0)
		background.mouse_filter = Control.MOUSE_FILTER_IGNORE
		background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		add_child(background)
		move_child(background, 0)
	var margin := get_node_or_null("ChronicleMargin") as MarginContainer
	if margin == null:
		margin = MarginContainer.new()
		margin.name = "ChronicleMargin"
		margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		margin.add_theme_constant_override("margin_left", 32)
		margin.add_theme_constant_override("margin_top", 48)
		margin.add_theme_constant_override("margin_right", 32)
		margin.add_theme_constant_override("margin_bottom", 48)
		add_child(margin)
	var layout := margin.get_node_or_null("ChronicleLayout") as VBoxContainer
	if layout == null:
		layout = VBoxContainer.new()
		layout.name = "ChronicleLayout"
		layout.add_theme_constant_override("separation", 16)
		margin.add_child(layout)
	_ensure_label(layout, "TitleLabel", 32, Color(0.94, 0.84, 0.66, 1.0), HORIZONTAL_ALIGNMENT_CENTER)
	_ensure_label(layout, "UidLabel", 18, Color(0.82, 0.72, 0.55, 1.0), HORIZONTAL_ALIGNMENT_CENTER)
	_ensure_label(layout, "SummaryLabel", 20, Color(0.96, 0.92, 0.83, 1.0), HORIZONTAL_ALIGNMENT_LEFT)
	_ensure_label(layout, "EntriesLabel", 20, Color(0.96, 0.92, 0.83, 1.0), HORIZONTAL_ALIGNMENT_LEFT)
	var return_button := layout.get_node_or_null("WorkshopReturnButton") as Button
	if return_button == null:
		return_button = Button.new()
		return_button.name = "WorkshopReturnButton"
		return_button.text = "작업대로 돌아가기"
		return_button.custom_minimum_size = Vector2(0, 48)
		return_button.add_theme_font_size_override("font_size", 20)
		layout.add_child(return_button)
	if not return_button.pressed.is_connected(_on_workshop_return_pressed):
		return_button.pressed.connect(_on_workshop_return_pressed)


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
	_set_label("ChronicleMargin/ChronicleLayout/TitleLabel", "작품 연대")
	_set_label("ChronicleMargin/ChronicleLayout/UidLabel", "작품 UID: %s" % str(_view_state.get("item_uid", "")))
	_set_label("ChronicleMargin/ChronicleLayout/SummaryLabel", str(_view_state.get("summary", "")))
	var lines: PackedStringArray = []
	for entry in _view_state.get("entries", []):
		if entry is Dictionary:
			lines.append("• %s" % str(entry.get("text", "")))
	_set_label("ChronicleMargin/ChronicleLayout/EntriesLabel", "\n".join(lines) if not lines.is_empty() else "아직 기록할 의미 있는 사건이 없습니다.")
	var return_button := get_node_or_null("ChronicleMargin/ChronicleLayout/WorkshopReturnButton") as Button
	if return_button != null:
		return_button.disabled = str(_view_state.get("item_uid", "")).is_empty()


func _set_label(path: String, value: String) -> void:
	var label := get_node_or_null(path) as Label
	if label != null:
		label.text = value


func _on_workshop_return_pressed() -> void:
	if not str(_view_state.get("item_uid", "")).is_empty():
		workshop_requested.emit()
