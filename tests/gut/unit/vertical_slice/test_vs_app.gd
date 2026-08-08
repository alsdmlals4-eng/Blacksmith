extends "res://addons/gut/test.gd"

const APP_PATH := "res://scripts/vertical_slice/ui/vs_app.gd"


func _new_app():
	if not ResourceLoader.exists(APP_PATH):
		return null
	var script = load(APP_PATH)
	if script == null:
		return null
	return script.new()


func test_app_router_surface_exists() -> void:
	assert_true(ResourceLoader.exists(APP_PATH), "Task 2 app router must exist at the approved script path")


func test_workshop_is_initial_state() -> void:
	var app = _new_app()
	assert_true(app != null, "Task 2 app router must load")
	if app == null:
		return
	assert_eq(app.current_state, "WORKSHOP", "Task 2 shell must enter at WORKSHOP")
	app.free()


func test_declared_edge_is_distinct_from_implemented_destination() -> void:
	var app = _new_app()
	assert_true(app != null, "Task 2 app router must load")
	if app == null:
		return
	assert_true(app.can_transition("WORKSHOP", "FORGE"), "WORKSHOP→FORGE must be declared")
	assert_eq(app.transition_to("FORGE"), app.MISSING_DESTINATION, "declared but unimplemented state must fail closed")
	assert_eq(app.current_state, "WORKSHOP", "missing destination must not mutate current state")
	app.free()


func test_undeclared_edge_fails_closed() -> void:
	var app = _new_app()
	assert_true(app != null, "Task 2 app router must load")
	if app == null:
		return
	assert_false(app.can_transition("WORKSHOP", "RESULT"), "WORKSHOP→RESULT must not bypass the declared graph")
	assert_eq(app.transition_to("RESULT"), app.INVALID_TRANSITION, "undeclared edge must fail closed")
	assert_eq(app.current_state, "WORKSHOP", "invalid transition must not mutate current state")
	app.free()
