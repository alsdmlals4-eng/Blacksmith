# 제작 완료 결과를 현재 정본 작품으로 1회 확정하고 선택 상태에 기록한다.
class_name VSItemBirthService
extends RefCounted

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const LedgerEntryScript = preload("res://scripts/vertical_slice/domain/vs_ledger_entry.gd")
const UidServiceScript = preload("res://scripts/vertical_slice/services/vs_uid_service.gd")

const SOURCE_CANON_ID := "BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825"

var _uid_service


func _init(uid_service = null) -> void:
	_uid_service = uid_service if uid_service != null else UidServiceScript.new()


func commit_first_forge(envelope, forging_result: Dictionary) -> Dictionary:
	if envelope == null or not envelope.validation_errors.is_empty():
		return _blocked("INVALID_ENVELOPE")
	if not envelope.items_by_uid.is_empty() or not str(envelope.active_run.get("selected_item_uid", "")).is_empty():
		return _blocked("FIRST_ITEM_ALREADY_CREATED")
	if not _is_valid_forging_result(forging_result):
		return _blocked("INVALID_FORGE_RESULT")

	var item_uid := str(_uid_service.create_uid(envelope.items_by_uid))
	if item_uid.is_empty():
		return _blocked("UID_GENERATION_FAILED")

	var item = ItemScript.new()
	item.uid = item_uid
	item.birth_rng_seed = _create_birth_rng_seed()
	item.primary_material_id = "iron"
	item.equipment_group = "SWORD"
	item.role_profile = "PHYSICAL_WEAPON_ATTACK"
	item.crafting_grade = str(forging_result.get("crafting_grade", ""))
	item.artistry = int(forging_result.get("artistry", -1))
	item.raw_role_stat = int(forging_result.get("base_attack", 0))
	item.weight_point = 15
	item.function_capacity = 0
	item.functions.clear()
	item.grade_affix = ""
	item.catalyst_affix = ""
	item.chronicle_affix = ""
	item.owner_id = "PLAYER"
	var birth_entry = LedgerEntryScript.create(
		1,
		"birth:%s" % item_uid,
		"ITEM_BORN",
		SOURCE_CANON_ID,
		"",
		"BORN:%s" % item_uid,
		int(envelope.active_run.get("current_day", 1)),
		{
			"weapon_id": str(forging_result.get("weapon_id", "")),
			"crafting_grade": item.crafting_grade,
			"tap_count": int(forging_result.get("tap_count", 0)),
			"fever_activation_count": int(forging_result.get("fever_activation_count", 0)),
			"fever_bonus_applied": bool(forging_result.get("fever_bonus_applied", false)),
		}
	)
	if item.append_ledger_entry(birth_entry.to_dict()) != OK:
		return _blocked("INVALID_BIRTH_LEDGER")
	item.validation_errors.clear()
	item = ItemScript.from_dict(item.to_dict())
	if not item.validation_errors.is_empty():
		return _blocked("INVALID_BORN_ITEM")
	if envelope.add_item(item) != OK:
		return _blocked("ITEM_PERSISTENCE_FAILED")
	envelope.active_run["selected_item_uid"] = item_uid
	return {"status": "APPLIED", "item_uid": item_uid, "item": item}


func _is_valid_forging_result(forging_result: Dictionary) -> bool:
	if str(forging_result.get("weapon_id", "")) != "iron_sword":
		return false
	if not ItemScript.CRAFTING_GRADES.has(str(forging_result.get("crafting_grade", ""))):
		return false
	return int(forging_result.get("base_attack", 0)) > 0 and int(forging_result.get("artistry", -1)) >= 0


func _create_birth_rng_seed() -> int:
	var seed_bytes := Crypto.new().generate_random_bytes(4)
	return int(seed_bytes.decode_u32(0)) if seed_bytes.size() == 4 else 0


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
