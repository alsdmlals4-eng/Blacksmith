from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_exact(rel: str, old: str, new: str, expected: int = 1) -> None:
    text = read(rel)
    count = text.count(old)
    if count != expected:
        raise RuntimeError(f"{rel}: expected {expected} matches, found {count}: {old[:80]!r}")
    write(rel, text.replace(old, new))


replace_exact("scripts/forging/forging_session.gd", '\t\t"quality_multiplier": attack_multiplier,\n', "")
replace_exact("scripts/enhancement/enhancement_session.gd", 'quality_attack_multiplier = maxf(float(weapon.get("quality_attack_multiplier", weapon.get("quality_multiplier", 1.0))), 0.01)', 'quality_attack_multiplier = maxf(float(weapon.get("quality_attack_multiplier", 1.0)), 0.01)')
replace_exact("scripts/ui/enhancement_screen.gd", '\t\t"quality_multiplier": float(weapon_result.get("quality_multiplier", 1.0)),\n', "")
replace_exact("scripts/ui/game_flow_screen.gd", 'const VERSION_TEXT := "POC v0.6.1 · main · 2026.07.22.1"', 'const VERSION_TEXT := "POC v0.6.2 · main · 2026.07.22.2"')
replace_exact("scripts/ui/game_flow_screen.gd", '\t\t"quality_multiplier": 1.0,\n', "")
replace_exact("scripts/ui/enhancement_test_runner.gd", 'const VERSION_TEXT := "POC v0.6.1 · main · 2026.07.22.1"', 'const VERSION_TEXT := "POC v0.6.2 · main · 2026.07.22.2"')
replace_exact("scripts/ui/enhancement_test_runner.gd", '''\t\t"weapon_id": "iron_sword",\n\t\t"weapon_name": "철검",\n\t\t"base_attack": 10,\n\t\t"quality_id": "TEST",\n\t\t"quality_label": "테스트용 철검",\n\t\t"quality_multiplier": 1.0,\n''', '''\t\t"weapon_id": "iron_sword",\n\t\t"weapon_name": "철검",\n\t\t"raw_base_attack": 10,\n\t\t"base_attack": 10,\n\t\t"quality_id": "TEST",\n\t\t"quality_label": "테스트용 철검",\n\t\t"quality_attack_multiplier": 1.0,\n\t\t"quality_value_multiplier": 1.0,\n''')
replace_exact("tests/integration/test_manual_enhancement_economy.gd", '''\t\t"weapon_id": "iron_sword",\n\t\t"weapon_name": "철검",\n\t\t"base_attack": 10,\n\t\t"quality_id": "TEST",\n\t\t"quality_label": "테스트",\n\t\t"quality_multiplier": 1.0,\n''', '''\t\t"weapon_id": "iron_sword",\n\t\t"weapon_name": "철검",\n\t\t"raw_base_attack": 10,\n\t\t"base_attack": 10,\n\t\t"quality_id": "TEST",\n\t\t"quality_label": "테스트",\n\t\t"quality_attack_multiplier": 1.0,\n\t\t"quality_value_multiplier": 1.0,\n''')

inventory_old = '''\tvar base_attack := int(weapon.get("base_attack", 10))\n\tvar progression_attack := int(weapon.get("progression_attack", base_attack))\n\tvar final_attack := int(weapon.get("final_attack", progression_attack))\n\tbox.add_child(_label(\n\t\t"기본 공격력 %d · 강화 공격력 %d · 최종 공격력 %d" % [base_attack, progression_attack, final_attack],\n\t\t19,\n\t\tColor("#f4f1e8")\n\t))\n'''
inventory_new = '''\tvar raw_base_attack := int(weapon.get("raw_base_attack", weapon.get("base_attack", 10)))\n\tvar base_attack := int(weapon.get("base_attack", raw_base_attack))\n\tvar progression_attack := int(weapon.get("progression_attack", base_attack))\n\tvar final_attack := int(weapon.get("final_attack", progression_attack))\n\tvar quality_attack_multiplier := float(weapon.get("quality_attack_multiplier", 1.0))\n\tvar quality_value_multiplier := float(weapon.get("quality_value_multiplier", 1.0))\n\tbox.add_child(_label(\n\t\t"원본 공격력 %d · 품질 적용 %d(×%.2f) · 강화 %d · 최종 %d" % [\n\t\t\traw_base_attack,\n\t\t\tbase_attack,\n\t\t\tquality_attack_multiplier,\n\t\t\tprogression_attack,\n\t\t\tfinal_attack,\n\t\t],\n\t\t19,\n\t\tColor("#f4f1e8")\n\t))\n\tbox.add_child(_label("제작 가치 ×%.2f" % quality_value_multiplier, 16, Color("#b7b0a3")))\n'''
replace_exact("scripts/ui/game_flow_screen.gd", inventory_old, inventory_new)
replace_exact("scripts/ui/enhancement_test_runner.gd", inventory_old, inventory_new)

replace_exact("[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md", '''### 4.3 정밀 마감\n\n- 제작 마무리에서 ON/OFF 가능\n- ON: 타이밍에 따라 완벽·좋음·보통 결과\n- OFF: 기본 결과로 즉시 마감\n- 정밀 마감 실패가 비사용보다 과도한 손해를 강제하지 않음\n''', '''### 4.3 정밀 마감과 품질 효과\n\n- 제작 마무리에서 ON/OFF 가능\n- ON: 타이밍에 따라 완벽·좋음·보통 결과\n- OFF: 보통 마감으로 즉시 완료\n- 정밀 마감 실패가 비사용보다 과도한 손해를 강제하지 않음\n\n| 품질 | 품질 적용 기본 공격력 | 제작 가치 |\n|---|---:|---:|\n| 보통 | 원본 ×1.00 | ×1.00 |\n| 좋음 | 원본 ×1.05 | ×1.05 |\n| 완벽 | 원본 ×1.10 | ×1.12 |\n\n- 원본 기본 공격력과 품질 적용 기본 공격력을 별도 보존한다.\n- 강화의 점진 성장은 품질 적용 기본 공격력에서 시작한다.\n- 제작 가치 배율은 강화 후 판매가 계산과 보관 기록까지 유지한다.\n- 반복 자동 단조로 새로 만드는 철검은 보통 마감으로 시작해 수동 GOOD/PERFECT 결과를 복제하지 않는다.\n- 실제 수치는 `data/crafting/forging_balance.json`이 책임진다.\n''')
replace_exact("[기획서]/00_프로젝트_허브/DECISION_LOG.md", "## DEC-016 검투사 경기 관람·베팅 보존\n", '''## DEC-017 제작 마감 품질의 성능·가치 반영\n\n- 상태: 확정·구현\n- 보통 마감은 공격력 ×1.00, 제작 가치 ×1.00이다.\n- 좋은 마감은 공격력 ×1.05, 제작 가치 ×1.05이다.\n- 완벽한 마감은 공격력 ×1.10, 제작 가치 ×1.12이다.\n- 원본 기본 공격력과 품질 적용 기본 공격력을 별도 필드로 보존한다.\n- 강화 성장과 판매 가치는 품질 효과를 이어받으며 보관 기록에서도 확인할 수 있다.\n- 반복 자동 단조의 새 철검은 보통 마감으로 시작한다.\n- 구형 단일 `quality_multiplier` 필드는 사용하지 않는다.\n- 이유: 제작 타이밍 선택에 실질 보상을 주되 강화의 복리 성장 때문에 초반 품질 격차가 과도하게 확대되지 않게 한다.\n- 재검토: 실제 판매 루프와 20~30분 성장 세션에서 품질별 기대 수익을 측정할 때\n\n## DEC-016 검투사 경기 관람·베팅 보존\n''')
replace_exact("docs/MVP-001_SCOPE.md", "- 움직이는 마감 포인터와 완벽·성공·보통 판정\n- 완성 결과 요약\n- 완성 철검을 MVP-002 강화 화면으로 전달\n", "- 움직이는 마감 포인터와 완벽·좋음·보통 판정\n- 보통 공격력 ×1.00·가치 ×1.00, 좋음 ×1.05·×1.05, 완벽 ×1.10·×1.12\n- 원본 공격력·품질 적용 공격력·제작 가치 배율을 포함한 완성 결과 요약\n- 완성 철검과 품질 효과를 MVP-002 강화 화면으로 전달\n")
replace_exact("docs/MVP-001_SCOPE.md", "- [x] 완성 결과를 강화 화면으로 전달하거나 다시 제작할 수 있다.\n- [x] 모델 단위 검증과 데이터 정적 검증이 통과한다.\n", "- [x] 완성 결과를 강화 화면으로 전달하거나 다시 제작할 수 있다.\n- [x] 좋은·완벽한 마감이 실제 기본 공격력과 제작 가치에 반영된다.\n- [x] 원본 공격력과 품질 적용 공격력을 분리해 강화·보관까지 전달한다.\n- [x] 모델 단위 검증·제작→강화 통합 검증·데이터 정적 검증이 통과한다.\n")
replace_exact("docs/MVP-002_SCOPE.md", "- 공격력 증가는 고정 덧셈이 아니라 현재 강화 적용 공격력과 목표 구간을 기준으로 계산한다.\n", "- 제작의 품질 적용 기본 공격력이 강화 성장의 시작점이다.\n- 제작 가치 배율은 강화 후 판매가 계산에 유지된다.\n- 공격력 증가는 고정 덧셈이 아니라 현재 강화 적용 공격력과 목표 구간을 기준으로 계산한다.\n")
replace_exact("docs/MVP-002_SCOPE.md", "- 이름·강화 단계·기본/강화/최종 공격력·판매가·누적 비용·손익·수식어·촉매·마감 품질 표시\n", "- 이름·강화 단계·원본/품질 적용/강화/최종 공격력·제작 가치 배율·판매가·누적 비용·손익·수식어·촉매·마감 품질 표시\n")
replace_exact("docs/MVP-002_SCOPE.md", "- 모델 테스트: `tests/unit/test_enhancement_session.gd`, `tests/unit/test_workshop_resources.gd`\n", "- 모델 테스트: `tests/unit/test_forging_session.gd`, `tests/unit/test_enhancement_session.gd`, `tests/unit/test_workshop_resources.gd`\n- 통합 테스트: `tests/integration/test_forging_quality_enhancement.gd`, `tests/integration/test_manual_enhancement_economy.gd`\n- 품질 계약 검사: `tests/check_forging_quality_contract.py`\n")
replace_exact("docs/MVP-002_SCOPE.md", "- [x] 수동·자동 강화가 동일한 골드·재료 거래를 사용하고 부족 시 판정을 시작하지 않는다.\n", "- [x] 수동·자동 강화가 동일한 골드·재료 거래를 사용하고 부족 시 판정을 시작하지 않는다.\n- [x] 제작 품질의 공격력·가치 효과가 강화·보관까지 유지된다.\n- [x] 반복 자동 단조의 새 철검은 보통 마감으로 시작한다.\n")

replace_exact("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", "수동·자동 강화 경제 통합을 완료했으며, 다음 단계에서 제작 마감 품질을 실제 무기 성능·가치에 연결한다.", "제작 마감 품질을 실제 무기 성능·가치에 연결하고 검증 중이며, 다음 단계는 제작 피버 결과 보너스다.")
replace_exact("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", "- 버전 표시: `POC v0.6.1 · main · 2026.07.22.1`\n- 제작: 광클·자동 작업·피버·선택적 정밀 마감 구현\n", "- 버전 표시: `POC v0.6.2 · main · 2026.07.22.2`\n- 제작: 광클·자동 작업·피버·선택적 정밀 마감 구현\n- 제작 품질: 보통 공격력/가치 ×1.00, 좋음 ×1.05/×1.05, 완벽 ×1.10/×1.12\n- 품질 전달: 원본 공격력·품질 적용 공격력·가치 배율을 강화와 보관까지 유지\n- 자동 반복 품질: 새 철검은 보통 마감으로 시작해 최초 수동 품질을 복제하지 않음\n")
replace_exact("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", "- 공유 경제 자동 검증: 단위 7건·실제 강화 UI 통합 2건 PASS\n- Godot 자동 검증: 4.7.1 import·parse, 강화 Scene, 제작·강화·공유 경제 모델, UI 통합, JSON PASS\n", "- 공유 경제 자동 검증: 단위 7건·실제 강화 UI 통합 2건 PASS\n- 제작 품질 자동 검증: 제작 모델 5건·제작→강화·보관 통합 2건·정적 계약 검사\n- Godot 자동 검증: 4.7.1 import·parse, 강화 Scene, 제작·강화·공유 경제·품질 모델, UI 통합, JSON PASS\n")
replace_exact("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", "- 테스트: `tests/unit/test_enhancement_session.gd`, `tests/unit/test_forging_session.gd`, `tests/unit/test_workshop_resources.gd`, `tests/integration/test_manual_enhancement_economy.gd`\n", "- 테스트: `tests/unit/test_enhancement_session.gd`, `tests/unit/test_forging_session.gd`, `tests/unit/test_workshop_resources.gd`, `tests/integration/test_manual_enhancement_economy.gd`, `tests/integration/test_forging_quality_enhancement.gd`, `tests/check_forging_quality_contract.py`\n")
replace_exact("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", "1. 제작의 좋은·완벽한 마감 품질을 실제 기본 공격력·판매 가치에 연결한다.\n2. 제작 피버가 무기 결과에 남기는 작은 보너스를 설계·검증한다.\n3. 강화 데이터의 중복 실패 정책을 제거하고 의미 검증을 강화한다.\n4. 위험·가격 곡선을 시뮬레이션으로 조정한다.\n5. 방문 검투사 판매를 구현한다.\n", "1. 제작 마감 품질의 공격력·가치 반영을 PR 검증·병합하고 main을 재확인한다.\n2. 제작 피버가 무기 결과에 남기는 작은 보너스를 설계·검증한다.\n3. 강화 데이터의 중복 실패 정책을 제거하고 의미 검증을 강화한다.\n4. 위험·가격 곡선을 시뮬레이션으로 조정한다.\n5. 방문 검투사 판매를 구현한다.\n")
replace_exact("[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md", "- 제작 품질 배율의 실제 공격력·판매가 반영\n", "- 제작 품질 효과의 실제 사람 화면·체감 검수\n")

replace_exact("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md", "| Implementation | PASS | 공유 경제 거래·수동/자동 소비자·단위/통합 테스트·문서 구현 |\n| Verification | CURRENT | 자동 검증 PASS, 실제 화면·Android·장시간 성능 증거 필요 |\n| Documentation | PASS | Active Context·Roadmap·Scope·플레이테스트·스크립트/테스트 안내 동기화 |\n| Integration·Completion | PASS | PR #18 최종 patch·리뷰·squash 병합과 main 핵심 파일 재확인 |\n", "| Implementation | PASS | 공유 경제와 제작 품질의 도메인·UI·데이터·단위/통합/정적 테스트 구현 |\n| Verification | CURRENT | 자동 검증 진행, 실제 화면·Android·장시간 성능 증거 필요 |\n| Documentation | PASS | Game Bible·Decision Log·Active Context·Roadmap·Scope·플레이테스트·README 동기화 |\n| Integration·Completion | CURRENT | PR #20 전체 patch·CI·리뷰·병합과 main 재확인 |\n")
replace_exact("[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md", "- [ ] 마감 품질의 실제 기본 공격력·판매 가치 반영\n", "- [x] 마감 품질의 실제 기본 공격력·판매 가치 반영\n- [x] 원본 공격력·품질 적용 공격력·가치 배율의 강화·보관 전달\n- [x] 반복 자동 단조의 새 철검 보통 마감 고정\n- [x] 제작 모델 5건·제작 품질 통합 2건·정적 품질 계약 검사\n")

replace_exact("[기획서]/00_프로젝트_허브/ROADMAP.md", "남음:\n- 제작 품질을 실제 기본 공격력·판매 가치에 연결\n- 제작 피버가 무기 결과에 남기는 작은 보너스 설계\n", "완료:\n- 보통·좋음·완벽 마감의 공격력·제작 가치 효과 연결\n- 원본 공격력·품질 적용 공격력·가치 배율의 강화·보관 전달\n- 반복 자동 단조의 새 철검 보통 마감 고정\n\n남음:\n- 제작 피버가 무기 결과에 남기는 작은 보너스 설계\n")
replace_exact("[기획서]/00_프로젝트_허브/ROADMAP.md", "1. 수동·자동 강화 경제 통합 — 구현 완료, 최종 PR 검증 중\n2. 제작 품질의 실제 공격력·가치 반영\n3. 제작 피버 결과 보너스\n4. 강화 실패 정책 정본 통합과 데이터 의미 검증\n5. 위험·가격 곡선 시뮬레이션과 조정\n", "1. 수동·자동 강화 경제 통합 — 완료·main 병합\n2. 제작 품질의 실제 공격력·가치 반영 — 구현 완료·PR 검증 중\n3. 제작 피버 결과 보너스 — NEXT\n4. 강화 실패 정책 정본 통합과 데이터 의미 검증\n5. 위험·가격 곡선 시뮬레이션과 조정\n")

replace_exact("docs/GODOT_PLAYTEST.md", "## 강화 분류\n", '''## 제작 품질 확인\n\n- 화면 버전이 `POC v0.6.2 · main · 2026.07.22.2`인지 확인한다.\n- 보통 마감: 원본 공격력 10 → 품질 적용 10, 제작 가치 ×1.00\n- 좋은 마감: 원본 공격력 10 → 품질 적용 11(반올림), 제작 가치 ×1.05\n- 완벽한 마감: 원본 공격력 10 → 품질 적용 11, 제작 가치 ×1.12\n- 강화 화면과 보관함에서 원본 공격력·품질 적용 공격력·가치 배율이 유지되는가\n- 반복 자동 단조의 두 번째 무기부터는 보통 마감으로 시작하는가\n\n## 강화 분류\n''')
replace_exact("docs/GODOT_PLAYTEST.md", "- 화면 버전이 `POC v0.6.1 · main · 2026.07.22.1`인지 확인한다.\n", "")

replace_exact("tests/README.md", "python tools/audit_project_operating_system.py --base-root <Base checkout>\n", "python tools/audit_project_operating_system.py --base-root <Base checkout>\npython tests/check_forging_quality_contract.py\n")
replace_exact("tests/README.md", "godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd\n", "godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd\ngodot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd\n")
replace_exact("tests/README.md", "- 제작 진행도·피버·정밀 마감·초기화\n", "- 제작 진행도·피버·정밀 마감·초기화\n- 보통·좋음·완벽 마감의 공격력·가치 배율과 제작→강화→보관 전달\n- 구형 단일 품질 배율·기본 공격력 덮어쓰기·옛 버전 재등장 차단\n")

replace_exact("scripts/README.md", "├─ forging/       # 제작 진행도·터치·피버·마감 상태\n", "├─ forging/       # 제작 진행도·터치·피버·마감 품질·원본/적용 공격력 상태\n")
replace_exact("scripts/README.md", "- 게임 규칙은 `forging/`과 `enhancement/`의 상태 모델이 소유한다.\n", "- 게임 규칙은 `forging/`과 `enhancement/`의 상태 모델이 소유한다.\n- 제작 품질은 `quality_attack_multiplier`와 `quality_value_multiplier`로 분리하며 구형 단일 배율을 사용하지 않는다.\n- 원본 기본 공격력과 품질 적용 기본 공격력을 별도로 보존하고 강화·보관 소비자에 전달한다.\n")

replace_exact("README.md", "- 완벽·좋음·보통 마감\n", "- 완벽·좋음·보통 마감\n- 보통 공격력/가치 ×1.00, 좋음 ×1.05/×1.05, 완벽 ×1.10/×1.12\n- 원본 공격력과 품질 적용 공격력을 강화·보관까지 유지\n")
replace_exact("README.md", "- 공격력·판매가·누적 비용·수식어·촉매·마감 품질 확인\n", "- 원본/품질 적용/강화/최종 공격력·제작 가치·판매가·누적 비용·수식어·촉매·마감 품질 확인\n")
replace_exact("README.md", "python tools/validate_game_data.py\n", "python tools/validate_game_data.py\npython tests/check_forging_quality_contract.py\n")
replace_exact("README.md", "godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd\n", "godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd\ngodot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd\n")

replace_exact("[기획서]/00_프로젝트_허브/CHANGELOG.md", "# Changelog\n\n", '''# Changelog\n\n## 2026-07-22 — POC v0.6.2 제작 마감 품질 효과\n\n- 보통·좋음·완벽 마감의 공격력·제작 가치 배율을 분리\n- 원본 기본 공격력과 품질 적용 기본 공격력을 강화·보관까지 전달\n- 강화 판매가에 제작 가치 배율 유지\n- 반복 자동 단조의 새 철검을 보통 마감으로 고정\n- 구형 단일 품질 배율 필드와 기본 공격력 덮어쓰기 제거\n- 제작 모델 5건·제작→강화·보관 통합 2건·정적 품질 계약 검사 추가\n\n## 2026-07-22 — POC v0.6.1 공유 강화 경제\n\n- 수동 강화와 자동 단조가 동일 골드·재료 거래를 사용\n- 수동 일반·특수 강화 실제 비용과 재료 차감\n- 골드·선택 재료 부족 시 무차감·무판정 차단\n- 자동 단조 재료 소진 fallback과 정밀 판정 선택 동기화\n- 공유 경제 단위 7건·실제 강화 UI 통합 2건 추가\n\n''')

replace_exact("skills/SKILL_LEARNING_LOG.md", "- 미검증: Android 실기기·AAB·사람 시각·접근성·성능 프로파일·Branch protection 강제 여부\n", '''- 미검증: Android 실기기·AAB·사람 시각·접근성·성능 프로파일·Branch protection 강제 여부\n\n## 2026-07-22 — 제작 품질 계약과 Workflow 보안 경계\n\n- 요청: 제작 마감 품질을 실제 공격력·가치에 연결하고 구형 소비자와 문서 drift를 제거한다.\n- 게임 디자인: 강화가 복리 성장하므로 GOOD/PERFECT 공격력 배율을 1.05/1.10으로 제한하고 가치 배율을 1.05/1.12로 분리했다.\n- 엔지니어링: 원본 공격력·품질 적용 공격력·가치 배율을 제작→강화→보관 계약으로 전달하고 자동 반복은 보통 마감으로 초기화했다.\n- QA: 구형 단일 품질 배율, 기본 공격력 덮어쓰기, 옛 버전 문구를 정적 계약 검사로 차단했다.\n- 실패와 수정: GitHub Actions bot 커밋에 Workflow 변경이 포함되면 push 권한 경계에서 막힐 수 있어, 자동 적용 커밋에서는 Workflow를 main 상태로 복원하고 Workflow 변경은 GitHub API 커밋으로 분리했다.\n- 교훈: 기능 파일 자동 적용과 Workflow 정책 변경을 한 bot 커밋에 섞지 않고, 최종 Head에서 두 검증을 다시 실행한다.\n- 미검증: 실제 사람 화면·Android·접근성·성능\n''')

checker = r'''from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def text(rel: str) -> str:
    path = ROOT / rel
    require(path.is_file(), f"필수 파일 누락: {rel}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


balance = json.loads(text("data/crafting/forging_balance.json"))
session = balance.get("session", {})
expected = {
    "weapon_base_attack": 10,
    "quality_standard_attack_multiplier": 1.0,
    "quality_standard_value_multiplier": 1.0,
    "quality_good_attack_multiplier": 1.05,
    "quality_good_value_multiplier": 1.05,
    "quality_perfect_attack_multiplier": 1.10,
    "quality_perfect_value_multiplier": 1.12,
}
for key, value in expected.items():
    require(session.get(key) == value, f"forging_balance.json {key}는 {value}여야 합니다.")

source_files = list((ROOT / "scripts").rglob("*.gd")) + list((ROOT / "tests").rglob("*.gd"))
for path in source_files:
    source = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    require('"quality_multiplier"' not in source, f"구형 단일 품질 배율 필드가 남아 있습니다: {rel}")
    require('weapon_result["base_attack"] = 10' not in source, f"제작 결과 기본 공격력 덮어쓰기가 남아 있습니다: {rel}")

for rel in ["scripts/ui/game_flow_screen.gd", "scripts/ui/enhancement_test_runner.gd"]:
    source = text(rel)
    require('POC v0.6.2 · main · 2026.07.22.2' in source, f"최신 버전 배지가 없습니다: {rel}")
    require('POC v0.6.1 · main · 2026.07.22.1' not in source, f"구형 버전 배지가 남아 있습니다: {rel}")

for rel in [
    "[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md",
    "docs/MVP-001_SCOPE.md",
    "docs/MVP-002_SCOPE.md",
    "docs/GODOT_PLAYTEST.md",
]:
    source = text(rel)
    require("×1.05" in source and "×1.12" in source, f"품질 공격력·가치 계약이 문서에 없습니다: {rel}")

workflow = text(".github/workflows/godot-validation.yml")
require("test_forging_quality_enhancement.gd" in workflow, "Godot Workflow에 제작 품질 통합 테스트가 없습니다.")
require("check_forging_quality_contract.py" in workflow, "Godot Workflow에 품질 정적 계약 검사가 없습니다.")

if FAILURES:
    for failure in FAILURES:
        print(f"ERROR: {failure}")
    raise SystemExit(1)

print("Forging quality contract PASSED")
'''
write("tests/check_forging_quality_contract.py", checker)

print("Forging quality finalization patch applied")
