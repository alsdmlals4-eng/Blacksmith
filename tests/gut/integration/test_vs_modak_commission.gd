extends GutTest

const Save = preload("res://scripts/vertical_slice/services/vs_save_service.gd")
const Init = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Modak = preload("res://scripts/vertical_slice/services/vs_modak_growth_service.gd")
const Commission = preload("res://scripts/vertical_slice/services/vs_commission_service.gd")
const Day = preload("res://scripts/vertical_slice/services/vs_recovery_order_service.gd")
var save

func before_each():
	save = Save.new("user://modak-handoff-" + str(Time.get_ticks_usec()) + ".json")
	assert_eq(save.save_envelope(Init.new().create_replan_candidate_envelope()), OK)

func after_each():
	for path in [save.save_path, save.temp_path, save.backup_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func _ready_order():
	var service = Commission.new()
	var accepted = service.accept(save.load_envelope(), "IRON_SWORD_BASIC_V1", save).envelope
	return service.forge(accepted, accepted.active_run.commission.active_order.order_id,
		{"equipment_id":"iron_sword", "quality_id":"GOOD", "base_attack":21}, save).envelope

class FaultSave extends RefCounted:
	var real
	var commit_then_error = false
	func load_envelope(): return real.load_envelope()
	func save_envelope(value):
		if commit_then_error: real.save_envelope(value)
		return ERR_CANT_CREATE

func test_handoff_and_productive_day_are_one_commit_and_retry_never_double_counts():
	assert_eq(Modak.new().join(save.load_envelope(), save).status, "APPLIED")
	var ready = _ready_order()
	assert_eq(ready.active_run.modak.productive_day_ids, [], "accepting and forging do not count")
	var id = ready.active_run.commission.active_order.order_id
	var fault = FaultSave.new()
	fault.real = save
	var service = Commission.new()
	assert_eq(service.handoff_with_rolls(ready, id, "heart_of_flame", [0, 99], fault).status, "BLOCKED")
	assert_eq(save.load_envelope().to_dict(), ready.to_dict())
	fault.commit_then_error = true
	assert_eq(service.handoff_with_rolls(ready, id, "heart_of_flame", [0, 99], fault).status, "COMMIT_UNCERTAIN")
	var actual = save.load_envelope()
	assert_eq(actual.active_run.modak.productive_day_ids, [1.0])
	assert_eq(actual.active_run.commission.active_order.phase, "IN_TRANSIT")
	assert_eq(service.handoff_with_rolls(ready, id, "heart_of_flame", [0, 99], save).status, "ALREADY_APPLIED")
	assert_eq(save.load_envelope().to_dict(), actual.to_dict())
	assert_eq(ready.active_run.modak.productive_day_ids, [])
	var closed = Day.new().close_day(actual, 1, save).envelope
	assert_eq(closed.active_run.modak.productive_day_ids, [1.0], "report arrival does not count again")
	closed = Day.new().close_day(closed, 2, save).envelope
	assert_eq(closed.active_run.modak.productive_day_ids, [1.0], "empty day does not count")
	var next = _ready_order()
	var next_result = service.handoff_with_rolls(next, next.active_run.commission.active_order.order_id, "earth_crystal", [0, 99], save)
	assert_eq(next_result.envelope.active_run.modak.productive_day_ids, [1.0, 3.0])
	assert_eq(Modak.new().view(next_result.envelope).stage, "EARLY")

func test_unjoined_handoff_and_join_afterwards_never_grant_retroactive_days():
	var ready = _ready_order()
	var delivered = Commission.new().handoff_with_rolls(ready, ready.active_run.commission.active_order.order_id, "earth_crystal", [0, 99], save).envelope
	assert_false(delivered.active_run.has("modak"))
	var joined = Modak.new().join(delivered, save).envelope
	assert_eq(joined.active_run.modak.productive_day_ids, [])
