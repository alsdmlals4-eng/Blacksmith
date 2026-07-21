extends SceneTree

const EnhancementSessionScript = preload("res://scripts/enhancement/enhancement_session.gd")

var failures: Array[String] = []
var materials: Array = [
	{
		"id": "whetstone",
		"name": "숫돌",
		"slot_types": ["secondary"],
		"affix_tags": ["sharp"],
	},
	{
		"id": "flame_stone",
		"name": "화염석",
		"slot_types": ["secondary"],
		"affix_tags": ["fire"],
	},
	{
		"id": "spirit_heart",
		"name": "정령의 심장",
		"slot_types": ["secondary"],
		"affix_tags": ["spirit"],
	},
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
		},
	},
	{
		"id": "flaming",
		"name": "불타는",
		"material_tags": ["fire"],
		"tiers": {
			"1": {"fire_damage": 5},
			"2": {"fire_damage": 12},
		},
	},
	{
		"id": "spirit_bound",
		"name": "정령이 깃든",
		"material_tags": ["spirit"],
		"tiers": {
			"1": {"special_trigger_chance": 0.05},
			"2": {"special_trigger_chance": 0.12},
		},
	},
]


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("EnhancementSession tests PASSED (7 cases)")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)


func _run_tests() -> void:
	_test_normal_level_resolves_in_one_click()
	_test_fifth_level_requires_precision()
	_test_failure_preserves_level_and_adds_pity()
	_test_catalyst_and_perfect_precision_stack_at_milestone()
	_test_level_five_adds_material_affix()
	_test_level_ten_upgrades_first_affix()
	_test_level_fifteen_and_twenty_complete_second_affix_path()


func _session(custom_config: Dictionary = {}):
	return EnhancementSessionScript.new(
		custom_config,
		materials,
		affixes,
		{"weapon_id": "iron_sword", "weapon_name": "철검"}
	)


func _test_normal_level_resolves_in_one_click() -> void:
	var session = _session()
	session.begin_attempt(0.0)
	_expect(session.enhancement_level == 1, "+1은 버튼 한 번으로 즉시 성공 판정되어야 합니다.")
	_expect(session.state == EnhancementSessionScript.State.READY, "+1 판정 후 바로 다음 강화 준비 상태여야 합니다.")
	_expect(str(session.last_attempt.get("precision_id", "")) == "ONE_CLICK", "일반 단계는 ONE_CLICK 판정으로 기록되어야 합니다.")


func _test_fifth_level_requires_precision() -> void:
	var session = _session(_all_success_config())
	_advance_to_level(session, 4)
	session.begin_attempt(0.0)
	_expect(session.enhancement_level == 4, "+5 정밀 강화 전에는 단계가 즉시 오르면 안 됩니다.")
	_expect(session.state == EnhancementSessionScript.State.PRECISION, "+5에서는 정밀 강화 상태로 전환되어야 합니다.")


func _test_failure_preserves_level_and_adds_pity() -> void:
	var session = _session({
		"base_success_by_target_level": {"1": 0.5},
	})
	session.begin_attempt(0.9)
	_expect(session.enhancement_level == 0, "강화 실패 시 단계가 내려가거나 올라가면 안 됩니다.")
	_expect(session.failure_streak == 1, "강화 실패 시 연속 실패 횟수가 증가해야 합니다.")
	_expect(is_equal_approx(session.calculate_success_chance(), 0.55), "실패 후 다음 성공률에 5%p 보정이 적용되어야 합니다.")


func _test_catalyst_and_perfect_precision_stack_at_milestone() -> void:
	var session = _session(_all_success_config())
	_advance_to_level(session, 4)
	session.config["base_success_by_target_level"]["5"] = 0.6
	session.set_catalyst_material("salamander_core")
	session.begin_attempt(0.9)
	session.precision_position = float(session.config["precision"]["target"])
	var result: Dictionary = session.finish_precision()
	_expect(is_equal_approx(float(result["success_chance"]), 0.95), "촉매 15%p와 PERFECT 20%p가 +5 기본 60%에 합산되어야 합니다.")
	_expect(bool(result["success"]), "0.9 판정은 최종 성공률 0.95에서 성공해야 합니다.")


func _test_level_five_adds_material_affix() -> void:
	var session = _session(_all_success_config())
	session.set_secondary_material("flame_stone")
	_advance_to_level(session, 5)
	_expect(session.affixes.size() == 1, "+5에서 첫 수식어 하나가 추가되어야 합니다.")
	_expect(str(session.affixes[0]["id"]) == "flaming", "화염석 누적 우세 시 불타는 수식어가 붙어야 합니다.")
	_expect(session.get_display_name() == "불타는 철검 +5", "완성 무기 이름에 수식어와 강화 단계가 표시되어야 합니다.")


func _test_level_ten_upgrades_first_affix() -> void:
	var session = _session(_all_success_config())
	session.set_secondary_material("flame_stone")
	_advance_to_level(session, 10)
	_expect(session.affixes.size() == 1, "+10까지 첫 수식어 슬롯 하나가 유지되어야 합니다.")
	_expect(int(session.affixes[0]["tier"]) == 2, "+10에서 첫 수식어가 2티어로 강화되어야 합니다.")
	_expect(int(session.affixes[0]["effects"]["fire_damage"]) == 12, "+10 수식어 효과가 2티어 값으로 갱신되어야 합니다.")


func _test_level_fifteen_and_twenty_complete_second_affix_path() -> void:
	var session = _session(_all_success_config())
	session.set_secondary_material("flame_stone")
	_advance_to_level(session, 10)
	session.set_secondary_material("whetstone")
	_advance_to_level(session, 20)
	_expect(session.state == EnhancementSessionScript.State.COMPLETE, "+20 성공 시 강화 테스트가 완료되어야 합니다.")
	_expect(session.affixes.size() == 2, "+15에서 두 번째 수식어가 추가되어야 합니다.")
	_expect(str(session.affixes[1]["id"]) == "sharp", "숫돌 구간 우세 시 두 번째 수식어는 날카로운이어야 합니다.")
	_expect(int(session.affixes[0]["tier"]) == 2, "첫 수식어는 +10에서 2티어여야 합니다.")
	_expect(int(session.affixes[1]["tier"]) == 2, "두 번째 수식어는 +20에서 2티어여야 합니다.")
	_expect(session.get_display_name() == "날카로운 불타는 철검 +20", "두 수식어와 +20 단계가 최종 이름에 표시되어야 합니다.")


func _advance_to_level(session, target_level: int) -> void:
	while session.enhancement_level < target_level:
		session.begin_attempt(0.0)
		if session.state == EnhancementSessionScript.State.PRECISION:
			session.precision_position = float(session.config["precision"]["target"])
			session.finish_precision()


func _all_success_config() -> Dictionary:
	var rates := {}
	for level in range(1, 21):
		rates[str(level)] = 1.0
	return {"base_success_by_target_level": rates}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)