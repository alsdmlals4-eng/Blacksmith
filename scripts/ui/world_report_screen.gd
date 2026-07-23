class_name WorldReportScreen
extends VBoxContainer

signal continue_requested

var title_label: Label
var result_label: Label
var evidence_label: Label
var history_label: Label
var continue_button: Button


func _ready() -> void:
	add_theme_constant_override("separation", 16)
	title_label = _label("경기 결과", 32, Color("#f2c14e"))
	result_label = _label("", 24, Color("#f4f1e8"))
	result_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	evidence_label = _label("", 17, Color("#d8d1c4"))
	evidence_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	history_label = _label("", 16, Color("#b7b0a3"))
	history_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	continue_button = Button.new()
	continue_button.text = "카일의 재방문 확인"
	continue_button.custom_minimum_size = Vector2(0.0, 72.0)
	continue_button.add_theme_font_size_override("font_size", 22)
	continue_button.pressed.connect(func() -> void: continue_requested.emit())
	for item in [title_label, result_label, evidence_label, history_label, continue_button]:
		add_child(item)


func configure(record: Dictionary) -> void:
	if result_label == null:
		return
	var result: Dictionary = record.get("result", {})
	var contributions: Dictionary = result.get("contributions", {})
	var effective: Array = result.get("effective_choices", [])
	var missing: Array = result.get("missing_conditions", [])
	var history: Array = record.get("history", [])
	result_label.text = "%s · 점수 %d\n%s" % [
		_result_name(str(result.get("result_id", ""))),
		int(result.get("score", 0)),
		str(result.get("result_text", "결과 기록이 생성되었습니다.")),
	]
	evidence_label.text = (
		"효과가 있었던 선택: %s\n"
		+ "부족했던 조건: %s\n"
		+ "기여 점수: %s\n"
		+ "명성 +%d · 관계 +%d"
	) % [
		_join_values(effective, "없음"),
		_join_values(missing, "없음"),
		_contribution_text(contributions),
		int(result.get("fame", 0)),
		int(result.get("relationship", 0)),
	]
	history_label.text = "장비 이력 %d건 · 소유자 %s · 보고 상태 %s" % [
		history.size(),
		str(record.get("owner_id", "")),
		str(record.get("report_state", "")),
	]


func _result_name(result_id: String) -> String:
	match result_id:
		"DEFEAT": return "패배"
		"WIN": return "승리"
		"DECISIVE_WIN": return "압도적 승리"
		_: return result_id


func _join_values(values: Array, fallback: String) -> String:
	var text_values: Array[String] = []
	for value in values:
		text_values.append(str(value))
	return fallback if text_values.is_empty() else ", ".join(text_values)


func _contribution_text(values: Dictionary) -> String:
	var parts: Array[String] = []
	for key in values:
		parts.append("%s +%d" % [str(key), int(values[key])])
	return "없음" if parts.is_empty() else ", ".join(parts)


func _label(value: String, size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = value
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	return label
