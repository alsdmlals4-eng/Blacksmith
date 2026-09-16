extends VBoxContainer

signal campaign_saved(envelope, result: Dictionary)
signal forge_requested(order_id: String)
signal uncertainty_changed

const Service = preload("res://scripts/vertical_slice/services/vs_commission_service.gd")
const Catalog = preload("res://scripts/vertical_slice/domain/vs_commission_catalog.gd")
const Equipment = preload("res://scripts/vertical_slice/domain/vs_equipment_catalog.gd")
var _envelope
var _save
var _pending: Dictionary = {}
var _uncertain = false
var _expanded = true
var _external_write_blocked = false
var _cancel_order_id = ""

func configure_context(envelope, save) -> void:
	_envelope = envelope
	_save = save
	_build()
	_refresh()

func _build() -> void:
	if has_node("Offers"): return
	add_theme_constant_override("separation", 12)
	_button("Toggle", "일반 의뢰 · 접기", _toggle)
	_label("Summary")
	_option("Offers", [])
	for definition in Catalog.all():
		var option = get_node("Offers")
		option.add_item("%s · %s +%d" % [Equipment.by_id(definition.equipment_id).display_name_ko,
			"기본" if definition.min_level == 0 else "목적", definition.min_level])
		option.set_item_metadata(option.item_count - 1, definition.definition_id)
	_option("Funding", ["고객 재료 · 판매", "개인 작품 · 판매", "개인 작품 · 대여"])
	_label("Comparison")
	_option("ItemChoice", [])
	_button("Accept", "선택 의뢰 수락 · 비용 없음", _execute.bind("ACCEPT"))
	_button("Reserve", "선택한 개인 작품을 의뢰에 배정", _execute.bind("RESERVE"))
	_button("Forge", "의뢰 재료로 제작 · 제작비 없음", _forge)
	_option("Catalyst", ["납품 보수 촉매 선택", "불의 심장 1개", "대지의 결정 1개"])
	_button("Handoff", "납품 · 보수 수령", _execute.bind("HANDOFF"))
	_button("Cancel", "의뢰 취소", _request_cancel)
	_button("Retry", "같은 거래 저장 결과 다시 확인", _retry)
	_label("Message")
	for key in ["Offers", "Funding", "ItemChoice", "Catalyst"]:
		get_node(key).item_selected.connect(func(_index): _refresh())

func _label(node_name: String) -> void:
	var label = Label.new()
	label.name = node_name
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	label.add_theme_font_size_override("font_size", 28)
	label.add_theme_color_override("font_color", Color("2d211a"))
	var style = StyleBoxFlat.new()
	style.bg_color = Color("f3e3bf")
	style.content_margin_left = 20
	style.content_margin_right = 20
	style.content_margin_top = 16
	style.content_margin_bottom = 16
	label.add_theme_stylebox_override("normal", style)
	add_child(label)

func _button(node_name: String, title: String, callback: Callable) -> void:
	var button = Button.new()
	button.name = node_name
	button.text = title
	button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	button.custom_minimum_size.y = 96
	button.add_theme_font_size_override("font_size", 28)
	button.pressed.connect(callback)
	add_child(button)

func _option(node_name: String, titles: Array) -> void:
	var option = OptionButton.new()
	option.name = node_name
	option.custom_minimum_size.y = 96
	option.fit_to_longest_item = false
	option.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	option.add_theme_font_size_override("font_size", 28)
	option.get_popup().add_theme_font_size_override("font_size", 28)
	for title in titles: option.add_item(title)
	add_child(option)

func _definition() -> Dictionary:
	var active = _envelope.active_run.get("commission", {}).get("active_order", {})
	if not active.is_empty(): return active.definition_snapshot
	var offers = get_node("Offers")
	return Catalog.by_id(str(offers.get_item_metadata(offers.selected)))

func _refresh() -> void:
	if _envelope == null: return
	var active = _envelope.active_run.get("commission", {}).get("active_order", {})
	var phase = active.get("phase", "OFFER")
	var definition = _definition()
	if definition.is_empty(): return
	var player = (get_node("Funding").selected > 0) if active.is_empty() else active.funding_origin == "PLAYER"
	var mode = ("LOAN" if get_node("Funding").selected == 2 else "SALE") if active.is_empty() else active.ownership_mode
	var choice = get_node("ItemChoice")
	var previous = str(choice.get_item_metadata(choice.selected)) if choice.selected >= 0 else ""
	choice.clear()
	choice.add_item("개인 작품을 선택하세요")
	choice.set_item_metadata(0, "")
	var uids = _envelope.items_by_uid.keys()
	uids.sort()
	for uid in uids:
		var item = _envelope.get_item(uid)
		if item.owner_id != "PLAYER" or item.current_durability <= 0: continue
		choice.add_item("%s +%d · %s" % [Equipment.by_item(item).display_name_ko, item.enhancement_level, str(uid).right(8)])
		choice.set_item_metadata(choice.item_count - 1, uid)
		if uid == previous: choice.select(choice.item_count - 1)
	var selected_uid = str(choice.get_item_metadata(choice.selected))
	var reserved_uid = str(active.get("item_uid", ""))
	var item = _envelope.get_item(reserved_uid if not reserved_uid.is_empty() else selected_uid)
	var preview = Catalog.preview(definition, item)
	get_node("Summary").text = "%s · 최소 +%d\n%s\n%s\n400골드 + 보강재 2 + 선택 촉매 1 (시험값)\n%s · 강화·수리비 환급 없음\n%s" % [
		preview.equipment_name, preview.min_level, preview.purpose.description, preview.purpose.recommendation,
		"판매 후 고객 소유 · 반환 없음" if mode == "SALE" else "대여 후 같은 UID 반환",
		"기본 검수: 인계 다음 날 보고" if definition.min_level == 0 else "전선 엄호: 인계 3일 뒤 보고 / 성공과 손상 독립"]
	if phase != "OFFER": get_node("Summary").text += "\n" + str(active.order_id) + " · " + str(phase)
	get_node("Summary").text += "\n" + ("기본 검수 · 비전투 / 손상 없음" if definition.min_level == 0 else "실제 사용 위험 HIGH · 내구도 상태 반영")
	var risk = Service.handoff_preview(definition, item)
	if not risk.is_empty():
		get_node("Summary").text += "\n성공 %.1f%% / 손상 %.1f%% · 독립 판정 (시험값)" % [risk.success_percent, risk.damage_percent]
	else:
		get_node("Summary").text += "\n작품 선택·준비 후 성공/손상 확률 확인 (시험값)"
	if phase == "IN_TRANSIT": get_node("Summary").text = Service.report(active)
	get_node("Comparison").text = "개인 작품의 종류·강화 단계를 비교해 배정하세요."
	if item != null:
		get_node("Comparison").text = "현재 작품 %s +%d / 요구 %s +%d\nUID %s\n%s" % [Equipment.by_item(item).display_name_ko,
			item.enhancement_level, preview.equipment_name, preview.min_level, item.uid,
			"납품 조건 충족" if preview.allowed else "종류 또는 최소 강화 단계 부족 · 아래 공방에서 준비하세요"]
	for child in get_children():
		if child is BaseButton: child.disabled = _uncertain or _external_write_blocked or _save == null
		if child is Control: child.visible = _expanded or child.name in ["Toggle", "Summary", "Message", "Retry"]
	get_node("Toggle").disabled = false
	get_node("Toggle").text = "일반 의뢰 · 접기" if _expanded else "일반 의뢰 · 펼치기"
	get_node("Offers").visible = _expanded and phase == "OFFER"
	get_node("Funding").visible = _expanded and phase == "OFFER"
	get_node("Accept").visible = _expanded and phase == "OFFER"
	get_node("ItemChoice").visible = _expanded and player and phase in ["OFFER", "ACCEPTED"]
	get_node("Comparison").visible = _expanded and phase != "IN_TRANSIT"
	get_node("Reserve").visible = _expanded and phase == "ACCEPTED" and player
	get_node("Reserve").disabled = _uncertain or _external_write_blocked or _save == null or selected_uid.is_empty()
	get_node("Forge").visible = _expanded and phase == "ACCEPTED" and not player
	get_node("Cancel").visible = _expanded and phase in ["ACCEPTED", "READY"]
	get_node("Cancel").text = "의뢰 취소 · 개인 작품 배정만 해제" if player else ("의뢰 취소 · 완성품을 고객에게 반환" if phase == "READY" else "의뢰 취소 · 미사용 재료 반환")
	get_node("Catalyst").visible = _expanded and phase == "READY"
	get_node("Handoff").visible = _expanded and phase == "READY"
	get_node("Handoff").disabled = _uncertain or _external_write_blocked or _save == null or not preview.allowed or item == null or item.current_durability <= 0 or get_node("Catalyst").selected == 0
	get_node("Retry").visible = _uncertain
	get_node("Retry").disabled = _save == null or _external_write_blocked
	get_node("Message").visible = not get_node("Message").text.is_empty()

func _toggle() -> void:
	_expanded = not _expanded
	_refresh()

func _forge() -> void:
	if not is_visible_in_tree() or _uncertain or _external_write_blocked: return
	var active = _envelope.active_run.get("commission", {}).get("active_order", {})
	if active.get("phase", "") == "ACCEPTED" and active.funding_origin == "COMMISSION_ESCROW": forge_requested.emit(active.order_id)

func _execute(action: String) -> void:
	if not is_visible_in_tree() or _uncertain or _external_write_blocked or _save == null: return
	var active = _envelope.active_run.get("commission", {}).get("active_order", {})
	var choice = get_node("ItemChoice")
	_pending = {"action":action, "source":_envelope, "order_id":active.get("order_id", ""),
		"definition_id":_definition().definition_id, "funding":"COMMISSION_ESCROW" if get_node("Funding").selected == 0 else "PLAYER",
		"mode":"LOAN" if get_node("Funding").selected == 2 else "SALE",
		"uid":str(choice.get_item_metadata(choice.selected)),
		"catalyst":["", "heart_of_flame", "earth_crystal"][get_node("Catalyst").selected]}
	_retry()

func _retry() -> void:
	if not is_visible_in_tree() or _pending.is_empty() or _external_write_blocked: return
	var service = Service.new()
	var result: Dictionary
	match _pending.action:
		"ACCEPT": result = service.accept(_pending.source, _pending.definition_id, _save, _pending.funding, _pending.mode)
		"RESERVE": result = service.reserve_item(_pending.source, _pending.order_id, _pending.uid, _save)
		"CANCEL": result = service.cancel(_pending.source, _pending.order_id, _save)
		"HANDOFF":
			if _pending.has("rolls"):
				result = service.handoff_with_rolls(_pending.source, _pending.order_id, _pending.catalyst, _pending.rolls, _save)
			else:
				result = service.handoff(_pending.source, _pending.order_id, _pending.catalyst, _save)
		_: return
	if result.has("envelope"):
		_uncertain = false
		_pending = {}
		_envelope = result.envelope
		get_node("Message").text = "저장 확인 완료 · 공방 재화·작품·일정 갱신"
		result["commission_refresh"] = true
		campaign_saved.emit(_envelope, result)
	else:
		if result.has("retry_rolls"): _pending["rolls"] = result.retry_rolls.duplicate()
		_uncertain = _uncertain or result.status == "COMMIT_UNCERTAIN"
		get_node("Message").text = ("저장 결과 확인 필요 · 같은 거래로 재확인하세요. " if _uncertain else "처리하지 못했습니다. ") + str(result.get("reason", ""))
	_refresh()
	uncertainty_changed.emit()

func set_external_write_blocked(blocked: bool) -> void:
	_external_write_blocked = blocked
	_refresh()

func _request_cancel() -> void:
	if not is_visible_in_tree() or _uncertain or _external_write_blocked or _save == null: return
	var active = _envelope.active_run.get("commission", {}).get("active_order", {})
	if active.get("phase", "") not in ["ACCEPTED", "READY"]: return
	if active.funding_origin == "PLAYER" or active.phase == "ACCEPTED":
		_execute("CANCEL")
		return
	var dialog = get_node_or_null("CancelConfirmation")
	if dialog == null:
		dialog = ConfirmationDialog.new()
		dialog.name = "CancelConfirmation"
		dialog.title = "완성품을 고객에게 반환할까요?"
		dialog.ok_button_text = "반환하고 취소"
		dialog.cancel_button_text = "의뢰 계속하기"
		add_child(dialog)
		dialog.get_label().add_theme_font_size_override("font_size", 28)
		dialog.get_label().autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		dialog.add_theme_constant_override("buttons_min_width", 272)
		dialog.add_theme_constant_override("buttons_min_height", 96)
		for button in [dialog.get_ok_button(), dialog.get_cancel_button()]: button.add_theme_font_size_override("font_size", 28)
		dialog.confirmed.connect(_confirm_cancel)
		dialog.canceled.connect(func(): _cancel_order_id = "")
	_cancel_order_id = active.order_id
	dialog.dialog_text = "고객 재료로 만든 완성 장비와 UID를 고객에게 반환합니다.\nUID %s\n개인 골드·촉매·보강재로 강화·수리한 비용 환급 없음.\n납품 보수 없음. 이 작품은 개인 소유로 남지 않습니다." % active.item_uid
	dialog.popup_centered(Vector2i(660, 520))

func _confirm_cancel() -> void:
	var active = _envelope.active_run.get("commission", {}).get("active_order", {})
	var confirmed_order = _cancel_order_id
	_cancel_order_id = ""
	if confirmed_order.is_empty() or active.get("order_id", "") != confirmed_order: return
	_execute("CANCEL")
