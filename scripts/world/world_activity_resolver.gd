class_name WorldActivityResolver
extends RefCounted

var config: Dictionary = {}

const DETAIL_TEXT := {
	"DEFEAT": [
		"장비는 버텼지만 경기의 흐름을 뒤집지 못했습니다.",
		"카일은 패배했지만 장비의 약점을 분명히 확인했습니다.",
	],
	"WIN": [
		"카일이 철검의 균형을 살려 경기를 승리했습니다.",
		"제작 선택이 안정적인 승리로 이어졌습니다.",
	],
	"DECISIVE_WIN": [
		"카일이 압도적인 승리를 거두며 철검의 이름을 알렸습니다.",
		"강화와 수식어 조합이 경기장을 지배했습니다.",
	],
}


func _init(activity_config: Dictionary = {}) -> void:
	config = activity_config.duplicate(true)


func resolve(fit: Dictionary, detail_roll: float = 0.0) -> Dictionary:
	var score := int(fit.get("score", 0))
	var band_id := _band_for_score(score)
	var band: Dictionary = _band_config(band_id)
	var details: Array = DETAIL_TEXT.get(band_id, ["결과 기록이 생성되었습니다."])
	var index := mini(int(floor(clampf(detail_roll, 0.0, 0.999999) * details.size())), details.size() - 1)
	return {
		"result_id": band_id,
		"score": score,
		"detail_variant": index,
		"result_text": str(details[index]),
		"fame": int(band.get("fame", 0)),
		"relationship": int(band.get("relationship", 0)),
		"effective_choices": Array(fit.get("effective_choices", [])).duplicate(),
		"missing_conditions": Array(fit.get("missing_conditions", [])).duplicate(),
		"contributions": Dictionary(fit.get("contributions", {})).duplicate(true),
	}


func _band_for_score(score: int) -> String:
	var selected := ""
	for band_value in config.get("result_bands", []):
		var band: Dictionary = band_value
		if score >= int(band.get("minimum_score", 0)):
			selected = str(band.get("id", ""))
	return selected


func _band_config(band_id: String) -> Dictionary:
	for band_value in config.get("result_bands", []):
		var band: Dictionary = band_value
		if str(band.get("id", "")) == band_id:
			return band
	return {}
