extends Control

const ForgingScreenScript = preload("res://scripts/ui/forging_screen.gd")
const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")
const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")
const VERSION_TEXT := "POC v0.6.3 · main · 2026.07.22.3"
const INVENTORY_CAPACITY := 6
const STARTING_GOLD := 25000000
const STARTING_MATERIAL_STOCK := {
	"whetstone": 20,
	"flame_stone": 20,
	"spirit_heart": 20,
	"salamander_core": 10,
	"guardian_powder": 10,
	"berserker_ember": 10,
}

var current_screen: Control
var enhance_button: Button
var inventory_button: Button
var inventory_overlay: Control
var version_badge: PanelContainer
var inventory: Array[Dictionary] = []
var workshop_resources = WorkshopResourcesScript.new(STARTING_GOLD, STARTING_MATERIAL_STOCK)
var auto_running: bool = false
var auto_weapon_template: Dictionary = {}


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_build_enhance_button()
	_build_inventory_button()
	_show_forging()
	_build_version_badge()
	set_process(true)


func _process(_delta: float) -> void:
	if current_screen == null or not is_instance_valid(current_screen):
		enhance_button.visible = false
		return
	if current_screen.get_script() == ForgingScreenScript:
		var forging_session = current_screen.get("session")
		enhance_button.visible = (
			forging_session != null
			and forging_session.state == ForgingSessionScript.State.COMPLETE
		)
	else:
		enhance_button.visible = false


func _build_enhance_button() -> void:
	enhance_button = Button.new()
	enhance_button.text = "완성한 철검 강화하기"
	enhance_button.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	enhance_button.position = Vector2(-270.0, -215.0)
	enhance_button.size = Vector2(540.0, 82.0)
	enhance_button.add_theme_font_size_override("font_size", 24)
	enhance_button.add_theme_color_override("font_color", Color("#241b0f"))
	enhance_button.add_theme_stylebox_override("normal", _button_style(Color("#f2c14e"), Color.WHITE, 20))
	enhance_button.add_theme_stylebox_override("pressed", _button_style(Color("#c99835"), Color.WHITE, 20))
	enhance_button.visible = false
	enhance_button.z_index = 70
	enhance_button.pressed.connect(_open_enhancement)
	add_child(enhance_button)


func _build_inventory_button() -> void:
	inventory_button = Button.new()
	inventory_button.text = "보관함 0/%d" % INVENTORY_CAPACITY
	inventory_button.set_anchors_preset(Control.PRESET_TOP_RIGHT)
	inventory_button.offset_left = -185.0
	inventory_button.offset_top = 12.0
	inventory_button.offset_right = -12.0
	inventory_button.offset_bottom = 64.0
	inventory_button.add_theme_font_size_override("font_size", 17)
	inventory_button.add_theme_stylebox_override("normal", _button_style(Color("#303641"), Color("#62a7d8"), 14))
	inventory_button.z_index = 80
	inventory_button.pressed.connect(_show_inventory)
	add_child(inventory_button)


func _show_forging() -> void:
	_close_inventory()
	_replace_screen(ForgingScreenScript.new())
	enhance_button.visible = false


func _open_enhancement() -> void:
	if current_screen == null:
		return
	var forging_session = current_screen.get("session")
	if forging_session == null:
		return
	var weapon_result: Dictionary = forging_session.result.duplicate(true)
	auto_weapon_template = weapon_result.duplicate(true)
	_show_enhancement_screen(weapon_result)
	enhance_button.visible = false


func _show_enhancement_screen(weapon_result: Dictionary) -> void:
	var enhancement_screen = EnhancementScreenScript.new()
	enhancement_screen.configure_weapon(weapon_result)
	enhancement_screen.set_inventory_count(inventory.size(), INVENTORY_CAPACITY)
	enhancement_screen.restart_requested.connect(_show_forging)
	enhancement_screen.store_requested.connect(_on_store_requested)
	enhancement_screen.inventory_requested.connect(_show_inventory)
	enhancement_screen.auto_forge_requested.connect(_on_auto_forge_requested)
	enhancement_screen.set_workshop_resources(workshop_resources)
	_replace_screen(enhancement_screen)


func _on_store_requested(weapon: Dictionary) -> void:
	if inventory.size() >= INVENTORY_CAPACITY or weapon.is_empty():
		return
	var stored := weapon.duplicate(true)
	stored["slot"] = inventory.size() + 1
	inventory.append(stored)
	_update_inventory_button()
	_show_forging()
	_show_inventory()



func _on_auto_forge_requested(options: Dictionary) -> void:
	if bool(options.get("stop", false)):
		auto_running = false
		if current_screen != null and current_screen.has_method("set_auto_status"):
			current_screen.set_auto_status("자동 단조 중지 요청 · 현재 시도 후 멈춥니다.")
		return
	if auto_running or inventory.size() >= INVENTORY_CAPACITY:
		return
	auto_running = true
	_run_auto_forge(options.duplicate(true))


func _run_auto_forge(options: Dictionary) -> void:
	var repeat_until_full := bool(options.get("repeat_until_full", false))
	var final_status := "자동 단조가 종료됐습니다."
	while auto_running and inventory.size() < INVENTORY_CAPACITY:
		var screen = current_screen
		if screen == null or not is_instance_valid(screen):
			final_status = "강화 화면을 찾지 못해 자동 단조를 중단했습니다."
			break
		screen.set_auto_running(true)
		var result: String = await _auto_enhance_current(screen, options)
		if result == "TARGET_REACHED":
			var record: Dictionary = screen.build_weapon_record()
			if record.is_empty():
				final_status = "보관할 무기 정보를 만들지 못했습니다."
				break
			_store_auto_weapon(record)
			final_status = "목표 강화 완료 · 보관함 %d/%d" % [inventory.size(), INVENTORY_CAPACITY]
			if not repeat_until_full or inventory.size() >= INVENTORY_CAPACITY:
				break
			_show_auto_enhancement()
			await get_tree().process_frame
			continue
		if result == "DESTROYED":
			final_status = "자동 단조 중 무기가 파괴됐습니다."
			if repeat_until_full and workshop_resources.gold > 0 and inventory.size() < INVENTORY_CAPACITY:
				_show_auto_enhancement()
				await get_tree().process_frame
				continue
			break
		if result == "NO_GOLD":
			final_status = "골드가 부족해 자동 단조를 중단했습니다."
			break
		if result == "STOPPED":
			final_status = "자동 단조를 중지했습니다."
			break
		final_status = "자동 단조 처리 중 오류가 발생했습니다."
		break

	auto_running = false
	if current_screen != null and is_instance_valid(current_screen):
		current_screen.set_auto_running(false)
		current_screen.set_auto_status(final_status)
	if not inventory.is_empty():
		_show_inventory()


func _auto_enhance_current(screen, options: Dictionary) -> String:
	var session = screen.get("session")
	if session == null:
		return "ERROR"
	var target_level := clampi(int(options.get("target_level", 10)), 1, int(session.config.get("max_level", 100)))
	var attempts := 0
	while auto_running and int(session.enhancement_level) < target_level and not bool(session.destroyed):
		attempts += 1
		if attempts > 2000:
			return "ERROR"
		var next_level := int(session.enhancement_level) + 1
		var desired_skill := str(options.get("skill_id", "balanced"))
		if desired_skill == "overdrive":
			if not session.can_use_skill_for_level("overdrive", next_level) or int(session.enhancement_level) + 2 > target_level:
				desired_skill = "balanced"
		if not session.set_skill(desired_skill):
			session.set_skill("balanced")

		var used_secondary := ""
		var used_catalyst := ""
		if session.uses_materials_for_level(next_level):
			used_secondary = workshop_resources.available_material_id(str(options.get("secondary_material_id", "")))
			used_catalyst = workshop_resources.available_material_id(str(options.get("catalyst_material_id", "")))
			session.set_secondary_material(used_secondary)
			session.set_catalyst_material(used_catalyst)

		var transaction: Dictionary = workshop_resources.try_begin_attempt(session, -1.0, -1.0, true)
		if not bool(transaction.get("ok", false)):
			if str(transaction.get("status", "")) == WorkshopResourcesScript.STATUS_NO_GOLD:
				return "NO_GOLD"
			return "ERROR"
		if int(session.state) == 1:
			session.precision_position = session.rng.randf()
			session.finish_precision()
		screen.set_auto_status("자동 단조 진행 · 현재 +%d / 목표 +%d · 보유 %sG" % [
			int(session.enhancement_level),
			target_level,
			_money(workshop_resources.gold),
		])
		await get_tree().create_timer(0.04).timeout
	if not auto_running:
		return "STOPPED"
	if bool(session.destroyed):
		return "DESTROYED"
	return "TARGET_REACHED" if int(session.enhancement_level) >= target_level else "ERROR"


func _show_auto_enhancement() -> void:
	# 반복 자동 단조는 최초 수동 제작의 GOOD/PERFECT 품질을 복제하지 않습니다.
	auto_weapon_template = {
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"raw_base_attack": 20,
		"base_attack": 20,
		"quality_id": "AUTO",
		"quality_label": "자동 단조 · 보통 마감",
		"quality_attack_multiplier": 1.0,
		"quality_value_multiplier": 1.0,
	}
	_show_enhancement_screen(auto_weapon_template)


func _store_auto_weapon(weapon: Dictionary) -> void:
	if inventory.size() >= INVENTORY_CAPACITY or weapon.is_empty():
		return
	var stored := weapon.duplicate(true)
	stored["slot"] = inventory.size() + 1
	inventory.append(stored)
	_update_inventory_button()


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
	layout.add_child(header)
	var title := _label("무기 보관함", 32, Color("#f4f1e8"))
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title)
	header.add_child(_label("%d / %d" % [inventory.size(), INVENTORY_CAPACITY], 24, Color("#f2c14e")))

	var guide := _label("제작과 강화를 끝낸 무기의 판매가, 강화비, 손익과 촉매 기록을 확인합니다.", 17, Color("#b7b0a3"))
	guide.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	layout.add_child(guide)

	if inventory.is_empty():
		var empty_panel := _panel(Color("#303641"))
		layout.add_child(empty_panel)
		var empty_label := _label("보관된 무기가 없습니다.\n철검을 제작하고 원하는 단계에서 보관하세요.", 20, Color("#b7b0a3"))
		empty_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		empty_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		empty_panel.add_child(empty_label)
	else:
		for weapon in inventory:
			layout.add_child(_weapon_card(weapon))

	var close_button := _action_button("대장간으로 돌아가기", Color("#8d4424"), Color("#f2c14e"))
	close_button.pressed.connect(_close_inventory)
	layout.add_child(close_button)
	_raise_fixed_ui()


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
	top.add_child(_label("슬롯 %d" % int(weapon.get("slot", 0)), 16, Color("#b7b0a3")))

	var raw_base_attack := int(weapon.get("raw_base_attack", weapon.get("base_attack", 20)))
	var base_attack := int(weapon.get("base_attack", raw_base_attack))
	var progression_attack := int(weapon.get("progression_attack", base_attack))
	var final_attack := int(weapon.get("final_attack", progression_attack))
	var quality_attack_multiplier := float(weapon.get("quality_attack_multiplier", 1.0))
	var quality_value_multiplier := float(weapon.get("quality_value_multiplier", 1.0))
	box.add_child(_label(
		"원본 공격력 %d · 품질 적용 %d(×%.2f) · 강화 %d · 최종 %d" % [
			raw_base_attack,
			base_attack,
			quality_attack_multiplier,
			progression_attack,
			final_attack,
		],
		19,
		Color("#f4f1e8")
	))
	box.add_child(_label("제작 가치 ×%.2f" % quality_value_multiplier, 16, Color("#b7b0a3")))

	var sale_price := int(weapon.get("sale_price", 0))
	var total_spent := int(weapon.get("total_spent", 0))
	var profit := int(weapon.get("estimated_profit", sale_price - total_spent))
	var profit_color := Color("#72b879") if profit >= 0 else Color("#e36c62")
	box.add_child(_label(
		"판매가 %sG · 누적 강화비 %sG · 예상 손익 %sG" % [
			_money(sale_price),
			_money(total_spent),
			_money(profit),
		],
		18,
		profit_color
	))

	var effect_label := _label("특수 강화 효과: %s" % str(weapon.get("special_effect_text", "없음")), 17, Color("#d9dde6"))
	effect_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(effect_label)

	var catalyst_label := _label(
		"촉매 기록: %s" % _format_catalyst_history(weapon.get("catalyst_history", [])),
		16,
		Color("#b7b0a3")
	)
	catalyst_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	box.add_child(catalyst_label)
	box.add_child(_label("마감: %s" % str(weapon.get("quality_label", "보통 마감")), 15, Color("#b7b0a3")))
	return panel


func _format_catalyst_history(history: Array) -> String:
	if history.is_empty():
		return "없음"
	var parts: Array[String] = []
	for value in history:
		if value is not Dictionary:
			continue
		var entry: Dictionary = value
		parts.append("+%d %s(%sG)" % [
			int(entry.get("level", 0)),
			str(entry.get("name", "촉매")),
			_money(int(entry.get("price", 0))),
		])
	return " · ".join(parts) if not parts.is_empty() else "없음"


func _close_inventory() -> void:
	if inventory_overlay != null and is_instance_valid(inventory_overlay):
		inventory_overlay.queue_free()
	inventory_overlay = null
	_update_inventory_button()
	if current_screen != null and current_screen.has_method("set_inventory_count"):
		current_screen.set_inventory_count(inventory.size(), INVENTORY_CAPACITY)


func _update_inventory_button() -> void:
	if inventory_button != null:
		inventory_button.text = "보관함 %d/%d" % [inventory.size(), INVENTORY_CAPACITY]


func _replace_screen(next_screen: Control) -> void:
	if current_screen != null and is_instance_valid(current_screen):
		current_screen.queue_free()
	current_screen = next_screen
	current_screen.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(current_screen)
	move_child(current_screen, 0)
	_raise_fixed_ui()


func _raise_fixed_ui() -> void:
	if enhance_button != null:
		move_child(enhance_button, get_child_count() - 1)
	if inventory_button != null:
		move_child(inventory_button, get_child_count() - 1)
	if inventory_overlay != null and is_instance_valid(inventory_overlay):
		move_child(inventory_overlay, get_child_count() - 1)
	if version_badge != null:
		move_child(version_badge, get_child_count() - 1)


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


func _money(value: int) -> String:
	var negative := value < 0
	var digits := str(absi(value))
	var chunks: Array[String] = []
	while digits.length() > 3:
		chunks.push_front(digits.right(3))
		digits = digits.left(digits.length() - 3)
	chunks.push_front(digits)
	return "%s%s" % ["-" if negative else "", ",".join(chunks)]


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
	button.custom_minimum_size = Vector2(0.0, 80.0)
	button.add_theme_font_size_override("font_size", 20)
	button.add_theme_stylebox_override("normal", _button_style(color, border_color, 17))
	return button


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
