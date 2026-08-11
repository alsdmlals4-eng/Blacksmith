extends SceneTree

const ProjectHandlerScript := preload("res://addons/godot_ai/handlers/project_handler.gd")
const ErrorCodes := preload("res://addons/godot_ai/utils/error_codes.gd")

const MAIN_SCENE_KEY := "application/run/main_scene"
const CURRENT_MAIN_SCENE := "res://scenes/vertical_slice/main_menu.tscn"

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("Godot AI 3.1.4 current main-scene guard tests PASSED")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_expect(
		not ProjectHandlerScript.startup_execution_key_refusal(MAIN_SCENE_KEY).is_empty(),
		"generic settings_set startup denylist must continue refusing application/run/main_scene",
	)

	var handler = ProjectHandlerScript.new(null, null, null)
	_expect(
		not handler.has_method("set_main_scene"),
		"official current 3.1.4 vendor must not reintroduce the retired Task2-only raw set_main_scene overlay",
	)

	_test_generic_main_scene_setting_stays_denied(handler)
	_expect(
		str(ProjectSettings.get_setting(MAIN_SCENE_KEY, "")) == CURRENT_MAIN_SCENE,
		"current project must already point application/run/main_scene at the approved MainMenu",
	)


func _test_generic_main_scene_setting_stays_denied(handler) -> void:
	var before := _snapshot_main_scene()
	var response: Dictionary = handler.call(
		"set_project_setting",
		{"key": MAIN_SCENE_KEY, "value": "res://scenes/test/enhancement_test.tscn"},
	)
	_expect_error_code(
		response,
		ErrorCodes.VALUE_OUT_OF_RANGE,
		"generic set_project_setting must keep refusing application/run/main_scene",
	)
	_expect(_main_scene_matches_snapshot(before), "generic refusal must not mutate main_scene")


func _snapshot_main_scene() -> Dictionary:
	var had_setting := ProjectSettings.has_setting(MAIN_SCENE_KEY)
	return {
		"had_setting": had_setting,
		"value": ProjectSettings.get_setting(MAIN_SCENE_KEY) if had_setting else null,
	}


func _main_scene_matches_snapshot(snapshot: Dictionary) -> bool:
	if bool(snapshot.get("had_setting", false)) != ProjectSettings.has_setting(MAIN_SCENE_KEY):
		return false
	if not bool(snapshot.get("had_setting", false)):
		return true
	return ProjectSettings.get_setting(MAIN_SCENE_KEY) == snapshot.get("value")


func _expect_error_code(response: Dictionary, code: String, message: String) -> void:
	var error: Dictionary = response.get("error", {})
	_expect(response.get("status", "") == "error", "%s (expected error response)" % message)
	_expect(str(error.get("code", "")) == code, "%s (expected %s, got %s)" % [message, code, error.get("code", "")])


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
