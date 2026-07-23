class_name EquipmentWorldRegistry
extends RefCounted

const LIFECYCLE_WORKSHOP := "WORKSHOP"
const LIFECYCLE_ACTIVE_OWNER := "ACTIVE_OWNER"
const LIFECYCLE_EVENT_ELIGIBLE := "EVENT_ELIGIBLE"
const LIFECYCLE_DORMANT := "DORMANT"
const LIFECYCLE_HISTORICAL := "HISTORICAL"
const LIFECYCLE_BROKEN_OR_LOST := "BROKEN_OR_LOST"

const REPORT_NONE := "NONE"
const REPORT_PENDING := "PENDING"
const REPORT_RESULT_READY := "RESULT_READY"
const REPORT_OPENED := "REPORT_OPENED"
const REPORT_RESULT_ERROR := "RESULT_ERROR"

var active_record_limit: int = 6
var records: Dictionary = {}
var transaction_to_equipment: Dictionary = {}
var sequence: int = 0


func _init(limit: int = 6) -> void:
	active_record_limit = maxi(limit, 1)


func deliver(
	equipment: Dictionary,
	customer_id: String,
	current_day: int,
	report_delay_days: int,
	delivery_transaction_id: String
) -> Dictionary:
	if delivery_transaction_id != "" and transaction_to_equipment.has(delivery_transaction_id):
		return Dictionary(records[transaction_to_equipment[delivery_transaction_id]]).duplicate(true)
	sequence += 1
	var equipment_uid := str(equipment.get("equipment_uid", "equipment_%04d" % sequence))
	var record := {
		"record_schema_version": 1,
		"equipment_uid": equipment_uid,
		"equipment": equipment.duplicate(true),
		"owner_id": customer_id,
		"lifecycle_state": LIFECYCLE_ACTIVE_OWNER,
		"report_state": REPORT_PENDING,
		"delivered_day": current_day,
		"result_due_day": current_day + maxi(report_delay_days, 0),
		"delivery_transaction_id": delivery_transaction_id,
		"history": [{"event_id": "delivery:%s" % delivery_transaction_id, "type": "DELIVERED", "day": current_day, "owner_id": customer_id}],
		"applied_event_ids": [],
		"result": {},
		"personal_masterpiece": bool(equipment.get("personal_masterpiece", false)),
	}
	records[equipment_uid] = record
	if delivery_transaction_id != "":
		transaction_to_equipment[delivery_transaction_id] = equipment_uid
	_enforce_active_limit()
	return record.duplicate(true)


func due_records(current_day: int) -> Array[Dictionary]:
	var due: Array[Dictionary] = []
	for record_value in records.values():
		var record: Dictionary = record_value
		if str(record.get("report_state", REPORT_NONE)) == REPORT_PENDING and int(record.get("result_due_day", 0)) <= current_day:
			due.append(record.duplicate(true))
	due.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		return int(a.get("delivered_day", 0)) < int(b.get("delivered_day", 0))
	)
	return due


func apply_result(equipment_uid: String, result: Dictionary, event_id: String) -> Dictionary:
	if not records.has(equipment_uid):
		return {"ok": false, "status": "NOT_FOUND"}
	var record: Dictionary = records[equipment_uid]
	var applied: Array = record.get("applied_event_ids", [])
	if applied.has(event_id):
		return {"ok": true, "status": "ALREADY_APPLIED", "record": record.duplicate(true)}
	applied.append(event_id)
	record["applied_event_ids"] = applied
	record["result"] = result.duplicate(true)
	record["report_state"] = REPORT_RESULT_READY
	record["lifecycle_state"] = LIFECYCLE_EVENT_ELIGIBLE
	var history: Array = record.get("history", [])
	history.append({"event_id": event_id, "type": "WORLD_RESULT", "result_id": result.get("result_id", ""), "score": result.get("score", 0)})
	record["history"] = history
	records[equipment_uid] = record
	return {"ok": true, "status": "APPLIED", "record": record.duplicate(true)}


func mark_report_opened(equipment_uid: String) -> Dictionary:
	if not records.has(equipment_uid):
		return {"ok": false, "status": "NOT_FOUND"}
	var record: Dictionary = records[equipment_uid]
	if str(record.get("report_state", "")) == REPORT_RESULT_READY:
		record["report_state"] = REPORT_OPENED
		records[equipment_uid] = record
	return {"ok": true, "record": record.duplicate(true)}


func mark_result_error(equipment_uid: String, error_code: String) -> Dictionary:
	if not records.has(equipment_uid):
		return {"ok": false, "status": "NOT_FOUND"}
	var record: Dictionary = records[equipment_uid]
	record["report_state"] = REPORT_RESULT_ERROR
	record["result_error"] = error_code
	records[equipment_uid] = record
	return {"ok": true, "record": record.duplicate(true)}


func retry_result(equipment_uid: String, result: Dictionary, event_id: String) -> Dictionary:
	if not records.has(equipment_uid):
		return {"ok": false, "status": "NOT_FOUND"}
	if str(records[equipment_uid].get("report_state", "")) != REPORT_RESULT_ERROR:
		return {"ok": false, "status": "NOT_IN_ERROR"}
	return apply_result(equipment_uid, result, event_id)


func snapshot() -> Dictionary:
	return {
		"record_schema_version": 1,
		"active_record_limit": active_record_limit,
		"records": records.duplicate(true),
	}


func _enforce_active_limit() -> void:
	var active: Array[Dictionary] = []
	for record_value in records.values():
		var record: Dictionary = record_value
		if str(record.get("lifecycle_state", "")) in [LIFECYCLE_ACTIVE_OWNER, LIFECYCLE_EVENT_ELIGIBLE]:
			active.append(record)
	active.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		return int(a.get("delivered_day", 0)) < int(b.get("delivered_day", 0))
	)
	while active.size() > active_record_limit:
		var candidate_index := -1
		for index in range(active.size()):
			if not bool(active[index].get("personal_masterpiece", false)):
				candidate_index = index
				break
		if candidate_index < 0:
			break
		var candidate: Dictionary = active[candidate_index]
		var uid := str(candidate.get("equipment_uid", ""))
		candidate["lifecycle_state"] = LIFECYCLE_DORMANT
		records[uid] = candidate
		active.remove_at(candidate_index)
