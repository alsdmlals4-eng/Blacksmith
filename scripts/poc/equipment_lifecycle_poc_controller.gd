class_name EquipmentLifecyclePocController
extends RefCounted

const STATE_CONTRACT := "CONTRACT"
const STATE_WORKSHOP := "WORKSHOP"
const STATE_REPORT_READY := "REPORT_READY"
const STATE_FOLLOW_UP := "FOLLOW_UP"

var contract
var registry
var resolver
var calendar
var resources
var telemetry

var state: String = STATE_CONTRACT
var inventory: Array[Dictionary] = []
var fame: int = 0
var relationship: int = 0
var follow_up_started: bool = false


func _init(
	customer_contract,
	world_registry,
	activity_resolver,
	workshop_calendar,
	workshop_resources,
	poc_telemetry = null
) -> void:
	contract = customer_contract
	registry = world_registry
	resolver = activity_resolver
	calendar = workshop_calendar
	resources = workshop_resources
	telemetry = poc_telemetry


func accept_contract() -> void:
	state = STATE_WORKSHOP
	_record("contract_viewed", {"day": calendar.day})


func add_equipment(equipment: Dictionary) -> void:
	inventory.append(equipment.duplicate(true))


func deliver(equipment_uid: String, delivery_transaction_id: String, failure_stage: String = "") -> Dictionary:
	if delivery_transaction_id != "" and registry.transaction_to_equipment.has(delivery_transaction_id):
		var existing_uid := str(registry.transaction_to_equipment[delivery_transaction_id])
		return {
			"ok": true,
			"status": "ALREADY_DELIVERED",
			"record": Dictionary(registry.records.get(existing_uid, {})).duplicate(true),
		}
	var index := _find_inventory_index(equipment_uid)
	if index < 0:
		return {"ok": false, "status": "NOT_FOUND"}
	var equipment: Dictionary = inventory[index].duplicate(true)
	var eligibility: Dictionary = contract.can_deliver(equipment, calendar.day)
	if not bool(eligibility.get("ok", false)):
		return eligibility

	var before := _transaction_snapshot()
	inventory.remove_at(index)
	if failure_stage == "after_inventory":
		_rollback(before)
		return {"ok": false, "status": "INJECTED_FAILURE"}

	equipment["owner_id"] = str(contract.config.get("customer_id", "gladiator_kyle"))
	if failure_stage == "after_owner":
		_rollback(before)
		return {"ok": false, "status": "INJECTED_FAILURE"}

	resources.gold += int(contract.config.get("payment_gold", 0))
	if failure_stage == "after_payment":
		_rollback(before)
		return {"ok": false, "status": "INJECTED_FAILURE"}

	fame += int(contract.config.get("immediate_fame", 0))
	if failure_stage == "after_fame":
		_rollback(before)
		return {"ok": false, "status": "INJECTED_FAILURE"}

	var record: Dictionary = registry.deliver(
		equipment,
		str(contract.config.get("customer_id", "gladiator_kyle")),
		calendar.day,
		int(contract.config.get("report_delay_days", 1)),
		delivery_transaction_id
	)
	if failure_stage == "after_record":
		_rollback(before)
		return {"ok": false, "status": "INJECTED_FAILURE"}

	_record("delivered", {"equipment_uid": equipment_uid, "transaction_id": delivery_transaction_id})
	return {"ok": true, "status": "DELIVERED", "record": record}


func end_day() -> Dictionary:
	calendar.end_day()
	_record("day_ended", {"day": calendar.day})
	var resolved: Array[Dictionary] = []
	for due in registry.due_records(calendar.day):
		var fit: Dictionary = contract.evaluate_fit(Dictionary(due.get("equipment", {})))
		var result: Dictionary = resolver.resolve(fit, 0.5)
		var uid := str(due.get("equipment_uid", ""))
		var event_id := "gladiator_match:%s:%d" % [uid, calendar.day]
		var applied: Dictionary = registry.apply_result(uid, result, event_id)
		if bool(applied.get("ok", false)):
			resolved.append(result)
	if not resolved.is_empty():
		state = STATE_REPORT_READY
	return {"day": calendar.day, "resolved_results": resolved, "snapshot": snapshot()}


func open_report(equipment_uid: String) -> Dictionary:
	if not registry.records.has(equipment_uid):
		return {"ok": false, "status": "NOT_FOUND"}
	var record: Dictionary = registry.records[equipment_uid]
	if str(record.get("report_state", "")) not in [registry.REPORT_RESULT_READY, registry.REPORT_OPENED]:
		return {"ok": false, "status": "REPORT_NOT_READY"}
	if not bool(record.get("report_rewards_applied", false)):
		var result: Dictionary = record.get("result", {})
		fame += int(result.get("fame", 0))
		relationship += int(result.get("relationship", 0))
		record["report_rewards_applied"] = true
		registry.records[equipment_uid] = record
	registry.mark_report_opened(equipment_uid)
	state = STATE_FOLLOW_UP
	follow_up_started = true
	_record("report_opened", {"equipment_uid": equipment_uid})
	_record("follow_up_started", {"customer_id": contract.config.get("customer_id", "")})
	return {"ok": true, "record": Dictionary(registry.records[equipment_uid]).duplicate(true), "snapshot": snapshot()}


func snapshot() -> Dictionary:
	return {
		"state": state,
		"inventory": inventory.duplicate(true),
		"fame": fame,
		"relationship": relationship,
		"follow_up_started": follow_up_started,
		"calendar": calendar.snapshot(),
		"resources": resources.snapshot(),
		"world": registry.snapshot(),
	}


func _find_inventory_index(equipment_uid: String) -> int:
	for index in range(inventory.size()):
		if str(inventory[index].get("equipment_uid", "")) == equipment_uid:
			return index
	return -1


func _transaction_snapshot() -> Dictionary:
	return {
		"inventory": inventory.duplicate(true),
		"gold": resources.gold,
		"fame": fame,
		"relationship": relationship,
		"records": registry.records.duplicate(true),
		"transactions": registry.transaction_to_equipment.duplicate(true),
		"sequence": registry.sequence,
	}


func _rollback(before: Dictionary) -> void:
	inventory.clear()
	for item in Array(before.get("inventory", [])):
		inventory.append(Dictionary(item).duplicate(true))
	resources.gold = int(before.get("gold", resources.gold))
	fame = int(before.get("fame", fame))
	relationship = int(before.get("relationship", relationship))
	registry.records = Dictionary(before.get("records", {})).duplicate(true)
	registry.transaction_to_equipment = Dictionary(before.get("transactions", {})).duplicate(true)
	registry.sequence = int(before.get("sequence", registry.sequence))


func _record(event_name: String, payload: Dictionary) -> void:
	if telemetry != null and telemetry.has_method("record"):
		telemetry.record(event_name, payload)
