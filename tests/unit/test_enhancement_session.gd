extends SceneTree

const EnhancementSessionScript = preload("res://scripts/enhancement/enhancement_session.gd")

var failures: Array[String] = []
var materials: Array = [
	{"id": "whetstone", "name": "숫돌", "slot_types": ["secondary"], "affix_tags": ["sharp"], "price": 25},
	{"id": "flame_stone", "name": "화염석", "slot_types": ["secondary"], "affix_tags": ["fire"], "price": 40},
	{"id": "spirit_heart", "name": "정령의 심장", "slot_types": ["secondary"], "affix_tags": ["spirit"], "price": 65},
	{
		"id": "salamander_core",
		"name": "살라맨더의 핵",
		"slot_types": ["catalyst"],
		"affix_tags": ["fire"],
		"success_bonus": 0.15,
		"growth_multiplier": 1.05,
		"sale_value_bonus": 0.20,
		"downgrade_multiplier": 1.0,
		"destroy_multiplier": 1.0,
		"price": 120,
	},
	{
		"id": "guardian_powder",
		"name": "수호 가루",
		"slot_types": ["catalyst"],
		"affix_tags": [],
		"success_bonus": 0.05,
		"growth_multiplier": 0.95,
		"sale_value_bonus": 0.05,
		"downgrade_multiplier": 0.5,
		"destroy_multiplier": 0.0,
		"price": 180,
	},
	{
		"id": "berserker_ember",
		"name": "폭주의 불씨",
		"slot_types": ["catalyst"],
		"affix_tags": ["fire"],
		"success_bonus": 0.08,
		"growth_multiplier": 1.25,
		"sale_value_bonus": 0.30,
		"downgrade_multiplier": 1.2,
		"destroy_multiplier": 1.75,
		"price": 90,
	},
]
var affixes: Array = [
	{
		"id": "sharp",
		"name": "날카로운",
		"material_tags": ["sharp"],
		"tiers": {
			"1": {"attack_percent": 0.08},
			"2": {"attack_percent": 0.16},
			"3": {"attack_percent": 0.26},
			"4": {"attack_percent": 0.40},
		},
	},
	{
		"id": "flaming",
		"name": "불타는",
		"material_tags": ["fire"],
		"tiers": {
			"1": {"fire_damage": 5},
			"2": {"fire_damage": 12},
			"3": {"fire_damage": 24},
			"4": {"fire_damage": 42},
		},
	},
	{
		"id": "spirit_bound",
		"name": "정령이 깃든",
		"material_tags": ["spirit"],
		"tiers": {
			"1": {"special_trigger_chance": 0.05},
			"2": {"special_trigger_chance": 0.12},
			"3": {"special_trigger_chance": 0.20},
			"4": {"special_trigger_chance": 0.30},
		},
	},
]
var milestones: Array = [
	{"level": 10, "effect": "ADD_AFFIX", "slot": 1},
	{"level": 20, "effect": "UPGRADE_AFFIX", "slot": 1, "tier_delta": 1},
	{"level": 30, "effect": "ADD_AFFIX", "slot": 2},
	{"level": 40, "effect": "UPGRADE_AFFIX", "slot": 2, "tier_delta": 1},
	{"level": 50, "effect": "ADD_AFFIX", "slot": 3},
	{"level": 60, "effect": "UPGRADE_AFFIX", "slot": 3, "tier_delta": 1},
	{"level": 70, "effect": "UPGRADE_AFFIX", "slot": 1, "tier_delta": 1},
	{"level": 80, "effect": "UPGRADE_AFFIX", "slot": 2, "tier_delta": 1},
	{"level": 90, "effect": "UPGRADE_AFFIX", "slot": 3, "tier_delta": 1},
	{"level": 100, "effect": "ASCEND_ALL", "tier_delta": 1},
]


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("EnhancementSession tests PASSED (11 cases)")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)


func _run_tests() -> void:
	_test_normal_and_special_screen_rules()
	_test_progressive_growth_accelerates()
	_test_attempt_cost_and_sale_price_accelerate()
	_test_catalyst_effect_and_price_are_in_preview()
	_test_safe_failure_holds_and_adds_pity()
	_test_high_level_failure_can_downgrade()
	_test_high_level_failure_can_destroy()
	_test_safeguard_blocks_destruction()
	_test_overdrive_increases_reward_and_risk()
	_test_level_ten_adds_selected_affix()
	_test_level_one_hundred_completes_three_affixes()


func _base_config() -> Dictionary:
	return {
		"max_level": 100,
		"precision_interval": 10,
		"material_interval": 10,
		"milestones": milestones,
		"pity": {"bonus_per_failure": 0.04, "max_bonus": 0.24},
		"growth": {
			"base_attack": 10,
			"normal_rate": 0.08,
			"normal_rate_per_decade": 0.01,
			"special_rate": 0.20,
			"special_rate_per_decade": 0.02,
		},
		"economy": {
			"base_weapon_price": 100,
			"attack_price_scale": 12.0,
			"attack_price_exponent": 1.18,
			"level_price_scale": 4.0,
			"level_price_exponent": 1.65,
			"base_attempt_cost": 25,
			"attempt_cost_exponent": 1.55,
			"attempt_decade_multiplier": 0.22,
			"special_cost_multiplier": 2.4,
		},
		"risk": {
			"safe_until_level": 10,
			"destroy_start_level": 30,
			"special_downgrade_multiplier": 1.15,
			"special_destroy_multiplier": 1.25,
			"downgrade_ratio_by_decade": {
				"0": 0.0, "1": 0.25, "2": 0.35, "3": 0.45, "4": 0.50,
				"5": 0.55, "6": 0.60, "7": 0.65, "8": 0.70, "9": 0.75,
			},
			"destroy_ratio_by_decade": {
				"0": 0.0, "1": 0.0, "2": 0.0, "3": 0.03, "4": 0.05,
				"5": 0.07, "6": 0.09, "7": 0.12, "8": 0.15, "9": 0.20,
			},
			"downgrade_steps_by_decade": {
				"0": 0, "1": 1, "2": 1, "3": 2, "4": 2,
				"5": 2, "6": 3, "7": 3, "8": 4, "9": 5,
			},
		},
		"skills": {
			"balanced": {
				"name": "균형 단조", "description": "기본",
				"success_bonus": 0.0, "cost_multiplier": 1.0,
				"growth_multiplier": 1.0, "sale_value_bonus": 0.0,
				"downgrade_multiplier": 1.0, "destroy_multiplier": 1.0,
				"precision_bonus_multiplier": 1.0,
			},
			"safeguard": {
				"name": "안정 단조", "description": "보호",
				"success_bonus": 0.0, "cost_multiplier": 1.8,
				"growth_multiplier": 0.95, "sale_value_bonus": 0.0,
				"downgrade_multiplier": 0.5, "destroy_multiplier": 0.0,
				"precision_bonus_multiplier": 1.0,
			},
			"overdrive": {
				"name": "폭주 단조", "description": "위험",
				"success_bonus": 0.05, "cost_multiplier": 1.15,
				"growth_multiplier": 1.15, "sale_value_bonus": 0.12,
				"downgrade_multiplier": 1.2, "destroy_multiplier": 1.5,
				"precision_bonus_multiplier": 1.15,
			},
		},
	}


func _session(custom_config: Dictionary = {}):
	var merged := _base_config()
	for key_value in custom_config:
		if merged.get(key_value) is Dictionary and custom_config[key_value] is Dictionary:
			var nested: Dictionary = merged[key_value]
			for nested_key in custom_config[key_value]:
				nested[nested_key] = custom_config[key_value][nested_key]
		else:
			merged[key_value] = custom_config[key_value]
	return EnhancementSessionScript.new(
		merged,
		materials,
		affixes,
		{"weapon_id": "iron_sword", "weapon_name": "철검", "base_attack": 10}
	)


func _test_normal_and_special_screen_rules() -> void:
	var session = _session(_all_success_config())
	_expect(not session.uses_materials_for_level(9), "+9는 일반 강화여야 합니다.")
	_expect(not session.requires_precision_for_level(9), "+9는 원클릭이어야 합니다.")
	_expect(session.uses_materials_for_level(10), "+10은 재료를 사용하는 특수 강화여야 합니다.")
	_expect(session.requires_precision_for_level(10), "+10은 정밀 판정을 사용해야 합니다.")


func _test_progressive_growth_accelerates() -> void:
	var session = _session(_all_success_config())
	var first_gain := int(session.get_next_preview()["growth_gain"])
	_advance_to_level(session, 50)
	var later_gain := int(session.get_next_preview()["growth_gain"])
	_expect(later_gain > first_gain, "현재 총 공격력과 단계에 비례해 고단계 강화 증가량이 커져야 합니다.")
	_expect(int(session.progression_attack) > 10 + 50, "강화 공격력은 고정 덧셈보다 빠르게 성장해야 합니다.")


func _test_attempt_cost_and_sale_price_accelerate() -> void:
	var session = _session(_all_success_config())
	var first_cost := session.calculate_attempt_cost()
	var first_price := session.get_current_sale_price()
	_advance_to_level(session, 40)
	_expect(session.calculate_attempt_cost() > first_cost * 20, "고단계 강화 비용은 초반보다 크게 증가해야 합니다.")
	_expect(session.get_current_sale_price() > first_price * 5, "고단계 무기 가격은 초반보다 크게 증가해야 합니다.")


func _test_catalyst_effect_and_price_are_in_preview() -> void:
	var session = _session(_all_success_config())
	_advance_to_level(session, 9)
	var no_catalyst_cost := session.calculate_attempt_cost()
	_expect(session.set_catalyst_material("salamander_core"), "+10에서 촉매를 선택할 수 있어야 합니다.")
	var preview: Dictionary = session.get_next_preview()
	_expect(session.calculate_attempt_cost() > no_catalyst_cost, "촉매 가격이 특수 강화 비용에 포함되어야 합니다.")
	_expect(float(preview.get("value_bonus", 0.0)) >= 0.20, "살라맨더 촉매의 가치 보너스가 성공 미리보기에 포함되어야 합니다.")
	_expect(int(preview.get("sale_price", 0)) > session.get_current_sale_price(), "촉매 적용 후 예상 판매가가 표시 가능해야 합니다.")


func _test_safe_failure_holds_and_adds_pity() -> void:
	var session = _session({"base_success_by_target_level": {"1": 0.50}})
	session.begin_attempt(0.90)
	_expect(str(session.last_attempt.get("outcome", "")) == "HOLD", "+10 이하 실패는 단계 유지여야 합니다.")
	_expect(session.enhancement_level == 0, "안전 구간 실패 시 단계가 유지되어야 합니다.")
	_expect(session.failure_streak == 1, "실패 보정 횟수가 누적되어야 합니다.")
	_expect(is_equal_approx(session.calculate_success_chance(), 0.54), "실패 후 성공률에 4%p 보정이 적용되어야 합니다.")


func _test_high_level_failure_can_downgrade() -> void:
	var rates := _rates_until(10, 1.0)
	rates["11"] = 0.0
	var session = _session({
		"base_success_by_target_level": rates,
		"risk": {"downgrade_ratio_by_decade": {"1": 1.0}, "destroy_ratio_by_decade": {"1": 0.0}},
	})
	_advance_to_level(session, 10)
	session.begin_attempt(0.50)
	_expect(str(session.last_attempt.get("outcome", "")) == "DOWNGRADE", "+11 이상 실패에서 단계 하락 결과가 가능해야 합니다.")
	_expect(session.enhancement_level == 9, "단계 하락 시 설정된 단계만큼 내려가야 합니다.")


func _test_high_level_failure_can_destroy() -> void:
	var rates := _rates_until(29, 1.0)
	rates["30"] = 0.0
	var session = _session({
		"base_success_by_target_level": rates,
		"risk": {
			"destroy_ratio_by_decade": {"2": 1.0},
			"downgrade_ratio_by_decade": {"2": 0.0},
			"destroy_start_level": 30,
			"special_destroy_multiplier": 1.0,
		},
	})
	_advance_to_level(session, 29)
	session.begin_attempt(0.0)
	session.precision_position = 0.0
	session.finish_precision()
	_expect(str(session.last_attempt.get("outcome", "")) == "DESTROY", "+30 이상 실패에서 무기 파괴가 가능해야 합니다.")
	_expect(session.destroyed, "파괴 결과 후 무기 상태가 destroyed여야 합니다.")
	_expect(session.state == EnhancementSessionScript.State.COMPLETE, "무기 파괴 시 강화 세션이 종료되어야 합니다.")


func _test_safeguard_blocks_destruction() -> void:
	var rates := _rates_until(29, 1.0)
	rates["30"] = 0.0
	var session = _session({
		"base_success_by_target_level": rates,
		"risk": {
			"destroy_ratio_by_decade": {"2": 1.0},
			"downgrade_ratio_by_decade": {"2": 1.0},
			"destroy_start_level": 30,
			"special_destroy_multiplier": 1.0,
		},
	})
	_advance_to_level(session, 29)
	session.set_skill("safeguard")
	session.set_catalyst_material("guardian_powder")
	session.begin_attempt(0.50)
	session.precision_position = 0.0
	session.finish_precision()
	_expect(not session.destroyed, "안정 단조와 수호 촉매는 파괴를 막아야 합니다.")
	_expect(float(session.last_attempt.get("destroy_chance", 1.0)) == 0.0, "보호 선택 시 표시 파괴 확률도 0%여야 합니다.")


func _test_overdrive_increases_reward_and_risk() -> void:
	var rates := _rates_until(29, 1.0)
	rates["30"] = 0.30
	var balanced = _session({"base_success_by_target_level": rates})
	var overdrive = _session({"base_success_by_target_level": rates})
	_advance_to_level(balanced, 29)
	_advance_to_level(overdrive, 29)
	overdrive.set_skill("overdrive")
	var balanced_preview: Dictionary = balanced.get_next_preview()
	var overdrive_preview: Dictionary = overdrive.get_next_preview()
	var balanced_risk: Dictionary = balanced.calculate_outcome_probabilities()
	var overdrive_risk: Dictionary = overdrive.calculate_outcome_probabilities()
	_expect(int(overdrive_preview["growth_gain"]) > int(balanced_preview["growth_gain"]), "폭주 단조는 성공 시 공격력 증가량이 더 커야 합니다.")
	_expect(int(overdrive_preview["sale_price"]) > int(balanced_preview["sale_price"]), "폭주 단조는 성공 시 예상 판매가가 더 커야 합니다.")
	_expect(float(overdrive_risk["destroy"]) > float(balanced_risk["destroy"]), "폭주 단조는 파괴 위험도 더 커야 합니다.")


func _test_level_ten_adds_selected_affix() -> void:
	var session = _session(_all_success_config())
	_advance_to_level(session, 9)
	session.set_secondary_material("flame_stone")
	_advance_to_level(session, 10)
	_expect(session.affixes.size() == 1, "+10 특수 강화에서 첫 수식어가 추가되어야 합니다.")
	_expect(str(session.affixes[0]["id"]) == "flaming", "+10 화염석 선택 시 불타는 수식어가 붙어야 합니다.")


func _test_level_one_hundred_completes_three_affixes() -> void:
	var session = _session(_all_success_config())
	var material_by_level := {10: "flame_stone", 30: "whetstone", 50: "spirit_heart"}
	while session.enhancement_level < 100:
		var target_level: int = int(session.enhancement_level) + 1
		if session.uses_materials_for_level(target_level) and material_by_level.has(target_level):
			session.set_secondary_material(str(material_by_level[target_level]))
		session.begin_attempt(0.0)
		if session.state == EnhancementSessionScript.State.PRECISION:
			session.precision_position = float(session.config["precision"]["target"])
			session.finish_precision()
	_expect(session.state == EnhancementSessionScript.State.COMPLETE, "+100 성공 시 강화 세션이 완료되어야 합니다.")
	_expect(session.enhancement_level == 100, "최대 강화 단계는 +100이어야 합니다.")
	_expect(session.affixes.size() == 3, "+100에서 세 개의 수식어 슬롯이 완성되어야 합니다.")
	for affix_value in session.affixes:
		var affix: Dictionary = affix_value
		_expect(int(affix.get("tier", 0)) == 4, "+100에서 모든 수식어가 4티어여야 합니다.")


func _advance_to_level(session, target_level: int) -> void:
	while session.enhancement_level < target_level and not session.destroyed:
		session.begin_attempt(0.0)
		if session.state == EnhancementSessionScript.State.PRECISION:
			session.precision_position = float(session.config["precision"]["target"])
			session.finish_precision()


func _all_success_config() -> Dictionary:
	return {"base_success_by_target_level": _rates_until(100, 1.0)}


func _rates_until(max_level: int, value: float) -> Dictionary:
	var rates := {}
	for level in range(1, max_level + 1):
		rates[str(level)] = value
	return rates


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
