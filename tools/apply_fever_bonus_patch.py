#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def r(rel: str, old: str, new: str) -> None:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"missing: {rel}")
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"anchor mismatch: {rel} count={count} old={old[:90]!r}")
    path.write_text(source.replace(old, new), encoding="utf-8")


def rn(rel: str, old: str, new: str, expected: int) -> None:
    path = ROOT / rel
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != expected:
        raise SystemExit(f"anchor count mismatch: {rel} count={count} expected={expected} old={old[:90]!r}")
    path.write_text(source.replace(old, new), encoding="utf-8")


def a(rel: str, marker: str, block: str) -> None:
    path = ROOT / rel
    source = path.read_text(encoding="utf-8")
    if marker in source:
        raise SystemExit(f"duplicate: {rel} {marker}")
    path.write_text(source.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


path = ROOT / "data/crafting/forging_balance.json"
data = json.loads(path.read_text(encoding="utf-8"))
data["schema_version"] = 2
session = data["session"]
ordered = {}
for key, value in session.items():
    ordered[key] = value
    if key == "fever_multiplier":
        ordered["fever_result_required_activations"] = 1
        ordered["fever_result_attack_multiplier"] = 1.05
        ordered["fever_result_value_multiplier"] = 1.03
data["session"] = ordered
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

r("scripts/forging/forging_session.gd",
  '\t"fever_multiplier": 2.5,\n\t"precision_speed": 0.85,',
  '\t"fever_multiplier": 2.5,\n\t"fever_result_required_activations": 1,\n\t"fever_result_attack_multiplier": 1.05,\n\t"fever_result_value_multiplier": 1.03,\n\t"precision_speed": 0.85,')
r("scripts/forging/forging_session.gd",
  '''\tstate = State.COMPLETE
\tvar raw_base_attack := maxi(int(config.get("weapon_base_attack", 20)), 1)
\tvar applied_base_attack := maxi(int(round(float(raw_base_attack) * attack_multiplier)), 1)
\tresult = {''',
  '''\tstate = State.COMPLETE
\tvar raw_base_attack := maxi(int(config.get("weapon_base_attack", 20)), 1)
\tvar required_activations := maxi(int(config.get("fever_result_required_activations", 1)), 1)
\tvar fever_bonus_applied := fever_activation_count >= required_activations
\tvar fever_attack_multiplier := float(config.get("fever_result_attack_multiplier", 1.05)) if fever_bonus_applied else 1.0
\tvar fever_value_multiplier := float(config.get("fever_result_value_multiplier", 1.03)) if fever_bonus_applied else 1.0
\tvar crafting_attack_multiplier := maxf(attack_multiplier + fever_attack_multiplier - 1.0, 0.01)
\tvar crafting_value_multiplier := maxf(value_multiplier + fever_value_multiplier - 1.0, 0.01)
\tvar applied_base_attack := maxi(int(round(float(raw_base_attack) * crafting_attack_multiplier)), 1)
\tresult = {''')
r("scripts/forging/forging_session.gd",
  '''\t\t"quality_attack_multiplier": attack_multiplier,
\t\t"quality_value_multiplier": value_multiplier,
\t\t"tap_count": tap_count,''',
  '''\t\t"quality_attack_multiplier": attack_multiplier,
\t\t"quality_value_multiplier": value_multiplier,
\t\t"fever_bonus_applied": fever_bonus_applied,
\t\t"fever_attack_multiplier": fever_attack_multiplier,
\t\t"fever_value_multiplier": fever_value_multiplier,
\t\t"crafting_attack_multiplier": crafting_attack_multiplier,
\t\t"crafting_value_multiplier": crafting_value_multiplier,
\t\t"tap_count": tap_count,''')

r("scripts/enhancement/enhancement_session.gd",
  '''var quality_attack_multiplier: float = 1.0
var quality_value_multiplier: float = 1.0
var progression_attack: int = 20''',
  '''var quality_attack_multiplier: float = 1.0
var quality_value_multiplier: float = 1.0
var fever_activation_count: int = 0
var fever_bonus_applied: bool = false
var fever_attack_multiplier: float = 1.0
var fever_value_multiplier: float = 1.0
var crafting_attack_multiplier: float = 1.0
var crafting_value_multiplier: float = 1.0
var progression_attack: int = 20''')
r("scripts/enhancement/enhancement_session.gd",
  '''\tquality_attack_multiplier = maxf(float(weapon.get("quality_attack_multiplier", 1.0)), 0.01)
\tquality_value_multiplier = maxf(float(weapon.get("quality_value_multiplier", 1.0)), 0.01)
\tbase_attack = maxi(int(weapon.get("base_attack", round(float(raw_base_attack) * quality_attack_multiplier))), 1)
\tprogression_attack = base_attack
\tvalue_bonus_total = maxf(quality_value_multiplier - 1.0, 0.0)''',
  '''\tquality_attack_multiplier = maxf(float(weapon.get("quality_attack_multiplier", 1.0)), 0.01)
\tquality_value_multiplier = maxf(float(weapon.get("quality_value_multiplier", 1.0)), 0.01)
\tfever_activation_count = maxi(int(weapon.get("fever_activation_count", 0)), 0)
\tfever_attack_multiplier = maxf(float(weapon.get("fever_attack_multiplier", 1.0)), 0.01)
\tfever_value_multiplier = maxf(float(weapon.get("fever_value_multiplier", 1.0)), 0.01)
\tfever_bonus_applied = bool(weapon.get("fever_bonus_applied", fever_activation_count > 0 and (fever_attack_multiplier > 1.0 or fever_value_multiplier > 1.0)))
\tcrafting_attack_multiplier = maxf(float(weapon.get("crafting_attack_multiplier", quality_attack_multiplier + fever_attack_multiplier - 1.0)), 0.01)
\tcrafting_value_multiplier = maxf(float(weapon.get("crafting_value_multiplier", quality_value_multiplier + fever_value_multiplier - 1.0)), 0.01)
\tbase_attack = maxi(int(weapon.get("base_attack", round(float(raw_base_attack) * crafting_attack_multiplier))), 1)
\tprogression_attack = base_attack
\tvalue_bonus_total = maxf(crafting_value_multiplier - 1.0, 0.0)''')
r("scripts/enhancement/enhancement_session.gd",
  '''\t\t"quality_attack_multiplier": quality_attack_multiplier,
\t\t"quality_value_multiplier": quality_value_multiplier,
\t\t"progression_attack": progression_attack,''',
  '''\t\t"quality_attack_multiplier": quality_attack_multiplier,
\t\t"quality_value_multiplier": quality_value_multiplier,
\t\t"fever_activation_count": fever_activation_count,
\t\t"fever_bonus_applied": fever_bonus_applied,
\t\t"fever_attack_multiplier": fever_attack_multiplier,
\t\t"fever_value_multiplier": fever_value_multiplier,
\t\t"crafting_attack_multiplier": crafting_attack_multiplier,
\t\t"crafting_value_multiplier": crafting_value_multiplier,
\t\t"progression_attack": progression_attack,''')
r("scripts/enhancement/enhancement_session.gd",
  '\tvalue_bonus_total = float(value_bonus_history.get(str(level), 0.0))',
  '\tvalue_bonus_total = float(value_bonus_history.get(str(level), maxf(crafting_value_multiplier - 1.0, 0.0)))')
r("scripts/enhancement/enhancement_session.gd",
  '''\t\t\t"destroyed": destroyed,
\t\t\t"final_attack": get_current_final_attack(),''',
  '''\t\t\t"destroyed": destroyed,
\t\t\t"raw_base_attack": raw_base_attack,
\t\t\t"base_attack": base_attack,
\t\t\t"quality_attack_multiplier": quality_attack_multiplier,
\t\t\t"quality_value_multiplier": quality_value_multiplier,
\t\t\t"fever_activation_count": fever_activation_count,
\t\t\t"fever_bonus_applied": fever_bonus_applied,
\t\t\t"fever_attack_multiplier": fever_attack_multiplier,
\t\t\t"fever_value_multiplier": fever_value_multiplier,
\t\t\t"crafting_attack_multiplier": crafting_attack_multiplier,
\t\t\t"crafting_value_multiplier": crafting_value_multiplier,
\t\t\t"final_attack": get_current_final_attack(),''')

r("scripts/ui/enhancement_screen.gd",
  '''\t\t"quality_attack_multiplier": float(snapshot.get("quality_attack_multiplier", 1.0)),
\t\t"quality_value_multiplier": float(snapshot.get("quality_value_multiplier", 1.0)),
\t\t"progression_attack": int(snapshot.get("progression_attack", 20)),''',
  '''\t\t"quality_attack_multiplier": float(snapshot.get("quality_attack_multiplier", 1.0)),
\t\t"quality_value_multiplier": float(snapshot.get("quality_value_multiplier", 1.0)),
\t\t"fever_activation_count": int(snapshot.get("fever_activation_count", 0)),
\t\t"fever_bonus_applied": bool(snapshot.get("fever_bonus_applied", false)),
\t\t"fever_attack_multiplier": float(snapshot.get("fever_attack_multiplier", 1.0)),
\t\t"fever_value_multiplier": float(snapshot.get("fever_value_multiplier", 1.0)),
\t\t"crafting_attack_multiplier": float(snapshot.get("crafting_attack_multiplier", 1.0)),
\t\t"crafting_value_multiplier": float(snapshot.get("crafting_value_multiplier", 1.0)),
\t\t"progression_attack": int(snapshot.get("progression_attack", 20)),''')

for rel in ("scripts/ui/game_flow_screen.gd", "scripts/ui/enhancement_test_runner.gd"):
    r(rel, 'POC v0.6.3 · main · 2026.07.22.3', 'POC v0.6.4 · main · 2026.07.23.1')
r("scripts/ui/game_flow_screen.gd",
  '''\t\t"quality_attack_multiplier": 1.0,
\t\t"quality_value_multiplier": 1.0,
\t}''',
  '''\t\t"quality_attack_multiplier": 1.0,
\t\t"quality_value_multiplier": 1.0,
\t\t"fever_activation_count": 0,
\t\t"fever_bonus_applied": false,
\t\t"fever_attack_multiplier": 1.0,
\t\t"fever_value_multiplier": 1.0,
\t\t"crafting_attack_multiplier": 1.0,
\t\t"crafting_value_multiplier": 1.0,
\t}''')
r("scripts/ui/game_flow_screen.gd",
  '''\tvar quality_attack_multiplier := float(weapon.get("quality_attack_multiplier", 1.0))
\tvar quality_value_multiplier := float(weapon.get("quality_value_multiplier", 1.0))
\tbox.add_child(_label(
\t\t"원본 공격력 %d · 품질 적용 %d(×%.2f) · 강화 %d · 최종 %d" % [
\t\t\traw_base_attack,
\t\t\tbase_attack,
\t\t\tquality_attack_multiplier,
\t\t\tprogression_attack,
\t\t\tfinal_attack,
\t\t],
\t\t19,
\t\tColor("#f4f1e8")
\t))
\tbox.add_child(_label("제작 가치 ×%.2f" % quality_value_multiplier, 16, Color("#b7b0a3")))''',
  '''\tvar quality_attack_multiplier := float(weapon.get("quality_attack_multiplier", 1.0))
\tvar quality_value_multiplier := float(weapon.get("quality_value_multiplier", 1.0))
\tvar fever_attack_multiplier := float(weapon.get("fever_attack_multiplier", 1.0))
\tvar fever_value_multiplier := float(weapon.get("fever_value_multiplier", 1.0))
\tvar crafting_attack_multiplier := float(weapon.get("crafting_attack_multiplier", quality_attack_multiplier + fever_attack_multiplier - 1.0))
\tvar crafting_value_multiplier := float(weapon.get("crafting_value_multiplier", quality_value_multiplier + fever_value_multiplier - 1.0))
\tbox.add_child(_label("원본 공격력 %d · 제작 적용 %d(×%.2f) · 강화 %d · 최종 %d" % [raw_base_attack, base_attack, crafting_attack_multiplier, progression_attack, final_attack], 19, Color("#f4f1e8")))
\tbox.add_child(_label("마감 공격력 ×%.2f · 피버 공격력 ×%.2f" % [quality_attack_multiplier, fever_attack_multiplier], 16, Color("#b7b0a3")))
\tbox.add_child(_label("제작 가치 ×%.2f (마감 ×%.2f · 피버 ×%.2f)" % [crafting_value_multiplier, quality_value_multiplier, fever_value_multiplier], 16, Color("#b7b0a3")))
\tbox.add_child(_label("피버 결과 보너스: %s · 발동 %d회" % ["적용" if bool(weapon.get("fever_bonus_applied", false)) else "미적용", int(weapon.get("fever_activation_count", 0))], 15, Color("#b7b0a3")))''')
r("scripts/ui/forging_screen.gd",
  '''\t\t\tresult_stats_label.text = "기본 공격력 %d → %d · 제작 가치 ×%.2f\\n망치질 %d회 · 피버 %d회" % [
\t\t\t\tint(finished.get("raw_base_attack", 20)),
\t\t\t\tint(finished.get("base_attack", 20)),
\t\t\t\tfloat(finished.get("quality_value_multiplier", 1.0)),
\t\t\t\tint(finished.get("tap_count", 0)),
\t\t\t\tint(finished.get("fever_activation_count", 0)),
\t\t\t]
\t\t\thelper_label.text = "MVP-001에서는 완성까지 검증합니다. 강화와 판매는 다음 수직 범위입니다."''',
  '''\t\t\tresult_stats_label.text = "원본 공격력 %d → 제작 공격력 %d · 제작 가치 ×%.2f\\n마감 공격력 ×%.2f · 피버 공격력 ×%.2f\\n망치질 %d회 · 피버 %d회 · 결과 보너스 %s" % [
\t\t\t\tint(finished.get("raw_base_attack", 20)), int(finished.get("base_attack", 20)), float(finished.get("crafting_value_multiplier", 1.0)),
\t\t\t\tfloat(finished.get("quality_attack_multiplier", 1.0)), float(finished.get("fever_attack_multiplier", 1.0)),
\t\t\t\tint(finished.get("tap_count", 0)), int(finished.get("fever_activation_count", 0)),
\t\t\t\t"적용" if bool(finished.get("fever_bonus_applied", false)) else "미적용",
\t\t\t]
\t\t\thelper_label.text = "완성 무기의 마감·피버 제작 보너스는 강화와 보관까지 유지됩니다."''')

r("tests/unit/test_forging_session.gd", 'print("ForgingSession tests PASSED (5 cases)")\n\t\tquit(0)', 'print("ForgingSession tests PASSED (7 cases)")\n\t\tquit(0)\n\t\treturn')
r("tests/unit/test_forging_session.gd",
  '''\t_test_quality_effect_values()
\t_test_reset_clears_session()''',
  '''\t_test_quality_effect_values()
\t_test_fever_result_bonus_applies_once()
\t_test_repeated_fever_does_not_stack_result_bonus()
\t_test_reset_clears_session()''')
r("tests/unit/test_forging_session.gd", '\t_expect(session.tap_count == 0, "reset 후 터치 횟수가 0이어야 합니다.")', '\t_expect(session.tap_count == 0, "reset 후 터치 횟수가 0이어야 합니다.")\n\t_expect(session.fever_activation_count == 0, "reset 후 피버 발동 횟수가 0이어야 합니다.")')
r("tests/unit/test_forging_session.gd",
  '\n\nfunc _test_reset_clears_session() -> void:\n',
  '''

func _test_fever_result_bonus_applies_once() -> void:
\tvar session = _new_fever_test_session()
\tsession.set_precision_enabled(false)
\t_activate_fever(session)
\tsession.config["target_progress"] = session.progress + 1.0
\tsession.register_tap()
\t_expect(bool(session.result.get("fever_bonus_applied", false)), "피버를 한 번 이상 발동하면 결과 보너스가 적용되어야 합니다.")
\t_expect(int(session.result.get("base_attack", 0)) == 21, "보통 마감+피버는 공격력 21이어야 합니다.")
\t_expect(is_equal_approx(float(session.result.get("fever_attack_multiplier", 0.0)), 1.05), "피버 공격력 배율은 1.05여야 합니다.")
\t_expect(is_equal_approx(float(session.result.get("fever_value_multiplier", 0.0)), 1.03), "피버 가치 배율은 1.03이어야 합니다.")


func _test_repeated_fever_does_not_stack_result_bonus() -> void:
\tvar session = _new_fever_test_session()
\tsession.set_precision_enabled(false)
\t_activate_fever(session)
\tsession.advance(0.3)
\t_activate_fever(session)
\tsession.advance(0.3)
\t_activate_fever(session)
\t_expect(session.fever_activation_count == 3, "피버 세 번 발동 경계를 만들어야 합니다.")
\tsession.config["target_progress"] = session.progress + 1.0
\tsession.register_tap()
\t_expect(is_equal_approx(float(session.result.get("fever_attack_multiplier", 0.0)), 1.05), "피버 반복 발동은 공격력 보너스를 중첩하면 안 됩니다.")
\t_expect(is_equal_approx(float(session.result.get("fever_value_multiplier", 0.0)), 1.03), "피버 반복 발동은 가치 보너스를 중첩하면 안 됩니다.")
\t_expect(int(session.result.get("base_attack", 0)) == 21, "피버 세 번도 공격력 21을 넘기면 안 됩니다.")


func _new_fever_test_session():
\treturn ForgingSessionScript.new({"target_progress": 1000.0, "tap_power": 10.0, "auto_work_per_second": 0.0, "rapid_tap_window_seconds": 1.0, "fever_gain_base": 50.0, "fever_gain_rapid": 50.0, "fever_charge_max": 100.0, "fever_decay_per_second": 0.0, "fever_duration_seconds": 0.2, "fever_multiplier": 2.0})


func _activate_fever(session) -> void:
\tsession.register_tap()
\tsession.advance(0.1)
\tsession.register_tap()


func _test_reset_clears_session() -> void:
''')

r("tests/integration/test_forging_quality_enhancement.gd", 'print("Forging quality enhancement integration tests PASSED (4 cases)")', 'print("Forging quality enhancement integration tests PASSED (6 cases)")')
r("tests/integration/test_forging_quality_enhancement.gd",
  '''\tawait _test_standard_quality_stays_baseline()
\tawait _test_quality_value_survives_downgrade_restore()''',
  '''\tawait _test_standard_quality_stays_baseline()
\tawait _test_fever_bonus_reaches_enhancement_and_storage()
\tawait _test_quality_and_fever_combine_additively_and_cap()
\tawait _test_quality_value_survives_downgrade_restore()''')
r("tests/integration/test_forging_quality_enhancement.gd", 'var screen = _new_screen(_forge_result("PERFECT"))\n\tawait process_frame\n\t_set_guaranteed_success(screen.session)', 'var screen = _new_screen(_forge_result("PERFECT", 1))\n\tawait process_frame\n\t_set_guaranteed_success(screen.session)')
r("tests/integration/test_forging_quality_enhancement.gd", 'int(screen.session.base_attack) == 22, "단계 하락 후에도 완벽한 마감 기본 공격력을 유지해야 합니다."', 'int(screen.session.base_attack) == 23, "단계 하락 후에도 완벽 마감+피버 기본 공격력을 유지해야 합니다."')
r("tests/integration/test_forging_quality_enhancement.gd", 'float(screen.session.value_bonus_total), 0.12), "단계 하락 복원 뒤에도 완벽한 마감 가치 +12%를 유지해야 합니다."', 'float(screen.session.value_bonus_total), 0.15), "단계 하락 복원 뒤에도 완벽 마감+피버 가치 +15%를 유지해야 합니다."')
r("tests/integration/test_forging_quality_enhancement.gd", 'func _forge_result(quality_id: String) -> Dictionary:\n\tvar session = ForgingSessionScript.new({"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0})', 'func _forge_result(quality_id: String, fever_activations: int = 0) -> Dictionary:\n\tvar session = ForgingSessionScript.new({"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0})\n\tsession.fever_activation_count = maxi(fever_activations, 0)')
r("tests/integration/test_forging_quality_enhancement.gd",
  '\n\nfunc _test_quality_value_survives_downgrade_restore() -> void:\n',
  '''

func _test_fever_bonus_reaches_enhancement_and_storage() -> void:
\tvar fever_screen = _new_screen(_forge_result("STANDARD", 1))
\tvar baseline_screen = _new_screen(_forge_result("STANDARD"))
\tawait process_frame
\t_expect(int(fever_screen.session.base_attack) == 21, "보통 마감+피버 공격력 21이 강화 세션에 전달되어야 합니다.")
\t_expect(is_equal_approx(float(fever_screen.session.value_bonus_total), 0.03), "피버 제작 가치 +3%가 판매가에 전달되어야 합니다.")
\t_expect(int(fever_screen.session.get_current_sale_price()) > int(baseline_screen.session.get_current_sale_price()), "피버 무기의 판매가는 기준 무기보다 높아야 합니다.")
\tvar record: Dictionary = fever_screen.build_weapon_record()
\t_expect(bool(record.get("fever_bonus_applied", false)), "보관 기록이 피버 적용 여부를 보존해야 합니다.")
\t_expect(int(record.get("fever_activation_count", 0)) == 1, "보관 기록이 피버 발동 횟수를 보존해야 합니다.")
\t_expect(is_equal_approx(float(record.get("fever_attack_multiplier", 0.0)), 1.05), "보관 기록이 피버 공격력 배율을 보존해야 합니다.")
\t_expect(is_equal_approx(float(record.get("fever_value_multiplier", 0.0)), 1.03), "보관 기록이 피버 가치 배율을 보존해야 합니다.")
\tfever_screen.queue_free()
\tbaseline_screen.queue_free()
\tawait process_frame


func _test_quality_and_fever_combine_additively_and_cap() -> void:
\tvar screen = _new_screen(_forge_result("PERFECT", 3))
\tawait process_frame
\t_expect(int(screen.session.base_attack) == 23, "완벽 마감+피버는 공격력 23이어야 합니다.")
\t_expect(is_equal_approx(float(screen.session.crafting_attack_multiplier), 1.15), "마감+피버 공격력은 가산 합성 ×1.15여야 합니다.")
\t_expect(is_equal_approx(float(screen.session.crafting_value_multiplier), 1.15), "마감+피버 가치는 가산 합성 ×1.15여야 합니다.")
\t_expect(is_equal_approx(float(screen.session.fever_attack_multiplier), 1.05), "피버 세 번도 공격력 보너스는 ×1.05여야 합니다.")
\t_expect(is_equal_approx(float(screen.session.fever_value_multiplier), 1.03), "피버 세 번도 가치 보너스는 ×1.03이어야 합니다.")
\tvar record: Dictionary = screen.build_weapon_record()
\t_expect(int(record.get("fever_activation_count", 0)) == 3, "발동 횟수는 기록하되 보너스는 중첩하지 않아야 합니다.")
\t_expect(is_equal_approx(float(record.get("crafting_value_multiplier", 0.0)), 1.15), "보관 기록이 합산 제작 가치를 보존해야 합니다.")
\tscreen.queue_free()
\tawait process_frame


func _test_quality_value_survives_downgrade_restore() -> void:
''')

r("tests/check_forging_quality_contract.py", 'balance = json.loads(text("data/crafting/forging_balance.json"))\nsession = balance.get("session", {})', 'balance = json.loads(text("data/crafting/forging_balance.json"))\nrequire(balance.get("schema_version") == 2, "forging_balance.json schema_version은 2여야 합니다.")\nsession = balance.get("session", {})')
r("tests/check_forging_quality_contract.py", '    "quality_perfect_value_multiplier": 1.12,\n}', '    "quality_perfect_value_multiplier": 1.12,\n    "fever_result_required_activations": 1,\n    "fever_result_attack_multiplier": 1.05,\n    "fever_result_value_multiplier": 1.03,\n}')
r("tests/check_forging_quality_contract.py",
  '\nenhancement_balance = json.loads(text("data/crafting/enhancement_balance.json"))\n',
  '''
fever_attack = float(session["fever_result_attack_multiplier"])
fever_value = float(session["fever_result_value_multiplier"])
fever_attacks = {quality: round(float(session["weapon_base_attack"]) * (float(session[f"quality_{quality}_attack_multiplier"]) + fever_attack - 1.0)) for quality in ("standard", "good", "perfect")}
fever_values = {quality: round(float(session[f"quality_{quality}_value_multiplier"]) + fever_value - 1.0, 2) for quality in ("standard", "good", "perfect")}
require(fever_attacks == {"standard": 21, "good": 22, "perfect": 23}, f"피버 적용 공격력이 21/22/23이어야 합니다: {fever_attacks}")
require(fever_values == {"standard": 1.03, "good": 1.08, "perfect": 1.15}, f"피버 적용 제작 가치가 1.03/1.08/1.15여야 합니다: {fever_values}")
require(round(float(session["quality_perfect_value_multiplier"]) * fever_value, 4) != fever_values["perfect"], "마감·피버 가치는 곱연산이 아니라 가산 합성이어야 합니다.")

enhancement_balance = json.loads(text("data/crafting/enhancement_balance.json"))
''')
rn("tests/check_forging_quality_contract.py", 'POC v0.6.3 · main · 2026.07.22.3', 'POC v0.6.4 · main · 2026.07.23.1', 2)
rn("tests/check_forging_quality_contract.py", 'POC v0.6.2 · main · 2026.07.22.2', 'POC v0.6.3 · main · 2026.07.22.3', 2)
r("tests/check_forging_quality_contract.py",
  '''    require("×1.05" in source and "×1.12" in source, f"품질 공격력·가치 계약이 문서에 없습니다: {rel}")
    require("20" in source and "21" in source and "22" in source, f"품질별 실제 공격력 20/21/22가 문서에 없습니다: {rel}")''',
  '''    require("×1.05" in source and "×1.03" in source, f"피버 결과 공격력·가치 계약이 문서에 없습니다: {rel}")
    require("비중첩" in source or "중첩되지" in source or "한 번만" in source, f"피버 반복 비중첩 계약이 문서에 없습니다: {rel}")
    require("21" in source and "22" in source and "23" in source, f"피버 적용 공격력 21/22/23이 문서에 없습니다: {rel}")''')
r("tests/check_forging_quality_contract.py",
  '''    require("통합 4건" in text(rel), f"제작 품질 통합 테스트 4건 기록이 최신이 아닙니다: {rel}")''',
  '''    source = text(rel)
    require("제작 모델 7건" in source, f"제작 모델 테스트 7건 기록이 최신이 아닙니다: {rel}")
    require("통합 6건" in source, f"제작 결과 통합 테스트 6건 기록이 최신이 아닙니다: {rel}")''')
r("tests/check_forging_quality_contract.py", '    "tests/unit/test_enhancement_session.gd": "EnhancementSession tests PASSED (12 cases)",', '    "tests/unit/test_forging_session.gd": "ForgingSession tests PASSED (7 cases)",\n    "tests/unit/test_enhancement_session.gd": "EnhancementSession tests PASSED (12 cases)",')
r("tests/check_forging_quality_contract.py", 'Forging quality enhancement integration tests PASSED (4 cases)', 'Forging quality enhancement integration tests PASSED (6 cases)')
r("tests/check_forging_quality_contract.py", 'dec_017 = decisions.find("## DEC-017 ")\ndec_018 = decisions.find("## DEC-018 ")\nrequire(dec_017 >= 0 and dec_018 > dec_017, "Decision Log는 DEC-017 뒤에 DEC-018을 배치해야 합니다.")', 'dec_019 = decisions.find("## DEC-019 ")\ndec_020 = decisions.find("## DEC-020 ")\nrequire(dec_019 >= 0 and dec_020 > dec_019, "Decision Log는 DEC-019 뒤에 DEC-020을 배치해야 합니다.")\nrequire("## DEC-018 품질별 실제 정수 공격력과 검증 종료코드\\n\\n- 상태: 확정·구현\\n" in decisions, "완료된 DEC-018이 구현 중 상태로 남으면 안 됩니다.")')
r("tests/check_forging_quality_contract.py", 'print("Forging quality contract PASSED")', 'print("Forging result contract PASSED")')
r("tests/check_forging_quality_contract.py",
  '\nplaytest = text("docs/GODOT_PLAYTEST.md")\n',
  '''
for rel in ["scripts/forging/forging_session.gd", "scripts/enhancement/enhancement_session.gd", "scripts/ui/enhancement_screen.gd", "scripts/ui/game_flow_screen.gd"]:
    source = text(rel)
    for field in ("fever_bonus_applied", "fever_attack_multiplier", "fever_value_multiplier", "crafting_attack_multiplier", "crafting_value_multiplier"):
        require(field in source, f"피버 결과 필드 소비 누락: {rel} / {field}")
require("fever_activation_count >= required_activations" in text("scripts/forging/forging_session.gd"), "피버 결과 보너스가 최소 발동 여부로 제한되어야 합니다.")
require('"fever_activation_count": 0' in text("scripts/ui/game_flow_screen.gd"), "자동 단조는 피버 0회여야 합니다.")
require('"fever_bonus_applied": false' in text("scripts/ui/game_flow_screen.gd"), "자동 단조는 피버 보너스 미적용이어야 합니다.")
require("_test_repeated_fever_does_not_stack_result_bonus" in text("tests/unit/test_forging_session.gd"), "피버 반복 비중첩 단위 테스트가 없습니다.")
require("_test_quality_and_fever_combine_additively_and_cap" in integration_test, "마감·피버 가산 합성 통합 테스트가 없습니다.")
require('base_attack) == 23' in integration_test, "완벽 마감+피버 공격력 23 통합 반례가 없습니다.")

playtest = text("docs/GODOT_PLAYTEST.md")
''')
r(".github/workflows/godot-validation.yml", '- name: Validate forging quality contract', '- name: Validate forging result contract')

r("README.md", '- 원본 공격력과 품질 적용 공격력을 강화·보관까지 유지', '- 제작 중 피버 1회 이상 발동 시 공격력 ×1.05·제작 가치 ×1.03, 추가 발동은 비중첩\n- 마감·피버·합산 제작 배율과 원본/제작 적용 공격력을 강화·보관까지 유지')
r("README.md", '- 원본/품질 적용/강화/최종 공격력·제작 가치·판매가·누적 비용·수식어·촉매·마감 품질 확인', '- 원본/제작 적용/강화/최종 공격력·마감·피버·합산 제작 가치·판매가·누적 비용·수식어·촉매 확인')
r("docs/MVP-001_SCOPE.md", '- 피버 중 터치·자동 작업 배율\n', '- 피버 중 터치·자동 작업 배율\n- 피버 1회 이상 발동 시 최종 공격력 ×1.05·제작 가치 ×1.03, 반복 발동 비중첩\n')
r("docs/MVP-001_SCOPE.md", '- 철검 원본 공격력은 20이며 보통 20(×1.00), 좋음 21(×1.05), 완벽 22(×1.10)로 실제 정수 공격력이 구분된다. 제작 가치는 각각 ×1.00·×1.05·×1.12다.\n', '- 철검 원본 공격력은 20이며 보통 20(×1.00), 좋음 21(×1.05), 완벽 22(×1.10)로 실제 정수 공격력이 구분된다. 제작 가치는 각각 ×1.00·×1.05·×1.12다.\n- 피버 적용 시 보통·좋음·완벽 공격력은 21·22·23, 합산 제작 가치는 ×1.03·×1.08·×1.15다.\n')
r("docs/MVP-001_SCOPE.md", '- 원본 공격력·품질 적용 공격력·제작 가치 배율을 포함한 완성 결과 요약\n- 완성 철검과 품질 효과를 MVP-002 강화 화면으로 전달', '- 원본 공격력·마감·피버·합산 제작 배율을 포함한 완성 결과 요약\n- 완성 철검과 마감·피버 제작 효과를 MVP-002 강화 화면으로 전달')
r("docs/MVP-001_SCOPE.md", '- [x] 원본 공격력과 품질 적용 공격력을 분리해 강화·보관까지 전달한다.\n', '- [x] 원본 공격력과 마감·피버·합산 제작 배율을 분리해 강화·보관까지 전달한다.\n- [x] 피버를 한 번 이상 발동하면 결과 보너스가 적용되고 반복 발동은 중첩되지 않는다.\n')
r("docs/MVP-002_SCOPE.md", '- 원본 기본 공격력과 품질 적용 기본 공격력을 별도 필드로 전달한다.\n- 반복 자동 단조의 새 철검은 보통 마감으로 시작한다.', '- 원본 기본 공격력과 마감·피버·합산 제작 배율을 별도 필드로 전달한다.\n- 피버 1회 이상은 공격력 ×1.05·제작 가치 ×1.03을 한 번만 더하며 마감 배율과 가산 합성한다.\n- 피버 적용 시 보통/좋음/완벽 공격력은 21/22/23, 제작 가치는 ×1.03/×1.08/×1.15다.\n- 반복 자동 단조의 새 철검은 보통 마감·피버 미적용으로 시작한다.')
r("docs/MVP-002_SCOPE.md", '원본/품질 적용/강화/최종 공격력·제작 가치 배율', '원본/제작 적용/강화/최종 공격력·마감·피버·합산 제작 가치')
r("docs/MVP-002_SCOPE.md", '- [x] 제작 품질의 공격력·가치 효과가 강화·보관까지 유지된다.\n- [x] 반복 자동 단조의 새 철검은 보통 마감으로 시작한다.', '- [x] 제작 마감·피버의 공격력·가치 효과가 강화·보관까지 유지된다.\n- [x] 반복 자동 단조의 새 철검은 보통 마감·피버 미적용으로 시작한다.')
r("docs/GODOT_PLAYTEST.md", 'POC v0.6.3 · main · 2026.07.22.3', 'POC v0.6.4 · main · 2026.07.23.1')
r("docs/GODOT_PLAYTEST.md", '- 완벽한 마감: 원본 공격력 20 → 품질 적용 22, 제작 가치 ×1.12\n- 강화 화면과 보관함에서 원본 공격력·품질 적용 공격력·가치 배율이 유지되는가\n- 반복 자동 단조의 두 번째 무기부터는 보통 마감으로 시작하는가', '- 완벽한 마감: 원본 공격력 20 → 품질 적용 22, 제작 가치 ×1.12\n- 피버 1회 이상이면 공격력 ×1.05·제작 가치 ×1.03이 한 번만 더해지는가\n- 여러 번 발동해도 결과 보너스가 중첩되지 않는가\n- 완벽 마감+피버가 공격력 23·제작 가치 ×1.15인가\n- 강화 화면과 보관함에서 원본·마감·피버·합산 제작 배율이 유지되는가\n- 반복 자동 단조의 두 번째 무기부터는 보통 마감·피버 미적용인가')
r("docs/GODOT_PLAYTEST.md", '원본/품질 적용/강화/최종 공격력·제작 가치 배율', '원본/제작 적용/강화/최종 공격력·마감·피버·합산 제작 가치')
r("scripts/README.md", '- 제작 품질은 `quality_attack_multiplier`와 `quality_value_multiplier`로 분리하며 구형 단일 배율을 사용하지 않는다.\n- 원본 기본 공격력과 품질 적용 기본 공격력을 별도로 보존하고 강화·보관 소비자에 전달한다.', '- 제작 마감은 `quality_*`, 피버 결과는 `fever_*`, 최종 합성은 `crafting_*` 배율로 분리한다.\n- 피버 결과 보너스는 1회 이상 발동 시 한 번만 적용하고 마감 보너스와 가산 합성한다.\n- 원본 기본 공격력과 제작 적용 기본 공격력을 별도로 보존하고 강화·보관 소비자에 전달한다.')
r("tests/README.md", '- 제작 진행도·피버·정밀 마감·초기화\n- 보통·좋음·완벽 마감의 공격력·가치 배율과 제작→강화→보관 전달', '- 제작 진행도·피버·정밀 마감·초기화\n- 피버 1회 이상 결과 보너스와 반복 발동 비중첩 경계\n- 보통·좋음·완벽 마감 및 마감+피버의 공격력·가치 배율과 제작→강화→보관 전달')

r("[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md", '- 마무리 보너스 증가\n\n광클에는 과열·피로 불이익을 두지 않는다.', '- 제작 중 피버를 1회 이상 발동하면 완성 무기에 공격력 ×1.05·제작 가치 ×1.03 결과 보너스 적용\n- 추가 발동 횟수는 기록하되 결과 보너스는 비중첩\n\n광클에는 과열·피로 불이익을 두지 않는다. 반복 자동 단조의 새 철검은 피버 미적용으로 시작한다.')
r("[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md", '- 공격력 단위 변경으로 초반 판매가가 급증하지 않도록 가격 계수는 함께 보정하며, 실제 수치는 `data/crafting/forging_balance.json`과 `data/crafting/enhancement_balance.json`이 책임진다.\n\n## 5. 기본 무기 제작', '- 공격력 단위 변경으로 초반 판매가가 급증하지 않도록 가격 계수는 함께 보정하며, 실제 수치는 `data/crafting/forging_balance.json`과 `data/crafting/enhancement_balance.json`이 책임진다.\n\n### 4.4 마감·피버 제작 보너스 합성\n\n마감과 피버는 별도 기록하며 최종 제작 배율은 두 배율을 곱하지 않고 기준 ×1.00 위에 보너스분을 더한다. 피버 적용 시 보통/좋음/완벽 공격력은 21/22/23, 제작 가치는 ×1.03/×1.08/×1.15다. 반복 발동은 중첩되지 않아 제작 지연 적립을 막는다.\n\n## 5. 기본 무기 제작')
r("[기획서]/00_프로젝트_허브/START_HERE.md", '1. 일반 제작은 빠른 연속 터치로 진행하고 광클은 피버 보상을 만든다.', '1. 일반 제작은 빠른 연속 터치로 진행하고 피버는 작업 가속과 1회 한정 완성 결과 보상을 만든다.')
r("[기획서]/00_프로젝트_허브/START_HERE.md", '- 터치·자동 작업·연속 터치 피버\n- 선택적 정밀 마감과 품질 결과\n- 완성 철검을 강화로 전달', '- 터치·자동 작업·연속 터치 피버\n- 피버 1회 이상 공격력 ×1.05·제작 가치 ×1.03, 추가 발동 비중첩\n- 선택적 정밀 마감과 품질 결과\n- 마감·피버·합산 제작 배율을 강화로 전달')
r("[기획서]/00_프로젝트_허브/START_HERE.md", '- 제작·강화 모델 테스트 PASS', '- 제작 모델 7건·강화 모델 12건·제작 결과 통합 6건 PASS')
r("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", 'POC v0.6.3 품질 정수 구분·CI 종료 흐름·Godot AI 감사 정합화를 main에 확정했다. 다음 제품 개선은 제작 피버가 최종 무기 결과에 남기는 작은 보너스다.', 'POC v0.6.4 제작 피버 결과 보너스와 마감·피버 합산 계약을 main 기준으로 확정했다. 다음 제품 개선은 강화 실패 정책 정본 통합과 데이터 의미 검증이다.')
r("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", 'POC v0.6.3 · main · 2026.07.22.3', 'POC v0.6.4 · main · 2026.07.23.1')
r("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", '- 제작 품질: 철검 원본 20 기준 보통 20/가치 ×1.00, 좋음 21/×1.05, 완벽 22/×1.12\n- 품질 전달: 원본 공격력·품질 적용 공격력·가치 배율을 강화와 보관까지 유지\n- 자동 반복 품질: 새 철검은 보통 마감으로 시작해 최초 수동 품질을 복제하지 않음', '- 제작 품질: 철검 원본 20 기준 보통 20/가치 ×1.00, 좋음 21/×1.05, 완벽 22/×1.12\n- 제작 피버 결과: 1회 이상 공격력 ×1.05·제작 가치 ×1.03, 추가 발동 비중첩\n- 합산 결과: 피버 적용 보통/좋음/완벽 공격력 21/22/23, 제작 가치 ×1.03/×1.08/×1.15\n- 제작 전달: 원본 공격력·마감·피버·합산 제작 배율을 강화와 보관까지 유지\n- 자동 반복 제작: 새 철검은 보통 마감·피버 미적용으로 시작')
r("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", '- 제작 품질 자동 검증: 제작 모델 5건·제작→강화·보관 통합 4건·정적 계약 검사 PASS\n- Godot 자동 검증: 4.7.1 import·parse, 강화·전체 흐름 Scene, 제작 5건·강화 12건·공유 자원 7건·수동 경제 2건·품질 통합 4건 PASS', '- 제작 결과 자동 검증: 제작 모델 7건·제작→강화·보관 통합 6건·정적 계약 검사 PASS\n- Godot 자동 검증: 4.7.1 import·parse, 강화·전체 흐름 Scene, 제작 모델 7건·강화 12건·공유 자원 7건·수동 경제 2건·제작 결과 통합 6건 PASS')
r("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", '1. 제작 피버가 무기 결과에 남기는 작은 보너스를 설계·검증한다.\n2. 강화 데이터의 중복 실패 정책을 제거하고 의미 검증을 강화한다.\n3. 위험·가격 곡선을 시뮬레이션으로 조정한다.\n4. 방문 검투사 판매를 구현한다.', '1. 강화 데이터의 중복 실패 정책을 제거하고 의미 검증을 강화한다.\n2. 위험·가격 곡선을 시뮬레이션으로 조정한다.\n3. 방문 검투사 판매를 구현한다.')
r("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", '- 제작 품질 효과의 실제 사람 화면·체감 검수', '- 제작 마감·피버 결과 효과의 실제 사람 화면·체감 검수')
r("[기획서]/00_프로젝트_허브/ROADMAP.md", '- 반복 자동 단조의 새 철검 보통 마감 고정\n\n남음:\n- 제작 피버가 무기 결과에 남기는 작은 보너스 설계', '- 피버 1회 이상 결과 공격력 ×1.05·제작 가치 ×1.03과 반복 발동 비중첩\n- 원본 공격력·마감·피버·합산 제작 배율의 강화·보관 전달\n- 반복 자동 단조의 새 철검 보통 마감·피버 미적용 고정\n\n남음:')
r("[기획서]/00_프로젝트_허브/ROADMAP.md", '3. 제작 피버 결과 보너스 — NEXT\n4. 강화 실패 정책 정본 통합과 데이터 의미 검증', '3. 제작 피버 결과 보너스 — 완료·main 반영\n4. 강화 실패 정책 정본 통합과 데이터 의미 검증 — NEXT')
r("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md", '| Implementation | PASS | 품질별 정수 공격력 20/21/22·가격 보정·테스트 러너 종료 흐름·도메인/UI/데이터/단위·통합·정적 테스트 구현 |', '| Implementation | PASS | 피버 1회 한정 결과 보너스·가산 합성·자동 반복 미적용·도메인/UI/데이터/단위·통합·정적 테스트 구현 |')
r("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md", '- [x] 제작 모델 5건·제작 품질 통합 4건·정적 품질 계약 검사\n- [ ] 피버가 최종 무기 결과에 남기는 보너스', '- [x] 제작 모델 7건·제작 결과 통합 6건·정적 제작 결과 계약 검사\n- [x] 피버 1회 이상 공격력 ×1.05·제작 가치 ×1.03\n- [x] 반복 발동 비중첩·자동 반복 미적용·강화/보관 전달')
r("[기획서]/00_프로젝트_허브/CHANGELOG.md", '# Changelog\n\n', '# Changelog\n\n## 2026-07-23 — POC v0.6.4 제작 피버 결과 보너스\n\n- 피버 1회 이상 공격력 ×1.05·제작 가치 ×1.03, 추가 발동 비중첩\n- 마감 `quality_*`·피버 `fever_*`·합산 `crafting_*` 분리와 가산 합성\n- 피버 적용 보통/좋음/완벽 공격력 21/22/23, 가치 ×1.03/×1.08/×1.15\n- 강화·판매가·단계 하락 복원·보관 전달과 자동 반복 미적용\n- 버전 `POC v0.6.4 · main · 2026.07.23.1`\n- 제작 모델 7건·제작 결과 통합 6건·정적 계약 검사 연결\n- DEC-018·DEC-019 stale 상태 표현 정리\n\n')
r("[기획서]/00_프로젝트_허브/DECISION_LOG.md", '## DEC-018 품질별 실제 정수 공격력과 검증 종료코드\n\n- 상태: 확정·구현 중', '## DEC-018 품질별 실제 정수 공격력과 검증 종료코드\n\n- 상태: 확정·구현')
r("[기획서]/00_프로젝트_허브/DECISION_LOG.md", '## DEC-019 Godot AI 벤더 개발 연동\n\n- 상태: 적용·검증 중', '## DEC-019 Godot AI 벤더 개발 연동\n\n- 상태: 적용·자동 검증 완료 / 로컬 연동 미검증')
a("[기획서]/00_프로젝트_허브/DECISION_LOG.md", '## DEC-020 제작 피버 결과 보너스', '''## DEC-020 제작 피버 결과 보너스

- 상태: 확정·구현
- 피버 1회 이상이면 공격력 ×1.05·제작 가치 ×1.03을 적용하고 추가 발동은 중첩하지 않는다.
- 마감·피버는 별도 필드로 보존하며 최종 제작 배율은 기준 ×1.00 위 가산 합성한다.
- 피버 적용 보통/좋음/완벽 공격력은 21/22/23, 가치는 ×1.03/×1.08/×1.15다.
- 반복 자동 단조의 새 철검은 보통 마감·피버 미적용이다.
- 이유: 수동 광클 의미는 남기되 제작 지연 반복 적립과 강화 복리 과증폭을 막는다.
- 재검토: 20~30분 플레이의 피버 달성률·입력 피로·수동/자동 효율을 측정할 때''')
a("skills/SKILL_LEARNING_LOG.md", '## 2026-07-23 — 제작 피버 결과 보너스와 반복 적립 상한', '''## 2026-07-23 — 제작 피버 결과 보너스와 반복 적립 상한

- 게임 디자인: 피버 1회 이상 공격력 ×1.05·제작 가치 ×1.03, 추가 발동 비중첩.
- 악용 검토: 횟수 비례 보상은 제작 지연 반복 적립을 최적화하므로 제외했다.
- 엔지니어링: `quality_*`·`fever_*`·`crafting_*`를 분리해 강화·판매가·하락 복원·보관까지 전달했다.
- 자동화 경계: 반복 자동 단조 새 철검은 보통 마감·피버 미적용이다.
- QA: 제작 모델 7건·통합 6건·정적 계약으로 실제 발동, 비중첩, 가산 합성, 전달·복원을 고정했다.
- 참조 감사: DEC-018 완료 상태와 DEC-019 자동/로컬 검증 상태를 정리했다.
- 미검증: 사람 체감·Android·장시간 성능·판매 경제''')

print("POC v0.6.4 compact patch applied")
