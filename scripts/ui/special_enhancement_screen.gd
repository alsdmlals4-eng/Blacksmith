# +10 단위에서만 재료 선택과 정밀 판정을 제공하는 특수 강화 화면입니다.
extends "res://scripts/ui/enhancement_screen.gd"


func _build_interface() -> void:
	super._build_interface()
	_replace_control_text(self, "+10 재료 이정표: 첫 수식어 추가", "+10 [특수 강화]: 첫 수식어 추가")
	_replace_control_text(self, "4회 원클릭 → +5 정밀 → +10 재료 정밀", "9회 원클릭 → +10 특수 강화")
	_replace_control_text(self, "+10 단위 강화 재료", "[특수 강화] 보조재료·촉매")
	_replace_control_text(
		self,
		"보조재료와 촉매는 +10·+20·…·+100에서만 선택하고 적용합니다.",
		"보조재료·촉매·정밀 판정은 +10·+20·…·+100 특수 강화에서만 적용합니다."
	)
	_replace_control_text(self, "정밀 강화", "[특수 강화] 정밀 판정")
	_replace_control_text(
		self,
		"+5 단위에서 흰 포인터가 황금 구간에 들어왔을 때 타격하세요.",
		"+10 단위 특수 강화에서 흰 포인터가 황금 구간에 들어왔을 때 타격하세요."
	)
	_replace_control_text(self, "정밀 강화 타격!", "특수 강화 타격!")
	_replace_control_text(
		self,
		"+5 단위는 정밀 강화, +10 단위에서만 재료를 선택합니다.",
		"+1~+9는 원클릭, +10 단위에서만 특수 강화를 진행합니다."
	)


func _refresh(snapshot: Dictionary) -> void:
	super._refresh(snapshot)
	var current_state := int(snapshot["state"])
	var target_level := int(snapshot["target_level"])
	var is_special := bool(snapshot["uses_materials"])
	material_panel.visible = is_special and current_state != EnhancementSessionScript.State.COMPLETE

	if is_special:
		var precision: Dictionary = session.config["precision"]
		var base_chance := float(snapshot["base_success_chance"])
		chance_label.text = "[특수 강화] 기본 %d%% · GOOD %d%% · PERFECT %d%%" % [
			int(round(base_chance * 100.0)),
			int(round(session.calculate_success_chance(float(precision["good_success_bonus"])) * 100.0)),
			int(round(session.calculate_success_chance(float(precision["perfect_success_bonus"])) * 100.0)),
		]
		attempt_button.text = "+%d 특수 강화" % target_level
		cadence_label.text = "+%d: 보조재료·촉매 선택 + 정밀 판정" % target_level
	else:
		chance_label.text = "원클릭 강화 성공률 %d%%" % int(round(float(snapshot["base_success_chance"]) * 100.0))
		attempt_button.text = "+%d 원클릭 강화" % target_level
		var next_special := int(ceil(float(target_level) / 10.0) * 10.0)
		cadence_label.text = "+%d까지 원클릭 · +%d에서 특수 강화" % [next_special - 1, next_special]

	if float(snapshot["pity_bonus"]) > 0.0:
		chance_label.text += " · 실패 보정 +%d%%" % int(round(float(snapshot["pity_bonus"]) * 100.0))


func _apply_state(new_state: int, snapshot: Dictionary) -> void:
	super._apply_state(new_state, snapshot)
	var is_special := bool(snapshot["uses_materials"])
	match new_state:
		EnhancementSessionScript.State.READY:
			helper_label.text = (
				"보조재료와 촉매를 선택한 뒤 특수 강화를 시작하세요."
				if is_special
				else "현재 단계는 원클릭 일반 강화입니다. 재료와 정밀 판정은 적용되지 않습니다."
			)
		EnhancementSessionScript.State.PRECISION:
			helper_label.text = "선택한 보조재료와 촉매는 이번 특수 강화 시도에만 적용됩니다."
		EnhancementSessionScript.State.COMPLETE:
			helper_label.text = "+100 특수 강화를 완료했습니다."


func _on_attempt_resolved(result: Dictionary) -> void:
	super._on_attempt_resolved(result)
	if bool(result.get("success", false)) and bool(result.get("uses_materials", false)):
		attempt_result_label.text = "특수 강화 성공! %s · +%d 수식어 성장 적용" % [
			str(session.get_display_name()),
			int(result.get("target_level", 0)),
		]


func _format_milestone_preview(preview: Dictionary) -> String:
	if preview.is_empty():
		return "+100 특수 강화 이정표 완료"
	var level := int(preview.get("level", 0))
	var label := str(preview.get("label", "특수 강화"))
	var effect := str(preview.get("effect", ""))
	if effect == "ASCEND_ALL":
		return "+%d [특수 강화] %s" % [level, label]
	var affix: Dictionary = preview.get("affix", {})
	var affix_name := str(affix.get("name", "미정"))
	if effect == "UPGRADE_AFFIX":
		return "+%d [특수 강화] %s: %s 티어 상승" % [level, label, affix_name]
	return "+%d [특수 강화] %s: %s 후보" % [level, label, affix_name]


func _replace_control_text(root: Node, before: String, after: String) -> void:
	for child in root.get_children():
		if child is Label and child.text == before:
			child.text = after
		elif child is Button and child.text == before:
			child.text = after
		_replace_control_text(child, before, after)
