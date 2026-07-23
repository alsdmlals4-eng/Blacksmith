extends SceneTree

const CalendarScript = preload("res://scripts/progression/workshop_calendar.gd")
const ResourcesScript = preload("res://scripts/economy/workshop_resources.gd")
const ContractScript = preload("res://scripts/customers/customer_contract.gd")
const RegistryScript = preload("res://scripts/world/equipment_world_registry.gd")
const ResolverScript = preload("res://scripts/world/world_activity_resolver.gd")
const ControllerScript = preload("res://scripts/poc/equipment_lifecycle_poc_controller.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("Equipment lifecycle controller integration tests PASSED (4 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_delivery_failure_injection_rolls_back()
	_test_delivery_transaction_is_idempotent()
	_test_day_end_resolves_delayed_result()
	_test_report_rewards_apply_once_and_start_follow_up()


func _test_delivery_failure_injection_rolls_back() -> void:
	for stage in ["after_inventory", "after_owner", "after_payment", "after_fame", "after_record"]:
		var controller = _controller()
		controller.add_equipment(_equipment("rollback_%s" % stage, "REFINED", 5))
		var before: Dictionary = controller.snapshot()
		var result: Dictionary = controller.deliver("rollback_%s" % stage, "tx-%s" % stage, stage)
		_expect(not bool(result.get("ok", true)), "%s 실패 주입은 실패해야 합니다." % stage)
		_expect(controller.snapshot() == before, "%s 실패는 inventory·gold·fame·world를 모두 복구해야 합니다." % stage)


func _test_delivery_transaction_is_idempotent() -> void:
	var controller = _controller()
	controller.add_equipment(_equipment("idempotent", "REFINED", 5))
	var first: Dictionary = controller.deliver("idempotent", "tx-idempotent")
	var gold_after_first: int = controller.resources.gold
	var fame_after_first: int = controller.fame
	var second: Dictionary = controller.deliver("idempotent", "tx-idempotent")
	_expect(bool(first.get("ok", false)) and bool(second.get("ok", false)), "동일 납품 재시도는 성공 상태를 반환해야 합니다.")
	_expect(second.get("status") == "ALREADY_DELIVERED", "동일 transaction은 ALREADY_DELIVERED여야 합니다.")
	_expect(controller.resources.gold == gold_after_first and controller.fame == fame_after_first, "동일 transaction은 대금·명성을 중복 적용하면 안 됩니다.")
	_expect(controller.registry.records.size() == 1, "동일 transaction은 world record를 중복 생성하면 안 됩니다.")


func _test_day_end_resolves_delayed_result() -> void:
	var controller = _controller()
	controller.add_equipment(_equipment("delayed", "REFINED", 5))
	controller.deliver("delayed", "tx-delayed")
	_expect(controller.registry.records["delayed"].get("report_state") == RegistryScript.REPORT_PENDING, "납품 직후 보고는 PENDING이어야 합니다.")
	var ended: Dictionary = controller.end_day()
	_expect(Array(ended.get("resolved_results", [])).size() == 1, "하루 종료 뒤 지연 결과 1건이 계산되어야 합니다.")
	_expect(controller.state == ControllerScript.STATE_REPORT_READY, "결과 도착 뒤 REPORT_READY 상태여야 합니다.")


func _test_report_rewards_apply_once_and_start_follow_up() -> void:
	var controller = _controller()
	controller.add_equipment(_equipment("report", "REFINED", 5))
	controller.deliver("report", "tx-report")
	controller.end_day()
	var before_fame: int = controller.fame
	var first: Dictionary = controller.open_report("report")
	var fame_after_first: int = controller.fame
	var second: Dictionary = controller.open_report("report")
	_expect(bool(first.get("ok", false)) and bool(second.get("ok", false)), "같은 보고서를 다시 열 수 있어야 합니다.")
	_expect(fame_after_first > before_fame, "첫 보고 열람은 세계 명성을 적용해야 합니다.")
	_expect(controller.fame == fame_after_first, "두 번째 열람은 명성을 중복 적용하면 안 됩니다.")
	_expect(controller.follow_up_started and controller.state == ControllerScript.STATE_FOLLOW_UP, "보고 뒤 같은 고객 재방문 상태로 전환해야 합니다.")


func _controller():
	var contract = ContractScript.new(_contract(), _activity(), 1)
	return ControllerScript.new(
		contract,
		RegistryScript.new(6),
		ResolverScript.new(_activity()),
		CalendarScript.new(),
		ResourcesScript.new(1000, {"iron": 10})
	)


func _equipment(uid: String, grade_id: String, level: int) -> Dictionary:
	return {
		"record_schema_version": 1,
		"equipment_uid": uid,
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
		"customer_id": "gladiator_kyle",
		"equipment_id": "iron_sword",
		"required_level": 5,
		"stretch_level": 10,
		"preferred_affix_ids": ["sharp", "flaming"],
		"deadline_days": 3,
		"report_delay_days": 1,
		"payment_gold": 500,
		"immediate_fame": 1,
	}


func _activity() -> Dictionary:
	return {
		"score_weights": {"required_level": 20, "stretch_level": 15, "preferred_affix": 25, "attack_threshold": 20, "attack": 10},
		"grade_scores": {"APPRENTICE": 0, "STANDARD": 5, "REFINED": 10, "MASTERWORK": 15, "PERFECT": 20},
		"result_bands": [
			{"id": "DEFEAT", "minimum_score": 0, "fame": 0, "relationship": 0},
			{"id": "WIN", "minimum_score": 35, "fame": 2, "relationship": 1},
			{"id": "DECISIVE_WIN", "minimum_score": 70, "fame": 5, "relationship": 2},
		],
	}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
