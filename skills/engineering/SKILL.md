# Blacksmith Engineering Skill

## Trigger
Godot, GDScript, Android, 저장, 데이터 로딩, 성능 또는 빌드 작업에 사용한다.

## Technical baseline
- Godot 4.7.1
- GDScript
- Android portrait
- 720×1280 base resolution
- `canvas_items` + `expand`
- Google Play AAB
- API 36 준비

## Rules
- 게임 규칙은 UI 애니메이션이 아니라 도메인 코드가 소유한다.
- JSON ID를 코드에 중복 하드코딩하지 않는다.
- 서명키와 export credentials를 커밋하지 않는다.
- 실제 기기에서 확인하지 않은 모바일 동작은 미검증으로 기록한다.

## Validation
- `python tools/validate_game_data.py`
- Godot headless or editor project load
- Android debug build
- 실제 기기 터치·화면 비율
