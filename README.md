# Blacksmith

Google Play 출시를 목표로 하는 Android 모바일용 방치형·클리커형 무기 제작·강화 게임 프로젝트입니다.

플레이어는 대장장이가 되어 재료를 조합해 무기를 만들고, 광클과 피버타임으로 제작을 가속합니다. +1~+9는 원클릭 일반 강화로 진행하며, +10·+20·…·+100에서는 보조재료·촉매·정밀 판정을 사용하는 `[특수 강화]`를 수행합니다.

## 현재 구현

### MVP-001 제작

```text
철 고정 → 광클·자동 작업 → 피버 → 선택적 정밀 마감 → 철검 완성
```

- 터치·자동 작업 진행
- 빠른 연속 터치로 피버 발동
- 피버 중 터치·자동 작업 배율
- 정밀 마감 ON/OFF
- 완벽·좋음·보통 마감 판정

### +100 강화 테스트

```text
철검 → +1~+9 원클릭 일반 강화 → +10 특수 강화 → 반복 → +100
```

- 최대 강화: +100
- 일반 강화: +10 단위가 아닌 모든 단계, 원클릭 즉시 판정
- 특수 강화: +10·+20·+30·…·+100
- 특수 강화에서만 보조재료·촉매 선택과 정밀 판정 적용
- 일반 강화에서는 이전에 선택했던 보조재료·촉매 효과가 적용되지 않음
- 실패 시 단계 유지·무기 파괴 없음
- 실패당 다음 시도 성공률 보정
- 성공률은 10단계 패턴을 반복하며 높은 구간일수록 점진적으로 감소

### +100 수식어 성장

- +10: 첫 수식어 1티어
- +20: 첫 수식어 2티어
- +30: 두 번째 수식어 1티어
- +40: 두 번째 수식어 2티어
- +50: 세 번째 수식어 1티어
- +60: 세 번째 수식어 2티어
- +70·+80·+90: 각 수식어 3티어
- +100: 모든 수식어 4티어

## Godot에서 바로 테스트

1. GitHub Desktop에서 `Fetch origin` 후 `Pull origin`을 누른다.
2. Godot 4.7.1로 `project.godot`을 연다.
3. `scenes/test/enhancement_test.tscn`을 열고 `F6`을 눌러 +0부터 +100까지 강화한다.

전체 제작→강화 흐름은 `scenes/main/main.tscn`에서 확인한다. 상세 안내는 `docs/GODOT_PLAYTEST.md`에 있다.

## 기술 기준

- Engine: Godot 4.7.1
- Language: GDScript
- Primary platform: Android mobile
- Distribution: Google Play
- Default orientation: Portrait 720×1280
- Store package: Android App Bundle (`.aab`)

## 시작 위치

1. `AGENTS.md`
2. `[기획서]/00_프로젝트_허브/START_HERE.md`
3. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
4. `docs/GODOT_PLAYTEST.md`
5. `docs/MVP-001_SCOPE.md`
6. `docs/MVP-002_SCOPE.md`

## 검증

```bash
python tools/validate_game_data.py
godot --headless --editor --path . --quit
godot --headless --path . res://scenes/test/enhancement_test.tscn --quit-after 2
godot --headless --path . --script res://tests/unit/test_forging_session.gd
godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
```

자동 검증을 통과한 뒤 실제 화면 렌더, 플레이 감각, Android 기기 터치와 AAB 배포를 별도로 검증합니다.
