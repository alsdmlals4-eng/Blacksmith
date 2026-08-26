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


func to_canonical_input(legacy_forge_result: Dictionary) -> Dictionary:
	if str(legacy_forge_result.get("weapon_id", "")) != "iron_sword":
		return _blocked("UNSUPPORTED_LEGACY_FORGE_RESULT")
	if int(legacy_forge_result.get("base_attack", 0)) < 1:
		return _blocked("INVALID_LEGACY_BASE_ATTACK")
	var legacy_grade_id := str(legacy_forge_result.get("craftsmanship_grade_id", ""))
	if not LEGACY_TO_CURRENT.has(legacy_grade_id):
		return _blocked("UNSUPPORTED_LEGACY_CRAFTSMANSHIP_GRADE")
	var mapped: Dictionary = LEGACY_TO_CURRENT[legacy_grade_id]
	return {
		"status": "READY",
		"weapon_id": "iron_sword",
		"base_attack": int(legacy_forge_result.get("base_attack", 0)),
		"crafting_grade": str(mapped["crafting_grade"]),
		"artistry": int(mapped["artistry"]),
	}


func to_canonical_input_from_completion(completed_forge_result: Dictionary) -> Dictionary:
	var legacy_grade_id := str(COMPLETION_TO_LEGACY_GRADE.get(
		str(completed_forge_result.get("quality_id", "")),
		""
	))
	var canonical_input := to_canonical_input({
		"weapon_id": str(completed_forge_result.get("weapon_id", "")),
		"base_attack": int(completed_forge_result.get("base_attack", 0)),
		"craftsmanship_grade_id": legacy_grade_id,
	})
	if str(canonical_input.get("status", "")) != "READY":
		return canonical_input
	canonical_input["tap_count"] = maxi(int(completed_forge_result.get("tap_count", 0)), 0)
	canonical_input["fever_activation_count"] = maxi(int(completed_forge_result.get("fever_activation_count", 0)), 0)
	canonical_input["fever_bonus_applied"] = bool(completed_forge_result.get("fever_bonus_applied", false))
	return canonical_input


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
