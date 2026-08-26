# 현재 정본의 수리 비용·품질·흉터 결과를 해석한다.
class_name VSRepairResolver
extends RefCounted

const SETUP_FRACTION := 0.05
const VARIABLE_FRACTION := 0.65
const REINFORCEMENT_UNITS := 1
const R_BAND := {"PLUS_0_10": {"iron": 125, "silver": 145, "meteor_iron": 170}, "PLUS_11_30": {"iron": 160, "silver": 185, "meteor_iron": 215}, "PLUS_31_60": {"iron": 220, "silver": 255, "meteor_iron": 295}, "PLUS_61_90": {"iron": 300, "silver": 345, "meteor_iron": 405}, "PLUS_91_100": {"iron": 400, "silver": 460, "meteor_iron": 540}}
const QUALITY := [{"id": "EXCELLENT", "upper_percent": 20.0, "ratio": 1.0}, {"id": "STANDARD", "upper_percent": 80.0, "ratio": 0.75}, {"id": "POOR", "upper_percent": 100.0, "ratio": 0.5}]
const SCAR_CHANCE := {"MINOR": {"PLUS_0_10": 10.0, "PLUS_11_30": 15.0, "PLUS_31_60": 20.0, "PLUS_61_90": 25.0, "PLUS_91_100": 30.0}, "MAJOR": {"PLUS_0_10": 25.0, "PLUS_11_30": 30.0, "PLUS_31_60": 35.0, "PLUS_61_90": 40.0, "PLUS_91_100": 45.0}}


func quote(item) -> Dictionary:
	if item == null: return _blocked("MISSING_ITEM")
	if str(item.physical_state) == "DESTROYED" or int(item.current_durability) <= 0: return _blocked("ITEM_DESTROYED")
	if not bool(item.repair_job_available): return _blocked("REPAIR_JOB_UNAVAILABLE")
	if int(item.current_durability) >= int(item.max_durability): return _blocked("NO_CURRENT_DAMAGE")
	var band := _r_band_key(int(item.highest_checkpoint))
	var material := str(item.primary_material_id)
	if not R_BAND[band].has(material): return _blocked("UNSUPPORTED_PRIMARY_MATERIAL")
	var missing := int(item.max_durability) - int(item.current_durability)
	var reference := int(R_BAND[band][material])
	var burden := SETUP_FRACTION + VARIABLE_FRACTION * (float(missing) / float(item.base_max_durability))
	var gold_cost := int(ceil(float(reference) * burden))
	return {"allowed": true, "reason": "", "base_max": int(item.base_max_durability), "missing_current": missing, "r_band": reference, "r_band_key": band, "gold_cost": gold_cost, "reinforcement_units": REINFORCEMENT_UNITS, "result_current": int(item.max_durability), "result_max": int(item.max_durability), "quality_recovery_percent": {"EXCELLENT": 100, "STANDARD": 75, "POOR": 50}, "max_scar_chance_percent": _scar_chance(item), "repair_job_consumed_on_start": true}


func apply_with_rolls(item, available_gold: int, available_reinforcement: int, rolls: Dictionary) -> Dictionary:
	var repair_quote := quote(item)
	if not bool(repair_quote.get("allowed", false)): return {"status": "BLOCKED", "reason": str(repair_quote.get("reason", "REPAIR_NOT_ALLOWED"))}
	if available_gold < int(repair_quote["gold_cost"]): return {"status": "BLOCKED", "reason": "INSUFFICIENT_GOLD"}
	if available_reinforcement < REINFORCEMENT_UNITS: return {"status": "BLOCKED", "reason": "INSUFFICIENT_REINFORCEMENT"}
	var old_current := int(item.current_durability)
	var quality: Dictionary = _quality_for_roll(float(rolls.get("quality_roll_percent", 0.0)))
	var scar_triggered := float(rolls.get("scar_roll_percent", 100.0)) < _scar_chance(item)
	var post_scar_max := int(item.max_durability)
	var scar_skipped := false
	if scar_triggered and post_scar_max > 1:
		if post_scar_max - 1 > old_current: post_scar_max -= 1
		else: scar_skipped = true
	elif scar_triggered: scar_skipped = true
	item.repair_job_available = false
	item.max_durability = post_scar_max
	var quality_target := int(ceil(float(post_scar_max) * float(quality["ratio"])))
	item.current_durability = mini(post_scar_max, maxi(old_current + 1, quality_target))
	return {"status": "APPLIED", "reason": "", "quality": str(quality["id"]), "scar_triggered": scar_triggered and not scar_skipped, "scar_skipped": scar_skipped, "gold_cost": int(repair_quote["gold_cost"]), "reinforcement_units": REINFORCEMENT_UNITS, "result_current": int(item.current_durability), "result_max": int(item.max_durability)}


func apply(item, available_gold: int, available_reinforcement: int) -> Dictionary:
	return apply_with_rolls(item, available_gold, available_reinforcement, {"quality_roll_percent": 0.0, "scar_roll_percent": 100.0})


func _quality_for_roll(roll_percent: float) -> Dictionary:
	for quality in QUALITY:
		if roll_percent < float(quality["upper_percent"]): return quality
	return QUALITY.back()


func _scar_chance(item) -> float:
	var state := str(item.effective_durability_state())
	return 0.0 if not SCAR_CHANCE.has(state) else float(SCAR_CHANCE[state][_r_band_key(int(item.highest_checkpoint))])


func _r_band_key(highest_checkpoint: int) -> String:
	if highest_checkpoint >= 90: return "PLUS_91_100"
	if highest_checkpoint >= 60: return "PLUS_61_90"
	if highest_checkpoint >= 30: return "PLUS_31_60"
	if highest_checkpoint >= 11: return "PLUS_11_30"
	return "PLUS_0_10"


func _blocked(reason: String) -> Dictionary:
	return {"allowed": false, "reason": reason}
