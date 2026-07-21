# Active Context

## 현재 목표

`MVP-001 제작 터치`와 `MVP-002 +5 강화·첫 수식어`를 연결해, 철검을 만들고 재료를 선택해 +5까지 강화한 뒤 첫 수식어를 얻는 짧은 모바일 성장 사이클을 검증한다.

## 현재 상태

- 제품 단계: Prototype
- 작업 게이트: Verification
- 구현 상태: 철검 제작과 +5 강화·첫 수식어 수직 프로토타입 구현
- 자동 검증: JSON PASS, Godot 프로젝트 파싱 PASS, 제작 모델 4건 PASS, 강화 모델 5건 PASS
- 모바일 검증: 실제 화면 렌더·Android 실기기 미실행

## 구현된 범위

### MVP-001 제작

- `scripts/forging/forging_session.gd`: 제작·피버·마감 상태 계산
- `scripts/ui/forging_screen.gd`: 모바일 중심 제작 UI와 입력
- `data/crafting/forging_balance.json`: 제작 수치
- `tests/unit/test_forging_session.gd`: 제작 모델 테스트

### MVP-002 강화

- `scripts/enhancement/enhancement_session.gd`: +0~+5 강화·확률·실패 보정·재료 누적·수식어 판정
- `scripts/ui/enhancement_screen.gd`: 재료·촉매 선택과 정밀 강화 모바일 UI
- `scripts/ui/game_flow_screen.gd`: 제작 완료 후 강화 진입과 새 제작 복귀
- `data/crafting/enhancement_balance.json`: 단계별 성공률과 보정 수치
- `data/crafting/materials.json`: 숫돌·화염석·정령의 심장·살라맨더의 핵
- `tests/unit/test_enhancement_session.gd`: 강화 모델 5개 테스트
- `docs/MVP-002_SCOPE.md`: 범위·수치·완료 기준

### 공통 검증

- `scenes/main/main.tscn`: 제작→강화 게임 흐름 진입점
- `.github/workflows/godot-validation.yml`: Godot 4.7.1 파싱과 제작·강화 모델 테스트
- `tools/validate_game_data.py`: JSON 정적 검증

## 보호 결정

- 광클은 피로·과열 불이익이 아니라 피버 보상으로 이어진다.
- 정밀작업은 제작 마감과 강화에서 ON/OFF 가능하다.
- 기본 제작품인 철검에는 수식어가 붙지 않는다.
- 수식어는 +5에서 강화에 사용한 보조재료 성질 누적으로 결정한다.
- 강화 실패 시 단계 유지, 무기 파괴·수리 없음, 재료 소모와 성공률 보정만 발생한다.
- 촉매·정밀 판정·실패 보정의 합산 결과를 화면에 표시한다.
- 숨은 무기와 판매는 각각 후속 수직 범위로 분리한다.
- 직원과 무기 수리는 초기 범위에서 제외한다.

## 다음 우선순위

1. 제작·강화 화면을 실제로 렌더해 배치·텍스트·화면 전환을 시각 검수한다.
2. Android 기기에서 터치·스크롤·세로 비율·안전 영역을 확인한다.
3. 플레이 감각에 따라 제작·강화 밸런스 JSON을 조정한다.
4. `MVP-003 방문 검투사 판매 → 경기 결과 → 인센티브·명성`을 구현한다.

## 확인된 검증

- `python tools/validate_game_data.py`: PASS
- Godot 4.7.1 `--headless --editor --path . --quit`: PASS
- `tests/unit/test_forging_session.gd`: PASS — 제작 모델 4건
- `tests/unit/test_enhancement_session.gd`: PASS — 강화 모델 5건
- 정밀 강화 OFF 성공, 실패 단계 유지, 촉매·PERFECT 확률 합산, 성공 시 실패 보정 초기화, +5 화염 수식어 생성 확인

## 미검증

- 실제 화면 렌더와 광클·강화 플레이 감각
- Android SDK/JDK 및 export template
- API 36 대상 AAB 생성
- 실제 Android 기기 터치·스크롤·화면 안전 영역
- 장시간 방치 저장·복귀
- 기획서 PDF/DOCX 발행과 사람 시각 검수
