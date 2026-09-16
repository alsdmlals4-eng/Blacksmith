extends GutTest

const Commission = preload("res://scripts/vertical_slice/services/vs_commission_service.gd")
const Save = preload("res://scripts/vertical_slice/services/vs_save_service.gd")
const Envelope = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const Init = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Day = preload("res://scripts/vertical_slice/services/vs_recovery_order_service.gd")
const App = preload("res://scenes/vertical_slice/vertical_slice_app.tscn")
var save
var service

func before_each():
	save = Save.new("user://commission-loop-" + str(Time.get_ticks_usec()) + ".json")
	service = Commission.new()
	assert_eq(save.save_envelope(Init.new().create_replan_candidate_envelope()), OK)

func after_each():
	for path in [save.save_path, save.save_path + ".tmp", save.save_path + ".bak"]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func _available():
	assert_true(service.has_method("handoff"), "Commission handoff must exist")
	return service.has_method("handoff")

func _ready_order(purpose = false, funding = "COMMISSION_ESCROW", mode = "SALE"):
	var current = save.load_envelope()
	var uid = ""
	if funding == "PLAYER":
		var isolated = Init.new().create_replan_candidate_envelope()
		var born = load("res://scripts/vertical_slice/services/vs_item_birth_service.gd").new().commit_first_forge(isolated,
			{"equipment_id":"iron_sword", "crafting_grade":"CRAFT_SUPERIOR", "base_attack":21, "artistry":3})
		uid = born.item_uid
		assert_eq(current.add_item(born.item), OK)
		current.active_run.selected_item_uid = uid
		assert_eq(save.save_envelope(current), OK)
	current = service.accept(current, "IRON_SWORD_PURPOSE_V1" if purpose else "IRON_SWORD_BASIC_V1", save, funding, mode).envelope
	var id = current.active_run.commission.active_order.order_id
	if funding == "PLAYER":
		current = service.reserve_item(current, id, uid, save).envelope
	else:
		current = service.forge(current, id, {"equipment_id":"iron_sword", "quality_id":"GOOD", "base_attack":21}, save).envelope
	if purpose:
		var item = current.get_item(current.active_run.commission.active_order.item_uid)
		item.enhancement_level = 10
		item.highest_checkpoint = 10
		item.used_precision_milestones.append(10)
		item.catalyst_affix.tags = {"BURST_OUTPUT":1}
		assert_eq(save.save_envelope(current), OK)
	return save.load_envelope()

class UncertainSave extends RefCounted:
	var actual
	var reads = 0
	func _init(value): actual = value
	func load_envelope():
		reads += 1
		return null if reads == 2 else actual.load_envelope()
	func save_envelope(envelope): return actual.save_envelope(envelope)

class FailSave extends RefCounted:
	var actual
	func _init(value): actual = value
	func load_envelope(): return actual.load_envelope()
	func save_envelope(_envelope): return ERR_CANT_OPEN

class UnknownPrewriteSave extends RefCounted:
	var actual
	var reads = 0
	var attempted: Dictionary = {}
	func _init(value): actual = value
	func load_envelope():
		reads += 1
		return actual.load_envelope() if reads == 1 else null
	func save_envelope(envelope):
		attempted = envelope.to_dict()
		return ERR_CANT_OPEN

func test_handoff_catalyst_validation_atomic_payout_and_uncertain_retry():
	if not _available(): return
	var source = _ready_order()
	var id = source.active_run.commission.active_order.order_id
	var before = source.to_dict()
	for catalyst in ["", "unknown"]:
		assert_eq(service.handoff(source, id, catalyst, save).status, "BLOCKED")
	assert_eq(service.handoff(source, id, "heart_of_flame", FailSave.new(save)).status, "BLOCKED")
	assert_eq(save.load_envelope().to_dict(), before)
	var result = service.handoff_with_rolls(source, id, "heart_of_flame", [0,99], UncertainSave.new(save))
	assert_eq(result.status, "COMMIT_UNCERTAIN")
	var paid = save.load_envelope()
	var record = paid.active_run.commission.active_order
	assert_eq(record.phase, "IN_TRANSIT")
	assert_false(record.escrow.reclaimed)
	assert_eq(paid.resource_snapshot().gold, source.resource_snapshot().gold + 400)
	assert_eq(paid.resource_snapshot().material_stock.heart_of_flame, source.resource_snapshot().material_stock.heart_of_flame + 1)
	assert_eq(paid.resource_snapshot().material_stock.common_reinforcement_material, source.resource_snapshot().material_stock.common_reinforcement_material + 2)
	assert_eq(paid.get_item(record.item_uid).current_durability, source.get_item(record.item_uid).current_durability)
	assert_eq(paid.get_item(record.item_uid).owner_id, "CUSTOMER")
	assert_eq(service.handoff(source, id, "heart_of_flame", save).status, "ALREADY_APPLIED")
	assert_eq(service.handoff(source, id, "earth_crystal", save).status, "BLOCKED")
	assert_eq(service.cancel(paid, id, save).status, "BLOCKED")
	assert_eq(save.load_envelope().to_dict(), paid.to_dict())

func test_basic_sale_customer_and_personal_loan_same_uid_due_next_day():
	if not _available(): return
	for mode in ["SALE", "LOAN"]:
		assert_eq(save.save_envelope(Init.new().create_replan_candidate_envelope()), OK)
		var source = _ready_order(false, "PLAYER", mode)
		var id = source.active_run.commission.active_order.order_id
		var uid = source.active_run.commission.active_order.item_uid
		var paid = service.handoff_with_rolls(source, id, "earth_crystal", [99,0], save).envelope
		assert_eq(Day.close_block_reason(paid), "")
		assert_false(service.item_action_allowed(paid, uid, "ENHANCE"))
		assert_eq(paid.active_run.commission.active_order.settlement.due_day, 2)
		var result = Day.new().close_day(paid, 1, save)
		assert_eq(result.status, "APPLIED")
		if not result.has("envelope"): return
		var settled = save.load_envelope()
		assert_eq(settled.active_run.commission.history[0].phase, "SETTLED")
		assert_eq(settled.get_item(uid).owner_id, "PLAYER" if mode == "LOAN" else "CUSTOMER")
		assert_eq(settled.resource_snapshot(), paid.resource_snapshot())
		var report = settled.active_run.commission.history[0].settlement
		assert_true(report.mission_success)
		assert_false(report.damage_applied)
		assert_eq(report.report_kind, "BASIC_CUSTOMER_CHECK")
		assert_eq(Day.new().close_day(paid, 1, save).status, "ALREADY_APPLIED")
		assert_eq(save.load_envelope().to_dict(), settled.to_dict())

func test_purpose_independent_four_results_day_before_due_after_restart():
	if not _available(): return
	for rolls in [[0,0],[0,99],[99,0],[99,99]]:
		assert_eq(save.save_envelope(Init.new().create_replan_candidate_envelope()), OK)
		var source = _ready_order(true)
		var id = source.active_run.commission.active_order.order_id
		var uid = source.active_run.commission.active_order.item_uid
		var paid = service.handoff_with_rolls(source, id, "heart_of_flame", rolls, save).envelope
		for day in [1,2]:
			assert_eq(Day.new().close_day(save.load_envelope(), day, save).status, "APPLIED")
			assert_eq(save.load_envelope().active_run.commission.active_order.phase, "IN_TRANSIT")
		var before_due = save.load_envelope()
		assert_eq(Day.new().close_day(before_due, 3, FailSave.new(save)).status, "BLOCKED")
		assert_eq(save.load_envelope().to_dict(), before_due.to_dict())
		assert_eq(Day.new().close_day(before_due, 3, UncertainSave.new(save)).status, "COMMIT_UNCERTAIN")
		assert_eq(Day.new().close_day(before_due, 3, save).status, "ALREADY_APPLIED")
		var settled = save.load_envelope()
		var report = settled.active_run.commission.history[0].settlement
		assert_eq(report.mission_success, rolls[0] == 0)
		assert_eq(report.damage_applied, rolls[1] == 0)
		assert_eq(settled.get_item(uid).current_durability, source.get_item(uid).current_durability - (1 if rolls[1] == 0 else 0))
		assert_eq(settled.resource_snapshot(), paid.resource_snapshot())
		assert_eq(Day.new().close_day(settled, 4, save).status, "APPLIED")
		assert_eq(save.load_envelope().active_run.commission.history[0].settlement, report)

func test_actual_workshop_commission_controls_visible_with_empty_selection():
	var source = save.load_envelope()
	var app = App.instantiate()
	add_child_autofree(app)
	var stock = source.resource_snapshot()
	var resources = load("res://scripts/economy/workshop_resources.gd").new(stock.gold, stock.material_stock)
	assert_true(app.configure_campaign(source, resources, null, null, save))
	var panel = app.get_node_or_null("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/CommissionPanel")
	assert_not_null(panel, "Actual commission controls must exist without a personal item")
	if panel == null: return
	assert_eq(panel.get_node("Offers").item_count, 10)
	assert_eq(panel.get_node("Funding").item_count, 3)
	panel.get_node("Accept").pressed.emit()
	assert_eq(save.load_envelope().active_run.commission.active_order.phase, "ACCEPTED")
	panel.get_node("Forge").pressed.emit()
	assert_not_null(app.get_node_or_null("GeneralCommissionForge"))

func _app_for(source):
	var app = App.instantiate()
	add_child_autofree(app)
	var stock = source.resource_snapshot()
	assert_true(app.configure_campaign(source, load("res://scripts/economy/workshop_resources.gd").new(stock.gold, stock.material_stock), null, null, save))
	return app

func test_panel_handoff_uncertain_retry_latches_inputs_and_result_view_survives_empty_selection():
	if not _available(): return
	var source = _ready_order()
	var app = _app_for(source)
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	var panel = workshop.get_node("WorkshopScroll/WorkshopLayout/CommissionPanel")
	panel.get_node("Catalyst").select(1)
	panel._save = UncertainSave.new(save)
	panel.get_node("Handoff").pressed.emit()
	assert_true(panel._uncertain)
	assert_true(panel.get_node("Catalyst").disabled)
	var paid = save.load_envelope()
	panel.get_node("Catalyst").select(2)
	panel._save = save
	panel.get_node("Retry").pressed.emit()
	assert_false(panel._uncertain)
	assert_eq(save.load_envelope().to_dict(), paid.to_dict())
	assert_null(workshop._item)
	assert_true(workshop.set_world_view_mode("FOCUS"))
	var report_before = workshop.get_node("WorldReportPanel/ReportScroll/ReportText").text
	assert_true(report_before.contains("고객 소유 유지"))
	assert_true(workshop.set_world_view_mode("COLLAPSED"))
	workshop._on_day_close_pressed()
	workshop._on_day_close_confirmed()
	var settled = save.load_envelope()
	assert_eq(settled.active_run.current_day, 2)
	assert_true(workshop.set_world_view_mode("SPLIT"))
	assert_true(workshop.get_node("WorldReportPanel/ReportScroll/ReportText").text.contains("검수 성공"))
	for mode in ["FOCUS", "COLLAPSED", "SPLIT"]: assert_true(workshop.set_world_view_mode(mode))
	assert_eq(save.load_envelope().to_dict(), settled.to_dict())

func test_day_close_loan_return_refreshes_selected_item_and_uncertain_same_day_retry():
	if not _available(): return
	var source = _ready_order(false, "PLAYER", "LOAN")
	var order = source.active_run.commission.active_order
	var paid = service.handoff_with_rolls(source, order.order_id, "earth_crystal", [0,99], save).envelope
	var app = _app_for(paid)
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	assert_null(workshop._item)
	workshop._save_service = UncertainSave.new(save)
	workshop._on_day_close_pressed()
	workshop._on_day_close_confirmed()
	assert_eq(save.load_envelope().active_run.current_day, 2)
	workshop._save_service = save
	workshop._on_day_close_confirmed()
	assert_eq(save.load_envelope().active_run.current_day, 2)
	assert_not_null(workshop._item, "Verified close refreshes returned same UID")
	if workshop._item != null: assert_eq(workshop._item.uid, order.item_uid)

func test_handoff_rejects_stale_missing_requirement_modes_rolls_and_corrupt_schedules():
	if not _available(): return
	var source = _ready_order(true)
	var order = source.active_run.commission.active_order
	for rolls in [[], [0], [0,100], [-1,0], [true,0], ["0",0], [NAN,0], [INF,0]]:
		assert_eq(service.handoff_with_rolls(source, order.order_id, "earth_crystal", rolls, save).status, "BLOCKED")
	var stale = Envelope.from_dict(source.to_dict())
	stale.workshop_resources.gold -= 1
	assert_eq(service.handoff(stale, order.order_id, "earth_crystal", save).status, "BLOCKED")
	var malformed = Envelope.from_dict(source.to_dict())
	malformed.active_run.commission.active_order.ownership_mode = "LOAN"
	assert_eq(service.handoff(malformed, order.order_id, "earth_crystal", save).status, "BLOCKED")
	assert_eq(save.load_envelope().to_dict(), source.to_dict())
	var paid = service.handoff_with_rolls(source, order.order_id, "earth_crystal", [0,99], save).envelope
	for change in [["schema_version",2],["ruleset_id","unknown"],["policy_id","unknown"],["due_day",1.5],["due_day",99],["success_percent",0],["damage_percent",true],["mission_success",true],["rolls",[0,100]],["event_id","foreign"]]:
		var raw = paid.to_dict()
		raw.active_run.commission.active_order.settlement[change[0]] = change[1]
		assert_false(Envelope.from_dict(raw).validation_errors.is_empty(), str(change))
	var raw = paid.to_dict()
	raw.active_run.commission.active_order.settlement.payout.gold = true
	assert_false(Envelope.from_dict(raw).validation_errors.is_empty())
	raw = paid.to_dict()
	raw.active_run.commission.active_order.settlement.item_snapshot.current_durability = 4.5
	assert_false(Envelope.from_dict(raw).validation_errors.is_empty())
	raw = paid.to_dict()
	raw.items_by_uid[order.item_uid].enhancement_level += 1
	assert_false(Envelope.from_dict(raw).validation_errors.is_empty())
	raw = paid.to_dict()
	var record = raw.active_run.commission.active_order
	record.item_uid = ""
	record.reserve_source_hash = ""
	record.previous_selected_item_uid = ""
	record.escrow.produced_item_uid = null
	record.escrow.consumed_qty = 0
	record.command_sequence -= 1
	raw.active_run.commission.command_sequence -= 1
	assert_false(Envelope.from_dict(raw).validation_errors.is_empty(), "Scheduled order requires a departure item")

func test_uncertain_prewrite_panel_retry_preserves_original_departure_draws():
	if not _available(): return
	var source = _ready_order(true)
	var app = _app_for(source)
	var panel = app.get_node("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/CommissionPanel")
	var failed = UnknownPrewriteSave.new(save)
	panel._save = failed
	panel.get_node("Catalyst").select(1)
	panel.get_node("Handoff").pressed.emit()
	assert_true(panel._uncertain)
	assert_eq(save.load_envelope().to_dict(), source.to_dict())
	panel._save = save
	panel.get_node("Retry").pressed.emit()
	assert_false(panel._uncertain)
	assert_true(Envelope.serialized_equal(save.load_envelope().active_run.commission.active_order.settlement.rolls,
		failed.attempted.active_run.commission.active_order.settlement.rolls), "Uncertain retry must keep original independent draws")

func test_personal_controls_compare_selected_uid_then_reserve_cancel_and_reach_precision_with_reward():
	if not _available(): return
	var source = _ready_order(false, "PLAYER", "SALE")
	var uid = source.active_run.commission.active_order.item_uid
	source = service.cancel(source, source.active_run.commission.active_order.order_id, save).envelope
	var app = _app_for(source)
	var panel = app.get_node("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/CommissionPanel")
	panel.get_node("Funding").select(2)
	panel.get_node("Accept").pressed.emit()
	panel.get_node("ItemChoice").select(1)
	panel.get_node("ItemChoice").item_selected.emit(1)
	assert_true(panel.get_node("Comparison").text.contains(uid), "Accepted personal order compares chosen UID before reservation")
	panel.get_node("Reserve").pressed.emit()
	assert_eq(save.load_envelope().active_run.commission.active_order.item_uid, uid)
	panel.get_node("Cancel").pressed.emit()
	assert_eq(save.load_envelope().get_item(uid).owner_id, "PLAYER")
	# A different customer item earns the next precision catalyst; personal +9 consumes it.
	var current = save.load_envelope()
	current.get_item(uid).enhancement_level = 9
	current.workshop_resources.material_stock.heart_of_flame = 0
	assert_eq(save.save_envelope(current), OK)
	current = service.accept(current, "IRON_SWORD_BASIC_V1", save).envelope
	var id = current.active_run.commission.active_order.order_id
	current = service.forge(current, id, {"equipment_id":"iron_sword", "quality_id":"GOOD", "base_attack":21}, save).envelope
	current = service.handoff_with_rolls(current, id, "heart_of_flame", [0,99], save).envelope
	assert_eq(current.resource_snapshot().material_stock.heart_of_flame, 1)
	var stock = current.resource_snapshot()
	var result = load("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd").new().resolve_and_save_with_rolls(current, uid, 10,
		{"success_roll_percent":0.0, "damage_roll_percent":99.0}, 1,
		load("res://scripts/economy/workshop_resources.gd").new(stock.gold, stock.material_stock), save,
		{"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912", "tag_id":"BURST_OUTPUT"})
	assert_eq(result.outcome, "SUCCESS")
	assert_eq(save.load_envelope().resource_snapshot().material_stock.heart_of_flame, 0)
	assert_eq(save.load_envelope().get_item(uid).enhancement_level, 10)

func test_purpose_minimum_blocks_handoff_and_existing_prepared_trial_still_blocks_close():
	if not _available(): return
	var current = _ready_order(false)
	current.active_run.commission.active_order.definition_snapshot = load("res://scripts/vertical_slice/domain/vs_commission_catalog.gd").by_id("IRON_SWORD_PURPOSE_V1")
	assert_eq(save.save_envelope(current), OK)
	assert_eq(service.handoff(current, current.active_run.commission.active_order.order_id, "heart_of_flame", save).status, "BLOCKED")
	assert_eq(service.cancel(current, current.active_run.commission.active_order.order_id, save).status, "APPLIED")
	current = _ready_order(true, "PLAYER", "LOAN")
	var uid = current.active_run.commission.active_order.item_uid
	current = service.cancel(current, current.active_run.commission.active_order.order_id, save).envelope
	var result = load("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd").new().prepare_world_with_rolls(current, uid, "AR", "OUTPUT", "BURST", [0,99], save)
	assert_eq(result.status, "PREPARED")
	assert_eq(Day.close_block_reason(save.load_envelope()), "PENDING_WORLD_RESULT")
	assert_eq(Day.new().close_day(save.load_envelope(), 1, save).status, "BLOCKED")

func test_settled_history_cannot_omit_uid_snapshot_or_splice_result_and_can_repeat_loan():
	if not _available(): return
	var current = _ready_order(false, "PLAYER", "LOAN")
	var order = current.active_run.commission.active_order
	var uid = order.item_uid
	current = service.handoff_with_rolls(current, order.order_id, "heart_of_flame", [0,99], save).envelope
	current = Day.new().close_day(current, 1, save).envelope
	var raw = current.to_dict()
	var old = raw.active_run.commission.history[0]
	old.item_uid = ""
	old.reserve_source_hash = ""
	old.previous_selected_item_uid = ""
	old.command_sequence -= 1
	raw.active_run.commission.command_sequence -= 1
	assert_false(Envelope.from_dict(raw).validation_errors.is_empty(), "Settled history cannot bypass validation by erasing UID")
	for field in ["mission_success", "damage_applied"]:
		raw = current.to_dict()
		raw.active_run.commission.history[0].settlement[field] = not raw.active_run.commission.history[0].settlement[field]
		assert_false(Envelope.from_dict(raw).validation_errors.is_empty())
	var first_report = current.active_run.commission.history[0].duplicate(true)
	current = service.accept(current, "IRON_SWORD_BASIC_V1", save, "PLAYER", "LOAN").envelope
	var id = current.active_run.commission.active_order.order_id
	current = service.reserve_item(current, id, uid, save).envelope
	current = service.handoff_with_rolls(current, id, "earth_crystal", [99,0], save).envelope
	current = Day.new().close_day(current, 2, save).envelope
	assert_eq(current.active_run.commission.history.size(), 2)
	assert_eq(current.active_run.commission.history[0], first_report)
	assert_eq(current.get_item(uid).owner_id, "PLAYER")
	assert_eq(current.items_by_uid.size(), 1)
