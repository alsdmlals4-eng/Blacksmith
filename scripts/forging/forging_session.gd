class_name ForgingSession
extends RefCounted

signal changed(snapshot: Dictionary)
signal state_changed(new_state: int)
signal fever_started
signal fever_ended
signal completed(result: Dictionary)

enum State {
	FORGING,
	FINISHING,
	COMPLETE,
}

const DEFAULT_CONFIG := {
	"target_progress": 100.0,
	"tap_power": 2.5,
	"auto_work_per_second": 1.5,
	"rapid_tap_window_seconds": 0.22,
	"fever_gain_base": 6.0,
	"fever_gain_rapid": 11.0,
	"fever_charge_max": 100.0,
	"fever_decay_per_second": 10.0,
	"fever_duration_seconds": 6.0,
	"fever_multiplier": 2.5,
	"precision_speed": 0.85,
	"precision_target": 0.5,
	"precision_perfect_radius": 0.07,
	"precision_good_radius": 0.18,
}

var config: Dictionary = {}
var state: int = State.FORGING
var precision_enabled: bool = true
var progress: float = 0.0
var fever_charge: float = 0.0
var fever_time_left: float = 0.0
var precision_position: float = 0.0
var precision_direction: float = 1.0
var time_since_tap: float = 999.0
var tap_count: int = 0
var fever_activation_count: int = 0
var result: Dictionary = {}


func _init(custom_config: Dictionary = {}) -> void:
	config = DEFAULT_CONFIG.duplicate(true)
	for key in custom_config:
		config[key] = custom_config[key]
	_reset_values()


func reset() -> void:
	_reset_values()
	_emit_state()


func _reset_values() -> void:
	state = State.FORGING
	progress = 0.0
	fever_charge = 0.0
	fever_time_left = 0.0
	precision_position = 0.0
	precision_direction = 1.0
	time_since_tap = 999.0
	tap_count = 0
	fever_activation_count = 0
	result = {}


func set_precision_enabled(enabled: bool) -> void:
	if state != State.FORGING:
		return
	precision_enabled = enabled
	_emit_changed()


func register_tap() -> bool:
	if state != State.FORGING:
		return false

	tap_count += 1
	var rapid_tap := time_since_tap <= float(config["rapid_tap_window_seconds"])
	time_since_tap = 0.0

	if not is_fever_active():
		var fever_gain := float(config["fever_gain_rapid"] if rapid_tap else config["fever_gain_base"])
		fever_charge = minf(fever_charge + fever_gain, float(config["fever_charge_max"]))
		if fever_charge >= float(config["fever_charge_max"]):
			_start_fever()

	_add_progress(float(config["tap_power"]) * get_work_multiplier())
	_emit_changed()
	return true


func advance(delta: float) -> void:
	if delta <= 0.0:
		return

	time_since_tap += delta

	if is_fever_active():
		fever_time_left = maxf(fever_time_left - delta, 0.0)
		if fever_time_left <= 0.0:
			fever_ended.emit()
	else:
		fever_charge = maxf(fever_charge - float(config["fever_decay_per_second"]) * delta, 0.0)

	if state == State.FORGING:
		_add_progress(float(config["auto_work_per_second"]) * get_work_multiplier() * delta)
	elif state == State.FINISHING:
		_advance_precision(delta)

	_emit_changed()


func finish_precision() -> Dictionary:
	if state != State.FINISHING:
		return {}

	var distance := absf(precision_position - float(config["precision_target"]))
	var quality_id := "STANDARD"
	var quality_label := "보통 마감"
	var quality_multiplier := 1.0

	if distance <= float(config["precision_perfect_radius"]):
		quality_id = "PERFECT"
		quality_label = "완벽한 마감"
		quality_multiplier = 1.2
	elif distance <= float(config["precision_good_radius"]):
		quality_id = "GOOD"
		quality_label = "좋은 마감"
		quality_multiplier = 1.1

	_complete(quality_id, quality_label, quality_multiplier)
	return result.duplicate(true)


func is_fever_active() -> bool:
	return fever_time_left > 0.0


func get_work_multiplier() -> float:
	return float(config["fever_multiplier"]) if is_fever_active() else 1.0


func get_progress_ratio() -> float:
	return clampf(progress / float(config["target_progress"]), 0.0, 1.0)


func get_fever_ratio() -> float:
	if is_fever_active():
		return clampf(fever_time_left / float(config["fever_duration_seconds"]), 0.0, 1.0)
	return clampf(fever_charge / float(config["fever_charge_max"]), 0.0, 1.0)


func snapshot() -> Dictionary:
	return {
		"state": state,
		"progress": progress,
		"progress_ratio": get_progress_ratio(),
		"fever_charge": fever_charge,
		"fever_ratio": get_fever_ratio(),
		"fever_active": is_fever_active(),
		"fever_time_left": fever_time_left,
		"work_multiplier": get_work_multiplier(),
		"precision_enabled": precision_enabled,
		"precision_position": precision_position,
		"tap_count": tap_count,
		"fever_activation_count": fever_activation_count,
		"result": result.duplicate(true),
	}


func _start_fever() -> void:
	fever_charge = 0.0
	fever_time_left = float(config["fever_duration_seconds"])
	fever_activation_count += 1
	fever_started.emit()


func _add_progress(amount: float) -> void:
	if state != State.FORGING:
		return
	progress = minf(progress + maxf(amount, 0.0), float(config["target_progress"]))
	if progress >= float(config["target_progress"]):
		if precision_enabled:
			state = State.FINISHING
			precision_position = 0.0
			precision_direction = 1.0
			state_changed.emit(state)
		else:
			_complete("STANDARD", "자동 마감", 1.0)


func _advance_precision(delta: float) -> void:
	precision_position += precision_direction * float(config["precision_speed"]) * delta
	while precision_position > 1.0 or precision_position < 0.0:
		if precision_position > 1.0:
			precision_position = 2.0 - precision_position
			precision_direction = -1.0
		elif precision_position < 0.0:
			precision_position = -precision_position
			precision_direction = 1.0


func _complete(quality_id: String, quality_label: String, quality_multiplier: float) -> void:
	state = State.COMPLETE
	result = {
		"weapon_id": "iron_sword",
		"weapon_name": "철검",
		"quality_id": quality_id,
		"quality_label": quality_label,
		"quality_multiplier": quality_multiplier,
		"tap_count": tap_count,
		"fever_activation_count": fever_activation_count,
	}
	state_changed.emit(state)
	completed.emit(result.duplicate(true))
	_emit_changed()


func _emit_state() -> void:
	state_changed.emit(state)
	_emit_changed()


func _emit_changed() -> void:
	changed.emit(snapshot())
