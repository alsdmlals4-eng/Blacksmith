extends SceneTree

const RegistryScript = preload("res://scripts/world/equipment_world_registry.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("EquipmentWorldRegistry tests PASSED (5 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_due_record_and_report_state()
	_test_duplicate_event_is_idempotent()
	_test_active_limit_preserves_all_records()
	_test_result_error_retry()
	_test_delivery_transaction_is_idempotent()


func _test_due_record_and_report_state() -> void:
	var registry = RegistryScript.new(6)
	var record: Dictionary = registry.deliver(_equipment("sword_a"), "gladiator_kyle", 1, 1, "tx-a")
	_expect(registry.due_records(1).is_empty(), "납품 당일에는 결과가 도착하면 안 됩니다.")
	_expect(registry.due_records(2).size() == 1, "최소 하루 뒤 결과 대상이 되어야 합니다.")
	registry.apply_result(str(record.get("equipment_uid")), {"result_id": "WIN", "score": 40}, "match-a")
	_expect(registry.records["sword_a"].get("report_state") == RegistryScript.REPORT_RESULT_READY, "결과 적용 뒤 RESULT_READY여야 합니다.")
	registry.mark_report_opened("sword_a")
	_expect(registry.records["sword_a"].get("report_state") == RegistryScript.REPORT_OPENED, "보고 열람 뒤 REPORT_OPENED여야 합니다.")


func _test_duplicate_event_is_idempotent() -> void:
	var registry = RegistryScript.new(6)
	registry.deliver(_equipment("sword_b"), "gladiator_kyle", 1, 1, "tx-b")
	registry.apply_result("sword_b", {"result_id": "WIN", "score": 40}, "match-b")
	var size_before: int = registry.records["sword_b"].get("history", []).size()
	registry.apply_result("sword_b", {"result_id": "WIN", "score": 40}, "match-b")
	_expect(registry.records["sword_b"].get("history", []).size() == size_before, "중복 event는 이력을 중복 추가하면 안 됩니다.")


func _test_active_limit_preserves_all_records() -> void:
	var registry = RegistryScript.new(6)
	for index in range(7):
		registry.deliver(_equipment("sword_%d" % index), "gladiator_kyle", index + 1, 1, "tx-%d" % index)
	_expect(registry.records.size() == 7, "상한을 넘어도 모든 납품 기록은 보존해야 합니다.")
	_expect(registry.records["sword_0"].get("lifecycle_state") == RegistryScript.LIFECYCLE_DORMANT, "가장 오래된 비대표 기록은 DORMANT가 되어야 합니다.")


func _test_result_error_retry() -> void:
	var registry = RegistryScript.new(6)
	registry.deliver(_equipment("sword_error"), "gladiator_kyle", 1, 1, "tx-error")
	registry.mark_result_error("sword_error", "MISSING_ACTIVITY_DATA")
	_expect(registry.records["sword_error"].get("report_state") == RegistryScript.REPORT_RESULT_ERROR, "결과 누락은 RESULT_ERROR여야 합니다.")
	var retry: Dictionary = registry.retry_result("sword_error", {"result_id": "DEFEAT", "score": 30}, "match-error")
	_expect(bool(retry.get("ok", false)), "같은 결정적 입력으로 재시도할 수 있어야 합니다.")
	_expect(registry.records["sword_error"].get("report_state") == RegistryScript.REPORT_RESULT_READY, "재시도 성공 뒤 RESULT_READY여야 합니다.")


func _test_delivery_transaction_is_idempotent() -> void:
	var registry = RegistryScript.new(6)
	var first: Dictionary = registry.deliver(_equipment("sword_tx"), "gladiator_kyle", 1, 1, "tx-same")
	var second: Dictionary = registry.deliver(_equipment("different_uid"), "gladiator_kyle", 1, 1, "tx-same")
	_expect(first.get("equipment_uid") == second.get("equipment_uid"), "동일 delivery transaction은 같은 기록을 반환해야 합니다.")
	_expect(registry.records.size() == 1, "동일 delivery transaction은 기록을 중복 생성하면 안 됩니다.")


func _equipment(uid: String) -> Dictionary:
	return {"record_schema_version": 1, "equipment_uid": uid, "weapon_id": "iron_sword", "enhancement_level": 5}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
