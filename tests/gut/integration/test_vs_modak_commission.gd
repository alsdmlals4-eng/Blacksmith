extends GutTest

const Save = preload("res://scripts/vertical_slice/services/vs_save_service.gd")
const Init = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Modak = preload("res://scripts/vertical_slice/services/vs_modak_growth_service.gd")
const Commission = preload("res://scripts/vertical_slice/services/vs_commission_service.gd")
const Day = preload("res://scripts/vertical_slice/services/vs_recovery_order_service.gd")
const App = preload("res://scenes/vertical_slice/vertical_slice_app.tscn")
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

func _app(source, backend = null):
	var app = App.instantiate()
	add_child_autofree(app)
	var stock = source.resource_snapshot()
	var resources = load("res://scripts/economy/workshop_resources.gd").new(stock.gold, stock.material_stock)
	assert_true(app.configure_campaign(source, resources, null, null, save if backend == null else backend))
	return app

func test_real_enhancement_destruction_and_blocked_write_show_correct_companion_reaction():
	var source = _ready_order()
	assert_eq(Modak.new().join(source, save).status, "APPLIED")
	source = save.load_envelope()
	var uid = source.active_run.commission.active_order.item_uid
	var item = source.get_item(uid)
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	item.used_precision_milestones.append(10)
	item.catalyst_affix.tags = {"BURST_OUTPUT":1}
	item.current_durability = 1
	assert_eq(save.save_envelope(source), OK)
	var app = _app(save.load_envelope())
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	var panel = workshop.get_node("WorkshopScroll/WorkshopLayout/ForgeCompanion")
	var result = workshop.request_enhancement_with_rolls({"success_roll_percent":99.0, "damage_roll_percent":0.0})
	assert_eq(result.outcome, "FAILED_DAMAGE")
	assert_eq(result.physical_state, "DESTROYED")
	assert_true(save.load_envelope().destroyed_history_by_uid.has(uid))
	assert_true(panel.get_node("Reaction").text.contains("다음 작품"), "destruction is not merely a crack")
	panel.present_committed_result("prior", "SUCCESS")
	workshop.request_enhancement_with_rolls({"success_roll_percent":0.0, "damage_roll_percent":99.0})
	assert_false(panel.get_node("Reaction").text.contains("더 튼튼"), "blocked next action clears stale celebration")

func test_workshop_uncertain_join_guard_unlocks_on_unchanged_readback():
	var fault = load("res://tests/gut/unit/vertical_slice/test_vs_forge_companion_panel.gd").MissingImmediateReadback.new()
	fault.real = save
	var app = _app(save.load_envelope(), fault)
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	var panel = workshop.get_node("WorkshopScroll/WorkshopLayout/ForgeCompanion")
	panel.request_join()
	assert_true(workshop.campaign_write_blocked())
	assert_true(workshop.get_node("WorkshopScroll/WorkshopLayout/CommissionPanel/Accept").disabled)
	panel.confirm_saved_join()
	assert_false(workshop.campaign_write_blocked())
	assert_false(workshop.get_node("WorkshopScroll/WorkshopLayout/CommissionPanel/Accept").disabled)

func test_blocked_handoff_clears_prior_celebration_without_claiming_a_save():
	assert_eq(Modak.new().join(save.load_envelope(), save).status, "APPLIED")
	var source = _ready_order()
	var fault = FaultSave.new()
	fault.real = save
	var app = _app(source, fault)
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	var companion = workshop.get_node("WorkshopScroll/WorkshopLayout/ForgeCompanion")
	var commission = workshop.get_node("WorkshopScroll/WorkshopLayout/CommissionPanel")
	companion.present_committed_result("previous-success", "SUCCESS")
	commission.get_node("Catalyst").select(1)
	watch_signals(commission)
	commission._execute("HANDOFF")
	assert_true(commission.get_node("Message").text.contains("처리하지 못했습니다"))
	assert_false(companion.get_node("Reaction").text.contains("더 튼튼"))
	assert_signal_not_emitted(commission, "campaign_saved")
	assert_eq(save.load_envelope().to_dict(), source.to_dict())
	assert_false(workshop.campaign_write_blocked())
