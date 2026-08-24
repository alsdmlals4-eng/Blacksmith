extends "res://addons/gut/test.gd"

const NADIA_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_nadia_schedule_resolver.gd"
const DAY_SERVICE_PATH := "res://scripts/vertical_slice/services/vs_day_progression_service.gd"


func test_task5_runtime_surfaces_exist() -> void:
	assert_true(ResourceLoader.exists(NADIA_RESOLVER_PATH), "Task5 requires a Nadia schedule resolver")
	assert_true(ResourceLoader.exists(DAY_SERVICE_PATH), "Task5 requires a day progression service")


func test_task5_handoff_and_day_progression_api_exist() -> void:
	var resolver = load(NADIA_RESOLVER_PATH).new()
	var service = load(DAY_SERVICE_PATH).new()
	assert_true(resolver.has_method("handoff"), "Nadia resolver must expose handoff")
	assert_true(service.has_method("register_handoff"), "day progression service must register accepted handoff proposals")
	assert_true(service.has_method("advance_day"), "day progression service must own end-of-day advancement")
