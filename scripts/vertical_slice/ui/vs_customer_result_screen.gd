# 고객 실제사용 결과의 저장된 내구도 사실과 다음 행동을 읽기 전용으로 표시한다.
class_name VSCustomerResultScreen
extends Control

const CustomerResultIllustrationTexture = preload("res://assets/ui/workshop/customer_result_return_illustration_v1.png")

var _view_state := {
	"event_id": "",
	"item_uid": "",
	"summary_text": "결과를 불러오는 중입니다.",
	"damage_text": "",
	"current_durability_text": "",
	"max_durability_text": "",
	"next_action_text": "",
	"repair_available": false,
}


func configure_resolved_result(result: Dictionary) -> Dictionary:
	var parsed := _parse_result(result)
	if parsed.is_empty():
		return {"status": "BLOCKED", "reason": "INVALID_DURABILITY_CONSEQUENCE"}
	_view_state = parsed
	_set_result_illustration_visible(true)
	_refresh_controls()
	return {"status": "APPLIED"}


func view_state() -> Dictionary:
	return _view_state.duplicate(true)


func _parse_result(result: Dictionary) -> Dictionary:
	var event_id: Variant = result.get("event_id", "")
	var next_action: Variant = result.get("primary_next_action", "")
	var item_refs: Variant = result.get("item_refs", [])
	var consequence: Variant = result.get("durability_consequence", null)
	if not event_id is String or event_id.is_empty() or not next_action is String:
		return {}
	if not item_refs is Array or not consequence is Dictionary:
		return {}
	var item_uid := _primary_item_uid(item_refs)
	if item_uid.is_empty() or not _has_valid_consequence(consequence):
		return {}

	var damage_applied: bool = bool(consequence["damage_applied"])
	var repair_available: bool = next_action == "REPAIR_ITEM" and bool(consequence["repair_job_available"])
	return {
		"event_id": event_id,
		"item_uid": item_uid,
		"summary_text": "고객의 실제 사용 결과입니다.",
		"damage_text": "실제 사용 중 손상이 발생했습니다." if damage_applied else "실제 사용 중 손상은 없었습니다.",
		"current_durability_text": "내구도: %d → %d" % [int(consequence["before_current_durability"]), int(consequence["after_current_durability"])],
		"max_durability_text": "최대 내구도: %d → %d" % [int(consequence["before_max_durability"]), int(consequence["after_max_durability"])],
		"next_action_text": "다음 행동: 수리하기" if repair_available else "다음 행동: 작품 확인",
		"repair_available": repair_available,
	}


func _primary_item_uid(item_refs: Array) -> String:
	for reference in item_refs:
		if reference is Dictionary and reference.get("role", "") == "PRIMARY_ITEM" and reference.get("uid", "") is String:
			return str(reference["uid"])
	return ""


func _has_valid_consequence(consequence: Dictionary) -> bool:
	var required_bools := ["actual_item_use", "damage_applied", "repair_job_available"]
	var required_numbers := [
		"before_current_durability",
		"after_current_durability",
		"before_max_durability",
		"after_max_durability",
	]
	for key in required_bools:
		if not consequence.has(key) or not consequence[key] is bool:
			return false
	for key in required_numbers:
		if not consequence.has(key) or not consequence[key] is int or int(consequence[key]) < 0:
			return false
	if not bool(consequence["actual_item_use"]):
		return false
	if int(consequence["after_current_durability"]) > int(consequence["before_current_durability"]):
		return false
	if int(consequence["after_max_durability"]) != int(consequence["before_max_durability"]):
		return false
	if bool(consequence["damage_applied"]) != (int(consequence["after_current_durability"]) < int(consequence["before_current_durability"])):
		return false
	return bool(consequence["repair_job_available"]) == bool(consequence["damage_applied"])


func _refresh_controls() -> void:
	_set_label("ResultLayout/SummaryLabel", str(_view_state["summary_text"]))
	_set_label("ResultLayout/DamageLabel", str(_view_state["damage_text"]))
	_set_label("ResultLayout/CurrentDurabilityLabel", str(_view_state["current_durability_text"]))
	_set_label("ResultLayout/MaxDurabilityLabel", str(_view_state["max_durability_text"]))
	_set_label("ResultLayout/NextActionLabel", str(_view_state["next_action_text"]))
	_set_label("ResultLayout/RepairActionHint", "작업대에서 수리하기" if bool(_view_state["repair_available"]) else "")


func _ready() -> void:
	_ensure_result_illustration()
	_set_result_illustration_visible(false)


func _ensure_result_illustration() -> void:
	var illustration := get_node_or_null("CustomerResultEventIllustration") as TextureRect
	if illustration == null:
		illustration = TextureRect.new()
		illustration.name = "CustomerResultEventIllustration"
		illustration.z_index = -1
		illustration.mouse_filter = Control.MOUSE_FILTER_IGNORE
		illustration.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		illustration.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		illustration.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
		add_child(illustration)
		move_child(illustration, 0)
	illustration.texture = CustomerResultIllustrationTexture
	var veil := get_node_or_null("CustomerResultReadabilityVeil") as ColorRect
	if veil == null:
		veil = ColorRect.new()
		veil.name = "CustomerResultReadabilityVeil"
		veil.z_index = -1
		veil.mouse_filter = Control.MOUSE_FILTER_IGNORE
		veil.color = Color(0.08, 0.05, 0.03, 0.62)
		veil.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		add_child(veil)
		move_child(veil, 1)


func _set_result_illustration_visible(visible: bool) -> void:
	_ensure_result_illustration()
	var illustration := get_node_or_null("CustomerResultEventIllustration") as TextureRect
	var veil := get_node_or_null("CustomerResultReadabilityVeil") as ColorRect
	var fallback := get_node_or_null("ResultBackground") as ColorRect
	if illustration != null:
		illustration.visible = visible
	if veil != null:
		veil.visible = visible
	if fallback != null:
		fallback.visible = not visible


func _set_label(path: String, value: String) -> void:
	var label := get_node_or_null(path) as Label
	if label != null:
		label.text = value
