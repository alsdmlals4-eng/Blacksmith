extends GutTest

const Commission = preload("res://scripts/vertical_slice/services/vs_commission_service.gd")
const Envelope = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const Save = preload("res://scripts/vertical_slice/services/vs_save_service.gd")
const Init = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Resources = preload("res://scripts/economy/workshop_resources.gd")
const Enhancement = preload("res://scripts/vertical_slice/services/vs_enhancement_action_service.gd")
const Maintenance = preload("res://scripts/vertical_slice/services/vs_workshop_maintenance_service.gd")
const World = preload("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd")
const AppScene = preload("res://scenes/vertical_slice/vertical_slice_app.tscn")
var save
var service

func before_each():
	save = Save.new("user://commission-forge-" + str(Time.get_ticks_usec()) + ".json")
	service = Commission.new()
	assert_eq(save.save_envelope(Init.new().create_replan_candidate_envelope()), OK)

func after_each():
	for path in [save.save_path, save.save_path + ".tmp", save.save_path + ".bak"]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func _available() -> bool:
	assert_true(service.has_method("forge"), "Commission forge must exist")
	assert_true(service.has_method("item_action_allowed"), "Shared item ownership guard must exist")
	return service.has_method("forge") and service.has_method("item_action_allowed")

func _completion(equipment = "iron_sword") -> Dictionary:
	return {"equipment_id":equipment, "quality_id":"GOOD", "base_attack":21, "tap_count":27,
		"fever_activation_count":0, "fever_bonus_applied":false}

func _accepted():
	return service.accept(save.load_envelope(), "IRON_SWORD_BASIC_V1", save).envelope

func _resources(envelope):
	var state = envelope.resource_snapshot()
	return Resources.new(state.gold, state.material_stock)

func test_customer_forge_consumes_escrow_once_and_retry_survives_reload():
	if not _available(): return
	var source = _accepted()
	var id = source.active_run.commission.active_order.order_id
	var before = source.resource_snapshot()
	var result = service.forge(source, id, _completion(), save)
	assert_eq(result.status, "APPLIED")
	if not result.has("envelope"): return
	var current = save.load_envelope()
	var order = current.active_run.commission.active_order
	assert_eq(order.phase, "READY")
	assert_eq(order.escrow.consumed_qty, 1)
	assert_eq(order.escrow.produced_item_uid, order.item_uid)
	assert_eq(order.command_sequence, 2)
	assert_eq(current.active_run.selected_item_uid, order.item_uid)
	assert_eq(current.get_item(order.item_uid).owner_id, "CUSTOMER_COMMISSION_RESERVED")
	assert_eq(current.resource_snapshot(), before)
	assert_eq(source.items_by_uid.size(), 0)
	assert_eq(service.forge(source, id, _completion(), save).status, "ALREADY_APPLIED")
	assert_eq(service.forge(current, id, _completion(), save).status, "ALREADY_APPLIED")
	assert_eq(save.load_envelope().items_by_uid.size(), 1)
	var different = _completion()
	different.tap_count = 28
	assert_eq(service.forge(source, id, different, save).status, "BLOCKED")

func test_mismatched_invalid_stale_and_consumed_forge_never_write():
	if not _available(): return
	var source = _accepted()
	var id = source.active_run.commission.active_order.order_id
	for completion in [_completion("iron_shield"), {}, {"equipment_id":"iron_sword", "quality_id":"GOOD", "base_attack":21.5}, {"equipment_id":"iron_sword", "quality_id":"GOOD", "base_attack":true}]:
		assert_eq(service.forge(source, id, completion, save).status, "BLOCKED")
	var stale = Envelope.from_dict(source.to_dict())
	stale.workshop_resources.gold -= 1
	assert_eq(service.forge(stale, id, _completion(), save).status, "BLOCKED")
	assert_eq(service.forge(source, "", _completion(), save).status, "BLOCKED")
	assert_eq(save.load_envelope().to_dict(), source.to_dict())
	assert_eq(service.cancel(source, id, save).status, "APPLIED")
	assert_eq(service.forge(source, id, _completion(), save).status, "BLOCKED")
	assert_eq(save.load_envelope().items_by_uid.size(), 0)

class UncertainSave extends RefCounted:
	var actual
	var reads = 0
	func _init(value): actual = value
	func load_envelope():
		reads += 1
		return null if reads == 2 else actual.load_envelope()
	func save_envelope(envelope): return actual.save_envelope(envelope)

class UnavailableSave extends RefCounted:
	func load_envelope(): return null
	func save_envelope(_envelope): return ERR_CANT_OPEN

func test_postwrite_uncertainty_retry_keeps_original_uid():
	if not _available(): return
	var source = _accepted()
	var id = source.active_run.commission.active_order.order_id
	var result = service.forge(source, id, _completion(), UncertainSave.new(save))
	assert_eq(result.status, "COMMIT_UNCERTAIN")
	assert_false(result.has("envelope"))
	var uid = save.load_envelope().active_run.selected_item_uid
	assert_eq(service.forge(source, id, _completion(), save).status, "ALREADY_APPLIED")
	assert_eq(save.load_envelope().active_run.selected_item_uid, uid)
	assert_eq(save.load_envelope().items_by_uid.size(), 1)

func test_reserved_permissions_personal_costs_and_customer_direct_service_denial():
	if not _available(): return
	var source = _accepted()
	var id = source.active_run.commission.active_order.order_id
	var current = service.forge(source, id, _completion(), save).envelope
	var uid = current.active_run.selected_item_uid
	for action in ["ENHANCE", "REPAIR", "HANDOFF"]:
		assert_true(service.item_action_allowed(current, uid, action), action)
	for action in ["INDEPENDENT_WORLD", "RESERVE", "SELL", ""]:
		assert_false(service.item_action_allowed(current, uid, action), action)
	var before = current.resource_snapshot()
	var result = Enhancement.new().resolve_and_save_with_rolls(current, uid, 1,
		{"success_roll_percent":0.0, "damage_roll_percent":99.0}, 1, _resources(current), save)
	assert_eq(result.outcome, "SUCCESS")
	current = save.load_envelope()
	assert_lt(current.resource_snapshot().gold, before.gold)
	assert_eq(current.active_run.commission.active_order.escrow.consumed_qty, 1)
	assert_eq(World.new().prepare_aqueduct_with_rolls(current, uid, "OUTPUT", "BURST", [0,99], save, "AR").reason, "COMMISSION_ACTION_NOT_ALLOWED")
	assert_eq(World.new().resolve_and_save_with_roll(current, uid, {}, 0, save).reason, "COMMISSION_ACTION_NOT_ALLOWED")
	current = service.cancel(current, id, save).envelope
	var frozen = current.to_dict()
	assert_eq(Enhancement.new().resolve_and_save_with_rolls(current, uid, 2, {}, 1, _resources(current), save).reason, "COMMISSION_ACTION_NOT_ALLOWED")
	assert_eq(Enhancement.new().backfill_precision_tag_and_save(current, uid, {}, save).reason, "COMMISSION_ACTION_NOT_ALLOWED")
	assert_eq(Maintenance.new().repair_and_save(current, uid, _resources(current), save).reason, "COMMISSION_ACTION_NOT_ALLOWED")
	assert_eq(World.new().resolve_and_save_with_roll(current, uid, {}, 0, save).reason, "COMMISSION_ACTION_NOT_ALLOWED")
	assert_eq(save.load_envelope().to_dict(), frozen)

func test_native_forge_locks_equipment_cancel_keeps_order_and_failed_commit_retries():
	if not _available(): return
	var source = _accepted()
	var id = source.active_run.commission.active_order.order_id
	var app = AppScene.instantiate()
	add_child_autofree(app)
	assert_true(app.configure_campaign(source, _resources(source), null, null, save))
	var workshop = app.get_node("ScreenHost/WorkshopScreen")
	assert_true(workshop.has_signal("commission_forge_requested"))
	if not workshop.has_signal("commission_forge_requested"): return
	workshop.commission_forge_requested.emit(id)
	var forge = app.get_node_or_null("GeneralCommissionForge")
	assert_not_null(forge)
	if forge == null: return
	assert_eq(forge.selected_equipment_id(), "iron_sword")
	assert_false(forge.find_child("EquipmentChoicePanel", true, false).visible)
	app._close_commission_forge()
	assert_eq(save.load_envelope().to_dict(), source.to_dict())
	workshop.commission_forge_requested.emit(id)
	forge = app.get_node("GeneralCommissionForge")
	forge._completed_result = _completion()
	app._save_service = UncertainSave.new(save)
	forge._on_result_commit_pressed()
	assert_not_null(app.get_node_or_null("GeneralCommissionForge"))
	assert_eq(forge._completed_result, _completion())
	assert_false(forge.result_commit_button.disabled)
	app._save_service = UnavailableSave.new()
	forge._on_result_commit_pressed()
	assert_true(forge.get_node("CommissionBack").disabled, "Unknown commit remains locked until verified, even after read failure")
	app._close_commission_forge()
	assert_not_null(app.get_node_or_null("GeneralCommissionForge"))
	if app.get_node_or_null("GeneralCommissionForge") == null: return
	app._save_service = save
	forge._on_result_commit_pressed()
	assert_null(app.get_node_or_null("GeneralCommissionForge"))
	assert_eq(workshop._item.uid, save.load_envelope().active_run.selected_item_uid)
	var cancelled = service.cancel(save.load_envelope(), id, save).envelope
	assert_true(app.configure_campaign(cancelled, _resources(cancelled), null, null, save))
	assert_false(workshop.view_state().has_item, "Only customer items remain: safe empty workshop")

func test_stale_player_source_cannot_overwrite_disk_reservation_from_other_services():
	if not _available(): return
	var source = save.load_envelope()
	var born = load("res://scripts/vertical_slice/services/vs_item_birth_service.gd").new().commit_first_forge(source,
		{"equipment_id":"iron_sword", "crafting_grade":"CRAFT_SUPERIOR", "base_attack":21, "artistry":3})
	assert_eq(save.save_envelope(source), OK)
	var uid = born.item_uid
	var accepted = service.accept(source, "IRON_SWORD_BASIC_V1", save, "PLAYER", "SALE").envelope
	assert_eq(service.reserve_item(accepted, accepted.active_run.commission.active_order.order_id, uid, save).status, "APPLIED")
	var before = save.load_envelope().to_dict()
	# Guard must reject stale state before event validation, not merely an invalid fixture event.
	assert_eq(World.new().resolve_and_save_with_roll(source, uid, {}, 0, save).reason, "ACTUAL_USE_SAVE_DIVERGED")
	assert_eq(Enhancement.new().backfill_precision_tag_and_save(source, uid, {}, save).reason, "ENHANCEMENT_SAVE_DIVERGED")
	assert_eq(save.load_envelope().to_dict(), before)

func test_customer_commission_reaches_precision_with_personal_resources_then_repairs():
	if not _available(): return
	var source = _accepted()
	var id = source.active_run.commission.active_order.order_id
	var current = service.forge(source, id, _completion(), save).envelope
	var uid = current.active_run.selected_item_uid
	var initial_resources = current.resource_snapshot()
	for target in range(1, 11):
		var selection = {"ruleset_id":"BLACKSMITH_REPLAN_TAGS_20260912", "tag_id":"BURST_OUTPUT"} if target == 10 else {}
		var result = Enhancement.new().resolve_and_save_with_rolls(current, uid, target,
			{"success_roll_percent":0.0, "damage_roll_percent":99.0}, 1, _resources(current), save, selection)
		assert_eq(result.outcome, "SUCCESS", "Customer commission target " + str(target))
		if not result.has("envelope"): return
		current = save.load_envelope()
	assert_eq(current.get_item(uid).enhancement_level, 10)
	assert_eq(current.get_item(uid).catalyst_affix.tags.BURST_OUTPUT, 1)
	assert_lt(current.resource_snapshot().gold, initial_resources.gold)
	assert_eq(current.active_run.commission.active_order.command_sequence, 2)
	assert_eq(service.forge(source, id, _completion(), save).status, "ALREADY_APPLIED")
	current.get_item(uid).apply_damage_event()
	assert_eq(save.save_envelope(current), OK)
	var damaged = current.get_item(uid).current_durability
	var repaired = Maintenance.new().repair_and_save(current, uid, _resources(current), save,
		{"quality_roll_percent":0.0, "scar_roll_percent":99.0})
	assert_eq(repaired.status, "APPLIED")
	assert_gt(save.load_envelope().get_item(uid).current_durability, damaged)
	var app = AppScene.instantiate()
	add_child_autofree(app)
	current = save.load_envelope()
	assert_true(app.configure_campaign(current, _resources(current), null, null, save))
	assert_eq(app.begin_phase1_customer_handoff(), "COMMISSION_ACTION_NOT_ALLOWED")
	assert_false(app.get_node("ScreenHost/WorkshopScreen").view_state().handoff_allowed)
