extends Control

const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const VERSION_TEXT := "POC v0.4.0 · main · 2026.07.21.2"
const INVENTORY_CAPACITY := 6

var current_screen: Control
var inventory: Array[Dictionary] = []
var inventory_overlay: Control
var version_badge: PanelContainer


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_show_enhancement_test()
	_build_version_badge()


func _show_enhancement_test() -> void:
	_close_inventory()
	if current_screen != null and is_instance_valid(current_screen):
		current_screen.queue_free()
	var screen = EnhancementScreenScript.new()
	screen.configure_weapon({
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"quality_id": "TEST",
		"quality_label": "테스트용 철검",
		"quality_multiplier": 1.0,
	})
	screen.set_inventory_count(inventory.size(), INVENTORY_CAPACITY)
	screen.restart_requested.connect(_show_enhancement_test)
	screen.store_requested.connect(_on_store_requested)
	screen.inventory_requested.connect(_show_inventory)
	current_screen = screen
	current_screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(current_screen)
	if version_badge != null:
		move_child(version_badge, get_child_count() - 1)


func _on_store_requested(weapon: Dictionary) -> void:
	if inventory.size() >= INVENTORY_CAPACITY or weapon.is_empty():
		return
	var stored := weapon.duplicate(true)
	stored["slot"] = inventory.size() + 1
	inventory.append(stored)
	_show_enhancement_test()
	_show_inventory()


func _show_inventory() -> void:
	_close_inventory()
	inventory_overlay = Control.new()
	inventory_overlay.name = "InventoryOverlay"
	inventory_overlay.z_index = 90
	inventory_overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(inventory_overlay)

	var background := ColorRect.new()
	background.color = Color("#17191f")
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	inventory_overlay.add_child(background)

	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_top", 24)
	margin.add_theme_constant_override("margin_bottom", 70)
	inventory_overlay.add_child(margin)

	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	margin.add_child(scroll)
	var layout := VBoxContainer.new()
	layout.custom_minimum_size = Vector2(672.0, 0.0)
	layout.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	layout.add_theme_constant_override("separation", 14)
	scroll.add_child(layout)

	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation", 10)
	layout.add_child(header)
	var title := _label("무기 보관함", 32, Color("#f4f1e8"))
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title)
	var count := _label("%d / %d" % [inventory.size(), INVENTORY_CAPACITY], 24, Color("#f2c14e"))
	header.add_child(count)

	var guide := _label("강화를 끝낸 무기의 기본 능력과 특수 강화 효과를 확인합니다.", 17, Color("#b7b0a3"))
	guide.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(guide)

	if inventory.is_empty():
		var empty_panel := _panel(Color("#303641"))
		layout.add_child(empty_panel)
		var empty_label := _label("보관된 무기가 없습니다.\n강화 화면에서 ‘강화 종료 및 보관’을 누르세요.", 20, Color("#b7b0a3"))
		empty_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		empty_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		empty_panel.add_child(empty_label)
	else:
		for weapon in inventory:
			layout.add_child(_weapon_card(weapon))

	var actions := HBoxContainer.new()
	actions.add_theme_constant_override("separation", 10)
	layout.add_child(actions)
	var close_button := _action_button("강화 화면으로", Color("#303641"), Color("#62a7d8"))
	close_button.pressed.connect(_close_inventory)
	actions.add_child(close_button)
	var new_button := _action_button("새 철검 강화", Color("#8d4424"), Color("#f2c14e"))
	new_button.pressed.connect(_show_enhancement_test)
	actions.add_child(new_button)

	if version_badge != null:
		move_child(version_badge, get_child_count() - 1)


func _weapon_card(weapon: Dictionary) -> PanelContainer:
	var panel := _panel(Color("#303641"))
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 8)
	panel.add_child(box)

	var top := HBoxContainer.new()
	box.add_child(top)
	var name_label := _label(str(weapon.get("weapon_name", "철검")), 24, Color("#f2c14e"))
	name_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	top.add_child(name_label)
	var slot_label := _label("슬롯 %d" % int(weapon.get("slot", 0)), 16, Color("#b7b0a3"))
	top.add_child(slot_label)

	var base_attack := int(weapon.get("base_attack", 10))
	var bonus := int(weapon.get("enhancement_bonus", 0))
	var final_attack := int(weapon.get("final_attack", base_attack + bonus))
	var stat_label := _label("기본 공격력 %d (+%d) · 강화 적용 %d" % [base_attack, bonus, final_attack], 19, Color("#f4f1e8"))
	box.add_child(stat_label)

	var effect_label := _label("특수 강화 효과: %s" % str(weapon.get("special_effect_text", "없음")), 17, Color("#d9dde6"))
	effect_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(effect_label)

	var quality_label := _label("마감: %s" % str(weapon.get("quality_label", "보통 마감")), 15, Color("#b7b0a3"))
	box.add_child(quality_label)
	return panel


func _close_inventory() -> void:
	if inventory_overlay != null and is_instance_valid(inventory_overlay):
		inventory_overlay.queue_free()
	inventory_overlay = null
	if current_screen != null and current_screen.has_method("set_inventory_count"):
		current_screen.set_inventory_count(inventory.size(), INVENTORY_CAPACITY)


func _build_version_badge() -> void:
	version_badge = PanelContainer.new()
	version_badge.name = "VersionBadge"
	version_badge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	version_badge.z_index = 100
	version_badge.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	version_badge.offset_left = -315.0
	version_badge.offset_top = -52.0
	version_badge.offset_right = -12.0
	version_badge.offset_bottom = -12.0
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.06, 0.08, 0.88)
	style.border_color = Color(0.45, 0.49, 0.57, 0.8)
	style.set_border_width_all(1)
	style.corner_radius_top_left = 10
	style.corner_radius_top_right = 10
	style.corner_radius_bottom_left = 10
	style.corner_radius_bottom_right = 10
	style.content_margin_left = 12.0
	style.content_margin_right = 12.0
	style.content_margin_top = 7.0
	style.content_margin_bottom = 7.0
	version_badge.add_theme_stylebox_override("panel", style)
	var label := Label.new()
	label.text = VERSION_TEXT
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", Color("#d9dde6"))
	version_badge.add_child(label)
	add_child(version_badge)


func _label(text_value: String, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	return label


func _panel(color: Color) -> PanelContainer:
	var panel := PanelContainer.new()
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.corner_radius_top_left = 20
	style.corner_radius_top_right = 20
	style.corner_radius_bottom_left = 20
	style.corner_radius_bottom_right = 20
	style.content_margin_left = 20.0
	style.content_margin_right = 20.0
	style.content_margin_top = 16.0
	style.content_margin_bottom = 16.0
	panel.add_theme_stylebox_override("panel", style)
	return panel


func _action_button(text_value: String, color: Color, border_color: Color) -> Button:
	var button := Button.new()
	button.text = text_value
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.custom_minimum_size = Vector2(0.0, 80.0)
	button.add_theme_font_size_override("font_size", 20)
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.border_color = border_color
	style.set_border_width_all(2)
	style.corner_radius_top_left = 17
	style.corner_radius_top_right = 17
	style.corner_radius_bottom_left = 17
	style.corner_radius_bottom_right = 17
	button.add_theme_stylebox_override("normal", style)
	return button
