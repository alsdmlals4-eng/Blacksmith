extends RefCounted

const Catalog = preload("res://scripts/vertical_slice/domain/vs_commission_catalog.gd")
const Equipment = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
const RULESET = "BLACKSMITH_REPLAN_TAGS_20260912"
const MAX_SAFE_INTEGER = 9007199254740991
const BUCKET_KEYS = ["schema_version", "command_sequence", "active_order", "history"]
const ORDER_KEYS = ["schema_version", "order_id", "definition_snapshot", "funding_origin",
	"ownership_mode", "phase", "accepted_day", "closed_day", "accepted_sequence",
	"command_sequence", "accept_source_hash", "reserve_source_hash", "item_uid",
	"previous_selected_item_uid", "escrow"]
const ESCROW_KEYS = ["order_id", "allocated_credit", "consumed_credit", "material_id",
	"allocated_qty", "consumed_qty", "produced_item_uid", "reclaimed"]
const SETTLEMENT_KEYS = ["schema_version", "ruleset_id", "policy_id", "event_id", "report_kind",
	"source_hash", "item_snapshot", "handed_off_day", "due_day", "rolls", "success_percent",
	"damage_percent", "payout", "mission_success", "damage_applied"]
const SCHEDULE_POLICY = "COMMISSION_SCHEDULE_TRIAL_V1"

static func validate(envelope) -> String:
	var run = envelope.active_run
	if not run.has("commission"): return ""
	if run.get("tag_ruleset_id", "") != RULESET or not _whole(run.get("current_day")) or run.current_day < 1:
		return "INVALID_COMMISSION_CAMPAIGN"
	var bucket = run.commission
	if not _fields(bucket, BUCKET_KEYS) or not _whole(bucket.schema_version) or bucket.schema_version != 1:
		return "INVALID_COMMISSION_BUCKET"
	if not _whole(bucket.command_sequence) or bucket.command_sequence < 1 or not bucket.history is Array or not bucket.active_order is Dictionary:
		return "INVALID_COMMISSION_SEQUENCE"
	var records = bucket.history.duplicate()
	if not bucket.active_order.is_empty(): records.append(bucket.active_order)
	if records.is_empty(): return "EMPTY_COMMISSION_BUCKET"
	var last_sequence = 0
	var last_day = 1
	for index in range(records.size()):
		var record = records[index]
		var active = index == bucket.history.size()
		var error = _validate_record(envelope, record, index + 1, active)
		if not error.is_empty(): return error
		if record.accepted_sequence != last_sequence + 1 or record.accepted_day < last_day:
			return "INVALID_COMMISSION_ORDER_SEQUENCE"
		last_sequence = record.command_sequence
		last_day = record.accepted_day if active else record.closed_day
	if last_sequence != bucket.command_sequence: return "COMMISSION_SEQUENCE_MISMATCH"
	return ""

static func _validate_record(envelope, record, number: int, active: bool) -> String:
	if not record is Dictionary: return "INVALID_COMMISSION_RECORD"
	var scheduled = record.get("phase", "") in ["IN_TRANSIT", "SETTLED"]
	if not _fields(record, ORDER_KEYS + (["settlement"] if scheduled else [])): return "INVALID_COMMISSION_RECORD"
	for key in ["schema_version", "accepted_day", "closed_day", "accepted_sequence", "command_sequence"]:
		if not _whole(record[key]): return "INVALID_COMMISSION_NUMBER"
	for key in ["order_id", "funding_origin", "ownership_mode", "phase", "accept_source_hash",
		"reserve_source_hash", "item_uid", "previous_selected_item_uid"]:
		if not record[key] is String: return "INVALID_COMMISSION_FIELD_TYPE"
	if record.schema_version != 1 or record.order_id != str(envelope.active_run.run_id) + "-commission-" + str(number):
		return "INVALID_COMMISSION_ID"
	if not record.definition_snapshot is Dictionary or not Catalog.validate_definition(record.definition_snapshot).is_empty():
		return "INVALID_COMMISSION_DEFINITION"
	if not _mode_allowed(record.funding_origin, record.ownership_mode): return "INVALID_COMMISSION_MODE"
	if record.accepted_day < 1 or record.accepted_day > envelope.active_run.current_day or record.accepted_sequence < 1:
		return "INVALID_COMMISSION_DAY"
	if not _hash_valid(record.accept_source_hash): return "INVALID_COMMISSION_SOURCE_HASH"
	if not record.reserve_source_hash.is_empty() and not _hash_valid(record.reserve_source_hash):
		return "INVALID_COMMISSION_RESERVE_HASH"
	if active:
		if record.phase not in ["ACCEPTED", "READY", "IN_TRANSIT"] or record.closed_day != 0: return "INVALID_COMMISSION_ACTIVE_PHASE"
	else:
		if record.phase not in ["CANCELLED", "SETTLED"] or record.closed_day < record.accepted_day or record.closed_day > envelope.active_run.current_day:
			return "INVALID_COMMISSION_HISTORY_PHASE"
	var has_item = not record.item_uid.is_empty()
	if scheduled and not has_item: return "MISSING_COMMISSION_DEPARTURE_ITEM"
	var expected_sequence = record.accepted_sequence + (1 if has_item else 0) + (1 if scheduled else 0) + (0 if active else 1)
	if record.command_sequence != expected_sequence: return "INVALID_COMMISSION_COMMAND_SEQUENCE"
	if active and (record.phase in ["READY", "IN_TRANSIT"]) != has_item: return "INVALID_COMMISSION_ITEM_PHASE"
	var escrow = record.escrow
	if not _fields(escrow, ESCROW_KEYS): return "INVALID_COMMISSION_ESCROW"
	for key in ["allocated_credit", "consumed_credit", "allocated_qty", "consumed_qty"]:
		if not _whole(escrow[key]): return "INVALID_COMMISSION_ESCROW_NUMBER"
	if not escrow.reclaimed is bool or escrow.reclaimed != (record.phase == "CANCELLED") or escrow.order_id != record.order_id or escrow.material_id != "iron":
		return "INVALID_COMMISSION_ESCROW_ID"
	var customer = record.funding_origin == "COMMISSION_ESCROW"
	if escrow.allocated_credit != 0 or escrow.consumed_credit != 0 or escrow.allocated_qty != (1 if customer else 0):
		return "INVALID_COMMISSION_ESCROW_ALLOCATION"
	if escrow.consumed_qty != (1 if customer and has_item else 0): return "INVALID_COMMISSION_ESCROW_CONSUMPTION"
	if escrow.produced_item_uid != (record.item_uid if customer and has_item else null):
		return "INVALID_COMMISSION_PRODUCED_ITEM"
	if not has_item:
		if not record.reserve_source_hash.is_empty() or not record.previous_selected_item_uid.is_empty():
			return "INVALID_COMMISSION_UNRESERVED_STATE"
		return ""
	if not _hash_valid(record.reserve_source_hash): return "MISSING_COMMISSION_RESERVE_HASH"
	var item = envelope.get_item(record.item_uid)
	if item == null: return "COMMISSION_ITEM_NOT_FOUND"
	if scheduled: return _validate_settlement(envelope, record)
	if active:
		var owner = "CUSTOMER_COMMISSION_RESERVED" if customer else "PLAYER_COMMISSION_RESERVED"
		if item.owner_id != owner or Equipment.by_item(item).get("equipment_id", "") != record.definition_snapshot.equipment_id:
			return "INVALID_COMMISSION_RESERVED_OWNER_EQUIPMENT"
		# Reservation requires a living item, but later enhancement may legitimately destroy it.
		if _pending(envelope, record.item_uid): return "INVALID_COMMISSION_RESERVED_ITEM"
		if not record.previous_selected_item_uid.is_empty() and envelope.get_item(record.previous_selected_item_uid) == null:
			return "INVALID_COMMISSION_PREVIOUS_SELECTION"
	elif customer and item.owner_id != "CUSTOMER":
		return "INVALID_COMMISSION_RETURNED_CUSTOMER_OWNER"
	return ""

static func _validate_settlement(envelope, record: Dictionary) -> String:
	var state = record.settlement
	if not _fields(state, SETTLEMENT_KEYS): return "INVALID_COMMISSION_SETTLEMENT"
	for key in ["schema_version", "handed_off_day", "due_day"]:
		if not _whole(state[key]): return "INVALID_COMMISSION_SETTLEMENT_NUMBER"
	if state.schema_version != 1 or state.ruleset_id != RULESET or state.policy_id != SCHEDULE_POLICY:
		return "UNKNOWN_COMMISSION_SETTLEMENT_POLICY"
	if not state.source_hash is String or not _hash_valid(state.source_hash): return "INVALID_HANDOFF_SOURCE"
	if state.event_id != record.order_id + "-world": return "INVALID_COMMISSION_EVENT"
	var basic = record.definition_snapshot.min_level == 0
	if state.report_kind != ("BASIC_CUSTOMER_CHECK" if basic else "AR"): return "INVALID_COMMISSION_REPORT_KIND"
	if state.handed_off_day < record.accepted_day or state.handed_off_day > envelope.active_run.current_day or state.due_day != state.handed_off_day + (1 if basic else 3):
		return "INVALID_COMMISSION_SCHEDULE"
	if not _valid_rolls(state.rolls): return "INVALID_COMMISSION_ROLLS"
	if not _fields(state.payout, ["policy_id", "gold", "common_reinforcement_material", "catalyst_id", "catalyst_qty", "bonus"]):
		return "INVALID_COMMISSION_PAYOUT"
	if state.payout.policy_id != "COMMISSION_ECONOMY_TRIAL_V1" or state.payout.catalyst_id not in ["heart_of_flame", "earth_crystal"]:
		return "INVALID_COMMISSION_PAYOUT_POLICY"
	for key in ["gold", "common_reinforcement_material", "catalyst_qty", "bonus"]:
		if not _whole(state.payout[key]) or state.payout[key] != {"gold":400, "common_reinforcement_material":2, "catalyst_qty":1, "bonus":0}[key]:
			return "INVALID_COMMISSION_PAYOUT_NUMBER"
	if not state.item_snapshot is Dictionary: return "INVALID_COMMISSION_SNAPSHOT"
	var item = load("res://scripts/vertical_slice/domain/vs_item.gd").from_dict(state.item_snapshot)
	if not item.validation_errors.is_empty() or not _equal(state.item_snapshot, item.to_dict()): return "INVALID_COMMISSION_SNAPSHOT"
	var owner = "CUSTOMER_COMMISSION_RESERVED" if record.funding_origin == "COMMISSION_ESCROW" else "PLAYER_COMMISSION_RESERVED"
	if item.uid != record.item_uid or item.owner_id != owner or item.current_durability <= 0 or not Catalog.preview(record.definition_snapshot, item).allowed:
		return "INVALID_COMMISSION_DEPARTURE_ITEM"
	var chances = _chances(record.definition_snapshot, item)
	if chances.is_empty(): return "INVALID_COMMISSION_CHANCES"
	for key in ["success_percent", "damage_percent"]:
		if typeof(state[key]) not in [TYPE_INT, TYPE_FLOAT] or not is_finite(float(state[key])) or state[key] != chances[key]:
			return "INVALID_COMMISSION_CHANCES"
	if record.phase == "IN_TRANSIT":
		if state.due_day <= envelope.active_run.current_day or state.mission_success != null or state.damage_applied != null:
			return "INVALID_COMMISSION_PENDING_RESULT"
	else:
		if record.closed_day != state.due_day or not state.mission_success is bool or not state.damage_applied is bool:
			return "INVALID_COMMISSION_RESULT"
		if state.mission_success != (state.rolls[0] < state.success_percent) or state.damage_applied != (state.rolls[1] < state.damage_percent):
			return "INVALID_COMMISSION_RESULT"
	var expected = _departure_item(record)
	if record.phase == "SETTLED": expected = _result_item(record)
	var actual = envelope.get_item(record.item_uid)
	if record.phase == "IN_TRANSIT" or record.ownership_mode == "SALE":
		if not _equal(expected.to_dict(), actual.to_dict()): return "COMMISSION_SCHEDULED_ITEM_CHANGED"
	else:
		# Returned personal items may be used again, but the immutable event prefix must survive.
		if actual.ledger.size() < expected.ledger.size(): return "COMMISSION_RESULT_LEDGER_MISSING"
		for index in range(expected.ledger.size()):
			if not _equal(actual.ledger[index], expected.ledger[index]): return "COMMISSION_RESULT_LEDGER_CHANGED"
	return ""

static func _valid_rolls(rolls) -> bool:
	if not rolls is Array or rolls.size() != 2: return false
	for value in rolls:
		if typeof(value) not in [TYPE_INT, TYPE_FLOAT] or not is_finite(float(value)) or value < 0 or value >= 100: return false
	return true

static func _equal(a, b) -> bool:
	return load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").serialized_equal(a, b)

static func _chances(definition: Dictionary, item) -> Dictionary:
	if definition.min_level == 0: return {"success_percent":100.0, "damage_percent":0.0}
	var preview = load("res://scripts/vertical_slice/domain/vs_replan_tag_rules.gd").new().world_preview("AR",
		definition.equipment_id, item.enhancement_level, item.catalyst_affix.tags, definition.purpose_axis, definition.purpose_rhythm)
	if not preview.get("ok", false): return {}
	return {"success_percent":preview.success_percent, "damage_percent":load("res://scripts/vertical_slice/resolvers/vs_customer_world_event_resolver.gd").new()._damage_percent(item, "HIGH")}

static func handoff_preview(definition: Dictionary, item) -> Dictionary:
	# The same pure departure calculation; no save, RNG or reservation changes.
	if not Catalog.validate_definition(definition).is_empty(): return {}
	if definition.min_level > 0 and (item == null or Equipment.by_item(item).get("equipment_id", "") != definition.equipment_id): return {}
	return _chances(definition, item)

static func _append_event(item, id: String, kind: String, day: int, before: String, after: String, payload: Dictionary) -> void:
	var entry = load("res://scripts/vertical_slice/domain/vs_ledger_entry.gd").create(item.ledger.size() + 1,
		id, kind, "BS-REPLAN-20260914-10", before, after, day, payload)
	item.append_ledger_entry(entry.to_dict())

static func _departure_item(record: Dictionary):
	var state = record.settlement
	var item = load("res://scripts/vertical_slice/domain/vs_item.gd").from_dict(state.item_snapshot)
	item.owner_id = "CUSTOMER" if record.ownership_mode == "SALE" else "CUSTOMER_BORROWED"
	_append_event(item, record.order_id + "-handoff", "COMMISSION_HANDOFF", state.handed_off_day,
		"RESERVED", "IN_TRANSIT", {"ownership_mode":record.ownership_mode, "payout":state.payout.duplicate(true), "due_day":state.due_day})
	return item

static func _result_item(record: Dictionary):
	var item = _departure_item(record)
	var state = record.settlement
	if state.damage_applied: item.apply_damage_event()
	if record.ownership_mode == "LOAN": item.owner_id = "PLAYER"
	_append_event(item, state.event_id, "COMMISSION_WORLD_RESULT", state.due_day, "IN_TRANSIT", "SETTLED",
		{"mission_success":state.mission_success, "damage_applied":state.damage_applied,
		"report_kind":state.report_kind, "owner_id":item.owner_id, "bonus":0})
	return item

func accept(envelope, definition_id: String, save, funding_origin: String = "COMMISSION_ESCROW", ownership_mode: String = "SALE") -> Dictionary:
	var current = _current(envelope, save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	if not _mode_allowed(funding_origin, ownership_mode): return _blocked("INVALID_MODE")
	var definition = Catalog.by_id(definition_id)
	if definition.is_empty(): return _blocked("UNKNOWN_DEFINITION")
	var bucket = current.active_run.get("commission", _empty_bucket())
	var active = bucket.active_order
	if not active.is_empty():
		if active.definition_snapshot.definition_id == definition_id and active.funding_origin == funding_origin and active.ownership_mode == ownership_mode:
			if _same(envelope, current) or active.accept_source_hash == _fingerprint(envelope): return _already(current)
		return _blocked("ACTIVE_ORDER_OR_STALE_SOURCE")
	if not _same(envelope, current): return _blocked("STALE_SOURCE")
	if bucket.command_sequence >= MAX_SAFE_INTEGER: return _blocked("SEQUENCE_EXHAUSTED")
	var order_id = str(current.active_run.run_id) + "-commission-" + str(bucket.history.size() + 1)
	bucket.command_sequence += 1
	bucket.active_order = {
		"schema_version":1, "order_id":order_id, "definition_snapshot":definition.duplicate(true),
		"funding_origin":funding_origin, "ownership_mode":ownership_mode, "phase":"ACCEPTED",
		"accepted_day":current.active_run.current_day, "closed_day":0,
		"accepted_sequence":bucket.command_sequence, "command_sequence":bucket.command_sequence,
		"accept_source_hash":_fingerprint(envelope), "reserve_source_hash":"", "item_uid":"",
		"previous_selected_item_uid":"", "escrow":{
			"order_id":order_id, "allocated_credit":0, "consumed_credit":0, "material_id":"iron",
			"allocated_qty":1 if funding_origin == "COMMISSION_ESCROW" else 0, "consumed_qty":0,
			"produced_item_uid":null, "reclaimed":false}}
	current.active_run.commission = bucket
	return _commit(current, save, envelope)

func reserve_item(envelope, order_id: String, item_uid: String, save) -> Dictionary:
	var current = _current(envelope, save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	var bucket = current.active_run.get("commission", _empty_bucket())
	var record = bucket.active_order
	if record.get("order_id", "") != order_id or record.get("funding_origin", "") != "PLAYER":
		return _blocked("INVALID_PLAYER_ORDER")
	if record.phase == "READY" and record.item_uid == item_uid and (_same(envelope, current) or record.reserve_source_hash == _fingerprint(envelope)):
		return _already(current)
	if record.phase != "ACCEPTED" or not _same(envelope, current): return _blocked("ORDER_NOT_ACCEPTED_OR_STALE")
	var item = current.get_item(item_uid)
	if item == null or item.owner_id != "PLAYER" or item.current_durability <= 0 or _pending(current, item_uid):
		return _blocked("ITEM_UNAVAILABLE")
	if Equipment.by_item(item).get("equipment_id", "") != record.definition_snapshot.equipment_id:
		return _blocked("EQUIPMENT_MISMATCH")
	if bucket.command_sequence >= MAX_SAFE_INTEGER: return _blocked("SEQUENCE_EXHAUSTED")
	record.reserve_source_hash = _fingerprint(envelope)
	record.previous_selected_item_uid = current.active_run.get("selected_item_uid", "")
	record.item_uid = item_uid
	record.phase = "READY"
	bucket.command_sequence += 1
	record.command_sequence = bucket.command_sequence
	item.owner_id = "PLAYER_COMMISSION_RESERVED"
	current.active_run.selected_item_uid = item_uid
	return _commit(current, save, envelope)

func forge(envelope, order_id: String, completion: Dictionary, save) -> Dictionary:
	if order_id.is_empty(): return _blocked("INVALID_ORDER_ID")
	var current = _current(envelope, save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	var bucket = current.active_run.get("commission", _empty_bucket())
	var record = bucket.active_order
	if record.get("order_id", "") != order_id or record.get("funding_origin", "") != "COMMISSION_ESCROW":
		return _blocked("INVALID_CUSTOMER_ORDER")
	# The legacy adapter intentionally coerces inputs; validate the transaction boundary first.
	if not _whole(completion.get("base_attack")) or completion.base_attack < 1:
		return _blocked("INVALID_FORGE_RESULT")
	for key in ["tap_count", "fever_activation_count"]:
		if not _whole(completion.get(key, 0)) or completion.get(key, 0) < 0:
			return _blocked("INVALID_FORGE_RESULT")
	if not completion.get("fever_bonus_applied", false) is bool: return _blocked("INVALID_FORGE_RESULT")
	var input = load("res://scripts/forging/canonical_first_item_input_adapter.gd").new().to_canonical_input_from_completion(completion)
	if input.get("status", "") != "READY": return _blocked("INVALID_FORGE_RESULT")
	if input.equipment_id != record.definition_snapshot.equipment_id: return _blocked("EQUIPMENT_MISMATCH")
	input.erase("status")
	var input_hash = JSON.stringify(JSON.parse_string(JSON.stringify(input))).sha256_text()
	if record.phase == "READY":
		var item = current.get_item(record.item_uid)
		if (_same(envelope, current) or record.reserve_source_hash == _fingerprint(envelope)) and item.ledger[0].payload.get("commission_forge_input_hash", "") == input_hash:
			return _already(current)
		return _blocked("FORGE_ALREADY_CONSUMED_OR_STALE")
	if record.phase != "ACCEPTED" or not _same(envelope, current): return _blocked("ORDER_NOT_ACCEPTED_OR_STALE")
	if record.escrow.consumed_qty != 0 or record.escrow.reclaimed: return _blocked("ESCROW_UNAVAILABLE")
	if bucket.command_sequence >= MAX_SAFE_INTEGER: return _blocked("SEQUENCE_EXHAUSTED")
	var isolated = load("res://scripts/vertical_slice/services/vs_run_initializer_service.gd").new().create_replan_candidate_envelope()
	isolated.active_run.current_day = current.active_run.current_day
	var born = load("res://scripts/vertical_slice/services/vs_item_birth_service.gd").new().commit_first_forge(isolated, input)
	if born.status != "APPLIED": return _blocked("INVALID_BORN_ITEM")
	if current.items_by_uid.has(born.item_uid): return _blocked("UID_COLLISION")
	born.item.owner_id = "CUSTOMER_COMMISSION_RESERVED"
	born.item.ledger[0].payload.commission_forge_input_hash = input_hash
	if current.add_item(born.item) != OK: return _blocked("INVALID_BORN_ITEM")
	record.reserve_source_hash = _fingerprint(envelope)
	record.previous_selected_item_uid = current.active_run.get("selected_item_uid", "")
	record.item_uid = born.item_uid
	record.phase = "READY"
	record.escrow.consumed_qty = 1
	record.escrow.produced_item_uid = born.item_uid
	bucket.command_sequence += 1
	record.command_sequence = bucket.command_sequence
	current.active_run.selected_item_uid = born.item_uid
	return _commit(current, save, envelope)

static func item_action_allowed(envelope, item_uid: String, action: String) -> bool:
	if action not in ["ENHANCE", "REPAIR", "INDEPENDENT_WORLD", "HANDOFF", "RESERVE"]: return false
	if envelope == null or not envelope.has_method("get_item"): return false
	var item = envelope.get_item(item_uid)
	if item == null: return false
	# Preserve the original untagged standalone service contract.
	if not envelope.active_run.has("commission") and envelope.active_run.get("tag_ruleset_id", "") != RULESET:
		return true
	if not validate(envelope).is_empty(): return false
	var record = envelope.active_run.get("commission", {}).get("active_order", {})
	if record.get("item_uid", "") == item_uid:
		return record.get("phase", "") == "READY" and action in ["ENHANCE", "REPAIR", "HANDOFF"] and not _pending(envelope, item_uid)
	return item.owner_id == "PLAYER"

static func personal_selection_uid(envelope, preferred_uid: String = "") -> String:
	# Selection includes pending personal items so their saved result remains reachable.
	# Editing eligibility is still enforced by each action's pending-trial gate.
	var preferred = envelope.get_item(preferred_uid)
	if preferred != null and preferred.owner_id == "PLAYER" and preferred.current_durability > 0:
		return preferred_uid
	var uids = envelope.items_by_uid.keys()
	uids.sort()
	for uid in uids:
		var item = envelope.get_item(uid)
		if item.owner_id == "PLAYER" and item.current_durability > 0: return str(uid)
	return ""

func cancel(envelope, order_id: String, save) -> Dictionary:
	if order_id.is_empty(): return _blocked("INVALID_ORDER_ID")
	var current = _current(envelope, save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	var bucket = current.active_run.get("commission", _empty_bucket())
	for historical in bucket.history:
		if historical.order_id == order_id:
			if historical.phase != "CANCELLED": return _blocked("ORDER_ALREADY_HANDED_OFF")
			var source_record = envelope.active_run.get("commission", {}).get("active_order", {})
			if _same(envelope, current) or source_record.get("order_id", "") == order_id: return _already(current)
			return _blocked("STALE_CANCEL_SOURCE")
	var record = bucket.active_order
	if record.is_empty() or record.get("order_id", "") != order_id or not _same(envelope, current): return _blocked("ORDER_NOT_FOUND_OR_STALE")
	if record.phase not in ["ACCEPTED", "READY"]: return _blocked("ORDER_ALREADY_HANDED_OFF")
	if bucket.command_sequence >= MAX_SAFE_INTEGER: return _blocked("SEQUENCE_EXHAUSTED")
	if not record.item_uid.is_empty():
		current.get_item(record.item_uid).owner_id = "CUSTOMER" if record.funding_origin == "COMMISSION_ESCROW" else "PLAYER"
		if current.active_run.get("selected_item_uid", "") == record.item_uid:
			current.active_run.selected_item_uid = personal_selection_uid(current, record.previous_selected_item_uid)
	record.phase = "CANCELLED"
	record.closed_day = current.active_run.current_day
	record.escrow.reclaimed = true
	bucket.command_sequence += 1
	record.command_sequence = bucket.command_sequence
	bucket.history.append(record.duplicate(true))
	bucket.active_order = {}
	return _commit(current, save, envelope)

func handoff(envelope, order_id: String, catalyst_id: String, save) -> Dictionary:
	return _handoff(envelope, order_id, catalyst_id, null, save)

func handoff_with_rolls(envelope, order_id: String, catalyst_id: String, rolls: Array, save) -> Dictionary:
	return _handoff(envelope, order_id, catalyst_id, rolls, save)

func _handoff(envelope, order_id: String, catalyst_id: String, rolls, save) -> Dictionary:
	if catalyst_id not in ["heart_of_flame", "earth_crystal"] or order_id.is_empty(): return _blocked("SELECT_CATALYST")
	if rolls != null and not _valid_rolls(rolls): return _blocked("INVALID_ROLLS")
	var current = _current(envelope, save)
	if current == null: return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	var bucket = current.active_run.get("commission", _empty_bucket())
	var record = bucket.active_order
	for historical in bucket.history:
		if historical.order_id == order_id: record = historical
	if record.get("order_id", "") != order_id: return _blocked("ORDER_NOT_FOUND")
	if record.phase in ["IN_TRANSIT", "SETTLED"]:
		var state = record.settlement
		if state.payout.catalyst_id == catalyst_id and (_same(envelope, current) or state.source_hash == _fingerprint(envelope)):
			if rolls == null or _equal(rolls, state.rolls): return _already(current)
		return _blocked("HANDOFF_INPUT_CHANGED")
	if record.phase != "READY" or not _same(envelope, current): return _blocked("ORDER_NOT_READY_OR_STALE")
	var item = current.get_item(record.item_uid)
	if item == null or item.current_durability <= 0 or not Catalog.preview(record.definition_snapshot, item).allowed or not item_action_allowed(current, record.item_uid, "HANDOFF"):
		return _blocked("HANDOFF_REQUIREMENTS_UNMET")
	var chances = _chances(record.definition_snapshot, item)
	if chances.is_empty(): return _blocked("INVALID_WORLD_REQUIREMENTS")
	var delay = 1 if record.definition_snapshot.min_level == 0 else 3
	if bucket.command_sequence >= MAX_SAFE_INTEGER or current.active_run.current_day > MAX_SAFE_INTEGER - delay:
		return _blocked("SEQUENCE_OR_DAY_EXHAUSTED")
	var stock = current.workshop_resources.material_stock
	if current.workshop_resources.gold > MAX_SAFE_INTEGER - 400 or stock.get("common_reinforcement_material", 0) > MAX_SAFE_INTEGER - 2 or stock.get(catalyst_id, 0) >= MAX_SAFE_INTEGER:
		return _blocked("RESOURCE_OVERFLOW")
	# Retry detection and all rejection checks precede production RNG consumption.
	if rolls == null:
		var rng = RandomNumberGenerator.new()
		rng.randomize()
		rolls = [rng.randf() * 99.999999, rng.randf() * 99.999999]
	record.settlement = {"schema_version":1, "ruleset_id":RULESET, "policy_id":SCHEDULE_POLICY,
		"event_id":order_id + "-world", "report_kind":"BASIC_CUSTOMER_CHECK" if delay == 1 else "AR",
		"source_hash":_fingerprint(envelope), "item_snapshot":item.to_dict(), "handed_off_day":current.active_run.current_day,
		"due_day":current.active_run.current_day + delay, "rolls":rolls.duplicate(),
		"success_percent":chances.success_percent, "damage_percent":chances.damage_percent,
		"payout":{"policy_id":"COMMISSION_ECONOMY_TRIAL_V1", "gold":400, "common_reinforcement_material":2,
			"catalyst_id":catalyst_id, "catalyst_qty":1, "bonus":0}, "mission_success":null, "damage_applied":null}
	record.phase = "IN_TRANSIT"
	bucket.command_sequence += 1
	record.command_sequence = bucket.command_sequence
	current.items_by_uid[record.item_uid] = _departure_item(record)
	current.workshop_resources.gold += 400
	stock["common_reinforcement_material"] = int(stock.get("common_reinforcement_material", 0)) + 2
	stock[catalyst_id] = int(stock.get(catalyst_id, 0)) + 1
	current.active_run.selected_item_uid = personal_selection_uid(current, record.previous_selected_item_uid)
	var result = _commit(current, save, envelope)
	# The caller retains these inputs when even the absence of a write is unverified.
	if result.status == "COMMIT_UNCERTAIN": result["retry_rolls"] = rolls.duplicate()
	return result

func settle_due(candidate, day: int) -> Dictionary:
	if candidate == null or not candidate.active_run.has("commission"): return {"status":"NO_DUE"}
	# Called before the close command advances current_day; never saves or draws.
	if not validate(candidate).is_empty() or day != candidate.active_run.current_day + 1:
		return _blocked("INVALID_SETTLEMENT_DAY")
	var bucket = candidate.active_run.commission
	var record = bucket.active_order
	if record.get("phase", "") != "IN_TRANSIT" or record.settlement.due_day > day: return {"status":"NO_DUE"}
	if bucket.command_sequence >= MAX_SAFE_INTEGER: return _blocked("SEQUENCE_EXHAUSTED")
	var state = record.settlement
	state.mission_success = state.rolls[0] < state.success_percent
	state.damage_applied = state.rolls[1] < state.damage_percent
	record.phase = "SETTLED"
	record.closed_day = day
	bucket.command_sequence += 1
	record.command_sequence = bucket.command_sequence
	candidate.items_by_uid[record.item_uid] = _result_item(record)
	bucket.history.append(record.duplicate(true))
	bucket.active_order = {}
	if candidate.active_run.get("selected_item_uid", "").is_empty():
		candidate.active_run.selected_item_uid = personal_selection_uid(candidate, record.item_uid)
	return {"status":"APPLIED"}

static func report(record: Dictionary) -> String:
	if record.get("phase", "") not in ["IN_TRANSIT", "SETTLED"]: return ""
	var state = record.settlement
	var item = load("res://scripts/vertical_slice/domain/vs_item.gd").from_dict(state.item_snapshot)
	var title = "고객 검수·반환" if state.report_kind == "BASIC_CUSTOMER_CHECK" else "전선 엄호"
	var lines = PackedStringArray(["%s · %s" % [record.order_id, title],
		"출발 작품 %s +%d · UID %s" % [Equipment.by_item(item).display_name_ko, item.enhancement_level, item.uid],
		"%d일 인계 → %d일 보고 · %s" % [state.handed_off_day, state.due_day, "판매 · 고객 소유 유지" if record.ownership_mode == "SALE" else "대여 · 같은 작품 반환"],
		"성공 %.1f%% / 손상 %.1f%% · 독립 판정 (시험값)" % [state.success_percent, state.damage_percent],
		"인계 보수 지급 완료: 400골드 + 보강재 2 + %s 1 · 결과 추가 보수 0" % ("불의 심장" if state.payout.catalyst_id == "heart_of_flame" else "대지의 결정")])
	if record.phase == "IN_TRANSIT": lines.append("운송·사용 중 · 작품 편집 잠금 / 마감으로 날짜 진행")
	else:
		lines.append("%s %s · 손상 %s" % ["검수" if state.report_kind == "BASIC_CUSTOMER_CHECK" else "임무", "성공" if state.mission_success else "실패", "발생" if state.damage_applied else "없음"])
		lines.append("출발 내구도 %d → 결과 %d / 한계 %d" % [item.current_durability, item.current_durability - (1 if state.damage_applied else 0), item.max_durability])
	return "\n".join(lines)

static func _empty_bucket() -> Dictionary:
	return {"schema_version":1, "command_sequence":0, "active_order":{}, "history":[]}

static func _whole(value) -> bool:
	return typeof(value) in [TYPE_INT, TYPE_FLOAT] and is_finite(float(value)) and abs(float(value)) <= MAX_SAFE_INTEGER and float(value) == floor(float(value))

static func _fields(value, keys: Array) -> bool:
	return value is Dictionary and value.size() == keys.size() and value.has_all(keys)

static func _mode_allowed(funding: String, ownership: String) -> bool:
	return (funding == "COMMISSION_ESCROW" and ownership == "SALE") or (funding == "PLAYER" and ownership in ["SALE", "LOAN"])

static func _hash_valid(value: String) -> bool:
	if value.length() != 64: return false
	for character in value:
		if character not in "0123456789abcdef": return false
	return true

static func _pending(envelope, uid: String) -> bool:
	return load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").pending_trial(envelope, uid)

func _current(envelope, save):
	if envelope == null or save == null or not save.has_method("load_envelope") or not save.has_method("save_envelope"):
		return null
	if envelope.recovered_from_backup or not envelope.validation_errors.is_empty(): return null
	var verified = load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").from_dict(envelope.to_dict())
	if not verified.validation_errors.is_empty(): return null
	var current = save.load_envelope()
	if current == null or current.recovered_from_backup or not current.validation_errors.is_empty(): return null
	if current.active_run.get("run_id", "") != envelope.active_run.get("run_id", "") or current.active_run.get("tag_ruleset_id", "") != RULESET:
		return null
	# Duplicate through the complete parser: failed commands never mutate the supplied source.
	current = load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").from_dict(current.to_dict())
	return current if current.validation_errors.is_empty() else null

func _fingerprint(envelope) -> String:
	# JSON round trip normalizes integer/float values exactly like serialized_equal.
	return JSON.stringify(JSON.parse_string(JSON.stringify(envelope.to_dict()))).sha256_text()

func _same(a, b) -> bool:
	return load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").serialized_equal(a.to_dict(), b.to_dict())

func _commit(candidate, save, source) -> Dictionary:
	var verified = load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").from_dict(candidate.to_dict())
	if not verified.validation_errors.is_empty(): return _blocked("INVALID_CANDIDATE")
	if save.save_envelope(verified) != OK:
		var after_error = save.load_envelope()
		if after_error != null and not after_error.recovered_from_backup and after_error.validation_errors.is_empty() and _same(source, after_error):
			return _blocked("SAVE_FAILED_UNCHANGED")
		return {"status":"COMMIT_UNCERTAIN", "reason":"SAVE_ERROR_STATE_UNKNOWN"}
	var actual = save.load_envelope()
	if actual == null or actual.recovered_from_backup or not actual.validation_errors.is_empty():
		return {"status":"COMMIT_UNCERTAIN", "reason":"READBACK_UNAVAILABLE"}
	var parsed = load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").from_dict(actual.to_dict())
	if not parsed.validation_errors.is_empty() or not _same(verified, parsed):
		return {"status":"COMMIT_UNCERTAIN", "reason":"READBACK_MISMATCH"}
	return {"status":"APPLIED", "envelope":parsed}

func _already(envelope) -> Dictionary:
	return {"status":"ALREADY_APPLIED", "envelope":envelope}

func _blocked(reason: String) -> Dictionary:
	return {"status":"BLOCKED", "reason":reason}
