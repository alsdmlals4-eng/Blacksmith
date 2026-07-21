extends SceneTree

const EnhancementSessionScript = preload("res://scripts/enhancement/enhancement_session.gd")

var failures: Array[String] = []
var materials: Array = [
	{"id": "whetstone", "name": "숫돌", "slot_types": ["secondary"], "affix_tags": ["sharp"]},
	{"id": "flame_stone", "name": "화염석", "slot_types": ["secondary"], "affix_tags": ["fire"]},
	{"id": "spirit_heart", "name": "정령의 심장", "slot_types": ["secondary"], "affix_tags": ["spirit"]},
	{
		"id": "salamander_core",
		"name": "살라맨더의 핵",
		"slot_types": ["catalyst"],
		"affix_tags": ["fire", "salamander"],
		"success_bonus": 0.15,
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
		print("EnhancementSession tests PASSED (8 cases)")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)


func _run_tests() -> void:
	_test_normal_level_resolves_in_one_click()
	_test_fifth_level_requires_precision_without_materials()
	_test_tenth_level_enables_materials()
	_test_catalyst_applies_only_at_ten_level_milestone()
	_test_failure_preserves_level_and_adds_pity()
	_test_level_ten_adds_selected_affix()
	_test_level_twenty_upgrades_first_affix()
	_test_level_one_hundred_completes_three_affixes()


func _session(custom_config: Dictionary = {}):
	var merged := {
		"max_level": 100,
		"precision_interval": 5,
		"material_interval": 10,
		"milestones": milestones,
	}
	for key_value in custom_config:
		merged[key_value] = custom_config[key_value]
	return EnhancementSessionScript.new(
		merged,
		materials,
		affixes,
		{"weapon_id": "iron_sword", "weapon_name": "철검"}
	)


func _test_normal_level_resolves_in_one_click() -> void:
	var session = _session(_all_success_config())
	session.begin_attempt(0.0)
	_expect(session.enhancement_level == 1, "+1은 버튼 한 번으로 즉시 판정되어야 합니다.")
	_expect(session.state == EnhancementSessionScript.State.READY, "+1 후 다음 강화 준비 상태여야 합니다.")
	_expect(str(session.last_attempt.get("precision_id", "")) == "ONE_CLICK", "일반 단계는 ONE_CLICK으로 기록되어야 합니다.")


func _test_fifth_level_requires_precision_without_materials() -> void:
	var session = _session(_all_success_config())
	_advance_to_level(session, 4)
	_expect(not session.uses_materials_for_level(5), "+5에서는 재료를 사용하지 않아야 합니다.")
	_expect(not session.set_secondary_material("flame_stone"), "+5 직전에는 보조재료를 변경할 수 없어야 합니다.")
	session.begin_attempt(0.0)
	_expect(session.state == EnhancementSessionScript.State.PRECISION, "+5에서는 정밀 강화 상태로 전환되어야 합니다.")
	_expect(session.material_scores.is_empty(), "+5 정밀 강화에는 재료 성질이 누적되면 안 됩니다.")


func _test_tenth_level_enables_materials() -> void:
	var session = _session(_all_success_config())
	_advance_to_level(session, 9)
	_expect(session.uses_materials_for_level(10), "+10은 재료 선택 단계여야 합니다.")
	_expect(session.set_secondary_material("flame_stone"), "+10 직전에는 보조재료를 선택할 수 있어야 합니다.")
	_expect(session.set_catalyst_material("salamander_core"), "+10 직전에는 촉매를 선택할 수 있어야 합니다.")
	session.begin_attempt(0.0)
	_expect(session.state == EnhancementSessionScript.State.PRECISION, "+10은 재료 선택 후 정밀 강화여야 합니다.")
	_expect(int(session.material_scores.get("fire", 0)) > 0, "+10 시도에서 화염 재료 성질이 누적되어야 합니다.")


func _test_catalyst_applies_only_at_ten_level_milestone() -> void:
	var session = _session({
		"base_success_by_target_level": {"5": 0.60, "10": 0.60},
	})
	_advance_to_level(session, 4)
	_expect(not session.set_catalyst_material("salamander_core"), "+5 직전에는 촉매를 선택할 수 없어야 합니다.")
	_expect(is_equal_approx(session.calculate_success_chance(), 0.60), "+5 성공률에는 촉매 보너스가 없어야 합니다.")
	session.begin_attempt(0.0)
	session.precision_position = float(session.config["precision"]["target"])
	session.finish_precision()
	_advance_to_level(session, 9)
	session.set_catalyst_material("salamander_core")
	_expect(is_equal_approx(session.calculate_success_chance(), 0.75), "+10 성공률에는 촉매 15%p가 적용되어야 합니다.")


func _test_failure_preserves_level_and_adds_pity() -> void:
	var session = _session({"base_success_by_target_level": {"1": 0.5}})
	session.begin_attempt(0.9)
	_expect(session.enhancement_level == 0, "강화 실패 시 단계가 유지되어야 합니다.")
	_expect(session.failure_streak == 1, "강화 실패 시 연속 실패 횟수가 증가해야 합니다.")
	_expect(is_equal_approx(session.calculate_success_chance(), 0.55), "실패 후 다음 성공률에 5%p 보정이 적용되어야 합니다.")


func _test_level_ten_adds_selected_affix() -> void:
	var session = _session(_all_success_config())
	_advance_to_level(session, 9)
	session.set_secondary_material("flame_stone")
	_advance_to_level(session, 10)
	_expect(session.affixes.size() == 1, "+10에서 첫 수식어가 추가되어야 합니다.")
	_expect(str(session.affixes[0]["id"]) == "flaming", "+10 화염석 선택 시 불타는 수식어가 붙어야 합니다.")
	_expect(session.get_display_name() == "불타는 철검 +10", "첫 수식어와 +10 단계가 이름에 표시되어야 합니다.")


func _test_level_twenty_upgrades_first_affix() -> void:
	var session = _session(_all_success_config())
	_advance_to_level(session, 9)
	session.set_secondary_material("flame_stone")
	_advance_to_level(session, 20)
	_expect(session.affixes.size() == 1, "+20까지 첫 수식어 슬롯 하나가 유지되어야 합니다.")
	_expect(int(session.affixes[0]["tier"]) == 2, "+20에서 첫 수식어가 2티어가 되어야 합니다.")
	_expect(int(session.affixes[0]["effects"]["fire_damage"]) == 12, "+20 수식어 효과가 2티어 값이어야 합니다.")


func _test_level_one_hundred_completes_three_affixes() -> void:
	var session = _session(_all_success_config())
	var material_by_level := {
		10: "flame_stone",
		30: "whetstone",
		50: "spirit_heart",
	}
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
	while session.enhancement_level < target_level:
		session.begin_attempt(0.0)
		if session.state == EnhancementSessionScript.State.PRECISION:
			session.precision_position = float(session.config["precision"]["target"])
			session.finish_precision()


func _all_success_config() -> Dictionary:
	var rates := {}
	for level in range(1, 101):
		rates[str(level)] = 1.0
	return {"base_success_by_target_level": rates}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
