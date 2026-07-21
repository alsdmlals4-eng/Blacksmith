# Active Context

## 현재 목표

`MVP-001 제작 터치 수직 프로토타입`을 통해 Android 세로 화면에서 광클·피버·선택적 정밀 마감이 하나의 짧은 제작 사이클로 작동하는지 검증한다.

## 현재 상태

- 제품 단계: Prototype
- 작업 게이트: Verification
- 구현 상태: 철검 제작 수직 프로토타입 구현
- 자동 검증: JSON PASS, Godot 프로젝트 파싱 PASS, 제작 모델 테스트 PASS
- 모바일 검증: Android 실기기 미실행

## 구현된 범위

- `scenes/main/main.tscn`: 세로형 제작 화면 진입점
- `scripts/forging/forging_session.gd`: 제작·피버·마감 상태 계산
- `scripts/ui/forging_screen.gd`: 모바일 중심 제작 UI와 입력
- `scripts/ui/precision_gauge.gd`: 정밀 마감 타이밍 게이지
- `data/crafting/forging_balance.json`: MVP 제작 수치
- `tests/unit/test_forging_session.gd`: 제작 모델 단위 테스트
- `.github/workflows/godot-validation.yml`: Godot 4.7.1 헤드리스 파싱·테스트

## 보호 결정

- 광클은 피로·과열 불이익이 아니라 피버 보상으로 이어진다.
- 정밀작업은 강제하지 않고 ON/OFF 가능하다.
- 기본 제작품인 철검에는 수식어가 붙지 않는다.
- +5 강화와 수식어, 고객 판매는 다음 수직 범위로 분리한다.
- 직원과 무기 수리는 초기 범위에서 제외한다.
- 모바일 단순 조작과 빠른 세션을 우선한다.

## 다음 우선순위

1. 실제 Godot 화면을 실행해 배치·텍스트·상태 전환을 시각 검수한다.
2. Android 기기에서 터치·세로 비율·안전 영역을 확인한다.
3. 플레이 감각에 따라 `forging_balance.json`을 조정한다.
4. `MVP-002 +5 강화 → 첫 수식어` 범위를 설계한다.

## 확인된 검증

- `python tools/validate_game_data.py`: PASS
- Godot 4.7.1 엔진 다운로드: PASS
- `--headless --editor --path . --quit`: PASS — 프로젝트·Main Scene·참조 스크립트 파싱
- `tests/unit/test_forging_session.gd`: PASS — 정밀 OFF, 피버 배율, 완벽 마감, 초기화 4건

## 미검증

- 실제 화면 렌더와 플레이 감각
- Android SDK/JDK 및 export template
- API 36 대상 AAB 생성
- 실제 Android 기기 터치·화면 안전 영역
- 장시간 방치 저장·복귀
