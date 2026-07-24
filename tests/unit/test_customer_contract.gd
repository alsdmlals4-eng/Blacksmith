extends SceneTree

const CustomerContractScript = preload("res://scripts/customers/customer_contract.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("CustomerContract tests PASSED (7 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	var contract = CustomerContractScript.new(_contract(), _activity(), 1)
	_test_plus4_rejected(contract)
	_test_plus5_allowed(contract)
	_test_plus10_stretch(contract)
	_test_preferred_affix(contract)
	_test_deadline_and_wrong_weapon(contract)
	_test_destroyed_rejected(contract)
	_test_reachable_scores(contract)


func _test_plus4_rejected(contract) -> void:
	var result: Dictionary = contract.can_deliver(_equipment(4, "REFINED"), 1)
	_expect(not bool(result.get("ok", true)), "+4 철검은 납품할 수 없어야 합니다.")
	_expect(Array(result.get("missing_conditions", [])).has(CustomerContractScript.STATUS_REQUIREMENT_NOT_MET), "+4는 요구 강화 미달이어야 합니다.")


func _test_plus5_allowed(contract) -> void:
	_expect(bool(contract.can_deliver(_equipment(5, "REFINED"), 1).get("ok", false)), "+5 철검은 납품 가능해야 합니다.")


func _test_plus10_stretch(contract) -> void:
	var fit: Dictionary = contract.evaluate_fit(_equipment(10, "REFINED"))
	_expect(int(fit.get("contributions", {}).get("stretch_level", 0)) == 15, "+10은 stretch 기여 15여야 합니다.")


func _test_preferred_affix(contract) -> void:
	var equipment := _equipment(10, "MASTERWORK")
	equipment["affixes"] = [{"id": "sharp", "tier": 1}]
	var fit: Dictionary = contract.evaluate_fit(equipment)
	_expect(int(fit.get("contributions", {}).get("preferred_affix", 0)) == 25, "선호 수식어는 25점이어야 합니다.")


func _test_deadline_and_wrong_weapon(contract) -> void:
	var expired: Dictionary = contract.can_deliver(_equipment(5, "REFINED"), 5)
	_expect(Array(expired.get("missing_conditions", [])).has(CustomerContractScript.STATUS_DEADLINE_EXPIRED), "기한 초과를 거부해야 합니다.")
	var wrong := _equipment(5, "REFINED")
	wrong["weapon_id"] = "iron_axe"
	_expect(Array(contract.can_deliver(wrong, 1).get("missing_conditions", [])).has(CustomerContractScript.STATUS_WRONG_EQUIPMENT), "다른 무기는 거부해야 합니다.")


func _test_destroyed_rejected(contract) -> void:
	var destroyed := _equipment(5, "REFINED")
	destroyed["destroyed"] = true
	_expect(Array(contract.can_deliver(destroyed, 1).get("missing_conditions", [])).has(CustomerContractScript.STATUS_DESTROYED), "파괴 장비는 거부해야 합니다.")


func _test_reachable_scores(contract) -> void:
	var apprentice: Dictionary = contract.evaluate_fit(_equipment(5, "APPRENTICE"))
	_expect(apprentice.get("score") == 30 and apprentice.get("band_id") == "DEFEAT", "미숙한 +5는 30점 DEFEAT여야 합니다.")
	var refined: Dictionary = contract.evaluate_fit(_equipment(5, "REFINED"))
	_expect(refined.get("score") == 40 and refined.get("band_id") == "WIN", "정교한 +5는 40점 WIN이어야 합니다.")
	var masterwork := _equipment(10, "MASTERWORK")
	masterwork["affixes"] = [{"id": "flaming", "tier": 1}]
	var decisive: Dictionary = contract.evaluate_fit(masterwork)
	_expect(decisive.get("score") == 85 and decisive.get("band_id") == "DECISIVE_WIN", "명품 +10 선호 수식어는 85점 DECISIVE_WIN이어야 합니다.")


func _equipment(level: int, grade_id: String) -> Dictionary:
	return {
		"record_schema_version": 1,
		"weapon_id": "iron_sword",
		"enhancement_level": level,
		"craftsmanship_grade_id": grade_id,
		"base_attack": 20,
		"progression_attack": 20,
		"affixes": [],
		"destroyed": false,
	}


func _contract() -> Dictionary:
	return {
		"equipment_id": "iron_sword",
		"required_level": 5,
		"stretch_level": 10,
		"preferred_affix_ids": ["sharp", "flaming"],
		"deadline_days": 3,
	}


func _activity() -> Dictionary:
	return {
		"score_weights": {"required_level": 20, "stretch_level": 15, "preferred_affix": 25, "attack_threshold": 20, "attack": 10},
		"grade_scores": {"APPRENTICE": 0, "STANDARD": 5, "REFINED": 10, "MASTERWORK": 15, "PERFECT": 20},
		"result_bands": [
			{"id": "DEFEAT", "minimum_score": 0},
			{"id": "WIN", "minimum_score": 35},
			{"id": "DECISIVE_WIN", "minimum_score": 70},
		],
	}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
