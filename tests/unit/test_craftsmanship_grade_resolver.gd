extends SceneTree

const ResolverScript = preload("res://scripts/forging/craftsmanship_grade_resolver.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("CraftsmanshipGradeResolver tests PASSED (4 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	_test_fixed_roll_distribution()
	_test_precision_and_grade_are_separate()
	_test_legacy_quality_is_preserved_as_precision()
	_test_auto_record_gets_standard_grade()


func _test_fixed_roll_distribution() -> void:
	var resolver = ResolverScript.new()
	var low: Dictionary = resolver.resolve("PERFECT", 0.01)
	var high: Dictionary = resolver.resolve("PERFECT", 0.99)
	_expect(low.get("craftsmanship_grade_id") == "APPRENTICE", "PERFECT 분포의 낮은 roll은 APPRENTICE 경계여야 합니다.")
	_expect(high.get("craftsmanship_grade_id") == "PERFECT", "PERFECT 분포의 높은 roll은 PERFECT 경계여야 합니다.")


func _test_precision_and_grade_are_separate() -> void:
	var resolver = ResolverScript.new()
	var result: Dictionary = resolver.resolve("GOOD", 0.5)
	_expect(result.get("precision_result_id") == "GOOD", "정밀 결과는 GOOD으로 보존되어야 합니다.")
	_expect(result.has("craftsmanship_grade_id"), "영구 완성도 필드가 별도로 존재해야 합니다.")
	_expect(result.get("quality_id") == result.get("craftsmanship_grade_id"), "신규 quality_id는 완성도 호환 별칭이어야 합니다.")


func _test_legacy_quality_is_preserved_as_precision() -> void:
	var resolver = ResolverScript.new()
	var normalized: Dictionary = resolver.normalize_record({"quality_id": "PERFECT", "quality_label": "완벽한 마감"})
	_expect(normalized.get("record_schema_version") == 1, "변환 기록은 schema version 1이어야 합니다.")
	_expect(normalized.get("precision_result_id") == "PERFECT", "legacy PERFECT는 정밀 결과로 보존해야 합니다.")
	_expect(normalized.get("craftsmanship_grade_id") == "STANDARD", "legacy 기록의 완성도를 조용히 PERFECT로 재해석하면 안 됩니다.")


func _test_auto_record_gets_standard_grade() -> void:
	var resolver = ResolverScript.new()
	var normalized: Dictionary = resolver.normalize_record({"quality_id": "AUTO", "quality_label": "자동 단조"})
	_expect(normalized.get("precision_result_id") == "AUTO", "AUTO는 정밀 결과로 유지해야 합니다.")
	_expect(normalized.get("craftsmanship_grade_id") == "STANDARD", "자동 단조 legacy 기록은 STANDARD 완성도여야 합니다.")


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
