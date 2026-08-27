# 고객 실제 사용 이벤트를 같은 작품 UID의 결과와 내구도 변화로 해석한다.
class_name VSCustomerWorldEventResolver
extends RefCounted

const ContentResultRecordScript = preload(
	"res://scripts/vertical_slice/domain/vs_content_result_record.gd"
)

const DAMAGE_PROFILE_PERCENT := {
	"NONE": 0.0,
	"LOW": 10.0,
	"MEDIUM": 20.0,
	"HIGH": 40.0,
	"DIRECT": 100.0,
}
const DAMAGE_STATE_MULTIPLIER := {
	"NORMAL": 1.0,
	"MINOR": 1.25,
	"MAJOR": 1.75,
}
const PROFILE_STEP_DOWN := {
	"LOW": "NONE",
	"MEDIUM": "LOW",
	"HIGH": "MEDIUM",
}
const PROBABILISTIC_DAMAGE_CAP := 95.0
const TOKEN_PATTERN := "^[A-Z0-9_]+$"


func resolve(envelope, item_uid: String, event: Dictionary, damage_roll_percent: float) -> Dictionary:
	if envelope == null:
		return _blocked("MISSING_ENVELOPE")
	if not envelope.validation_errors.is_empty():
		return _blocked("INVALID_ENVELOPE")
	if item_uid.is_empty():
		return _blocked("MISSING_ITEM_UID")
	if (
		not envelope.active_run.has("resolved_events")
		or not envelope.active_run["resolved_events"] is Dictionary
	):
		return _blocked("INVALID_RESOLVED_EVENTS")
	var item = envelope.get_item(item_uid)
	if item == null:
		return _blocked("ITEM_NOT_FOUND")
	if str(item.uid) != item_uid:
		return _blocked("ITEM_UID_MISMATCH")
	if int(item.current_durability) <= 0 or str(item.physical_state) == "DESTROYED":
		return _blocked("ITEM_DESTROYED")

	var raw_content_result: Variant = event.get("content_result", null)
	if not raw_content_result is Dictionary:
		return _blocked("INVALID_CONTENT_RESULT")
	var record = ContentResultRecordScript.from_dict(raw_content_result)
	if not record.validation_errors.is_empty():
		return _blocked("INVALID_CONTENT_RESULT")
	if not _is_single_primary_item_record(record, item_uid):
		return _blocked("CONTENT_RESULT_ITEM_MISMATCH")
	if envelope.active_run["resolved_events"].has(record.event_id):
		return _blocked("EVENT_ALREADY_RESOLVED")

	var actual_item_use: Variant = event.get("actual_item_use", null)
	if not actual_item_use is bool:
		return _blocked("INVALID_ACTUAL_ITEM_USE")
	var declared_profile := str(event.get("damage_profile", ""))
	if not DAMAGE_PROFILE_PERCENT.has(declared_profile):
		return _blocked("INVALID_DAMAGE_PROFILE")
	var raw_damage_cause: Variant = event.get("damage_cause", "")
	if bool(actual_item_use) and not raw_damage_cause is String:
		return _blocked("INVALID_DAMAGE_CAUSE")
	var damage_cause := str(raw_damage_cause)
	if bool(actual_item_use) and not _is_token(damage_cause):
		return _blocked("INVALID_DAMAGE_CAUSE")
	if (
		bool(actual_item_use)
		and declared_profile != "DIRECT"
		and (
			is_nan(damage_roll_percent)
			or is_inf(damage_roll_percent)
			or damage_roll_percent < 0.0
			or damage_roll_percent > 100.0
		)
	):
		return _blocked("INVALID_DAMAGE_ROLL")
	if bool(actual_item_use) and record.causal_reasons.size() >= 4 and not record.causal_reasons.has(damage_cause):
		return _blocked("CONTENT_RESULT_REASON_CAPACITY_EXCEEDED")

	var effective_profile := _effective_profile(item, event, declared_profile) if bool(actual_item_use) else "NONE"
	var damage_percent := _damage_percent(item, effective_profile) if bool(actual_item_use) else 0.0
	var before_current := int(item.current_durability)
	var before_max := int(item.max_durability)
	var damage_applied := false
	if bool(actual_item_use) and effective_profile == "DIRECT":
		damage_applied = item.apply_damage_event()
	elif bool(actual_item_use) and damage_roll_percent < damage_percent:
		damage_applied = item.apply_damage_event()

	if bool(actual_item_use) and not record.causal_reasons.has(damage_cause):
		record.causal_reasons.append(damage_cause)
	record.durability_consequence = {
		"actual_item_use": bool(actual_item_use),
		"damage_applied": damage_applied,
		"damage_cause": damage_cause,
		"declared_damage_profile": declared_profile,
		"effective_damage_profile": effective_profile,
		"before_current_durability": before_current,
		"after_current_durability": int(item.current_durability),
		"before_max_durability": before_max,
		"after_max_durability": int(item.max_durability),
		"repair_job_available": bool(item.repair_job_available),
	}
	envelope.active_run["resolved_events"][record.event_id] = record.to_dict()
	return {
		"status": "APPLIED",
		"reason": "",
		"event_id": record.event_id,
		"item_uid": item_uid,
		"actual_item_use": bool(actual_item_use),
		"damage_cause": damage_cause,
		"declared_damage_profile": declared_profile,
		"effective_damage_profile": effective_profile,
		"damage_percent": damage_percent,
		"damage_applied": damage_applied,
		"before_current_durability": before_current,
		"after_current_durability": int(item.current_durability),
		"before_max_durability": before_max,
		"after_max_durability": int(item.max_durability),
		"repair_job_available": bool(item.repair_job_available),
	}


func _effective_profile(item, event: Dictionary, declared_profile: String) -> String:
	if declared_profile == "DIRECT":
		return "DIRECT"
	var relevant_protection_function_id := str(event.get("relevant_protection_function_id", ""))
	if (
		not relevant_protection_function_id.is_empty()
		and item.functions.has(relevant_protection_function_id)
	):
		return str(PROFILE_STEP_DOWN.get(declared_profile, declared_profile))
	return declared_profile


func _damage_percent(item, profile: String) -> float:
	if profile == "DIRECT":
		return 100.0
	var state := str(item.effective_durability_state())
	var multiplier := float(DAMAGE_STATE_MULTIPLIER.get(state, 0.0))
	return minf(PROBABILISTIC_DAMAGE_CAP, float(DAMAGE_PROFILE_PERCENT[profile]) * multiplier)


func _is_single_primary_item_record(record, item_uid: String) -> bool:
	return (
		record.item_refs.size() == 1
		and str(record.item_refs[0].get("role", "")) == "PRIMARY_ITEM"
		and str(record.item_refs[0].get("uid", "")) == item_uid
	)


func _is_token(value: String) -> bool:
	var regex := RegEx.new()
	return regex.compile(TOKEN_PATTERN) == OK and regex.search(value) != null


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
