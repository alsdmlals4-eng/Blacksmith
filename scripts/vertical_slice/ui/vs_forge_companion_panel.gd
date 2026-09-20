extends VBoxContainer

signal campaign_saved(envelope, result: Dictionary)
signal uncertainty_changed

const Service = preload("res://scripts/vertical_slice/services/vs_modak_growth_service.gd")
var _envelope
var _save
var _uncertain = false
var _external_write_blocked = false
var _seen: Dictionary = {}
var _run_id = ""
var _phase = "IDLE"
var _reduced_motion = false
var _tween: Tween

func configure_context(envelope, save) -> void:
	var run_id = str(envelope.active_run.get("run_id", "")) if envelope != null else ""
	if run_id != _run_id:
		skip_presentation()
		_seen.clear()
		_uncertain = false
		_run_id = run_id
	_envelope = envelope
	_save = save
	_build()
	_refresh()

func _build() -> void:
	if has_node("Summary"): return
	add_theme_constant_override("separation", 12)
	_label("Summary")
	_label("Reaction")
	_button("Join", "모닥을 공방 조수로 맞이하기 · 비용 없음", request_join)
	_button("Retry", "모닥 합류 저장 결과 다시 확인", confirm_saved_join)
	_button("Skip", "반응 바로 마치기", skip_presentation)
	var reduced = CheckButton.new()
	reduced.name = "ReducedMotion"
	reduced.text = "간단한 반응만 보기"
	reduced.custom_minimum_size.y = 96
	reduced.add_theme_font_size_override("font_size", 28)
	reduced.toggled.connect(set_reduced_motion)
	add_child(reduced)

func _label(node_name: String) -> void:
	var label = Label.new()
	label.name = node_name
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size", 28)
	label.add_theme_color_override("font_color", Color("2d211a"))
	var style = StyleBoxFlat.new()
	style.bg_color = Color("f3e3bf")
	for side in [SIDE_LEFT, SIDE_TOP, SIDE_RIGHT, SIDE_BOTTOM]: style.set_content_margin(side, 16)
	label.add_theme_stylebox_override("normal", style)
	add_child(label)

func _button(node_name: String, title: String, action: Callable) -> void:
	var button = Button.new()
	button.name = node_name
	button.text = title
	button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	button.custom_minimum_size.y = 96
	button.add_theme_font_size_override("font_size", 28)
	button.pressed.connect(action)
	add_child(button)

func _refresh() -> void:
	if not has_node("Summary"): return
	var state = Service.new().view(_envelope)
	var joined = state.stage == "EARLY"
	get_node("Summary").text = ("모닥 · 어린 불의 정령\n함께 납품한 날 %d일 · 합류 영업일 %d일\n아직 서툴지만, 여기서 함께 배워가요." % [state.productive_days, state.joined_day]) if joined else "작은 불의 정령이 공방을 기웃거립니다.\n힘을 되찾을 때까지 함께 일해도 될까요?"
	get_node("Join").visible = state.stage == "NOT_JOINED"
	get_node("Join").disabled = _uncertain or _external_write_blocked or _save == null
	get_node("Retry").visible = _uncertain
	get_node("Retry").disabled = _external_write_blocked or _save == null
	get_node("Skip").visible = _phase != "IDLE"
	get_node("ReducedMotion").visible = joined
	get_node("Reaction").visible = not get_node("Reaction").text.is_empty()

func request_join() -> void:
	if not is_visible_in_tree() or _uncertain or _external_write_blocked: return
	var result = Service.new().join(_envelope, _save)
	if result.has("envelope"):
		_envelope = result.envelope
		get_node("Reaction").text = "모닥: 나도 도울게! 아직 조금 서툴지만…!"
		campaign_saved.emit(_envelope, result)
	else:
		_uncertain = result.status == "COMMIT_UNCERTAIN"
		get_node("Reaction").text = "저장 결과를 확인해야 해요. 합류 성공으로 표시하지 않았습니다." if _uncertain else "합류를 저장하지 못했어요. 현재 저장을 확인한 뒤 다시 시도해 주세요."
	_refresh()
	uncertainty_changed.emit()

func confirm_saved_join() -> void:
	if not is_visible_in_tree() or not _uncertain or _external_write_blocked or _save == null: return
	var current = _save.load_envelope()
	if current == null or current.recovered_from_backup or not current.validation_errors.is_empty(): return
	if current.active_run.get("run_id", "") != _run_id: return
	var result = Service.new().join(current, _save) if current.active_run.has("modak") else {}
	if result.get("status", "") != "ALREADY_APPLIED": return
	_uncertain = false
	_envelope = result.envelope
	get_node("Reaction").text = "합류 저장을 다시 확인했어요. 이어서 작업할 수 있습니다."
	campaign_saved.emit(_envelope, result)
	_refresh()
	uncertainty_changed.emit()

func set_external_write_blocked(blocked: bool) -> void:
	_external_write_blocked = blocked
	_refresh()

func write_uncertain() -> bool:
	return _uncertain

# Caller supplies only a verified disk result identity. Never writes or rolls.
func present_committed_result(result_id: String, outcome: String) -> bool:
	if _uncertain or _external_write_blocked or not is_visible_in_tree() or Service.new().view(_envelope).stage != "EARLY": return false
	if result_id.is_empty() or _seen.has(result_id): return false
	var messages = {"SUCCESS":"모닥: 우와, 더 튼튼해졌어!", "FAILED_HOLD":"모닥: 앗… 괜찮아. 다시 차근차근 해보자.", "FAILED_DAMAGE":"모닥: 앗, 금이 갔어! 먼저 상태를 살펴보자.", "DESTROYED":"모닥: …다음 작품은 내가 더 잘 도울게.", "HANDOFF":"모닥: 잘 다녀와! 우리가 만든 작품이야."}
	if not messages.has(outcome): return false
	_seen[result_id] = true
	skip_presentation()
	get_node("Reaction").text = messages[outcome]
	if not _reduced_motion:
		_phase = "REACTION"
		_tween = create_tween()
		_tween.tween_interval(1.4)
		_tween.tween_callback(skip_presentation)
	_refresh()
	return true

func presentation_state() -> String:
	return _phase

func skip_presentation() -> void:
	if _tween != null and _tween.is_valid(): _tween.kill()
	_tween = null
	_phase = "IDLE"
	_refresh()

func set_reduced_motion(enabled: bool) -> void:
	_reduced_motion = enabled
	if enabled: skip_presentation()

func _exit_tree() -> void:
	if _tween != null and _tween.is_valid(): _tween.kill()
	_tween = null
	_phase = "IDLE"
