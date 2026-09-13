extends RefCounted

const RULESET = "BLACKSMITH_REPLAN_TAGS_20260912"
const KEYS = ["schema_version","order_id","phase","material_units","item_uid","gold_reward","material_reward","accepted_day"]

static func validate(envelope) -> String:
	var run = envelope.active_run
	if not _whole(run.get("current_day",null)) or run.current_day < 1:
		return "INVALID_RECOVERY_CURRENT_DAY"
	if run.has("recovery_calendar"):
		var calendar = run.recovery_calendar
		if not calendar is Dictionary or calendar.size() != 3 or not calendar.has_all(["schema_version","policy_id","last_closed_day"]):
			return "INVALID_RECOVERY_CALENDAR"
		if not _whole(calendar.schema_version) or calendar.schema_version != 1 or calendar.policy_id != "MANUAL_CLOSE_V1":
			return "INVALID_RECOVERY_CALENDAR_POLICY"
		if not _whole(calendar.last_closed_day) or calendar.last_closed_day < 1 or calendar.last_closed_day != run.current_day - 1:
			return "INVALID_RECOVERY_CALENDAR_DAY"
	var history = run.get("recovery_order_history",[])
	if not history is Array:
		return "INVALID_RECOVERY_HISTORY"
	if run.has("recovery_order_history") and (history.is_empty() or not run.has("recovery_calendar")):
		return "INVALID_RECOVERY_HISTORY_CALENDAR"
	var uids = []
	var previous_delivery_day = 0
	for index in range(history.size()):
		var error = _validate_record(envelope,history[index],index+1)
		if not error.is_empty(): return error
		var record = history[index]
		if record.phase != "DELIVERED" or record.item_uid in uids or record.accepted_day <= previous_delivery_day:
			return "INVALID_RECOVERY_HISTORY_ORDER"
		previous_delivery_day = int(envelope.get_item(record.item_uid).ledger[-1].occurred_at_game_day)
		if previous_delivery_day > run.recovery_calendar.last_closed_day:
			return "INVALID_RECOVERY_HISTORY_DAY"
		uids.append(record.item_uid)
	if run.has("recovery_order"):
		var error = _validate_record(envelope,run.recovery_order,history.size()+1)
		if not error.is_empty(): return error
		if run.recovery_order.item_uid in uids or run.recovery_order.accepted_day <= previous_delivery_day:
			return "INVALID_RECOVERY_ACTIVE_ORDER"
	if (run.has("recovery_calendar") or run.has("recovery_order_history") or run.has("recovery_order")) and run.get("tag_ruleset_id","") != RULESET:
		return "INVALID_RECOVERY_POLICY"
	return ""

static func _whole(value) -> bool:
	return (value is int or value is float) and is_finite(float(value)) and float(value) == floor(float(value))

static func _validate_record(envelope,record,number: int) -> String:
	if not record is Dictionary or record.size() != KEYS.size():
		return "INVALID_RECOVERY_RECORD"
	for key in KEYS:
		if not record.has(key): return "INVALID_RECOVERY_FIELDS"
	for key in ["schema_version","material_units","gold_reward","material_reward","accepted_day"]:
		if not (record[key] is int or record[key] is float) or not is_finite(float(record[key])) or float(record[key]) != floor(float(record[key])):
			return "INVALID_RECOVERY_NUMBER"
	if envelope.active_run.get("tag_ruleset_id","") != RULESET or record.schema_version != 1 or record.gold_reward != 400 or record.material_reward != 2:
		return "INVALID_RECOVERY_POLICY"
	if record.order_id != str(envelope.active_run.run_id) + "-recovery-" + str(number) or record.accepted_day < 1 or record.accepted_day > envelope.active_run.current_day:
		return "INVALID_RECOVERY_ID_DAY"
	if not record.item_uid is String or record.phase not in ["ACCEPTED","READY","DELIVERED"]:
		return "INVALID_RECOVERY_PHASE"
	if record.phase == "ACCEPTED":
		return "" if record.item_uid == "" and record.material_units == 1 else "INVALID_RECOVERY_MATERIAL"
	var item = envelope.get_item(record.item_uid)
	if record.material_units != 0 or item == null or item.enhancement_level != 0 or item.current_durability != 5 or item.max_durability != 5:
		return "INVALID_RECOVERY_ITEM"
	if str(envelope.active_run.get("selected_item_uid","")) == record.item_uid:
		return "RECOVERY_ITEM_NOT_SELECTABLE"
	var expected_owner = "CUSTOMER_RECOVERY_RESERVED" if record.phase == "READY" else "CUSTOMER_RECOVERY"
	if item.owner_id != expected_owner or item.ledger.size() != (1 if record.phase == "READY" else 2):
		return "INVALID_RECOVERY_OWNERSHIP"
	var birth_day = item.ledger[0].occurred_at_game_day
	if not _whole(birth_day) or birth_day < record.accepted_day or birth_day > envelope.active_run.current_day:
		return "INVALID_RECOVERY_BIRTH_DAY"
	if record.phase == "DELIVERED":
		var entry = item.ledger[-1]
		if not _whole(entry.occurred_at_game_day) or entry.occurred_at_game_day < birth_day or entry.occurred_at_game_day > envelope.active_run.current_day:
			return "INVALID_RECOVERY_DELIVERY_DAY"
		if entry.event_id != record.order_id + "-delivery" or entry.event_type != "RECOVERY_DELIVERED" or JSON.parse_string(JSON.stringify(entry.payload)) != JSON.parse_string('{"gold":400,"common_reinforcement_material":2}'):
			return "INVALID_RECOVERY_SETTLEMENT"
	return ""

func accept(envelope, save) -> Dictionary:
	var current = _current(envelope, save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	if current.active_run.has("recovery_order"): return _already(current)
	if not _same(envelope,current): return _blocked("STALE_SOURCE")
	current.active_run["recovery_order"] = {
		"schema_version":1,"order_id":str(current.active_run.run_id)+"-recovery-"+str(current.active_run.get("recovery_order_history",[]).size()+1),
		"phase":"ACCEPTED","material_units":1,"item_uid":"","gold_reward":400,
		"material_reward":2,"accepted_day":int(current.active_run.current_day)}
	return _commit(current,save)

func forge(envelope, completion: Dictionary, save) -> Dictionary:
	var current = _current(envelope,save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	var record = current.active_run.get("recovery_order",{})
	if record.get("phase","") in ["READY","DELIVERED"]: return _already(current)
	if record.get("phase","") != "ACCEPTED" or not _same(envelope,current): return _blocked("ORDER_NOT_ACCEPTED_OR_STALE")
	var input = load("res://scripts/forging/canonical_first_item_input_adapter.gd").new().to_canonical_input_from_completion(completion)
	if input.get("status","") != "READY": return _blocked("INVALID_FORGE_RESULT")
	input.erase("status")
	var isolated = load("res://scripts/vertical_slice/services/vs_run_initializer_service.gd").new().create_replan_candidate_envelope()
	if isolated == null: return _blocked("BIRTH_SETUP_FAILED")
	isolated.active_run.current_day = current.active_run.current_day
	var born = load("res://scripts/vertical_slice/services/vs_item_birth_service.gd").new().commit_first_forge(isolated,input)
	if born.status != "APPLIED": return born
	if current.items_by_uid.has(born.item_uid): return _blocked("UID_COLLISION")
	born.item.owner_id = "CUSTOMER_RECOVERY_RESERVED"
	if current.add_item(born.item) != OK: return _blocked("INVALID_BORN_ITEM")
	record.phase = "READY"
	record.material_units = 0
	record.item_uid = born.item_uid
	return _commit(current,save)

func deliver(envelope, save) -> Dictionary:
	var current = _current(envelope,save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	var record = current.active_run.get("recovery_order",{})
	if record.get("phase","") == "DELIVERED": return _already(current)
	if record.get("phase","") != "READY" or not _same(envelope,current): return _blocked("ORDER_NOT_READY_OR_STALE")
	var item = current.get_item(record.item_uid)
	var entry = load("res://scripts/vertical_slice/domain/vs_ledger_entry.gd").create(
		item.ledger.size()+1, record.order_id+"-delivery","RECOVERY_DELIVERED","BS-REPLAN-20260913-04",
		"RESERVED","DELIVERED",int(current.active_run.current_day),{"gold":400,"common_reinforcement_material":2})
	if item.append_ledger_entry(entry.to_dict()) != OK: return _blocked("INVALID_DELIVERY_LEDGER")
	item.owner_id = "CUSTOMER_RECOVERY"
	record.phase = "DELIVERED"
	current.workshop_resources.gold += 400
	var stock = current.workshop_resources.material_stock
	stock["common_reinforcement_material"] = int(stock.get("common_reinforcement_material",0))+2
	return _commit(current,save)

static func close_block_reason(envelope) -> String:
	if envelope == null or not envelope.validation_errors.is_empty() or envelope.active_run.get("tag_ruleset_id","") != RULESET:
		return "INVALID_CAMPAIGN"
	if not envelope.schedule_state.is_empty():
		return "UNKNOWN_SCHEDULE"
	for uid in envelope.items_by_uid:
		if load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").pending_trial(envelope,str(uid)):
			return "PENDING_WORLD_RESULT"
	return ""

func close_day(envelope,source_day,save) -> Dictionary:
	if not _whole(source_day) or source_day < 1:
		return _blocked("INVALID_SOURCE_DAY")
	var current = _current(envelope,save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	if not _whole(current.active_run.current_day) or current.active_run.current_day < 1:
		return _blocked("INVALID_CURRENT_DAY")
	var day = int(current.active_run.current_day)
	if int(source_day) == day - 1 and current.active_run.get("recovery_calendar",{}).get("last_closed_day",0) == source_day:
		return _already(current)
	if source_day != day or not _same(envelope,current):
		return _blocked("STALE_SOURCE_DAY")
	var reason = close_block_reason(current)
	if not reason.is_empty(): return _blocked(reason)
	var record = current.active_run.get("recovery_order",{})
	if record.get("phase","") == "DELIVERED":
		var history = current.active_run.get("recovery_order_history",[]).duplicate(true)
		history.append(record.duplicate(true))
		current.active_run["recovery_order_history"] = history
		current.active_run.erase("recovery_order")
	current.active_run.current_day = day + 1
	current.active_run["recovery_calendar"] = {"schema_version":1,"policy_id":"MANUAL_CLOSE_V1","last_closed_day":day}
	return _commit(current,save)

func _current(envelope,save):
	if envelope == null or save == null or not envelope.validation_errors.is_empty() or not save.has_method("load_envelope") or not save.has_method("save_envelope"):
		return null
	if envelope.active_run.get("tag_ruleset_id","") != RULESET: return null
	var current = save.load_envelope()
	if current == null or not current.validation_errors.is_empty() or current.recovered_from_backup: return null
	if current.active_run.get("run_id","") != envelope.active_run.get("run_id","") or current.active_run.get("tag_ruleset_id","") != RULESET: return null
	return current

func _same(a,b) -> bool:
	return load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").serialized_equal(a.to_dict(),b.to_dict())

func _commit(candidate,save) -> Dictionary:
	var verified = load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").from_dict(candidate.to_dict())
	if not verified.validation_errors.is_empty(): return _blocked("INVALID_CANDIDATE")
	if save.save_envelope(verified) != OK: return _blocked("SAVE_FAILED")
	var actual = save.load_envelope()
	if actual == null or not actual.validation_errors.is_empty() or actual.recovered_from_backup or not _same(verified,actual):
		return _blocked("READBACK_FAILED")
	return {"status":"APPLIED","envelope":actual}

func _already(envelope) -> Dictionary:
	return {"status":"ALREADY_APPLIED","envelope":envelope}

func _blocked(reason: String) -> Dictionary:
	return {"status":"BLOCKED","reason":reason}
