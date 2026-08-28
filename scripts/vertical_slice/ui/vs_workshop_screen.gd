# 작업대 화면에서 현재 정본 내구도·수리 상태를 표시하고 수리 실행을 연결한다.
class_name VSWorkshopScreen
extends Control

const RepairResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")
const MaintenanceServiceScript = preload("res://scripts/vertical_slice/services/vs_workshop_maintenance_service.gd")
const EnhancementResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd")
const EnhancementActionServiceScript = preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const PrecisionResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")
const WorkshopBackgroundTexture = preload("res://assets/ui/workshop/workshop_enhancement_background_v2.png")
const WorkpieceDurabilityStateAtlasTexture = preload("res://assets/ui/workshop/workpiece_durability_state_atlas_v1.png")

signal enhancement_saved(envelope, result: Dictionary)

var _item = null
var _resources = null
var _maintenance_service = null
var _enhancement_action_service = null
var _save_service = null
var _campaign_envelope = null


func _ready() -> void:
	_ensure_illustrated_background()
	_ensure_workpiece_durability_hero()
	_ensure_enhancement_controls()
	var repair_button := get_node_or_null("WorkshopLayout/RepairButton") as Button
	if repair_button != null and not repair_button.pressed.is_connected(_on_repair_pressed):
		repair_button.pressed.connect(_on_repair_pressed)
	var enhancement_button := get_node_or_null("WorkshopLayout/EnhancementButton") as Button
	if enhancement_button != null and not enhancement_button.pressed.is_connected(_on_enhancement_pressed):
		enhancement_button.pressed.connect(_on_enhancement_pressed)
	var lineage_option := get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	if lineage_option != null and not lineage_option.item_selected.is_connected(_on_precision_selection_changed):
		lineage_option.item_selected.connect(_on_precision_selection_changed)
	var method_option := get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
	if method_option != null and not method_option.item_selected.is_connected(_on_precision_selection_changed):
		method_option.item_selected.connect(_on_precision_selection_changed)
	var backfill_button := get_node_or_null("WorkshopLayout/PrecisionBackfillButton") as Button
	if backfill_button != null and not backfill_button.pressed.is_connected(_on_precision_backfill_pressed):
		backfill_button.pressed.connect(_on_precision_backfill_pressed)
	_refresh_controls()


func configure_context(item, resources, maintenance_service = null, enhancement_action_service = null, save_service = null, campaign_envelope = null) -> void:
	_item = item
	_resources = resources
	_maintenance_service = maintenance_service if maintenance_service != null else MaintenanceServiceScript.new()
	_enhancement_action_service = enhancement_action_service if enhancement_action_service != null else EnhancementActionServiceScript.new()
	_save_service = save_service
	_campaign_envelope = campaign_envelope
	_refresh_controls()


func view_state() -> Dictionary:
	if _item == null:
		return {
			"has_item": false,
			"durability_text": "작품 선택 필요",
			"durability_state": "UNAVAILABLE",
			"repair_allowed": false,
			"repair_reason": "MISSING_ITEM",
			"repair_gold_cost": 0,
			"repair_material_units": 0,
			"repair_quality_summary": "",
			"repair_scar_summary": "",
			"repair_job_summary": "",
		}
	var quote: Dictionary = RepairResolverScript.new().quote(_item)
	var precision_mode := _precision_mode()
	var precision_selection := _precision_selection()
	var enhancement: Dictionary = EnhancementResolverScript.new().preview(
		_item,
		int(_item.enhancement_level) + 1,
		precision_selection
	)
	var precision_preview: Dictionary = {}
	if precision_mode == "ATTEMPT":
		precision_preview = enhancement.get("precision_tag_preview", {})
	elif precision_mode == "BACKFILL":
		precision_preview = PrecisionResolverScript.new().backfill_preview(_item, precision_selection, true)
		enhancement["allowed"] = false
		enhancement["reason"] = "PRECISION_PLACEHOLDER_REQUIRES_BACKFILL"
	elif precision_mode == "BACKFILL_INELIGIBLE":
		precision_preview = {"allowed": false, "reason": "PRECISION_PLACEHOLDER_SOURCE_INELIGIBLE"}
		enhancement["allowed"] = false
		enhancement["reason"] = "PRECISION_PLACEHOLDER_SOURCE_INELIGIBLE"
	var recovery: Dictionary = quote.get("quality_recovery_percent", {})
	var repair_allowed := bool(quote.get("allowed", false))
	return {
		"has_item": true,
		"durability_text": "%d / %d / %d" % [int(_item.current_durability), int(_item.max_durability), int(_item.base_max_durability)],
		"durability_state": str(_item.effective_durability_state()),
		"repair_allowed": repair_allowed,
		"repair_reason": str(quote.get("reason", "")),
		"repair_gold_cost": int(quote.get("gold_cost", 0)),
		"repair_material_units": int(quote.get("reinforcement_units", 0)),
		"repair_quality_summary": "예상 회복: 최상 %d%% / 표준 %d%% / 미흡 %d%%" % [int(recovery.get("EXCELLENT", 0)), int(recovery.get("STANDARD", 0)), int(recovery.get("POOR", 0))] if repair_allowed else "",
		"repair_scar_summary": "MAX 흉터 가능성: %d%%" % int(quote.get("max_scar_chance_percent", 0)) if repair_allowed else "",
		"repair_job_summary": "수리하면 다음 실제 손상 전까지 다시 수리할 수 없습니다" if repair_allowed and bool(quote.get("repair_job_consumed_on_start", false)) else "",
		"enhancement_allowed": bool(enhancement.get("allowed", false)) and _has_enhancement_context(),
		"enhancement_reason": str(enhancement.get("reason", "")),
		"enhancement_target_level": int(enhancement.get("target_level", 0)),
		"enhancement_cost_summary": "비용: %d Gold · 보강재 %d개" % [int(enhancement.get("gold_cost", 0)), int(enhancement.get("reinforcement_units", 0))],
		"enhancement_outcomes_summary": _enhancement_outcomes_summary(enhancement),
		"precision_visible": precision_mode == "ATTEMPT" or precision_mode == "BACKFILL",
		"precision_mode": precision_mode,
		"precision_tag_id": str(precision_preview.get("tag_id", "")),
		"precision_preview_summary": _precision_preview_summary(precision_preview, precision_mode),
		"precision_backfill_allowed": precision_mode == "BACKFILL" and bool(precision_preview.get("allowed", false)) and _has_enhancement_context(),
	}


func request_repair_with_rolls(rolls: Dictionary) -> Dictionary:
	if _item == null or _resources == null:
		return {"status": "BLOCKED", "reason": "MISSING_WORKSHOP_CONTEXT"}
	if _maintenance_service == null:
		_maintenance_service = MaintenanceServiceScript.new()
	var result: Dictionary = _maintenance_service.try_repair_with_rolls(_item, _resources, rolls)
	_refresh_controls()
	return result


func request_repair() -> Dictionary:
	if _item == null or _resources == null:
		return {"status": "BLOCKED", "reason": "MISSING_WORKSHOP_CONTEXT"}
	if _maintenance_service == null:
		_maintenance_service = MaintenanceServiceScript.new()
	var result: Dictionary = _maintenance_service.try_repair(_item, _resources)
	_refresh_controls()
	return result


func request_enhancement_with_rolls(rolls: Dictionary) -> Dictionary:
	if not _has_enhancement_context():
		return {"outcome": "BLOCKED", "reason": "MISSING_ENHANCEMENT_CONTEXT"}
	var target_level := int(_item.enhancement_level) + 1
	var item_uid := str(_item.uid)
	var result: Dictionary = _enhancement_action_service.resolve_and_save_with_rolls(
		_campaign_envelope,
		item_uid,
		target_level,
		rolls,
		int(_campaign_envelope.active_run.get("current_day", 1)),
		_resources,
		_save_service,
		_precision_selection()
	)
	if str(result.get("outcome", "")) != "BLOCKED":
		_campaign_envelope = result.get("envelope", null)
		_item = _campaign_envelope.get_item(item_uid) if _campaign_envelope != null else null
		if target_level == 10:
			_clear_precision_selection()
		enhancement_saved.emit(_campaign_envelope, result)
	_refresh_controls()
	return result


func request_precision_backfill() -> Dictionary:
	if not _has_enhancement_context():
		return {"outcome": "BLOCKED", "reason": "MISSING_ENHANCEMENT_CONTEXT"}
	var item_uid := str(_item.uid)
	var result: Dictionary = _enhancement_action_service.backfill_precision_tag_and_save(
		_campaign_envelope,
		item_uid,
		_precision_selection(),
		_save_service
	)
	if str(result.get("outcome", "")) == "APPLIED":
		_campaign_envelope = result.get("envelope", null)
		_item = _campaign_envelope.get_item(item_uid) if _campaign_envelope != null else null
		_clear_precision_selection()
		enhancement_saved.emit(_campaign_envelope, result)
	_refresh_controls()
	return result


func request_enhancement() -> Dictionary:
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	return request_enhancement_with_rolls({
		"success_roll_percent": rng.randf_range(0.0, 100.0),
		"damage_roll_percent": rng.randf_range(0.0, 100.0),
	})


func refresh_after_enhancement() -> void:
	_refresh_controls()


func set_precision_selection(lineage_id: String, method_id: String) -> void:
	_select_precision_option("WorkshopLayout/PrecisionLineageOption", lineage_id)
	_select_precision_option("WorkshopLayout/PrecisionMethodOption", method_id)
	_refresh_controls()


func _on_repair_pressed() -> void:
	var result := request_repair()
	var message := get_node_or_null("WorkshopLayout/RepairMessageLabel") as Label
	if message != null:
		message.text = "수리 완료" if str(result.get("status", "")) == "APPLIED" else "수리 불가: %s" % str(result.get("reason", "UNKNOWN"))


func _on_enhancement_pressed() -> void:
	var result := request_enhancement()
	var message := get_node_or_null("WorkshopLayout/EnhancementMessageLabel") as Label
	if message != null:
		message.text = "강화 결과: %s" % str(result.get("outcome", "BLOCKED"))


func _on_precision_selection_changed(_index: int) -> void:
	_refresh_controls()


func _on_precision_backfill_pressed() -> void:
	var result := request_precision_backfill()
	var message := get_node_or_null("WorkshopLayout/EnhancementMessageLabel") as Label
	if message != null:
		message.text = "정밀 태그 정정 완료" if str(result.get("outcome", "")) == "APPLIED" else "정밀 태그 정정 불가"


func _refresh_controls() -> void:
	_ensure_workpiece_durability_hero()
	_ensure_enhancement_controls()
	var state := view_state()
	var durability := get_node_or_null("WorkshopLayout/DurabilityValueLabel") as Label
	var condition := get_node_or_null("WorkshopLayout/DurabilityStateLabel") as Label
	var quote := get_node_or_null("WorkshopLayout/RepairQuoteLabel") as Label
	var quality := get_node_or_null("WorkshopLayout/RepairQualityLabel") as Label
	var scar := get_node_or_null("WorkshopLayout/RepairScarLabel") as Label
	var job := get_node_or_null("WorkshopLayout/RepairJobLabel") as Label
	var repair_button := get_node_or_null("WorkshopLayout/RepairButton") as Button
	var enhancement_quote := get_node_or_null("WorkshopLayout/EnhancementQuoteLabel") as Label
	var enhancement_outcomes := get_node_or_null("WorkshopLayout/EnhancementOutcomesLabel") as Label
	var enhancement_button := get_node_or_null("WorkshopLayout/EnhancementButton") as Button
	var precision_title := get_node_or_null("WorkshopLayout/PrecisionTitleLabel") as Label
	var precision_lineage_label := get_node_or_null("WorkshopLayout/PrecisionLineageLabel") as Label
	var precision_lineage_option := get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	var precision_method_label := get_node_or_null("WorkshopLayout/PrecisionMethodLabel") as Label
	var precision_method_option := get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
	var precision_preview := get_node_or_null("WorkshopLayout/PrecisionPreviewLabel") as Label
	var precision_backfill_button := get_node_or_null("WorkshopLayout/PrecisionBackfillButton") as Button
	if durability != null:
		durability.text = str(state["durability_text"])
	if condition != null:
		condition.text = "상태: %s" % _player_facing_durability_state(str(state["durability_state"]))
	if quote != null:
		quote.text = "수리: %d Gold · 보강재 %d개" % [int(state["repair_gold_cost"]), int(state["repair_material_units"])] if bool(state["repair_allowed"]) else "수리 불가: %s" % _player_facing_repair_reason(str(state["repair_reason"]))
	if quality != null:
		quality.text = str(state["repair_quality_summary"])
	if scar != null:
		scar.text = str(state["repair_scar_summary"])
	if job != null:
		job.text = str(state["repair_job_summary"])
	if repair_button != null:
		repair_button.disabled = not bool(state["repair_allowed"])
	if enhancement_quote != null:
		enhancement_quote.text = "다음 강화 +%d · %s" % [int(state.get("enhancement_target_level", 0)), str(state.get("enhancement_cost_summary", ""))]
	if enhancement_outcomes != null:
		enhancement_outcomes.text = str(state.get("enhancement_outcomes_summary", ""))
	if enhancement_button != null:
		enhancement_button.disabled = not bool(state.get("enhancement_allowed", false))
	var precision_visible := bool(state.get("precision_visible", false))
	for control in [precision_title, precision_lineage_label, precision_lineage_option, precision_method_label, precision_method_option, precision_preview]:
		if control != null:
			control.visible = precision_visible
	if precision_preview != null:
		precision_preview.text = str(state.get("precision_preview_summary", ""))
	if precision_lineage_option != null:
		precision_lineage_option.disabled = not precision_visible
	if precision_method_option != null:
		precision_method_option.disabled = not precision_visible
	if precision_backfill_button != null:
		precision_backfill_button.visible = str(state.get("precision_mode", "")) == "BACKFILL"
		precision_backfill_button.disabled = not bool(state.get("precision_backfill_allowed", false))


func _has_enhancement_context() -> bool:
	return _item != null and _resources != null and _campaign_envelope != null and _save_service != null and _enhancement_action_service != null


func _precision_mode() -> String:
	if _item == null:
		return ""
	if int(_item.enhancement_level) == 9:
		return "ATTEMPT"
	if int(_item.enhancement_level) >= 10 and str(_item.catalyst_affix) == "PRECISION_KEYWORD_PENDING_CONTENT":
		return "BACKFILL" if _legacy_v3_precision_backfill_eligible() else "BACKFILL_INELIGIBLE"
	return ""


func _legacy_v3_precision_backfill_eligible() -> bool:
	return _campaign_envelope != null and _campaign_envelope.has_method("is_legacy_v3_precision_backfill_eligible") and _campaign_envelope.is_legacy_v3_precision_backfill_eligible(str(_item.uid))


func _precision_selection() -> Dictionary:
	var lineage_option := get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method_option := get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
	var lineage_id := ""
	var method_id := ""
	if lineage_option != null and lineage_option.get_selected() >= 0:
		lineage_id = str(lineage_option.get_item_metadata(lineage_option.get_selected()))
	if method_option != null and method_option.get_selected() >= 0:
		method_id = str(method_option.get_item_metadata(method_option.get_selected()))
	return {"lineage_id": lineage_id, "method_id": method_id}


func _clear_precision_selection() -> void:
	var lineage_option := get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method_option := get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
	if lineage_option != null:
		lineage_option.select(0)
	if method_option != null:
		method_option.select(0)


func _select_precision_option(path: NodePath, target_id: String) -> void:
	var option := get_node_or_null(path) as OptionButton
	if option == null:
		return
	for index in range(option.item_count):
		if str(option.get_item_metadata(index)) == target_id:
			option.select(index)
			return
	option.select(0)


func _player_facing_durability_state(state: String) -> String:
	match state:
		"NORMAL":
			return "정상"
		"MINOR":
			return "경미 손상"
		"MAJOR":
			return "심각 손상"
		"DESTROYED":
			return "파괴됨"
		_:
			return "작품 없음"


func _player_facing_repair_reason(reason: String) -> String:
	match reason:
		"REPAIR_JOB_UNAVAILABLE":
			return "실제 손상 후 수리 가능"
		"FULL_DURABILITY":
			return "현재 내구도가 가득 참"
		"ITEM_DESTROYED":
			return "파괴된 작품은 수리할 수 없음"
		"MISSING_ITEM":
			return "작품을 선택하세요"
		_:
			return reason


func _enhancement_outcomes_summary(enhancement: Dictionary) -> String:
	if not bool(enhancement.get("allowed", false)):
		return "강화 불가: %s" % _player_facing_enhancement_reason(str(enhancement.get("reason", "UNKNOWN")))
	var outcomes: Dictionary = enhancement.get("display_outcomes", {})
	return "성공 %.1f%% · 실패 유지 %.1f%% · 실패 손상 %.1f%%" % [
		float(outcomes.get("success_percent", 0.0)),
		float(outcomes.get("failed_hold_percent", 0.0)),
		float(outcomes.get("failed_damage_percent", 0.0)),
	]


func _precision_preview_summary(preview: Dictionary, mode: String) -> String:
	if mode.is_empty():
		return ""
	if not bool(preview.get("allowed", false)):
		return _player_facing_enhancement_reason(str(preview.get("reason", "")))
	var axis_label := "역할 능력치" if str(preview.get("effect_axis", "")) == "RAW_ROLE_STAT" else "무게"
	return "결과 태그: %s · %s %d → %d · 내구도 변화 없음" % [
		str(preview.get("tag_display_name_ko", "")),
		axis_label,
		int(preview.get("before_value", 0)),
		int(preview.get("after_value", 0)),
	]


func _player_facing_enhancement_reason(reason: String) -> String:
	match reason:
		"MISSING_CATALYST_LINEAGE":
			return "촉매 계보를 고르세요"
		"MISSING_PRECISION_METHOD":
			return "정밀 강화 방식을 고르세요"
		"INVALID_PRECISION_TAG_COMBINATION":
			return "선택한 정밀 조합을 확인하세요"
		"PRECISION_PLACEHOLDER_REQUIRES_BACKFILL":
			return "정밀 태그 정정을 먼저 완료하세요"
		"PRECISION_PLACEHOLDER_SOURCE_INELIGIBLE":
			return "정밀 태그 상태를 확인할 수 없습니다"
		"CATALYST_AFFIX_ALREADY_RESOLVED":
			return "이미 정밀 태그가 적용된 작품입니다"
		"CATALYST_AFFIX_UNKNOWN_FAIL_CLOSED":
			return "정밀 태그 상태를 확인할 수 없습니다"
		_:
			return reason


func _ensure_enhancement_controls() -> void:
	var layout := get_node_or_null("WorkshopLayout") as VBoxContainer
	if layout == null:
		return
	if layout.has_node("EnhancementButton"):
		_populate_precision_options()
		return
	var nodes: Array[Control] = []
	var title := Label.new()
	title.name = "EnhancementTitleLabel"
	title.text = "다음 강화"
	title.add_theme_font_size_override("font_size", 20)
	nodes.append(title)
	var quote := Label.new()
	quote.name = "EnhancementQuoteLabel"
	quote.add_theme_font_size_override("font_size", 18)
	nodes.append(quote)
	var outcomes := Label.new()
	outcomes.name = "EnhancementOutcomesLabel"
	outcomes.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	outcomes.add_theme_font_size_override("font_size", 17)
	nodes.append(outcomes)
	var precision_title := Label.new()
	precision_title.name = "PrecisionTitleLabel"
	precision_title.text = "정밀 강화 · +9 → +10"
	precision_title.add_theme_font_size_override("font_size", 20)
	nodes.append(precision_title)
	var precision_lineage_label := Label.new()
	precision_lineage_label.name = "PrecisionLineageLabel"
	precision_lineage_label.text = "촉매 계보"
	precision_lineage_label.add_theme_font_size_override("font_size", 18)
	nodes.append(precision_lineage_label)
	var precision_lineage_option := OptionButton.new()
	precision_lineage_option.name = "PrecisionLineageOption"
	precision_lineage_option.custom_minimum_size = Vector2(0, 48)
	precision_lineage_option.add_theme_font_size_override("font_size", 18)
	nodes.append(precision_lineage_option)
	var precision_method_label := Label.new()
	precision_method_label.name = "PrecisionMethodLabel"
	precision_method_label.text = "정밀 강화 방식"
	precision_method_label.add_theme_font_size_override("font_size", 18)
	nodes.append(precision_method_label)
	var precision_method_option := OptionButton.new()
	precision_method_option.name = "PrecisionMethodOption"
	precision_method_option.custom_minimum_size = Vector2(0, 48)
	precision_method_option.add_theme_font_size_override("font_size", 18)
	nodes.append(precision_method_option)
	var precision_preview := Label.new()
	precision_preview.name = "PrecisionPreviewLabel"
	precision_preview.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	precision_preview.add_theme_font_size_override("font_size", 17)
	nodes.append(precision_preview)
	var precision_backfill_button := Button.new()
	precision_backfill_button.name = "PrecisionBackfillButton"
	precision_backfill_button.text = "정밀 태그 정정 적용"
	precision_backfill_button.custom_minimum_size = Vector2(0, 56)
	precision_backfill_button.add_theme_font_size_override("font_size", 20)
	nodes.append(precision_backfill_button)
	var button := Button.new()
	button.name = "EnhancementButton"
	button.text = "강화 시도"
	button.custom_minimum_size = Vector2(0, 64)
	button.add_theme_font_size_override("font_size", 22)
	nodes.append(button)
	var message := Label.new()
	message.name = "EnhancementMessageLabel"
	message.add_theme_font_size_override("font_size", 18)
	nodes.append(message)
	var repair_index := layout.get_node("RepairButton").get_index()
	for node in nodes:
		layout.add_child(node)
		layout.move_child(node, repair_index)
		repair_index += 1
	_populate_precision_options()


func _populate_precision_options() -> void:
	var lineage_option := get_node_or_null("WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method_option := get_node_or_null("WorkshopLayout/PrecisionMethodOption") as OptionButton
	if lineage_option == null or method_option == null:
		return
	if lineage_option.item_count > 0 and method_option.item_count > 0:
		return
	var catalog := PrecisionResolverScript.new().catalog()
	lineage_option.clear()
	lineage_option.add_item("촉매 계보를 고르세요")
	lineage_option.set_item_metadata(0, "")
	for lineage in catalog.get("lineages", []):
		if lineage is Dictionary:
			lineage_option.add_item(str(lineage.get("display_name_ko", "")))
			lineage_option.set_item_metadata(lineage_option.item_count - 1, str(lineage.get("id", "")))
	lineage_option.select(0)
	method_option.clear()
	method_option.add_item("정밀 강화 방식을 고르세요")
	method_option.set_item_metadata(0, "")
	for method in catalog.get("methods", []):
		if method is Dictionary:
			method_option.add_item(str(method.get("display_name_ko", "")))
			method_option.set_item_metadata(method_option.item_count - 1, str(method.get("id", "")))
	method_option.select(0)


func _ensure_illustrated_background() -> void:
	var fallback := get_node_or_null("WorkshopBackground") as ColorRect
	if fallback != null:
		fallback.visible = false
	var background := get_node_or_null("WorkshopIllustratedBackground") as TextureRect
	if background == null:
		background = TextureRect.new()
		background.name = "WorkshopIllustratedBackground"
		background.z_index = -1
		background.mouse_filter = Control.MOUSE_FILTER_IGNORE
		background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		add_child(background)
		move_child(background, 0)
	background.texture = WorkshopBackgroundTexture


func _ensure_workpiece_durability_hero() -> void:
	var layout := get_node_or_null("WorkshopLayout") as VBoxContainer
	if layout == null:
		return
	var hero := layout.get_node_or_null("WorkpieceDurabilityHero") as TextureRect
	if hero == null:
		hero = TextureRect.new()
		hero.name = "WorkpieceDurabilityHero"
		hero.custom_minimum_size = Vector2(0, 176)
		hero.mouse_filter = Control.MOUSE_FILTER_IGNORE
		hero.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		hero.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		layout.add_child(hero)
		layout.move_child(hero, min(1, layout.get_child_count() - 1))
	if _item == null:
		hero.visible = false
		return
	var state := str(_item.effective_durability_state())
	hero.visible = true
	hero.texture = _workpiece_texture_for_durability_state(state)
	hero.tooltip_text = "작품 상태: %s" % _player_facing_durability_state(state)


func _workpiece_texture_for_durability_state(state: String) -> AtlasTexture:
	var cell_width := int(WorkpieceDurabilityStateAtlasTexture.get_width() / 2)
	var cell_height := int(WorkpieceDurabilityStateAtlasTexture.get_height() / 2)
	var origin := Vector2.ZERO
	match state:
		"MINOR":
			origin = Vector2(cell_width, 0)
		"MAJOR":
			origin = Vector2(0, cell_height)
		"DESTROYED":
			origin = Vector2(cell_width, cell_height)
	var texture := AtlasTexture.new()
	texture.atlas = WorkpieceDurabilityStateAtlasTexture
	texture.region = Rect2(origin, Vector2(cell_width, cell_height))
	return texture
