# 구형 제작 완성도를 현재 첫 작품 생성 입력으로 경계 변환한다.
class_name CanonicalFirstItemInputAdapter
extends RefCounted

const LEGACY_TO_CURRENT := {
	"APPRENTICE": {"crafting_grade": "CRAFT_NORMAL", "artistry": 1},
	"STANDARD": {"crafting_grade": "CRAFT_SUPERIOR", "artistry": 3},
	"REFINED": {"crafting_grade": "CRAFT_FINE", "artistry": 5},
	"MASTERWORK": {"crafting_grade": "CRAFT_MASTERWORK", "artistry": 7},
	"PERFECT": {"crafting_grade": "CRAFT_LEGENDARY", "artistry": 10},
}
const COMPLETION_TO_LEGACY_GRADE := {
	"STANDARD": "APPRENTICE",
	"GOOD": "STANDARD",
	"PERFECT": "REFINED",
}
const EquipmentCatalogScript = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")


func to_canonical_input(legacy_forge_result: Dictionary) -> Dictionary:
	if str(legacy_forge_result.get("weapon_id", "")) != "iron_sword":
		return _blocked("UNSUPPORTED_LEGACY_FORGE_RESULT")
	if int(legacy_forge_result.get("base_attack", 0)) < 1:
		return _blocked("INVALID_LEGACY_BASE_ATTACK")
	var legacy_grade_id := str(legacy_forge_result.get("craftsmanship_grade_id", ""))
	if not LEGACY_TO_CURRENT.has(legacy_grade_id):
		return _blocked("UNSUPPORTED_LEGACY_CRAFTSMANSHIP_GRADE")
	var mapped: Dictionary = LEGACY_TO_CURRENT[legacy_grade_id]
	var equipment: Dictionary = EquipmentCatalogScript.by_id("iron_sword")
	return {
		"status": "READY",
		"equipment_id": "iron_sword",
		"equipment_name": str(equipment.get("display_name_ko", "철검")),
		"equipment_group": str(equipment.get("equipment_group", "SWORD")),
		"role_profile": str(equipment.get("role_profile", "PHYSICAL_WEAPON_ATTACK")),
		"base_attack": int(legacy_forge_result.get("base_attack", 0)),
		"crafting_grade": str(mapped["crafting_grade"]),
		"artistry": int(mapped["artistry"]),
	}


func to_canonical_input_from_completion(completed_forge_result: Dictionary) -> Dictionary:
	var legacy_grade_id := str(COMPLETION_TO_LEGACY_GRADE.get(
		str(completed_forge_result.get("quality_id", "")),
		""
	))
	if not LEGACY_TO_CURRENT.has(legacy_grade_id):
		return _blocked("UNSUPPORTED_LEGACY_CRAFTSMANSHIP_GRADE")
	var equipment_id := str(completed_forge_result.get("equipment_id", completed_forge_result.get("weapon_id", "")))
	var equipment: Dictionary = EquipmentCatalogScript.by_id(equipment_id)
	if equipment.is_empty():
		return _blocked("UNSUPPORTED_COMPLETED_EQUIPMENT")
	if int(completed_forge_result.get("base_attack", 0)) < 1:
		return _blocked("INVALID_LEGACY_BASE_ATTACK")
	var mapped: Dictionary = LEGACY_TO_CURRENT[legacy_grade_id]
	return {
		"status": "READY",
		"equipment_id": equipment_id,
		"equipment_name": str(equipment.get("display_name_ko", "")),
		"equipment_group": str(equipment.get("equipment_group", "")),
		"role_profile": str(equipment.get("role_profile", "")),
		"base_attack": int(completed_forge_result.get("base_attack", 0)),
		"crafting_grade": str(mapped["crafting_grade"]),
		"artistry": int(mapped["artistry"]),
		"tap_count": maxi(int(completed_forge_result.get("tap_count", 0)), 0),
		"fever_activation_count": maxi(int(completed_forge_result.get("fever_activation_count", 0)), 0),
		"fever_bonus_applied": bool(completed_forge_result.get("fever_bonus_applied", false)),
	}


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
