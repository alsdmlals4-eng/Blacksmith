class_name VSRunInitializerService
extends RefCounted

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const TOKEN_SIZE_BYTES := 16


func create_candidate_envelope():
	var crypto := Crypto.new()
	var token := crypto.generate_random_bytes(TOKEN_SIZE_BYTES)
	if token.size() != TOKEN_SIZE_BYTES:
		return null

	var envelope = SaveEnvelopeScript.new()
	envelope.saved_at_utc = Time.get_datetime_string_from_system(true, false) + "Z"
	envelope.active_run = {
		"run_id": "RUN-" + token.hex_encode(),
		"run_rng_seed": token.decode_u32(0),
		"current_day": 1,
		"resolved_events": {},
	}
	envelope.items_by_uid = {}
	envelope.customer_state = {}
	envelope.schedule_state = {}
	envelope.global_ledger_sequence = 0

	return SaveEnvelopeScript.from_dict(envelope.to_dict())
