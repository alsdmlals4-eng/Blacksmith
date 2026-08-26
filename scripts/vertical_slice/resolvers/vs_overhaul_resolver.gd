# 대수선 폐기 경로를 명시적으로 차단한다.
class_name VSOverhaulResolver
extends RefCounted


func quote(_item) -> Dictionary:
	return {"allowed": false, "reason": "OVERHAUL_SUPERSEDED"}


func apply(_item, _available_gold: int, _available_reinforcement: int) -> Dictionary:
	return {"status": "BLOCKED", "reason": "OVERHAUL_SUPERSEDED"}
