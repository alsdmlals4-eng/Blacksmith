# Blacksmith

Google Play 출시를 목표로 하는 Android 모바일용 방치형·클리커형 무기 제작·강화 게임 프로젝트입니다.

플레이어는 대장장이가 되어 재료를 조합해 무기를 만들고, 광클과 피버타임으로 제작을 가속하며, 선택적 정밀작업으로 강화 성공률과 품질을 높입니다. 완성한 무기는 고객에게 직접 제공하거나 상인의 납품 의뢰로 판매합니다.

## 현재 구현

`MVP-001`에서 다음 제작 사이클을 구현했습니다.

```text
철 고정 → 광클·자동 작업 → 피버 → 선택적 정밀 마감 → 철검 완성 → 다시 제작
```

- 터치·자동 작업 진행
- 빠른 연속 터치로 피버 발동
- 피버 중 터치·자동 작업 배율
- 정밀 마감 ON/OFF
- 완벽·좋음·보통 마감 판정
- Godot 헤드리스 프로젝트 파싱과 제작 모델 테스트

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
4. `docs/MVP-001_SCOPE.md`

## 검증

```bash
python tools/validate_game_data.py
godot --headless --editor --path . --quit
godot --headless --path . --script res://tests/unit/test_forging_session.gd
```

자동 검증은 통과했습니다. 실제 화면 렌더, 플레이 감각, Android 기기 터치와 AAB 배포는 아직 검증 전입니다.
