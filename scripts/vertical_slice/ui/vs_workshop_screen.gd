# 작업대 화면에서 현재 정본 내구도·수리 상태를 표시하고 수리 실행을 연결한다.
class_name VSWorkshopScreen
extends Control

const RepairResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")
const MaintenanceServiceScript = preload("res://scripts/vertical_slice/services/vs_workshop_maintenance_service.gd")
const EnhancementResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd")
const EnhancementActionServiceScript = preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const WorkshopBackgroundTexture = preload("res://assets/ui/workshop/workshop_enhancement_background_v2.png")

signal enhancement_saved(envelope, result: Dictionary)

var _item = null
var _resources = null
var _maintenance_service = null
var _enhancement_action_service = null
var _save_service = null
var _campaign_envelope = null


func _ready() -> void:
	_ensure_illustrated_background()
	_ensure_enhancement_controls()
	var repair_button := get_node_or_null("WorkshopLayout/RepairButton") as Button
	if repair_button != null and not repair_button.pressed.is_connected(_on_repair_pressed):
		repair_button.pressed.connect(_on_repair_pressed)
	var enhancement_button := get_node_or_null("WorkshopLayout/EnhancementButton") as Button
	if enhancement_button != null and not enhancement_button.pressed.is_connected(_on_enhancement_pressed):
		enhancement_button.pressed.connect(_on_enhancement_pressed)
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
	var enhancement: Dictionary = EnhancementResolverScript.new().preview(_item, int(_item.enhancement_level) + 1)
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
	var result: Dictionary = _enhancement_action_service.resolve_and_save_with_rolls(
		_campaign_envelope,
		str(_item.uid),
		int(_item.enhancement_level) + 1,
		rolls,
		int(_campaign_envelope.active_run.get("current_day", 1)),
		_resources,
		_save_service
	)
	if str(result.get("outcome", "")) != "BLOCKED":
		_campaign_envelope = result.get("envelope", null)
		_item = _campaign_envelope.get_item(str(_item.uid)) if _campaign_envelope != null else null
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


func _refresh_controls() -> void:
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


func _has_enhancement_context() -> bool:
	return _item != null and _resources != null and _campaign_envelope != null and _save_service != null and _enhancement_action_service != null


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
		return "강화 불가: %s" % str(enhancement.get("reason", "UNKNOWN"))
	var outcomes: Dictionary = enhancement.get("display_outcomes", {})
	return "성공 %.1f%% · 실패 유지 %.1f%% · 실패 손상 %.1f%%" % [
		float(outcomes.get("success_percent", 0.0)),
		float(outcomes.get("failed_hold_percent", 0.0)),
		float(outcomes.get("failed_damage_percent", 0.0)),
	]


func _ensure_enhancement_controls() -> void:
	var layout := get_node_or_null("WorkshopLayout") as VBoxContainer
	if layout == null or layout.has_node("EnhancementButton"):
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
