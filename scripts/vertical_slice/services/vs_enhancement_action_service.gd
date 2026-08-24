class_name VSEnhancementActionService
extends RefCounted

const ItemScript = preload("res://scripts/vertical_slice/domain/vs_item.gd")
const EnhancementResolverScript = preload(
	"res://scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd"
)
const DestroyedHistoryRecordScript = preload(
	"res://scripts/vertical_slice/domain/vs_destroyed_history_record.gd"
)


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
		var failure_family := str(result.get("failure_family", ""))
		if failure_family.is_empty():
			return _blocked("MISSING_DESTRUCTION_CAUSE")
		var direct_cause := "ENHANCEMENT_%s" % failure_family
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
	item.max_enhancement_reached = bool(staged_item.max_enhancement_reached)
	item.physical_state = str(staged_item.physical_state)


func _blocked(reason: String) -> Dictionary:
	return {
		"outcome": "BLOCKED",
		"reason": reason,
		"destroyed_history_archived": false,
	}
