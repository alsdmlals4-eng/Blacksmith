class_name WorkshopHud
extends HBoxContainer

var day_label: Label
var fatigue_label: Label
var gold_label: Label
var deadline_label: Label


func _ready() -> void:
	add_theme_constant_override("separation", 14)
	day_label = _label("1일차")
	fatigue_label = _label("작업 20 / 기본 20")
	gold_label = _label("0G")
	deadline_label = _label("기한 3일")
	for item in [day_label, fatigue_label, gold_label, deadline_label]:
		add_child(item)


func update_snapshot(calendar_snapshot: Dictionary, resource_snapshot: Dictionary, remaining_days: int) -> void:
	if day_label == null:
		return
	day_label.text = "%d일차" % int(calendar_snapshot.get("day", 1))
	fatigue_label.text = "현재 작업 %d / 기본 %d · 이월 %d" % [
		int(calendar_snapshot.get("current_fatigue", 0)),
		int(calendar_snapshot.get("base_fatigue", 0)),
		int(calendar_snapshot.get("carryover", 0)),
	]
	gold_label.text = "%dG" % int(resource_snapshot.get("gold", 0))
	deadline_label.text = "기한 %d일" % remaining_days


func _label(value: String) -> Label:
	var label := Label.new()
	label.text = value
	label.add_theme_font_size_override("font_size", 16)
	label.add_theme_color_override("font_color", Color("#f4f1e8"))
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	return label
