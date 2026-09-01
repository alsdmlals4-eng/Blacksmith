# 작업대 화면에서 현재 정본 내구도·수리 상태를 표시하고 수리 실행을 연결한다.
class_name VSWorkshopScreen
extends Control

const RepairResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")
const MaintenanceServiceScript = preload("res://scripts/vertical_slice/services/vs_workshop_maintenance_service.gd")
const EnhancementResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd")
const EnhancementActionServiceScript = preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const PrecisionResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_precision_resolver.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const EquipmentCatalogScript = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
const WorkshopBackgroundTexture = preload("res://assets/ui/workshop/workshop_enhancement_background_v2.png")
const WorkpieceDurabilityStateAtlasTexture = preload("res://assets/ui/workshop/workpiece_durability_state_atlas_v1.png")

# The project previews a 720px canvas in a 360px mobile window. These source
# values retain a 14px body and 48px minimum touch target in that preview.
const MOBILE_BODY_FONT_SIZE := 28
const MOBILE_SECTION_FONT_SIZE := 35
const MOBILE_TITLE_FONT_SIZE := 44
const WIREFRAME_CARD_TITLE_FONT_SIZE := 30
const MOBILE_TOUCH_TARGET_HEIGHT := 96
const MOBILE_PRIMARY_TOUCH_TARGET_HEIGHT := 112

const MOBILE_TITLE_CONTROL_PATHS := [
	"WorkshopScroll/WorkshopLayout/WorkshopTitle",
	"WorkshopScroll/WorkshopLayout/DurabilityValueLabel",
]
const MOBILE_SECTION_CONTROL_PATHS := [
	"WorkshopScroll/WorkshopLayout/DurabilityTitleLabel",
	"WorkshopScroll/WorkshopLayout/EnhancementTitleLabel",
	"WorkshopScroll/WorkshopLayout/PrecisionTitleLabel",
]
const MOBILE_BODY_CONTROL_PATHS := [
	"WorkshopScroll/WorkshopLayout/DurabilityStateLabel",
	"WorkshopScroll/WorkshopLayout/RepairQuoteLabel",
	"WorkshopScroll/WorkshopLayout/RepairQualityLabel",
	"WorkshopScroll/WorkshopLayout/RepairScarLabel",
	"WorkshopScroll/WorkshopLayout/RepairJobLabel",
	"WorkshopScroll/WorkshopLayout/EnhancementQuoteLabel",
	"WorkshopScroll/WorkshopLayout/EnhancementOutcomesLabel",
	"WorkshopScroll/WorkshopLayout/PrecisionActionLabel",
	"WorkshopScroll/WorkshopLayout/PrecisionTagLabel",
	"WorkshopScroll/WorkshopLayout/PrecisionLineageLabel",
	"WorkshopScroll/WorkshopLayout/PrecisionMethodLabel",
	"WorkshopScroll/WorkshopLayout/PrecisionTagEntriesLabel",
	"WorkshopScroll/WorkshopLayout/PrecisionPreviewLabel",
	"WorkshopScroll/WorkshopLayout/EnhancementMessageLabel",
	"WorkshopScroll/WorkshopLayout/RepairMessageLabel",
]
const MOBILE_ACTION_CONTROL_PATHS := [
	"WorkshopScroll/WorkshopLayout/RepairButton",
	"WorkshopScroll/WorkshopLayout/PrecisionActionAddButton",
	"WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton",
	"WorkshopScroll/WorkshopLayout/PrecisionTagOption",
	"WorkshopScroll/WorkshopLayout/PrecisionLineageOption",
	"WorkshopScroll/WorkshopLayout/PrecisionMethodOption",
	"WorkshopScroll/WorkshopLayout/PrecisionBackfillButton",
	"WorkshopScroll/WorkshopLayout/HandoffButton",
	"WorkshopScroll/WorkshopLayout/ChronicleButton",
]
const MOBILE_PRIMARY_ACTION_CONTROL_PATHS := [
	"WorkshopScroll/WorkshopLayout/EnhancementButton",
]

signal enhancement_saved(envelope, result: Dictionary)
signal handoff_requested
signal chronicle_requested

var _item = null
var _resources = null
var _maintenance_service = null
var _enhancement_action_service = null
var _save_service = null
var _campaign_envelope = null
var _precision_action := ""
var _precision_selection_data: Dictionary = {}


func _ready() -> void:
	_ensure_scrollable_layout()
	_ensure_illustrated_background()
	_ensure_workpiece_durability_hero()
	_ensure_equipment_identity_hero()
	_ensure_enhancement_controls()
	_ensure_wireframe_cards()
	_apply_mobile_readability_tokens()
	var repair_button := get_node_or_null("WorkshopScroll/WorkshopLayout/RepairButton") as Button
	if repair_button != null and not repair_button.pressed.is_connected(_on_repair_pressed):
		repair_button.pressed.connect(_on_repair_pressed)
	var enhancement_button := get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementButton") as Button
	if enhancement_button != null and not enhancement_button.pressed.is_connected(_on_enhancement_pressed):
		enhancement_button.pressed.connect(_on_enhancement_pressed)
	_connect_handoff_control()
	_connect_chronicle_control()
	var catalyst_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	if catalyst_option != null and not catalyst_option.item_selected.is_connected(_on_precision_catalyst_selected):
		catalyst_option.item_selected.connect(_on_precision_catalyst_selected)
	var method_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	if method_option != null and not method_option.item_selected.is_connected(_on_precision_method_selected):
		method_option.item_selected.connect(_on_precision_method_selected)
	var backfill_button := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionBackfillButton") as Button
	if backfill_button != null and not backfill_button.pressed.is_connected(_on_precision_backfill_pressed):
		backfill_button.pressed.connect(_on_precision_backfill_pressed)
	_connect_precision_controls()
	_refresh_controls()


func _ensure_scrollable_layout() -> void:
	var layout := get_node_or_null("WorkshopLayout") as VBoxContainer
	if layout == null:
		return
	var scroll := get_node_or_null("WorkshopScroll") as ScrollContainer
	if scroll == null:
		scroll = ScrollContainer.new()
		scroll.name = "WorkshopScroll"
		scroll.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		scroll.offset_left = 32.0
		scroll.offset_top = 24.0
		scroll.offset_right = -32.0
		scroll.offset_bottom = -24.0
		scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
		scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
		scroll.follow_focus = true
		scroll.scroll_deadzone = 12
		scroll.scroll_vertical_custom_step = 64.0
		scroll.scroll_hint_mode = ScrollContainer.SCROLL_HINT_MODE_ALL
		add_child(scroll)
		move_child(scroll, layout.get_index())
	if layout.get_parent() != scroll:
		layout.reparent(scroll)
		layout.set_anchors_preset(Control.PRESET_TOP_WIDE)
		layout.offset_left = 32.0
		layout.offset_top = 48.0
		layout.offset_right = -32.0
		layout.offset_bottom = 0.0
		layout.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		layout.size_flags_vertical = Control.SIZE_SHRINK_BEGIN
	_ensure_scroll_bottom_padding(layout)


func _ensure_scroll_bottom_padding(layout: VBoxContainer) -> void:
	if layout.has_node("ScrollBottomPadding"):
		return
	var padding := Control.new()
	padding.name = "ScrollBottomPadding"
	padding.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	padding.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layout.add_child(padding)


func _apply_mobile_readability_tokens() -> void:
	_apply_font_size_to_controls(MOBILE_TITLE_CONTROL_PATHS, MOBILE_TITLE_FONT_SIZE)
	_apply_font_size_to_controls(MOBILE_SECTION_CONTROL_PATHS, MOBILE_SECTION_FONT_SIZE)
	_apply_font_size_to_controls(MOBILE_BODY_CONTROL_PATHS, MOBILE_BODY_FONT_SIZE)
	_apply_font_size_to_controls(MOBILE_ACTION_CONTROL_PATHS, MOBILE_BODY_FONT_SIZE)
	_apply_font_size_to_controls(MOBILE_PRIMARY_ACTION_CONTROL_PATHS, MOBILE_SECTION_FONT_SIZE)
	_apply_minimum_height_to_controls(MOBILE_ACTION_CONTROL_PATHS, MOBILE_TOUCH_TARGET_HEIGHT)
	_apply_minimum_height_to_controls(MOBILE_PRIMARY_ACTION_CONTROL_PATHS, MOBILE_PRIMARY_TOUCH_TARGET_HEIGHT)
	_apply_portrait_text_wrapping()


func _apply_portrait_text_wrapping() -> void:
	var layout := get_node_or_null("WorkshopScroll/WorkshopLayout") as VBoxContainer
	if layout == null:
		return
	for child in layout.get_children():
		var label := child as Label
		if label == null:
			continue
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		label.size_flags_horizontal = Control.SIZE_EXPAND_FILL


func _apply_font_size_to_controls(paths: Array, font_size: int) -> void:
	for path in paths:
		var control := get_node_or_null(path) as Control
		if control != null:
			control.add_theme_font_size_override("font_size", font_size)


func _apply_minimum_height_to_controls(paths: Array, minimum_height: float) -> void:
	for path in paths:
		var control := get_node_or_null(path) as Control
		if control != null:
			control.custom_minimum_size = Vector2(0, minimum_height)


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
			"precision_target": "",
			"precision_mode": "",
			"precision_tag_entries": [],
			"precision_action": "",
			"precision_candidates": [],
			"precision_preview_summary": "",
			"enhancement_allowed": false,
			"handoff_allowed": false,
			"handoff_reason": "MISSING_ITEM",
			"chronicle_allowed": false,
			"workpiece_summary": "작품 선택 필요",
			"decision_summary": "강화할 작품을 선택하세요",
			"precision_summary": "",
			"destination_summary": "작품을 선택하면 수리·인계·연대기를 확인할 수 있습니다",
		}
	var quote: Dictionary = RepairResolverScript.new().quote(_item)
	var precision_mode := _precision_mode()
	var precision_target := _precision_target_level()
	var enhancement: Dictionary = EnhancementResolverScript.new().preview(
		_item,
		int(_item.enhancement_level) + 1,
		_precision_selection_data
	)
	var precision_catalyst_reason := _precision_catalyst_resource_reason(enhancement)
	var enhancement_allowed := bool(enhancement.get("allowed", false)) and precision_catalyst_reason.is_empty() and _has_enhancement_context()
	var enhancement_reason := precision_catalyst_reason if not precision_catalyst_reason.is_empty() else str(enhancement.get("reason", ""))
	var precision_preview := _precision_preview(precision_mode)
	if precision_mode == "BACKFILL":
		enhancement["allowed"] = false
		enhancement["reason"] = "PRECISION_PLACEHOLDER_REQUIRES_BACKFILL"
		enhancement_allowed = false
		enhancement_reason = "PRECISION_PLACEHOLDER_REQUIRES_BACKFILL"
	var recovery: Dictionary = quote.get("quality_recovery_percent", {})
	var repair_allowed := bool(quote.get("allowed", false))
	var candidates := _precision_candidates_for_action(_precision_action, precision_mode)
	var add_available := not _precision_candidates_for_action("ADD_TAG", precision_mode).is_empty()
	var upgrade_available := precision_mode == "ATTEMPT" and precision_target > 10 and not _precision_candidates_for_action("UPGRADE_TAG", precision_mode).is_empty()
	var handoff_allowed := _phase1_handoff_allowed()
	var state := {
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
		"enhancement_allowed": enhancement_allowed,
		"enhancement_reason": enhancement_reason,
		"enhancement_target_level": int(enhancement.get("target_level", int(_item.enhancement_level) + 1)),
		"enhancement_cost_summary": "비용: %d Gold · 보강재 %d개" % [int(enhancement.get("gold_cost", 0)), int(enhancement.get("reinforcement_units", 0))],
		"enhancement_outcomes_summary": _enhancement_outcomes_summary(enhancement),
		"precision_visible": not precision_mode.is_empty(),
		"precision_target": _precision_target_text(precision_target),
		"precision_mode": precision_mode,
		"precision_tag_entries": _player_facing_precision_tag_entries(precision_target, precision_mode),
		"precision_action": _precision_action,
		"precision_candidates": _player_facing_precision_candidates(candidates, precision_mode),
		"precision_add_available": add_available,
		"precision_upgrade_available": upgrade_available,
		"precision_tag_id": str(precision_preview.get("tag_id", "")),
		"precision_preview_summary": _precision_preview_summary(precision_preview, precision_mode),
		"precision_catalyst_stock_summary": _precision_catalyst_stock_summary(),
		"precision_backfill_allowed": precision_mode == "BACKFILL" and bool(precision_preview.get("allowed", false)) and _has_enhancement_context(),
		"handoff_allowed": handoff_allowed,
		"handoff_reason": _phase1_handoff_reason(),
		"chronicle_allowed": _item != null and _campaign_envelope != null,
	}
	var equipment: Dictionary = EquipmentCatalogScript.by_item(_item)
	state["workpiece_summary"] = _workpiece_summary(equipment, state)
	state["decision_summary"] = _decision_summary(state)
	state["precision_summary"] = _precision_summary(state)
	state["destination_summary"] = _destination_summary(state)
	return state


func _workpiece_summary(equipment: Dictionary, state: Dictionary) -> String:
	var equipment_name := str(equipment.get("display_name_ko", "미확인 작품"))
	var uid := str(_item.uid) if _item != null else ""
	var tag_summary := _precision_tag_entries_summary(state.get("precision_tag_entries", []))
	return "%s · UID %s\n강화 +%d\n%s\n상태: %s" % [
		equipment_name,
		uid,
		int(_item.enhancement_level) if _item != null else 0,
		tag_summary,
		_player_facing_durability_state(str(state.get("durability_state", "UNAVAILABLE"))),
	]


func _decision_summary(state: Dictionary) -> String:
	var target_level := int(state.get("enhancement_target_level", 0))
	var decision_lines: PackedStringArray = [
		"다음 판단: +%d" % target_level,
		str(state.get("enhancement_cost_summary", "")),
		str(state.get("enhancement_outcomes_summary", "")),
	]
	if not bool(state.get("enhancement_allowed", false)):
		decision_lines.append("막힌 이유: %s" % _player_facing_enhancement_reason(str(state.get("enhancement_reason", ""))))
	return "\n".join(decision_lines)


func _precision_summary(state: Dictionary) -> String:
	if not bool(state.get("precision_visible", false)):
		return ""
	var target_text := str(state.get("precision_target", ""))
	var target_parts := target_text.split("→")
	var target_label := str(target_parts[target_parts.size() - 1]).strip_edges() if not target_parts.is_empty() else target_text
	var action := str(state.get("precision_action", ""))
	var action_text := "태그 행동을 고르세요" if action.is_empty() else "선택한 행동: %s" % ("태그 추가" if action == "ADD_TAG" else "태그 강화")
	return "정밀강화 %s\n%s\n촉매 보유: %s\n%s" % [
		target_label,
		action_text,
		str(state.get("precision_catalyst_stock_summary", "확인 필요")),
		str(state.get("precision_preview_summary", "")),
	]


func _destination_summary(state: Dictionary) -> String:
	var repair_text := "수리 가능" if bool(state.get("repair_allowed", false)) else "수리: %s" % _player_facing_repair_reason(str(state.get("repair_reason", "")))
	var handoff_text := "인계 가능" if bool(state.get("handoff_allowed", false)) else "인계: %s" % _phase1_handoff_reason()
	var chronicle_text := "연대기 보기 가능" if bool(state.get("chronicle_allowed", false)) else "연대기: 캠페인 정보 필요"
	return "%s\n%s\n%s" % [repair_text, handoff_text, chronicle_text]


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
		_precision_selection_data
	)
	if str(result.get("outcome", "")) != "BLOCKED":
		_campaign_envelope = result.get("envelope", null)
		_item = _campaign_envelope.get_item(item_uid) if _campaign_envelope != null else null
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
		_precision_selection_data,
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


func set_precision_selection(selection: Dictionary) -> void:
	_precision_selection_data = selection
	_precision_action = str(selection.get("action", ""))
	_select_precision_option("WorkshopScroll/WorkshopLayout/PrecisionLineageOption", str(selection.get("catalyst_id", "")))
	_select_precision_option("WorkshopScroll/WorkshopLayout/PrecisionMethodOption", str(selection.get("method_id", "")))
	_select_precision_option("WorkshopScroll/WorkshopLayout/PrecisionTagOption", str(selection.get("tag_id", "")))
	_refresh_controls()


func _on_repair_pressed() -> void:
	var result := request_repair()
	var message := get_node_or_null("WorkshopScroll/WorkshopLayout/RepairMessageLabel") as Label
	if message != null:
		message.text = "수리 완료" if str(result.get("status", "")) == "APPLIED" else "수리 불가: %s" % str(result.get("reason", "UNKNOWN"))


func _on_enhancement_pressed() -> void:
	var result := request_enhancement()
	var message := get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementMessageLabel") as Label
	if message != null:
		message.text = "강화 결과: %s" % str(result.get("outcome", "BLOCKED"))


func _on_precision_catalyst_selected(_index: int) -> void:
	if _precision_action == "ADD_TAG":
		_precision_selection_data = {
			"action": "ADD_TAG",
			"catalyst_id": _selected_precision_option("WorkshopScroll/WorkshopLayout/PrecisionLineageOption"),
			"method_id": str(_precision_selection_data.get("method_id", "")),
		}
	_refresh_controls()


func _on_precision_method_selected(_index: int) -> void:
	if _precision_action == "ADD_TAG":
		_precision_selection_data = {
			"action": "ADD_TAG",
			"catalyst_id": str(_precision_selection_data.get("catalyst_id", "")),
			"method_id": _selected_precision_option("WorkshopScroll/WorkshopLayout/PrecisionMethodOption"),
		}
	_refresh_controls()


func _on_precision_tag_selected(_index: int) -> void:
	if _precision_action == "UPGRADE_TAG":
		_precision_selection_data = {
			"action": "UPGRADE_TAG",
			"tag_id": _selected_precision_option("WorkshopScroll/WorkshopLayout/PrecisionTagOption"),
		}
	_refresh_controls()


func _on_precision_add_pressed() -> void:
	_precision_action = "ADD_TAG"
	_precision_selection_data = {"action": "ADD_TAG"}
	_refresh_controls()


func _on_precision_upgrade_pressed() -> void:
	_precision_action = "UPGRADE_TAG"
	_precision_selection_data = {"action": "UPGRADE_TAG"}
	_refresh_controls()


func _on_precision_backfill_pressed() -> void:
	var result := request_precision_backfill()
	var message := get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementMessageLabel") as Label
	if message != null:
		message.text = "정밀 태그 정정 완료" if str(result.get("outcome", "")) == "APPLIED" else "정밀 태그 정정 불가"


func _refresh_controls() -> void:
	_ensure_workpiece_durability_hero()
	_ensure_equipment_identity_hero()
	_ensure_enhancement_controls()
	_ensure_wireframe_cards()
	_connect_precision_controls()
	_connect_handoff_control()
	_connect_chronicle_control()
	var state := view_state()
	var title := get_node_or_null("WorkshopScroll/WorkshopLayout/WorkshopTitle") as Label
	if title != null and _item != null:
		var equipment: Dictionary = EquipmentCatalogScript.by_item(_item)
		title.text = "첫 작품 · %s" % str(equipment.get("display_name_ko", "미확인 작품"))
	var durability := get_node_or_null("WorkshopScroll/WorkshopLayout/DurabilityValueLabel") as Label
	var condition := get_node_or_null("WorkshopScroll/WorkshopLayout/DurabilityStateLabel") as Label
	var quote := get_node_or_null("WorkshopScroll/WorkshopLayout/RepairQuoteLabel") as Label
	var quality := get_node_or_null("WorkshopScroll/WorkshopLayout/RepairQualityLabel") as Label
	var scar := get_node_or_null("WorkshopScroll/WorkshopLayout/RepairScarLabel") as Label
	var job := get_node_or_null("WorkshopScroll/WorkshopLayout/RepairJobLabel") as Label
	var repair_button := get_node_or_null("WorkshopScroll/WorkshopLayout/RepairButton") as Button
	var enhancement_quote := get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementQuoteLabel") as Label
	var enhancement_outcomes := get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementOutcomesLabel") as Label
	var enhancement_button := get_node_or_null("WorkshopScroll/WorkshopLayout/EnhancementButton") as Button
	var handoff_button := get_node_or_null("WorkshopScroll/WorkshopLayout/HandoffButton") as Button
	var chronicle_button := get_node_or_null("WorkshopScroll/WorkshopLayout/ChronicleButton") as Button
	var precision_title := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTitleLabel") as Label
	var precision_actions_label := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionLabel") as Label
	var precision_add_button := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button
	var precision_upgrade_button := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button
	var precision_tag_label := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTagLabel") as Label
	var precision_tag_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTagOption") as OptionButton
	var precision_lineage_label := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageLabel") as Label
	var precision_lineage_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	var precision_method_label := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodLabel") as Label
	var precision_method_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	var precision_tag_entries := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTagEntriesLabel") as Label
	var precision_preview := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionPreviewLabel") as Label
	var precision_backfill_button := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionBackfillButton") as Button
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
	if handoff_button != null:
		handoff_button.visible = bool(state.get("handoff_allowed", false))
		handoff_button.disabled = not bool(state.get("handoff_allowed", false))
	if chronicle_button != null:
		chronicle_button.visible = bool(state.get("chronicle_allowed", false))
		chronicle_button.disabled = not bool(state.get("chronicle_allowed", false))
	var precision_visible := bool(state.get("precision_visible", false))
	var action := str(state.get("precision_action", ""))
	var add_selected := action == "ADD_TAG"
	var upgrade_selected := action == "UPGRADE_TAG"
	for control in [precision_title, precision_actions_label, precision_add_button, precision_upgrade_button, precision_tag_entries, precision_preview]:
		if control != null:
			control.visible = precision_visible
	for control in [precision_lineage_label, precision_lineage_option, precision_method_label, precision_method_option]:
		if control != null:
			control.visible = precision_visible and add_selected
	for control in [precision_tag_label, precision_tag_option]:
		if control != null:
			control.visible = precision_visible and upgrade_selected
	var precision_mode := str(state.get("precision_mode", ""))
	if precision_title != null:
		if precision_mode == "ATTEMPT":
			precision_title.text = "정밀 강화 · %s" % str(state.get("precision_target", ""))
		elif precision_mode == "BACKFILL":
			precision_title.text = "정밀 태그 정정 · %s" % str(state.get("precision_target", ""))
		else:
			precision_title.text = "정밀 강화 · %s" % str(state.get("precision_target", ""))
	if precision_actions_label != null:
		if precision_mode == "WEAPON_ONLY":
			precision_actions_label.text = "정밀 태그는 검·방패·활에만 적용됩니다"
		else:
			var action_summary := "행동을 먼저 고르세요" if action.is_empty() else "선택한 행동: %s" % ("태그 추가" if add_selected else "태그 강화")
			precision_actions_label.text = "%s · 촉매 보유: %s" % [action_summary, str(state.get("precision_catalyst_stock_summary", "확인 필요"))]
	if precision_add_button != null:
		precision_add_button.visible = precision_visible and bool(state.get("precision_add_available", false))
		precision_add_button.disabled = not bool(state.get("precision_add_available", false))
	if precision_upgrade_button != null:
		precision_upgrade_button.visible = precision_visible and bool(state.get("precision_upgrade_available", false))
		precision_upgrade_button.disabled = not bool(state.get("precision_upgrade_available", false))
	if precision_tag_entries != null:
		precision_tag_entries.text = _precision_tag_entries_summary(state.get("precision_tag_entries", []))
	if precision_preview != null:
		precision_preview.text = str(state.get("precision_preview_summary", ""))
	if precision_lineage_option != null:
		precision_lineage_option.disabled = not precision_visible or not add_selected
	if precision_method_option != null:
		precision_method_option.disabled = not precision_visible or not add_selected
	if precision_tag_option != null:
		precision_tag_option.disabled = not precision_visible or not upgrade_selected
	if precision_backfill_button != null:
		precision_backfill_button.visible = str(state.get("precision_mode", "")) == "BACKFILL"
		precision_backfill_button.disabled = not bool(state.get("precision_backfill_allowed", false))
	_refresh_wireframe_cards(state)


func _has_enhancement_context() -> bool:
	return _item != null and _resources != null and _campaign_envelope != null and _save_service != null and _enhancement_action_service != null


func _phase1_handoff_allowed() -> bool:
	return _phase1_handoff_reason().is_empty()


func _phase1_handoff_reason() -> String:
	if _item == null:
		return "MISSING_ITEM"
	if int(_item.enhancement_level) < 10:
		return "HANDOFF_REQUIRES_LEVEL_10"
	if int(_item.current_durability) <= 0 or str(_item.physical_state) == "DESTROYED":
		return "ITEM_DESTROYED"
	if _campaign_envelope == null or not _campaign_envelope.active_run is Dictionary:
		return "MISSING_CAMPAIGN_CONTEXT"
	var item_uid := str(_item.uid)
	if item_uid.is_empty() or str(_campaign_envelope.active_run.get("selected_item_uid", "")) != item_uid:
		return "ITEM_NOT_ACTIVE"
	var resolved_events: Variant = _campaign_envelope.active_run.get("resolved_events", {})
	if resolved_events is Dictionary and resolved_events.has("phase1-nadia-actual-use-%s" % item_uid):
		return "EVENT_ALREADY_RESOLVED"
	return ""


func _precision_mode() -> String:
	if _item == null:
		return ""
	if _item.has_initial_tag_backfill_pending():
		return "BACKFILL" if EquipmentCatalogScript.is_precision_tag_eligible(_item) else "WEAPON_ONLY"
	if PrecisionResolverScript.PRECISION_TARGETS.has(int(_item.enhancement_level) + 1):
		return "ATTEMPT" if EquipmentCatalogScript.is_precision_tag_eligible(_item) else "WEAPON_ONLY"
	return ""


func _precision_target_level() -> int:
	if _item == null:
		return 0
	if _item.has_initial_tag_backfill_pending():
		return 10
	var target_level := int(_item.enhancement_level) + 1
	return target_level if PrecisionResolverScript.PRECISION_TARGETS.has(target_level) else 0


func _precision_target_text(target_level: int) -> String:
	if target_level <= 0:
		return ""
	return "+%d → +%d" % [target_level - 1, target_level]


func _precision_preview(precision_mode: String) -> Dictionary:
	if precision_mode == "WEAPON_ONLY":
		return {"allowed": false, "reason": "PRECISION_TAG_WEAPON_ONLY"}
	if precision_mode.is_empty() or _precision_action.is_empty():
		return {"allowed": false, "reason": "PRECISION_ACTION_REQUIRED"}
	if precision_mode == "BACKFILL":
		if _item == null or not _item.has_method("to_dict"):
			return {"allowed": false, "reason": "MISSING_ITEM"}
		var staged_item = ItemScript.from_dict(_item.to_dict())
		if staged_item == null or not staged_item.validation_errors.is_empty():
			return {"allowed": false, "reason": "INVALID_ITEM_STATE"}
		var backfill: Dictionary = PrecisionResolverScript.new().backfill_initial_tag(staged_item, _precision_selection_data)
		if not bool(backfill.get("applied", false)):
			return {"allowed": false, "reason": str(backfill.get("reason", "INVALID_PRECISION_BACKFILL"))}
		backfill["allowed"] = true
		return backfill
	return PrecisionResolverScript.new().selection_preview(_item, _precision_target_level(), _precision_selection_data)


func _precision_candidates_for_action(action: String, precision_mode: String) -> Array:
	var candidates: Array = []
	if _item == null or precision_mode.is_empty():
		return candidates
	var catalog: Dictionary = PrecisionResolverScript.new().catalog()
	if action == "ADD_TAG":
		for catalyst in catalog.get("catalysts", []):
			if not catalyst is Dictionary:
				continue
			for method in catalog.get("methods", []):
				if not method is Dictionary:
					continue
				var selection := {
					"action": "ADD_TAG",
					"catalyst_id": str(catalyst.get("id", "")),
					"method_id": str(method.get("id", "")),
				}
				var preview := _precision_preview_for_selection(precision_mode, selection)
				if bool(preview.get("allowed", false)):
					preview["selection"] = selection
					candidates.append(preview)
	elif action == "UPGRADE_TAG" and precision_mode == "ATTEMPT" and _precision_target_level() > 10:
		for entry in _item.catalyst_tag_entries():
			var selection := {"action": "UPGRADE_TAG", "tag_id": str(entry.get("tag_id", ""))}
			var preview := _precision_preview_for_selection(precision_mode, selection)
			if bool(preview.get("allowed", false)):
				preview["selection"] = selection
				candidates.append(preview)
	return candidates


func _precision_preview_for_selection(precision_mode: String, selection: Dictionary) -> Dictionary:
	var saved_selection := _precision_selection_data
	var saved_action := _precision_action
	_precision_selection_data = selection
	_precision_action = str(selection.get("action", ""))
	var preview := _precision_preview(precision_mode)
	_precision_selection_data = saved_selection
	_precision_action = saved_action
	return preview


func _player_facing_precision_candidates(candidates: Array, precision_mode: String) -> Array:
	var player_facing: Array = []
	for candidate in candidates:
		if not candidate is Dictionary:
			continue
		player_facing.append({
			"tag_display_name_ko": str(candidate.get("tag_display_name_ko", "")),
			"precision_catalyst_display_name_ko": str(candidate.get("precision_catalyst_display_name_ko", "")),
			"method_display_name_ko": str(candidate.get("method_display_name_ko", "")),
			"stage_before_roman": _stage_roman(int(candidate.get("stage_before", 0))),
			"stage_after_roman": _stage_roman(int(candidate.get("stage_after", 0))),
			"preview_summary": _precision_preview_summary(candidate, precision_mode),
		})
	return player_facing


func _player_facing_precision_tag_entries(target_level: int, precision_mode: String) -> Array:
	var player_facing: Array = []
	if _item == null:
		return player_facing
	var catalog: Dictionary = PrecisionResolverScript.new().catalog()
	for entry in _item.catalyst_tag_entries():
		var tag_id := str(entry.get("tag_id", ""))
		var tag: Dictionary = _catalog_entry_by_id(catalog.get("tags", []), tag_id)
		if tag.is_empty():
			continue
		var catalyst: Dictionary = _catalog_entry_by_id(catalog.get("catalysts", []), str(tag.get("catalyst_id", "")))
		var next_preview: Dictionary = {}
		if precision_mode == "ATTEMPT" and target_level > 10:
			next_preview = _precision_preview_for_selection(precision_mode, {"action": "UPGRADE_TAG", "tag_id": tag_id})
		player_facing.append({
			"tag_display_name_ko": str(tag.get("display_name_ko", "")),
			"precision_catalyst_display_name_ko": str(catalyst.get("display_name_ko", "")),
			"stage_roman": _stage_roman(int(entry.get("stage", 0))),
			"next_effect_preview": _precision_preview_summary(next_preview, precision_mode) if bool(next_preview.get("allowed", false)) else "다음 단계 강화 불가",
		})
	return player_facing


func _catalog_entry_by_id(entries: Array, entry_id: String) -> Dictionary:
	for entry in entries:
		if entry is Dictionary and str(entry.get("id", "")) == entry_id:
			return entry
	return {}


func _stage_roman(stage: int) -> String:
	var numerals := ["", "I", "II", "III", "IV"]
	return str(numerals[stage]) if stage > 0 and stage < numerals.size() else ""


func _clear_precision_selection() -> void:
	_precision_action = ""
	_precision_selection_data = {}
	var tag_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTagOption") as OptionButton
	var lineage_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	if tag_option != null:
		tag_option.select(0)
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


func _selected_precision_option(path: NodePath) -> String:
	var option := get_node_or_null(path) as OptionButton
	if option == null or option.get_selected() < 0:
		return ""
	return str(option.get_item_metadata(option.get_selected()))


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
	return "촉매: %s\n결과 태그: %s · 단계 %s → %s · %s %d → %d · 내구도 변화 없음" % [
		_precision_catalyst_consumption_summary(preview),
		str(preview.get("tag_display_name_ko", "")),
		_stage_roman(int(preview.get("stage_before", 0))),
		_stage_roman(int(preview.get("stage_after", 0))),
		axis_label,
		int(preview.get("before_value", 0)),
		int(preview.get("after_value", 0)),
	]


func _precision_catalyst_consumption_summary(preview: Dictionary) -> String:
	var display_name := str(preview.get("precision_catalyst_display_name_ko", ""))
	var stock_key := str(preview.get("precision_catalyst_stock_key", ""))
	var units := int(preview.get("precision_catalyst_units", 0))
	if display_name.is_empty() or stock_key.is_empty() or units <= 0:
		return "정보 확인 필요"
	var owned := _precision_catalyst_owned_units(stock_key)
	return "%s %d개 소모 · 보유 %d개" % [display_name, units, owned]


func _precision_catalyst_stock_summary() -> String:
	var catalog: Dictionary = PrecisionResolverScript.new().catalog()
	var labels: PackedStringArray = []
	for catalyst in catalog.get("catalysts", []):
		if not catalyst is Dictionary:
			continue
		var display_name := str(catalyst.get("display_name_ko", ""))
		var stock_key := str(catalyst.get("material_stock_key", ""))
		if display_name.is_empty() or stock_key.is_empty():
			continue
		labels.append("%s %d개" % [display_name, _precision_catalyst_owned_units(stock_key)])
	return " · ".join(labels) if not labels.is_empty() else "확인 필요"


func _precision_catalyst_owned_units(stock_key: String) -> int:
	if _resources == null or not _resources.has_method("get_material_count"):
		return 0
	return int(_resources.get_material_count(stock_key))


func _precision_catalyst_resource_reason(enhancement: Dictionary) -> String:
	var catalyst_id := str(enhancement.get("precision_catalyst_id", ""))
	if catalyst_id.is_empty():
		return ""
	var stock_key := str(enhancement.get("precision_catalyst_stock_key", ""))
	var units := int(enhancement.get("precision_catalyst_units", 0))
	if stock_key.is_empty() or units != 1:
		return "INVALID_PRECISION_CATALYST_COST"
	if _resources == null or not _resources.has_method("get_material_count"):
		return "MISSING_PRECISION_CATALYST_RESOURCE_CONTEXT"
	if _precision_catalyst_owned_units(stock_key) < units:
		return "INSUFFICIENT_PRECISION_CATALYST"
	return ""


func _precision_tag_entries_summary(entries: Array) -> String:
	if entries.is_empty():
		return "활성 태그 없음"
	var lines: PackedStringArray = []
	for entry in entries:
		if entry is Dictionary:
			lines.append("%s · %s · %s · %s" % [
				str(entry.get("tag_display_name_ko", "")),
				str(entry.get("precision_catalyst_display_name_ko", "")),
				str(entry.get("stage_roman", "")),
				str(entry.get("next_effect_preview", "")),
			])
	return "\n".join(lines)


func _player_facing_enhancement_reason(reason: String) -> String:
	match reason:
		"PRECISION_ACTION_REQUIRED", "INVALID_PRECISION_ACTION":
			return "태그 행동을 먼저 고르세요"
		"MISSING_PRECISION_CATALYST":
			return "정밀 촉매를 고르세요"
		"INSUFFICIENT_PRECISION_CATALYST":
			return "필요한 정밀 촉매가 부족합니다"
		"INVALID_PRECISION_CATALYST_COST", "MISSING_PRECISION_CATALYST_RESOURCE_CONTEXT":
			return "정밀 촉매 정보를 확인할 수 없습니다"
		"MISSING_PRECISION_METHOD":
			return "정밀 강화 방식을 고르세요"
		"MISSING_PRECISION_TAG":
			return "강화할 태그를 고르세요"
		"INVALID_PRECISION_TAG_COMBINATION":
			return "선택한 정밀 조합을 확인하세요"
		"PRECISION_EFFECT_UNAVAILABLE":
			return "현재 작품에는 이 효과를 적용할 수 없습니다"
		"PRECISION_TAG_WEAPON_ONLY":
			return "정밀 태그는 검·방패·활에만 적용됩니다"
		"PRECISION_TAG_CAP_REACHED":
			return "활성 태그는 세 개까지입니다"
		"PRECISION_TAG_MASTERED":
			return "이 태그는 이미 IV 단계입니다"
		"DUPLICATE_PRECISION_TAG":
			return "이미 선택된 정밀 태그입니다"
		"INCOMPATIBLE_PRECISION_TAG":
			return "함께 적용할 수 없는 정밀 태그입니다"
		"INACTIVE_PRECISION_TAG":
			return "현재 작품에 없는 정밀 태그입니다"
		"INVALID_CATALYST_TAG_STATE", "INVALID_PRECISION_MILESTONE_STATE", "INVALID_ITEM_STATE":
			return "정밀 태그 상태를 확인할 수 없습니다"
		"PRECISION_PLACEHOLDER_REQUIRES_BACKFILL":
			return "정밀 태그 정정을 먼저 완료하세요"
		"CATALYST_AFFIX_ALREADY_RESOLVED":
			return "이미 정밀 태그가 적용된 작품입니다"
		"CATALYST_AFFIX_UNKNOWN_FAIL_CLOSED":
			return "정밀 태그 상태를 확인할 수 없습니다"
		_:
			return "강화 조건을 확인하세요"


func _connect_precision_controls() -> void:
	var add_button := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionAddButton") as Button
	if add_button != null and not add_button.pressed.is_connected(_on_precision_add_pressed):
		add_button.pressed.connect(_on_precision_add_pressed)
	var upgrade_button := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionActionUpgradeButton") as Button
	if upgrade_button != null and not upgrade_button.pressed.is_connected(_on_precision_upgrade_pressed):
		upgrade_button.pressed.connect(_on_precision_upgrade_pressed)
	var tag_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTagOption") as OptionButton
	if tag_option != null and not tag_option.item_selected.is_connected(_on_precision_tag_selected):
		tag_option.item_selected.connect(_on_precision_tag_selected)
	var lineage_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	if lineage_option != null and not lineage_option.item_selected.is_connected(_on_precision_catalyst_selected):
		lineage_option.item_selected.connect(_on_precision_catalyst_selected)
	var method_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	if method_option != null and not method_option.item_selected.is_connected(_on_precision_method_selected):
		method_option.item_selected.connect(_on_precision_method_selected)


func _connect_handoff_control() -> void:
	var handoff_button := get_node_or_null("WorkshopScroll/WorkshopLayout/HandoffButton") as Button
	if handoff_button != null and not handoff_button.pressed.is_connected(_on_handoff_pressed):
		handoff_button.pressed.connect(_on_handoff_pressed)


func _connect_chronicle_control() -> void:
	var chronicle_button := get_node_or_null("WorkshopScroll/WorkshopLayout/ChronicleButton") as Button
	if chronicle_button != null and not chronicle_button.pressed.is_connected(_on_chronicle_pressed):
		chronicle_button.pressed.connect(_on_chronicle_pressed)


func _on_handoff_pressed() -> void:
	if _phase1_handoff_allowed():
		handoff_requested.emit()


func _on_chronicle_pressed() -> void:
	if _item != null and _campaign_envelope != null:
		chronicle_requested.emit()


func _ensure_enhancement_controls() -> void:
	var layout := get_node_or_null("WorkshopScroll/WorkshopLayout") as VBoxContainer
	if layout == null:
		return
	if layout.has_node("EnhancementButton"):
		_ensure_handoff_button(layout)
		_ensure_chronicle_button(layout)
		_populate_precision_options()
		return
	var nodes: Array[Control] = []
	var title := Label.new()
	title.name = "EnhancementTitleLabel"
	title.text = "다음 강화"
	title.add_theme_font_size_override("font_size", MOBILE_SECTION_FONT_SIZE)
	nodes.append(title)
	var quote := Label.new()
	quote.name = "EnhancementQuoteLabel"
	quote.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(quote)
	var outcomes := Label.new()
	outcomes.name = "EnhancementOutcomesLabel"
	outcomes.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	outcomes.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(outcomes)
	var precision_title := Label.new()
	precision_title.name = "PrecisionTitleLabel"
	precision_title.text = "정밀 강화"
	precision_title.add_theme_font_size_override("font_size", MOBILE_SECTION_FONT_SIZE)
	nodes.append(precision_title)
	var precision_actions_label := Label.new()
	precision_actions_label.name = "PrecisionActionLabel"
	precision_actions_label.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_actions_label)
	var precision_add_button := Button.new()
	precision_add_button.name = "PrecisionActionAddButton"
	precision_add_button.text = "태그 추가"
	precision_add_button.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	precision_add_button.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_add_button)
	var precision_upgrade_button := Button.new()
	precision_upgrade_button.name = "PrecisionActionUpgradeButton"
	precision_upgrade_button.text = "태그 강화"
	precision_upgrade_button.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	precision_upgrade_button.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_upgrade_button)
	var precision_tag_label := Label.new()
	precision_tag_label.name = "PrecisionTagLabel"
	precision_tag_label.text = "강화할 태그"
	precision_tag_label.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_tag_label)
	var precision_tag_option := OptionButton.new()
	precision_tag_option.name = "PrecisionTagOption"
	precision_tag_option.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	precision_tag_option.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_tag_option)
	var precision_lineage_label := Label.new()
	precision_lineage_label.name = "PrecisionLineageLabel"
	precision_lineage_label.text = "정밀 촉매"
	precision_lineage_label.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_lineage_label)
	var precision_lineage_option := OptionButton.new()
	precision_lineage_option.name = "PrecisionLineageOption"
	precision_lineage_option.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	precision_lineage_option.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_lineage_option)
	var precision_method_label := Label.new()
	precision_method_label.name = "PrecisionMethodLabel"
	precision_method_label.text = "정밀 강화 방식"
	precision_method_label.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_method_label)
	var precision_method_option := OptionButton.new()
	precision_method_option.name = "PrecisionMethodOption"
	precision_method_option.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	precision_method_option.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_method_option)
	var precision_tag_entries := Label.new()
	precision_tag_entries.name = "PrecisionTagEntriesLabel"
	precision_tag_entries.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	precision_tag_entries.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_tag_entries)
	var precision_preview := Label.new()
	precision_preview.name = "PrecisionPreviewLabel"
	precision_preview.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	precision_preview.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_preview)
	var precision_backfill_button := Button.new()
	precision_backfill_button.name = "PrecisionBackfillButton"
	precision_backfill_button.text = "정밀 태그 정정 적용 · 비용 없음"
	precision_backfill_button.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	precision_backfill_button.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(precision_backfill_button)
	var button := Button.new()
	button.name = "EnhancementButton"
	button.text = "강화 시도"
	button.custom_minimum_size = Vector2(0, MOBILE_PRIMARY_TOUCH_TARGET_HEIGHT)
	button.add_theme_font_size_override("font_size", MOBILE_SECTION_FONT_SIZE)
	nodes.append(button)
	var message := Label.new()
	message.name = "EnhancementMessageLabel"
	message.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	nodes.append(message)
	var repair_index := layout.get_node("RepairButton").get_index()
	for node in nodes:
		layout.add_child(node)
		layout.move_child(node, repair_index)
		repair_index += 1
	_ensure_handoff_button(layout)
	_ensure_chronicle_button(layout)
	_populate_precision_options()


func _ensure_wireframe_cards() -> void:
	var layout := get_node_or_null("WorkshopScroll/WorkshopLayout") as VBoxContainer
	if layout == null:
		return
	_ensure_wireframe_card(layout, "WireframeWorkpieceCard", "현재 작품", "EquipmentIdentityHero", false)
	_ensure_wireframe_card(layout, "WireframeDecisionCard", "지금의 판단", "EnhancementTitleLabel", true)
	_ensure_wireframe_card(layout, "WireframePrecisionCard", "정밀강화", "PrecisionTitleLabel", true)
	_ensure_wireframe_card(layout, "WireframeDestinationCard", "다음 목적지", "HandoffButton", true)


func _ensure_wireframe_card(layout: VBoxContainer, card_name: String, title_text: String, anchor_name: String, insert_before_anchor: bool) -> void:
	if layout.has_node(card_name):
		return
	var card := PanelContainer.new()
	card.name = card_name
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.add_theme_stylebox_override("panel", _wireframe_card_style())
	var content := VBoxContainer.new()
	content.name = "CardContent"
	content.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content.add_theme_constant_override("separation", 8)
	card.add_child(content)
	var title := Label.new()
	title.name = "CardTitle"
	title.text = title_text
	title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	title.add_theme_font_size_override("font_size", WIREFRAME_CARD_TITLE_FONT_SIZE)
	title.add_theme_color_override("font_color", Color("643d24"))
	content.add_child(title)
	var body := Label.new()
	body.name = "CardBody"
	body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	body.add_theme_color_override("font_color", Color("2d211a"))
	content.add_child(body)
	layout.add_child(card)
	var anchor := layout.get_node_or_null(anchor_name) as Control
	if anchor != null:
		var target_index := anchor.get_index() if insert_before_anchor else anchor.get_index() + 1
		layout.move_child(card, target_index)


func _wireframe_card_style() -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color("f4e2bed9")
	style.border_color = Color("704a2f")
	style.set_border_width_all(2)
	style.set_corner_radius_all(16)
	style.set_content_margin_all(18.0)
	return style


func _refresh_wireframe_cards(state: Dictionary) -> void:
	_set_wireframe_card_state("WireframeWorkpieceCard", str(state.get("workpiece_summary", "")), bool(state.get("has_item", false)))
	_set_wireframe_card_state("WireframeDecisionCard", str(state.get("decision_summary", "")), bool(state.get("has_item", false)))
	_set_wireframe_card_state("WireframePrecisionCard", str(state.get("precision_summary", "")), bool(state.get("precision_visible", false)))
	_set_wireframe_card_state("WireframeDestinationCard", str(state.get("destination_summary", "")), bool(state.get("has_item", false)))


func _set_wireframe_card_state(card_name: String, body_text: String, card_visible: bool) -> void:
	var card := get_node_or_null("WorkshopScroll/WorkshopLayout/%s" % card_name) as PanelContainer
	if card == null:
		return
	card.visible = card_visible
	var body := card.get_node_or_null("CardContent/CardBody") as Label
	if body != null:
		body.text = body_text


func _ensure_handoff_button(layout: VBoxContainer) -> void:
	if layout.has_node("HandoffButton"):
		return
	var handoff_button := Button.new()
	handoff_button.name = "HandoffButton"
	handoff_button.text = "나디아에게 인계 · 인계 손상 없음"
	handoff_button.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	handoff_button.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	var repair_button := layout.get_node_or_null("RepairButton") as Control
	layout.add_child(handoff_button)
	if repair_button != null:
		layout.move_child(handoff_button, repair_button.get_index())


func _ensure_chronicle_button(layout: VBoxContainer) -> void:
	if layout.has_node("ChronicleButton"):
		return
	var chronicle_button := Button.new()
	chronicle_button.name = "ChronicleButton"
	chronicle_button.text = "작품 연대 보기"
	chronicle_button.custom_minimum_size = Vector2(0, MOBILE_TOUCH_TARGET_HEIGHT)
	chronicle_button.add_theme_font_size_override("font_size", MOBILE_BODY_FONT_SIZE)
	var repair_button := layout.get_node_or_null("RepairButton") as Control
	layout.add_child(chronicle_button)
	if repair_button != null:
		layout.move_child(chronicle_button, repair_button.get_index())


func _populate_precision_options() -> void:
	var tag_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionTagOption") as OptionButton
	var lineage_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionLineageOption") as OptionButton
	var method_option := get_node_or_null("WorkshopScroll/WorkshopLayout/PrecisionMethodOption") as OptionButton
	if tag_option == null or lineage_option == null or method_option == null:
		return
	tag_option.clear()
	tag_option.add_item("강화할 태그를 고르세요")
	tag_option.set_item_metadata(0, "")
	lineage_option.clear()
	lineage_option.add_item("정밀 촉매를 고르세요")
	lineage_option.set_item_metadata(0, "")
	method_option.clear()
	method_option.add_item("정밀 강화 방식을 고르세요")
	method_option.set_item_metadata(0, "")
	var selected_catalyst := str(_precision_selection_data.get("catalyst_id", ""))
	var selected_method := str(_precision_selection_data.get("method_id", ""))
	var seen_catalysts: Dictionary = {}
	var seen_methods: Dictionary = {}
	for candidate in _precision_candidates_for_action(_precision_action, _precision_mode()):
		if not candidate is Dictionary:
			continue
		var action := str(candidate.get("action", ""))
		if action == "ADD_TAG":
			var catalyst_id := str(candidate.get("precision_catalyst_id", ""))
			var method_id := str(candidate.get("method_id", ""))
			if (selected_method.is_empty() or method_id == selected_method) and not seen_catalysts.has(catalyst_id):
				seen_catalysts[catalyst_id] = true
				var catalyst_name := str(candidate.get("precision_catalyst_display_name_ko", ""))
				var catalyst_stock_key := str(candidate.get("precision_catalyst_stock_key", ""))
				lineage_option.add_item("%s · 보유 %d개" % [catalyst_name, _precision_catalyst_owned_units(catalyst_stock_key)])
				lineage_option.set_item_metadata(lineage_option.item_count - 1, catalyst_id)
			if (selected_catalyst.is_empty() or catalyst_id == selected_catalyst) and not seen_methods.has(method_id):
				seen_methods[method_id] = true
				method_option.add_item(str(candidate.get("method_display_name_ko", "")))
				method_option.set_item_metadata(method_option.item_count - 1, method_id)
		elif action == "UPGRADE_TAG":
			tag_option.add_item(str(candidate.get("tag_display_name_ko", "")))
			tag_option.set_item_metadata(tag_option.item_count - 1, str(candidate.get("tag_id", "")))
	_select_precision_option("WorkshopScroll/WorkshopLayout/PrecisionTagOption", str(_precision_selection_data.get("tag_id", "")))
	_select_precision_option("WorkshopScroll/WorkshopLayout/PrecisionLineageOption", str(_precision_selection_data.get("catalyst_id", "")))
	_select_precision_option("WorkshopScroll/WorkshopLayout/PrecisionMethodOption", str(_precision_selection_data.get("method_id", "")))


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
	var layout := get_node_or_null("WorkshopScroll/WorkshopLayout") as VBoxContainer
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


func _ensure_equipment_identity_hero() -> void:
	var layout := get_node_or_null("WorkshopScroll/WorkshopLayout") as VBoxContainer
	if layout == null:
		return
	var hero := layout.get_node_or_null("EquipmentIdentityHero") as TextureRect
	if hero == null:
		hero = TextureRect.new()
		hero.name = "EquipmentIdentityHero"
		hero.custom_minimum_size = Vector2(0, 156)
		hero.mouse_filter = Control.MOUSE_FILTER_IGNORE
		hero.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		hero.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		layout.add_child(hero)
		layout.move_child(hero, min(1, layout.get_child_count() - 1))
	if _item == null:
		hero.visible = false
		return
	var equipment: Dictionary = EquipmentCatalogScript.by_item(_item)
	var image_path := str(equipment.get("image_path", ""))
	hero.texture = ResourceLoader.load(image_path) as Texture2D if not image_path.is_empty() and ResourceLoader.exists(image_path) else null
	hero.visible = hero.texture != null
	hero.tooltip_text = "현재 작품: %s" % str(equipment.get("display_name_ko", "미확인 작품"))


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
