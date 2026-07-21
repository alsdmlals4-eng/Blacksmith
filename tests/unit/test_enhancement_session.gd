extends SceneTree

const EnhancementSessionScript = preload("res://scripts/enhancement/enhancement_session.gd")

var failures: Array[String] = []
var base_config: Dictionary
var materials: Array
var affixes: Array
var milestones: Array


func _initialize() -> void:
	base_config = _read_json("res://data/crafting/enhancement_balance.json")
	materials = _read_json("res://data/crafting/materials.json").get("materials", [])
	affixes = _read_json("res://data/crafting/affixes.json").get("affixes", [])
	milestones = _read_json("res://data/crafting/enhancement_milestones.json").get("milestones", [])
	_run_tests()
	if failures.is_empty():
		print("EnhancementSession tests PASSED (12 cases)")
		quit(0)
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_normal_and_special_rules()
	_test_progressive_growth()
	_test_cost_and_price_acceleration()
	_test_catalyst_price_and_value()
	_test_safe_hold_and_pity()
	_test_downgrade()
	_test_destruction()
	_test_safeguard()
	_test_overdrive_leaps_two_levels()
	_test_overdrive_is_blocked_near_special()
	_test_level_ten_affix()
	_test_level_one_hundred()


func _new_session(overrides: Dictionary = {}):
	var config := base_config.duplicate(true)
	config["milestones"] = milestones.duplicate(true)
	for key_value in overrides:
		var key := str(key_value)
		if config.get(key) is Dictionary and overrides[key_value] is Dictionary:
			var nested: Dictionary = config[key]
			for nested_key in overrides[key_value]:
				nested[nested_key] = overrides[key_value][nested_key]
		else:
			config[key] = overrides[key_value]
	return EnhancementSessionScript.new(
		config,
		materials,
		affixes,
		{"weapon_id": "iron_sword", "weapon_name": "철검", "base_attack": 10}
	)


func _test_normal_and_special_rules() -> void:
	var session = _new_session()
	_expect(not session.uses_materials_for_level(9), "+9는 일반 강화여야 합니다.")
	_expect(not session.requires_precision_for_level(9), "+9는 원클릭이어야 합니다.")
	_expect(session.uses_materials_for_level(10), "+10은 특수 강화여야 합니다.")
	_expect(session.requires_precision_for_level(10), "+10은 정밀 판정이어야 합니다.")


func _test_progressive_growth() -> void:
	var session = _new_session({"base_success_by_target_level": _rates(100, 1.0)})
	var first_gain := int(session.get_next_preview().get("growth_gain", 0))
	_advance_to(session, 50)
	var later_gain := int(session.get_next_preview().get("growth_gain", 0))
	_expect(later_gain > first_gain, "총 공격력과 단계가 높아질수록 다음 강화 효과가 커져야 합니다.")
	_expect(int(session.progression_attack) > 60, "공격력은 단순 고정 덧셈보다 빠르게 성장해야 합니다.")


func _test_cost_and_price_acceleration() -> void:
	var session = _new_session({"base_success_by_target_level": _rates(100, 1.0)})
	var early_cost := session.calculate_attempt_cost()
	var early_price := session.get_current_sale_price()
	_advance_to(session, 40)
	_expect(session.calculate_attempt_cost() > early_cost * 20, "고단계 강화 비용이 가속되어야 합니다.")
	_expect(session.get_current_sale_price() > early_price * 5, "고단계 무기 가격이 가속되어야 합니다.")


func _test_catalyst_price_and_value() -> void:
	var session = _new_session({"base_success_by_target_level": _rates(100, 1.0)})
	_advance_to(session, 9)
	var plain_cost := session.calculate_attempt_cost()
	_expect(session.set_catalyst_material("salamander_core"), "+10에서 촉매를 선택할 수 있어야 합니다.")
	var preview: Dictionary = session.get_next_preview()
	_expect(session.calculate_attempt_cost() >= plain_cost + 120, "촉매 가격이 시도 비용에 포함되어야 합니다.")
	_expect(float(preview.get("value_bonus", 0.0)) >= 0.20, "촉매 가치 보너스가 성공 미리보기에 포함되어야 합니다.")
	_expect(int(preview.get("sale_price", 0)) > session.get_current_sale_price(), "촉매 적용 예상 판매가가 증가해야 합니다.")


func _test_safe_hold_and_pity() -> void:
	var session = _new_session({"base_success_by_target_level": {"1": 0.50}})
	session.begin_attempt(0.90)
	_expect(str(session.last_attempt.get("outcome", "")) == "HOLD", "+10 이하 실패는 단계 유지여야 합니다.")
	_expect(session.enhancement_level == 0, "안전 구간에서 단계가 내려가면 안 됩니다.")
	_expect(session.failure_streak == 1, "실패 횟수가 누적되어야 합니다.")
	_expect(is_equal_approx(session.calculate_success_chance(), 0.54), "실패 후 성공률 보정이 적용되어야 합니다.")


func _test_downgrade() -> void:
	var rates := _rates(10, 1.0)
	rates["11"] = 0.0
	var session = _new_session({
		"base_success_by_target_level": rates,
		"risk": {
			"downgrade_ratio_by_decade": {"1": 1.0},
			"destroy_ratio_by_decade": {"1": 0.0},
			"downgrade_steps_by_decade": {"1": 1},
		},
	})
	_advance_to(session, 10)
	session.begin_attempt(0.50)
	_expect(str(session.last_attempt.get("outcome", "")) == "DOWNGRADE", "+11부터 단계 하락이 가능해야 합니다.")
	_expect(session.enhancement_level == 9, "단계 하락 결과가 실제 단계에 반영되어야 합니다.")


func _test_destruction() -> void:
	var rates := _rates(29, 1.0)
	rates["30"] = 0.0
	var session = _new_session({"base_success_by_target_level": rates})
	_advance_to(session, 29)
	session.begin_attempt(0.0)
	session.precision_position = 0.0
	session.finish_precision()
	_expect(str(session.last_attempt.get("outcome", "")) == "DESTROY", "+30부터 무기 파괴가 가능해야 합니다.")
	_expect(session.destroyed, "파괴 결과가 무기 상태에 기록되어야 합니다.")
	_expect(session.state == EnhancementSessionScript.State.COMPLETE, "파괴 시 강화 세션이 종료되어야 합니다.")


func _test_safeguard() -> void:
	var rates := _rates(29, 1.0)
	rates["30"] = 0.0
	var session = _new_session({"base_success_by_target_level": rates})
	_advance_to(session, 29)
	session.set_skill("safeguard")
	session.set_catalyst_material("guardian_powder")
	var risk: Dictionary = session.calculate_outcome_probabilities()
	_expect(float(risk.get("destroy", 1.0)) == 0.0, "안정 단조와 수호 가루 선택 시 파괴 확률이 0%여야 합니다.")
	session.begin_attempt(0.50)
	session.precision_position = 0.0
	session.finish_precision()
	_expect(not session.destroyed, "보호 선택 시 무기가 파괴되면 안 됩니다.")


func _test_overdrive_leaps_two_levels() -> void:
	var session = _new_session({"base_success_by_target_level": _rates(100, 1.0)})
	_advance_to(session, 5)
	_expect(session.set_skill("overdrive"), "+5에서는 폭주 단조를 선택할 수 있어야 합니다.")
	var preview: Dictionary = session.get_next_preview()
	_expect(is_equal_approx(float(preview.get("leap_chance", 0.0)), 0.08), "폭주 도약 확률은 8%여야 합니다.")
	session.begin_attempt(0.0, 0.0)
	_expect(bool(session.last_attempt.get("leap_triggered", false)), "폭주 도약 판정이 성공해야 합니다.")
	_expect(int(session.last_attempt.get("levels_gained", 0)) == 2, "폭주 도약 성공 시 총 2단계 상승해야 합니다.")
	_expect(session.enhancement_level == 7, "+5에서 폭주 도약 성공 시 +7이 되어야 합니다.")


func _test_overdrive_is_blocked_near_special() -> void:
	var session = _new_session({"base_success_by_target_level": _rates(100, 1.0)})
	_advance_to(session, 28)
	_expect(not session.can_use_skill_for_level("overdrive", 29), "+28에서는 폭주 도약이 +30 특수 강화를 건너뛸 수 있어 사용 불가여야 합니다.")
	_advance_to(session, 29)
	_expect(not session.set_skill("overdrive"), "+29에서는 다음 +30 특수 강화 때문에 폭주 단조를 사용할 수 없어야 합니다.")
	_expect(not session.can_use_skill_for_level("overdrive", 30), "특수 강화 자체에서도 폭주 단조를 사용할 수 없어야 합니다.")


func _test_level_ten_affix() -> void:
	var session = _new_session({"base_success_by_target_level": _rates(100, 1.0)})
	_advance_to(session, 9)
	session.set_secondary_material("flame_stone")
	_advance_to(session, 10)
	_expect(session.affixes.size() == 1, "+10에서 첫 수식어가 추가되어야 합니다.")
	_expect(str(session.affixes[0].get("id", "")) == "flaming", "화염석 선택 시 불타는 수식어가 붙어야 합니다.")


func _test_level_one_hundred() -> void:
	var session = _new_session({"base_success_by_target_level": _rates(100, 1.0)})
	var selections := {10: "flame_stone", 30: "whetstone", 50: "spirit_heart"}
	while session.enhancement_level < 100:
		var target := int(session.enhancement_level) + 1
		if selections.has(target):
			session.set_secondary_material(str(selections[target]))
		session.begin_attempt(0.0)
		if session.state == EnhancementSessionScript.State.PRECISION:
			session.precision_position = float(session.config["precision"]["target"])
			session.finish_precision()
	_expect(session.enhancement_level == 100, "최대 강화는 +100이어야 합니다.")
	_expect(session.affixes.size() == 3, "+100에는 세 수식어가 있어야 합니다.")
	for value in session.affixes:
		var affix: Dictionary = value
		_expect(int(affix.get("tier", 0)) == 4, "+100에서 모든 수식어가 4티어여야 합니다.")


func _advance_to(session, target_level: int) -> void:
	while session.enhancement_level < target_level and not session.destroyed:
		session.begin_attempt(0.0, 1.0)
		if session.state == EnhancementSessionScript.State.PRECISION:
			session.precision_position = float(session.config["precision"]["target"])
			session.finish_precision()


func _rates(max_level: int, value: float) -> Dictionary:
	var result := {}
	for level in range(1, max_level + 1):
		result[str(level)] = value
	return result


func _read_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		failures.append("%s 파일을 읽지 못했습니다." % path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
