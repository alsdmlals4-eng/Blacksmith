class_name CraftsmanshipGradeResolver
extends RefCounted

const DEFAULT_DATA_PATH := "res://data/crafting/craftsmanship_grades.json"

var grade_by_id: Dictionary = {}
var distributions: Dictionary = {}


func _init(config: Dictionary = {}) -> void:
	var source := config.duplicate(true)
	if source.is_empty():
		source = _load_json(DEFAULT_DATA_PATH)
	for item in source.get("grades", []):
		if item is Dictionary:
			grade_by_id[str(item.get("id", ""))] = Dictionary(item).duplicate(true)
	distributions = Dictionary(source.get("precision_distributions", {})).duplicate(true)


func resolve(precision_result_id: String, roll: float) -> Dictionary:
	var distribution: Dictionary = distributions.get(precision_result_id, distributions.get("STANDARD", {}))
	if distribution.is_empty():
		return {}
	var normalized_roll := clampf(roll, 0.0, 0.999999)
	var cursor := 0.0
	for grade_id in _ordered_grade_ids():
		cursor += float(distribution.get(grade_id, 0.0))
		if normalized_roll < cursor:
			return _grade_result(grade_id, precision_result_id)
	var fallback_id := _ordered_grade_ids().back() if not _ordered_grade_ids().is_empty() else ""
	return _grade_result(fallback_id, precision_result_id)


func normalize_record(record: Dictionary) -> Dictionary:
	var normalized := record.duplicate(true)
	var legacy_quality_id := str(normalized.get("quality_id", "STANDARD"))
	var precision_id := str(normalized.get("precision_result_id", legacy_quality_id))
	if precision_id == "":
		precision_id = "STANDARD"
	var grade_id := str(normalized.get("craftsmanship_grade_id", ""))
	if grade_id == "" or not grade_by_id.has(grade_id):
		grade_id = "STANDARD" if grade_by_id.has("STANDARD") else _ordered_grade_ids()[0]
	var grade: Dictionary = grade_by_id.get(grade_id, {})
	normalized["record_schema_version"] = 1
	normalized["precision_result_id"] = precision_id
	normalized["precision_result_label"] = str(normalized.get("precision_result_label", normalized.get("quality_label", _precision_label(precision_id))))
	normalized["craftsmanship_grade_id"] = grade_id
	normalized["craftsmanship_grade_label"] = str(grade.get("name", grade_id))
	normalized["craftsmanship_score_bonus"] = int(grade.get("score_bonus", 0))
	# 신규 quality_*는 완성도 호환 별칭이다. legacy 입력은 precision_result_*에 보존한다.
	normalized["quality_id"] = grade_id
	normalized["quality_label"] = str(grade.get("name", grade_id))
	return normalized


func _grade_result(grade_id: String, precision_result_id: String) -> Dictionary:
	if not grade_by_id.has(grade_id):
		return {}
	var grade: Dictionary = Dictionary(grade_by_id[grade_id]).duplicate(true)
	return {
		"record_schema_version": 1,
		"precision_result_id": precision_result_id,
		"precision_result_label": _precision_label(precision_result_id),
		"craftsmanship_grade_id": grade_id,
		"craftsmanship_grade_label": str(grade.get("name", grade_id)),
		"craftsmanship_score_bonus": int(grade.get("score_bonus", 0)),
		"craftsmanship_attack_multiplier": float(grade.get("attack_multiplier", 1.0)),
		"craftsmanship_value_multiplier": float(grade.get("value_multiplier", 1.0)),
		"quality_id": grade_id,
		"quality_label": str(grade.get("name", grade_id)),
	}


func _ordered_grade_ids() -> Array[String]:
	var ids: Array[String] = []
	for grade_id in grade_by_id:
		ids.append(str(grade_id))
	ids.sort_custom(func(a: String, b: String) -> bool:
		return int(grade_by_id[a].get("score_bonus", 0)) < int(grade_by_id[b].get("score_bonus", 0))
	)
	return ids


func _precision_label(precision_result_id: String) -> String:
	match precision_result_id:
		"AUTO": return "자동 마감"
		"GOOD": return "좋은 마감"
		"PERFECT": return "완벽한 마감"
		_: return "보통 마감"


func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	return parsed if parsed is Dictionary else {}
