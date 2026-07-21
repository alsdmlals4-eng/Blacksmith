# Blacksmith

Google Play 출시를 목표로 하는 Android 모바일용 방치형·클리커형 무기 제작·강화 게임 프로젝트입니다.

플레이어는 대장장이가 되어 재료를 조합해 무기를 만들고, 광클과 피버타임으로 제작을 가속합니다. 일반 강화는 빠르게 원클릭으로 진행하고 수식어가 변화하는 이정표에서만 정밀 강화를 수행합니다.

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

### 강화 이정표 테스트

```text
철검 → 4단계 원클릭 강화 → 이정표 정밀 강화 → 수식어 변화 → +20
```

- +1~+4, +6~+9, +11~+14, +16~+19: 원클릭 즉시 판정
- +5: 첫 수식어 1티어 추가
- +10: 첫 수식어 2티어 강화
- +15: 두 번째 수식어 1티어 추가
- +20: 두 번째 수식어 2티어 강화
- 숫돌·화염석·정령의 심장 성질 누적
- 살라맨더의 핵 성공률 보너스
- 이정표 정밀 강화 GOOD·PERFECT 성공률 보너스
- 실패 시 단계 유지·무기 파괴 없음
- 실패당 다음 시도 성공률 보정

## Godot에서 바로 테스트

1. Godot 4.7.1로 `project.godot`을 연다.
2. `scenes/test/enhancement_test.tscn`을 연다.
3. `F6`을 눌러 +0부터 +20까지 강화한다.

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

자동 검증은 통과했습니다. 실제 화면 렌더, 플레이 감각, Android 기기 터치와 AAB 배포는 아직 검증 전입니다.
