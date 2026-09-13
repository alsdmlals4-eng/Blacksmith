extends RefCounted

const RULESET = "BLACKSMITH_REPLAN_TAGS_20260912"
const KEYS = ["schema_version","order_id","phase","material_units","item_uid","gold_reward","material_reward","accepted_day"]

static func validate(envelope) -> String:
	if not envelope.active_run.has("recovery_order"):
		return ""
	var record = envelope.active_run.recovery_order
	if not record is Dictionary or record.size() != KEYS.size():
		return "INVALID_RECOVERY_RECORD"
	for key in KEYS:
		if not record.has(key): return "INVALID_RECOVERY_FIELDS"
	for key in ["schema_version","material_units","gold_reward","material_reward","accepted_day"]:
		if not (record[key] is int or record[key] is float) or not is_finite(float(record[key])) or float(record[key]) != floor(float(record[key])):
			return "INVALID_RECOVERY_NUMBER"
	if envelope.active_run.get("tag_ruleset_id","") != RULESET or record.schema_version != 1 or record.gold_reward != 400 or record.material_reward != 2:
		return "INVALID_RECOVERY_POLICY"
	if record.order_id != str(envelope.active_run.run_id) + "-recovery-1" or record.accepted_day < 1 or record.accepted_day > envelope.active_run.current_day:
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
	if record.phase == "DELIVERED":
		var entry = item.ledger[-1]
		if entry.event_id != record.order_id + "-delivery" or entry.event_type != "RECOVERY_DELIVERED" or JSON.parse_string(JSON.stringify(entry.payload)) != JSON.parse_string('{"gold":400,"common_reinforcement_material":2}'):
			return "INVALID_RECOVERY_SETTLEMENT"
	return ""

func accept(envelope, save) -> Dictionary:
	var current = _current(envelope, save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	if current.active_run.has("recovery_order"): return _already(current)
	if not _same(envelope,current): return _blocked("STALE_SOURCE")
	current.active_run["recovery_order"] = {
		"schema_version":1,"order_id":str(current.active_run.run_id)+"-recovery-1",
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
