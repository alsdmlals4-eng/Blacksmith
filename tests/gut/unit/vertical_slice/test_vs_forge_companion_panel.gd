extends GutTest

const Save = preload("res://scripts/vertical_slice/services/vs_save_service.gd")
const Init = preload("res://scripts/vertical_slice/services/vs_run_initializer_service.gd")
const Modak = preload("res://scripts/vertical_slice/services/vs_modak_growth_service.gd")
const PANEL = "res://scripts/vertical_slice/ui/vs_forge_companion_panel.gd"
var save
var panel

func before_each():
	save = Save.new("user://modak-panel-" + str(Time.get_ticks_usec()) + ".json")
	assert_eq(save.save_envelope(Init.new().create_replan_candidate_envelope()), OK)
	panel = load(PANEL).new() if ResourceLoader.exists(PANEL) else null
	if panel != null:
		add_child_autofree(panel)
		panel.configure_context(save.load_envelope(), save)

func after_each():
	for path in [save.save_path, save.temp_path, save.backup_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func _available():
	assert_not_null(panel)
	return panel != null

func test_join_is_voluntary_and_signals_only_verified_save():
	if not _available(): return
	watch_signals(panel)
	assert_false(save.load_envelope().active_run.has("modak"))
	assert_true(panel.get_node("Join").visible)
	panel.request_join()
	assert_signal_emitted(panel, "campaign_saved")
	assert_true(save.load_envelope().active_run.has("modak"))
	assert_false(panel.get_node("Join").visible)

func test_duplicate_skip_reduced_motion_and_reconfigure_never_mutate_save():
	if not _available(): return
	panel.request_join()
	var before = save.load_envelope().to_dict()
	assert_true(panel.present_committed_result("event-1", "HANDOFF"))
	assert_false(panel.present_committed_result("event-1", "HANDOFF"))
	panel.skip_presentation()
	assert_eq(panel.presentation_state(), "IDLE")
	panel.configure_context(save.load_envelope(), save)
	assert_false(panel.present_committed_result("event-1", "HANDOFF"))
	panel.set_reduced_motion(true)
	assert_true(panel.present_committed_result("event-2", "FAILED_HOLD"))
	assert_eq(panel.presentation_state(), "IDLE")
	assert_eq(save.load_envelope().to_dict(), before)
	assert_false(panel.present_committed_result("", "SUCCESS"))
	assert_false(panel.present_committed_result("event-3", "BLOCKED"))

class UncertainSave extends RefCounted:
	var real
	func load_envelope(): return real.load_envelope()
	func save_envelope(value):
		real.save_envelope(value)
		return ERR_CANT_CREATE

func test_uncertainty_blocks_other_writes_and_explicit_readback_recovers_without_celebration():
	if not _available(): return
	var fault = UncertainSave.new()
	fault.real = save
	panel.configure_context(save.load_envelope(), fault)
	watch_signals(panel)
	panel.request_join()
	assert_true(panel.write_uncertain())
	assert_signal_not_emitted(panel, "campaign_saved")
	assert_false(panel.present_committed_result("event-1", "SUCCESS"))
	assert_true(panel.get_node("Retry").visible)
	panel.confirm_saved_join()
	assert_false(panel.write_uncertain())
	assert_signal_emitted(panel, "campaign_saved")
	assert_eq(panel.presentation_state(), "IDLE")

func test_external_guard_hidden_panel_and_scene_exit_do_not_write():
	if not _available(): return
	var before = save.load_envelope().to_dict()
	panel.set_external_write_blocked(true)
	panel.request_join()
	assert_eq(save.load_envelope().to_dict(), before)
	panel.set_external_write_blocked(false)
	panel.hide()
	panel.request_join()
	assert_eq(save.load_envelope().to_dict(), before)
	panel.show()
	panel.request_join()
	before = save.load_envelope().to_dict()
	panel.present_committed_result("exit", "SUCCESS")
	remove_child(panel)
	assert_eq(save.load_envelope().to_dict(), before)

class MissingImmediateReadback extends RefCounted:
	var real
	var miss_next = false
	func load_envelope():
		if miss_next:
			miss_next = false
			return null
		return real.load_envelope()
	func save_envelope(_value):
		miss_next = true
		return ERR_CANT_CREATE

func test_uncertain_prewrite_recovers_unchanged_unjoined_save_and_allows_retry():
	if not _available(): return
	var fault = MissingImmediateReadback.new()
	fault.real = save
	panel.configure_context(save.load_envelope(), fault)
	var original = save.load_envelope().to_dict()
	panel.request_join()
	assert_true(panel.write_uncertain())
	panel.confirm_saved_join()
	assert_false(panel.write_uncertain())
	assert_eq(save.load_envelope().to_dict(), original)
	assert_true(panel.get_node("Join").visible)
