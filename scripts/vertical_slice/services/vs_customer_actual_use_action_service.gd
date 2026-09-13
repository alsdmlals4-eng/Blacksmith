# 고객 실제사용 이벤트를 저장 후보에서 해결하고 성공한 저장본만 반환한다.
class_name VSCustomerActualUseActionService
extends RefCounted

const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const CustomerWorldEventResolverScript = preload(
	"res://scripts/vertical_slice/resolvers/vs_customer_world_event_resolver.gd"
)


func resolve_and_save_with_roll(
	envelope,
	item_uid: String,
	event: Dictionary,
	damage_roll_percent: float,
	save_service
) -> Dictionary:
	if save_service == null or not save_service.has_method("save_envelope"):
		return _blocked("INVALID_SAVE_SERVICE")
	if envelope == null or not envelope.has_method("to_dict"):
		return _blocked("INVALID_SAVE_ENVELOPE")

	var candidate = SaveEnvelopeScript.from_dict(envelope.to_dict())
	if candidate == null or not candidate.validation_errors.is_empty():
		return _blocked("INVALID_SAVE_ENVELOPE")

	var result: Dictionary = CustomerWorldEventResolverScript.new().resolve(
		candidate,
		item_uid,
		event.duplicate(true),
		damage_roll_percent
	)
	if str(result.get("status", "")) != "APPLIED":
		return result

	var save_error: Error = save_service.save_envelope(candidate)
	if save_error != OK:
		return _blocked("SAVE_FAILED:%d" % int(save_error))

	result["envelope"] = candidate
	return result


# Prepare commits the two independent draws before applying any consequence.
func prepare_aqueduct(envelope, item_uid: String, axis: String, rhythm: String, save_service) -> Dictionary:
	var rng := RandomNumberGenerator.new()
	rng.randomize()
	return prepare_aqueduct_with_rolls(envelope, item_uid, axis, rhythm,
		[rng.randf() * 99.999999, rng.randf() * 99.999999], save_service)


func prepare_aqueduct_with_rolls(envelope, item_uid: String, axis: String, rhythm: String, rolls: Array, save_service) -> Dictionary:
	var candidate = _aqueduct_candidate(envelope, save_service)
	if candidate == null:
		return _blocked("INVALID_AQUEDUCT_CONTEXT")
	var trials: Dictionary = candidate.active_run.get("aqueduct_trials", {})
	if trials.has(item_uid):
		return {"status": "ALREADY_RESOLVED" if trials[item_uid].phase == "RESOLVED" else "PREPARED",
			"record": trials[item_uid].duplicate(true), "envelope": candidate}
	var item = candidate.get_item(item_uid)
	if item == null or item.current_durability <= 0:
		return _blocked("INVALID_AQUEDUCT_ITEM")
	var catalog = load("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
	var rules = load("res://scripts/vertical_slice/domain/vs_replan_tag_rules.gd").new()
	var preview: Dictionary = rules.aqueduct_preview(str(catalog.by_item(item).get("equipment_id", "")),
		int(item.enhancement_level), item.catalyst_affix.get("tags", {}), axis, rhythm)
	if not preview.get("ok", false):
		return _blocked(str(preview.get("reason", "INVALID_AQUEDUCT_PREVIEW")))
	var record := {"record_type": "AQUEDUCT_TRIAL_V1", "schema_version": 1,
		"ruleset_id": rules.RULESET_ID, "event_id": "aq-trial-" + item_uid, "item_uid": item_uid,
		"phase": "PREPARED", "axis": axis, "rhythm": rhythm, "item_snapshot": item.to_dict(),
		"rolls": rolls.duplicate(), "success_percent": preview.success_percent,
		"damage_percent": CustomerWorldEventResolverScript.new()._damage_percent(item, "LOW"),
		"reward": "NONE", "mission_success": null, "damage_applied": null}
	var error := SaveEnvelopeScript.validate_aqueduct_trial(record, item_uid)
	if not error.is_empty():
		return _blocked(error)
	trials[item_uid] = record
	candidate.active_run["aqueduct_trials"] = trials
	return _commit_aqueduct(candidate, record, "PREPARED", save_service)


func resolve_prepared_aqueduct(envelope, item_uid: String, save_service) -> Dictionary:
	var candidate = _aqueduct_candidate(envelope, save_service)
	if candidate == null:
		return _blocked("INVALID_AQUEDUCT_CONTEXT")
	var trials: Dictionary = candidate.active_run.get("aqueduct_trials", {})
	if not trials.has(item_uid):
		return _blocked("AQUEDUCT_NOT_PREPARED")
	var record: Dictionary = trials[item_uid]
	if record.phase == "RESOLVED":
		return {"status": "ALREADY_RESOLVED", "record": record.duplicate(true), "envelope": candidate}
	var item = candidate.get_item(item_uid)
	var snapshot = SaveEnvelopeScript.ItemScript.from_dict(record.item_snapshot)
	if item == null or item.to_dict() != snapshot.to_dict():
		return _blocked("AQUEDUCT_ITEM_CHANGED")
	record.mission_success = record.rolls[0] < record.success_percent
	record.damage_applied = record.rolls[1] < record.damage_percent
	if record.damage_applied:
		item.apply_damage_event()
	record.phase = "RESOLVED"
	return _commit_aqueduct(candidate, record, "APPLIED", save_service)


# The report reads the immutable departure snapshot, never the current item.
func aqueduct_report(record: Dictionary) -> Dictionary:
	if not SaveEnvelopeScript.validate_aqueduct_trial(record, str(record.get("item_uid", ""))).is_empty():
		return {"ok": false, "body": "수로 모험 기록을 확인할 수 없습니다."}
	var rules = load("res://scripts/vertical_slice/domain/vs_replan_tag_rules.gd").new()
	var definition: Dictionary = rules.AQUEDUCT_REQUIREMENTS[record.axis + ":" + record.rhythm]
	var snapshot = SaveEnvelopeScript.ItemScript.from_dict(record.item_snapshot)
	var estimate: Dictionary = rules.aqueduct_preview("iron_shield", int(snapshot.enhancement_level), snapshot.catalyst_affix.tags, record.axis, record.rhythm)
	var tags: PackedStringArray = []
	for tag_id in snapshot.catalyst_affix.tags:
		tags.append("%s %s" % [rules.DISPLAY_NAMES_KO[tag_id], ["I","II","III","IV"][int(snapshot.catalyst_affix.tags[tag_id]) - 1]])
	var lines: PackedStringArray = [
		"무너진 수로의 측량대 · " + str(definition.content_id),
		"임무: " + str(definition.purpose),
		"출발 작품: 철방패 +%d · %s" % [int(snapshot.enhancement_level), " / ".join(tags)],
		"기본 %.1f%% + 태그 기여 %.1f%%p = %.1f%%" % [float(estimate.base_percent), float(estimate.applied_support_percent), float(estimate.success_percent)],
		"장비 손상 위험 %.1f%% · 임무와 독립 판정" % float(record.damage_percent),
	]
	if record.phase == "PREPARED":
		lines.append("측량대에 대여 중 · 강화/수리 잠금")
		lines.append("판정 저장 완료 · 아래에서 결과 확인")
	else:
		lines.append("임무 %s · %s" % ["성공" if record.mission_success else "실패", definition.success if record.mission_success else definition.failure])
		var after_current := int(snapshot.current_durability) - (1 if record.damage_applied else 0)
		lines.append("장비 %s · 내구도 %d → %d / 한계 %d" % [
			"손상 발생" if record.damage_applied else "손상 없음", int(snapshot.current_durability), after_current, int(snapshot.max_durability)])
		lines.append("공방 반환 · 편집 가능" if after_current > 0 else "파괴 · 작품 기록 보존 / 편집 불가")
	lines.append("보상 없음 · 시험 판정 / 재열람은 결과를 바꾸지 않음")
	return {"ok": true, "content_id": definition.content_id, "body": "\n".join(lines)}


func _aqueduct_candidate(envelope, save_service):
	if envelope == null or not envelope.has_method("to_dict") or save_service == null or not save_service.has_method("save_envelope"):
		return null
	var candidate = SaveEnvelopeScript.from_dict(envelope.to_dict())
	if save_service.has_method("load_envelope"):
		var committed = save_service.load_envelope()
		if committed != null and committed.validation_errors.is_empty():
			if committed.active_run.get("run_id", "") != candidate.active_run.get("run_id", ""):
				return null
			var uid := str(candidate.active_run.get("selected_item_uid", ""))
			if not committed.active_run.get("aqueduct_trials", {}).has(uid):
				if candidate.to_dict().items_by_uid != committed.to_dict().items_by_uid or candidate.resource_snapshot() != committed.resource_snapshot():
					return null
			candidate = committed
		elif committed == null or committed.validation_errors != ["SAVE_NOT_FOUND"]:
			return null
	if not candidate.validation_errors.is_empty() or candidate.active_run.get("tag_ruleset_id", "") != "BLACKSMITH_REPLAN_TAGS_20260912":
		return null
	return candidate


func _commit_aqueduct(candidate, record: Dictionary, status: String, save_service) -> Dictionary:
	var save_error: Error = save_service.save_envelope(candidate)
	if save_error != OK:
		return _blocked("SAVE_FAILED:%d" % int(save_error))
	if save_service.has_method("load_envelope"):
		var committed = save_service.load_envelope()
		if committed == null or not committed.validation_errors.is_empty():
			return _blocked("AQUEDUCT_READBACK_FAILED")
		var actual: Variant = committed.active_run.get("aqueduct_trials", {}).get(record.item_uid)
		if committed.active_run.get("run_id", "") != candidate.active_run.get("run_id", "") or not actual is Dictionary:
			return _blocked("AQUEDUCT_READBACK_FAILED")
		if JSON.parse_string(JSON.stringify(actual)) != JSON.parse_string(JSON.stringify(record)):
			return _blocked("AQUEDUCT_READBACK_FAILED")
		candidate = committed
		record = actual
	return {"status": status, "record": record.duplicate(true), "envelope": candidate}


func _blocked(reason: String) -> Dictionary:
	return {"status": "BLOCKED", "reason": reason}
