class_name VSDayProgressionService
extends RefCounted


func register_handoff(save_envelope, handoff_proposal: Dictionary) -> Dictionary:
	if save_envelope == null:
		return _blocked("MISSING_SAVE_ENVELOPE")
	if str(handoff_proposal.get("status", "")) != "HANDOFF_ACCEPTED":
		return _blocked("INVALID_HANDOFF_PROPOSAL")
	if str(handoff_proposal.get("customer_id", "")) != "NADIA_VENN":
		return _blocked("CUSTOMER_NOT_NADIA")
	if str(handoff_proposal.get("content_id", "")) != "ADVENTURER_01":
		return _blocked("CONTENT_MISMATCH")
	if str(handoff_proposal.get("schedule_type", "")) != "PERSONAL_SCHEDULE":
		return _blocked("SCHEDULE_TYPE_MISMATCH")

	var assigned_uid := str(handoff_proposal.get("assigned_uid", ""))
	if assigned_uid.is_empty() or save_envelope.get_item(assigned_uid) == null:
		return _blocked("ASSIGNED_ITEM_NOT_FOUND")

	var existing_schedule: Dictionary = save_envelope.schedule_state.get("NADIA_VENN", {})
	if str(existing_schedule.get("status", "")) == "ACTIVE":
		return _blocked("SCHEDULE_ALREADY_ACTIVE")

	var current_day := int(save_envelope.active_run.get("current_day", 1))
	save_envelope.customer_state["NADIA_VENN"] = {
		"customer_id": "NADIA_VENN",
		"content_id": "ADVENTURER_01",
		"assigned_uid": assigned_uid,
		"status": "AWAY",
		"result_available": false,
	}
	save_envelope.schedule_state["NADIA_VENN"] = {
		"schedule_type": "PERSONAL_SCHEDULE",
		"customer_id": "NADIA_VENN",
		"content_id": "ADVENTURER_01",
		"assigned_uid": assigned_uid,
		"stage": str(handoff_proposal.get("initial_stage", "PREP_AND_ENTRY")),
		"status": "ACTIVE",
		"activated_day": current_day,
		"last_checked_day": current_day,
		"checks_completed": 0,
	}
	return {
		"status": "REGISTERED",
		"customer_id": "NADIA_VENN",
		"assigned_uid": assigned_uid,
		"current_day": current_day,
	}


func advance_day(_save_envelope, _daily_checks: Dictionary = {}) -> Dictionary:
	return {"status": "NOT_IMPLEMENTED"}


func _blocked(reason: String) -> Dictionary:
	return {
		"status": "BLOCKED",
		"reason": reason,
	}
