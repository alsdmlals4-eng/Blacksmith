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
	assert_false(report_before.contains("아직 저장된 세계 사건이 없습니다"), "A commission report replaces the empty placeholder")
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

func test_uncertain_handoff_blocks_competing_workshop_writes_and_preserves_retry():
	var source = _ready_order(false, "PLAYER", "LOAN")
	var app = _app_for(source)
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	var panel = workshop.get_node("WorkshopScroll/WorkshopLayout/CommissionPanel")
	var unknown = UnknownPrewriteSave.new(save)
	panel._save = unknown
	panel.get_node("Catalyst").select(1)
	panel.get_node("Handoff").pressed.emit()
	assert_true(panel._uncertain)
	var draws = panel._pending.rolls.duplicate()
	var before = FileAccess.get_file_as_string(save.save_path)
	workshop._on_day_close_pressed()
	workshop._on_day_close_confirmed()
	if workshop.has_node("DayCloseConfirmation"): workshop.get_node("DayCloseConfirmation").hide()
	workshop._on_catalyst_exchange_pressed("heart_of_flame")
	workshop._on_catalyst_exchange_confirmed()
	if workshop.has_node("CatalystExchangeConfirmation"): workshop.get_node("CatalystExchangeConfirmation").hide()
	workshop._on_recovery_order_pressed()
	workshop.request_enhancement_with_rolls({"success_roll_percent":0.0, "damage_roll_percent":99.0})
	workshop.request_repair_with_rolls({})
	workshop._on_aqueduct_pressed()
	app._on_recovery_forge_requested()
	assert_null(app.get_node_or_null("RecoveryForge"))
	assert_true(FileAccess.get_file_as_string(save.save_path) == before, "Other UI commands cannot stale the uncertain source")
	assert_true(workshop.get_node("WorkshopScroll/WorkshopLayout/RecoveryOrder/DayClose").disabled)
	assert_true(workshop.get_node("WorkshopScroll/WorkshopLayout/EnhancementButton").disabled)
	assert_eq(app.transition_to("FORGE"), "INVALID_TRANSITION")
	assert_eq(app.begin_item_chronicle(), "OK", "Read-only Chronicle remains reachable")
	app.get_node("ScreenHost/ItemChronicleScreen/ChronicleMargin/ChronicleLayout/WorkshopReturnButton").pressed.emit()
	assert_true(panel.get_node("Retry").is_visible_in_tree(), "Read-only navigation returns to the same pending command")
	panel._save = save
	panel.get_node("Retry").pressed.emit()
	assert_false(panel._uncertain)
	if panel._uncertain: return
	var paid = save.load_envelope()
	assert_eq(paid.active_run.current_day, 1)
	assert_eq(paid.resource_snapshot().gold, source.resource_snapshot().gold + 400)
	assert_eq(JSON.stringify(paid.active_run.commission.active_order.settlement.rolls), JSON.stringify(draws))
	panel.get_node("Retry").pressed.emit()
	assert_eq(save.load_envelope().to_dict(), paid.to_dict())

func test_uncertain_close_blocks_commission_and_keeps_same_day_recheck_reachable():
	var source = _ready_order(false, "PLAYER", "LOAN")
	var app = _app_for(source)
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	var panel = workshop.get_node("WorkshopScroll/WorkshopLayout/CommissionPanel")
	workshop._save_service = UnknownPrewriteSave.new(save)
	workshop._on_day_close_pressed()
	workshop._on_day_close_confirmed()
	assert_true(workshop._day_close_uncertain)
	if workshop.has_node("DayCloseConfirmation"): workshop.get_node("DayCloseConfirmation").hide()
	var before = FileAccess.get_file_as_string(save.save_path)
	panel._save = save
	panel.get_node("Catalyst").select(1)
	panel.get_node("Handoff").pressed.emit()
	panel.get_node("Cancel").pressed.emit()
	workshop._save_service = save
	workshop._on_recovery_order_pressed()
	workshop._on_catalyst_exchange_pressed("earth_crystal")
	workshop._on_catalyst_exchange_confirmed()
	workshop.request_enhancement_with_rolls({"success_roll_percent":0.0, "damage_roll_percent":99.0})
	if workshop.has_node("CatalystExchangeConfirmation"): workshop.get_node("CatalystExchangeConfirmation").hide()
	assert_true(FileAccess.get_file_as_string(save.save_path) == before)
	assert_false(workshop.get_node("WorkshopScroll/WorkshopLayout/RecoveryOrder/DayClose").disabled)
	assert_true(panel.get_node("Handoff").disabled)
	workshop._on_day_close_pressed()
	workshop._on_day_close_confirmed()
	assert_false(workshop._day_close_uncertain)
	assert_eq(save.load_envelope().active_run.current_day, 2)
	workshop._on_day_close_confirmed()
	assert_eq(save.load_envelope().active_run.current_day, 2)

func test_customer_finished_cancel_requires_confirmation_and_discloses_uid_costs():
	var source = _ready_order()
	var uid = source.active_run.commission.active_order.item_uid
	var app = _app_for(source)
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	assert_eq(workshop.request_enhancement_with_rolls({"success_roll_percent":0.0, "damage_roll_percent":99.0}).outcome, "SUCCESS")
	source = save.load_envelope()
	assert_eq(source.get_item(uid).enhancement_level, 1)
	var panel = app.get_node("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/CommissionPanel")
	var before = FileAccess.get_file_as_string(save.save_path)
	panel.get_node("Cancel").pressed.emit()
	assert_true(FileAccess.get_file_as_string(save.save_path) == before, "Opening cancellation cannot transfer ownership")
	var dialog = panel.get_node_or_null("CancelConfirmation")
	assert_not_null(dialog)
	if dialog == null: return
	assert_true(dialog.dialog_text.contains(uid))
	assert_true(dialog.dialog_text.contains("환급 없음"))
	dialog.canceled.emit()
	dialog.hide()
	assert_eq(FileAccess.get_file_as_string(save.save_path), before)
	panel.get_node("Cancel").pressed.emit()
	dialog.confirmed.emit()
	dialog.hide()
	assert_eq(save.load_envelope().get_item(uid).owner_id, "CUSTOMER")
	assert_eq(save.load_envelope().get_item(uid).enhancement_level, 1, "Personally purchased enhancement stays on returned customer UID")
	assert_eq(save.load_envelope().resource_snapshot(), source.resource_snapshot())

func test_offer_risk_and_cancellation_copy_follow_funding_and_phase():
	var app = _app_for(save.load_envelope())
	var panel = app.get_node("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/CommissionPanel")
	assert_true(panel.get_node("Summary").text.contains("비전투"))
	assert_true(panel.get_node("Summary").text.contains("성공 100.0% / 손상 0.0%"))
	panel.get_node("Offers").select(1)
	panel.get_node("Offers").item_selected.emit(1)
	assert_true(panel.get_node("Summary").text.contains("HIGH"))
	panel.get_node("Accept").pressed.emit()
	assert_true(panel.get_node("Cancel").text.contains("미사용 재료 반환"))
	panel.get_node("Cancel").pressed.emit()
	assert_true(save.load_envelope().active_run.commission.active_order.is_empty())
	panel.get_node("Funding").select(2)
	panel.get_node("Accept").pressed.emit()
	assert_true(panel.get_node("Cancel").text.contains("개인 작품 배정만 해제"))
	panel.get_node("Cancel").pressed.emit()
	assert_true(save.load_envelope().active_run.commission.active_order.is_empty())

func test_offer_and_prepared_risk_are_visible_pure_and_match_departure():
	var source = _ready_order(true, "PLAYER", "LOAN")
	var uid = source.active_run.commission.active_order.item_uid
	var app = _app_for(source)
	var panel = app.get_node("ScreenHost/WorkshopScreen/WorkshopScroll/WorkshopLayout/CommissionPanel")
	var before = FileAccess.get_file_as_string(save.save_path)
	var summary = panel.get_node("Summary").text
	assert_true(summary.contains("HIGH"), "Purpose risk must be disclosed before handoff")
	assert_true(summary.contains("손상 40.0%"))
	assert_true(summary.contains("독립"))
	assert_true(summary.contains("시험값"))
	assert_true(service.has_method("handoff_preview"))
	if not service.has_method("handoff_preview"): return
	var preview = service.handoff_preview(source.active_run.commission.active_order.definition_snapshot, source.get_item(uid))
	var changed = Envelope.from_dict(source.to_dict())
	changed.get_item(uid).current_durability = 1
	changed.get_item(uid).enhancement_level = 20
	changed.get_item(uid).catalyst_affix.tags = {"BURST_OUTPUT":2}
	var prepared = service.handoff_preview(changed.active_run.commission.active_order.definition_snapshot, changed.get_item(uid))
	assert_ne(prepared.damage_percent, preview.damage_percent)
	assert_ne(prepared.success_percent, preview.success_percent)
	panel._refresh()
	assert_eq(FileAccess.get_file_as_string(save.save_path), before)
	assert_true(panel._pending.is_empty())
	var paid = service.handoff_with_rolls(source, source.active_run.commission.active_order.order_id, "heart_of_flame", [0,99], save).envelope
	assert_eq(preview.success_percent, paid.active_run.commission.active_order.settlement.success_percent)
	assert_eq(preview.damage_percent, paid.active_run.commission.active_order.settlement.damage_percent)
	var basic = service.handoff_preview(load("res://scripts/vertical_slice/domain/vs_commission_catalog.gd").by_id("IRON_SWORD_BASIC_V1"), null)
	assert_eq(basic.success_percent, 100.0)
	assert_eq(basic.damage_percent, 0.0)

func test_thirty_mixed_catalog_commissions_keep_uid_balances_and_close_idempotent():
	var definitions = load("res://scripts/vertical_slice/domain/vs_commission_catalog.gd").all()
	var initial = save.load_envelope().resource_snapshot()
	var seen_uids: Array = []
	for cycle in range(30):
		var definition = definitions[cycle % definitions.size()]
		var loan = (cycle + floori(float(cycle) / 10.0)) % 2 == 1
		var current = save.load_envelope()
		var uid = ""
		if loan:
			var birth = load("res://scripts/vertical_slice/services/vs_item_birth_service.gd").new().commit_first_forge(
				Init.new().create_replan_candidate_envelope(), {"equipment_id":definition.equipment_id,
				"crafting_grade":"CRAFT_SUPERIOR", "base_attack":21, "artistry":3})
			uid = birth.item_uid
			assert_eq(current.add_item(birth.item), OK)
			current.active_run.selected_item_uid = uid
			assert_eq(save.save_envelope(current), OK)
		current = service.accept(current, definition.definition_id, save, "PLAYER" if loan else "COMMISSION_ESCROW", "LOAN" if loan else "SALE").envelope
		var id = current.active_run.commission.active_order.order_id
		if loan:
			current = service.reserve_item(current, id, uid, save).envelope
		else:
			current = service.forge(current, id, {"equipment_id":definition.equipment_id, "quality_id":"GOOD", "base_attack":21}, save).envelope
		uid = current.active_run.commission.active_order.item_uid
		assert_false(uid in seen_uids)
		seen_uids.append(uid)
		if definition.min_level > 0:
			var item = current.get_item(uid)
			item.enhancement_level = 10
			item.highest_checkpoint = 10
			item.used_precision_milestones.append(10)
			item.catalyst_affix.tags = {"BURST_OUTPUT":1}
			assert_eq(save.save_envelope(current), OK)
		var paid = service.handoff_with_rolls(current, id, "heart_of_flame" if not loan else "earth_crystal", [0,99], save)
		assert_eq(paid.status, "APPLIED", "Cycle %d handoff" % cycle)
		if not paid.has("envelope"): return
		assert_eq(service.handoff_with_rolls(current, id, "heart_of_flame" if not loan else "earth_crystal", [0,99], save).status, "ALREADY_APPLIED")
		current = paid.envelope
		var due_day = current.active_run.commission.active_order.settlement.due_day
		while current.active_run.current_day < due_day:
			var day = int(current.active_run.current_day)
			var closed = Day.new().close_day(current, day, save)
			assert_eq(closed.status, "APPLIED")
			assert_eq(Day.new().close_day(current, day, save).status, "ALREADY_APPLIED")
			current = save.load_envelope()
		assert_eq(current.items_by_uid.size(), cycle + 1)
		assert_eq(current.active_run.commission.history.size(), cycle + 1)
		assert_eq(current.get_item(uid).owner_id, "PLAYER" if loan else "CUSTOMER")
		assert_eq(current.get_item(uid).current_durability, 5)
		assert_eq(current.resource_snapshot().gold, initial.gold + 400 * (cycle + 1))
		assert_eq(current.resource_snapshot().material_stock.common_reinforcement_material, initial.material_stock.common_reinforcement_material + 2 * (cycle + 1))
	var final = save.load_envelope()
	assert_eq(final.resource_snapshot().material_stock.heart_of_flame, initial.material_stock.heart_of_flame + 15)
	assert_eq(final.resource_snapshot().material_stock.earth_crystal, initial.material_stock.earth_crystal + 15)
	assert_true(final.validation_errors.is_empty())

func test_returned_loan_chronicle_reads_handoff_result_and_reopens_without_write():
	var source = _ready_order(false, "PLAYER", "LOAN")
	var order = source.active_run.commission.active_order
	source = service.handoff_with_rolls(source, order.order_id, "earth_crystal", [0,99], save).envelope
	source = Day.new().close_day(source, 1, save).envelope
	var app = _app_for(source)
	var before = FileAccess.get_file_as_string(save.save_path)
	for repeat in range(2):
		app.begin_item_chronicle()
		var chronicle = app.get_node("ScreenHost/ItemChronicleScreen")
		var text = chronicle.get_node("ChronicleMargin/ChronicleLayout/EntriesLabel").text
		assert_true(text.contains("대여"))
		assert_true(text.contains("인계"))
		assert_true(text.contains("검수 성공"))
		assert_true(text.contains("손상 없음"))
		assert_true(text.contains("같은 UID 반환"))
		assert_eq(chronicle.view_state().item_uid, order.item_uid)
		chronicle.get_node("ChronicleMargin/ChronicleLayout/WorkshopReturnButton").pressed.emit()
	assert_eq(FileAccess.get_file_as_string(save.save_path), before)
