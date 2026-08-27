class_name VSEnhancementActionService
extends RefCounted

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const SaveEnvelopeScript = preload("res://scripts/vertical_slice/domain/vs_save_envelope.gd")
const EnhancementResolverScript = preload(
	"res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd"
)
const DestroyedHistoryRecordScript = preload(
	"res://scripts/vertical_slice/domain/vs_destroyed_history_record.gd"
)
const REINFORCEMENT_MATERIAL_ID := "common_reinforcement_material"


func resolve_and_save_with_rolls(
	envelope,
	item_uid: String,
	target_level: int,
	rolls: Dictionary,
	game_day: int,
	resources,
	save_service
) -> Dictionary:
	if resources == null or not resources.has_method("snapshot") or not resources.has_method("get_material_count"):
		return _blocked("INVALID_RESOURCES")
	if save_service == null or not save_service.has_method("save_envelope"):
		return _blocked("INVALID_SAVE_SERVICE")
	if envelope == null or not envelope.has_method("to_dict") or not envelope.has_method("resource_snapshot"):
		return _blocked("INVALID_SAVE_ENVELOPE")
	if resources.snapshot() != envelope.resource_snapshot():
		return _blocked("RESOURCE_SAVE_DIVERGED")

	var source_item = envelope.get_item(item_uid) if envelope.has_method("get_item") else null
	var preview := EnhancementResolverScript.new().preview(source_item, target_level)
	if not bool(preview.get("allowed", false)):
		return _blocked(str(preview.get("reason", "INVALID_ATTEMPT")))
	var gold_cost := int(preview.get("gold_cost", 0))
	var reinforcement_units := int(preview.get("reinforcement_units", 0))
	if int(resources.gold) < gold_cost:
		return _blocked("INSUFFICIENT_GOLD")
	if int(resources.get_material_count(REINFORCEMENT_MATERIAL_ID)) < reinforcement_units:
		return _blocked("INSUFFICIENT_REINFORCEMENT")

	var candidate = SaveEnvelopeScript.from_dict(envelope.to_dict())
	if candidate == null or not candidate.validation_errors.is_empty():
		return _blocked("INVALID_SAVE_ENVELOPE")
	var staged_resources: Dictionary = resources.snapshot()
	staged_resources["gold"] = int(staged_resources.get("gold", 0)) - gold_cost
	var staged_stock: Dictionary = staged_resources.get("material_stock", {}).duplicate(true)
	staged_stock[REINFORCEMENT_MATERIAL_ID] = (
		int(staged_stock.get(REINFORCEMENT_MATERIAL_ID, 0)) - reinforcement_units
	)
	staged_resources["material_stock"] = staged_stock
	candidate.workshop_resources = staged_resources

	var result := resolve_with_rolls(candidate, item_uid, target_level, rolls, game_day)
	if str(result.get("outcome", "")) == "BLOCKED":
		return result
	var save_error: Error = save_service.save_envelope(candidate)
	if save_error != OK:
		return _blocked("SAVE_FAILED:%d" % int(save_error))

	resources.gold = int(staged_resources["gold"])
	resources.material_stock = staged_stock.duplicate(true)
	resources.changed.emit(resources.snapshot())
	result["gold_cost"] = gold_cost
	result["reinforcement_units"] = reinforcement_units
	result["envelope"] = candidate
	return result


func resolve_with_rolls(
	envelope,
	item_uid: String,
	target_level: int,
	rolls: Dictionary,
	game_day: int
) -> Dictionary:
	if envelope == null:
		return _blocked("MISSING_SAVE_ENVELOPE")
	if game_day < 1:
		return _blocked("INVALID_GAME_DAY")
	if not envelope.has_method("get_item") or not envelope.has_method("archive_destroyed_record"):
		return _blocked("INVALID_SAVE_ENVELOPE")

	var item = envelope.get_item(item_uid)
	if item == null:
		return _blocked("ITEM_NOT_FOUND")
	if str(item.physical_state) == "DESTROYED":
		return _blocked("ITEM_DESTROYED")
	if envelope.destroyed_history_by_uid.has(item_uid):
		return _blocked("DESTROYED_HISTORY_UID_CONFLICT")

	var staged_item = ItemScript.from_dict(item.to_dict())
	if staged_item == null or not staged_item.validation_errors.is_empty():
		return _blocked("INVALID_ITEM_STATE")

	var before_current: int = int(staged_item.current_durability)
	var before_max: int = int(staged_item.max_durability)
	var resolver = EnhancementResolverScript.new()
	var result: Dictionary = resolver.resolve_with_rolls(
		staged_item,
		target_level,
		rolls.duplicate(true)
	)
	if str(result.get("outcome", "")) == "BLOCKED":
		result["destroyed_history_archived"] = false
		return result

	var staged_record = null
	if str(staged_item.physical_state) == "DESTROYED":
		var direct_cause := _destruction_cause_for_result(str(result.get("outcome", "")))
		if direct_cause.is_empty():
			return _blocked("MISSING_DESTRUCTION_CAUSE")
		staged_record = DestroyedHistoryRecordScript.from_item(
			staged_item,
			game_day,
			direct_cause,
			before_current,
			before_max
		)
		if staged_record == null or not staged_record.validation_errors.is_empty():
			return _blocked("INVALID_DESTROYED_HISTORY_RECORD")
		var archive_error: Error = envelope.archive_destroyed_record(staged_record)
		if archive_error != OK:
			return _blocked("DESTROYED_HISTORY_ARCHIVE_FAILED:%d" % int(archive_error))

	_commit_enhancement_state(item, staged_item)
	result["destroyed_history_archived"] = staged_record != null
	return result


func _commit_enhancement_state(item, staged_item) -> void:
	item.enhancement_level = int(staged_item.enhancement_level)
	item.highest_checkpoint = int(staged_item.highest_checkpoint)
	item.enhancement_recovery_by_target = staged_item.enhancement_recovery_by_target.duplicate(true)
	item.current_durability = int(staged_item.current_durability)
	item.max_durability = int(staged_item.max_durability)
	item.base_max_durability = int(staged_item.base_max_durability)
	item.repair_job_available = bool(staged_item.repair_job_available)
	item.max_enhancement_reached = bool(staged_item.max_enhancement_reached)
	item.physical_state = str(staged_item.physical_state)
	item.catalyst_affix = str(staged_item.catalyst_affix)


func _destruction_cause_for_result(outcome: String) -> String:
	if outcome == "FAILED_DAMAGE":
		return "ENHANCEMENT_DAMAGE"
	return ""


func _blocked(reason: String) -> Dictionary:
	return {
		"outcome": "BLOCKED",
		"reason": reason,
		"destroyed_history_archived": false,
	}
