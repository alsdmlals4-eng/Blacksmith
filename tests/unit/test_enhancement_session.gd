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
		"tiers": {"1": {"attack_percent": 0.08}},
	},
	{
		"id": "flaming",
		"name": "불타는",
		"material_tags": ["fire"],
		"tiers": {"1": {"fire_damage": 5}},
	},
	{
		"id": "spirit_bound",
		"name": "정령이 깃든",
		"material_tags": ["spirit"],
		"tiers": {"1": {"special_trigger_chance": 0.05}},
	},
]


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("EnhancementSession tests PASSED (5 cases)")
		quit(0)
	else:
		for failure in failures:
			push_error(failure)
		quit(1)


func _run_tests() -> void:
	_test_precision_off_success()
	_test_failure_preserves_level_and_adds_pity()
	_test_catalyst_and_perfect_precision_stack()
	_test_success_clears_failure_streak()
	_test_level_five_adds_material_affix()


func _session(custom_config: Dictionary = {}) -> RefCounted:
	return EnhancementSessionScript.new(
		custom_config,
		materials,
		affixes,
		{"weapon_id": "iron_sword", "weapon_name": "철검"}
	)


func _test_precision_off_success() -> void:
	var session = _session()
	session.set_precision_enabled(false)
	session.begin_attempt(0.0)
	_expect(session.enhancement_level == 1, "정밀 강화 OFF에서도 +1 성공이 가능해야 합니다.")
	_expect(session.state == EnhancementSessionScript.State.READY, "+1 성공 후 다음 강화 준비 상태여야 합니다.")


func _test_failure_preserves_level_and_adds_pity() -> void:
	var session = _session({
		"base_success_by_target_level": {"1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5, "5": 0.5},
	})
	session.set_precision_enabled(false)
	session.begin_attempt(0.9)
	_expect(session.enhancement_level == 0, "강화 실패 시 단계가 내려가거나 올라가면 안 됩니다.")
	_expect(session.failure_streak == 1, "강화 실패 시 연속 실패 횟수가 증가해야 합니다.")
	_expect(is_equal_approx(session.calculate_success_chance(), 0.55), "실패 후 다음 성공률에 5%p 보정이 적용되어야 합니다.")


func _test_catalyst_and_perfect_precision_stack() -> void:
	var session = _session({
		"base_success_by_target_level": {"1": 0.6, "2": 0.6, "3": 0.6, "4": 0.6, "5": 0.6},
	})
	session.set_catalyst_material("salamander_core")
	session.begin_attempt(0.9)
	session.precision_position = float(session.config["precision"]["target"])
	var result: Dictionary = session.finish_precision()
	_expect(is_equal_approx(float(result["success_chance"]), 0.95), "촉매 15%p와 PERFECT 20%p가 기본 60%에 합산되어야 합니다.")
	_expect(bool(result["success"]), "0.9 판정은 최종 성공률 0.95에서 성공해야 합니다.")


func _test_success_clears_failure_streak() -> void:
	var session = _session({
		"base_success_by_target_level": {"1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5, "5": 0.5},
	})
	session.set_precision_enabled(false)
	session.begin_attempt(0.9)
	session.begin_attempt(0.0)
	_expect(session.enhancement_level == 1, "실패 후 성공하면 강화 단계가 올라야 합니다.")
	_expect(session.failure_streak == 0, "강화 성공 시 연속 실패 보정이 초기화되어야 합니다.")


func _test_level_five_adds_material_affix() -> void:
	var session = _session({
		"base_success_by_target_level": {"1": 1.0, "2": 1.0, "3": 1.0, "4": 1.0, "5": 1.0},
	})
	session.set_precision_enabled(false)
	session.set_secondary_material("flame_stone")
	for _index in range(5):
		session.begin_attempt(0.0)
	_expect(session.state == EnhancementSessionScript.State.COMPLETE, "+5 성공 시 강화 세션이 완료되어야 합니다.")
	_expect(session.affixes.size() == 1, "+5에서 첫 수식어 하나가 추가되어야 합니다.")
	_expect(str(session.affixes[0]["id"]) == "flaming", "화염석 누적 우세 시 불타는 수식어가 붙어야 합니다.")
	_expect(session.get_display_name() == "불타는 철검 +5", "완성 무기 이름에 수식어와 강화 단계가 표시되어야 합니다.")


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
