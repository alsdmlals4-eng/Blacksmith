extends "res://addons/gut/test.gd"

const NADIA_RESOLVER_PATH := "res://scripts/vertical_slice/resolvers/vs_nadia_schedule_resolver.gd"
const DAY_SERVICE_PATH := "res://scripts/vertical_slice/services/vs_day_progression_service.gd"
const CustomerProfileScript = preload("res://scripts/vertical_slice/domain/vs_customer_profile.gd")
const ContextPacketScript = preload("res://scripts/vertical_slice/domain/vs_customer_context_packet.gd")
const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const RunInitializerScript = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")

const ITEM_UID := "BSI-0123456789abcdef0123456789abcdef"


func _customer(customer_id: String = "NADIA_VENN"):
	var customer = CustomerProfileScript.new()
	customer.customer_id = customer_id
	customer.name = "Synthetic Nadia"
	customer.role = "TEST_ROLE"
	customer.public_epithet = "TEST_EPITHET"
	customer.public_standing_grade = "ELITE"
	customer.content_id = "ADVENTURER_01"
	customer.content_goal = "SURVIVAL_AND_RECOVERY"
	customer.numeric_capability_profile = "SYNTHETIC_TEST_FIXTURE"
	return customer


func _context(strength: int = 4):
	var context = ContextPacketScript.new()
	context.customer_id = "NADIA_VENN"
	context.content_id = "ADVENTURER_01"
	context.primary_need = "SAFE_RETURN"
	context.secondary_need = "RECOVERY_POSSIBILITY"
	context.known_context.append("RUINS")
	context.risk = 6
	context.strength = strength
	context.dexterity = 5
	context.constitution = 6
	context.judgment = 5
	context.weapon_proficiency = 2
	context.related_ability = "CONSTITUTION"
	context.relevant_precision_axes.append("WEIGHT")
	context.relevant_precision_axes.append("DURABILITY")
	return context


func _item(weight: int = 40, physical_state: String = "ACTIVE"):
	var item = ItemScript.new()
	item.uid = ITEM_UID
	item.weight_point = weight
	item.enhancement_level = 10
	item.highest_checkpoint = 10
	item.current_durability = 100
	item.max_durability = 100
	item.physical_state = physical_state
	if physical_state == "DESTROYED":
		item.current_durability = 0
	return item


func _envelope_with_item():
	var envelope = RunInitializerScript.new().create_candidate_envelope()
	if envelope != null:
		envelope.add_item(_item())
	return envelope


func _registered_envelope():
	var envelope = _envelope_with_item()
	if envelope == null:
		return null
	var proposal: Dictionary = load(NADIA_RESOLVER_PATH).new().handoff(_customer(), envelope.get_item(ITEM_UID), _context())
	var registered: Dictionary = load(DAY_SERVICE_PATH).new().register_handoff(envelope, proposal)
	if str(registered.get("status", "")) != "REGISTERED":
		return null
	return envelope


func test_task5_runtime_surfaces_exist() -> void:
	assert_true(ResourceLoader.exists(NADIA_RESOLVER_PATH), "Task5 requires a Nadia schedule resolver")
	assert_true(ResourceLoader.exists(DAY_SERVICE_PATH), "Task5 requires a day progression service")


func test_task5_handoff_and_day_progression_api_exist() -> void:
	var resolver = load(NADIA_RESOLVER_PATH).new()
	var service = load(DAY_SERVICE_PATH).new()
	assert_true(resolver.has_method("handoff"), "Nadia resolver must expose handoff")
	assert_true(service.has_method("register_handoff"), "day progression service must register accepted handoff proposals")
	assert_true(service.has_method("advance_day"), "day progression service must own end-of-day advancement")


func test_nadia_handoff_creates_delayed_same_uid_schedule_proposal_without_world_result() -> void:
	var item = _item()
	var before := item.to_dict()
	var result: Dictionary = load(NADIA_RESOLVER_PATH).new().handoff(_customer(), item, _context())
	assert_eq(result.get("status", ""), "HANDOFF_ACCEPTED")
	assert_eq(result.get("customer_id", ""), "NADIA_VENN")
	assert_eq(result.get("content_id", ""), "ADVENTURER_01")
	assert_eq(result.get("assigned_uid", ""), ITEM_UID)
	assert_eq(result.get("schedule_type", ""), "PERSONAL_SCHEDULE")
	assert_eq(result.get("initial_stage", ""), "PREP_AND_ENTRY")
	assert_eq(result.get("schedule_status", ""), "ACTIVE")
	assert_false(bool(result.get("result_available", true)), "handoff acknowledgement must not fake the delayed world result")
	assert_false(result.has("result_axes"), "handoff must not resolve Nadia's three world-result axes immediately")
	assert_eq(item.to_dict(), before, "handoff proposal must not mutate the item")


func test_nadia_handoff_fails_closed_for_wrong_customer_invalid_context_destroyed_or_overweight_item() -> void:
	var resolver = load(NADIA_RESOLVER_PATH).new()
	var wrong_customer: Dictionary = resolver.handoff(_customer("OTHER_CUSTOMER"), _item(), _context())
	assert_eq(wrong_customer.get("status", ""), "BLOCKED")
	assert_eq(wrong_customer.get("reason", ""), "CUSTOMER_NOT_NADIA")

	var invalid_context = ContextPacketScript.from_dict({})
	var invalid: Dictionary = resolver.handoff(_customer(), _item(), invalid_context)
	assert_eq(invalid.get("status", ""), "BLOCKED")
	assert_eq(invalid.get("reason", ""), "INVALID_CONTEXT")

	var destroyed: Dictionary = resolver.handoff(_customer(), _item(40, "DESTROYED"), _context())
	assert_eq(destroyed.get("status", ""), "BLOCKED")
	assert_eq(destroyed.get("reason", ""), "ITEM_DESTROYED")

	var overweight: Dictionary = resolver.handoff(_customer(), _item(45), _context(4))
	assert_eq(overweight.get("status", ""), "BLOCKED")
	assert_eq(overweight.get("reason", ""), "OVERWEIGHT")


func test_register_handoff_activates_personal_schedule_without_resolving_world_result() -> void:
	var envelope = _envelope_with_item()
	assert_not_null(envelope)
	if envelope == null:
		return
	var proposal: Dictionary = load(NADIA_RESOLVER_PATH).new().handoff(_customer(), envelope.get_item(ITEM_UID), _context())
	var result: Dictionary = load(DAY_SERVICE_PATH).new().register_handoff(envelope, proposal)
	assert_eq(result.get("status", ""), "REGISTERED")
	assert_eq(envelope.customer_state.get("NADIA_VENN", {}).get("assigned_uid", ""), ITEM_UID)
	assert_eq(envelope.customer_state.get("NADIA_VENN", {}).get("status", ""), "AWAY")
	assert_false(bool(envelope.customer_state.get("NADIA_VENN", {}).get("result_available", true)))
	var schedule: Dictionary = envelope.schedule_state.get("NADIA_VENN", {})
	assert_eq(schedule.get("schedule_type", ""), "PERSONAL_SCHEDULE")
	assert_eq(schedule.get("stage", ""), "PREP_AND_ENTRY")
	assert_eq(schedule.get("status", ""), "ACTIVE")
	assert_eq(int(schedule.get("activated_day", -1)), 1)
	assert_eq(int(schedule.get("last_checked_day", -1)), 1)
	assert_eq(int(schedule.get("checks_completed", -1)), 0)
	assert_false(schedule.has("fixed_duration_days"), "Nadia schedule must not invent a universal fixed duration")
	assert_true(envelope.active_run.get("resolved_events", {}).is_empty(), "handoff registration must not resolve a world result")


func test_duplicate_active_handoff_is_atomic_and_does_not_replace_schedule() -> void:
	var envelope = _envelope_with_item()
	assert_not_null(envelope)
	if envelope == null:
		return
	var service = load(DAY_SERVICE_PATH).new()
	var proposal: Dictionary = load(NADIA_RESOLVER_PATH).new().handoff(_customer(), envelope.get_item(ITEM_UID), _context())
	assert_eq(service.register_handoff(envelope, proposal).get("status", ""), "REGISTERED")
	var before: Dictionary = envelope.to_dict()
	var duplicate_result: Dictionary = service.register_handoff(envelope, proposal)
	assert_eq(duplicate_result.get("status", ""), "BLOCKED")
	assert_eq(duplicate_result.get("reason", ""), "SCHEDULE_ALREADY_ACTIVE")
	assert_eq(envelope.to_dict(), before, "duplicate active handoff must not mutate campaign state")


func test_advance_day_without_check_never_auto_progresses_nadia() -> void:
	var envelope = _registered_envelope()
	assert_not_null(envelope)
	if envelope == null:
		return
	var result: Dictionary = load(DAY_SERVICE_PATH).new().advance_day(envelope, {})
	assert_eq(result.get("status", ""), "DAY_ADVANCED")
	assert_eq(int(envelope.active_run.get("current_day", -1)), 2)
	var schedule: Dictionary = envelope.schedule_state.get("NADIA_VENN", {})
	assert_eq(schedule.get("stage", ""), "PREP_AND_ENTRY")
	assert_eq(int(schedule.get("last_checked_day", -1)), 1)
	assert_eq(int(schedule.get("checks_completed", -1)), 0)
	assert_true(envelope.active_run.get("resolved_events", {}).is_empty())


func test_wait_consumes_one_end_of_day_check_and_keeps_stage() -> void:
	var envelope = _registered_envelope()
	assert_not_null(envelope)
	if envelope == null:
		return
	var result: Dictionary = load(DAY_SERVICE_PATH).new().advance_day(envelope, {
		"NADIA_VENN": {"action": "WAIT"},
	})
	assert_eq(result.get("status", ""), "DAY_ADVANCED")
	assert_eq(int(envelope.active_run.get("current_day", -1)), 2)
	var schedule: Dictionary = envelope.schedule_state.get("NADIA_VENN", {})
	assert_eq(schedule.get("stage", ""), "PREP_AND_ENTRY")
	assert_eq(int(schedule.get("last_checked_day", -1)), 2)
	assert_eq(int(schedule.get("checks_completed", -1)), 1)
	assert_true(envelope.active_run.get("resolved_events", {}).is_empty())


func test_advance_moves_at_most_one_nadia_stage_per_day() -> void:
	var envelope = _registered_envelope()
	assert_not_null(envelope)
	if envelope == null:
		return
	var service = load(DAY_SERVICE_PATH).new()
	var day2: Dictionary = service.advance_day(envelope, {
		"NADIA_VENN": {"action": "ADVANCE"},
	})
	assert_eq(day2.get("status", ""), "DAY_ADVANCED")
	assert_eq(int(envelope.active_run.get("current_day", -1)), 2)
	assert_eq(envelope.schedule_state.get("NADIA_VENN", {}).get("stage", ""), "EXPLORATION")
	assert_eq(int(envelope.schedule_state.get("NADIA_VENN", {}).get("checks_completed", -1)), 1)

	var day3: Dictionary = service.advance_day(envelope, {
		"NADIA_VENN": {"action": "ADVANCE"},
	})
	assert_eq(day3.get("status", ""), "DAY_ADVANCED")
	assert_eq(int(envelope.active_run.get("current_day", -1)), 3)
	assert_eq(envelope.schedule_state.get("NADIA_VENN", {}).get("stage", ""), "WITHDRAWAL_AND_RECOVERY")
	assert_eq(int(envelope.schedule_state.get("NADIA_VENN", {}).get("checks_completed", -1)), 2)
	assert_true(envelope.active_run.get("resolved_events", {}).is_empty(), "stage progression must not auto-resolve Nadia")


func test_unknown_schedule_action_is_atomic_before_day_increment() -> void:
	var envelope = _registered_envelope()
	assert_not_null(envelope)
	if envelope == null:
		return
	var before: Dictionary = envelope.to_dict()
	var result: Dictionary = load(DAY_SERVICE_PATH).new().advance_day(envelope, {
		"NADIA_VENN": {"action": "SKIP_TO_RESULT"},
	})
	assert_eq(result.get("status", ""), "BLOCKED")
	assert_eq(result.get("reason", ""), "UNKNOWN_SCHEDULE_ACTION")
	assert_eq(envelope.to_dict(), before, "invalid day action must not advance day or mutate schedule")


func test_advance_from_withdrawal_requires_explicit_resolution_payload_and_is_atomic() -> void:
	var envelope = _registered_envelope()
	assert_not_null(envelope)
	if envelope == null:
		return
	var service = load(DAY_SERVICE_PATH).new()
	assert_eq(service.advance_day(envelope, {"NADIA_VENN": {"action": "ADVANCE"}}).get("status", ""), "DAY_ADVANCED")
	assert_eq(service.advance_day(envelope, {"NADIA_VENN": {"action": "ADVANCE"}}).get("status", ""), "DAY_ADVANCED")
	assert_eq(envelope.schedule_state.get("NADIA_VENN", {}).get("stage", ""), "WITHDRAWAL_AND_RECOVERY")
	var before: Dictionary = envelope.to_dict()
	var blocked: Dictionary = service.advance_day(envelope, {"NADIA_VENN": {"action": "ADVANCE"}})
	assert_eq(blocked.get("status", ""), "BLOCKED")
	assert_eq(blocked.get("reason", ""), "RESOLUTION_PAYLOAD_REQUIRED")
	assert_eq(envelope.to_dict(), before, "withdrawal must wait for explicit result evidence instead of auto-resolving")
