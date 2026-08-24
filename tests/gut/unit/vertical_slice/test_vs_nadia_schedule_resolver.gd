extends "res://addons/gut/test.gd"

const NADIA_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_nadia_schedule_resolver.gd"
const DAY_SERVICE_PATH := "res://scripts/vertical_slice/services/vs_day_progression_service.gd"


func test_task5_runtime_surfaces_exist() -> void:
	assert_true(ResourceLoader.exists(NADIA_RESOLVER_PATH), "Task5 requires a Nadia schedule resolver")
	assert_true(ResourceLoader.exists(DAY_SERVICE_PATH), "Task5 requires a day progression service")
