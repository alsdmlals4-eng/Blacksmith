extends "res://addons/gut/test.gd"

const REPOSITORY_PATH := "res://scripts/vertical_slice/services/vs_customer_profile_repository.gd"


func _repository_script():
	return load(REPOSITORY_PATH) if ResourceLoader.exists(REPOSITORY_PATH) else null


func test_repository_loads_only_the_registered_current_nadia_profile() -> void:
	var script = _repository_script()
	assert_not_null(script, "the current customer handoff must read its registered profile through one repository")
	if script == null:
		return
	var loaded: Dictionary = script.new().load_profile("NADIA_VENN")
	assert_eq(loaded.get("status", ""), "APPLIED")
	var profile = loaded.get("profile", null)
	assert_not_null(profile)
	if profile == null:
		return
	assert_eq(profile.customer_id, "NADIA_VENN")
	assert_eq(profile.name, "나디아 벤")
	assert_eq(profile.work_request_summary_ko(), "생환과 회수를 위한 탐사")


func test_repository_fails_closed_for_an_unregistered_customer_without_directory_discovery() -> void:
	var script = _repository_script()
	assert_not_null(script)
	if script == null:
		return
	assert_eq(
		script.new().load_profile("UNREGISTERED_CUSTOMER"),
		{"status": "BLOCKED", "reason": "UNKNOWN_CUSTOMER_ID"}
	)
