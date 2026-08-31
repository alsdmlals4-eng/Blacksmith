extends "res://addons/gut/test.gd"

const INITIALIZER_PATH := "res://scripts/vertical_slice/services/vs_run_initializer_service.gd"


func _new_initializer():
	if not ResourceLoader.exists(INITIALIZER_PATH):
		return null
	var script = load(INITIALIZER_PATH)
	if script == null:
		return null
	return script.new()


func test_initializer_service_surface_exists() -> void:
	assert_true(ResourceLoader.exists(INITIALIZER_PATH), "initializer service must exist at the approved path")


func test_initializer_creates_valid_empty_campaign_envelope() -> void:
	var initializer = _new_initializer()
	assert_true(initializer != null, "initializer service must load")
	if initializer == null:
		return
	assert_true(initializer.has_method("create_candidate_envelope"), "initializer must expose create_candidate_envelope")
	if not initializer.has_method("create_candidate_envelope"):
		return

	var envelope = initializer.create_candidate_envelope()
	assert_true(envelope != null, "initializer must return an envelope")
	if envelope == null:
		return
	assert_true(envelope.validation_errors.is_empty(), "new campaign envelope must validate before persistence")
	assert_eq(envelope.schema_version, 4, "current implementation must use V4 save schema")
	assert_eq(envelope.preset_version, "VS-2026.08.27-D", "current implementation must use V4 preset")
	assert_eq(envelope.workshop_resources.get("gold", -1), 20000, "new campaign starts with mutable TEMP_TEST_BUDGET gold")
	assert_eq(
		(envelope.workshop_resources.get("material_stock", {}) as Dictionary).get(
			"common_reinforcement_material", -1
		),
		30,
		"new campaign starts with mutable TEMP_TEST_BUDGET reinforcement material"
	)
	assert_eq(int(envelope.active_run.get("current_day", 0)), 1, "new campaign starts on day 1")
	assert_eq(envelope.active_run.get("resolved_events", {}), {}, "initializer must not resolve gameplay events")
	assert_true(envelope.items_by_uid.is_empty(), "initializer must not create an item")
	assert_true(envelope.customer_state.is_empty(), "initializer must not create customer outcomes")
	assert_true(envelope.schedule_state.is_empty(), "initializer must not create schedule outcomes")
	assert_eq(envelope.global_ledger_sequence, 0, "new campaign ledger starts at zero")


func test_initializer_run_identity_seed_and_timestamp_match_approved_contract() -> void:
	var initializer = _new_initializer()
	assert_true(initializer != null, "initializer service must load")
	if initializer == null or not initializer.has_method("create_candidate_envelope"):
		return
	var envelope = initializer.create_candidate_envelope()
	assert_true(envelope != null, "initializer must return an envelope")
	if envelope == null:
		return

	var run_id := str(envelope.active_run.get("run_id", ""))
	var run_id_pattern := RegEx.new()
	assert_eq(run_id_pattern.compile("^RUN-[0-9a-f]{32}$"), OK, "run id regex must compile")
	assert_true(run_id_pattern.search(run_id) != null, "run_id must be RUN- plus 32 lowercase hex")

	var run_seed = envelope.active_run.get("run_rng_seed", -1)
	assert_true(run_seed is int, "run_rng_seed must be an integer")
	assert_true(int(run_seed) >= 0, "run_rng_seed must be unsigned")
	assert_true(int(run_seed) <= 4294967295, "run_rng_seed must fit u32")

	var timestamp_pattern := RegEx.new()
	assert_eq(timestamp_pattern.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"), OK, "UTC timestamp regex must compile")
	assert_true(timestamp_pattern.search(envelope.saved_at_utc) != null, "saved_at_utc must be UTC ISO seconds with Z")
