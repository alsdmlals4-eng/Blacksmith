# Tests

현재 자동 검증은 JSON 데이터와 Godot 4.7.1 헤드리스 모델 테스트를 실행한다.

## 데이터 검증

```bash
python tools/validate_game_data.py
```

## Godot 모델 테스트

```bash
Godot --headless --path . --script res://tests/unit/test_forging_session.gd
Godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
```

현재 검증 범위:

- 제작 진행도와 피버 게이지
- 정밀 마감 ON/OFF와 완벽 판정
- 제작 세션 초기화
- 강화 성공과 실패
- 실패 시 단계 유지와 누적 성공 보정
- 촉매·정밀 강화 성공률 합산
- +5 재료 누적 수식어 생성

후속 테스트:

- 정밀작업 판정 경계값 전체
- +10 수식어 강화와 +15 두 번째 수식어
- 숨은 레시피 변환
- 고객 방문 인센티브
- 상인 납품 가격 계산
- 저장·방치 복귀
- Android 터치 입력과 화면 비율
