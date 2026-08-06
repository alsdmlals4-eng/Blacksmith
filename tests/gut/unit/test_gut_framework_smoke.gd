extends "res://addons/gut/test.gd"


func test_gut_framework_is_consumed_by_ci() -> void:
    assert_eq(2 + 2, 4, "GUT 9.7.1 should execute a real project test")
