extends GutTest

const SERVICE_PATH = "res://scripts/vertical_slice/services/vs_commission_service.gd"
const Envelope = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const Save = preload("res://scripts/vertical_slice/services/vs_save_service.gd")
const Initializer = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Birth = preload("res://scripts/vertical_slice/services/vs_item_birth_service.gd")
var save
var service
var paths: Array[String] = []

func before_each():
	var path = "user://commission-test-" + str(Time.get_ticks_usec()) + ".json"
	paths.append_array([path, path + ".tmp", path + ".bak"])
	save = Save.new(path)
	assert_eq(save.save_envelope(Initializer.new().create_replan_candidate_envelope()), OK)
	service = load(SERVICE_PATH).new() if ResourceLoader.exists(SERVICE_PATH) else null

func after_each():
	for path in paths:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	paths.clear()

func _available() -> bool:
	assert_not_null(service, "Commission transaction service must exist")
	return service != null

func _item(envelope, equipment = "iron_sword"):
	var born = Birth.new().commit_first_forge(envelope, {"equipment_id":equipment,
		"crafting_grade":"CRAFT_SUPERIOR", "base_attack":10, "artistry":3})
	assert_eq(born.status, "APPLIED")
	return born.item

func test_accept_disk_retry_and_thirty_cancel_cycles_have_no_player_income():
	if not _available(): return
	var before = save.load_envelope().resource_snapshot()
	for index in range(30):
		var original = save.load_envelope()
		var result = service.accept(original, "IRON_SWORD_BASIC_V1", save)
		assert_eq(result.status, "APPLIED")
		if result.status != "APPLIED": return
		var order = result.envelope.active_run.commission.active_order
		assert_eq(order.order_id, original.active_run.run_id + "-commission-" + str(index + 1))
		assert_eq(order.escrow.allocated_qty, 1)
		assert_eq(save.load_envelope().resource_snapshot(), before)
		var retry = service.accept(original, "IRON_SWORD_BASIC_V1", save)
		assert_eq(retry.status, "ALREADY_APPLIED")
		assert_eq(retry.envelope.active_run.commission.active_order.order_id, order.order_id)
		assert_eq(service.cancel(save.load_envelope(), order.order_id, save).status, "APPLIED")
		assert_eq(service.cancel(result.envelope, order.order_id, save).status, "ALREADY_APPLIED")
		assert_eq(save.load_envelope().resource_snapshot(), before)
		assert_eq(service.accept(original, "IRON_SWORD_BASIC_V1", save).status, "BLOCKED")

func test_accept_rejects_stale_other_run_backup_and_different_mode_retries():
	if not _available(): return
	var original = save.load_envelope()
	var stale = Envelope.from_dict(original.to_dict())
	stale.workshop_resources.gold -= 1
	assert_eq(service.accept(stale, "IRON_SWORD_BASIC_V1", save).status, "BLOCKED")
	assert_eq(service.accept(Initializer.new().create_replan_candidate_envelope(), "IRON_SWORD_BASIC_V1", save).status, "BLOCKED")
	assert_eq(service.accept(original, "IRON_SWORD_BASIC_V1", save).status, "APPLIED")
	assert_eq(service.accept(original, "IRON_SWORD_BASIC_V1", save, "PLAYER", "LOAN").status, "BLOCKED")
	var file = FileAccess.open(save.save_path, FileAccess.WRITE)
	file.store_string("corrupt")
	file.close()
	assert_eq(service.accept(original, "IRON_SWORD_BASIC_V1", save).status, "BLOCKED")

func test_old_accept_cannot_be_confused_with_later_same_definition():
	if not _available(): return
	var original = save.load_envelope()
	var first = service.accept(original, "IRON_SWORD_BASIC_V1", save)
	assert_eq(service.cancel(first.envelope, first.envelope.active_run.commission.active_order.order_id, save).status, "APPLIED")
	assert_eq(service.accept(save.load_envelope(), "IRON_SWORD_BASIC_V1", save).status, "APPLIED")
	assert_eq(service.accept(original, "IRON_SWORD_BASIC_V1", save).status, "BLOCKED")

func test_player_reservation_cancel_restores_selection_and_can_reserve_again():
	if not _available(): return
	var initial = save.load_envelope()
	var item = _item(initial)
	assert_eq(save.save_envelope(initial), OK)
	var before = initial.resource_snapshot()
	for mode in ["SALE", "LOAN"]:
		var accepted = service.accept(save.load_envelope(), "IRON_SWORD_BASIC_V1", save, "PLAYER", mode)
		var order = accepted.envelope.active_run.commission.active_order
		assert_eq(order.escrow.allocated_qty, 0)
		assert_eq(order.escrow.allocated_credit, 0)
		var reserved = service.reserve_item(accepted.envelope, order.order_id, item.uid, save)
		assert_eq(reserved.status, "APPLIED")
		if reserved.status != "APPLIED": return
		assert_eq(reserved.envelope.active_run.selected_item_uid, item.uid)
		assert_eq(service.reserve_item(accepted.envelope, order.order_id, item.uid, save).status, "ALREADY_APPLIED")
		assert_eq(service.reserve_item(reserved.envelope, "other-order", item.uid, save).status, "BLOCKED")
		assert_eq(service.cancel(reserved.envelope, order.order_id, save).status, "APPLIED")
		assert_eq(save.load_envelope().active_run.selected_item_uid, item.uid)
		assert_eq(save.load_envelope().get_item(item.uid).owner_id, "PLAYER")
		assert_eq(save.load_envelope().resource_snapshot(), before)
		var later = save.load_envelope()
		later.get_item(item.uid).raw_role_stat += 1
		assert_eq(save.save_envelope(later), OK, "Cancelled history must not freeze a player item")

func test_reserve_rejects_foreign_owner_wrong_equipment_and_escrow_item():
	if not _available(): return
	var initial = save.load_envelope()
	var item = _item(initial, "iron_shield")
	assert_eq(save.save_envelope(initial), OK)
	var accepted = service.accept(initial, "IRON_SWORD_BASIC_V1", save, "PLAYER", "SALE")
	var order_id = accepted.envelope.active_run.commission.active_order.order_id
	assert_eq(service.reserve_item(accepted.envelope, order_id, item.uid, save).status, "BLOCKED")
	assert_eq(service.cancel(accepted.envelope, order_id, save).status, "APPLIED")
	var foreign = save.load_envelope()
	foreign.get_item(item.uid).owner_id = "CUSTOMER"
	assert_eq(save.save_envelope(foreign), OK)
	accepted = service.accept(foreign, "IRON_SHIELD_BASIC_V1", save, "PLAYER", "SALE")
	order_id = accepted.envelope.active_run.commission.active_order.order_id
	assert_eq(service.reserve_item(accepted.envelope, order_id, item.uid, save).status, "BLOCKED")

func test_bucket_rejects_malformed_numbers_ids_definitions_and_duplicates():
	if not _available(): return
	var result = service.accept(save.load_envelope(), "IRON_SWORD_BASIC_V1", save)
	var raw = result.envelope.to_dict()
	for value in [0, -1, 1.5, INF, NAN, "1", true, 9007199254740992]:
		var broken = raw.duplicate(true)
		broken.active_run.commission.command_sequence = value
		assert_false(Envelope.from_dict(broken).validation_errors.is_empty(), str(value))
	for field in ["order_id", "accepted_day", "definition_snapshot", "escrow"]:
		var broken = raw.duplicate(true)
		broken.active_run.commission.active_order[field] = null
		assert_false(Envelope.from_dict(broken).validation_errors.is_empty(), field)
	var duplicate = raw.duplicate(true)
	duplicate.active_run.commission.history.append(duplicate.active_run.commission.active_order.duplicate(true))
	assert_false(Envelope.from_dict(duplicate).validation_errors.is_empty())

class FaultSave extends RefCounted:
	var real_save
	var wrote = false
	var mode = "NULL"
	func _init(actual): real_save = actual
	func load_envelope():
		if wrote and mode == "NULL": return null
		var result = real_save.load_envelope()
		if wrote and mode == "MISMATCH": result.workshop_resources.gold += 1
		return result
	func save_envelope(value):
		if mode == "PREWRITE": return ERR_CANT_CREATE
		var result = real_save.save_envelope(value)
		wrote = true
		return ERR_CANT_CREATE if mode == "POSTWRITE_ERROR" else result

func test_postwrite_unknown_has_no_usable_envelope_and_retry_recovers():
	if not _available(): return
	var original = save.load_envelope()
	var fault = FaultSave.new(save)
	var result = service.accept(original, "IRON_SWORD_BASIC_V1", fault)
	assert_eq(result.status, "COMMIT_UNCERTAIN")
	assert_false(result.has("envelope"))
	assert_eq(service.accept(original, "IRON_SWORD_BASIC_V1", save).status, "ALREADY_APPLIED")

func test_prewrite_failure_keeps_disk_and_source_unchanged():
	if not _available(): return
	var original = save.load_envelope()
	var before = original.to_dict()
	var fault = FaultSave.new(save)
	fault.mode = "PREWRITE"
	var result = service.accept(original, "IRON_SWORD_BASIC_V1", fault)
	assert_eq(result.status, "BLOCKED")
	assert_true(Envelope.serialized_equal(before, original.to_dict()))
	assert_true(Envelope.serialized_equal(before, save.load_envelope().to_dict()))

func test_cancel_customer_forged_fixture_returns_item_without_refund():
	if not _available(): return
	var accepted = service.accept(save.load_envelope(), "IRON_SWORD_BASIC_V1", save)
	var candidate = accepted.envelope
	var before = candidate.resource_snapshot()
	var item = _item(candidate)
	var record = candidate.active_run.commission.active_order
	record.phase = "READY"
	record.item_uid = item.uid
	record.reserve_source_hash = "a".repeat(64)
	record.command_sequence = 2
	record.escrow.consumed_qty = 1
	record.escrow.produced_item_uid = item.uid
	candidate.active_run.commission.command_sequence = 2
	item.owner_id = "CUSTOMER_COMMISSION_RESERVED"
	assert_eq(save.save_envelope(candidate), OK)
	var result = service.cancel(save.load_envelope(), record.order_id, save)
	assert_eq(result.status, "APPLIED")
	if result.status != "APPLIED": return
	assert_eq(result.envelope.get_item(item.uid).owner_id, "CUSTOMER")
	assert_eq(result.envelope.active_run.selected_item_uid, "")
	assert_eq(result.envelope.resource_snapshot(), before)
	assert_true(result.envelope.active_run.commission.history[0].escrow.reclaimed)

func test_postwrite_mismatch_is_uncertain_and_invalid_modes_never_allocate():
	if not _available(): return
	var original = save.load_envelope()
	for mode in [["COMMISSION_ESCROW", "LOAN"], ["INVALID", "SALE"], ["PLAYER", "INVALID"]]:
		assert_eq(service.accept(original, "IRON_SWORD_BASIC_V1", save, mode[0], mode[1]).status, "BLOCKED")
	var fault = FaultSave.new(save)
	fault.mode = "MISMATCH"
	var result = service.accept(original, "IRON_SWORD_BASIC_V1", fault)
	assert_eq(result.status, "COMMIT_UNCERTAIN")
	assert_false(result.has("envelope"))

func test_active_reserved_owner_and_escrow_forgery_fail_load():
	if not _available(): return
	var initial = save.load_envelope()
	var item = _item(initial)
	assert_eq(save.save_envelope(initial), OK)
	var accepted = service.accept(initial, "IRON_SWORD_BASIC_V1", save, "PLAYER", "SALE")
	var reserved = service.reserve_item(accepted.envelope, accepted.envelope.active_run.commission.active_order.order_id, item.uid, save)
	var raw = reserved.envelope.to_dict()
	var changed = raw.duplicate(true)
	changed.items_by_uid[item.uid].owner_id = "PLAYER"
	assert_false(Envelope.from_dict(changed).validation_errors.is_empty())
	for field in ["allocated_qty", "consumed_qty", "allocated_credit", "consumed_credit"]:
		changed = raw.duplicate(true)
		changed.active_run.commission.active_order.escrow[field] = 1
		assert_false(Envelope.from_dict(changed).validation_errors.is_empty(), field)

func test_error_after_write_does_not_claim_command_was_blocked():
	if not _available(): return
	var original = save.load_envelope()
	var fault = FaultSave.new(save)
	fault.mode = "POSTWRITE_ERROR"
	var result = service.accept(original, "IRON_SWORD_BASIC_V1", fault)
	assert_eq(result.status, "COMMIT_UNCERTAIN")
	assert_false(result.has("envelope"))
	assert_eq(service.accept(original, "IRON_SWORD_BASIC_V1", save).status, "ALREADY_APPLIED")

func test_pending_actual_world_use_cannot_be_reserved_for_commission():
	if not _available(): return
	var initial = save.load_envelope()
	var item = _item(initial)
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	item.used_precision_milestones.assign([10])
	item.catalyst_affix.tags = {"BURST_OUTPUT":1}
	assert_eq(save.save_envelope(initial), OK)
	var world = load("res://scripts/vertical_slice/services/vs_customer_actual_use_action_service.gd").new()
	var prepared = world.prepare_world_with_rolls(save.load_envelope(), item.uid, "DU", "OUTPUT", "BURST", [1, 99], save)
	assert_eq(prepared.status, "PREPARED")
	if prepared.status != "PREPARED": return
	var accepted = service.accept(prepared.envelope, "IRON_SWORD_BASIC_V1", save, "PLAYER", "SALE")
	assert_eq(accepted.status, "APPLIED")
	var order_id = accepted.envelope.active_run.commission.active_order.order_id
	assert_eq(service.reserve_item(accepted.envelope, order_id, item.uid, save).status, "BLOCKED")
