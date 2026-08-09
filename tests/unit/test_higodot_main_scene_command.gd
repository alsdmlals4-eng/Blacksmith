extends SceneTree

const ProjectHandlerScript := preload("res://addons/godot_ai/handlers/project_handler.gd")
const ErrorCodes := preload("res://addons/godot_ai/utils/error_codes.gd")

const MAIN_SCENE_KEY := "application/run/main_scene"
const VALID_SCENE := "res://scenes/test/enhancement_test.tscn"
const NON_SCENE_TMP := "res://tests/.tmp_higodot_non_scene.tscn"

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	_cleanup_non_scene_tmp()
	if failures.is_empty():
		print("HiGodot main-scene command tests PASSED")
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

	var seam_supported := _supports_save_seam()
	_expect(seam_supported, "ProjectHandler must accept an optional fourth Callable persistence seam")

	var handler = ProjectHandlerScript.new(null, null, null)
	var command_exists := handler.has_method("set_main_scene")
	_expect(command_exists, "ProjectHandler must expose dedicated set_main_scene(params)")

	_test_generic_main_scene_setting_stays_denied(handler)
	if not seam_supported or not command_exists:
		return

	_test_missing_and_invalid_scene_params()
	_test_unsafe_and_non_scene_paths()
	_test_missing_scene_resource()
	_test_non_packed_scene_resource()
	_test_existing_confined_scene_is_accepted()
	_test_save_failure_restores_old_value()


func _test_generic_main_scene_setting_stays_denied(handler) -> void:
	var before := _snapshot_main_scene()
	var response: Dictionary = handler.call(
		"set_project_setting",
		{"key": MAIN_SCENE_KEY, "value": VALID_SCENE},
	)
	_expect_error_code(
		response,
		ErrorCodes.VALUE_OUT_OF_RANGE,
		"generic set_project_setting must keep refusing application/run/main_scene",
	)
	_expect(_main_scene_matches_snapshot(before), "generic refusal must not mutate main_scene")


func _test_missing_and_invalid_scene_params() -> void:
	var handler = _new_handler(Callable(self, "_save_ok"))
	_expect_error_code(
		handler.call("set_main_scene", {}),
		ErrorCodes.MISSING_REQUIRED_PARAM,
		"missing scene must fail closed",
	)
	_expect_error_code(
		handler.call("set_main_scene", {"scene": ""}),
		ErrorCodes.MISSING_REQUIRED_PARAM,
		"empty scene must fail closed",
	)
	_expect_error_code(
		handler.call("set_main_scene", {"scene": 42}),
		ErrorCodes.WRONG_TYPE,
		"non-string scene must fail closed",
	)


func _test_unsafe_and_non_scene_paths() -> void:
	var handler = _new_handler(Callable(self, "_save_ok"))
	for scene in [
		"uid://badhigodotmain",
		"user://main_menu.tscn",
		"/tmp/main_menu.tscn",
		"C:/tmp/main_menu.tscn",
		"res://../main_menu.tscn",
		"res://scripts/forging/forging_session.gd",
	]:
		_expect_error_code(
			handler.call("set_main_scene", {"scene": scene}),
			ErrorCodes.VALUE_OUT_OF_RANGE,
			"unsafe or non-.tscn scene must fail closed: %s" % scene,
		)


func _test_missing_scene_resource() -> void:
	var handler = _new_handler(Callable(self, "_save_ok"))
	_expect_error_code(
		handler.call("set_main_scene", {"scene": "res://tests/does_not_exist_main_scene.tscn"}),
		ErrorCodes.RESOURCE_NOT_FOUND,
		"missing confined .tscn must fail closed",
	)


func _test_non_packed_scene_resource() -> void:
	if not _write_non_scene_tmp():
		return
	var handler = _new_handler(Callable(self, "_save_ok"))
	_expect_error_code(
		handler.call("set_main_scene", {"scene": NON_SCENE_TMP}),
		ErrorCodes.WRONG_TYPE,
		"existing .tscn-shaped resource that is not PackedScene must fail closed",
	)
	_cleanup_non_scene_tmp()


func _test_existing_confined_scene_is_accepted() -> void:
	var before := _snapshot_main_scene()
	var handler = _new_handler(Callable(self, "_save_ok"))
	var response: Dictionary = handler.call("set_main_scene", {"scene": VALID_SCENE})
	_expect(response.get("status", "") != "error", "existing confined PackedScene should be accepted")
	var data: Dictionary = response.get("data", {})
	_expect(str(data.get("key", "")) == MAIN_SCENE_KEY, "success must report the exact ProjectSettings key")
	_expect(str(data.get("value", "")) == VALID_SCENE, "success must report the accepted scene")
	_expect(bool(data.get("undoable", true)) == false, "main-scene persistence must be non-undoable")
	_expect(str(ProjectSettings.get_setting(MAIN_SCENE_KEY, "")) == VALID_SCENE, "accepted scene must update in-memory ProjectSettings")
	_restore_main_scene(before)


func _test_save_failure_restores_old_value() -> void:
	var before := _snapshot_main_scene()
	var sentinel := "res://scenes/main/main.tscn"
	ProjectSettings.set_setting(MAIN_SCENE_KEY, sentinel)
	var handler = _new_handler(Callable(self, "_save_fail"))
	var response: Dictionary = handler.call("set_main_scene", {"scene": VALID_SCENE})
	_expect_error_code(response, ErrorCodes.INTERNAL_ERROR, "persistence failure must fail closed")
	_expect(
		str(ProjectSettings.get_setting(MAIN_SCENE_KEY, "")) == sentinel,
		"persistence failure must restore the old in-memory main_scene value",
	)
	_restore_main_scene(before)


func _supports_save_seam() -> bool:
	# Keep the RED parseable while production still has its three-argument
	# constructor. Introspect the instance script instead of spelling a
	# four-argument .new() call that Godot would reject at parse time.
	var probe = ProjectHandlerScript.new(null, null, null)
	var script: Script = probe.get_script()
	for method in script.get_script_method_list():
		if str(method.get("name", "")) == "_init":
			return Array(method.get("args", [])).size() >= 4
	return false


func _new_handler(save_callable: Callable):
	var handler = ProjectHandlerScript.new(null, null, null)
	# Once GREEN adds the approved persistence seam, inject the test Callable
	# dynamically. Constructor arity is locked separately by _supports_save_seam().
	if _has_script_property(handler, "_project_settings_save"):
		handler.set("_project_settings_save", save_callable)
	return handler


func _has_script_property(instance, property_name: String) -> bool:
	for property in instance.get_property_list():
		if str(property.get("name", "")) == property_name:
			return true
	return false


func _save_ok() -> int:
	return OK


func _save_fail() -> int:
	return ERR_CANT_CREATE


func _write_non_scene_tmp() -> bool:
	var file := FileAccess.open(NON_SCENE_TMP, FileAccess.WRITE)
	if file == null:
		failures.append("could not create temporary non-PackedScene resource")
		return false
	file.store_string("[gd_resource type=\"Resource\" format=3]\n\n[resource]\n")
	file.close()
	return true


func _cleanup_non_scene_tmp() -> void:
	var absolute := ProjectSettings.globalize_path(NON_SCENE_TMP)
	if FileAccess.file_exists(NON_SCENE_TMP):
		DirAccess.remove_absolute(absolute)


func _snapshot_main_scene() -> Dictionary:
	var had_setting := ProjectSettings.has_setting(MAIN_SCENE_KEY)
	return {
		"had_setting": had_setting,
		"value": ProjectSettings.get_setting(MAIN_SCENE_KEY) if had_setting else null,
	}


func _restore_main_scene(snapshot: Dictionary) -> void:
	if bool(snapshot.get("had_setting", false)):
		ProjectSettings.set_setting(MAIN_SCENE_KEY, snapshot.get("value"))
	else:
		ProjectSettings.clear(MAIN_SCENE_KEY)


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
