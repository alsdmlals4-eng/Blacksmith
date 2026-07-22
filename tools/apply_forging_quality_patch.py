#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rep(path: str, old: str, new: str, count: int = 1) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    found = text.count(old)
    if found != count:
        raise RuntimeError(f"{path}: expected {count}, found {found}: {old[:120]!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def patch_balance() -> None:
    p = ROOT / "data/crafting/forging_balance.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["session"].update({
        "weapon_base_attack": 10,
        "quality_standard_attack_multiplier": 1.0,
        "quality_standard_value_multiplier": 1.0,
        "quality_good_attack_multiplier": 1.05,
        "quality_good_value_multiplier": 1.05,
        "quality_perfect_attack_multiplier": 1.10,
        "quality_perfect_value_multiplier": 1.12
    })
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def patch_forging_session() -> None:
    path = "scripts/forging/forging_session.gd"
    rep(path, '\t"precision_good_radius": 0.18,\n}', '\t"precision_good_radius": 0.18,\n\t"weapon_base_attack": 10,\n\t"quality_standard_attack_multiplier": 1.0,\n\t"quality_standard_value_multiplier": 1.0,\n\t"quality_good_attack_multiplier": 1.05,\n\t"quality_good_value_multiplier": 1.05,\n\t"quality_perfect_attack_multiplier": 1.10,\n\t"quality_perfect_value_multiplier": 1.12,\n}')
    rep(path, '''\tvar quality_multiplier := 1.0

\tif distance <= float(config["precision_perfect_radius"]):
\t\tquality_id = "PERFECT"
\t\tquality_label = "완벽한 마감"
\t\tquality_multiplier = 1.2
\telif distance <= float(config["precision_good_radius"]):
\t\tquality_id = "GOOD"
\t\tquality_label = "좋은 마감"
\t\tquality_multiplier = 1.1

\t_complete(quality_id, quality_label, quality_multiplier)''', '''\tvar attack_multiplier := float(config["quality_standard_attack_multiplier"])
\tvar value_multiplier := float(config["quality_standard_value_multiplier"])

\tif distance <= float(config["precision_perfect_radius"]):
\t\tquality_id = "PERFECT"
\t\tquality_label = "완벽한 마감"
\t\tattack_multiplier = float(config["quality_perfect_attack_multiplier"])
\t\tvalue_multiplier = float(config["quality_perfect_value_multiplier"])
\telif distance <= float(config["precision_good_radius"]):
\t\tquality_id = "GOOD"
\t\tquality_label = "좋은 마감"
\t\tattack_multiplier = float(config["quality_good_attack_multiplier"])
\t\tvalue_multiplier = float(config["quality_good_value_multiplier"])

\t_complete(quality_id, quality_label, attack_multiplier, value_multiplier)''')
    rep(path, '\t\t\t_complete("STANDARD", "자동 마감", 1.0)', '''\t\t\t_complete(
\t\t\t\t"STANDARD",
\t\t\t\t"자동 마감",
\t\t\t\tfloat(config["quality_standard_attack_multiplier"]),
\t\t\t\tfloat(config["quality_standard_value_multiplier"])
\t\t\t)''')
    rep(path, '''func _complete(quality_id: String, quality_label: String, quality_multiplier: float) -> void:
\tstate = State.COMPLETE
\tresult = {
\t\t"weapon_id": "iron_sword",
\t\t"weapon_name": "철검",
\t\t"quality_id": quality_id,
\t\t"quality_label": quality_label,
\t\t"quality_multiplier": quality_multiplier,''', '''func _complete(
\tquality_id: String,
\tquality_label: String,
\tattack_multiplier: float,
\tvalue_multiplier: float
) -> void:
\tstate = State.COMPLETE
\tvar raw_base_attack := maxi(int(config.get("weapon_base_attack", 10)), 1)
\tvar applied_base_attack := maxi(int(round(float(raw_base_attack) * attack_multiplier)), 1)
\tresult = {
\t\t"weapon_id": "iron_sword",
\t\t"weapon_name": "철검",
\t\t"raw_base_attack": raw_base_attack,
\t\t"base_attack": applied_base_attack,
\t\t"quality_id": quality_id,
\t\t"quality_label": quality_label,
\t\t"quality_multiplier": attack_multiplier,
\t\t"quality_attack_multiplier": attack_multiplier,
\t\t"quality_value_multiplier": value_multiplier,''')


def patch_enhancement_session() -> None:
    path = "scripts/enhancement/enhancement_session.gd"
    rep(path, 'var base_attack: int = 10\nvar progression_attack: int = 10', 'var raw_base_attack: int = 10\nvar base_attack: int = 10\nvar quality_attack_multiplier: float = 1.0\nvar quality_value_multiplier: float = 1.0\nvar progression_attack: int = 10')
    rep(path, '''\tbase_attack = int(weapon.get("base_attack", config.get("growth", {}).get("base_attack", 10)))
\tprogression_attack = base_attack
\tattack_history["0"] = progression_attack
\tvalue_bonus_history["0"] = 0.0''', '''\traw_base_attack = maxi(int(weapon.get("raw_base_attack", weapon.get("base_attack", config.get("growth", {}).get("base_attack", 10)))), 1)
\tquality_attack_multiplier = maxf(float(weapon.get("quality_attack_multiplier", weapon.get("quality_multiplier", 1.0))), 0.01)
\tquality_value_multiplier = maxf(float(weapon.get("quality_value_multiplier", 1.0)), 0.01)
\tbase_attack = maxi(int(weapon.get("base_attack", round(float(raw_base_attack) * quality_attack_multiplier))), 1)
\tprogression_attack = base_attack
\tvalue_bonus_total = maxf(quality_value_multiplier - 1.0, 0.0)
\tattack_history["0"] = progression_attack
\tvalue_bonus_history["0"] = value_bonus_total''')
    rep(path, '''\t\t"base_attack": base_attack,
\t\t"progression_attack": progression_attack,''', '''\t\t"raw_base_attack": raw_base_attack,
\t\t"base_attack": base_attack,
\t\t"quality_attack_multiplier": quality_attack_multiplier,
\t\t"quality_value_multiplier": quality_value_multiplier,
\t\t"progression_attack": progression_attack,''')


def patch_flow_and_ui() -> None:
    rep("scripts/ui/game_flow_screen.gd", '\tweapon_result["base_attack"] = 10\n', '')
    rep("scripts/ui/game_flow_screen.gd", '''func _show_auto_enhancement() -> void:
\tif auto_weapon_template.is_empty():
\t\tauto_weapon_template = {
\t\t\t"weapon_id": "iron_sword",
\t\t\t"weapon_name": "철검",
\t\t\t"base_attack": 10,
\t\t\t"quality_id": "AUTO",
\t\t\t"quality_label": "자동 단조",
\t\t\t"quality_multiplier": 1.0,
\t\t}
\t_show_enhancement_screen(auto_weapon_template)''', '''func _show_auto_enhancement() -> void:
\t# 반복 자동 단조는 최초 수동 제작의 GOOD/PERFECT 품질을 복제하지 않습니다.
\tauto_weapon_template = {
\t\t"weapon_id": "iron_sword",
\t\t"weapon_name": "철검",
\t\t"raw_base_attack": 10,
\t\t"base_attack": 10,
\t\t"quality_id": "AUTO",
\t\t"quality_label": "자동 단조 · 보통 마감",
\t\t"quality_multiplier": 1.0,
\t\t"quality_attack_multiplier": 1.0,
\t\t"quality_value_multiplier": 1.0,
\t}
\t_show_enhancement_screen(auto_weapon_template)''')
    rep("scripts/ui/enhancement_screen.gd", '''\t\t"base_attack": int(snapshot.get("base_attack", 10)),
\t\t"progression_attack": int(snapshot.get("progression_attack", 10)),''', '''\t\t"raw_base_attack": int(snapshot.get("raw_base_attack", snapshot.get("base_attack", 10))),
\t\t"base_attack": int(snapshot.get("base_attack", 10)),
\t\t"quality_attack_multiplier": float(snapshot.get("quality_attack_multiplier", 1.0)),
\t\t"quality_value_multiplier": float(snapshot.get("quality_value_multiplier", 1.0)),
\t\t"progression_attack": int(snapshot.get("progression_attack", 10)),''')
    rep("scripts/ui/forging_screen.gd", '''\t\t\tresult_stats_label.text = "망치질 %d회 · 피버 %d회" % [
\t\t\t\tint(finished.get("tap_count", 0)),
\t\t\t\tint(finished.get("fever_activation_count", 0)),
\t\t\t]''', '''\t\t\tresult_stats_label.text = "기본 공격력 %d → %d · 제작 가치 ×%.2f\\n망치질 %d회 · 피버 %d회" % [
\t\t\t\tint(finished.get("raw_base_attack", 10)),
\t\t\t\tint(finished.get("base_attack", 10)),
\t\t\t\tfloat(finished.get("quality_value_multiplier", 1.0)),
\t\t\t\tint(finished.get("tap_count", 0)),
\t\t\t\tint(finished.get("fever_activation_count", 0)),
\t\t\t]''')


def patch_tests() -> None:
    path = "tests/unit/test_forging_session.gd"
    rep(path, 'ForgingSession tests PASSED (4 cases)', 'ForgingSession tests PASSED (5 cases)')
    rep(path, '\t_test_precision_perfect_result()\n\t_test_reset_clears_session()', '\t_test_precision_perfect_result()\n\t_test_quality_effect_values()\n\t_test_reset_clears_session()')
    rep(path, '\n\nfunc _test_reset_clears_session() -> void:', '''

func _test_quality_effect_values() -> void:
\tvar good_session = ForgingSessionScript.new({"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0})
\tgood_session.register_tap()
\tgood_session.precision_position = float(good_session.config["precision_target"]) + 0.10
\tvar good: Dictionary = good_session.finish_precision()
\t_expect(good.get("quality_id") == "GOOD", "GOOD 범위는 좋은 마감이어야 합니다.")
\t_expect(is_equal_approx(float(good.get("quality_attack_multiplier", 0.0)), 1.05), "좋은 마감 공격력 배율은 1.05여야 합니다.")
\t_expect(is_equal_approx(float(good.get("quality_value_multiplier", 0.0)), 1.05), "좋은 마감 가치 배율은 1.05여야 합니다.")

\tvar perfect_session = ForgingSessionScript.new({"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0})
\tperfect_session.register_tap()
\tperfect_session.precision_position = float(perfect_session.config["precision_target"])
\tvar perfect: Dictionary = perfect_session.finish_precision()
\t_expect(int(perfect.get("raw_base_attack", 0)) == 10, "완벽한 마감은 원본 공격력 10을 보존해야 합니다.")
\t_expect(int(perfect.get("base_attack", 0)) == 11, "완벽한 마감은 적용 공격력 11을 만들어야 합니다.")
\t_expect(is_equal_approx(float(perfect.get("quality_attack_multiplier", 0.0)), 1.10), "완벽한 마감 공격력 배율은 1.10이어야 합니다.")
\t_expect(is_equal_approx(float(perfect.get("quality_value_multiplier", 0.0)), 1.12), "완벽한 마감 가치 배율은 1.12여야 합니다.")


func _test_reset_clears_session() -> void:''')

    integration = ROOT / "tests/integration/test_forging_quality_enhancement.gd"
    integration.write_text('''extends SceneTree

const ForgingSessionScript = preload("res://scripts/forging/forging_session.gd")
const EnhancementScreenScript = preload("res://scripts/ui/enhancement_screen.gd")
const WorkshopResourcesScript = preload("res://scripts/economy/workshop_resources.gd")

var failures: Array[String] = []

func _initialize() -> void:
\tcall_deferred("_run")

func _run() -> void:
\tawait _test_perfect_quality_reaches_enhancement_and_storage()
\tawait _test_standard_quality_stays_baseline()
\tif failures.is_empty():
\t\tprint("Forging quality enhancement integration tests PASSED (2 cases)")
\t\tquit(0)
\tfor failure in failures:
\t\tpush_error(failure)
\tquit(1)

func _test_perfect_quality_reaches_enhancement_and_storage() -> void:
\tvar result := _forge_result(true)
\tvar screen = _new_screen(result)
\tawait process_frame
\t_expect(int(screen.session.raw_base_attack) == 10, "원본 공격력 10을 보존해야 합니다.")
\t_expect(int(screen.session.base_attack) == 11, "완벽한 마감 공격력이 강화 세션에 전달되어야 합니다.")
\t_expect(is_equal_approx(float(screen.session.value_bonus_total), 0.12), "완벽한 마감 가치 +12%가 판매가에 전달되어야 합니다.")
\tvar record: Dictionary = screen.build_weapon_record()
\t_expect(int(record.get("raw_base_attack", 0)) == 10, "보관 기록이 원본 공격력을 보존해야 합니다.")
\t_expect(int(record.get("base_attack", 0)) == 11, "보관 기록이 품질 적용 공격력을 보존해야 합니다.")
\t_expect(is_equal_approx(float(record.get("quality_value_multiplier", 0.0)), 1.12), "보관 기록이 가치 배율을 보존해야 합니다.")
\tscreen.queue_free()
\tawait process_frame

func _test_standard_quality_stays_baseline() -> void:
\tvar result := _forge_result(false)
\tvar screen = _new_screen(result)
\tawait process_frame
\t_expect(int(screen.session.base_attack) == 10, "자동 마감은 공격력 10을 유지해야 합니다.")
\t_expect(is_zero_approx(float(screen.session.value_bonus_total)), "자동 마감은 가치 보너스를 만들면 안 됩니다.")
\tscreen.queue_free()
\tawait process_frame

func _forge_result(perfect: bool) -> Dictionary:
\tvar session = ForgingSessionScript.new({"target_progress": 1.0, "tap_power": 1.0, "auto_work_per_second": 0.0})
\tif not perfect:
\t\tsession.set_precision_enabled(false)
\tsession.register_tap()
\tif perfect:
\t\tsession.precision_position = float(session.config["precision_target"])
\t\treturn session.finish_precision()
\treturn session.result.duplicate(true)

func _new_screen(result: Dictionary):
\tvar screen = EnhancementScreenScript.new()
\tscreen.configure_weapon(result)
\tscreen.set_workshop_resources(WorkshopResourcesScript.new(1000000, {"whetstone": 20}))
\tget_root().add_child(screen)
\treturn screen

func _expect(condition: bool, message: String) -> void:
\tif not condition:
\t\tfailures.append(message)
''', encoding="utf-8")

    workflow = " .github/workflows/godot-validation.yml".strip()
    rep(workflow, '''          echo "== ManualEnhancementEconomy ==" | tee -a godot-test.log
          ./godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd >> godot-test.log 2>&1
          manual_economy_status=$?

          cat godot-test.log''', '''          echo "== ManualEnhancementEconomy ==" | tee -a godot-test.log
          ./godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd >> godot-test.log 2>&1
          manual_economy_status=$?

          echo "== ForgingQualityEnhancement ==" | tee -a godot-test.log
          ./godot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd >> godot-test.log 2>&1
          forging_quality_status=$?

          cat godot-test.log''')
    rep(workflow, '''          if ! grep -q "Manual enhancement economy integration tests PASSED" godot-test.log; then
            status=1
          fi
          if [ "$forging_status" -ne 0 ] || [ "$enhancement_status" -ne 0 ] || [ "$workshop_status" -ne 0 ] || [ "$manual_economy_status" -ne 0 ]; then
            echo "Godot reported non-zero test process status: forging=$forging_status enhancement=$enhancement_status workshop=$workshop_status manual_economy=$manual_economy_status"
          fi''', '''          if ! grep -q "Manual enhancement economy integration tests PASSED" godot-test.log; then
            status=1
          fi
          if ! grep -q "Forging quality enhancement integration tests PASSED" godot-test.log; then
            status=1
          fi
          if [ "$forging_status" -ne 0 ] || [ "$enhancement_status" -ne 0 ] || [ "$workshop_status" -ne 0 ] || [ "$manual_economy_status" -ne 0 ] || [ "$forging_quality_status" -ne 0 ]; then
            echo "Godot reported non-zero test process status: forging=$forging_status enhancement=$enhancement_status workshop=$workshop_status manual_economy=$manual_economy_status forging_quality=$forging_quality_status"
          fi''')


def main() -> None:
    patch_balance()
    patch_forging_session()
    patch_enhancement_session()
    patch_flow_and_ui()
    patch_tests()
    print("forging quality patch applied")


if __name__ == "__main__":
    main()
