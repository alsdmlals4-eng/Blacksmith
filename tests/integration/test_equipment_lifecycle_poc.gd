extends SceneTree

const WorkshopCalendarScript = preload("res://scripts/progression/workshop_calendar.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")
const WorkshopActionServiceScript = preload("res://scripts/poc/workshop_action_service.gd")
const CustomerContractScript = preload("res://scripts/customers/customer_contract.gd")
const EquipmentWorldRegistryScript = preload("res://scripts/world/equipment_world_registry.gd")
const WorldActivityResolverScript = preload("res://scripts/world/world_activity_resolver.gd")
const EquipmentLifecycleControllerScript = preload("res://scripts/poc/equipment_lifecycle_poc_controller.gd")
const PocTelemetryScript = preload("res://scripts/telemetry/poc_telemetry.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("Equipment lifecycle PoC integration tests PASSED (6 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_normal_lifecycle_reaches_follow_up()
	_test_apprentice_plus_five_reaches_defeat()
	_test_masterwork_plus_ten_preferred_reaches_decisive_win()
	_test_resource_failures_are_atomic()
	_test_delivery_retry_is_idempotent()
	_test_result_retry_is_deterministic()


func _test_normal_lifecycle_reaches_follow_up() -> void:
	var context := _context()
	var controller = context["controller"]
	var action_service = context["action_service"]
	var calendar = context["calendar"]
	var telemetry = context["telemetry"]
	controller.accept_contract()
	var forge: Dictionary = action_service.try_begin_forging(100, "iron", 1, func() -> bool: return true)
	_expect(bool(forge.get("ok", false)), "정상 경로 제작 시작은 성공해야 합니다.")
	_expect(calendar.current_fatigue == 17, "제작 시작은 작업량 3을 소비해야 합니다.")
	var equipment := _equipment("normal_sword", 5, "REFINED", [], 20)
	controller.add_equipment(equipment)
	var delivery: Dictionary = controller.deliver("normal_sword", "tx_normal")
	_expect(bool(delivery.get("ok", false)), "+5 정교한 철검은 납품 가능해야 합니다.")
	var day_result: Dictionary = controller.end_day()
	var resolved: Array = day_result.get("resolved_results", [])
	_expect(resolved.size() == 1, "하루 종료 뒤 지연 경기 결과 1건이 생성되어야 합니다.")
	_expect(str(resolved[0].get("result_id", "")) == "WIN", "정교한 +5 철검은 WIN이어야 합니다.")
	var report: Dictionary = controller.open_report("normal_sword")
	_expect(bool(report.get("ok", false)), "준비된 보고서는 열 수 있어야 합니다.")
	_expect(controller.state == controller.STATE_FOLLOW_UP, "보고 후 같은 고객 재방문 상태로 진입해야 합니다.")
	_expect(controller.follow_up_started, "재방문 플래그가 기록되어야 합니다.")
	_expect(telemetry.events_named("follow_up_started").size() == 1, "재방문 telemetry가 한 번 기록되어야 합니다.")


func _test_apprentice_plus_five_reaches_defeat() -> void:
	var context := _context()
	var fit: Dictionary = context["contract"].evaluate_fit(_equipment("defeat_sword", 5, "APPRENTICE", [], 20))
	var result: Dictionary = context["resolver"].resolve(fit, 0.2)
	_expect(int(fit.get("score", -1)) == 30, "미숙한 +5 철검 점수는 30이어야 합니다.")
	_expect(str(result.get("result_id", "")) == "DEFEAT", "미숙한 +5 철검은 DEFEAT 밴드여야 합니다.")


func _test_masterwork_plus_ten_preferred_reaches_decisive_win() -> void:
	var context := _context()
	var affixes := [{"id": "sharp", "name": "날카로운", "tier": 1}]
	var fit: Dictionary = context["contract"].evaluate_fit(_equipment("decisive_sword", 10, "MASTERWORK", affixes, 24))
	var result: Dictionary = context["resolver"].resolve(fit, 0.8)
	_expect(int(fit.get("score", -1)) == 85, "명품 +10 선호 수식어 철검 점수는 85여야 합니다.")
	_expect(str(result.get("result_id", "")) == "DECISIVE_WIN", "명품 +10 선호 수식어 철검은 DECISIVE_WIN이어야 합니다.")


func _test_resource_failures_are_atomic() -> void:
	var context := _context()
	var action_service = context["action_service"]
	var calendar = context["calendar"]
	var resources = context["resources"]
	var before_calendar: Dictionary = calendar.snapshot()
	var before_resources: Dictionary = resources.snapshot()
	var no_gold: Dictionary = action_service.try_begin_forging(99999, "iron", 1, func() -> bool: return true)
	_expect(str(no_gold.get("status", "")) == "NO_GOLD", "골드 부족은 NO_GOLD를 반환해야 합니다.")
	_expect(calendar.snapshot() == before_calendar, "골드 부족은 작업량을 변경하면 안 됩니다.")
	_expect(resources.snapshot() == before_resources, "골드 부족은 자원을 변경하면 안 됩니다.")
	calendar.current_fatigue = 0
	var no_fatigue: Dictionary = action_service.try_begin_forging(1, "iron", 1, func() -> bool: return true)
	_expect(str(no_fatigue.get("status", "")) == "NO_FATIGUE", "작업량 부족은 NO_FATIGUE를 반환해야 합니다.")


func _test_delivery_retry_is_idempotent() -> void:
	var context := _context()
	var controller = context["controller"]
	var resources = context["resources"]
	controller.accept_contract()
	controller.add_equipment(_equipment("retry_sword", 5, "REFINED", [], 20))
	var first: Dictionary = controller.deliver("retry_sword", "tx_retry")
	var gold_after_first := resources.gold
	var fame_after_first := controller.fame
	var second: Dictionary = controller.deliver("retry_sword", "tx_retry")
	_expect(bool(first.get("ok", false)) and bool(second.get("ok", false)), "같은 납품 transaction 재시도는 성공 응답이어야 합니다.")
	_expect(str(second.get("status", "")) == "ALREADY_DELIVERED", "중복 납품은 ALREADY_DELIVERED여야 합니다.")
	_expect(resources.gold == gold_after_first, "중복 납품은 대금을 다시 지급하면 안 됩니다.")
	_expect(controller.fame == fame_after_first, "중복 납품은 즉시 명성을 다시 지급하면 안 됩니다.")


func _test_result_retry_is_deterministic() -> void:
	var context := _context()
	var registry = context["registry"]
	var contract = context["contract"]
	var resolver = context["resolver"]
	var equipment := _equipment("error_sword", 5, "REFINED", [], 20)
	registry.deliver(equipment, "gladiator_kyle", 1, 1, "tx_error")
	registry.mark_result_error("error_sword", "TEMPORARY")
	var fit: Dictionary = contract.evaluate_fit(equipment)
	var first_result: Dictionary = resolver.resolve(fit, 0.5)
	var retry: Dictionary = registry.retry_result("error_sword", first_result, "match:error_sword:2")
	var stored: Dictionary = registry.records["error_sword"].get("result", {})
	_expect(bool(retry.get("ok", false)), "RESULT_ERROR 기록은 재시도 가능해야 합니다.")
	_expect(stored == first_result, "결과 재시도는 같은 결정적 입력의 결과를 보존해야 합니다.")


func _context() -> Dictionary:
	var day_config := _read_json("res://data/progression/workshop_day_balance.json")
	var contract_config := _read_json("res://data/customers/gladiator_poc.json")
	var result_config := _read_json("res://data/world/gladiator_match_poc.json")
	var calendar = WorkshopCalendarScript.new(day_config)
	var resources = WorkshopResourcesScript.new(1000, {"iron": 3, "whetstone": 3})
	var action_service = WorkshopActionServiceScript.new(calendar, resources)
	var contract = CustomerContractScript.new(contract_config, result_config, calendar.day)
	var registry = EquipmentWorldRegistryScript.new(6)
	var resolver = WorldActivityResolverScript.new(result_config)
	var telemetry = PocTelemetryScript.new()
	var controller = EquipmentLifecycleControllerScript.new(contract, registry, resolver, calendar, resources, telemetry)
	return {
		"calendar": calendar,
		"resources": resources,
		"action_service": action_service,
		"contract": contract,
		"registry": registry,
		"resolver": resolver,
		"telemetry": telemetry,
		"controller": controller,
	}


func _equipment(uid: String, level: int, grade_id: String, affixes: Array, attack: int) -> Dictionary:
	return {
		"record_schema_version": 1,
		"equipment_uid": uid,
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"enhancement_level": level,
		"craftsmanship_grade_id": grade_id,
		"progression_attack": attack,
		"base_attack": 20,
		"affixes": affixes.duplicate(true),
		"destroyed": false,
		"lifecycle_state": "WORKSHOP",
	}


func _read_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		failures.append("필수 JSON을 읽지 못했습니다: %s" % path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
