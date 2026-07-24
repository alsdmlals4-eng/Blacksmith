extends SceneTree

const TelemetryScript = preload("res://scripts/telemetry/poc_telemetry.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("PocTelemetry tests PASSED (4 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_order_and_filter()
	_test_payload_is_deep_copied()
	_test_explicit_json_export()
	_test_clear_resets_state()


func _test_order_and_filter() -> void:
	var telemetry = TelemetryScript.new()
	telemetry.record("contract_viewed", {"day": 1})
	telemetry.record("enhancement_attempted", {"level": 1})
	telemetry.record("contract_viewed", {"day": 2})
	var matches: Array[Dictionary] = telemetry.events_named("contract_viewed")
	_expect(matches.size() == 2, "이름 필터는 두 contract_viewed 이벤트를 반환해야 합니다.")
	_expect(matches[0].get("sequence") == 1 and matches[1].get("sequence") == 3, "이벤트 순서를 보존해야 합니다.")


func _test_payload_is_deep_copied() -> void:
	var telemetry = TelemetryScript.new()
	var payload := {"equipment": {"level": 5}}
	telemetry.record("delivered", payload)
	payload["equipment"]["level"] = 10
	_expect(telemetry.events[0].get("payload", {}).get("equipment", {}).get("level") == 5, "기록 payload는 deep copy여야 합니다.")
	var copy: Array[Dictionary] = telemetry.events_named("delivered")
	copy[0]["payload"]["equipment"]["level"] = 20
	_expect(telemetry.events[0].get("payload", {}).get("equipment", {}).get("level") == 5, "필터 결과 수정이 원본 기록을 바꾸면 안 됩니다.")


func _test_explicit_json_export() -> void:
	var telemetry = TelemetryScript.new()
	telemetry.record("report_opened", {"equipment_uid": "sword_1"})
	var parsed = JSON.parse_string(telemetry.export_json())
	_expect(parsed is Dictionary, "export_json은 JSON object를 반환해야 합니다.")
	_expect(parsed.get("schema_version") == 1, "telemetry export schema_version은 1이어야 합니다.")
	_expect(parsed.get("events", []).size() == 1, "명시적 export에 이벤트가 포함되어야 합니다.")


func _test_clear_resets_state() -> void:
	var telemetry = TelemetryScript.new()
	telemetry.record("day_ended")
	telemetry.clear()
	_expect(telemetry.events.is_empty() and telemetry.sequence == 0, "clear는 이벤트와 sequence를 초기화해야 합니다.")


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
