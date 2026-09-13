extends RefCounted

# Immutable compatibility policy for Blueprint39's controlled economy trial.
const POLICY = "CATALYST_EXCHANGE_TRIAL_V1"
const RULESET = "BLACKSMITH_REPLAN_TAGS_20260912"
const COST = 1000
const MAX_EXACT = 9007199254740991
const CATALYSTS = {"heart_of_flame":"불의 심장","earth_crystal":"대지의 결정"}

static func _whole(value) -> bool:
	return (value is int or value is float) and is_finite(float(value)) and value >= 0 and value <= MAX_EXACT and float(value) == floor(float(value))

static func validate(envelope) -> String:
	if not envelope.active_run.has("catalyst_exchange"): return ""
	var receipt = envelope.active_run.catalyst_exchange
	if not receipt is Dictionary or receipt.size() != 5 or not receipt.has_all(["schema_version","policy_id","sequence","catalyst","day"]):
		return "INVALID_EXCHANGE_RECEIPT"
	if not _whole(receipt.schema_version) or receipt.schema_version != 1 or receipt.policy_id != POLICY:
		return "INVALID_EXCHANGE_POLICY"
	if envelope.active_run.get("tag_ruleset_id","") != RULESET or not receipt.catalyst is String or not CATALYSTS.has(receipt.catalyst):
		return "INVALID_EXCHANGE_RULESET_OR_CATALYST"
	if not _whole(receipt.sequence) or receipt.sequence < 1 or not _whole(receipt.day) or receipt.day < 1 or receipt.day > envelope.active_run.current_day:
		return "INVALID_EXCHANGE_SEQUENCE_OR_DAY"
	return ""

static func quote(envelope,catalyst: String) -> Dictionary:
	if envelope == null or not envelope.validation_errors.is_empty() or envelope.active_run.get("tag_ruleset_id","") != RULESET or not validate(envelope).is_empty():
		return _blocked("INVALID_CAMPAIGN")
	if not CATALYSTS.has(catalyst): return _blocked("INVALID_CATALYST")
	var sequence = envelope.active_run.get("catalyst_exchange",{}).get("sequence",0)
	var stock = envelope.workshop_resources.material_stock.get(catalyst,0)
	var gold = envelope.workshop_resources.gold
	if not _whole(sequence) or sequence >= MAX_EXACT or not _whole(stock) or stock >= MAX_EXACT or not _whole(gold):
		return _blocked("UNSAFE_RESOURCE_OR_SEQUENCE")
	if gold < COST: return _blocked("INSUFFICIENT_GOLD")
	return {"status":"READY","sequence":int(sequence)+1,"cost":COST,"stock":int(stock),"catalyst":catalyst}

func purchase(envelope,catalyst: String,sequence,save) -> Dictionary:
	if not _whole(sequence) or sequence < 1 or not CATALYSTS.has(catalyst):
		return _blocked("INVALID_REQUEST")
	if envelope == null or save == null or not envelope.validation_errors.is_empty() or not save.has_method("load_envelope") or not save.has_method("save_envelope"):
		return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	var current = save.load_envelope()
	if current == null or not current.validation_errors.is_empty() or current.recovered_from_backup:
		return _blocked("INVALID_OR_UNAVAILABLE_SAVE")
	if current.active_run.get("run_id","") != envelope.active_run.get("run_id","") or current.active_run.get("tag_ruleset_id","") != RULESET or envelope.active_run.get("tag_ruleset_id","") != RULESET:
		return _blocked("INVALID_CAMPAIGN")
	var receipt = current.active_run.get("catalyst_exchange",{})
	if sequence == receipt.get("sequence",0) and catalyst == receipt.get("catalyst",""):
		return {"status":"ALREADY_APPLIED","envelope":current}
	if not _same(current,envelope): return _blocked("STALE_SOURCE")
	var offer = quote(current,catalyst)
	if offer.status != "READY": return offer
	if sequence != offer.sequence: return _blocked("STALE_SEQUENCE")
	current.workshop_resources.gold -= COST
	current.workshop_resources.material_stock[catalyst] = offer.stock+1
	current.active_run["catalyst_exchange"] = {"schema_version":1,"policy_id":POLICY,"sequence":int(sequence),"catalyst":catalyst,"day":int(current.active_run.current_day)}
	var checked = load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").from_dict(current.to_dict())
	if not checked.validation_errors.is_empty(): return _blocked("INVALID_CANDIDATE")
	if save.save_envelope(checked) != OK: return _blocked("SAVE_FAILED")
	var actual = save.load_envelope()
	if actual == null or not actual.validation_errors.is_empty() or actual.recovered_from_backup or not _same(actual,checked):
		return _blocked("READBACK_FAILED")
	return {"status":"APPLIED","envelope":actual}

static func _same(a,b) -> bool:
	return load("res://scripts/vertical_slice/domain/vs_save_envelope.gd").serialized_equal(a.to_dict(),b.to_dict())

static func _blocked(reason: String) -> Dictionary:
	return {"status":"BLOCKED","reason":reason}
