extends SceneTree

const ResolverScript = preload("res://scripts/world/world_activity_resolver.gd")

var failures: Array[String] = []


func _initialize() -> void:
	_run_tests()
	if failures.is_empty():
		print("WorldActivityResolver tests PASSED (4 cases)")
		quit(0)
		return
	for failure in failures:
		push_error(failure)
	quit(1)


func _run_tests() -> void:
	var resolver = ResolverScript.new(_config())
	_test_band(resolver, 30, "DEFEAT")
	_test_band(resolver, 40, "WIN")
	_test_band(resolver, 85, "DECISIVE_WIN")
	_test_detail_roll_does_not_change_band(resolver)


func _test_band(resolver, score: int, expected: String) -> void:
	var result: Dictionary = resolver.resolve(_fit(score), 0.25)
	_expect(result.get("result_id") == expected, "%d점은 %s여야 합니다." % [score, expected])


func _test_detail_roll_does_not_change_band(resolver) -> void:
	var low: Dictionary = resolver.resolve(_fit(40), 0.0)
	var high: Dictionary = resolver.resolve(_fit(40), 0.99)
	_expect(low.get("result_id") == high.get("result_id"), "detail roll은 결과 밴드를 바꾸면 안 됩니다.")
	_expect(low.get("detail_variant") != high.get("detail_variant"), "detail roll은 같은 밴드의 문장 변형만 바꿔야 합니다.")


func _fit(score: int) -> Dictionary:
	return {
		"score": score,
		"effective_choices": ["required_level"],
		"missing_conditions": ["preferred_affix"],
		"contributions": {"required_level": 20},
	}


func _config() -> Dictionary:
	return {
		"result_bands": [
			{"id": "DEFEAT", "minimum_score": 0, "fame": 0, "relationship": 0},
			{"id": "WIN", "minimum_score": 35, "fame": 2, "relationship": 1},
			{"id": "DECISIVE_WIN", "minimum_score": 70, "fame": 5, "relationship": 2},
		],
	}


func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
