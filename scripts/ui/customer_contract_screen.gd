class_name CustomerContractScreen
extends VBoxContainer

signal accepted

var config: Dictionary = {}
var title_label: Label
var detail_label: Label
var accept_button: Button


func _ready() -> void:
	add_theme_constant_override("separation", 18)
	title_label = _label("검투사 의뢰", 32, Color("#f2c14e"))
	detail_label = _label("", 19, Color("#f4f1e8"))
	detail_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	accept_button = Button.new()
	accept_button.text = "의뢰 수락"
	accept_button.custom_minimum_size = Vector2(0.0, 72.0)
	accept_button.add_theme_font_size_override("font_size", 24)
	accept_button.pressed.connect(func() -> void: accepted.emit())
	add_child(title_label)
	add_child(detail_label)
	add_child(accept_button)
	_refresh()


func configure(contract_config: Dictionary) -> void:
	config = contract_config.duplicate(true)
	_refresh()


func _refresh() -> void:
	if detail_label == null:
		return
	var preferred: Array[String] = []
	for value in config.get("preferred_affix_ids", []):
		preferred.append(_affix_name(str(value)))
	detail_label.text = (
		"고객: %s\n"
		+ "요청 장비: 철검\n"
		+ "필수 강화: +%d\n"
		+ "선택 목표: +%d에서 첫 수식어\n"
		+ "선호 수식어: %s\n"
		+ "기한: %d일 · 대금: %dG"
	) % [
		str(config.get("customer_name", "검투사 카일")),
		int(config.get("required_level", 5)),
		int(config.get("stretch_level", 10)),
		", ".join(preferred),
		int(config.get("deadline_days", 3)),
		int(config.get("payment_gold", 0)),
	]


func _affix_name(affix_id: String) -> String:
	match affix_id:
		"sharp": return "날카로운"
		"flaming": return "불타는"
		_: return affix_id


func _label(value: String, size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = value
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", color)
	return label
