# 작업대 화면에서 현재 정본 내구도·수리 상태를 표시하고 수리 실행을 연결한다.
class_name VSWorkshopScreen
extends Control

const RepairResolverScript = preload("res://scripts/vertical_slice/resolvers/vs_repair_resolver.gd")
const MaintenanceServiceScript = preload("res://scripts/vertical_slice/services/vs_workshop_maintenance_service.gd")

var _item = null
var _resources = null
var _maintenance_service = null


func _ready() -> void:
	var repair_button := get_node_or_null("WorkshopLayout/RepairButton") as Button
	if repair_button != null and not repair_button.pressed.is_connected(_on_repair_pressed):
		repair_button.pressed.connect(_on_repair_pressed)
	_refresh_controls()


func configure_context(item, resources, maintenance_service = null) -> void:
	_item = item
	_resources = resources
	_maintenance_service = maintenance_service if maintenance_service != null else MaintenanceServiceScript.new()
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
		}
	var quote: Dictionary = RepairResolverScript.new().quote(_item)
	return {
		"has_item": true,
		"durability_text": "%d / %d / %d" % [int(_item.current_durability), int(_item.max_durability), int(_item.base_max_durability)],
		"durability_state": str(_item.effective_durability_state()),
		"repair_allowed": bool(quote.get("allowed", false)),
		"repair_reason": str(quote.get("reason", "")),
		"repair_gold_cost": int(quote.get("gold_cost", 0)),
		"repair_material_units": int(quote.get("reinforcement_units", 0)),
	}


func request_repair_with_rolls(rolls: Dictionary) -> Dictionary:
	if _item == null or _resources == null:
		return {"status": "BLOCKED", "reason": "MISSING_WORKSHOP_CONTEXT"}
	if _maintenance_service == null:
		_maintenance_service = MaintenanceServiceScript.new()
	var result: Dictionary = _maintenance_service.try_repair_with_rolls(_item, _resources, rolls)
	_refresh_controls()
	return result


func refresh_after_enhancement() -> void:
	_refresh_controls()


func _on_repair_pressed() -> void:
	var result := request_repair_with_rolls({})
	var message := get_node_or_null("WorkshopLayout/RepairMessageLabel") as Label
	if message != null:
		message.text = "수리 완료" if str(result.get("status", "")) == "APPLIED" else "수리 불가: %s" % str(result.get("reason", "UNKNOWN"))


func _refresh_controls() -> void:
	var state := view_state()
	var durability := get_node_or_null("WorkshopLayout/DurabilityValueLabel") as Label
	var condition := get_node_or_null("WorkshopLayout/DurabilityStateLabel") as Label
	var quote := get_node_or_null("WorkshopLayout/RepairQuoteLabel") as Label
	var repair_button := get_node_or_null("WorkshopLayout/RepairButton") as Button
	if durability != null:
		durability.text = str(state["durability_text"])
	if condition != null:
		condition.text = "상태: %s" % str(state["durability_state"])
	if quote != null:
		quote.text = "수리: %d Gold · 보강재 %d개" % [int(state["repair_gold_cost"]), int(state["repair_material_units"])] if bool(state["repair_allowed"]) else "수리 불가: %s" % str(state["repair_reason"])
	if repair_button != null:
		repair_button.disabled = not bool(state["repair_allowed"])
